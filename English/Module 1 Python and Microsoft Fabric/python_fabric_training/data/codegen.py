"""
codegen.py — Génération des fichiers d'entrée de l'Workshop 1 (Module 1)

Produit deux fichiers CSV cohérents avec le Module 2 (mêmes 6 sites, mêmes anomalies) :
  - sites_reference.csv          : référentiel des 6 sites
  - consommation_echantillon.csv : 1 journée de mesures horaires (6 sites x 24 h)
                                   avec anomalies volontaires

Anomalies injectées (comme dans consumption_raw.csv du Module 2) :
  - formats de timestamp hétérogènes (ISO avec 'T', ISO avec espace, JJ/MM/AAAA)
  - codes erreur capteur : -999, -888, -777
  - valeurs manquantes (consumption_mw vide)
  - doublons exacts

Usage : python codegen.py
"""
import csv
import math
import random
from datetime import datetime, timedelta

random.seed(42)  # reproductibilité : mêmes données à chaque exécution

SITES = [
    # site_id, site_type, capacity_mw, flexible, baseline_mw, curtailment_price_eur_mwh, region
    ("SITE_IND_001", "Industrie",   5.0, True,  2.5,  102.0, "Ile-de-France"),
    ("SITE_IND_002", "Industrie",   3.5, True,  1.75, 116.0, "Auvergne-Rhone-Alpes"),
    ("SITE_COM_001", "Commercial",  2.0, False, 1.0,  None,  "Auvergne-Rhone-Alpes"),
    ("SITE_COM_002", "Commercial",  1.5, False, 0.75, None,  "Ile-de-France"),
    ("SITE_RES_001", "Residentiel", 0.8, True,  0.4,  None,  "Auvergne-Rhone-Alpes"),
    ("SITE_RES_002", "Residentiel", 0.6, True,  0.3,  None,  "Ile-de-France"),
]

JOUR = datetime(2025, 1, 3)


def profil_horaire(site_type: str, heure: int) -> float:
    """Coefficient de charge selon le type de site et l'heure (0.5 à 1.3)."""
    if site_type == "Industrie":
        return 1.2 if 6 <= heure <= 20 else 0.7
    if site_type == "Commercial":
        return 1.3 if 8 <= heure <= 19 else 0.5
    # Résidentiel : pics matin et soir
    return 1.3 if heure in (7, 8, 18, 19, 20, 21) else 0.8


def formater(ts: datetime, style: int) -> str:
    if style == 0:
        return ts.strftime("%Y-%m-%dT%H:%M:%S")
    if style == 1:
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    return ts.strftime("%d/%m/%Y %H:%M:%S")


def main() -> None:
    # --- Référentiel des sites -------------------------------------------------
    with open("sites_reference.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["site_id", "site_type", "capacity_mw", "flexible", "baseline_mw",
                    "curtailment_price_eur_mwh", "region"])
        for s in SITES:
            w.writerow(["" if v is None else v for v in s])

    # --- Mesures de consommation -----------------------------------------------
    lignes = []
    for site_id, site_type, cap, _flex, base, _prix, _reg in SITES:
        for h in range(24):
            ts = JOUR + timedelta(hours=h)
            conso = base * profil_horaire(site_type, h) * random.uniform(0.9, 1.1)
            conso = round(min(conso, cap), 3)
            tension = round(random.gauss(230, 4), 1)
            freq = round(random.gauss(50.0, 0.12), 2)
            style = random.choices([0, 1, 2], weights=[70, 15, 15])[0]
            lignes.append([formater(ts, style), site_id, conso, tension, freq, "OK"])

    # Codes erreur capteur (statut ERROR) : -999 x4, -888 x3, -777 x2
    indices = random.sample(range(len(lignes)), 13)
    for i, code in zip(indices[:9], [-999] * 4 + [-888] * 3 + [-777] * 2):
        lignes[i][2] = code
        lignes[i][5] = "ERROR"
    # Valeurs manquantes (consumption_mw vide) x4
    for i in indices[9:]:
        lignes[i][2] = ""
        lignes[i][5] = "ERROR"

    # Doublons exacts x6
    doublons = random.sample(range(len(lignes)), 6)
    for i in doublons:
        lignes.append(list(lignes[i]))

    random.shuffle(lignes)

    with open("consommation_echantillon.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "site_id", "consumption_mw", "voltage_v", "frequency_hz", "status"])
        w.writerows(lignes)

    print(f"✅ sites_reference.csv : {len(SITES)} lignes")
    print(f"✅ consommation_echantillon.csv : {len(lignes)} lignes")


if __name__ == "__main__":
    main()
