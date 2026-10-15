# Annexe — Techniques de prompt engineering

## Objet

- **But :** montrer, pour chaque prompt des ateliers 2 et 3, comment une demande vague devient un prompt précis et contrôlable.
- **Lecture :** chaque prompt évolue en trois ou quatre versions. La première est volontairement faible ; chaque version suivante ajoute une amélioration.
- **Version finale :** elle reprend mot pour mot le prompt présenté dans l’atelier.
- **Usage :** comparer les versions, puis tester une version faible dans Fabric pour observer l’écart avec la version finale.

---

# Atelier 2

## Atelier 2 — Prompt A.2-1 — Charger `ventes_brut`

**Version 1**

> Charge le fichier ventes_brut.

- **Critique :** Ni source, ni destination, ni format : Copilot peut lire avec Pandas, créer plusieurs cellules ou exécuter sans revue.

**Version 2**

> Lis Files/atelier1/ventes_brut.csv avec l’en-tête et écris-le au format Delta dans la table ventes_brut.

- **Amélioration :** Source exacte, table cible et format Delta sont nommés : Copilot n’a plus à deviner le chemin ni le stockage.

**Version 3**

> Crée une nouvelle cellule PySpark. Lis Files/atelier1/ventes_brut.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table ventes_brut en mode overwrite, puis affiche le nombre de lignes.

- **Amélioration :** La surface (une cellule PySpark), un mode d’écriture rejouable et une sortie de contrôle sont fixés.

**Version 4 — prompt de l’atelier**

> Crée une nouvelle cellule PySpark intitulée « Cellule 1 — Charger ventes_brut ». Lis Files/atelier1/ventes_brut.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table ventes_brut en mode overwrite, puis affiche le nombre de lignes. N’utilise pas Pandas. N’exécute pas la cellule.

- **Amélioration :** Le titre de cellule facilite la relecture ; les interdits (Pandas, exécution) laissent la revue à l’humain avant toute exécution.

## Atelier 2 — Prompt A.3-1 — Charger `produits`

**Version 1**

> Charge le fichier produits.

- **Critique :** Ni source, ni destination, ni format : Copilot peut lire avec Pandas, créer plusieurs cellules ou exécuter sans revue.

**Version 2**

> Lis Files/atelier1/produits.csv avec l’en-tête et écris-le au format Delta dans la table produits.

- **Amélioration :** Source exacte, table cible et format Delta sont nommés : Copilot n’a plus à deviner le chemin ni le stockage.

**Version 3**

> Crée une nouvelle cellule PySpark. Lis Files/atelier1/produits.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table produits en mode overwrite, puis affiche le nombre de lignes.

- **Amélioration :** La surface (une cellule PySpark), un mode d’écriture rejouable et une sortie de contrôle sont fixés.

**Version 4 — prompt de l’atelier**

> Crée une nouvelle cellule PySpark intitulée « Cellule 2 — Charger produits ». Lis Files/atelier1/produits.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table produits en mode overwrite, puis affiche le nombre de lignes. N’utilise pas Pandas. N’exécute pas la cellule.

- **Amélioration :** Le titre de cellule facilite la relecture ; les interdits (Pandas, exécution) laissent la revue à l’humain avant toute exécution.

## Atelier 2 — Prompt A.4-1 — Charger `magasins`

**Version 1**

> Charge le fichier magasins.

- **Critique :** Ni source, ni destination, ni format : Copilot peut lire avec Pandas, créer plusieurs cellules ou exécuter sans revue.

**Version 2**

> Lis Files/atelier1/magasins.csv avec l’en-tête et écris-le au format Delta dans la table magasins.

- **Amélioration :** Source exacte, table cible et format Delta sont nommés : Copilot n’a plus à deviner le chemin ni le stockage.

**Version 3**

> Crée une nouvelle cellule PySpark. Lis Files/atelier1/magasins.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table magasins en mode overwrite, puis affiche le nombre de lignes.

- **Amélioration :** La surface (une cellule PySpark), un mode d’écriture rejouable et une sortie de contrôle sont fixés.

**Version 4 — prompt de l’atelier**

> Crée une nouvelle cellule PySpark intitulée « Cellule 3 — Charger magasins ». Lis Files/atelier1/magasins.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table magasins en mode overwrite, puis affiche le nombre de lignes. N’utilise pas Pandas. N’exécute pas la cellule.

- **Amélioration :** Le titre de cellule facilite la relecture ; les interdits (Pandas, exécution) laissent la revue à l’humain avant toute exécution.

## Atelier 2 — Prompt A.5-1 — Charger `retours`

**Version 1**

> Charge le fichier retours.

- **Critique :** Ni source, ni destination, ni format : Copilot peut lire avec Pandas, créer plusieurs cellules ou exécuter sans revue.

**Version 2**

> Lis Files/atelier1/retours.csv avec l’en-tête et écris-le au format Delta dans la table retours.

- **Amélioration :** Source exacte, table cible et format Delta sont nommés : Copilot n’a plus à deviner le chemin ni le stockage.

**Version 3**

> Crée une nouvelle cellule PySpark. Lis Files/atelier1/retours.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table retours en mode overwrite, puis affiche le nombre de lignes.

- **Amélioration :** La surface (une cellule PySpark), un mode d’écriture rejouable et une sortie de contrôle sont fixés.

**Version 4 — prompt de l’atelier**

> Crée une nouvelle cellule PySpark intitulée « Cellule 4 — Charger retours ». Lis Files/atelier1/retours.csv avec l’en-tête et l’inférence de schéma activée. Écris le résultat au format Delta dans la table retours en mode overwrite, puis affiche le nombre de lignes. N’utilise pas Pandas. N’exécute pas la cellule.

- **Amélioration :** Le titre de cellule facilite la relecture ; les interdits (Pandas, exécution) laissent la revue à l’humain avant toute exécution.

## Atelier 2 — Prompt B.2-1 — Générer la requête des volumes

**Version 1**

> Combien de lignes dans mes tables ?

- **Critique :** Copilot ne sait pas de quelles tables il s’agit ; il peut répondre en texte, sans requête, voire inventer des chiffres.

**Version 2**

> Génère une requête T-SQL qui compte les lignes des tables `dbo.ventes_brut`, `dbo.produits`, `dbo.magasins` et `dbo.retours`.

- **Amélioration :** Le livrable (une requête) et les tables exactes sont nommés : la réponse devient vérifiable.

**Version 3**

> Génère une requête T-SQL qui retourne, sur une seule ligne, le nombre de lignes des tables `dbo.ventes_brut`, `dbo.produits`, `dbo.magasins` et `dbo.retours`, dans des colonnes portant le nom de chaque table.

- **Amélioration :** La forme du résultat est imposée, ce qui le rend comparable à la requête de référence.

**Version 4 — prompt de l’atelier**

> Génère une requête T-SQL en lecture seule qui retourne, sur une seule ligne, le nombre de lignes des tables `dbo.ventes_brut`, `dbo.produits`, `dbo.magasins` et `dbo.retours`, dans des colonnes portant le nom de chaque table. Ne l’exécute pas.

- **Amélioration :** « En lecture seule » et « Ne l’exécute pas » bornent l’action : Copilot propose, l’utilisateur relit puis exécute.

## Atelier 2 — Prompt B.3-1 — Générer l’exploration du canal Magasin

**Version 1**

> Montre-moi les ventes en magasin.

- **Critique :** « En magasin » est ambigu (canal ou magasin physique ?) et aucune limite de volume n’est donnée.

**Version 2**

> Génère une requête T-SQL qui retourne les lignes de `dbo.ventes_brut` dont le canal vaut « Magasin ».

- **Amélioration :** La colonne et la valeur filtrées sont désignées sans ambiguïté.

**Version 3**

> Génère une requête T-SQL qui retourne au plus 1 000 lignes distinctes de `dbo.ventes_brut` dont le canal vaut « Magasin ».

- **Amélioration :** Le volume est borné et les doublons exacts sont exclus du résultat.

**Version 4 — prompt de l’atelier**

> Génère une requête T-SQL en lecture seule qui retourne au plus 1 000 lignes distinctes de `dbo.ventes_brut` dont le canal vaut « Magasin », en ignorant la casse et les espaces autour de la valeur. Ne l’exécute pas.

- **Amélioration :** La tolérance à la casse et aux espaces anticipe les variantes de saisie ; lecture seule et non-exécution bornent l’action.

## Atelier 2 — Prompt B.4-1 — Générer la jointure ventes-produits

**Version 1**

> Joins les ventes et les produits.

- **Critique :** Ni colonnes ni volume : Copilot peut produire un `SELECT *` massif, sur une clé qu’il choisit seul.

**Version 2**

> Génère une requête T-SQL qui joint `dbo.ventes_brut` à `dbo.produits` et retourne les 20 premières lignes.

- **Amélioration :** Les tables et le volume sont fixés.

**Version 3**

> Génère une requête T-SQL qui retourne les 20 premières lignes de `dbo.ventes_brut` avec `id_vente`, `id_produit`, le libellé et la catégorie du produit, et le canal.

- **Amélioration :** La projection est explicite : la réponse devient comparable à la requête de référence.

**Version 4 — prompt de l’atelier**

> Génère une requête T-SQL en lecture seule qui retourne les 20 premières lignes de `dbo.ventes_brut` avec `id_vente`, `id_produit`, le libellé et la catégorie du produit issus de `dbo.produits`, et le canal. Ne l’exécute pas.

- **Amélioration :** La provenance des colonnes est précisée ; la clé de jointure est volontairement tue pour observer si Copilot la déduit du schéma.

## Atelier 2 — Prompt B.5-1 — Générer le chiffre d’affaires par canal

**Version 1**

> Donne-moi le chiffre d’affaires.

- **Critique :** Ni table, ni axe, ni règle de calcul ; `montant` étant du texte, Copilot peut additionner sans conversion.

**Version 2**

> Génère une requête T-SQL qui calcule le chiffre d’affaires par canal à partir de `dbo.ventes_brut`.

- **Amélioration :** La source et l’axe d’analyse sont précisés.

**Version 3**

> Génère une requête T-SQL qui calcule le chiffre d’affaires par canal à partir de `dbo.ventes_brut`, en additionnant `montant` converti en `decimal(18,2)`.

- **Amélioration :** La règle de calcul et le type cible sont explicites.

**Version 4 — prompt de l’atelier**

> Génère une requête T-SQL en lecture seule qui calcule le chiffre d’affaires par canal à partir de `dbo.ventes_brut`, en additionnant `montant` converti en `decimal(18,2)`, trié par chiffre d’affaires décroissant. Ne l’exécute pas.

- **Amélioration :** L’ordre de sortie est fixé, et l’action reste bornée à une proposition en lecture seule.

## Atelier 2 — Prompt B.6-1 — Générer le comptage des retours valides

**Version 1**

> Compte les retours valides.

- **Critique :** « Valides » n’est pas défini : Copilot choisit seul la règle métier.

**Version 2**

> Génère une requête T-SQL qui compte les lignes de `dbo.retours` par `motif`.

- **Amélioration :** La table et le regroupement sont précisés.

**Version 3**

> Génère une requête T-SQL qui compte les lignes de `dbo.retours` par `motif`, en ne gardant que les retours dont la vente existe dans `dbo.ventes_brut` et dont le produit existe dans `dbo.produits`.

- **Amélioration :** La règle de validité est explicitée en deux conditions.

**Version 4 — prompt de l’atelier**

> Génère une requête T-SQL en lecture seule qui compte les lignes de `dbo.retours` par `motif`, en ne gardant que les retours dont la vente existe dans `dbo.ventes_brut` et dont le produit existe dans `dbo.produits`. Trie par nombre de retours décroissant. Ne l’exécute pas.

- **Amélioration :** Tri et bornage complètent le prompt ; les deux conditions restent séparées pour observer si Copilot vérifie le couple vente-produit.

## Atelier 2 — Prompt B.7-1 — Générer le top 10 des produits

**Version 1**

> Quels sont les meilleurs produits ?

- **Critique :** « Meilleurs » : en chiffre d’affaires, en quantité, en nombre de lignes ? Ni nombre ni colonnes attendues.

**Version 2**

> Génère une requête T-SQL qui retourne les 10 produits de `dbo.produits` les plus présents dans `dbo.ventes_brut`.

- **Amélioration :** Le critère (présence dans les ventes) et le nombre de produits sont fixés.

**Version 3**

> Génère une requête T-SQL qui retourne les 10 produits de `dbo.produits` les plus présents dans `dbo.ventes_brut`, avec `product_code`, `libelle_produit`, le nombre de lignes de vente et le nombre de ventes distinctes.

- **Amélioration :** Les colonnes et les deux mesures distinctes sont nommées.

**Version 4 — prompt de l’atelier**

> Génère une requête T-SQL en lecture seule qui retourne les 10 produits de `dbo.produits` les plus présents dans `dbo.ventes_brut`, avec `product_code`, `libelle_produit`, le nombre de lignes de vente et le nombre de ventes distinctes, triés par nombre de lignes décroissant puis par `product_code`. Ne l’exécute pas.

- **Amélioration :** Le tri secondaire sur `product_code` rend le top 10 déterministe malgré les égalités ; l’action reste bornée.

## Atelier 2 — Prompt B.9-1 — Présenter les volumes en lignes

**Version 1**

> Améliore la requête des volumes.

- **Critique :** « Améliore » sans critère : Copilot peut tout réécrire, ajouter des colonnes ou changer de tables.

**Version 2**

> Génère une requête T-SQL avec deux colonnes nommées `table_name` et `row_count`, et une ligne par table.

- **Amélioration :** La forme cible du résultat est décrite.

**Version 3**

> Génère une requête T-SQL avec deux colonnes nommées `table_name` et `row_count`. Retourne une ligne pour chacune des tables `dbo.ventes_brut`, `dbo.produits`, `dbo.magasins` et `dbo.retours`. Utilise `UNION ALL`.

- **Amélioration :** Le périmètre et la technique SQL sont imposés.

**Version 4 — prompt de l’atelier**

> Génère une seule requête T-SQL en lecture seule avec deux colonnes nommées `table_name` et `row_count`. Retourne une ligne pour chacune des tables `dbo.ventes_brut`, `dbo.produits`, `dbo.magasins` et `dbo.retours`. Utilise `UNION ALL`. Limite la requête à 15 lignes. Ne l’exécute pas.

- **Amélioration :** « Une seule requête », lecture seule et limite de 15 lignes rendent la proposition courte et relisable.

## Atelier 2 — Prompt B.10-1 — Mesurer avant de simplifier

**Version 1**

> La requête Magasin est-elle correcte ?

- **Critique :** Question fermée sans critère : Copilot répond oui ou non, sans preuve chiffrée.

**Version 2**

> Génère une requête T-SQL qui compte les lignes de `dbo.ventes_brut` dont `canal` vaut `'Magasin'`.

- **Amélioration :** On demande une mesure plutôt qu’un avis.

**Version 3**

> Génère une requête T-SQL sur `dbo.ventes_brut` qui retourne le nombre de lignes dont `canal` vaut `'Magasin'` et le nombre de lignes distinctes sur toutes les colonnes pour ce même canal.

- **Amélioration :** La seconde mesure révèle l’effet réel de `DISTINCT`.

**Version 4 — prompt de l’atelier**

> Génère une seule requête T-SQL en lecture seule sur `dbo.ventes_brut` qui retourne trois colonnes : `total_rows`, le nombre de lignes dont `canal` vaut `'Magasin'` ; `distinct_rows`, le nombre de lignes distinctes sur toutes les colonnes dont `canal` vaut `'Magasin'` ; `original_filter_rows`, le nombre de lignes dont `UPPER(LTRIM(RTRIM(canal)))` vaut `'MAGASIN'`. N’utilise pas `TOP`. Limite la requête à 15 lignes. Ne l’exécute pas.

- **Amélioration :** La troisième mesure compare les deux filtres, et l’interdiction de `TOP` évite qu’une limite masque l’écart.

## Atelier 2 — Prompt B.10-2 — Simplifier en conservant le résultat

**Version 1**

> Simplifie la requête Magasin.

- **Critique :** Copilot peut retirer `DISTINCT` et changer le résultat sans le signaler.

**Version 2**

> Génère une requête T-SQL sur `dbo.ventes_brut` qui retourne les lignes dont `canal` vaut `'Magasin'`, avec uniquement `id_ligne`, `id_vente`, `date_vente`, `id_magasin`, `id_produit`, `montant` et `canal`.

- **Amélioration :** La projection explicite remplace `SELECT *`.

**Version 3**

> Génère une requête T-SQL sur `dbo.ventes_brut` qui retourne les lignes distinctes dont `canal` vaut `'Magasin'`, avec uniquement `id_ligne`, `id_vente`, `date_vente`, `id_magasin`, `id_produit`, `montant` et `canal`. Conserve `DISTINCT`. Trie par `id_ligne`.

- **Amélioration :** Le résultat est préservé (doublons) et l’échantillon devient reproductible.

**Version 4 — prompt de l’atelier**

> Génère une seule requête T-SQL en lecture seule sur `dbo.ventes_brut` qui retourne les 1 000 premières lignes distinctes avec uniquement `id_ligne`, `id_vente`, `date_vente`, `id_magasin`, `id_produit`, `montant` et `canal`. Garde uniquement les lignes dont `canal` vaut `'Magasin'`. Conserve `DISTINCT`. Trie par `id_ligne`. N’utilise ni `SELECT *`, ni `UPPER`, ni `LTRIM`, ni `RTRIM`. Limite la requête à 12 lignes. Ne l’exécute pas.

- **Amélioration :** Les interdits explicites et la limite de 12 lignes empêchent Copilot de réintroduire les fonctions retirées.

## Atelier 2 — Prompt B.11-1 — Préciser la correction

**Version 1**

> Corrige la requête.

- **Critique :** Sans cible, Copilot peut réécrire toute la requête et changer les colonnes affichées.

**Version 2**

> Corrige uniquement la jointure invalide avec les produits.

- **Amélioration :** Le périmètre de la correction est limité à l’erreur.

**Version 3**

> Corrige uniquement la jointure invalide avec les produits. Relie `dbo.ventes_brut.id_produit` à la véritable clé produit de `dbo.produits`.

- **Amélioration :** On indique quoi relier sans imposer le nom de la clé : Copilot doit le lire dans le schéma.

**Version 4 — prompt de l’atelier**

> Corrige uniquement la jointure invalide avec les produits. Relie `dbo.ventes_brut.id_produit` à la véritable clé produit de `dbo.produits`. Conserve sans changement les cinq colonnes affichées.

- **Amélioration :** La conservation des cinq colonnes protège la sortie attendue.

## Atelier 2 — Prompt B.12-1 — Expliquer sans générer de code

**Version 1**

> Pourquoi ma requête plante ?

- **Critique :** Ni l’expression ni le type ne sont cités : la réponse sera générique, souvent accompagnée de code.

**Version 2**

> Explique pourquoi `CAST(montant AS decimal(18,2))` peut échouer.

- **Amélioration :** L’expression en cause est désignée.

**Version 3**

> Explique pourquoi `CAST(montant AS decimal(18,2))` peut échouer lorsque `montant` est stocké sous forme de texte. Ne génère pas de SQL.

- **Amélioration :** Le type réel est donné, et le mode « expliquer » exclut toute génération de code.

**Version 4 — prompt de l’atelier**

> La requête active utilise `CAST(montant AS decimal(18,2))`. Explique en trois points au maximum pourquoi cette conversion peut échouer lorsque `montant` est stocké sous forme de texte. Ne génère pas de SQL.

- **Amélioration :** L’ancrage sur la requête active et la limite de trois points rendent la réponse courte et ciblée.

## Atelier 2 — Prompt B.12-2 — Exposer les échecs de conversion

**Version 1**

> Corrige les montants.

- **Critique :** Copilot peut remplacer les valeurs invalides par zéro et masquer le problème.

**Version 2**

> Génère une requête T-SQL sur `dbo.ventes_brut` qui calcule le chiffre d’affaires par canal avec `TRY_CONVERT(decimal(18,2), montant)`.

- **Amélioration :** Une conversion tolérante est imposée.

**Version 3**

> Génère une requête T-SQL sur `dbo.ventes_brut` qui calcule le chiffre d’affaires par canal avec `TRY_CONVERT(decimal(18,2), montant)`. Compte aussi les valeurs non vides de `montant` qui ne peuvent pas être converties.

- **Amélioration :** L’échec de conversion devient mesurable.

**Version 4 — prompt de l’atelier**

> Génère une seule requête T-SQL en lecture seule sur `dbo.ventes_brut`. Pour chaque canal, calcule le chiffre d’affaires avec `TRY_CONVERT(decimal(18,2), montant)`. Compte aussi les valeurs non vides de `montant` qui ne peuvent pas être converties. Ne filtre pas les conversions en échec. Limite la requête à 20 lignes. Ne l’exécute pas.

- **Amélioration :** L’interdiction de filtrer les échecs empêche de les masquer ; la limite de taille garde la requête lisible.

## Atelier 2 — Prompt B.13-1 — Questionner la logique

**Version 1**

> Cette requête est-elle bonne ?

- **Critique :** Aucun critère : Copilot a tendance à valider la requête existante.

**Version 2**

> Les deux prédicats `IN` prouvent-ils que le produit appartient à la vente ?

- **Amélioration :** La question porte précisément sur la logique à vérifier.

**Version 3**

> Les deux prédicats `IN` indépendants prouvent-ils que `r.id_produit` appartient à `r.id_vente` sur une même ligne de `dbo.ventes_brut` ?

- **Amélioration :** La condition exacte à tester est formulée avec les colonnes réelles.

**Version 4 — prompt de l’atelier**

> Dans la requête active, les deux prédicats `IN` indépendants prouvent-ils que `r.id_produit` appartient à `r.id_vente` sur une même ligne de `dbo.ventes_brut` ? Réponds en trois phrases au maximum. Ne génère pas de SQL.

- **Amélioration :** L’ancrage sur la requête active, la limite de trois phrases et l’absence de SQL cadrent une réponse d’analyse.

## Atelier 2 — Prompt B.13-2 — Générer une correspondance unique

**Version 1**

> Réécris la requête des retours.

- **Critique :** Sans règle, Copilot peut conserver les deux `IN` séparés.

**Version 2**

> Génère une requête T-SQL qui compte les lignes de `dbo.retours` par `motif`, en vérifiant le couple `id_vente` et `id_produit` dans `dbo.ventes_brut`.

- **Amélioration :** La règle métier exacte est donnée.

**Version 3**

> Génère une requête T-SQL qui compte les lignes de `dbo.retours` par `motif`. Garde un retour uniquement si une seule sous-requête `EXISTS` trouve le même `id_vente` et le même `id_produit` dans `dbo.ventes_brut` et relie ce produit à `dbo.produits.product_code`.

- **Amélioration :** La technique (`EXISTS` unique) et la clé produit sont imposées.

**Version 4 — prompt de l’atelier**

> Génère une seule requête T-SQL en lecture seule qui compte les lignes de `dbo.retours` par `motif`. Garde un retour uniquement si une seule sous-requête `EXISTS` trouve le même `id_vente` et le même `id_produit` dans `dbo.ventes_brut` et relie ce produit à `dbo.produits.product_code`. Limite la requête à 20 lignes. Ne l’exécute pas.

- **Amélioration :** « Une seule requête », lecture seule et limite de 20 lignes bornent la proposition.

## Atelier 2 — Prompt B.14-1 — Réécrire la requête témoin

**Version 1**

> Optimise la requête témoin.

- **Critique :** « Optimise » sans contrainte : le résultat peut changer et le gain n’est pas mesurable.

**Version 2**

> Génère une requête T-SQL sur `dbo.produits` et `dbo.ventes_brut` avec un seul `LEFT JOIN` et un seul `GROUP BY`.

- **Amélioration :** La structure cible remplace les sous-requêtes corrélées.

**Version 3**

> Génère une requête T-SQL sur `dbo.produits` et `dbo.ventes_brut`. Utilise un seul `LEFT JOIN` et un seul `GROUP BY` pour retourner le TOP 10 avec `product_code`, `libelle_produit`, le nombre de lignes et le nombre de ventes distinctes. Conserve les produits sans vente.

- **Amélioration :** Le résultat attendu est décrit pour garantir l’équivalence avec la requête témoin.

**Version 4 — prompt de l’atelier**

> Génère une seule requête T-SQL en lecture seule sur `dbo.produits` et `dbo.ventes_brut`. Utilise un seul `LEFT JOIN` et un seul `GROUP BY` pour retourner le TOP 10 avec `product_code`, `libelle_produit`, le nombre de lignes et le nombre de ventes distinctes. Conserve les produits sans vente. Trie par nombre de lignes décroissant, puis par `product_code` croissant. Ajoute `OPTION (LABEL = 'ATELIER2_APRES_COPILOT')`. Limite la requête à 20 lignes. Ne l’exécute pas.

- **Amélioration :** Le tri déterministe permet la comparaison, et le label rend les exécutions retrouvables dans Monitor.

---

# Atelier 3

## Atelier 3 — Prompt A.1-1 — Classer faits et dimensions

**Version 1**

> Analyse mon modèle.

- **Critique :** Ni périmètre ni livrable : Copilot peut aussi proposer, voire appliquer, des modifications.

**Version 2**

> Classe les tables ventes_brut, retours, produits et magasins comme table de faits ou dimension.

- **Amélioration :** La tâche et les tables sont précisées.

**Version 3**

> Classe les tables ventes_brut, retours, produits et magasins comme table de faits ou dimension et justifie chaque choix en une phrase.

- **Amélioration :** La justification rend le raisonnement de Copilot vérifiable.

**Version 4 — prompt de l’atelier**

> Analyse uniquement les tables ventes_brut, retours, produits et magasins. Classe chacune comme table de faits ou dimension et justifie chaque choix en une phrase. Ne modifie pas le modèle.

- **Amélioration :** « Uniquement » et « Ne modifie pas le modèle » protègent le modèle ouvert en mode Editing.

## Atelier 3 — Prompt A.1-2 — Grain et clé candidate

**Version 1**

> Quelles sont les clés ?

- **Critique :** Copilot présentera des clés déduites des noms comme si elles étaient vérifiées.

**Version 2**

> Indique le grain supposé et la clé candidate de chacune des quatre tables.

- **Amélioration :** Deux notions distinctes, le grain et la clé, sont demandées pour chaque table.

**Version 3 — prompt de l’atelier**

> Indique le grain supposé et la clé candidate de chacune des quatre tables. Sépare ce qui est prouvé par le modèle de ce qui doit être vérifié dans les données. Ne modifie rien.

- **Amélioration :** Séparer le prouvé du supposé oblige Copilot à distinguer hypothèse et preuve, sans toucher au modèle.

## Atelier 3 — Prompt A.2-1 — Clés des dimensions

**Version 1**

> Les clés des dimensions sont-elles bonnes ?

- **Critique :** Question d’avis : la réponse n’apportera aucune preuve chiffrée.

**Version 2**

> Vérifie l’unicité de produits[product_code] et magasins[store_code].

- **Amélioration :** Les colonnes à contrôler sont nommées.

**Version 3 — prompt de l’atelier**

> Vérifie l’unicité de produits[product_code] et magasins[store_code]. Pour chaque colonne, retourne le nombre de lignes, le nombre de valeurs distinctes et leur différence. Ne modifie pas le modèle.

- **Amélioration :** Les trois nombres demandés (lignes, distinctes, différence) font de l’unicité une preuve lisible.

## Atelier 3 — Prompt A.2-2 — Clés des faits

**Version 1**

> Les tables de faits ont-elles des doublons ?

- **Critique :** Question d’avis, sans colonne de référence : la notion de doublon reste floue.

**Version 2**

> Vérifie l’unicité de ventes_brut[id_ligne] et retours[id_retour].

- **Amélioration :** Les clés de ligne à contrôler sont nommées.

**Version 3 — prompt de l’atelier**

> Vérifie l’unicité de ventes_brut[id_ligne] et retours[id_retour]. Pour chaque colonne, retourne le nombre de lignes, le nombre de valeurs distinctes et leur différence. Ne modifie pas le modèle.

- **Amélioration :** Les trois nombres demandés rendent tout doublon immédiatement visible, sans modifier le modèle.

## Atelier 3 — Prompt A.3-1 — Produits orphelins des ventes

**Version 1**

> Y a-t-il des produits manquants ?

- **Critique :** Ni sens de comparaison ni colonnes : Copilot ne sait pas quelle table contrôler contre quelle autre.

**Version 2**

> Compte les valeurs distinctes de ventes_brut[id_produit] qui n’existent pas dans produits[product_code].

- **Amélioration :** La direction du contrôle et les colonnes exactes sont désignées.

**Version 3 — prompt de l’atelier**

> Compte les valeurs distinctes de ventes_brut[id_produit] qui n’existent pas dans produits[product_code]. Retourne seulement le nombre et quelques exemples s’il est supérieur à zéro. Ne modifie rien.

- **Amélioration :** La sortie est bornée au nombre, avec des exemples seulement en cas d’écart, et le modèle reste intact.

## Atelier 3 — Prompt A.3-2 — Magasins orphelins des ventes

**Version 1**

> Y a-t-il des magasins manquants ?

- **Critique :** Ni sens de comparaison ni colonnes : Copilot ne sait pas quelle table contrôler contre quelle autre.

**Version 2**

> Compte les valeurs distinctes de ventes_brut[id_magasin] qui n’existent pas dans magasins[store_code].

- **Amélioration :** La direction du contrôle et les colonnes exactes sont désignées.

**Version 3 — prompt de l’atelier**

> Compte les valeurs distinctes de ventes_brut[id_magasin] qui n’existent pas dans magasins[store_code]. Retourne seulement le nombre et quelques exemples s’il est supérieur à zéro. Ne modifie rien.

- **Amélioration :** La sortie est bornée au nombre, avec des exemples seulement en cas d’écart, et le modèle reste intact.

## Atelier 3 — Prompt A.3-3 — Produits orphelins des retours

**Version 1**

> Y a-t-il des produits retournés manquants ?

- **Critique :** Ni sens de comparaison ni colonnes : Copilot ne sait pas quelle table contrôler contre quelle autre.

**Version 2**

> Compte les valeurs distinctes de retours[id_produit] qui n’existent pas dans produits[product_code].

- **Amélioration :** La direction du contrôle et les colonnes exactes sont désignées.

**Version 3 — prompt de l’atelier**

> Compte les valeurs distinctes de retours[id_produit] qui n’existent pas dans produits[product_code]. Retourne seulement le nombre et quelques exemples s’il est supérieur à zéro. Ne modifie rien.

- **Amélioration :** La sortie est bornée au nombre, avec des exemples seulement en cas d’écart, et le modèle reste intact.

## Atelier 3 — Prompt A.4-1 — Renommer `ventes_brut`

**Version 1**

> Renomme les tables avec de meilleurs noms.

- **Critique :** Copilot choisit seul les noms et peut renommer d’autres objets que les tables visées.

**Version 2**

> Renomme la table ventes_brut en FactVentes.

- **Amélioration :** La table cible et le nouveau nom sont explicites.

**Version 3 — prompt de l’atelier**

> Renomme uniquement la table ventes_brut en FactVentes. Ne modifie aucun autre objet.

- **Amélioration :** « Uniquement » et « aucun autre objet » limitent l’action à un seul renommage vérifiable.

## Atelier 3 — Prompt A.4-2 — Renommer `retours`

**Version 1**

> Renomme les tables avec de meilleurs noms.

- **Critique :** Copilot choisit seul les noms et peut renommer d’autres objets que les tables visées.

**Version 2**

> Renomme la table retours en FactRetours.

- **Amélioration :** La table cible et le nouveau nom sont explicites.

**Version 3 — prompt de l’atelier**

> Renomme uniquement la table retours en FactRetours. Ne modifie aucun autre objet.

- **Amélioration :** « Uniquement » et « aucun autre objet » limitent l’action à un seul renommage vérifiable.

## Atelier 3 — Prompt A.4-3 — Renommer `produits`

**Version 1**

> Renomme les tables avec de meilleurs noms.

- **Critique :** Copilot choisit seul les noms et peut renommer d’autres objets que les tables visées.

**Version 2**

> Renomme la table produits en DimProduit.

- **Amélioration :** La table cible et le nouveau nom sont explicites.

**Version 3 — prompt de l’atelier**

> Renomme uniquement la table produits en DimProduit. Ne modifie aucun autre objet.

- **Amélioration :** « Uniquement » et « aucun autre objet » limitent l’action à un seul renommage vérifiable.

## Atelier 3 — Prompt A.4-4 — Renommer `magasins`

**Version 1**

> Renomme les tables avec de meilleurs noms.

- **Critique :** Copilot choisit seul les noms et peut renommer d’autres objets que les tables visées.

**Version 2**

> Renomme la table magasins en DimMagasin.

- **Amélioration :** La table cible et le nouveau nom sont explicites.

**Version 3 — prompt de l’atelier**

> Renomme uniquement la table magasins en DimMagasin. Ne modifie aucun autre objet.

- **Amélioration :** « Uniquement » et « aucun autre objet » limitent l’action à un seul renommage vérifiable.

## Atelier 3 — Prompt A.5-1 — Relier `DimProduit` à `FactVentes`

**Version 1**

> Relie DimProduit à FactVentes.

- **Critique :** Ni colonnes, ni cardinalité, ni sens de filtrage : Copilot peut créer une relation plusieurs-à-plusieurs ou bidirectionnelle.

**Version 2**

> Crée une relation de DimProduit[product_code] vers FactVentes[id_produit].

- **Amélioration :** Les colonnes exactes de la relation sont désignées.

**Version 3**

> Crée une relation de DimProduit[product_code], côté 1, vers FactVentes[id_produit], côté plusieurs.

- **Amélioration :** La cardinalité un-à-plusieurs est imposée.

**Version 4 — prompt de l’atelier**

> Crée uniquement une relation active de DimProduit[product_code], côté 1, vers FactVentes[id_produit], côté plusieurs. Utilise un filtrage à sens unique de DimProduit vers FactVentes.

- **Amélioration :** « Uniquement », relation active et filtrage à sens unique fixent le comportement attendu, sans autre création.

## Atelier 3 — Prompt A.5-2 — Relier `DimMagasin` à `FactVentes`

**Version 1**

> Relie DimMagasin à FactVentes.

- **Critique :** Ni colonnes, ni cardinalité, ni sens de filtrage : Copilot peut créer une relation plusieurs-à-plusieurs ou bidirectionnelle.

**Version 2**

> Crée une relation de DimMagasin[store_code] vers FactVentes[id_magasin].

- **Amélioration :** Les colonnes exactes de la relation sont désignées.

**Version 3**

> Crée une relation de DimMagasin[store_code], côté 1, vers FactVentes[id_magasin], côté plusieurs.

- **Amélioration :** La cardinalité un-à-plusieurs est imposée.

**Version 4 — prompt de l’atelier**

> Crée uniquement une relation active de DimMagasin[store_code], côté 1, vers FactVentes[id_magasin], côté plusieurs. Utilise un filtrage à sens unique de DimMagasin vers FactVentes.

- **Amélioration :** « Uniquement », relation active et filtrage à sens unique fixent le comportement attendu, sans autre création.

## Atelier 3 — Prompt A.5-3 — Relier `DimProduit` à `FactRetours`

**Version 1**

> Relie DimProduit à FactRetours.

- **Critique :** Ni colonnes, ni cardinalité, ni sens de filtrage : Copilot peut créer une relation plusieurs-à-plusieurs ou bidirectionnelle.

**Version 2**

> Crée une relation de DimProduit[product_code] vers FactRetours[id_produit].

- **Amélioration :** Les colonnes exactes de la relation sont désignées.

**Version 3**

> Crée une relation de DimProduit[product_code], côté 1, vers FactRetours[id_produit], côté plusieurs.

- **Amélioration :** La cardinalité un-à-plusieurs est imposée.

**Version 4 — prompt de l’atelier**

> Crée uniquement une relation active de DimProduit[product_code], côté 1, vers FactRetours[id_produit], côté plusieurs. Utilise un filtrage à sens unique de DimProduit vers FactRetours.

- **Amélioration :** « Uniquement », relation active et filtrage à sens unique fixent le comportement attendu, sans autre création.

## Atelier 3 — Prompt A.6-1 — Audit du modèle

**Version 1**

> Le modèle est-il bon ?

- **Critique :** Avis global : Copilot peut aussi proposer ou appliquer des corrections.

**Version 2**

> Examine le modèle et liste les tables de faits, les dimensions et les relations actives.

- **Amélioration :** Un inventaire structuré remplace l’avis.

**Version 3 — prompt de l’atelier**

> Examine le modèle après les modifications. Liste uniquement les tables de faits, les dimensions, les relations actives et les anomalies restantes. Ne crée et ne modifie aucun objet.

- **Amélioration :** Les anomalies restantes complètent l’inventaire, et l’interdiction de créer ou de modifier garde l’audit en lecture seule.

## Atelier 3 — Prompt B.1-1 — Charger les sources CSV

**Version 1**

> Charge les données.

- **Critique :** Quelles données, avec quel outil, dans combien de cellules ? Copilot décidera seul.

**Version 2**

> Lis avec Spark les quatre fichiers `ventes_brut.csv`, `produits.csv`, `magasins.csv` et `retours.csv` dans `Files/atelier1`.

- **Amélioration :** Les sources et le moteur sont désignés.

**Version 3**

> Lis avec Spark les quatre fichiers `ventes_brut.csv`, `produits.csv`, `magasins.csv` et `retours.csv` dans `Files/atelier1`. Utilise `header=True` et `inferSchema=False`. Crée respectivement `df_ventes_raw`, `df_produits_raw`, `df_magasins_raw` et `df_retours_raw`.

- **Amélioration :** Lecture sans inférence et noms de variables imposés préparent les prompts suivants.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.1 — Charger les sources CSV`. Lis avec Spark les quatre fichiers `ventes_brut.csv`, `produits.csv`, `magasins.csv` et `retours.csv` dans `Files/atelier1`. Utilise `header=True` et `inferSchema=False`. Crée respectivement `df_ventes_raw`, `df_produits_raw`, `df_magasins_raw` et `df_retours_raw`. Affiche uniquement le nombre de lignes de chaque DataFrame. Ne transforme aucune donnée et ne crée aucune table. Limite la cellule à 25 lignes.

- **Amélioration :** Une seule cellule titrée, un affichage limité aux volumes et l’interdiction de transformer gardent l’étape courte et contrôlable.

## Atelier 3 — Prompt B.2-1 — Préparer `DimProduit`

**Version 1**

> Crée la dimension produit.

- **Critique :** Copilot complète le schéma avec des colonnes plausibles mais inexistantes, comme `product_name` ou `marque`.

**Version 2**

> Crée `df_dim_produit` à partir de `df_produits_raw`, dont le schéma exact est : `product_code`, `libelle_produit`, `categorie`, `prix_catalogue`.

- **Amélioration :** Le prompt est ancré dans le schéma réel.

**Version 3**

> Crée `df_dim_produit` à partir de `df_produits_raw`, dont le schéma exact est : `product_code`, `libelle_produit`, `categorie`, `prix_catalogue`. Utilise uniquement ces quatre colonnes. N’utilise pas `product_name`, `marque` ou une autre colonne non indiquée. Vérifie que `product_code` ne contient ni valeur nulle ni doublon et déclenche une erreur explicite sinon.

- **Amélioration :** Les interdits viennent de l’erreur observée, et le contrôle bloque une dimension invalide.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant exactement par `# Cellule B.2 — Préparer DimProduit`. Le schéma exact de `df_produits_raw` est : `product_code`, `libelle_produit`, `categorie`, `prix_catalogue`. Utilise uniquement ces quatre colonnes. N’utilise pas `product_name`, `marque` ou une autre colonne non indiquée. Applique `trim` aux trois colonnes texte, convertis `prix_catalogue` en `decimal(18,2)`, puis vérifie que `product_code` ne contient ni valeur nulle ni doublon. Si le contrôle échoue, déclenche une erreur explicite. Crée `product_key` avec `row_number`, dans l’ordre de `product_code`. Crée `df_dim_produit` avec `product_key`, `product_code`, `libelle_produit`, `categorie` et `prix_catalogue`. Affiche le nombre de lignes, le nombre de codes distincts et les cinq premières lignes. Ne crée aucune table. Limite la cellule à 25 lignes.

- **Amélioration :** Nettoyage, clé de substitution, colonnes de sortie, affichage de contrôle et limite de taille complètent la spécification.

## Atelier 3 — Prompt B.3-1 — Préparer `DimMagasin`

**Version 1**

> Crée la dimension magasin.

- **Critique :** Le doublon `MAG-004` sera conservé ou supprimé au hasard.

**Version 2**

> Crée `df_dim_magasin` à partir de `df_magasins_raw`, dont le schéma exact est : `store_code`, `nom_magasin`, `region`, `surface_m2`.

- **Amélioration :** Le prompt est ancré dans le schéma réel.

**Version 3**

> Crée `df_dim_magasin` à partir de `df_magasins_raw`, dont le schéma exact est : `store_code`, `nom_magasin`, `region`, `surface_m2`. Pour le doublon `MAG-004`, conserve la fiche dont `nom_magasin` ne contient pas `ancienne fiche`. Vérifie ensuite que `store_code` est unique.

- **Amélioration :** La règle métier du doublon est explicite et contrôlée.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.3 — Préparer DimMagasin`. Le schéma exact de `df_magasins_raw` est : `store_code`, `nom_magasin`, `region`, `surface_m2`. Utilise uniquement ces colonnes. Supprime les espaces autour des textes et convertis `surface_m2` en entier. Pour le doublon `MAG-004`, conserve la fiche dont `nom_magasin` ne contient pas `ancienne fiche`. Vérifie ensuite que `store_code` est unique. Crée `magasin_key` avec `row_number`, dans l’ordre de `store_code`, puis crée `df_dim_magasin`. Affiche le nombre de lignes, le nombre de codes distincts et la ligne `MAG-004` conservée. Ne crée aucune table. Limite la cellule à 25 lignes.

- **Amélioration :** Nettoyage des textes, typage, clé de substitution et affichage de la ligne conservée rendent le résultat vérifiable.

## Atelier 3 — Prompt B.4-1 — Nettoyer les ventes

**Version 1**

> Nettoie les ventes.

- **Critique :** « Nettoyer » n’est pas défini : doublons, dates, montants ? Copilot fera tout à la fois, ou rien de précis.

**Version 2**

> À partir de `df_ventes_raw`, conserve une seule ligne par `id_ligne` et convertis `date_vente` en acceptant `yyyy-MM-dd` et `dd/MM/yyyy`.

- **Amélioration :** Les règles de dédoublonnage et de conversion sont précises.

**Version 3**

> Le schéma exact de `df_ventes_raw` est : `id_ligne`, `id_vente`, `date_vente`, `id_magasin`, `id_produit`, `quantite`, `montant`, `canal`. Conserve une seule ligne par `id_ligne`. Convertis `date_vente` en acceptant `yyyy-MM-dd` et `dd/MM/yyyy`, convertis `quantite` en entier et supprime les espaces autour de `canal`. Ne traite pas encore `montant`.

- **Amélioration :** Ancrage dans le schéma et découpage de la tâche : les montants sont reportés à une autre cellule.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.4 — Nettoyer les ventes`. Le schéma exact de `df_ventes_raw` est : `id_ligne`, `id_vente`, `date_vente`, `id_magasin`, `id_produit`, `quantite`, `montant`, `canal`. Utilise uniquement ces colonnes. Conserve une seule ligne par `id_ligne`. Convertis `date_vente` en acceptant `yyyy-MM-dd` et `dd/MM/yyyy`, convertis `quantite` en entier et supprime les espaces autour de `canal`. Crée `df_ventes_etape` sans modifier `df_ventes_raw`. Conserve `id_vente`, `id_magasin`, `id_produit` et `montant`. Affiche le nombre de lignes, de dates invalides et de quantités invalides. Ne traite pas encore `montant`. Ne crée aucune table. Limite la cellule à 25 lignes.

- **Amélioration :** Les compteurs de contrôle, la variable de sortie et la limite de taille rendent l’étape vérifiable.

## Atelier 3 — Prompt B.5-1 — Normaliser les montants

**Version 1**

> Convertis les montants.

- **Critique :** Quatre formats coexistent : Copilot appliquera une seule règle et faussera une partie des valeurs.

**Version 2**

> À partir de `df_ventes_etape`, convertis `montant` en `decimal(18,2)` selon ces règles : `1.234,56` devient `1234.56`, `1,234.56` devient `1234.56`, une virgule seule est décimale et un point seul reste décimal.

- **Amélioration :** Une règle explicite est donnée pour chaque format.

**Version 3**

> À partir de `df_ventes_etape`, convertis `montant` en `decimal(18,2)` selon ces règles : `1.234,56` devient `1234.56`, `1,234.56` devient `1234.56`, une virgule seule est décimale et un point seul reste décimal. Conserve la valeur d’origine. Crée une colonne booléenne `montant_invalide` quand une valeur non vide ne peut pas être convertie. Ne supprime aucune ligne invalide.

- **Amélioration :** La valeur d’origine est tracée et les échecs restent visibles au lieu d’être supprimés.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.5 — Normaliser les montants`. À partir de `df_ventes_etape`, convertis `montant` en `decimal(18,2)` selon ces règles : `1.234,56` devient `1234.56`, `1,234.56` devient `1234.56`, une virgule seule est décimale et un point seul reste décimal. Conserve la valeur d’origine. Crée une colonne booléenne `montant_invalide` quand une valeur non vide ne peut pas être convertie. Crée `df_ventes_clean`. Pour compter les valeurs invalides, convertis le booléen en `1` ou `0` avant d’utiliser `sum`. Affiche ce nombre et la somme de `montant_decimal`. Ne supprime aucune ligne invalide et ne crée aucune table. Limite la cellule à 30 lignes.

- **Amélioration :** La consigne sur `sum` anticipe l’erreur de type, et la somme affichée sert de contrôle chiffré.

## Atelier 3 — Prompt B.5-2 — Corriger le comptage des montants invalides

**Version 1**

> Ça ne marche pas, corrige.

- **Critique :** Sans erreur ni cible, Copilot régénère toute la cellule et peut casser la normalisation.

**Version 2**

> Corrige uniquement le calcul du nombre de montants invalides dans la cellule B.5.

- **Amélioration :** La cible de la correction est désignée.

**Version 3**

> Corrige uniquement le calcul du nombre de montants invalides dans la cellule B.5. `montant_invalide` est de type Boolean et ne peut pas être additionné directement avec `sum()` dans Spark.

- **Amélioration :** La cause de l’erreur est fournie à Copilot.

**Version 4 — prompt de l’atelier**

> Corrige uniquement le calcul du nombre de montants invalides dans la cellule B.5. `montant_invalide` est de type Boolean et ne peut pas être additionné directement avec `sum()` dans Spark. Remplace uniquement cette agrégation par `F.sum(F.when(F.col("montant_invalide"), 1).otherwise(0))`. Conserve les quatre règles de normalisation, la valeur d’origine, `montant_decimal`, `montant_invalide` et `df_ventes_clean`. N’ajoute pas une nouvelle cellule.

- **Amélioration :** Le remplacement exact et la liste des éléments à conserver protègent le reste de la cellule.

## Atelier 3 — Prompt B.6-1 — Construire `FactVentes`

**Version 1**

> Crée la table de faits des ventes.

- **Critique :** Sources, jointures et colonnes restent à deviner.

**Version 2**

> À partir de `df_ventes_clean`, joins `df_dim_produit` avec `id_produit = product_code`, puis `df_dim_magasin` avec `id_magasin = store_code`.

- **Amélioration :** Les conditions de jointure sont explicites.

**Version 3**

> À partir de `df_ventes_clean`, joins `df_dim_produit` avec `id_produit = product_code`, puis `df_dim_magasin` avec `id_magasin = store_code`. Crée `df_fact_ventes` avec uniquement `id_ligne`, `id_vente`, la date convertie renommée `date_vente`, `product_key`, `magasin_key`, la quantité convertie renommée `quantite`, `montant_decimal` renommé `montant` et le canal nettoyé renommé `canal`.

- **Amélioration :** La projection et les renommages du fait sont fixés.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.6 — Construire FactVentes`. À partir de `df_ventes_clean`, joins `df_dim_produit` avec `id_produit = product_code`, puis `df_dim_magasin` avec `id_magasin = store_code`. Crée `df_fact_ventes` avec uniquement `id_ligne`, `id_vente`, la date convertie renommée `date_vente`, `product_key`, `magasin_key`, la quantité convertie renommée `quantite`, `montant_decimal` renommé `montant` et le canal nettoyé renommé `canal`. Affiche le nombre de lignes et le nombre de clés de dimension absentes. Ne crée aucune table. Limite la cellule à 25 lignes.

- **Amélioration :** Le contrôle des clés de dimension absentes et la limite de taille rendent l’étape vérifiable.

## Atelier 3 — Prompt B.7-1 — Construire `FactRetours`

**Version 1**

> Crée la table des retours.

- **Critique :** Une jointure sur `id_vente` seul multiplierait les retours d’une vente à plusieurs produits.

**Version 2**

> Joins `df_retours_raw` à `df_ventes_clean` sur `id_vente` et `id_produit`.

- **Amélioration :** La clé composite de rapprochement est imposée.

**Version 3**

> Le schéma exact de `df_retours_raw` est : `id_retour`, `id_vente`, `id_produit`, `quantite_retour`, `motif`. Convertis `quantite_retour` en entier. Joins `df_retours_raw` à `df_ventes_clean` sur `id_vente` et `id_produit` afin de récupérer `id_ligne`, la date de vente convertie et `id_magasin`. Joins ensuite `df_dim_produit` et `df_dim_magasin`.

- **Amélioration :** Ancrage dans le schéma et chaîne de jointures complète.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.7 — Construire FactRetours`. Le schéma exact de `df_retours_raw` est : `id_retour`, `id_vente`, `id_produit`, `quantite_retour`, `motif`. Convertis `quantite_retour` en entier. Joins `df_retours_raw` à `df_ventes_clean` sur `id_vente` et `id_produit` afin de récupérer `id_ligne`, la date de vente convertie et `id_magasin`. Joins ensuite `df_dim_produit` et `df_dim_magasin`. Crée `df_fact_retours` avec `id_retour`, `id_vente`, `id_ligne`, la date renommée `date_vente_origine`, `product_key`, `magasin_key`, `quantite_retour` et `motif`. Affiche le nombre de lignes et le nombre de retours sans correspondance. Ne crée aucune table. Limite la cellule à 30 lignes.

- **Amélioration :** Les colonnes de sortie, le renommage de la date et le comptage des retours sans correspondance rendent le fait contrôlable.

## Atelier 3 — Prompt B.8-1 — Valider avant écriture

**Version 1**

> Vérifie que tout est bon.

- **Critique :** Critère subjectif : Copilot répondra par un avis, pas par des chiffres.

**Version 2**

> Construis un tableau de contrôle pour `df_dim_produit`, `df_dim_magasin`, `df_fact_ventes` et `df_fact_retours`.

- **Amélioration :** Les objets à contrôler sont nommés.

**Version 3**

> Construis un tableau de contrôle pour `df_dim_produit`, `df_dim_magasin`, `df_fact_ventes` et `df_fact_retours`. Affiche pour chaque DataFrame son nom, son nombre de lignes, le nombre de clés principales distinctes et leur différence. Utilise respectivement `product_key`, `magasin_key`, `id_ligne` et `id_retour` comme clés principales.

- **Amélioration :** Les mesures et la clé de chaque table sont précisées.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.8 — Valider le modèle préparé`. Construis un tableau de contrôle pour `df_dim_produit`, `df_dim_magasin`, `df_fact_ventes` et `df_fact_retours`. Affiche pour chaque DataFrame son nom, son nombre de lignes, le nombre de clés principales distinctes et leur différence. Utilise respectivement `product_key`, `magasin_key`, `id_ligne` et `id_retour` comme clés principales. Affiche aussi le nombre de lignes des faits ayant une clé de dimension absente. Ne modifie aucune donnée et ne crée aucune table. Limite la cellule à 30 lignes.

- **Amélioration :** Le contrôle des clés de dimension absentes complète le tableau, sans aucune modification de données.

## Atelier 3 — Prompt B.9-1 — Persister les tables `gold`

**Version 1**

> Enregistre les tables.

- **Critique :** Où, dans quel format, avec quel mode ? Copilot peut écraser d’autres tables.

**Version 2**

> Enregistre en Delta avec `mode("overwrite")` et `saveAsTable` : `df_dim_produit` dans `gold.dim_produit`, `df_dim_magasin` dans `gold.dim_magasin`, `df_fact_ventes` dans `gold.fact_ventes` et `df_fact_retours` dans `gold.fact_retours`.

- **Amélioration :** Format, mode et correspondance DataFrame-table sont explicites.

**Version 3**

> Crée le schéma `gold` s’il n’existe pas. Enregistre en Delta avec `mode("overwrite")` et `saveAsTable` : `df_dim_produit` dans `gold.dim_produit`, `df_dim_magasin` dans `gold.dim_magasin`, `df_fact_ventes` dans `gold.fact_ventes` et `df_fact_retours` dans `gold.fact_retours`. N’écris et ne supprime aucune autre table.

- **Amélioration :** Le schéma cible est préparé et les autres tables sont protégées.

**Version 4 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.9 — Persister les tables gold`. Vérifie d’abord que le Lakehouse par défaut accepte les schémas. S’il ne les accepte pas, arrête la cellule avec un message explicite sans écrire de table. Sinon, crée le schéma `gold` s’il n’existe pas. Enregistre en Delta avec `mode("overwrite")` et `saveAsTable` : `df_dim_produit` dans `gold.dim_produit`, `df_dim_magasin` dans `gold.dim_magasin`, `df_fact_ventes` dans `gold.fact_ventes` et `df_fact_retours` dans `gold.fact_retours`. N’écris et ne supprime aucune autre table. Affiche le nom des quatre tables enregistrées. Limite la cellule à 25 lignes.

- **Amélioration :** La vérification préalable des schémas arrête la cellule proprement si l’écriture est impossible.

## Atelier 3 — Prompt B.10-1 — Vérifier les tables `gold`

**Version 1**

> Les tables sont-elles bien enregistrées ?

- **Critique :** Question d’avis : Copilot peut répondre sans relire les tables.

**Version 2**

> Relis avec `spark.table` les quatre tables `gold.dim_produit`, `gold.dim_magasin`, `gold.fact_ventes` et `gold.fact_retours`, puis affiche leur nombre de lignes.

- **Amélioration :** La relecture porte sur les tables persistées, pas sur les DataFrames en mémoire.

**Version 3 — prompt de l’atelier**

> Ajoute une seule cellule commençant par `# Cellule B.10 — Vérifier les tables gold`. Relis avec `spark.table` les quatre tables `gold.dim_produit`, `gold.dim_magasin`, `gold.fact_ventes` et `gold.fact_retours`. Affiche uniquement leur nom et leur nombre de lignes. Ne transforme, ne remplace et ne supprime aucune donnée. Limite la cellule à 20 lignes.

- **Amélioration :** Une cellule titrée, un affichage limité et l’interdiction de modifier gardent ce contrôle en lecture seule.
