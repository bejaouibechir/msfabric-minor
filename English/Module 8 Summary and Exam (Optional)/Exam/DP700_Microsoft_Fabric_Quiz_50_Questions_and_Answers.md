# DP-700 Microsoft Fabric Quiz — 50 Questions and Answers

## Question 1

**Nature** : Choix unique

**Stated**:  
You must store the initial files and data without any business correction to ensure traceability. What layer should you use?

**Alternatives** :  
A. Bronze  
B. Silver  
C. Gold  
D. Copper

**Solution** :  
A. Bronze**  
*Justification*: The Bronze layer retains raw data, exactly as ingested, without any transformation. It is the foundation of the Medallion architecture that guarantees reproducibility and traceability.  
*Why others are wrong*:  

- **B. Silver**: contains cleaned and validated data, not raw.  
- **C. Gold**: contains aggregated data, ready for analysis.  
- **D. Copper**: is not a standard layer of Medallion architecture.  
  🔗 [Documentation Medallion](https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture)

---

##Question 2

**Nature**: Multiple choice (2 expected answers)

**Stated**:  
Which operations ** do not primarily belong to the Silver layer? Select two answers.

**Alternatives** :  
A. Deducting consumption lines  
B. Correct types and filter invalid values  
C. Aggregating data  
D. Delete source data after ingestion  
E. Modelling as a star scheme

**Solution** :  
* Correct answers: C and E**  
*Justification* :  

- **C. Aggregate data**: falls under the Gold layer (pre-agreed data for the trade).  
- **E. Model as a star scheme**: also part of the Gold layer or semantic model.  
  *Why other options belong to Silver*:  
- **A** and **B** are typical cleaning/validation actions (Silver).  
- **D** (delete sources) is not recommended at all, but it is not a Silver function.  
  🔗 https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture#what-is-medallion-architecture

---

## Question 3

**Nature**: Table to be completed (multiple choice grid - associated)

**Stated**:  
Match each need to the most appropriate layer.  

| Besoin                                          | A. Bronze | B. Silver | C. Gold |
| ----------------------------------------------- | --------- | --------- | ------- |
| Keep data close to the crude           |           |           |         |
| Produce a clean and enriched table         |           |           |         |
| Provide daily KPI ready for Power BI |           |           |         |

**Solution** :  
Keep data close to the crude → **A. Bronze**  
Produce a clean and enriched table → **B. Silver**  
的 Provide daily KPI ready for Power BI → **C. Gold**  

*Justification*: See standard definitions of the Medallion architecture.  
🔗 [Documentation couches](https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture)

---

## Question 4

**Nature** : Choix unique

**Stated**:  
You have a Fabric pipeline that loads raw data into a Bronze table, then cleans it in a Silver table. You want to create a Gold table aggregated by **site and per day**.  
What is the most flexible ** method** to implement this transformation?

**Alternatives** :  
A. Use an activity **Dataflow Gen2** (visual interface)  
B. Use a **Notebook Spark** with DataFrames  
C. Make aggregations in Power BI Desktop before publishing  
D. Using a standard SQL view** in the Warehouse

**Solution** :  
* Correct answer: B. Spark Notebook**  
*Justification*: The PySpark notebook allows complex logic, testing, external libraries, and fine performance management (partitioning, optimization). This is the most flexible solution for evolutionary transformations.  
*Why others are wrong*:  

- **A**: Dataflow Gen2 is more limited in advanced logic.  
- **C**: Deporting aggregation in Power BI is a bad practice (non-mutualized, non-reusable computing load).  
- **D**: SQL view lacks flexibility for complex transformations and can suffer from performance on large volumes.  
  🔗 [Notebooks Fabric](https://learn.microsoft.com/fr-fr/fabric/data-engineering/author-notebook)

---

## Question 5

**Nature** : Choix unique

**Stated**:  
You have a joint between the DimCustomer table and the FactSales table which leads to a very large number of rows. What cause is most likely?

**Alternatives** :  
A. The join column on the DimCustomer side does not impose the single value constraint  
B. Because you use a Left joint  
C. Because you use a Right Joint  
D. Because you use an Inner joint

**Solution** :  
**Response correct: A**  
*Justification*: If the join column in the dimension is not unique, each line in the table of facts joins several lines of the dimension, multiplying the number of lines (partial Cartesian product).  
*Why others are wrong*:  

- **B / C / D** : The types of join (Left, Right, Inner) do not create a default multiplication; Only a key not unique in the dimension causes this problem.  
  [Relations in Power BI]](https://learn.microsoft.com/fr-fr/power-bi/guidance/relationships)

---

## Question 6

**Nature** : Choix unique

**Stated**:  
At the pipeline level, you must dynamically list the files in a folder before browsing them. What activity should you use to prepare the ground?

**Alternatives** :  
A. Get Metadata  
B. Set Variable  
C. ForEach  
D. Execute Pipeline

**Solution** :  
A. Get Metadata**  
*Justification*: Get Metadata allows you to retrieve the list of files (childItems) from a folder. It is essential for any dynamic loop.  
*Why others are wrong*:  

- **B**: Set Variable does not read metadata.  
- **C** : ForEach itère on an already existing list.  
- **D**: Execute Pipeline runs another pipeline.  
  [Get Metadata Activity](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-get-metadata-activity)

---

## Question 7

**Nature** : Choix unique

**Stated**:  
You must apply the same copy logic to each file returned by the metadata activity. What activity should you use?

**Alternatives** :  
A. If Condition  
B. ForEach  
C. Until  
D. Do-Until

**Solution** :  
* Correct answer: B. ForEach**  
*Justification*: ForEach is the native activity to iterate on a collection (file list) and perform one or more activities for each item.  
*Why others are wrong*:  

- **A** : If Condition is used to connect according to a condition, not to be closed.  
- **C / D** : Until/Do-Until are conditional loops, but not suitable for a fixed list.  
  (ForEach Activity)](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-for-each-activity)

---

## Question 8

**Nature** : Drag & Drop textuel / appariement

**Stated**:  
Associate each pipeline activity with its role.

| Activity            | Role                                            |
| ------------------- | ----------------------------------------------- |
| 1. Lookup           | A. Run a child pipeline                  |
| 2. If Condition     | B. Read the first line                       |
| 3. Until            | C. Choosing a branch according to an expression     |
| 4. Execute Pipeline | D. Repeat until a condition is satisfied |

**Solution** :  
  
✅ 2 → **C** (If Condition branche selon expression)  
3 → **D** (Until repeats until true condition)  
4 → **A** (Execute Pipeline runs a child pipeline)  

*Justification* : cf. documentation Azure Data Factory / Fabric pipelines.  
[Flux control activities](https://learn.microsoft.com/fr-fr/azure/data-factory/concepts-pipelines-activities)

---

## Question 9

**Nature** : Choix unique

**Stated**:  
An activity **Lookup** questions a threshold table containing **4 lines**. By default (without changing parameters), how many rows does this activity return?

**Alternatives** :  
A. 0 line (error)  
B. 1 line (first line only)  
C. 4 lines (all lines)  
D. Depends on the type of connection used

**Solution** :  
* Correct answer: B. 1 line**  
*Justification*: By default, Lookup activity returns only the **first line** of the result set, unless you change the property`firstRowOnly`False.  
*Why others are wrong*:  

- **C** : Need to disable`firstRowOnly`.  
- **A** : There is no error, the first line is returned.  
  [Activity Lookup]](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-lookup-activity)

---

## Question 10

**Nature** : Choix unique

**Stated**:  
After copying the active infrastructure since activity **CopyInfrastructureActive**, the pipeline must continue only if`rowsCopied`is greater than zero. What is the most coherent expression?

**Alternatives** :  
A. `@greater(activity('CopierInfrastructuresActives').output.rowsCopied, 0)`  
B. `@equals(variables('NombreIterations'), 'Gold')`  
C. `@contains(triggerBody().fileName, '.pbix')`  
D. `@less(activity('CopierInfrastructuresActives').output.rowsCopied, 0)`

**Solution** :  
**Response correct: A**  
*Justification* : L'expression `greater(..., 0)`is the correct syntax to test if the number of lines copied is strictly positive.  
*Why others are wrong*:  

- **B**: Compares a variable to an irrelevant string.  
- **C**: Test the presence of an extension in a trigger.  
- **D**: Test the inferiority, the opposite of what is required.  
  🔗 [Fonctions d'expression](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-expression-language-functions)

---

## Question 11

**Nature**: Multiple choice (2 expected answers)

**Stated**:  
In Microsoft Fabric, among the following elements, **two** are real** pipeline native activities** commonly used for end-to-end orchestration. Select the two correct answers.

**Alternatives** :  
A. Execute Pipeline  
B. Wait  
C. KQL summarize  
D. DAX CALCULATE  
E. Power BI bookmark

**Solution** :  
A and B**  
*Justification* :  

- **Execute Pipeline** is a native activity to call another pipeline.  
- **Wait** is a native activity to introduce a break.  
  *Others are not pipeline operations*:  
- **C** : `KQL summarize`is a KQL instruction, not an activity.  
- **D** : `DAX CALCULATE`is a DAX function in Power BI.  
- **E** : `Power BI bookmark`is a Power BI interface element.  
  ](https://learn.microsoft.com/fr-fr/fabric/data-factory/pipeline-activities)

---

## Question 12

**Nature** : Choix unique

**Stated**:  
In a Fabric pipeline orchestrating Bronze, Silver and Gold layers, you have to perform several processing activities on the Silver layer. However, these transformations should only start if the Bronze ingestion has been successfully completed without error.  
What pipeline activity do you use to implement this condition?

**Alternatives** :  
A. Execute Pipeline  
B. If Condition  
C. When Condition  
D. Filter

**Solution** :  
**Response correct: B. If Condition**  
*Justification*: The **If Condition** activity can only run a block of activities if a Boolean expression (e.g. verification of success of the previous activity) is true. This is the standard tool for conditional branching.  
*Why others are wrong*:  

- **A** : Execute Pipeline does not condition, it executes.  
- **C** : When Condition does not exist as a standard activity (it is a condition in triggers).  
- **D**: Filter is used to filter a list, not to condition execution.  
  [Activity If Condition](https://learn.microsoft.com/fr-fr/azure/data-factory/control-flow-if-condition-activity)

---

## Question 13

**Nature** : Choix unique

**Stated**:  
A Microsoft Fabric pipeline is triggered automatically upon the arrival of a **new file** in a source folder (evental trigger). In the notebook called by this pipeline, the developer incorrectly coded the script to cause a reading of **the whole source folder** at each trigger, instead of using only the path of the file received by the trigger.  
What result?

**Alternatives** :  
A. Files already processed can be duplicated  
B. Event trigger stops running after first run  
C. Notebook performance decreases, but no data is duplicated  
D. The pipeline automatically ignores files already read through Spark checkpointing

**Solution** :  
**Response correct: A**  
*Justification*: If the notebook rereads the entire folder at each trigger without deduplication logic (MERGE, upsert), the already processed files will be read and their data inserted again, creating duplicates.  
*Why others are wrong*:  

- **B** : The trigger continues to work, it is not a trigger problem.  
- **C** : There is a risk of duplication, not just performance.  
- **D** : Spark checkpointing does not automatically apply to raw file playback.  
  [Good incremental ingestion practices](https://learn.microsoft.com/fr-fr/fabric/data-engineering/incremental-refresh)

---

## Question 14

**Nature**: Multiple choice (several possible answers)

**Stated**:  
You need to harmonize several energy files with an up-to-date low-code interface before loading the result. Which tool is the most suitable?

**Alternatives** :  
A. Dataflow Gen2  
B. Warehouse with T-SQL  
C. Lakehouse with shortcuts  
D. Dataflow Gen1  
E. Pipeline

**Solution** :  
A. Dataflow Gen2**  
*Justification*: Dataflow Gen2 is the modern low-code tool for ingestion, processing and loading (ETL) in Fabric. It offers a rich visual interface and is designed to harmonize various sources.  
*Why others are less suitable*:  

- **B** : T-SQL is not low code.  
- **C** : Lakehouse is a storage, not a low-code transformation tool.  
- **D**: Dataflow Gen1 is depreciated for Gen2.  
- **E** : An orchestra pipeline but does not natively transform into low-code.  
  [Dataflow Gen2 in Fabric](https://learn.microsoft.com/fr-fr/fabric/data-factory/dataflow-gen2-overview)

---

## Question 15

**Nature**: Multiple choice (several possible answers)

**Stated**:  
In Microsoft Fabric, you need to calculate the carbon footprint from CSV files (volumes) and a SQL table (emission factors) residing in a different Lakehouse. You want a unique result **without physical copy of the data**. What two techniques do you combine?

**Alternatives** :  
A. Shortcut to CSV + Shortcut files to the SQL table of the other Lakehouse  
B. Dataflow Gen2 with direct link to both sources  
C. Lakehouse with Spark view using shortcuts  
D. Warehouse with SQL view using shortcuts  
E. Pipeline with Copy Data activity and merger

**Solution** :  
A and C**  
*Justification* :  

- **A**: Shortcuts allow access to data without copying it.  
- **C** : A Spark view (or notebook) can then read through these shortcuts and attach the data.  
  *Why others are incorrect for lack of copy*:  
- **B** : Dataflow Gen2 can link directly, but it can materialize data. Nevertheless, the A+C association is more native.  
- **D** : Warehouse with SQL view does not natively read CSV files via shortcut without prior copy.  
- **E**: Copy Data makes a physical copy.  
  [Shortcuts in OneLake]](https://learn.microsoft.com/fr-fr/fabric/onelake/onelake-shortcuts)

---

## Question 16

**Nature** : Choix unique

**Stated**:  
A notebook must rewrite a Delta Silver table after cleaning. Which instruction is most consistent?

**Alternatives** :  
A.`df.write.format("delta").mode("overwrite").saveAsTable("silver.table")`  
B. `df.to_excel("silver.table")`  
C. `CREATE EVENTSTREAM silver.table`  
D. `git merge silver.table`

**Solution** :  
**Response correct: A**  
*Justification*: In PySpark, writing a Delta DataFrame table is done with`write.format("delta").mode("overwrite").saveAsTable(...)`, which makes it possible to completely replace the Silver table.  
*Why others are wrong*:  

- **B** : `to_excel`does not exist for Spark, and Excel is not suitable.  
- **C** : CREATE EVENTSTREAM creates an event stream, not a table.  
- **D** : `git merge`is a version management command.  
  [Write Delta table]](https://learn.microsoft.com/fr-fr/fabric/data-engineering/delta-lake-table-operations)

---

## Question 17

**Nature** : Choix unique

**Stated**:  
You have a Delta table named`sales_raw`which receives every hour new lines in mode`append`. Developer adds new column`region`in source files. You want this column to be automatically added to the table without breaking the existing structure. What option should you use in your PySpark notebook?

**Alternatives** :  
A. `.option("mergeSchema", "true")`  
B. `.mode("overwrite")`  
C. `.option("header", "true")`  
D. `.mode("failfast")`

**Solution** :  
**Response correct: A**  
*Justification* : L'option `mergeSchema`allows to automatically add new columns when writing (append or overwrite) without destroying the existing schema. That is exactly what is required.  
*Why others are wrong*:  

- **B** : `overwrite`delete and recreate the table without preserving the old data.  
- **C** : `header`manages the header of CSV files, not schema evolution.  
- **D** : `failfast`fail the first mistake, which we do not want.  
  [Evolution of Delta Schema](https://learn.microsoft.com/fr-fr/azure/databricks/delta/schema-evolution)

---

## Question 18

**Nature**: Table to be completed (multiple choice grid)

**Stated**:  
Match the treatment with the most coherent tool.

| Treatment                                    | A. Dataflow Gen2 | B. Spark Notebook | C. Power BI |
| --------------------------------------------- | ---------------- | ----------------- | ----------- |
| Transformation low-code de sources tabulaires |                  |                   |             |
| Advanced cleaning with DataFrames              |                  |                   |             |
| Visualisation and business measures               |                  |                   |             |

**Solution** :  
✅ Transformation low-code → **A. Dataflow Gen2**  
Advanced cleaning with DataFrames → **B. Spark Notebook**  
Visualization and business measurements → **C. Power BI**  

*Justification*: Each of these tools has one main objective: ETL visual (Dataflow), processing code (Notebook), reporting (Power BI).  
(Choose between Dataflow and Notebook)](https://learn.microsoft.com/fr-fr/fabric/data-engineering/choose-dataflow-notebook)

---

## Question 19

**Nature** : Choix multiple

**Stated**:  
You have a Fabric pipeline that loads 100 CSV files every day in a Lakehouse. A corrupt file makes the entire pipeline fail. You want valid files to be loaded and corrupt files to be ignored and saved in an error table. Which Pipeline activity or Dataflow option allows this?

**Alternatives** :  
A. Activity **Copy Data** with error tolerance  
B. Activity **Notebook** with`spark.conf.set("spark.sql.files.ignoreCorruptFiles", "true")`  
C. Activity **Get Metadata** alone  
D. Activity **Web** calling for a REST API

**Solution** :  
  
*Justification* :  

- **A** : Copy Data activity allows you to configure an error tolerance (`fault tolerance`) to ignore corrupt lines or files.  
- **B** : In a notebook, the Spark parameter`spark.sql.files.ignoreCorruptFiles`allows you to ignore corrupted files during playback.  
  *Why others are wrong*:  
- **C**: Get Metadata does not load data.  
- **D** : Web calls an API but does not manage the tolerance to corrupt files.  
  [Copy Data Error Tolerance]](https://learn.microsoft.com/fr-fr/azure/data-factory/connector-troubleshoot-fault-tolerance)and [ignorsCorruptFiles Spark](https://spark.apache.org/docs/latest/sql-data-sources-generic-options.html)

---

## Question 20

**Nature** : Choix unique

**Stated**:  
Why should an incremental treatment use a MERGE key or logic rather than a systematic append?

**Alternatives** :  
A. To avoid duplication and make loading ideal  
B. To avoid errors and data conflicts  
C. To avoid data overwriting  
D. To speed up the execution time of requests

**Solution** :  
**Response correct: A**  
*Justification*: The MERGE (upsert) allows to insert new lines and update existing lines on the basis of a business key. This avoids duplicates and guarantees ease of use: restarting the same load does not change the final result.  
*Why others are wrong*:  

- **B**: The merge does not correct data conflicts of the same type.  
- **C** : Sometimes you want to crush some parts, not avoid any crash.  
- **D** : The merge may be slower than a simple append.  
  ](https://learn.microsoft.com/fr-fr/fabric/data-engineering/delta-lake-table-operations#upsert-into-a-table-using-merge)

---

## Question 21

**Nature** : Choix unique

**Stated**:  
Which destination is best followed to interview IoT events in near real time with KQL?

**Alternatives** :  
A. KQL Database / Eventhouse  
B. Scheduler  
C. Trigger  
D. EventStream and Activator

**Solution** :  
A. KQL Database / Eventhouse**  
*Justification*: The Eventhouse (formerly KQL Database) is the real-time storage and query engine for Fabric Real-Time Intelligence. It allows to execute KQL queries on event streams with very low latency.  
*Why others are wrong*:  

- **B** : Scheduler is not a destination, it is a planner.  
- **C**: Trigger triggers actions, but does not question.  
- **D** : EventStream and Activator are used to route and react, not to interview interactively.  
  [Eventhouse in Fabric](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/eventhouse)

---

## Question 22

**Nature** : Choix unique

**Stated**:  
You must count events by turbine and five-minute window in TurbinEvents. Which KQL request is the most consistent?

**Alternatives** :  
A. `TurbineEvents | summarize count() by bin(Timestamp, 5m)`  
B. `SELECT COUNT(*) FROM TurbineEvents GROUP BY DATEADD(MINUTE, DATEDIFF(MINUTE, 0, Timestamp) / 5 * 5, 0)`  
C. `CALCULATE(COUNTROWS(TurbineEvents))`  
D. `SELECT turbine, COUNT(*) FROM TurbineEvents GROUP BY turbine, window(Timestamp, '5 minutes')`

**Solution** :  
**Response correct: A**  
*Justification*: In KQL, the function`bin()`allows to create regular intervals (in 5 minutes) for dates. Syntax`summarize count() by bin(Timestamp, 5m)`is the native KQL way of counting by window.  
*Why others are wrong*:  

- **B** : Syntaxe T-SQL pure, non KQL.  
- **C** : Syntaxe DAX (Power BI).  
- **D**: SQL and`window()`which is not standard KQL.  
  🔗 [Fonction bin() en KQL](https://learn.microsoft.com/fr-fr/kusto/query/bin-function)

---

## Question 23

**Nature**: Multiple choice (several possible answers)

**Stated**:  
In a KQL table`TurbineEvents`which continuously receives measurements (temperature, vibration, power), what two operations are possible and relevant in real-time KQL request?

**Alternatives** :  
A. Filter lines with `| where temperature > 85`  
B. Group by window with `| summarize avg(vibration) by bin(Timestamp, 1m)`  
C. Attach two KQL tables with `| lookup`  
D. Creating a materialized view with`CREATE MATERIALIZED VIEW`  
E. Update an existing line with`UPDATE`

**Solution** :  
A and B**  
*Justification* :  

- **A**: Filtering`where`is fundamental in KQL.  
- **B** : Aggregation by window (`bin`) is typical of real time.  
  *Why others are less suitable or impossible in pure real time*:  
- **C** : `lookup`is possible but expensive and less common in continuous streaming.  
- **D**: The materialized views exist but are more for optimization than for interactive real time.  
- **E** : `UPDATE`is not a typical operation in real-time KQL (KQL tables are immutable by addition).  
  [Requests KQL](https://learn.microsoft.com/fr-fr/kusto/query/)

---

## Question 24

**Nature** : Choix unique

**Stated**:  
You must automatically power an alert table from an event table. Which design fits best?

**Alternatives** :  
A. Detection KQL function + update policy to alert table  
B. Manual copying of lines in Excel  
C. DAX measure that writes in KQL  
D. Stream Analytics + Activator with threshold trigger

**Solution** :  
**Response correct: A**  
*Justification*: In Fabric Real-Time Intelligence, the idiomatic approach is to create a **function KQL** that detects alerts, and use a **update policy** to write results into an alert table automatically and continuously.  
*Why others are wrong*:  

- **B**: Manual, not automated.  
- **C** : DAX cannot write in KQL.  
- **D** : Stream Analytics + Activator is more for notifications than for table power.  
  [Update policies in Kusto]](https://learn.microsoft.com/fr-fr/kusto/management/update-policy)

---

## Question 25

**Nature**: Table to be completed

**Stated**:  
Match each real time requirement to the most coherent component.

| Besoin                                        | A. Eventstream | B. KQL Database / Eventhouse | C. Real-Time Dashboard |
| --------------------------------------------- | -------------- | ---------------------------- | ---------------------- |
| Receive and route incoming events    |                |                              |                        |
| Store and interview events with KQL |                |                              |                        |
| View real-time indicators         |                |                              |                        |

**Solution** :  
Receive and route → **A. Eventstream**  
Store and interview with KQL → **B. KQL Database / Eventhouse**  
的 View real-time indicators → **C. Real-Time Dashboard**  

🔗 [Composants Real-Time Intelligence](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/overview)

---

## Question 26

**Nature** : Choix unique

**Stated**:  
In a star scheme, which table contains numerical measurements as quantity, amount or margin?

**Alternatives** :  
A. Table of facts  
B. Size table  
C. Traditional T-SQL table  
D. Association table

**Solution** :  
A. Table of Facts**  
*Justification*: The table of facts contains quantifiable measurements (facts) and foreign keys to dimensions. Dimensions contain descriptive attributes.  
*Why others are wrong*:  

- **B**: Dimension contains cluster attributes.  
- **C**: A classic T-SQL table may be either, but the question is about the star model.  
- **D**: Association table is generally used for many-to-many relationships.  
  (Schema in star)](https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema)

---

## Question 27

**Nature**: Multiple choice (2 answers)

**Stated**:  
What are the characteristics of a history dimension in SCD Type 2? Select two answers.

**Alternatives** :  
A. A column showing the current version  
B. Start and end dates  
C. Systematic deletion of older versions  
D. One modified line without history  
E. A mandatory DAX measure for each change

**Solution** :  
A and B**  
*Justification*: The Type 2 (Slowly Changing Dimension) keeps the history by creating a new line for each change, with columns`date_debut`and`date_fin`(or`est_courant`).  
*Why others are wrong*:  

- **C**: The versions are not deleted, they are retained.  
- **D**: This is Type 1.  
- **E**: No DAX measures are mandatory.  
  🔗 [SCD Type 2](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/slowly-changing-dimensions)

---

## Question 28

**Nature** : Choix unique

**Stated**:  
Before loading a table of facts, what verification avoids invalid relationships with dimensions?

**Alternatives** :  
A. Check that the dimension keys can be solved  
B. Check only the name of the report  
C. Delete all surrogate keys  
D. Write facts only in TXT

**Solution** :  
**Response correct: A**  
*Justification*: Ensure that each foreign key in the table of facts exists in the corresponding dimension (reference integrity). Otherwise, relationships will be invalid.  
*Why others are wrong*:  

- **B**: Does not concern data integrity.  
- **C**: Delete keys destroys the relationship.  
- **D**: The format is not relevant.  
  [Reference integrity]](https://learn.microsoft.com/fr-fr/sql/relational-databases/tables/primary-and-foreign-key-constraints)

---

## Question 29

**Nature** : Choix unique

**Stated**:  
A Delta table contains many small files after several loads. What action is most consistent with the workshop performance objective?

**Alternatives** :  
A. Run`OPTIMIZE`on the Delta table  
B. Increase the number of partitions with`REPARTITION`  
C. Change format to compressed CSV  
D. Disable Delta logging (`_delta_log`)

**Solution** :  
**Response correct: A**  
*Justification*: The command`OPTIMIZE`(or`OPTIMIZE ... ZORDER BY`) compacts small files into larger files, which improves playback performance.  
*Why others are wrong*:  

- **B** : `REPARTITION`increases the number of partitions, which can create even more small files.  
- **C**: Compressed CSV is no better for analytics than Delta.  
- **D**: Disable the Delta journal removes atomity and versioning.  
  [OPTIMIZE in Delta Lake]](https://learn.microsoft.com/fr-fr/azure/databricks/delta/optimize)

---

## Question 30

**Nature** : Choix unique

**Stated**:  
What practice could seriously degrade the partitioning of a large analytical table?

**Alternatives** :  
A. Partitionner par identifiant unique  
B. Partition per month when the volume warrants  
C. Aggregating Gold data per day  
D. Control the grain before join

**Solution** :  
**Response correct: A**  
*Justification* : Partitioning by a column with very high cardinality (like a unique identifier) creates thousands of partitions, each containing one or very few lines. It destroys performance. Partitioning must be done on a column with moderate cardinality (date, region, etc.).  
*Why others are correct* :  

- **B**: Partitioning per month is a good practice.  
- **C**: Aggregation per day is a good choice of grain.  
- **D**: Controlling grain is fundamental.  
  (Delta table sharing)](https://learn.microsoft.com/fr-fr/azure/databricks/delta/best-practices#partitioning)

---

## Question 31

**Nature** : Drag & Drop textuel / appariement

**Stated**:  
Match each concept to its definition.

| Concept           | Definition                                               |
| ----------------- | -------------------------------------------------------- |
| 1. Table of facts | A. Stable technical key for connecting facts and dimensions  |
| 2. Dimension      | B. Table containing analytical measurements and events |
| 3. Surrogate key  | C. Analysis axis as customer, product or date           |
| 4. SCD Type 2     | D. Technique for historicalizing changes             |

**Solution** :  
✅ 1 → **B**  
✅ 2 → **C**  
✅ 3 → **A**  
✅ 4 → **D**  

[Glossary of the data model](https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema)

---

## Question 32

**Nature** : Choix unique

**Stated**:  
In a Fabric warehouse, a table`Sales`contains columns`Amount`(amount sold) and`TargetAmount`(objective). You need to create a view`SalesRates`which displays the rate of achievement per seller. What definition is correct?

**Alternatives** :  
A. `SELECT SellerId, Amount / TargetAmount AS AchievementRate FROM Sales`  
B. `SELECT SellerId, Amount * TargetAmount AS AchievementRate FROM Sales`  
C. `SELECT SellerId, Amount / COUNT(*) AS AchievementRate FROM Sales`  
D. `SELECT SellerId, TargetAmount / Amount AS AchievementRate FROM Sales`

**Solution** :  
**Response correct: A**  
*Justification*: The rate of achievement is (realized/objective) either`Amount / TargetAmount`.  
*Why others are wrong*:  

- **B** : Multiplication gives a product, not a rate.  
- **C**: Division by number of lines makes no sense.  
- **D**: Reverse ratio (objective/realized).  
  🔗 [Syntaxe SQL de base](https://learn.microsoft.com/fr-fr/sql/t-sql/functions/mathematical-functions)

---

## Question 33

**Nature** : Choix unique

**Stated**:  
What mechanism specifically limits the lines visible in a table depending on the user or his perimeter?

**Alternatives** :  
A. Row-Level Security  
B. Deny on the resource  
C. Object-Level Security  
D. The Roles of Workspace

**Solution** :  
A. Row-Level Security (RLS)**  
*Justification*: RLS restricts access to a table line based on the user's privileges (for example, a seller sees only its own sales).  
*Why others are wrong*:  

- **B** : Deny is a general permission, not limited to lines.  
- **C**: Object-Level Security limits access to objects (table, column).  
- **D**: Workspace roles manage access at the workspace level, not within tables.  
  [Row-Level Security in Fabric](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/row-level-security)

---

## Question 34

**Nature** : Choix unique

**Stated**:  
What mechanism allows you to refuse reading a sensitive column like email or internal margin?

**Alternatives** :  
A. Column-Level Security / permissions colonne  
B. Eventstream routing  
C. Spark partitionBy uniquement  
D. Power BI theme

**Solution** :  
A. Column-Level Security**  
*Justification*: Column security allows access to or denial of access to specific columns of a table, regardless of the rest.  
*Why others are wrong*:  

- **B** : Eventstream route of events.  
- **C** : `partitionBy`is a physical optimization.  
- **D** : Power BI theme concerne l'apparence.  
  🔗 [Column-Level Security](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/column-level-security)

---

## Question 35

**Nature**: Multiple choice (3 expected responses)

**Stated**:  
Select three answers from those **managed directly by Fabric at the application level** (excluding infrastructure encryption).

**Alternatives** :  
A. Workspace roles  
B. SQL Permissions on Warehouse  
C. RLS in the Power BI semantic model  
D. Column Safety (column masking) in Lakehouse  
E. Cache requests

**Solution** :  
A, B, C**  
*Justification*: Fabric natively manages workspace roles (A), SQL permissions on Warehouse (B), and RLS in Power BI (C) models. Column safety in Lakehouse (D) is not yet fully equivalent to that of the Warehouse. Cache (E) is not a security mechanism.  
[Safety in Fabric](https://learn.microsoft.com/fr-fr/fabric/security/security-overview)

---

## Question 36

**Nature** : Choix unique

**Stated**:  
A user has access to the workspace but receives a`DENY SELECT`explicit on a sensitive column in the Warehouse. What behavior is expected?

**Alternatives** :  
A. The refused column must not be readable by that user  
B. Refusal physically removes the column  
C. Refusal creates a Gold table  
D. Refusal launches pipeline

**Solution** :  
**Response correct: A**  
*Justification*: One`DENY SELECT`on a column prevents the user (even with other permissions) from reading this column. It's an explicit security.  
*Why others are wrong*:  

- **B** : Aucune suppression physique.  
- **C** / **D**: Unbound.  
  🔗 [DENY (Transact-SQL)](https://learn.microsoft.com/fr-fr/sql/t-sql/statements/deny-transact-sql)

---

## Question 37

**Nature** : Choix unique

**Stated**:  
In Microsoft Fabric, a data engineer must give a marketing team **read only** access to a specific table in the Warehouse, without allowing them to see the other tables in the same scheme. How to proceed?

**Alternatives** :  
A. Add users to the **Viewer** role of the workspace, then create a view of the target table and grant them **SELECT** on this view only  
B. Add users to the role **Workspace contributor**, the RLS will do the rest  
C. Add users to the role **Admin** of workspace, then hide other tables by interface  
D. Add users to the role **Viewer** of the workspace, then grant them **SELECT** on all tables in the Warehouse

**Solution** :  
**Response correct: A**  
*Justification*: Viewer gives minimal access to workspace (see elements). Next, one can create a view covering only the desired table and grant`SELECT`on this view. Other tables are not accessible because rights are not granted.  
*Why others are wrong*:  

- **B** : Contributor a trop de droits (modification).  
- **C** : Admin is even more permissive.  
- **D** : Select on all tables is not restricted.  
  [Permissions on Warehouse objects]](https://learn.microsoft.com/fr-fr/fabric/data-warehouse/security)

---

## Question 38

**Nature** : Choix unique

**Stated**:  
A user has the role **Contributer** on a Fabric workspace. He wished to give read-only access to a Power BI report to an external colleague. Can he do it?

**Alternatives** :  
A. Yes, directly via report sharing  
B. Yes, adding the colleague as **Viewer** from workspace  
C. No, only one **Admin** of the workspace can share a report  
D. No, external users can never access Fabric

**Solution** :  
**Response correct: C**  
*Justification*: In Fabric, permission to share items (such as a Power BI report) is reserved for **members of the workspace Admin** role. Contributors and Viewer cannot share. External users can access via B2B if configured.  
*Why others are wrong*:  

- **A / B** : Contributor ne peut pas partager.  
- **D** : Externals can access (Azure AD B2B).  
  [Workspace hub Fabric](https://learn.microsoft.com/fr-fr/fabric/get-started/workspace-roles)

---

## Question 39

**Nature** : Choix unique

**Stated**:  
A data engineer applies a **RLS (Row Level Security)** to a Warehouse table. Users with the **Viewer** role of workspace see no data. What is the probable cause?

**Alternatives** :  
A. The RLS blocks by default any access without explicit rules  
B. Viewers never have access to Warehouse data  
C. The role **Admin** with RLS is mandatory  
D. The RLS automatically disables the workspace

**Solution** :  
**Response correct: A**  
*Justification*: By default, if you apply an RLS without setting a predicate that allows access for these users (or if no user is mapped to a security function), the default rule is not to show any lines. There is an explicit need to create a policy that returns TRUE for some users.  
*Why others are wrong*:  

- **B** : Viewers can see the data if no restrictive SLR is applied.  
- **C**: Admin is not required; We can assign RLS roles to Viewers.  
- **D**: RLS does not affect the existence of workspace.  
  ](https://learn.microsoft.com/fr-fr/sql/relational-databases/security/row-level-security)

---

## Question 40

**Nature** : Choix unique

**Stated**:  
One company wants an external provider to **read** Lakehouse table data, but not **change**. What minimum workspace role + which SQL permission is required?

**Alternatives** :  
A. **Viewer** + permission **SELECT** on the table  
B. **Contributer** + permission **INSERT** on the table  
C. **Admin** + aucune permission SQL  
D. **Viewer** + permission **UPDATE** on the table

**Solution** :  
**Response correct: A**  
*Justification*: The role **Viewer** gives read access to the metadata of the workspace. Next, you must explicitly grant permission **SELECT** on the table in question (in Lakehouse via SQL Analytics Endpoint or through Spark permissions).  
*Why others are wrong*:  

- **B**: Contributor already allows too much (modification).  
- **C**: Admin gives all rights.  
- **D** : UPDATE allows modification.  
  🔗 [Permissions Lakehouse](https://learn.microsoft.com/fr-fr/fabric/data-engineering/lakehouse-security)

---

## Question 41

**Nature**: Table to be completed

**Stated**:  
Match each need for governance with the most coherent mechanism.

| Besoin                                                    | A. Workspace role | B. Permission SQL | C. Semantic security (Power BI model) |
| --------------------------------------------------------- | ----------------- | ----------------- | ---------------------------------------- |
| Control who administers or contributes in the workspace   |                   |                   |                                          |
| Control access to a Warehouse table or column        |                   |                   |                                          |
| Control the playback experience in the Power BI model |                   |                   |                                          |

**Solution** :  
Workspace administration control → **A. Workspace role**  
Control table/column access Warehouse → **B. SQL Permission**  
Semantic safety** (RLS/OLS in model)  

[Safety in Fabric](https://learn.microsoft.com/fr-fr/fabric/security/security-overview)

---

## Question 42

**Nature** : Choix unique

**Stated**:  
A company receives 50 CSV files daily in a Lakehouse Bronze. A pipeline must:

1. Read Files
2. Clean data (remove null lines)
3. Apply RLS (Row Level Security)
4. Write to Delta Silver table

Which Fabric tool combination is the most suitable?

**Alternatives** :  
A. Dataflow Gen2 (cleaning) → Warehouse (RLS) → Silver Table  
B. Pipeline + Copy Data activity (reading) → Notebook PySpark (cleaning + RLS + Silver writing)  
C. KQL Database (reading) → Eventhouse (cleaning) → Power BI (RLS)  
D. Git (versioning) → Lakehouse (stockage) → RLS (automatique)

**Solution** :  
**Response correct: B**  
*Justification*: A pipeline can orchestrate reading (Copy Data) and then a PySpark notebook to perform cleaning, business logic, application of RLS (via conditional transformations) and writing in Delta Silver. This is the most flexible and efficient combination.  
*Why others are wrong*:  

- **A**: Dataflow Gen2 can clean, but the RLS at the Warehouse level is not the right layer for a Silver table in a Lakehouse.  
- **C** : KQL/Eventhouse is not suitable for batch cleaning of CSV.  
- **D**: Git does not process data.  
  [Ingestion scenario with pipeline and notebook](https://learn.microsoft.com/fr-fr/fabric/data-engineering/ingest-data-with-notebooks)

---

## Question 43

**Nature** : Choix unique

**Stated**:  
A Power BI report shows inconsistent results after a Silver join. Which technical verification is a priority?

**Alternatives** :  
A. Check whether the joint is established between the two entities in the semantic model  
B. Verify whether the join keys apply the necessary rules and constraints  
C. Check whether the Silver table has been properly updated (refreshed)  
D. Verify that the Power BI semantic model has been redeployed after join

**Solution** :  
**Response correct: B**  
*Justification*: Incoherence often comes from non-unique keys (as in question 5) or poorly defined relationships. First, the integrity and uniqueness of the upstream joint keys in the Silver table must be checked.  
*Why others are less priority*:  

- **A**: The semantic model may have the join, but if the underlying data have key problems, the result will be false.  
- **C**: Update is important, but structural inconsistency is more likely.  
- **D** : The redeployment does not affect the inconsistency of the data.  
  [Current Joint Problems](https://learn.microsoft.com/fr-fr/power-bi/guidance/relationships-common-issues)

---

## Question 44

**Nature** : Choix unique

**Stated**:  
You must choose between Dataflow Gen2 and Notebook Spark. Processing requires a lot of logic and a potentially important processing complexity, advanced quality controls and Delta writing. Which choice is the most coherent?

**Alternatives** :  
A. Notebook PySpark  
B. Dataflow Gen2  
C. Notebook Spark SQL  
D. Pipeline

**Solution** :  
A. Notebook PySpark**  
*Justification*: For complex transformations, advanced logic and quality control, a PySpark notebook (Python language) offers maximum flexibility (libraries, modular code, tests). Dataflow Gen2 is lower-code, less suited to complexity.  
*Why others are wrong* :  

- **B**: Dataflow Gen2 is more limited.  
- **C**: Spark SQL is less flexible than PySpark.  
- **D** : Pipeline is an orchestrator, not a transformation tool.  
  🔗 [Notebook vs Dataflow](https://learn.microsoft.com/fr-fr/fabric/data-engineering/choose-dataflow-notebook)

---

## Question 45

**Nature** : Choix unique

**Stated**:  
A pipeline loads Gold data while Silver tables are not yet available. Which architecture correction is the most appropriate?

**Alternatives** :  
A. Add sequential orchestration with dependencies and possibly Wait  
B. Perform Gold before Bronze systematically  
C. Remove Silver Layer  
D. Replace all tables with CSV files instead of TXT

**Solution** :  
**Response correct: A**  
*Justification*: The pipeline must be orchestrated so that the Gold stage explicitly depends on the success of the Silver stage (e.g. via the "If Condition" or "Wait" activity in a pipeline). Activities can also be chained with dependency properties.  
*Why others are wrong*:  

- **B** : Order must be Bronze → Silver → Gold.  
- **C** : Supprimer Silver rompt l'architecture.  
- **D** : Format is not the problem.  
  (dependencies in pipelines)](https://learn.microsoft.com/fr-fr/azure/data-factory/concepts-pipeline-execution-triggers#activity-dependencies)

---

## Question 46

**Nature**: Multiple choice (2 answers)

**Stated**:  
What elements can reduce the risk of duplication in incremental loading? Select two answers.

**Alternatives** :  
A. Using a business key in logic`MERGE`or`INSERT...ON CONFLICT`  
B. Check the existence of each line in the target table before insertion (lookup)  
C. Add a composite uniqueness constraint to the key columns in the Delta table  
D. Apply a deduplication window (`ROW_NUMBER() OVER(PARTITION BY key ORDER BY timestamp)`) in the notebook  
E. Load raw data in`append`then remove duplicates periodically by dedicated batch

**Solution** :  
A and D**  
*Justification* :  

- **A**:`MERGE`(or`INSERT ON CONFLICT`) is the standard method to avoid duplicate insertion/upsert.  
- **D**: Use`ROW_NUMBER()`with partitioning by business key and time window allows to keep only the most recent line, eliminating duplicates in the stream itself.  
  *Why others are less effective*:  
- **B** : The line-by-line lookup is very ineffective.  
- **C**: Unique constraints are not fully supported in Delta Lake standard (writing verification, but not guaranteed in competition).  
- **E** : Delete duplicates after the blow is heavier and does not prevent the storage of duplicates.  
  [Deduplication in Delta Lake]](https://learn.microsoft.com/fr-fr/azure/databricks/delta/merge#upsert-into-a-table-using-merge)

---

## Question 47

**Nature** : Choix unique

**Stated**:  
You have to explain why the Gold layer should not replace Bronze and Silver. What is the most direct justification?

**Alternatives** :  
A. Gold is used for aggregate analysis (business view), while Bronze retains the immutable crude and Silver prepares the cleaned and validated data  
B. Replacing Bronze and Silver with Gold would prevent any resumption of the pipeline in the event of an error of transformation or change of business rules  
C. Gold is often too aggregated and loses the fine grain needed to recalculate indicators differently later  
D. Bronze/Silver/Gold separation helps to isolate problems: ingestion (Bronze), quality (Silver), business (Gold)

**Solution** :  
  
*Justification*: If you delete Bronze and Silver, you lose the ability to **replay** pipeline from raw data. In case of error in Gold transformation or change of business rules, you could not rebuild the data without re-ingesting the sources. Bronze is the immutable archive essential for reproducibility.  
*Why others are also fair but less direct*:  

- **A**: Describes roles but does not emphasize reproducibility.  
- **C**: Aggregate Gold loses fine grain, but could have fine Gold.  
- **D**: Isolation of problems is a benefit, but the most direct justification for not **to replace** Bronze and Silver is reproducibility.  
  [Benefits from Medallion architecture]](https://learn.microsoft.com/fr-fr/fabric/data-engineering/medallion-lakehouse-architecture#why-are-bronze-and-silver-important)

---

## Question 48

**Nature** : Choix unique

**Stated**:  
An analyst asks why dimensions and table of fact are preferable to a single large flat table for reporting Warehouse. What answer is most relevant?

**Alternatives** :  
A. They structure the axes of analysis (time, product, customer, etc.) and avoid redundancy of descriptive attributes in each line of fact  
B. They allow to modify an attribute (e.g. product name) in one place, without rewriting millions of lines of facts  
C. They reduce the size of the model and improve the performance of aggregation requests compared to a giant flat table  
D. They allow implicit joins in the reporting tools (Power BI, Tableau) and simplify navigation for the business user

**Solution** :  
A** (most fundamental)  
*Justification*: The star scheme avoids redundancy of dimensional attributes in each line of fact. This saves space and simplifies maintenance. B, C and D are also true, but A is the main reason for modelling. In the context of review, A can be considered the most directly related issue.  
[Benefits of the star scheme](https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema#benefits-of-a-star-schema)

---

## Question 49

**Nature**: Multiple choice (several possible answers)

**Stated**:  
In a Microsoft Fabric workshop, three frequent errors can significantly degrade data quality and performance. Which ones?

**Alternatives** :  
A. Make an incremental append without trade key or duplication logic  
B. Attach two tables with incompatible granularities  
C. Read only the first line of a file (`first row only`) while several threshold lines have to be processed  
D. Implementing`OPTIMIZE`after each small insertion (less than 1 000 lines)  
E. Apply a RLS (Row Level Security) directly into the Lakehouse without sight or Warehouse  
F. Partition a table by a column with very high cardinality (e.g. unique identifier)

**Solution** :  
A, B, F**  
*Justification* :  

- **A** : Append without deduplication creates duplicates → degrades quality.  
- **B** : Jointing of different granularities (e.g. daily vs. monthly) produces mathematically false results → degrades quality.  
- **F** : Partitioning by high cardinality creates too many small files → degrades performance.  

*Why others are less critical or incorrect*:  

- **C** : Reading first line is sometimes desired (e.g. for metadata), this is not a common general error.  
- **D** : OPTIMIZE after small insertion is useless but not very penalizing.  
- **E** : RLS can be applied in Lakehouse via SQL endpoint, this is not an error.  
  🔗 [Bonnes pratiques Delta Lake](https://learn.microsoft.com/fr-fr/azure/databricks/delta/best-practices)

---

## Question 50

**Nature** : Choix unique

**Stated**:  
A company must process IoT data (50,000 events/second), produce alerts in less than 5 seconds, and keep all raw events for future replay. She also has to exhibit KPI trade over the last 3 months at a Power BI dashboard.  
Which Fabric architecture is the most suitable?

**Alternatives** :  
A. Eventhouse (ingestion KQL) → KQL Detection Function → Update policy to alert table → Activator (notification) → Lakehouse for raw archiving  
B. Eventhouse (ingestion KQL) → Pipeline with activity Notebook → Delta Bronze Table → Stream Analytics → Power BI  
C. Lakehouse (crude storage) → Pipeline with Dataflow Gen2 → Silver → Gold → Power BI Direct Lake → RLS  
D. KQL Database → Eventstream → Materialized view → Warehouse → Power BI import mode

**Solution** :  
**Response correct: A**  
*Justification*: Eventhouse is designed for high-speed ingestion (50k events/s). KQL functions and update policies allow very fast real-time alerts (<5s). Raw archiving can be done to a Lakehouse via the Eventhouse (retention or export). Power BI can connect directly to the Eventhouse for KPI. This is the typical Real-Time Intelligence architecture.  
*Why others are wrong*:  

- **B** : Pipeline with notebook introduces too high latency.  
- **C**: Raw Lakehouse is not suitable for high frequency real-time ingestion.  
- **D** : KQL Database + Eventstream + Warehouse + Import mode is complex and less efficient.  
  [Real time architecture Fabric](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/overview#scenarios)
