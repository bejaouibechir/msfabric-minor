"""qualite_pandas.py — Nettoyage des mesures EnergiaNord avec pandas (Atelier 2)."""
import pandas as pd

CODES = (-999, -888, -777)
FORMATS = ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S")


def parser_dates(serie: pd.Series) -> pd.Series:
    """Convertit des timestamps en 3 formats ; NaT si aucun format ne convient."""
    resultat = pd.Series(pd.NaT, index=serie.index, dtype="datetime64[us]")
    for fmt in FORMATS:
        resultat = resultat.fillna(pd.to_datetime(serie, format=fmt, errors="coerce"))
    return resultat


def nettoyer(brut: pd.DataFrame) -> pd.DataFrame:
    """Doublons exacts, dates, codes erreur en NaN, tri par site et date."""
    return (
        brut
        .drop_duplicates()
        .assign(
            timestamp=lambda d: parser_dates(d["timestamp"]),
            conso_mw=lambda d: d["conso_mw"].mask(d["conso_mw"].isin(CODES)),
        )
        .sort_values(["site_id", "timestamp"], ignore_index=True)
    )


def resume_sites(propre: pd.DataFrame) -> pd.DataFrame:
    """Mesures, valides, taux d'anomalies et consommation moyenne par site."""
    return propre.groupby("site_id", observed=True).agg(
        mesures=("conso_mw", "size"),
        valides=("conso_mw", "count"),
        moyenne_mw=("conso_mw", "mean"),
    ).assign(taux_anomalies=lambda d: (1 - d["valides"] / d["mesures"]).round(3)).round(3)
