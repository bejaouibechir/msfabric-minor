"""Atelier 1 - Python pour Microsoft Fabric : cellules de reference.

Chaque bloc "# %%" correspond a une cellule du notebook atelier1_langage.ipynb.
Execution complete : python atelier1_langage.py (depuis le dossier formation_python_fabric).
"""

# %% Cellule 1 — Vérification de l'environnement
# === CELLULE 1 : Vérification de l'environnement ===
import platform
import sys
from pathlib import Path

print(f"Python         : {sys.version.split()[0]}")
print(f"Implémentation : {platform.python_implementation()}")
print(f"Système        : {platform.system()} {platform.machine()}")
print(f"Interpréteur   : {sys.executable}")
print(f"Dossier actif  : {Path.cwd()}")
print(f"Dans un venv   : {sys.prefix != sys.base_prefix}")

# %% Cellule 2 — Premier contact : `print`, commentaires, indentation
# === CELLULE 2 : print, commentaires, indentation ===
# Ceci est un commentaire

print("Réseau EnergiaNord : 6 sites")
print("Site", "SITE_IND_001", "5.0 MW", sep=" | ")
print("Chargement...", end=" ")
print("terminé")

message = ("Mesures toutes les 15 minutes "
           "sur 6 sites")                # les parenthèses permettent de couper une ligne
if len(message) > 20:
    print(f"Message de {len(message)} caractères")

# %% Cellule 3 — Variables et typage dynamique
# === CELLULE 3 : Variables et typage dynamique ===
site_id = "SITE_IND_001"
capacity_mw = 5.0
flexible = True
nb_mesures = 720
curtailment_price = None

for nom, valeur in [("site_id", site_id), ("capacity_mw", capacity_mw),
                    ("flexible", flexible), ("nb_mesures", nb_mesures),
                    ("curtailment_price", curtailment_price)]:
    print(f"{nom:<18} {valeur!r:<16} {type(valeur).__name__}")

x = 10
x = "dix"                     # même variable, autre type : autorisé
print(type(x).__name__, isinstance(flexible, int))

# %% Cellule 4 — Nombres : division, flottants, `Decimal`
# === CELLULE 4 : Nombres — division, flottants, Decimal ===
import math
from decimal import Decimal

print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)
print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(Decimal("0.1") + Decimal("0.2"))

# %% Cellule 5 — Nombres : arrondi, grands entiers, `NaN` et `None`
# === CELLULE 5 : Arrondi, grands entiers, NaN et None ===
print(round(0.5), round(1.5), round(2.5), round(3.5))
print(round(2.675, 2))
print(1_000_000 * 1.5, 2 ** 100)

valeur_nan = float("nan")
print(valeur_nan == valeur_nan, math.isnan(valeur_nan))
print(None == 0, None is None)

# %% Cellule 6 — Constantes
# === CELLULE 6 : Constantes, Final et MappingProxyType ===
from types import MappingProxyType
from typing import Final

CAPACITE_MAX_MW: Final = 5.0
SITES_FLEXIBLES = ("SITE_IND_001", "SITE_IND_002", "SITE_RES_001", "SITE_RES_002")
CODES_ERREUR = MappingProxyType({
    -999: "Capteur hors service",
    -888: "Valeur non transmise",
    -777: "Recalibrage en cours",
})

CAPACITE_MAX_MW = 6.0             # Python l'accepte : c'est une convention
print(CAPACITE_MAX_MW)

try:
    CODES_ERREUR[-1] = "test"
except TypeError as erreur:
    print(f"Modification refusée : {erreur}")

# %% Cellule 7 — Énumérations : `StrEnum`
# === CELLULE 7 : StrEnum ===
from enum import Enum, StrEnum

class StatutAncien(str, Enum):            # Hier
    OK = "OK"
    ERROR = "ERROR"

class Statut(StrEnum):                    # Aujourd'hui (3.11+)
    OK = "OK"
    ERROR = "ERROR"

print(str(StatutAncien.OK), "|", str(Statut.OK))
print(Statut.OK == "OK", Statut("ERROR") is Statut.ERROR)
print(f"{Statut.ERROR} / {[s.value for s in Statut]}")

# %% Cellule 8 — Chaînes : découpage et méthodes
# === CELLULE 8 : Chaînes — découpage et méthodes ===
ligne = "  2025-01-03T04:30:00,SITE_IND_002,0.865,234.6,49.89,OK  "
champs = ligne.strip().split(",")
print(champs)

timestamp, site_id, conso, tension, freq, statut = champs
print(site_id[:8], site_id[-3:], site_id[::-1])
print(site_id.lower(), site_id.replace("_", "-"), site_id.startswith("SITE_"))
print(site_id.removeprefix("SITE_"), site_id.removesuffix("_002"))

# %% Cellule 9 — Chaînes : trois générations de formatage
# === CELLULE 9 : Chaînes — formatage ===
nom, mw = "SITE_IND_001", 2.5
print("Site %s : %.2f MW" % (nom, mw))
print("Site {} : {:.2f} MW".format(nom, mw))
print(f"Site {nom} : {mw:.2f} MW")

print(f"{mw=}")
print(f"{1234567.891:,.2f} | {0.0345:.1%} | {42:05d} | {nom:>15}")
print(r"C:\Users\formation\data\consommation.csv")

# %% Cellule 10 — Valeurs de vérité et comparaisons
# === CELLULE 10 : Valeurs de vérité et comparaisons ===
conso, capacite = 0.865, 5.0
print(0 <= conso <= capacite)

print([bool(v) for v in (0, 0.0, "", [], None, "0", -999)])

a, b = [1, 2], [1, 2]
print(a == b, a is b, a is not None)

# %% Cellule 11 — Opérateurs logiques, `in` et opérateur morse
# === CELLULE 11 : Opérateurs logiques, in et := ===
statut = None
print(statut or "INCONNU")

print("SITE_IND" in "SITE_IND_001", conso in (-999, -888, -777))

mesures = ["0.865", "abc", "1.2"]
if (n := len(mesures)) > 2:
    print(f"{n} mesures reçues")

# %% Cellule 12 — Conditions : `if` / `elif` / `else`
# === CELLULE 12 : Conditions ===
capacites = {"SITE_IND_001": 5.0, "SITE_COM_002": 1.5, "SITE_RES_002": 0.6}
mesures = {"SITE_IND_001": 4.6, "SITE_COM_002": 0.4, "SITE_RES_002": 0.61}

for site_id, capacite in capacites.items():
    taux = mesures[site_id] / capacite
    if taux > 1:
        niveau = "ANOMALIE (dépasse la capacité)"
    elif taux >= 0.8:
        niveau = "CRITIQUE"
    elif taux >= 0.5:
        niveau = "SOUTENU"
    else:
        niveau = "NORMAL"
    profil = "flexible" if site_id.startswith(("SITE_IND", "SITE_RES")) else "rigide"
    print(f"{site_id} : {taux:6.1%} -> {niveau:<32} ({profil})")

# %% Cellule 13 — `match` / `case` : hier et aujourd'hui
# === CELLULE 13 : match / case ===
def decrire_ancien(code):                                     # Hier
    if code is None or code == "":
        return "valeur manquante"
    elif code == -999:
        return "capteur hors service"
    elif code == -888 or code == -777:
        return "valeur non transmise ou recalibrage"
    elif isinstance(code, (int, float)) and code >= 0:
        return "mesure valide"
    else:
        return "valeur inattendue"

def decrire(code):                                            # Aujourd'hui (3.10+)
    match code:
        case None | "":
            return "valeur manquante"
        case -999:
            return "capteur hors service"
        case -888 | -777:
            return "valeur non transmise ou recalibrage"
        case int() | float() if code >= 0:
            return "mesure valide"
        case _:
            return "valeur inattendue"

for valeur in (0.865, -999, -888, None, "", "abc"):
    print(f"{valeur!r:>8} -> {decrire(valeur):<38} identique : {decrire(valeur) == decrire_ancien(valeur)}")

# %% Cellule 14 — `match` sur un dictionnaire
# === CELLULE 14 : match sur un enregistrement ===
def traiter(enregistrement):
    match enregistrement:
        case {"status": "ERROR", "consumption_mw": code} if code in CODES_ERREUR:
            return f"rejet : {CODES_ERREUR[code]}"
        case {"status": "OK", "consumption_mw": float(valeur)}:
            return f"accepté : {valeur} MW"
        case _:
            return "à examiner"

print(traiter({"status": "ERROR", "consumption_mw": -999}))
print(traiter({"status": "OK", "consumption_mw": 1.224}))
print(traiter({"status": "OK"}))

# %% Cellule 15 — Boucles `for` : `enumerate` et `zip`
# === CELLULE 15 : for, enumerate, zip ===
sites = ["SITE_IND_001", "SITE_IND_002", "SITE_COM_001",
         "SITE_COM_002", "SITE_RES_001", "SITE_RES_002"]
capacites_mw = [5.0, 3.5, 2.0, 1.5, 0.8, 0.6]

for rang, site in enumerate(sites, start=1):
    print(rang, site)

for site, cap in zip(sites, capacites_mw):
    print(f"{site} : {cap} MW")

# %% Cellule 16 — `zip` paresseux et `strict=True`
# === CELLULE 16 : zip paresseux et strict ===
paires = zip(sites, capacites_mw)
print(paires)
print(list(paires)[:2])

print(len(list(zip(sites, capacites_mw[:4]))))          # 4 : perte silencieuse de 2 sites

try:
    list(zip(sites, capacites_mw[:4], strict=True))
except ValueError as erreur:
    print(f"ValueError : {erreur}")

# %% Cellule 17 — `break`, `continue`, `else` de boucle, `while`
# === CELLULE 17 : break, continue, else, while ===
for site, cap in zip(sites, capacites_mw):
    if cap < 1.0:
        continue
    if cap > 3.0:
        print(f"Premier site > 3 MW : {site}")
        break
else:
    print("Aucun site > 3 MW")

cumul_mwh, heure = 0.0, 0
while cumul_mwh < 10:
    cumul_mwh += 2.5
    heure += 1
print(f"{cumul_mwh} MWh atteints après {heure} h")

# %% Cellule 18 — Compréhensions de liste
# === CELLULE 18 : Compréhensions de liste ===
mesures_brutes = [0.865, -999, 1.224, "", 0.149, -888, 1.105]

valides = []                                             # Hier
for m in mesures_brutes:
    if isinstance(m, float) and m >= 0:
        valides.append(m)

valides = [m for m in mesures_brutes if isinstance(m, float) and m >= 0]   # Aujourd'hui
print(valides)

# %% Cellule 19 — Compréhensions de dictionnaire, d'ensemble et générateurs
# === CELLULE 19 : Dictionnaires, ensembles, générateurs ===
capacite_par_site = {s: c for s, c in zip(sites, capacites_mw)}
familles = {s.split("_")[1] for s in sites}
print(capacite_par_site["SITE_COM_001"], sorted(familles))

gen = (m * 1000 for m in valides)
print(type(gen).__name__, next(gen))
print(sum(m for m in valides))

# %% Cellule 20 — Définir une fonction, documenter, retourner
# === CELLULE 20 : Fonctions ===
def taux_charge(conso_mw, capacite_mw):
    """Retourne le taux de charge d'un site (1.0 = 100 % de la capacité)."""
    return conso_mw / capacite_mw

def statistiques(valeurs):
    """Retourne (minimum, maximum, moyenne) : un tuple."""
    return min(valeurs), max(valeurs), sum(valeurs) / len(valeurs)

print(taux_charge(2.5, 5.0), "|", taux_charge.__doc__)
mini, maxi, moyenne = statistiques(valides)
print(mini, maxi, round(moyenne, 3))

# %% Cellule 21 — Paramètres nommés et valeurs par défaut
# === CELLULE 21 : Paramètres ===
def normaliser(valeur, capacite_mw, *, arrondi=3, plafond=1.0):
    return round(min(valeur / capacite_mw, plafond), arrondi)

print(normaliser(1.224, 2.0))
print(normaliser(capacite_mw=2.0, valeur=3.0, plafond=0.95))

try:
    normaliser(1.224, 2.0, 1)
except TypeError as erreur:
    print(f"TypeError : {erreur}")

def classer(conso_mw, /, capacite_mw):
    return "critique" if conso_mw / capacite_mw >= 0.8 else "normal"

print(classer(1.7, capacite_mw=2.0))

# %% Cellule 22 — Piège : valeur par défaut mutable
# === CELLULE 22 : Valeur par défaut mutable ===
def enregistrer_erreur_piege(code, historique=[]):
    historique.append(code)
    return historique

print(enregistrer_erreur_piege(-999))
print(enregistrer_erreur_piege(-888))

def enregistrer_erreur(code, historique=None):
    if historique is None:
        historique = []
    historique.append(code)
    return historique

print(enregistrer_erreur(-999), enregistrer_erreur(-888))

# %% Cellule 23 — `*args`, `**kwargs` et dépaquetage
# === CELLULE 23 : *args, **kwargs, dépaquetage ===
def moyenne_sites(*consos, ignorer=()):
    retenues = [c for c in consos if c not in ignorer]
    return sum(retenues) / len(retenues)

print(moyenne_sites(0.865, 1.224, -999, ignorer=(-999,)))

def config_lecture(chemin, **options):
    return {"chemin": chemin, **options}

options = {"encoding": "utf-8-sig", "sep": ","}
print(config_lecture("data/consommation_echantillon.csv", **options))

premier, *milieu, dernier = sites
print(premier, len(milieu), dernier)

# %% Cellule 24 — Fusion de dictionnaires : `{**a, **b}` et `|`
# === CELLULE 24 : Fusion de dictionnaires ===
defauts = {"encoding": "utf-8-sig", "sep": ","}
perso = {"sep": ";"}

print({**defauts, **perso})
print(defauts | perso)
print(defauts | perso == {**defauts, **perso})

# %% Cellule 25 — Annotations de types
# === CELLULE 25 : Annotations de types ===
from typing import List, Optional

def moyenne_v1(valeurs: List[float]) -> Optional[float]:          # Hier
    return sum(valeurs) / len(valeurs) if valeurs else None

def moyenne_v2(valeurs: list[float]) -> float | None:             # Aujourd'hui
    return sum(valeurs) / len(valeurs) if valeurs else None

print(moyenne_v2.__annotations__)
print(moyenne_v1([]), moyenne_v2([1.0, 2.0]))
print(moyenne_v2([1, 2, 3]))

# %% Cellule 26 — `TypedDict` : décrire un enregistrement
# === CELLULE 26 : TypedDict ===
from typing import TypedDict

class Mesure(TypedDict):
    timestamp: str
    site_id: str
    consumption_mw: float | None
    status: str

exemple: Mesure = {"timestamp": "2025-01-03T04:30:00", "site_id": "SITE_IND_002",
                   "consumption_mw": 0.865, "status": "OK"}
print(exemple["site_id"], list(Mesure.__annotations__))
print(type(exemple).__name__)

# %% Cellule 27 — `lambda`, tri, `filter`
# === CELLULE 27 : lambda et tri ===
parc = [{"id": "SITE_IND_001", "cap": 5.0}, {"id": "SITE_COM_002", "cap": 1.5},
        {"id": "SITE_RES_002", "cap": 0.6}, {"id": "SITE_IND_002", "cap": 3.5}]

tri = sorted(parc, key=lambda s: s["cap"], reverse=True)
print([s["id"] for s in tri])

grands = list(filter(lambda s: s["cap"] >= 2, parc))           # Hier
grands = [s for s in parc if s["cap"] >= 2]                     # Aujourd'hui
print(len(grands))

# %% Cellule 28 — `partial` et `lru_cache`
# === CELLULE 28 : partial et lru_cache ===
from functools import lru_cache, partial

arrondir_2 = partial(round, ndigits=2)
print(arrondir_2(2.34567))

@lru_cache(maxsize=None)
def facteur_emission(source):
    print(f"  calcul pour {source}")
    return {"solaire": 0.032, "eolien": 0.012, "gaz": 0.490}[source]

print(facteur_emission("gaz"), facteur_emission("gaz"))
print(facteur_emission.cache_info().hits)

# %% Cellule 29 — Portée des variables
# === CELLULE 29 : Portée (LEGB) ===
compteur = 0

def incrementer_faux():
    compteur = 1
    return compteur

def incrementer():
    global compteur
    compteur += 1
    return compteur

incrementer_faux()
print(compteur)
incrementer()
print(compteur)
print("sites" in globals(), "capacite_par_site" in globals())

# %% Cellule 30 — Fermetures (closures)
# === CELLULE 30 : Fermetures ===
def fabrique_detecteur(seuil):
    def est_critique(taux):
        return taux >= seuil
    return est_critique

critique_80 = fabrique_detecteur(0.8)
critique_95 = fabrique_detecteur(0.95)
print(critique_80(0.85), critique_95(0.85))

# %% Cellule 31 — `try` / `except` / `else` / `finally`
# === CELLULE 31 : Gestion des erreurs ===
def convertir_mesure(texte):
    texte = texte.strip()
    return None if texte == "" else float(texte)

def lire_valeur(texte):
    try:
        valeur = convertir_mesure(texte)
    except ValueError:
        print(f"  {texte!r} : illisible")
        return None
    else:
        return valeur
    finally:
        print(f"  {texte!r} traité")

for brut in ("0.865", "abc", ""):
    print(lire_valeur(brut))

# %% Cellule 32 — Erreurs métier et chaînage `raise ... from`
# === CELLULE 32 : raise ... from ===
from datetime import datetime

class TimestampInvalide(ValueError):
    """Levée quand un timestamp ne correspond à aucun format connu."""

def horodatage(texte):
    try:
        return datetime.strptime(texte, "%Y-%m-%dT%H:%M:%S")
    except ValueError as erreur:
        raise TimestampInvalide(f"Format inconnu : {texte!r}") from erreur

try:
    horodatage("hier soir")
except TimestampInvalide as erreur:
    print(f"{erreur} <- cause : {erreur.__cause__}")

# %% Cellule 33 — Groupes d'exceptions : `except*` et `add_note` (3.11)
# === CELLULE 33 : ExceptionGroup, except*, add_note ===
def valider_lot(valeurs):
    erreurs = []
    for i, v in enumerate(valeurs):
        try:
            float(v)
        except ValueError as e:
            e.add_note(f"ligne {i}")
            erreurs.append(e)
    if erreurs:
        raise ExceptionGroup("Lot invalide", erreurs)

try:
    valider_lot(["0.5", "x", "1.2", "y"])
except* ValueError as groupe:
    print(len(groupe.exceptions), "erreurs :", [e.__notes__[0] for e in groupe.exceptions])

# %% Cellule 34 — Dates : lecture de plusieurs formats
# === CELLULE 34 : Dates — formats multiples ===
from datetime import datetime, timedelta

FORMATS_TIMESTAMP = ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S")

def parse_timestamp(texte):
    for fmt in FORMATS_TIMESTAMP:
        try:
            return datetime.strptime(texte.strip(), fmt)
        except ValueError:
            continue
    raise TimestampInvalide(f"Format inconnu : {texte!r}")

bruts = ["2025-01-03T04:30:00", "2025-01-03 04:30:00", "03/01/2025 04:30:00"]
parses = [parse_timestamp(t) for t in bruts]
print(parses[0], all(p == parses[0] for p in parses))

debut = parses[0]
print(debut + timedelta(minutes=15), debut.strftime("%d/%m/%Y %Hh%M"), debut.weekday())

# %% Cellule 35 — Fuseaux horaires et nouveautés 3.11
# === CELLULE 35 : Fuseaux horaires ===
from datetime import UTC
from zoneinfo import ZoneInfo

print(datetime.fromisoformat("2025-01-03T04:30:00Z"))

utc = datetime(2025, 1, 3, 4, 30, tzinfo=UTC)
paris = utc.astimezone(ZoneInfo("Europe/Paris"))
print(utc.isoformat(), "->", paris.isoformat())

ete = datetime(2025, 7, 3, 4, 30, tzinfo=UTC).astimezone(ZoneInfo("Europe/Paris"))
print(ete.isoformat())

print(datetime.now(UTC).tzinfo)            # Hier : datetime.utcnow() (déprécié depuis 3.12)

# %% Cellule 36 — Fichiers : `pathlib`
# === CELLULE 36 : pathlib ===
from pathlib import Path

DATA = Path("data")
print(DATA.exists(), [p.name for p in sorted(DATA.glob("*.csv"))])

fichier = DATA / "sites_reference.csv"
print(fichier.suffix, fichier.stem, fichier.stat().st_size, "octets")

# %% Cellule 37 — Fichiers : lire un CSV et le BOM UTF-8
# === CELLULE 37 : CSV et BOM ===
import csv

print(fichier.read_bytes()[:3])
with open(fichier, encoding="utf-8") as f:
    print(repr(f.readline()[:12]))

with open(fichier, encoding="utf-8-sig", newline="") as f:
    sites_ref = list(csv.DictReader(f))
print(len(sites_ref), sites_ref[0])

# %% Cellule 38 — Fichiers : écrire du JSON, lire du TOML
# === CELLULE 38 : JSON et TOML ===
import json
import tomllib

sortie = Path("out")
sortie.mkdir(exist_ok=True)
(sortie / "sites.json").write_text(json.dumps(sites_ref, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.loads((sortie / "sites.json").read_text(encoding="utf-8"))[1]["site_id"])

Path("config.toml").write_text('''[chemins]
entree = "data/consommation_echantillon.csv"
sites = "data/sites_reference.csv"

[seuils]
anomalies_max = 0.10
taux_charge_critique = 0.8
''', encoding="utf-8")
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
print(config["seuils"], type(config["seuils"]["anomalies_max"]).__name__)

# %% Cellule 39 — Journalisation avec `logging`
# === CELLULE 39 : logging ===
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s | %(name)s | %(message)s", force=True)
log = logging.getLogger("qualite")

log.debug("Message de mise au point (masqué au niveau INFO)")
log.info("Lecture de %s", config["chemins"]["entree"])
log.warning("%d mesures avec code erreur", 9)
try:
    convertir_mesure("abc")
except ValueError as erreur:
    log.error("Conversion impossible : %s", erreur)

# %% Cellule 40 — Préparer les tests de compatibilité
# === CELLULE 40 : Outils de test de compatibilité ===
import importlib
import sys

def syntaxe_ok(source):
    try:
        compile(source, "<test>", "exec")
        return True
    except SyntaxError:
        return False

def module_ok(nom, attribut=None):
    try:
        module = importlib.import_module(nom)
    except ImportError:
        return False
    return attribut is None or hasattr(module, attribut)

def zip_strict_ok():
    try:
        list(zip([1], [2, 3], strict=True))
    except ValueError:
        return True
    return False

# %% Cellule 41 — Matrice de compatibilité de l'interpréteur courant
# === CELLULE 41 : Matrice de compatibilité ===
TESTS = [
    ("3.8   opérateur :=",                       lambda: syntaxe_ok("(n := 10)")),
    ("3.9   dict | dict",                        lambda: {"a": 1} | {"b": 2} == {"a": 1, "b": 2}),
    ("3.9   str.removeprefix",                   lambda: hasattr(str, "removeprefix")),
    ("3.10  match / case",                       lambda: syntaxe_ok("match 1:\n    case 1: pass")),
    ("3.10  int | None à l'exécution",           lambda: (int | None) is not None),
    ("3.10  zip(strict=True)",                   lambda: syntaxe_ok("zip([1], [2], strict=True)") and zip_strict_ok()),
    ("3.11  except* / ExceptionGroup",           lambda: syntaxe_ok("try:\n    pass\nexcept* ValueError:\n    pass")),
    ("3.11  tomllib",                            lambda: module_ok("tomllib")),
    ("3.11  enum.StrEnum",                       lambda: module_ok("enum", "StrEnum")),
    ("3.11  datetime.UTC",                       lambda: module_ok("datetime", "UTC")),
    ("3.12  f-string : mêmes guillemets",        lambda: syntaxe_ok('d = {"a": 1}\nf"{d["a"]}"')),
    ("3.12  instruction type",                   lambda: syntaxe_ok("type Mesure = tuple[str, float]")),
    ("3.12  génériques def f[T](x: T)",          lambda: syntaxe_ok("def f[T](x: T) -> T:\n    return x")),
    ("3.12  itertools.batched",                  lambda: module_ok("itertools", "batched")),
    ("3.12  typing.override",                    lambda: module_ok("typing", "override")),
    ("3.13  copy.replace",                       lambda: module_ok("copy", "replace")),
    ("3.13  warnings.deprecated",                lambda: module_ok("warnings", "deprecated")),
    ("--    distutils (retiré de la bibliothèque standard en 3.12)",         lambda: module_ok("distutils")),
]

print(f"Python {sys.version.split()[0]}")
for libelle, test in TESTS:
    print(f"{'OK ' if test() else 'NON'} | {libelle}")

# %% Cellule 42 — Inspecter les bibliothèques installées
# === CELLULE 42 : Bibliothèques installées ===
import importlib.metadata as metadata

for paquet in ("ipython", "ipykernel", "tzdata", "pandas", "numpy"):
    try:
        print(f"{paquet:<10} {metadata.version(paquet)}")
    except metadata.PackageNotFoundError:
        print(f"{paquet:<10} non installé  ->  pip install {paquet}")

# %% Cellule 43 — Le problème : du code coincé dans le notebook
# === CELLULE 43 : Ce que la session a défini ===
utiles = sorted(nom for nom, obj in globals().items()
                if callable(obj) and getattr(obj, "__module__", None) == "__main__"
                and obj.__name__ != "<lambda>" and not nom.startswith("_"))
print(len(utiles), "objets définis dans ce notebook :")
print(utiles)

# %% Cellule 44 — Créer un module (1/2) : constantes et conversions
# === CELLULE 44 : energie_utils.py — première moitié ===
Path("energie_utils.py").write_text('''"""energie_utils.py — Utilitaires de qualité de données du réseau EnergiaNord."""
import csv
from datetime import datetime
from types import MappingProxyType
from typing import Iterator

CODES_ERREUR = MappingProxyType({
    -999: "Capteur hors service",
    -888: "Valeur non transmise",
    -777: "Recalibrage en cours",
})

FORMATS_TIMESTAMP = (
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
)


class TimestampInvalide(ValueError):
    """Levée quand un timestamp ne correspond à aucun format connu."""


def parse_timestamp(texte: str) -> datetime:
    """Convertit un timestamp texte (3 formats possibles) en datetime."""
    for fmt in FORMATS_TIMESTAMP:
        try:
            return datetime.strptime(texte.strip(), fmt)
        except ValueError:
            continue
    raise TimestampInvalide(f"Format inconnu : {texte!r}")


def convertir_mesure(texte: str) -> float | None:
    """'' -> None ; '0.865' -> 0.865 ; '-999' -> -999.0"""
    texte = texte.strip()
    if texte == "":
        return None
    return float(texte)
''', encoding="utf-8")
print(Path("energie_utils.py").stat().st_size, "octets écrits")

# %% Cellule 45 — Créer un module (2/2) : qualité et lecture
# === CELLULE 45 : energie_utils.py — seconde moitié ===
with open("energie_utils.py", "a", encoding="utf-8") as f:
    f.write('''

def qualifier_mesure(valeur: float | None) -> str:
    """Classe une mesure : MANQUANTE, CODE_ERREUR, NEGATIVE ou VALIDE."""
    match valeur:
        case None:
            return "MANQUANTE"
        case v if v in CODES_ERREUR:
            return "CODE_ERREUR"
        case v if v < 0:
            return "NEGATIVE"
        case _:
            return "VALIDE"


def lire_csv(chemin) -> Iterator[dict]:
    """Lit un CSV (UTF-8 avec ou sans BOM) et produit un dictionnaire par ligne."""
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)
''')
print(len(Path("energie_utils.py").read_text(encoding="utf-8").splitlines()), "lignes au total")

# %% Cellule 46 — Importer un module
# === CELLULE 46 : Importer energie_utils ===
import importlib
importlib.invalidate_caches()

import energie_utils
print(energie_utils.__name__, "|", Path(energie_utils.__file__).name)
print([n for n, o in vars(energie_utils).items()
       if callable(o) and getattr(o, "__module__", None) == "energie_utils"])

from energie_utils import qualifier_mesure as qualifier
print(qualifier(0.865), qualifier(-999.0), qualifier(None), qualifier(-3.2))
print(energie_utils.CODES_ERREUR[-999])

# %% Cellule 47 — Modifier un module sans redémarrer : `reload`
# === CELLULE 47 : Modifier puis recharger un module ===
try:
    energie_utils.est_code_erreur(-999)
except AttributeError as erreur:
    print(f"Avant : {erreur}")

with open("energie_utils.py", "a", encoding="utf-8") as f:
    f.write('''

def est_code_erreur(valeur: float | None) -> bool:
    """Vrai si la valeur est un code d'erreur capteur."""
    return valeur in CODES_ERREUR
''')

importlib.reload(energie_utils)
print("Après :", energie_utils.est_code_erreur(-999), energie_utils.est_code_erreur(0.865))

# %% Cellule 48 — La bibliothèque standard : des modules déjà installés
# === CELLULE 48 : Modules de la bibliothèque standard ===
from collections import Counter
from statistics import mean, median, stdev

from energie_utils import convertir_mesure, lire_csv, qualifier_mesure

lignes = list(lire_csv("data/consommation_echantillon.csv"))
convertis = [convertir_mesure(l["consumption_mw"]) for l in lignes]
etats = Counter(qualifier_mesure(v) for v in convertis)
print(len(lignes), "lignes |", dict(etats))

valeurs = [v for v in convertis if qualifier_mesure(v) == "VALIDE"]
print(f"moyenne {mean(valeurs):.3f} | médiane {median(valeurs):.3f} | écart-type {stdev(valeurs):.3f}")

# %% Cellule 49 — L'idiome `if __name__ == "__main__"`
# === CELLULE 49 : L'idiome main ===
import subprocess

Path("demo_main.py").write_text('''"""Démonstration de l'idiome main."""
import sys


def main(argv=None) -> None:
    arguments = sys.argv[1:] if argv is None else argv
    print(f"__name__ vaut : {__name__}")
    print(f"Arguments     : {arguments}")


if __name__ == "__main__":
    main()
''', encoding="utf-8")

resultat = subprocess.run([sys.executable, "demo_main.py", "site_1", "--verbose"],
                          capture_output=True, text=True)
print(resultat.stdout)

import demo_main
print(demo_main.__name__)
demo_main.main(["appel", "depuis", "un", "notebook"])

# %% Cellule 50 — Arguments de ligne de commande avec `argparse`
# === CELLULE 50 : argparse ===
import argparse

parser = argparse.ArgumentParser(prog="analyse_sites",
                                 description="Contrôle qualité des mesures de consommation")
parser.add_argument("--input", "-i", required=True, help="fichier CSV des mesures")
parser.add_argument("--seuil", type=float, default=0.10, help="taux d'anomalies maximal toléré")
parser.add_argument("--json", action="store_true", help="écrire aussi un rapport JSON")

args = parser.parse_args(["-i", "data/consommation_echantillon.csv", "--seuil", "0.15", "--json"])
print(args)
print(type(args.seuil).__name__, args.seuil + 1)

# %% Cellule 51 — Assembler le script (1/3) : comptage
# === CELLULE 51 : analyse_sites.py — comptage ===
Path("analyse_sites.py").write_text('''"""analyse_sites.py — Contrôle qualité des mesures de consommation (Atelier 1).

Usage :
    python analyse_sites.py --input data/consommation_echantillon.csv
    python analyse_sites.py -i data/consommation_echantillon.csv --seuil 0.05 --json
"""
import argparse
import json
import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path

from energie_utils import (TimestampInvalide, convertir_mesure, lire_csv,
                           parse_timestamp, qualifier_mesure)

log = logging.getLogger("analyse_sites")


def compter(chemin_mesures: Path) -> dict:
    """Parcourt le fichier : états par site, somme des valeurs valides, doublons."""
    vues = set()
    qualite = defaultdict(Counter)
    somme_mw = defaultdict(float)
    doublons = horodatages_invalides = 0

    for ligne in lire_csv(chemin_mesures):
        cle = tuple(ligne.values())
        if cle in vues:                       # doublon exact : on l'écarte
            doublons += 1
            continue
        vues.add(cle)

        try:
            parse_timestamp(ligne["timestamp"])
        except TimestampInvalide:
            horodatages_invalides += 1

        etat = qualifier_mesure(convertir_mesure(ligne["consumption_mw"]))
        qualite[ligne["site_id"]][etat] += 1
        if etat == "VALIDE":
            somme_mw[ligne["site_id"]] += float(ligne["consumption_mw"])

    return {"qualite": qualite, "somme_mw": somme_mw, "doublons": doublons,
            "horodatages_invalides": horodatages_invalides}
''', encoding="utf-8")
print("analyse_sites.py :", len(Path("analyse_sites.py").read_text(encoding="utf-8").splitlines()), "lignes")

# %% Cellule 52 — Assembler le script (2/3) : indicateurs par site
# === CELLULE 52 : analyse_sites.py — indicateurs ===
with open("analyse_sites.py", "a", encoding="utf-8") as f:
    f.write('''

def analyser(chemin_mesures: Path, chemin_sites: Path) -> dict:
    """Calcule les indicateurs qualité et charge par site."""
    sites = {s["site_id"]: s for s in lire_csv(chemin_sites)}
    brut = compter(chemin_mesures)

    par_site = {}
    for site_id, compteur in sorted(brut["qualite"].items()):
        total = sum(compteur.values())
        valides = compteur["VALIDE"]
        conso_moyenne = brut["somme_mw"][site_id] / valides if valides else 0.0
        capacite = float(sites[site_id]["capacity_mw"])
        par_site[site_id] = {
            "mesures": total,
            "valides": valides,
            "manquantes": compteur["MANQUANTE"],
            "codes_erreur": compteur["CODE_ERREUR"],
            "taux_anomalies": round((total - valides) / total, 3),
            "conso_moyenne_mw": round(conso_moyenne, 3),
            "taux_charge_moyen": round(conso_moyenne / capacite, 3),
        }

    total = sum(s["mesures"] for s in par_site.values())
    anomalies = sum(s["mesures"] - s["valides"] for s in par_site.values())
    return {
        "sites": par_site,
        "doublons_ecartes": brut["doublons"],
        "horodatages_invalides": brut["horodatages_invalides"],
        "taux_anomalies_global": round(anomalies / total, 3),
    }
''')
print("analyse_sites.py :", len(Path("analyse_sites.py").read_text(encoding="utf-8").splitlines()), "lignes")

# %% Cellule 53 — Assembler le script (3/3) : affichage, arguments, `main`
# === CELLULE 53 : analyse_sites.py — interface en ligne de commande ===
with open("analyse_sites.py", "a", encoding="utf-8") as f:
    f.write('''

def afficher(rapport: dict) -> None:
    print(f"{'Site':<14}{'Mesures':>8}{'Valides':>9}{'Manq.':>7}{'Codes':>7}{'Anom.':>8}{'Charge':>9}")
    for site_id, s in rapport["sites"].items():
        print(f"{site_id:<14}{s['mesures']:>8}{s['valides']:>9}{s['manquantes']:>7}"
              f"{s['codes_erreur']:>7}{s['taux_anomalies']:>8.1%}{s['taux_charge_moyen']:>9.1%}")
    print(f"Doublons écartés      : {rapport['doublons_ecartes']}")
    print(f"Horodatages invalides : {rapport['horodatages_invalides']}")
    print(f"Taux d'anomalies      : {rapport['taux_anomalies_global']:.1%}")


def lire_arguments(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="analyse_sites", description=__doc__.splitlines()[0])
    parser.add_argument("--input", "-i", required=True, type=Path, help="fichier CSV des mesures")
    parser.add_argument("--sites", type=Path, default=Path("data/sites_reference.csv"),
                        help="référentiel des sites (défaut : %(default)s)")
    parser.add_argument("--seuil", type=float, default=0.10, help="taux d'anomalies maximal toléré")
    parser.add_argument("--json", action="store_true", help="écrire out/rapport_qualite.json")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    args = lire_arguments(argv)

    log.info("Analyse de %s", args.input)
    rapport = analyser(args.input, args.sites)
    afficher(rapport)

    if args.json:
        Path("out").mkdir(exist_ok=True)
        Path("out/rapport_qualite.json").write_text(
            json.dumps(rapport, indent=2, ensure_ascii=False), encoding="utf-8")
        log.info("Rapport écrit dans out/rapport_qualite.json")

    if rapport["taux_anomalies_global"] > args.seuil:
        log.error("Seuil dépassé : %.1f %% > %.1f %%",
                  rapport["taux_anomalies_global"] * 100, args.seuil * 100)
        return 1
    log.info("Qualité conforme au seuil")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''')
print("analyse_sites.py :", len(Path("analyse_sites.py").read_text(encoding="utf-8").splitlines()), "lignes")

# %% Cellule 54 — Exécuter le script comme en production
# === CELLULE 54 : Lancer analyse_sites.py ===
def lancer(*arguments):
    resultat = subprocess.run([sys.executable, "analyse_sites.py", *arguments],
                              capture_output=True, text=True)
    print(resultat.stdout, end="")
    print(resultat.stderr, end="")
    print(f"[code de sortie : {resultat.returncode}]\n")

lancer("--input", "data/consommation_echantillon.csv", "--json")
lancer("--input", "data/consommation_echantillon.csv", "--seuil", "0.05")

# %% Cellule 55 — Pont vers Fabric : un code portable
# === CELLULE 55 : Chemins portables local / Fabric ===
import importlib.util
DANS_FABRIC = importlib.util.find_spec("notebookutils") is not None
print(f"Exécution dans Fabric : {DANS_FABRIC}")

def resoudre_chemin(nom_fichier: str) -> Path:
    if DANS_FABRIC:
        return Path("/lakehouse/default/Files/data_python") / nom_fichier
    return Path("data") / nom_fichier

chemin = resoudre_chemin("consommation_echantillon.csv")
print(chemin, "| existe :", chemin.exists())
