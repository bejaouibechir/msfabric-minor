"""Traite incrémentalement les lots capteurs avec Structured Streaming."""

from __future__ import annotations

import argparse
import logging
import time
import uuid
from typing import Any

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from capteurs_sjd_utils import REGLES_GRANDEURS, schema_entree


LOGGER = logging.getLogger("traitement_capteurs")
TABLE_MESURES = "mesures_capteurs_sjd"
TABLE_QUARANTAINE = "mesures_quarantaine_sjd"
TABLE_AUDIT = "journal_runs_sjd"
CLÉS_MÉTIER = ("capteur_id", "timestamp", "grandeur")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--landing-path", default="Files/landing_capteurs")
    parser.add_argument("--checkpoint-path", default="Files/checkpoints/sjd2_capteurs")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--max-files-per-trigger", type=int, default=100)
    parser.add_argument("--fail-after-batch", type=int, default=None)
    args = parser.parse_args()
    if args.max_files_per_trigger < 1:
        parser.error("--max-files-per-trigger doit être supérieur ou égal à 1")
    return args


def _condition_merge(cles: tuple[str, ...]) -> str:
    return " AND ".join(f"cible.`{col}` <=> source.`{col}`" for col in cles)


def _fusionner(spark: SparkSession, df: DataFrame, table: str, cles: tuple[str, ...]) -> None:
    source = df.dropDuplicates(list(cles))
    if spark.catalog.tableExists(table):
        (DeltaTable.forName(spark, table).alias("cible")
         .merge(source.alias("source"), _condition_merge(cles))
         .whenMatchedUpdateAll()
         .whenNotMatchedInsertAll()
         .execute())
    else:
        source.write.format("delta").mode("errorifexists").saveAsTable(table)


def _enrichir_batch(df: DataFrame) -> DataFrame:
    timestamp_normalise = F.coalesce(
        F.to_timestamp("timestamp", "yyyy-MM-dd'T'HH:mm:ssX"),
        F.to_timestamp("timestamp", "dd/MM/yyyy HH:mm:ss"),
    )
    source_fichier = F.input_file_name()
    lot_id = F.regexp_extract(source_fichier, r"(lot\d{3})", 1)
    base = (df
            .withColumn("timestamp_normalise", timestamp_normalise)
            .withColumn("source_fichier", source_fichier)
            .withColumn("lot_id", lot_id)
            .withColumn("ingested_at", F.current_timestamp()))

    fenetre = Window.partitionBy("capteur_id", "timestamp_normalise", "grandeur").orderBy(
        "source_fichier", F.monotonically_increasing_id()
    )
    base = base.withColumn("rang_doublon", F.row_number().over(fenetre))

    null_requis = F.lit(False)
    for colonne in ("capteur_id", "site_id", "timestamp", "grandeur", "valeur", "unite"):
        null_requis = null_requis | F.col(colonne).isNull()

    hors_plage = F.lit(False)
    unite_invalide = F.lit(False)
    grandeur_connue = F.col("grandeur").isin(list(REGLES_GRANDEURS))
    for grandeur, (minimum, maximum, unite) in REGLES_GRANDEURS.items():
        est_grandeur = F.col("grandeur") == F.lit(grandeur)
        hors_plage = hors_plage | (est_grandeur & ~F.col("valeur").between(minimum, maximum))
        unite_invalide = unite_invalide | (est_grandeur & (F.col("unite") != F.lit(unite)))

    motifs = F.array_compact(F.array(
        F.when(null_requis, F.lit("VALEUR_NULLE")),
        F.when(F.col("timestamp").isNotNull() & F.col("timestamp_normalise").isNull(), F.lit("TIMESTAMP_INVALIDE")),
        F.when(F.col("grandeur").isNotNull() & ~grandeur_connue, F.lit("GRANDEUR_INCONNUE")),
        F.when(unite_invalide, F.lit("UNITE_INVALIDE")),
        F.when(hors_plage, F.lit("HORS_PLAGE")),
        F.when(F.col("rang_doublon") > 1, F.lit("DOUBLON")),
    ))
    return base.withColumn("motifs_rejet", motifs)


def _ecrire_audit(spark: SparkSession, ligne: dict[str, Any]) -> None:
    audit = spark.createDataFrame([ligne])
    _fusionner(spark, audit, TABLE_AUDIT, ("run_id", "micro_batch_id"))


def executer_stream(spark: SparkSession, args: argparse.Namespace) -> None:
    run_id = args.run_id or str(uuid.uuid4())
    etat = {"batches": 0}

    def traiter_batch(batch_df: DataFrame, batch_id: int) -> None:
        debut = time.monotonic()
        enrichi = _enrichir_batch(batch_df).persist()
        try:
            lignes_lues = enrichi.count()
            valides = enrichi.filter(F.size("motifs_rejet") == 0)
            rejetees = enrichi.filter(F.size("motifs_rejet") > 0)
            lignes_valides = valides.count()
            lignes_rejetees = rejetees.count()

            cible = valides.select(
                "capteur_id", "site_id",
                F.col("timestamp_normalise").alias("timestamp"),
                "grandeur", "valeur", "unite", "qualite",
                "ingested_at", "source_fichier", "lot_id",
            )
            quarantaine = (rejetees
                .withColumn("motif_rejet", F.concat_ws("|", "motifs_rejet"))
                .withColumn("rejet_id", F.sha2(F.concat_ws("||",
                    F.coalesce("source_fichier", F.lit("")),
                    F.coalesce("capteur_id", F.lit("")),
                    F.coalesce("timestamp", F.lit("")),
                    F.coalesce("grandeur", F.lit("")),
                    F.col("rang_doublon").cast("string")), 256))
                .select("rejet_id", "capteur_id", "site_id", "timestamp", "grandeur",
                        "valeur", "unite", "qualite", "motif_rejet", "ingested_at",
                        "source_fichier", "lot_id"))

            if lignes_valides:
                _fusionner(spark, cible, TABLE_MESURES, CLÉS_MÉTIER)
            if lignes_rejetees:
                _fusionner(spark, quarantaine, TABLE_QUARANTAINE, ("rejet_id",))

            lots = ",".join(
                ligne["lot_id"] for ligne in enrichi.select("lot_id").distinct().collect()
                if ligne["lot_id"]
            )
            _ecrire_audit(spark, {
                "run_id": run_id,
                "micro_batch_id": int(batch_id),
                "lots": lots,
                "lignes_lues": lignes_lues,
                "lignes_ecrites": lignes_valides,
                "lignes_rejetees": lignes_rejetees,
                "duree_secondes": round(time.monotonic() - debut, 3),
            })
            etat["batches"] += 1
            LOGGER.info("batch=%s lues=%s écrites=%s rejetées=%s", batch_id, lignes_lues, lignes_valides, lignes_rejetees)
            if args.fail_after_batch is not None and batch_id >= args.fail_after_batch:
                raise RuntimeError("Panne simulée demandée par --fail-after-batch")
        finally:
            enrichi.unpersist()

    flux = (spark.readStream
            .schema(schema_entree())
            .option("maxFilesPerTrigger", args.max_files_per_trigger)
            .json(args.landing_path))
    requete = (flux.writeStream
               .queryName("sjd2-capteurs-available-now")
               .foreachBatch(traiter_batch)
               .option("checkpointLocation", args.checkpoint_path)
               .trigger(availableNow=True)
               .start())
    requete.awaitTermination()

    if etat["batches"] == 0:
        _ecrire_audit(spark, {
            "run_id": run_id,
            "micro_batch_id": -1,
            "lots": "",
            "lignes_lues": 0,
            "lignes_ecrites": 0,
            "lignes_rejetees": 0,
            "duree_secondes": 0.0,
        })
        LOGGER.info("Aucun nouveau fichier à traiter")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    args = arguments()
    spark = SparkSession.builder.appName("SJD2_Traitement_Capteurs").getOrCreate()
    try:
        executer_stream(spark, args)
    except Exception:
        LOGGER.exception("Échec du traitement incrémental")
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()

