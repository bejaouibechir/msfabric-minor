"""Ingestion idempotente des données d'énergie vers trois tables Delta `_sjd`."""

from __future__ import annotations

import argparse
import logging
from typing import Any

from delta.tables import DeltaTable
from pyspark.sql import SparkSession

from energie_sjd_utils import DATASETS, dataset_config, schema_brut, typer_dataframe


LOGGER = logging.getLogger("ingestion_energie")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=("api", "files"), required=True)
    parser.add_argument("--base-url", help="URL racine de l'Azure Function, requise avec --source api")
    parser.add_argument("--dataset", choices=tuple(DATASETS), required=True)
    parser.add_argument("--landing-path", default="Files/landing_sjd")
    args = parser.parse_args()
    if args.source == "api" and not args.base_url:
        parser.error("--base-url est requis avec --source api")
    return args


def lire_api(spark: SparkSession, dataset: str, base_url: str):
    import requests

    config = dataset_config(dataset)
    url = f"{base_url.rstrip('/')}/api/{config['endpoint']}"
    LOGGER.info("Lecture de %s", url)
    reponse = requests.get(url, timeout=30)
    reponse.raise_for_status()
    contenu: Any = reponse.json()
    if not isinstance(contenu, list):
        raise ValueError("La réponse API doit être un tableau JSON racine")
    return spark.createDataFrame(contenu, schema=schema_brut(dataset))


def lire_fichier(spark: SparkSession, dataset: str, landing_path: str):
    config = dataset_config(dataset)
    chemin = f"{landing_path.rstrip('/')}/{config['file']}"
    LOGGER.info("Lecture de %s", chemin)
    return (spark.read.schema(schema_brut(dataset))
            .option("multiLine", "true").json(chemin))


def fusionner_delta(spark: SparkSession, df, dataset: str) -> int:
    config = dataset_config(dataset)
    table = config["table"]
    cles = tuple(config["key"])
    source = df.dropDuplicates(list(cles))
    conditions = " AND ".join(f"cible.`{nom}` <=> source.`{nom}`" for nom in cles)

    if spark.catalog.tableExists(table):
        (DeltaTable.forName(spark, table).alias("cible")
         .merge(source.alias("source"), conditions)
         .whenMatchedUpdateAll()
         .whenNotMatchedInsertAll()
         .execute())
    else:
        source.write.format("delta").mode("errorifexists").saveAsTable(table)
    return spark.table(table).count()


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    args = arguments()
    spark = SparkSession.builder.appName("SJD_Ingestion_Energie").getOrCreate()
    try:
        brut = (lire_api(spark, args.dataset, args.base_url)
                if args.source == "api"
                else lire_fichier(spark, args.dataset, args.landing_path))
        df = typer_dataframe(brut, args.dataset, args.source)
        config = dataset_config(args.dataset)
        invalides = df.filter(" OR ".join(f"`{c}` IS NULL" for c in config["key"])).count()
        if invalides:
            raise ValueError(f"{invalides} ligne(s) ont une clé métier incomplète")
        total = fusionner_delta(spark, df, args.dataset)
        LOGGER.info("Table %s prête: %d lignes", config["table"], total)
    except Exception:
        LOGGER.exception("Échec de l'ingestion du jeu %s", args.dataset)
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
