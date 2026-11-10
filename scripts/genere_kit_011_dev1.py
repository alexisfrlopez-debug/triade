#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""genere_kit_011_dev1.py — Le générateur du KIT 0.1.1-dev.1 (la vague de
LA VERSION COMMANDÉE, D178/D179 — le treizième kit, loupe-kit-13/).

L'ÈRE 0.1.0 EST REFERMÉE SUR SA BALISE SCELLÉE (D178 : le onzième run
recoupé 39/39 — T0→T7 TOUT VERT POUR LA QUATRIÈME FOIS, LA CASCADE 205
VÉCUE ENTIÈRE LA PREMIÈRE FOIS, LA VITRINE VIVANTE LA SECONDE FOIS ;
la balise `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE, loupe.exe 054de960…
INTACT — LE JALON M10 FRANCHI). LE DÉVELOPPEUR A COMMANDÉ « b et c » :
la consolidation v0.9.0 de la spécification ET le soldage de la dette
[R10-PÉRIMÉE] à la version 0.1.1+ (D179).

LA PIÈCE 0.1.1-dev.1 NAÎT DE LA RECOMPOSITION MÊME (le build la scelle
dans sa carte génération 17) :
  - LA DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE : les 17 sommes de
    l'ère dev.5 que les retouches des Entrées 210/214 changèrent sans
    rafraîchir — la porte R10 de la pièce porte désormais LA VÉRITÉ de
    ses blocs (chaque somme == son bloc relu, par construction) ;
  - LE QWORD VERSION PORTÉ 0x00010008 → 0x00010101 (l'ère 0.1.1-dev.1) ;
  - 0 OCTET AILLEURS : le code BYTE-IDENTIQUE au vécu des onze runs
    (R4 : le contrat stable ; R7 : les adresses intactes) — la pièce
    0.1.0 (054de960…) demeurant au git et au coffre.

LE KIT : la pièce 0.1.1-dev.1 (sha256 c1115105…, 127 488 o) + le
scénario dev.12 PORTÉ aux constantes de l'ère (SHA_EXE, VERSION_R10,
le docstring) + le témoin vitrine (les littéraux portés) + le LISEZMOI
(le chapitre 0.1.1 : la dette soldée, la version commandée, LE
DOUZIÈME RUN — le même critère : le scénario ENTIER T0 → S0 → LA
LIAISON ET la vitrine vivante ; LA BALISE `loupe 0.1.1` SE SCELLERA
SUR LE VERT RECOUPÉ, le miroir D165/D170).

Entrées : les TROIS pièces du kit dev.12 (loupe/terrain/, le dépôt —
== le kit couru au onzième run, recoupé md5 pièce à pièce) + loupe.exe
(sha256 c1115105…) ; sorties : build-011-dev1/ + kit-loupe.zip.
"""
import hashlib
import os
import py_compile
import shutil
import sys
import zipfile

SRC = "/home/z/my-project/triade/loupe/terrain"   # le kit dev.12 du dépôt
PIECE = "/home/z/my-project/triade/loupe/loupe.exe"
DST = "/home/z/my-project/build-011-dev1"

SHA_011 = ("c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef66"
           "6fd76ceb93e61d1")
SHA_010 = ("054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69")
MD5_SC12 = "7353e7342ff056eeb428f0d78445a7de"     # le scénario dev.12 couru
MD5_BAT12 = "2d3bc31f54c7140de1d931be0d80fb93"    # le bat dev.12 couru
MD5_LIV12 = "8ec9553b0b02fe7ecb25870a427e8e42"    # le LISEZMOI dev.12 couru

os.makedirs(DST, exist_ok=True)


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


# ═════════════════════════════════════════════════════════════════════
# 0. LA PIÈCE — 0.1.1-dev.1 NÉE DE LA RECOMPOSITION (la dette soldée)
# ═════════════════════════════════════════════════════════════════════
piece = open(PIECE, "rb").read()
assert len(piece) == 127488, f"taille inattendue {len(piece)}"
assert hashlib.sha256(piece).hexdigest() == SHA_011, \
    "la pièce n'est pas la 0.1.1-dev.1 (c1115105…) !"
open(os.path.join(DST, "loupe.exe"), "wb").write(piece)
print(f"[0] la pièce 0.1.1-dev.1 : {len(piece)} o, sha256 {SHA_011[:16]}… "
      f"(la dette [R10-PÉRIMÉE] soldée à la naissance — la 0.1.0 "
      f"[054de960…] demeure au git et au coffre)")

# ═════════════════════════════════════════════════════════════════════
# 1. LE SCÉNARIO — les constantes portées à l'ère 0.1.1
# ═════════════════════════════════════════════════════════════════════
assert md5(os.path.join(SRC, "scenario-loupe.py")) == MD5_SC12, \
    "la source n'est pas le scénario dev.12 couru au onzième run"
sc = open(os.path.join(SRC, "scenario-loupe.py"), encoding="utf-8").read()
print(f"[1] le scénario dev.12 lu : {len(sc)} octets, md5 {MD5_SC12[:8]}…")


def remplace(ancien, nouveau, combien=1):
    global sc
    n = sc.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:70]!r}"
    sc = sc.replace(ancien, nouveau)


# 1a. l'en-tête — la vague 0.1.1-dev.1
remplace("NATURE (kit dev.12, l'Entrée 216).",
         "NATURE (kit 0.1.1-dev.1, l'Entrée 221).")

# 1b. la pièce — le bloc descriptif de loupe.exe (l'ère 0.1.1 en tête,
#     l'histoire dev.8 demeurant en retrait)
remplace(
    "  loupe.exe   le build 0.1.0-dev.8 du jalon M10 — 127 488 o, sha256\n"
    "              054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69\n"
    "              (LA RETOUCHE DE L'ENTRÉE 214 : le neuvième run a tenu",
    "  loupe.exe   le build 0.1.1-dev.1 du jalon M10 — 127 488 o, sha256\n"
    "              c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1\n"
    "              (LA VERSION COMMANDÉE PAR LE DÉVELOPPEUR — D178/D179 :\n"
    "              l'ère 0.1.0 est REFERMÉE sur sa balise SCELLÉE [le\n"
    "              onzième run recoupé 39/39, la vitrine vivante la\n"
    "              seconde fois — loupe.exe 054de960… INTACT au git et au\n"
    "              coffre] ; la 0.1.1 naît de LA RECOMPOSITION MÊME : LA\n"
    "              DETTE [R10-PÉRIMÉE] SOLDÉE À LA NAISSANCE [les 17\n"
    "              sommes de l'ère dev.5 rafraîchies à la vérité des\n"
    "              blocs — chaque somme == son bloc relu, par\n"
    "              construction], LE QWORD VERSION PORTÉ 0x00010008 →\n"
    "              0x00010101, 0 OCTET AILLEURS [le code BYTE-IDENTIQUE\n"
    "              au vécu des onze runs — R4 : le contrat stable, R7 :\n"
    "              les adresses intactes] ; la carte est à sa GÉNÉRATION\n"
    "              RÉELLE 17 ; LA BALISE `loupe 0.1.1` se scellera PAR\n"
    "              FAIT DE CARTE sur le vert recoupé DU DOUZIÈME RUN.\n"
    "              L'HISTOIRE DE L'ÈRE 0.1.0 (LA RETOUCHE DE L'ENTRÉE\n"
    "              214 : le neuvième run a tenu")

# 1c. les constantes — SHA_EXE et VERSION_R10
remplace(
    'SHA_EXE = ("054de960c31425d022f6900f27e59bdd'
    '82a120b0b3fe543a67e778867e9c7a69")',
    'SHA_EXE = ("c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef66'
    '6fd76ceb93e61d1")')
remplace(
    "VERSION_R10 = 0x00010008          # loupe 0.1.0-dev.8 (le qword @0x2E80 —",
    "VERSION_R10 = 0x00010101          # loupe 0.1.1-dev.1 (le qword @0x2E80 —")
remplace(
    "                                   # la retouche de l'Entrée 214 : [OFT-QWORD]",
    "                                   # la version commandée D179 : la dette")
remplace(
    "                                   # nommé sur les octets du run 9, les QUATRE",
    "                                   # [R10-PÉRIMÉE] soldée, l'ère 0.1.1 ouverte)")
remplace(
    "                                   # OFT compactés au pas DWORD du chargeur)",
    "                                   # (l'ère 0.1.0 SCELLÉE demeure : 054de960…)")
remplace("le présent scénario dev.12 MARCHE LUI-MÊME",
         "le présent scénario 0.1.1-dev.1 MARCHE LUI-MÊME")

# 1d. l'assert de l'empreinte — le sha COMPLET de la 0.1.0 ne vit plus
#     nulle part (seule la forme tronquée historique « 054de960… » demeure)
assert sc.count("054de960c31425d022f6900f27e59bdd"
                "82a120b0b3fe543a67e778867e9c7a69") == 0, \
    "le sha complet 0.1.0 doit avoir quitté le scénario (l'assert vivant = la 0.1.1)"
assert sc.count(SHA_011) == 2, \
    "le sha 0.1.1 doit vivre au docstring ET à l'assert SHA_EXE"
open(os.path.join(DST, "scenario-loupe.py"), "w", encoding="utf-8",
     newline="\n").write(sc)
py_compile.compile(os.path.join(DST, "scenario-loupe.py"), doraise=True)
print(f"[1] le scénario 0.1.1-dev.1 : {len(sc)} octets — SHA_EXE/VERSION_R10 "
      f"portés, py_compile VERT")

# ═════════════════════════════════════════════════════════════════════
# 2. LE TÉMOIN VITRINE — les littéraux portés
# ═════════════════════════════════════════════════════════════════════
assert md5(os.path.join(SRC, "temoin-vitrine.bat")) == MD5_BAT12, \
    "la source n'est pas le bat dev.12 couru au onzième run"
bat = open(os.path.join(SRC, "temoin-vitrine.bat"), encoding="latin-1").read()
assert bat.count("loupe.exe 0.1.0-dev.8 ^(kit dev.12, Entree 216^)") == 1
bat = bat.replace(
    "loupe.exe 0.1.0-dev.8 ^(kit dev.12, Entree 216^)",
    "loupe.exe 0.1.1-dev.1 ^(kit 0.1.1-dev.1, Entree 221^)")
assert bat.count("LE TEMOIN VITRINE DU KIT LOUPE (Entree 216)") == 1
bat = bat.replace("LE TEMOIN VITRINE DU KIT LOUPE (Entree 216)",
                  "LE TEMOIN VITRINE DU KIT LOUPE (Entree 221, l'ere 0.1.1)")
assert bat.count("kit 0.1.1-dev.1, Entree 221") == 1
assert bat.count("dev.12") == 0
open(os.path.join(DST, "temoin-vitrine.bat"), "w", encoding="latin-1",
     newline="\n").write(bat)
print(f"[2] le témoin vitrine 0.1.1-dev.1 : {len(bat)} octets — les deux "
      f"littéraux portés")

# ═════════════════════════════════════════════════════════════════════
# 3. LE LISEZMOI — le chapitre 0.1.1 (la dette soldée, le douzième run)
# ═════════════════════════════════════════════════════════════════════
assert md5(os.path.join(SRC, "LISEZMOI-KIT-LOUPE.md")) == MD5_LIV12, \
    "la source n'est pas le LISEZMOI dev.12 couru au onzième run"
lz = open(os.path.join(SRC, "LISEZMOI-KIT-LOUPE.md"), encoding="utf-8").read()


def lz_remplace(ancien, nouveau, combien=1):
    global lz
    n = lz.count(ancien)
    assert n == combien, f"ancre LISEZMOI {n}x (attendu {combien}) : {ancien[:70]!r}"
    lz = lz.replace(ancien, nouveau)


# 3a. LE CHAPITRE 0.1.1 — inséré après le récit du dixième run (avant
#     « ## 1. Ce que ce kit contient »)
ancre_chapitre = "## 1. Ce que ce kit contient"
assert lz.count(ancre_chapitre) == 1, "l'ancre du chapitre est introuvable"
lz = lz.replace(ancre_chapitre,
    "> **LE ONZIÈME RUN A TENU — L'ÈRE 0.1.0 EST REFERMÉE SUR SA BALISE\n"
    "> SCELLÉE** (l'Entrée 217 : T0 → T7 TOUT VERT POUR LA QUATRIÈME\n"
    "> FOIS, LA CASCADE 205 VÉCUE ENTIÈRE LA PREMIÈRE FOIS, LA VITRINE\n"
    "> VIVANTE LA SECONDE FOIS — 0 et 0 — le vert recoupé 39/39 : LA\n"
    "> BALISE `loupe 0.1.0` SCELLÉE PAR FAIT DE CARTE [D178], loupe.exe\n"
    "> 054de960… INTACT — **LE JALON M10 FRANCHI, la méthode TRIADE\n"
    "> entière prouvée par la CRÉATION : onze runs, onze leçons**).\n"
    ">\n"
    "> **LA PRÉSENTE VAGUE EST CELLE DE LA VERSION COMMANDÉE : 0.1.1-dev.1\n"
    "> (D178/D179 — le développeur a commandé le soldage de la dette\n"
    "> [R10-PÉRIMÉE] à la version 0.1.1+)** : la pièce 0.1.0 scellée\n"
    "> portait à sa porte R10 les SOMMES DE L'ÈRE dev.5 — les retouches\n"
    "> des Entrées 210/214 changèrent les octets des blocs SANS\n"
    "> rafraîchir la table (dette nommée au scellage même, jamais un\n"
    "> hot-fix d'un scellé) ; la 0.1.1 naît de LA RECOMPOSITION : **LA\n"
    "> DETTE SOLDÉE À LA NAISSANCE** — les 17 sommes rafraîchies à la\n"
    "> VÉRITÉ des blocs (chaque somme == son bloc relu, par\n"
    "> construction), le qword version porté 0x00010008 → 0x00010101,\n"
    "> **0 OCTET AILLEURS** — le code BYTE-IDENTIQUE au vécu des ONZE\n"
    "> RUNS (R4 : le contrat stable ; R7 : les adresses intactes) ;\n"
    "> **loupe.exe 0.1.1-dev.1**, 127 488 o, sha256\n"
    "> `c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1`,\n"
    "> la carte GÉNÉRATION 17 (la 16 demeure celle de la balise 0.1.0\n"
    "> scellée) ; la pièce 0.1.0 (054de960…) demeure AU GIT ET AU\n"
    "> COFFRE.\n"
    ">\n"
    "> **LE DOUZIÈME RUN — LE MÊME CRITÈRE, LA BALISE 0.1.1** : le\n"
    "> scénario ENTIER (T0 → S0 → LA LIAISON — tous les temps déjà vécus\n"
    "> verts au onzième run, la MÊME mécanique, la pièce nouvelle à la\n"
    "> place de l'ancienne) ET LA VITRINE VIVANTE (les deux codes à 0 —\n"
    "> la vitrine a déjà vécu deux fois, la même pièce au code près) ;\n"
    "> SI LE VERT TIENT : LA BALISE `loupe 0.1.1` SCELLÉE sur run\n"
    "> terrain recoupé — la version de la dette soldée, le miroir\n"
    "> D165/D170 (la porte est de processus) ; si une mort vient : le\n"
    "> journal la nommera — chaque défaut a été nommé, chaque défaut a\n"
    "> reçu sa retouche.\n\n"
    + ancre_chapitre)

# 3b. les littéraux de version — le contenu du kit
lz_remplace(
    "loupe-kit-12/\n├── loupe.exe          l'ARTEFACT 0.1.0-dev.8 (127 488 o, sha256\n"
    "│                      054de960… — LA RETOUCHE DE L'ENTRÉE 214 : les",
    "loupe-kit-13/\n"
    "├── loupe.exe          l'ARTEFACT 0.1.1-dev.1 (127 488 o, sha256\n"
    "│                      c1115105… — LA VERSION COMMANDÉE D179 : la")
lz_remplace(
    "│                      QUATRE OFT compactés au pas DWORD du chargeur —\n"
    "│                      [OFT-QWORD] nommé au run 9, la sixième mort\n"
    "│                      reçut SA retouche ; le .text/.text2/.data\n"
    "│                      octet-identiques au dev.7, les adresses scellées\n"
    "│                      INTACTES, la taille CONSTANTE ; lecture seule\n"
    "│                      pour le run ; la carte privée ne voyage JAMAIS\n"
    "│                      avec l'artefact, R1) ;",
    "│                      dette [R10-PÉRIMÉE] SOLDÉE à la naissance [les\n"
    "│                      17 sommes rafraîchies à la vérité des blocs],\n"
    "│                      le qword porté 0x00010101, 0 OCTET AILLEURS\n"
    "│                      [le code byte-identique au vécu des ONZE RUNS\n"
    "│                      — R4/R7] ; lecture seule pour le run ; la carte\n"
    "│                      privée ne voyage JAMAIS avec l'artefact, R1) ;")
lz_remplace("├── scenario-loupe.py  LE SCÉNARIO dev.12 (python SEUL : ctypes,",
            "├── scenario-loupe.py  LE SCÉNARIO 0.1.1-dev.1 (python SEUL : ctypes,")
lz_remplace("├── temoin-vitrine.bat LE TÉMOIN VITRINE dev.12 — PORTANT : les quatre",
            "├── temoin-vitrine.bat LE TÉMOIN VITRINE 0.1.1-dev.1 — PORTANT : les quatre")

# 3c. le dossier du kit (l'occurrence de l'arborescence fut portée par
#     3b — il demeure celle du geste § 2)
n_kit12 = lz.count("loupe-kit-12/")
assert n_kit12 >= 1, f"le dossier loupe-kit-12/ n'apparaît que {n_kit12}x"
lz = lz.replace("loupe-kit-12/", "loupe-kit-13/")
lz_remplace("`loupe-kit-12b/` si besoin", "`loupe-kit-13b/` si besoin")
lz_remplace("celui de dev.1 à dev.11 par exemple",
            "celui de dev.1 à dev.12 par exemple")

# 3d. la section 2 — l'ère de la vitrine (elle a DEUX FOIS vécu)
lz_remplace(
    "sont attendus : la vitrine dev.8 A DÉJÀ VÉCU AU DIXIÈME RUN** (0 et\n"
    "   0, la première fois après six morts — le onzième run la reverra\n"
    "   vivre, la dette du kit n'étant que le scénario ENTIER ; la pièce\n"
    "   est acquittée : le défaut [FREE-SANS-TYPE] fut celui du KIT —",
    "sont attendus : la vitrine A DÉJÀ VÉCU DEUX FOIS (0 et 0 au\n"
    "   dixième, 0 et 0 au onzième run — le code est le MÊME à la porte\n"
    "   R10 près : la 0.1.1 doit vivre pareil ; la pièce est acquittée\n"
    "   de toute charge : les défauts restants furent ceux du KIT —")

# 3e. la section 5 — le critère du douzième run (la balise 0.1.1)
lz_remplace(
    "constats croisés contre le dépôt, les empreintes recalculées — **LE\n"
    "DIXIÈME RUN A DÉJÀ VÉCU LA VITRINE (0 et 0, la première fois :\n"
    "l'application née de TRIADE a vécu chez son utilisateur) ; LA DETTE\n"
    "RESTANTE EST LE SCÉNARIO ENTIER : S0 ET LA LIAISON, jamais courus à\n"
    "ce jour**. ET SI LE VERT TIENT — le scénario ENTIER (T0 → S0 → LA LIAISON, le contrôle\n"
    "D54 ÉTENDU en tête, LA CASCADE RÉPARÉE) ET LA VITRINE VIVANTE (les deux\n"
    "codes à 0) : LA BALISE `loupe 0.1.0` SCELLÉE sur run terrain recoupé —\n"
    "LE JALON M10, la méthode TRIADE entière prouvée par la CRÉATION : de\n"
    "l'intention (la couche I) à l'octet vécu chez son utilisateur.**",
    "constats croisés contre le dépôt, les empreintes recalculées — **LE\n"
    "ONZIÈME RUN A TOUT VÉCU : le scénario ENTIER (T0 → S0 → LA LIAISON)\n"
    "ET LA VITRINE (0 et 0 la seconde fois) — la 0.1.0 est SCELLÉE\n"
    "(D178) ; la 0.1.1 porte LE MÊME MÉCANISME à la pièce près [la\n"
    "porte R10 véridique, le qword porté — 0 octet de code changé]**.\n"
    "ET SI LE VERT TIENT — le scénario ENTIER (T0 → S0 → LA LIAISON, le\n"
    "contrôle D54 ÉTENDU en tête, LA CASCADE RÉPARÉE) ET LA VITRINE\n"
    "VIVANTE (les deux codes à 0) : LA BALISE `loupe 0.1.1` SCELLÉE sur\n"
    "run terrain recoupé — LA VERSION DE LA DETTE SOLDÉE (D179), le\n"
    "miroir D165/D170 : la porte est de processus.**")

# 3f. les invariants du LISEZMOI
assert lz.count("loupe-kit-13/") >= 2, "le dossier du kit"
assert lz.count("[R10-PÉRIMÉE]") >= 2, "la dette nommée"
assert lz.count("SOLDÉE") >= 3, "la dette soldée (chapitre, arbre, critère)"
assert lz.count("c1115105") >= 2, "l'empreinte de la pièce neuve"
assert lz.count("`loupe 0.1.1`") >= 1, "la balise du douzième run"
open(os.path.join(DST, "LISEZMOI-KIT-LOUPE.md"), "w", encoding="utf-8",
     newline="\n").write(lz)
print(f"[3] le LISEZMOI 0.1.1-dev.1 : {len(lz)} octets — loupe-kit-13, la "
      f"dette soldée, le douzième run")

# ═════════════════════════════════════════════════════════════════════
# 4. LE ZIP — les QUATRE pièces du contrat, extraction vierge
# ═════════════════════════════════════════════════════════════════════
QUATRE = ["loupe.exe", "scenario-loupe.py", "temoin-vitrine.bat",
          "LISEZMOI-KIT-LOUPE.md"]
zip_ch = os.path.join(DST, "kit-loupe.zip")
if os.path.exists(zip_ch):
    os.remove(zip_ch)
with zipfile.ZipFile(zip_ch, "w", zipfile.ZIP_DEFLATED) as z:
    for nom in QUATRE:
        z.write(os.path.join(DST, nom), nom)

extraction = os.path.join(DST, "_extraction")
shutil.rmtree(extraction, ignore_errors=True)
os.makedirs(extraction)
with zipfile.ZipFile(zip_ch) as z:
    z.extractall(extraction)
    assert sorted(z.namelist()) == sorted(QUATRE), \
        "le zip ne porte pas les QUATRE pièces"
for nom in QUATRE:
    a = open(os.path.join(DST, nom), "rb").read()
    b = open(os.path.join(extraction, nom), "rb").read()
    assert a == b, f"l'extraction diffère : {nom}"
shutil.rmtree(extraction)

zip_bytes = open(zip_ch, "rb").read()
print(f"[4] kit-loupe.zip : {len(zip_bytes)} o, md5 "
      f"{hashlib.md5(zip_bytes).hexdigest()}… — extraction VIERGE, "
      f"les QUATRE pièces du contrat")
print("\nLA VAGUE 0.1.1-dev.1 EST NÉE : build-011-dev1/ + kit-loupe.zip")
print("la dette [R10-PÉRIMÉE] soldée à la naissance ; le code "
      "byte-identique au vécu des onze runs ; le douzième run attendu")
