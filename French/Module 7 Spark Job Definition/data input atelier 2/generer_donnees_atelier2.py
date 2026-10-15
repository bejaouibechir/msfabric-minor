#!/usr/bin/env python3
"""Génère des lots JSON Lines de mesures capteurs avec anomalies connues."""

from __future__ import annotations

import argparse
import copy
import json
import random
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


GRANDEURS = {
    "temperature": (18.0, 34.0, "°C", -30.0),
    "irradiance": (100.0, 1100.0, "W/m2", 5000.0),
    "vitesse_vent": (0.0, 25.0, "m/s", 120.0),
    "puissance": (0.0, 900.0, "kW", 9999.0),
}


def _indices(debut: int, pas: int, taille: int, interdits: set[int]) -> list[int]:
    return [i for i in range(debut, taille, pas) if i not in interdits]


def creer_lot(numero: int, taille: int, rng: random.Random) -> tuple[list[dict[str, Any]], dict[str, int]]:
    origine = datetime(2025, 2, 1, tzinfo=timezone.utc) + timedelta(hours=numero)
    lignes: list[dict[str, Any]] = []
    for index in range(taille):
        grandeur = list(GRANDEURS)[(numero + index) % len(GRANDEURS)]
        minimum, maximum, unite, _ = GRANDEURS[grandeur]
        lignes.append({
            "capteur_id": f"CAP-{1 + (index % 12):03d}",
            "site_id": f"SITE-{1 + (index % 3):02d}",
            "timestamp": (origine + timedelta(seconds=30 * index)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "grandeur": grandeur,
            "valeur": round(rng.uniform(minimum, maximum), 3),
            "unite": unite,
            "qualite": "OK",
        })

    utilises: set[int] = set()
    nulls = _indices(3, 23, taille, utilises)
    utilises.update(nulls)
    hors_plage = _indices(5, 19, taille, utilises)
    utilises.update(hors_plage)
    heterogenes = _indices(7, 17, taille, utilises)
    utilises.update(heterogenes)
    doublons = [i for i in _indices(9, 29, taille, utilises) if i > 0]

    for index in nulls:
        lignes[index]["valeur"] = None
        lignes[index]["qualite"] = "INCOMPLETE"
    for index in hors_plage:
        lignes[index]["valeur"] = GRANDEURS[lignes[index]["grandeur"]][3]
        lignes[index]["qualite"] = "HORS_PLAGE"
    for index in heterogenes:
        instant = origine + timedelta(seconds=30 * index)
        lignes[index]["timestamp"] = instant.strftime("%d/%m/%Y %H:%M:%S")
        lignes[index]["qualite"] = "FORMAT_DATE"
    for index in doublons:
        lignes[index] = copy.deepcopy(lignes[index - 1])

    compteurs = {
        "nulls": sum(ligne["valeur"] is None for ligne in lignes),
        "valeurs_hors_plage": sum(ligne["qualite"] == "HORS_PLAGE" for ligne in lignes),
        "doublons": sum(lignes[i] == lignes[i - 1] for i in range(1, len(lignes))),
        "timestamps_heterogenes": sum("/" in ligne["timestamp"] for ligne in lignes),
    }
    return lignes, compteurs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("sortie"))
    parser.add_argument("--lots", type=int, default=3)
    parser.add_argument("--lignes-par-lot", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20251002)
    parser.add_argument("--intervalle", type=float, default=0.0, help="Secondes entre deux lots")
    args = parser.parse_args()
    if args.lots < 1 or args.lignes_par_lot < 1 or args.intervalle < 0:
        parser.error("lots et lignes doivent être >= 1 ; intervalle doit être >= 0")

    args.out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    rapport: dict[str, Any] = {
        "parametres": {"lots": args.lots, "lignes_par_lot": args.lignes_par_lot,
                       "seed": args.seed, "intervalle": args.intervalle},
        "lots": [],
        "totaux": {"lignes": 0, "nulls": 0, "valeurs_hors_plage": 0,
                   "doublons": 0, "timestamps_heterogenes": 0},
    }
    for numero in range(args.lots):
        lignes, anomalies = creer_lot(numero, args.lignes_par_lot, rng)
        horodatage = (datetime(2025, 2, 1, tzinfo=timezone.utc) + timedelta(hours=numero)).strftime("%Y%m%dT%H%M%SZ")
        chemin = args.out / f"mesures_{horodatage}_lot{numero + 1:03d}.jsonl"
        chemin.write_text("".join(json.dumps(l, ensure_ascii=False) + "\n" for l in lignes), encoding="utf-8")
        rapport["lots"].append({"fichier": chemin.name, "lignes": len(lignes), **anomalies})
        rapport["totaux"]["lignes"] += len(lignes)
        for nom, valeur in anomalies.items():
            rapport["totaux"][nom] += valeur
        print(f"{chemin}: {len(lignes)} lignes, anomalies={sum(anomalies.values())}")
        if numero + 1 < args.lots and args.intervalle:
            time.sleep(args.intervalle)

    rapport_path = args.out / "rapport_anomalies.json"
    rapport_path.write_text(json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{rapport_path}: {rapport['totaux']}")


if __name__ == "__main__":
    main()
