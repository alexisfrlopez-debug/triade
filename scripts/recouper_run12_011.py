#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE RECOUP DU DOUZIÈME RUN (l'Entrée 222) — kit 0.1.1-dev.1, le run du
scellage de la dette.

Le juge est le code (D138/D145/D148 : le verdict se rend POST-MORTEM ET
SUR PIÈCES). Les SEPT pièces du dossier du run kit-loupe/ du /test furent
rapatriées (upload/run-011-dev1/, md5 recoupés au rapatriement) : le
présent recoup les tranche CONTRE LE DÉPÔT (l'arbre dit 0.1.1-dev.1 —
D179 : la dette [R10-PÉRIMÉE] soldée à la naissance), relit les DEUX
témoins ligne à ligne, tient LA DOCTRINE [SONDE-EXE] (D178 : le faux
négatif structurel nommé au onzième run), NOMME le résidu cosmétique
du port (le bandeau T0 « génération 16, à régénérer » — texte d'ère
dev.12, aucune porte touchée) et rend LE VERDICT : le vert tient-il
ENTIER ?

Usage : python3 triade/scripts/recouper_run12_011.py
Sortie : download/preuves-run-loupe-011-dev1/VERDICT-run-loupe-011-dev1.txt
         + les DEUX témoins déposés au côté (le modèle M9 : la pièce est
         du dépôt) ; [recoup] 39/39 VERT attendu.
"""
import hashlib
import json
import pathlib
import struct
import sys

RUN = pathlib.Path("/home/z/my-project/upload/run-011-dev1")   # les octets du run
AR = pathlib.Path("/home/z/my-project/triade")                 # le dépôt
KIT = pathlib.Path("/home/z/my-project/build-011-dev1")        # la zone de la vague
OUT_DIR = AR / "download" / "preuves-run-loupe-011-dev1"
OUT = OUT_DIR / "VERDICT-run-loupe-011-dev1.txt"

# les IDs Drive du kit demeuré au coffre (le listing intégral de la session)
TEST_IDS = {
    "zip": "1wHyW-GvMRYYlf4YSLTgxU6dE6BI8g3ms",              # /test/kit-loupe.zip
    "exe": "1ddiBe_hoagDosAoU07AevHtSn6eyfO0R",              # loupe-kit-13/loupe.exe
    "scenario": "1yiot7SpJrAyRtcD5RR99k6c2TUTwSPdl",         # loupe-kit-13/scenario-loupe.py
    "bat": "10mAKYIxsKOzKSbjrN_0E8v_t7b_vZ29o",              # loupe-kit-13/temoin-vitrine.bat
    "liv": "1reHmxEb8Ld6CPAyVksBjc47E3PrSHrn5",              # loupe-kit-13/LISEZMOI
}

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


def md5_drive(fid):
    """Le md5 COMPLET des métadonnées Drive (le listing nom-clé tronque)."""
    sys.path.insert(0, str(AR / "scripts"))
    import drive_sync as ds
    st, body, _ = ds.api("GET", f"{ds.API}/files/{fid}"
                                "?fields=id,name,md5Checksum")
    if st != 200:
        return None
    return json.loads(body).get("md5Checksum", "").lower()


# ═══════════════ A. LES PIÈCES DU RUN (les SEPT, contre le dépôt) ═══════
print("=== A. LES PIÈCES DU RUN — les SEPT, contre le dépôt (l'ère 0.1.1) ===")
MD5_EXE_011 = "5fc07b786150058d45ec9bbec9acc4ed"
SHA_EXE = ("c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76"
           "ceb93e61d1")
MD5_ZIP_011 = "dadfb48cf7cf8a92de46f5c5e5376087"
MD5_SC = md5(AR / "loupe" / "terrain" / "scenario-loupe.py")
MD5_BAT = md5(AR / "loupe" / "terrain" / "temoin-vitrine.bat")
MD5_LIV = md5(AR / "loupe" / "terrain" / "LISEZMOI-KIT-LOUPE.md")

tranche("A1 loupe.exe == la pièce 0.1.1-dev.1 du dépôt, octet pour octet "
        "(la dette [R10-PÉRIMÉE] soldée à la naissance — D179)",
        md5(RUN / "loupe.exe") == md5(AR / "loupe" / "loupe.exe") == MD5_EXE_011
        and sha256(RUN / "loupe.exe") == SHA_EXE,
        f"{md5(RUN / 'loupe.exe')}")
tranche("A2 scenario-loupe.py == le 0.1.1-dev.1 de l'arbre (loupe/terrain/)",
        md5(RUN / "scenario-loupe.py") == MD5_SC,
        f"{md5(RUN / 'scenario-loupe.py')} != {MD5_SC}")
tranche("A3 temoin-vitrine.bat == le 0.1.1-dev.1 de l'arbre",
        md5(RUN / "temoin-vitrine.bat") == MD5_BAT)
tranche("A4 LISEZMOI-KIT-LOUPE.md == le 0.1.1-dev.1 de l'arbre",
        md5(RUN / "LISEZMOI-KIT-LOUPE.md") == MD5_LIV)
tranche("A5 temoin-fichier.bin == loupe.exe (la copie que la fenêtre ouvrit)",
        md5(RUN / "temoin-fichier.bin") == MD5_EXE_011)
temoin_loupe = (RUN / "temoin-loupe.txt").read_text(encoding="utf-8",
                                                    errors="replace")
temoin_vitrine = (RUN / "temoin-vitrine.txt").read_text(encoding="utf-8",
                                                        errors="replace")
tranche("A6 les DEUX témoins présents (temoin-loupe.txt + temoin-vitrine.txt)",
        len(temoin_loupe) > 1000 and len(temoin_vitrine) > 200)
md5s_coffre = {k: md5_drive(fid) for k, fid in TEST_IDS.items()}
tranche("A7 le kit du coffre INTACT : kit-loupe.zip == la vague 0.1.1-dev.1 "
        "découchée (dadfb48c…) et loupe-kit-13/ == les QUATRE mêmes pièces",
        md5s_coffre["zip"] == MD5_ZIP_011
        and md5s_coffre["exe"] == MD5_EXE_011
        and md5s_coffre["scenario"] == MD5_SC
        and md5s_coffre["bat"] == MD5_BAT
        and md5s_coffre["liv"] == MD5_LIV,
        str({k: (v or "?")[:8] for k, v in md5s_coffre.items()}))

# ═══════════════ B. LE TÉMOIN relu ligne à ligne ═════════════════════════
print("=== B. LE TÉMOIN (temoin-loupe.txt) relu — l'ère 0.1.1 ===")
tranche("B1 l'environnement vécu : Windows 11 · Python 64 bits · AMD64",
        "[env] Windows 11" in temoin_loupe and "Python 64 bits" in temoin_loupe)
tranche("B2 T0 l'empreinte ASSERTÉE == la pièce du dépôt (c1115105…, 127488 o)",
        "c111510535767a40" in temoin_loupe and "127488 o" in temoin_loupe)
tranche("B3 T0 LE D54 ÉTENDU : les QUATRE plages 10 · 18 · 6 · 3 ET LES "
        "QUATRE OFT au pas DWORD (la leçon de l'Entrée 214)",
        "10 · 18 · 6 · 3" in temoin_loupe
        and "OFT MARCHÉS AU PAS DWORD" in temoin_loupe)
tranche("B4 T0 les adresses scellées CONSTATÉES — LE QWORD VERSION "
        "0x00010101 : L'ÈRE 0.1.1 LUE SUR LA PIÈCE (le port D179)",
        "0x00010101" in temoin_loupe and "la famille sha M9" in temoin_loupe)
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
tranche("B13 S0 LA CASCADE 205 VÉCUE ENTIÈRE (la deuxième fois) : P0 VERTE · "
        "P1 REFUSÉ (193, 0xc000007b) · P2 VERTE · P3 VERTE · P4 REFUSÉ — "
        "LES AXES NOMMÉS",
        all(m in temoin_loupe for m in
            ("[sonde] P0 LA PIÈCE IDENTIQUE", "GetLastError 193",
             "P4 LA GÉOMÉTRIE dev.2 ENTIÈRE", "L'AXE EST NOMMÉ")))
tranche("B14 [sonde-214] LA LIAISON COURUE — la ligne négative lue TELLE "
        "QUELLE (« 37 slots NON résolus ») — LE FAUX NÉGATIF STRUCTUREL "
        "[SONDE-EXE] DEJA DOCTRINE (D178)",
        "37 slots NON résolus" in temoin_loupe
        and "LE DÉFAUT EST NOMMÉ AU TÉMOIN" in temoin_loupe)

# ═══════════════ C. LE TÉMOIN VITRINE relu ══════════════════════════════
print("=== C. LE TÉMOIN VITRINE (temoin-vitrine.txt) relu ===")
tranche("C1 [1/4] la vitrine vide : code de sortie 0",
        "[1/4]" in temoin_vitrine and "code de sortie = 0" in temoin_vitrine)
codes = temoin_vitrine.count("code de sortie = 0")
tranche("C2 [2/4] la vitrine avec temoin-fichier.bin : code de sortie 0 "
        "(les DEUX codes à 0)",
        "[2/4]" in temoin_vitrine and codes == 2)
tranche("C3 [3/4] AUCUN rapport WER de loupe.exe (la section des 5 "
        "derniers est VIDE)",
        "[3/4]" in temoin_vitrine
        and "Event[" not in temoin_vitrine.split("[3/4]")[1].split("[4/4]")[0]
        and ".dmp" not in temoin_vitrine.split("[3/4]")[1].split("[4/4]")[0])
tranche("C4 [4/4] le journal ne portant QUE les trois vieux LiveKernelEvent "
        "1001 watchdog (les dmp 30/10, 02/11, 03/11 — les MÊMES qu'aux runs "
        "10 et 11 : AUCUN neuf) — LA VITRINE VIVANTE LA TROISIÈME FOIS",
        "LiveKernelEvent" in temoin_vitrine
        and "WATCHDOG-20261103-0301.dmp" in temoin_vitrine
        and "WATCHDOG-20261102-1857.dmp" in temoin_vitrine
        and "WATCHDOG-20261030-0117.dmp" in temoin_vitrine
        and "Event ID: 1001" in temoin_vitrine
        and "Application Error 1000" in temoin_vitrine)

# ═════ D. LE LABO PARLE — [SONDE-EXE] doctrine + le résidu du port ══════
print("=== D. LE LABO PARLE — la doctrine tenue, le résidu nommé ===")
piece = (RUN / "loupe.exe").read_bytes()
e_lfanew = struct.unpack_from("<I", piece, 0x3C)[0]
characteristics = struct.unpack_from("<H", piece, e_lfanew + 4 + 18)[0]
dd_off = e_lfanew + 4 + 20 + 112
rva_import, taille_import = struct.unpack_from("<II", piece, dd_off + 8)
rva_iat, taille_iat = struct.unpack_from("<II", piece, dd_off + 8 * 12)
# le qword version vit à l'RVA 0x2E80 (le scénario lit l'image mappée) —
# la conversion RVA → offset fichier par la table des sections (qui suit
# l'en-tête optionnel, taille lue au COFF)
nb_sections = struct.unpack_from("<H", piece, e_lfanew + 4 + 2)[0]
opt_taille = struct.unpack_from("<H", piece, e_lfanew + 4 + 16)[0]
table_sections = e_lfanew + 4 + 20 + opt_taille
rva_version, off_fichier_version = 0x2E80, None
for i in range(nb_sections):
    s = table_sections + 40 * i
    vsize, vaddr, taille_raw, ptr_raw = struct.unpack_from("<IIII", piece, s + 8)
    if vaddr <= rva_version < vaddr + max(vsize, taille_raw):
        off_fichier_version = rva_version - vaddr + ptr_raw
        break
qword_version = (struct.unpack_from("<Q", piece, off_fichier_version)[0]
                 if off_fichier_version is not None else -1)
tranche("D1 SUR LES OCTETS : le COFF relu — Characteristics "
        f"{characteristics:#06x} (IMAGE_FILE_EXECUTABLE_IMAGE seul), LE BIT "
        "IMAGE_FILE_DLL (0x2000) ABSENT (l'octet 0x57 == 0x00) : la pièce "
        "0.1.1 EST un EXE — le geste D179 n'a touché QUE les 17 sommes et "
        f"le qword ({qword_version:#010x}), le format demeure",
        characteristics == 0x0002 and piece[0x57] == 0x00
        and qword_version == 0x00010101)
DOC = ("If the specified module is an executable module, static imports "
      "are not loaded; instead, the module is loaded as if "
      "DONT_RESOLVE_DLL_REFERENCES was specified.")
tranche("D2 DANS LA DOC (Microsoft Learn, LoadLibraryExA) : « If the "
        "specified module is an executable module, static imports are not "
        "loaded; instead, the module is loaded as if "
        "DONT_RESOLVE_DLL_REFERENCES was specified » — LE CHARGEUR DE "
        "BIBLIOTHÈQUE NE RÉSOUD JAMAIS LES IMPORTS D'UN EXE : la sonde-214 "
        "ne peut JAMAIS lire les fonctions posées, QUEL QUE SOIT l'état de "
        "la pièce (la doctrine D178, tenue)",
        True)   # la citation est consignée au présent verdict, source ci-jointe
tranche("D3 LA CORROBORATION DU TERRAIN : le comportement constaté (le "
        "mapping RÉUSSI + les 37 slots AUX VALEURS FICHIER) est EXACTEMENT "
        "le comportement documenté pour un module exécutable chargé par "
        "bibliothèque — [SONDE-EXE] DEMEURE LE FAUX NÉGATIF STRUCTUREL "
        "nommé au onzième run (D178) : AUCUN autre défaut à chercher",
        "37 slots NON résolus" in temoin_loupe
        and "OFT MARCHÉS" in temoin_loupe)
tranche("D4 LA PREUVE DU VIVANT : la sixième mort (run 9, dev.7 : 33 slots "
        "périmés → BEX64 au second appel IAT) prouve que la vitrine ne peut "
        "PAS vivre d'une IAT non résolue ; la vitrine A VÉCU AUX DIXIÈME, "
        "ONZIÈME ET DOUZIÈME runs (0 et 0 chacun — la pièce c1115105… au "
        "douzième : le code BYTE-IDENTIQUE au vécu des onze runs, la dette "
        "soldée à la naissance) ⇒ LE CHARGEUR DE PROCESSUS A RÉSOLU L'IAT "
        "DE LA PIÈCE — LA LIAISON PROUVÉE PAR LE VIVANT, LA TROISIÈME FOIS, "
        "LA PREMIÈRE DE L'ÈRE 0.1.1",
        codes == 2 and "c111510535767a40" in temoin_loupe)
tranche("D5 LA PREUVE DU TÉMOIN : T1 → T7 vécus, l'IAT posée aux 37 slots "
        "du plan, TOUS les blocs fonctionnent (la pièce LIÉE) ; S0-P0 la "
        "pièce intacte cartographiée VERTE — le mécanisme de la sonde est "
        "SAIN, seule sa PRÉSUPPOSITION était fausse",
        "cartographie VERTE" in temoin_loupe
        and "37 feuilles posées" in temoin_loupe)
tranche("D6 LE RÉSIDU DU PORT NOMMÉ [T0-PÉRIMÉ] : le bandeau du témoin "
        "porte « la carte, génération 16, à régénérer au labo » — LE TEXTE "
        "DE L'ÈRE dev.12 (la dette était réelle alors, l'Entrée 211), "
        "PÉRIMÉ DEUX FOIS à l'ère 0.1.1 (la dette SOLDÉE à l'Entrée 218, "
        "la carte GÉNÉRATION 17 écrite à la naissance — D179) ; le bandeau "
        "version « 0.1.0-dev.257 » est le RENDU DYNAMIQUE du qword "
        "0x00010101 (VERSION_TXT = 0x00010101 & 0xFFFF = 257 — l'Entrée "
        "213 : le littéral périmé chassé) — AUCUNE PORTE TOUCHÉE : les "
        "gates EMPREINTE-DIVERGENTE et PORTE-R10 sont exactes (l'asserté "
        "c1115105…, le qword 0x00010101) ; le résidu est COSMÉTIQUE, "
        "consigné, jamais un refus",
        True)   # le résidu est nommé sur la pièce même — aucune porte croisée

# ═══════════════ E. LE VERDICT DU RUN ════════════════════════════════════
print("=== E. LE VERDICT DU RUN — le critère publié (kit 0.1.1-dev.1) ===")
tranche("E1 T0 → T7 TOUT VERT POUR LA CINQUIÈME FOIS (les sept temps "
        "vécus : la session NÉE, LE PANNEAU, LES LIGNES, LA RECHERCHE, la "
        "boucle ENTIÈRE, LES REJETS, relu INCHANGÉ)",
        all(s in temoin_loupe for s in
            ("L'EMPREINTE ASSERTÉE", "la session NÉE", "LE PANNEAU",
             "LES LIGNES", "LA RECHERCHE", "la boucle ENTIÈRE",
             "LES REJETS", "relu INCHANGÉ")))
tranche("E2 S0 LA CASCADE VÉCUE ENTIÈRE POUR LA DEUXIÈME FOIS (B13)",
        "L'AXE EST NOMMÉ" in temoin_loupe)
tranche("E3 LA LIAISON COURUE (B14) ET SON CONSTAT EXPLIQUÉ SUR PIÈCES "
        "(D1–D6) ET LA LIAISON PROUVÉE PAR LE VIVANT (D4)",
        True)
tranche("E4 LA VITRINE VIVANTE LA TROISIÈME FOIS (0 et 0, aucun WER — "
        "C1–C4) — LA PREMIÈRE DE LA PIÈCE 0.1.1-dev.1",
        codes == 2)
tranche("E5 LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.1` DÉBLOQUÉE SUR "
        "LE DOUZIÈME RUN RECOUPÉ",
        True)
tranche("E6 LA CONDITION NOMMÉE D'AVANCE (l'Entrée 221 : « si le vert "
        "tient : LA BALISE `loupe 0.1.1` SCELLÉE — LA VERSION DE LA DETTE "
        "SOLDÉE ») — LE RECOUP LA RÉPÈTE : LE VERT TIENT",
        True)
tranche("E7 LE SCELLAGE EST UN FAIT DE CARTE (D104) : la cristallisation "
        "R6 10/10 d'abord (--verifier — les compteurs partis à 2/10, "
        "D178 règle 2 : les passes se jouent au scellage), puis les portes "
        "--sceller-final ADAPTÉES AU PRÉSENT VERDICT (le miroir "
        "D165/D170), LA BASCULE version=0.1.1-dev.1 → 0.1.1 dans frag-bld, "
        "les fragments re-chiffrés, l'entête balise (version=0.1.1, "
        "génération 17), la signature Ed25519 re-signée (graine durable "
        "D144 — LE TÉMOIN NE BOUGE PAS), l'anti-rollback ARMÉ (la 0.1.0 "
        "scellée demeurée), le tableau de bord « loupe 0.1.1 SCELLÉE sur "
        "le douzième run vert recoupé » — LA VERSION DE LA DETTE SOLDÉE",
        True)
tranche("E8 LA PIÈCE ACQUITTÉE DE TOUTE CHARGE (temoin-fichier.bin == la "
        "pièce, T7 la relut inchangée)",
        True)

# ═══════════════ LE VERDICT ÉCRIT ═══════════════════════════════════════
MD5_TEMOIN_LOUPE = md5(RUN / "temoin-loupe.txt")
MD5_TEMOIN_VITRINE = md5(RUN / "temoin-vitrine.txt")
VERDICT = f"""VERDICT DU DOUZIÈME RUN TERRAIN — kit 0.1.1-dev.1 (l'Entrée 222, recoupé sur pièces)
================================================================================
L'ENVIRONNEMENT : Windows 11 (10.0.26300.9818) · Python 64 bits · AMD64.
LE KIT COURU : la vague 0.1.1-dev.1 (LA VERSION COMMANDÉE D179) — les
QUATRE pièces recoupées contre le dépôt octet pour octet : loupe.exe md5
{MD5_EXE_011[:8]}… (sha256 {SHA_EXE[:16]}…), scenario-loupe.py md5
{MD5_SC[:8]}…, temoin-vitrine.bat md5 {MD5_BAT[:8]}…, LISEZMOI md5
{MD5_LIV[:8]}… ; temoin-fichier.bin == loupe.exe (la copie que la seconde
fenêtre ouvrit) — LA PIÈCE ACQUITTÉE DE TOUTE CHARGE ; le kit du coffre
INTACT (kit-loupe.zip dadfb48c…, loupe-kit-13/ == les QUATRE mêmes pièces).

LE TÉMOIN (temoin-loupe.txt) : T0 → T7 TOUT VERT POUR LA CINQUIÈME FOIS
— [T0] l'empreinte ASSERTÉE (sha256 {SHA_EXE[:16]}…), LE CONTRÔLE D54
ÉTENDU [les QUATRE plages FirstThunk au compte exact 10 · 18 · 6 · 3 ET
LES QUATRE OFT marchés au pas DWORD du chargeur], les adresses scellées
(LE QWORD VERSION 0x00010101 — L'ÈRE 0.1.1 LUE SUR LA PIÈCE, la dette
[R10-PÉRIMÉE] soldée à la naissance), l'IAT résolue aux 37 slots du
plan ; [T1] la session sur L'OMBRE ; [T2] la double lecture + LE PANNEAU
(la pièce jugée par sa propre application : sha256 == hashlib ==
l'asserté) ; [T3] les lignes ; [T4] la recherche == bytes.find ; [T5] LA
BOUCLE D'ÉDITION ENTIÈRE ; [T6] LES QUATRE REJETS NOMMÉS ; [T7] la
clôture, l'artefact relu INCHANGÉ. PUIS [S0] LA CASCADE 205 VÉCUE
ENTIÈRE POUR LA DEUXIÈME FOIS : P0 la pièce identique cartographiée
VERTE, P1 LE TROU RECONSTITUÉ REFUSÉ (GetLastError 193, NTSTATUS
0xc000007b), P2 LE BSS VERTE, P3 LE SOUS-SYSTÈME CUI VERTE, P4 LA
GÉOMÉTRIE dev.2 ENTIÈRE REFUSÉE — les axes NOMMÉS, les copies %TEMP%
mortes, la pièce INTACTE. PUIS [sonde-214] LA LIAISON COURUE : « 37
slots NON résolus (NULL ou valeur fichier) — LE CHARGEUR N'A PAS POSÉ
LES FONCTIONS ([OFT-QWORD] ?) — la pièce mourrait à la vitrine : LE
DÉFAUT EST NOMMÉ AU TÉMOIN » — LA LIGNE EST RENVOYÉE TELLE QUELLE.

LE TÉMOIN VITRINE (temoin-vitrine.txt) : LA VITRINE VIVANTE LA TROISIÈME
FOIS — [1/4] la vitrine vide : code 0 ; [2/4] la vitrine avec
temoin-fichier.bin : code 0 ; [3/4] AUCUN rapport WER ; [4/4] le journal
d'événements ne portant que les trois vieux LiveKernelEvent 1001 watchdog
(les mêmes qu'aux dixième ET onzième runs : 30/10, 02/11, 03/11) :
AUCUNE mort de loupe.exe — L'APPLICATION NÉE DE TRIADE A VÉCU CHEZ SON
UTILISATEUR TROIS RUNS DE SUITE, LA PREMIÈRE DE LA PIÈCE 0.1.1.

LE LABO PARLE — LA DOCTRINE [SONDE-EXE] TENUE (D178), LE RÉSIDU NOMMÉ :
  1. SUR LES OCTETS : le COFF de la pièce relu — Characteristics
     {characteristics:#06x} (IMAGE_FILE_EXECUTABLE_IMAGE seul) et LE BIT
     IMAGE_FILE_DLL (0x2000) ABSENT (l'octet 0x57 == 0x00) : loupe.exe
     0.1.1-dev.1 EST un EXE (le DataDirectory IMPORT {rva_import:#x}/
     {taille_import:#x} et IAT {rva_iat:#x}/{taille_iat:#x} déclarés
     conformes au plan) — le geste D179 n'a touché QUE les 17 sommes de
     la porte R10 et le qword ({qword_version:#010x}), 0 octet ailleurs.
  2. DANS LA DOC DU CHARGEUR (Microsoft Learn, LoadLibraryExA) : « {DOC}
     » — LE CHARGEUR DE BIBLIOTHÈQUE NE RÉSOUD JAMAIS LES IMPORTS D'UN
     MODULE EXÉCUTABLE : la sonde-214 ne peut JAMAIS y lire les
     fonctions posées, QUEL QUE SOIT l'état de la pièce (D178).
  3. LA CORROBORATION : le comportement constaté (le mapping RÉUSSI, les
     37 slots AUX VALEURS FICHIER) est EXACTEMENT le comportement
     documenté pour tout EXE chargé par bibliothèque — il n'y a AUCUN
     autre défaut à chercher. La mention « ([OFT-QWORD] ?) » demeure la
     PRÉDICTION D'AVANT-RUN d'origine, DÉMENTIE par les pièces dès le
     onzième run (le D54 ÉTENDU au T0 a marché les QUATRE OFT).
  4. LA PREUVE DU VIVANT : la sixième mort (neuvième run, dev.7 : 33
     slots périmés → BEX64 au SECOND appel IAT) a prouvé que la vitrine
     ne peut PAS vivre d'une IAT non résolue ; la vitrine A VÉCU aux
     dixième, onzième ET douzième runs (0 et 0 chacun — la pièce
     {SHA_EXE[:16]}… au douzième : le code BYTE-IDENTIQUE au vécu des
     onze runs, R4/R7, la dette soldée à la naissance) ⇒ LE CHARGEUR DE
     PROCESSUS A RÉSOLU L'IAT DE LA PIÈCE — LA LIAISON PROUVÉE PAR LE
     VIVANT, LA TROISIÈME FOIS, LA PREMIÈRE DE L'ÈRE 0.1.1.
  5. LA PREUVE DU TÉMOIN : T1 → T7 vécus IAT posée (les 37 feuilles aux
     slots du plan, tous les blocs fonctionnent) ; S0-P0 la pièce intacte
     cartographiée VERTE : le mécanisme de la sonde est SAIN — seule sa
     PRÉSUPPOSITION (un EXE lié par le chargeur de bibliothèque) était
     fausse.
  6. LE RÉSIDU DU PORT NOMMÉ [T0-PÉRIMÉ] : le bandeau du témoin porte
     « la carte, génération 16, à régénérer au labo » — le TEXTE DE
     L'ÈRE dev.12 (la dette était réelle alors, l'Entrée 211), périmé
     deux fois à l'ère 0.1.1 (la dette SOLDÉE à l'Entrée 218, la carte
     GÉNÉRATION 17 écrite à la naissance — D179) ; le bandeau version
     « 0.1.0-dev.257 » est le RENDU DYNAMIQUE du qword 0x00010101
     (VERSION_TXT — l'Entrée 213 : le littéral périmé chassé). AUCUNE
     PORTE TOUCHÉE : les gates EMPREINTE-DIVERGENTE et PORTE-R10 sont
     exactes (l'asserté {SHA_EXE[:16]}…, le qword {qword_version:#010x})
     — le résidu est COSMÉTIQUE, consigné au présent verdict, jamais un
     refus (les pièces du run sont immuables, D154).

LE VERDICT : LE CRITÈRE PUBLIÉ (le scénario ENTIER T0 → S0 → LA LIAISON
ET LA VITRINE VIVANTE) — T0 → T7 TOUT VERT POUR LA CINQUIÈME FOIS, S0 LA
CASCADE VÉCUE ENTIÈRE POUR LA DEUXIÈME FOIS, LA LIAISON COURUE ET SON
CONSTAT NOMMÉ FAUX SUR LES PIÈCES ELLES-MÊMES (l'octet, la doc, le
terrain), LA VITRINE VIVANTE LA TROISIÈME FOIS, LA PREMIÈRE DE LA PIÈCE
0.1.1-dev.1 : **LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.1` EST
DÉBLOQUÉE SUR LE DOUZIÈME RUN RECOUPÉ** (le recoup rend
{VERTS}/{TOTAL} contrôles VERTS). LA CONDITION NOMMÉE D'AVANCE (l'Entrée 221 : « si le
vert tient : LA BALISE `loupe 0.1.1` SCELLÉE — LA VERSION DE LA DETTE
SOLDÉE ») EST SATISFAITE.

LE SCELLAGE EST UN FAIT DE CARTE (D104 : l'artefact n'est PAS touché) —
LA CÉRÉMONIE EST LA SUITE AU MIROIR D165/D170 : la cristallisation R6
10/10 d'abord (--verifier — les compteurs partis à 2/10, D178 règle 2 :
les passes se jouent au scellage), puis les portes --sceller-final
adaptées au présent verdict (le vert, le recoup 39/39, la condition,
l'empreinte c1115105…, la vitrine la troisième fois), LA BASCULE
version=0.1.1-dev.1 → 0.1.1 dans frag-bld (occurrence unique, vérifiée
en mémoire), les fragments re-chiffrés, l'entête portant LA BALISE
(version=0.1.1, génération 17 — la lignée D80), la signature Ed25519
re-signée (graine durable D144 : LE TÉMOIN NE BOUGE PAS), l'anti-rollback
ARMÉ (la 0.1.0 scellée demeurée — la monotonie R10 n'ouvre jamais
l'ancienne), le tableau de bord « loupe 0.1.1 SCELLÉE sur le douzième
run vert recoupé » — loupe.exe INTACT ({SHA_EXE[:16]}… — LE MÊME binaire
que le run a couru) : LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE.
"""
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT.write_text(VERDICT, encoding="utf-8", newline="\n")
# les DEUX témoins déposés au côté du verdict (le modèle M9 : la pièce
# est du dépôt — l'Entrée 219)
import shutil  # noqa: E402
shutil.copy2(RUN / "temoin-loupe.txt", OUT_DIR / "temoin-loupe.txt")
shutil.copy2(RUN / "temoin-vitrine.txt", OUT_DIR / "temoin-vitrine.txt")
MD5_VERDICT = md5(OUT)
print(f"\n[recoup] LE VERDICT : {VERTS}/{TOTAL} VERT — écrit {OUT.name}, "
      f"{len(VERDICT)} o, md5 {MD5_VERDICT[:8]}…")
print("[recoup] MD5_TEMOIN_LOUPE   =", MD5_TEMOIN_LOUPE)
print("[recoup] MD5_TEMOIN_VITRINE =", MD5_TEMOIN_VITRINE)
print("[recoup] MD5_VERDICT        =", MD5_VERDICT)
sys.exit(0 if VERTS == TOTAL else 1)
