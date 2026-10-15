"""Schémas, conversions et métadonnées des jeux d'énergie de l'atelier SJD."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Iterable, Mapping


DATASETS: dict[str, dict[str, Any]] = {
    "besoins": {
        "endpoint": "besoins",
        "file": "besoins.json",
        "table": "besoins_energetiques_sjd",
        "key": ("Timestamp", "Zone"),
        "columns": (("Timestamp", "timestamp"), ("Zone", "string"),
                    ("Consommation_kWh", "double"), ("Type_Energie", "string"),
                    ("Cout_Euro", "double")),
    },
    "production-solaire": {
        "endpoint": "production-solaire",
        "file": "production-solaire.json",
        "table": "production_solaire_sjd",
        "key": ("PanneauID", "Date"),
        "columns": (("PanneauID", "string"), ("Date", "date"),
                    ("Zone_Installation", "string"), ("Production_kWh", "double"),
                    ("Ensoleillement_Heures", "double"), ("Rendement_Pct", "double")),
    },
    "production-eolienne": {
        "endpoint": "production-eolienne",
        "file": "production-eolienne.json",
        "table": "production_eolienne_sjd",
        "key": ("TurbineID", "Timestamp"),
        "columns": (("TurbineID", "string"), ("Timestamp", "timestamp"),
                    ("Vitesse_Vent_ms", "double"), ("Production_kWh", "double"),
                    ("Statut", "string")),
    },
}


def dataset_config(dataset: str) -> dict[str, Any]:
    """Retourne la configuration ou lève une erreur explicite."""
    try:
        return DATASETS[dataset]
    except KeyError as exc:
        raise ValueError(f"Jeu inconnu: {dataset}. Valeurs: {', '.join(DATASETS)}") from exc


def _convertir(valeur: Any, type_cible: str) -> Any:
    if valeur is None:
        return None
    if type_cible == "double":
        return float(valeur)
    if type_cible == "timestamp":
        return datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))
    if type_cible == "date":
        return date.fromisoformat(str(valeur))
    return str(valeur)


def convertir_enregistrement(dataset: str, ligne: Mapping[str, Any]) -> dict[str, Any]:
    """Conversion Python pure, testable localement sans PySpark."""
    config = dataset_config(dataset)
    attendues = {nom for nom, _ in config["columns"]}
    manquantes = attendues.difference(ligne)
    if manquantes:
        raise ValueError(f"Colonnes manquantes pour {dataset}: {sorted(manquantes)}")
    return {nom: _convertir(ligne[nom], type_cible) for nom, type_cible in config["columns"]}


def cle_metier(dataset: str, ligne: Mapping[str, Any]) -> tuple[Any, ...]:
    """Construit la clé composite documentée du jeu."""
    config = dataset_config(dataset)
    return tuple(ligne[nom] for nom in config["key"])


def compter_cles_dupliquees(dataset: str, lignes: Iterable[Mapping[str, Any]]) -> int:
    vues: set[tuple[Any, ...]] = set()
    doublons = 0
    for ligne in lignes:
        cle = cle_metier(dataset, ligne)
        if cle in vues:
            doublons += 1
        vues.add(cle)
    return doublons


def schema_brut(dataset: str):
    """Construit le StructType d'entrée avec les dates encore sous forme de texte."""
    from pyspark.sql.types import DoubleType, StringType, StructField, StructType

    champs = []
    for nom, type_cible in dataset_config(dataset)["columns"]:
        type_spark = DoubleType() if type_cible == "double" else StringType()
        champs.append(StructField(nom, type_spark, True))
    return StructType(champs)


def typer_dataframe(df, dataset: str, source: str):
    """Applique les types cibles et ajoute les deux colonnes techniques."""
    from pyspark.sql import functions as F

    config = dataset_config(dataset)
    expressions = []
    for nom, type_cible in config["columns"]:
        expressions.append(F.col(nom).cast(type_cible).alias(nom))
    return (df.select(*expressions)
              .withColumn("ingested_at", F.current_timestamp())
              .withColumn("source", F.lit(source)))
