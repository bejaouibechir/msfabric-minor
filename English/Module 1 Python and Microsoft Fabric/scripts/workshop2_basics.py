"""Workshop 2 (venv-base) - cellules de reference. Chaque bloc "# %%" = une cellule du notebook workshop2."""

# %% Cellule 1 — Vérification de l'environnement
# === CELLULE 1 : Vérification de l'environnement ===
import sys                                   # informations sur l'interpréteur Python
from pathlib import Path                     # manipulation de chemins de fichiers

import numpy as np                           # calcul sur tableaux (installé dans .venv-base)

# --- Le Python qui exécute cette cellule
print(f"Python       : {sys.version.split()[0]}")        # numéro de version
print(f"Interpréteur : {sys.executable}")                 # doit passer par .venv-base

# --- Les bibliothèques et le dossier de travail
print(f"NumPy        : {np.__version__}")                 # version de NumPy
print(f"Dossier      : {Path.cwd().name}")                # nom du dossier de travail

# --- Les fichiers attendus
print(f"Fichiers     : {sorted(p.name for p in Path('data').glob('*.csv'))}")   # CSV présents dans data/
print(f"Module A1    : {Path('energie_utils.py').exists()}")                    # le module de l'Workshop 1 est-il là ?

# %% Cellule 2 — Charger le fichier de 30 jours
# === CELLULE 2 : Charger les mesures ===
import sys
from pathlib import Path

# --- 1. Trouver energie_utils.py : dossier de travail, dossiers parents, sous-dossier scripts
dossier = Path.cwd()                                   # dossier de travail du kernel
candidats = [dossier, dossier / "scripts", *dossier.parents[:3]]
trouve = next((d for d in candidats if (d / "energie_utils.py").exists()), None)

# --- 2. Rendre ce dossier visible pour import (sans effet s'il l'est déjà)
if trouve is None:
    print("Dossier de travail :", dossier)             # chemin complet, pour diagnostiquer
    print("Fichiers .py       :", sorted(p.name for p in dossier.glob("*.py")))
    raise FileNotFoundError("energie_utils.py introuvable : le copier dans le dossier de travail")
if str(trouve) not in sys.path:
    sys.path.insert(0, str(trouve))                    # Python cherchera d'abord ici
print("energie_utils.py trouvé dans :", trouve.name)

# --- 2. On importe les quatre fonctions du module de l'Workshop 1
from energie_utils import convertir_mesure, lire_csv, parse_timestamp, qualifier_mesure

# --- 3. lire_csv est un générateur ; list() le consomme et garde toutes les lignes en mémoire
lignes = list(lire_csv("data/consommation_30jours.csv"))

print(len(lignes), "lignes")                       # nombre de lignes lues
print(type(lignes).__name__, type(lignes[0]).__name__)   # une liste de dictionnaires
print(lignes[0])                                   # la première ligne, valeurs en texte

# %% Cellule 3 — Listes : indexation, tranches, tri
# === CELLULE 3 : Listes ===

# Les 10 premières consommations, converties du texte en nombres (une valeur vide donne None)
conso = [convertir_mesure(l["consumption_mw"]) for l in lignes[:10]]
print(conso)

# Indices et tranches
print(conso[0], conso[-1], conso[2:5], conso[::3])    # premier, dernier, éléments 2 à 4, un sur trois

# On écarte d'abord les None et les codes d'erreur négatifs, puis on calcule
valides = [c for c in conso if c is not None and c >= 0]
print(sorted(valides, reverse=True)[:3])              # les trois plus fortes (tri décroissant, sans toucher à conso)
print(min(valides), max(valides), round(sum(valides) / len(valides), 3))   # minimum, maximum, moyenne

# %% Cellule 4 — Listes : ajout, retrait et méthodes utiles
# === CELLULE 4 : Méthodes de liste ===

# On construit la liste des sites dans leur ordre d'apparition, sans répétition
sites_vus = []
for l in lignes:
    if l["site_id"] not in sites_vus:        # « not in » : pas encore rencontré
        sites_vus.append(l["site_id"])       # on l'ajoute à la fin
print(sites_vus)

# Ajouts
sites_vus.extend(["SITE_TEST_999"])          # ajoute un élément à la fin
sites_vus.insert(0, "SITE_ENTETE")           # ajoute au début (position 0) : tout le reste est décalé

# Retrait et recherche
print(sites_vus.pop(),                       # retire et renvoie le dernier : SITE_TEST_999
      sites_vus.index("SITE_IND_001"),       # sa position (décalée d'un cran par SITE_ENTETE)
      sites_vus.count("SITE_IND_001"))       # combien de fois il apparaît
sites_vus.remove("SITE_ENTETE")              # retire la première occurrence de cette valeur
print(len(sites_vus))                        # nombre d'éléments restants

# %% Cellule 5 — Mutabilité : alias, copie superficielle, copie profonde
# === CELLULE 5 : Alias et copies ===
import copy                                   # module qui fournit deepcopy

a = [{"site": "SITE_IND_001", "mw": 2.5}, {"site": "SITE_COM_001", "mw": 1.0}]

alias = a                                     # même liste, deux noms
superficielle = a.copy()                      # nouvelle liste, mêmes dictionnaires
profonde = copy.deepcopy(a)                   # tout est recopié

a[0]["mw"] = 99.0                             # modification d'un dictionnaire INTERNE
a.append({"site": "SITE_RES_001", "mw": 0.4}) # ajout à la liste elle-même

print(len(alias), len(superficielle), len(profonde))          # taille de chaque version
print(alias[0]["mw"], superficielle[0]["mw"], profonde[0]["mw"])   # la valeur modifiée est-elle visible ?

# %% Cellule 6 — Tuples : `namedtuple` (hier) et `dataclass` (aujourd'hui)
# === CELLULE 6 : namedtuple et dataclass ===
from collections import namedtuple
from dataclasses import dataclass

# Hier : un tuple dont les positions ont un nom
MesureNT = namedtuple("MesureNT", ["site_id", "mw", "statut"])

# Aujourd'hui (3.10+) : une classe de données, non modifiable
@dataclass(frozen=True, slots=True)
class Mesure:
    site_id: str                  # champ obligatoire, de type texte
    mw: float | None              # un décimal, ou None si la mesure manque
    statut: str = "OK"            # valeur par défaut

    def est_valide(self) -> bool:                       # une méthode : du comportement attaché aux données
        return self.mw is not None and self.mw >= 0

nt = MesureNT("SITE_IND_001", 2.5, "OK")
dc = Mesure("SITE_IND_001", 2.5)                        # « statut » prend sa valeur par défaut
print(nt, "|", dc)                                      # affichage automatique des deux objets
print(nt.mw, dc.mw, dc.est_valide())                    # accès par nom, appel d'une méthode

# Un objet « frozen » refuse toute modification
try:
    dc.mw = 0.0
except AttributeError as erreur:
    print(f"Modification refusée : {type(erreur).__name__}")

# %% Cellule 7 — Dictionnaires : lecture sûre et valeurs par défaut
# === CELLULE 7 : Dictionnaires ===
capacites = {"SITE_IND_001": 5.0, "SITE_IND_002": 3.5, "SITE_COM_001": 2.0}

# Lecture : directe, avec repli, ou avec repli chiffré
print(capacites["SITE_IND_001"],            # clé présente : 5.0
      capacites.get("SITE_XXX"),            # clé absente : None, sans erreur
      capacites.get("SITE_XXX", 0.0))       # clé absente : la valeur de repli 0.0

# Une clé absente avec [] provoque une erreur
try:
    capacites["SITE_XXX"]
except KeyError as erreur:
    print(f"KeyError : {erreur}")

# setdefault : ajoute la clé seulement si elle n'existe pas
capacites.setdefault("SITE_COM_002", 1.5)
print(list(capacites.items())[-1], len(capacites))    # dernier couple (clé, valeur) et nombre de clés

# %% Cellule 8 — Compter et regrouper : `Counter` et `defaultdict`
# === CELLULE 8 : Counter et defaultdict ===
from collections import Counter, defaultdict

# Combien de lignes par site ? (le générateur entre parenthèses produit un site_id par ligne)
par_site = Counter(l["site_id"] for l in lignes)
print(par_site.most_common(3))               # les trois sites les plus fréquents

# Regrouper les mesures VALIDES par site
groupes = defaultdict(list)                  # chaque nouvelle clé démarre avec une liste vide
for l in lignes:
    v = convertir_mesure(l["consumption_mw"])          # texte -> décimal (ou None)
    if qualifier_mesure(v) == "VALIDE":                 # règle de qualité de l'Workshop 1
        groupes[l["site_id"]].append(v)                 # pas besoin de créer la liste avant

# Une ligne de résumé par site
for site_id, valeurs in sorted(groupes.items()):
    print(f"{site_id} : {len(valeurs):>4} mesures valides, moyenne {sum(valeurs)/len(valeurs):.3f} MW")

# %% Cellule 9 — Ensembles : doublons et comparaisons
# === CELLULE 9 : Ensembles ===

# Les sites du référentiel et les sites présents dans les données
referentiel = {l["site_id"] for l in lire_csv("data/sites_reference.csv")}
recus = {l["site_id"] for l in lignes}
print(len(referentiel), len(recus), referentiel == recus)      # tailles, et égalité des deux ensembles

# Différence (-) et différence symétrique (^)
print(sorted(referentiel - {"SITE_RES_002"}), "|", sorted({"A", "B"} ^ {"B", "C"}))

# Quels jours du mois sont présents ? (un ensemble ne garde qu'une fois chaque jour)
jours = {parse_timestamp(l["timestamp"]).day for l in lignes}
print(len(jours), sorted(set(range(1, 32)) - jours))           # nombre de jours, et jours absents de 1 à 31

# Dédoublonner les lignes : chaque ligne devient un tuple de ses valeurs
uniques = {tuple(l.values()) for l in lignes}
print(len(lignes), "lignes ->", len(uniques), "uniques :", len(lignes) - len(uniques), "doublons")

# %% Cellule 10 — Structures imbriquées et JSON
# === CELLULE 10 : Structures imbriquées ===
import json                                   # lecture et écriture de JSON
from datetime import datetime                 # pour fabriquer une date d'exemple

# --- 1. Construire l'arbre site -> jour -> liste de valeurs (400 premières lignes seulement)
arbre = defaultdict(lambda: defaultdict(list))        # chaque nouveau site reçoit son propre dictionnaire de jours
for l in lignes[:400]:
    v = convertir_mesure(l["consumption_mw"])         # texte -> décimal (ou None)
    if qualifier_mesure(v) == "VALIDE":               # on ne garde que les mesures valides
        jour = parse_timestamp(l["timestamp"]).date().isoformat()   # date au format texte « 2025-01-03 »
        arbre[l["site_id"]][jour].append(v)           # site, puis jour, puis on ajoute la valeur

# --- 2. Lire un chemin dans l'arbre
site = "SITE_IND_001"
premier_jour = sorted(arbre[site])[0]                 # le jour le plus ancien pour ce site
print(site, premier_jour, arbre[site][premier_jour])  # site, jour, valeurs de ce jour

# --- 3. Écrire en JSON : un petit document à exporter
extrait = {"site": site, "genere_le": datetime(2025, 2, 1, 8, 0),      # une vraie date, inconnue de JSON
           "jour": premier_jour, "valeurs": arbre[site][premier_jour][:3]}
texte = json.dumps(extrait, indent=2, ensure_ascii=False, default=str)  # default=str convertit la date en texte
print(texte)

# --- 4. Aller-retour : on relit le texte JSON et on regarde le type de la date
print(json.loads(texte)["genere_le"], type(json.loads(texte)["genere_le"]).__name__)

# %% Cellule 11 — Choisir la bonne structure : coût de la recherche
# === CELLULE 11 : Liste, ensemble, dictionnaire : coût de `in` ===
import timeit

# Trois structures contenant les mêmes 20 000 clés
cles_liste = [f"K{i:05d}" for i in range(20_000)]      # K00000, K00001, ... K19999
cles_set = set(cles_liste)
cles_dict = dict.fromkeys(cles_liste, 0)               # dictionnaire dont toutes les valeurs valent 0
cherche = "K19999"                                     # la clé la plus éloignée dans la liste : pire cas

# On mesure 2 000 recherches par structure, puis on divise pour avoir le coût d'une seule
for nom, struct in [("liste", cles_liste), ("ensemble", cles_set), ("dictionnaire", cles_dict)]:
    duree = timeit.timeit(lambda: cherche in struct, number=2_000) / 2_000
    print(f"{nom:<13}: {duree * 1e6:10.2f} µs par recherche")     # en microsecondes

# %% Cellule 12 — `pairwise`, `batched` et `nlargest`
# === CELLULE 12 : itertools et heapq ===
import heapq
from itertools import islice, pairwise

serie = groupes["SITE_COM_001"][:8]                    # 8 mesures d'un site
print([round(b - a, 3) for a, b in pairwise(serie)])   # variation entre chaque mesure et la suivante

# batched n'existe qu'à partir de Python 3.12 : on prévoit un repli pour 3.11
try:
    from itertools import batched
except ImportError:
    def batched(iterable, n):                          # même résultat, écrit à la main
        it = iter(iterable)
        while lot := tuple(islice(it, n)):             # prend n éléments à la fois jusqu'à épuisement
            yield lot                                  # yield : produit un lot puis reprend ici

lots = list(batched(range(10), 4))                     # 10 nombres en lots de 4 : le dernier est plus court
print(lots)
print(heapq.nlargest(3, groupes["SITE_IND_001"]))      # les 3 plus fortes consommations du site

# %% Cellule 13 — Afficher un objet proprement : `__repr__` et `__str__`
# === CELLULE 13 : __repr__ et __str__ ===

# Classe SANS méthode magique d'affichage
class ReleveBrut:
    def __init__(self, site_id, mw):          # __init__ : appelée à la création de l'objet
        self.site_id = site_id                # les données sont rangées dans l'objet (self)
        self.mw = mw

# Même classe AVEC __repr__ et __str__
class Releve:
    def __init__(self, site_id, mw):
        self.site_id = site_id
        self.mw = mw

    def __repr__(self):                       # diagnostic : ressemble à l'appel qui recrée l'objet
        return f"Releve({self.site_id!r}, {self.mw})"

    def __str__(self):                        # lisible : pour l'utilisateur
        return f"{self.site_id} : {self.mw} MW"

brut = ReleveBrut("SITE_IND_001", 2.5)
r1, r2 = Releve("SITE_IND_001", 2.5), Releve("SITE_COM_001", 1.0)

print(brut)               # sans méthode magique : une adresse mémoire
print(r1)                 # print utilise __str__
print(repr(r1))           # repr() appelle __repr__
print([r1, r2])           # une liste affiche le __repr__ de chaque élément

# %% Cellule 14 — Comparer et trier des objets : `__eq__` et `__lt__`
# === CELLULE 14 : __eq__ et __lt__ ===
class ReleveOrdonne(Releve):                  # hérite de Releve : affichage déjà écrit
    def __eq__(self, autre):                  # a == b : même site ET même valeur
        return self.site_id == autre.site_id and self.mw == autre.mw

    def __lt__(self, autre):                  # a < b : on compare les valeurs en MW
        return self.mw < autre.mw

# Six relevés valides pris dans le fichier
releves = []
for l in lignes:
    v = convertir_mesure(l["consumption_mw"])
    if qualifier_mesure(v) == "VALIDE":
        releves.append(ReleveOrdonne(l["site_id"], v))
    if len(releves) == 6:
        break

print(releves[0] == ReleveOrdonne(releves[0].site_id, releves[0].mw))   # True : __eq__
print(releves[0] is ReleveOrdonne(releves[0].site_id, releves[0].mw))   # False : deux objets distincts
print(releves[0] < releves[1], releves[0] > releves[1])                 # __lt__, et > déduit de <

print(sorted(releves)[:2])                    # sorted utilise __lt__ : les deux plus petits
print("plus fort :", max(releves))            # max aussi

# %% Cellule 15 — Une série de mesures : `__len__`, `__iter__`, `__contains__`, `__getitem__`
# === CELLULE 15 : Serie ===
class Serie:
    def __init__(self, valeurs):
        self.valeurs = list(valeurs)                  # les données, dans une liste

    def __repr__(self):                               # affichage : 3 premières valeurs et la taille
        debut = ", ".join(str(v) for v in self.valeurs[:3])
        suite = ", ..." if len(self) > 3 else ""
        return f"Serie([{debut}{suite}], {len(self)} valeurs)"

    def __len__(self):                                # len(s)
        return len(self.valeurs)

    def __iter__(self):                               # for v in s
        return iter(self.valeurs)

    def __contains__(self, x):                        # x in s
        return x in self.valeurs

    def __getitem__(self, cle):                       # s[cle] : trois cas selon ce qu'on reçoit
        if isinstance(cle, Serie):                    # un masque de True/False : on filtre
            return Serie(v for v, garder in zip(self.valeurs, cle) if garder)
        if isinstance(cle, slice):                    # une tranche : on renvoie une Serie
            return Serie(self.valeurs[cle])
        return self.valeurs[cle]                      # un entier : une valeur

    def __gt__(self, seuil):                          # s > 3.5 : un masque
        return Serie(v > seuil for v in self.valeurs)

ind2 = Serie(groupes["SITE_IND_002"])                 # mesures valides d'un site (capacité 3,5 MW)

print(ind2)                                           # __repr__
print(len(ind2), ind2[0], ind2[1:3])                  # __len__, entier, tranche
print(ind2[0] in ind2, 99.0 in ind2)                  # __contains__
print(round(sum(v for v in ind2), 1))                 # __iter__ : parcours pour additionner

masque = ind2 > 3.5                                   # __gt__ : un masque de True/False
print(masque)
pics = ind2[masque]                                   # __getitem__ avec un masque : filtre
print(len(pics), sorted(pics.valeurs))                # les valeurs au-dessus de la capacité

# %% Cellule 16 — Un mini-DataFrame : colonnes par `[ ]` et par `.` avec `__getattr__`
# === CELLULE 16 : Tableau ===

# --- 1. Un mini-DataFrame : un dictionnaire de colonnes, chaque colonne étant une Serie
class Tableau:
    def __init__(self, colonnes):
        self.colonnes = {nom: Serie(vals) for nom, vals in colonnes.items()}

    def __repr__(self):                               # résumé lisible dans le notebook
        return f"Tableau({len(self)} lignes, colonnes={list(self.colonnes)})"

    def __len__(self):                                # nombre de lignes = taille de la première colonne
        return len(next(iter(self.colonnes.values())))

    def __iter__(self):                               # parcourir un tableau donne les noms de colonnes (comme pandas)
        return iter(self.colonnes)

    def __contains__(self, nom):                      # "conso_mw" in t : la colonne existe-t-elle ?
        return nom in self.colonnes

    # --- 2. __getitem__ : quatre façons de sélectionner, selon ce qu'on met entre crochets
    def __getitem__(self, cle):
        if isinstance(cle, str):                      # t["conso_mw"] : une colonne
            return self.colonnes[cle]
        if isinstance(cle, list):                     # t[["site_id", "conso_mw"]] : plusieurs colonnes
            return Tableau({nom: self.colonnes[nom].valeurs for nom in cle})
        if isinstance(cle, int):                      # t[0] : une ligne, sous forme de dictionnaire
            return {nom: col[cle] for nom, col in self.colonnes.items()}
        if isinstance(cle, Serie):                    # t[masque] : on filtre TOUTES les colonnes
            return Tableau({nom: col[cle].valeurs for nom, col in self.colonnes.items()})
        raise TypeError(f"clé non prise en charge : {type(cle).__name__}")

    # --- 3. __getattr__ : t.conso_mw à la place de t["conso_mw"]
    def __getattr__(self, nom):                       # appelée seulement si l'attribut n'existe pas
        colonnes = self.__dict__.get("colonnes", {})  # on passe par __dict__ pour éviter une boucle infinie
        if nom in colonnes:
            return colonnes[nom]
        raise AttributeError(f"pas de colonne {nom!r}")

# --- 4. Un tableau à deux colonnes, construit à partir des mesures valides
valides_l = [l for l in lignes if qualifier_mesure(convertir_mesure(l["consumption_mw"])) == "VALIDE"]
t = Tableau({"site_id": [l["site_id"] for l in valides_l],
             "conso_mw": [convertir_mesure(l["consumption_mw"]) for l in valides_l]})

# --- 5. Essais
print(t)                                              # __repr__
print(len(t), list(t))                                # __len__ et __iter__ (noms de colonnes)
print("conso_mw" in t, "tension" in t)                # __contains__
print(t[0])                                           # __getitem__ avec un entier : la première ligne
print(t[["site_id"]])                                 # __getitem__ avec une liste : une sélection de colonnes
print(t["conso_mw"] is t.conso_mw)                    # [ ] et . donnent la même colonne

forts = t[t.conso_mw > 3.5]                           # masque + __getitem__ : lignes au-dessus de 3,5 MW
print(forts, sorted(set(forts.site_id)))              # sites concernés

try:
    t.tension                                         # colonne inexistante
except AttributeError as erreur:
    print("AttributeError :", erreur)

# %% Cellule 17 — Des objets qu'on appelle comme des fonctions : `__call__`
# === CELLULE 17 : __call__ ===

# --- 1. Une transformation paramétrée : multiplie par un facteur et compte ses usages
class Convertisseur:
    def __init__(self, facteur, unite):
        self.facteur = facteur                        # paramètre de la transformation
        self.unite = unite
        self.appels = 0                               # état : combien de fois l'objet a servi

    def __call__(self, valeur):                       # appelée par en_kw(valeur)
        self.appels += 1
        return round(valeur * self.facteur, 3)

# --- 2. Une transformation qui plafonne une valeur
class Plafonneur:
    def __init__(self, maximum):
        self.maximum = maximum

    def __call__(self, valeur):                       # ramène la valeur au maximum autorisé
        return min(valeur, self.maximum)

# --- 3. Une chaîne de transformations : chaque étape reçoit la sortie de la précédente
class Chaine:
    def __init__(self, *etapes):
        self.etapes = etapes                          # les objets appelables, dans l'ordre

    def __call__(self, valeur):
        for etape in self.etapes:
            valeur = etape(valeur)
        return valeur

# --- 4. Utilisation
en_kw = Convertisseur(1000, "kW")
print(en_kw(0.865), callable(en_kw))                  # appelé comme une fonction ; callable() le confirme
print(list(map(en_kw, [0.5, 1.2, 2.0])), en_kw.appels)   # passé à map ; le compteur a avancé (1 + 3 = 4)

# Chaîne : plafonner à la capacité (3,5 MW) puis convertir en kW
neutralise = Chaine(Plafonneur(3.5), en_kw)
print([neutralise(v) for v in pics])                  # appliquée aux pics de la Cellule 15

# %% Cellule 18 — Gérer une ressource proprement : `__enter__` et `__exit__`
# === CELLULE 18 : with, __enter__ et __exit__ ===
import csv                                            # lecture de CSV ligne par ligne

# --- 1. Un lecteur qui ouvre le fichier, compte les lignes et le referme toujours
class LecteurCSV:
    def __init__(self, chemin):
        self.chemin = chemin
        self.nb_lues = 0                              # état : lignes déjà lues
        self.fichier = None                           # le fichier n'est pas encore ouvert

    def __enter__(self):                              # début du bloc with : on ouvre la ressource
        self.fichier = open(self.chemin, encoding="utf-8-sig", newline="")
        print("  ouverture")
        return self                                   # devient la variable après « as »

    def __exit__(self, type_erreur, erreur, trace):   # fin du bloc with, même après une erreur
        self.fichier.close()                          # nettoyage garanti
        print(f"  fermeture après {self.nb_lues} lignes | erreur : {type_erreur.__name__ if type_erreur else 'aucune'}")
        return False                                  # False : une éventuelle erreur continue de remonter

    def __iter__(self):                               # permet « for ligne in lecteur »
        for ligne in csv.DictReader(self.fichier):
            self.nb_lues += 1
            yield ligne                               # produit une ligne à la fois

# --- 2. Cas normal : lecture complète
with LecteurCSV("data/consommation_30jours.csv") as lecteur:
    total = sum(1 for _ in lecteur)                   # on compte les lignes en les parcourant
print(total, "lignes | fichier fermé :", lecteur.fichier.closed)

# --- 3. Cas d'erreur : le fichier est refermé quand même
try:
    with LecteurCSV("data/consommation_30jours.csv") as lecteur:
        for ligne in lecteur:
            if lecteur.nb_lues == 3:
                raise ValueError("arrêt volontaire")  # simule une panne en cours de lecture
except ValueError as erreur:
    print("erreur propagée :", erreur, "| fichier fermé :", lecteur.fichier.closed)

# %% Cellule 19 — Du liste au tableau : `dtype`, `shape`, mémoire
# === CELLULE 19 : Premiers tableaux NumPy ===
import sys

# Les mesures valides d'un site, en liste puis en tableau
valeurs = [float(v) for v in groupes["SITE_IND_001"]]
tab = np.array(valeurs)

print(tab.dtype, tab.shape, tab.ndim, tab.size)          # type, dimensions, nombre d'axes, nombre d'éléments

# Comparaison mémoire : la liste stocke un objet Python par valeur, le tableau non
print(f"liste : {sys.getsizeof(valeurs) + sum(sys.getsizeof(v) for v in valeurs):>7} octets")
print(f"array : {tab.nbytes:>7} octets")

# Homogénéité : NumPy choisit un type commun
print(np.array([1, 2.5, 3]).dtype,        # entiers + décimal -> float64
      np.array([1, 2, 3]).dtype,          # entiers seulement -> int64
      np.array([1, "a"]).dtype)           # texte présent -> tout devient du texte

# %% Cellule 20 — Créer des tableaux : `arange`, `linspace`, `zeros`, `reshape`
# === CELLULE 20 : Création et forme ===
heures = np.arange(24)                            # 0, 1, ..., 23
print(heures)
print(np.linspace(0, 1, 5))                       # 5 points de 0 à 1 : 0, 0.25, 0.5, 0.75, 1
print(np.zeros((2, 3)), np.full((2, 2), np.nan), sep="\n")   # tableaux préremplis (forme = tuple)

grille = np.arange(24).reshape(4, 6)              # 24 valeurs réorganisées en 4 lignes x 6 colonnes
print(grille)
print(grille.shape, grille.T.shape, grille.reshape(-1).shape)   # forme, transposée, aplatie

# %% Cellule 21 — Construire la matrice sites × heures
# === CELLULE 21 : La matrice de consommation ===
sites = sorted(referentiel)                          # les 6 sites, par ordre alphabétique
rang = {s: i for i, s in enumerate(sites)}           # dictionnaire site -> numéro de ligne
debut = parse_timestamp("2025-01-01 00:00:00")       # origine du temps

conso = np.full((len(sites), 30 * 24), np.nan)       # tableau (6, 720) rempli de NaN

for l in lignes:
    ts = parse_timestamp(l["timestamp"])                       # texte -> datetime (3 formats gérés)
    heure_abs = (ts - debut).days * 24 + ts.hour               # colonne : heures écoulées depuis le 1er janvier
    v = convertir_mesure(l["consumption_mw"])                  # texte -> décimal (ou None)
    if qualifier_mesure(v) in ("VALIDE", "NEGATIVE"):          # on écarte codes erreur et vides
        conso[rang[l["site_id"]], heure_abs] = v               # écriture dans la bonne case

print(sites)
print(conso.shape, conso.dtype, f"{conso.nbytes / 1024:.1f} Ko")
print("valeurs NaN :", int(np.isnan(conso).sum()), "sur", conso.size)    # cases restées vides

# %% Cellule 22 — Indexation, tranches et masques
# === CELLULE 22 : Indexation ===
print(conso[0, :6])                              # site 0, six premières heures
print(conso[:, 12].round(2))                     # midi du 1er jour, pour les 6 sites
print(conso[1, 24:48].shape)                     # 2e site, 2e jour : 24 valeurs
print(conso[[0, 5], :3].round(2))                # lignes 0 et 5, trois premières heures

# Masque : valeurs du site 3 au-dessus de 3,5 MW (sa capacité)
print(conso[3][conso[3] > 3.5].round(2))

# %% Cellule 23 — Vectorisation : boucle contre tableau
# === CELLULE 23 : Taux de charge — boucle et vectorisation ===

# --- 1. Les capacités des 6 sites, dans le même ordre alphabétique que les lignes de la matrice
cap = np.array([float(l["capacity_mw"]) for l in sorted(lire_csv("data/sites_reference.csv"),
                                                          key=lambda s: s["site_id"])])
print(cap)

# --- 2. Deux façons de calculer la même chose
def taux_boucle():                                   # version Python : une boucle dans une boucle
    return [[c / cap[i] for c in ligne] for i, ligne in enumerate(conso.tolist())]

def taux_numpy():                                    # version NumPy : une seule opération
    return conso / cap[:, None]                      # chaque ligne divisée par la capacité de son site

# --- 3. Mesurer : chaque version est exécutée 20 fois, on garde la durée moyenne
t_boucle = timeit.timeit(taux_boucle, number=20) / 20
t_numpy = timeit.timeit(taux_numpy, number=20) / 20
print(f"boucle : {t_boucle * 1e3:7.2f} ms | numpy : {t_numpy * 1e3:7.3f} ms | x{t_boucle / t_numpy:.0f}")

# --- 4. Vérifier que les deux donnent le même résultat (equal_nan : un NaN est « égal » à un NaN)
print(np.allclose(np.array(taux_boucle()), taux_numpy(), equal_nan=True))

# %% Cellule 24 — Broadcasting : combiner des formes différentes
# === CELLULE 24 : Broadcasting ===

# --- 1. Cas qui fonctionne : (6, 720) avec (6, 1) ; l'axe de taille 1 est étiré à 720
taux = conso / cap[:, None]
print(conso.shape, cap.shape, cap[:, None].shape, "->", taux.shape)

# --- 2. Cas qui échoue : (6, 720) avec (6,) ; comparées à droite, 720 et 6 sont incompatibles
try:
    conso / cap
except ValueError as erreur:
    print(f"ValueError : {erreur}")

# --- 3. Écart à la moyenne de chaque site : keepdims garde la forme (6, 1) de la moyenne
moyenne_site = np.nanmean(conso, axis=1, keepdims=True)      # une moyenne par site, en ignorant les NaN
ecart = conso - moyenne_site                                 # (6, 720) - (6, 1) : broadcasting
print(moyenne_site.shape, ecart.shape, np.nanmean(ecart, axis=1).round(6))    # la moyenne des écarts vaut 0

# %% Cellule 25 — Valeurs manquantes : `NaN` et fonctions `nan*`
# === CELLULE 25 : NaN ===
site0 = conso[0]                                     # les 720 heures du premier site
print(np.mean(site0), np.nanmean(site0).round(3))    # nan contre 0.847 : la moyenne ignorant les NaN

print(np.nan == np.nan, np.isnan(np.nan))            # False True : le bon test est isnan

manquants = np.isnan(conso).sum(axis=1)              # combien de NaN par site (True compte pour 1)
print(dict(zip(sites, manquants.tolist())))
print((np.isnan(conso).mean(axis=1) * 100).round(1)) # la même chose en pourcentage

# %% Cellule 26 — Agrégations par axe : le profil horaire moyen
# === CELLULE 26 : Profil horaire moyen ===
cube = conso.reshape(6, 30, 24)                   # (site, jour, heure)
profil = np.nanmean(cube, axis=1)                 # moyenne sur les 30 jours -> (6, 24)
print(cube.shape, profil.shape)

# Pour chaque site : heure et valeur de la pointe et du creux
for site, courbe in zip(sites, profil):
    print(f"{site} : pointe à {courbe.argmax():02d}h ({courbe.max():.2f} MW), creux à {courbe.argmin():02d}h ({courbe.min():.2f} MW)")

# %% Cellule 27 — Détecter les anomalies : `where`, `clip`, percentiles
# === CELLULE 27 : Pics aberrants ===
depasse = conso > cap[:, None]                    # True où la mesure dépasse la capacité de SON site (NaN > x vaut False)
print("pics par site :", dict(zip(sites, depasse.sum(axis=1).tolist())))

# where : les pics deviennent NaN (ils ne sont pas des mesures fiables)
propre = np.where(depasse, np.nan, conso)
print(np.isnan(propre).sum() - np.isnan(conso).sum(), "valeurs neutralisées")

# clip : autre choix, ramener les pics à la capacité
plafonne = np.clip(conso, 0, cap[:, None])
print(np.nanmax(conso, axis=1).round(2), np.nanmax(plafonne, axis=1).round(2), sep="\n")   # maxima avant / après

# Percentiles : médiane, 95 % et 99 % des mesures propres
print(np.nanpercentile(propre, [50, 95, 99]).round(3))

# %% Cellule 28 — Tri, `argsort` et corrélation
# === CELLULE 28 : Top pics et corrélation ===
ind1 = propre[0]                                                   # une ligne de la matrice propre
ordre = np.argsort(np.nan_to_num(ind1, nan=-1))[::-1][:3]          # positions triées, en ordre décroissant, top 3
print([(int(i // 24 + 1), int(i % 24), round(float(ind1[i]), 2)) for i in ordre])   # (jour, heure, MW)

# Corrélation entre deux sites, sur les heures valides des deux
ok = ~np.isnan(propre[0]) & ~np.isnan(propre[1])                   # ~ = « non » ; & = « et »
print(np.corrcoef(propre[0][ok], propre[1][ok]).round(3))          # matrice 2 x 2

ok = ~np.isnan(propre[0]) & ~np.isnan(propre[4])
print(np.corrcoef(propre[0][ok], propre[4][ok])[0, 1].round(3))    # seulement le coefficient entre les deux

# %% Cellule 29 — Nombres aléatoires : `np.random.seed` (hier), `default_rng` (aujourd'hui)
# === CELLULE 29 : Générateurs aléatoires ===
np.random.seed(42)                                # Hier : état global
ancien = np.random.normal(230, 4, 3).round(1)     # 3 tensions autour de 230 V

rng = np.random.default_rng(42)                   # Aujourd'hui : générateur local
nouveau = rng.normal(230, 4, 3).round(1)
print(ancien, nouveau)                            # valeurs différentes : algorithmes différents

# Même graine -> mêmes tirages
rng = np.random.default_rng(42)
print(np.array_equal(nouveau, rng.normal(230, 4, 3).round(1)))

bruit = rng.normal(0, 0.05, size=(6, 24))         # un tableau de bruit (6, 24)
print(bruit.shape, rng.choice(sites, size=3, replace=False))   # 3 sites tirés sans remise

# %% Cellule 30 — Sauvegarder : `.npy`, `.npz`, `savetxt`
# === CELLULE 30 : Sauvegarde ===
Path("out").mkdir(exist_ok=True)                                   # dossier de sortie
np.save("out/conso_30jours.npy", conso)                            # un tableau
np.savez_compressed("out/conso_30jours.npz", conso=conso, capacites=cap, sites=np.array(sites))   # trois tableaux nommés
np.savetxt("out/profil_horaire.csv", profil, delimiter=";", fmt="%.3f")   # le profil (6 x 24), en texte

# Taille de chaque fichier
for nom in ("conso_30jours.npy", "conso_30jours.npz", "profil_horaire.csv"):
    print(f"{nom:<20} {Path('out', nom).stat().st_size:>7} octets")

# Relecture et vérification
relu = np.load("out/conso_30jours.npy")
print(np.array_equal(relu, conso, equal_nan=True), np.load("out/conso_30jours.npz")["sites"][:2])

# %% Cellule 31 — NumPy 1.x et NumPy 2.x : ce qui a disparu
# === CELLULE 31 : Alias supprimés dans NumPy 2 ===
print("NumPy", np.__version__)                       # version installée

# --- 1. Pour chaque ancien nom : existe-t-il encore ? et son remplaçant ? (hasattr teste sans provoquer d'erreur)
for ancien, nouveau in [("float_", "float64"), ("NaN", "nan"), ("product", "prod"), ("in1d", "isin")]:
    print(f"np.{ancien:<8} {'présent' if hasattr(np, ancien) else 'ABSENT ':<8} -> np.{nouveau:<8} {'présent' if hasattr(np, nouveau) else 'ABSENT'}")

# --- 2. Les remplaçants en action
print(np.isin([1, 5], [1, 2, 3]),                    # chaque valeur de la 1re liste est-elle dans la 2e ?
      np.prod([2, 3, 4]))                            # produit des valeurs : 24
