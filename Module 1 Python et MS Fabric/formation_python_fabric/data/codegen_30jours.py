"""
codegen_30jours.py — Génération du jeu de données de l'Atelier 2 (Module 1)

Produit consommation_30jours.csv : 30 jours (1er au 30 janvier 2025) de mesures horaires
pour les 6 sites du référentiel (6 x 24 x 30 = 4 320 mesures) avec les anomalies du Module 2 :
  - formats de timestamp hétérogènes (ISO avec 'T', ISO avec espace, JJ/MM/AAAA)
  - codes erreur capteur : -999, -888, -777 (statut ERROR)
  - valeurs manquantes (consumption_mw vide, statut ERROR)
  - pics aberrants (consommation supérieure à la capacité du site, statut OK)
  - doublons exacts
Usage : python codegen_30jours.py   (graine fixe : mêmes données à chaque exécution)
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

SITES = [
    ("SITE_IND_001", "Industrie",   5.0, 2.5),
    ("SITE_IND_002", "Industrie",   3.5, 1.75),
    ("SITE_COM_001", "Commercial",  2.0, 1.0),
    ("SITE_COM_002", "Commercial",  1.5, 0.75),
    ("SITE_RES_001", "Residentiel", 0.8, 0.4),
    ("SITE_RES_002", "Residentiel", 0.6, 0.3),
]
DEBUT = datetime(2025, 1, 1)
NB_JOURS = 30


def profil_horaire(site_type, heure):
    if site_type == "Industrie":
        return 1.2 if 6 <= heure <= 20 else 0.7
    if site_type == "Commercial":
        return 1.3 if 8 <= heure <= 19 else 0.5
    return 1.3 if heure in (7, 8, 18, 19, 20, 21) else 0.8


def facteur_jour(site_type, jour):
    """Week-end : moins d'activité pour l'industrie et le commerce, plus pour le résidentiel."""
    weekend = jour.weekday() >= 5
    if not weekend:
        return 1.0
    return {"Industrie": 0.6, "Commercial": 0.7, "Residentiel": 1.15}[site_type]


def formater(ts, style):
    return ts.strftime(("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S")[style])


def main():
    lignes = []
    for site_id, site_type, cap, base in SITES:
        for j in range(NB_JOURS):
            for h in range(24):
                ts = DEBUT + timedelta(days=j, hours=h)
                conso = base * profil_horaire(site_type, h) * facteur_jour(site_type, ts) * random.uniform(0.9, 1.1)
                conso = round(min(conso, cap), 3)
                tension = round(random.gauss(230, 4), 1)
                freq = round(random.gauss(50.0, 0.12), 2)
                style = random.choices([0, 1, 2], weights=[70, 15, 15])[0]
                lignes.append([formater(ts, style), site_id, conso, tension, freq, "OK"])
    n = len(lignes)
    tirage = random.sample(range(n), 260 + 90 + 15)
    codes = [-999] * 110 + [-888] * 85 + [-777] * 65
    for i, code in zip(tirage[:260], codes):
        lignes[i][2], lignes[i][5] = code, "ERROR"
    for i in tirage[260:350]:
        lignes[i][2], lignes[i][5] = "", "ERROR"
    caps = {s[0]: s[2] for s in SITES}
    for i in tirage[350:]:                       # pics aberrants : 1,3 à 1,8 fois la capacité
        lignes[i][2] = round(caps[lignes[i][1]] * random.uniform(1.3, 1.8), 3)
    for i in random.sample(range(n), 45):        # doublons exacts
        lignes.append(list(lignes[i]))
    random.shuffle(lignes)
    with open("consommation_30jours.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "site_id", "consumption_mw", "voltage_v", "frequency_hz", "status"])
        w.writerows(lignes)
    print(f"consommation_30jours.csv : {len(lignes)} lignes")


if __name__ == "__main__":
    main()
