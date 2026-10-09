"""Workshop 3 (venv-ml) - cellules de reference. Chaque bloc "# %%" = une cellule du notebook workshop3."""

# %% Cellule 1 — Vérification de l'environnement
# === CELLULE 1 : Vérification de l'environnement ===
# --- 1. Importer les outils de la bibliothèque standard ---
import sys                                # informations sur l'interpréteur Python en cours
from importlib.metadata import version    # lit la version installée d'un paquet
from pathlib import Path                  # manipule les chemins de fichiers

# --- 2. Identifier Python et l'interpréteur utilisé ---
# split()[0] garde seulement le numéro de version (avant le premier espace)
print(f"Python       : {sys.version.split()[0]}")
# le chemin de python.exe indique quel environnement virtuel tourne (attendu : .venv-ml)
print(f"Interpréteur : {sys.executable}")

# --- 3. Lister les versions des bibliothèques clés ---
# boucle sur les quatre paquets ; version() lit le numéro installé dans l'environnement actif
for paquet in ("numpy", "pandas", "scikit-learn", "mlflow"):
    print(f"{paquet:<13}: {version(paquet)}")    # {paquet:<13} aligne les noms sur 13 caractères

# --- 4. Vérifier le dossier de travail et les fichiers attendus ---
print(f"Dossier      : {Path.cwd().name}")    # nom du dossier actif (cwd = dossier courant)
# glob("*.csv") liste les fichiers CSV de data/ ; sorted les trie par nom
print(f"Fichiers     : {sorted(p.name for p in Path('data').glob('*.csv'))}")
# on ne garde que les modules qui existent réellement dans le dossier actif
print(f"Modules      : {[p for p in ('energie_utils.py', 'qualite_pandas.py') if Path(p).exists()]}")

# %% Cellule 2 — Ce que voit chaque noyau
# === CELLULE 2 : Ce que voit le noyau actif ===
# --- 1. Importer les outils de détection de paquets ---
import sys                                    # pour afficher l'interpréteur du noyau actif
from importlib.metadata import version        # lit la version installée d'un paquet
from importlib.util import find_spec          # teste la présence d'un paquet sans l'importer

# --- 2. Afficher l'interpréteur du noyau ---
print("Interpréteur :", sys.executable)    # change selon le noyau choisi (venv-data ou venv-ml)

# --- 3. Tester chaque paquet ---
# chaque couple = (nom à importer, nom du paquet installé) ; ils diffèrent pour scikit-learn (sklearn)
for nom, paquet in (("pandas", "pandas"), ("matplotlib", "matplotlib"), ("seaborn", "seaborn"),
                    ("sklearn", "scikit-learn"), ("mlflow", "mlflow"), ("joblib", "joblib")):
    if find_spec(nom) is None:                       # None = le noyau ne trouve pas ce paquet
        print(f"{nom:<11} ABSENT")                   # paquet non installé dans cet environnement
    else:
        print(f"{nom:<11} {version(paquet)}")        # paquet présent : on affiche sa version

# %% Cellule 3 — Importer scikit-learn : l'erreur, puis la réussite
# === CELLULE 3 : Importer scikit-learn et MLflow ===
# --- 1. Importer les bibliothèques (échoue avec ModuleNotFoundError dans venv-data) ---
import pandas as pd                # tableaux de données (déjà présent dans venv-data)
import sklearn                     # scikit-learn : absent de venv-data, présent dans venv-ml
import mlflow                      # suivi des expériences (Partie 6)
# un modèle de prévision (gradient boosting) : l'import prouve que scikit-learn est complet
from sklearn.ensemble import HistGradientBoostingRegressor

# --- 2. Afficher les versions pour confirmer la réussite ---
# __version__ : numéro de version que chaque bibliothèque expose
print("pandas", pd.__version__, "| scikit-learn", sklearn.__version__, "| mlflow", mlflow.__version__)
# afficher un modèle non entraîné montre ses réglages par défaut (aucun calcul ici)
print(HistGradientBoostingRegressor())

# %% Cellule 4 — Charger et nettoyer avec le module de l'Workshop 2
# === CELLULE 4 : Charger et nettoyer ===
# --- 1. Importer les bibliothèques ---
import numpy as np                 # calcul numérique (utilisé plus loin, ex. NaN)
import pandas as pd                # lecture et manipulation de tableaux
import qualite_pandas as qp        # module de l'Workshop 2 : fonction de nettoyage

# --- 2. Lire les deux fichiers CSV ---
# encoding="utf-8-sig" : lit correctement les accents et le BOM éventuel ; rename : nom de colonne plus court
brut = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
ref = pd.read_csv("data/sites_reference.csv", encoding="utf-8-sig")    # une ligne par site (type, capacité)

# --- 3. Nettoyer puis ajouter type et capacité de chaque site ---
# nettoyer : doublons supprimés, dates converties, codes d'erreur remplacés par NaN (Workshop 2)
# how="left" : on garde toutes les mesures ; validate="m:1" : plusieurs mesures par site, un seul site
# dans ref, sinon erreur (protège contre des lignes dupliquées)
d = qp.nettoyer(brut).merge(ref[["site_id", "site_type", "capacity_mw"]], on="site_id", how="left", validate="m:1")

# --- 4. Contrôler le résultat ---
print(len(brut), "->", len(d), "lignes")    # lignes avant / après nettoyage
# aperçu des 3 premières lignes des colonnes utiles
print(d[["timestamp", "site_id", "site_type", "capacity_mw", "conso_mw"]].head(3))
print(d["conso_mw"].isna().sum(), "valeurs manquantes")    # isna() marque les NaN, sum() les compte

# %% Cellule 5 — La cible : retirer les pics aberrants
# === CELLULE 5 : Pics aberrants ===
# --- 1. Conserver une copie de la mesure d'origine ---
d["conso_brute"] = d["conso_mw"]    # sert à la détection d'anomalies (Partie 5)

# --- 2. Repérer les pics : mesures au-dessus de la capacité du site ---
# comparaison ligne à ligne : True si la consommation dépasse la capacité (impossible physiquement)
d["pic"] = d["conso_mw"] > d["capacity_mw"]
print(d["pic"].sum(), "pics au-dessus de la capacité")    # True vaut 1 : sum() compte les pics
# d.loc[masque, colonnes] : n'affiche que les lignes-pics et 3 colonnes ; head(3) = 3 premières
print(d.loc[d["pic"], ["site_id", "conso_mw", "capacity_mw"]].head(3))

# --- 3. Retirer les pics de la cible ---
# mask(condition) remplace par NaN les valeurs où la condition est vraie ; les autres ne changent pas
d["conso_mw"] = d["conso_mw"].mask(d["pic"])
print(d["conso_mw"].isna().sum(), "valeurs manquantes après retrait des pics")    # NaN d'origine + pics

# %% Cellule 6 — Variables de calendrier
# === CELLULE 6 : Variables de calendrier ===
# --- 1. Extraire heure et jour de la semaine depuis la date ---
d["heure"] = d["timestamp"].dt.hour            # .dt donne accès aux parties de la date : heure de 0 à 23
d["jour_sem"] = d["timestamp"].dt.dayofweek    # jour de semaine : 0 = lundi ... 6 = dimanche

# --- 2. Indiquer si c'est un week-end ---
# jour_sem >= 5 : samedi ou dimanche (True/False) ; astype(int) convertit en 1 ou 0
d["weekend"] = (d["jour_sem"] >= 5).astype(int)

# --- 3. Vérifier sur trois lignes ---
# iloc[[0, 30, 130]] : lignes n° 0, 30 et 130 (choisies pour couvrir des jours différents)
print(d[["timestamp", "heure", "jour_sem", "weekend"]].iloc[[0, 30, 130]])

# --- 4. Comparer semaine et week-end par type de site ---
# taux d'utilisation : comparable entre sites de tailles différentes
d["taux"] = d["conso_mw"] / d["capacity_mw"]
# pivot_table : une ligne par type de site, une colonne par valeur de weekend, moyenne du taux dans chaque case
print(d.pivot_table(index="site_type", columns="weekend", values="taux", aggfunc="mean").round(3))

# %% Cellule 7 — Le principe de scikit-learn : `fit`, `predict`, `score`
# === CELLULE 7 : L'interface commune ===
# --- 1. Importer deux modèles de types différents ---
from sklearn.ensemble import RandomForestRegressor    # forêt d'arbres de décision
from sklearn.linear_model import LinearRegression     # droite (somme pondérée des variables)

# --- 2. Préparer les données d'un seul site ---
# on garde un site et on écarte les lignes sans cible (NaN refusés par ces modèles)
site = d[(d["site_id"] == "SITE_COM_001") & d["conso_mw"].notna()]
# X : variables explicatives (double crochet = tableau à 2 dimensions) ; y : cible (1 dimension)
X, y = site[["heure"]], site["conso_mw"]

# --- 3. Appliquer les mêmes trois verbes à chaque modèle ---
# n_estimators=50 : 50 arbres ; random_state=0 : résultat reproductible d'une exécution à l'autre
for modele in (LinearRegression(), RandomForestRegressor(n_estimators=50, random_state=0)):
    modele.fit(X, y)    # fit : le modèle apprend la relation entre X et y
    # predict : prévision pour de nouvelles heures (3 h et 14 h), données sous forme de tableau
    prevu = modele.predict(pd.DataFrame({"heure": [3, 14]}))
    # score : R² sur les données d'apprentissage (1 = parfait) ; type(modele).__name__ = nom de la classe
    print(f"{type(modele).__name__:<22} 3 h / 14 h : {prevu.round(2)}   R² sur ces données : {modele.score(X, y):.2f}")

# --- 4. Lire ce que le modèle linéaire a appris ---
# coef_ : poids appris par variable ; on ré-entraîne un modèle linéaire car la boucle a réutilisé le nom modele
print("Coefficient appris (linéaire) :", round(LinearRegression().fit(X, y).coef_[0], 4))

# %% Cellule 8 — Valeurs décalées : la veille et la semaine dernière
# === CELLULE 8 : Valeurs décalées ===
# --- 1. Vérifier que la grille est régulière (une ligne par heure) ---
# groupby("site_id") : calcul séparé pour chaque site ; diff() : écart avec la ligne précédente
ecarts = d.groupby("site_id")["timestamp"].diff().dropna()    # dropna : retire la 1re ligne de chaque site
# value_counts : on doit voir un seul écart (1 heure), sinon shift(24) ne vaudrait pas « 24 h avant »
print("Écarts entre lignes :", ecarts.value_counts().to_dict())

# --- 2. Créer la consommation de la veille et de la semaine dernière ---
g = d.groupby("site_id")["conso_mw"]    # groupes par site : le décalage ne traverse jamais deux sites
d["lag_24"] = g.shift(24)               # valeur d'il y a 24 lignes = même heure la veille
d["lag_168"] = g.shift(168)             # 168 = 7 × 24 : même heure la semaine dernière

# --- 3. Contrôler sur un site ---
site = d[d["site_id"] == "SITE_COM_001"]
# lignes 0 et 24 : début de la série ; 168 et 192 : premières lignes où les décalages existent
print(site[["timestamp", "conso_mw", "lag_24", "lag_168"]].iloc[[0, 24, 168, 192]])

# --- 4. Compter les valeurs absentes créées par le décalage ---
# les 24 (ou 168) premières heures de chaque site n'ont pas d'historique : NaN
print(d[["lag_24", "lag_168"]].isna().sum().to_dict())

# %% Cellule 9 — Moyenne glissante sans regarder l'avenir
# === CELLULE 9 : Moyenne glissante ===
# --- 1. Calculer la moyenne des 24 h se terminant 24 h avant la mesure ---
# transform : renvoie une valeur par ligne d'origine, calculée séparément pour chaque site (g vient de la cellule précédente)
# shift(24) d'abord : la fenêtre se termine la veille, donc rien du futur n'entre dans le calcul
# rolling(24) : fenêtre de 24 valeurs ; min_periods=12 : calcul accepté dès 12 valeurs connues (sinon NaN)
d["moy_veille"] = g.transform(lambda s: s.shift(24).rolling(24, min_periods=12).mean())

# --- 2. Recalculer une valeur à la main pour vérifier ---
i = 500    # ligne à contrôler (choisie arbitrairement, loin du début des séries)
# la fenêtre couvre les lignes i-47 à i-24 ; .loc inclut les deux bornes : 24 valeurs
a_la_main = d.loc[i - 47:i - 24, "conso_mw"].mean()
print("Ligne", i, d.loc[i, "site_id"], d.loc[i, "timestamp"])    # site et date de la ligne testée

# --- 3. Comparer avec la colonne calculée ---
print("À la main :", round(a_la_main, 4), "| colonne moy_veille :", round(d.loc[i, "moy_veille"], 4))
print(d["moy_veille"].isna().sum(), "valeurs absentes")    # début des séries + trous dans les mesures

# %% Cellule 10 — Découpage temporel : passé pour apprendre, futur pour tester
# === CELLULE 10 : Découpage temporel ===
# --- 1. Définir les variables explicatives et la date de coupure ---
# liste des colonnes données au modèle pour prévoir conso_mw
VARIABLES = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]
COUPURE = pd.Timestamp("2025-01-24")    # avant : apprentissage ; à partir de là : test

# --- 2. Écarter les 7 premiers jours et les lignes sans cible ---
# avant le 8 janvier, lag_168 n'existe pas encore ; on retire aussi les lignes où la cible est NaN
utile = d[(d["timestamp"] >= "2025-01-08") & d["conso_mw"].notna()]

# --- 3. Couper dans le temps, jamais au hasard ---
train = utile[utile["timestamp"] < COUPURE]     # le passé : le modèle apprend dessus
# le futur sert de test ; dropna(subset=...) retire les lignes sans lag_24 ou lag_168
test = utile[utile["timestamp"] >= COUPURE].dropna(subset=["lag_24", "lag_168"])

# --- 4. Vérifier les périodes et les valeurs manquantes ---
# min() et max() donnent la première et la dernière date de chaque jeu ; .date() garde le jour seul
print("Entraînement :", len(train), "lignes,", train["timestamp"].min().date(), "->", train["timestamp"].max().date())
print("Test         :", len(test), "lignes,", test["timestamp"].min().date(), "->", test["timestamp"].max().date())
# colonnes ayant encore des NaN dans train : [lambda s: s > 0] ne garde que celles où le compte dépasse 0
print("Manquants dans train :", train[VARIABLES].isna().sum()[lambda s: s > 0].to_dict())

# %% Cellule 11 — Corrélation avec la cible
# === CELLULE 11 : Corrélations ===
# --- 1. Mesurer le lien linéaire de chaque variable avec la cible ---
# corr() : tableau des corrélations (de -1 à 1) entre toutes les colonnes ; on garde la colonne conso_mw
# drop("conso_mw") retire la corrélation de la cible avec elle-même (toujours 1) ; round(2) : 2 décimales
print(train[VARIABLES + ["conso_mw"]].corr()["conso_mw"].drop("conso_mw").round(2))

# %% Cellule 12 — Les références à battre
# === CELLULE 12 : Références ===
# --- 1. Importer les trois mesures d'erreur ---
# MAE : erreur absolue moyenne (MW) ; RMSE : racine de l'erreur quadratique (pénalise les gros écarts) ; R² : part expliquée
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

# --- 2. Écrire une fonction qui résume la qualité d'une prévision ---
def evaluer(y_vrai, y_pred):
    # y_vrai : valeurs réelles ; y_pred : valeurs prévues ; retourne un dictionnaire de trois métriques
    return {"MAE": mean_absolute_error(y_vrai, y_pred),         # écart moyen en MW (plus petit = mieux)
            "RMSE": root_mean_squared_error(y_vrai, y_pred),    # écart en MW, gros écarts amplifiés
            "R2": r2_score(y_vrai, y_pred)}                     # 1 = parfait ; 0 = pas mieux que la moyenne

# --- 3. Calculer la moyenne d'entraînement de chaque site ---
# uniquement sur train : le test représente le futur, inconnu au moment de prévoir
moyenne_site = train.groupby("site_id")["conso_mw"].mean()

# --- 4. Construire trois prévisions très simples, sans apprentissage ---
references = {
    "même heure la veille": test["lag_24"],                        # on recopie la consommation de la veille
    "même heure la semaine dernière": test["lag_168"],             # on recopie celle de la semaine dernière
    "moyenne du site": test["site_id"].map(moyenne_site),          # chaque ligne reçoit la moyenne de son site
}

# --- 5. Évaluer chaque référence sur le même jeu de test ---
# pour chaque (nom, prévision) : dictionnaire MAE / RMSE / R² ; resultats servira aux cellules suivantes
resultats = {nom: evaluer(test["conso_mw"], p) for nom, p in references.items()}
# .T : transpose pour avoir une ligne par référence ; round(3) : 3 décimales
print(pd.DataFrame(resultats).T.round(3))

# %% Cellule 13 — Première régression : `LinearRegression`
# === CELLULE 13 : Régression linéaire ===
# --- 1. Importer le modèle ---
from sklearn.linear_model import LinearRegression    # somme pondérée des variables

# --- 2. Préparer le remplacement des valeurs manquantes ---
# LinearRegression refuse les NaN : médiane de chaque colonne, calculée sur train uniquement
# (utiliser celle du test ferait fuiter de l'information du futur)
mediane = train[VARIABLES].median()

# --- 3. Entraîner puis prévoir ---
# fillna(mediane) remplace chaque NaN par la médiane de sa colonne ; fit : apprentissage sur le passé
lin = LinearRegression().fit(train[VARIABLES].fillna(mediane), train["conso_mw"])
# predict : prévision sur le futur (test), avec la même médiane que pour l'entraînement
p_lin = lin.predict(test[VARIABLES].fillna(mediane))

# --- 4. Évaluer et lire les poids appris ---
resultats["régression linéaire"] = evaluer(test["conso_mw"], p_lin)    # on ajoute une ligne au tableau
# coef_ : un poids par variable, dans l'ordre de VARIABLES ; zip associe chaque nom à son poids
print({v: round(float(c), 3) for v, c in zip(VARIABLES, lin.coef_)})
print(pd.Series(resultats["régression linéaire"]).round(3).to_dict())    # métriques du modèle

# %% Cellule 14 — Modèles à base d'arbres : forêt aléatoire et gradient boosting
# === CELLULE 14 : Forêt et gradient boosting ===
# --- 1. Importer les deux modèles à base d'arbres ---
# forêt : moyenne de nombreux arbres ; gradient boosting : arbres construits l'un après l'autre, chacun corrige le précédent
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

# --- 2. Entraîner la forêt aléatoire ---
# n_estimators=200 : 200 arbres ; random_state=0 : résultat reproductible ; n_jobs=-1 : tous les cœurs du processeur
foret = RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1)
# la forêt refuse les NaN : on utilise la médiane d'entraînement (cellule précédente)
foret.fit(train[VARIABLES].fillna(mediane), train["conso_mw"])

# --- 3. Entraîner le gradient boosting ---
# accepte les NaN tels quels (pas d'imputation) ; fit retourne le modèle, d'où l'enchaînement
hgb = HistGradientBoostingRegressor(random_state=0).fit(train[VARIABLES], train["conso_mw"])

# --- 4. Prévoir sur le futur (test) ---
p_foret = foret.predict(test[VARIABLES].fillna(mediane))    # prévisions de la forêt
p_hgb = hgb.predict(test[VARIABLES])                        # prévisions du gradient boosting

# --- 5. Évaluer et afficher les deux modèles ---
resultats["forêt aléatoire"] = evaluer(test["conso_mw"], p_foret)
resultats["gradient boosting"] = evaluer(test["conso_mw"], p_hgb)
# .loc[[...]] ne garde que les deux nouvelles lignes du tableau
print(pd.DataFrame(resultats).T.loc[["forêt aléatoire", "gradient boosting"]].round(3))

# %% Cellule 15 — Comparer tous les modèles
# === CELLULE 15 : Tableau comparatif ===
# --- 1. Rassembler et classer tous les résultats ---
# une ligne par modèle ; sort_values("MAE") place la plus petite erreur moyenne en premier
tableau = pd.DataFrame(resultats).T.sort_values("MAE").round(3)
print(tableau)

# --- 2. Tester une prévision sans aucun historique ---
# on prend la 1re ligne du test (double crochet = garde un tableau) ; assign remplace les trois
# variables d'historique par NaN (np.nan = valeur manquante)
ligne = test.iloc[[0]][VARIABLES].assign(lag_24=np.nan, lag_168=np.nan, moy_veille=np.nan)
# le gradient boosting accepte les NaN : predict renvoie un tableau, [0] prend sa seule valeur ; réel en comparaison
print("\nSans aucun historique -> prévision :", round(float(hgb.predict(ligne)[0]), 3), "MW | réel :", round(float(test.iloc[0]["conso_mw"]), 3), "MW")

# %% Cellule 16 — Le plafond : le bruit qu'aucun modèle ne peut prévoir
# === CELLULE 16 : Erreur incompressible ===
# --- 1. Calculer le profil moyen de chaque (site, heure, type de jour) ---
# c'est la meilleure prévision possible si seul le bruit aléatoire reste : la moyenne de chaque combinaison
profil = train.groupby(["site_id", "heure", "weekend"])["conso_mw"].mean()

# --- 2. Associer à chaque ligne du test son profil ---
# set_index(...).index : combinaisons (site, heure, weekend) de chaque ligne ; map les remplace par la moyenne du profil
p_profil = test.set_index(["site_id", "heure", "weekend"]).index.map(profil)

# --- 3. Mesurer l'erreur de ce plafond ---
r = evaluer(test["conso_mw"], p_profil)    # mêmes métriques que pour les modèles
print({k: round(v, 3) for k, v in r.items()})    # dictionnaire arrondi à 3 décimales

# --- 4. Exprimer l'erreur en proportion de la consommation ---
print("Niveau moyen de la consommation :", round(test["conso_mw"].mean(), 3), "MW")
# :.1% formate en pourcentage avec une décimale ; à comparer au bruit de ±10 % des données simulées
print("MAE / niveau moyen :", f"{r['MAE'] / test['conso_mw'].mean():.1%}")

# %% Cellule 17 — `Pipeline` et `ColumnTransformer` : le prétraitement avec le modèle
# === CELLULE 17 : Pipeline complet ===
# --- 1. Importer les briques de prétraitement ---
from sklearn.compose import ColumnTransformer        # applique un traitement différent par groupe de colonnes
from sklearn.impute import SimpleImputer             # remplace les valeurs manquantes
from sklearn.pipeline import Pipeline, make_pipeline # enchaîne des étapes en un seul objet
from sklearn.preprocessing import OneHotEncoder, StandardScaler    # texte -> colonnes 0/1 ; mise à l'échelle

# --- 2. Décrire le prétraitement par groupe de colonnes ---
numeriques = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]    # colonnes numériques
prep = ColumnTransformer([
    # site_id est du texte : une colonne 0/1 par site ; handle_unknown="ignore" : site inconnu = que des 0
    ("site", OneHotEncoder(handle_unknown="ignore"), ["site_id"]),
    # nombres : NaN remplacés par la médiane, puis valeurs centrées et réduites (moyenne 0, écart-type 1)
    ("nombres", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeriques),
])

# --- 3. Relier le prétraitement au modèle, puis entraîner ---
# étapes nommées, exécutées dans l'ordre : prétraitement puis modèle
pipe_lin = Pipeline([("prep", prep), ("modele", LinearRegression())])
# un seul fit : apprend médianes, échelles et poids sur train uniquement
pipe_lin.fit(train[["site_id"] + numeriques], train["conso_mw"])

# --- 4. Prévoir et évaluer ---
# predict applique automatiquement tout le prétraitement avant le modèle
p = pipe_lin.predict(test[["site_id"] + numeriques])
resultats["linéaire + pipeline"] = evaluer(test["conso_mw"], p)

# --- 5. Inspecter le pipeline ---
print(list(pipe_lin.named_steps))    # noms des étapes : prep, modele
# [:-1] = toutes les étapes sauf le modèle ; get_feature_names_out : noms des colonnes produites (8 premières)
print(list(pipe_lin[:-1].get_feature_names_out())[:8], "...")
print(pd.Series(resultats["linéaire + pipeline"]).round(3).to_dict())    # métriques du pipeline

# %% Cellule 18 — Pipeline final : catégories natives et gradient boosting
# === CELLULE 18 : Pipeline gradient boosting ===
# --- 1. Importer les briques ---
from sklearn.compose import make_column_transformer    # version courte de ColumnTransformer (noms automatiques)
from sklearn.preprocessing import OrdinalEncoder       # texte -> entier (un numéro par site)

# --- 2. Définir les colonnes d'entrée ---
COLONNES = ["site_id"] + VARIABLES    # site_id en premier : il sera la colonne n° 0 après transformation

# --- 3. Décrire le prétraitement ---
prep_hgb = make_column_transformer(
    # site_id devient un entier ; unknown_value=np.nan : un site jamais vu donne NaN au lieu d'une erreur
    (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan), ["site_id"]),
    remainder="passthrough",    # les autres colonnes passent sans changement (le modèle accepte les NaN)
)

# --- 4. Relier prétraitement et modèle ---
# categorical_features=[0] : la colonne n° 0 (site) est une catégorie, pas une quantité
pipe_hgb = make_pipeline(prep_hgb, HistGradientBoostingRegressor(categorical_features=[0], random_state=0))
pipe_hgb.fit(train[COLONNES], train["conso_mw"])    # un seul fit sur le passé

# --- 5. Prévoir et évaluer sur le futur ---
p_pipe = pipe_hgb.predict(test[COLONNES])    # prétraitement appliqué automatiquement avant la prévision
resultats["gradient boosting + pipeline"] = evaluer(test["conso_mw"], p_pipe)
print(pd.Series(resultats["gradient boosting + pipeline"]).round(3).to_dict())    # métriques du modèle final

# %% Cellule 19 — Prévision contre réalité sur la semaine de test
# === CELLULE 19 : Figure prévision ===
# --- 1. Importer les outils et créer le dossier de sortie ---
import matplotlib.pyplot as plt    # bibliothèque de tracé
from pathlib import Path           # chemins de fichiers

Path("out").mkdir(exist_ok=True)    # crée out/ ; exist_ok=True : pas d'erreur s'il existe déjà

# --- 2. Ajouter les prévisions et isoler un site ---
t = test.assign(prevu=p_pipe)          # nouvelle colonne prevu = prévisions du pipeline (copie du test)
s = t[t["site_id"] == "SITE_IND_001"]  # une seule courbe par variable : on garde un site

# --- 3. Créer la figure ---
fig, ax = plt.subplots(figsize=(10, 3.8))    # une figure, un graphique ; taille en pouces (largeur, hauteur)

# --- 4. Tracer les trois courbes ---
ax.plot(s["timestamp"], s["conso_mw"], color="#1f77b4", linewidth=1.4, label="réel")    # mesures (bleu)
ax.plot(s["timestamp"], s["prevu"], color="#d62728", linewidth=1.2, label="gradient boosting")    # rouge
# référence « semaine dernière » : gris pointillé, plus fin
ax.plot(s["timestamp"], s["lag_168"], color="#7f7f7f", linewidth=1, linestyle=":", label="semaine dernière")

# --- 5. Titre, axes, légende et grille ---
ax.set_title("SITE_IND_001 : semaine du 24 au 30 janvier")    # titre du graphique
ax.set_ylabel("MW")                                           # unité de l'axe vertical
ax.set_ylim(0.6, 4.0)                                         # bornes de l'axe vertical, identiques pour comparer
ax.legend(loc="upper right", ncol=3)                          # légende en haut à droite, sur 3 colonnes
ax.grid(alpha=0.3)                                            # grille discrète (alpha = transparence)
fig.autofmt_xdate()                                           # incline les dates de l'axe horizontal pour les lire

# --- 6. Enregistrer l'image ---
# dpi=110 : résolution ; bbox_inches="tight" : rogne les marges blanches
fig.savefig("out/fig_prevision.png", dpi=110, bbox_inches="tight")

# %% Cellule 20 — L'erreur site par site
# === CELLULE 20 : Erreur par site ===
# --- 1. Calculer l'erreur absolue de chaque prévision ---
# assign ajoute deux colonnes : prevu (prévision) et erreur = |réel - prévu|, calculée par la fonction lambda
t = test.assign(prevu=p_pipe, erreur=lambda x: (x["conso_mw"] - x["prevu"]).abs())

# --- 2. Résumer par site ---
# agg : deux résultats par site : consommation moyenne et erreur moyenne (MAE)
par_site = t.groupby("site_id").agg(niveau_mw=("conso_mw", "mean"), mae_mw=("erreur", "mean"))

# --- 3. Calculer l'erreur relative ---
# MAE ÷ niveau moyen : comparable entre sites ; map("{:.1%}".format) affiche un pourcentage à 1 décimale
par_site["mae_relative"] = (par_site["mae_mw"] / par_site["niveau_mw"]).map("{:.1%}".format)
print(par_site.round(3))    # tableau final, chiffres arrondis à 3 décimales

# %% Étape manuelle — Créer le module `prevision_conso.py`
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('prevision_conso.py', 'w', encoding='utf-8') as f:
    f.write('"""prevision_conso.py — Préparation, évaluation et modèle de prévision (Workshop 3)."""\n# --- Imports : calcul, tableaux, outils scikit-learn utilisés par les fonctions ---\nimport numpy as np                                                    # np.nan : valeur manquante\nimport pandas as pd                                                   # tableaux de données\nfrom sklearn.compose import make_column_transformer                   # prétraitement par groupe de colonnes\nfrom sklearn.ensemble import HistGradientBoostingRegressor            # modèle de gradient boosting\nfrom sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error    # métriques d\'erreur\nfrom sklearn.pipeline import make_pipeline                            # enchaîne prétraitement et modèle\nfrom sklearn.preprocessing import OrdinalEncoder                      # texte -> entier\n\nimport qualite_pandas as qp    # module de l\'Workshop 2 : nettoyage des mesures\n\n# --- Constantes partagées par le notebook et le module ---\n# variables numériques données au modèle pour prévoir la consommation\nVARIABLES = ["heure", "weekend", "capacity_mw", "lag_24", "lag_168", "moy_veille"]\n# colonnes d\'entrée complètes : le site (texte) en premier, puis les variables numériques\nCOLONNES = ["site_id"] + VARIABLES\n# début de la période utile : les 7 premiers jours n\'ont pas encore de lag_168\nDEBUT_UTILE = pd.Timestamp("2025-01-08")\n# date de coupure : avant = apprentissage, à partir de là = test\nCOUPURE = pd.Timestamp("2025-01-24")\n\n\n# Rôle : lire les deux CSV, nettoyer les mesures et ajouter type et capacité de chaque site.\n# Entrées : chemins des deux fichiers (valeurs par défaut du dossier data/). Sortie : DataFrame propre.\ndef charger_propre(mesures="data/consommation_30jours.csv", reference="data/sites_reference.csv"):\n    """Mesures nettoyées (Workshop 2), avec type et capacité des sites."""\n    # lecture des mesures (utf-8-sig : accents et BOM) ; nom de colonne raccourci\n    brut = pd.read_csv(mesures, encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})\n    # lecture de la table des sites, en ne gardant que les 3 colonnes utiles\n    ref = pd.read_csv(reference, encoding="utf-8-sig")[["site_id", "site_type", "capacity_mw"]]\n    # nettoyage puis jointure ; validate="m:1" : erreur si un site apparaît deux fois dans ref\n    return qp.nettoyer(brut).merge(ref, on="site_id", how="left", validate="m:1")\n\n\n# Rôle : construire la cible et toutes les variables explicatives.\n# Entrée : DataFrame propre d. Sortie : copie enrichie (l\'original n\'est pas modifié).\ndef ajouter_variables(d):\n    """Cible sans pics, variables de calendrier, valeurs décalées, moyenne glissante."""\n    d = d.copy()    # copie : on ne modifie pas le tableau de l\'appelant\n    # 1. cible : copie brute conservée, pics au-dessus de la capacité repérés puis remplacés par NaN\n    d["conso_brute"] = d["conso_mw"]\n    d["pic"] = d["conso_mw"] > d["capacity_mw"]\n    d["conso_mw"] = d["conso_mw"].mask(d["pic"])\n    # 2. calendrier : heure (0-23), jour de semaine (0 = lundi), week-end (1 si samedi/dimanche)\n    d["heure"] = d["timestamp"].dt.hour\n    d["jour_sem"] = d["timestamp"].dt.dayofweek\n    d["weekend"] = (d["jour_sem"] >= 5).astype(int)\n    # 3. taux d\'utilisation : consommation rapportée à la capacité du site\n    d["taux"] = d["conso_mw"] / d["capacity_mw"]\n    # 4. valeurs décalées, calculées site par site pour ne jamais mélanger deux sites\n    g = d.groupby("site_id")["conso_mw"]\n    d["lag_24"] = g.shift(24)      # même heure la veille\n    d["lag_168"] = g.shift(168)    # même heure la semaine dernière\n    # 5. moyenne des 24 h se terminant 24 h avant la mesure (aucune information du futur)\n    d["moy_veille"] = g.transform(lambda s: s.shift(24).rolling(24, min_periods=12).mean())\n    return d    # tableau enrichi\n\n\n# Rôle : enchaîner chargement et création des variables.\n# Entrée : chemins optionnels (mots-clés transmis à charger_propre). Sortie : tableau prêt à découper.\ndef preparer(**chemins):\n    return ajouter_variables(charger_propre(**chemins))    # sortie de charger_propre passée à ajouter_variables\n\n\n# Rôle : couper dans le temps, jamais au hasard.\n# Entrées : tableau préparé d, date de coupure. Sortie : couple (train, test).\ndef decouper(d, coupure=COUPURE):\n    """Passé pour apprendre, futur (lags complets) pour tester."""\n    # on écarte les 7 premiers jours et les lignes sans cible\n    utile = d[(d["timestamp"] >= DEBUT_UTILE) & d["conso_mw"].notna()]\n    # premier élément : le passé (train) ; second : le futur (test), sans ligne où lag_24 ou lag_168 manque\n    return (utile[utile["timestamp"] < coupure],\n            utile[utile["timestamp"] >= coupure].dropna(subset=["lag_24", "lag_168"]))\n\n\n# Rôle : résumer la qualité d\'une prévision.\n# Entrées : valeurs réelles y_vrai, valeurs prévues y_pred. Sortie : dictionnaire MAE / RMSE / R2.\ndef evaluer(y_vrai, y_pred):\n    return {"MAE": mean_absolute_error(y_vrai, y_pred),         # écart moyen en MW\n            "RMSE": root_mean_squared_error(y_vrai, y_pred),    # écart en MW, gros écarts amplifiés\n            "R2": r2_score(y_vrai, y_pred)}                     # part de variation expliquée (1 = parfait)\n\n\n# Rôle : fabriquer le pipeline final (non entraîné).\n# Entrée : réglages facultatifs du modèle (**params). Sortie : pipeline prêt pour fit / predict.\ndef construire_modele(**params):\n    """Pipeline final : site encodé comme catégorie + gradient boosting."""\n    # étape 1 : site_id devient un entier (un site inconnu donne NaN) ; les autres colonnes passent telles quelles\n    prep = make_column_transformer(\n        (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan), ["site_id"]),\n        remainder="passthrough",\n    )\n    # étape 2 : gradient boosting ; colonne 0 (site) traitée comme catégorie ; random_state=0 : reproductible\n    return make_pipeline(prep, HistGradientBoostingRegressor(categorical_features=[0], random_state=0, **params))\n')
print('prevision_conso.py', ':', len(open('prevision_conso.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 21 — Vérifier que le module reproduit la préparation
# === CELLULE 21 : Contrôle du module ===
# --- 1. Importer le module tout juste créé ---
import importlib
importlib.invalidate_caches()    # oblige Python à revoir le contenu du dossier (le fichier est nouveau)

import prevision_conso as pc    # notre module : pc.preparer, pc.decouper, pc.construire_modele...

# --- 2. Refaire la préparation avec le module ---
d2 = pc.preparer()    # chargement, nettoyage et variables en un seul appel
colonnes = ["timestamp", "site_id", "conso_mw", "heure", "weekend", "lag_24", "lag_168", "moy_veille"]
# assert_frame_equal : lève une erreur si une seule valeur diffère du d construit à la main
pd.testing.assert_frame_equal(d2[colonnes], d[colonnes])

# --- 3. Refaire découpage, entraînement et évaluation ---
tr2, te2 = pc.decouper(d2)    # jeux d'apprentissage et de test
# construire_modele : le pipeline final (non entraîné) ; fit : apprentissage sur le passé
modele = pc.construire_modele().fit(tr2[pc.COLONNES], tr2["conso_mw"])
# predict sur le futur, puis evaluer ; ["MAE"] extrait l'erreur moyenne
mae = pc.evaluer(te2["conso_mw"], modele.predict(te2[pc.COLONNES]))["MAE"]

# --- 4. Comparer avec le résultat de la cellule précédente ---
# la dernière valeur (True/False) indique si la MAE est identique à 6 décimales
print(len(tr2), len(te2), "lignes | MAE :", round(mae, 3), "| identique à la Cellule 18 :", round(mae, 6) == round(resultats["gradient boosting + pipeline"]["MAE"], 6))

# %% Cellule 22 — Reprendre proprement avec le module
# === CELLULE 22 : Reprise ===
# --- 1. Importer les outils (numpy, pandas et notre module) ---
import numpy as np                    # calcul numérique (utilisé par le module)
import pandas as pd                   # tableaux de données (DataFrame)
import prevision_conso as pc          # module écrit à la main : chargement, variables, découpage, modèle

# --- 2. Rejouer la préparation des données (identique pour tous) ---
d = pc.preparer()                     # charge, nettoie, puis ajoute les variables (décalages, moyenne, calendrier)
train, test = pc.decouper(d)          # passé = entraînement, futur = test (on ne mélange jamais le temps)

# --- 3. Contrôler que tout est en place ---
print(len(d), "lignes |", len(train), "entraînement |", len(test), "test")   # taille du tout et de chaque partie
print(pc.COLONNES)                    # liste des colonnes données au modèle (site + variables)

# %% Cellule 23 — Piège 1 : la fuite de données
# === CELLULE 23 : Fuite de données ===
# --- 1. Importer le modèle et la mesure d'erreur ---
from sklearn.ensemble import HistGradientBoostingRegressor   # gradient boosting : modèle de prévision rapide
from sklearn.metrics import mean_absolute_error              # MAE : erreur moyenne en valeur absolue (en MW)

# --- 2. Fabriquer une variable "truquée" qui contient la réponse ---
# groupby("site_id") : un calcul séparé par site ; rolling(2) : moyenne des 2 dernières valeurs.
# Pas de shift : la fenêtre inclut l'heure courante, donc la réponse à prédire (c'est la fuite).
# transform : renvoie une valeur par ligne, alignée sur le tableau d'origine.
d_f = d.assign(moy_fuite=d.groupby("site_id")["conso_mw"].transform(lambda s: s.rolling(2, min_periods=1).mean()))
# assign : ajoute la colonne sur une copie ; le tableau d reste intact.
tr_f, te_f = pc.decouper(d_f)         # même découpage passé / futur, mais avec la variable truquée

# --- 3. Comparer le score sans et avec la fuite ---
for nom, cols in (("sans fuite", pc.VARIABLES), ("avec fuite", pc.VARIABLES + ["moy_fuite"])):
    # fit : le modèle apprend sur l'entraînement ; random_state=0 : résultat reproductible
    m = HistGradientBoostingRegressor(random_state=0).fit(tr_f[cols], tr_f["conso_mw"])
    # predict : prévisions sur le test ; MAE : écart moyen entre réel et prévu (plus bas = "mieux")
    print(f"{nom:<11} MAE test : {mean_absolute_error(te_f['conso_mw'], m.predict(te_f[cols])):.4f} MW")

# %% Cellule 24 — Piège 2 : mélanger le temps
# === CELLULE 24 : Découpage aléatoire ou temporel ===
# --- 1. Importer l'outil de découpage aléatoire ---
from sklearn.model_selection import train_test_split   # tire au hasard des lignes pour le test

# --- 2. Simuler une tendance à la hausse sur une copie des données ---
# Numéro du jour : écart entre chaque date et la première date, exprimé en jours entiers.
jours = (d["timestamp"] - d["timestamp"].min()).dt.days
# Consommation multipliée par (1 + 3 % x jour) ; jour_num = variable "tendance" ; dropna : retire les valeurs manquantes.
tendance = d.assign(conso_mw=d["conso_mw"] * (1 + 0.03 * jours), jour_num=jours).dropna(subset=["conso_mw"])
cols = ["heure", "weekend", "capacity_mw", "jour_num"]   # variables données au modèle

# --- 3. Fabriquer les deux découpages ---
# Aléatoire : 25 % des lignes tirées au hasard pour le test ; random_state=0 : tirage reproductible.
a, b = train_test_split(tendance, test_size=0.25, random_state=0)
# Temporel : passé avant la date de coupure pour apprendre, futur après pour tester.
passe, futur = tendance[tendance["timestamp"] < pc.COUPURE], tendance[tendance["timestamp"] >= pc.COUPURE]

# --- 4. Entraîner et évaluer sur chacun ---
for nom, (ent, val) in {"aléatoire": (a, b), "temporel": (passe, futur)}.items():
    # fit sur l'entraînement uniquement ; random_state=0 : résultat reproductible
    m = HistGradientBoostingRegressor(random_state=0).fit(ent[cols], ent["conso_mw"])
    # predict sur la partie de validation, puis MAE (plus bas = meilleur score apparent)
    print(f"{nom:<10} MAE : {mean_absolute_error(val['conso_mw'], m.predict(val[cols])):.3f} MW")
# Niveau moyen : sert d'échelle pour juger si l'erreur est petite ou grande
print("Niveau moyen :", round(tendance["conso_mw"].mean(), 2), "MW")

# %% Cellule 25 — Validation croisée pour séries temporelles
# === CELLULE 25 : TimeSeriesSplit ===
# --- 1. Importer le découpeur temporel et l'évaluateur ---
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

# --- 2. Trier les données dans l'ordre du temps ---
# Le découpeur coupe par position : les lignes doivent être triées par date (puis site) ; reset_index renumérote de 0.
ordre = train.sort_values(["timestamp", "site_id"]).reset_index(drop=True)

# --- 3. Créer le découpeur et afficher les plis ---
# n_splits=4 : 4 plis ; chaque pli entraîne sur le passé et valide sur la période qui suit.
tscv = TimeSeriesSplit(n_splits=4)
# split renvoie les positions des lignes d'entraînement (ent) et de validation (val) ; enumerate(..., 1) numérote dès 1.
for i, (ent, val) in enumerate(tscv.split(ordre), 1):
    # On affiche la première et la dernière date de chaque partie : l'entraînement précède toujours la validation.
    print(f"pli {i} : entraînement {ordre.loc[ent[0], 'timestamp']:%d/%m} -> {ordre.loc[ent[-1], 'timestamp']:%d/%m} | validation {ordre.loc[val[0], 'timestamp']:%d/%m} -> {ordre.loc[val[-1], 'timestamp']:%d/%m}")

# --- 4. Évaluer le modèle sur chaque pli ---
# cross_val_score : fit puis score sur chaque pli. cv=tscv : on impose le découpage temporel.
# scoring="neg_mean_absolute_error" : MAE négative (scikit-learn maximise) ; on remet le signe plus après.
scores = cross_val_score(HistGradientBoostingRegressor(random_state=0), ordre[pc.VARIABLES], ordre["conso_mw"],
                         cv=tscv, scoring="neg_mean_absolute_error")
# -scores : MAE positives ; la moyenne résume, l'écart entre plis montre la stabilité.
print("MAE par pli :", (-scores).round(3), "| moyenne :", round(-scores.mean(), 3))

# %% Cellule 26 — Piège 3 : entraîner avec les pics aberrants
# === CELLULE 26 : Effet des pics sur l'entraînement ===
# --- 1. Importer les deux autres modèles à comparer ---
from sklearn.ensemble import RandomForestRegressor      # forêt aléatoire : moyenne de nombreux arbres
from sklearn.linear_model import LinearRegression       # régression linéaire : une droite (combinaison de variables)

# --- 2. Reconstituer un entraînement avec les pics aberrants ---
# Mêmes dates que l'entraînement propre, mais cible = mesure brute (pics inclus) au lieu de la cible nettoyée.
avec = d[(d["timestamp"] >= pc.DEBUT_UTILE) & (d["timestamp"] < pc.COUPURE) & d["conso_brute"].notna()].assign(conso_mw=lambda x: x["conso_brute"])
# Somme des True = nombre de pics présents dans cet entraînement
print(int(avec["pic"].sum()), "pics dans l'entraînement")
# Médiane de chaque variable : servira à remplacer les valeurs manquantes (la régression linéaire n'en accepte pas).
med = train[pc.VARIABLES].median()

# --- 3. Définir les trois modèles ---
# n_estimators=100 : 100 arbres ; n_jobs=-1 : tous les processeurs ; random_state=0 : résultat reproductible.
modeles = {"linéaire": LinearRegression(),
           "forêt": RandomForestRegressor(n_estimators=100, random_state=0, n_jobs=-1),
           "gradient boosting": HistGradientBoostingRegressor(random_state=0)}
lignes = {}                                   # résultats : un dictionnaire par modèle
# --- 4. Entraîner chaque modèle avec puis sans pics, toujours tester sur le même test propre ---
for nom, m in modeles.items():                # un modèle à la fois
    ligne = {}                                # erreurs de ce modèle, une par type d'entraînement
    for etiquette, jeu in (("sans pics", train), ("avec pics", avec)):   # les deux entraînements à comparer
        # fit : apprentissage ; fillna(med) : comble les trous avec la médiane
        m.fit(jeu[pc.VARIABLES].fillna(med), jeu["conso_mw"])
        # predict sur le test propre, puis MAE : la même règle pour les deux entraînements
        ligne[etiquette] = mean_absolute_error(test["conso_mw"], m.predict(test[pc.VARIABLES].fillna(med)))   # range la MAE
    lignes[nom] = ligne                       # range les deux erreurs sous le nom du modèle

# --- 5. Afficher le tableau (.T : un modèle par ligne) ---
print(pd.DataFrame(lignes).T.round(3))

# %% Cellule 27 — Régler les hyperparamètres : `GridSearchCV`
# === CELLULE 27 : GridSearchCV ===
# --- 1. Importer l'outil de recherche de réglages ---
from sklearn.model_selection import GridSearchCV

# --- 2. Définir la grille des réglages à essayer ---
# max_depth : profondeur des arbres ; learning_rate : vitesse d'apprentissage ; max_iter : nombre d'arbres.
# 3 x 3 x 2 = 18 combinaisons.
grille = {"max_depth": [3, 6, None], "learning_rate": [0.05, 0.1, 0.3], "max_iter": [100, 300]}

# --- 3. Lancer la recherche avec la validation temporelle ---
# cv=tscv : plis passé -> futur ; scoring : MAE négative ; n_jobs=-1 : calculs en parallèle.
gs = GridSearchCV(HistGradientBoostingRegressor(random_state=0), grille, cv=tscv,
                  scoring="neg_mean_absolute_error", n_jobs=-1)
# fit : essaie chaque combinaison sur chaque pli, puis réentraîne la meilleure sur tout l'entraînement.
gs.fit(ordre[pc.VARIABLES], ordre["conso_mw"])

# --- 4. Lire le meilleur résultat ---
print("Meilleurs réglages :", gs.best_params_)                     # combinaison gagnante
print("MAE validation croisée :", round(-gs.best_score_, 4))       # son erreur moyenne sur les plis (signe remis)

# --- 5. Comparer sur le test (utilisé une seule fois) ---
# Modèle aux réglages par défaut, entraîné sur l'entraînement.
defaut = HistGradientBoostingRegressor(random_state=0).fit(train[pc.VARIABLES], train["conso_mw"])
# predict + MAE sur le test : le défaut d'abord, puis le meilleur modèle de la grille (gs.predict).
print("MAE test, réglages par défaut :", round(mean_absolute_error(test["conso_mw"], defaut.predict(test[pc.VARIABLES])), 4))
print("MAE test, meilleurs réglages  :", round(mean_absolute_error(test["conso_mw"], gs.predict(test[pc.VARIABLES])), 4))

# --- 6. Voir les 3 meilleures combinaisons ---
# cv_results_ : tableau de tous les essais ; on classe par rang et on garde les 3 premiers.
res = pd.DataFrame(gs.cv_results_).sort_values("rank_test_score").head(3)
# On affiche les réglages et le score moyen ; si les scores sont proches, le choix compte peu.
print(res[["param_max_depth", "param_learning_rate", "param_max_iter", "mean_test_score"]].round(3).to_string(index=False))

# %% Cellule 28 — Quelles variables comptent ? `permutation_importance`
# === CELLULE 28 : Importance des variables ===
# --- 1. Importer les outils de dessin, de fichiers et d'importance ---
import matplotlib.pyplot as plt                                   # tracé de figures
from pathlib import Path                                          # gestion des dossiers
from sklearn.inspection import permutation_importance             # mesure l'importance en mélangeant une colonne

# --- 2. Entraîner le modèle final du module ---
# construire_modele : pipeline (encodage du site + gradient boosting) ; fit sur l'entraînement uniquement.
final = pc.construire_modele().fit(train[pc.COLONNES], train["conso_mw"])

# --- 3. Calculer l'importance par permutation sur le test ---
# n_repeats=10 : 10 mélanges par colonne (résultat plus stable) ; random_state=0 : mélanges reproductibles.
# scoring : MAE négative ; l'importance = hausse de l'erreur quand la colonne est mélangée.
r = permutation_importance(final, test[pc.COLONNES], test["conso_mw"], n_repeats=10, random_state=0,
                           scoring="neg_mean_absolute_error", n_jobs=-1)
# importances_mean : moyenne des 10 répétitions ; sort_values : classement (le graphique barh affiche le premier en bas).
importance = pd.Series(r.importances_mean, index=pc.COLONNES).sort_values()
print(importance.sort_values(ascending=False).round(3).to_string())   # affichage du plus important au moins important

# --- 4. Dessiner et enregistrer le graphique ---
Path("out").mkdir(exist_ok=True)                                  # crée le dossier out/ s'il n'existe pas
fig, ax = plt.subplots(figsize=(7, 3.4))                          # une figure, un seul graphique (largeur x hauteur en pouces)
importance.plot.barh(ax=ax, color="#1f77b4")                      # barres horizontales, une par variable
ax.set_xlabel("Hausse de l'erreur (MW) quand la variable est mélangée")   # titre de l'axe horizontal
ax.set_title("Importance par permutation")                        # titre du graphique
ax.grid(alpha=0.3, axis="x")                                      # quadrillage léger vertical
fig.savefig("out/fig_importance.png", dpi=110, bbox_inches="tight")   # fichier image ; bbox_inches : pas de marge coupée

# %% Cellule 29 — Réel contre prévu, et erreur par heure
# === CELLULE 29 : Diagnostic graphique ===
# --- 1. Calculer les prévisions et l'erreur de chaque ligne du test ---
# predict : prévision du modèle final sur le test (jamais vu à l'apprentissage).
t = test.assign(prevu=final.predict(test[pc.COLONNES]))
t["erreur"] = (t["conso_mw"] - t["prevu"]).abs()      # erreur absolue : écart entre réel et prévu, sans signe

# --- 2. Préparer une figure à deux graphiques côte à côte ---
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))   # 1 ligne, 2 colonnes : a1 à gauche, a2 à droite

# --- 3. Graphique de gauche : réel contre prévu ---
a1.scatter(t["conso_mw"], t["prevu"], s=6, alpha=0.5, color="#1f77b4")   # un point par mesure ; alpha : transparence
# Diagonale réel = prévu (prévision parfaite) : plus les points s'en écartent, plus l'erreur est grande.
a1.plot([0, t["conso_mw"].max()], [0, t["conso_mw"].max()], color="#d62728", linestyle="--", linewidth=1)
# Titres des axes, titre du graphique et quadrillage léger
a1.set_xlabel("réel (MW)"); a1.set_ylabel("prévu (MW)"); a1.set_title("Réel contre prévu"); a1.grid(alpha=0.3)

# --- 4. Graphique de droite : erreur moyenne par heure ---
# groupby("heure") puis mean : MAE de chaque heure (0 à 23) ; plot.bar : une barre par heure.
t.groupby("heure")["erreur"].mean().plot.bar(ax=a2, color="#ff7f0e")
# Titres des axes, titre du graphique et quadrillage horizontal
a2.set_xlabel("heure"); a2.set_ylabel("MAE (MW)"); a2.set_title("Erreur moyenne par heure"); a2.grid(alpha=0.3, axis="y")

# --- 5. Ajuster et enregistrer la figure ---
fig.tight_layout()                                     # évite que les titres se chevauchent
fig.savefig("out/fig_diagnostic.png", dpi=110, bbox_inches="tight")   # fichier image dans out/

# --- 6. Repérer les heures difficiles et faciles ---
par_heure = t.groupby("heure")["erreur"].mean()        # MAE par heure
# idxmax / idxmin : l'heure (l'étiquette de ligne) où l'erreur est la plus grande / la plus petite
print("Heure la plus difficile :", int(par_heure.idxmax()), "h | MAE", round(par_heure.max(), 3))
print("Heure la plus facile    :", int(par_heure.idxmin()), "h | MAE", round(par_heure.min(), 3))

# %% Cellule 30 — Une prévision avec marge : régression quantile
# === CELLULE 30 : Fourchette de prévision ===
# --- 1. Définir une fonction qui prédit une borne basse et une borne haute ---
# **reglages : réglages optionnels transmis tels quels aux deux modèles (rien = réglages par défaut).
def fourchette(**reglages):
    # loss="quantile" avec quantile=0.1 : le modèle apprend une valeur sous laquelle tombent 10 % des mesures.
    bas = HistGradientBoostingRegressor(loss="quantile", quantile=0.1, random_state=0, **reglages).fit(train[pc.VARIABLES], train["conso_mw"])
    # quantile=0.9 : valeur sous laquelle tombent 90 % des mesures ; entre les deux, 80 % des mesures.
    haut = HistGradientBoostingRegressor(loss="quantile", quantile=0.9, random_state=0, **reglages).fit(train[pc.VARIABLES], train["conso_mw"])
    # predict sur le test : une borne basse et une borne haute par ligne
    return bas.predict(test[pc.VARIABLES]), haut.predict(test[pc.VARIABLES])

# --- 2. Comparer deux réglages : par défaut et plus prudent ---
# max_depth=3 : arbres peu profonds ; min_samples_leaf=40 : au moins 40 lignes par feuille (modèle moins nerveux).
for nom, reglages in (("réglages par défaut", {}), ("plus prudent (feuilles ≥ 40)", {"max_depth": 3, "min_samples_leaf": 40})):
    q10, q90 = fourchette(**reglages)                  # bornes basse et haute du test
    # Une mesure est "dans" la fourchette si elle est entre les deux bornes (True/False par ligne).
    dans = (test["conso_mw"] >= q10) & (test["conso_mw"] <= q90)
    # dans.mean() = part de True = couverture (visée : 80 %) ; largeur = écart moyen entre les bornes
    print(f"{nom:<30} couverture {dans.mean():.1%} (visé 80 %) | largeur moyenne {(q90 - q10).mean():.3f} MW")

# %% Cellule 31 — La règle métier : taux de charge supérieur à 1
# === CELLULE 31 : Règle de taux de charge ===
# --- 1. Préparer les mesures brutes et le taux de charge ---
# On garde les lignes où la mesure brute existe (les pics ne sont pas encore retirés) ; copy évite les avertissements.
a = d[d["conso_brute"].notna()].copy()
a["taux_brut"] = a["conso_brute"] / a["capacity_mw"]   # taux de charge : mesure divisée par la capacité du site
vrais = a["pic"]                                       # vérité connue : True pour les 15 pics injectés

# --- 2. Définir une fonction de bilan ---
# Entrée : predits, série True/False (True = alerte). Sortie : dictionnaire VP, FP, FN, précision, rappel.
def bilan(predits):
    vp = int((vrais & predits).sum())      # vrais positifs : vrais pics signalés
    fp = int((~vrais & predits).sum())     # faux positifs : alertes sur des points normaux
    fn = int((vrais & ~predits).sum())     # faux négatifs : vrais pics manqués
    # précision = part des alertes qui sont de vrais pics ; rappel = part des vrais pics retrouvés ;
    # max(..., 1) évite une division par zéro.
    return {"VP": vp, "FP": fp, "FN": fn,
            "précision": round(vp / max(vp + fp, 1), 2), "rappel": round(vp / max(vp + fn, 1), 2)}

# --- 3. Appliquer la règle "taux > 1" (aucun apprentissage) ---
print(len(a), "mesures valides,", int(vrais.sum()), "pics")   # taille du jeu et nombre de pics à retrouver
print("Règle taux > 1 :", bilan(a["taux_brut"] > 1))          # alerte si la mesure dépasse la capacité

# %% Cellule 32 — `IsolationForest` sur la consommation brute
# === CELLULE 32 : IsolationForest, consommation brute ===
# --- 1. Importer le modèle ---
from sklearn.ensemble import IsolationForest    # détecte les points rares en les isolant par coupes aléatoires

# --- 2. Fixer la proportion d'anomalies attendue ---
taux_anomalie = vrais.mean()                    # moyenne de True/False = part de pics (15 sur le total)

# --- 3. Entraîner le détecteur ---
# contamination : part de points à déclarer anormaux ; random_state=0 : résultat reproductible.
# fit : apprend sur la seule colonne de consommation brute (les doubles crochets donnent un tableau).
iso = IsolationForest(contamination=taux_anomalie, random_state=0).fit(a[["conso_brute"]])

# --- 4. Prédire et faire le bilan ---
# predict renvoie -1 (anomalie) ou 1 (normal) ; "== -1" le convertit en True/False.
predits = iso.predict(a[["conso_brute"]]) == -1
print("Consommation brute :", bilan(predits))   # VP, FP, FN, précision, rappel

# --- 5. Regarder les 6 alertes les plus basses ---
# loc[masque, colonnes] : lignes signalées ; tri par consommation ; head(6) : les 6 premières.
print(a.loc[predits, ["site_id", "conso_brute", "pic"]].sort_values("conso_brute").head(6).to_string(index=False))

# %% Cellule 33 — La même méthode sur le taux de charge
# === CELLULE 33 : IsolationForest, taux de charge ===
# --- 1. Détecteur avec contamination fixée, sur le taux de charge ---
# Même algorithme, autre variable : le taux rend les six sites comparables.
iso_t = IsolationForest(contamination=taux_anomalie, random_state=0).fit(a[["taux_brut"]])   # apprentissage
predits_t = iso_t.predict(a[["taux_brut"]]) == -1     # -1 = anomalie, converti en True/False
print("Taux de charge, contamination fixée :", bilan(predits_t))   # bilan à comparer avec la cellule précédente

# --- 2. Détecteur avec contamination automatique ---
# contamination="auto" : le modèle choisit seul son seuil (sans connaître la vérité).
auto = IsolationForest(contamination="auto", random_state=0).fit(a[["taux_brut"]])
predits_auto = auto.predict(a[["taux_brut"]]) == -1   # alertes sous ce seuil automatique
# Le nombre d'alertes montre si le seuil auto est trop généreux ou trop strict.
print("Taux de charge, contamination auto  :", bilan(predits_auto), "|", int(predits_auto.sum()), "alertes")

# %% Cellule 34 — Deux algorithmes, trois jeux de variables
# === CELLULE 34 : Comparatif ===
# --- 1. Importer le second algorithme ---
from sklearn.neighbors import LocalOutlierFactor   # compare la densité d'un point à celle de ses voisins

# --- 2. Définir les trois jeux de variables à tester ---
jeux = {"conso brute": ["conso_brute"], "taux": ["taux_brut"], "taux + heure": ["taux_brut", "heure"]}
lignes = []                                        # une ligne de résultats par combinaison

# --- 3. Essayer chaque algorithme sur chaque jeu ---
for nom_jeu, cols in jeux.items():
    # Trois détecteurs, tous avec la même contamination : la comparaison est équitable.
    # n_neighbors : nombre de voisins regardés par LOF (20 puis 50).
    for nom_algo, algo in (("IsolationForest", IsolationForest(contamination=taux_anomalie, random_state=0)),
                           ("LOF, 20 voisins", LocalOutlierFactor(n_neighbors=20, contamination=taux_anomalie)),
                           ("LOF, 50 voisins", LocalOutlierFactor(n_neighbors=50, contamination=taux_anomalie))):
        # fit_predict : apprend et prédit en une étape (LOF n'a pas de predict séparé) ; -1 = anomalie.
        p = algo.fit_predict(a[cols]) == -1
        # **bilan(p) : ajoute VP, FP, FN, précision, rappel à la ligne de résultats
        lignes.append({"variables": nom_jeu, "algorithme": nom_algo, **bilan(p)})

# --- 4. Afficher le tableau comparatif ---
print(pd.DataFrame(lignes).to_string(index=False))

# %% Cellule 35 — Classer plutôt que trancher : les scores d'anomalie
# === CELLULE 35 : Scores d'anomalie ===
# --- 1. Calculer un score par mesure ---
# score_samples : score continu de l'IsolationForest ; plus il est bas, plus le point est anormal.
a["score"] = iso_t.score_samples(a[["taux_brut"]])

# --- 2. Classer du plus suspect au moins suspect ---
classement = a.sort_values("score")                  # tri croissant : les plus anormaux en tête
# Les 3 plus suspects : site, taux, score, et vrai pic ou non
print(classement[["site_id", "taux_brut", "score", "pic"]].head(3).round(3).to_string(index=False))

# --- 3. Mesurer la qualité du classement ---
# Précision@15 : part de vrais pics parmi les 15 premiers (True = 1, False = 0, donc la moyenne suffit).
print("Précision@15 :", round(classement["pic"].head(15).mean(), 2))
# Écart entre le 15e et le 16e score : un grand saut indique une frontière nette entre pics et normaux.
print("Écart entre le 15e et le 16e score :", round(classement["score"].iloc[15] - classement["score"].iloc[14], 3))
# Écart moyen entre deux scores voisins : référence pour juger si le saut précédent est grand.
print("Écart moyen entre deux scores voisins :", round(classement["score"].diff().abs().mean(), 5))

# %% Cellule 36 — Anomalies par le modèle de prévision : les résidus
# === CELLULE 36 : Résidus du modèle ===
# --- 1. Reprendre les mesures brutes (pics inclus) ---
# On garde les lignes dès la date utile où la mesure brute existe ; copy évite les avertissements.
b = d[(d["timestamp"] >= pc.DEBUT_UTILE) & d["conso_brute"].notna()].copy()

# --- 2. Calculer prévision et résidu ---
# predict : prévision du modèle final (entraîné sans les pics) pour chaque ligne.
b["prevu"] = final.predict(b[pc.COLONNES])
b["residu"] = b["conso_brute"] - b["prevu"]          # résidu : mesure moins prévision (signe conservé)
# Résidu centré sur sa médiane et divisé par l'écart-type : combien d'écarts-types la mesure s'éloigne du normal.
b["z"] = (b["residu"] - b["residu"].median()) / b["residu"].std()

# --- 3. Retenir les 15 plus gros résidus ---
# On trie par résidu absolu décroissant : reindex remet les lignes dans cet ordre ; head(15) garde les 15 premières.
haut = b.reindex(b["residu"].abs().sort_values(ascending=False).index).head(15)
print("Parmi les 15 plus gros résidus :", int(haut["pic"].sum()), "pics")   # combien sont de vrais pics
# Les 3 premiers avec leur prévision arrondie (assign remplace la colonne prevu par sa version arrondie)
print(haut[["site_id", "timestamp", "conso_brute", "prevu"]].head(3).assign(prevu=lambda x: x["prevu"].round(2)).to_string(index=False))

# --- 4. Donner l'ordre de grandeur d'un résidu normal ---
# ~b["pic"] : lignes qui ne sont pas des pics ; on prend la médiane de leur résidu absolu.
print("Résidu médian des mesures normales :", round(b.loc[~b["pic"], "residu"].abs().median(), 3), "MW")

# %% Cellule 37 — Piège : chercher des anomalies dans des données non nettoyées
# === CELLULE 37 : Données non nettoyées ===
# --- 1. Charger les données brutes, sans aucun nettoyage ---
# Référence des sites : on ne garde que l'identifiant et la capacité ; encoding="utf-8-sig" gère l'en-tête du fichier.
ref = pd.read_csv("data/sites_reference.csv", encoding="utf-8-sig")[["site_id", "capacity_mw"]]
# Mesures brutes ; rename : la colonne consumption_mw devient conso_mw (nom utilisé partout).
brut = pd.read_csv("data/consommation_30jours.csv", encoding="utf-8-sig").rename(columns={"consumption_mw": "conso_mw"})
# Doublons retirés, capacité ajoutée par site (merge), lignes vides écartées (dropna) : les codes -999 restent.
sale = brut.drop_duplicates().merge(ref, on="site_id").dropna(subset=["conso_mw"])
sale = sale.assign(taux=sale["conso_mw"] / sale["capacity_mw"])   # taux de charge, codes capteur compris

# --- 2. Lancer le détecteur comme avant ---
# contamination : 15 alertes attendues sur l'ensemble ; random_state=0 : résultat reproductible.
iso_s = IsolationForest(contamination=15 / len(sale), random_state=0).fit(sale[["taux"]])
alertes = sale[iso_s.predict(sale[["taux"]]) == -1]   # lignes signalées (-1 = anomalie)

# --- 3. Voir ce qui est vraiment signalé ---
# value_counts : nombre d'alertes par valeur de conso_mw ; les codes -999, -888, -777 apparaissent-ils ?
print(len(alertes), "alertes | valeurs de conso_mw signalées :", alertes["conso_mw"].value_counts().to_dict())
# Un vrai pic a un taux > 1 : on compte les vrais pics réellement trouvés parmi les alertes.
print("Pics réellement trouvés :", int((alertes["taux"] > 1).sum()))

# %% Cellule 38 — Voir les anomalies détectées
# === CELLULE 38 : Figure anomalies ===
# --- 1. Importer les outils de dessin et de fichiers ---
import matplotlib.pyplot as plt     # tracé de figures
from pathlib import Path            # gestion des dossiers

# --- 2. Préparer les données et la figure ---
Path("out").mkdir(exist_ok=True)    # crée le dossier out/ s'il n'existe pas
a["alerte"] = predits_t             # colonne True/False : anomalie retenue par IsolationForest sur le taux de charge
# 2 lignes x 3 colonnes = un panneau par site ; sharey=True : même échelle verticale, donc sites comparables.
fig, axes = plt.subplots(2, 3, figsize=(11, 5), sharey=True)

# --- 3. Un panneau par site ---
# groupby("site_id") : un sous-tableau g par site ; zip l'associe à un panneau (axes.ravel() met les 6 panneaux en liste).
for ax, (site, g) in zip(axes.ravel(), a.groupby("site_id")):
    ax.plot(g["timestamp"], g["taux_brut"], color="#1f77b4", linewidth=0.6)   # courbe du taux de charge dans le temps
    # Points rouges : uniquement les mesures signalées comme anomalies ; zorder=3 les place au-dessus de la courbe.
    ax.scatter(g.loc[g["alerte"], "timestamp"], g.loc[g["alerte"], "taux_brut"], color="#d62728", s=18, zorder=3)
    ax.axhline(1, color="#7f7f7f", linestyle="--", linewidth=0.8)             # ligne pointillée : capacité (taux = 1)
    ax.set_title(site, fontsize=9); ax.grid(alpha=0.3)                        # nom du site en titre, quadrillage léger
    ax.tick_params(axis="x", labelsize=7, rotation=30)                        # dates plus petites et inclinées, lisibles

# --- 4. Titre commun, mise en page et sauvegarde ---
fig.supylabel("taux de charge")        # titre de l'axe vertical commun aux 6 panneaux
fig.tight_layout()                     # évite que les éléments se chevauchent
fig.savefig("out/fig_anomalies.png", dpi=110, bbox_inches="tight")   # fichier image dans out/
print(int(a["alerte"].sum()), "alertes affichées")   # nombre total de points rouges

# %% Cellule 39 — Un profil par site et par jour
# === CELLULE 39 : Profils journaliers ===
# --- 1. Combler les manquants et repérer chaque jour (site par site) ---
# assign() renvoie une copie de d avec deux colonnes en plus ; d n'est pas modifié.
comble = d.assign(
    # groupby("site_id") : chaque site est traité seul, pour ne jamais mélanger deux sites.
    # interpolate : remplace un trou par une valeur entre ses voisins ; "both" gère aussi les bords.
    conso_i=d.groupby("site_id")["conso_mw"].transform(lambda s: s.interpolate(limit_direction="both")),
    # normalize() : ramène l'horodatage à minuit, ce qui donne la date du jour.
    jour=d["timestamp"].dt.normalize())

# --- 2. Un tableau « une ligne = un site et un jour, une colonne = une heure » ---
# pivot_table : range les 24 valeurs de chaque site-jour sur une même ligne (24 colonnes).
absolus = comble.pivot_table(index=["site_id", "jour"], columns="heure", values="conso_i")
# On divise chaque ligne par sa moyenne : 1 = niveau moyen du jour, 1,3 = 30 % au-dessus.
# axis=1 : la moyenne est calculée par ligne ; axis=0 : la division s'applique ligne par ligne.
formes = absolus.div(absolus.mean(axis=1), axis=0)

# --- 3. Contrôler le résultat ---
# Attendu : 180 lignes (6 x 30) et 24 colonnes, sans valeur manquante.
print(formes.shape, "| valeurs manquantes :", int(formes.isna().sum().sum()))
# Deux premières lignes, colonnes des heures 0, 6, 12 et 18 seulement, pour rester lisible.
print(formes.iloc[:2, [0, 6, 12, 18]].round(2))

# --- 4. Retrouver le type de chaque site (sert plus loin à juger les regroupements) ---
# Une ligne par site (drop_duplicates), indexée par l'identifiant du site.
types = d.drop_duplicates("site_id").set_index("site_id")["site_type"]
# On lit l'identifiant de site de chaque ligne de formes et on en déduit son type.
type_jour = formes.index.get_level_values("site_id").map(types).to_numpy(dtype=object)
# Nombre de profils par type : 30 jours par site, donc un multiple de 30.
print(pd.Series(type_jour).value_counts().to_dict())

# %% Cellule 40 — Combien de groupes ? Inertie et silhouette
# === CELLULE 40 : Choisir k ===
# --- 1. Importer les outils ---
# KMeans : algorithme qui regroupe des courbes proches, sans connaître de réponse à l'avance.
from sklearn.cluster import KMeans
# silhouette_score : note de 1 à -1 qui dit si les groupes sont bien séparés.
from sklearn.metrics import silhouette_score

# --- 2. Essayer plusieurs nombres de groupes et comparer ---
# k est le nombre de groupes demandé ; on teste 2, 3, 4, 5 et 6.
for k in range(2, 7):
    # n_clusters=k : nombre de groupes à former.
    # n_init=10 : l'algorithme démarre 10 fois avec des centres différents et garde le meilleur.
    # random_state=0 : tirages fixés, donc résultat reproductible.
    # fit(formes) : apprend les groupes à partir des 180 profils (aucune étiquette fournie).
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(formes)
    # inertia_ : distance totale des profils à leur centre (baisse toujours quand k monte).
    # labels_ : groupe attribué à chaque profil, utilisé par la silhouette.
    print(f"k = {k} | inertie {km.inertia_:7.2f} | silhouette {silhouette_score(formes, km.labels_):.3f}")

# %% Cellule 41 — Les familles trouvées, comparées aux types connus
# === CELLULE 41 : KMeans, k = 3 ===
# --- 1. Importer la mesure de comparaison ---
# adjusted_rand_score : compare deux regroupements ; 1 = identiques, 0 = hasard.
from sklearn.metrics import adjusted_rand_score

# --- 2. Former les 3 groupes retenus ---
# Mêmes réglages qu'avant : 3 groupes, 10 départs, tirages fixés (random_state=0).
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(formes)

# --- 3. Comparer les groupes trouvés aux types de sites réels ---
# crosstab : compte, pour chaque type de site, combien de profils sont tombés dans chaque groupe.
# Les Series reçoivent un nom pour titrer lignes et colonnes du tableau.
print(pd.crosstab(pd.Series(type_jour, name="type de site"), pd.Series(km.labels_, name="groupe")))
# Un seul chiffre pour résumer l'accord entre groupes et types (l'algorithme ne connaissait pas les types).
print("Indice de Rand ajusté :", round(adjusted_rand_score(type_jour, km.labels_), 3))

# %% Cellule 42 — Le profil moyen de chaque groupe
# === CELLULE 42 : Figure des groupes ===
# --- 1. Importer les outils de dessin ---
import matplotlib.pyplot as plt
from pathlib import Path

# --- 2. Préparer le dossier de sortie et la figure ---
# Les figures sont rangées dans out/ pour les retrouver et les réutiliser.
# exist_ok=True : pas d'erreur si le dossier out existe déjà.
Path("out").mkdir(exist_ok=True)
# fig = la feuille, ax = le graphique ; figsize = largeur et hauteur en pouces.
fig, ax = plt.subplots(figsize=(8, 3.6))

# --- 3. Tracer une courbe par groupe ---
# cluster_centers_ : une ligne par groupe, 24 valeurs = son profil moyen.
for i, centre in enumerate(km.cluster_centers_):
    # Type de site le plus fréquent dans ce groupe (mode), pour aider à le nommer.
    type_majoritaire = pd.Series(type_jour[km.labels_ == i]).mode()[0]
    # Abscisse = heures 0 à 23 ; marker="o" : un point par heure ; label : texte de la légende.
    ax.plot(range(24), centre, marker="o", markersize=3, label=f"groupe {i} ({type_majoritaire})")

# --- 4. Titre, axes, légende et grille ---
# Chaque appel ci-dessous habille le graphique ax.
# Axes : heure en abscisse, consommation rapportée à la moyenne du jour en ordonnée.
ax.set_xlabel("heure"); ax.set_ylabel("consommation / moyenne du jour")
ax.set_title("Profils moyens des trois groupes")
# Graduation toutes les 2 heures ; légende ; grille discrète (alpha = transparence).
ax.set_xticks(range(0, 24, 2)); ax.legend(); ax.grid(alpha=0.3)

# --- 5. Enregistrer et lire la pointe de chaque groupe ---
# dpi=110 : résolution ; bbox_inches="tight" : rogne les marges blanches.
fig.savefig("out/fig_groupes.png", dpi=110, bbox_inches="tight")
# Valeur maximale de chaque profil moyen : mesure l'intensité de la pointe.
print(np.round(km.cluster_centers_.max(axis=1), 2), "pointe de chaque groupe")

# %% Cellule 43 — Pourquoi mettre à l'échelle : `StandardScaler`
# === CELLULE 43 : Mise à l'échelle ===
# --- 1. Importer l'outil de mise à l'échelle ---
# StandardScaler : recentre chaque colonne (moyenne 0) et la réduit (écart-type 1).
from sklearn.preprocessing import StandardScaler

# --- 2. Résumer chaque site-jour par trois variables d'unités très différentes ---
# Un DataFrame construit à partir d'un dictionnaire : une clé = une colonne.
resume = pd.DataFrame({
    # Consommation moyenne du jour, multipliée par 1000 pour passer en kW (valeurs de l'ordre des centaines).
    "moyenne_kw": absolus.mean(axis=1) * 1000,
    # Nuit (heures 0 à 5) sur jour (heures 8 à 17) : petit chiffre, autour de 0 à 4.
    # .loc[:, 0:5] : toutes les lignes, colonnes des heures 0 à 5 (bornes incluses).
    "ratio_nuit_jour": absolus.loc[:, 0:5].mean(axis=1) / absolus.loc[:, 8:17].mean(axis=1),
    # Maximum sur minimum du jour : mesure à quel point la courbe varie.
    "contraste": absolus.max(axis=1) / absolus.min(axis=1),
})
# Moyenne et écart-type de chaque colonne : les échelles n'ont rien de commun.
# describe() : statistiques ; .loc garde seulement les lignes mean et std.
print(resume.describe().loc[["mean", "std"]].round(2))

# --- 3. Regrouper sans, puis avec mise à l'échelle ---
# Sans : la colonne en kW domine les distances et écrase les deux autres.
sans = KMeans(n_clusters=3, n_init=10, random_state=0).fit(resume)
# Avec : fit_transform apprend moyenne et écart-type de chaque colonne, puis les applique.
avec = KMeans(n_clusters=3, n_init=10, random_state=0).fit(StandardScaler().fit_transform(resume))

# --- 4. Comparer aux vrais types de sites ---
# type_jour n'a servi ni à l'un ni à l'autre regroupement : il ne sert qu'à noter le résultat.
# Plus le Rand ajusté est proche de 1, plus les groupes retrouvent les types réels.
print("Rand ajusté sans mise à l'échelle :", round(adjusted_rand_score(type_jour, sans.labels_), 3))
print("Rand ajusté avec mise à l'échelle :", round(adjusted_rand_score(type_jour, avec.labels_), 3))

# %% Cellule 44 — Classer le type de site : validation par site
# === CELLULE 44 : Classification du type de site ===
# --- 1. Importer les outils ---
# RandomForestClassifier : forêt d'arbres de décision qui vote pour une catégorie.
from sklearn.ensemble import RandomForestClassifier
# accuracy_score : part de bonnes réponses ; confusion_matrix : qui est pris pour qui.
from sklearn.metrics import accuracy_score, confusion_matrix
# LeaveOneGroupOut : à chaque tour, un site entier est mis de côté pour le test.
# cross_val_predict : rend la prédiction faite sur chaque ligne quand elle était au test.
from sklearn.model_selection import LeaveOneGroupOut, cross_val_predict

# --- 2. Préparer le modèle et les groupes de validation ---
# Identifiant de site de chaque profil : les 30 jours d'un site restent ensemble.
sites = formes.index.get_level_values("site_id").to_numpy(dtype=object)
# 200 arbres ; random_state=0 : résultat reproductible.
clf = RandomForestClassifier(n_estimators=200, random_state=0)

# --- 3. Prédire chaque site sans l'avoir vu à l'entraînement ---
# X = formes, réponse = type_jour ; groups=sites indique à quel site appartient chaque ligne.
predit = cross_val_predict(clf, formes, type_jour, groups=sites, cv=LeaveOneGroupOut())

# --- 4. Mesurer la qualité ---
# Ordre des classes utilisé pour lignes et colonnes de la matrice.
noms = ["Industrie", "Commercial", "Residentiel"]
# Part de profils dont le type est bien deviné.
print("Précision globale :", accuracy_score(type_jour, predit))
# Lignes = type réel, colonnes = type prédit ; la diagonale compte les bonnes réponses.
print(pd.DataFrame(confusion_matrix(type_jour, predit, labels=noms), index=noms, columns=noms))

# %% Cellule 45 — Classes déséquilibrées : reconnaître un jour de week-end
# === CELLULE 45 : Jour de week-end ===
# --- 1. Importer les outils ---
# DummyClassifier : modèle témoin qui applique une règle simple (ici : toujours la classe la plus fréquente).
from sklearn.dummy import DummyClassifier
# LogisticRegression : modèle linéaire qui calcule une probabilité.
from sklearn.linear_model import LogisticRegression
# Trois mesures : F1 = compromis entre précision et rappel.
from sklearn.metrics import f1_score, precision_score, recall_score

# --- 2. Construire les profils relatifs au niveau habituel du site ---
# Moyenne de chaque site, répétée sur chacune de ses lignes.
niveau = comble.groupby("site_id")["conso_i"].transform("mean")
# rel = consommation / niveau du site ; puis même mise en tableau que pour les profils (site-jour x 24 heures).
relatif = comble.assign(rel=comble["conso_i"] / niveau).pivot_table(index=["site_id", "jour"], columns="heure", values="rel")

# --- 3. Définir la cible et couper le temps en deux ---
# Date de chaque profil.
jour = relatif.index.get_level_values("jour")
# Cible y : 1 si samedi ou dimanche (dayofweek 5 ou 6), sinon 0.
y = (jour.dayofweek >= 5).astype(int)
# passe = avant la date de coupure (entraînement) ; futur = après (test). On ne mélange pas les périodes.
passe, futur = jour < pc.COUPURE, jour >= pc.COUPURE
# Nombre de week-ends sur nombre de jours dans chaque période.
print("Week-ends : entraînement", int(y[passe].sum()), "/", int(passe.sum()), "| test", int(y[futur].sum()), "/", int(futur.sum()))

# --- 4. Trois candidats, du plus simple au plus riche ---
# Témoin : répond toujours la classe la plus fréquente (most_frequent), sans regarder les données.
# Régression logistique : max_iter = nombre d'itérations permises pour converger.
# Forêt : 200 arbres, random_state=0 pour un résultat reproductible.
candidats = {"toujours « semaine »": DummyClassifier(strategy="most_frequent"),
             "régression logistique": LogisticRegression(max_iter=1000),
             "forêt": RandomForestClassifier(n_estimators=200, random_state=0)}
lignes = {}

# --- 5. Entraîner et évaluer chaque candidat sur la période de test ---
for nom, m in candidats.items():
    # fit : apprentissage sur le passé uniquement.
    m.fit(relatif[passe], y[passe])
    # predict : 0 ou 1 pour chaque jour du futur.
    p = m.predict(relatif[futur])
    # zero_division=0 : renvoie 0 (et non une erreur) si le modèle ne prédit jamais « week-end ».
    # exactitude = part de bonnes réponses ; précision = alertes justes / alertes données ;
    # rappel = week-ends trouvés / week-ends réels ; F1 = moyenne équilibrée des deux précédentes.
    lignes[nom] = {"exactitude": accuracy_score(y[futur], p),  # bonnes réponses
                   "précision": precision_score(y[futur], p, zero_division=0),  # alertes justes
                   "rappel": recall_score(y[futur], p),  # week-ends retrouvés
                   "F1": f1_score(y[futur], p)}  # compromis précision / rappel

# --- 6. Comparer les candidats ---
# Une ligne par modèle (.T transpose le tableau), arrondi à 2 décimales.
print(pd.DataFrame(lignes).T.round(2))

# %% Cellule 46 — Régler le seuil : précision contre rappel
# === CELLULE 46 : Seuil de décision ===
# --- 1. Obtenir une probabilité de week-end pour chaque jour du test ---
# Régression logistique entraînée sur le passé (max_iter=1000 : laisse le temps de converger).
logit = LogisticRegression(max_iter=1000).fit(relatif[passe], y[passe])
# predict_proba : deux colonnes (semaine, week-end) ; [:, 1] garde la probabilité de week-end.
proba = logit.predict_proba(relatif[futur])[:, 1]

# --- 2. Faire varier le seuil de décision ---
for seuil in (0.5, 0.3, 0.2, 0.1):
    # Un jour est déclaré week-end si sa probabilité atteint le seuil (1 = oui, 0 = non).
    p = (proba >= seuil).astype(int)
    # Seuil bas : le rappel monte, la précision baisse (plus de fausses alertes).
    print(f"seuil {seuil:.1f} | précision {precision_score(y[futur], p, zero_division=0):.2f} | rappel {recall_score(y[futur], p):.2f}")

# --- 3. Autre levier : donner plus de poids à la classe rare ---
# class_weight="balanced" : une erreur sur un week-end (rare) coûte davantage pendant l'apprentissage.
equilibre = LogisticRegression(max_iter=1000, class_weight="balanced").fit(relatif[passe], y[passe])
# predict garde ici le seuil 0,5 ; c'est le modèle lui-même qui a changé.
p = equilibre.predict(relatif[futur])
print(f"class_weight balanced | précision {precision_score(y[futur], p, zero_division=0):.2f} | rappel {recall_score(y[futur], p):.2f}")

# %% Cellule 47 — Sauvegarder et recharger un modèle avec `joblib`
# === CELLULE 47 : joblib ===
# --- 1. Importer les outils ---
import json  # écrire le fichier de métadonnées
from pathlib import Path  # manipuler chemins et dossiers

import joblib  # enregistre et relit des objets Python (dont les modèles)
import sklearn  # sert ici à lire le numéro de version

# --- 2. Entraîner le pipeline final et l'écrire sur disque ---
# Crée le dossier modeles s'il n'existe pas (exist_ok=True : pas d'erreur sinon).
Path("modeles").mkdir(exist_ok=True)
# construire_modele() : pipeline du module ; fit apprend sur la période d'entraînement.
modele = pc.construire_modele().fit(train[pc.COLONNES], train["conso_mw"])
# dump : sérialise le modèle entraîné dans un fichier .joblib.
joblib.dump(modele, "modeles/modele_conso.joblib")

# --- 3. Écrire les métadonnées à côté du modèle ---
# Version de scikit-learn, variables attendues, date de fin d'entraînement et MAE sur le test :
# ce qu'il faut savoir avant de réutiliser le fichier ailleurs.
meta = {"scikit_learn": sklearn.__version__, "variables": pc.COLONNES, "entraine_jusqu_au": "2025-01-23",
        "mae_test": round(pc.evaluer(test["conso_mw"], modele.predict(test[pc.COLONNES]))["MAE"], 4)}
# indent=2 : JSON lisible ; ensure_ascii=False : garde les accents ; UTF-8 pour la relecture.
Path("modeles/modele_conso.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

# --- 4. Recharger et vérifier que rien n'a changé ---
# load : relit le fichier et rend un objet identique au modèle d'origine.
recharge = joblib.load("modeles/modele_conso.joblib")
# allclose : vrai si toutes les prévisions sont égales (aux arrondis machine près).
memes = np.allclose(modele.predict(test[pc.COLONNES]), recharge.predict(test[pc.COLONNES]))
# Taille du fichier en Ko (octets / 1024).
print("Taille du fichier :", round(Path("modeles/modele_conso.joblib").stat().st_size / 1024), "Ko")
print("Prévisions identiques après rechargement :", memes)
print(meta)

# %% Cellule 48 — Le modèle change de machine : entraîné ici, lu par un scikit-learn plus ancien
# === CELLULE 48 : Modèle récent, bibliothèque ancienne ===
# --- 1. Trouver l'interpréteur Python de l'ancien environnement ---
import os  # os.name : "nt" sous Windows
import subprocess  # lance un autre programme depuis le notebook

# os.name vaut "nt" sous Windows, "posix" ailleurs.
# Sous Windows l'exécutable est dans Scripts, ailleurs dans bin.
python_ancien = Path(".venv-ml-ancien") / ("Scripts" if os.name == "nt" else "bin") / "python"

# Chemin construit avec / : Path("...") / "bin" / "python" équivaut à .venv-ml-ancien/bin/python.
# --- 2. Entraîner ici, avec la version récente, et préparer des exemples ---
# HistGradientBoostingRegressor : modèle de boosting ; random_state=0 : reproductible.
hgb_ici = HistGradientBoostingRegressor(random_state=0).fit(train[pc.VARIABLES], train["conso_mw"])
# Sauvegarde du modèle : c'est ce fichier que l'ancien environnement va tenter de lire.
joblib.dump(hgb_ici, "modeles/hgb_ici.joblib")
# index=False : n'écrit pas le numéro de ligne dans le fichier.
# Trois lignes d'exemple en CSV, que l'autre programme relira (les deux processus ne partagent pas de mémoire).
test[pc.VARIABLES].head(3).to_csv("out/exemples.csv", index=False)
# Version utilisée ici et prévisions de référence (round(3) : 3 décimales).
# .head(3) : les 3 premières lignes du test ; ce sont les mêmes exemples que dans le CSV.
print("Ici      : scikit-learn", sklearn.__version__, "| prévisions", hgb_ici.predict(test[pc.VARIABLES].head(3)).round(3))

# --- 3. Écrire le petit programme que l'ancien Python va exécuter ---
# Le texte ci-dessous est du code Python stocké dans une chaîne : il ne s'exécute pas dans ce notebook.
# Il relit les exemples, charge le modèle en capturant les avertissements, puis prédit et affiche la version.
lecture = """
import warnings, joblib, pandas as pd, sklearn
X = pd.read_csv("out/exemples.csv")
with warnings.catch_warnings(record=True) as avis:
    warnings.simplefilter("always")
    m = joblib.load("modeles/hgb_ici.joblib")
print("Ancien   : scikit-learn", sklearn.__version__, "| prévisions", m.predict(X).round(3))
print("Avertissement :", avis[0].category.__name__ if avis else "aucun")
"""

# --- 4. Lancer l'ancien interpréteur et afficher son résultat ---
# subprocess.run : lance un programme, attend la fin et rend un objet r (r.stdout : affichage, r.stderr : erreurs).
# Liste des arguments : l'exécutable de l'ancien Python, l'option -c, puis le texte du programme.
# "-c" : exécute le texte fourni ; capture_output=True : récupère ce qu'il affiche ; text=True : en texte.
r = subprocess.run([str(python_ancien), "-c", lecture], capture_output=True, text=True)
# Affiche la sortie normale ; en cas d'échec, les 400 derniers caractères de l'erreur.
print(r.stdout.strip() or r.stderr.strip()[-400:])

# %% Cellule 49 — Le modèle vieillit : entraîné avec l'ancienne version, lu par la récente
# === CELLULE 49 : Modèle ancien, bibliothèque récente ===
# --- 1. Importer les outils ---
import warnings  # capter les avertissements de version au chargement
from sklearn.ensemble import RandomForestRegressor  # forêt aléatoire (deuxième modèle testé)

# Les deux modèles seront entraînés par un autre programme : il faut lui fournir les données dans un fichier.
# --- 2. Donner les données d'entraînement à l'ancien environnement ---
# CSV : moyen de passer les données à un autre programme.
train[pc.VARIABLES + ["conso_mw"]].to_csv("out/apprentissage.csv", index=False)

# --- 3. Écrire le programme d'entraînement exécuté par l'ancien Python ---
# Chaîne de texte contenant du code : elle ne s'exécute pas ici. Elle relit le CSV,
# sépare X (variables) et y (cible), entraîne les deux modèles et les sauvegarde.
entrainement = """
import joblib, pandas as pd, sklearn
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
t = pd.read_csv("out/apprentissage.csv")
X, y = t.drop(columns="conso_mw"), t["conso_mw"]
joblib.dump(HistGradientBoostingRegressor(random_state=0).fit(X, y), "modeles/hgb_ancien.joblib")
joblib.dump(RandomForestRegressor(n_estimators=50, random_state=0).fit(X.fillna(0), y), "modeles/foret_ancien.joblib")
print("Entraîné avec scikit-learn", sklearn.__version__)
"""
# --- 4. Lancer l'entraînement dans l'ancien environnement ---
# subprocess.run : exécute l'interpréteur ancien avec "-c" (texte à exécuter) ; capture_output et text récupèrent l'affichage.
r = subprocess.run([str(python_ancien), "-c", entrainement], capture_output=True, text=True)
# Sortie normale ; sinon fin du message d'erreur.
# [-400:] : les 400 derniers caractères, là où se trouve la cause de l'échec.
print(r.stdout.strip() or r.stderr.strip()[-400:])

# Si le chargement se passe mal, on veut voir l'erreur ou l'avertissement sans arrêter la boucle.
# --- 5. Relire ici, avec la version récente, les deux modèles anciens ---
# nom : radical du fichier ; on relit successivement le boosting puis la forêt.
for nom in ("hgb_ancien", "foret_ancien"):
    # record=True : les avertissements sont mis en liste (avis) au lieu d'être affichés.
    # catch_warnings : capte les avertissements émis dans le bloc with.
    with warnings.catch_warnings(record=True) as avis:
        # "always" : aucun avertissement n'est ignoré, même déjà vu.
        warnings.simplefilter("always")
        try:
            # Tente de charger le modèle sauvegardé avec l'ancienne version.
            m = joblib.load(f"modeles/{nom}.joblib")  # relecture du fichier
            # Si on arrive ici, le chargement a réussi (des avertissements restent possibles).
            etat = "chargé"
        # except : exécuté seulement si le try a échoué ; e contient l'erreur.
        except Exception as e:
            # Le chargement peut échouer : on garde le type d'erreur et son message.
            # f-string : insère le type d'erreur et son message dans le texte.
            etat = f"ERREUR {type(e).__name__} : {e}"
    # Bilan : état du chargement et types d'avertissements (sans doublon, triés).
    # {nom:<13} : nom aligné à gauche sur 13 caractères, pour former des colonnes.
    print(f"{nom:<13} {etat} | avertissements : {sorted({w.category.__name__ for w in avis}) or 'aucun'}")

# %% Cellule 50 — Suivre les expériences avec MLflow
# === CELLULE 50 : Suivi avec MLflow ===
# --- 1. Configurer MLflow ---
import logging  # règle le niveau de messages affichés
import mlflow  # bibliothèque de suivi d'expériences

# Réduit le bruit : seules les erreurs de MLflow sont affichées.
logging.getLogger("mlflow").setLevel(logging.ERROR)
# Où stocker les résultats : une base SQLite locale, sans serveur.
mlflow.set_tracking_uri("sqlite:///mlflow.db")
# Une expérience regroupe les essais d'un même projet ; elle est créée si elle n'existe pas.
mlflow.set_experiment("prevision_conso_energianord")

# --- 2. Définir les essais à comparer ---
# Nom de l'essai -> réglages à modifier ({} = réglages par défaut).
essais = {"défaut": {}, "profondeur 3": {"max_depth": 3}, "vitesse 0,05": {"learning_rate": 0.05}}
# Adresse MLflow de chaque modèle enregistré, pour le recharger plus tard.
adresses = {}

# --- 3. Un essai = un « run » MLflow ---
for nom, params in essais.items():
    # start_run : ouvre un enregistrement ; tout ce qui suit lui est rattaché ; run_name : son nom lisible.
    with mlflow.start_run(run_name=nom):
        # Entraînement avec les réglages de l'essai.
        m = pc.construire_modele(**params).fit(train[pc.COLONNES], train["conso_mw"])
        # Erreurs mesurées sur la période de test.
        r = pc.evaluer(test["conso_mw"], m.predict(test[pc.COLONNES]))
        # log_params : enregistre les réglages (paramètres) ; "défaut" si non modifié.
        mlflow.log_params({"max_depth": params.get("max_depth", "défaut"), "learning_rate": params.get("learning_rate", "défaut")})
        # log_metrics : enregistre les résultats chiffrés (MAE, RMSE, R2).
        mlflow.log_metrics({"mae": r["MAE"], "rmse": r["RMSE"], "r2": r["R2"]})
        # log_model : enregistre le modèle lui-même ; cloudpickle : format de sérialisation choisi.
        info = mlflow.sklearn.log_model(m, name="modele", serialization_format="cloudpickle")
        # model_uri : adresse du modèle, gardée pour le recharger.
        adresses[nom] = info.model_uri

# --- 4. Comparer les essais ---
# search_runs : tableau de tous les essais de l'expérience ; trié du plus petit MAE (meilleur) au plus grand.
runs = mlflow.search_runs(experiment_names=["prevision_conso_energianord"]).sort_values("metrics.mae")
# Colonnes utiles seulement, arrondies, sans numéro de ligne.
print(runs[["tags.mlflow.runName", "params.max_depth", "params.learning_rate", "metrics.mae", "metrics.r2"]].round(4).to_string(index=False))

# %% Cellule 51 — Recharger le meilleur essai
# === CELLULE 51 : Recharger depuis MLflow ===
# --- 1. Choisir le meilleur essai ---
# runs est trié par MAE : la première ligne (iloc[0]) est le meilleur essai ; on lit son nom.
meilleur = runs.iloc[0]["tags.mlflow.runName"]

# --- 2. Recharger son modèle ---
# load_model : relit le pipeline scikit-learn à partir de son adresse (model_uri).
charge = mlflow.sklearn.load_model(adresses[meilleur])
print("Meilleur essai :", meilleur)
# Le type doit être Pipeline : c'est bien le modèle complet qui a été enregistré.
print("Type rechargé  :", type(charge).__name__)

# --- 3. Vérifier que les prévisions sont les mêmes ---
# On compare avec un modèle réentraîné avec les mêmes réglages (essais[meilleur]) : allclose = égalité aux arrondis près.
print("Prévisions identiques à celles de l'essai :", np.allclose(charge.predict(test[pc.COLONNES]),
      pc.construire_modele(**essais[meilleur]).fit(train[pc.COLONNES], train["conso_mw"]).predict(test[pc.COLONNES])))

# %% Cellule 52 — La journalisation automatique : `autolog`
# === CELLULE 52 : Autolog ===
# --- 1. Activer la journalisation automatique et entraîner ---
# mlflow.sklearn : partie de MLflow dédiée à scikit-learn.
# autolog : MLflow enregistre tout seul paramètres et métriques à chaque fit ; log_models=False : sans copie du modèle.
mlflow.sklearn.autolog(log_models=False)
# Un run est ouvert pour recevoir ces enregistrements ; "as run" garde une référence pour le relire.
with mlflow.start_run(run_name="autolog") as run:
    # Aucun log_param ni log_metric ici : le fit suffit.
    pc.construire_modele().fit(train[pc.COLONNES], train["conso_mw"])
# disable=True : coupe l'autolog pour ne pas enregistrer les cellules suivantes.
mlflow.autolog(disable=True)

# --- 2. Relire ce qui a été enregistré ---
# run.info.run_id : identifiant unique du run ouvert plus haut.
# get_run : retrouve le run par son identifiant.
enreg = mlflow.get_run(run.info.run_id)
# len(...) : nombre de paramètres notés sans aucune instruction de notre part.
print(len(enreg.data.params), "paramètres enregistrés automatiquement, dont :")
# Quelques paramètres du modèle, préfixés par le nom de l'étape du pipeline.
# Noms des quatre paramètres à afficher.
cles = ["learning_rate", "max_iter", "max_depth", "random_state"]
print({c: enreg.data.params[f"histgradientboostingregressor__{c}"] for c in cles})
# Métriques calculées automatiquement (sur les données d'entraînement).
print("Métriques :", sorted(enreg.data.metrics))

# %% Étape manuelle — Créer le module `modele_conso.py`
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('modele_conso.py', 'w', encoding='utf-8') as f:
    f.write('"""modele_conso.py — Entraîner, sauvegarder et utiliser le modèle de prévision (Workshop 3)."""\n# --- 1. Importer les bibliothèques ---\nimport argparse  # lit les options tapées en ligne de commande\nimport json  # écrit le fichier de métadonnées\nfrom pathlib import Path  # manipule les chemins de fichiers\n\nimport joblib  # sauvegarde le modèle sur disque\nimport numpy as np  # valeurs manquantes (np.nan)\nimport pandas as pd  # tableaux de données\nimport sklearn  # sert à lire le numéro de version\n\n# Module de la Partie 3 : préparation des données, découpage, pipeline, évaluation.\nimport prevision_conso as pc\n\n\n# Fonction entrainer\n# Entrées : d = tableau préparé ; coupure = date qui sépare entraînement et test (par défaut pc.COUPURE).\n# Sortie : le modèle entraîné et ses erreurs (MAE, RMSE, R2) sur la période de test.\ndef entrainer(d, coupure=pc.COUPURE):\n    """Entraîne le pipeline final ; renvoie le modèle et son erreur sur la période de test."""\n    # Couper le temps en deux : le passé pour apprendre, le futur pour tester.\n    train, test = pc.decouper(d, coupure)\n    # Construire le pipeline et l\'entraîner sur la période d\'entraînement.\n    modele = pc.construire_modele().fit(train[pc.COLONNES], train["conso_mw"])\n    # Mesurer l\'erreur sur le test, période que le modèle n\'a pas vue.\n    # return : les deux résultats sont rendus ensemble (un tuple).\n    return modele, pc.evaluer(test["conso_mw"], modele.predict(test[pc.COLONNES]))\n\n\n# Fonction prevoir_jour\n# Entrées : modele = modèle entraîné ; d = historique préparé ; jour = date à prévoir.\n# Sortie : tableau (site_id, timestamp, prevu_mw), 24 lignes par site.\ndef prevoir_jour(modele, d, jour):\n    """Prévision horaire de chaque site pour la date `jour` (historique jusqu\'à la veille au moins)."""\n    # Une ligne par site avec ses caractéristiques fixes (type, capacité).\n    # drop_duplicates("site_id") garde la première ligne de chaque site.\n    sites = d.drop_duplicates("site_id")[["site_id", "site_type", "capacity_mw"]]\n    # Les 24 heures du jour à prévoir.\n    heures = pd.date_range(jour, periods=24, freq="h")\n    # Toutes les combinaisons site x heure, en tableau à colonnes site_id et timestamp.\n    futur = pd.MultiIndex.from_product([sites["site_id"], heures], names=["site_id", "timestamp"]).to_frame(index=False)\n    # Rattacher type et capacité à chaque ligne.\n    futur = futur.merge(sites, on="site_id")\n    # La consommation du jour à prévoir est inconnue : valeur manquante.\n    # np.nan : valeur manquante, le modèle la remplacera par une prévision.\n    futur["conso_mw"] = np.nan\n    # Historique : mêmes colonnes, la consommation brute devenant conso_mw.\n    base = d[["timestamp", "site_id", "site_type", "capacity_mw", "conso_brute"]].rename(columns={"conso_brute": "conso_mw"})\n    # Empiler historique et jour à prévoir, triés par site puis par heure : les décalages (retards) deviennent calculables.\n    tout = pd.concat([base, futur], ignore_index=True).sort_values(["site_id", "timestamp"], ignore_index=True)\n    # Calculer les variables du modèle (heure, retards, etc.) sur l\'ensemble.\n    tout = pc.ajouter_variables(tout)\n    # Ne garder que les lignes du jour à prévoir.\n    cible = tout[tout["timestamp"].isin(heures)].copy()\n    # Prédire la consommation de chaque site et chaque heure.\n    cible["prevu_mw"] = modele.predict(cible[pc.COLONNES])\n    # Renvoyer seulement les colonnes utiles.\n    # Fin de la fonction : la prévision est rendue à l\'appelant.\n    return cible[["site_id", "timestamp", "prevu_mw"]]\n\n\n# Fonction main\n# Entrée : argv = liste d\'options (None : lit celles de la ligne de commande).\n# Sortie : le tableau de prévisions ; entraîne, sauvegarde et prévoit en une commande.\ndef main(argv=None):\n    # Déclarer les options acceptées.\n    # ArgumentParser : objet qui lit les options ; description : texte affiché par --help.\n    p = argparse.ArgumentParser(description="Entraîner le modèle et prévoir un jour.")\n    # --sortie : fichier où écrire le modèle ; --jour : date à prévoir.\n    p.add_argument("--sortie", default="modeles/modele_conso.joblib")\n    # default : valeur utilisée si l\'option n\'est pas fournie.\n    p.add_argument("--jour", default="2025-01-31")\n    # Lire les options fournies (sinon les valeurs par défaut s\'appliquent).\n    args = p.parse_args(argv)\n\n    # Charger et préparer les données.\n    d = pc.preparer()\n    # Entraîner le modèle et obtenir ses erreurs sur le test.\n    modele, mesures = entrainer(d)\n    # Créer le dossier de destination s\'il manque.\n    Path(args.sortie).parent.mkdir(exist_ok=True)\n    # Sauvegarder le modèle.\n    joblib.dump(modele, args.sortie)\n    # Écrire à côté un fichier .json (même nom) : version de scikit-learn, variables, MAE.\n    Path(args.sortie).with_suffix(".json").write_text(json.dumps(\n        {"scikit_learn": sklearn.__version__, "variables": pc.COLONNES, "mae_test": round(mesures["MAE"], 4)},\n        indent=2), encoding="utf-8")\n    # Prévoir le jour demandé.\n    prevision = prevoir_jour(modele, d, args.jour)\n    # Résumé affiché : fichier écrit, erreur de test, taille et total de la prévision.\n    print(f"Modèle enregistré : {args.sortie} | MAE test {mesures[\'MAE\']:.3f} MW")\n    print(f"Prévision du {args.jour} : {len(prevision)} lignes, total {prevision[\'prevu_mw\'].sum():.1f} MWh")\n    # Rendre la prévision : utile si main est appelée depuis un autre programme.\n    return prevision\n\n\n# __name__ vaut "__main__" seulement quand le fichier est lancé directement.\n# Ce bloc ne s\'exécute que si le fichier est lancé directement (python modele_conso.py),\n# et non quand il est importé par un notebook.\nif __name__ == "__main__":\n    main()\n')
print('modele_conso.py', ':', len(open('modele_conso.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 53 — Lancer le module comme un script
# === CELLULE 53 : Exécution en ligne de commande ===
# --- 1. Lancer le module comme un programme séparé ---
import sys  # sys.executable : chemin de l'interpréteur Python en cours

# Même interpréteur que le noyau (donc venv-ml) ; arguments : le script, puis l'option --sortie.
# capture_output=True et text=True : on récupère ce que le script affiche, sous forme de texte.
r = subprocess.run([sys.executable, "modele_conso.py", "--sortie", "modeles/modele_cli.joblib"], capture_output=True, text=True)
# Sortie du script, ou fin du message d'erreur s'il a échoué.
print(r.stdout.strip() or r.stderr.strip()[-500:])

# --- 2. Importer le module qui vient d'être créé ---
# Python garde en mémoire la liste des fichiers connus : on la vide pour qu'il voie le nouveau fichier.
importlib = __import__("importlib"); importlib.invalidate_caches()
import modele_conso as mc

# --- 3. Prévoir le 31 janvier avec le modèle sauvegardé par le script ---
# load : relit le modèle enregistré ; prevoir_jour : prévision des 24 heures de chaque site.
prevision = mc.prevoir_jour(joblib.load("modeles/modele_cli.joblib"), d, "2025-01-31")
# Tableau lisible : une ligne par site, une colonne par heure (3 h, 9 h, 14 h, 20 h), arrondi à 2 décimales.
print(prevision.assign(heure=prevision["timestamp"].dt.hour).pivot(index="site_id", columns="heure", values="prevu_mw")[[3, 9, 14, 20]].round(2))
