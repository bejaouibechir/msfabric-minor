# Atelier 5 — Traitement des données non structurées

## Partie 3 : Analyse des résultats et conclusions

**Thème : exploration SQL, visualisations Python et interprétation métier**

---

## Contexte

Les deux premières parties ont déjà construit et validé la solution technique :

- `LH_SolarVoix` contient les fichiers d'appels et les tables Delta ;
- `silver_appels_enrichis` contient les résultats de l'analyse IA ;
- `alertes_critiques` journalise les alertes produites par le traitement incrémental ;
- `PL_Traitement_Appel_Entrant` traite automatiquement les nouveaux fichiers ;
- `TR_test`, hébergée dans `ACT_SolarVoix_Appels`, écoute les événements OneLake ;
- `CALL_0121` a été traité automatiquement avec un score de risque de `100/100`.

Cette troisième partie ne crée ni modèle sémantique ni rapport Power BI. Elle sert uniquement à consulter les résultats, les visualiser simplement et formuler des conclusions.

## Objectifs

1. Contrôler les résultats finaux sans modifier les données.
2. Comparer le sentiment prédit à la vérité terrain.
3. Examiner les appels et produits les plus exposés au churn.
4. Distinguer les alertes historiques des alertes opérationnelles.
5. Tirer les conclusions métier et techniques de l'atelier.

> Toutes les requêtes de cette partie sont en lecture seule. Aucun nouveau traitement Fabric n'est nécessaire pour comprendre les résultats déjà validés.

---

# Bloc 1 — Contrôler les résultats avec SQL

## 1.1 — Ouvrir le point de terminaison SQL

1. Ouvrir `LH_SolarVoix`.
2. Basculer vers **SQL analytics endpoint**.
3. Créer une nouvelle requête SQL.

> Le point de terminaison SQL peut avoir un léger délai de synchronisation après une écriture Spark. Si les dernières lignes ne sont pas immédiatement visibles, attendre quelques instants puis actualiser.

## 1.2 — Vérifier les volumes et les principaux indicateurs

```sql
SELECT
    COUNT(*) AS total_appels,
    ROUND(AVG(CAST(score_risque_churn AS FLOAT)), 1) AS score_churn_moyen,
    SUM(CASE WHEN alerte_critique = 1 THEN 1 ELSE 0 END) AS appels_en_alerte,
    ROUND(
        100.0 * SUM(CASE WHEN alerte_critique = 1 THEN 1 ELSE 0 END)
        / COUNT(*),
        1
    ) AS taux_alertes_pct
FROM dbo.silver_appels_enrichis;
```

Résultats attendus après les Ateliers 1 et 2 :

| Indicateur | Valeur attendue |
|---|---:|
| Total d'appels | 121 |
| Score churn moyen | environ 58,0 |
| Appels signalés dans Silver | 85 |
| Taux d'alertes | environ 70,2 % |

Les 120 premiers appels proviennent du traitement batch. `CALL_0121` est l'appel critique ajouté pendant le test événementiel.

## 1.3 — Examiner la distribution du sentiment IA

```sql
SELECT
    sentiment_ia,
    COUNT(*) AS nb_appels,
    ROUND(AVG(CAST(score_risque_churn AS FLOAT)), 1) AS score_churn_moyen,
    SUM(CASE WHEN alerte_critique = 1 THEN 1 ELSE 0 END) AS nb_alertes
FROM dbo.silver_appels_enrichis
GROUP BY sentiment_ia
ORDER BY nb_appels DESC;
```

Après l'ajout de `CALL_0121`, la distribution attendue est :

| Sentiment IA | Nombre d'appels |
|---|---:|
| `negatif` | 91 |
| `positif` | 30 |

Le modèle utilisé ramène ici les appels neutres et très négatifs vers la classe `negatif`. Cette simplification doit être prise en compte lors de l'interprétation.

## 1.4 — Identifier les produits les plus exposés

```sql
SELECT
    COALESCE(produit, 'Métadonnée absente') AS produit,
    COUNT(*) AS nb_appels,
    SUM(CASE WHEN alerte_critique = 1 THEN 1 ELSE 0 END) AS nb_alertes,
    ROUND(AVG(CAST(score_risque_churn AS FLOAT)), 1) AS score_churn_moyen
FROM dbo.silver_appels_enrichis
GROUP BY COALESCE(produit, 'Métadonnée absente')
ORDER BY nb_alertes DESC, score_churn_moyen DESC;
```

Répartition historique des 84 alertes issues de la Partie 1 :

| Produit | Alertes |
|---|---:|
| Batterie stockage | 27 |
| Pompe à chaleur PAC | 21 |
| Panneaux solaires photovoltaïques | 20 |
| Borne recharge VE | 16 |

`CALL_0121` ajoute une alerte avec une métadonnée produit absente, car le test événementiel a créé uniquement le fichier texte et aucune nouvelle ligne dans `calls_metadata.csv`.

## 1.5 — Contrôler la qualité de la prédiction de sentiment

Les libellés de vérité terrain contiennent `tres_negatif`, alors que le modèle produit seulement `negatif` ou `positif` dans les résultats observés. Il faut donc normaliser les libellés avant de calculer une précision interprétable.

```sql
WITH evaluation AS (
    SELECT
        call_id,
        sentiment_ia,
        sentiment_reel,
        CASE
            WHEN sentiment_reel IN ('negatif', 'tres_negatif') THEN 'negatif'
            WHEN sentiment_reel = 'positif' THEN 'positif'
            WHEN sentiment_reel = 'neutre' THEN 'neutre'
            ELSE NULL
        END AS sentiment_reel_normalise
    FROM dbo.silver_appels_enrichis
    WHERE sentiment_reel IS NOT NULL
)
SELECT
    sentiment_reel_normalise,
    sentiment_ia,
    COUNT(*) AS nb_appels
FROM evaluation
GROUP BY sentiment_reel_normalise, sentiment_ia
ORDER BY sentiment_reel_normalise, sentiment_ia;
```

Calcul de la précision normalisée :

```sql
WITH evaluation AS (
    SELECT
        sentiment_ia,
        CASE
            WHEN sentiment_reel IN ('negatif', 'tres_negatif') THEN 'negatif'
            WHEN sentiment_reel = 'positif' THEN 'positif'
            WHEN sentiment_reel = 'neutre' THEN 'neutre'
        END AS sentiment_reel_normalise
    FROM dbo.silver_appels_enrichis
    WHERE sentiment_reel IS NOT NULL
)
SELECT
    COUNT(*) AS appels_evalues,
    SUM(CASE WHEN sentiment_ia = sentiment_reel_normalise THEN 1 ELSE 0 END) AS predictions_correctes,
    ROUND(
        100.0 * SUM(CASE WHEN sentiment_ia = sentiment_reel_normalise THEN 1 ELSE 0 END)
        / COUNT(*),
        1
    ) AS precision_normalisee_pct
FROM evaluation;
```

Résultat attendu sur les 120 appels disposant d'une vérité terrain :

- 90 prédictions normalisées correctes sur 120 ;
- précision normalisée : `75,0 %` ;
- les 30 appels réellement neutres sont classés `negatif`.

## 1.6 — Examiner les alertes opérationnelles

```sql
SELECT
    call_id,
    score_risque_churn,
    sentiment_ia,
    intent_detecte,
    statut,
    date_alerte
FROM dbo.alertes_critiques
ORDER BY date_alerte DESC;
```

Résultat validé :

| call_id | score | sentiment | intention | statut |
|---|---:|---|---|---|
| `CALL_0121` | 100 | `negatif` | `resiliation` | `NON_TRAITEE` |

> `silver_appels_enrichis` contient 85 lignes marquées comme critiques, tandis que `alertes_critiques` contient uniquement l'alerte opérationnelle créée par le traitement incrémental. Les 84 alertes historiques n'ont pas été rétrochargées dans cette table.

---

# Bloc 2 — Visualiser simplement avec Python

Cette partie est facultative. Elle remplace le rapport Power BI par trois graphiques légers dans un Notebook Fabric.

## 2.1 — Créer le Notebook d'analyse

1. Créer un Notebook nommé `NB_Analyse_Resultats`.
2. Attacher `LH_SolarVoix` comme Lakehouse par défaut.
3. Ajouter les cellules suivantes.

### Cellule 1 — Charger les données

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = spark.table("silver_appels_enrichis").toPandas()
df_historique = df[df["sentiment_reel"].notna()].copy()

df_historique["sentiment_reel_normalise"] = (
    df_historique["sentiment_reel"]
    .replace({"tres_negatif": "negatif"})
)

print(f"Appels Silver          : {len(df)}")
print(f"Appels avec vérité IA  : {len(df_historique)}")
```

### Cellule 2 — Volume et score par sentiment

```python
resume_sentiment = (
    df.groupby("sentiment_ia", dropna=False)
      .agg(
          nb_appels=("call_id", "count"),
          score_moyen=("score_risque_churn", "mean"),
          nb_alertes=("alerte_critique", "sum")
      )
      .reset_index()
)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

sns.barplot(
    data=resume_sentiment,
    x="sentiment_ia",
    y="nb_appels",
    hue="sentiment_ia",
    legend=False,
    ax=axes[0]
)
axes[0].set_title("Nombre d'appels par sentiment IA")
axes[0].set_xlabel("Sentiment IA")
axes[0].set_ylabel("Nombre d'appels")

sns.barplot(
    data=resume_sentiment,
    x="sentiment_ia",
    y="score_moyen",
    hue="sentiment_ia",
    legend=False,
    ax=axes[1]
)
axes[1].axhline(50, color="red", linestyle="--", label="Seuil critique = 50")
axes[1].set_title("Score churn moyen par sentiment")
axes[1].set_xlabel("Sentiment IA")
axes[1].set_ylabel("Score moyen")
axes[1].legend()

plt.tight_layout()
plt.show()
```

### Cellule 3 — Matrice de confusion normalisée

```python
matrice = pd.crosstab(
    df_historique["sentiment_reel_normalise"],
    df_historique["sentiment_ia"]
)

plt.figure(figsize=(6, 4))
sns.heatmap(matrice, annot=True, fmt="d", cmap="Blues")
plt.title("Sentiment réel normalisé vs sentiment IA")
plt.xlabel("Sentiment prédit")
plt.ylabel("Sentiment réel normalisé")
plt.tight_layout()
plt.show()
```

### Cellule 4 — Alertes par produit

```python
alertes_par_produit = (
    df[df["alerte_critique"] == True]
    .assign(produit=lambda x: x["produit"].fillna("Métadonnée absente"))
    .groupby("produit")
    .size()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 4))
alertes_par_produit.plot(kind="bar", color="#C0392B")
plt.title("Nombre d'alertes critiques par produit")
plt.xlabel("Produit")
plt.ylabel("Nombre d'alertes")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.show()
```

---

# Bloc 3 — Conclusions de l'atelier

## 3.1 — Conclusions métier

1. Le risque churn est élevé : environ 70 % des appels dépassent le seuil critique de 50.
2. Les batteries de stockage concentrent le plus grand nombre d'alertes historiques.
3. Les appels négatifs portent naturellement les scores les plus élevés.
4. L'intention `resiliation` associée à un score de 100 justifie une prise en charge immédiate de `CALL_0121`.
5. La table `alertes_critiques` peut servir de file de travail opérationnelle grâce au statut `NON_TRAITEE`.

## 3.2 — Conclusions sur le modèle IA

1. Le modèle sépare correctement les appels positifs des appels négatifs.
2. Les 25 appels `tres_negatif` sont correctement ramenés vers `negatif` après normalisation.
3. Les 30 appels neutres sont classés négatifs : le modèle surévalue donc le risque sur cette catégorie.
4. La précision normalisée observée est de 75 %, ce qui reste insuffisant pour automatiser seul une décision client sensible.
5. Le score IA doit rester un outil d'aide à la priorisation et non une décision définitive.

## 3.3 — Conclusions techniques

1. Le traitement batch a produit 120 lignes cohérentes et sans jointure manquante.
2. Le traitement événementiel a ajouté `CALL_0121` automatiquement.
3. Deux événements OneLake ont déclenché deux exécutions, mais les `MERGE` idempotents ont conservé une seule ligne Silver et une seule alerte.
4. Le traitement incrémental du fichier texte n'ajoute pas les métadonnées client, produit ou ville. Une solution de production devrait ingérer les métadonnées du nouvel appel dans le même flux.
5. Pour des volumes importants, le chemin du fichier fourni par l'événement devrait être transmis directement au Pipeline plutôt que de comparer tout le dossier à Silver.

---

## Récapitulatif de la Partie 3

| Élément | Contenu |
|---|---|
| Power BI | Supprimé de cette version |
| Modèle sémantique et DAX | Non nécessaires |
| SQL | Requêtes de contrôle et d'analyse en lecture seule |
| Python | Trois visualisations simples et facultatives |
| Résultats de référence | 121 appels, 85 critiques, score moyen proche de 58 |
| Qualité IA | 75 % après normalisation ; faiblesse sur la classe neutre |
| Alerte opérationnelle | `CALL_0121`, score 100, statut `NON_TRAITEE` |

La Partie 3 clôt l'Atelier 5 en transformant les sorties techniques des Parties 1 et 2 en constats exploitables, sans ajouter de nouvelle couche Power BI.
