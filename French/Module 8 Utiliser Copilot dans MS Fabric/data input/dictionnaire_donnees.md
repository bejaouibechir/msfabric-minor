# Dictionnaire des données — Maison Lumière

## `ventes_brut.csv`

| Colonne      | Sens métier                     | Type attendu après nettoyage | Rôle                                              |
| ------------ | ------------------------------- | ---------------------------- | ------------------------------------------------- |
| `id_ligne`   | Identifiant d’une ligne produit | chaîne                       | **Clé de ligne**                                  |
| `id_vente`   | Identifiant du ticket de caisse | chaîne                       | **Clé de vente**, répétée sur plusieurs produits  |
| `date_vente` | Date du ticket                  | date                         | Formats bruts ISO et français                     |
| `id_magasin` | Magasin ayant réalisé la vente  | chaîne                       | À rapprocher de `magasins.store_code`             |
| `id_produit` | Produit vendu                   | chaîne                       | À rapprocher de `produits.product_code`           |
| `quantite`   | Quantité vendue                 | entier                       | Strictement positive                              |
| `montant`    | Montant TTC de la ligne         | décimal                      | Formats point, virgule et séparateurs de milliers |
| `canal`      | Origine de la commande          | chaîne                       | `Magasin` ou `Click & Collect`                    |

## `magasins.csv`

| Colonne       | Sens métier           | Rôle                                                     |
| ------------- | --------------------- | -------------------------------------------------------- |
| `store_code`  | Code magasin          | **Clé attendue**, mais une duplication volontaire existe |
| `nom_magasin` | Libellé du magasin    | Attribut descriptif                                      |
| `region`      | Région administrative | Axe d’analyse                                            |
| `surface_m2`  | Surface commerciale   | Attribut numérique                                       |

## `produits.csv`

| Colonne           | Sens métier     | Rôle                |
| ----------------- | --------------- | ------------------- |
| `product_code`    | Code produit    | **Clé produit**     |
| `libelle_produit` | Nom du produit  | Attribut descriptif |
| `categorie`       | Famille produit | Axe d’analyse       |
| `prix_catalogue`  | Prix catalogue  | Valeur de référence |

## `retours.csv`

| Colonne           | Sens métier           | Rôle                                             |
| ----------------- | --------------------- | ------------------------------------------------ |
| `id_retour`       | Identifiant du retour | Clé du retour                                    |
| `id_vente`        | Ticket d’origine      | Insuffisant seul pour retrouver la ligne produit |
| `id_produit`      | Produit retourné      | Complète la clé de rapprochement                 |
| `quantite_retour` | Quantité retournée    | Mesure                                           |
| `motif`           | Motif déclaré         | Attribut descriptif                              |

## Contrat reproductible du générateur

- **Graine :** `20261012`.
- **Volume brut :** 60 000 lignes de ventes.
- **Doublons exacts :** 500 lignes ; 59 500 lignes restent après dédoublonnage sur `id_ligne`.
- **Échantillon trompeur :** les 5 000 premières lignes utilisent uniquement une date ISO et un montant simple avec point décimal.
- **Dates brutes :** 35 278 ISO et 24 722 françaises, dont 10 020 à jour inférieur ou égal à 12.
- **Montants bruts :** 35 777 simples à point, 14 128 à virgule, 6 051 groupés européens et 4 044 groupés américains.
- **Somme correcte :** 111 350 063,34 EUR après dédoublonnage et conversion.
- **Dimension magasins :** 5 010 ventes uniques concernent `MAG-004` ; une jointure avec la dimension non dédupliquée produit 64 510 lignes.
- **Retours :** 3 000 lignes ; `id_vente` seul produit 9 000 correspondances, contre 3 000 avec `id_vente` + `id_produit`.
