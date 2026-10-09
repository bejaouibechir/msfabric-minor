# Workshop 5 — Part 2: Automated Pipeline and Critical Call Alerts

#### Theme : Orchestration Data Factory + Activator (Real-Time Intelligence)

---

## Background and context

Part 1 created the table`silver_appels_enrichis`with 120 manually scanned calls.

Problem: **this processing must start automatically** with each new incoming audio file. An operator cannot manually restart the Notebook every day.

**Part 2:** Build a Pipeline Data Factory that:

1. Starts when a new file arrives in the folder`audio_calls/`
2. Process file (update of Silver table)
3. Save an alert to the table`alertes_critiques`if the churn score ≥ 50 (visible in Fabric Monitor and Power BI)

**Architecture of this part — 100% native Fabric**

```
Nouveau fichier .txt dans Files/audio_calls/
        ↓
  Pipeline Data Factory (déclencheur événementiel OneLake FileCreated)
     ├─ Activité 1 : Notebook paramétré (enrichissement + MERGE Silver)
     ├─ Activité 2 : If Condition (score_risque_churn ≥ 50 ?)
     │       ├─ OUI → Set Variable "ALERTE" (visible Monitor) + écriture table alertes_critiques
     │       └─ NON → Set Variable "OK" (visible Monitor)
        ↓
  Table Delta alertes_critiques (consultable SQL + Power BI Partie 3)
```

> **Note** All alerts are drawn in a Delta table`alertes_critiques`Lakehouse. This approach is free, persistent, SQL-requestable, and directly usable in Part 3's Power BI report — without any external subscription.

---

# PART 2

---

## Block 1 — Set Notebook (processing a single file)

> Part 1 processed the 120 files in batch. Here we process **one file at a time** dynamically, via a parameter passed by the Pipeline.

### 1.1 — Create the parameter Notebook

1. Workspace → **+ New item** → **Notebook**
2. Nommer : `NB_Incremental_Processing`
3. Add`LH_SolarVoix`

> `sentiment_tfidf.joblib`From OneLake. If it does not exist yet, it automatically drives it from the tables`bronze_transcriptions`and`bronze_calls_metadata`. No Hugging Face or PyTorch download required.

### 1.2 — Installation of dependencies

Add this cell only once at the beginning of the Notebook. It installs the necessary light ML libraries and then restarts the Python interpreter.

```python
# === CELLULE 0 : Installation des dépendances ===

import subprocess
import sys

packages = ["scikit-learn", "joblib"]
subprocess.run(
    [sys.executable, "-m", "pip", "install", "--quiet", *packages],
    check=True,
)

print("✅ Packages installés avec succès")

# Le redémarrage rend les packages nouvellement installés disponibles.
# Aucun autre code ne doit être placé après cette instruction dans la cellule.
import notebookutils
notebookutils.session.restartPython()
```

> This notebook no longer uses`transformers`, PyTorch or Hugging Face. The lightweight model is loaded directly from OneLake.

### 1.3 — Cell 1: Parameter declaration

```python
# === CELLULE 1 : Paramètre d'entrée ===
#
# IMPORTANT : cette cellule doit rester marquée comme "Parameters".
# Fabric insère la valeur transmise par le Pipeline juste après
# l'exécution de cette cellule.

call_file_path = "AUTO"
```

To mark the cell, open its menu`...`, select **Toggle parameter cell**, then check that the **Parameters** banner appears at the bottom right.

> The cell marked **Parameters** must only declare the parameter. Do not place automatic detection in this cell: Fabric injects the value of the Pipeline after its execution.

### 1.3 bis — Normal cell: file resolution to be processed

Insert immediately after cell`Parameters`a normal code cell, not marked **Parameters**:

```python
# === CELLULE 1 BIS : Résolution du fichier à traiter ===

from notebookutils import mssparkutils

if call_file_path == "AUTO":
    try:
        fichiers_dossier = mssparkutils.fs.ls("Files/audio_calls/")

        ids_dossier = {
            fichier.name.removesuffix(".txt")
            for fichier in fichiers_dossier
            if fichier.name.endswith(".txt")
        }

        df_silver = spark.table("silver_appels_enrichis")
        ids_silver = {
            ligne.call_id
            for ligne in df_silver.select("call_id").collect()
        }

        nouveaux_ids = ids_dossier - ids_silver

        print(f"📊 Fichiers présents dans audio_calls : {len(ids_dossier)}")
        print(f"📊 Appels déjà traités dans Silver    : {len(ids_silver)}")
        print(f"📊 Nouveaux appels à traiter          : {len(nouveaux_ids)}")

        if not nouveaux_ids:
            raise RuntimeError(
                "Aucun nouveau fichier n'est disponible dans Files/audio_calls/."
            )

        call_id_temp = sorted(nouveaux_ids)[0]
        call_file_path = f"Files/audio_calls/{call_id_temp}.txt"

        print(
            "🚀 Nouveau fichier détecté automatiquement "
            f"→ {call_file_path}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Échec de la détection automatique : {e}"
        ) from e

else:
    print(
        "🧪 Chemin explicite reçu du Pipeline : "
        f"{call_file_path}"
    )

print(f"Paramètre final utilisé : call_file_path = {call_file_path}")
```

### 1.4 — Cell 2: Extract call id from the path

```python
# === CELLULE 2 : Extraction du call_id ===
#
# OBJECTIF : Dériver le call_id depuis le chemin de fichier reçu en paramètre.
#
# Exemple : "Files/audio_calls/CALL_0121.txt"
#           → call_id = "CALL_0121"
#
# On utilise os.path.basename pour extraire le nom du fichier,
# puis str.replace pour supprimer l'extension.
# Robuste même si le chemin contient des sous-dossiers supplémentaires.

import os
import re

nom_fichier = os.path.basename(call_file_path)   # "CALL_0121.txt"
call_id = nom_fichier.replace(".txt", "")         # "CALL_0121"

# Validation : le call_id doit correspondre au pattern CALL_XXXX
if not re.match(r"^CALL_\d{4}$", call_id):
    raise ValueError(f"Format call_id invalide : '{call_id}'. Attendu: CALL_XXXX")

print(f"call_id extrait : {call_id}")
```

### 1.5 — Cell 3: Reading and enrichment of the file

```python
# === CELLULE 3 : Traitement d'un seul appel (Version corrigée) ===

from pathlib import Path
import joblib
import pyspark.sql.functions as F

# ====================== VARIABLES PAR DÉFAUT ======================
# Sécurité : valeurs par défaut si la cellule est exécutée isolément
try:
    call_file_path
except NameError:
    call_file_path = "Files/audio_calls/CALL_0001.txt"

try:
    call_id
except NameError:
    # On extrait le nom du fichier comme call_id (ex: CALL_0001)
    call_id = call_file_path.split("/")[-1].replace(".txt", "")

# ====================== LECTURE DU FICHIER ======================
try:
    # mssparkutils.fs.head retourne déjà un str (UTF-8)
    transcription_text = mssparkutils.fs.head(call_file_path, 10000).strip()

    if not transcription_text:
        raise ValueError("Le fichier est vide ou ne contient que des espaces.")

    print(f"Fichier lu avec succès : {len(transcription_text)} caractères")
    print(f"Call ID : {call_id} | Chemin : {call_file_path}")

except Exception as e:
    raise FileNotFoundError(f"Impossible de lire le fichier {call_file_path} : {e}") from e

# ====================== CHARGEMENT / CRÉATION DU MODÈLE ======================
MODEL_PATH = "/lakehouse/default/Files/models/sentiment_tfidf.joblib"

if not Path(MODEL_PATH).exists():
    print("Modèle absent : entraînement local automatique depuis les tables Bronze...")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    tables_requises = {"bronze_transcriptions", "bronze_calls_metadata"}
    tables_absentes = [t for t in tables_requises if not spark.catalog.tableExists(t)]
    if tables_absentes:
        raise RuntimeError(
            "Impossible de créer le modèle : tables Bronze absentes : "
            + ", ".join(sorted(tables_absentes))
        )

    df_entrainement = (
        spark.table("bronze_transcriptions").alias("t")
        .join(spark.table("bronze_calls_metadata").alias("m"), "call_id")
        .select("transcription_text", "sentiment_reel")
        .dropna()
    )
    lignes_entrainement = df_entrainement.collect()
    if not lignes_entrainement:
        raise RuntimeError("Impossible de créer le modèle : aucune donnée Bronze étiquetée.")

    def normaliser_label(label: str) -> str:
        if label in {"tres_negatif", "negatif"}:
            return "negatif"
        if label == "positif":
            return "positif"
        return "neutre"

    textes_entrainement = [r.transcription_text for r in lignes_entrainement]
    labels_entrainement = [normaliser_label(r.sentiment_reel) for r in lignes_entrainement]
    if len(set(labels_entrainement)) < 2:
        raise RuntimeError("Impossible de créer le modèle : au moins deux classes sont nécessaires.")

    modele_sentiment = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True, strip_accents="unicode", ngram_range=(1, 2), min_df=1
        )),
        ("classifier", LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=42
        )),
    ])
    modele_sentiment.fit(textes_entrainement, labels_entrainement)
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modele_sentiment, MODEL_PATH)
    print(f"Modèle local entraîné et sauvegardé : {MODEL_PATH}")
else:
    print(f"Chargement du modèle local depuis OneLake : {MODEL_PATH}")
    modele_sentiment = joblib.load(MODEL_PATH)

# ====================== FONCTION PRINCIPALE ======================
def enrichir_appel(call_id: str, texte: str, duree_sec: int = 180) -> dict:
    """
    Applique l'analyse IA et calcule le score churn pour un appel unique.
    Retourne un dictionnaire prêt pour la table silver_appels_enrichis.
    """
    # Sentiment IA
    # Conversion explicite de numpy.str_ vers str Python pour Spark.
    sentiment_ia = str(modele_sentiment.predict([texte])[0])
    probabilites = modele_sentiment.predict_proba([texte])[0]
    score_sentiment = round(float(max(probabilites)), 4)

    # Détection d'intention (mots-clés)
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

    texte_lower = texte.lower()
    intent_detecte = "autre"
    priorite = ["resiliation", "menace_juridique", "churn_imminent",
                "plainte_technique", "plainte_sav", "question_facturation",
                "suivi_commande", "satisfaction", "information"]
    for intent in priorite:
        if any(kw in texte_lower for kw in KEYWORDS_INTENT[intent]):
            intent_detecte = intent
            break

    # Même formule que dans la Partie 1 afin qu'un même appel conserve le même score.
    score = 0
    if sentiment_ia == "negatif":
        score += 40

    mots_resil = ["résilie", "résiliation", "annuler", "quitter", "partir", "dernier"]
    if any(m in texte_lower for m in mots_resil):
        score += 30

    mots_menace = ["avocat", "plainte", "dgccrf", "médiateur", "tribunal", "assurance"]
    if any(m in texte_lower for m in mots_menace):
        score += 20

    mots_plainte = ["panne", "ne fonctionne pas", "inacceptable", "scandaleux",
                    "inadmissible", "trois fois", "cinq fois", "rappelle pas"]
    if any(m in texte_lower for m in mots_plainte):
        score += 15

    if duree_sec > 300:
        score += 10

    score_risque_churn = min(score, 100)

    return {
        "call_id":            call_id,
        "sentiment_ia":       sentiment_ia,
        "score_sentiment":    score_sentiment,
        "intent_detecte":     intent_detecte,
        "score_risque_churn": score_risque_churn,
        "alerte_critique":    score_risque_churn >= 50,
        "duree_sec":          duree_sec,           # utile de le garder
    }


# ====================== EXÉCUTION ======================
resultat = enrichir_appel(call_id, transcription_text, duree_sec=180)

print(f"\n✅ Résultat de l'enrichissement de l'appel :")
for k, v in resultat.items():
    print(f"   {k:20} : {v}")
```

### 1.6 — Cell 4: UPSERT Silver Table Update

```python
# === CELLULE 4 : UPSERT dans la table Silver (Delta MERGE) ===
#
# OBJECTIF : Mettre à jour la table silver_appels_enrichis pour le call_id traité.
#            Si le call_id existe déjà → UPDATE (ré-analyse).
#            Si le call_id est nouveau → INSERT.
#
# MERGE INTO est la commande Delta pour les UPSERTS.
# Plus efficace que DELETE + INSERT car Delta ne réécrit que les fichiers concernés.
#
# Note : mssparkutils.notebook.exit() retourne un JSON au Pipeline Data Factory.
# Ce JSON contient le score churn ET le chemin du fichier réellement traité.
# Le Pipeline utilise json(...).score pour la condition d'alerte
# et json(...).fichier pour identifier le fichier dans les logs Monitor.

from datetime import datetime
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, BooleanType, TimestampType,
)

# Schéma explicite : évite l'inférence de types lors d'un appel Pipeline.
schema_nouveau = StructType([
    StructField("call_id", StringType(), False),
    StructField("sentiment_ia", StringType(), False),
    StructField("score_sentiment", DoubleType(), False),
    StructField("intent_detecte", StringType(), False),
    StructField("score_risque_churn", IntegerType(), False),
    StructField("alerte_critique", BooleanType(), False),
    StructField("date_mise_a_jour", TimestampType(), False),
])

ligne_nouvelle = (
    str(resultat["call_id"]),
    str(resultat["sentiment_ia"]),
    float(resultat["score_sentiment"]),
    str(resultat["intent_detecte"]),
    int(resultat["score_risque_churn"]),
    bool(resultat["alerte_critique"]),
    datetime.now(),
)
df_nouveau = spark.createDataFrame([ligne_nouvelle], schema=schema_nouveau)
df_nouveau.createOrReplaceTempView("staging_appel")

# MERGE INTO : UPSERT sur call_id
spark.sql("""
    MERGE INTO silver_appels_enrichis AS target
    USING staging_appel AS source
    ON target.call_id = source.call_id
    WHEN MATCHED THEN
        UPDATE SET
            target.sentiment_ia       = source.sentiment_ia,
            target.score_sentiment    = source.score_sentiment,
            target.intent_detecte     = source.intent_detecte,
            target.score_risque_churn = source.score_risque_churn,
            target.alerte_critique    = source.alerte_critique
    WHEN NOT MATCHED THEN
        INSERT (call_id, sentiment_ia, score_sentiment,
                intent_detecte, score_risque_churn, alerte_critique)
        VALUES (source.call_id, source.sentiment_ia, source.score_sentiment,
                source.intent_detecte, source.score_risque_churn, source.alerte_critique)
""")

print(f"MERGE terminé pour {call_id}")
print(f"Score churn : {resultat['score_risque_churn']} — Alerte : {resultat['alerte_critique']}")

# -------------------------------------------------------
# ÉCRITURE DANS LA TABLE alertes_critiques (si score ≥ 50)
# -------------------------------------------------------
# Cette table est la seule "notification" nécessaire : elle est
# requêtable en SQL, visible dans Power BI, et ne dépend d'aucun
# service externe (pas de Teams, pas d'email, pas de webhook).
#
# Le Pipeline lit le score via mssparkutils.notebook.exit()
# pour afficher le statut dans le panneau Monitor de Fabric.

if resultat["alerte_critique"]:
    df_alerte = spark.createDataFrame([{
        "call_id":            resultat["call_id"],
        "score_risque_churn": int(resultat["score_risque_churn"]),
        "sentiment_ia":       resultat["sentiment_ia"],
        "intent_detecte":     resultat["intent_detecte"],
        "statut":             "NON_TRAITEE",
        "date_alerte":        datetime.now(),
    }])
    df_alerte.createOrReplaceTempView("staging_alerte")

    if not spark.catalog.tableExists("alertes_critiques"):
        df_alerte.write.mode("overwrite").format("delta").saveAsTable("alertes_critiques")
        print(f"🚨 Table alertes_critiques créée pour {call_id}")
    else:
        spark.sql("""
            MERGE INTO alertes_critiques AS target
            USING staging_alerte AS source
            ON target.call_id = source.call_id
            WHEN MATCHED THEN
                UPDATE SET
                    target.score_risque_churn = source.score_risque_churn,
                    target.sentiment_ia       = source.sentiment_ia,
                    target.intent_detecte     = source.intent_detecte,
                    target.statut             = source.statut,
                    target.date_alerte        = source.date_alerte
            WHEN NOT MATCHED THEN
                INSERT (call_id, score_risque_churn, sentiment_ia,
                        intent_detecte, statut, date_alerte)
                VALUES (source.call_id, source.score_risque_churn, source.sentiment_ia,
                        source.intent_detecte, source.statut, source.date_alerte)
        """)
        print(f"🚨 Alerte mise à jour dans alertes_critiques pour {call_id}")
else:
    print(f"✅ Appel {call_id} traité sans alerte (score = {resultat['score_risque_churn']})")

# Retourne un JSON au Pipeline → visible dans Monitor → panneau Output
# Contient le score ET le fichier réellement traité (détecté automatiquement)
# Le Pipeline lit json(...).score pour la condition et json(...).fichier pour les logs
import json
mssparkutils.notebook.exit(json.dumps({
    "score": resultat["score_risque_churn"],
    "fichier": call_file_path
}))
```

---

## Bloc 2 — Pipeline Data Factory

### 2.1 — Creating the Pipeline

1. Workspace → **+ New item** → **Data pipeline**
2. Nommer : `PL_Traitement_Appel_Entrant`

> The validated JSON definition of this Pipeline is provided in`Notebooks/Workshop 2/PL_Traitement_Appel_Entrant.json`. It can be used as a reference to control the names, parameters, variables and expressions described below.

### 2.2 — Activity 1: Parametric Notebook

1. In the canvas → **Activities** (left sign) → drag **Notebook** on the canvas
2. Name the activity:`ACT_Analyser_Appel`
3. In the **Settings** tab:
   - **Notebook** : `NB_Incremental_Processing`
   - **Base parameters** → **+ New parameter** :
     - Nom : `call_file_path`
     - Value: @pipeline().parameters.file enter

> 💡 **Explication `@pipeline().parameters.fichier_entrant`:** This dynamic expression (data Factory expression language) reads the parameter value`fichier_entrant`transmitted to the Pipeline during a manual test or by the OneLake trigger configured in Block 3.

4. Tab **Collection parameters** (not activity) → **+ New**:
   - Nom : `fichier_entrant`
   - Type : `String`
   - Default:`AUTO`

> `NB_Incremental_Processing`, actually develop **Base parameters**. The parameter is not added automatically by creating the activity. Without`call_file_path = @pipeline().parameters.fichier_entrant`, the Notebook keeps`AUTO`, even if a path is entered in the window **Pipeline run**.

### 2.3 — Activity 2: Condition If (alert threshold)

1. Slide **If Condition** on canvas after`ACT_Analyser_Appel`

2. Relier `ACT_Analyser_Appel` → `If Condition`(green arrow = success)

3. Nommer : `ACT_Condition_Alerte`

4. Expression :
   
   ```
   @greaterOrEquals(
    int(json(activity('ACT_Analyser_Appel').output.result.exitValue).score),
    50
   )
   ```

> 💡 **Explication :** `activity('ACT_Analyser_Appel').output.result.exitValue`recovers the JSON returned by`mssparkutils.notebook.exit()`. `json(...).score`extracts the numerical score, converted in full with`int()`for comparison at threshold 50. Syntactic validation also accepts`output.runOutput`, but the Pipeline run test confirmed that, in this Fabric environment, the value is actually exposed in`result.exitValue`.

**Branche TRUE — Registered Alert:**

1. In the TRUE branch → **+ Add activity** → **Set variable**

2. Nommer : `ACT_Log_Alerte`

3. Pipeline Variables → **+ New** : name`statut_traitement`, type `String`

4. Value:
   
   ```
   @concat('ALERTE CRITIQUE — ',
    json(activity('ACT_Analyser_Appel').output.result.exitValue).fichier,
    ' — Score: ',
    string(json(activity('ACT_Analyser_Appel').output.result.exitValue).score),
    '/100')
   ```

5. This value appears in **Monitor → Pipeline runs → Output** of each execution

> The alert is already written in`alertes_critiques`Notebook (Cellule 4). This Variable Set activity is only used to make the status **readable in Fabric's Monitor** panel without any additional tools.

**Branche FALSE — Logging normal :**

1. In the FALSE branch → **+ Add activity** → **Set variable**

2. Nommer : `ACT_Log_Normal`

3. Same variable`statut_traitement`

4. Value:
   
   ```
   @concat('OK — ',
    json(activity('ACT_Analyser_Appel').output.result.exitValue).fichier,
    ' traité sans alerte')
   ```

### 2.4 — Manual Pipeline Test

1. In the Pipeline → click **Validate** (top bar) → **Run**
2. In the popup → **file enter** :`Files/audio_calls/CALL_0001.txt`
3. Cliquer **OK**
4. Observe execution in the **Output** panel below:
   - `ACT_Analyser_Appel` → statut In progress → Succeeded
   - `ACT_Condition_Alerte`→ True or False according to score
   - Related activity → Followed

> The Pipeline was validated and successfully executed in Fabric. The execution test also confirmed that the JSON output of the Notebook should be read with`activity('ACT_Analyser_Appel').output.result.exitValue`in this environment.

---

### Block 3 — Automatic trigger (trigger OneLake)

> 💡 **Architecture retenue** :  
> Pipeline automatically triggers each new file filed in`LH_SolarVoix/Files/audio_calls/`via a OneLake Events trigger.  
> The file to be processed is detected by the Notebook itself (comparison of the file vs Silver).

#### 3.1 — Configure OneLake Events trigger

1. Open Pipeline`PL_Traitement_Appel_Entrant`

2. Tab **Home** → **Trigger**, then choose **OneLake events**.

3. In **Configure connection settings**:
   
   - **Event type(s)** : `Microsoft.Fabric.OneLake.FileCreated`
   - **Source** : `LH_SolarVoix`in`WS_SolarVoix`
   - selected folder:`Files/audio_calls`

4. Add the following two filters:
   
   | Field      | Operator         | Value                |
   | ---------- | ---------------- | -------------------- |
   | `subject`  | String contains  | `Files/audio_calls/` |
   | `data.url` | String ends with | `.txt`               |

5. Click **Next**, control the page **Review + connect**, then click **Finish**.

6. In the panel **Add rule**:
   
   - **Rule name** : `TR_test`
   - **Check** : `On each event`
   - **Select action** : `Run Pipeline`
   - **Fabric item** : `PL_Traitement_Appel_Entrant`
   - keep automatic event settings`Type`, `Subject`and`Source`
   - add parameter`fichier_entrant`, type`String`value`AUTO`

7. In **Save location**:
   
   - **Workspace** : `WS_SolarVoix`
   - **Item** : `Create a new item`
   - **New item name** : `ACT_SolarVoix_Appels`

8. Click **Create**, then check in the **Rules** panel that`TR_test`is in condition **Running**.

> The **Create** button remains disabled until the **Rule name** field is specified. The element`ACT_SolarVoix_Appels`is the Activator container;`TR_test`is the rule he hosts.

> OneLake repository can produce more than one event`FileCreated`during the creation or finalization of the same file. The`MERGE`on`call_id`return here Silver and`alertes_critiques`idempotents: several executions do not create duplicate jobs.

#### 3.2 — Modify the Notebook for automatic detection of new files

The separation described in sections **1.3** and **1.3 bis** is mandatory:

1. the cell marked **Parameters** declares only`call_file_path = "AUTO"` ;
2. Fabric then inserts an overload cell when calling by the Pipeline;
3. the next normal cell resolves`AUTO`or keeps the explicit path injected.

For a targeted manual test, enter`Files/audio_calls/CALL_0001.txt`in the window **Pipeline run**. The validated test then displays`Chemin explicite reçu du Pipeline`and follows the normal branch with a score of`15`.

### Order of execution for the test (most effective):

1. Update`NB_Incremental_Processing`with the cell`AUTO`, then set the default for Pipeline`fichier_entrant`to`AUTO`.
2. In`Test_Simulation_Appel_Critique`, run only the initialization cell of`alertes_critiques`.
3. Configure, save and activate the OneLake Events trigger.
4. Then run the simulation cell that creates`CALL_0121.txt`. Creating the file is the event that must automatically trigger the Pipeline.
5. For a manual test independent of the trigger, launch the Pipeline by explicitly providing`Files/audio_calls/CALL_0001.txt`or another existing path.

---

### 3.4 — Test de bout en bout

1. **Create a Test Notebook**:
   
   - Workspace → **+ New item** → **Notebook**
   - Nom : `Test_Simulation_Appel_Critique`
   - Attach Lakehouse`LH_SolarVoix`

2. **Step 0 — Initialize the table`alertes_critiques`** (to be executed first):
   
   > This cell creates the empty table if it does not exist yet, which avoids error`Invalid object name`later SQL checks.

```python
# === INITIALISATION — Création préventive de la table alertes_critiques ===
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from datetime import datetime

schema_alertes = StructType([
    StructField("call_id",             StringType(),    True),
    StructField("score_risque_churn",  IntegerType(),   True),
    StructField("sentiment_ia",        StringType(),    True),
    StructField("intent_detecte",      StringType(),    True),
    StructField("statut",              StringType(),    True),
    StructField("date_alerte",         TimestampType(), True),
])

# Crée la table Delta vide seulement si elle n’existe pas déjà
if not spark.catalog.tableExists("alertes_critiques"):
    df_vide = spark.createDataFrame([], schema_alertes)
    df_vide.write.format("delta").saveAsTable("alertes_critiques")
    print("✅ Table alertes_critiques créée (vide) — prête à recevoir des alertes.")
else:
    print("ℹ️ Table alertes_critiques déjà existante.")
```

3. ** Run simulation script**:

```python
# === TEST DE SIMULATION — Création d’un nouvel appel critique ===

texte_critique = """[Appel entrant - 08/04/2026] Client : Marie Dubois.
Produit concerné : Pompe à chaleur PAC.
Transcription : Je suis extrêmement en colère. Votre pompe à chaleur est tombée en panne
pour la troisième fois ce mois-ci. J’ai des enfants en bas âge et il fait froid.
J’ai contacté votre SAV cinq fois sans résultat. Je vais résilier mon contrat dès demain
et contacter mon avocat. C’est inadmissible et je veux un remboursement complet."""

chemin_test = "Files/audio_calls/CALL_0121.txt"

if mssparkutils.fs.exists(chemin_test):
    raise RuntimeError(
        f"{chemin_test} existe déjà. Supprimez-le ou choisissez un nouvel identifiant "
        "avant de tester un événement FileCreated."
    )

mssparkutils.fs.put(chemin_test, texte_critique, overwrite=False)

print("✅ Fichier CALL_0121.txt créé dans audio_calls/")
```

4. **Do not re-execute the creation cell.** Wait a few minutes, then open **Monitor**. One or more automatic executions of`PL_Traitement_Appel_Entrant`must appear.

5. **Add a verification cell**:

```python
# === VÉRIFICATION DU TRAITEMENT ÉVÉNEMENTIEL ===

call_id_test = "CALL_0121"

df_silver_test = (
    spark.table("silver_appels_enrichis")
    .filter(f"call_id = '{call_id_test}'")
)

df_alerte_test = (
    spark.table("alertes_critiques")
    .filter(f"call_id = '{call_id_test}'")
)

nb_silver = df_silver_test.count()
nb_alertes = df_alerte_test.count()

print(f"Lignes Silver pour {call_id_test} : {nb_silver}")
print(f"Alertes pour {call_id_test}       : {nb_alertes}")

print("\n=== ENREGISTREMENT SILVER ===")
display(df_silver_test)

print("\n=== ALERTE CRITIQUE ===")
display(df_alerte_test)

if nb_silver != 1:
    raise AssertionError(
        f"Une seule ligne Silver était attendue, résultat : {nb_silver}"
    )

if nb_alertes != 1:
    raise AssertionError(
        f"Une seule alerte était attendue, résultat : {nb_alertes}"
    )

alerte = df_alerte_test.first()

if alerte.score_risque_churn < 50:
    raise AssertionError(
        f"Le score d'alerte est insuffisant : {alerte.score_risque_churn}"
    )

print(
    f"\n✅ Validation réussie : {call_id_test} a été traité "
    f"une seule fois dans chaque table avec un score de "
    f"{alerte.score_risque_churn}/100."
)
```

### Actual validated results

| Monitoring                            | Observed result           |
| ----------------------------------- | --------------------------:|
| Automatic Pipeline Executions | 2, toutes deux `Succeeded` |
| Silver lines for`CALL_0121`      | 1                          |
| Alerts for`CALL_0121`            | 1                          |
| Sentiment IA                        | `negatif`                  |
| Intention detected                  | `resiliation`              |
| Score de risque churn               | `100/100`                  |
| Statut de l'alerte                  | `NON_TRAITEE`              |

> Trade columns such as`client_nom`, `ville`or`produit`remain nil for`CALL_0121`, because the test only creates a text file and no corresponding line in the initial metadata.

---

**Simple summary:**

1. Run cell **Step 0** → table`alertes_critiques`is guaranteed to exist
2. Check that`TR_test`is **Running**
3. Run the simulation script once →`CALL_0121.txt`is created
4. Pipeline is triggered automatically → processing + writing alert
5. Run verification cell → Silver line and critical alert
