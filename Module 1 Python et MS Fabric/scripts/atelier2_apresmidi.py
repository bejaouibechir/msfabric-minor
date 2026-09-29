"""Atelier 2 (apres-midi : venv-data) - cellules de reference. Chaque bloc "# %%" = une cellule du notebook atelier2."""

# %% Cellule 26 — Contrôle des bibliothèques disponibles
# === CELLULE 26 : Ce que voit le noyau actif ===
import importlib.metadata as metadata
import sys
from importlib.util import find_spec

print("Interpréteur :", sys.executable)
for nom in ("numpy", "pandas", "matplotlib", "seaborn", "pyarrow"):
    if find_spec(nom) is None:
        print(f"{nom:<11} ABSENT")
    else:
        print(f"{nom:<11} {metadata.version(nom)}")

# %% Cellule 27 — Importer pandas : l'erreur, puis la réussite
# === CELLULE 27 : Importer les bibliothèques de données ===
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

print("pandas", pd.__version__, "| matplotlib", matplotlib.__version__, "| seaborn", sns.__version__)

# %% Cellule 28 — Lire le fichier CSV avec `read_csv`
# === CELLULE 28 : read_csv ===
from pathlib import Path

df = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig")
print(df.shape)
print(df.columns.tolist())
print(df.head(4))

# %% Cellule 29 — Explorer : `info`, `dtypes`, `describe`
# === CELLULE 29 : Explorer le DataFrame ===
df.info()
print()
print(df["consumption_mw"].describe().round(3))
print(df["status"].value_counts())

# %% Cellule 30 — `Series`, `loc` et `iloc`
# === CELLULE 30 : Séries, loc et iloc ===
s = df["consumption_mw"]
print(type(s).__name__, s.dtype, len(s))
print(df.loc[0, "site_id"], "|", df.iloc[0, 1])
print(df.iloc[0:3, 1:3])
print(df.loc[df["site_id"] == "SITE_IND_001", "consumption_mw"].head(3).tolist())

# %% Cellule 31 — Filtrer : masques, `isin`, `between`, `query`
# === CELLULE 31 : Filtres ===
fort = df[df["consumption_mw"] > 3.5]
print(len(fort), fort["site_id"].unique().tolist())

masque = (df["site_id"] == "SITE_IND_002") & (df["consumption_mw"] > 3.5)
print(masque.sum())
print(df["site_id"].isin(["SITE_RES_001", "SITE_RES_002"]).sum())
print(df["consumption_mw"].between(1, 2).sum())
print(len(df.query("site_id == 'SITE_IND_002' and consumption_mw > 3.5")))

# %% Cellule 32 — Nouvelles colonnes : `assign`, `rename`, copie indépendante
# === CELLULE 32 : Colonnes, renommage, Copy-on-Write ===
df = df.rename(columns={"consumption_mw": "conso_mw"})
df = df.assign(famille=lambda d: d["site_id"].str.split("_").str[1])
print(df["famille"].value_counts().to_dict())

sous = df[df["site_id"] == "SITE_IND_001"]
sous = sous.assign(conso_kw=sous["conso_mw"] * 1000)
print("colonne conso_kw dans df :", "conso_kw" in df.columns, "| dans sous :", "conso_kw" in sous.columns)

df.loc[df["conso_mw"] > 100, "conso_mw"] = np.nan
print(df["conso_mw"].max())

# %% Cellule 33 — Types : `astype`, `category`, `to_numeric`
# === CELLULE 33 : Types et mémoire ===
avant = df.memory_usage(deep=True).sum()
df["site_id"] = df["site_id"].astype("category")
df["famille"] = df["famille"].astype("category")
apres = df.memory_usage(deep=True).sum()
print(f"{avant / 1024:.0f} Ko -> {apres / 1024:.0f} Ko")
print(df.dtypes)

texte = pd.Series(["0.865", "abc", "", "1.2"])
print(pd.to_numeric(texte, errors="coerce").tolist())

# %% Cellule 34 — Codes erreur : `isin`, `mask`, `replace`
# === CELLULE 34 : Codes erreur en NaN ===
CODES = [-999, -888, -777]
print(df["conso_mw"].isin(CODES).sum(), "codes erreur")
print(df.loc[df["conso_mw"].isin(CODES), "conso_mw"].value_counts().to_dict())

nettoye = df["conso_mw"].mask(df["conso_mw"].isin(CODES))
equivalent = df["conso_mw"].replace(CODES, np.nan)
print(nettoye.isna().sum(), nettoye.equals(equivalent))
print(nettoye.min(), nettoye.max())

# %% Cellule 35 — Doublons : `duplicated` et `drop_duplicates`
# === CELLULE 35 : Doublons ===
print(df.duplicated().sum(), "doublons exacts")
print(df.duplicated(subset=["timestamp", "site_id"]).sum(), "doublons sur (timestamp, site)")

exemple = df[df.duplicated(keep=False)].sort_values(["site_id", "timestamp"]).head(4)
print(exemple[["timestamp", "site_id", "conso_mw"]])

sans_doublons = df.drop_duplicates()
print(len(df), "->", len(sans_doublons))

# %% Cellule 36 — Dates : `to_datetime`, formats multiples, `dt`
# === CELLULE 36 : Dates ===
FORMATS = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"]

def parser_dates(serie):
    resultat = pd.Series(pd.NaT, index=serie.index, dtype="datetime64[us]")
    for fmt in FORMATS:
        resultat = resultat.fillna(pd.to_datetime(serie, format=fmt, errors="coerce"))
    return resultat

ts = parser_dates(sans_doublons["timestamp"])
print(ts.dtype, ts.isna().sum(), "dates illisibles")
print(ts.min(), "->", ts.max())

brut_txt = sans_doublons["timestamp"]
mixte = pd.to_datetime(brut_txt, format="mixed")
mixte_fr = pd.to_datetime(brut_txt, format="mixed", dayfirst=True)
print("mixed              : dates fausses =", int((mixte != ts).sum()))
print("mixed + dayfirst   : dates fausses =", int((mixte_fr != ts).sum()))

# %% Cellule 37 — L'accesseur `.dt` et les fuseaux horaires
# === CELLULE 37 : Accesseur .dt et fuseaux ===
print(ts.dt.hour.head(3).tolist(), ts.dt.day_name().head(3).tolist())
print(ts.dt.dayofweek.value_counts().sort_index().to_dict())

utc = ts.dt.tz_localize("UTC")
paris = utc.dt.tz_convert("Europe/Paris")
print(utc.iloc[0], "->", paris.iloc[0])
print(paris.dt.hour.iloc[0] - utc.dt.hour.iloc[0])

# %% Cellule 38 — Chaînes : l'accesseur `.str`
# === CELLULE 38 : Chaînes ===
ids = pd.Series(sans_doublons["site_id"].astype(str).unique())
print(ids.str.replace("SITE_", "", regex=False).tolist())
print(ids.str.contains("IND").tolist())
print(ids.str.extract(r"SITE_(?P<famille>[A-Z]{3})_(?P<numero>\d+)"))

# %% Cellule 39 — Valeurs manquantes : compter et remplacer
# === CELLULE 39 : Manquants ===
propre = sans_doublons.assign(timestamp=ts, conso_mw=nettoye[sans_doublons.index])
propre = propre.sort_values(["site_id", "timestamp"], ignore_index=True)

print(propre["conso_mw"].isna().sum(), "manquants au total")
print((propre.groupby("site_id", observed=True)["conso_mw"].apply(lambda s: s.isna().mean()) * 100).round(1).to_dict())

try:
    propre["conso_mw"].fillna(method="ffill")
except TypeError as erreur:
    print("TypeError :", erreur)

comble = propre.groupby("site_id", observed=True)["conso_mw"].transform(lambda s: s.interpolate(limit=3))
print(propre["conso_mw"].isna().sum(), "->", comble.isna().sum())

# %% Cellule 40 — Un nettoyage lisible avec `pipe` et une fonction
# === CELLULE 40 : Fonction de nettoyage ===
def nettoyer(brut: pd.DataFrame) -> pd.DataFrame:
    return (
        brut
        .drop_duplicates()
        .assign(
            timestamp=lambda d: parser_dates(d["timestamp"]),
            conso_mw=lambda d: d["conso_mw"].mask(d["conso_mw"].isin(CODES)),
        )
        .sort_values(["site_id", "timestamp"], ignore_index=True)
    )

brut = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
propre = brut.pipe(nettoyer)
print(len(brut), "->", len(propre), "lignes")
print(propre["conso_mw"].isna().sum(), "manquants,", propre["timestamp"].isna().sum(), "dates illisibles")
print(propre.dtypes)

# %% Cellule 41 — Vérifier avec le module de l'Atelier 1
# === CELLULE 41 : Comparaison avec analyse_sites.py ===
from analyse_sites import analyser

rapport = analyser(Path("data/consommation_30jours.csv"), Path("data/sites_reference.csv"))
ref = {s: v["taux_anomalies"] for s, v in rapport["sites"].items()}

taux = propre.groupby("site_id", observed=True)["conso_mw"].apply(lambda s: round(s.isna().mean(), 3))
print(pd.DataFrame({"pandas": taux, "atelier1": pd.Series(ref)}))
print("identiques :", taux.to_dict() == ref)
print(rapport["doublons_ecartes"], "doublons |", f"{rapport['taux_anomalies_global']:.1%} d'anomalies")

# %% Cellule 42 — `groupby` et agrégations nommées
# === CELLULE 42 : groupby et agg ===
resume = propre.groupby("site_id", observed=True).agg(
    mesures=("conso_mw", "size"),
    valides=("conso_mw", "count"),
    moyenne_mw=("conso_mw", "mean"),
    mediane_mw=("conso_mw", "median"),
    max_mw=("conso_mw", "max"),
    ecart_type=("conso_mw", "std"),
).round(3)
print(resume)

# %% Cellule 43 — `transform` : garder la forme du DataFrame
# === CELLULE 43 : transform ===
g = propre.groupby("site_id", observed=True)["conso_mw"]
propre = propre.assign(
    ecart_site=lambda d: d["conso_mw"] - g.transform("mean"),
    rang_site=g.rank(ascending=False, method="min"),
)
print(propre[["site_id", "timestamp", "conso_mw", "ecart_site", "rang_site"]].head(4).round({"conso_mw": 3, "ecart_site": 3}))
print(propre.nsmallest(2, "rang_site")[["site_id", "conso_mw", "rang_site"]])

# %% Cellule 44 — Joindre le référentiel : `merge`
# === CELLULE 44 : merge ===
sites = pd.read_csv("data/sites_reference.csv", encoding="utf-8-sig")
print(sites[["site_id", "site_type", "capacity_mw", "flexible"]])

complet = propre.merge(sites, on="site_id", how="left", validate="m:1", indicator=True)
print(len(propre), "->", len(complet), "| sans correspondance :", int((complet["_merge"] != "both").sum()))

complet = complet.assign(taux_charge=lambda d: d["conso_mw"] / d["capacity_mw"]).drop(columns="_merge")
print(complet.groupby("site_id", observed=True)["taux_charge"].agg(["mean", "max"]).round(3))

# %% Cellule 45 — Séries temporelles : `resample`
# === CELLULE 45 : resample ===
serie = complet.set_index("timestamp")
jour = serie.groupby("site_id", observed=True)["conso_mw"].resample("D").mean().unstack(0)
print(jour.round(2).head(4))
print(jour.shape)

try:
    serie[serie["site_id"] == "SITE_IND_001"]["conso_mw"].resample("H").mean()
except ValueError as erreur:
    print("ValueError :", str(erreur).split(". ")[0])
print(serie.loc["2025-01-02", "conso_mw"].size, "mesures le 2 janvier")

# %% Cellule 46 — Fenêtres glissantes : `rolling`, `shift`, `diff`
# === CELLULE 46 : rolling, shift, diff ===
ind1 = serie[serie["site_id"] == "SITE_IND_001"]["conso_mw"]
lisse = ind1.rolling("24h", min_periods=12).mean()
print(pd.DataFrame({"mesure": ind1, "moyenne_24h": lisse, "variation": ind1.diff()}).iloc[24:28].round(3))
print((ind1.shift(24) - ind1).abs().dropna().mean().round(3), "MW d'écart moyen avec la veille")

# %% Cellule 47 — `pivot_table` et `melt` : large et long
# === CELLULE 47 : pivot_table et melt ===
serie = serie.assign(heure=serie.index.hour)
profil = serie.pivot_table(index="heure", columns="site_id", values="conso_mw", aggfunc="mean", observed=True)
print(profil.shape)
print(profil.round(2).iloc[[0, 8, 12, 19]])

long = profil.reset_index().melt(id_vars="heure", var_name="site_id", value_name="mw_moyen")
print(long.shape, long.columns.tolist())

# %% Cellule 48 — Classer : `pd.cut`, `crosstab`, groupes multiples
# === CELLULE 48 : cut, crosstab ===
niveaux = pd.cut(complet["taux_charge"], bins=[0, 0.5, 0.8, 1.0, float("inf")],
                 labels=["NORMAL", "SOUTENU", "CRITIQUE", "DÉPASSEMENT"])
complet = complet.assign(niveau=niveaux)
print(complet["niveau"].value_counts(sort=False))
print(pd.crosstab(complet["site_type"], complet["niveau"]))
print(complet.groupby(["site_type", "flexible"], observed=True)["conso_mw"].mean().round(3))

# %% Cellule 49 — matplotlib : figure, axe, courbe
# === CELLULE 49 : Première courbe ===
Path("out").mkdir(exist_ok=True)
semaine = complet[(complet["site_id"] == "SITE_IND_001") & (complet["timestamp"] >= "2025-01-06") & (complet["timestamp"] < "2025-01-13")]

fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(semaine["timestamp"], semaine["conso_mw"], color="#1f77b4", linewidth=1.4, label="SITE_IND_001")
ax.axhline(5.0, color="#d62728", linestyle="--", linewidth=1, label="capacité 5 MW")
ax.set_title("Consommation horaire, semaine du 6 janvier")
ax.set_ylabel("MW")
ax.legend(loc="upper right", ncol=2)
ax.grid(alpha=0.3)
fig.autofmt_xdate()
fig.savefig("out/fig_courbe.png", dpi=110, bbox_inches="tight")

# %% Cellule 50 — Plusieurs graphiques : `subplots` et axes partagés
# === CELLULE 50 : Trois familles de sites ===
familles = {"Industrie": ["SITE_IND_001", "SITE_IND_002"],
            "Commercial": ["SITE_COM_001", "SITE_COM_002"],
            "Résidentiel": ["SITE_RES_001", "SITE_RES_002"]}

fig, axes = plt.subplots(1, 3, figsize=(12, 3.4), sharey=True)
for ax, (nom, sites_famille) in zip(axes, familles.items()):
    for s in sites_famille:
        ax.plot(profil.index, profil[s], marker="o", markersize=3, label=s[-7:])
    ax.set_title(nom)
    ax.set_xlabel("heure")
    ax.legend()
axes[0].set_ylabel("MW moyen")
fig.tight_layout()
fig.savefig("out/fig_familles.png", dpi=110, bbox_inches="tight")

# %% Cellule 51 — seaborn : `lineplot` avec `hue`
# === CELLULE 51 : lineplot ===
sns.set_theme(style="whitegrid", palette="colorblind")

fig, ax = plt.subplots(figsize=(9, 3.8))
sns.lineplot(data=long, x="heure", y="mw_moyen", hue="site_id", ax=ax)
ax.set_title("Profil horaire moyen par site")
ax.set_ylabel("MW moyen")
ax.legend(title="", fontsize=8, ncol=2)
fig.savefig("out/fig_profils.png", dpi=110, bbox_inches="tight")

# %% Cellule 52 — Distributions : `boxplot` et repérage des anomalies
# === CELLULE 52 : boxplot ===
fig, ax = plt.subplots(figsize=(9, 3.8))
sns.boxplot(data=complet, x="site_id", y="taux_charge", ax=ax, color="#8fb8de", fliersize=3)
ax.axhline(1, color="#d62728", linestyle="--", linewidth=1)
ax.set_ylabel("taux de charge")
ax.set_xlabel("")
ax.tick_params(axis="x", labelrotation=20)
fig.savefig("out/fig_boxplot.png", dpi=110, bbox_inches="tight")
print(complet.loc[complet["taux_charge"] > 1, "site_id"].value_counts().to_dict())

# %% Cellule 53 — Carte de chaleur : jour × heure
# === CELLULE 53 : heatmap ===
un_site = complet[complet["site_id"] == "SITE_IND_001"].assign(jour=lambda d: d["timestamp"].dt.day, heure=lambda d: d["timestamp"].dt.hour)
grille = un_site.pivot_table(index="jour", columns="heure", values="conso_mw", aggfunc="mean")

fig, ax = plt.subplots(figsize=(10, 5.2))
sns.heatmap(grille, cmap="Blues", cbar_kws={"label": "MW"}, ax=ax)
ax.set_title("SITE_IND_001 : consommation par jour et par heure")
fig.savefig("out/fig_heatmap.png", dpi=110, bbox_inches="tight")
print(grille.shape)

# %% Cellule 54 — Histogramme par famille de sites
# === CELLULE 54 : histplot ===
fig, ax = plt.subplots(figsize=(9, 3.6))
sns.histplot(data=complet, x="taux_charge", hue="site_type", bins=40, element="step",
             stat="probability", common_norm=False, ax=ax)
ax.set_xlabel("taux de charge")
fig.savefig("out/fig_histogramme.png", dpi=110, bbox_inches="tight")
print(complet.groupby("site_type", observed=True)["taux_charge"].median().round(3).to_dict())

# %% Cellule 55 — Exporter : CSV, Parquet et relecture
# === CELLULE 55 : Exports ===
final = complet[["timestamp", "site_id", "site_type", "conso_mw", "taux_charge", "niveau"]]
final.to_csv("out/mesures_propres.csv", index=False, encoding="utf-8-sig")
final.to_parquet("out/mesures_propres.parquet", index=False)

for nom in ("mesures_propres.csv", "mesures_propres.parquet"):
    print(f"{nom:<25} {Path('out', nom).stat().st_size / 1024:7.0f} Ko")

lu_csv = pd.read_csv("out/mesures_propres.csv", encoding="utf-8-sig")
lu_pq = pd.read_parquet("out/mesures_propres.parquet")
print(lu_csv["timestamp"].dtype, "|", lu_pq["timestamp"].dtype)
print(lu_pq["niveau"].dtype)

# %% Cellule 56 — Ranger le nettoyage dans un module
# === CELLULE 56 : qualite_pandas.py ===
Path("qualite_pandas.py").write_text('''"""qualite_pandas.py — Nettoyage des mesures EnergiaNord avec pandas (Atelier 2)."""
import pandas as pd

CODES = (-999, -888, -777)
FORMATS = ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S")


def parser_dates(serie: pd.Series) -> pd.Series:
    """Convertit des timestamps en 3 formats ; NaT si aucun format ne convient."""
    resultat = pd.Series(pd.NaT, index=serie.index, dtype="datetime64[us]")
    for fmt in FORMATS:
        resultat = resultat.fillna(pd.to_datetime(serie, format=fmt, errors="coerce"))
    return resultat


def nettoyer(brut: pd.DataFrame) -> pd.DataFrame:
    """Doublons exacts, dates, codes erreur en NaN, tri par site et date."""
    return (
        brut
        .drop_duplicates()
        .assign(
            timestamp=lambda d: parser_dates(d["timestamp"]),
            conso_mw=lambda d: d["conso_mw"].mask(d["conso_mw"].isin(CODES)),
        )
        .sort_values(["site_id", "timestamp"], ignore_index=True)
    )


def resume_sites(propre: pd.DataFrame) -> pd.DataFrame:
    """Mesures, valides, taux d'anomalies et consommation moyenne par site."""
    return propre.groupby("site_id", observed=True).agg(
        mesures=("conso_mw", "size"),
        valides=("conso_mw", "count"),
        moyenne_mw=("conso_mw", "mean"),
    ).assign(taux_anomalies=lambda d: (1 - d["valides"] / d["mesures"]).round(3)).round(3)
''', encoding="utf-8")
print(Path("qualite_pandas.py").stat().st_size, "octets écrits")

# %% Cellule 57 — Importer et réutiliser le module
# === CELLULE 57 : Réutiliser qualite_pandas ===
import importlib
importlib.invalidate_caches()

import qualite_pandas as qp

brut2 = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
propre2 = qp.nettoyer(brut2)
print(qp.resume_sites(propre2))
print(len(propre2), "lignes | module :", qp.__name__)

# %% Cellule 58 — Un chargement portable : local et Fabric
# === CELLULE 58 : Chargement portable ===
from importlib.util import find_spec

DANS_FABRIC = find_spec("notebookutils") is not None

def charger_mesures(nom="consommation_30jours.csv") -> pd.DataFrame:
    dossier = Path("/lakehouse/default/Files/data_python") if DANS_FABRIC else Path("data")
    return pd.read_csv(dossier / nom, encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})

mesures = charger_mesures()
print(f"Dans Fabric : {DANS_FABRIC} | {len(mesures)} lignes | {len(qp.nettoyer(mesures))} après nettoyage")
