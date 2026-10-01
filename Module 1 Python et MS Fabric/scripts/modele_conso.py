"""modele_conso.py — Entraîner, sauvegarder et utiliser le modèle de prévision (Atelier 3)."""
# --- 1. Importer les bibliothèques ---
import argparse  # lit les options tapées en ligne de commande
import json  # écrit le fichier de métadonnées
from pathlib import Path  # manipule les chemins de fichiers

import joblib  # sauvegarde le modèle sur disque
import numpy as np  # valeurs manquantes (np.nan)
import pandas as pd  # tableaux de données
import sklearn  # sert à lire le numéro de version

# Module de la Partie 3 : préparation des données, découpage, pipeline, évaluation.
import prevision_conso as pc


# Fonction entrainer
# Entrées : d = tableau préparé ; coupure = date qui sépare entraînement et test (par défaut pc.COUPURE).
# Sortie : le modèle entraîné et ses erreurs (MAE, RMSE, R2) sur la période de test.
def entrainer(d, coupure=pc.COUPURE):
    """Entraîne le pipeline final ; renvoie le modèle et son erreur sur la période de test."""
    # Couper le temps en deux : le passé pour apprendre, le futur pour tester.
    train, test = pc.decouper(d, coupure)
    # Construire le pipeline et l'entraîner sur la période d'entraînement.
    modele = pc.construire_modele().fit(train[pc.COLONNES], train["conso_mw"])
    # Mesurer l'erreur sur le test, période que le modèle n'a pas vue.
    # return : les deux résultats sont rendus ensemble (un tuple).
    return modele, pc.evaluer(test["conso_mw"], modele.predict(test[pc.COLONNES]))


# Fonction prevoir_jour
# Entrées : modele = modèle entraîné ; d = historique préparé ; jour = date à prévoir.
# Sortie : tableau (site_id, timestamp, prevu_mw), 24 lignes par site.
def prevoir_jour(modele, d, jour):
    """Prévision horaire de chaque site pour la date `jour` (historique jusqu'à la veille au moins)."""
    # Une ligne par site avec ses caractéristiques fixes (type, capacité).
    # drop_duplicates("site_id") garde la première ligne de chaque site.
    sites = d.drop_duplicates("site_id")[["site_id", "site_type", "capacity_mw"]]
    # Les 24 heures du jour à prévoir.
    heures = pd.date_range(jour, periods=24, freq="h")
    # Toutes les combinaisons site x heure, en tableau à colonnes site_id et timestamp.
    futur = pd.MultiIndex.from_product([sites["site_id"], heures], names=["site_id", "timestamp"]).to_frame(index=False)
    # Rattacher type et capacité à chaque ligne.
    futur = futur.merge(sites, on="site_id")
    # La consommation du jour à prévoir est inconnue : valeur manquante.
    # np.nan : valeur manquante, le modèle la remplacera par une prévision.
    futur["conso_mw"] = np.nan
    # Historique : mêmes colonnes, la consommation brute devenant conso_mw.
    base = d[["timestamp", "site_id", "site_type", "capacity_mw", "conso_brute"]].rename(columns={"conso_brute": "conso_mw"})
    # Empiler historique et jour à prévoir, triés par site puis par heure : les décalages (retards) deviennent calculables.
    tout = pd.concat([base, futur], ignore_index=True).sort_values(["site_id", "timestamp"], ignore_index=True)
    # Calculer les variables du modèle (heure, retards, etc.) sur l'ensemble.
    tout = pc.ajouter_variables(tout)
    # Ne garder que les lignes du jour à prévoir.
    cible = tout[tout["timestamp"].isin(heures)].copy()
    # Prédire la consommation de chaque site et chaque heure.
    cible["prevu_mw"] = modele.predict(cible[pc.COLONNES])
    # Renvoyer seulement les colonnes utiles.
    # Fin de la fonction : la prévision est rendue à l'appelant.
    return cible[["site_id", "timestamp", "prevu_mw"]]


# Fonction main
# Entrée : argv = liste d'options (None : lit celles de la ligne de commande).
# Sortie : le tableau de prévisions ; entraîne, sauvegarde et prévoit en une commande.
def main(argv=None):
    # Déclarer les options acceptées.
    # ArgumentParser : objet qui lit les options ; description : texte affiché par --help.
    p = argparse.ArgumentParser(description="Entraîner le modèle et prévoir un jour.")
    # --sortie : fichier où écrire le modèle ; --jour : date à prévoir.
    p.add_argument("--sortie", default="modeles/modele_conso.joblib")
    # default : valeur utilisée si l'option n'est pas fournie.
    p.add_argument("--jour", default="2025-01-31")
    # Lire les options fournies (sinon les valeurs par défaut s'appliquent).
    args = p.parse_args(argv)

    # Charger et préparer les données.
    d = pc.preparer()
    # Entraîner le modèle et obtenir ses erreurs sur le test.
    modele, mesures = entrainer(d)
    # Créer le dossier de destination s'il manque.
    Path(args.sortie).parent.mkdir(exist_ok=True)
    # Sauvegarder le modèle.
    joblib.dump(modele, args.sortie)
    # Écrire à côté un fichier .json (même nom) : version de scikit-learn, variables, MAE.
    Path(args.sortie).with_suffix(".json").write_text(json.dumps(
        {"scikit_learn": sklearn.__version__, "variables": pc.COLONNES, "mae_test": round(mesures["MAE"], 4)},
        indent=2), encoding="utf-8")
    # Prévoir le jour demandé.
    prevision = prevoir_jour(modele, d, args.jour)
    # Résumé affiché : fichier écrit, erreur de test, taille et total de la prévision.
    print(f"Modèle enregistré : {args.sortie} | MAE test {mesures['MAE']:.3f} MW")
    print(f"Prévision du {args.jour} : {len(prevision)} lignes, total {prevision['prevu_mw'].sum():.1f} MWh")
    # Rendre la prévision : utile si main est appelée depuis un autre programme.
    return prevision


# __name__ vaut "__main__" seulement quand le fichier est lancé directement.
# Ce bloc ne s'exécute que si le fichier est lancé directement (python modele_conso.py),
# et non quand il est importé par un notebook.
if __name__ == "__main__":
    main()
