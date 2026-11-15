#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_kits_unite13.py — LES DEUX KITS DE L'UNITÉ 5 (loupe-13 recherche,
la campagne D204), la gravure des 9 pièces chacun : la pièce, la notation +
le brouillon [T] ou le source + le .def [C], le scénario, le lanceur, le
scellé proxy.exe LE DORÉ, temoin-3f.bin LA GÉNÉRATION FIXE (== la gravure
des kits 01/02/05/08), EMPREINTES, LISEZMOI ; le zip plat + l'extraction
vierge recoupée."""
import hashlib
import pathlib
import py_compile
import shutil
import zipfile

ICI = pathlib.Path(__file__).resolve().parent
U_T = ICI / "unite-13-T"
U_C = ICI / "unite-13-C"
REPO = ICI.parent.parent
BAC302 = pathlib.Path("/home/z/my-project/scripts/bac-302/livraison")
PROXY = REPO / "tls13" / "proxy.exe"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- LE LANCEUR (la signature commune : le double BOM, CRLF) -----------------
def lanceur(bras: str, scenario: str, receptacle: str, temoin: str) -> bytes:
    texte = (
        "﻿\uFEFF@echo off\r\n"  # le double BOM — la signature commune
        "rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 5\r\n"
        f"rem (loupe-13 recherche x bras {bras}, la campagne D204). Le run "
        "court dans SA\r\n"
        "rem PROPRE console, INTACT : le GUI ne l'intercepte jamais (CA6).\r\n"
        "rem Le temoin ne se signe JAMAIS ici : votre main, toujours (D99).\r\n"
        "rem La capture console vit en UTF-8 des deux cotes du tuyau "
        "(l'edition\r\n"
        "rem v2 du kit 01, la meme discipline).\r\n"
        f"title TRIADE - Unite 5 (loupe-13 recherche x bras {bras}) - "
        f"campagne D204\r\n"
        'cd /d "%~dp0"\r\n'
        "where python >nul 2>nul\r\n"
        "if errorlevel 1 (\r\n"
        "  echo [REFUS] python introuvable au PATH - le kit exige "
        "Python 3.\r\n"
        "  pause\r\n"
        "  exit /b 2\r\n"
        ")\r\n"
        "set PYTHONIOENCODING=utf-8\r\n"
        "powershell -NoProfile -Command \"[Console]::OutputEncoding="
        f"[Text.Encoding]::UTF8; python {scenario} 2>&1 | Tee-Object "
        f"-FilePath run-console-unite13{bras}.txt\"\r\n"
        "set CODE=%ERRORLEVEL%\r\n"
        "echo.\r\n"
        "echo === LE RUN A FINI (code %CODE%) ===\r\n"
        f"echo Le temoin vit a {receptacle}\\{temoin} :\r\n"
        "echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au "
        "coffre /test.\r\n"
        "pause\r\n"
        "exit /b %CODE%\r\n")
    return texte.encode("utf-8")


# ---- LE LISEZMOI T -----------------------------------------------------------
LISEZMOI_T = """LISEZMOI — LE KIT DE L'UNITÉ 5 : LOUPE-13 RECHERCHE × BRAS T
(la campagne de comparaison des workflows D204 ; le kit livré par le labo
au coffre /test en son dossier daté — le GUI vous attend à l'onglet 1·KIT
de l'unité loupe-13 × T)
========================================================================

L'OBJET : la CINQUIÈME unité de la partie contrôlée — le bloc loupe-13
RECHERCHE au BRAS T (la notation scellée). La pièce de ce kit est le
build du plan où le slot loupe-13 (RVA 0x5740, 192 o) porte LA NOTATION
DE CAMPAGNE : écrite à la main par l'agent depuis le contrat loupe-13:R1
(la première occurrence d'un motif de 1 à 32 o dans une fenêtre, à
partir d'un départ donné — la position ABSOLUE de la PREMIÈRE, jamais la
seconde ; l'absence → -1 LA FIN NOMMÉE de la table ; le motif plus long
que la plage restante → -1 IMMÉDIAT, le constat trivial, jamais une
boucle ; le départ = la taille [la plage vide] → -1, le miroir ; les
trois refus → -5 ENTRÉE : le motif vide [chercher rien n'est pas
chercher], le motif > 32 [la borne du quotidien MOTIF_MAX], le départ
au-delà de la fenêtre [le départ est une position, pas un vœu] ; LA
COMPARAISON PAR LA CARTE : chaque candidat testé par libc-02 memcmp LE
BLOC SCELLÉ M1 à 0x1180, jamais une boucle réécrite — la liste
d'appels FERMÉE ; la fenêtre et le motif LUS SEULS ; AUCUNE entrée IAT —
la feuille pure). LES DIX-SEPT autres blocs demeurent les SCELLÉS du
projet.

LA CONSTRUCTION (consignée, les défauts nommés AVANT toute livraison) :
l'oracle écrit-avant-code (le modèle indépendant AVANT les octets ; le
juge ne relit jamais l'accusé) ; la notation à la main 116 o, 46
instructions, 5 étiquettes (mes choix : LE DÉPART LU AU-DEVANT, LES
BORNES AVANT LE CADRE — P5 lu à [rsp+0x28] avant tout push, les trois
refus SANS AUCUN GESTE, deux sorties, la droite et la refusée ; LA
BORNE EN ADRESSE — le dernier candidat posé une fois en adresse
[fenêtre + taille − motif], la boucle compare POINTEUR À POINTEUR,
l'arithmétique ne revit jamais à l'intérieur ; LE CURSEUR EST LE
POINTEUR — le candidat avance par inc, la position rendue par une seule
soustraction à la sortie ; LE CADRE HONNÊTE — cinq pushes + l'ombre
0x20, le scellé a droit à son ombre d'appel, l'alignement tenu ; LES
MOINS VRAIS PAR LA PILE — push −1/pop rax, l'imm8 dépassé du signe à 64
bits, « mov eax, −1 » mentirait le haut) ; le build aux verrous 121
(round-trip R5, les mesures D161 des dix-sept scellées, le réseau des
specs, l'audit msx64 — chaque argument 5+ écrit à son slot), le
différentiel au scellé CONFINÉ au slot loupe-13 et à la porte R10 (5
plages, 125 o) ; la cristallisation : DIX rebuilds consécutifs
IDENTIQUES (loupe.exe 127 488 o, sha256 78f5d5cddf90320a…) ; l'oracle
du bloc : 10 VERT, 0 ROUGE (le doré : LE CORPUS DE L'ÉCOLE — le motif
au premier octet, au dernier, à cheval sur le départ, l'occurrence
DOUBLE LA PREMIÈRE exigée, AAAA dans AAAAB, le presque-frère, le
départ au milieu, la fenêtre vide, la plage vide, le motif trop long —
+ LES MARQUES DE PROXY.EXE SCELLÉ : MZ @0, PE @+0x40, « This program »
et « PEMax » les marques ABSENTES [les en-têtes écrits à la main] →
-1 LA FIN NOMMÉE ; le différentiel 10 000 cas == le modèle [alphabets
plein ET pauvre, 1 584 occurrences VRAIES], la fenêtre et le motif LUS
SEULS, l'état propre aux 10 000 gestes ; les TROIS rejets -5 ; LA
FALSIFICATION DEMANDÉE : la position avancée d'un [lea rax, rbx+1
contre mov rax, rbx — le mutant re-résolu par l'auteur, une vraie
notation, jamais un texte balafré] — les 44 cas à occurrence TOUS
divergents, la notation juste rejouée verte au retrait de la mutation)
; l'épreuve du scénario livré : son modèle extrait par AST, confronté
au contre-modèle (2 000 cas + les frontières), LES CONSTANTES AUDITÉES
(R_LOUPE13 == LOUPE13_VA du plan, le slot i110013 0xC0), le
générateur déterministe (deux passages identiques, les MÊMES tirages au
labo et au terrain) ; L'ÉPREUVE DU KIT, PLOMBERIE COMPRISE (la leçon de
la 302) : les blocs V1/V3/V4 du scénario livré extraits VERBATIM et
exécutés au labo contre la pièce réelle du bras C — l'école, les
marques, les rejets, la falsification et le fixture AU RÉCEPTACLE ;
le bloc découverte du C exécuté contre la dll réelle == le juge
indépendant.

LE GESTE (tout au clic, l'ordre de jeu d'une unité) :
  1. AU GUI (TRIADE_gui_tous_runs_v1 ou TRIADE_gui_campagne_v1), onglet
     1·KIT de l'unité loupe-13 × T : CHOISIR CE DOSSIER
     (kit-unite-loupe-13-T-20261115) — le GUI recoupe les EMPREINTES
     gravées (une divergence, rien ne court) ;
  2. onglet 2·RUN : LANCER LANCEUR-UNITE-13-T.bat (le lanceur officiel —
     il court dans SA PROPRE console, INTACT) : le scénario recoupe la
     pièce à la gravure, charge l'image (LoadLibraryEx DONT_RESOLVE —
     LA FEUILLE PURE N'APPELLE PERSONNE : aucune feuille kernel32 à
     résoudre), appelle loupe-13 à son adresse au plan (le 5e argument
     posé par ctypes AU SLOT msx64 [rsp+0x28]), juge par le modèle
     indépendant (bytes.find de Python), et écrit le témoin ; le
     dossier preuves-unite13/ naît sur votre machine ;
  3. onglet 3·TÉMOIN : ouvrir preuves-unite13\\temoin-unite13.txt au
     bloc-notes, le DATER, le SIGNER DE VOTRE MAIN — jamais automatisé
     (D99) ;
  4. renvoyer preuves-unite13/ ENTIER (le témoin signé +
     falsifie-16.bin le fixture de la falsification) AU COFFRE /test ;
  5. les onglets compagnons aux gestes vécus : 4·CARNET M3, 5·LIVRAISON
     (la ligne T-loupe-13-it1 : kit 2026-11-15, run 2026-11-15, le
     verdict de la console), 6·DÉFAUTS s'il y en a, 7·CHRONO M4.

LES VECTEURS DU RUN (le contrat loupe-13 révision 1) :
  V1 le doré : LE CORPUS DE L'ÉCOLE + LES MARQUES DE PROXY.EXE SCELLÉ
     sur sa première fenêtre de 8 192 o (MZ @0, PE @+0x40, « This
     program » et « PEMax » les marques ABSENTES → -1 LA FIN NOMMÉE) ;
  V2 le différentiel : 10 000 cas aléatoires (fenêtres 0..4 096 o,
     motifs 1..32, départs aléatoires, alphabet plein ET pauvre — la
     graine fixe 20261115, les mêmes tirages au labo) : rax ==
     bytes.find À L'IDENTIQUE, y compris les -1 (Q1-Q4) ; la fenêtre
     et le motif LUS SEULS (I3) ;
  V3 les rejets : le motif vide, le motif de 33 o, le départ au-delà
     → les TROIS verdicts -5 (E1/E2/E3) ;
  V4 la falsification demandée : LE DORÉ COPIÉ AU RÉCEPTACLE avec
     l'octet 1 muté (0x5A → 0x6F — le « MZ » détruit) : la même gamme
     rend -1 LA FIN NOMMÉE QUI DIVERGE du modèle de l'original (0) ET
     == le modèle du mutant : la pièce a lu SES octets, la
     différentielle attrape le faux (le fixture falsifie-16.bin vit
     au réceptacle preuves-unite13/, renvoyé ENTIER avec le témoin).

LE LANCEUR NOMMÉ : le double BOM (ef bb bf ×2) en tête — LA SIGNATURE
COMMUNE de tous les lanceurs de la campagne (01 v2, 02, 05, 08 T/C,
13 T/C) : la première ligne erre, l'echo demeure allumé, MAIS le run,
la capture Tee et l'encodage du tuyau sont INTACTS (nommé à la 302,
aucun fix mi-campagne).

AUCUN SECRET ICI : le kit ne porte que des preuves publiques — la
pièce, le scellé, les empreintes, les textes. (verrouillé à D204)
"""

# ---- LE LISEZMOI C -----------------------------------------------------------
LISEZMOI_C = """LISEZMOI — LE KIT DE L'UNITÉ 5 : LOUPE-13 RECHERCHE × BRAS C
(la campagne de comparaison des workflows D204 ; le kit livré par le labo
au coffre /test en son dossier daté — le GUI vous attend à l'onglet 1·KIT
de l'unité loupe-13 × C)
========================================================================

L'OBJET : la CINQUIÈME unité de la partie contrôlée — le bloc loupe-13
RECHERCHE au BRAS C (le flux standard gcc -O2). La pièce de ce kit est
le source écrit par l'agent compilé par la chaîne croisée : loupe_13_
recherche (les bornes d'abord : le motif vide, le motif > 32 MOTIF_MAX,
le départ au-delà → -5 AVANT toute lecture ; le constat trivial AVANT
la boucle — le motif plus long que la plage restante → -1 IMMÉDIAT,
jamais une boucle ; la recherche directe honnête O(n·m), m ≤ 32 — chaque
candidat testé par LE memcmp DE LA BIBLIOTHÈQUE [I2 : la liste
d'appels FERMÉE, jamais une boucle de comparaison réécrite], la
dernière candidate posée une fois, la fenêtre et le motif LUS SEULS ;
la position ABSOLUE de la PREMIÈRE [Q1/Q4], l'absence → -1 LA FIN
NOMMÉE [Q2/Q3]), compilée gcc -O2 croisée (la commande consignée :
x86_64-w64-mingw32-gcc-posix -O2 -shared — la chaîne TRIXIE extraite
des .deb sans root) : loupe-13-c.dll — L'EXPORT UNIQUE loupe_13_
recherche, AUCUN autre appel dans sa clôture (le seul : le thunk
memcmp de la bibliothèque), les imports KERNEL32/msvcrt servent le
démarreur CRT du lieur seul.

LA CONSTRUCTION (consignée, les défauts nommés AVANT toute livraison)
: LE CONTRAT REJOUÉ AU POSIX contre la pièce même : la dll mappée par
sections à la base préférée (le geste de LoadLibraryEx rejoué), LE
TRAMPOLINE SysV→msx64 À CINQ ARGUMENTS (les quatre registres
réarrangés + le départ posé AU SLOT [rsp+0x28] — le choc des ABI nommé
et adapté, jamais la pièce réécrite), LE SHIM MEMCMP (la feuille
unique de la liste fermée : le slot IAT repointé au memcmp de la libc
du labo — RDI ET RSI NON-VOLATILS EN msx64, sauvés et rendus par le
shim, l'alignement compté) — 11 VERT, 0 ROUGE : l'école 10/10 + les
marques du scellé (MZ @0, PE @+0x40, les absentes → LA FIN NOMMÉE) ;
le différentiel 10 000/10 000 (les MÊMES tirages que le juge T —
l'appariement du plan) ; les TROIS rejets -5 ; LA FALSIFICATION
DOUBLE : la fenêtre mutée (la première occurrence détruite → la
seconde : la pièce a lu SES octets) ET LE PAS DE LA PIÈCE MUTÉ
(add rbx, 1 → 2 : les 100 cas de l'école impairs TOUS divergents —
le juge attrape la pièce fausse, le pas restauré rend le vert) ; les
contrôles binaires : PE32+ DLL x86-64, l'export UNIQUE, la liste
d'appels FERMÉE. L'épreuve du scénario livré : son modèle extrait par
AST == le contre-modèle (2 000 cas + les frontières), les constantes
auditées (AUCUNE RVA codée — la découverte par la table d'exports, la
convention (base, rva) unifiée de la 302), le générateur déterministe
; L'ÉPREUVE DU KIT, PLOMBERIE COMPRISE : le bloc découverte du
scénario livré extrait VERBATIM et exécuté au labo contre la dll
réelle == le juge indépendant.

LE GESTE (tout au clic, l'ordre de jeu d'une unité) :
  1. AU GUI (TRIADE_gui_tous_runs_v1 ou TRIADE_gui_campagne_v1), onglet
     1·KIT de l'unité loupe-13 × C : CHOISIR CE DOSSIER
     (kit-unite-loupe-13-C-20261115) — le GUI recoupe les EMPREINTES
     gravées (une divergence, rien ne court) ;
  2. onglet 2·RUN : LANCER LANCEUR-UNITE-13-C.bat (le lanceur officiel —
     il court dans SA PROPRE console, INTACT) : le scénario recoupe la
     pièce à la gravure, charge l'image (LoadLibraryEx DONT_RESOLVE),
     DÉCOUVRE L'EXPORT UNIQUE PAR LA TABLE D'EXPORTS (la convention
     (base, rva) unifiée), appelle loupe_13_recherche à SA RVA
     DÉCOUVERTE (le 5e argument posé par ctypes AU SLOT msx64
     [rsp+0x28]), juge par le modèle indépendant (bytes.find de
     Python), et écrit le témoin ; le dossier preuves-unite13C/ naît
     sur votre machine ;
  3. onglet 3·TÉMOIN : ouvrir preuves-unite13C\\temoin-unite13C.txt au
     bloc-notes, le DATER, le SIGNER DE VOTRE MAIN — jamais automatisé
     (D99) ;
  4. renvoyer preuves-unite13C/ ENTIER (le témoin signé +
     falsifie-16.bin le fixture de la falsification) AU COFFRE /test ;
  5. les onglets compagnons aux gestes vécus : 4·CARNET M3, 5·LIVRAISON
     (la ligne C-loupe-13-it1 : kit 2026-11-15, run 2026-11-15, le
     verdict de la console), 6·DÉFAUTS s'il y en a, 7·CHRONO M4.

LES VECTEURS DU RUN (les mêmes que le bras T — l'appariement du plan)
: V1 l'école + les marques du scellé ; V2 le différentiel 10 000 (la
graine 20261115, les mêmes tirages que le juge T) ; V3 les trois
rejets -5 ; V4 la falsification (le « MZ » du doré détruit → LA FIN
NOMMÉE, le fixture falsifie-16.bin au réceptacle).

LE LANCEUR NOMMÉ : le double BOM (ef bb bf ×2) en tête — LA SIGNATURE
COMMUNE de tous les lanceurs de la campagne : la première ligne erre,
MAIS le run, la capture Tee et l'encodage du tuyau sont INTACTS (nommé
à la 302, aucun fix mi-campagne).

AUCUN SECRET ICI : le kit ne porte que des preuves publiques. (verrouillé
à D204)
"""


def assembler(unite: pathlib.Path, nom_kit: str, pieces: dict,
              emp_nom: str, lisezmoi: str, suffixe: str) -> None:
    kit = unite / "kit"
    if kit.exists():
        shutil.rmtree(kit)
    kit.mkdir()
    # les pièces copiées et recoupées
    for nom, source in pieces.items():
        shutil.copy2(source, kit / nom)
    # le lanceur (la signature commune : le double BOM)
    scenario_nom = [n for n in pieces if n.startswith("scenario-unite13")][0]
    (kit / f"LANCEUR-UNITE-13-{suffixe}.bat").write_bytes(
        lanceur(suffixe, scenario_nom,
                f"preuves-unite13{'' if suffixe == 'T' else 'C'}",
                f"temoin-unite13{'' if suffixe == 'T' else 'C'}.txt"))
    # le LISEZMOI (UTF-8, LF — le format du kit 08)
    (kit / f"LISEZMOI-KIT-UNITE-13-{suffixe}.txt").write_text(
        lisezmoi, encoding="utf-8", newline="\n")
    # py_compile du scénario livré
    py_compile.compile(str(kit / scenario_nom), doraise=True)
    # l'EMPREINTES (BOM + CRLF — le format du kit 08)
    gravure = [p for p in sorted(kit.iterdir())
               if p.is_file() and p.name != emp_nom]
    lignes = [
        "﻿EMPREINTES — LE KIT DE L'UNITÉ 5 (loupe-13 RECHERCHE × bras "
        f"{suffixe}, la campagne D204)",
        "(chaque pièce sha256 — le GUI recoupe à l'onglet 1·KIT ; une "
        "divergence, rien ne court)",
        "",
    ]
    for p in gravure:
        lignes.append(f"{sha(p)}  {p.name}")
    (kit / emp_nom).write_text("\r\n".join(lignes) + "\r\n",
                               encoding="utf-8", newline="")
    # le recoup : chaque pièce == sa ligne de gravure
    emp = {}
    for l in (kit / emp_nom).read_text(encoding="utf-8-sig").splitlines():
        parts = l.strip().split(None, 1)
        if len(parts) == 2 and len(parts[0]) == 64:
            emp[parts[1].strip()] = parts[0]
    attendus = {p.name for p in kit.iterdir()
                if p.is_file() and p.name != emp_nom}
    assert set(emp) == attendus, f"{sorted(emp)} != {sorted(attendus)}"
    for p in sorted(kit.iterdir()):
        if p.is_file() and p.name in emp:
            assert sha(p) == emp[p.name], f"{p.name} != sa gravure"
    # le zip plat + l'extraction vierge
    cible = unite / f"{nom_kit}.zip"
    with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(kit.iterdir()):
            if p.is_file():
                zf.write(p, p.name)
    with zipfile.ZipFile(cible) as zf:
        for p in sorted(kit.iterdir()):
            if p.is_file():
                assert hashlib.sha256(zf.read(p.name)).hexdigest() == sha(p), \
                    f"l'extraction de {p.name} diverge"
    nb = sum(1 for p in kit.iterdir() if p.is_file())
    assert nb == 9, f"{nom_kit} : {nb} pièces != 9"
    print(f"[kit] {nom_kit} : {nb} pièces gravées, le zip "
          f"({cible.stat().st_size} o) l'extraction vierge recoupée")


TEM = BAC302 / "kit-unite-loupe-08-T-20261115-v2" / "temoin-3f.bin"
assert sha(TEM) == "c5fc1f28e471059d56a892ba82df1e215f5263aafd8c43fdb0e76e110d1d5ca3", \
    "temoin-3f.bin != la génération FIXE des kits 01/02/05/08"

assembler(
    U_T, "kit-unite-loupe-13-T-20261115",
    {"loupe.exe": U_T / "piece" / "loupe.exe",
     "notation-loupe-13-recherche.asm": U_T / "notation" / "loupe-13-recherche.asm",
     "brouillon-loupe-13-recherche.asm": U_T / "brouillons" / "loupe-13-recherche.asm",
     "scenario-unite13.py": U_T / "scenario-unite13.py",
     "proxy.exe": PROXY,
     "temoin-3f.bin": TEM},
    "EMPREINTES-KIT-UNITE-13-T.txt", LISEZMOI_T, "T")

assembler(
    U_C, "kit-unite-loupe-13-C-20261115",
    {"loupe-13-c.dll": U_C / "source" / "loupe-13-c.dll",
     "loupe-13-c.c": U_C / "source" / "loupe-13-c.c",
     "loupe-13-c.def": U_C / "source" / "loupe-13-c.def",
     "scenario-unite13C.py": U_C / "scenario-unite13C.py",
     "proxy.exe": PROXY,
     "temoin-3f.bin": TEM},
    "EMPREINTES-KIT-UNITE-13-C.txt", LISEZMOI_C, "C")

print("=== LES DEUX KITS 13 ASSEMBLÉS, GRAVÉS, ZIPPÉS — l'épreuve du kit "
      "(plomberie comprise) contre les pièces livrées mêmes, puis le coffre ===")
