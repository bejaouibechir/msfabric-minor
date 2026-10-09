"""Atelier 2 (venv-data) - cellules de reference. Chaque bloc "# %%" = une cellule du notebook atelier2."""

# %% Cellule 32 — Contrôle des bibliothèques disponibles
# === CELLULE 32 : Ce que voit le noyau actif ===
import importlib.metadata as metadata      # versions des paquets installés
import sys
from importlib.util import find_spec       # teste la présence d'un paquet sans l'importer

# --- 1. Quel Python exécute cette cellule ?
print("Interpréteur :", sys.executable)

# --- 2. Pour chaque paquet : absent, ou sa version
for nom in ("numpy", "pandas", "matplotlib", "seaborn", "pyarrow"):
    if find_spec(nom) is None:                        # None = introuvable dans cet environnement
        print(f"{nom:<11} ABSENT")
    else:
        print(f"{nom:<11} {metadata.version(nom)}")

# %% Cellule 33 — Importer pandas : l'erreur, puis la réussite
# === CELLULE 33 : Importer les bibliothèques de données ===
import numpy as np                       # calcul sur tableaux
import pandas as pd                      # tableaux de données (DataFrame)
import matplotlib                        # graphiques : bibliothèque de base
import matplotlib.pyplot as plt          # son interface de dessin
import seaborn as sns                    # graphiques statistiques

print("pandas", pd.__version__, "| matplotlib", matplotlib.__version__, "| seaborn", sns.__version__)

# %% Cellule 34 — Lire le fichier CSV avec `read_csv`
# === CELLULE 34 : read_csv ===
from pathlib import Path

df = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig")   # lecture, BOM retiré
print(df.shape)                       # (nombre de lignes, nombre de colonnes)
print(df.columns.tolist())            # noms des colonnes
print(df.head(4))                     # aperçu des 4 premières lignes

# %% Cellule 35 — Explorer : `info`, `dtypes`, `describe`
# === CELLULE 35 : Explorer le DataFrame ===
df.info()                                              # structure du tableau
print()
print(df["consumption_mw"].describe().round(3))        # statistiques de la colonne de consommation
print(df["status"].value_counts())                     # répartition des statuts

# %% Cellule 36 — `Series`, `loc` et `iloc`
# === CELLULE 36 : Séries, loc et iloc ===
s = df["consumption_mw"]                              # une colonne = une Series
print(type(s).__name__, s.dtype, len(s))              # type de l'objet, type des valeurs, nombre de valeurs

print(df.loc[0, "site_id"], "|", df.iloc[0, 1])       # même case : par étiquette, puis par position
print(df.iloc[0:3, 1:3])                              # lignes 0 à 2, colonnes 1 et 2
print(df.loc[df["site_id"] == "SITE_IND_001", "consumption_mw"].head(3).tolist())   # masque + colonne

# Les mêmes syntaxes que sur le Tableau de la Partie 3
print(len(df), "site_id" in df, list(df)[:3])         # __len__, __contains__, __iter__ (noms de colonnes)
print(df.site_id.equals(df["site_id"]))               # __getattr__ : df.site_id est df["site_id"]

# %% Cellule 37 — Filtrer : masques, `isin`, `between`, `query`
# === CELLULE 37 : Filtres ===
fort = df[df["consumption_mw"] > 3.5]                 # lignes au-dessus de 3,5 MW
print(len(fort), fort["site_id"].unique().tolist())   # combien, et de quels sites

# Deux conditions : parenthèses obligatoires autour de chacune
masque = (df["site_id"] == "SITE_IND_002") & (df["consumption_mw"] > 3.5)
print(masque.sum())                                   # True compte pour 1

print(df["site_id"].isin(["SITE_RES_001", "SITE_RES_002"]).sum())   # lignes des deux sites résidentiels
print(df["consumption_mw"].between(1, 2).sum())                     # mesures entre 1 et 2 MW

# La même sélection que « masque », écrite avec query
print(len(df.query("site_id == 'SITE_IND_002' and consumption_mw > 3.5")))

# %% Cellule 38 — Nouvelles colonnes : `assign`, `rename`, copie indépendante
# === CELLULE 38 : Colonnes, renommage, Copy-on-Write ===

# --- 1. Renommer une colonne (nom plus court)
df = df.rename(columns={"consumption_mw": "conso_mw"})

# --- 2. Ajouter une colonne « famille » : le 2e morceau de site_id (SITE_IND_001 -> IND)
df = df.assign(famille=lambda d: d["site_id"].str.split("_").str[1])      # d = le DataFrame en cours
print(df["famille"].value_counts().to_dict())

# --- 3. Copy-on-Write : on ajoute une colonne à un DataFrame dérivé ; l'original reste intact
sous = df[df["site_id"] == "SITE_IND_001"]                                # un sous-ensemble
sous = sous.assign(conso_kw=sous["conso_mw"] * 1000)                      # nouvelle colonne, en kW
print("colonne conso_kw dans df :", "conso_kw" in df.columns, "| dans sous :", "conso_kw" in sous.columns)

# --- 4. Modifier des lignes précises : ici, aucune valeur ne dépasse 100
df.loc[df["conso_mw"] > 100, "conso_mw"] = np.nan
print(df["conso_mw"].max())

# %% Cellule 39 — Types : `astype`, `category`, `to_numeric`
# === CELLULE 39 : Types et mémoire ===

# --- 1. Convertir en « category » les colonnes à peu de valeurs distinctes, et mesurer le gain
avant = df.memory_usage(deep=True).sum()                 # mémoire avant conversion (textes compris)
df["site_id"] = df["site_id"].astype("category")         # 6 valeurs distinctes sur 4 365 lignes
df["famille"] = df["famille"].astype("category")         # 3 valeurs distinctes
apres = df.memory_usage(deep=True).sum()                 # mémoire après conversion
print(f"{avant / 1024:.0f} Ko -> {apres / 1024:.0f} Ko")
print(df.dtypes)                                         # les nouveaux types

# --- 2. Convertir du texte en nombres : ce qui est illisible devient NaN au lieu de faire échouer
texte = pd.Series(["0.865", "abc", "", "1.2"])
print(pd.to_numeric(texte, errors="coerce").tolist())

# %% Cellule 40 — Codes erreur : `isin`, `mask`, `replace`
# === CELLULE 40 : Codes erreur en NaN ===
CODES = [-999, -888, -777]

# Compter avant de nettoyer
print(df["conso_mw"].isin(CODES).sum(), "codes erreur")
print(df.loc[df["conso_mw"].isin(CODES), "conso_mw"].value_counts().to_dict())

# Deux écritures du même nettoyage
nettoye = df["conso_mw"].mask(df["conso_mw"].isin(CODES))     # NaN là où la valeur est un code
equivalent = df["conso_mw"].replace(CODES, np.nan)            # remplace chaque code par NaN
print(nettoye.isna().sum(), nettoye.equals(equivalent))       # nombre de NaN, résultats identiques ?
print(nettoye.min(), nettoye.max())                           # plus aucune valeur négative

# %% Cellule 41 — Doublons : `duplicated` et `drop_duplicates`
# === CELLULE 41 : Doublons ===
print(df.duplicated().sum(), "doublons exacts")                                        # ligne entière identique
print(df.duplicated(subset=["timestamp", "site_id"]).sum(), "doublons sur (timestamp, site)")   # même instant, même site

# Afficher les deux copies de quelques doublons (keep=False marque toutes les copies)
exemple = df[df.duplicated(keep=False)].sort_values(["site_id", "timestamp"]).head(4)
print(exemple[["timestamp", "site_id", "conso_mw"]])

sans_doublons = df.drop_duplicates()                   # on garde la première copie
print(len(df), "->", len(sans_doublons))

# %% Cellule 42 — Dates : `to_datetime`, formats multiples, `dt`
# === CELLULE 42 : Dates ===

# --- 1. Les trois formats présents dans le fichier
FORMATS = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"]

# --- 2. Convertir : on essaie chaque format, et on garde ce qui a réussi
def parser_dates(serie):
    resultat = pd.Series(pd.NaT, index=serie.index, dtype="datetime64[us]")     # départ : que des NaT (dates absentes)
    for fmt in FORMATS:
        # to_datetime avec errors="coerce" donne NaT quand le format ne correspond pas ;
        # fillna garde ce qui est déjà converti et complète le reste
        resultat = resultat.fillna(pd.to_datetime(serie, format=fmt, errors="coerce"))
    return resultat

# --- 3. Vérifier : type obtenu, dates illisibles, période couverte
ts = parser_dates(sans_doublons["timestamp"])
print(ts.dtype, ts.isna().sum(), "dates illisibles")
print(ts.min(), "->", ts.max())

# --- 4. Le piège : « mixed » devine chaque date seule, souvent à tort ; on compte les écarts avec notre résultat
brut_txt = sans_doublons["timestamp"]
mixte = pd.to_datetime(brut_txt, format="mixed")                        # sans indication
mixte_fr = pd.to_datetime(brut_txt, format="mixed", dayfirst=True)      # en privilégiant le jour en premier
print("mixed              : dates fausses =", int((mixte != ts).sum()))
print("mixed + dayfirst   : dates fausses =", int((mixte_fr != ts).sum()))

# %% Cellule 43 — L'accesseur `.dt` et les fuseaux horaires
# === CELLULE 43 : Accesseur .dt et fuseaux ===
print(ts.dt.hour.head(3).tolist(), ts.dt.day_name().head(3).tolist())   # heure et nom du jour, sans boucle
print(ts.dt.dayofweek.value_counts().sort_index().to_dict())              # nombre de lignes par jour de semaine

utc = ts.dt.tz_localize("UTC")                        # les dates sont déclarées en UTC
paris = utc.dt.tz_convert("Europe/Paris")             # mêmes instants, vus à Paris
print(utc.iloc[0], "->", paris.iloc[0])
print(paris.dt.hour.iloc[0] - utc.dt.hour.iloc[0])    # décalage en heures (hiver : 1)

# %% Cellule 44 — Chaînes : l'accesseur `.str`
# === CELLULE 44 : Chaînes ===
ids = pd.Series(sans_doublons["site_id"].astype(str).unique())     # les 6 identifiants distincts
print(ids.str.replace("SITE_", "", regex=False).tolist())          # enlève le préfixe
print(ids.str.contains("IND").tolist())                            # quels sites sont industriels ?
print(ids.str.extract(r"SITE_(?P<famille>[A-Z]{3})_(?P<numero>\d+)"))   # deux colonnes : famille, numero

# %% Cellule 45 — Valeurs manquantes : compter et remplacer
# === CELLULE 45 : Manquants ===

# --- 1. DataFrame de travail : sans doublons, dates converties, codes remplacés par NaN
propre = sans_doublons.assign(timestamp=ts, conso_mw=nettoye[sans_doublons.index])
propre = propre.sort_values(["site_id", "timestamp"], ignore_index=True)     # tri par site puis par date

# --- 2. Compter les manquants : au total, puis en pourcentage par site
print(propre["conso_mw"].isna().sum(), "manquants au total")
print((propre.groupby("site_id", observed=True)["conso_mw"].apply(lambda s: s.isna().mean()) * 100).round(1).to_dict())

# --- 3. L'ancienne écriture : erreur en pandas 3, simple avertissement en pandas 2
import warnings
try:
    with warnings.catch_warnings():
        warnings.simplefilter("error")                 # un avertissement devient une erreur : même comportement dans les deux versions
        propre["conso_mw"].fillna(method="ffill")
except (TypeError, FutureWarning) as erreur:
    print(type(erreur).__name__, ":", str(erreur).split(". ")[0])

# --- 4. Comblement par interpolation, site par site (jamais d'un site à l'autre), trous de 3 heures maximum
comble = propre.groupby("site_id", observed=True)["conso_mw"].transform(lambda s: s.interpolate(limit=3))
print(propre["conso_mw"].isna().sum(), "->", comble.isna().sum())     # manquants avant -> après

# %% Cellule 46 — Un nettoyage lisible avec `pipe` et une fonction
# === CELLULE 46 : Fonction de nettoyage ===

# --- 1. Toutes les étapes dans une fonction : une étape par ligne, dans l'ordre
def nettoyer(brut: pd.DataFrame) -> pd.DataFrame:
    return (
        brut
        .drop_duplicates()                                                   # 1. doublons exacts
        .assign(
            timestamp=lambda d: parser_dates(d["timestamp"]),                # 2. dates converties (d = DataFrame en cours)
            conso_mw=lambda d: d["conso_mw"].mask(d["conso_mw"].isin(CODES)),   # 3. codes erreur -> NaN
        )
        .sort_values(["site_id", "timestamp"], ignore_index=True)            # 4. tri par site puis date
    )

# --- 2. On repart du fichier brut pour prouver que la fonction fait tout
brut = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
propre = brut.pipe(nettoyer)                     # pipe : équivaut à nettoyer(brut)

# --- 3. Contrôler le résultat
print(len(brut), "->", len(propre), "lignes")                                                   # doublons retirés
print(propre["conso_mw"].isna().sum(), "manquants,", propre["timestamp"].isna().sum(), "dates illisibles")
print(propre.dtypes)                                                                            # types corrects ?

# %% Cellule 47 — Vérifier avec le module de l'Atelier 1
# === CELLULE 47 : Comparaison avec analyse_sites.py ===
from analyse_sites import analyser                     # le script de l'Atelier 1, importé comme un module

# --- 1. Résultat de l'Atelier 1 (boucles Python) : taux d'anomalies par site
rapport = analyser(Path("data/consommation_30jours.csv"), Path("data/sites_reference.csv"))
ref = {s: v["taux_anomalies"] for s, v in rapport["sites"].items()}    # dictionnaire {site: taux}

# --- 2. Résultat pandas : proportion de NaN par site (un NaN = une mesure invalide ou manquante)
taux = propre.groupby("site_id", observed=True)["conso_mw"].apply(lambda s: round(s.isna().mean(), 3))

# --- 3. Comparaison côte à côte, puis verdict
print(pd.DataFrame({"pandas": taux, "atelier1": pd.Series(ref)}))     # deux colonnes, alignées par site
print("identiques :", taux.to_dict() == ref)                         # True si les deux méthodes donnent les mêmes taux
print(rapport["doublons_ecartes"], "doublons |", f"{rapport['taux_anomalies_global']:.1%} d'anomalies")

# %% Cellule 48 — `groupby` et agrégations nommées
# === CELLULE 48 : groupby et agg ===

# --- 1. Regrouper les lignes par site, puis calculer plusieurs statistiques en une seule passe
#     observed=True : on ne garde que les sites réellement présents (utile car site_id est de type « category »)
resume = propre.groupby("site_id", observed=True).agg(
    # syntaxe : nom_de_la_colonne_resultat=("colonne_source", "fonction")
    mesures=("conso_mw", "size"),        # nombre de lignes par site, NaN compris
    valides=("conso_mw", "count"),       # nombre de lignes non nulles (donc mesures - manquants)
    moyenne_mw=("conso_mw", "mean"),     # moyenne ; les NaN sont ignorés automatiquement
    mediane_mw=("conso_mw", "median"),   # valeur du milieu : peu sensible aux pics
    max_mw=("conso_mw", "max"),          # plus forte consommation observée
    ecart_type=("conso_mw", "std"),      # dispersion autour de la moyenne
).round(3)                               # arrondi à 3 décimales pour la lisibilité

# --- 2. Afficher le tableau : une ligne par site, une colonne par statistique
print(resume)

# %% Cellule 49 — `transform` : garder la forme du DataFrame
# === CELLULE 49 : transform ===

# --- 1. Préparer le regroupement : la colonne de consommation, découpée site par site
g = propre.groupby("site_id", observed=True)["conso_mw"]

# --- 2. Ajouter deux colonnes qui gardent le nombre de lignes d'origine (contrairement à agg)
propre = propre.assign(
    ecart_site=lambda d: d["conso_mw"] - g.transform("mean"),   # transform("mean") répète la moyenne du site sur chacune de ses lignes
    rang_site=g.rank(ascending=False, method="min"),            # 1 = plus forte valeur du site ; « min » : les égalités partagent le même rang
)

# --- 3. Contrôler : les 4 premières lignes avec les nouvelles colonnes
print(propre[["site_id", "timestamp", "conso_mw", "ecart_site", "rang_site"]].head(4).round({"conso_mw": 3, "ecart_site": 3}))

# --- 4. Les lignes de rang 1 : la plus forte consommation de chaque site
print(propre.nsmallest(2, "rang_site")[["site_id", "conso_mw", "rang_site"]])    # nsmallest : les 2 plus petits rangs

# %% Cellule 50 — Joindre le référentiel : `merge`
# === CELLULE 50 : merge ===

# --- 1. Charger le référentiel : une ligne par site (type, capacité, flexibilité)
sites = pd.read_csv("data/sites_reference.csv", encoding="utf-8-sig")   # utf-8-sig : gère l'éventuel BOM du fichier
print(sites[["site_id", "site_type", "capacity_mw", "flexible"]])       # les colonnes utiles pour la suite

# --- 2. Jointure : chaque mesure reçoit les colonnes de son site
#     on="site_id"    : la colonne commune aux deux tableaux
#     how="left"      : on garde toutes les mesures, même sans site connu
#     validate="m:1"  : erreur si un site apparaît deux fois dans le référentiel (sinon les lignes seraient dupliquées)
#     indicator=True  : ajoute une colonne « _merge » qui dit si la ligne a trouvé son site
complet = propre.merge(sites, on="site_id", how="left", validate="m:1", indicator=True)
print(len(propre), "->", len(complet), "| sans correspondance :", int((complet["_merge"] != "both").sum()))   # même nombre de lignes, 0 orpheline

# --- 3. Taux de charge = consommation / capacité ; on retire la colonne technique _merge devenue inutile
complet = complet.assign(taux_charge=lambda d: d["conso_mw"] / d["capacity_mw"]).drop(columns="_merge")

# --- 4. Contrôle : taux moyen et taux maximum de chaque site (au-dessus de 1 = dépassement de capacité)
print(complet.groupby("site_id", observed=True)["taux_charge"].agg(["mean", "max"]).round(3))

# %% Cellule 51 — Séries temporelles : `resample`
# === CELLULE 51 : resample ===

# --- 1. Les dates deviennent l'index : nécessaire pour resample, rolling et la sélection par date
serie = complet.set_index("timestamp")

# --- 2. Moyenne journalière par site
#     groupby("site_id") : un calcul par site, pour ne jamais mélanger deux sites
#     resample("D")      : regrouper les mesures horaires par jour (D = day)
#     unstack(0)         : place les sites en colonnes (un tableau jour x site)
jour = serie.groupby("site_id", observed=True)["conso_mw"].resample("D").mean().unstack(0)
print(jour.round(2).head(4))                          # les 4 premiers jours
print(jour.shape)                                     # (30 jours, 6 sites)

# --- 3. L'ancienne fréquence « H » : erreur en pandas 3, avertissement en pandas 2.2 ; on écrit « h »
import warnings
try:
    with warnings.catch_warnings():
        warnings.simplefilter("error")                 # un avertissement devient une erreur : même comportement dans les deux versions
        serie[serie["site_id"] == "SITE_IND_001"]["conso_mw"].resample("H").mean()   # « H » : l'ancien nom, à ne plus utiliser
except (ValueError, FutureWarning) as erreur:
    print(type(erreur).__name__, ":", str(erreur).split(". ")[0])   # nom de l'erreur et première phrase du message

# --- 4. Sélection par date grâce à l'index : tout ce qui date du 2 janvier
print(serie.loc["2025-01-02", "conso_mw"].size, "mesures le 2 janvier")   # 6 sites x 24 h = 144 attendues

# %% Cellule 52 — Fenêtres glissantes : `rolling`, `shift`, `diff`
# === CELLULE 52 : rolling, shift, diff ===

# --- 1. Isoler la série d'un seul site : rolling et shift supposent une suite continue dans le temps
ind1 = serie[serie["site_id"] == "SITE_IND_001"]["conso_mw"]

# --- 2. Moyenne glissante : chaque point devient la moyenne des 24 dernières heures
#     "24h"          : fenêtre définie par une durée (et non par un nombre de lignes)
#     min_periods=12 : il faut au moins 12 mesures dans la fenêtre, sinon le résultat reste NaN
lisse = ind1.rolling("24h", min_periods=12).mean()

# --- 3. Comparer côte à côte : la mesure, sa moyenne glissante et sa variation depuis l'heure précédente
#     diff() : valeur de l'heure - valeur de l'heure précédente
print(pd.DataFrame({"mesure": ind1, "moyenne_24h": lisse, "variation": ind1.diff()}).iloc[24:28].round(3))   # lignes 24 à 27

# --- 4. Écart moyen avec la même heure de la veille
#     shift(24) : décale la série de 24 lignes, donc chaque heure est alignée avec celle de la veille
#     abs()     : on ne garde que la taille de l'écart ; dropna() : les 24 premières heures n'ont pas de veille
print((ind1.shift(24) - ind1).abs().dropna().mean().round(3), "MW d'écart moyen avec la veille")

# %% Cellule 53 — `pivot_table` et `melt` : large et long
# === CELLULE 53 : pivot_table et melt ===

# --- 1. Ajouter une colonne « heure » (0 à 23), lue dans l'index de dates
serie = serie.assign(heure=serie.index.hour)

# --- 2. Format LARGE : une ligne par heure, une colonne par site, valeur = consommation moyenne
#     index="heure"   : ce qui devient les lignes
#     columns="site_id": ce qui devient les colonnes
#     aggfunc="mean"  : comment combiner les 30 jours d'une même heure
profil = serie.pivot_table(index="heure", columns="site_id", values="conso_mw", aggfunc="mean", observed=True)
print(profil.shape)                                   # (24 heures, 6 sites)
print(profil.round(2).iloc[[0, 8, 12, 19]])           # lignes choisies : minuit, 8 h, midi, 19 h

# --- 3. Format LONG : une ligne par couple (heure, site), le format attendu par seaborn
#     melt fait l'opération inverse de pivot_table
#     id_vars="heure" : la colonne conservée telle quelle ; les colonnes sites deviennent des lignes
long = profil.reset_index().melt(id_vars="heure", var_name="site_id", value_name="mw_moyen")
print(long.shape, long.columns.tolist())              # 24 x 6 = 144 lignes, 3 colonnes

# %% Cellule 54 — Classer : `pd.cut`, `crosstab`, groupes multiples
# === CELLULE 54 : cut, crosstab ===

# --- 1. Découper le taux de charge en 4 classes
#     bins   : les bornes (0-0,5 / 0,5-0,8 / 0,8-1,0 / au-delà de 1,0 = dépassement)
#     labels : le nom de chaque classe, dans l'ordre des intervalles
niveaux = pd.cut(complet["taux_charge"], bins=[0, 0.5, 0.8, 1.0, float("inf")],
                 labels=["NORMAL", "SOUTENU", "CRITIQUE", "DÉPASSEMENT"])
complet = complet.assign(niveau=niveaux)               # nouvelle colonne « niveau »
print(complet["niveau"].value_counts(sort=False))      # effectif de chaque classe (sort=False : ordre des classes conservé)

# --- 2. Tableau croisé : combien de lignes pour chaque couple (type de site, niveau) ?
print(pd.crosstab(complet["site_type"], complet["niveau"]))

# --- 3. Moyenne par type de site ET par flexibilité (regroupement sur deux colonnes)
print(complet.groupby(["site_type", "flexible"], observed=True)["conso_mw"].mean().round(3))

# %% Cellule 55 — matplotlib : figure, axe, courbe
# === CELLULE 55 : Première courbe ===

# --- 1. Préparer le dossier de sortie (sans erreur s'il existe déjà)
Path("out").mkdir(exist_ok=True)

# --- 2. Sélectionner une semaine (6 au 12 janvier) d'un seul site : trois conditions combinées avec &
semaine = complet[(complet["site_id"] == "SITE_IND_001") & (complet["timestamp"] >= "2025-01-06") & (complet["timestamp"] < "2025-01-13")]

# --- 3. Créer la figure : fig = la toile, ax = le graphique dessiné dessus
fig, ax = plt.subplots(figsize=(10, 3.6))              # figsize : largeur x hauteur en pouces

# --- 4. Dessiner la courbe et le seuil de capacité
ax.plot(semaine["timestamp"], semaine["conso_mw"], color="#1f77b4", linewidth=1.4, label="SITE_IND_001")   # x = dates, y = consommation
ax.axhline(5.0, color="#d62728", linestyle="--", linewidth=1, label="capacité 5 MW")                        # ligne horizontale pointillée

# --- 5. Habillage : titre, unité, légende, grille, dates lisibles
ax.set_title("Consommation horaire, semaine du 6 janvier")
ax.set_ylabel("MW")                                    # unité de l'axe vertical
ax.legend(loc="upper right", ncol=2)                   # légende en haut à droite, sur 2 colonnes
ax.grid(alpha=0.3)                                     # grille discrète (30 % d'opacité)
fig.autofmt_xdate()                                    # incline les dates pour qu'elles ne se chevauchent pas

# --- 6. Enregistrer l'image : dpi = netteté, bbox_inches="tight" = pas de marge inutile
fig.savefig("out/fig_courbe.png", dpi=110, bbox_inches="tight")

# %% Cellule 56 — Plusieurs graphiques : `subplots` et axes partagés
# === CELLULE 56 : Trois familles de sites ===

# --- 1. Regrouper les sites par famille : un dictionnaire {nom de la famille: liste de sites}
familles = {"Industrie": ["SITE_IND_001", "SITE_IND_002"],
            "Commercial": ["SITE_COM_001", "SITE_COM_002"],
            "Résidentiel": ["SITE_RES_001", "SITE_RES_002"]}

# --- 2. Créer 3 graphiques côte à côte (1 ligne, 3 colonnes)
#     sharey=True : même échelle verticale, pour comparer les familles honnêtement
#     axes est une liste de 3 graphiques, un par famille
fig, axes = plt.subplots(1, 3, figsize=(12, 3.4), sharey=True)

# --- 3. Remplir chaque graphique : zip associe un graphique à une famille
for ax, (nom, sites_famille) in zip(axes, familles.items()):
    for s in sites_famille:
        # profil = tableau heure x site de la cellule précédente ; marker="o" : un point par heure
        ax.plot(profil.index, profil[s], marker="o", markersize=3, label=s[-7:])   # s[-7:] : les 7 derniers caractères (ex. IND_001)
    ax.set_title(nom)                                  # titre du graphique = nom de la famille
    ax.set_xlabel("heure")
    ax.legend()

# --- 4. Finitions
axes[0].set_ylabel("MW moyen")                         # un seul libellé vertical, sur le graphique de gauche
fig.tight_layout()                                     # ajuste les marges pour éviter tout chevauchement
fig.savefig("out/fig_familles.png", dpi=110, bbox_inches="tight")

# %% Cellule 57 — seaborn : `lineplot` avec `hue`
# === CELLULE 57 : lineplot ===

# --- 1. Style global de seaborn, valable pour tous les graphiques suivants
#     style="whitegrid" : fond blanc avec quadrillage ; palette="colorblind" : couleurs distinctes pour les daltoniens
sns.set_theme(style="whitegrid", palette="colorblind")

# --- 2. Une courbe par site, à partir du DataFrame au format long de la cellule précédente
fig, ax = plt.subplots(figsize=(9, 3.8))
#     x, y : les colonnes à placer sur les axes ; hue : une couleur (donc une courbe) par valeur de site_id
sns.lineplot(data=long, x="heure", y="mw_moyen", hue="site_id", ax=ax)

# --- 3. Habillage et enregistrement
ax.set_title("Profil horaire moyen par site")
ax.set_ylabel("MW moyen")
ax.legend(title="", fontsize=8, ncol=2)               # légende sur 2 colonnes, sans titre, en petits caractères
fig.savefig("out/fig_profils.png", dpi=110, bbox_inches="tight")

# %% Cellule 58 — Distributions : `boxplot` et repérage des anomalies
# === CELLULE 58 : boxplot ===

# --- 1. Créer la figure et son graphique
fig, ax = plt.subplots(figsize=(9, 3.8))

# --- 2. Une boîte par site : la boîte = 50 % des valeurs, la barre = médiane, les points = valeurs extrêmes
#     x = catégorie (site), y = valeur mesurée ; fliersize : taille des points extrêmes
sns.boxplot(data=complet, x="site_id", y="taux_charge", ax=ax, color="#8fb8de", fliersize=3)

# --- 3. Repère : ligne à 1 = 100 % de la capacité ; au-dessus, la mesure est physiquement impossible
ax.axhline(1, color="#d62728", linestyle="--", linewidth=1)

# --- 4. Habillage et enregistrement
ax.set_ylabel("taux de charge")
ax.set_xlabel("")                                      # pas de titre d'axe : les noms de sites suffisent
ax.tick_params(axis="x", labelrotation=20)             # noms des sites inclinés de 20 degrés
fig.savefig("out/fig_boxplot.png", dpi=110, bbox_inches="tight")

# --- 5. Compter les dépassements par site pour confirmer ce que montre le graphique
print(complet.loc[complet["taux_charge"] > 1, "site_id"].value_counts().to_dict())

# %% Cellule 59 — Carte de chaleur : jour × heure
# === CELLULE 59 : heatmap ===

# --- 1. Ne garder qu'un site, et ajouter deux colonnes lues dans la date : le jour du mois et l'heure
un_site = complet[complet["site_id"] == "SITE_IND_001"].assign(
    jour=lambda d: d["timestamp"].dt.day,              # .dt.day : jour du mois (1 à 30)
    heure=lambda d: d["timestamp"].dt.hour)            # .dt.hour : heure (0 à 23)

# --- 2. Tableau jours (lignes) x heures (colonnes) ; chaque case = consommation moyenne du jour à cette heure
grille = un_site.pivot_table(index="jour", columns="heure", values="conso_mw", aggfunc="mean")

# --- 3. Dessiner : une couleur par case (plus foncé = plus forte consommation)
fig, ax = plt.subplots(figsize=(10, 5.2))
#     cmap="Blues" : dégradé de bleus ; cbar_kws : titre de la barre de couleurs ; les cases blanches sont des NaN
sns.heatmap(grille, cmap="Blues", cbar_kws={"label": "MW"}, ax=ax)
ax.set_title("SITE_IND_001 : consommation par jour et par heure")

# --- 4. Enregistrer, puis contrôler la forme du tableau
fig.savefig("out/fig_heatmap.png", dpi=110, bbox_inches="tight")
print(grille.shape)                                  # (30 jours, 24 heures)

# %% Cellule 60 — Histogramme par famille de sites
# === CELLULE 60 : histplot ===

# --- 1. Créer la figure
fig, ax = plt.subplots(figsize=(9, 3.6))

# --- 2. Histogramme du taux de charge, un par famille de sites
#     hue="site_type"       : une couleur par famille
#     bins=40               : 40 tranches de valeurs
#     element="step"        : contours plutôt que barres pleines (les familles se lisent même superposées)
#     stat="probability"    : hauteur = part des mesures (et non un simple compte)
#     common_norm=False     : chaque famille est ramenée à 100 % séparément, pour comparer leurs formes
sns.histplot(data=complet, x="taux_charge", hue="site_type", bins=40, element="step",
             stat="probability", common_norm=False, ax=ax)

# --- 3. Habillage et enregistrement
ax.set_xlabel("taux de charge")
fig.savefig("out/fig_histogramme.png", dpi=110, bbox_inches="tight")

# --- 4. Médiane du taux de charge par famille : la valeur « typique », insensible aux pics
print(complet.groupby("site_type", observed=True)["taux_charge"].median().round(3).to_dict())

# %% Cellule 61 — Exporter : CSV, Parquet et relecture
# === CELLULE 61 : Exports ===

# --- 1. Choisir les colonnes utiles, puis écrire dans deux formats
final = complet[["timestamp", "site_id", "site_type", "conso_mw", "taux_charge", "niveau"]]
final.to_csv("out/mesures_propres.csv", index=False, encoding="utf-8-sig")   # CSV : lisible dans Excel ; index=False : sans numéros de ligne
final.to_parquet("out/mesures_propres.parquet", index=False)                 # Parquet : binaire, typé et compressé

# --- 2. Comparer le poids des deux fichiers
for nom in ("mesures_propres.csv", "mesures_propres.parquet"):
    print(f"{nom:<25} {Path('out', nom).stat().st_size / 1024:7.0f} Ko")     # taille en octets / 1024 = Ko

# --- 3. Relire les deux fichiers : les types survivent-ils ?
lu_csv = pd.read_csv("out/mesures_propres.csv", encoding="utf-8-sig")
lu_pq = pd.read_parquet("out/mesures_propres.parquet")
print(lu_csv["timestamp"].dtype, "|", lu_pq["timestamp"].dtype)     # CSV : texte ; Parquet : vrai datetime
print(lu_pq["niveau"].dtype)                                        # la catégorie est conservée par Parquet

# %% Étape manuelle — Créer le module `qualite_pandas.py`
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('qualite_pandas.py', 'w', encoding='utf-8') as f:
    f.write('"""qualite_pandas.py — Nettoyage des mesures EnergiaNord avec pandas (Atelier 2)."""\nimport pandas as pd\n\nCODES = (-999, -888, -777)\nFORMATS = ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S")\n\n\ndef parser_dates(serie: pd.Series) -> pd.Series:\n    """Convertit des timestamps en 3 formats ; NaT si aucun format ne convient."""\n    resultat = pd.Series(pd.NaT, index=serie.index, dtype="datetime64[us]")\n    for fmt in FORMATS:\n        resultat = resultat.fillna(pd.to_datetime(serie, format=fmt, errors="coerce"))\n    return resultat\n\n\ndef nettoyer(brut: pd.DataFrame) -> pd.DataFrame:\n    """Doublons exacts, dates, codes erreur en NaN, tri par site et date."""\n    return (\n        brut\n        .drop_duplicates()\n        .assign(\n            timestamp=lambda d: parser_dates(d["timestamp"]),\n            conso_mw=lambda d: d["conso_mw"].mask(d["conso_mw"].isin(CODES)),\n        )\n        .sort_values(["site_id", "timestamp"], ignore_index=True)\n    )\n\n\ndef resume_sites(propre: pd.DataFrame) -> pd.DataFrame:\n    """Mesures, valides, taux d\'anomalies et consommation moyenne par site."""\n    return propre.groupby("site_id", observed=True).agg(\n        mesures=("conso_mw", "size"),\n        valides=("conso_mw", "count"),\n        moyenne_mw=("conso_mw", "mean"),\n    ).assign(taux_anomalies=lambda d: (1 - d["valides"] / d["mesures"]).round(3)).round(3)\n')
print('qualite_pandas.py', ':', len(open('qualite_pandas.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 62 — Importer et réutiliser le module
# === CELLULE 62 : Réutiliser qualite_pandas ===
import importlib, sys
from pathlib import Path

# --- 1. Préparer l'import : dossier de travail dans sys.path, et cache des dossiers rafraîchi
if str(Path.cwd()) not in sys.path:
    sys.path.insert(0, str(Path.cwd()))               # Python cherchera d'abord dans ce dossier
importlib.invalidate_caches()                         # le fichier vient d'être créé : Python doit re-scanner le dossier
print("qualite_pandas.py présent :", Path("qualite_pandas.py").exists(), "| dossier :", Path.cwd().name)   # doit afficher True

# --- 2. Importer votre module sous un nom court
import qualite_pandas as qp

# --- 3. Repartir du fichier brut, comme le ferait n'importe quel autre notebook
brut2 = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})

# --- 4. Appeler les fonctions du module : plus aucune étape de nettoyage écrite dans le notebook
propre2 = qp.nettoyer(brut2)                          # doublons, dates, codes erreur, tri : tout est dans la fonction
print(qp.resume_sites(propre2))                       # tableau récapitulatif par site
print(len(propre2), "lignes | module :", qp.__name__)   # __name__ : nom sous lequel le module est connu

# %% Cellule 63 — Envelopper un DataFrame avec __getattr__
# === CELLULE 63 : Un wrapper autour d'un DataFrame ===

# --- 1. La classe : un DataFrame à l'intérieur, une méthode métier à l'extérieur
class SuiviSite:
    def __init__(self, df):
        self._df = df                                     # le DataFrame enveloppé

    def __repr__(self):                                   # affichage court dans le notebook
        return f"SuiviSite({len(self)} mesures, {self._df['site_id'].nunique()} sites)"

    def __len__(self):
        return len(self._df)

    def __getitem__(self, cle):                           # suivi["conso_mw"], suivi[masque]... : délégué à pandas
        return self._df[cle]

    def __getattr__(self, nom):                           # appelée seulement si l'attribut n'existe pas ici
        if nom == "_df":                                  # évite une boucle infinie pendant la construction
            raise AttributeError(nom)
        return getattr(self._df, nom)                     # sinon : on demande au DataFrame

    def taux_anomalies(self):                             # méthode métier ajoutée par le wrapper
        return self._df["conso_mw"].isna().mean().round(3)

# --- 2. Utilisation sur le DataFrame nettoyé de la cellule précédente
suivi = SuiviSite(propre2)
print(suivi)                                              # __repr__
print(len(suivi), "|", suivi.shape)                       # __len__, puis .shape : délégué au DataFrame
print(suivi.taux_anomalies())                             # méthode du wrapper
print(suivi["conso_mw"].max())                            # __getitem__ délégué
print(suivi.head(2))                                      # .head() : jamais défini dans la classe

# %% Cellule 64 — Un chargement portable : local et Fabric
# === CELLULE 64 : Chargement portable ===
from importlib.util import find_spec

# --- 1. Détecter l'environnement : le module notebookutils n'existe que dans Fabric
DANS_FABRIC = find_spec("notebookutils") is not None   # find_spec cherche le module sans l'importer (donc sans erreur)

# --- 2. Une seule fonction porte la différence entre les deux mondes
def charger_mesures(nom="consommation_30jours.csv") -> pd.DataFrame:
    # Dossier du Lakehouse dans Fabric, dossier data/ en local
    dossier = Path("/lakehouse/default/Files/data_python") if DANS_FABRIC else Path("data")
    # Le reste de la lecture est identique partout : c'est le but
    return pd.read_csv(dossier / nom, encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})

# --- 3. Utilisation : le code appelant ne change pas d'un environnement à l'autre
mesures = charger_mesures()
print(f"Dans Fabric : {DANS_FABRIC} | {len(mesures)} lignes | {len(qp.nettoyer(mesures))} après nettoyage")   # qp = module de la cellule précédente
