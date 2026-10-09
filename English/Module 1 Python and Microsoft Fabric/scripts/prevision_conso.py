"""prevision_conso.py — Préparation, évaluation et modèle de prévision (Workshop 3)."""
# --- Imports : calcul, tableaux, outils scikit-learn utilisés par les fonctions ---
import numpy as np                                                    # np.nan : valeur manquante
import pandas as pd                                                   # tableaux de données
from sklearn.compose import make_column_transformer                   # prétraitement par groupe de colonnes
from sklearn.ensemble import HistGradientBoostingRegressor            # modèle de gradient boosting
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error    # métriques d'erreur
from sklearn.pipeline import make_pipeline                            # enchaîne prétraitement et modèle
from sklearn.preprocessing import OrdinalEncoder                      # texte -> entier

import qualite_pandas as qp    # module de l'Workshop 2 : nettoyage des mesures

# --- Constantes partagées par le notebook et le module ---
# variables numériques données au modèle pour prévoir la consommation
VARIABLES = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]
# colonnes d'entrée complètes : le site (texte) en premier, puis les variables numériques
COLONNES = ["site_id"] + VARIABLES
# début de la période utile : les 7 premiers jours n'ont pas encore de lag_168
DEBUT_UTILE = pd.Timestamp("2025-01-08")
# date de coupure : avant = apprentissage, à partir de là = test
COUPURE = pd.Timestamp("2025-01-24")


# Rôle : lire les deux CSV, nettoyer les mesures et ajouter type et capacité de chaque site.
# Entrées : chemins des deux fichiers (valeurs par défaut du dossier data/). Sortie : DataFrame propre.
def charger_propre(mesures="data/consommation_30jours.csv", reference="data/sites_reference.csv"):
    """Mesures nettoyées (Workshop 2), avec type et capacité des sites."""
    # lecture des mesures (utf-8-sig : accents et BOM) ; nom de colonne raccourci
    brut = pd.read_csv(mesures, encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
    # lecture de la table des sites, en ne gardant que les 3 colonnes utiles
    ref = pd.read_csv(reference, encoding="utf-8-sig")[["site_id", "site_type", "capacity_mw"]]
    # nettoyage puis jointure ; validate="m:1" : erreur si un site apparaît deux fois dans ref
    return qp.nettoyer(brut).merge(ref, on="site_id", how="left", validate="m:1")


# Rôle : construire la cible et toutes les variables explicatives.
# Entrée : DataFrame propre d. Sortie : copie enrichie (l'original n'est pas modifié).
def ajouter_variables(d):
    """Cible sans pics, variables de calendrier, valeurs décalées, moyenne glissante."""
    d = d.copy()    # copie : on ne modifie pas le tableau de l'appelant
    # 1. cible : copie brute conservée, pics au-dessus de la capacité repérés puis remplacés par NaN
    d["conso_brute"] = d["conso_mw"]
    d["pic"] = d["conso_mw"] > d["capacity_mw"]
    d["conso_mw"] = d["conso_mw"].mask(d["pic"])
    # 2. calendrier : heure (0-23), jour de semaine (0 = lundi), week-end (1 si samedi/dimanche)
    d["heure"] = d["timestamp"].dt.hour
    d["jour_sem"] = d["timestamp"].dt.dayofweek
    d["weekend"] = (d["jour_sem"] >= 5).astype(int)
    # 3. taux d'utilisation : consommation rapportée à la capacité du site
    d["taux"] = d["conso_mw"] / d["capacity_mw"]
    # 4. valeurs décalées, calculées site par site pour ne jamais mélanger deux sites
    g = d.groupby("site_id")["conso_mw"]
    d["lag_24"] = g.shift(24)      # même heure la veille
    d["lag_168"] = g.shift(168)    # même heure la semaine dernière
    # 5. moyenne des 24 h se terminant 24 h avant la mesure (aucune information du futur)
    d["moy_veille"] = g.transform(lambda s: s.shift(24).rolling(24, min_periods=12).mean())
    return d    # tableau enrichi


# Rôle : enchaîner chargement et création des variables.
# Entrée : chemins optionnels (mots-clés transmis à charger_propre). Sortie : tableau prêt à découper.
def preparer(**chemins):
    return ajouter_variables(charger_propre(**chemins))    # sortie de charger_propre passée à ajouter_variables


# Rôle : couper dans le temps, jamais au hasard.
# Entrées : tableau préparé d, date de coupure. Sortie : couple (train, test).
def decouper(d, coupure=COUPURE):
    """Passé pour apprendre, futur (lags complets) pour tester."""
    # on écarte les 7 premiers jours et les lignes sans cible
    utile = d[(d["timestamp"] >= DEBUT_UTILE) & d["conso_mw"].notna()]
    # premier élément : le passé (train) ; second : le futur (test), sans ligne où lag_24 ou lag_168 manque
    return (utile[utile["timestamp"] < coupure],
            utile[utile["timestamp"] >= coupure].dropna(subset=["lag_24", "lag_168"]))


# Rôle : résumer la qualité d'une prévision.
# Entrées : valeurs réelles y_vrai, valeurs prévues y_pred. Sortie : dictionnaire MAE / RMSE / R2.
def evaluer(y_vrai, y_pred):
    return {"MAE": mean_absolute_error(y_vrai, y_pred),         # écart moyen en MW
            "RMSE": root_mean_squared_error(y_vrai, y_pred),    # écart en MW, gros écarts amplifiés
            "R2": r2_score(y_vrai, y_pred)}                     # part de variation expliquée (1 = parfait)


# Rôle : fabriquer le pipeline final (non entraîné).
# Entrée : réglages facultatifs du modèle (**params). Sortie : pipeline prêt pour fit / predict.
def construire_modele(**params):
    """Pipeline final : site encodé comme catégorie + gradient boosting."""
    # étape 1 : site_id devient un entier (un site inconnu donne NaN) ; les autres colonnes passent telles quelles
    prep = make_column_transformer(
        (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan), ["site_id"]),
        remainder="passthrough",
    )
    # étape 2 : gradient boosting ; colonne 0 (site) traitée comme catégorie ; random_state=0 : reproductible
    return make_pipeline(prep, HistGradientBoostingRegressor(categorical_features=[0], random_state=0, **params))
