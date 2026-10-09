# Data Generator — Workshop 2

The script writes a JSON Lines file by lot and a report counting exactly
zero values, off-range values, duplicates and timestamps at
heterogeneous format.

```powershell
python .\generate_workshop2_data.py --out .\sortie --lots 3 --lignes-par-lot 100 --intervalle 0
```

Workshop 2 Reference Command:

```powershell
python .\generate_workshop2_data.py --out .\sortie_reference --lots 5 --lignes-par-lot 200 --seed 20251002 --intervalle 0
```

This command produces 5 files, 1,000 lines and the following actual report:
50 null values, 55 off-range values, 35 duplicates and 55 timestamps
heterogeneous. First place the five lots in`Files/landing_capteurs/`then
Keep the additional batches out of this folder until the recovery step.

Arguments:`--out`,`--lots`,`--lignes-par-lot`,`--seed`and`--intervalle`
(secondes ; `0`writes lots immediately). Files are named
`mesures_YYYYMMDDTHHMMSSZ_lotNNN.jsonl`.
