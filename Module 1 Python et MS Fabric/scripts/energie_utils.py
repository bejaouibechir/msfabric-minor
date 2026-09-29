"""energie_utils.py — Utilitaires de qualité de données du réseau EnergiaNord."""
import csv
from datetime import datetime
from types import MappingProxyType
from typing import Iterator

CODES_ERREUR = MappingProxyType({
    -999: "Capteur hors service",
    -888: "Valeur non transmise",
    -777: "Recalibrage en cours",
})

FORMATS_TIMESTAMP = (
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
)


class TimestampInvalide(ValueError):
    """Levée quand un timestamp ne correspond à aucun format connu."""


def parse_timestamp(texte: str) -> datetime:
    """Convertit un timestamp texte (3 formats possibles) en datetime."""
    for fmt in FORMATS_TIMESTAMP:
        try:
            return datetime.strptime(texte.strip(), fmt)
        except ValueError:
            continue
    raise TimestampInvalide(f"Format inconnu : {texte!r}")


def convertir_mesure(texte: str) -> float | None:
    """'' -> None ; '0.865' -> 0.865 ; '-999' -> -999.0"""
    texte = texte.strip()
    if texte == "":
        return None
    return float(texte)


def qualifier_mesure(valeur: float | None) -> str:
    """Classe une mesure : MANQUANTE, CODE_ERREUR, NEGATIVE ou VALIDE."""
    match valeur:
        case None:
            return "MANQUANTE"
        case v if v in CODES_ERREUR:
            return "CODE_ERREUR"
        case v if v < 0:
            return "NEGATIVE"
        case _:
            return "VALIDE"


def lire_csv(chemin) -> Iterator[dict]:
    """Lit un CSV (UTF-8 avec ou sans BOM) et produit un dictionnaire par ligne."""
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def est_code_erreur(valeur: float | None) -> bool:
    """Vrai si la valeur est un code d'erreur capteur."""
    return valeur in CODES_ERREUR
