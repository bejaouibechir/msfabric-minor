"""analyse_sites.py — Contrôle qualité des mesures de consommation (Workshop 1).

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


def afficher(rapport: dict) -> None:
    print(f"{'Site':<14}{'Mesures':>8}{'Valides':>9}{'Manq.':>7}{'Codes':>7}{'Anom.':>8}{'Charge':>9}")
    for site_id, s in rapport["sites"].items():
        print(f"{site_id:<14}{s['mesures']:>8}{s['valides']:>9}{s['manquantes']:>7}"
              f"{s['codes_erreur']:>7}{s['taux_anomalies']:>8.1%}{s['taux_charge_moyen']:>9.1%}")
    print(f"Doublons écartés      : {rapport['doublons_ecartes']}")
    print(f"Horodatages invalides : {rapport['horodatages_invalides']}")
    print(f"Taux d'anomalies      : {rapport['taux_anomalies_global']:.1%}")


def lire_arguments(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="analyse_sites", description=__doc__.splitlines()[0])
    parser.add_argument("--input", "-i", required=True, type=Path, help="fichier CSV des mesures")
    parser.add_argument("--sites", type=Path, default=Path("data/sites_reference.csv"),
                        help="référentiel des sites (défaut : %(default)s)")
    parser.add_argument("--seuil", type=float, default=0.10, help="taux d'anomalies maximal toléré")
    parser.add_argument("--json", action="store_true", help="écrire out/rapport_qualite.json")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    args = lire_arguments(argv)

    log.info("Analyse de %s", args.input)
    rapport = analyser(args.input, args.sites)
    afficher(rapport)

    if args.json:
        Path("out").mkdir(exist_ok=True)
        Path("out/rapport_qualite.json").write_text(
            json.dumps(rapport, indent=2, ensure_ascii=False), encoding="utf-8")
        log.info("Rapport écrit dans out/rapport_qualite.json")

    if rapport["taux_anomalies_global"] > args.seuil:
        log.error("Seuil dépassé : %.1f %% > %.1f %%",
                  rapport["taux_anomalies_global"] * 100, args.seuil * 100)
        return 1
    log.info("Qualité conforme au seuil")
    return 0


if __name__ == "__main__":
    sys.exit(main())
