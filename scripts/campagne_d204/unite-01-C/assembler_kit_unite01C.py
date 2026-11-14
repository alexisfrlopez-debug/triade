#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_unite01C.py — L'ASSEMBLAGE DU KIT DE L'UNITÉ 1 × BRAS C
(loupe-01, la campagne D204) : la pièce (le source C + le .def + la DLL
compilée gcc -O2), le scénario adapté au PE compilé, les QUATRE témoins
(les MÊMES octets que le kit du bras T — la génération fixe), le
lanceur, le LISEZMOI, la GRAVURE générée du montage même, le zip."""
import hashlib
import pathlib
import shutil
import subprocess
import zipfile

UNITE = pathlib.Path("/home/z/my-project/work/triade/scripts/campagne_d204"
                     "/unite-01-C")
BAC = pathlib.Path("/home/z/my-project/download/kit_unite_loupe_01_C")
KIT = BAC / "kit-unite-loupe-01-C-20261114"
TEMOINS_SRC = pathlib.Path("/home/z/my-project/work/uni01")


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


if BAC.exists():
    shutil.rmtree(BAC)
KIT.mkdir(parents=True)

# --- 1. la pièce (le source, la définition, le binaire) -----------------------
for nom in ("loupe-01-c.c", "loupe-01-c.def"):
    shutil.copy2(UNITE / "source" / nom, KIT / nom)
shutil.copy2(UNITE / "epreuves" / "loupe-01-c.dll", KIT / "loupe-01-c.dll")

# --- 2. le scénario (l'adaptation au PE compilé) ------------------------------
shutil.copy2(UNITE / "scenario-unite01C.py", KIT / "scenario-unite01C.py")

# --- 3. les témoins (les MÊMES octets que le kit T — recoupés) ----------------
GRAVURE_T = {}
for ligne in (TEMOINS_SRC / "EMPREINTES-KIT-UNITE-01-T.txt").read_text(
        encoding="utf-8-sig").splitlines():
    p = ligne.strip().split(None, 1)
    if len(p) == 2 and len(p[0]) == 64:
        GRAVURE_T[p[1].strip()] = p[0]
for nom in ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin"):
    src = TEMOINS_SRC / nom
    assert sha256(src) == GRAVURE_T[nom], f"le témoin {nom} diverge du kit T !"
    shutil.copy2(src, KIT / nom)
    print(f"[témoin identique] {nom}  {sha256(src)[:16]}… == la gravure du kit T")

# --- 4. le lanceur (la capture console en UTF-8, les textes du bras C) --------
bat = """@echo off
rem LANCEUR-UNITE-01-C.bat — LE LANCEUR OFFICIEL du kit de l'unite 1
rem x BRAS C (loupe-01, la campagne D204, le flux standard gcc -O2).
rem Le run court dans SA PROPRE console, INTACT : le GUI ne l'intercepte
rem jamais (CA6). Le temoin ne se signe JAMAIS ici : votre main (D99).
rem La capture console vit en UTF-8 des deux cotes du tuyau (l'edition
rem v2 du lanceur du bras T, la meme discipline).
title TRIADE - Unite 1 x bras C (loupe-01, gcc -O2) - campagne D204
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
set PYTHONIOENCODING=utf-8
powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; python scenario-unite01C.py 2>&1 | Tee-Object -FilePath run-console-unite01C.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite01C\temoin-unite01C.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
pause
exit /b %CODE%
"""
(KIT / "LANCEUR-UNITE-01-C.bat").write_bytes(
    b"\xef\xbb\xbf" + bat.replace("\n", "\r\n").encode("utf-8"))

# --- 5. le LISEZMOI -------------------------------------------------------------
lisezmoi = """LISEZMOI — LE KIT DE L'UNITÉ 1 : LOUPE-01 OUVRIR × BRAS C
(la campagne de comparaison des workflows D204 ; le kit livré par le labo
au coffre /test en son dossier daté — le GUI vous attend à l'onglet 1·KIT
de l'unité loupe-01 × C)
========================================================================

L'OBJET : la PREMIÈRE unité du BRAS C (le flux standard, C + gcc) — le
MÊME contrat de couche I que le bras T (loupe-01 OUVRIR, révision 3),
lu comme cahier des charges. La pièce de ce kit est la DLL COMPILÉE du
source C écrit par le MÊME agent au fil de ONZE éditions — la phase
spec (le contrat lu, 5 605 tokens), la phase oracle (les attentes du
juge dérivées du contrat AVANT le code, 4 423 tokens), la phase
source-c (14 660 tokens), SEPT correctifs comptés (39 224 tokens) et la
phase tests-c (3 563 tokens — 67 475 tokens au total, tous LUS DU LOG
d'usage, zéro estimation). La compilation : gcc -O2 -shared (la commande
consignée au journal M4 du labo). Les épreuves du labo AVANT la
livraison : la couche MD5+SHA-256 32 VERT 0 ROUGE (toutes les frontières
du rembourrage, l'absorption irrégulière — le juge hashlib) ; le contrat
ENTIER 17 VERT 0 ROUGE au POSIX (D122 — les quatre témoins champ à
champ, les rejets d'OS, la borne 2 Gio, la session double, le chemin
trop long) ; les contrôles binaires 16 VERT 0 ROUGE (le format PE32+
DLL, les QUATRE exports, les feuilles kernel32 aux slots réels, AUCUN
appel CRT dans la clôture des fonctions — le CRT ne vit jamais sous
DONT_RESOLVE, les relocations).

LE GESTE (tout au clic, l'ordre de jeu d'une unité) :
  1. AU GUI (TRIADE_gui_tous_runs_v1), onglet 1·KIT de l'unité
     loupe-01 × C : CHOISIR CE DOSSIER — le GUI recoupe les EMPREINTES
     gravées (une divergence, rien ne court) ;
  2. onglet 2·RUN : LANCER LANCEUR-UNITE-01-C.bat (le lanceur officiel —
     il court dans SA PROPRE console, INTACT) : le scénario recoupe la
     pièce à la gravure, charge l'image (LoadLibraryEx DONT_RESOLVE),
     découvre les adresses PAR LA TABLE D'EXPORTS de la pièce, résout
     lui-même les feuilles kernel32 AUX SLOTS RÉELS de sa table
     d'imports, appelle loupe_01_ouvrir aux témoins du kit, juge par le
     modèle indépendant (hashlib), et écrit le témoin ; le dossier
     preuves-unite01C/ naît sur votre machine ;
  3. onglet 3·TÉMOIN : ouvrir preuves-unite01C\\temoin-unite01C.txt au
     bloc-notes, le DATER, le SIGNER DE VOTRE MAIN — jamais automatisé
     (D99) — puis renvoyer le dossier ENTIER au coffre /test ;
  4. aux onglets 4-7 : la ligne de carnet AU GESTE (M3), la livraison
     (M1 — la cap tenue par le GUI : au plus TROIS par bloc, l'arrêt au
     premier vert), les défauts nommés s'il y en a, le chrono (M4) ;
  5. le labo recoupe le run revenu — PUIS l'unité suivante commence.

LES PIÈCES DU KIT :
  loupe-01-c.dll        la pièce (la DLL PE32+ compilée gcc -O2 — le
                        binaire de la livraison du bras C) ;
  loupe-01-c.c          le SOURCE de la pièce (le code écrit par
                        l'agent — la métrique M1 côté pièce le compte ;
                        la gravure le recoupe comme toute pièce) ;
  loupe-01-c.def        la définition des exports (loupe_01_ouvrir,
                        loupe_03_fermer, cadre DATA, panneau DATA) ;
  scenario-unite01C.py  le scénario (le chargeur adapté au PE compilé :
                        la découverte par les tables, la résolution aux
                        slots réels, les MÊMES vecteurs, le modèle
                        indépendant, le témoin) ;
  LANCEUR-UNITE-01-C.bat le lanceur officiel (le double-clic) ;
  temoin-1.bin, temoin-384.bin, temoin-3f.bin, vide.bin
                        les témoins du kit — les MÊMES octets que le kit
                        du bras T (la génération FIXE du labo, graine
                        20261107, recoupés à la gravure du kit T) ;
  EMPREINTES-KIT-UNITE-01-C.txt la gravure (chaque pièce, sha256,
                        générée du montage même) ;
  le présent LISEZMOI.

LES ÉCARTS NOMMÉS DU BRAS C (consignés, jamais maquillés) :
  — SetFilePointerEx : la pièce ne l'importe pas (sa lecture est
    séquentielle depuis l'ouverture — le bras T la résolvait à son plan
    fixe) : l'ÉCART NOMMÉ, le scénario résout les feuilles que la pièce
    déclare, les cinq suffisent ;
  — les imports du CRT de lancement mingw (InitializeCriticalSection…)
    vivent à la table sans jamais être appelées : sous DONT_RESOLVE
    aucun point d'entrée ne court — l'audit de la clôture des fonctions
    le prouve (aucun appel CRT, seize contrôles VERT) ;
  — l'accès refusé (E3) ne s'arme pas proprement au terrain : NOMMÉ
    ABSENT, le vecteur ne compte pas ;
  — le chemin de 260 caractères sans NUL : au terrain, le SYSTÈME
    refuse lui-même le chemin trop long — le verdict exact (-2/-5/-6)
    est CONSIGNÉ TEL QUEL au témoin.

LA FRONTIÈRE : le run est À VOUS (CA6 — le labo ne court JAMAIS le
terrain) ; le témoin se signe de VOTRE MAIN (D99) ; le renvoi du dossier
ENTIER vous appartient ; la pièce ne bouge pas (l'empreinte gravée —
une divergence, rien ne court).

*La consignation vit au journal de travail (l'Entrée 284) ; les journaux
de la campagne vivent à scripts/preuves_v150/comparaison_resultats/ (les
tokens M2, les temps M4) ; le détail du plan à
PLAN_PREREGISTRE_COMPARAISON.md (a78caf8c…, VERROUILLÉ).*
"""
(KIT / "LISEZMOI-KIT-UNITE-01-C.txt").write_text(lisezmoi, encoding="utf-8",
                                                 newline="\n")

# --- 6. la gravure (générée du montage même) -----------------------------------
pieces = ["loupe-01-c.dll", "loupe-01-c.c", "loupe-01-c.def",
          "scenario-unite01C.py", "LANCEUR-UNITE-01-C.bat",
          "temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin",
          "LISEZMOI-KIT-UNITE-01-C.txt"]
lignes = ["EMPREINTES — LE KIT DE L'UNITÉ 1 × BRAS C (loupe-01, la "
          "campagne D204)",
          "(chaque pièce sha256, générée du montage même — le GUI recoupe "
          "à l'onglet 1·KIT ; une divergence, rien ne court)", ""]
for nom in pieces:
    lignes.append(f"{sha256(KIT / nom)}  {nom}")
(KIT / "EMPREINTES-KIT-UNITE-01-C.txt").write_text(
    "\n".join(lignes) + "\n", encoding="utf-8", newline="\n")

# --- 7. le zip -------------------------------------------------------------------
zip_path = KIT / "kit-unite-loupe-01-C-20261114.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for nom in pieces + ["EMPREINTES-KIT-UNITE-01-C.txt"]:
        z.write(KIT / nom, f"kit-unite-loupe-01-C-20261114/{nom}")

print("\n[le kit assemblé]")
for f in sorted(KIT.iterdir()):
    print(f"  {f.stat().st_size:>8} o  {f.name}  {sha256(f)[:16]}…")
print(f"\n[gravure] {len(pieces)} pièces ; le zip "
      f"{zip_path.stat().st_size:,} o")
