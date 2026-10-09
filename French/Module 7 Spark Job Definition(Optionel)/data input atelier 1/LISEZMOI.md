# Générateur de données — Atelier 1

Ce script produit les trois tableaux JSON attendus par le mode `files` du Spark Job :
`besoins.json`, `production-solaire.json` et `production-eolienne.json`.

```powershell
python .\generer_donnees_atelier1.py --out .\sortie --lignes 30
```

Arguments : `--out` (défaut `./sortie`), `--seed` (défaut `20251001`) et
`--lignes` (défaut `30`). Avec les valeurs par défaut, le contenu reproduit les
trois réponses JSON de l'API T08. Chargez ensuite les fichiers dans
`Files/landing_sjd/` du lakehouse.
