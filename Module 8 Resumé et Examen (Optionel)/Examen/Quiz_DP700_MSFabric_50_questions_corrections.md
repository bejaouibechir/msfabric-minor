## Évaluation des compétences – 50 questions corrigées sur Microsoft Fabric

## Question 1

**Nature** : Choix unique

**Énoncé** :  
Vous devez stocker les fichiers et données initiales sans correction métier afin de garantir la traçabilité. Quelle couche devez-vous utiliser ?

**Alternatives** :  
A. Bronze  
B. Silver  
C. Gold  
D. Copper

**Solution** :  
✅ **Réponse correcte : A. Bronze**  
*Justification* : La couche Bronze conserve les données brutes, exactement comme ingérées, sans aucune transformation métier. C'est le fondement de l'architecture Medallion qui garantit la reproductibilité et la traçabilité.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B. Silver** : contient des données nettoyées et validées, non brutes.  
- **C. Gold** : contient des données agrégées, prêtes pour l'analyse.  
- **D. Copper** : n'est pas une couche standard de l'architecture Medallion.  
  🔗 [Documentation Medallion](https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture)

---

##Question 2

**Nature** : Choix multiple (2 réponses attendues)

**Énoncé** :  
Quelles opérations **n'appartiennent pas principalement** à la couche Silver ? Sélectionnez deux réponses.

**Alternatives** :  
A. Déduublonner les lignes de consommation  
B. Corriger les types et filtrer les valeurs invalides  
C. Aggréger les données  
D. Supprimer les données sources après ingestion  
E. Modéliser en schéma en étoile

**Solution** :  
✅ **Réponses correctes : C et E**  
*Justification* :  

- **C. Aggréger les données** : relève de la couche Gold (données pré-agrégées pour le métier).  
- **E. Modéliser en schéma en étoile** : relève également de la couche Gold ou du modèle sémantique.  
  ❌ *Pourquoi les autres options appartiennent à Silver* :  
- **A** et **B** sont des actions typiques de nettoyage/validation (Silver).  
- **D** (supprimer les sources) n'est pas recommandé du tout, mais ce n'est pas une fonction de Silver.  
  🔗 https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture#what-is-medallion-architecture

---

## Question 3

**Nature** : Tableau à compléter (grille à choix multiples - associée)

**Énoncé** :  
Associez chaque besoin à la couche la plus appropriée.  

| Besoin                                          | A. Bronze | B. Silver | C. Gold |
| ----------------------------------------------- | --------- | --------- | ------- |
| Conserver les données proches du brut           |           |           |         |
| Produire une table nettoyée et enrichie         |           |           |         |
| Fournir des KPI journaliers prêts pour Power BI |           |           |         |

**Solution** :  
✅ Conserver les données proches du brut → **A. Bronze**  
✅ Produire une table nettoyée et enrichie → **B. Silver**  
✅ Fournir des KPI journaliers prêts pour Power BI → **C. Gold**  

*Justification* : Voir les définitions standards de l'architecture Medallion.  
🔗 [Documentation couches](https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture)

---

## Question 4

**Nature** : Choix unique

**Énoncé** :  
Vous avez un pipeline Fabric qui charge des données brutes dans une table Bronze, puis les nettoie dans une table Silver. Vous voulez créer une table Gold agrégée par **site et par jour**.  
Quelle est la méthode **la plus flexible** pour implémenter cette transformation ?

**Alternatives** :  
A. Utiliser une activité **Dataflow Gen2** (interface visuelle)  
B. Utiliser un **Notebook Spark** avec des DataFrames  
C. Faire les agrégations dans Power BI Desktop avant de publier  
D. Utiliser une **vue SQL** standard dans le Warehouse

**Solution** :  
✅ **Réponse correcte : B. Notebook Spark**  
*Justification* : Le notebook PySpark permet une logique complexe, des tests, des librairies externes, et une gestion fine des performances (partitionnement, optimisation). C'est la solution la plus flexible pour des transformations évolutives.  
❌ *Pourquoi les autres sont incorrectes* :  

- **A** : Dataflow Gen2 est plus limité en logique avancée.  
- **C** : Déporter l'agrégation dans Power BI est une mauvaise pratique (charge de calcul non mutualisée, non réutilisable).  
- **D** : Une vue SQL manque de flexibilité pour des transformations complexes et peut souffrir de performances sur gros volumes.  
  🔗 [Notebooks Fabric](https://learn.microsoft.com/fr-fr/fabric/data-engineering/author-notebook)

---

## Question 5

**Nature** : Choix unique

**Énoncé** :  
Vous avez une jointure entre la table DimCustomer et la table FactSales qui aboutit à un très grand nombre de lignes. Quelle cause est la plus probable ?

**Alternatives** :  
A. La colonne de jointure du côté DimCustomer n'impose pas la contrainte de valeur unique  
B. Parce que vous utilisez une jointure Left  
C. Parce que vous utilisez une jointure Right  
D. Parce que vous utilisez une jointure Inner

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Si la colonne de jointure dans la dimension n'est pas unique, chaque ligne de la table de faits se joint à plusieurs lignes de la dimension, multipliant le nombre de lignes (produit cartésien partiel).  
❌ *Pourquoi les autres sont incorrectes* :  

- **B / C / D** : Les types de jointure (Left, Right, Inner) ne créent pas de multiplication par défaut ; seule une clé non unique dans la dimension cause ce problème.  
  🔗 [Relations dans Power BI](https://learn.microsoft.com/fr-fr/power-bi/guidance/relationships)

---

## Question 6

**Nature** : Choix unique

**Énoncé** :  
Au niveau d'un pipeline, vous devez lister dynamiquement les fichiers présents dans un dossier avant de les parcourir. Quelle activité devez-vous utiliser pour préparer le terrain ?

**Alternatives** :  
A. Get Metadata  
B. Set Variable  
C. ForEach  
D. Execute Pipeline

**Solution** :  
✅ **Réponse correcte : A. Get Metadata**  
*Justification* : L'activité Get Metadata permet de récupérer la liste des fichiers (childItems) d'un dossier. Elle est incontournable pour toute boucle dynamique.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Set Variable ne lit pas les métadonnées.  
- **C** : ForEach itère sur une liste déjà existante.  
- **D** : Execute Pipeline exécute un autre pipeline.  
  🔗 [Activité Get Metadata](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-get-metadata-activity)

---

## Question 7

**Nature** : Choix unique

**Énoncé** :  
Vous devez appliquer la même logique de copie à chaque fichier retourné par l'activité de métadonnées. Quelle activité devez-vous utiliser ?

**Alternatives** :  
A. If Condition  
B. ForEach  
C. Until  
D. Do-Until

**Solution** :  
✅ **Réponse correcte : B. ForEach**  
*Justification* : ForEach est l'activité native pour itérer sur une collection (liste de fichiers) et exécuter une ou plusieurs activités pour chaque élément.  
❌ *Pourquoi les autres sont incorrectes* :  

- **A** : If Condition sert à brancher selon une condition, pas à boucler.  
- **C / D** : Until/Do-Until sont des boucles conditionnelles, mais pas adaptées à une liste fixe.  
  🔗 [Activité ForEach](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-for-each-activity)

---

## Question 8

**Nature** : Drag & Drop textuel / appariement

**Énoncé** :  
Associez chaque activité de pipeline à son rôle.

| Activité            | Role                                            |
| ------------------- | ----------------------------------------------- |
| 1. Lookup           | A. Exécuter un pipeline enfant                  |
| 2. If Condition     | B. Lire la première ligne                       |
| 3. Until            | C. Choisir une branche selon une expression     |
| 4. Execute Pipeline | D. Répéter jusqu'à satisfaction d'une condition |

**Solution** :  
✅ 1 → **B** (Lookup lit généralement la première ligne, sauf paramétrage)  
✅ 2 → **C** (If Condition branche selon expression)  
✅ 3 → **D** (Until répète jusqu'à condition vraie)  
✅ 4 → **A** (Execute Pipeline exécute un pipeline enfant)  

*Justification* : cf. documentation Azure Data Factory / Fabric pipelines.  
🔗 [Activités de contrôle de flux](https://learn.microsoft.com/fr-fr/azure/data-factory/concepts-pipelines-activities)

---

## Question 9

**Nature** : Choix unique

**Énoncé** :  
Une activité **Lookup** interroge une table de seuils contenant **4 lignes**. Par défaut (sans modification des paramètres), combien de lignes cette activité retourne-t-elle ?

**Alternatives** :  
A. 0 ligne (erreur)  
B. 1 ligne (la première uniquement)  
C. 4 lignes (toutes les lignes)  
D. Cela dépend du type de connexion utilisée

**Solution** :  
✅ **Réponse correcte : B. 1 ligne**  
*Justification* : Par défaut, l'activité Lookup ne retourne que la **première ligne** de l'ensemble de résultats, sauf si vous modifiez la propriété `firstRowOnly` à false.  
❌ *Pourquoi les autres sont incorrectes* :  

- **C** : Nécessite de désactiver `firstRowOnly`.  
- **A** : Il n'y a pas d'erreur, la première ligne est retournée.  
  🔗 [Activité Lookup](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-lookup-activity)

---

## Question 10

**Nature** : Choix unique

**Énoncé** :  
Après la copie des infrastructures actives depuis l'activité **CopierInfrastructuresActives**, le pipeline doit continuer seulement si `rowsCopied` est supérieur à zéro. Quelle expression est la plus cohérente ?

**Alternatives** :  
A. `@greater(activity('CopierInfrastructuresActives').output.rowsCopied, 0)`  
B. `@equals(variables('NombreIterations'), 'Gold')`  
C. `@contains(triggerBody().fileName, '.pbix')`  
D. `@less(activity('CopierInfrastructuresActives').output.rowsCopied, 0)`

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : L'expression `greater(..., 0)` est la syntaxe correcte pour tester si le nombre de lignes copiées est strictement positif.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Compare une variable à une chaîne non pertinente.  
- **C** : Teste la présence d'une extension dans un déclencheur.  
- **D** : Teste l'infériorité, l'inverse de ce qui est demandé.  
  🔗 [Fonctions d'expression](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-expression-language-functions)

---

## Question 11

**Nature** : Choix multiple (2 réponses attendues)

**Énoncé** :  
Dans Microsoft Fabric, parmi les éléments suivants, **deux** sont des vraies **activités natives de pipeline** couramment utilisées pour une orchestration de bout en bout. Sélectionnez les deux bonnes réponses.

**Alternatives** :  
A. Execute Pipeline  
B. Wait  
C. KQL summarize  
D. DAX CALCULATE  
E. Power BI bookmark

**Solution** :  
✅ **Réponses correctes : A et B**  
*Justification* :  

- **Execute Pipeline** est une activité native pour appeler un autre pipeline.  
- **Wait** est une activité native pour introduire une pause.  
  ❌ *Les autres ne sont pas des activités de pipeline* :  
- **C** : `KQL summarize` est une instruction KQL, non une activité.  
- **D** : `DAX CALCULATE` est une fonction DAX dans Power BI.  
- **E** : `Power BI bookmark` est un élément d'interface Power BI.  
  🔗 [Activités de pipeline Fabric](https://learn.microsoft.com/fr-fr/fabric/data-factory/pipeline-activities)

---

## Question 12

**Nature** : Choix unique

**Énoncé** :  
Dans un pipeline Fabric orchestrant les couches Bronze, Silver et Gold, vous devez exécuter plusieurs activités de transformation sur la couche Silver. Cependant, ces transformations ne doivent démarrer que si l'ingestion Bronze s'est terminée avec succès, sans erreur.  
Quelle activité de pipeline utilisez-vous pour implémenter cette condition ?

**Alternatives** :  
A. Execute Pipeline  
B. If Condition  
C. When Condition  
D. Filter

**Solution** :  
✅ **Réponse correcte : B. If Condition**  
*Justification* : L'activité **If Condition** permet d'exécuter un bloc d'activités uniquement si une expression booléenne (par exemple, vérification du succès de l'activité précédente) est vraie. C'est l'outil standard pour le branching conditionnel.  
❌ *Pourquoi les autres sont incorrectes* :  

- **A** : Execute Pipeline ne conditionne pas, il exécute.  
- **C** : When Condition n'existe pas en tant qu'activité standard (c'est une condition dans les déclencheurs).  
- **D** : Filter sert à filtrer une liste, pas à conditionner l'exécution.  
  🔗 [Activité If Condition](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-if-condition-activity)

---

## Question 13

**Nature** : Choix unique

**Énoncé** :  
Un pipeline Microsoft Fabric est déclenché automatiquement dès l'arrivée d'un **nouveau fichier** dans un dossier source (trigger événementiel). Dans le notebook appelé par ce pipeline, le développeur a mal codé le script de façon à provoquer une lecture de **tout le dossier source** à chaque déclenchement, au lieu d'utiliser uniquement le chemin du fichier reçu par le trigger.  
Quelle conséquence en résulte ?

**Alternatives** :  
A. Les fichiers déjà traités peuvent être réinsérés en doublon  
B. Le trigger événementiel cesse de fonctionner après la première exécution  
C. Les performances du notebook diminuent, mais aucune donnée n'est dupliquée  
D. Le pipeline ignore automatiquement les fichiers déjà lus grâce au checkpointing de Spark

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Si le notebook relit tout le dossier à chaque déclenchement sans logique de déduplication (MERGE, upsert), les fichiers déjà traités seront relus et leurs données insérées à nouveau, créant des doublons.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Le trigger continue de fonctionner, ce n'est pas un problème de trigger.  
- **C** : Il y a bien un risque de duplication, pas seulement de performance.  
- **D** : Le checkpointing Spark ne s'applique pas automatiquement aux lectures brutes de fichiers.  
  🔗 [Bonnes pratiques d'ingestion incrémentale](https://learn.microsoft.com/fr-fr/fabric/data-engineering/incremental-refresh)

---

## Question 14

**Nature** : Choix multiple (plusieurs réponses possibles)

**Énoncé** :  
Vous devez harmoniser plusieurs fichiers énergétiques avec une interface low-code à jour avant de charger le résultat. Quel outil est le plus adapté ?

**Alternatives** :  
A. Dataflow Gen2  
B. Warehouse avec T-SQL  
C. Lakehouse avec raccourcis  
D. Dataflow Gen1  
E. Pipeline

**Solution** :  
✅ **Réponse correcte : A. Dataflow Gen2**  
*Justification* : Dataflow Gen2 est l'outil low-code moderne pour l'ingestion, la transformation et le chargement (ETL) dans Fabric. Il offre une interface visuelle riche et est conçu pour l'harmonisation de sources variées.  
❌ *Pourquoi les autres sont moins adaptés* :  

- **B** : T-SQL n'est pas low-code.  
- **C** : Lakehouse est un stockage, pas un outil de transformation low-code.  
- **D** : Dataflow Gen1 est déprécié au profit de Gen2.  
- **E** : Un pipeline orchestre mais ne transforme pas nativement en low-code.  
  🔗 [Dataflow Gen2 dans Fabric](https://learn.microsoft.com/fr-fr/fabric/data-factory/dataflow-gen2-overview)

---

## Question 15

**Nature** : Choix multiple (plusieurs réponses possibles)

**Énoncé** :  
Dans Microsoft Fabric, vous devez calculer l'empreinte carbone à partir de fichiers CSV (volumes) et d'une table SQL (facteurs d'émission) résidant dans un Lakehouse différent. Vous voulez un résultat unique **sans copie physique des données**. Quelles deux techniques combinez-vous ?

**Alternatives** :  
A. Shortcut vers les fichiers CSV + Shortcut vers la table SQL de l'autre Lakehouse  
B. Dataflow Gen2 avec liaison directe aux deux sources  
C. Lakehouse avec vue Spark utilisant des shortcuts  
D. Warehouse avec vue SQL utilisant des shortcuts  
E. Pipeline avec activité Copy Data et fusion

**Solution** :  
✅ **Réponses correctes : A et C**  
*Justification* :  

- **A** : Les raccourcis permettent d'accéder aux données sans les copier.  
- **C** : Une vue Spark (ou notebook) peut alors lire via ces raccourcis et joindre les données.  
  ❌ *Pourquoi les autres sont incorrects pour l'absence de copie* :  
- **B** : Dataflow Gen2 peut lier directement, mais il peut matérialiser des données. Néanmoins, l'association A+C est plus native.  
- **D** : Warehouse avec vue SQL ne lit pas nativement des fichiers CSV via shortcut sans copie préalable.  
- **E** : Copy Data effectue une copie physique.  
  🔗 [Shortcuts dans OneLake](https://learn.microsoft.com/fr-fr/fabric/onelake/onelake-shortcuts)

---

## Question 16

**Nature** : Choix unique

**Énoncé** :  
Un notebook doit réécrire une table Delta Silver après nettoyage. Quelle instruction est la plus cohérente ?

**Alternatives** :  
A.`df.write.format("delta").mode("overwrite").saveAsTable("silver.table")`  
B. `df.to_excel("silver.table")`  
C. `CREATE EVENTSTREAM silver.table`  
D. `git merge silver.table`

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : En PySpark, écrire un DataFrame en table Delta se fait avec `write.format("delta").mode("overwrite").saveAsTable(...)`, ce qui permet de remplacer complètement la table Silver.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : `to_excel` n'existe pas pour Spark, et Excel n'est pas adapté.  
- **C** : CREATE EVENTSTREAM crée un flux d'événements, pas une table.  
- **D** : `git merge` est une commande de gestion de version.  
  🔗 [Écrire une table Delta](https://learn.microsoft.com/fr-fr/fabric/data-engineering/delta-lake-table-operations)

---

## Question 17

**Nature** : Choix unique

**Énoncé** :  
Vous avez une table Delta nommée `sales_raw` qui reçoit chaque heure de nouvelles lignes en mode `append`. Un développeur ajoute une nouvelle colonne `region` dans les fichiers sources. Vous voulez que cette colonne soit automatiquement ajoutée à la table sans casser la structure existante. Quelle option devez-vous utiliser dans votre notebook PySpark ?

**Alternatives** :  
A. `.option("mergeSchema", "true")`  
B. `.mode("overwrite")`  
C. `.option("header", "true")`  
D. `.mode("failfast")`

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : L'option `mergeSchema` permet d'ajouter automatiquement de nouvelles colonnes lors d'une écriture (append ou overwrite) sans détruire le schéma existant. C'est exactement ce qui est demandé.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : `overwrite` supprime et recrée la table sans préserver les anciennes données.  
- **C** : `header` gère l'en-tête des fichiers CSV, pas l'évolution de schéma.  
- **D** : `failfast` échoue à la première erreur, ce qu'on ne veut pas.  
  🔗 [Évolution du schéma Delta](https://learn.microsoft.com/fr-fr/azure/databricks/delta/schema-evolution)

---

## Question 18

**Nature** : Tableau à compléter (grille à choix multiples)

**Énoncé** :  
Associez le traitement à l'outil le plus cohérent.

| Traitement                                    | A. Dataflow Gen2 | B. Notebook Spark | C. Power BI |
| --------------------------------------------- | ---------------- | ----------------- | ----------- |
| Transformation low-code de sources tabulaires |                  |                   |             |
| Nettoyage avancé avec DataFrames              |                  |                   |             |
| Visualisation et mesures métier               |                  |                   |             |

**Solution** :  
✅ Transformation low-code → **A. Dataflow Gen2**  
✅ Nettoyage avancé avec DataFrames → **B. Notebook Spark**  
✅ Visualisation et mesures métier → **C. Power BI**  

*Justification* : Chacun de ces outils a un objectif principal : ETL visuel (Dataflow), traitement code (Notebook), reporting (Power BI).  
🔗 [Choisir entre Dataflow et Notebook](https://learn.microsoft.com/fr-fr/fabric/data-engineering/choose-dataflow-notebook)

---

## Question 19

**Nature** : Choix multiple

**Énoncé** :  
Vous avez un pipeline Fabric qui charge chaque jour 100 fichiers CSV dans un Lakehouse. Un fichier corrompu fait échouer tout le pipeline. Vous voulez que les fichiers valides soient chargés et que les fichiers corrompus soient ignorés et enregistrés dans une table d'erreurs. Quelle activité Pipeline ou option Dataflow permet cela ?

**Alternatives** :  
A. Activité **Copy Data** avec tolérance d'erreur (error tolerance)  
B. Activité **Notebook** avec `spark.conf.set("spark.sql.files.ignoreCorruptFiles", "true")`  
C. Activité **Get Metadata** seule  
D. Activité **Web** appelant une API REST

**Solution** :  
✅ **Réponses correctes : A et B** (question à choix multiple, plusieurs réponses possibles)  
*Justification* :  

- **A** : L'activité Copy Data permet de configurer une tolérance d'erreur (`fault tolerance`) pour ignorer les lignes ou fichiers corrompus.  
- **B** : Dans un notebook, le paramètre Spark `spark.sql.files.ignoreCorruptFiles` permet d'ignorer les fichiers corrompus pendant la lecture.  
  ❌ *Pourquoi les autres sont incorrectes* :  
- **C** : Get Metadata ne charge pas les données.  
- **D** : Web appelle une API mais ne gère pas la tolérance aux fichiers corrompus.  
  🔗 [Tolérance d'erreur Copy Data](https://learn.microsoft.com/fr-fr/azure/data-factory/connector-troubleshoot-fault-tolerance) et [ignoreCorruptFiles Spark](https://spark.apache.org/docs/latest/sql-data-sources-generic-options.html)

---

## Question 20

**Nature** : Choix unique

**Énoncé** :  
Pourquoi un traitement incrémental doit-il utiliser une clé ou une logique de MERGE plutôt qu'un append systématique ?

**Alternatives** :  
A. Pour éviter les doublons et rendre le chargement idempotent  
B. Pour éviter les erreurs et les conflits des données  
C. Pour éviter l'écrasement des données  
D. Pour accélérer le temps d'exécution des requêtes

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Le MERGE (upsert) permet d’insérer les nouvelles lignes et de mettre à jour les lignes existantes sur la base d’une clé métier. Cela évite les doublons et garantit l’idempotence : relancer le même chargement ne change pas le résultat final.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Le merge ne corrige pas les conflits de données du même type.  
- **C** : On veut parfois écraser certaines parties, pas éviter tout écrasement.  
- **D** : Le merge peut être plus lent qu'un simple append.  
  🔗 [MERGE dans les tables Delta](https://learn.microsoft.com/fr-fr/fabric/data-engineering/delta-lake-table-operations#upsert-into-a-table-using-merge)

---

## Question 21

**Nature** : Choix unique

**Énoncé** :  
Quelle destination est la plus adaptée pour interroger des événements IoT en quasi temps réel avec KQL ?

**Alternatives** :  
A. KQL Database / Eventhouse  
B. Scheduler  
C. Trigger  
D. EventStream et Activator

**Solution** :  
✅ **Réponse correcte : A. KQL Database / Eventhouse**  
*Justification* : L'Eventhouse (anciennement KQL Database) est le moteur de stockage et d'interrogation temps réel de Fabric Real-Time Intelligence. Il permet d'exécuter des requêtes KQL sur des flux d'événements avec une latence très faible.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Scheduler n'est pas une destination, c'est un planificateur.  
- **C** : Trigger déclenche des actions, mais n'interroge pas.  
- **D** : EventStream et Activator servent à router et réagir, pas à interroger de manière interactive.  
  🔗 [Eventhouse dans Fabric](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/eventhouse)

---

## Question 22

**Nature** : Choix unique

**Énoncé** :  
Vous devez compter les événements par turbine et par fenêtre de cinq minutes dans TurbineEvents. Quelle requête KQL est la plus cohérente ?

**Alternatives** :  
A. `TurbineEvents | summarize count() by bin(Timestamp, 5m)`  
B. `SELECT COUNT(*) FROM TurbineEvents GROUP BY DATEADD(MINUTE, DATEDIFF(MINUTE, 0, Timestamp) / 5 * 5, 0)`  
C. `CALCULATE(COUNTROWS(TurbineEvents))`  
D. `SELECT turbine, COUNT(*) FROM TurbineEvents GROUP BY turbine, window(Timestamp, '5 minutes')`

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : En KQL, la fonction `bin()` permet de créer des intervalles réguliers (ici 5 minutes) pour les dates. La syntaxe `summarize count() by bin(Timestamp, 5m)` est la manière native KQL de compter par fenêtre.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Syntaxe T-SQL pure, non KQL.  
- **C** : Syntaxe DAX (Power BI).  
- **D** : Mélange SQL et `window()` qui n'est pas KQL standard.  
  🔗 [Fonction bin() en KQL](https://learn.microsoft.com/fr-fr/kusto/query/bin-function)

---

## Question 23

**Nature** : Choix multiple (plusieurs réponses possibles)

**Énoncé** :  
Dans une table KQL `TurbineEvents` qui reçoit en continu des mesures (température, vibration, puissance), quelles deux opérations sont possibles et pertinentes en requête KQL temps réel ?

**Alternatives** :  
A. Filtrer les lignes avec `| where temperature > 85`  
B. Grouper par fenêtre avec `| summarize avg(vibration) by bin(Timestamp, 1m)`  
C. Joindre deux tables KQL avec `| lookup`  
D. Créer une vue matérialisée avec `CREATE MATERIALIZED VIEW`  
E. Mettre à jour une ligne existante avec `UPDATE`

**Solution** :  
✅ **Réponses correctes : A et B**  
*Justification* :  

- **A** : Le filtrage `where` est fondamental en KQL.  
- **B** : L'agrégation par fenêtre (`bin`) est typique du temps réel.  
  ❌ *Pourquoi les autres sont moins adaptés ou impossibles en temps réel pur* :  
- **C** : `lookup` est possible mais coûteux et moins courant en streaming continu.  
- **D** : Les vues matérialisées existent mais sont plus pour l'optimisation que pour le temps réel interactif.  
- **E** : `UPDATE` n'est pas une opération typique en KQL temps réel (les tables KQL sont immuables par ajout).  
  🔗 [Requêtes KQL](https://learn.microsoft.com/fr-fr/kusto/query/)

---

## Question 24

**Nature** : Choix unique

**Énoncé** :  
Vous devez alimenter automatiquement une table d'alertes à partir d'une table d'événements. Quelle conception correspond le mieux ?

**Alternatives** :  
A. Fonction KQL de détection + update policy vers table d'alertes  
B. Copie manuelle des lignes dans Excel  
C. DAX measure qui écrit dans KQL  
D. Stream Analytics + Activator avec déclenchement sur seuil

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Dans Fabric Real-Time Intelligence, l'approche idiomatique est de créer une **function KQL** qui détecte les alertes, et d'utiliser une **update policy** pour écrire les résultats dans une table d'alertes de manière automatique et en continu.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Manuel, non automatisé.  
- **C** : DAX ne peut pas écrire dans KQL.  
- **D** : Stream Analytics + Activator est plus pour des notifications que pour alimenter une table.  
  🔗 [Update policies dans Kusto](https://learn.microsoft.com/fr-fr/kusto/management/update-policy)

---

## Question 25

**Nature** : Tableau à compléter

**Énoncé** :  
Associez chaque besoin temps réel au composant le plus cohérent.

| Besoin                                        | A. Eventstream | B. KQL Database / Eventhouse | C. Real-Time Dashboard |
| --------------------------------------------- | -------------- | ---------------------------- | ---------------------- |
| Recevoir et router les événements entrants    |                |                              |                        |
| Stocker et interroger les événements avec KQL |                |                              |                        |
| Visualiser les indicateurs temps réel         |                |                              |                        |

**Solution** :  
✅ Recevoir et router → **A. Eventstream**  
✅ Stocker et interroger avec KQL → **B. KQL Database / Eventhouse**  
✅ Visualiser les indicateurs temps réel → **C. Real-Time Dashboard**  

🔗 [Composants Real-Time Intelligence](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/overview)

---

## Question 26

**Nature** : Choix unique

**Énoncé** :  
Dans un schéma en étoile, quelle table contient les mesures numériques comme quantité, montant ou marge ?

**Alternatives** :  
A. Table de faits  
B. Table de dimension  
C. Table T-SQL classique  
D. Table d'association

**Solution** :  
✅ **Réponse correcte : A. Table de faits**  
*Justification* : La table de faits contient les mesures quantifiables (faits) et les clés étrangères vers les dimensions. Les dimensions contiennent des attributs descriptifs.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Dimension contient des attributs de regroupement.  
- **C** : Une table T-SQL classique peut être l'un ou l'autre, mais la question porte sur le modèle en étoile.  
- **D** : Table d'association sert généralement pour les relations many-to-many.  
  🔗 [Schéma en étoile](https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema)

---

## Question 27

**Nature** : Choix multiple (2 réponses)

**Énoncé** :  
Quelles caractéristiques correspondent à une dimension historisée en SCD Type 2 ? Sélectionnez deux réponses.

**Alternatives** :  
A. Une colonne indiquant la version courante  
B. Des dates de début et de fin de validité  
C. Une suppression systématique des anciennes versions  
D. Une seule ligne modifiée sans historique  
E. Une mesure DAX obligatoire pour chaque changement

**Solution** :  
✅ **Réponses correctes : A et B**  
*Justification* : Le Type 2 (Slowly Changing Dimension) conserve l'historique en créant une nouvelle ligne pour chaque changement, avec des colonnes `date_debut` et `date_fin` (ou `est_courant`).  
❌ *Pourquoi les autres sont incorrectes* :  

- **C** : On ne supprime pas les versions, on les conserve.  
- **D** : C'est le Type 1.  
- **E** : Aucune mesure DAX n'est obligatoire.  
  🔗 [SCD Type 2](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/slowly-changing-dimensions)

---

## Question 28

**Nature** : Choix unique

**Énoncé** :  
Avant de charger une table de faits, quelle vérification évite des relations invalides avec les dimensions ?

**Alternatives** :  
A. Vérifier que les clés de dimension peuvent être résolues  
B. Vérifier uniquement le nom du rapport  
C. Supprimer toutes les surrogate keys  
D. Écrire les faits uniquement en TXT

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Il faut s'assurer que chaque clé étrangère dans la table de faits existe bien dans la dimension correspondante (intégrité référentielle). Sinon, les relations seront invalides.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Ne concerne pas l'intégrité des données.  
- **C** : Supprimer les clés détruit la relation.  
- **D** : Le format n'est pas pertinent.  
  🔗 [Intégrité référentielle](https://learn.microsoft.com/fr-fr/sql/relational-databases/tables/primary-and-foreign-key-constraints)

---

## Question 29

**Nature** : Choix unique

**Énoncé** :  
Une table Delta contient de nombreux petits fichiers après plusieurs chargements. Quelle action est la plus cohérente avec l'objectif de performance des ateliers ?

**Alternatives** :  
A. Exécuter `OPTIMIZE` sur la table Delta  
B. Augmenter le nombre de partitions avec `REPARTITION`  
C. Changer le format en CSV compressé  
D. Désactiver la journalisation Delta (`_delta_log`)

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : La commande `OPTIMIZE` (ou `OPTIMIZE ... ZORDER BY`) compacte les petits fichiers en fichiers plus gros, ce qui améliore les performances de lecture.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : `REPARTITION` augmente le nombre de partitions, ce qui peut créer encore plus de petits fichiers.  
- **C** : Le CSV compressé n'est pas plus performant pour l'analytique que Delta.  
- **D** : Désactiver le journal Delta supprime l'atomicité et le versioning.  
  🔗 [OPTIMIZE dans Delta Lake](https://learn.microsoft.com/fr-fr/azure/databricks/delta/optimize)

---

## Question 30

**Nature** : Choix unique

**Énoncé** :  
Quelle pratique risque de dégrader fortement le partitionnement d'une table analytique volumineuse ?

**Alternatives** :  
A. Partitionner par identifiant unique  
B. Partitionner par mois lorsque le volume le justifie  
C. Aggréger les données Gold par jour  
D. Contrôler le grain avant jointure

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Partitionner par une colonne à très haute cardinalité (comme un identifiant unique) crée des milliers de partitions, chacune contenant une ou très peu de lignes. Cela détruit les performances. Le partitionnement doit être fait sur une colonne à cardinalité modérée (date, région, etc.).  
❌ *Pourquoi les autres sont correctes* :  

- **B** : Partitionner par mois est une bonne pratique.  
- **C** : Agrégation par jour est un bon choix de grain.  
- **D** : Contrôler le grain est fondamental.  
  🔗 [Partitionnement des tables Delta](https://learn.microsoft.com/fr-fr/azure/databricks/delta/best-practices#partitioning)

---

## Question 31

**Nature** : Drag & Drop textuel / appariement

**Énoncé** :  
Associez chaque concept à sa définition.

| Concept           | Definition                                               |
| ----------------- | -------------------------------------------------------- |
| 1. Table de faits | A. Clé technique stable pour relier faits et dimensions  |
| 2. Dimension      | B. Table contenant les mesures et événements analysables |
| 3. Surrogate key  | C. Axe d'analyse comme client, produit ou date           |
| 4. SCD Type 2     | D. Technique d'historisation des changements             |

**Solution** :  
✅ 1 → **B**  
✅ 2 → **C**  
✅ 3 → **A**  
✅ 4 → **D**  

🔗 [Glossaire du modèle de données](https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema)

---

## Question 32

**Nature** : Choix unique

**Énoncé** :  
Dans un warehouse Fabric, une table `Sales` contient les colonnes `Amount` (montant vendu) et `TargetAmount` (objectif). Vous devez créer une vue `SalesRates` qui affiche le taux d'atteinte par vendeur. Quelle définition est correcte ?

**Alternatives** :  
A. `SELECT SellerId, Amount / TargetAmount AS AchievementRate FROM Sales`  
B. `SELECT SellerId, Amount * TargetAmount AS AchievementRate FROM Sales`  
C. `SELECT SellerId, Amount / COUNT(*) AS AchievementRate FROM Sales`  
D. `SELECT SellerId, TargetAmount / Amount AS AchievementRate FROM Sales`

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Le taux d'atteinte est (réalisé / objectif), soit `Amount / TargetAmount`.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Multiplication donne un produit, pas un taux.  
- **C** : Division par le nombre de lignes n'a pas de sens.  
- **D** : Inverse le ratio (objectif/réalisé).  
  🔗 [Syntaxe SQL de base](https://learn.microsoft.com/fr-fr/sql/t-sql/functions/mathematical-functions)

---

## Question 33

**Nature** : Choix unique

**Énoncé** :  
Quel mécanisme limite précisément les lignes visibles dans une table selon l'utilisateur ou son périmètre ?

**Alternatives** :  
A. Row-Level Security  
B. Deny sur la ressource  
C. Object-Level Security  
D. Les rôles de Workspace

**Solution** :  
✅ **Réponse correcte : A. Row-Level Security (RLS)**  
*Justification* : La RLS restreint l'accès au niveau des lignes d'une table en fonction des privilèges de l'utilisateur (par exemple, un vendeur ne voit que ses propres ventes).  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Deny est une permission générale, pas limitée aux lignes.  
- **C** : Object-Level Security limite l'accès aux objets (table, colonne).  
- **D** : Les rôles de workspace gèrent l'accès au niveau du workspace, pas au sein des tables.  
  🔗 [Row-Level Security dans Fabric](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/row-level-security)

---

## Question 34

**Nature** : Choix unique

**Énoncé** :  
Quel mécanisme permet de refuser la lecture d'une colonne sensible comme email ou marge interne ?

**Alternatives** :  
A. Column-Level Security / permissions colonne  
B. Eventstream routing  
C. Spark partitionBy uniquement  
D. Power BI theme

**Solution** :  
✅ **Réponse correcte : A. Column-Level Security**  
*Justification* : La sécurité au niveau des colonnes permet d'accorder ou de refuser l'accès à des colonnes spécifiques d'une table, indépendamment du reste.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Eventstream route des événements.  
- **C** : `partitionBy` est une optimisation physique.  
- **D** : Power BI theme concerne l'apparence.  
  🔗 [Column-Level Security](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/column-level-security)

---

## Question 35

**Nature** : Choix multiple (3 réponses attendues)

**Énoncé** :  
Sélectionnez trois réponses parmi celles qui sont **gérées directement par Fabric au niveau applicatif** (hors chiffrement infrastructure).

**Alternatives** :  
A. Rôles workspace  
B. Permissions SQL sur Warehouse  
C. RLS dans le modèle sémantique Power BI  
D. Sécurité au niveau des colonnes (column masking) dans le Lakehouse  
E. Mise en cache des requêtes

**Solution** :  
✅ **Réponses correctes : A, B, C**  
*Justification* : Fabric gère nativement les rôles workspace (A), les permissions SQL sur Warehouse (B), et la RLS dans les modèles Power BI (C). La sécurité au niveau des colonnes dans le Lakehouse (D) n'est pas encore totalement équivalente à celle du Warehouse. La mise en cache (E) n'est pas un mécanisme de sécurité.  
🔗 [Sécurité dans Fabric](https://learn.microsoft.com/fr-fr/fabric/security/security-overview)

---

## Question 36

**Nature** : Choix unique

**Énoncé** :  
Un utilisateur dispose d'un accès au workspace mais reçoit un `DENY SELECT` explicite sur une colonne sensible dans le Warehouse. Quel comportement est attendu ?

**Alternatives** :  
A. La colonne refusée ne doit pas être lisible par cet utilisateur  
B. Le refus supprime physiquement la colonne  
C. Le refus crée une table Gold  
D. Le refus lance un pipeline

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Un `DENY SELECT` sur une colonne empêche l'utilisateur (même avec d'autres permissions) de lire cette colonne. C'est une sécurité explicite.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Aucune suppression physique.  
- **C** / **D** : Non lié.  
  🔗 [DENY (Transact-SQL)](https://learn.microsoft.com/fr-fr/sql/t-sql/statements/deny-transact-sql)

---

## Question 37

**Nature** : Choix unique

**Énoncé** :  
Dans Microsoft Fabric, un data engineer doit donner à une équipe marketing l'accès en **lecture seule** à une table spécifique du Warehouse, sans leur permettre de voir les autres tables du même schéma. Comment procéder ?

**Alternatives** :  
A. Ajouter les utilisateurs au rôle **Viewer** du workspace, puis créer une vue sur la table cible et leur accorder **SELECT** sur cette vue uniquement  
B. Ajouter les utilisateurs au rôle **Contributor** du workspace, la RLS fera le reste  
C. Ajouter les utilisateurs au rôle **Admin** du workspace, puis masquer les autres tables par interface  
D. Ajouter les utilisateurs au rôle **Viewer** du workspace, puis leur accorder **SELECT** sur toutes les tables du Warehouse

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Le rôle Viewer donne un accès minimal au workspace (voir les éléments). Ensuite, on peut créer une vue ne couvrant que la table souhaitée et accorder `SELECT` sur cette vue. Les autres tables ne sont pas accessibles car les droits ne sont pas octroyés.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Contributor a trop de droits (modification).  
- **C** : Admin est encore plus permissif.  
- **D** : Select sur toutes les tables n'est pas restreint.  
  🔗 [Permissions sur les objets Warehouse](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/security)

---

## Question 38

**Nature** : Choix unique

**Énoncé** :  
Un utilisateur a le rôle **Contributor** sur un workspace Fabric. Il souhaite donner l'accès en lecture seule à un rapport Power BI à un collègue externe. Peut-il le faire ?

**Alternatives** :  
A. Oui, directement via le partage du rapport  
B. Oui, en ajoutant le collègue comme **Viewer** du workspace  
C. Non, seul un **Admin** du workspace peut partager un rapport  
D. Non, les utilisateurs externes ne peuvent jamais accéder à Fabric

**Solution** :  
✅ **Réponse correcte : C**  
*Justification* : Dans Fabric, la permission de partager des éléments (comme un rapport Power BI) est réservée aux **membres du rôle Admin** du workspace. Les Contributor et Viewer ne peuvent pas partager. Les utilisateurs externes peuvent accéder via B2B si configuré.  
❌ *Pourquoi les autres sont incorrectes* :  

- **A / B** : Contributor ne peut pas partager.  
- **D** : Les externes peuvent accéder (Azure AD B2B).  
  🔗 [Rôles de workspace Fabric](https://learn.microsoft.com/fr-fr/fabric/get-started/workspace-roles)

---

## Question 39

**Nature** : Choix unique

**Énoncé** :  
Un data engineer applique une **RLS (Row Level Security)** sur une table Warehouse. Les utilisateurs avec le rôle **Viewer** du workspace ne voient aucune donnée. Quelle est la cause probable ?

**Alternatives** :  
A. La RLS bloque par défaut tout accès sans règle explicite  
B. Les Viewers n'ont jamais accès aux données Warehouse  
C. Il faut obligatoirement le rôle **Admin** avec RLS  
D. La RLS désactive automatiquement le workspace

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Par défaut, si vous appliquez une RLS sans définir de prédicat qui autorise l'accès pour ces utilisateurs (ou si aucun utilisateur n'est mappé à une fonction de sécurité), la règle par défaut est de ne montrer aucune ligne. Il faut explicitement créer une politique qui retourne TRUE pour certains utilisateurs.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Les Viewers peuvent voir les données si aucune RLS restrictive n'est appliquée.  
- **C** : Admin n'est pas nécessaire ; on peut attribuer des rôles RLS à des Viewers.  
- **D** : La RLS n'affecte pas l'existence du workspace.  
  🔗 [Fonctionnement de la RLS](https://learn.microsoft.com/fr-fr/sql/relational-databases/security/row-level-security)

---

## Question 40

**Nature** : Choix unique

**Énoncé** :  
Une entreprise veut qu'un prestataire externe puisse **lire** les données d'une table Lakehouse, mais pas les **modifier**. Quel rôle workspace minimum + quelle permission SQL sont nécessaires ?

**Alternatives** :  
A. **Viewer** + permission **SELECT** sur la table  
B. **Contributor** + permission **INSERT** sur la table  
C. **Admin** + aucune permission SQL  
D. **Viewer** + permission **UPDATE** sur la table

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Le rôle **Viewer** donne un accès en lecture aux métadonnées du workspace. Ensuite, il faut accorder explicitement la permission **SELECT** sur la table en question (dans le Lakehouse via le SQL Analytics Endpoint ou via les permissions Spark).  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Contributor permet déjà trop (modification).  
- **C** : Admin donne tous les droits.  
- **D** : UPDATE permet la modification.  
  🔗 [Permissions Lakehouse](https://learn.microsoft.com/fr-fr/fabric/data-engineering/lakehouse-security)

---

## Question 41

**Nature** : Tableau à compléter

**Énoncé** :  
Associez chaque besoin de gouvernance au mécanisme le plus cohérent.

| Besoin                                                    | A. Rôle workspace | B. Permission SQL | C. Sécurité sémantique (modèle Power BI) |
| --------------------------------------------------------- | ----------------- | ----------------- | ---------------------------------------- |
| Contrôler qui administre ou contribue dans le workspace   |                   |                   |                                          |
| Contrôler l'accès à une table ou colonne Warehouse        |                   |                   |                                          |
| Contrôler l'expérience de lecture dans le modèle Power BI |                   |                   |                                          |

**Solution** :  
✅ Contrôle administration workspace → **A. Rôle workspace**  
✅ Contrôle accès table/colonne Warehouse → **B. Permission SQL**  
✅ Contrôle expérience lecture Power BI → **C. Sécurité sémantique** (RLS/OLS dans le modèle)  

🔗 [Sécurité dans Fabric](https://learn.microsoft.com/fr-fr/fabric/security/security-overview)

---

## Question 42

**Nature** : Choix unique

**Énoncé** :  
Une entreprise reçoit quotidiennement 50 fichiers CSV dans un Lakehouse Bronze. Un pipeline doit :

1. Lire les fichiers
2. Nettoyer les données (supprimer les lignes nulles)
3. Appliquer une RLS (Row Level Security)
4. Écrire en table Delta Silver

Quelle combinaison d'outils Fabric est la plus adaptée ?

**Alternatives** :  
A. Dataflow Gen2 (nettoyage) → Warehouse (RLS) → Table Silver  
B. Pipeline + activité Copy Data (lecture) → Notebook PySpark (nettoyage + RLS + écriture Silver)  
C. KQL Database (lecture) → Eventhouse (nettoyage) → Power BI (RLS)  
D. Git (versioning) → Lakehouse (stockage) → RLS (automatique)

**Solution** :  
✅ **Réponse correcte : B**  
*Justification* : Un pipeline peut orchestrer la lecture (Copy Data) puis un notebook PySpark pour effectuer le nettoyage, la logique métier, l'application de la RLS (via des transformations conditionnelles) et l'écriture en Delta Silver. C'est la combinaison la plus flexible et performante.  
❌ *Pourquoi les autres sont incorrectes* :  

- **A** : Dataflow Gen2 peut nettoyer, mais la RLS au niveau Warehouse n'est pas la bonne couche pour une table Silver dans un Lakehouse.  
- **C** : KQL/Eventhouse n'est pas adapté au nettoyage batch de CSV.  
- **D** : Git ne traite pas les données.  
  🔗 [Scénario d'ingestion avec pipeline et notebook](https://learn.microsoft.com/fr-fr/fabric/data-engineering/ingest-data-with-notebooks)

---

## Question 43

**Nature** : Choix unique

**Énoncé** :  
Un rapport Power BI affiche des résultats incohérents après une jointure Silver. Quelle vérification technique est prioritaire ?

**Alternatives** :  
A. Vérifier si la jointure est établie entre les deux entités dans le modèle sémantique  
B. Vérifier si les clés de jointure appliquent les règles et les contraintes nécessaires  
C. Vérifier si la table Silver a été correctement actualisée (rafraîchie)  
D. Vérifier si le modèle sémantique Power BI a été redéployé après la jointure

**Solution** :  
✅ **Réponse correcte : B**  
*Justification* : L'incohérence vient souvent de clés non uniques (comme à la question 5) ou de relations mal définies. Il faut donc d'abord vérifier l'intégrité et l'unicité des clés de jointure en amont, dans la table Silver.  
❌ *Pourquoi les autres sont moins prioritaires* :  

- **A** : Le modèle sémantique peut bien avoir la jointure, mais si les données sous-jacentes ont des problèmes de clés, le résultat sera faux.  
- **C** : L'actualisation est importante, mais l'incohérence structurelle est plus probable.  
- **D** : Le redéploiement n'affecte pas l'incohérence des données.  
  🔗 [Problèmes courants de jointure](https://learn.microsoft.com/fr-fr/power-bi/guidance/relationships-common-issues)

---

## Question 44

**Nature** : Choix unique

**Énoncé** :  
Vous devez choisir entre Dataflow Gen2 et Notebook Spark. Le traitement demande beaucoup de logique et une complexité de transformation estimée potentiellement importante, contrôles qualité avancés et écriture Delta. Quel choix est le plus cohérent ?

**Alternatives** :  
A. Notebook PySpark  
B. Dataflow Gen2  
C. Notebook Spark SQL  
D. Pipeline

**Solution** :  
✅ **Réponse correcte : A. Notebook PySpark**  
*Justification* : Pour des transformations complexes, de la logique avancée et des contrôles qualité, un notebook PySpark (langage Python) offre une flexibilité maximale (bibliothèques, code modulaire, tests). Dataflow Gen2 est plus low-code, moins adapté à la complexité.  
❌ *Pourquoi les autres sont incorrects* :  

- **B** : Dataflow Gen2 est plus limité.  
- **C** : Spark SQL est moins flexible que PySpark.  
- **D** : Pipeline est un orchestrateur, pas un outil de transformation.  
  🔗 [Notebook vs Dataflow](https://learn.microsoft.com/fr-fr/fabric/data-engineering/choose-dataflow-notebook)

---

## Question 45

**Nature** : Choix unique

**Énoncé** :  
Un pipeline charge des données Gold alors que les tables Silver ne sont pas encore disponibles. Quelle correction d'architecture est la plus appropriée ?

**Alternatives** :  
A. Ajouter une orchestration séquentielle avec dépendances et éventuellement Wait  
B. Exécuter Gold avant Bronze systématiquement  
C. Supprimer la couche Silver  
D. Remplacer toutes les tables par des fichiers CSV au lieu de TXT

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : Il faut orchestrer le pipeline pour que l'étape Gold dépende explicitement de la réussite de l'étape Silver (par exemple via l'activité "If Condition" ou "Wait" dans un pipeline). On peut aussi chaîner les activités avec les propriétés de dépendance.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : L'ordre doit être Bronze → Silver → Gold.  
- **C** : Supprimer Silver rompt l'architecture.  
- **D** : Le format n'est pas le problème.  
  🔗 [Dépendances dans les pipelines](https://learn.microsoft.com/fr-fr/azure/data-factory/concepts-pipeline-execution-triggers#activity-dependencies)

---

## Question 46

**Nature** : Choix multiple (2 réponses)

**Énoncé** :  
Quels éléments peuvent réduire le risque de doublons dans un chargement incrémental ? Sélectionnez deux réponses.

**Alternatives** :  
A. Utiliser une clé métier dans une logique `MERGE` ou `INSERT...ON CONFLICT`  
B. Vérifier l'existence de chaque ligne dans la table cible avant insertion (lookup)  
C. Ajouter une contrainte d'unicité composite sur les colonnes clés dans la table Delta  
D. Appliquer une fenêtre de déduplication (`ROW_NUMBER() OVER(PARTITION BY key ORDER BY timestamp)`) dans le notebook  
E. Charger les données brutes en `append` puis supprimer les doublons périodiquement par batch dédié

**Solution** :  
✅ **Réponses correctes : A et D**  
*Justification* :  

- **A** : Le `MERGE` (ou `INSERT ON CONFLICT`) est la méthode standard pour éviter les doublons en insertion/upsert.  
- **D** : Utiliser `ROW_NUMBER()` avec partitionnement par clé métier et fenêtre temporelle permet de ne garder que la ligne la plus récente, éliminant les doublons dans le flux lui-même.  
  ❌ *Pourquoi les autres sont moins efficaces* :  
- **B** : Le lookup ligne par ligne est très inefficace.  
- **C** : Les contraintes d'unicité ne sont pas totalement supportées dans Delta Lake standard (vérification à l'écriture, mais pas garantie en concurrence).  
- **E** : Supprimer les doublons après coup est plus lourd et n'empêche pas le stockage des doublons.  
  🔗 [Déduplication dans Delta Lake](https://learn.microsoft.com/fr-fr/azure/databricks/delta/merge#upsert-into-a-table-using-merge)

---

## Question 47

**Nature** : Choix unique

**Énoncé** :  
Vous devez expliquer pourquoi la couche Gold ne doit pas remplacer Bronze et Silver. Quelle justification est la plus directe ?

**Alternatives** :  
A. Gold sert à l'analyse agrégée (vue métier), tandis que Bronze conserve le brut immuable et Silver prépare les données nettoyées et validées  
B. Remplacer Bronze et Silver par Gold empêcherait toute reprise du pipeline en cas d'erreur de transformation ou de changement de règle métier  
C. Gold est souvent trop agrégé et perd le grain fin nécessaire pour recalculer des indicateurs différemment ultérieurement  
D. La séparation Bronze/Silver/Gold permet d'isoler les problèmes : ingestion (Bronze), qualité (Silver), business (Gold)

**Solution** :  
✅ **Réponse correcte : B** (considérée comme la plus directe, bien que plusieurs soient valables)  
*Justification* : Si vous supprimez Bronze et Silver, vous perdez la possibilité de **rejouer** le pipeline à partir des données brutes. En cas d'erreur dans la transformation Gold ou de changement de règles métier, vous ne pourriez pas reconstruire les données sans re-ingérer les sources. Bronze est l'archive immuable indispensable à la reproductibilité.  
❌ *Pourquoi les autres sont également justes mais moins directes* :  

- **A** : Décrit les rôles mais n'insiste pas sur la reproductibilité.  
- **C** : Gold agrégée perd le grain fin, mais on pourrait avoir Gold fine.  
- **D** : L'isolation des problèmes est un bénéfice, mais la justification la plus directe pour ne **pas remplacer** Bronze et Silver est la reproductibilité.  
  🔗 [Bénéfices de l'architecture Medallion](https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture#why-are-bronze-and-silver-important)

---

## Question 48

**Nature** : Choix unique

**Énoncé** :  
Un analyste demande pourquoi les dimensions et table de fait sont préférables à une seule grande table plate pour le reporting Warehouse. Quelle réponse est la plus pertinente ?

**Alternatives** :  
A. Elles structurent les axes d'analyse (temps, produit, client, etc.) et évitent la redondance des attributs descriptifs dans chaque ligne de fait  
B. Elles permettent de modifier un attribut (ex: nom de produit) en un seul endroit, sans réécrire des millions de lignes de faits  
C. Elles réduisent la taille du modèle et améliorent les performances des requêtes d'agrégation par rapport à une table plate géante  
D. Elles autorisent les jointures implicites dans les outils de reporting (Power BI, Tableau) et simplifient la navigation pour l'utilisateur métier

**Solution** :  
✅ **Réponse correcte : A** (la plus fondamentale)  
*Justification* : Le schéma en étoile évite la redondance des attributs dimensionnels dans chaque ligne de fait. Cela économise de l'espace et simplifie la maintenance. B, C et D sont également vrais, mais A est la raison principale du point de vue de la modélisation. En contexte d'examen, on peut considérer A comme la plus directement liée à la question.  
🔗 [Avantages du schéma en étoile](https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema#benefits-of-a-star-schema)

---

## Question 49

**Nature** : Choix multiple (plusieurs réponses possibles)

**Énoncé** :  
Dans un atelier Microsoft Fabric, trois erreurs fréquentes peuvent dégrader fortement la qualité des données et les performances. Lesquelles ?

**Alternatives** :  
A. Faire un append incrémental sans clé métier ni logique de dédoublonnage  
B. Joindre deux tables avec des granularités incompatibles  
C. Lire uniquement la première ligne d'un fichier (`first row only`) alors que plusieurs lignes seuils doivent être traitées  
D. Exécuter `OPTIMIZE` après chaque petite insertion (moins de 1 000 lignes)  
E. Appliquer une RLS (Row Level Security) directement dans le Lakehouse sans vue ni Warehouse  
F. Partitionner une table par une colonne à très haute cardinalité (ex : identifiant unique)

**Solution** :  
✅ **Réponses correctes : A, B, F**  
*Justification* :  

- **A** : Append sans déduplication crée des doublons → dégrade qualité.  
- **B** : Jointure de granularités différentes (ex: quotidien vs mensuel) produit des résultats mathématiquement faux → dégrade qualité.  
- **F** : Partitionnement par haute cardinalité crée trop de petits fichiers → dégrade performances.  

❌ *Pourquoi les autres sont moins critiques ou incorrectes* :  

- **C** : Lire première ligne est parfois voulu (ex: pour des métadonnées), ce n'est pas une erreur fréquente généralisée.  
- **D** : OPTIMIZE après petite insertion est inutile mais pas très pénalisant.  
- **E** : La RLS peut s'appliquer dans le Lakehouse via le endpoint SQL, ce n'est pas une erreur.  
  🔗 [Bonnes pratiques Delta Lake](https://learn.microsoft.com/fr-fr/azure/databricks/delta/best-practices)

---

## Question 50

**Nature** : Choix unique

**Énoncé** :  
Une entreprise doit traiter des données IoT (50 000 événements/seconde), produire des alertes en moins de 5 secondes, et conserver tous les événements bruts pour rejeu futur. Elle doit aussi exposer des KPI métier sur les 3 derniers mois à un dashboard Power BI.  
Quelle architecture Fabric est la plus adaptée ?

**Alternatives** :  
A. Eventhouse (ingestion KQL) → KQL Function de détection → Update policy vers table d'alertes → Activator (notification) → Lakehouse pour archivage brut  
B. Eventhouse (ingestion KQL) → Pipeline avec activité Notebook → Table Delta Bronze → Stream Analytics → Power BI  
C. Lakehouse (stockage brut) → Pipeline avec Dataflow Gen2 → Silver → Gold → Power BI Direct Lake → RLS  
D. KQL Database → Eventstream → Materialized view → Warehouse → Power BI import mode

**Solution** :  
✅ **Réponse correcte : A**  
*Justification* : L'Eventhouse est conçu pour l'ingestion haut débit (50k événements/s). Les fonctions KQL et update policies permettent des alertes en temps réel très rapides (<5s). L'archivage brut peut se faire vers un Lakehouse via l'Eventhouse (rétention ou export). Power BI peut se connecter en Direct Lake à l'Eventhouse pour les KPI. C'est l'architecture Real-Time Intelligence typique.  
❌ *Pourquoi les autres sont incorrectes* :  

- **B** : Pipeline avec notebook introduit une latence trop élevée.  
- **C** : Lakehouse brut n'est pas adapté à l'ingestion temps réel haute fréquence.  
- **D** : KQL Database + Eventstream + Warehouse + Import mode est complexe et moins performant.  
  🔗 [Architecture temps réel Fabric](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/overview#scenarios)
