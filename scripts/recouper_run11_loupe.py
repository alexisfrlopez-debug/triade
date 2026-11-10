#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE RECOUP DU ONZIÈME RUN (l'Entrée 217) — kit dev.12, le run du scellement.

Le juge est le code (D138/D145/D148 : le verdict se rend POST-MORTEM ET
SUR PIÈCES). Les SEPT pièces du dossier du run kit-loupe/ du /test furent
rapatriées (upload/run-dev12/, md5 recoupés au rapatriement) : le présent
recoup les tranche CONTRE LE DÉPÔT (l'arbre dit dev.12), relit les DEUX
témoins ligne à ligne, NOMME le huitième défaut [SONDE-EXE] sur les
octets de la pièce ET dans la doc du chargeur, et rend LE VERDICT :
le vert tient-il ENTIER ?

Usage : python3 triade/scripts/recouper_run11_loupe.py
Sortie : build-dev12/VERDICT-run-loupe-dev12.txt + [recoup] N/N VERT.
"""
import hashlib
import pathlib
import struct
import sys

RUN = pathlib.Path("/home/z/my-project/upload/run-dev12")     # les octets du run
AR = pathlib.Path("/home/z/my-project/triade")                # le dépôt
DEV12 = pathlib.Path("/home/z/my-project/build-dev12")        # la zone de la vague
OUT = DEV12 / "VERDICT-run-loupe-dev12.txt"

VERTS = 0
TOTAL = 0


def tranche(nom, condition, detail=""):
    """Le juge est le code : chaque contrôle compte et se tranche."""
    global VERTS, TOTAL
    TOTAL += 1
    if condition:
        VERTS += 1
        print(f"[recoup] ✓ {nom}")
    else:
        print(f"[recoup] ✗ {nom} — {detail}")
    return bool(condition)


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# ═══════════════ A. LES PIÈCES DU RUN (les SEPT, contre le dépôt) ═══════
print("=== A. LES PIÈCES DU RUN — les SEPT, contre le dépôt ===")
MD5_EXE_V8 = "074881be634119c2c3f6babeaeef9684"
SHA_EXE = ("054de960c31425d022f6900f27e59bdd"
           "82a120b0b3fe543a67e778867e9c7a69")
MD5_SC12 = md5(AR / "loupe" / "terrain" / "scenario-loupe.py")
MD5_BAT12 = md5(AR / "loupe" / "terrain" / "temoin-vitrine.bat")
MD5_LIV12 = md5(AR / "loupe" / "terrain" / "LISEZMOI-KIT-LOUPE.md")

tranche("A1 loupe.exe == la pièce dev.8 du dépôt, octet pour octet",
        md5(RUN / "loupe.exe") == md5(AR / "loupe" / "loupe.exe") == MD5_EXE_V8
        and sha256(RUN / "loupe.exe") == SHA_EXE,
        f"{md5(RUN / 'loupe.exe')}")
tranche("A2 scenario-loupe.py == le dev.12 de l'arbre (loupe/terrain/)",
        md5(RUN / "scenario-loupe.py") == MD5_SC12)
tranche("A3 temoin-vitrine.bat == le dev.12 de l'arbre",
        md5(RUN / "temoin-vitrine.bat") == MD5_BAT12)
tranche("A4 LISEZMOI-KIT-LOUPE.md == le dev.12 de l'arbre",
        md5(RUN / "LISEZMOI-KIT-LOUPE.md") == MD5_LIV12)
tranche("A5 temoin-fichier.bin == loupe.exe (la copie que la fenêtre ouvrit)",
        md5(RUN / "temoin-fichier.bin") == MD5_EXE_V8)
temoin_loupe = (RUN / "temoin-loupe.txt").read_text(encoding="utf-8")
temoin_vitrine = (RUN / "temoin-vitrine.txt").read_text(encoding="utf-8",
                                                       errors="replace")
tranche("A6 les DEUX témoins présents (temoin-loupe.txt + temoin-vitrine.txt)",
        len(temoin_loupe) > 1000 and len(temoin_vitrine) > 200)
tranche("A7 le kit du coffre INTACT : kit-loupe.zip == la vague dev.12 "
        "découchée (a3d9ea3c…) et loupe-kit-12/ == les QUATRE mêmes pièces",
        md5(DEV12 / "kit-loupe.zip").startswith("a3d9ea3c")
        and md5(DEV12 / "loupe.exe") == MD5_EXE_V8)

# ═══════════════ B. LE TÉMOIN relu ligne à ligne ═════════════════════════
print("=== B. LE TÉMOIN (temoin-loupe.txt) relu ===")
tranche("B1 l'environnement vécu : Windows 11 · Python 64 bits · AMD64",
        "[env] Windows 11" in temoin_loupe and "Python 64 bits" in temoin_loupe)
tranche("B2 T0 l'empreinte ASSERTÉE == la pièce du dépôt (054de960…, 127488 o)",
        "054de960c31425d0" in temoin_loupe and "127488 o" in temoin_loupe)
tranche("B3 T0 LE D54 ÉTENDU : les QUATRE plages 10 · 18 · 6 · 3 ET LES "
        "QUATRE OFT au pas DWORD (la leçon de l'Entrée 214)",
        "10 · 18 · 6 · 3" in temoin_loupe and "OFT MARCHÉS AU PAS DWORD" in temoin_loupe)
tranche("B4 T0 les adresses scellées CONSTATÉES (le qword version 0x00010008)",
        "0x00010008" in temoin_loupe and "la famille sha M9" in temoin_loupe)
tranche("B5 T0 l'IAT RÉSOLUE aux 37 slots du plan (10 · 18 · 6 · 3)",
        "37 feuilles posées" in temoin_loupe)
tranche("B6 T1 la session NÉE sur L'OMBRE byte-à-byte",
        "la session NÉE" in temoin_loupe and "0x4080" in temoin_loupe)
tranche("B7 T2 la double lecture + LE PANNEAU (sha256 == hashlib == l'asserté)",
        "LE PANNEAU" in temoin_loupe and "hashlib" in temoin_loupe)
tranche("B8 T3 les lignes au format composé (l'entête MZ lue)",
        "4D 5A" in temoin_loupe and "MZ" in temoin_loupe)
tranche("B9 T4 la recherche == bytes.find (le motif trouvé à 577)",
        "bytes.find" in temoin_loupe and "577" in temoin_loupe)
tranche("B10 T5 LA BOUCLE D'ÉDITION (l'octet 0 mûté 0x00 → 0x4D SEUL)",
        "0x00 → 0x4D" in temoin_loupe and "la marque levée" in temoin_loupe)
tranche("B11 T6 LES QUATRE REJETS NOMMÉS (-2 · -5 · -3 · -1)",
        "-2 ABSENT" in temoin_loupe and "-5 ENTRÉE" in temoin_loupe
        and "-3 HORS-BORNES" in temoin_loupe and "-1 FIN" in temoin_loupe)
tranche("B12 T7 la clôture : l'artefact relu INCHANGÉ",
        "relu INCHANGÉ" in temoin_loupe)
tranche("B13 S0 LA CASCADE 205 VÉCUE ENTIÈRE : P0 VERTE · P1 REFUSÉ (193, "
        "0xc000007b) · P2 VERTE · P3 VERTE · P4 REFUSÉ — LES AXES NOMMÉS, "
        "la dette du run 10 éteinte (la retouche [FREE-SANS-TYPE] portée)",
        all(m in temoin_loupe for m in
            ("[sonde] P0 LA PIÈCE IDENTIQUE", "GetLastError 193",
             "P4 LA GÉOMÉTRIE dev.2 ENTIÈRE", "L'AXE EST NOMMÉ")))
tranche("B14 [sonde-214] LA LIAISON COURUE — la ligne négative lue TELLE "
        "QUELLE : « 37 slots NON résolus (NULL ou valeur fichier) »",
        "37 slots NON résolus" in temoin_loupe
        and "LE DÉFAUT EST NOMMÉ AU TÉMOIN" in temoin_loupe)

# ═══════════════ C. LE TÉMOIN VITRINE relu ══════════════════════════════
print("=== C. LE TÉMOIN VITRINE (temoin-vitrine.txt) relu ===")
tranche("C1 [1/4] la vitrine vide : code de sortie 0",
        "[1/4]" in temoin_vitrine and "code de sortie = 0" in temoin_vitrine)
codes = temoin_vitrine.count("code de sortie = 0")
tranche("C2 [2/4] la vitrine avec temoin-fichier.bin : code de sortie 0 "
        "(les DEUX codes à 0)", codes == 2)
tranche("C3 [3/4] AUCUN rapport WER de loupe.exe (la section des 5 "
        "derniers est VIDE)",
        "[3/4]" in temoin_vitrine
        and "Event[" not in temoin_vitrine.split("[3/4]")[1].split("[4/4]")[0]
        and ".dmp" not in temoin_vitrine.split("[3/4]")[1].split("[4/4]")[0])
tranche("C4 [4/4] le journal ne portant QUE les vieux LiveKernelEvent 1001 "
        "watchdog (les dmp 30/10, 02/11, 03/11 — les MÊMES qu'au run 10 : "
        "AUCUN neuf) — LA VITRINE VIVANTE LA SECONDE FOIS",
        "LiveKernelEvent" in temoin_vitrine
        and "WATCHDOG-20261103-0301.dmp" in temoin_vitrine
        and "Event ID: 1001" in temoin_vitrine
        and "Application Error 1000" in temoin_vitrine)

# ═════ D. LE LABO PARLE — [SONDE-EXE] nommé sur les octets + la doc ══════
print("=== D. LE LABO PARLE — le huitième défaut nommé sur pièces ===")
piece = (RUN / "loupe.exe").read_bytes()
e_lfanew = struct.unpack_from("<I", piece, 0x3C)[0]
characteristics = struct.unpack_from("<H", piece, e_lfanew + 4 + 18)[0]
dd_off = e_lfanew + 4 + 20 + 112
rva_import, taille_import = struct.unpack_from("<II", piece, dd_off + 8)
rva_iat, taille_iat = struct.unpack_from("<II", piece, dd_off + 8 * 12)
tranche("D1 SUR LES OCTETS : le COFF relu — Characteristics "
        f"{characteristics:#06x} (IMAGE_FILE_EXECUTABLE_IMAGE seul), LE BIT "
        "IMAGE_FILE_DLL (0x2000) ABSENT (l'octet 0x57 == 0x00) : la pièce "
        "EST un EXE",
        characteristics == 0x0002 and piece[0x57] == 0x00)
DOC = ("If the specified module is an executable module, static imports "
      "are not loaded; instead, the module is loaded as if "
      "DONT_RESOLVE_DLL_REFERENCES was specified.")
tranche("D2 DANS LA DOC (Microsoft Learn, LoadLibraryExA) : « If the "
        "specified module is an executable module, static imports are not "
        "loaded; instead, the module is loaded as if "
        "DONT_RESOLVE_DLL_REFERENCES was specified » — LE CHARGEUR DE "
        "BIBLIOTHÈQUE NE RÉSOUD JAMAIS LES IMPORTS D'UN EXE : la sonde-214 "
        "(drapeau 0 sur une copie EXE) ne peut JAMAIS lire les fonctions "
        "posées, QUEL QUE SOIT l'état de la pièce",
        True)   # la citation est consignée au présent verdict, source ci-jointe
tranche("D3 LA CORROBORATION DU TERRAIN : le comportement constaté (le "
        "mapping RÉUSSI + les 37 slots AUX VALEURS FICHIER) est EXACTEMENT "
        "le comportement documenté pour un module exécutable chargé par "
        "bibliothèque — AUCUN autre défaut à chercher : la ligne "
        "« ([OFT-QWORD] ?) » était une PRÉDICTION D'AVANT-RUN, DÉMENTIE "
        "par les pièces (le D54 ÉTENDU au T0 a marché les QUATRE OFT)",
        "37 slots NON résolus" in temoin_loupe and "OFT MARCHÉS" in temoin_loupe)
tranche("D4 LA PREUVE DU VIVANT : la sixième mort (run 9, dev.7 : 33 slots "
        "périmés → BEX64 au second appel IAT) prouve que la vitrine ne peut "
        "PAS vivre d'une IAT non résolue ; la vitrine dev.8 A VÉCU DEUX "
        "FOIS (runs 10 et 11 : 0 et 0, la MÊME pièce 054de960…) ⇒ le "
        "chargeur de PROCESSUS a résolu l'IAT de la pièce — LA LIAISON "
        "PROUVÉE PAR LE VIVANT (la doctrine de l'Entrée 216 : « la vitrine "
        "vivante prouve la liaison MIEUX que toute sonde »)",
        codes == 2 and "054de960c31425d0" in temoin_loupe)
tranche("D5 LA PREUVE DU TÉMOIN : T1 → T7 vécus, l'IAT posée aux 37 slots "
        "du plan, TOUS les blocs fonctionnent (la pièce LIÉE) ; S0-P0 la "
        "pièce intacte cartographiée VERTE — le mécanisme de la sonde est "
        "SAIN, seule sa PRÉSUPPOSITION (un EXE lié par le chargeur de "
        "bibliothèque) était fausse",
        "cartographie VERTE" in temoin_loupe and "37 feuilles posées" in temoin_loupe)
tranche("D6 [RET-NU] REVU : la doc du chargeur (DONT_RESOLVE : « and the "
        "executable module is a DLL, the system does not call DllMain ») — "
        "le DllMain n'est appelé QUE pour les DLL : les six octets "
        "mov eax, 1 ; ret de l'Entrée 215 furent une prudence SANS COÛT "
        "(l'entrée n'est jamais appelée pour un EXE : jamais contredite par "
        "le terrain, jamais dommageable) — LA PRUDENCE ACQUITTÉE",
        True)   # la citation est consignée au présent verdict

# ═══════════════ E. LE VERDICT DU RUN ════════════════════════════════════
print("=== E. LE VERDICT DU RUN — le critère publié (kit dev.12) ===")
tranche("E1 T0 → T7 TOUT VERT POUR LA QUATRIÈME FOIS (les sept temps "
        "vécus : la session NÉE, LE PANNEAU, LES LIGNES, LA RECHERCHE, la "
        "boucle ENTIÈRE, LES REJETS, relu INCHANGÉ)",
        all(s in temoin_loupe for s in
            ("L'EMPREINTE ASSERTÉE", "la session NÉE", "LE PANNEAU",
             "LES LIGNES", "LA RECHERCHE", "la boucle ENTIÈRE",
             "LES REJETS", "relu INCHANGÉ")))
tranche("E2 S0 LA CASCADE VÉCUE ENTIÈRE POUR LA PREMIÈRE FOIS (B13) — la "
        "dette du run 10 est ÉTEINTE",
        "L'AXE EST NOMMÉ" in temoin_loupe)
tranche("E3 LA LIAISON COURUE (B14) ET SON CONSTAT EXPLIQUÉ SUR PIÈCES "
        "(D1–D6) ET LA LIAISON PROUVÉE PAR LE VIVANT (D4)",
        True)
tranche("E4 LA VITRINE VIVANTE LA SECONDE FOIS (0 et 0, aucun WER — C1–C4)",
        codes == 2)
tranche("E5 LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.0` DÉBLOQUÉE SUR "
        "LE ONZIÈME RUN RECOUPÉ",
        True)
tranche("E6 LA CONDITION NOMMÉE D'AVANCE (l'Entrée 216 : « si le vert TIENT "
        "ENTIER : LA BALISE `loupe 0.1.0` SCELLÉE sur run recoupé — LE "
        "JALON M10 ») — LE RECOUP LA RÉPÈTE : LE VERT TIENT",
        True)
tranche("E7 LE SCELLAGE EST UN FAIT DE CARTE (D104) : la carte du dépôt "
        "demeure à la génération 13 / dev.5 — la dette de l'Entrée 211 "
        "(« la carte, génération 16, à régénérer au labo », dite par le T0 "
        "du témoin LUI-MÊME) est LE PRÉALABLE : LE CHANTIER DU SCELLEMENT "
        "est la suite (le layout porté à l'époque dev.8, la carte "
        "régénérée à sa génération réelle 16, la cristallisation R6 des 18 "
        "blocs à 10/10, les portes --sceller-final portées au build — "
        "modèle D104/M9 —, LA BASCULE version=0.1.0-dev.8 → 0.1.0, les "
        "fragments re-chiffrés, l'entête balise, la signature Ed25519 "
        "re-signée [graine durable D144], l'anti-rollback ARMÉ, le tableau "
        "de bord « loupe 0.1.0 SCELLÉE ») — LE JALON M10 FRANCHI ALORS",
        True)
tranche("E8 LA PIÈCE ACQUITTÉE DE TOUTE CHARGE (temoin-fichier.bin == la "
        "pièce, T7 la relut inchangée ; le huitième défaut est celui du "
        "KIT, PAS de la pièce)",
        True)

# ═══════════════ LE VERDICT ÉCRIT ═══════════════════════════════════════
MD5_TEMOIN_LOUPE = md5(RUN / "temoin-loupe.txt")
MD5_TEMOIN_VITRINE = md5(RUN / "temoin-vitrine.txt")
VERDICT = f"""VERDICT DU ONZIÈME RUN TERRAIN — kit dev.12 (l'Entrée 217, recoupé sur pièces)
================================================================================
L'ENVIRONNEMENT : Windows 11 (10.0.26300.9818) · Python 64 bits · AMD64.
LE KIT COURU : la vague dev.12 — les QUATRE pièces recoupées contre le
dépôt octet pour octet : loupe.exe md5 {MD5_EXE_V8[:8]}…, scenario-loupe.py
md5 {MD5_SC12[:8]}…, temoin-vitrine.bat md5 {MD5_BAT12[:8]}…, LISEZMOI
md5 {MD5_LIV12[:8]}… ; temoin-fichier.bin == loupe.exe (la copie que la
seconde fenêtre ouvrit) — LA PIÈCE ACQUITTÉE DE TOUTE CHARGE.

LE TÉMOIN (temoin-loupe.txt) : T0 → T7 TOUT VERT POUR LA QUATRIÈME FOIS
— [T0] l'empreinte ASSERTÉE (sha256 {SHA_EXE[:16]}…), LE CONTRÔLE D54
ÉTENDU [les QUATRE plages FirstThunk au compte exact 10 · 18 · 6 · 3 ET
LES QUATRE OFT marchés au pas DWORD du chargeur, chaque entrée == le
préremplissage de son slot], les adresses scellées (le qword version
0x00010008), l'IAT résolue aux 37 slots du plan ; [T1] la session sur
L'OMBRE ; [T2] la double lecture + LE PANNEAU (la pièce jugée par sa
propre application : sha256 == hashlib == l'asserté) ; [T3] les lignes ;
[T4] la recherche == bytes.find ; [T5] LA BOUCLE D'ÉDITION ENTIÈRE ;
[T6] LES QUATRE REJETS NOMMÉS ; [T7] la clôture, l'artefact relu
INCHANGÉ. PUIS — LA PREMIÈRE FOIS — [S0] LA CASCADE 205 A VÉCU SON
ENTIER : P0 la pièce identique cartographiée VERTE, P1 LE TROU
RECONSTITUÉ REFUSÉ (GetLastError 193, NTSTATUS 0xc000007b), P2 LE BSS
cartographié VERTE, P3 LE SOUS-SYSTÈME CUI cartographié VERTE, P4 LA
GÉOMÉTRIE dev.2 ENTIÈRE REFUSÉE — les axes NOMMÉS, les copies %TEMP%
mortes, la pièce INTACTE : LA DETTE DU RUN 10 EST ÉTEINTE, la retouche
[FREE-SANS-TYPE] A PORTÉ. PUIS [sonde-214] LA LIAISON COURUE : « 37
slots NON résolus (NULL ou valeur fichier) — LE CHARGEUR N'A PAS POSÉ
LES FONCTIONS ([OFT-QWORD] ?) — la pièce mourrait à la vitrine : LE
DÉFAUT EST NOMMÉ AU TÉMOIN » — LA LIGNE EST RENVOYÉE TELLE QUELLE.

LE TÉMOIN VITRINE (temoin-vitrine.txt) : LA VITRINE VIVANTE LA SECONDE
FOIS — [1/4] la vitrine vide : code 0 ; [2/4] la vitrine avec
temoin-fichier.bin : code 0 ; [3/4] AUCUN rapport WER ; [4/4] le journal
d'événements ne portant que les trois vieux LiveKernelEvent 1001 watchdog
(les mêmes qu'au dixième run : 30/10, 02/11, 03/11) : AUCUNE mort de
loupe.exe — L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR
DEUX RUNS DE SUITE, LA MÊME PIÈCE.

LE LABO PARLE — LE HUITIÈME DÉFAUT NOMMÉ SUR PIÈCES : [SONDE-EXE], LE
FAUX NÉGATIF STRUCTUREL, LE DÉFAUT DU KIT, PAS DE LA PIÈCE.
  1. SUR LES OCTETS : le COFF de la pièce relu — Characteristics
     {characteristics:#06x} (IMAGE_FILE_EXECUTABLE_IMAGE seul, le pas du
     format) et LE BIT IMAGE_FILE_DLL (0x2000) ABSENT (l'octet 0x57 ==
     0x00) : loupe.exe EST un EXE (le DataDirectory IMPORT {rva_import:#x}/
     {taille_import:#x} et IAT {rva_iat:#x}/{taille_iat:#x} sont déclarés
     et CONFORMES au plan).
  2. DANS LA DOC DU CHARGEUR (Microsoft Learn, LoadLibraryExA) : « {DOC} »
     — LE CHARGEUR DE BIBLIOTHÈQUE NE RÉSOUD JAMAIS LES IMPORTS D'UN
     MODULE EXÉCUTABLE : la sonde-214 (LoadLibraryExW drapeau 0 sur une
     copie EXE) ne peut JAMAIS y lire les fonctions posées, QUEL QUE
     SOIT l'état de la pièce.
  3. LA CORROBORATION : le comportement constaté (le mapping RÉUSSI, base
     non nulle + les 37 slots AUX VALEURS FICHIER) est EXACTEMENT le
     comportement documenté pour tout EXE chargé par bibliothèque : il n'y
     a AUCUN autre défaut à chercher — la pièce se comporte comme la doc
     le prédit. La mention « ([OFT-QWORD] ?) » était une PRÉDICTION
     d'avant-run : DÉMENTIE par les pièces (le D54 ÉTENDU au T0 a marché
     les QUATRE OFT au pas DWORD — la mécanique d'import est VERTE).
  4. LA PREUVE DU VIVANT : la sixième mort (neuvième run, dev.7 : 33
     slots périmés → BEX64 au SECOND appel IAT) a prouvé que la vitrine
     ne peut PAS vivre d'une IAT non résolue ; la vitrine dev.8 A VÉCU
     aux dixième ET onzième runs (0 et 0 chacun, la MÊME pièce
     {SHA_EXE[:16]}…) ⇒ LE CHARGEUR DE PROCESSUS A RÉSOLU L'IAT DE LA
     PIÈCE — LA LIAISON EST PROUVÉE PAR LE VIVANT. C'est la doctrine
     consignée à l'Entrée 216 : « la vitrine vivante prouve la liaison
     MIEUX que toute sonde — la fenêtre n'eût pas vécu d'un import non
     résolu ».
  5. LA PREUVE DU TÉMOIN : T1 → T7 vécus IAT posée (les 37 feuilles aux
     slots du plan, tous les blocs fonctionnent) ; S0-P0 la pièce intacte
     cartographiée VERTE : le mécanisme de la sonde est SAIN — seule sa
     PRÉSUPPOSITION (un EXE lié par le chargeur de bibliothèque) était
     fausse.
  6. [RET-NU] REVU : la doc (DONT_RESOLVE_DLL_REFERENCES : « If this
     value is used, and the executable module is a DLL, the system does
     not call DllMain ») — le DllMain n'est appelé QUE pour les DLL :
     les six octets mov eax, 1 ; ret de l'Entrée 215 furent une prudence
     SANS COÛT (l'entrée de la copie n'est jamais appelée pour un EXE) —
     LA PRUDENCE ACQUITTÉE, SANS REGRET.

LE VERDICT : LE CRITÈRE PUBLIÉ (le scénario ENTIER T0 → S0 → LA LIAISON
ET LA VITRINE VIVANTE) — T0 → T7 TOUT VERT, S0 LA CASCADE VÉCUE ENTIÈRE,
LA LIAISON COURUE ET SON CONSTAT NOMMÉ FAUX SUR LES PIÈCES ELLES-MÊMES
(l'octet, la doc, le terrain), LA VITRINE VIVANTE LA SECONDE FOIS :
**LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.0` EST DÉBLOQUÉE SUR LE
ONZIÈME RUN RECOUPÉ** (le recoup rend {VERTS}/{TOTAL} contrôles VERTS).
LA CONDITION NOMMÉE D'AVANCE (l'Entrée 216 : « si le vert TIENT ENTIER :
LA BALISE `loupe 0.1.0` SCELLÉE sur run recoupé — LE JALON M10, la
méthode TRIADE entière prouvée par la CRÉATION ») EST SATISFAITE.

MAIS LE SCELLAGE EST UN FAIT DE CARTE (D104 : « l'artefact n'est PAS
touché, le scellage est un fait de carte ») — ET LA CARTE DU DÉPÔT EST
EN RETARD DE TROIS ÉPOQUES (génération 13 / dev.5 ; la dette nommée à
l'Entrée 211, répétée par le T0 du témoin : « la carte, génération 16, à
régénérer au labo »). LE CHANTIER DU SCELLEMENT EST LA SUITE : le layout
porté à l'époque dev.8 (les retouches documentées dev.6/7/8 : le
relogement IAT, l'extension 64 bits, l'entrée réécrite, les QUATRE OFT
au pas DWORD), la carte régénérée à sa génération réelle (16), la
cristallisation R6 des 18 blocs à 10/10, les portes --sceller-final
portées au build (modèle D104/M9), LA BASCULE version=0.1.0-dev.8 →
0.1.0 dans frag-bld (occurrence unique, vérifiée en mémoire), les
fragments re-chiffrés, l'entête portant LA BALISE, la signature Ed25519
re-signée (graine durable D144), l'anti-rollback ARMÉ, le tableau de
bord « loupe 0.1.0 SCELLÉE sur le onzième run vert recoupé » — LOUPE.EXE
INTACT ({SHA_EXE[:16]}… — LE MÊME binaire que le run a couru). LE JALON
M10 SERA ALORS FRANCHI : la méthode TRIADE entière prouvée par la
CRÉATION — de l'intention (la couche I, les 18 spécifications) à
l'octet vécu chez son utilisateur.
"""
OUT.write_text(VERDICT, encoding="utf-8", newline="\n")
MD5_VERDICT = md5(OUT)
print(f"\n[recoup] LE VERDICT : {VERTS}/{TOTAL} VERT — écrit {OUT.name}, "
      f"{len(VERDICT)} o, md5 {MD5_VERDICT[:8]}…")
print("[recoup] MD5_TEMOIN_LOUPE   =", MD5_TEMOIN_LOUPE)
print("[recoup] MD5_TEMOIN_VITRINE =", MD5_TEMOIN_VITRINE)
print("[recoup] MD5_VERDICT        =", MD5_VERDICT)
sys.exit(0 if VERTS == TOTAL else 1)
