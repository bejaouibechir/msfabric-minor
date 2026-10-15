# Atelier 2 bis (optionnel) — Découvrir Copilot dans un Dataflow Gen2 et un pipeline

## Contexte de l’atelier

- **Statut :** atelier complémentaire et optionnel, à réaliser si le temps le permet après l’atelier 2.
- **Durée indicative :** 20 à 30 minutes.
- **Espace de travail :** `WS_Copilot`.
- **Lakehouse :** `lh_maison_lumiere`.
- **Point de départ :** la table `dbo.ventes_brut` créée dans la partie A de l’atelier 2.
- **Objectif :** découvrir Copilot dans deux autres surfaces de Fabric, sans approfondir.

## Périmètre

- **Partie A :** transformer des données avec Copilot dans un Dataflow Gen2.
- **Partie B :** orchestrer ce dataflow avec Copilot dans un pipeline.
- **Isolation :** cet atelier crée uniquement le dataflow `DF_Copilot_Canal`, le pipeline `PL_Copilot_Canal` et la table `dbo.dfg2_ventes_par_canal`.
- **Sans effet sur l’atelier 3 :** aucune table `dbo` existante ni aucune table `gold` n’est lue en écriture, modifiée ou supprimée.

## Méthode de progression

- **Piloter par Copilot :** chaque transformation est demandée à Copilot. Les interventions manuelles (source, destination, exécution) sont signalées.
- **Libellés d’interface :** les libellés marqués `[À VÉRIFIER SUR TENANT]` restent à confirmer dans l’instance Fabric.

# 

## Partie A — Copilot dans un Dataflow Gen2

### A.1 — Créer le dataflow et sa source

#### Avant d’exécuter

- **Création :** dans `WS_Copilot`, créer un **Dataflow Gen2** nommé `DF_Copilot_Canal`.
- **Source (intervention manuelle) :** **Get data > Lakehouse**, puis `lh_maison_lumiere`, table `dbo.ventes_brut`.
- **Copilot :** sélectionner **Copilot** dans le ruban du dataflow. `[À VÉRIFIER SUR TENANT]`

### A.2 — Transformer avec Copilot

#### Prompt

**Prompt A.2-1 — Réduire et dédoublonner**

> Conserve uniquement les colonnes `id_ligne`, `canal` et `quantite`. Supprime les lignes en double sur `id_ligne`.

**Prompt A.2-2 — Regrouper par canal**

> Regroupe les lignes par `canal` et ajoute deux colonnes : `nombre_lignes`, le nombre de lignes, et `quantite_totale`, la somme de `quantite`.

#### Résultats

| `canal`           | `nombre_lignes` | `quantite_totale` |
| ----------------- | ---------------:| -----------------:|
| `Magasin`         | 39 508          | 118 307           |
| `Click & Collect` | 19 992          | 60 051            |

- **Étapes appliquées :** vérifier dans **Applied steps** que Copilot a ajouté une sélection de colonnes, une suppression des doublons et un regroupement.
- **Montants :** `montant` est volontairement écarté ; ses formats mélangés sont traités dans l’atelier 3.

### A.3 — Publier vers le Lakehouse

#### Étapes

1. **Destination (intervention manuelle) :** **Add data destination > Lakehouse**, `lh_maison_lumiere`, nouvelle table `dfg2_ventes_par_canal`.
2. **Publication :** sélectionner **Publish** et attendre la fin de l’actualisation.

#### Résultats

- **Lakehouse :** la table `dfg2_ventes_par_canal` apparaît avec deux lignes, conformes au tableau de A.2.

## Partie B — Copilot dans un pipeline

### B.1 — Créer le pipeline avec Copilot

#### Avant d’exécuter

- **Création :** dans `WS_Copilot`, créer un **Data pipeline** nommé `PL_Copilot_Canal`.
- **Copilot :** sélectionner **Copilot** dans le ruban du pipeline. `[À VÉRIFIER SUR TENANT]`

#### Prompt

**Prompt B.1-1 — Ajouter l’activité Dataflow**

> Ajoute une seule activité Dataflow qui exécute le dataflow `DF_Copilot_Canal` de l’espace de travail `WS_Copilot`. N’ajoute aucune autre activité.

#### Résultats

- **Canevas :** une seule activité **Dataflow**, pointant vers `DF_Copilot_Canal`.

### B.2 — Exécuter et contrôler

#### Étapes

1. **Exécution (intervention manuelle) :** sélectionner **Run**.
2. **Suivi :** ouvrir l’onglet **Output** du pipeline.

#### Résultats

- **Statut :** l’activité Dataflow est à **Succeeded**.
- **Table :** `dfg2_ventes_par_canal` contient toujours les deux lignes attendues.

### Résultat de l’atelier

- **Dataflow :** Copilot a produit les étapes Power Query d’une transformation simple, vérifiée par un résultat chiffré.
- **Pipeline :** Copilot a ajouté l’activité d’orchestration demandée, sans activité superflue.
- **Copilot observé :** à compléter après l’essai sur le tenant.
