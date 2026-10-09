"""Workshop 3 (matin : venv-ml) - cellules de reference. Chaque bloc "# %%" = une cellule du notebook."""

# %% Cellule 1 — Vérification de l'environnement
# === CELLULE 1 : Vérification de l'environnement ===
import sys
from importlib.metadata import version
from pathlib import Path

print(f"Python       : {sys.version.split()[0]}")
print(f"Interpréteur : {sys.executable}")
for paquet in ("numpy", "pandas", "scikit-learn", "mlflow"):
    print(f"{paquet:<13}: {version(paquet)}")
print(f"Dossier      : {Path.cwd().name}")
print(f"Fichiers     : {sorted(p.name for p in Path('data').glob('*.csv'))}")
print(f"Modules      : {[p for p in ('energie_utils.py', 'qualite_pandas.py') if Path(p).exists()]}")

# %% Cellule 2 — Ce que voit chaque noyau
# === CELLULE 2 : Ce que voit le noyau actif ===
import sys
from importlib.metadata import version
from importlib.util import find_spec

print("Interpréteur :", sys.executable)
for nom, paquet in (("pandas", "pandas"), ("matplotlib", "matplotlib"), ("seaborn", "seaborn"),
                    ("sklearn", "scikit-learn"), ("mlflow", "mlflow"), ("joblib", "joblib")):
    if find_spec(nom) is None:
        print(f"{nom:<11} ABSENT")
    else:
        print(f"{nom:<11} {version(paquet)}")

# %% Cellule 3 — Importer scikit-learn : l'erreur, puis la réussite
# === CELLULE 3 : Importer scikit-learn et MLflow ===
import pandas as pd
import sklearn
import mlflow
from sklearn.ensemble import HistGradientBoostingRegressor

print("pandas", pd.__version__, "| scikit-learn", sklearn.__version__, "| mlflow", mlflow.__version__)
print(HistGradientBoostingRegressor())

# %% Cellule 4 — Charger et nettoyer avec le module de l'Workshop 2
# === CELLULE 4 : Charger et nettoyer ===
import numpy as np
import pandas as pd
import qualite_pandas as qp

brut = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
ref = pd.read_csv("data/sites_reference.csv", encoding="utf-8-sig")

d = qp.nettoyer(brut).merge(ref[["site_id", "site_type", "capacity_mw"]], on="site_id", how="left", validate="m:1")
print(len(brut), "->", len(d), "lignes")
print(d[["timestamp", "site_id", "site_type", "capacity_mw", "conso_mw"]].head(3))
print(d["conso_mw"].isna().sum(), "valeurs manquantes")

# %% Cellule 5 — La cible : retirer les pics aberrants
# === CELLULE 5 : Pics aberrants ===
d["conso_brute"] = d["conso_mw"]
d["pic"] = d["conso_mw"] > d["capacity_mw"]
print(d["pic"].sum(), "pics au-dessus de la capacité")
print(d.loc[d["pic"], ["site_id", "conso_mw", "capacity_mw"]].head(3))

d["conso_mw"] = d["conso_mw"].mask(d["pic"])
print(d["conso_mw"].isna().sum(), "valeurs manquantes après retrait des pics")

# %% Cellule 6 — Variables de calendrier
# === CELLULE 6 : Variables de calendrier ===
d["heure"] = d["timestamp"].dt.hour
d["jour_sem"] = d["timestamp"].dt.dayofweek
d["weekend"] = (d["jour_sem"] >= 5).astype(int)

print(d[["timestamp", "heure", "jour_sem", "weekend"]].iloc[[0, 30, 130]])
d["taux"] = d["conso_mw"] / d["capacity_mw"]
print(d.pivot_table(index="site_type", columns="weekend", values="taux", aggfunc="mean").round(3))

# %% Cellule 7 — Le principe de scikit-learn : `fit`, `predict`, `score`
# === CELLULE 7 : L'interface commune ===
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

site = d[(d["site_id"] == "SITE_COM_001") & d["conso_mw"].notna()]
X, y = site[["heure"]], site["conso_mw"]

for modele in (LinearRegression(), RandomForestRegressor(n_estimators=50, random_state=0)):
    modele.fit(X, y)
    prevu = modele.predict(pd.DataFrame({"heure": [3, 14]}))
    print(f"{type(modele).__name__:<22} 3 h / 14 h : {prevu.round(2)}   R² sur ces données : {modele.score(X, y):.2f}")
print("Coefficient appris (linéaire) :", round(LinearRegression().fit(X, y).coef_[0], 4))

# %% Cellule 8 — Valeurs décalées : la veille et la semaine dernière
# === CELLULE 8 : Valeurs décalées ===
ecarts = d.groupby("site_id")["timestamp"].diff().dropna()
print("Écarts entre lignes :", ecarts.value_counts().to_dict())

g = d.groupby("site_id")["conso_mw"]
d["lag_24"] = g.shift(24)
d["lag_168"] = g.shift(168)

site = d[d["site_id"] == "SITE_COM_001"]
print(site[["timestamp", "conso_mw", "lag_24", "lag_168"]].iloc[[0, 24, 168, 192]])
print(d[["lag_24", "lag_168"]].isna().sum().to_dict())

# %% Cellule 9 — Moyenne glissante sans regarder l'avenir
# === CELLULE 9 : Moyenne glissante ===
d["moy_veille"] = g.transform(lambda s: s.shift(24).rolling(24, min_periods=12).mean())

i = 500
a_la_main = d.loc[i - 47:i - 24, "conso_mw"].mean()
print("Ligne", i, d.loc[i, "site_id"], d.loc[i, "timestamp"])
print("À la main :", round(a_la_main, 4), "| colonne moy_veille :", round(d.loc[i, "moy_veille"], 4))
print(d["moy_veille"].isna().sum(), "valeurs absentes")

# %% Cellule 10 — Découpage temporel : passé pour apprendre, futur pour tester
# === CELLULE 10 : Découpage temporel ===
VARIABLES = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]
COUPURE = pd.Timestamp("2025-01-24")

utile = d[(d["timestamp"] >= "2025-01-08") & d["conso_mw"].notna()]
train = utile[utile["timestamp"] < COUPURE]
test = utile[utile["timestamp"] >= COUPURE].dropna(subset=["lag_24", "lag_168"])

print("Entraînement :", len(train), "lignes,", train["timestamp"].min().date(), "->", train["timestamp"].max().date())
print("Test         :", len(test), "lignes,", test["timestamp"].min().date(), "->", test["timestamp"].max().date())
print("Manquants dans train :", train[VARIABLES].isna().sum()[lambda s: s > 0].to_dict())

# %% Cellule 11 — Corrélation avec la cible
# === CELLULE 11 : Corrélations ===
print(train[VARIABLES + ["conso_mw"]].corr()["conso_mw"].drop("conso_mw").round(2))

# %% Cellule 12 — Les références à battre
# === CELLULE 12 : Références ===
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

def evaluer(y_vrai, y_pred):
    return {"MAE": mean_absolute_error(y_vrai, y_pred),
            "RMSE": root_mean_squared_error(y_vrai, y_pred),
            "R2": r2_score(y_vrai, y_pred)}

moyenne_site = train.groupby("site_id")["conso_mw"].mean()
references = {
    "même heure la veille": test["lag_24"],
    "même heure la semaine dernière": test["lag_168"],
    "moyenne du site": test["site_id"].map(moyenne_site),
}
resultats = {nom: evaluer(test["conso_mw"], p) for nom, p in references.items()}
print(pd.DataFrame(resultats).T.round(3))

# %% Cellule 13 — Première régression : `LinearRegression`
# === CELLULE 13 : Régression linéaire ===
from sklearn.linear_model import LinearRegression

mediane = train[VARIABLES].median()
lin = LinearRegression().fit(train[VARIABLES].fillna(mediane), train["conso_mw"])
p_lin = lin.predict(test[VARIABLES].fillna(mediane))

resultats["régression linéaire"] = evaluer(test["conso_mw"], p_lin)
print({v: round(float(c), 3) for v, c in zip(VARIABLES, lin.coef_)})
print(pd.Series(resultats["régression linéaire"]).round(3).to_dict())

# %% Cellule 14 — Modèles à base d'arbres : forêt aléatoire et gradient boosting
# === CELLULE 14 : Forêt et gradient boosting ===
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

foret = RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1)
foret.fit(train[VARIABLES].fillna(mediane), train["conso_mw"])
hgb = HistGradientBoostingRegressor(random_state=0).fit(train[VARIABLES], train["conso_mw"])

p_foret = foret.predict(test[VARIABLES].fillna(mediane))
p_hgb = hgb.predict(test[VARIABLES])
resultats["forêt aléatoire"] = evaluer(test["conso_mw"], p_foret)
resultats["gradient boosting"] = evaluer(test["conso_mw"], p_hgb)
print(pd.DataFrame(resultats).T.loc[["forêt aléatoire", "gradient boosting"]].round(3))

# %% Cellule 15 — Comparer tous les modèles
# === CELLULE 15 : Tableau comparatif ===
tableau = pd.DataFrame(resultats).T.sort_values("MAE").round(3)
print(tableau)

ligne = test.iloc[[0]][VARIABLES].assign(lag_24=np.nan, lag_168=np.nan, moy_veille=np.nan)
print("\nSans aucun historique -> prévision :", round(float(hgb.predict(ligne)[0]), 3), "MW | réel :", round(float(test.iloc[0]["conso_mw"]), 3), "MW")

# %% Cellule 16 — Le plafond : le bruit qu'aucun modèle ne peut prévoir
# === CELLULE 16 : Erreur incompressible ===
profil = train.groupby(["site_id", "heure", "weekend"])["conso_mw"].mean()
p_profil = test.set_index(["site_id", "heure", "weekend"]).index.map(profil)

r = evaluer(test["conso_mw"], p_profil)
print({k: round(v, 3) for k, v in r.items()})
print("Niveau moyen de la consommation :", round(test["conso_mw"].mean(), 3), "MW")
print("MAE / niveau moyen :", f"{r['MAE'] / test['conso_mw'].mean():.1%}")

# %% Cellule 17 — `Pipeline` et `ColumnTransformer` : le prétraitement avec le modèle
# === CELLULE 17 : Pipeline complet ===
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeriques = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]
prep = ColumnTransformer([
    ("site", OneHotEncoder(handle_unknown="ignore"), ["site_id"]),
    ("nombres", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeriques),
])
pipe_lin = Pipeline([("prep", prep), ("modele", LinearRegression())])
pipe_lin.fit(train[["site_id"] + numeriques], train["conso_mw"])

p = pipe_lin.predict(test[["site_id"] + numeriques])
resultats["linéaire + pipeline"] = evaluer(test["conso_mw"], p)
print(list(pipe_lin.named_steps))
print(list(pipe_lin[:-1].get_feature_names_out())[:8], "...")
print(pd.Series(resultats["linéaire + pipeline"]).round(3).to_dict())

# %% Cellule 18 — Pipeline final : catégories natives et gradient boosting
# === CELLULE 18 : Pipeline gradient boosting ===
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OrdinalEncoder

COLONNES = ["site_id"] + VARIABLES
prep_hgb = make_column_transformer(
    (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan), ["site_id"]),
    remainder="passthrough",
)
pipe_hgb = make_pipeline(prep_hgb, HistGradientBoostingRegressor(categorical_features=[0], random_state=0))
pipe_hgb.fit(train[COLONNES], train["conso_mw"])

p_pipe = pipe_hgb.predict(test[COLONNES])
resultats["gradient boosting + pipeline"] = evaluer(test["conso_mw"], p_pipe)
print(pd.Series(resultats["gradient boosting + pipeline"]).round(3).to_dict())

# %% Cellule 19 — Prévision contre réalité sur la semaine de test
# === CELLULE 19 : Figure prévision ===
import matplotlib.pyplot as plt
from pathlib import Path

Path("out").mkdir(exist_ok=True)
t = test.assign(prevu=p_pipe)
s = t[t["site_id"] == "SITE_IND_001"]

fig, ax = plt.subplots(figsize=(10, 3.8))
ax.plot(s["timestamp"], s["conso_mw"], color="#1f77b4", linewidth=1.4, label="réel")
ax.plot(s["timestamp"], s["prevu"], color="#d62728", linewidth=1.2, label="gradient boosting")
ax.plot(s["timestamp"], s["lag_168"], color="#7f7f7f", linewidth=1, linestyle=":", label="semaine dernière")
ax.set_title("SITE_IND_001 : semaine du 24 au 30 janvier")
ax.set_ylabel("MW")
ax.set_ylim(0.6, 4.0)
ax.legend(loc="upper right", ncol=3)
ax.grid(alpha=0.3)
fig.autofmt_xdate()
fig.savefig("out/fig_prevision.png", dpi=110, bbox_inches="tight")

# %% Cellule 20 — L'erreur site par site
# === CELLULE 20 : Erreur par site ===
t = test.assign(prevu=p_pipe, erreur=lambda x: (x["conso_mw"] - x["prevu"]).abs())
par_site = t.groupby("site_id").agg(niveau_mw=("conso_mw", "mean"), mae_mw=("erreur", "mean"))
par_site["mae_relative"] = (par_site["mae_mw"] / par_site["niveau_mw"]).map("{:.1%}".format)
print(par_site.round(3))

# %% Cellule 21 — Enregistrer la préparation dans un module
# === CELLULE 21 : prevision_conso.py ===
from pathlib import Path

Path("prevision_conso.py").write_text('''"""prevision_conso.py — Préparation, évaluation et modèle de prévision (Workshop 3)."""
import numpy as np
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder

import qualite_pandas as qp

VARIABLES = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]
COLONNES = ["site_id"] + VARIABLES
DEBUT_UTILE = pd.Timestamp("2025-01-08")
COUPURE = pd.Timestamp("2025-01-24")


def charger_propre(mesures="data/consommation_30jours.csv", reference="data/sites_reference.csv"):
    """Mesures nettoyées (Workshop 2), avec type et capacité des sites."""
    brut = pd.read_csv(mesures, encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
    ref = pd.read_csv(reference, encoding="utf-8-sig")[["site_id", "site_type", "capacity_mw"]]
    return qp.nettoyer(brut).merge(ref, on="site_id", how="left", validate="m:1")


def ajouter_variables(d):
    """Cible sans pics, variables de calendrier, valeurs décalées, moyenne glissante."""
    d = d.copy()
    d["conso_brute"] = d["conso_mw"]
    d["pic"] = d["conso_mw"] > d["capacity_mw"]
    d["conso_mw"] = d["conso_mw"].mask(d["pic"])
    d["heure"] = d["timestamp"].dt.hour
    d["jour_sem"] = d["timestamp"].dt.dayofweek
    d["weekend"] = (d["jour_sem"] >= 5).astype(int)
    d["taux"] = d["conso_mw"] / d["capacity_mw"]
    g = d.groupby("site_id")["conso_mw"]
    d["lag_24"] = g.shift(24)
    d["lag_168"] = g.shift(168)
    d["moy_veille"] = g.transform(lambda s: s.shift(24).rolling(24, min_periods=12).mean())
    return d


def preparer(**chemins):
    return ajouter_variables(charger_propre(**chemins))


def decouper(d, coupure=COUPURE):
    """Passé pour apprendre, futur (lags complets) pour tester."""
    utile = d[(d["timestamp"] >= DEBUT_UTILE) & d["conso_mw"].notna()]
    return (utile[utile["timestamp"] < coupure],
            utile[utile["timestamp"] >= coupure].dropna(subset=["lag_24", "lag_168"]))


def evaluer(y_vrai, y_pred):
    return {"MAE": mean_absolute_error(y_vrai, y_pred),
            "RMSE": root_mean_squared_error(y_vrai, y_pred),
            "R2": r2_score(y_vrai, y_pred)}


def construire_modele(**params):
    """Pipeline final : site encodé comme catégorie + gradient boosting."""
    prep = make_column_transformer(
        (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan), ["site_id"]),
        remainder="passthrough",
    )
    return make_pipeline(prep, HistGradientBoostingRegressor(categorical_features=[0], random_state=0, **params))
''', encoding="utf-8")
print(Path("prevision_conso.py").stat().st_size, "octets écrits")

# %% Cellule 22 — Vérifier que le module reproduit la préparation
# === CELLULE 22 : Contrôle du module ===
import importlib
importlib.invalidate_caches()

import prevision_conso as pc

d2 = pc.preparer()
colonnes = ["timestamp", "site_id", "conso_mw", "heure", "weekend", "lag_24", "lag_168", "moy_veille"]
pd.testing.assert_frame_equal(d2[colonnes], d[colonnes])

tr2, te2 = pc.decouper(d2)
modele = pc.construire_modele().fit(tr2[pc.COLONNES], tr2["conso_mw"])
mae = pc.evaluer(te2["conso_mw"], modele.predict(te2[pc.COLONNES]))["MAE"]
print(len(tr2), len(te2), "lignes | MAE :", round(mae, 3), "| identique à la Cellule 18 :", round(mae, 6) == round(resultats["gradient boosting + pipeline"]["MAE"], 6))
