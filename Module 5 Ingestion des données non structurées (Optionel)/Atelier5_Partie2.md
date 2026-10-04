#### Partie 2 : Pipeline automatisé + alertes sur appels critiques

#### Thème : Orchestration Data Factory + Activator (Real-Time Intelligence)

---

## Rappel et contexte

La Partie 1 a créé la table `silver_appels_enrichis` avec 120 appels analysés manuellement.

Problème : **ce traitement doit se déclencher automatiquement** à chaque nouveau fichier audio entrant. Un opérateur ne peut pas relancer manuellement le Notebook chaque jour.

**Objectif de la Partie 2 :** Construire un Pipeline Data Factory qui :

1. Se déclenche à l'arrivée d'un nouveau fichier dans le dossier `audio_calls/`
2. Traite le fichier (mise à jour de la table Silver)
3. Enregistre une alerte dans la table `alertes_critiques` si le score churn ≥ 50 (visible dans Fabric Monitor et Power BI)

**Architecture de cette partie — 100% native Fabric**

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

> 💡 **Remarque** Toutes les alertes sont tracées dans une table Delta `alertes_critiques` dans le Lakehouse. Cette approche est gratuite, persistante, requêtable en SQL, et directement exploitable dans le rapport Power BI de la Partie 3 — sans aucun abonnement externe.

---

# PARTIE 2

---

## Bloc 1 — Notebook paramétré (traitement d'un fichier unique)

> La Partie 1 traitait les 120 fichiers en batch. Ici, on traite **un seul fichier à la fois** de façon dynamique, via un paramètre passé par le Pipeline.

### 1.1 — Créer le Notebook paramétré

1. Workspace → **+ New item** → **Notebook**
2. Nommer : `NB_Traitement_Incremental`
3. Ajouter `LH_SolarVoix`

### 1.2 — Installation des dépendances

Ajoutez cette cellule une seule fois au début du Notebook. Elle installe les trois packages nécessaires dans la session Spark sans dupliquer l'installation plus loin dans le Notebook.

```python
# === CELLULE 0 : Installation des dépendances ===

import subprocess
import sys

packages = ["transformers", "torch", "sentencepiece"]
subprocess.run(
    [sys.executable, "-m", "pip", "install", "--quiet", *packages],
    check=True,
)

print("✅ Packages installés avec succès")
```

### 1.3 — Cellule 1 : Déclaration du paramètre

```python
# === CELLULE 1 : Paramètre d'entrée ===
#
# IMPORTANT : cette cellule doit rester marquée comme "Parameters".
# Fabric insère la valeur transmise par le Pipeline juste après
# l'exécution de cette cellule.

call_file_path = "AUTO"
```

Pour marquer la cellule, ouvrez son menu `...`, sélectionnez **Toggle parameter cell**, puis vérifiez que le bandeau **Parameters** apparaît en bas à droite.

> ⚠️ La cellule marquée **Parameters** doit uniquement déclarer le paramètre. Ne placez pas la détection automatique dans cette cellule : Fabric injecte la valeur du Pipeline après son exécution.

### 1.3 bis — Cellule normale : résolution du fichier à traiter

Insérez immédiatement après la cellule `Parameters` une cellule de code normale, non marquée **Parameters** :

```python
# === CELLULE 1 BIS : Résolution du fichier à traiter ===

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

### 1.4 — Cellule 2 : Extraction du call_id depuis le chemin

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

### 1.5 — Cellule 3 : Lecture et enrichissement du fichier

```python
# === CELLULE 3 : Traitement d'un seul appel (Version corrigée) ===

from transformers import pipeline as hf_pipeline
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

# ====================== CHARGEMENT DU MODÈLE ======================
print("Chargement du modèle de sentiment (nlptown/bert-base-multilingual-uncased-sentiment)...")
sentiment_pipeline = hf_pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=-1,          # CPU
    truncation=True,
    max_length=512
)

def mapper_sentiment(label: str) -> str:
    nb = int(label[0])
    if nb <= 2:
        return "negatif"
    elif nb == 3:
        return "neutre"
    else:
        return "positif"

# ====================== FONCTION PRINCIPALE ======================
def enrichir_appel(call_id: str, texte: str, duree_sec: int = 180) -> dict:
    """
    Applique l'analyse IA et calcule le score churn pour un appel unique.
    Retourne un dictionnaire prêt pour la table silver_appels_enrichis.
    """
    # Sentiment IA
    res = sentiment_pipeline([texte], batch_size=1)[0]
    sentiment_ia = mapper_sentiment(res["label"])
    score_sentiment = round(res["score"], 4)

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

### 1.6 — Cellule 4 : Mise à jour UPSERT de la table Silver

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
from pyspark.sql import Row

# Création d'un DataFrame temporaire avec le résultat
df_nouveau = spark.createDataFrame([Row(
    call_id           = resultat["call_id"],
    sentiment_ia      = resultat["sentiment_ia"],
    score_sentiment   = float(resultat["score_sentiment"]),
    intent_detecte    = resultat["intent_detecte"],
    score_risque_churn= int(resultat["score_risque_churn"]),
    alerte_critique   = bool(resultat["alerte_critique"]),
    date_mise_a_jour  = datetime.now(),
)])
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

### 2.1 — Créer le Pipeline

1. Workspace → **+ New item** → **Data pipeline**
2. Nommer : `PL_Traitement_Appel_Entrant`

> 💡 La définition JSON validée de ce Pipeline est fournie dans `Notebooks/Atelier 2/PL_Traitement_Appel_Entrant.json`. Elle peut être utilisée comme référence pour contrôler les noms, paramètres, variables et expressions décrits ci-dessous.

### 2.2 — Activité 1 : Notebook paramétré

1. Dans le canvas → **Activities** (panneau gauche) → glisser **Notebook** sur le canvas
2. Nommer l'activité : `ACT_Analyser_Appel`
3. Dans l'onglet **Settings** :
   - **Notebook** : `NB_Traitement_Incremental`
   - **Base parameters** → **+ New parameter** :
     - Nom : `call_file_path`
     - Valeur : @pipeline().parameters.fichier_entrant

> 💡 **Explication `@pipeline().parameters.fichier_entrant` :** Cette expression dynamique (langage d'expressions Data Factory) lit la valeur du paramètre `fichier_entrant` transmis au Pipeline lors d'un test manuel ou par le déclencheur OneLake configuré dans le Bloc 3.

4. Onglet **Parameters** du Pipeline (pas de l'activité) → **+ New** :
   - Nom : `fichier_entrant`
   - Type : `String`
   - Valeur par défaut : `AUTO`

> ⚠️ **Point de contrôle validé :** après avoir sélectionné `NB_Traitement_Incremental`, développez réellement **Base parameters**. Le paramètre n'est pas ajouté automatiquement par la création de l'activité. Sans `call_file_path = @pipeline().parameters.fichier_entrant`, le Notebook conserve `AUTO`, même si un chemin est saisi dans la fenêtre **Pipeline run**.

### 2.3 — Activité 2 : Condition If (seuil alerte)

1. Glisser **If Condition** sur le canvas après `ACT_Analyser_Appel`

2. Relier `ACT_Analyser_Appel` → `If Condition` (flèche verte = succès)

3. Nommer : `ACT_Condition_Alerte`

4. Expression :
   
   ```
   @greaterOrEquals(
    int(json(activity('ACT_Analyser_Appel').output.result.exitValue).score),
    50
   )
   ```

> 💡 **Explication :** `activity('ACT_Analyser_Appel').output.result.exitValue` récupère le JSON retourné par `mssparkutils.notebook.exit()`. `json(...).score` extrait le score numérique, converti en entier avec `int()` pour la comparaison au seuil 50. La validation syntaxique accepte également `output.runOutput`, mais le test d'exécution du Pipeline a confirmé que, dans cet environnement Fabric, la valeur est réellement exposée dans `result.exitValue`.

**Branche TRUE — Alerte enregistrée :**

1. Dans la branche TRUE → **+ Add activity** → **Set variable**

2. Nommer : `ACT_Log_Alerte`

3. Variables du Pipeline → **+ New** : nom `statut_traitement`, type `String`

4. Valeur :
   
   ```
   @concat('ALERTE CRITIQUE — ',
    json(activity('ACT_Analyser_Appel').output.result.exitValue).fichier,
    ' — Score: ',
    string(json(activity('ACT_Analyser_Appel').output.result.exitValue).score),
    '/100')
   ```

5. Cette valeur apparaît dans **Monitor → Pipeline runs → Output** de chaque exécution

> 💡 L'alerte est déjà écrite dans `alertes_critiques` par le Notebook (Cellule 4). Cette activité Set Variable sert uniquement à rendre le statut **lisible dans le panneau Monitor** de Fabric sans outil supplémentaire.

**Branche FALSE — Logging normal :**

1. Dans la branche FALSE → **+ Add activity** → **Set variable**

2. Nommer : `ACT_Log_Normal`

3. Même variable `statut_traitement`

4. Valeur :
   
   ```
   @concat('OK — ',
    json(activity('ACT_Analyser_Appel').output.result.exitValue).fichier,
    ' traité sans alerte')
   ```

### 2.4 — Test manuel du Pipeline

1. Dans le Pipeline → cliquer **Validate** (barre du haut) → **Run**
2. Dans la popup → **fichier_entrant** : `Files/audio_calls/CALL_0001.txt`
3. Cliquer **OK**
4. Observer l'exécution dans le panneau **Output** en bas :
   - `ACT_Analyser_Appel` → statut In progress → Succeeded
   - `ACT_Condition_Alerte` → True ou False selon le score
   - Activité correspondante → Succeeded

> ✅ **Résultat de validation :** le Pipeline a été validé puis exécuté avec succès dans Fabric. Le test d'exécution a également confirmé que la sortie JSON du Notebook doit être lue avec `activity('ACT_Analyser_Appel').output.result.exitValue` dans cet environnement.

---

### Bloc 3 — Déclencheur automatique (trigger OneLake)

> 💡 **Architecture retenue** :  
> Le Pipeline se déclenche automatiquement à chaque nouveau fichier déposé dans `LH_SolarVoix/Files/audio_calls/` via un trigger OneLake Events.  
> La détection du fichier à traiter est assurée par le Notebook lui-même (comparaison dossier vs Silver).

#### 3.1 — Configurer le trigger OneLake Events (déclenchement sur nouveau fichier)

1. Ouvrir le Pipeline `PL_Traitement_Appel_Entrant`

2. Onglet **Home** → **Trigger**, puis choisir **OneLake events**.

3. Dans **Configure connection settings** :
   
   - **Event type(s)** : `Microsoft.Fabric.OneLake.FileCreated`
   - **Source** : `LH_SolarVoix` dans `WS_SolarVoix`
   - dossier sélectionné : `Files/audio_calls`

4. Ajouter les deux filtres suivants :
   
   | Field      | Operator         | Value                |
   | ---------- | ---------------- | -------------------- |
   | `subject`  | String contains  | `Files/audio_calls/` |
   | `data.url` | String ends with | `.txt`               |

5. Cliquer **Next**, contrôler la page **Review + connect**, puis cliquer **Finish**.

6. Dans le panneau **Add rule** :
   
   - **Rule name** : `TR_test`
   - **Check** : `On each event`
   - **Select action** : `Run Pipeline`
   - **Fabric item** : `PL_Traitement_Appel_Entrant`
   - conserver les paramètres événementiels automatiques `Type`, `Subject` et `Source`
   - ajouter le paramètre `fichier_entrant`, type `String`, valeur `AUTO`

7. Dans **Save location** :
   
   - **Workspace** : `WS_SolarVoix`
   - **Item** : `Create a new item`
   - **New item name** : `ACT_SolarVoix_Appels`

8. Cliquer **Create**, puis vérifier dans le panneau **Rules** que `TR_test` est en état **Running**.

> 💡 Le bouton **Create** reste désactivé tant que le champ obligatoire **Rule name** n'est pas renseigné. L'élément `ACT_SolarVoix_Appels` est le conteneur Activator ; `TR_test` est la règle qu'il héberge.

> ⚠️ Un dépôt OneLake peut produire plus d'un événement `FileCreated` pendant la création ou la finalisation du même fichier. Les `MERGE` sur `call_id` rendent ici Silver et `alertes_critiques` idempotentes : plusieurs exécutions ne créent pas de doublons métier.

#### 3.2 — Modifier le Notebook pour la détection automatique des nouveaux fichiers

La séparation décrite aux sections **1.3** et **1.3 bis** est obligatoire :

1. la cellule marquée **Parameters** déclare seulement `call_file_path = "AUTO"` ;
2. Fabric insère ensuite une cellule de surcharge lors de l'appel par le Pipeline ;
3. la cellule normale suivante résout `AUTO` ou conserve le chemin explicite injecté.

Pour un test manuel ciblé, saisissez `Files/audio_calls/CALL_0001.txt` dans la fenêtre **Pipeline run**. Le test validé affiche alors `Chemin explicite reçu du Pipeline` et suit la branche normale avec un score de `15`.

### Ordre d’exécution pour le test (le plus efficace) :

1. Mettre à jour `NB_Traitement_Incremental` avec la cellule `AUTO`, puis mettre la valeur par défaut du paramètre Pipeline `fichier_entrant` à `AUTO`.
2. Dans `Test_Simulation_Appel_Critique`, exécuter uniquement la cellule d'initialisation de `alertes_critiques`.
3. Configurer, enregistrer et activer le déclencheur OneLake Events.
4. Exécuter ensuite la cellule de simulation qui crée `CALL_0121.txt`. La création du fichier constitue l'événement qui doit déclencher automatiquement le Pipeline.
5. Pour un test manuel indépendant du déclencheur, lancez le Pipeline en fournissant explicitement `Files/audio_calls/CALL_0001.txt` ou un autre chemin existant.

---

### 3.4 — Test de bout en bout

1. **Créer un Notebook dédié au test** :
   
   - Workspace → **+ New item** → **Notebook**
   - Nom : `Test_Simulation_Appel_Critique`
   - Attacher le Lakehouse `LH_SolarVoix`

2. **Étape 0 — Initialiser la table `alertes_critiques`** (à exécuter en premier) :
   
   > Cette cellule crée la table vide si elle n’existe pas encore, ce qui évite l’erreur `Invalid object name` lors des vérifications SQL ultérieures.

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

3. **Exécuter le script de simulation** :

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

4. **Ne pas réexécuter la cellule de création.** Attendre quelques minutes, puis ouvrir **Monitor**. Une ou plusieurs exécutions automatiques de `PL_Traitement_Appel_Entrant` doivent apparaître.

5. **Ajouter une cellule de vérification** :

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

### Résultats réellement validés

| Contrôle                            | Résultat observé           |
| ----------------------------------- | --------------------------:|
| Exécutions automatiques du Pipeline | 2, toutes deux `Succeeded` |
| Lignes Silver pour `CALL_0121`      | 1                          |
| Alertes pour `CALL_0121`            | 1                          |
| Sentiment IA                        | `negatif`                  |
| Intention détectée                  | `resiliation`              |
| Score de risque churn               | `100/100`                  |
| Statut de l'alerte                  | `NON_TRAITEE`              |

> Les colonnes métier telles que `client_nom`, `ville` ou `produit` restent nulles pour `CALL_0121`, car le test crée uniquement un fichier texte et aucune ligne correspondante dans les métadonnées initiales.

---

**Résumé simple :**

1. Exécuter la cellule **Étape 0** → la table `alertes_critiques` est garantie d’exister
2. Vérifier que `TR_test` est **Running**
3. Exécuter une seule fois le script de simulation → `CALL_0121.txt` est créé
4. Le Pipeline est déclenché automatiquement → traitement + écriture de l'alerte
5. Exécuter la cellule de vérification → une ligne Silver et une alerte critique
