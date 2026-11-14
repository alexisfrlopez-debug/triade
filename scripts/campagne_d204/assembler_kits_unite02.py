#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kits_unite02.py — LES DEUX KITS DE L'UNITÉ 2 ASSEMBLÉS ET
ÉPROUVÉS au labo (le modèle assembler_kit_unite01.py, D153 : le labo NE
PEUT PAS exécuter les scénarios — Windows + les VRAIS kernel32 exigés, le
cœur même du run terrain, D122).

  1. L'ASSEMBLAGE des DEUX kits : kit-unite-loupe-02-T/ (la pièce
     loupe.exe 98354ff6… recoupée contre le build cristallisé + la
     notation + le brouillon + le scénario + le lanceur + les QUATRE
     témoins + LISEZMOI + EMPREINTES) et kit-unite-loupe-02-C/ (la pièce
     loupe-02-c.dll 925cd019… + le source C + le .def + le scénario + le
     lanceur + les MÊMES témoins + LISEZMOI + EMPREINTES) ;
  2. LA COMPILATION : py_compile des DEUX scénarios ;
  3. L'ÉPREUVE D'EXTRACTION VIERGE : chaque zip extrait dans un répertoire
     NEUF, chaque empreinte re-constatée ;
  4. LES ZIPS déposés au bac du labo (download/kits-unite-02/)."""
from __future__ import annotations

import hashlib
import os
import py_compile
import shutil
import sys
import tempfile
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))          # .../work/triade
sys.path.insert(0, os.path.join(REPO, "loupe"))
import harnais_noyau as HN   # noqa: E402  (la génération FIXE des témoins)

CAMP = os.path.dirname(os.path.abspath(__file__))
UT = os.path.join(CAMP, "unite-02-T")
UC = os.path.join(CAMP, "unite-02-C")
BAC = "/home/z/my-project/download/kits-unite-02"

SHA_EXE = "98354ff6ac07cf291199e9b33acd032bf2285bcbc7490b8f174bc24f91770f6e"
SHA_DLL = ("925cd0190d6b3073407737a6a7588db6a9de5ec17ae578a99de2fef5"
           "1c61bcad")
TEMOINS_KIT01 = {  # la génération FIXE — recoupée à la gravure du kit 01
    "temoin-1.bin": "df7e70e5021544f4834bbee64a9e3789febc4be81470df629cad6ddb03320a5c",
    "temoin-384.bin": "3396717b98b4859b20ec0d673dcf168314834fc170fbc6b877f4eb32461d68c6",
    "temoin-3f.bin": "c5fc1f28e471059d56a892ba82df1e215f5263aafd8c43fdb0e76e110d1d5ca3",
    "vide.bin": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def refus(nom, detail):
    print(f"[assemblage] REFUS {nom} : {detail}")
    sys.exit(2)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


LISEZMOI_T = """﻿LISEZMOI — LE KIT DE L'UNITÉ 2 : LOUPE-02 LIRE × BRAS T
(la campagne de comparaison des workflows D204 ; le kit livré par le labo
au coffre /test en son dossier daté — le GUI vous attend à l'onglet 1·KIT
de l'unité loupe-02 × T)
========================================================================

L'OBJET : la DEUXIÈME unité de la partie contrôlée — le bloc loupe-02
LIRE au BRAS T (la notation scellée). La pièce de ce kit est le build du
plan où le slot loupe-02 (RVA 0x4240, 320 o) porte LA NOTATION DE
CAMPAGNE : écrite à la main par l'agent depuis le contrat loupe-02:R1 (la
fenêtre d'octets au tampon de session, BORNÉE par la taille réelle — la
double borne — puis LE RECOUVREMENT du journal d'édition : ce que
l'utilisateur a écrit survit au défilement). LES DIX-SEPT autres blocs
demeurent les SCELLÉS du projet — dont loupe-01, qui APPELLE la notation
de campagne à CHAQUE naissance de session (la fenêtre à la vue 0) : la
première fenêtre de chaque fichier ouvert naît de la pièce mesurée.

LA CONSTRUCTION (consignée, les défauts nommés AVANT toute livraison) :
l'oracle écrit-avant-code (le modèle Python du contrat, avant la
notation) ; la notation à la main — TROIS fautes nommées en route :
l'adressage à deux bases (keystone refuse [r14 + rcx*16] — le pointeur
qui marche), le débordement du slot (325 o > 320 : la notation compactée
à 292 o — le lu pré-contré, le min par cmov, la poignée tenue en
registre), la chute de boucle (le recouvrement tombait dans l'échec
système — le saut du succès rendu explicite) ; la cristallisation : DIX
rebuilds consécutifs IDENTIQUES (sha256 98354ff6…) ; l'oracle du bloc au
labo : 22 VERT, 0 ROUGE (le différentiel à 2 032 décalages sur les
témoins + le scellé proxy.exe, le recouvrement aux bords et non aligné,
les rejets au tampon empoisonné, l'échec ReadFile armé, la falsification
détectable) ; l'épreuve du scénario livré (son juge extrait par AST,
confronté à un contre-modèle : 2 000 cas VERT — une frontière dupliquée
y fut prise, nommée, corrigée AVANT le run).

LE GESTE (tout au clic, l'ordre de jeu d'une unité) :
  1. AU GUI (TRIADE_gui_campagne_v1 ou TRIADE_gui_tous_runs_v1), onglet
     1·KIT de l'unité loupe-02 × T : CHOISIR CE DOSSIER
     (kit-unite-loupe-02-T-20261114) — le GUI recoupe les EMPREINTES
     gravées (une divergence, rien ne court) ;
  2. onglet 2·RUN : LANCER LANCEUR-UNITE-02-T.bat (le lanceur officiel —
     il court dans SA PROPRE console, INTACT) : le scénario recoupe la
     pièce à la gravure, charge l'image (LoadLibraryEx DONT_RESOLVE),
     résout lui-même les six feuilles kernel32 du noyau, ouvre la
     session PAR LOUPE-01 SCELLÉ (la fenêtre née de la notation de
     campagne), appelle loupe-02 aux décalages du kit, juge par le
     modèle indépendant (les découpes hashlib), et écrit le témoin ; le
     dossier preuves-unite02/ naît sur votre machine ;
  3. onglet 3·TÉMOIN : ouvrir preuves-unite02\\temoin-unite02.txt au
     bloc-notes, le DATER, le SIGNER DE VOTRE MAIN — jamais automatisé
     (D99) — puis renvoyer le dossier ENTIER au coffre /test ;
  4. aux onglets 4-7 : la ligne de carnet AU GESTE (M3), la livraison
     (M1 — la cap tenue par le GUI : au plus TROIS par bloc, l'arrêt au
     premier vert), les défauts nommés s'il y en a, le chrono (M4) ;
  5. le labo recoupe le run revenu — PUIS l'unité suivante commence.

LES PIÈCES DU KIT :
  loupe.exe                     la pièce (127 488 o, sha256 98354ff6…) —
                                le build du plan, le slot loupe-02 portant
                                la notation de campagne (292 o de code,
                                28 de padding NOP) ;
  notation-loupe-02-lire.asm    la notation LIVRÉE (l'explicite, résolue
                                par l'auteur d'arithmétique d'adresses) ;
  brouillon-loupe-02-lire.asm   le brouillon de la main (les choix, les
                                fautes nommées en commentaires) ;
  scenario-unite02.py           le scénario (le chargeur + le juge) ;
  LANCEUR-UNITE-02-T.bat        le lanceur officiel (la capture console
                                en UTF-8 des deux côtés du tuyau) ;
  temoin-1.bin, temoin-384.bin, temoin-3f.bin, vide.bin
                                les témoins du kit (la génération FIXE du
                                labo, graine 20261107 — les MÊMES octets
                                que le kit 01) ;
  EMPREINTES-KIT-UNITE-02-T.txt la gravure (chaque pièce, sha256) ;
  le présent LISEZMOI.

LES ÉCARTS NOMMÉS DU RUN TERRAIN (consignés, jamais maquillés) :
  — le vecteur V4 (l'échec système) arme un VERROU DE PLAGE (LockFile
    d'un second détenteur sur [0, 384)) : si le système de fichiers
    l'ignore au terrain, le vecteur est NOMMÉ ABSENT — jamais maquillé ;
  — l'accès refusé ne s'arme pas proprement au terrain (le refus d'ACL
    dépend du compte) : hors du contrat de loupe-02, rien à armer.

LA FRONTIÈRE : le run est À VOUS (CA6 — le labo ne court JAMAIS le
terrain) ; le témoin se signe de VOTRE MAIN (D99) ; le renvoi du dossier
ENTIER vous appartient ; la pièce ne bouge pas (l'empreinte gravée — une
divergence, rien ne court).

*La consignation vit au journal de travail (l'Entrée 290) ; le détail du
plan à PLAN_PREREGISTRE_COMPARAISON.md (a78caf8c…, VERROUILLÉ).*
"""

LISEZMOI_C = """﻿LISEZMOI — LE KIT DE L'UNITÉ 2 : LOUPE-02 LIRE × BRAS C
(la campagne de comparaison des workflows D204 ; le kit livré par le labo
au coffre /test en son dossier daté — le GUI vous attend à l'onglet 1·KIT
de l'unité loupe-02 × C)
========================================================================

L'OBJET : LA MÊME deuxième unité du bras C (le flux standard, C + gcc),
le même contrat de couche I que le bras T (loupe-02 LIRE, révision 1) :
la fenêtre d'octets au tampon de session, BORNÉE par la taille réelle,
PUIS le recouvrement du journal d'édition. LA PIÈCE NEUVE :
loupe_02_lire (le source écrit par l'agent) ; le bloc session
(loupe_01_ouvrir, loupe_03_fermer) repris TEL QUEL du kit 01 (le flux
standard réutilise son code éprouvé — l'écart nommé du bras C : sa
première fenêtre est lue INLINE à l'ouverture, là où le loupe-01 du plan
APPELLE loupe-02).

LA COMPILATION (M4, la commande consignée) : x86_64-w64-mingw32-gcc-posix
-O2 -shared -o loupe-02-c.dll loupe-02-c.c loupe-02-c.def — le
compilateur croisé gcc-mingw-w64 14.2 extrait des paquets Debian SANS
ROOT au bac du labo (l'outillage au travail/mingw-debs ; la reconstruction
du bac après la remise à zéro du conteneur : les paquets 14.2.0-19+27+b1
du jour — l'horodatage PE du lieur fait que deux builds ne sont jamais
identiques : NOMMÉ, la cristallisation est la règle du bras T, pas du
bras C ; la gravure fixe LA pièce).

LES ÉPREUVES DU LABO (D122 — la logique rejouée au POSIX) :
  — LE CONTRAT ENTIER REJOUÉ : 20 VERT 0 ROUGE (le harnais à shims du
    kit 01, SetFilePointerEx déclarée À LA VALEUR — le vrai prototype,
    l'écart nommé du kit 01 : la pièce 01 ne l'appelait pas, la
    déclaration n'y fut jamais éprouvée ; le tiroir d'échec de ReadFile
    pour E4) : les quatre témoins, les frontières, le recouvrement aux
    bords et non aligné, le journal INTACT, les rejets au poison, la
    session qui SURVIT à l'échec, la falsification détectable ;
  — LES CONTRÔLES BINAIRES : 18 VERT 0 ROUGE (PE32+ DLL x86-64, les SIX
    exports — loupe_02_lire et journal DONNÉE compris —, les SIX feuilles
    kernel32 : SetFilePointerEx PRÉSENTE cette fois, l'écart nommé du
    kit 01 n'existe plus ; AUCUN appel CRT dans la clôture des trois
    fonctions ; les relocations) ;
  — L'ÉPREUVE DU SCÉNARIO LIVRÉ : son juge extrait par AST, confronté à
    un contre-modèle indépendant : 2 000 cas VERT ; la découverte et la
    traversée d'imports du scénario exécutées CONTRE la pièce elle-même
    (l'image mappée par sections) : les SIX exports et les SIX feuilles
    lus.

LE GESTE (tout au clic, l'ordre de jeu d'une unité — INCHANGÉ) :
  1. AU GUI (TRIADE_gui_tous_runs_v1), onglet 1·KIT de l'unité
     loupe-02 × C : CHOISIR CE DOSSIER (kit-unite-loupe-02-C-20261114) —
     le GUI recoupe les EMPREINTES gravées (une divergence, rien ne
     court) ;
  2. onglet 2·RUN : LANCER LANCEUR-UNITE-02-C.bat (le lanceur officiel —
     il court dans SA PROPRE console, INTACT) : le scénario recoupe la
     pièce à la gravure, charge l'image (LoadLibraryEx DONT_RESOLVE),
     découvre les adresses PAR LA TABLE D'EXPORTS, résout les feuilles
     kernel32 AUX SLOTS RÉELS de la table d'imports (l'édition v2 du kit
     01 : le terminateur au CHAMP Name, les gardes fail-closed), ouvre
     la session par la pièce, appelle loupe_02_lire aux décalages du
     kit, juge par le modèle indépendant, et écrit le témoin ; le
     dossier preuves-unite02C/ naît ;
  3. onglet 3·TÉMOIN : ouvrir preuves-unite02C\\temoin-unite02C.txt au
     bloc-notes, le DATER, le SIGNER DE VOTRE MAIN — jamais automatisé
     (D99) — puis renvoyer le dossier ENTIER au coffre /test ;
  4. aux onglets 4-7 : la ligne de carnet AU GESTE (M3), la livraison
     (M1 — au plus TROIS par bloc, l'arrêt au premier vert), les défauts
     nommés s'il y en a, le chrono (M4) ;
  5. le labo recoupe le run revenu — PUIS l'unité suivante commence.

LES PIÈCES DU KIT :
  loupe-02-c.dll        la pièce (95 413 o, sha256 925cd019…) ;
  loupe-02-c.c/.def     le source et la définition des exports (la
                        livraison du bras C : le binaire ET le source) ;
  scenario-unite02C.py  le scénario (la découverte, la résolution, le
                        juge) ;
  LANCEUR-UNITE-02-C.bat le lanceur officiel (la capture console en
                        UTF-8 des deux côtés du tuyau) ;
  temoin-1.bin, temoin-384.bin, temoin-3f.bin, vide.bin
                        les témoins du kit (les MÊMES octets que le kit
                        T — la génération fixe du labo) ;
  EMPREINTES-KIT-UNITE-02-C.txt la gravure (chaque pièce, sha256) ;
  le présent LISEZMOI.

LES ÉCARTS NOMMÉS (consignés, jamais maquillés) :
  — la première fenêtre lue INLINE au bloc session (le loupe-01 du plan
    APPELLE loupe-02 : l'écart structurel du bras C, nommé) ;
  — le vecteur V4 arme un VERROU DE PLAGE (LockFile d'un second
    détenteur) : si le système de fichiers l'ignore au terrain, NOMMÉ
    ABSENT ;
  — les imports du CRT de lancement mingw (InitializeCriticalSection…)
    vivent à la table sans jamais être appelées : sous DONT_RESOLVE
    aucun point d'entrée ne court — l'audit de la clôture le prouve ;
  — l'écho du lanceur rend « preuves-unite02C\\temoin… » : le « \\t » du
    chemin rendu TAB par la console — COSMÉTIQUE, nommé (le kit 01 le
    portait déjà).

LA FRONTIÈRE : le run est À VOUS (CA6 — le labo ne court JAMAIS le
terrain) ; le témoin se signe de VOTRE MAIN (D99) ; le renvoi du dossier
ENTIER vous appartient ; la pièce ne bouge pas (l'empreinte gravée — une
divergence, rien ne court).

*La consignation vit au journal de travail (l'Entrée 290) ; le détail du
plan à PLAN_PREREGISTRE_COMPARAISON.md (a78caf8c…, VERROUILLÉ).*
"""

LANCEUR_T = """﻿@echo off
rem LANCEUR-UNITE-02-T.bat — LE LANCEUR OFFICIEL du kit de l'unite 2
rem (loupe-02 x bras T, la campagne D204). Le run court dans SA PROPRE
rem console, INTACT : le GUI ne l'intercepte jamais (CA6).
rem Le temoin ne se signe JAMAIS ici : votre main, toujours (D99).
rem La capture console vit en UTF-8 des deux cotes du tuyau (l'edition
rem v2 du kit 01, la meme discipline).
title TRIADE - Unite 2 (loupe-02 lire x T) - campagne D204
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
set PYTHONIOENCODING=utf-8
powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; python scenario-unite02.py 2>&1 | Tee-Object -FilePath run-console-unite02.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite02\temoin-unite02.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
pause
exit /b %CODE%
"""

LANCEUR_C = """﻿@echo off
rem LANCEUR-UNITE-02-C.bat — LE LANCEUR OFFICIEL du kit de l'unite 2
rem x BRAS C (loupe-02 lire, la campagne D204, le flux standard gcc -O2).
rem Le run court dans SA PROPRE console, INTACT : le GUI ne l'intercepte
rem jamais (CA6). Le temoin ne se signe JAMAIS ici : votre main (D99).
rem La capture console vit en UTF-8 des deux cotes du tuyau (l'edition
rem v2 du kit 01, la meme discipline).
title TRIADE - Unite 2 x bras C (loupe-02 lire, gcc -O2) - campagne D204
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
set PYTHONIOENCODING=utf-8
powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; python scenario-unite02C.py 2>&1 | Tee-Object -FilePath run-console-unite02C.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite02C\temoin-unite02C.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
pause
exit /b %CODE%
"""


def assembler(bras, dossier, pieces, lisezmoi, lanceur, empreintes_nom,
              titre_gravure):
    sortie = os.path.join(CAMP, f"unite-02-{bras}", "kit")
    if os.path.exists(sortie):
        shutil.rmtree(sortie)
    os.makedirs(sortie)
    gravure = [titre_gravure, ""]
    for source, nom in pieces:
        shutil.copy2(source, os.path.join(sortie, nom))
        gravure.append(f"{sha(os.path.join(sortie, nom))}  {nom}")
    with open(os.path.join(sortie, f"LANCEUR-UNITE-02-{bras}.bat"), "w",
              encoding="utf-8-sig", newline="\r\n") as f:
        f.write(lanceur)
    gravure.append(f"{sha(os.path.join(sortie, f'LANCEUR-UNITE-02-{bras}.bat'))}"
                   f"  LANCEUR-UNITE-02-{bras}.bat")
    with open(os.path.join(sortie, f"LISEZMOI-KIT-UNITE-02-{bras}.txt"), "w",
              encoding="utf-8-sig", newline="\r\n") as f:
        f.write(lisezmoi)
    gravure.append(f"{sha(os.path.join(sortie, f'LISEZMOI-KIT-UNITE-02-{bras}.txt'))}"
                   f"  LISEZMOI-KIT-UNITE-02-{bras}.txt")
    with open(os.path.join(sortie, empreintes_nom), "w",
              encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(gravure) + "\n")
    # le zip
    zip_chemin = os.path.join(sortie, dossier + ".zip")
    with zipfile.ZipFile(zip_chemin, "w", zipfile.ZIP_DEFLATED) as z:
        for nom in sorted(os.listdir(sortie)):
            if nom != dossier + ".zip":
                z.write(os.path.join(sortie, nom), arcname=f"{dossier}/{nom}")
    return sortie, zip_chemin, gravure


def epreuve_vierge(zip_chemin, gravure):
    """L'extraction vierge : chaque empreinte re-constatée."""
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zip_chemin) as z:
            z.extractall(tmp)
        attendus = {}
        for ligne in gravure:
            parties = ligne.split()
            if len(parties) == 2 and len(parties[0]) == 64:
                attendus[parties[1]] = parties[0]
        racine = os.path.join(tmp, os.listdir(tmp)[0])
        for nom, h in attendus.items():
            if sha(os.path.join(racine, nom)) != h:
                refus("EXTRACTION-VIERGE", f"{nom} diverge au zip")
        return len(attendus)


def main() -> int:
    print("=== L'ASSEMBLAGE DES DEUX KITS DE L'UNITÉ 2 (loupe-02 LIRE) ===")

    # la pièce T : recoupée contre le build cristallisé
    if sha(os.path.join(UT, "piece", "loupe.exe")) != SHA_EXE:
        refus("PIÈCE-T", "loupe.exe != le build cristallisé 98354ff6…")
    # la pièce C : recoupée contre la compilation consignée
    if sha(os.path.join(UC, "epreuves", "loupe-02-c.dll")) != SHA_DLL:
        refus("PIÈCE-C", "loupe-02-c.dll != la compilation 925cd019…")

    # les témoins : la génération FIXE, recoupée à la gravure du kit 01
    temoins = HN.composer_temoins()
    tmp_temoins = os.path.join(CAMP, "unite-02-T", "kit-temoins")
    os.makedirs(tmp_temoins, exist_ok=True)
    with open(os.path.join(tmp_temoins, "temoin-1.bin"), "wb") as f:
        f.write(temoins["temoin-1.bin"])
    with open(os.path.join(tmp_temoins, "temoin-384.bin"), "wb") as f:
        f.write(temoins["temoin-384.bin"])
    with open(os.path.join(tmp_temoins, "temoin-3f.bin"), "wb") as f:
        f.write(temoins["temoin-3f.bin"])
    with open(os.path.join(tmp_temoins, "vide.bin"), "wb") as f:
        f.write(b"")
    for nom, h in TEMOINS_KIT01.items():
        if sha(os.path.join(tmp_temoins, nom)) != h:
            refus("TÉMOIN", f"{nom} != la gravure du kit 01 ({h[:16]}…)")
    print(f"[témoins] la génération FIXE recoupée : les QUATRE == la gravure "
          f"du kit 01 octet pour octet")

    # la compilation des scénarios
    py_compile.compile(os.path.join(UT, "scenario-unite02.py"),
                       doraise=True)
    py_compile.compile(os.path.join(UC, "scenario-unite02C.py"),
                       doraise=True)
    print("[py_compile] les DEUX scénarios compilent")

    # ---- le kit T -----------------------------------------------------------
    pieces_t = [
        (os.path.join(UT, "piece", "loupe.exe"), "loupe.exe"),
        (os.path.join(UT, "notation", "loupe-02-lire.asm"),
         "notation-loupe-02-lire.asm"),
        (os.path.join(UT, "brouillons", "loupe-02-lire.asm"),
         "brouillon-loupe-02-lire.asm"),
        (os.path.join(UT, "scenario-unite02.py"), "scenario-unite02.py"),
    ] + [(os.path.join(tmp_temoins, n), n) for n in TEMOINS_KIT01]
    sortie_t, zip_t, gravure_t = assembler(
        "T", "kit-unite-loupe-02-T-20261114", pieces_t, LISEZMOI_T,
        LANCEUR_T, "EMPREINTES-KIT-UNITE-02-T.txt",
        "﻿EMPREINTES — LE KIT DE L'UNITÉ 2 (loupe-02 LIRE × bras T, la "
        "campagne D204)\n(chaque pièce sha256 — le GUI recoupe à l'onglet "
        "1·KIT ; une divergence, rien ne court)")
    n_t = epreuve_vierge(zip_t, gravure_t)
    print(f"[kit T] {len(gravure_t) - 2} pièces gravées, l'extraction "
          f"vierge {n_t}/{n_t} VERT — {os.path.basename(zip_t)}")

    # ---- le kit C -----------------------------------------------------------
    pieces_c = [
        (os.path.join(UC, "epreuves", "loupe-02-c.dll"), "loupe-02-c.dll"),
        (os.path.join(UC, "source", "loupe-02-c.c"), "loupe-02-c.c"),
        (os.path.join(UC, "source", "loupe-02-c.def"), "loupe-02-c.def"),
        (os.path.join(UC, "scenario-unite02C.py"), "scenario-unite02C.py"),
    ] + [(os.path.join(tmp_temoins, n), n) for n in TEMOINS_KIT01]
    sortie_c, zip_c, gravure_c = assembler(
        "C", "kit-unite-loupe-02-C-20261114", pieces_c, LISEZMOI_C,
        LANCEUR_C, "EMPREINTES-KIT-UNITE-02-C.txt",
        "﻿EMPREINTES — LE KIT DE L'UNITÉ 2 (loupe-02 LIRE × bras C, la "
        "campagne D204)\n(chaque pièce sha256 — le GUI recoupe à l'onglet "
        "1·KIT ; une divergence, rien ne court)")
    n_c = epreuve_vierge(zip_c, gravure_c)
    print(f"[kit C] {len(gravure_c) - 2} pièces gravées, l'extraction "
          f"vierge {n_c}/{n_c} VERT — {os.path.basename(zip_c)}")

    # ---- le bac du labo -------------------------------------------------------
    os.makedirs(BAC, exist_ok=True)
    for d in (sortie_t, sortie_c):
        for nom in os.listdir(d):
            shutil.copy2(os.path.join(d, nom),
                         os.path.join(BAC, nom))
    print(f"[bac] les DEUX kits versés à {BAC}")
    print("\nLES DEUX KITS DE L'UNITÉ 2 SONT ASSEMBLÉS, GRAVÉS ET "
          "ÉPROUVÉS — prêts pour la livraison au coffre /test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
