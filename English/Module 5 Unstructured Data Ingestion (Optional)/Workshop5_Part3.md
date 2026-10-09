# Workshop 5 — Part 3: Power BI Report, KPIs, and Churn Analysis

**Theme: Direct Lake semantic model + Table Date + Analytical DAX measurements + 5 pages of report**

---

## Background and context

Parts 1 and 2 produced the table`silver_appels_enrichis`with the following columns:

| Colonne            | Type     | Description                                           |
| ------------------ | -------- | ----------------------------------------------------- |
| call id            | Text     | Unique call identifier                         |
| client_nom         | Text     | Client name                                         |
| ville              | Text     | Client city                                       |
| produit            | Text     | Product concerned by the call                          |
| date_appel         | DateTime | Date and time of call                              |
| duree_minutes      | Decimal  | Call duration in minutes                           |
| tranche_horaire    | Text     | Morning / Afternoon / End of day                   |
| jour_semaine       | Integer  | Day Number (1=Monday ... 7=Sunday)                 |
| sentiment_ia       | Text     | Sentiment predicted by model IA                     |
| score_sentiment    | Decimal  | Confidence in prediction IA (0 to 1)                 |
| intent_detecte     | Text     | Intention detected automatically                    |
| score_risque_churn | Integer  | Churn risk score (0 to 100)                       |
| alerte_critique    | Boolean  | TRUE si score ≥ 50                                    |
| sentiment_reel     | Text     | Real feeling (land truth for AI quality audit) |
| intention_reelle   | Text     | Actual intention declared by the client               |

** Objective of Part 3:**

1. **Table Date DimDate** — fully exploit the temporal dimension
2. **Analytical DAX measurements** — comparisons, deviations, precision IA, ratios
3. **Report 5 pages** — each page answers a specific analytical question:
   - Page 1 : Vue d'ensemble & KPIs comparatifs
   - Page 2: Churn risk analysis (scading, scattering, thresholds)
   - Page 3: Geographical analysis (city)
   - Page 4: Quality AI & real intentions
   - Page 5: Call Detail (drill-through)
4. **Views T-SQL** — SQL exploration of feelings about Lakehouse
5. **Visualizations Python** — in-depth analysis of feelings

---

## Block 1 — Creation of the semantic model

### 1.1—Create model from Lakehouse

1. In`WS_SolarVoix` → ouvrir `LH_SolarVoix`
2. In the Explorer Tables → check`silver_appels_enrichis`
3. Click **New semantic model** (top bar)
4. Nommer : `SM_SolarVoix_Appels`
5. Cliquer **Confirm**

### 1.2—Check Direct Lake Connection

1. Semantic model → tab **Model view**
2. Badge **Direct Lake** visible on the table
3. Check columns in the right panel

### 

## Block 2 — Table Date DimDate

> **Why a Date table?** Without a dedicated Date table, Power BI cannot make time comparisons (previous week, same month last year), nor properly sort months by name. A DimDate is **indispensable** to exploit the temporal dimension.

### 2.1 — Create the DimDate table in LH SolarVoix (Notebook)

> **Why in Lakehouse?** The Semantic Model`SM_SolarVoix_Appels`operating in **Direct Lake** mode: it reads data from`LH_SolarVoix`but ** has no writing rights**. It is impossible to create a calculated DAX table. The table`DimDate`must therefore be created directly in the Lakehouse and then referenced by the model.

**Step 1 — Open a Notebook in LH SolarVoix**

1. In`WS_SolarVoix` → ouvrir `LH_SolarVoix`
2. Top bar → **Open notebook** → **New notebook**
3. Name the notebook:`NB_Create_DimDate`
4. Check that Lakehouse`LH_SolarVoix`is well attached (left panel)

**Step 2 — Generate DimDate with Silver calls enriched dates**

The date range is calculated directly from`silver_appels_enrichis[date_appel]`to ensure consistency.

```python
from pyspark.sql import functions as F
from pyspark.sql.types import DateType

# Lire la plage de dates depuis silver_appels_enrichis
df_appels = spark.table("silver_appels_enrichis")
date_range = df_appels.agg(
    F.min(F.col("date_appel").cast(DateType())).alias("date_min"),
    F.max(F.col("date_appel").cast(DateType())).alias("date_max")
).collect()[0]

date_min = date_range["date_min"]
date_max = date_range["date_max"]
print(f"Plage de dates : {date_min} → {date_max}")

# Générer la séquence de dates
df_dim = spark.sql(f"""
    SELECT sequence(
        TO_DATE('{date_min}'),
        TO_DATE('{date_max}'),
        INTERVAL 1 DAY
    ) AS date_array
""").select(F.explode("date_array").alias("Date"))

# Ajouter toutes les colonnes de dimension temporelle
df_dimdate = df_dim.select(
    F.col("Date"),
    F.year("Date").alias("Année"),
    F.concat(F.lit("T"), F.ceil(F.month("Date") / 3).cast("string")).alias("Trimestre"),
    F.month("Date").alias("Mois_Num"),
    F.date_format("Date", "MMMM").alias("Nom_Mois"),
    F.date_format("Date", "yyyy-MM").alias("Année_Mois"),
    F.weekofyear("Date").alias("Semaine"),
    F.dayofweek("Date").alias("Jour_Semaine"),   # 1=Dim ... 7=Sam (Spark)
    F.date_format("Date", "EEEE").alias("Nom_Jour"),
    F.when(F.dayofweek("Date").isin([1, 7]), True).otherwise(False).alias("Est_Weekend")
)

# Écrire dans le Lakehouse en mode overwrite
df_dimdate.write.format("delta").mode("overwrite").saveAsTable("DimDate")

print(f"Table DimDate créée : {df_dimdate.count()} lignes")
df_dimdate.show(5)
```

**Step 3 — Add a date call date column to silver calls enriched**

> Why this step is indispensable? **`silver_appels_enrichis[date_appel]`is of type **TimestampType** (date + hour), while`DimDate[Date]`is **DateType** type (date only). In Direct Lake mode, a relationship between two columns of different types is silently inactive — visuals show`(Blank)`. A column of type should therefore be added`DateType`in`silver_appels_enrichis`to serve as a relationship key.

In the same notebook`NB_Create_DimDate`add a second cell:

```python
# Ajouter la colonne à la structure Delta (sans réécrire la table)
spark.sql("ALTER TABLE silver_appels_enrichis ADD COLUMN date_appel_date DATE")

# Remplir la colonne avec le cast Timestamp → Date
spark.sql("UPDATE silver_appels_enrichis SET date_appel_date = CAST(date_appel AS DATE)")

# Vérifier sur une lecture fraîche
spark.sql("SELECT date_appel, date_appel_date FROM silver_appels_enrichis LIMIT 3").show()
```

> 💡 `ALTER TABLE` + `UPDATE`Delta modifies the table surgically without rewriting all the Parquet files — it's faster and without risk of playing conflict.

The table`silver_appels_enrichis`now contains a column`date_appel_date`**DateType** type, compatible with`DimDate[Date]`.

**Step 4 — Check both tables in LH SolarVoix**

1. In the left panel of the Notebook → **Tables** → update (icon 
2. `DimDate`and`silver_appels_enrichis`(update) must appear
3. Right click on each → **Load data** → check the first lines

**Step 5 — Add DimDate to the semantic model**

1. In`WS_SolarVoix` → ouvrir `SM_SolarVoix_Appels`
2. Top bar → **Edit data model** → tab **Model view**
3. Top bar → **Add data** (or **Edit tables**)
4. Cocher `DimDate` → **Confirm**
5. The two tables appear in the model with the badge **Direct Lake**

### 2.2 — Create the DimDate relationship

The relationship is based on`date_appel_date`(DateType) side made — not on`date_appel` (TimestampType).

1. In **Model view** → slide`DimDate[Date]` vers `silver_appels_enrichis[date_appel_date]`
2. Relationship created: DimDate (1) → silver calles enrichis (*)
3. Check: Cardinality = **One to many**, Cross filter = **Single**

### 2.3 — Mark DimDate as Table Official Date

1. Right click on`DimDate`→ **Mark as date table**
2. Select Column`Date`
3. Cliquer **OK**

> This tagging activates Time Intelligence DAX (`DATEADD`, `SAMEPERIODLASTYEAR`etc.) on this table.

---

## Bloc 3 — Mesures DAX

> **Convention:** All measurements are created in the table`silver_appels_enrichis`. Right click on table → **New measure**.

---

### Group A — Constant measures (mandatory for Jauges)

> In Power BI Fabric, the fields **Minimum value** and **Maximum value** of the gauges do not accept manually entered values. It is imperative that ** measures DAX** return a constant.

**Mesure C1 — Score Minimum**

```dax
Score Min =
0
```

**Mesure C2 — Score Maximum**

```dax
Score Max =
100
```

**Mesure C3 — Seuil Alerte**

```dax
Seuil Alerte =
40
```

**Measure C4 — Objective Rate Alerts**

```dax
Objectif Taux Alertes =
0.10
```

**Mesure C5 — Max Taux Alertes**

```dax
Max Taux Alertes =
0.30
```

**Measure C6 — Objective Detection Termination**

```dax
Objectif Détection Résiliation =
0.80
```

*These 6 measurements are used only to power the Min/Max/Target fields of gauges and visuals Goal. *

---

### Groupe B — Mesures de base

**Mesure B1 — Score Churn Moyen**

```dax
Score Churn Moyen =
AVERAGE(silver_appels_enrichis[score_risque_churn])
```

**Mesure B2 — Taux Alertes Critiques**

```dax
Taux Alertes Critiques =
DIVIDE(
    COUNTROWS(FILTER(silver_appels_enrichis, silver_appels_enrichis[alerte_critique] = TRUE())),
    COUNTROWS(silver_appels_enrichis),
    0
)
```

*Format: Percentage, 1 decimal place*

**Mesure B3 — Nb Appels en Alerte**

```dax
Nb Appels en Alerte =
CALCULATE(COUNTROWS(silver_appels_enrichis), silver_appels_enrichis[alerte_critique] = TRUE())
```

**Mesure B4 — Total Appels**

```dax
Total Appels =
COUNTROWS(silver_appels_enrichis)
```

**Mesure B5 — Seuil Danger P90**

```dax
Seuil Danger P90 =
PERCENTILE.INC(silver_appels_enrichis[score_risque_churn], 0.90)
```

**Measure B6 — Negative Churn Score**

```dax
Score Churn Négatifs =
CALCULATE(
    AVERAGE(silver_appels_enrichis[score_risque_churn]),
    silver_appels_enrichis[sentiment_ia] = "negatif"
)
```

**Mesure B7 — Score Churn Hors Positif**

```dax
Score Churn Hors Positif =
CALCULATE(
    AVERAGE(silver_appels_enrichis[score_risque_churn]),
    silver_appels_enrichis[sentiment_ia] <> "positif"
)
```

**Measure B8 — Rates Termination**

```dax
Taux Résiliation =
DIVIDE(
    CALCULATE(COUNTROWS(silver_appels_enrichis), silver_appels_enrichis[intent_detecte] = "resiliation"),
    COUNTROWS(silver_appels_enrichis),
    0
)
```

*Format: Percentage, 1 decimal place*

**Measure B9 — Duration Moy Critical Calls**

```dax
Durée Moy Appels Critiques =
CALCULATE(
    AVERAGE(silver_appels_enrichis[duree_minutes]),
    silver_appels_enrichis[alerte_critique] = TRUE()
)
```

---

### Group C — Comparison and deviation measures

**Measure D1 — Difference Negative vs Medium**

```dax
Écart Négatifs vs Moyen =
[Score Churn Négatifs] - [Score Churn Moyen]
```

*Format: Decimal number, 1 decimal place*

> If this measure is +15, negative calls score 15 points above the overall average. This quantifyes the impact of negative sentiment on the risk of churn.

**Measure D2 — Ratio Score Off Positive vs Negative**

```dax
Ratio Hors Positif vs Négatifs =
DIVIDE([Score Churn Hors Positif], [Score Churn Négatifs], 0)
```

*Format: Percentage, 1 decimal place*

> If the ratio is close to 100%, neutral calls have almost the same score as negative ones — neutral feeling is actually as risky. If the ratio is 60%, neutrals are significantly less risky.

**Measure D3 — Ratio Termination vs Alerts**

```dax
Ratio Résiliation vs Alertes =
DIVIDE([Taux Résiliation], [Taux Alertes Critiques], 0)
```

*Format: Percentage, 1 decimal place*

> If this ratio is more than 100%, there are more plans to terminate than critical alerts generated — the alert system: some at-risk customers go under radar.

**Measure D4 — Critical Duration vs Global Duration**

```dax
Durée Critique vs Globale =
[Durée Moy Appels Critiques] - AVERAGE(silver_appels_enrichis[duree_minutes])
```

*Format: Decimal number, 1 decimal place*

> Quantifies the operational incremental cost of critical calls. If +3 min, each alert consumes 3 minutes more than a normal call.

---

### Group D — Quality measures IA

**Measure Q1 — Precision IA**

```dax
Précision IA =
DIVIDE(
    CALCULATE(
        COUNTROWS(silver_appels_enrichis),
        silver_appels_enrichis[sentiment_ia] = silver_appels_enrichis[sentiment_reel]
    ),
    COUNTROWS(silver_appels_enrichis),
    0
)
```

*Format: Percentage, 1 decimal place*

> Direct measurement of the reliability of model IA. If 80%, the model correctly predicts feeling in 80% of cases.

**Measure Q2 — Rate Intention Actual Termination**

```dax
Taux Intention Réelle Résiliation =
DIVIDE(
    CALCULATE(
        COUNTROWS(silver_appels_enrichis),
        silver_appels_enrichis[intention_reelle] = "resiliation"
    ),
    COUNTROWS(silver_appels_enrichis),
    0
)
```

*Format: Percentage, 1 decimal place*

> Compared to`Taux Résiliation`(based on`intent_detecte`), this measure uses the truth field. If the gap is large, the model lacks actual termination intentions.

**Measure Q3 — Detection Rate Termination**

```dax
Taux Détection Résiliation =
DIVIDE([Taux Résiliation], [Taux Intention Réelle Résiliation], 0)
```

*Format: Percentage, 1 decimal place*

> A score < 100% means that the model lacks actual cases of termination.

---

## Block 4 — Creating the report in Fabric

### 4.0 — Launching the report editor from the semantic model

Everything happens in the browser, directly from the workspace Fabric.

1. In`WS_SolarVoix` → ouvrir `SM_SolarVoix_Appels`
2. Top bar → **Create report**
3. Fabric report editor opens in a new browser tab
4. **Ctrl+S** → name the report`RPT_SolarVoix_Appels` → **Save**

> The report is automatically connected to the semantic model`SM_SolarVoix_Appels`in Direct Lake mode. All tables and measurements created in Blocks 2 and 3 are immediately available in the **Data** panel on the right.

### Presentation of the Fabric Editor's Interface

```
┌──────────────────────────────────────────────────────────────────┐
│  Barre du haut : File / Insert / Modeling / View                  │
├──────────┬───────────────────────────────┬───────────────────────┤
│ Filtres  │         CANVAS                │  Panneau droit        │
│ (gauche) │  Zone de construction         │  ① Visualizations     │
│          │  du rapport                   │     ├ Build visual    │
│          │                               │     ├ Format visual   │
│          │                               │     └ Analytics       │
│          │                               │  ② Data (champs)      │
├──────────┴───────────────────────────────┴───────────────────────┤
│  Onglets de pages (bas)                                           │
└──────────────────────────────────────────────────────────────────┘
```

The three basic gestures to remember in this publisher:

- **Add a visual** → click an icon in the panel **Visualizations** (right panel, tab 1) — the visual appears on the canvas, selected
- **Configure a visual** → selected visual → tab **Build visual** (graph icon) → drag fields from **Data** (sign 2) to Value / Axis / Legend areas etc.
- **Shape** → visual selected → tab **Visual** (brush icon)

### Create and name the 5 pages

1. Click **+** at the bottom left for each new page
2. Right click on the tab → **Rename page**
3. Name in order:`Vue d'ensemble`,`Risque Churn`,`Géographie`,`Qualité IA`,`Détail appel`

---

### Page 1 — Vue d'ensemble & KPIs comparatifs

**Objective:** The VAS manager must respond in 15 seconds to: "Does the situation improve or deteriorate?"

---

#### Visuel 1 — KPI : Score churn moyen vs seuil

The visual **KPI** is different from the visual **Card**: it displays the current value, a target value, and a trend indicator (high/low coloured arrow).

**Insert:**

1. Empty canvas → **Visualizations** → icon **KPI** (circle with number and arrow — search for "KPI" in the list)

**Build visual :**

- **Value** : `Score Churn Moyen`
- **Target** : `Seuil Alerte` (mesure C3 = 40)
- **Trend axis** : `DimDate[Année_Mois]`

**Result:** The arrow is green if the score is under 40, red if above. The monthly trend is displayed in miniature below the value.

---

#### Visual 2 — Goals: Critical alert rates vs 10% target

The visual **Goals** (or **Gauge** in linear mode) shows the progression towards a lens.

**Insert:**

1. Canvas vide → **Visualizations** → **Gauge**

**Build visual :**

- **Value** : `Taux Alertes Critiques`
- **Minimum value** : `Score Min` (mesure C1 — retourne 0)
- **Maximum value** : `Max Taux Alertes` (mesure C5 — retourne 0.30)
- **Target value**:`Objectif Taux Alertes`(Measure C4 — Return 0.10)

> The gauge ranges from 0 to 30%. The target line at 10% is clearly visible. If the actual rate exceeds 10%, the needle crosses the target without overflowing — the exceedance signal is immediate and legible. Never use the lens as Maximum: when the value exceeds the target, the gauge becomes inconsistent.

---

#### Visuel 3 — Carte KPI : Nb appels en alerte

**Visualizations → Card**

- **Fields** : `Nb Appels en Alerte`
- **Title** : `Appels à risque élevé`

---

#### Visual 4 — KPI card : Termination rate vs alerts

**Visualizations → Card**

- **Fields** : `Ratio Résiliation vs Alertes`
- **Title** : `Résiliations / Alertes`

> If this card displays > 100%, the alert system is insufficient — customers say they want to terminate without triggering an alert. This is the KPI calibration of the alert threshold.

---

#### Visual 5 — KPI card : Ratio Score Not Positive vs Negative

**Visualizations → Card**

- **Fields** : `Ratio Hors Positif vs Négatifs`
- **Title** : `Neutres vs Négatifs (%)`

> Answer the question: "Are neutral calls as risky as negative ones?" If > 80%, the neutral/negative distinction does not have much value for predicting churn.

---

#### Visual 6 — Ribbon Chart : Classification of feelings by product over time

The **Ribbon Chart** is a bar graph stacked with "rubans" that connect the bars between periods, showing how **rangs** change over time.

**Insert:**

1. Canvas → **Visualizations** → **Ribbon chart** (search "ribbon" in icons)

**Build visual :**

- **X-axis** : `DimDate[Nom Mois]`
- **Y-axis** : `Total Appels`
- **Legend** : `sentiment_ia`

**Analytics → Constant line :**

- Value : `Seuil Alerte` (mesure C3)
- Label : `Seuil 40`

> The ribbon chart shows how the volume of calls per sentiment changes month by month and whether the ranking of feelings changes. If the "negative" tape gradually rises up, the situation deteriorates.

---

#### Visual 7 — Trend curve with P90 threshold by date

**Insert:**

1. Canvas → **Visualizations** → **Line chart**

**Build visual :**

- **X-axis** : `DimDate[Année_Mois]`
- **Y-axis** : `Score Churn Moyen`
- **Secondary Y** : `Seuil Danger P90`

**Analytics → Constant line :**

- Value : `Seuil Alerte` (40)
- Color : rouge, Dotted, Label : `Seuil alerte`

> The P90 curve shows the evolution of the score of 10% of the most risky calls. If P90 rises while the Medium Score remains stable, there is a concentration of extreme cases that get worse.

---

#### Visuel 8 — Slicer : Filtre tranche horaire

**Visualizations → Slicer**

- **Field** : `tranche_horaire`
- **Style** : Tile

> To isolate morning/afternoon/end of day calls to detect if the churn is higher at certain hours.

---

### Page 2 — Risque Churn

**Objective:** Understand risk concentrations, correlations and product comparisons.

---

#### Visuel 1 — Jauge : Score churn global

**Visualizations → Gauge**

**Build visual :**

- **Value** : `Score Churn Moyen`
- **Minimum value** : `Score Min` (mesure C1)
- **Maximum value** : `Score Max` (mesure C2)
- **Target value** : `Seuil Alerte` (mesure C3)

> 

**Format visual → Colors → Fill color → Conditional formatting :**

- 0–25 → `#27AE60` (vert)
- 25–40 → `#F39C12` (orange)
- 40–100 → `#E74C3C` (rouge)

---

#### Visual 2 — Comparative gauge: Churn score negative calls

**Visualizations → Gauge** (second gauge side by side)

**Build visual :**

- **Value** : `Score Churn Négatifs`
- **Minimum value** : `Score Min`
- **Maximum value** : `Score Max`
- **Target value** : `Seuil Alerte`

> The two gauges side by side show the difference between the overall score and the negative call score. The deviation shown =`Écart Négatifs vs Moyen`.

---

#### Visual 3 — KPI card: Negative vs Medium

**Visualizations → Card**

- **Fields** : `Écart Négatifs vs Moyen`
- **Title** : `Surrisque appels négatifs`

> Complete both gauges by encrypting the gap. +20 points means that negative calls have a risk churn 20 points above average.

---

#### Visual 4 — Scatter Chart : Churn score vs Call time (by product)

The **Scatter Chart** shows two-dimensional phenomena concentrations. Each bubble = one product.

**Insert:**

1. Canvas → **Visualizations** → **Scatter chart**

**Build visual :**

- **X-axis**:`Durée Moy Appels Critiques`(warning duration of critical calls)
- **Y-axis** : `Score Churn Moyen`
- **Size** : `Nb Appels en Alerte`(Bubble size = number of alerts)
- **Legend** : `produit`(one bubble per product, each product with its color)
- **Values** : laisser vide

**Analytics → Constant line :**

- On Y axis: Value =`Seuil Alerte`(40) — separate safe zone / red zone
- On X axis: create a measure`Durée Moy Globale`=`AVERAGE(silver_appels_enrichis[duree_minutes])`and use it as a reference

> **Analytical reading:** The high-right quadrant (high score + high duration) contains the most problematic products — they generate both high-risk calls AND mobilize agents for a long time. These are the priorities for action.

---

#### Visuel 5 — Scatter Chart : Confiance IA vs Score churn

**Visualizations → Scatter chart**

**Build visual :**

- **X-axis** : `score_sentiment`(Average — confidence of model IA)
- **Y-axis** : `Score Churn Moyen`
- **Legend** : `sentiment_ia`
- **Details** : `call_id`

> If IA low-confidence points (x < 0.6) have very dispersed churn scores, this means that the IA model is unreliable on these cases — alerts generated on low-confidence predictions are less reliable.

---

#### Visual 6 — Pie Chart: Distribution of intentions detected

**Visualizations → Pie chart**

**Build visual :**

- **Legend** : `intent_detecte`
- **Values** : `Total Appels`

> The Pie Chart is adapted here because we want to see the relative proportions of intentions. The part of the "resilience" and "legal threat" intentions is directly legible.

---

#### Visual 7 — Horizontal bars : Termination rate vs Alert rates per product

**Visualizations → Clustered bar chart**

**Build visual :**

- **Y-axis** : `produit`
- **X-axis**: two superimposed measurements:
  - `Taux Résiliation`
  - `Taux Alertes Critiques`
- **Legend**: automatic (names of measurements)

> **Analytical question:** For each product, does the termination rate exceed the alert rate? If so, the alert threshold is too high for this specific product. This chart identifies sub-surveilled products.

---

#### Visuel 8 — Slicer : Filtre sentiment_ia

**Visualizations → Slicer**

- **Field** : `sentiment_ia`
- **Style** : Tile

---

### Page 3 — Geographical analysis

**Objective:** Identify cities and regions where the risk of churn is concentrated to guide field actions.

---

#### Visual 1 — Treemap: Top 10 cities per volume and risk churn

**Visualizations → Treemap**

**Build visual :**

- **Category** : `ville`
- **Values** : `Total Appels` (taille de chaque tuile = volume d'appels)
- **Color saturation** : `Score Churn Moyen`
- **Tooltips** : `Nb Appels en Alerte`, `Taux Alertes Critiques`

**Apply two filters to the visual:**

**Filter 1 — Exclude zero cities:**

1. Selected visual → panel **Filters** → section **Filters on this visual**
2. Glisser `ville`in this area
3. Filter type = **Basic filtering** → Uncheck **(Blank)**
4. Cliquer **Apply filter**

**Filtre 2 — Top 10 villes par score churn :**

1. In the same area **Filters on this visual**, drag again`ville`
2. Filter type = **Top N**
3. **Show items** : `Top` `10`
4. **By value**: drag measurement **`Score Churn Moyen`**
5. Cliquer **Apply filter**

> 💡 `Score Churn Moyen`as a selection criterion is consistent with the Treemap's Saturation Color — the 10 cities displayed are exactly those with the highest churn risk. Do not use`Total Appels`(favours large cities regardless of risk)`Taux Résiliation`(rate biased on cities with few calls).

---

#### Visuel 2 — Barres horizontales : Top 10 villes par score churn

**Visualizations → Clustered bar chart**

**Build visual :**

- **Y-axis** : `ville`
- **X-axis** : `Score Churn Moyen`
- **Filters panel** (left) → add`ville` → Top N = 10 (par `Score Churn Moyen`)

---

#### Visuel 3 — Matrice : Score churn — Ville × Produit

**Visualizations → Matrix**

**Build visual :**

- **Rows** : `ville`
- **Columns** : `produit`
- **Values** : `Score Churn Moyen`

**Format visual → Cell elements → Background color → Conditional formatting :**

- 0–25 : vert `#D5F5E3`
- 25–40 : orange `#FFF3CD`
- 40–100 : rouge `#FDDEDE`

> The matrix reveals the most problematic city/product combinations. A red cell in a specific city for a specific product = localized problem (installation, technician, network).

---

#### Visuel 4 — Slicer : Filtre produit

**Visualizations → Slicer** → `produit` → Style : Tile

---

### Page 4 — Quality IA & Intents

**Objective:** Assess the reliability of the AI model by comparing its predictions (`sentiment_ia`, `intent_detecte`) with reality (`sentiment_reel`, `intention_reelle`). Identify cases where the model is wrong.

---

#### Visual 1 — KPI: Overall precision of the IA model

**Visualizations → KPI**

**Build visual :**

- **Value** : `Précision IA`
- **Target**: Create a measure`Objectif Précision IA = 0.80`(80% as the minimum acceptable threshold)
- **Trend axis** : `DimDate[Nom Mois]`

> If the accuracy falls below 80%, the model produces too many errors and the alerts generated are unreliable. This is the re-training signal of the model.

---

#### Visuel 2 — Matrice de confusion : sentiment_reel vs sentiment_ia

**Visualizations → Matrix**

**Build visual :**

- **Rows** : `sentiment_reel`(Truth field)
- **Columns** : `sentiment_ia`(prediction IA)
- **Values** : `Total Appels`

**Format visual → Cell elements → Background color → Conditional formatting :**

- High values outside diagonal = model errors → red
- Values on the diagonal (good prediction) → green

> The diagonal (negative/negative, neutral/neutral, positive/positive) contains the correct predictions. Outside diagonal boxes contain errors. A red box in (feel reel="neutral", feeling ia="negative") means that the model over-prevents the negative feeling for truly neutral calls.

---

#### Visual 3 — Card comparison: Resilience detected vs. actual

Two yards side by side — no division, no instability due to data density.

**Visual 3a — Card: Termination rate detected by IA**

`Visualizations → Card`

- **Fields** : `Taux Résiliation`
- **Title** : `Résiliations détectées (IA)`
- Format: Percentage, 1 decimal place

**Visual 3b — Card: Actual termination rate**

`Visualizations → Card`

- **Fields** : `Taux Intention Réelle Résiliation`
- **Title** : `Résiliations réelles (clients)`
- Format: Percentage, 1 decimal place

> The difference between the two values is the key signal: if the AI detects 5% but the reality is 15%, the model lacks 10 actual termination points without triggering an alert. This direct reading is more reliable than a ratio`DIVIDE`which returns 0 as soon as one of the terms is missing over a period.

---

#### Visual 4 — Scatter : Feeling score (IA confidence) vs Product precision

**Visualizations → Scatter chart**

**Build visual :**

- **X-axis** : `score_sentiment` (Average — confiance IA)
- **Y-axis** : `Précision IA`
- **Details** : `produit`
- **Size** : `Total Appels`
- **Legend** : `produit`

> If some products have low AI AND low precision confidence, the model is unreliable on these specific calls. This may justify different pre-treatment for these categories.

---

#### Visuel 5 — Slicer : Filtre produit

**Visualizations → Slicer** → `produit` → Style : Tile

---

#### Visual 6 — Critical call table (drill-through entry point)

> This table is essential to test the drill through to Page 5. He exposes`call_id`at the line level — otherwise, the "Drill through" menu does not appear on the right click.

**Visualizations → Table**

**Build visual → Columns :**
`call_id`, `client_nom`, `ville`, `produit`, `score_risque_churn`, `sentiment_ia`, `alerte_critique`

**Filter on this visual :**
Glisser `alerte_critique` → Basic filtering → cocher **TRUE** → **Apply filter**

Click on the header`score_risque_churn`to sort in descending order.

**Test the drill through:**
Right click on any line → **Drill through** → **Detail call** → Page 5 opens filtered on this`call_id`.

---

### Page 5 — Call Detail (Drill-through)

> **Drill-through:** From any page, the user right-clicks on an item (bulle, bar, line) → "Drill through" → "Detail call". Page 5 opens filtered on this item.

**Configure drill-through:**

1. Make sure to be on the page`Détail appel`
2. Panneau **Visualizations** → **Build visual** → section **Drill through**
3. Glisser `call_id`in the area **Add drill-through fields here**

---

#### Visual 1 — KPI: Selected call score

**Visualizations → KPI**

- **Value** : `Score Churn Moyen`
- **Target** : `Seuil Alerte`

---

#### Visuel 2 — Carte : Sentiment IA

**Visualizations → Card** → `sentiment_ia` (First)

- **Title** : `Sentiment IA`

---

#### Visual 3 — Map : Real feeling

**Visualizations → Card** → `sentiment_reel` (First)

- **Title**:`Sentiment réel (audit)`

> Place both sentiment cards side by side. If they diverge, the IA prediction was incorrect for this call.

---

#### Visual 4 — Map : Intention detected vs. Intention

**Visualizations → Card** → `intent_detecte` (First) + **Visualizations → Card** → `intention_reelle` (First)

- Place side by side
- Titres : `Intention IA`and`Intention réelle`

---

#### Visual 5 — Table: Full call data

**Visualizations → Table**

**Build visual → Columns :**
`call_id`, `client_nom`, `ville`, `produit`, `date_appel`, `duree_minutes`, `tranche_horaire`, `sentiment_ia`, `sentiment_reel`, `intent_detecte`, `intention_reelle`, `score_risque_churn`, `alerte_critique`

**Format visual → Specific column → `score_risque_churn` → Conditional formatting :**

- 0–25 : `#D5F5E3`, 25–40 : `#FFF3CD`, ≥ 40 : `#FDDEDE`

---

#### Bouton retour

**Insert → Buttons → Back** — position on top left

- Text : `← Retour`

---

## Block 5 — T-SQL Views to analyze customer feelings

> Access SQL endpoint: in`LH_SolarVoix`→ drop-down menu **Lakehouse** → **SQL analytics endpoint** → **New query**

### View 1 — Distribution of feelings by product

```sql
CREATE VIEW v_sentiments_par_produit AS
SELECT
    produit,
    sentiment_ia,
    COUNT(*)                                          AS nb_appels,
    ROUND(AVG(CAST(score_risque_churn AS FLOAT)), 1)  AS score_churn_moyen,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY produit), 1) AS pct_dans_produit
FROM silver_appels_enrichis
GROUP BY produit, sentiment_ia;
```

```sql
SELECT * FROM v_sentiments_par_produit ORDER BY produit, sentiment_ia;
```

### View 2 — Clients most at risk

```sql
CREATE VIEW v_clients_a_risque AS
SELECT
    call_id, client_nom, ville, produit,
    sentiment_ia, intent_detecte, score_risque_churn,
    alerte_critique, date_appel,
    CASE
        WHEN score_risque_churn >= 70 THEN 'CRITIQUE'
        WHEN score_risque_churn >= 40 THEN 'ÉLEVÉ'
        WHEN score_risque_churn >= 25 THEN 'MODÉRÉ'
        ELSE 'FAIBLE'
    END AS niveau_risque
FROM silver_appels_enrichis
WHERE alerte_critique = 1;
```

```sql
SELECT TOP 20 * FROM v_clients_a_risque ORDER BY score_risque_churn DESC;
```

### Vue 3 — Comparaison sentiment_ia vs sentiment_reel (matrice de confusion SQL)

```sql
CREATE VIEW v_precision_ia AS
SELECT
    sentiment_reel,
    sentiment_ia,
    COUNT(*)                                        AS nb_appels,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY sentiment_reel), 1) AS pct_dans_classe
FROM silver_appels_enrichis
GROUP BY sentiment_reel, sentiment_ia;
```

```sql
-- Matrice de confusion : lignes = réel, colonnes = prédit
SELECT * FROM v_precision_ia ORDER BY sentiment_reel, sentiment_ia;
```

```sql
-- Précision globale
SELECT
    ROUND(100.0 * SUM(CASE WHEN sentiment_ia = sentiment_reel THEN 1 ELSE 0 END) / COUNT(*), 1)
    AS precision_pct
FROM silver_appels_enrichis;
```

### View 4 — Actual intentions vs. detected by product

```sql
CREATE VIEW v_intention_comparison AS
SELECT
    produit,
    intention_reelle,
    intent_detecte,
    COUNT(*) AS nb_appels,
    ROUND(AVG(CAST(score_risque_churn AS FLOAT)), 1) AS score_moyen,
    CASE WHEN intention_reelle = intent_detecte THEN 'CORRECT' ELSE 'ERREUR' END AS detection_ok
FROM silver_appels_enrichis
GROUP BY produit, intention_reelle, intent_detecte;
```

```sql
-- Taux de détection correcte par produit
SELECT produit,
       COUNT(*) AS nb_total,
       SUM(CASE WHEN detection_ok = 'CORRECT' THEN 1 ELSE 0 END) AS nb_correct,
       ROUND(100.0 * SUM(CASE WHEN detection_ok = 'CORRECT' THEN 1 ELSE 0 END) / COUNT(*), 1) AS precision_pct
FROM v_intention_comparison
GROUP BY produit
ORDER BY precision_pct;
```

### Vue 5 — Tendance hebdomadaire

```sql
CREATE VIEW v_tendance_hebdomadaire AS
SELECT
    DATEPART(YEAR, date_appel)  AS annee,
    DATEPART(WEEK, date_appel)  AS semaine,
    sentiment_ia,
    COUNT(*)                                         AS nb_appels,
    ROUND(AVG(CAST(score_risque_churn AS FLOAT)), 1) AS score_moyen
FROM silver_appels_enrichis
GROUP BY DATEPART(YEAR, date_appel), DATEPART(WEEK, date_appel), sentiment_ia;
```

---

## Block 6 — Python visualization with Seaborn and Matplotlib

### Prerequisites — Loading data

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

df = spark.table("silver_appels_enrichis").toPandas()  # Lakehouse attaché = nom simple suffisant, ne pas utiliser LH_SolarVoix.dbo.silver_appels_enrichis
df["date_appel"] = pd.to_datetime(df["date_appel"])

PALETTE = {"negatif": "#E74C3C", "neutre": "#F39C12", "positif": "#27AE60"}
SEUIL_ALERTE = 40

print(f"Données chargées : {len(df)} appels")
print(df[["sentiment_ia", "sentiment_reel", "score_risque_churn", "ville", "produit"]].describe(include="all").T)
```

---

### Figure 1 — Distribution of churn scores by sentiment

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
fig.suptitle("Distribution du score churn par sentiment", fontsize=14, fontweight="bold")

for ax, sent in zip(axes, ["negatif", "neutre", "positif"]):
    sous = df[df["sentiment_ia"] == sent]["score_risque_churn"]
    ax.hist(sous, bins=15, color=PALETTE[sent], alpha=0.75, edgecolor="white")
    ax.axvline(sous.mean(), color="black", linestyle="--", lw=1.5, label=f"Moy : {sous.mean():.1f}")
    ax.axvline(SEUIL_ALERTE, color="#C0392B", linestyle=":", lw=1.5, label="Seuil 40")
    ax.set_title(sent.capitalize(), fontweight="bold")
    ax.set_xlabel("Score churn")
    ax.legend(fontsize=8)
    ax.set_xlim(0, 100)

plt.tight_layout()
plt.show()
```

---

### Graph 2 — Mustache box: Churn score by product and sentiment

```python
fig, ax = plt.subplots(figsize=(14, 6))

sns.boxplot(data=df, x="produit", y="score_risque_churn", hue="sentiment_ia",
            palette=PALETTE, width=0.6, linewidth=1.2, ax=ax)

ax.axhline(SEUIL_ALERTE, color="#E74C3C", linestyle="--", lw=1.5, label="Seuil alerte (40)")
ax.axhline(25, color="#F39C12", linestyle=":", lw=1.2, label="Seuil vigilance (25)")
ax.set_title("Score churn par produit et sentiment", fontsize=13, fontweight="bold")
ax.set_ylim(0, 105)
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()
```

---

### Graphique 3 — Heatmap : Score moyen — Produit × Sentiment

```python
pivot = df.pivot_table(values="score_risque_churn", index="produit",
                       columns="sentiment_ia", aggfunc="mean").round(1)
pivot = pivot[[c for c in ["negatif", "neutre", "positif"] if c in pivot.columns]]

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn_r",
            vmin=0, vmax=100, linewidths=0.5, ax=ax,
            cbar_kws={"label": "Score churn moyen"})

ax.set_title("Score churn moyen — Produit × Sentiment", fontsize=13, fontweight="bold")
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
```

---

### Graphique 4 — Matrice de confusion : sentiment_ia vs sentiment_reel

```python
from sklearn.metrics import confusion_matrix

# Supprimer les lignes nulles sur les deux colonnes simultanément
df_clean = df.dropna(subset=["sentiment_reel", "sentiment_ia"])

labels = sorted(df_clean["sentiment_reel"].unique())
cm = confusion_matrix(df_clean["sentiment_reel"], df_clean["sentiment_ia"], labels=labels)

fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(pd.DataFrame(cm, index=labels, columns=labels),
            annot=True, fmt="d", cmap="Blues",
            linewidths=0.5, ax=ax)

ax.set_ylabel("Sentiment réel", fontsize=11)
ax.set_title("Matrice de confusion — Qualité du modèle IA", fontsize=13, fontweight="bold")

precision = cm.diagonal().sum() / cm.sum()
ax.set_xlabel(f"Sentiment prédit (IA)\nPrécision globale : {precision:.1%}", fontsize=11)
plt.tight_layout()
plt.show()
```

---

### Figure 5 — Trend curve with coloured threshold areas

```python
tendance = df.groupby(df["date_appel"].dt.to_period("D"))["score_risque_churn"].mean().reset_index()
tendance["date_appel"] = tendance["date_appel"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(14, 5))

ax.axhspan(0,  25,  alpha=0.08, color="#27AE60", label="Zone verte (< 25)")
ax.axhspan(25, 40,  alpha=0.08, color="#F39C12", label="Zone orange (25–40)")
ax.axhspan(40, 100, alpha=0.08, color="#E74C3C", label="Zone rouge (> 40)")

ax.plot(tendance["date_appel"], tendance["score_risque_churn"],
        color="#2C3E50", lw=2, marker="o", markersize=4, label="Score moyen journalier")
ax.axhline(SEUIL_ALERTE, color="#E74C3C", linestyle="--", lw=1.5, label="Seuil alerte (40)")

ax.set_title("Évolution quotidienne du score churn avec zones de risque", fontsize=13, fontweight="bold")
ax.set_ylim(0, 100)
ax.legend(loc="upper left", fontsize=9)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()
```

---

### Graph 6 — Scatter: Duration of critical calls vs Nb calls by product

```python
# Agrégation par produit
agg = df.groupby("produit").agg(
    score_moyen=("score_risque_churn", "mean"),
    duree_critique=("duree_minutes", lambda x: x[df.loc[x.index, "alerte_critique"] == True].mean()),
    nb_appels=("call_id", "count"),
    nb_alertes=("alerte_critique", "sum")
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(
    agg["nb_appels"], agg["duree_critique"],
    s=agg["score_moyen"] * 10,       # taille = score churn moyen
    c=agg["nb_alertes"],              # couleur = nb alertes
    cmap="RdYlGn_r", alpha=0.85,
    edgecolors="black", linewidths=0.8
)

for _, row in agg.iterrows():
    ax.annotate(row["produit"], (row["nb_appels"], row["duree_critique"]),
                fontsize=8, ha="center", va="bottom", xytext=(0, 6),
                textcoords="offset points")

ax.set_xlabel("Nombre d'appels total par produit", fontsize=11)
ax.set_ylabel("Durée moyenne des appels critiques (min)", fontsize=11)
ax.set_title("Durée critique vs Volume — Taille = Score churn moyen", fontsize=12, fontweight="bold")
plt.colorbar(scatter, label="Nb alertes")
ax.axhline(df[df["alerte_critique"]==True]["duree_minutes"].mean(),
           color="gray", linestyle=":", label="Durée moy critique globale")
ax.legend(fontsize=9)
plt.tight_layout()
plt.show()
```

> This graph responds directly to the question: "What products involve the most critical call agents AND generate the most alerts?" The product in the right-high quadrant is both highly sought after AND each alert lasts for a long time—maximum priority for training agents or product improvement.

---

## Summary of Part 3

| Composant             | Contenu                                                                                             |
| --------------------- | --------------------------------------------------------------------------------------------------- |
| `DimDate`             | Delta table in LH SolarVoix — year, month, week, day, weekend — beach set on`date_appel` |
| 21 mesures DAX        | Constants gauges, scores, gaps, quality AI, intentions                                           |
| Page 1 Vue d'ensemble | KPI vs seuil, Goals, Ribbon chart, tendance P90                                                     |
| Page 2 Risque Churn   | 2 gauges compared, scatter duration/score, Pie intentions, bars                                     |
| Page 3 Geography     | Carte, Top villes, scatter ville, matrice ville×produit                                             |
| Page 4 Quality IA     | Matrix confusion, KPI precision, comparison intentions                                            |
| Page 5 Call Detail   | Drill-through, sentiment ia vs sentiment reel, complete array                                      |
| 5 vues T-SQL          | Distribution, clients at risk, SQL confusion, intentions, trend                                 |
| 6 graphiques Python   | Histos, boxplot, heatmap, confusion, tendance, scatter produit                                      |

---

## Global summary of Workshop 5

| Part       | Duration   | Tools                                        | Liquid                             |
| ------------ | ------- | --------------------------------------------- | ------------------------------------- |
| **Part 1** | ~60 min | Lakehouse, PySpark Notebook, local NLP model | Bronze + Silver enriched tables      |
| **Part 2** | ~60 min | Pipeline Data Factory, Eventstream, Activator | Automatic pipeline, alarms, logging |
| **Part 3** | ~12     |                                               |                                       |
