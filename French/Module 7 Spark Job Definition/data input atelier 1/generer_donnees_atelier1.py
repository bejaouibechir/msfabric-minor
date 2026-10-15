#!/usr/bin/env python3
"""Génère les trois jeux JSON de l'atelier Spark Job Definition.

Avec la graine par défaut et 30 lignes, les fichiers reproduisent exactement les
données de l'API pédagogique T08. Une autre graine conserve les mêmes schémas et
produit des valeurs fictives légèrement différentes.
"""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


GRAINE_PAR_DEFAUT = 20251001

BESOINS = [
    ("2025-01-01T00:00:00", "Atelier_A", 245.67, "Fossile", 52.34),
    ("2025-01-01T01:00:00", "Bureaux", 89.23, "Fossile", 18.92),
    ("2025-01-01T02:00:00", "Atelier_B", 312.45, "Fossile", 66.54),
    ("2025-01-01T03:00:00", "Entrepot", 156.78, "Fossile", 33.21),
    ("2025-01-01T04:00:00", "Atelier_A", 289.34, "Fossile", 61.45),
    ("2025-01-01T05:00:00", "Atelier_B", 378.92, "Fossile", 80.56),
    ("2025-01-01T06:00:00", "Bureaux", 134.56, "Fossile", 28.67),
    ("2025-01-01T07:00:00", "Atelier_A", 423.12, "Fossile", 89.87),
    ("2025-01-01T08:00:00", "Entrepot", 201.45, "Fossile", 42.78),
    ("2025-01-01T09:00:00", "Atelier_B", 456.78, "Fossile", 97.12),
    ("2025-01-01T10:00:00", "Bureaux", 167.89, "Fossile", 35.67),
    ("2025-01-01T11:00:00", "Atelier_A", 389.23, "Fossile", 82.78),
    ("2025-01-01T12:00:00", "Atelier_B", 412.56, "Fossile", 87.65),
    ("2025-01-01T13:00:00", "Entrepot", 178.34, "Fossile", 37.89),
    ("2025-01-01T14:00:00", "Bureaux", 145.67, "Fossile", 30.98),
    ("2025-01-01T15:00:00", "Atelier_A", 367.89, "Fossile", 78.23),
    ("2025-01-01T16:00:00", "Atelier_B", 398.45, "Fossile", 84.67),
    ("2025-01-01T17:00:00", "Entrepot", 189.56, "Fossile", 40.23),
    ("2025-01-01T18:00:00", "Bureaux", 112.34, "Fossile", 23.87),
    ("2025-01-01T19:00:00", "Atelier_A", 334.67, "Fossile", 71.12),
    ("2025-01-01T20:00:00", "Atelier_B", 356.89, "Fossile", 75.89),
    ("2025-01-01T21:00:00", "Entrepot", 167.23, "Fossile", 35.54),
    ("2025-01-01T22:00:00", "Bureaux", 98.45, "Fossile", 20.92),
    ("2025-01-01T23:00:00", "Atelier_A", 278.90, "Fossile", 59.28),
    ("2025-01-02T00:00:00", "Atelier_B", 312.45, "Fossile", 66.43),
    ("2025-01-02T01:00:00", "Entrepot", 145.67, "Fossile", 30.95),
    ("2025-01-02T02:00:00", "Bureaux", 87.34, "Fossile", 18.56),
    ("2025-01-02T03:00:00", "Atelier_A", 267.89, "Fossile", 56.94),
    ("2025-01-02T04:00:00", "Atelier_B", 334.56, "Fossile", 71.12),
    ("2025-01-02T05:00:00", "Entrepot", 178.23, "Fossile", 37.87),
]

SOLAIRE = [
    ("SOL_001", "2025-01-01", "Toit_Sud", 38.5, 8.5, 20.3),
    ("SOL_002", "2025-01-01", "Toit_Nord", 22.3, 6.2, 17.8),
    ("SOL_003", "2025-01-01", "Parking", 31.7, 7.8, 19.5),
    ("SOL_004", "2025-01-01", "Toit_Sud", 42.1, 9.2, 21.4),
    ("SOL_005", "2025-01-01", "Toit_Nord", 18.9, 5.5, 16.2),
    ("SOL_006", "2025-01-01", "Parking", 28.4, 7.1, 18.7),
    ("SOL_007", "2025-01-01", "Toit_Sud", 39.8, 8.8, 20.9),
    ("SOL_008", "2025-01-01", "Toit_Nord", 24.6, 6.7, 18.1),
    ("SOL_009", "2025-01-01", "Parking", 33.2, 7.9, 19.8),
    ("SOL_010", "2025-01-01", "Toit_Sud", 41.3, 9.0, 21.1),
    ("SOL_011", "2025-01-01", "Toit_Nord", 20.5, 6.0, 17.3),
    ("SOL_012", "2025-01-01", "Parking", 29.7, 7.4, 19.0),
    ("SOL_013", "2025-01-01", "Toit_Sud", 37.9, 8.4, 20.5),
    ("SOL_014", "2025-01-01", "Toit_Nord", 23.1, 6.5, 17.9),
    ("SOL_015", "2025-01-01", "Parking", 32.5, 7.7, 19.6),
    ("SOL_016", "2025-01-01", "Toit_Sud", 40.6, 8.9, 21.0),
    ("SOL_017", "2025-01-01", "Toit_Nord", 21.8, 6.3, 17.6),
    ("SOL_018", "2025-01-01", "Parking", 30.4, 7.5, 19.2),
    ("SOL_019", "2025-01-01", "Toit_Sud", 38.2, 8.6, 20.4),
    ("SOL_020", "2025-01-01", "Toit_Nord", 19.7, 5.8, 16.9),
    ("SOL_021", "2025-01-01", "Parking", 27.9, 7.2, 18.8),
    ("SOL_022", "2025-01-01", "Toit_Sud", 43.4, 9.4, 21.6),
    ("SOL_023", "2025-01-01", "Toit_Nord", 25.3, 6.9, 18.3),
    ("SOL_024", "2025-01-01", "Parking", 34.1, 8.1, 19.9),
    ("SOL_025", "2025-01-01", "Toit_Sud", 36.8, 8.2, 20.1),
    ("SOL_001", "2025-01-02", "Toit_Sud", 35.2, 8.0, 19.8),
    ("SOL_002", "2025-01-02", "Toit_Nord", 20.1, 5.9, 17.1),
    ("SOL_003", "2025-01-02", "Parking", 29.3, 7.3, 18.9),
    ("SOL_004", "2025-01-02", "Toit_Sud", 39.7, 8.7, 20.7),
    ("SOL_005", "2025-01-02", "Toit_Nord", 17.4, 5.2, 15.9),
]

EOLIEN = [
    ("EOL_1", "2025-01-01T00:00:00", 12.3, 65.4, "Operationnel"),
    ("EOL_2", "2025-01-01T00:00:00", 8.7, 42.1, "Operationnel"),
    ("EOL_3", "2025-01-01T00:00:00", 15.2, 78.9, "Operationnel"),
    ("EOL_4", "2025-01-01T00:00:00", 6.4, 28.3, "Operationnel"),
    ("EOL_5", "2025-01-01T00:00:00", 3.1, 0.0, "Maintenance"),
    ("EOL_1", "2025-01-01T01:00:00", 11.8, 62.3, "Operationnel"),
    ("EOL_2", "2025-01-01T01:00:00", 9.2, 45.7, "Operationnel"),
    ("EOL_3", "2025-01-01T01:00:00", 14.6, 75.2, "Operationnel"),
    ("EOL_4", "2025-01-01T01:00:00", 7.1, 32.8, "Operationnel"),
    ("EOL_5", "2025-01-01T01:00:00", 2.8, 0.0, "Maintenance"),
    ("EOL_1", "2025-01-01T02:00:00", 13.5, 69.8, "Operationnel"),
    ("EOL_2", "2025-01-01T02:00:00", 8.3, 39.4, "Operationnel"),
    ("EOL_3", "2025-01-01T02:00:00", 16.1, 80.0, "Operationnel"),
    ("EOL_4", "2025-01-01T02:00:00", 5.9, 24.7, "Operationnel"),
    ("EOL_5", "2025-01-01T02:00:00", 10.4, 56.2, "Operationnel"),
    ("EOL_1", "2025-01-01T03:00:00", 12.7, 66.9, "Operationnel"),
    ("EOL_2", "2025-01-01T03:00:00", 9.8, 48.3, "Operationnel"),
    ("EOL_3", "2025-01-01T03:00:00", 14.3, 73.6, "Operationnel"),
    ("EOL_4", "2025-01-01T03:00:00", 6.7, 30.1, "Operationnel"),
    ("EOL_5", "2025-01-01T03:00:00", 11.2, 59.8, "Operationnel"),
    ("EOL_1", "2025-01-01T04:00:00", 11.4, 60.5, "Operationnel"),
    ("EOL_2", "2025-01-01T04:00:00", 8.9, 43.2, "Operationnel"),
    ("EOL_3", "2025-01-01T04:00:00", 15.7, 79.1, "Operationnel"),
    ("EOL_4", "2025-01-01T04:00:00", 6.2, 26.9, "Operationnel"),
    ("EOL_5", "2025-01-01T04:00:00", 3.5, 0.0, "Maintenance"),
    ("EOL_1", "2025-01-01T05:00:00", 13.1, 68.2, "Operationnel"),
    ("EOL_2", "2025-01-01T05:00:00", 9.5, 46.8, "Operationnel"),
    ("EOL_3", "2025-01-01T05:00:00", 14.9, 76.5, "Operationnel"),
    ("EOL_4", "2025-01-01T05:00:00", 7.4, 34.2, "Operationnel"),
    ("EOL_5", "2025-01-01T05:00:00", 10.8, 58.1, "Operationnel"),
]


def _etendre(lignes: list[tuple[Any, ...]], nombre: int, type_date: str) -> list[tuple[Any, ...]]:
    resultat: list[tuple[Any, ...]] = []
    for index in range(nombre):
        base = list(lignes[index % len(lignes)])
        cycle = index // len(lignes)
        if cycle:
            position = 0 if type_date == "timestamp-premier" else 1
            format_date = "%Y-%m-%dT%H:%M:%S" if "T" in str(base[position]) else "%Y-%m-%d"
            date = datetime.strptime(str(base[position]), format_date) + timedelta(days=cycle * 2)
            base[position] = date.strftime(format_date)
        resultat.append(tuple(base))
    return resultat


def _ajuster(valeur: float, rng: random.Random, actif: bool) -> float:
    return valeur if not actif else round(max(0.0, valeur * rng.uniform(0.94, 1.06)), 2)


def construire(nombre: int, graine: int) -> dict[str, list[dict[str, Any]]]:
    rng = random.Random(graine)
    varier = graine != GRAINE_PAR_DEFAUT
    besoins = [
        {"Timestamp": t, "Zone": z, "Consommation_kWh": _ajuster(c, rng, varier),
         "Type_Energie": e, "Cout_Euro": _ajuster(cout, rng, varier)}
        for t, z, c, e, cout in _etendre(BESOINS, nombre, "timestamp-premier")
    ]
    solaire = [
        {"PanneauID": p, "Date": d, "Zone_Installation": z,
         "Production_kWh": _ajuster(prod, rng, varier),
         "Ensoleillement_Heures": _ajuster(ens, rng, varier),
         "Rendement_Pct": _ajuster(rend, rng, varier)}
        for p, d, z, prod, ens, rend in _etendre(SOLAIRE, nombre, "date-second")
    ]
    eolien = [
        {"TurbineID": turbine, "Timestamp": t,
         "Vitesse_Vent_ms": _ajuster(vent, rng, varier),
         "Production_kWh": _ajuster(prod, rng, varier), "Statut": statut}
        for turbine, t, vent, prod, statut in _etendre(EOLIEN, nombre, "date-second")
    ]
    return {"besoins.json": besoins, "production-solaire.json": solaire,
            "production-eolienne.json": eolien}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("sortie"), help="Dossier de sortie")
    parser.add_argument("--seed", type=int, default=GRAINE_PAR_DEFAUT, help="Graine aléatoire")
    parser.add_argument("--lignes", type=int, default=30, help="Nombre de lignes par fichier")
    args = parser.parse_args()
    if args.lignes < 1:
        parser.error("--lignes doit être supérieur ou égal à 1")
    args.out.mkdir(parents=True, exist_ok=True)
    for nom, contenu in construire(args.lignes, args.seed).items():
        chemin = args.out / nom
        chemin.write_text(json.dumps(contenu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{chemin}: {len(contenu)} lignes")


if __name__ == "__main__":
    main()
