"""Validation pure et schéma des mesures de capteurs de l'atelier SJD 2."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping


FORMATS_TIMESTAMP = ("%Y-%m-%dT%H:%M:%SZ", "%d/%m/%Y %H:%M:%S")

# Bornes pédagogiques cohérentes avec le générateur de l'atelier.
REGLES_GRANDEURS: dict[str, tuple[float, float, str]] = {
    "temperature": (-20.0, 80.0, "°C"),
    "irradiance": (0.0, 1500.0, "W/m2"),
    "vitesse_vent": (0.0, 60.0, "m/s"),
    "puissance": (0.0, 2000.0, "kW"),
}

CHAMPS_REQUIS = (
    "capteur_id",
    "site_id",
    "timestamp",
    "grandeur",
    "valeur",
    "unite",
    "qualite",
)


@dataclass(frozen=True)
class Validation:
    """Résultat déterministe de la validation d'une ligne."""

    ligne: dict[str, Any]
    timestamp_normalise: datetime | None
    motifs: tuple[str, ...]
    timestamp_heterogene: bool

    @property
    def valide(self) -> bool:
        return not self.motifs


def normaliser_timestamp(valeur: Any) -> tuple[datetime | None, bool]:
    """Retourne un instant UTC et indique si le second format a été utilisé."""
    if valeur is None or str(valeur).strip() == "":
        return None, False
    texte = str(valeur).strip()
    for index, format_timestamp in enumerate(FORMATS_TIMESTAMP):
        try:
            instant = datetime.strptime(texte, format_timestamp).replace(tzinfo=timezone.utc)
            return instant, index > 0
        except ValueError:
            continue
    return None, False


def cle_metier(ligne: Mapping[str, Any], timestamp_normalise: datetime | None) -> tuple[Any, ...]:
    """Construit la clé capteur + instant UTC + grandeur."""
    return ligne.get("capteur_id"), timestamp_normalise, ligne.get("grandeur")


def valider_ligne(ligne: Mapping[str, Any]) -> Validation:
    """Applique les règles unitaires sans dépendance à Spark."""
    copie = dict(ligne)
    motifs: list[str] = []
    timestamp_normalise, heterogene = normaliser_timestamp(copie.get("timestamp"))

    champs_absents = [champ for champ in CHAMPS_REQUIS if champ not in copie]
    if champs_absents:
        motifs.append("CHAMP_ABSENT")

    if any(copie.get(champ) in (None, "") for champ in ("capteur_id", "site_id", "timestamp", "grandeur", "valeur", "unite")):
        motifs.append("VALEUR_NULLE")

    if copie.get("timestamp") not in (None, "") and timestamp_normalise is None:
        motifs.append("TIMESTAMP_INVALIDE")

    grandeur = copie.get("grandeur")
    regle = REGLES_GRANDEURS.get(str(grandeur))
    if grandeur not in (None, "") and regle is None:
        motifs.append("GRANDEUR_INCONNUE")
    elif regle is not None:
        minimum, maximum, unite = regle
        if copie.get("unite") not in (None, "", unite):
            motifs.append("UNITE_INVALIDE")
        valeur = copie.get("valeur")
        if valeur not in (None, ""):
            try:
                mesure = float(valeur)
            except (TypeError, ValueError):
                motifs.append("VALEUR_NON_NUMERIQUE")
            else:
                if not minimum <= mesure <= maximum:
                    motifs.append("HORS_PLAGE")

    return Validation(copie, timestamp_normalise, tuple(dict.fromkeys(motifs)), heterogene)


def analyser_lignes(lignes: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Compte les validations et ajoute DOUBLON aux clés déjà rencontrées."""
    cles_vues: set[tuple[Any, ...]] = set()
    resultats: list[Validation] = []
    compteurs = {
        "lignes": 0,
        "valides": 0,
        "rejetees": 0,
        "nulls": 0,
        "valeurs_hors_plage": 0,
        "doublons": 0,
        "timestamps_heterogenes": 0,
    }

    for ligne in lignes:
        validation = valider_ligne(ligne)
        motifs = list(validation.motifs)
        cle = cle_metier(validation.ligne, validation.timestamp_normalise)
        if all(element is not None for element in cle):
            if cle in cles_vues:
                motifs.append("DOUBLON")
            cles_vues.add(cle)
        validation = Validation(
            validation.ligne,
            validation.timestamp_normalise,
            tuple(dict.fromkeys(motifs)),
            validation.timestamp_heterogene,
        )
        resultats.append(validation)
        compteurs["lignes"] += 1
        compteurs["timestamps_heterogenes"] += int(validation.timestamp_heterogene)
        compteurs["nulls"] += int("VALEUR_NULLE" in validation.motifs)
        compteurs["valeurs_hors_plage"] += int("HORS_PLAGE" in validation.motifs)
        compteurs["doublons"] += int("DOUBLON" in validation.motifs)
        compteurs["rejetees"] += int(not validation.valide)
        compteurs["valides"] += int(validation.valide)

    return {"compteurs": compteurs, "validations": resultats}


def schema_entree():
    """Construit le schéma Spark explicite du JSON Lines."""
    from pyspark.sql.types import DoubleType, StringType, StructField, StructType

    return StructType([
        StructField("capteur_id", StringType(), True),
        StructField("site_id", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("grandeur", StringType(), True),
        StructField("valeur", DoubleType(), True),
        StructField("unite", StringType(), True),
        StructField("qualite", StringType(), True),
    ])

