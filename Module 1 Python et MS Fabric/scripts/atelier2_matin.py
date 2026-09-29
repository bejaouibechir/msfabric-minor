"""Atelier 2 (matin : venv-base) - cellules de reference. Chaque bloc "# %%" = une cellule du notebook atelier2."""

# %% Cellule 1 — Vérification de l'environnement
# === CELLULE 1 : Vérification de l'environnement ===
import sys
from pathlib import Path

import numpy as np

print(f"Python       : {sys.version.split()[0]}")
print(f"Interpréteur : {sys.executable}")
print(f"NumPy        : {np.__version__}")
print(f"Dossier      : {Path.cwd().name}")
print(f"Fichiers     : {sorted(p.name for p in Path('data').glob('*.csv'))}")
print(f"Module A1    : {Path('energie_utils.py').exists()}")

# %% Cellule 2 — Charger le fichier de 30 jours
# === CELLULE 2 : Charger les mesures ===
from energie_utils import convertir_mesure, lire_csv, parse_timestamp, qualifier_mesure

lignes = list(lire_csv("data/consommation_30jours.csv"))
print(len(lignes), "lignes")
print(type(lignes).__name__, type(lignes[0]).__name__)
print(lignes[0])

# %% Cellule 3 — Listes : indexation, tranches, tri
# === CELLULE 3 : Listes ===
conso = [convertir_mesure(l["consumption_mw"]) for l in lignes[:10]]
print(conso)
print(conso[0], conso[-1], conso[2:5], conso[::3])

valides = [c for c in conso if c is not None and c >= 0]
print(sorted(valides, reverse=True)[:3])
print(min(valides), max(valides), round(sum(valides) / len(valides), 3))

# %% Cellule 4 — Listes : ajout, retrait et méthodes utiles
# === CELLULE 4 : Méthodes de liste ===
sites_vus = []
for l in lignes:
    if l["site_id"] not in sites_vus:
        sites_vus.append(l["site_id"])
print(sites_vus)

sites_vus.extend(["SITE_TEST_999"])
sites_vus.insert(0, "SITE_ENTETE")
print(sites_vus.pop(), sites_vus.index("SITE_IND_001"), sites_vus.count("SITE_IND_001"))
sites_vus.remove("SITE_ENTETE")
print(len(sites_vus))

# %% Cellule 5 — Mutabilité : alias, copie superficielle, copie profonde
# === CELLULE 5 : Alias et copies ===
import copy

a = [{"site": "SITE_IND_001", "mw": 2.5}, {"site": "SITE_COM_001", "mw": 1.0}]
alias = a
superficielle = a.copy()
profonde = copy.deepcopy(a)

a[0]["mw"] = 99.0
a.append({"site": "SITE_RES_001", "mw": 0.4})
print(len(alias), len(superficielle), len(profonde))
print(alias[0]["mw"], superficielle[0]["mw"], profonde[0]["mw"])

# %% Cellule 6 — Tuples : `namedtuple` (hier) et `dataclass` (aujourd'hui)
# === CELLULE 6 : namedtuple et dataclass ===
from collections import namedtuple
from dataclasses import dataclass

MesureNT = namedtuple("MesureNT", ["site_id", "mw", "statut"])     # Hier

@dataclass(frozen=True, slots=True)                                 # Aujourd'hui (3.10+)
class Mesure:
    site_id: str
    mw: float | None
    statut: str = "OK"

    def est_valide(self) -> bool:
        return self.mw is not None and self.mw >= 0

nt = MesureNT("SITE_IND_001", 2.5, "OK")
dc = Mesure("SITE_IND_001", 2.5)
print(nt, "|", dc)
print(nt.mw, dc.mw, dc.est_valide())

try:
    dc.mw = 0.0
except AttributeError as erreur:
    print(f"Modification refusée : {type(erreur).__name__}")

# %% Cellule 7 — Dictionnaires : lecture sûre et valeurs par défaut
# === CELLULE 7 : Dictionnaires ===
capacites = {"SITE_IND_001": 5.0, "SITE_IND_002": 3.5, "SITE_COM_001": 2.0}

print(capacites["SITE_IND_001"], capacites.get("SITE_XXX"), capacites.get("SITE_XXX", 0.0))
try:
    capacites["SITE_XXX"]
except KeyError as erreur:
    print(f"KeyError : {erreur}")

capacites.setdefault("SITE_COM_002", 1.5)
print(list(capacites.items())[-1], len(capacites))

# %% Cellule 8 — Compter et regrouper : `Counter` et `defaultdict`
# === CELLULE 8 : Counter et defaultdict ===
from collections import Counter, defaultdict

par_site = Counter(l["site_id"] for l in lignes)
print(par_site.most_common(3))

groupes = defaultdict(list)
for l in lignes:
    v = convertir_mesure(l["consumption_mw"])
    if qualifier_mesure(v) == "VALIDE":
        groupes[l["site_id"]].append(v)

for site_id, valeurs in sorted(groupes.items()):
    print(f"{site_id} : {len(valeurs):>4} mesures valides, moyenne {sum(valeurs)/len(valeurs):.3f} MW")

# %% Cellule 9 — Ensembles : doublons et comparaisons
# === CELLULE 9 : Ensembles ===
referentiel = {l["site_id"] for l in lire_csv("data/sites_reference.csv")}
recus = {l["site_id"] for l in lignes}
print(len(referentiel), len(recus), referentiel == recus)
print(sorted(referentiel - {"SITE_RES_002"}), "|", sorted({"A", "B"} ^ {"B", "C"}))

jours = {parse_timestamp(l["timestamp"]).day for l in lignes}
print(len(jours), sorted(set(range(1, 32)) - jours))

uniques = {tuple(l.values()) for l in lignes}
print(len(lignes), "lignes ->", len(uniques), "uniques :", len(lignes) - len(uniques), "doublons")

# %% Cellule 10 — Structures imbriquées et JSON
# === CELLULE 10 : Structures imbriquées ===
import json
from datetime import datetime

arbre = defaultdict(lambda: defaultdict(list))
for l in lignes[:400]:
    v = convertir_mesure(l["consumption_mw"])
    if qualifier_mesure(v) == "VALIDE":
        jour = parse_timestamp(l["timestamp"]).date().isoformat()
        arbre[l["site_id"]][jour].append(v)

site = "SITE_IND_001"
premier_jour = sorted(arbre[site])[0]
print(site, premier_jour, arbre[site][premier_jour])

extrait = {"site": site, "genere_le": datetime(2025, 2, 1, 8, 0),
           "jour": premier_jour, "valeurs": arbre[site][premier_jour][:3]}
texte = json.dumps(extrait, indent=2, ensure_ascii=False, default=str)
print(texte)
print(json.loads(texte)["genere_le"], type(json.loads(texte)["genere_le"]).__name__)

# %% Cellule 11 — Choisir la bonne structure : coût de la recherche
# === CELLULE 11 : Liste, ensemble, dictionnaire : coût de `in` ===
import timeit

cles_liste = [f"K{i:05d}" for i in range(20_000)]
cles_set = set(cles_liste)
cles_dict = dict.fromkeys(cles_liste, 0)
cherche = "K19999"

for nom, struct in [("liste", cles_liste), ("ensemble", cles_set), ("dictionnaire", cles_dict)]:
    duree = timeit.timeit(lambda: cherche in struct, number=2_000) / 2_000
    print(f"{nom:<13}: {duree * 1e6:10.2f} µs par recherche")

# %% Cellule 12 — `pairwise`, `batched` et `nlargest`
# === CELLULE 12 : itertools et heapq ===
import heapq
from itertools import islice, pairwise

serie = groupes["SITE_COM_001"][:8]
print([round(b - a, 3) for a, b in pairwise(serie)])                    # variations consécutives

try:
    from itertools import batched                                        # 3.12+
except ImportError:
    def batched(iterable, n):                                            # repli pour 3.11
        it = iter(iterable)
        while lot := tuple(islice(it, n)):
            yield lot

lots = list(batched(range(10), 4))
print(lots)
print(heapq.nlargest(3, groupes["SITE_IND_001"]))

# %% Cellule 13 — Du liste au tableau : `dtype`, `shape`, mémoire
# === CELLULE 13 : Premiers tableaux NumPy ===
import sys

valeurs = [float(v) for v in groupes["SITE_IND_001"]]
tab = np.array(valeurs)

print(tab.dtype, tab.shape, tab.ndim, tab.size)
print(f"liste : {sys.getsizeof(valeurs) + sum(sys.getsizeof(v) for v in valeurs):>7} octets")
print(f"array : {tab.nbytes:>7} octets")
print(np.array([1, 2.5, 3]).dtype, np.array([1, 2, 3]).dtype, np.array([1, "a"]).dtype)

# %% Cellule 14 — Créer des tableaux : `arange`, `linspace`, `zeros`, `reshape`
# === CELLULE 14 : Création et forme ===
heures = np.arange(24)
print(heures)
print(np.linspace(0, 1, 5))
print(np.zeros((2, 3)), np.full((2, 2), np.nan), sep="\n")

grille = np.arange(24).reshape(4, 6)
print(grille)
print(grille.shape, grille.T.shape, grille.reshape(-1).shape)

# %% Cellule 15 — Construire la matrice sites × heures
# === CELLULE 15 : La matrice de consommation ===
sites = sorted(referentiel)
rang = {s: i for i, s in enumerate(sites)}
debut = parse_timestamp("2025-01-01 00:00:00")

conso = np.full((len(sites), 30 * 24), np.nan)
for l in lignes:
    ts = parse_timestamp(l["timestamp"])
    heure_abs = (ts - debut).days * 24 + ts.hour
    v = convertir_mesure(l["consumption_mw"])
    if qualifier_mesure(v) in ("VALIDE", "NEGATIVE"):
        conso[rang[l["site_id"]], heure_abs] = v

print(sites)
print(conso.shape, conso.dtype, f"{conso.nbytes / 1024:.1f} Ko")
print("valeurs NaN :", int(np.isnan(conso).sum()), "sur", conso.size)

# %% Cellule 16 — Indexation, tranches et masques
# === CELLULE 16 : Indexation ===
print(conso[0, :6])
print(conso[:, 12].round(2))                     # midi du 1er jour, 6 sites
print(conso[1, 24:48].shape)                     # 2e site, 2e jour
print(conso[[0, 5], :3].round(2))                # indexation par liste (fancy)

print(conso[3][conso[3] > 3.5].round(2))         # valeurs > 3,5 MW du site 4 (capacité 3,5 MW)

# %% Cellule 17 — Vectorisation : boucle contre tableau
# === CELLULE 17 : Taux de charge — boucle et vectorisation ===
cap = np.array([float(l["capacity_mw"]) for l in sorted(lire_csv("data/sites_reference.csv"),
                                                          key=lambda s: s["site_id"])])
print(cap)

def taux_boucle():
    return [[c / cap[i] for c in ligne] for i, ligne in enumerate(conso.tolist())]

def taux_numpy():
    return conso / cap[:, None]

t_boucle = timeit.timeit(taux_boucle, number=20) / 20
t_numpy = timeit.timeit(taux_numpy, number=20) / 20
print(f"boucle : {t_boucle * 1e3:7.2f} ms | numpy : {t_numpy * 1e3:7.3f} ms | x{t_boucle / t_numpy:.0f}")
print(np.allclose(np.array(taux_boucle()), taux_numpy(), equal_nan=True))

# %% Cellule 18 — Broadcasting : combiner des formes différentes
# === CELLULE 18 : Broadcasting ===
taux = conso / cap[:, None]
print(conso.shape, cap.shape, cap[:, None].shape, "->", taux.shape)

try:
    conso / cap
except ValueError as erreur:
    print(f"ValueError : {erreur}")

moyenne_site = np.nanmean(conso, axis=1, keepdims=True)
ecart = conso - moyenne_site
print(moyenne_site.shape, ecart.shape, np.nanmean(ecart, axis=1).round(6))

# %% Cellule 19 — Valeurs manquantes : `NaN` et fonctions `nan*`
# === CELLULE 19 : NaN ===
site0 = conso[0]
print(np.mean(site0), np.nanmean(site0).round(3))
print(np.nan == np.nan, np.isnan(np.nan))

manquants = np.isnan(conso).sum(axis=1)
print(dict(zip(sites, manquants.tolist())))
print((np.isnan(conso).mean(axis=1) * 100).round(1))

# %% Cellule 20 — Agrégations par axe : le profil horaire moyen
# === CELLULE 20 : Profil horaire moyen ===
cube = conso.reshape(6, 30, 24)
profil = np.nanmean(cube, axis=1)                 # moyenne sur les 30 jours -> (6, 24)
print(cube.shape, profil.shape)

for site, courbe in zip(sites, profil):
    print(f"{site} : pointe à {courbe.argmax():02d}h ({courbe.max():.2f} MW), creux à {courbe.argmin():02d}h ({courbe.min():.2f} MW)")

# %% Cellule 21 — Détecter les anomalies : `where`, `clip`, percentiles
# === CELLULE 21 : Pics aberrants ===
depasse = conso > cap[:, None]                    # NaN > x vaut False
print("pics par site :", dict(zip(sites, depasse.sum(axis=1).tolist())))

propre = np.where(depasse, np.nan, conso)
print(np.isnan(propre).sum() - np.isnan(conso).sum(), "valeurs neutralisées")

plafonne = np.clip(conso, 0, cap[:, None])
print(np.nanmax(conso, axis=1).round(2), np.nanmax(plafonne, axis=1).round(2), sep="\n")
print(np.nanpercentile(propre, [50, 95, 99]).round(3))

# %% Cellule 22 — Tri, `argsort` et corrélation
# === CELLULE 22 : Top pics et corrélation ===
ind1 = propre[0]
ordre = np.argsort(np.nan_to_num(ind1, nan=-1))[::-1][:3]
print([(int(i // 24 + 1), int(i % 24), round(float(ind1[i]), 2)) for i in ordre])   # (jour, heure, MW)

ok = ~np.isnan(propre[0]) & ~np.isnan(propre[1])
print(np.corrcoef(propre[0][ok], propre[1][ok]).round(3))

ok = ~np.isnan(propre[0]) & ~np.isnan(propre[4])
print(np.corrcoef(propre[0][ok], propre[4][ok])[0, 1].round(3))

# %% Cellule 23 — Nombres aléatoires : `np.random.seed` (hier), `default_rng` (aujourd'hui)
# === CELLULE 23 : Générateurs aléatoires ===
np.random.seed(42)                                # Hier
ancien = np.random.normal(230, 4, 3).round(1)

rng = np.random.default_rng(42)                   # Aujourd'hui
nouveau = rng.normal(230, 4, 3).round(1)
print(ancien, nouveau)

rng = np.random.default_rng(42)
print(np.array_equal(nouveau, rng.normal(230, 4, 3).round(1)))
bruit = rng.normal(0, 0.05, size=(6, 24))
print(bruit.shape, rng.choice(sites, size=3, replace=False))

# %% Cellule 24 — Sauvegarder : `.npy`, `.npz`, `savetxt`
# === CELLULE 24 : Sauvegarde ===
Path("out").mkdir(exist_ok=True)
np.save("out/conso_30jours.npy", conso)
np.savez_compressed("out/conso_30jours.npz", conso=conso, capacites=cap, sites=np.array(sites))
np.savetxt("out/profil_horaire.csv", profil, delimiter=";", fmt="%.3f")

for nom in ("conso_30jours.npy", "conso_30jours.npz", "profil_horaire.csv"):
    print(f"{nom:<20} {Path('out', nom).stat().st_size:>7} octets")

relu = np.load("out/conso_30jours.npy")
print(np.array_equal(relu, conso, equal_nan=True), np.load("out/conso_30jours.npz")["sites"][:2])

# %% Cellule 25 — NumPy 1.x et NumPy 2.x : ce qui a disparu
# === CELLULE 25 : Alias supprimés dans NumPy 2 ===
print("NumPy", np.__version__)
for ancien, nouveau in [("float_", "float64"), ("NaN", "nan"), ("product", "prod"), ("in1d", "isin")]:
    print(f"np.{ancien:<8} {'présent' if hasattr(np, ancien) else 'ABSENT ':<8} -> np.{nouveau:<8} {'présent' if hasattr(np, nouveau) else 'ABSENT'}")

print(np.isin([1, 5], [1, 2, 3]), np.prod([2, 3, 4]))
