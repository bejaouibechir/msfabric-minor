"""analyse_sites.py — Contrôle qualité des mesures de consommation (Atelier 1).

Usage :
    python analyse_sites.py --input data/consommation_echantillon.csv
    python analyse_sites.py -i data/consommation_echantillon.csv --seuil 0.05 --json
"""
import argparse
import json
import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path

from energie_utils import (TimestampInvalide, convertir_mesure, lire_csv,
                           parse_timestamp, qualifier_mesure)

log = logging.getLogger("analyse_sites")


def compter(chemin_mesures: Path) -> dict:
    """Parcourt le fichier : états par site, somme des valeurs valides, doublons."""
    vues = set()
    qualite = defaultdict(Counter)
    somme_mw = defaultdict(float)
    doublons = horodatages_invalides = 0

    for ligne in lire_csv(chemin_mesures):
        cle = tuple(ligne.values())
        if cle in vues:                       # doublon exact : on l'écarte
            doublons += 1
            continue
        vues.add(cle)

        try:
            parse_timestamp(ligne["timestamp"])
        except TimestampInvalide:
            horodatages_invalides += 1

        etat = qualifier_mesure(convertir_mesure(ligne["consumption_mw"]))
        qualite[ligne["site_id"]][etat] += 1
        if etat == "VALIDE":
            somme_mw[ligne["site_id"]] += float(ligne["consumption_mw"])

    return {"qualite": qualite, "somme_mw": somme_mw, "doublons": doublons,
            "horodatages_invalides": horodatages_invalides}


def analyser(chemin_mesures: Path, chemin_sites: Path) -> dict:
    """Calcule les indicateurs qualité et charge par site."""
    sites = {s["site_id"]: s for s in lire_csv(chemin_sites)}
    brut = compter(chemin_mesures)

    par_site = {}
    for site_id, compteur in sorted(brut["qualite"].items()):
        total = sum(compteur.values())
        valides = compteur["VALIDE"]
        conso_moyenne = brut["somme_mw"][site_id] / valides if valides else 0.0
        capacite = float(sites[site_id]["capacity_mw"])
        par_site[site_id] = {
            "mesures": total,
            "valides": valides,
            "manquantes": compteur["MANQUANTE"],
            "codes_erreur": compteur["CODE_ERREUR"],
            "taux_anomalies": round((total - valides) / total, 3),
            "conso_moyenne_mw": round(conso_moyenne, 3),
            "taux_charge_moyen": round(conso_moyenne / capacite, 3),
        }

    total = sum(s["mesures"] for s in par_site.values())
    anomalies = sum(s["mesures"] - s["valides"] for s in par_site.values())
    return {
        "sites": par_site,
        "doublons_ecartes": brut["doublons"],
        "horodatages_invalides": brut["horodatages_invalides"],
        "taux_anomalies_global": round(anomalies / total, 3),
    }
