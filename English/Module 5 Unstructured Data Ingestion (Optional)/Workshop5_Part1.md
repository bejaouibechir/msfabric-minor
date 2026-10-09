# Workshop 5 — Part 1: AI Ingestion, Enrichment, and the Silver Layer

### Theme: Audio customer calls — Renewable Energy Sector

---

## Business context

**SolarVoix** is a French renewable energy player (solar panels, heat pumps, VE charging stations). Their customer relationship centre receives **120 calls a week**. Today, these calls are recorded in MP3, archived in a network folder, and **no one analyzes them**. As a result, dissatisfied customers leave without the company knowing, and the rate of churn rises.

**Problematic:** How to automatically detect risk calls (very negative feeling, intention to terminate) to alert the VAS manager in real time?

**Architecture cible (3 parties) :**

```
Fichiers audio (MP3 synthétiques)
        ↓
  Lakehouse Bronze  ← ingestion brute
        ↓
  Notebook PySpark + modèle NLP local (sans clé API)
        ↓
  Lakehouse Silver  ← transcriptions + scores enrichis
        ↓
  Pipeline Data Factory + Activator (Partie 2)
        ↓
  Modèle sémantique + Rapport Power BI Fabric (Partie 3)
```

> * This workshop does not use any paid Azure keys**. The analysis is based on a local NLP model TF-IDF + logistic regression, trained with the workshop's synthetic data and then retained in OneLake.

---

## Prerequisite

| Element          | Value                                                            |
| ---------------- | ----------------------------------------------------------------- |
| Workspace Fabric | `WS_SolarVoix`(F64 or Trial Capacity)                            |
| Lakehouse        | `LH_SolarVoix`                                                    |
| Notebook 1       | `NB_Data_Generation`                                           |
| Notebook 2       | `NB_Bronze_to_Silver`                                             |
| Notebook 3       | `NB_Visualizations`                                               |
| Libraries    | `scikit-learn`, `joblib`, `pydub`, `faker` (installables via %pip) |

---

# PART 1

---

## Bloc 1 — Mise en place de l'environnement

### 1.1 — Creating Workspace

1. Go to **app.fabric.microsoft.com**
2. In the left menu → **Workspaces** → **+ New workspace**
3. Nom : `WS_SolarVoix`
4. Licence Method: **Trial** or **Manufacture capacity**
5. Cliquer **Apply**

> Note the expiry date in your training prerequisites.

### 1.2—Create Lakehouse

1. In`WS_SolarVoix` → **+ New item** → **Lakehouse**
2. Nom : `LH_SolarVoix`
3. Cliquer **Create**
4. Check that the folders **Tables** and **Files** appear in the left explorer

### 1.3 — Create the first Notebook

1. Workspace → **+ New item** → **Notebook**
2. Nommer : `NB_Data_Generation`
3. In the panel **Lakehouses** on the left → **Add** → select`LH_SolarVoix`

---

## Block 2 — Generation of synthetic data

> For this workshop, we generate 120 fictitious but realistic calls (products, complaints, intentions typical of the energy sector). This allows to replay the workshop as many times as desired.

### 2.1 — Cell 1: Installation of libraries

```python
# === CELLULE 1 : Installation des dépendances ===
#
# OBJECTIF : Installer les bibliothèques nécessaires pour générer les données
#            synthétiques et effectuer l'analyse IA sans clé externe.
#
# %pip install s'exécute dans l'environnement du cluster Spark.
# L'installation est temporaire (durée de la session Spark).
# Pour persister, utilisez Environment items dans Fabric.
#
# faker    → génère des noms, villes, dates aléatoires réalistes
# pydub    → manipulation audio (création de fichiers WAV/MP3 vides)
# scikit-learn et joblib seront installés plus tard dans le notebook d'analyse


import subprocess, sys
pkgs = ["faker", "pydub"]
subprocess.run([sys.executable, "-m", "pip", "install", "--quiet"] + pkgs, check=True)
print("Installation terminée")
```

** Expected result:**`Installation terminée`(may take 2-3 minutes at first launch)

### 2.2 — Cell 2: Generation of transcripts and metadata

```python
# === CELLULE 2 : Génération des 120 appels synthétiques ===
#
# OBJECTIF : Créer deux fichiers dans le Lakehouse :
#   1. 120 fichiers .txt dans Files/audio_calls/  (simulent des transcriptions)
#   2. Un fichier calls_metadata.csv (horodatage, durée, client, produit)
#
# Dans un projet réel, les .txt seraient remplacés par des .mp3 et la
# transcription serait effectuée par un modèle Whisper ou Azure Speech.
# La structure des données est identique — seule la source change.
#
# Vocabulaire métier SolarVoix :
#   - PSF  = Panneaux Solaires Fotovoltaïques
#   - PAC  = Pompe À Chaleur
#   - BORNE = Borne de recharge VE

import random
import csv
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("fr_FR")
random.seed(42)  # Graine fixe → résultats reproductibles entre sessions

# -------------------------------------------------------
# DÉFINITION DU CORPUS DE TRANSCRIPTIONS
# -------------------------------------------------------
# Chaque catégorie contient des phrases typiques d'un appel client.
# Les catégories couvrent le spectre complet : très satisfait → très mécontent.

TEMPLATES = {
    "positif": [
        "Bonjour, je voulais juste vous remercier pour l'installation de mes panneaux solaires. "
        "Le technicien était très professionnel et tout fonctionne parfaitement. "
        "Je suis vraiment satisfait du service et je vous recommanderai à mes voisins.",

        "Votre équipe a fait un travail remarquable pour ma pompe à chaleur. "
        "L'installation a été rapide, propre, et les économies sur ma facture sont déjà visibles. "
        "Continuez comme ça, c'est exactement ce qu'on attend.",

        "Je viens de recevoir ma première facture EDF depuis l'installation des panneaux. "
        "J'économise déjà 40 pourcent. Votre solution est excellente, merci à toute l'équipe.",
    ],
    "neutre": [
        "Bonjour, je souhaite avoir des informations sur vos offres de maintenance pour panneaux solaires. "
        "Mon contrat expire dans trois mois et je voudrais connaître les options de renouvellement.",

        "Je vous appelle pour signaler un délai de livraison de ma borne de recharge. "
        "On m'avait annoncé 10 jours, il en est au 14ème. Pouvez-vous me donner une date précise ?",

        "Bonjour, j'aimerais avoir une information sur le remboursement de la TVA "
        "pour mon installation de panneaux solaires. Quels documents dois-je fournir ?",
    ],
    "negatif": [
        "Ça fait deux semaines que j'attends un technicien pour réparer ma pompe à chaleur. "
        "C'est inacceptable, j'ai des enfants à la maison et il fait froid. "
        "Si ça continue, je vais déposer une plainte auprès de la DGCCRF.",

        "Mon application de suivi de production solaire ne fonctionne plus depuis 10 jours. "
        "J'ai appelé trois fois, personne ne rappelle. C'est un manque de respect total envers les clients. "
        "Je suis vraiment déçu de votre service après-vente.",

        "Vos techniciens ont endommagé ma toiture lors de la pose des panneaux. "
        "J'attends toujours une réponse de votre responsable depuis deux semaines. "
        "Cette situation est inadmissible et je vais en parler à mon assurance.",
    ],
    "tres_negatif": [
        "Je vais résilier mon contrat immédiatement. Ça fait trois mois que votre borne de recharge "
        "ne fonctionne pas et vous ne faites rien. J'ai perdu confiance en votre entreprise. "
        "Je vais laisser des avis négatifs partout et déposer une plainte formelle.",

        "C'est la dernière fois que je vous appelle. Vous m'avez vendu une pompe à chaleur "
        "qui tombe en panne chaque mois. Je veux un remboursement complet et je vais saisir "
        "le médiateur de l'énergie si vous ne réglez pas ça dans les 48 heures.",

        "Votre entreprise est une arnaque. Mes panneaux solaires n'ont jamais produit "
        "ce que vous m'aviez promis. Je contacte mon avocat cette semaine "
        "et je résilie tous mes contrats avec vous. Vous allez avoir de mes nouvelles.",
    ],
}

PRODUITS = ["Panneaux solaires PSF", "Pompe à chaleur PAC", "Borne recharge VE", "Batterie stockage"]
INTENTIONS = {
    "positif":     ["satisfaction", "recommandation"],
    "neutre":      ["information", "suivi_commande", "question_facturation"],
    "negatif":     ["plainte_technique", "plainte_sav", "reclamation"],
    "tres_negatif":["resiliation", "menace_juridique", "churn_imminent"],
}

# -------------------------------------------------------
# GÉNÉRATION DES 120 APPELS
# -------------------------------------------------------
# Répartition : 30 positifs, 30 neutres, 35 négatifs, 25 très négatifs
# → Représentation réaliste d'un centre SAV sous tension

REPARTITION = (
    [("positif", 30)] +
    [("neutre", 30)] +
    [("negatif", 35)] +
    [("tres_negatif", 25)]
)

appels = []
call_id = 1
date_debut = datetime(2024, 10, 1)

for sentiment, count in REPARTITION:
    for _ in range(count):
        template = random.choice(TEMPLATES[sentiment])
        intention = random.choice(INTENTIONS[sentiment])
        produit = random.choice(PRODUITS)
        duree_sec = random.randint(60, 480)  # 1 à 8 minutes
        date_appel = date_debut + timedelta(
            days=random.randint(0, 89),      # sur 3 mois
            hours=random.randint(8, 18),
            minutes=random.randint(0, 59)
        )
        # Enrichissement du texte avec le produit mentionné
        texte_complet = f"[Appel entrant - {date_appel.strftime('%d/%m/%Y %H:%M')}] " \
                        f"Client : {fake.name()}. Produit concerné : {produit}. " \
                        f"Transcription : {template}"

        appels.append({
            "call_id": f"CALL_{call_id:04d}",
            "client_nom": fake.name(),
            "client_email": fake.email(),
            "ville": fake.city(),
            "produit": produit,
            "date_appel": date_appel.strftime("%Y-%m-%d %H:%M:%S"),
            "duree_secondes": duree_sec,
            "sentiment_reel": sentiment,       # colonne de vérité terrain (pour évaluation)
            "intention_reelle": intention,
            "texte_transcription": texte_complet,
        })
        call_id += 1

random.shuffle(appels)  # Mélanger pour ne pas avoir les sentiments triés
print(f"Nombre d'appels générés : {len(appels)}")
print(f"Répartition sentiments : { {s: sum(1 for a in appels if a['sentiment_reel']==s) for s in TEMPLATES} }")
```

** Expected result:**

```
Nombre d'appels générés : 120
Répartition sentiments : {'positif': 30, 'neutre': 30, 'negatif': 35, 'tres_negatif': 25}
```

### 2.3 — Cell 3: Lakehouse backup

```python
# === CELLULE 3 : Écriture dans le Lakehouse (couche Bronze) ===
#
# OBJECTIF : Persister les données générées dans deux formats :
#   1. Fichiers .txt individuels dans Files/audio_calls/
#      → Simulant des transcriptions de fichiers audio réels
#      → En production : ce seraient des .mp3 traités par Whisper ou Azure Speech
#   2. Fichier CSV de métadonnées dans Files/metadata/
#      → Contient toutes les colonnes sauf le texte de transcription
#
# mssparkutils.fs.put() écrit directement dans le système de fichiers OneLake
# du Lakehouse attaché au Notebook.
# overwrite=True → idempotent (peut être relancé sans dupliquer les données)

# -------------------------------------------------------
# ÉCRITURE DES FICHIERS .TXT DE TRANSCRIPTION
# -------------------------------------------------------
for appel in appels:
    chemin = f"Files/audio_calls/{appel['call_id']}.txt"
    mssparkutils.fs.put(chemin, appel["texte_transcription"], overwrite=True)

print(f"✅ {len(appels)} fichiers .txt écrits dans Files/audio_calls/")

# -------------------------------------------------------
# ÉCRITURE DU CSV MÉTADONNÉES
# -------------------------------------------------------
# On utilise Python natif (io + csv) pour construire le CSV en mémoire
# puis mssparkutils.fs.put() pour l'écrire dans le Lakehouse en une seule opération.
# Évite de créer un fichier temporaire local (/tmp/...) qui ne persiste pas.

import io, csv as csv_module

buffer = io.StringIO()
champs = ["call_id","client_nom","client_email","ville","produit",
          "date_appel","duree_secondes","sentiment_reel","intention_reelle"]
writer = csv_module.DictWriter(buffer, fieldnames=champs, extrasaction="ignore")
writer.writeheader()
writer.writerows(appels)

mssparkutils.fs.put("Files/metadata/calls_metadata.csv", buffer.getvalue(), overwrite=True)
print("✅ calls_metadata.csv écrit dans Files/metadata/")
```

** Visual verification:**
In the Lakehouse's left explorer → **Files** → you must see two files:`audio_calls/`(120 .txt files) and`metadata/`(1 CSV file).

---

## Bloc 3 — Ingestion Bronze

### 3.1 — Create the Intake Notebook

1. Workspace → **+ New item** → **Notebook**
2. Nommer : `NB_Bronze_to_Silver`
3. Add`LH_SolarVoix`in Lakehouses panel

### 3.2 — Cell 1: Loading Bronze transcripts

```python
# === CELLULE 1 : Ingestion Bronze — Fichiers texte ===
#
# OBJECTIF : Lire tous les fichiers .txt du dossier audio_calls/
#            en une seule opération Spark et créer la table bronze_transcriptions.
#
# spark.read.text() lit chaque fichier comme une ligne par ligne.
# Pour avoir une ligne par FICHIER (= un appel complet), on utilise
# spark.read.format("binaryFile") qui charge le contenu binaire du fichier,
# puis on le décode en UTF-8.
#
# Colonnes créées automatiquement par binaryFile :
#   path    → chemin complet du fichier (ex: abfss://...CALL_0001.txt)
#   content → contenu brut en bytes
#   length  → taille du fichier en bytes

from pyspark.sql import functions as F

# Lecture de tous les fichiers .txt en mode binaryFile
df_raw = (
    spark.read
    .format("binaryFile")
    .option("pathGlobFilter", "*.txt")  # filtre sur l'extension
    .load("Files/audio_calls/")
)

# Décodage UTF-8 + extraction du call_id depuis le nom du fichier
# F.decode(content, "utf-8") convertit les bytes en chaîne lisible
# F.regexp_extract extrait "CALL_0001" depuis le chemin complet du fichier
df_bronze_transcriptions = (
    df_raw
    .withColumn("transcription_text", F.decode(F.col("content"), "utf-8"))
    .withColumn("call_id",
        F.regexp_extract(F.col("path"), r"(CALL_\d+)\.txt", 1))
    .withColumn("file_size_bytes", F.col("length"))
    .select("call_id", "transcription_text", "file_size_bytes")
)

df_bronze_transcriptions.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze_transcriptions")

print(f"bronze_transcriptions : {df_bronze_transcriptions.count()} lignes")
df_bronze_transcriptions.show(3, truncate=80)
```

### 3.3 — Cell 2: Loading Bronze Metadata

```python
# === CELLULE 2 : Ingestion Bronze — Métadonnées CSV ===
#
# OBJECTIF : Lire le fichier calls_metadata.csv et créer bronze_calls_metadata.
#
# inferSchema=True détecte automatiquement :
#   - date_appel → TimestampType (si format reconnu)
#   - duree_secondes → IntegerType
#   - les colonnes texte → StringType
#
# Bonne pratique : en production, définir un StructType explicite
# pour éviter les surprises de typage sur de gros volumes.

df_meta = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("Files/metadata/calls_metadata.csv")
)

df_meta.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("bronze_calls_metadata")

print(f"bronze_calls_metadata : {df_meta.count()} lignes")
df_meta.printSchema()
```

### 3.4 — Cell 3: Bronze quality diagnosis

```python
# === CELLULE 3 : Diagnostic qualité ===
#
# OBJECTIF : Vérifier l'intégrité des données avant de commencer l'enrichissement IA.
#
# Règle d'or : diagnostiquer avant de transformer.
# On vérifie :
#   1. Nulls dans les colonnes critiques
#   2. Cohérence du nombre d'appels (120 attendus)
#   3. Jointure entre les deux tables Bronze (call_id doit matcher)

from pyspark.sql import functions as F

df_t = spark.table("bronze_transcriptions")
df_m = spark.table("bronze_calls_metadata")

print("=== VÉRIFICATION BRONZE ===")
print(f"Transcriptions : {df_t.count()} lignes (attendu: 120)")
print(f"Métadonnées    : {df_m.count()} lignes (attendu: 120)")

# Vérification des nulls sur transcription_text (critique pour l'IA)
nulls_text = df_t.filter(F.col("transcription_text").isNull() |
                          (F.length("transcription_text") < 10)).count()
print(f"\nTranscriptions vides ou trop courtes : {nulls_text}")

# Vérification de la jointure (call_ids qui matchent)
ids_t = set(r.call_id for r in df_t.select("call_id").collect())
ids_m = set(r.call_id for r in df_m.select("call_id").collect())
orphelins = ids_t.symmetric_difference(ids_m)
print(f"call_ids sans correspondance : {len(orphelins)}")
if len(orphelins) > 0:
    print(f"  ⚠️ IDs orphelins : {list(orphelins)[:5]}")
else:
    print("  ✅ Jointure parfaite entre les deux tables")

# Distribution des sentiments réels (vérité terrain)
print("\n=== RÉPARTITION SENTIMENTS (vérité terrain) ===")
df_m.groupBy("sentiment_reel").count().orderBy("count", ascending=False).show()
```

** Interpretation:** 120 lines, no null, perfect joint. The actual distribution (25 very negative + 35 negative = 50% problematic calls) represents a VAS center under high pressure.

---

## Block 4 — Local and reliable AI enrichment

> **Undownloaded external model architecture:** the notebook results in a lightweight NLP classifier with TF-IDF and logistic regression from the already labelled 120 transcripts. It doesn't depend on Hugging Face, PyTorch, or an external token. The model is saved in OneLake for incremental treatment.

> `hf_pipeline`, `MODEL_ID`, `cmarkea/distilcamembert-base-sentiment`or`nlptown/bert-base-multilingual-uncased-sentiment`, you run the old version. Remove this cell and replace it with cells 4A and 4B below, or reimport the notebook`NB_Bronze_to_Silver.ipynb`updated. A modification to the local file does not automatically replace a notebook already imported into the Fabric workspace.

### 4.1 — 4A cell: Install ML engine and restart Python

```python
# === CELLULE 4A : Installation des dépendances ML légères ===
%pip install -q scikit-learn joblib

import notebookutils
notebookutils.session.restartPython()
```

Wait until the restart is over, then run the next cell.

### 4.2 — Cell 4B: Training and saving the sentiment model

```python
# === CELLULE 4B : Modèle local TF-IDF + régression logistique ===

from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = "/lakehouse/default/Files/models/sentiment_tfidf.joblib"

# Jointure des textes et des étiquettes générées dans les tables Bronze.
df_entrainement = (
    spark.table("bronze_transcriptions").alias("t")
    .join(spark.table("bronze_calls_metadata").alias("m"), "call_id")
    .select("call_id", "transcription_text", "sentiment_reel")
)

lignes = df_entrainement.collect()
texts = [r.transcription_text for r in lignes]
call_ids = [r.call_id for r in lignes]

def normaliser_label(label: str) -> str:
    if label in {"tres_negatif", "negatif"}:
        return "negatif"
    if label == "positif":
        return "positif"
    return "neutre"

labels = [normaliser_label(r.sentiment_reel) for r in lignes]

modele_sentiment = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        min_df=1,
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )),
])

modele_sentiment.fit(texts, labels)

# Persistance du modèle dans OneLake pour NB_Incremental_Processing.
Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
joblib.dump(modele_sentiment, MODEL_PATH)
print(f"Modèle ML sauvegardé dans OneLake : {MODEL_PATH}")

predictions = modele_sentiment.predict(texts)
probabilites = modele_sentiment.predict_proba(texts)

resultats = []
for call_id, sentiment_ia, proba in zip(call_ids, predictions, probabilites):
    resultats.append({
        "call_id": call_id,
        "sentiment_ia": sentiment_ia,
        "score_sentiment": round(float(max(proba)), 4),
    })

print(f"\nAnalyse terminée : {len(resultats)} appels traités")
for r in resultats[:5]:
    print(f"  {r['call_id']} → {r['sentiment_ia']} (confiance: {r['score_sentiment']})")
```

### 4.3 — Cell 5: Intent Detection and Churn Risk Score

```python
# === CELLULE 5 : Détection d'intention par règles + calcul du score churn ===
#
# OBJECTIF : Deux enrichissements complémentaires :
#   1. intent_detecte : catégorie d'intention basée sur mots-clés métier
#      (plus rapide et explicable qu'un modèle NLP pour la classification métier)
#   2. score_risque_churn : score de 0 à 100 combinant plusieurs signaux
#
# Logique du score risque churn :
#   - Sentiment IA très négatif  : +50 points
#   - Sentiment IA négatif       : +25 points
#   - Mots de résiliation        : +30 points
#   - Mots de menace (avocat, DGCCRF) : +20 points
#   - Durée > 5 minutes (frustration prolongée) : +10 points
#   - Score plafonné à 100
#
# Cette formule est délibérément simple et explicable.
# En production, on l'enrichirait avec l'historique CRM du client.

import re

# Dictionnaire des mots-clés par intention métier
KEYWORDS_INTENT = {
    "resiliation":         ["résilie", "résiliation", "annuler", "annule", "partir", "quitter"],
    "menace_juridique":    ["avocat", "plainte", "dgccrf", "médiateur", "tribunal", "juridique"],
    "churn_imminent":      ["jamais", "arnaque", "honte", "incompétent", "remboursement total"],
    "plainte_technique":   ["panne", "ne fonctionne pas", "cassé", "défaillant", "réparer"],
    "plainte_sav":         ["rappelle pas", "personne ne", "inacceptable", "scandaleux"],
    "question_facturation":["facture", "tva", "remboursement", "devis", "tarif", "prix"],
    "suivi_commande":      ["livraison", "délai", "date", "quand", "attends"],
    "satisfaction":        ["merci", "excellent", "parfait", "satisfait", "recommande"],
    "information":         ["information", "renseignement", "savoir", "comprendre"],
}

def detecter_intention(texte: str) -> str:
    """Retourne la première intention trouvée par ordre de priorité."""
    texte_lower = texte.lower()
    # Ordre de priorité : les intentions critiques d'abord
    priorite = ["resiliation", "menace_juridique", "churn_imminent",
                "plainte_technique", "plainte_sav", "question_facturation",
                "suivi_commande", "satisfaction", "information"]
    for intent in priorite:
        for kw in KEYWORDS_INTENT[intent]:
            if kw in texte_lower:
                return intent
    return "autre"

def calculer_score_churn(sentiment: str, texte: str, duree_sec: int) -> int:
    """
    Calcule un score de risque churn entre 0 et 100.
    Plus le score est élevé, plus le risque que le client parte est important.
    """
    score = 0
    texte_lower = texte.lower()

    # Signal 1 : Sentiment IA (base élevée — le sentiment est le signal le plus fort)
    if sentiment == "negatif":
        score += 40

    # Signal 2 : Mots de résiliation explicites
    mots_resil = ["résilie", "résiliation", "annuler", "quitter", "partir", "dernier"]
    if any(m in texte_lower for m in mots_resil):
        score += 30

    # Signal 3 : Menaces juridiques ou institutionnelles
    mots_menace = ["avocat", "plainte", "dgccrf", "médiateur", "tribunal", "assurance"]
    if any(m in texte_lower for m in mots_menace):
        score += 20

    # Signal 4 : Plainte technique ou SAV explicite
    mots_plainte = ["panne", "ne fonctionne pas", "inacceptable", "scandaleux",
                    "inadmissible", "trois fois", "cinq fois", "rappelle pas"]
    if any(m in texte_lower for m in mots_plainte):
        score += 15

    # Signal 5 : Durée prolongée (>5 min = client insistant = problème sérieux)
    if duree_sec > 300:
        score += 10

    # Plafonnement à 100
    return min(score, 100)

# -------------------------------------------------------
# APPLICATION SUR LES 120 APPELS
# -------------------------------------------------------
# On joint les résultats de sentiment avec les métadonnées (durée)
df_meta_pd = spark.table("bronze_calls_metadata").toPandas()
df_meta_dict = {r["call_id"]: r for _, r in df_meta_pd.iterrows()}

for r in resultats:
    texte = next(t for c, t in zip(call_ids, texts) if c == r["call_id"])
    meta = df_meta_dict.get(r["call_id"], {})
    duree = meta.get("duree_secondes", 0)

    r["intent_detecte"] = detecter_intention(texte)
    r["score_risque_churn"] = calculer_score_churn(r["sentiment_ia"], texte, duree)
    r["alerte_critique"] = r["score_risque_churn"] >= 50  # booléen pour Activator (Partie 2)

# Statistiques rapides
scores = [r["score_risque_churn"] for r in resultats]
alertes = sum(r["alerte_critique"] for r in resultats)
print(f"Score churn moyen : {sum(scores)/len(scores):.1f}/100")
print(f"Score churn max   : {max(scores)}/100")
print(f"Appels en alerte critique (score ≥ 50) : {alertes}")
```

** Job interpretation:** Average score of 31.8/100, 20 critical alerts ( ≥ 50) on 120 calls or 16.7%. The maximum score of 85 corresponds to calls combining negative feeling + termination words + legal threat — these are the cases to be treated as a top priority within 24 hours. Each alert represents a risk of loss estimated at €2,000–8000 of recurring contracts (maintenance, renewal, extension).

> **Model Note IA:** The local classifier directly produces three classes:`negatif`, `neutre`and`positif`. It is suitable for the demonstration and synthetic vocabulary of SolarVoix; The Churn score of Cell 5 adds business rules.

---

## Block 5 — Creating the Silver Layer

### 5.1 — Cell 6: Junction and Silver Writing

```python
# === CELLULE 6 : Construction de la table Silver ===
#
# OBJECTIF : Créer silver_appels_enrichis en joignant :
#   - bronze_calls_metadata  (informations client, produit, date)
#   - Les résultats d'enrichissement IA (sentiment, intent, churn)
#
# La couche Silver = données propres + enrichies, prêtes pour le rapport.
# On écrit en Delta → partitionnement par sentiment_ia pour accélérer
# les requêtes filtrées dans Power BI.
#
# Colonnes finales de la table Silver :
#   call_id, client_nom, client_email, ville, produit
#   date_appel, duree_secondes, duree_minutes (calculée)
#   sentiment_ia, score_sentiment
#   intent_detecte, score_risque_churn, alerte_critique
#   (sentiment_reel, intention_reelle → colonnes de vérité terrain pour audit)

from pyspark.sql import Row
import pyspark.sql.functions as F

# Conversion de la liste Python → DataFrame Spark
df_enrichi = spark.createDataFrame([Row(**r) for r in resultats])

# Jointure avec les métadonnées Bronze
df_meta_spark = spark.table("bronze_calls_metadata")

df_silver = (
    df_meta_spark
    .join(df_enrichi, on="call_id", how="inner")

    # Calcul de la durée en minutes (arrondi 1 décimale) pour lisibilité métier
    .withColumn("duree_minutes",
        F.round(F.col("duree_secondes") / 60.0, 1))

    # Conversion de la date en type Timestamp pour Power BI
    .withColumn("date_appel", F.to_timestamp("date_appel"))

    # Extraction jour de la semaine (1=Lundi ... 7=Dimanche) pour analyses
    .withColumn("jour_semaine", F.dayofweek("date_appel"))

    # Extraction heure pour analyser les pics d'appels
    .withColumn("heure_appel", F.hour("date_appel"))

    # Tranche horaire métier (matin / après-midi / fin de journée)
    .withColumn("tranche_horaire",
        F.when(F.col("heure_appel") < 12, "Matin")
        .when(F.col("heure_appel") < 17, "Après-midi")
        .otherwise("Fin de journée"))

    # Sélection et ordre des colonnes finales
    .select(
        "call_id", "client_nom", "client_email", "ville", "produit",
        "date_appel", "duree_secondes", "duree_minutes",
        "tranche_horaire", "jour_semaine",
        "sentiment_ia", "score_sentiment",
        "intent_detecte", "score_risque_churn", "alerte_critique",
        "sentiment_reel", "intention_reelle"  # colonnes audit
    )
)

# Écriture Silver partitionnée par sentiment_ia
# Avantage : Power BI en mode Direct Lake lit uniquement les partitions filtrées
df_silver.write \
    .mode("overwrite") \
    .format("delta") \
    .partitionBy("sentiment_ia") \
    .saveAsTable("silver_appels_enrichis")

print(f"silver_appels_enrichis : {df_silver.count()} lignes")
print("\nDistribution sentiment IA :")
df_silver.groupBy("sentiment_ia").count().orderBy("count", ascending=False).show()
```

### 5.2 — Cell 7: Silver Quality Control

```python
# === CELLULE 7 : Contrôle qualité Silver ===
#
# OBJECTIF : Valider la qualité de la table Silver avant de passer à la visualisation.
# On vérifie les distributions, les scores extrêmes, et la cohérence métier.

df_s = spark.table("silver_appels_enrichis")

print("=== CONTRÔLE QUALITÉ SILVER ===\n")

# 1. Nulls sur les colonnes critiques
cols_critiques = ["sentiment_ia", "intent_detecte", "score_risque_churn"]
for col in cols_critiques:
    nulls = df_s.filter(F.col(col).isNull()).count()
    statut = "✅" if nulls == 0 else "⚠️"
    print(f"{statut} {col} : {nulls} nulls")

# 2. Distribution des scores churn
print("\n--- Distribution score_risque_churn ---")
df_s.select(
    F.min("score_risque_churn").alias("min"),
    F.max("score_risque_churn").alias("max"),
    F.avg("score_risque_churn").alias("moyenne"),
    F.percentile_approx("score_risque_churn", 0.75).alias("p75"),
    F.percentile_approx("score_risque_churn", 0.90).alias("p90"),
).show()

# 3. Appels en alerte critique par produit
print("--- Alertes critiques par produit ---")
df_s.filter(F.col("alerte_critique") == True) \
    .groupBy("produit") \
    .count() \
    .orderBy("count", ascending=False) \
    .show()

# 4. Cohérence : sentiment IA vs sentiment réel (matrice de confusion simplifiée)
print("--- Cohérence IA vs vérité terrain ---")
df_s.groupBy("sentiment_reel", "sentiment_ia").count() \
    .orderBy("sentiment_reel", "sentiment_ia") \
    .show()
```

** Interpretation:** The matrix here measures the fit of the model on the synthetic game used for training. A high score is expected, but it is not an independent evaluation. The column`score_risque_churn`completes the classification with explicit business rules.

---

## Bloc 6 — Visualisations analytiques

### 6.1 — Creating the Visualisation Notebook

1. Workspace → **+ New item** → **Notebook**
2. Nommer : `NB_Visualizations`
3. Add`LH_SolarVoix`

### 6.2 — Cell 1: Imports and loading

```python
# === CELLULE 1 : Chargement des données pour visualisation ===
#
# On convertit la table Silver en Pandas DataFrame pour seaborn/matplotlib.
# Acceptable ici : 120 lignes. Au-delà de 100K lignes, utiliser des agrégats Spark.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Style cohérent pour toutes les figures
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
COULEURS_SENTIMENT = {
    "positif": "#27AE60",
    "neutre":  "#F39C12",
    "negatif": "#E74C3C",
}

df = spark.table("silver_appels_enrichis").toPandas()
df["date_appel"] = pd.to_datetime(df["date_appel"])

# Convertir les entiers/booléens nullable Pandas (Int32, Int64, boolean...) en float numpy
# → compatibilité matplotlib/seaborn (ufunc isfinite)
# On exclut les StringDtype pour ne pas écraser les colonnes texte
for col in df.columns:
    if pd.api.types.is_extension_array_dtype(df[col]) and pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].astype(float)

df["semaine"] = df["date_appel"].dt.isocalendar().week.astype(float)

print(f"Données chargées : {len(df)} appels")
```

### 6.3 — Cell 2: Scoreboard sentiment + churn

```python
# === CELLULE 2 : Dashboard 4 visualisations ===
#
# VIZ 1 : Distribution des sentiments (donut chart)
# VIZ 2 : Score churn par produit (boxplot)
# VIZ 3 : Évolution temporelle des alertes (lineplot hebdomadaire)
# VIZ 4 : Heatmap heure × intention (qui appelle quand et pourquoi)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("SolarVoix — Analyse des 120 appels clients", fontsize=16, fontweight="bold", y=1.01)

# -------------------------------------------------------
# VIZ 1 : Donut — Répartition des sentiments IA
# -------------------------------------------------------
ax1 = axes[0, 0]
counts_sent = df["sentiment_ia"].value_counts()
couleurs = [COULEURS_SENTIMENT.get(s, "#95A5A6") for s in counts_sent.index]
wedges, texts, autotexts = ax1.pie(
    counts_sent.values, labels=counts_sent.index,
    autopct="%1.0f%%", colors=couleurs,
    wedgeprops={"width": 0.5},   # width < 1 → donut
    startangle=90
)
for at in autotexts:
    at.set_fontsize(11)
ax1.set_title("Répartition des sentiments (IA)", fontweight="bold")

# -------------------------------------------------------
# VIZ 2 : Boxplot — Score churn par produit
# -------------------------------------------------------
ax2 = axes[0, 1]
ordre_produits = df.groupby("produit")["score_risque_churn"].median() \
                   .sort_values(ascending=False).index
sns.boxplot(data=df, x="produit", y="score_risque_churn",
            order=ordre_produits, ax=ax2,
            palette="Reds", linewidth=1.5)
ax2.axhline(50, color="red", linestyle="--", linewidth=1, label="Seuil alerte (50)")
ax2.set_title("Score de risque churn par produit", fontweight="bold")
ax2.set_xlabel("")
ax2.set_ylabel("Score churn (0-100)")
ax2.tick_params(axis="x", rotation=20)
ax2.legend(fontsize=9)

# -------------------------------------------------------
# VIZ 3 : Lineplot — Alertes critiques par semaine
# -------------------------------------------------------
ax3 = axes[1, 0]
alertes_semaine = (
    df[df["alerte_critique"]]
    .groupby("semaine")
    .size()
    .reset_index(name="nb_alertes")
)
sns.lineplot(data=alertes_semaine, x="semaine", y="nb_alertes",
             ax=ax3, marker="o", color="#E74C3C", linewidth=2)
ax3.fill_between(alertes_semaine["semaine"], alertes_semaine["nb_alertes"],
                  alpha=0.15, color="#E74C3C")
ax3.set_title("Alertes critiques par semaine (score ≥ 50)", fontweight="bold")
ax3.set_xlabel("Semaine de l'année")
ax3.set_ylabel("Nombre d'alertes")
ax3.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

# -------------------------------------------------------
# VIZ 4 : Heatmap — Intentions par tranche horaire
# -------------------------------------------------------
ax4 = axes[1, 1]
pivot = (
    df.groupby(["tranche_horaire", "intent_detecte"])
    .size()
    .unstack(fill_value=0)
)
# Garder les 6 intentions les plus fréquentes pour lisibilité
top6_intents = df["intent_detecte"].value_counts().head(6).index
pivot = pivot[[c for c in top6_intents if c in pivot.columns]]

sns.heatmap(pivot, annot=True, fmt="d", cmap="YlOrRd",
            linewidths=0.5, ax=ax4, cbar_kws={"label": "Nb appels"})
ax4.set_title("Intentions par tranche horaire", fontweight="bold")
ax4.set_xlabel("")
ax4.set_ylabel("")
ax4.tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("/tmp/dashboard_solarvoix.png", dpi=150, bbox_inches="tight")
plt.show()
print("Dashboard sauvegardé")
```

** Interpretation of visualizations:**

**Donut — Distribution of sentiments**

- Compare predicted distribution to baseline feelings generated at the beginning of the workshop
- A difference between the two distributions is normal: the model works on the text and not on the reference wording
- Use churn score and business keywords to complete model classification

**Boxplot — Score churn par produit**

- **Storage battery**: highest median (~35) and 85 outside — recent technology, less mature VAS
- **All products** remain below threshold 50 in median → alerts come from **extreme values** (whiskers), not from average
- **Borne recharge VE**: the most widespread distribution — very heterogeneous customer profiles (technology novices vs early adopters)

**Lineplot — Alertes critiques par semaine**

- **Pic Weeks 40 and 44**: corresponds to the first temperature decreases — CAP and heat demand, rising incidents
- **Maximum 3 alerts/week** on this volume of 120 calls — in real production (500+ calls/sem), the curve will be much more critical
- **Slow Week 49**: may reflect a period of less activity (free) or random generator bias

**Heatmap — Intentions par tranche horaire**

- **`plainte_technique`Afternoon (24)**: customers see the breakdowns when returning home — predictable and actionable peak (strengthen VAS from 2pm to 6pm)
- **`menace_juridique`concentrated afternoon (13)**: frustrated customers climb at the end of the day — critical intervention window before 5pm
- ** Morning dominated by`plainte_technique`**: problems detected the night before, call made from the opening of the centre

### 6.4 — Cell 3: Visualization of the IA performance matrix

```python
# === CELLULE 3 : Évaluation de la qualité du modèle IA ===
#
# OBJECTIF : Visualiser la matrice de confusion (sentiment IA vs réel)
#            pour mesurer la fiabilité du modèle sur nos données métier.

from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Filtrer les lignes avec des valeurs manquantes dans les colonnes sentiment
df_cm = df.dropna(subset=["sentiment_reel", "sentiment_ia"]).copy()

# On mappe "tres_negatif" → "negatif" pour la comparaison
# (le modèle local utilise 3 classes)
df_cm["sentiment_reel_3classes"] = df_cm["sentiment_reel"].astype(str).replace(
    {"tres_negatif": "negatif"}
)

labels = ["positif", "neutre", "negatif"]
y_true = df_cm["sentiment_reel_3classes"]
y_pred = df_cm["sentiment_ia"].astype(str)

cm = confusion_matrix(y_true, y_pred, labels=labels)
print(f"Lignes utilisées pour la matrice : {len(df_cm)} / {len(df)}")

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=labels, yticklabels=labels,
            linewidths=0.5, ax=ax)
ax.set_xlabel("Prédiction IA", fontsize=12)
ax.set_ylabel("Vérité terrain", fontsize=12)
ax.set_title("Matrice de confusion — Modèle de sentiment", fontweight="bold")
plt.tight_layout()
plt.show()

print("\n=== RAPPORT DE CLASSIFICATION ===")
print(classification_report(y_true, y_pred, labels=labels))
```

** Interpretation:** An overall accuracy of 70-80% is expected with this generalistic model. False negatives (neutral negative calls) are more problematic for the job than false positives — a missed churn costs more than a false alarm.

---

## Block 7 — Silver Table Optimization (optional but recommended)

> **Notebook concerned:`NB_Bronze_to_Silver`** — This cell does not execute **not** in`NB_Visualizations`. Return to the notebook`NB_Bronze_to_Silver`and add this cell to it following cells 1 to 7 already created. The numbering "Cellule 8" is the direct continuation of this notebook.

### 7.1 — Cell 8: OPTIMIZE and VACUUM *(in Notebook NB Bronze to Silver) *

Go to Notebook **NB Bronze to Silver** and add Cell 8

Here is the reasoning:

The numbering of cells in the workshop follows the notebook`NB_Bronze_to_Silver`, pas `NB_Visualizations` :

| Notebook            | Cellule     | Bloc                          |
| ------------------- | ----------- | ----------------------------- |
| NB_Bronze_to_Silver | 1, 2, 3     | Bloc 3 (ingestion Bronze)     |
| NB_Bronze_to_Silver | 4           | Bloc 4 (sentiment IA)         |
| NB_Bronze_to_Silver | 5, 6, 7     | Bloc 5 (intent + Silver + QC) |
| NB_Visualizations   | **1, 2, 3** | Bloc 6 (visualisations)       |
| NB_Bronze_to_Silver | **8**       | Bloc 7 (OPTIMIZE/VACUUM)      |

**Cell 8** logically belongs to`NB_Bronze_to_Silver`(continuation of cells 1→7),`NB_Visualizations`. OPTIMIZE/VACUUM applies to the Silver table we just wrote — it would be inconsistent to put it in the visualization notebook.

**Conclusion:** Block 7 should have had a title indicating`NB_Bronze_to_Silver`(like Block 3). Numbering goes back to 1 for`NB_Visualizations`(Bloc 6), then resume at 8 to continue`NB_Bronze_to_Silver`— it is just a lack of clarity in the drafting.

```python
# === CELLULE 8 : Optimisation Delta ===
#
# OBJECTIF : Optimiser la table Silver pour les lectures Power BI Direct Lake.
#
# OPTIMIZE : compacte les petits fichiers Parquet en fichiers de ~128-256 MB
#   → réduit le nombre de fichiers à lire pour Power BI
#   → améliore les temps de requête
#
# VACUUM (7 jours) : supprime les anciens fichiers Delta non référencés
#   → libère l'espace de stockage OneLake
#   ⚠️ Ne pas descendre sous 7 jours si vous avez du Time Travel actif

spark.sql("OPTIMIZE silver_appels_enrichis")
print("OPTIMIZE terminé")

spark.sql("VACUUM silver_appels_enrichis RETAIN 168 HOURS")
print("VACUUM terminé")

# Statistiques de la table après optimisation
spark.sql("DESCRIBE DETAIL silver_appels_enrichis") \
    .select("numFiles", "sizeInBytes", "partitionColumns") \
    .show(truncate=False)
```

---

## Summary of Part 1

| Step               | Outil                    | Result                          |
| ------------------- | ------------------------ | --------------------------------- |
| Data generation  | Python / Faker           | 120 realistic synthetic calls |
| Ingestion Bronze    | Spark binaryFile + CSV   | 2 tables Delta Bronze             |
| Analyse sentiment   | TF-IDF + logistic regression | sentiment_ia + score_sentiment |
| Intention detection | Rules                   |                                   |
