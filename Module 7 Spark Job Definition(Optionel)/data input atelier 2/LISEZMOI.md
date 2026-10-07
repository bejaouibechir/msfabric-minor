# Générateur de données — Atelier 2

Le script écrit un fichier JSON Lines par lot et un rapport comptant exactement
les valeurs nulles, les valeurs hors plage, les doublons et les timestamps au
format hétérogène.

```powershell
python .\generer_donnees_atelier2.py --out .\sortie --lots 3 --lignes-par-lot 100 --intervalle 0
```

Commande de référence de l'Atelier 2 :

```powershell
python .\generer_donnees_atelier2.py --out .\sortie_reference --lots 5 --lignes-par-lot 200 --seed 20251002 --intervalle 0
```

Cette commande produit 5 fichiers, 1 000 lignes et le rapport réel suivant :
50 valeurs nulles, 55 valeurs hors plage, 35 doublons et 55 timestamps
hétérogènes. Déposez d'abord les cinq lots dans `Files/landing_capteurs/`, puis
conservez les lots supplémentaires hors de ce dossier jusqu'à l'étape de reprise.

Arguments : `--out`, `--lots`, `--lignes-par-lot`, `--seed` et `--intervalle`
(secondes ; `0` écrit les lots immédiatement). Les fichiers se nomment
`mesures_YYYYMMDDTHHMMSSZ_lotNNN.jsonl`.
