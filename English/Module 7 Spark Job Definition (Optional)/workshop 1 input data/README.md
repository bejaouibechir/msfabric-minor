# Data Generator — Workshop 1

This script produces the three JSON tables expected by the mode`files`Spark Job:
`besoins.json`, `production-solaire.json`and`production-eolienne.json`.

```powershell
python .\generate_workshop1_data.py --out .\sortie --lignes 30
```

Arguments : `--out`(default`./sortie`), `--seed`(default`20251001`) and
`--lignes`(default`30`). With default values, the content reproduces the
Three JSON responses from API T08. Then load the files in
`Files/landing_sjd/`Lakehouse.
