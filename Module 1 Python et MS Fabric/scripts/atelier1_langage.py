"""Atelier 1 - Python pour Microsoft Fabric : cellules de reference.

Chaque bloc "# %%" correspond a une cellule du notebook atelier1_langage.ipynb.
Les blocs "Etape manuelle" creent les fichiers que les apprenants creent a la main.
Execution complete : py atelier1_langage.py (depuis le dossier formation_python_fabric).
"""

# %% Cellule 1 — Vérification de l'environnement et techniques d'importation
# === CELLULE 1 : Vérification de l'environnement et techniques d'importation ===

# Technique 1 : « import module ». On garde le nom complet : on écrira ensuite « sys.version ».
import sys

# Technique 2 : « import module as alias ». On donne un nom court au module.
# C'est l'usage courant pour les bibliothèques de données (« import pandas as pd »).
import platform as pf

# Technique 3 : « from module import objet ». On importe UN objet précis, utilisable sans préfixe.
from pathlib import Path

# Technique 4 : « from module import objet as alias ». Comme la 3, avec un autre nom
# (utile quand deux modules proposent le même nom).
from datetime import datetime as dt

# Technique 5 : « import paquet.sous_module ». Un paquet est un dossier de modules ; on écrira « os.path.xxx ».
import os.path

# Technique 6 : import à partir d'un TEXTE. Utile quand le nom du module vient d'un fichier de configuration.
from importlib import import_module
module_json = import_module("json")

# ❌ À éviter : « from module import * » importe tous les noms d'un coup et peut écraser vos propres variables.

# --- Vérification de l'environnement (utilise les imports ci-dessus)
print(f"Python         : {sys.version.split()[0]}")             # technique 1 : préfixe « sys. »
print(f"Implémentation : {pf.python_implementation()}")          # technique 2 : alias « pf »
print(f"Système        : {pf.system()} {pf.machine()}")
print(f"Interpréteur   : {sys.executable}")                       # le Python qui exécute cette cellule
print(f"Dossier actif  : {Path.cwd()}")                           # technique 3 : « Path » sans préfixe
print(f"Dans un venv   : {sys.prefix != sys.base_prefix}")        # True si un environnement virtuel est actif

# --- Les autres techniques en action
print(dt(2025, 1, 3).strftime("%d/%m/%Y"))                        # technique 4 : alias « dt »
print(os.path.basename("data/sites_reference.csv"))               # technique 5 : os.path.xxx
print(module_json.dumps({"site": "SITE_IND_001"}))                # technique 6 : module obtenu par son nom

# %% Cellule 2 — Premier contact : `print`, commentaires, indentation
# === CELLULE 2 : print, commentaires, indentation ===
# Ceci est un commentaire : Python l'ignore.

print("Réseau EnergiaNord : 6 sites")                 # affichage simple, retour à la ligne automatique

# sep : ce qui sépare les éléments (par défaut un espace)
print("Site", "SITE_IND_001", "5.0 MW", sep=" | ")   # affiche : Site | SITE_IND_001 | 5.0 MW

# end : ce qui termine la ligne (par défaut un retour à la ligne)
print("Chargement...", end=" ")                       # reste sur la même ligne
print("terminé")                                      # complète la ligne précédente

# Des parenthèses permettent de couper une longue instruction sur plusieurs lignes
message = ("Mesures toutes les 15 minutes "
           "sur 6 sites")
if len(message) > 20:                                 # len() compte les caractères ; la ligne finit par « : »
    print(f"Message de {len(message)} caractères")    # ligne indentée = dans le bloc du « if »

# %% Cellule 3 — Variables et typage dynamique
# === CELLULE 3 : Variables et typage dynamique ===

# Création de cinq variables : on écrit « nom = valeur »
site_id = "SITE_IND_001"       # texte (str)
capacity_mw = 5.0              # nombre décimal (float)
flexible = True                # booléen (bool) : True ou False, avec une majuscule
nb_mesures = 720               # nombre entier (int)
curtailment_price = None       # None : ce site n'a pas de prix d'effacement

# Affichage : pour chaque variable, son nom, sa valeur et son type
# (« !r » montre la valeur telle qu'on l'écrirait en code, avec les guillemets pour un texte)
for nom, valeur in [("site_id", site_id), ("capacity_mw", capacity_mw),
                    ("flexible", flexible), ("nb_mesures", nb_mesures),
                    ("curtailment_price", curtailment_price)]:
    print(f"{nom:<18} {valeur!r:<16} {type(valeur).__name__}")

# Typage dynamique : le même nom peut désigner, plus tard, une valeur d'un autre type
x = 10                         # x désigne un entier
x = "dix"                      # x désigne maintenant un texte : c'est autorisé
print(type(x).__name__)        # str

# Un booléen est aussi un entier : True vaut 1 et False vaut 0
print(isinstance(flexible, int))   # True : « flexible » (un bool) est reconnu comme un int

# %% Cellule 4 — Nombres : division, flottants, `Decimal`
# === CELLULE 4 : Nombres — division, flottants, Decimal ===
import math
from decimal import Decimal

# --- 1) Les opérateurs arithmétiques
print(7 / 2)       # 3.5   : « / » donne toujours un nombre décimal
print(7 // 2)      # 3     : « // » donne la division entière (quotient)
print(7 % 2)       # 1     : « % » donne le reste de la division
print(2 ** 10)     # 1024  : « ** » élève à la puissance

# --- 2) Le piège des nombres décimaux (float)
somme = 0.1 + 0.2                                  # on additionne deux décimaux
print("0.1 + 0.2 vaut          :", somme)          # 0.30000000000000004 : un minuscule écart apparaît
print("0.1 + 0.2 == 0.3 ?      :", somme == 0.3)   # False : la comparaison exacte échoue à cause de cet écart

# À la place de « == », on compare avec une tolérance
print("math.isclose(somme, 0.3):", math.isclose(somme, 0.3))   # True : l'écart infime est accepté

# --- 3) Decimal : calcul exact, pour les montants
# On lui passe des TEXTES (« "0.1" »), pas des décimaux, pour éviter l'erreur de départ.
print("Decimal :", Decimal("0.1") + Decimal("0.2"))            # 0.3 exactement

# %% Cellule 5 — Nombres : arrondi, grands entiers, `NaN` et `None`
# === CELLULE 5 : Arrondi, grands entiers, NaN et None ===

# --- Arrondi : au pair le plus proche quand la décimale est exactement 5
print(round(0.5), round(1.5), round(2.5), round(3.5))   # 0 2 2 4 : 0.5 -> 0 (pair), 1.5 -> 2, 2.5 -> 2 (pair), 3.5 -> 4
print(round(2.675, 2))          # 2.67 (et non 2.68) : 2.675 est stocké en binaire un peu en dessous de 2.675

# --- Grands nombres
print(1_000_000 * 1.5)          # 1500000.0 : le « _ » est ignoré, il sert seulement à la lecture
print(2 ** 100)                 # un entier de 31 chiffres : aucune limite de taille

# --- NaN : un résultat indéfini
valeur_nan = float("nan")                               # on crée un NaN à partir du texte "nan"
print(valeur_nan == valeur_nan)                         # False : un NaN n'est égal à rien, pas même à lui-même
print(math.isnan(valeur_nan))                           # True : c'est la bonne façon de le détecter

# --- None : l'absence de valeur
print(None == 0)                                        # False : None n'est pas zéro
print(None is None)                                     # True : on teste None avec « is »

# %% Cellule 6 — Constantes
# === CELLULE 6 : Constantes, Final et MappingProxyType ===
from types import MappingProxyType
from typing import Final

# Une constante « par convention » : nom en MAJUSCULES, annotée « Final » pour les outils d'analyse
CAPACITE_MAX_MW: Final = 5.0

# Un tuple : une séquence qui ne peut pas être modifiée après sa création (parenthèses)
SITES_FLEXIBLES = ("SITE_IND_001", "SITE_IND_002", "SITE_RES_001", "SITE_RES_002")

# Un dictionnaire en lecture seule : associe un code d'erreur à sa signification
CODES_ERREUR = MappingProxyType({
    -999: "Capteur hors service",
    -888: "Valeur non transmise",
    -777: "Recalibrage en cours",
})

# Test 1 : réaffecter une constante « Final » -> Python l'accepte (seul un outil d'analyse protesterait)
CAPACITE_MAX_MW = 6.0
print(CAPACITE_MAX_MW)                    # 6.0

# Test 2 : modifier un dictionnaire en lecture seule -> Python refuse (TypeError)
try:
    CODES_ERREUR[-1] = "test"
except TypeError as erreur:
    print(f"Modification refusée : {erreur}")

# %% Cellule 7 — Énumérations : `StrEnum`
# === CELLULE 7 : StrEnum ===
from enum import Enum, StrEnum

# Hier : on combine « str » et « Enum » pour obtenir une énumération de textes
class StatutAncien(str, Enum):
    OK = "OK"
    ERROR = "ERROR"

# Aujourd'hui (Python 3.11+) : StrEnum fait la même chose en plus simple
class Statut(StrEnum):
    OK = "OK"            # le nom (OK) et la valeur ("OK") du membre
    ERROR = "ERROR"

print(str(StatutAncien.OK), "|", str(Statut.OK))     # StatutAncien.OK | OK : l'affichage diffère

# Un membre StrEnum est un vrai texte : on peut le comparer à une chaîne
print(Statut.OK == "OK")                             # True
print(Statut("ERROR") is Statut.ERROR)               # True : on retrouve un membre à partir de sa valeur

# Dans une f-string, on obtient directement le texte ; « [s.value for s in Statut] » liste les valeurs
print(f"{Statut.ERROR} / {[s.value for s in Statut]}")

# %% Cellule 8 — Chaînes : découpage et méthodes
# === CELLULE 8 : Chaînes — découpage et méthodes ===

# Une ligne du fichier CSV, avec des espaces parasites au début et à la fin
ligne = "  2025-01-03T04:30:00,SITE_IND_002,0.865,234.6,49.89,OK  "

# strip() retire les espaces des extrémités ; split(",") coupe la ligne à chaque virgule -> une liste de 6 champs
champs = ligne.strip().split(",")
print(champs)

# Dépaquetage : 6 noms à gauche, 6 valeurs à droite, affectées dans l'ordre
timestamp, site_id, conso, tension, freq, statut = champs

# Découpage : [début:fin], avec une fin exclue ; les indices négatifs comptent depuis la fin
print(site_id[:8])       # SITE_IND : les 8 premiers caractères
print(site_id[-3:])      # 002      : les 3 derniers
print(site_id[::-1])     # 200_DNI_ETIS : le texte à l'envers

# Quelques méthodes : chacune renvoie une NOUVELLE chaîne (site_id n'est pas modifié)
print(site_id.lower())                    # site_ind_002
print(site_id.replace("_", "-"))          # SITE-IND-002
print(site_id.startswith("SITE_"))        # True
print(site_id.removeprefix("SITE_"))      # IND_002 : retire le début exact « SITE_ »
print(site_id.removesuffix("_002"))       # SITE_IND : retire la fin exacte « _002 »

# %% Cellule 9 — Chaînes : trois générations de formatage
# === CELLULE 9 : Chaînes — formatage ===
nom, mw = "SITE_IND_001", 2.5

# Trois écritures qui produisent le MÊME texte
print("Site %s : %.2f MW" % (nom, mw))            # Hier : « % » (%s = texte, %.2f = décimal à 2 chiffres)
print("Site {} : {:.2f} MW".format(nom, mw))      # Ensuite : .format(), les {} sont remplis dans l'ordre
print(f"Site {nom} : {mw:.2f} MW")                # Aujourd'hui : f-string, on écrit directement les variables

# {mw=} affiche « mw=2.5 » : le nom ET la valeur (idéal pour déboguer)
print(f"{mw=}")

# Le mini-langage de mise en forme, après les deux-points
print(f"{1234567.891:,.2f} | {0.0345:.1%} | {42:05d} | {nom:>15}")
#      milliers + 2 décimales | pourcentage | zéros devant | aligné à droite sur 15 caractères

# Chaîne « brute » : le préfixe r ignore les séquences d'échappement (\U, \f, \n...)
print(r"C:\Users\formation\data\consommation.csv")

# %% Cellule 10 — Valeurs de vérité et comparaisons
# === CELLULE 10 : Valeurs de vérité et comparaisons ===
conso, capacite = 0.865, 5.0             # deux variables créées en une ligne

# --- Comparaison chaînée : « conso est-elle comprise entre 0 et la capacité ? »
print(0 <= conso <= capacite)            # True

# --- Quelles valeurs sont « vraies » ou « fausses » ? bool(valeur) donne la réponse
valeurs = (0, 0.0, "", [], None, "0", -999)
print([bool(v) for v in valeurs])
# Résultat : les 5 premières sont False (0, 0.0, "", [], None) ; "0" et -999 sont True

# --- == (même contenu) contre is (même objet)
a = [1, 2]
b = [1, 2]                               # une AUTRE liste, qui contient la même chose
print(a == b)                            # True  : même contenu
print(a is b)                            # False : deux objets distincts en mémoire
print(a is not None)                     # True  : la façon correcte de tester « a n'est pas None »

# %% Cellule 11 — Opérateurs logiques, `in` et opérateur morse
# === CELLULE 11 : Opérateurs logiques, in et := ===

# --- « or » : valeur de repli. statut est None (faux), donc « or » renvoie le second opérande
statut = None
print(statut or "INCONNU")                       # INCONNU

# --- « in » : appartenance
print("SITE_IND" in "SITE_IND_001")              # True  : ce morceau de texte est dans le texte
print(conso in (-999, -888, -777))               # False : 0.865 n'est pas un code d'erreur

# --- « := » : calculer et garder le résultat dans la même expression
mesures = ["0.865", "abc", "1.2"]
# Sans « := », on écrirait : n = len(mesures) puis, sur la ligne suivante, if n > 2:
if (n := len(mesures)) > 2:                      # len(mesures) est calculé UNE fois, rangé dans n, puis comparé à 2
    print(f"{n} mesures reçues")                 # n est utilisable ici

# %% Cellule 12 — Conditions : `if` / `elif` / `else`
# === CELLULE 12 : Conditions ===

# Deux dictionnaires : capacité de chaque site, et une mesure en MW
capacites = {"SITE_IND_001": 5.0, "SITE_COM_002": 1.5, "SITE_RES_002": 0.6}
mesures = {"SITE_IND_001": 4.6, "SITE_COM_002": 0.4, "SITE_RES_002": 0.61}

# .items() donne, à chaque tour, une clé (le site) et sa valeur (la capacité)
for site_id, capacite in capacites.items():
    taux = mesures[site_id] / capacite          # taux de charge : 1.0 = 100 % de la capacité

    # Les tests sont évalués dans l'ordre : le premier qui est vrai décide.
    if taux > 1:                                # d'abord le cas impossible : la mesure dépasse la capacité
        niveau = "ANOMALIE (dépasse la capacité)"
    elif taux >= 0.8:                           # sinon, très chargé
        niveau = "CRITIQUE"
    elif taux >= 0.5:                           # sinon, chargé
        niveau = "SOUTENU"
    else:                                       # tous les autres cas
        niveau = "NORMAL"

    # Ternaire : « valeur_si_vrai if condition else valeur_si_faux ».
    # startswith accepte un TUPLE de préfixes : vrai si le texte commence par l'un d'eux.
    profil = "flexible" if site_id.startswith(("SITE_IND", "SITE_RES")) else "rigide"

    print(f"{site_id} : {taux:6.1%} -> {niveau:<32} ({profil})")

# %% Cellule 13 — `match` / `case` : hier et aujourd'hui
# === CELLULE 13 : match / case ===

# Hier : une chaîne de if / elif, où « code » est répété à chaque ligne
def decrire_ancien(code):
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

# Aujourd'hui (3.10+) : match / case. Python compare « code » à chaque motif, de haut en bas.
def decrire(code):
    match code:
        case None | "":                       # « | » : ce motif OU celui-là
            return "valeur manquante"
        case -999:                            # un motif peut être une valeur littérale
            return "capteur hors service"
        case -888 | -777:
            return "valeur non transmise ou recalibrage"
        case int() | float() if code >= 0:    # int() : « est un entier » ; « if » : garde supplémentaire
            return "mesure valide"
        case _:                               # « _ » : tous les autres cas (comme else)
            return "valeur inattendue"

# On vérifie que les deux versions donnent le même résultat sur six valeurs
for valeur in (0.865, -999, -888, None, "", "abc"):
    print(f"{valeur!r:>8} -> {decrire(valeur):<38} identique : {decrire(valeur) == decrire_ancien(valeur)}")

# %% Cellule 14 — `match` sur un dictionnaire
# === CELLULE 14 : match sur un enregistrement ===
def traiter(enregistrement):
    match enregistrement:
        # Cas 1 : statut ERROR ET une clé consumption_mw, dont la valeur est capturée dans « code »
        #         (la garde « if » vérifie que c'est un code connu de CODES_ERREUR)
        case {"status": "ERROR", "consumption_mw": code} if code in CODES_ERREUR:
            return f"rejet : {CODES_ERREUR[code]}"
        # Cas 2 : statut OK ET une valeur décimale (float), capturée dans « valeur »
        case {"status": "OK", "consumption_mw": float(valeur)}:
            return f"accepté : {valeur} MW"
        # Cas 3 : tout le reste
        case _:
            return "à examiner"

print(traiter({"status": "ERROR", "consumption_mw": -999}))   # cas 1
print(traiter({"status": "OK", "consumption_mw": 1.224}))     # cas 2
print(traiter({"status": "OK"}))                              # cas 3 : la clé consumption_mw manque

# %% Cellule 15 — Boucles `for` : `enumerate` et `zip`
# === CELLULE 15 : for, enumerate, zip ===
sites = ["SITE_IND_001", "SITE_IND_002", "SITE_COM_001",
         "SITE_COM_002", "SITE_RES_001", "SITE_RES_002"]
capacites_mw = [5.0, 3.5, 2.0, 1.5, 0.8, 0.6]           # même ordre que « sites »

# enumerate : (numéro, élément) à chaque tour ; start=1 pour compter à partir de 1
for rang, site in enumerate(sites, start=1):
    print(rang, site)

# zip : on lit « sites » et « capacites_mw » en parallèle
for site, cap in zip(sites, capacites_mw):
    print(f"{site} : {cap} MW")

# %% Cellule 16 — `zip` paresseux et `strict=True`
# === CELLULE 16 : zip paresseux et strict ===
paires = zip(sites, capacites_mw)
print(paires)                           # <zip object ...> : un itérateur, pas une liste
print(list(paires)[:2])                 # list(...) le consomme : les 2 premières paires

# Sans strict : listes de longueurs différentes (6 sites, 4 capacités) -> aucune erreur
print(len(list(zip(sites, capacites_mw[:4]))))     # 4 : deux sites disparaissent en silence

# Avec strict=True : la différence de longueur est détectée
try:
    list(zip(sites, capacites_mw[:4], strict=True))
except ValueError as erreur:
    print(f"ValueError : {erreur}")

# %% Cellule 17 — `break`, `continue`, `else` de boucle, `while`
# === CELLULE 17 : break, continue, else, while ===

# On cherche le premier site de plus de 3 MW, en ignorant les sites de moins de 1 MW
for site, cap in zip(sites, capacites_mw):
    if cap < 1.0:
        continue                                # site trop petit : on passe au suivant
    if cap > 3.0:
        print(f"Premier site > 3 MW : {site}")
        break                                   # trouvé : on quitte la boucle (le « else » ci-dessous est alors sauté)
else:
    print("Aucun site > 3 MW")                  # atteint seulement si la boucle n'a jamais fait « break »

# while : on répète tant que le cumul est inférieur à 10 MWh
cumul_mwh, heure = 0.0, 0
while cumul_mwh < 10:
    cumul_mwh += 2.5                            # +2.5 MWh à chaque heure
    heure += 1
print(f"{cumul_mwh} MWh atteints après {heure} h")

# %% Cellule 18 — Compréhensions de liste
# === CELLULE 18 : Compréhensions de liste ===

# Des mesures brutes mélangées : décimaux, codes d'erreur (entiers) et texte vide
mesures_brutes = [0.865, -999, 1.224, "", 0.149, -888, 1.105]

# --- Sans compréhension (4 lignes)
valides = []                                            # 1. on crée une liste vide
for m in mesures_brutes:                                # 2. on parcourt les mesures
    if isinstance(m, float) and m >= 0:                 # 3. on garde les décimaux positifs (isinstance teste le type)
        valides.append(m)                               # 4. on ajoute à la liste

# --- Avec compréhension (1 ligne) : « m pour chaque m de mesures_brutes, si la condition est vraie »
valides = [m for m in mesures_brutes if isinstance(m, float) and m >= 0]
print(valides)                                          # [0.865, 1.224, 0.149, 1.105]

# %% Cellule 19 — Compréhensions de dictionnaire et d'ensemble
# === CELLULE 19 : Dictionnaires et ensembles par compréhension ===

# Dictionnaire : pour chaque couple (site, capacité) de zip, on crée « site: capacité »
capacite_par_site = {s: c for s, c in zip(sites, capacites_mw)}
print(capacite_par_site["SITE_COM_001"])           # 2.0 : on retrouve une capacité à partir du site

# Ensemble : « SITE_IND_001 ».split("_") donne ["SITE", "IND", "001"] ; [1] prend "IND"
familles = {s.split("_")[1] for s in sites}        # 6 sites, mais seulement 3 familles distinctes
print(sorted(familles))                            # sorted(...) : un ensemble n'a pas d'ordre, on trie pour l'affichage

# %% Cellule 20 — Générateurs : calculer à la demande
# === CELLULE 20 : Générateurs ===

# Avec des parenthèses : rien n'est calculé pour l'instant
gen = (m * 1000 for m in valides)         # les mesures (MW) converties en kW, une par une, à la demande
print(type(gen).__name__)                 # generator : ce n'est pas une liste
print(next(gen))                          # calcule et donne la 1re valeur : 865.0
print(next(gen))                          # la 2e : 1224.0

# Le reste du générateur : list() demande toutes les valeurs restantes
print(list(gen))                          # [149.0, 1105.0] : les deux premières ont déjà été consommées
print(list(gen))                          # [] : un générateur épuisé est vide

# sum() accepte directement un générateur : la somme se calcule sans créer de liste
print(sum(m for m in valides))            # 3.343

# %% Cellule 21 — Un objet qui se comporte comme une liste : `__len__`, `__getitem__`, `__iter__`, `__contains__`
# === CELLULE 21 : Méthodes magiques d'une collection ===
class ParcSites:
    """Un parc de sites qui se comporte comme une collection Python."""

    def __init__(self, identifiants):         # appelée à la création : ParcSites(liste)
        self._sites = list(identifiants)      # on garde les identifiants dans une liste interne

    def __repr__(self):                       # __repr__ : ce que le notebook affiche pour l'objet
        return f"ParcSites({len(self._sites)} sites)"

    def __len__(self):                        # __len__ : appelée par len(parc)
        return len(self._sites)

    def __getitem__(self, position):          # __getitem__ : appelée par parc[0], parc[-1], parc[1:3]
        return self._sites[position]

    def __iter__(self):                       # __iter__ : appelée par « for site in parc »
        return iter(self._sites)

    def __contains__(self, site_id):          # __contains__ : appelée par « "SITE_X" in parc »
        return site_id in self._sites

parc = ParcSites(sites)                       # « sites » : la liste de six identifiants de la Cellule 15
print(parc)                                   # __repr__ : ParcSites(6 sites)
print(len(parc))                              # __len__ : 6
print(parc[0], "|", parc[-1], "|", parc[1:3]) # __getitem__ : un élément, le dernier, une tranche
print("SITE_COM_001" in parc, "SITE_XXX" in parc)   # __contains__ : True False
print([s for s in parc if s.startswith("SITE_RES")])   # __iter__ : parcours avec une compréhension

# %% Cellule 22 — Définir une fonction, documenter, retourner
# === CELLULE 22 : Fonctions ===
def taux_charge(conso_mw, capacite_mw):
    """Retourne le taux de charge d'un site (1.0 = 100 % de la capacité)."""   # docstring
    return conso_mw / capacite_mw                       # return : le résultat renvoyé à l'appelant

def statistiques(valeurs):
    """Retourne (minimum, maximum, moyenne) : un tuple de trois valeurs."""
    return min(valeurs), max(valeurs), sum(valeurs) / len(valeurs)

print(taux_charge(2.5, 5.0))                            # 0.5 : appel avec deux arguments
print(taux_charge.__doc__)                              # la docstring est conservée dans l'objet fonction

# « valides » vient de la Cellule 18 ; on déballe le tuple en trois variables
mini, maxi, moyenne = statistiques(valides)
print(mini, maxi, round(moyenne, 3))                    # round(x, 3) : arrondi à 3 décimales

# %% Cellule 23 — Paramètres nommés et valeurs par défaut
# === CELLULE 23 : Paramètres ===

# « valeur » et « capacite_mw » sont libres ; « arrondi » et « plafond » viennent APRÈS le « * » :
# ils doivent obligatoirement être nommés à l'appel, et ils ont une valeur par défaut.
def normaliser(valeur, capacite_mw, *, arrondi=3, plafond=1.0):
    return round(min(valeur / capacite_mw, plafond), arrondi)   # min(...) plafonne le résultat

print(normaliser(1.224, 2.0))                                   # défauts : arrondi=3, plafond=1.0
print(normaliser(capacite_mw=2.0, valeur=3.0, plafond=0.95))    # nommés, dans un autre ordre

try:
    normaliser(1.224, 2.0, 1)       # ambigu : que représente « 1 » ? Python refuse
except TypeError as erreur:
    print(f"TypeError : {erreur}")

# « / » : conso_mw doit être passé par POSITION ; capacite_mw peut être nommé
def classer(conso_mw, /, capacite_mw):
    return "critique" if conso_mw / capacite_mw >= 0.8 else "normal"

print(classer(1.7, capacite_mw=2.0))                            # critique (1.7 / 2.0 = 85 %)

# %% Cellule 24 — Piège : valeur par défaut mutable
# === CELLULE 24 : Valeur par défaut mutable ===

# ❌ Version piégée : « historique=[] » est créée UNE fois et réutilisée à chaque appel
def enregistrer_erreur_piege(code, historique=[]):
    historique.append(code)
    return historique

print(enregistrer_erreur_piege(-999))     # [-999]
print(enregistrer_erreur_piege(-888))     # on attend [-888] ; on obtient [-999, -888]

# ✅ Version correcte : None par défaut, la liste est créée à chaque appel
def enregistrer_erreur(code, historique=None):
    if historique is None:                # aucun historique fourni : on en crée un neuf
        historique = []
    historique.append(code)
    return historique

print(enregistrer_erreur(-999), enregistrer_erreur(-888))   # [-999] [-888]

# %% Cellule 25 — `*args`, `**kwargs` et dépaquetage
# === CELLULE 25 : *args, **kwargs, dépaquetage ===

# *consos : autant de valeurs que l'on veut ; elles arrivent dans un tuple « consos »
def moyenne_sites(*consos, ignorer=()):
    retenues = [c for c in consos if c not in ignorer]     # on écarte les valeurs à ignorer
    return sum(retenues) / len(retenues)

print(moyenne_sites(0.865, 1.224, -999, ignorer=(-999,)))  # 1.0445 : le -999 est ignoré

# **options : tous les arguments nommés arrivent dans le dictionnaire « options »
def config_lecture(chemin, **options):
    return {"chemin": chemin, **options}                   # ** réinjecte le dictionnaire

options = {"encoding": "utf-8-sig", "sep": ","}
print(config_lecture("data/consommation_echantillon.csv", **options))   # ** à l'appel : un dict devient des arguments nommés

# Déballage étoilé : premier, dernier, et le reste au milieu
premier, *milieu, dernier = sites
print(premier, len(milieu), dernier)                       # SITE_IND_001 4 SITE_RES_002

# %% Cellule 26 — Fusion de dictionnaires : `{**a, **b}` et `|`
# === CELLULE 26 : Fusion de dictionnaires ===

# Les options par défaut, et la surcharge de l'utilisateur (une seule clé change)
defauts = {"encoding": "utf-8-sig", "sep": ","}
perso = {"sep": ";"}

# Hier : chaque ** déverse un dictionnaire dans un nouveau ; la clé « sep » de « perso » écrase l'ancienne
print({**defauts, **perso})       # {'encoding': 'utf-8-sig', 'sep': ';'}

# Aujourd'hui (3.9+) : l'opérateur | fait la même chose, plus lisiblement
print(defauts | perso)            # {'encoding': 'utf-8-sig', 'sep': ';'}

# Les deux écritures donnent le même résultat ; « defauts » n'a pas été modifié
print((defauts | perso) == {**defauts, **perso})   # True
print(defauts)                                     # {'encoding': 'utf-8-sig', 'sep': ','}

# %% Cellule 27 — Annotations de types
# === CELLULE 27 : Annotations de types ===
from typing import List, Optional

# Hier : il fallait importer List et Optional
def moyenne_v1(valeurs: List[float]) -> Optional[float]:
    return sum(valeurs) / len(valeurs) if valeurs else None    # None si la liste est vide

# Aujourd'hui : « float | None » se lit « un float ou None »
def moyenne_v2(valeurs: list[float]) -> float | None:
    return sum(valeurs) / len(valeurs) if valeurs else None

print(moyenne_v2.__annotations__)              # les annotations sont stockées, sans être vérifiées
print(moyenne_v1([]), moyenne_v2([1.0, 2.0]))  # None 1.5
print(moyenne_v2([1, 2, 3]))                   # des int alors que l'annotation annonce des float : 2.0, aucune erreur

# %% Cellule 28 — `TypedDict` : décrire un enregistrement
# === CELLULE 28 : TypedDict ===
from typing import TypedDict

# Le schéma d'une ligne du CSV : quatre clés, chacune avec son type
class Mesure(TypedDict):
    timestamp: str
    site_id: str
    consumption_mw: float | None      # peut être vide dans le fichier
    status: str

# Un dictionnaire conforme au schéma (l'annotation « : Mesure » le déclare)
exemple: Mesure = {"timestamp": "2025-01-03T04:30:00", "site_id": "SITE_IND_002",
                   "consumption_mw": 0.865, "status": "OK"}
print(exemple["site_id"], list(Mesure.__annotations__))   # les clés déclarées
print(type(exemple).__name__)                             # dict : à l'exécution, rien de spécial

# %% Cellule 29 — Classe et méthodes magiques : `__init__`, `__repr__`, `__str__`, `__eq__`, `__lt__`
# === CELLULE 29 : Classe et méthodes magiques ===
class Site:
    def __init__(self, site_id, capacite_mw):     # appelée par Site("SITE_IND_001", 5.0)
        self.site_id = site_id                    # « self. » : les données sont rangées dans l'objet
        self.capacite_mw = capacite_mw

    def __repr__(self):                           # texte de diagnostic : ce que le notebook affiche
        return f"Site({self.site_id!r}, {self.capacite_mw})"

    def __str__(self):                            # texte lisible : ce que print() affiche
        return f"{self.site_id} ({self.capacite_mw} MW)"

    def __eq__(self, autre):                      # appelée par « a == b » : deux sites sont égaux si même identifiant
        return isinstance(autre, Site) and self.site_id == autre.site_id

    def __lt__(self, autre):                      # appelée par « a < b » (et par sorted) : on compare les capacités
        return self.capacite_mw < autre.capacite_mw

gros = Site("SITE_IND_001", 5.0)
petit = Site("SITE_RES_002", 0.6)

print(gros)                                       # __str__  : SITE_IND_001 (5.0 MW)
print(repr(gros))                                 # __repr__ : Site('SITE_IND_001', 5.0)
print([gros, petit])                              # une liste affiche les __repr__ de ses éléments
print(gros == Site("SITE_IND_001", 999))          # __eq__ : True (même identifiant, capacité différente)
print(petit < gros)                               # __lt__ : True (0.6 < 5.0)
print(sorted([gros, petit]))                      # sorted utilise __lt__ : du plus petit au plus grand

# %% Cellule 30 — `lambda`, tri, `filter`
# === CELLULE 30 : lambda et tri ===
flotte = [{"id": "SITE_IND_001", "cap": 5.0}, {"id": "SITE_COM_002", "cap": 1.5},
          {"id": "SITE_RES_002", "cap": 0.6}, {"id": "SITE_IND_002", "cap": 3.5}]

# key=lambda s: s["cap"] : « pour trier, regarde la clé "cap" de chaque élément »
tri = sorted(flotte, key=lambda s: s["cap"], reverse=True)     # reverse=True : du plus grand au plus petit
print([s["id"] for s in tri])

# Hier : filter garde les éléments pour lesquels la lambda est vraie
grands = list(filter(lambda s: s["cap"] >= 2, flotte))
# Aujourd'hui : la même chose avec une compréhension
grands = [s for s in flotte if s["cap"] >= 2]
print(len(grands))                                              # 2

# %% Cellule 31 — `partial` et `lru_cache`
# === CELLULE 31 : partial et lru_cache ===
from functools import lru_cache, partial

# partial : « round » avec ndigits=2 déjà rempli ; arrondir_2(x) équivaut à round(x, ndigits=2)
arrondir_2 = partial(round, ndigits=2)
print(arrondir_2(2.34567))                     # 2.35

@lru_cache(maxsize=None)                       # décorateur : mémorise les résultats
def facteur_emission(source):
    print(f"  calcul pour {source}")           # ce message prouve qu'un vrai calcul a lieu
    return {"solaire": 0.032, "eolien": 0.012, "gaz": 0.490}[source]

print(facteur_emission("gaz"), facteur_emission("gaz"))   # deux appels, un seul calcul
print(facteur_emission.cache_info().hits)                 # 1 : nombre de fois où le cache a servi

# %% Cellule 32 — Portée des variables
# === CELLULE 32 : Portée des variables ===
compteur = 0                                    # variable du niveau supérieur (« globale »)

def incrementer_faux():
    compteur = 1                                # crée une variable LOCALE ; la globale n'est pas touchée
    return compteur

def incrementer():
    global compteur                             # « compteur » désigne ici la variable globale
    compteur += 1
    return compteur

incrementer_faux()
print(compteur)                                 # 0 : inchangé
incrementer()
print(compteur)                                 # 1 : modifié
print("sites" in globals(), "capacite_par_site" in globals())   # les variables des cellules précédentes existent

# %% Cellule 33 — Fermetures (closures)
# === CELLULE 33 : Fermetures ===
def fabrique_detecteur(seuil):
    def est_critique(taux):                     # fonction interne
        return taux >= seuil                    # « seuil » vient de la fonction englobante : elle le mémorise
    return est_critique                         # on renvoie la fonction elle-même, sans l'appeler

critique_80 = fabrique_detecteur(0.8)           # une fonction qui se souvient de 0.8
critique_95 = fabrique_detecteur(0.95)          # une autre, qui se souvient de 0.95
print(critique_80(0.85), critique_95(0.85))     # True False : même taux, deux seuils

# %% Cellule 34 — Un objet qu'on appelle comme une fonction : `__call__`
# === CELLULE 34 : __call__ ===
class Detecteur:
    def __init__(self, seuil):
        self.seuil = seuil                       # donnée visible et modifiable
        self.appels = 0                          # compteur d'appels

    def __call__(self, taux):                    # appelée par detecteur(taux)
        self.appels += 1
        return taux >= self.seuil

detecteur = Detecteur(0.8)
print(detecteur(0.85), detecteur(0.5))           # True False : utilisé comme une fonction
print(detecteur.appels, detecteur.seuil)         # 2 0.8 : données lisibles, contrairement à la fermeture
detecteur.seuil = 0.9                            # et modifiables
print(detecteur(0.85))                           # False : le nouveau seuil s'applique
print(callable(detecteur))                       # True : Python le considère comme appelable

# %% Cellule 35 — `try` / `except` / `else` / `finally`
# === CELLULE 35 : Gestion des erreurs ===
def convertir_mesure(texte):
    texte = texte.strip()                        # enlève les espaces autour
    return None if texte == "" else float(texte) # texte vide -> None ; sinon conversion (peut lever ValueError)

def lire_valeur(texte):
    try:
        valeur = convertir_mesure(texte)         # ligne qui peut échouer
    except ValueError:                           # seulement l'erreur attendue : texte non numérique
        print(f"  {texte!r} : illisible")
        return None
    else:                                        # aucune erreur : on renvoie la valeur
        return valeur
    finally:                                     # s'exécute dans TOUS les cas, même après un return
        print(f"  {texte!r} traité")

for brut in ("0.865", "abc", ""):                # une valeur correcte, un texte illisible, une valeur vide
    print(lire_valeur(brut))

# %% Cellule 36 — Erreurs métier et chaînage `raise ... from`
# === CELLULE 36 : raise ... from ===
from datetime import datetime

class TimestampInvalide(ValueError):             # notre erreur métier : hérite de ValueError, corps vide
    """Levée quand un timestamp ne correspond à aucun format connu."""

def horodatage(texte):
    try:
        # strptime : texte -> datetime, selon le format (%Y année, %m mois, %d jour, %H heure, %M minute, %S seconde)
        return datetime.strptime(texte, "%Y-%m-%dT%H:%M:%S")
    except ValueError as erreur:                 # « as erreur » : on récupère l'erreur d'origine
        # On lève notre erreur métier ; « from erreur » garde la cause d'origine
        raise TimestampInvalide(f"Format inconnu : {texte!r}") from erreur

try:
    horodatage("hier soir")                      # ce texte n'est pas une date
except TimestampInvalide as erreur:              # l'appelant n'a besoin de connaître que notre erreur
    print(f"{erreur} <- cause : {erreur.__cause__}")

# %% Cellule 37 — Groupes d'exceptions : `except*` et `add_note` (3.11)
# === CELLULE 37 : ExceptionGroup, except*, add_note ===
def valider_lot(valeurs):
    erreurs = []                                      # on collecte les erreurs au lieu de s'arrêter
    for i, v in enumerate(valeurs):
        try:
            float(v)
        except ValueError as e:
            e.add_note(f"ligne {i}")                  # on attache le numéro de ligne à l'erreur
            erreurs.append(e)
    if erreurs:
        raise ExceptionGroup("Lot invalide", erreurs) # un seul « raise » pour toutes les erreurs

try:
    valider_lot(["0.5", "x", "1.2", "y"])             # deux valeurs invalides : "x" (ligne 1) et "y" (ligne 3)
except* ValueError as groupe:                         # « except* » : le groupe contient toutes les ValueError
    print(len(groupe.exceptions), "erreurs :", [e.__notes__[0] for e in groupe.exceptions])

# %% Cellule 38 — Dates : lecture de plusieurs formats
# === CELLULE 38 : Dates — formats multiples ===
from datetime import datetime, timedelta

# Les trois formats présents dans le fichier de mesures
FORMATS_TIMESTAMP = ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S")

def parse_timestamp(texte):
    for fmt in FORMATS_TIMESTAMP:                       # on essaie chaque format à tour de rôle
        try:
            return datetime.strptime(texte.strip(), fmt) # succès : on renvoie tout de suite
        except ValueError:
            continue                                     # échec : format suivant
    raise TimestampInvalide(f"Format inconnu : {texte!r}")  # aucun format ne convient

bruts = ["2025-01-03T04:30:00", "2025-01-03 04:30:00", "03/01/2025 04:30:00"]   # trois écritures du même instant
parses = [parse_timestamp(t) for t in bruts]
print(parses[0], all(p == parses[0] for p in parses))   # all(...) : vrai si TOUTES les comparaisons sont vraies

debut = parses[0]
print(debut + timedelta(minutes=15))                    # ajout d'une durée de 15 minutes
print(debut.strftime("%d/%m/%Y %Hh%M"))                 # datetime -> texte au format français
print(debut.weekday())                                  # jour de la semaine : lundi = 0

# %% Cellule 39 — Fuseaux horaires et nouveautés 3.11
# === CELLULE 39 : Fuseaux horaires ===
from datetime import UTC
from zoneinfo import ZoneInfo

print(datetime.fromisoformat("2025-01-03T04:30:00Z"))   # « Z » = UTC, accepté depuis 3.11

utc = datetime(2025, 1, 3, 4, 30, tzinfo=UTC)           # 04:30 en UTC, en hiver
paris = utc.astimezone(ZoneInfo("Europe/Paris"))        # même instant, vu à Paris
print(utc.isoformat(), "->", paris.isoformat())

# Même heure UTC, mais en été : Paris est alors à UTC+2
ete = datetime(2025, 7, 3, 4, 30, tzinfo=UTC).astimezone(ZoneInfo("Europe/Paris"))
print(ete.isoformat())

print(datetime.now(UTC).tzinfo)                         # Hier : datetime.utcnow() (déprécié depuis 3.12)

# %% Cellule 40 — Fichiers : `pathlib`
# === CELLULE 40 : pathlib ===
from pathlib import Path

DATA = Path("data")                                                # dossier de données, relatif au dossier courant
print(DATA.exists(), [p.name for p in sorted(DATA.glob("*.csv"))]) # glob("*.csv") : tous les fichiers .csv du dossier

fichier = DATA / "sites_reference.csv"                             # « / » assemble : data/sites_reference.csv
print(fichier.suffix, fichier.stem, fichier.stat().st_size, "octets")   # extension, nom sans extension, taille

# %% Cellule 41 — Fichiers : lire un CSV et le BOM UTF-8
# === CELLULE 41 : CSV et BOM ===
import csv

print(fichier.read_bytes()[:3])                   # les 3 premiers octets bruts du fichier
with open(fichier, encoding="utf-8") as f:        # ❌ lecture avec « utf-8 » : le BOM reste dans le texte
    print(repr(f.readline()[:12]))                # repr() rend les caractères invisibles visibles

with open(fichier, encoding="utf-8-sig", newline="") as f:   # ✅ « utf-8-sig » retire le BOM
    sites_ref = list(csv.DictReader(f))           # une liste de dictionnaires
print(len(sites_ref), sites_ref[0])

# %% Cellule 42 — Un dictionnaire accessible par attributs : `__getattr__`
# === CELLULE 42 : __getattr__ ===
class Enregistrement:
    def __init__(self, donnees):
        self._donnees = donnees                      # le dictionnaire d'origine

    def __getattr__(self, nom):                      # appelée quand « nom » n'est pas un attribut normal
        try:
            return self._donnees[nom]                # on répond avec la clé du dictionnaire
        except KeyError:
            raise AttributeError(f"pas de champ {nom!r}") from None   # attribut inconnu

    def __repr__(self):
        return f"Enregistrement({self._donnees})"

ligne = Enregistrement(sites_ref[0])                 # une ligne du CSV lu à la cellule précédente
print(ligne.site_id, ligne.capacity_mw)              # au lieu de ligne["site_id"], ligne["capacity_mw"]
print(hasattr(ligne, "region"), hasattr(ligne, "inconnu"))   # True False : hasattr s'appuie sur AttributeError

# %% Cellule 43 — Expressions régulières : chercher un motif
# === CELLULE 43 : Expressions régulières — chercher ===
import re

texte = "Alerte 2025-01-03T04:30:00 sur SITE_COM_002 : code -999, puis SITE_IND_001 : code -888"

# Motif d'un identifiant de site : SITE_ + 3 lettres majuscules + _ + 3 chiffres
motif_site = r"SITE_[A-Z]{3}_\d{3}"

m = re.search(motif_site, texte)               # search : le PREMIER résultat, ou None
print(m.group(), "| position", m.start())      # group() : le texte trouvé ; start() : où

print(re.findall(motif_site, texte))           # findall : TOUS les résultats, dans une liste
print(re.findall(r"-\d{3}", texte))            # tous les codes négatifs à 3 chiffres

# Les parenthèses créent des GROUPES : on récupère séparément la famille et le numéro
m = re.search(r"SITE_([A-Z]{3})_(\d{3})", texte)
print(m.groups(), "| famille =", m.group(1))

# fullmatch : le texte ENTIER doit correspondre (validation d'un identifiant)
for candidat in ("SITE_IND_001", "SITE_IND_1", "site_ind_001"):
    print(f"{candidat:<14} valide : {bool(re.fullmatch(motif_site, candidat))}")

# %% Cellule 44 — Expressions régulières : remplacer et classer
# === CELLULE 44 : Expressions régulières — remplacer et classer ===

# --- 1. Remplacer : masquer les codes d'erreur
print(re.sub(r"-\d{3}", "<CODE>", texte))

# --- 2. Réordonner une date : (année)-(mois)-(jour) devient jour/mois/année
#     \1 = année, \2 = mois, \3 = jour
print(re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", "2025-01-03"))

# --- 3. Groupes nommés : lire une ligne de journal dans un dictionnaire
LIGNE = re.compile(r"(?P<ts>\S+) (?P<site>SITE_\w+) (?P<niveau>[A-Z]+) (?P<code>-?\d+)")
extrait = LIGNE.search("2025-01-03T04:30:00 SITE_COM_002 ERROR -999")
print(extrait.groupdict())

# --- 4. Classer les formats de date du vrai fichier de mesures
FORMATS_REGEX = {
    "ISO avec T":      re.compile(r"^\d{4}-\d{2}-\d{2}T"),        # 2025-01-03T04:30:00
    "ISO avec espace": re.compile(r"^\d{4}-\d{2}-\d{2} "),        # 2025-01-03 04:30:00
    "Jour/Mois/Année": re.compile(r"^\d{2}/\d{2}/\d{4} "),        # 03/01/2025 04:30:00
}
with open(DATA / "consommation_echantillon.csv", encoding="utf-8-sig", newline="") as f:
    horodatages = [ligne["timestamp"] for ligne in csv.DictReader(f)]

for nom, motif in FORMATS_REGEX.items():
    print(f"{nom:<16} : {sum(1 for h in horodatages if motif.match(h))} lignes")   # match : motif au DÉBUT du texte

# %% Cellule 45 — Fichiers : écrire du JSON, lire du TOML
# === CELLULE 45 : JSON et TOML ===
import json
import tomllib

sortie = Path("out")
sortie.mkdir(exist_ok=True)                                     # crée le dossier « out »
(sortie / "sites.json").write_text(json.dumps(sites_ref, indent=2, ensure_ascii=False), encoding="utf-8")   # objet -> fichier JSON
print(json.loads((sortie / "sites.json").read_text(encoding="utf-8"))[1]["site_id"])                        # fichier JSON -> objet

# On écrit un petit fichier de configuration TOML...
Path("config.toml").write_text('''[chemins]
entree = "data/consommation_echantillon.csv"
sites = "data/sites_reference.csv"

[seuils]
anomalies_max = 0.10
taux_charge_critique = 0.8
''', encoding="utf-8")
# ... puis on le lit (mode binaire obligatoire pour tomllib)
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
print(config["seuils"], type(config["seuils"]["anomalies_max"]).__name__)

# %% Cellule 46 — Gestionnaire de contexte : `with`, `__enter__`, `__exit__`
# === CELLULE 46 : Gestionnaire de contexte ===
import time

class Chronometre:
    def __enter__(self):                         # appelée à l'entrée du « with »
        self.debut = time.perf_counter()
        self.erreur = None
        return self                              # devient la variable après « as »

    def __exit__(self, type_erreur, erreur, trace):   # appelée à la sortie, même après une erreur
        self.duree = time.perf_counter() - self.debut
        self.erreur = erreur                     # None si tout s'est bien passé
        return False                             # False : l'erreur éventuelle continue de remonter

# Cas normal : on mesure la lecture du fichier
with Chronometre() as chrono:
    lignes_mesures = list(csv.DictReader(open(DATA / "consommation_echantillon.csv", encoding="utf-8-sig", newline="")))
print(len(lignes_mesures), "lignes | durée mesurée :", chrono.duree >= 0)

# Cas d'erreur : __exit__ est appelée quand même
try:
    with Chronometre() as chrono2:
        float("abc")                             # lève une ValueError
except ValueError:
    print("erreur vue par __exit__ :", type(chrono2.erreur).__name__, "| durée mesurée :", chrono2.duree >= 0)

# %% Cellule 47 — Journalisation avec `logging`
# === CELLULE 47 : logging ===
import logging

# Niveau INFO : les messages DEBUG seront masqués ; « format » décrit la ligne affichée
logging.basicConfig(level=logging.INFO, format="%(levelname)-8s | %(name)s | %(message)s", force=True)
log = logging.getLogger("qualite")                  # un journal nommé

log.debug("Message de mise au point (masqué au niveau INFO)")
log.info("Lecture de %s", config["chemins"]["entree"])            # %s remplacé par le 2e argument
log.warning("%d mesures avec code erreur", 9)
try:
    convertir_mesure("abc")
except ValueError as erreur:
    log.error("Conversion impossible : %s", erreur)

# %% Cellule 48 — Le problème : du code coincé dans le notebook
# === CELLULE 48 : Ce que la session a défini ===

import inspect

# On liste les fonctions et classes définies dans CE notebook (module « __main__ »)
utiles = sorted(nom for nom, obj in globals().items()
                if (inspect.isfunction(obj) or inspect.isclass(obj))     # une fonction ou une classe
                and obj.__module__ == "__main__"                         # définie ici, pas importée
                and obj.__name__ != "<lambda>" and not nom.startswith("_"))
print(len(utiles), "objets définis dans ce notebook :")
print(utiles)

# %% Étape manuelle — Créer le module `energie_utils.py` (1/2) : constantes et conversions
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('energie_utils.py', 'w', encoding='utf-8') as f:
    f.write('"""energie_utils.py — Utilitaires de qualité de données du réseau EnergiaNord."""\nimport csv\nfrom datetime import datetime\nfrom types import MappingProxyType\nfrom typing import Iterator\n\nCODES_ERREUR = MappingProxyType({\n    -999: "Capteur hors service",\n    -888: "Valeur non transmise",\n    -777: "Recalibrage en cours",\n})\n\nFORMATS_TIMESTAMP = (\n    "%Y-%m-%dT%H:%M:%S",\n    "%Y-%m-%d %H:%M:%S",\n    "%d/%m/%Y %H:%M:%S",\n)\n\n\nclass TimestampInvalide(ValueError):\n    """Levée quand un timestamp ne correspond à aucun format connu."""\n\n\ndef parse_timestamp(texte: str) -> datetime:\n    """Convertit un timestamp texte (3 formats possibles) en datetime."""\n    for fmt in FORMATS_TIMESTAMP:\n        try:\n            return datetime.strptime(texte.strip(), fmt)\n        except ValueError:\n            continue\n    raise TimestampInvalide(f"Format inconnu : {texte!r}")\n\n\ndef convertir_mesure(texte: str) -> float | None:\n    """\'\' -> None ; \'0.865\' -> 0.865 ; \'-999\' -> -999.0"""\n    texte = texte.strip()\n    if texte == "":\n        return None\n    return float(texte)\n')
print('energie_utils.py :', len(open('energie_utils.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 49 — Importer un module
# === CELLULE 49 : Importer energie_utils ===
import importlib
importlib.invalidate_caches()             # le fichier vient d'être créé : on force Python à re-scanner le dossier

import energie_utils                      # charge le module
print(energie_utils.__name__, "|", Path(energie_utils.__file__).name)   # nom du module | fichier source

# Les fonctions définies dans le module (et pas importées d'ailleurs)
print([n for n, o in vars(energie_utils).items()
       if callable(o) and getattr(o, "__module__", None) == "energie_utils"])

from energie_utils import parse_timestamp as lire_date       # import ciblé, avec un alias
print(lire_date("03/01/2025 04:30:00"))
print(energie_utils.CODES_ERREUR[-999])                      # une constante du module, par son nom qualifié

# %% Cellule 50 — Où Python cherche-t-il un module ?
# === CELLULE 50 : sys.path et modules trouvés ===
import sys
import importlib.util

# La liste ordonnée des dossiers où Python cherche
for rang, dossier in enumerate(sys.path):
    print(rang, dossier)

print()
# Où se trouve energie_utils ? Dans le dossier de travail : le premier de la liste
origine = Path(importlib.util.find_spec("energie_utils").origin)
print("energie_utils.py est dans le dossier courant :", origine.parent == Path.cwd())

# json est dans la bibliothèque standard ; un module qui n'existe nulle part donne None
print(importlib.util.find_spec("json") is not None, importlib.util.find_spec("module_inexistant"))

try:
    import module_inexistant              # introuvable dans tous les dossiers
except ModuleNotFoundError as erreur:
    print(f"ModuleNotFoundError : {erreur}")

# %% Étape manuelle — Compléter `energie_utils.py` (2/2) : qualité et lecture
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('energie_utils.py', 'a', encoding='utf-8') as f:
    f.write('\n\ndef qualifier_mesure(valeur: float | None) -> str:\n    """Classe une mesure : MANQUANTE, CODE_ERREUR, NEGATIVE ou VALIDE."""\n    match valeur:\n        case None:\n            return "MANQUANTE"\n        case v if v in CODES_ERREUR:\n            return "CODE_ERREUR"\n        case v if v < 0:\n            return "NEGATIVE"\n        case _:\n            return "VALIDE"\n\n\ndef lire_csv(chemin) -> Iterator[dict]:\n    """Lit un CSV (UTF-8 avec ou sans BOM) et produit un dictionnaire par ligne."""\n    with open(chemin, encoding="utf-8-sig", newline="") as f:\n        yield from csv.DictReader(f)\n')
print('energie_utils.py :', len(open('energie_utils.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 51 — Le module est en cache : `reload`
# === CELLULE 51 : Modifier un module puis le recharger ===

# Le fichier contient maintenant qualifier_mesure, mais le module en mémoire est l'ancienne version
try:
    from energie_utils import qualifier_mesure
except ImportError as erreur:
    print("Avant reload : ImportError :", str(erreur).split(" (")[0])

importlib.reload(energie_utils)           # relit energie_utils.py depuis le disque

from energie_utils import qualifier_mesure
print("Après reload :", qualifier_mesure(0.865), qualifier_mesure(-999.0), qualifier_mesure(None), qualifier_mesure(-3.2))

# %% Cellule 52 — La bibliothèque standard : des modules déjà installés
# === CELLULE 52 : Modules de la bibliothèque standard ===
from collections import Counter                     # compteur d'occurrences
from statistics import mean, median, stdev          # statistiques simples

from energie_utils import convertir_mesure, lire_csv, qualifier_mesure   # NOTRE module

lignes = list(lire_csv("data/consommation_echantillon.csv"))              # lire_csv est un générateur : list() le consomme
convertis = [convertir_mesure(l["consumption_mw"]) for l in lignes]       # texte -> décimal, ou None
etats = Counter(qualifier_mesure(v) for v in convertis)                   # combien de VALIDE, MANQUANTE...
print(len(lignes), "lignes |", dict(etats))

valeurs = [v for v in convertis if qualifier_mesure(v) == "VALIDE"]       # on ne garde que les valides
print(f"moyenne {mean(valeurs):.3f} | médiane {median(valeurs):.3f} | écart-type {stdev(valeurs):.3f}")

# %% Étape manuelle — Créer `demo_main.py` : l'idiome `main`
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('demo_main.py', 'w', encoding='utf-8') as f:
    f.write('"""Démonstration de l\'idiome main."""\nimport sys\n\n\ndef main(argv=None) -> None:\n    arguments = sys.argv[1:] if argv is None else argv\n    print(f"__name__ vaut : {__name__}")\n    print(f"Arguments     : {arguments}")\n\n\nif __name__ == "__main__":\n    main()\n')
print('demo_main.py :', len(open('demo_main.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 53 — L'idiome `if __name__ == "__main__"`
# === CELLULE 53 : L'idiome main ===
import subprocess

# 1) Exécution comme un SCRIPT (un vrai processus Python)
resultat = subprocess.run([sys.executable, "demo_main.py", "site_1", "--verbose"],
                          capture_output=True, text=True)
print(resultat.stdout)

# 2) Import comme un MODULE : rien ne se lance tout seul
importlib.invalidate_caches()
import demo_main
print(demo_main.__name__)

# 3) On appelle main() nous-mêmes, avec nos propres arguments
demo_main.main(["appel", "depuis", "un", "notebook"])

# %% Cellule 54 — Arguments de ligne de commande avec `argparse`
# === CELLULE 54 : argparse ===
import argparse

parser = argparse.ArgumentParser(prog="analyse_sites",
                                 description="Contrôle qualité des mesures de consommation")
parser.add_argument("--input", "-i", required=True, help="fichier CSV des mesures")               # obligatoire
parser.add_argument("--seuil", type=float, default=0.10, help="taux d'anomalies maximal toléré")  # converti en float
parser.add_argument("--json", action="store_true", help="écrire aussi un rapport JSON")           # drapeau : vrai s'il est présent

# On simule une ligne de commande avec une liste
args = parser.parse_args(["-i", "data/consommation_echantillon.csv", "--seuil", "0.15", "--json"])
print(args)
print(type(args.seuil).__name__, args.seuil + 1)      # float 1.15 : la conversion a eu lieu

# %% Étape manuelle — Créer `analyse_sites.py` (1/3) : comptage
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('analyse_sites.py', 'w', encoding='utf-8') as f:
    f.write('"""analyse_sites.py — Contrôle qualité des mesures de consommation (Atelier 1).\n\nUsage :\n    python analyse_sites.py --input data/consommation_echantillon.csv\n    python analyse_sites.py -i data/consommation_echantillon.csv --seuil 0.05 --json\n"""\nimport argparse\nimport json\nimport logging\nimport sys\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nfrom energie_utils import (TimestampInvalide, convertir_mesure, lire_csv,\n                           parse_timestamp, qualifier_mesure)\n\nlog = logging.getLogger("analyse_sites")\n\n\ndef compter(chemin_mesures: Path) -> dict:\n    """Parcourt le fichier : états par site, somme des valeurs valides, doublons."""\n    vues = set()\n    qualite = defaultdict(Counter)\n    somme_mw = defaultdict(float)\n    doublons = horodatages_invalides = 0\n\n    for ligne in lire_csv(chemin_mesures):\n        cle = tuple(ligne.values())\n        if cle in vues:                       # doublon exact : on l\'écarte\n            doublons += 1\n            continue\n        vues.add(cle)\n\n        try:\n            parse_timestamp(ligne["timestamp"])\n        except TimestampInvalide:\n            horodatages_invalides += 1\n\n        etat = qualifier_mesure(convertir_mesure(ligne["consumption_mw"]))\n        qualite[ligne["site_id"]][etat] += 1\n        if etat == "VALIDE":\n            somme_mw[ligne["site_id"]] += float(ligne["consumption_mw"])\n\n    return {"qualite": qualite, "somme_mw": somme_mw, "doublons": doublons,\n            "horodatages_invalides": horodatages_invalides}\n')
print('analyse_sites.py :', len(open('analyse_sites.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 55 — Vérifier l'étape 1 : `compter`
# === CELLULE 55 : Tester compter ===
importlib.invalidate_caches()
import analyse_sites                                          # le fichier vient d'être créé

brut = analyse_sites.compter(Path("data/consommation_echantillon.csv"))
print("doublons écartés      :", brut["doublons"])
print("horodatages invalides :", brut["horodatages_invalides"])
print("SITE_IND_001          :", dict(brut["qualite"]["SITE_IND_001"]))   # états comptés pour un site
print("nombre de sites       :", len(brut["qualite"]))

# %% Étape manuelle — Compléter `analyse_sites.py` (2/3) : indicateurs par site
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('analyse_sites.py', 'a', encoding='utf-8') as f:
    f.write('\n\ndef analyser(chemin_mesures: Path, chemin_sites: Path) -> dict:\n    """Calcule les indicateurs qualité et charge par site."""\n    sites = {s["site_id"]: s for s in lire_csv(chemin_sites)}\n    brut = compter(chemin_mesures)\n\n    par_site = {}\n    for site_id, compteur in sorted(brut["qualite"].items()):\n        total = sum(compteur.values())\n        valides = compteur["VALIDE"]\n        conso_moyenne = brut["somme_mw"][site_id] / valides if valides else 0.0\n        capacite = float(sites[site_id]["capacity_mw"])\n        par_site[site_id] = {\n            "mesures": total,\n            "valides": valides,\n            "manquantes": compteur["MANQUANTE"],\n            "codes_erreur": compteur["CODE_ERREUR"],\n            "taux_anomalies": round((total - valides) / total, 3),\n            "conso_moyenne_mw": round(conso_moyenne, 3),\n            "taux_charge_moyen": round(conso_moyenne / capacite, 3),\n        }\n\n    total = sum(s["mesures"] for s in par_site.values())\n    anomalies = sum(s["mesures"] - s["valides"] for s in par_site.values())\n    return {\n        "sites": par_site,\n        "doublons_ecartes": brut["doublons"],\n        "horodatages_invalides": brut["horodatages_invalides"],\n        "taux_anomalies_global": round(anomalies / total, 3),\n    }\n')
print('analyse_sites.py :', len(open('analyse_sites.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 56 — Vérifier l'étape 2 : `analyser`
# === CELLULE 56 : Tester analyser ===
importlib.reload(analyse_sites)                    # on a ajouté « analyser » dans le fichier

rapport = analyse_sites.analyser(Path("data/consommation_echantillon.csv"), Path("data/sites_reference.csv"))
print(rapport["sites"]["SITE_IND_001"])            # les indicateurs d'un site
print("taux global :", rapport["taux_anomalies_global"])

# %% Étape manuelle — Terminer `analyse_sites.py` (3/3) : affichage, arguments, `main`
# Étape manuelle : les apprenants créent ce fichier dans l'Explorateur ; ici, création automatique.
with open('analyse_sites.py', 'a', encoding='utf-8') as f:
    f.write('\n\ndef afficher(rapport: dict) -> None:\n    print(f"{\'Site\':<14}{\'Mesures\':>8}{\'Valides\':>9}{\'Manq.\':>7}{\'Codes\':>7}{\'Anom.\':>8}{\'Charge\':>9}")\n    for site_id, s in rapport["sites"].items():\n        print(f"{site_id:<14}{s[\'mesures\']:>8}{s[\'valides\']:>9}{s[\'manquantes\']:>7}"\n              f"{s[\'codes_erreur\']:>7}{s[\'taux_anomalies\']:>8.1%}{s[\'taux_charge_moyen\']:>9.1%}")\n    print(f"Doublons écartés      : {rapport[\'doublons_ecartes\']}")\n    print(f"Horodatages invalides : {rapport[\'horodatages_invalides\']}")\n    print(f"Taux d\'anomalies      : {rapport[\'taux_anomalies_global\']:.1%}")\n\n\ndef lire_arguments(argv=None) -> argparse.Namespace:\n    parser = argparse.ArgumentParser(prog="analyse_sites", description=__doc__.splitlines()[0])\n    parser.add_argument("--input", "-i", required=True, type=Path, help="fichier CSV des mesures")\n    parser.add_argument("--sites", type=Path, default=Path("data/sites_reference.csv"),\n                        help="référentiel des sites (défaut : %(default)s)")\n    parser.add_argument("--seuil", type=float, default=0.10, help="taux d\'anomalies maximal toléré")\n    parser.add_argument("--json", action="store_true", help="écrire out/rapport_qualite.json")\n    return parser.parse_args(argv)\n\n\ndef main(argv=None) -> int:\n    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")\n    args = lire_arguments(argv)\n\n    log.info("Analyse de %s", args.input)\n    rapport = analyser(args.input, args.sites)\n    afficher(rapport)\n\n    if args.json:\n        Path("out").mkdir(exist_ok=True)\n        Path("out/rapport_qualite.json").write_text(\n            json.dumps(rapport, indent=2, ensure_ascii=False), encoding="utf-8")\n        log.info("Rapport écrit dans out/rapport_qualite.json")\n\n    if rapport["taux_anomalies_global"] > args.seuil:\n        log.error("Seuil dépassé : %.1f %% > %.1f %%",\n                  rapport["taux_anomalies_global"] * 100, args.seuil * 100)\n        return 1\n    log.info("Qualité conforme au seuil")\n    return 0\n\n\nif __name__ == "__main__":\n    sys.exit(main())\n')
print('analyse_sites.py :', len(open('analyse_sites.py', encoding='utf-8').read().splitlines()), 'lignes')

# %% Cellule 57 — Exécuter le script comme en production
# === CELLULE 57 : Lancer analyse_sites.py ===
def lancer(*arguments):
    resultat = subprocess.run([sys.executable, "analyse_sites.py", *arguments],
                              capture_output=True, text=True)
    print(resultat.stdout, end="")                     # sortie normale (le tableau)
    print(resultat.stderr, end="")                     # messages du journal (logging)
    print(f"[code de sortie : {resultat.returncode}]\n")

lancer("--input", "data/consommation_echantillon.csv", "--json")           # seuil par défaut : 10 %
lancer("--input", "data/consommation_echantillon.csv", "--seuil", "0.05")  # seuil strict : 5 %

# %% Cellule 58 — Pont vers Fabric : un code portable
# === CELLULE 58 : Chemins portables local / Fabric ===
DANS_FABRIC = importlib.util.find_spec("notebookutils") is not None   # True seulement dans Fabric
print(f"Exécution dans Fabric : {DANS_FABRIC}")

def resoudre_chemin(nom_fichier: str) -> Path:
    if DANS_FABRIC:
        return Path("/lakehouse/default/Files/data_python") / nom_fichier   # dossier du Lakehouse
    return Path("data") / nom_fichier                                       # dossier local

chemin = resoudre_chemin("consommation_echantillon.csv")
print(chemin, "| existe :", chemin.exists())
