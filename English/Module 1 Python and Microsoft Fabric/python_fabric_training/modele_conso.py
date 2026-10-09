"""modele_conso.py — Entraîner, sauvegarder et utiliser le modèle de prévision (Workshop 3)."""
import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

import prevision_conso as pc


def entrainer(d, coupure=pc.COUPURE):
    """Entraîne le pipeline final ; renvoie le modèle et son erreur sur la période de test."""
    train, test = pc.decouper(d, coupure)
    modele = pc.construire_modele().fit(train[pc.COLONNES], train["conso_mw"])
    return modele, pc.evaluer(test["conso_mw"], modele.predict(test[pc.COLONNES]))


def prevoir_jour(modele, d, jour):
    """Prévision horaire de chaque site pour la date `jour` (historique jusqu'à la veille au moins)."""
    sites = d.drop_duplicates("site_id")[["site_id", "site_type", "capacity_mw"]]
    heures = pd.date_range(jour, periods=24, freq="h")
    futur = pd.MultiIndex.from_product([sites["site_id"], heures], names=["site_id", "timestamp"]).to_frame(index=False)
    futur = futur.merge(sites, on="site_id")
    futur["conso_mw"] = np.nan
    base = d[["timestamp", "site_id", "site_type", "capacity_mw", "conso_brute"]].rename(columns={"conso_brute": "conso_mw"})
    tout = pd.concat([base, futur], ignore_index=True).sort_values(["site_id", "timestamp"], ignore_index=True)
    tout = pc.ajouter_variables(tout)
    cible = tout[tout["timestamp"].isin(heures)].copy()
    cible["prevu_mw"] = modele.predict(cible[pc.COLONNES])
    return cible[["site_id", "timestamp", "prevu_mw"]]


def main(argv=None):
    p = argparse.ArgumentParser(description="Entraîner le modèle et prévoir un jour.")
    p.add_argument("--sortie", default="modeles/modele_conso.joblib")
    p.add_argument("--jour", default="2025-01-31")
    args = p.parse_args(argv)

    d = pc.preparer()
    modele, mesures = entrainer(d)
    Path(args.sortie).parent.mkdir(exist_ok=True)
    joblib.dump(modele, args.sortie)
    Path(args.sortie).with_suffix(".json").write_text(json.dumps(
        {"scikit_learn": sklearn.__version__, "variables": pc.COLONNES, "mae_test": round(mesures["MAE"], 4)},
        indent=2), encoding="utf-8")
    prevision = prevoir_jour(modele, d, args.jour)
    print(f"Modèle enregistré : {args.sortie} | MAE test {mesures['MAE']:.3f} MW")
    print(f"Prévision du {args.jour} : {len(prevision)} lignes, total {prevision['prevu_mw'].sum():.1f} MWh")
    return prevision


if __name__ == "__main__":
    main()
