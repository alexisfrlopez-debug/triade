#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le générateur du KIT dev.10 — la réponse de l'Entrée 214 au run 9.

Transforme le kit dev.9 (run9/) en kit dev.10 (build-dev10/) :
  - scenario-loupe.py : SHA_EXE (pièce dev.8), VERSION_R10 0x00010008,
    LA MARCHE DES QUATRE OFT au pas DWORD du chargeur (le contrôle qui
    eût nommé [OFT-QWORD]), la sonde 205 réparée (FreeLibrary avant
    suppression — le PermissionError du run 9) et rendue inextinguible
    (try/except par essai), ET LA NOUVELLE SONDE DE LIAISON (une copie
    chargée SANS DONT_RESOLVE, l'entrée neutralisée d'un octet ret, les
    37 slots relus : le chargeur doit y avoir posé les fonctions) ;
  - temoin-vitrine.bat : les littéraux portés à dev.8 / kit dev.10 ;
  - LISEZMOI-KIT-LOUPE.md : l'histoire du run 9 et de la sixième mort
    nommée, la retouche, les nouveaux contrôles.
"""
import os
import py_compile
import re
import shutil
import sys

SRC = "/home/z/my-project/run9"
DST = "/home/z/my-project/build-dev10"
SHA_V8 = "054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69"

os.makedirs(DST, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════
# 1. LE SCÉNARIO
# ═════════════════════════════════════════════════════════════════════
sc = open(os.path.join(SRC, "scenario-loupe.py"), encoding="utf-8").read()

def remplace(ancien, nouveau, combien=1):
    global sc
    n = sc.count(ancien)
    assert n == combien, f"ancre {n}× (attendu {combien}) : {ancien[:60]!r}"
    sc = sc.replace(ancien, nouveau)

# 1a. l'en-tête du docstring
remplace("NATURE (kit dev.8, l'Entrée 210).",
         "NATURE (kit dev.10, l'Entrée 214).")

# 1b. le bloc-artefact du docstring — l'histoire du run 9 et de dev.8
debut = sc.index("  loupe.exe   le build 0.1.0-dev.7 du jalon M10")
fin = sc.index("              0x00010007) ;") + len("              0x00010007) ;")
nouveau_bloc = """  loupe.exe   le build 0.1.0-dev.8 du jalon M10 — 127 488 o, sha256
              054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69
              (LA RETOUCHE DE L'ENTRÉE 214 : le neuvième run a tenu
              T0 → T7 TOUT VERT POUR LA SECONDE FOIS, puis a nommé
              DEUX faits. PREMIER FAIT [PERMISSION-SONDE] À LA SONDE :
              la réparation dev.9 VÉCUT (l'AttributeError de ctypes
              est morte) mais la cascade mourut sur SON PROPRE
              NETTOYAGE — un module LoadLibraryEx-é est CHARGÉ : il se
              LIBÈRE (FreeLibrary) avant de se supprimer, le
              PermissionError(13) du run 9 ne passera plus, et chaque
              essai vit dans son try : la cascade ne meurt JAMAIS sur
              son propre geste. SECOND FAIT — LA SIXIÈME MORT DE LA
              VITRINE, NOMMÉE PAR LE SYSTÈME PUIS PAR LE LABO : le
              témoin portant [4/4] livra LE JOURNAL D'ÉVÉNEMENTS —
              BEX64, module fautif « unknown », 0xC0000005, exécution
              sur mémoire non exécutable — et le recoup labo nomma LA
              CAUSE SUR LES OCTETS : [OFT-QWORD] — les QUATRE tableaux
              OriginalFirstThunk étaient écrits à PAS DE QWORD (RVA +
              quatre octets de zéro) au lieu du PAS DE DWORD du format
              PE : le VRAI chargeur lit OFT[1] = 0, croit chaque liste
              terminée, résout UNE fonction par DLL — les 33 autres
              slots IAT gardent leur valeur fichier (les RVA des
              noms) — le SECOND appel de l'entrée (GetCommandLineW,
              slot 0x3108) saute à l'adresse absolue 0x2A53, page non
              mappée, aucun module : LA MORT NOMMÉE, la cinquième
              comme elle. LA CÉCITÉ DES VERTS EXPLIQUÉE : le
              scénario-chargeur pose les 37 feuilles À LA MAIN (il ne
              lit jamais l'OFT), le simulateur branche des relais, la
              sonde 205 cartographie DONT_RESOLVE (le drapeau qui
              SAUTE la résolution des imports), le contrôle D54
              marchait la FirstThunk — jamais l'OFT. LA RETOUCHE :
              les QUATRE OFT COMPACTÉS AU PAS DE DWORD [10 · 18 · 6 · 3
              + terminateurs], en place — les pointeurs de
              descripteurs inchangés, la table de noms inchangée, le
              .text/.text2/.data/les en-têtes OCTET-IDENTIQUES, les
              adresses scellées INTACTES, la taille CONSTANTE — 89
              octets modifiés en tout ; ET LA LEÇON INSTITUTIONNALISÉE
              : le présent scénario dev.10 MARCHE LUI-MÊME LES QUATRE
              OFT au pas DWORD du chargeur [chaque entrée == le
              préremplissage de son slot — [OFT-QWORD] ne passera
              plus jamais], ET LA NOUVELLE SONDE DE LIAISON VIT LE
              VRAI CHARGEUR POSER LES FONCTIONS ; le qword version
              0x00010007 → 0x00010008) ;"""
sc = sc[:debut] + nouveau_bloc + sc[fin:]

# 1c. les 37 feuilles (le littéral 34 datait d'avant la double entrée)
remplace("puis il RÉSOUT LUI-MÊME les 34 feuilles de",
         "puis il RÉSOUT LUI-MÊME les 37 feuilles de")

# 1d. le paragraphe S0 du docstring — la sonde de liaison
remplace("TÉMOIN, pas muré derrière un bouton OK.",
         """TÉMOIN, pas muré derrière un bouton OK. ET LA SONDE DE L'ENTRÉE
214 COMPLÈTE LE TABLEAU : LA LIAISON VÉCUE — une copie chargée SANS
DONT_RESOLVE (l'entrée de la copie neutralisée d'un seul octet ret :
la fenêtre n'y est jamais lancée), les 37 slots RELUS — le VRAI
chargeur doit y avoir posé LES ADRESSES DES FONCTIONS, plus AUCUNE
valeur fichier : la sixième mort [OFT-QWORD] y était invisible, jamais
plus. (Et la cascade 205 réparée de son propre nettoyage : le module
chargé se LIBÈRE avant sa suppression — le PermissionError du run 9.)""")

# 1e. la génération de la carte
remplace("#     en génération 13 — la régénération est dette au labo, l'Entrée 211) -----",
         "#     en génération 16 — la régénération est dette au labo, l'Entrée 211) -----")
remplace("la carte, génération 13, à régénérer au labo",
         "la carte, génération 16, à régénérer au labo")

# 1f. SHA_EXE — la pièce dev.8
sc = re.sub(r'SHA_EXE = \(.*?\)\n',
            f'SHA_EXE = ("{SHA_V8}")\n', sc, count=1, flags=re.S)

# 1g. VERSION_R10 — dev.8
remplace("""VERSION_R10 = 0x00010007          # loupe 0.1.0-dev.7 (le qword @0x2E80 —
                                   # la retouche de l'Entrée 210 : [D54-QUATRIÈME]
                                   # chassé, l'IAT relogée séparée à 0x3100,
                                   # et [EAX-SANS-SIGNE] étendu au 64 bits)""",
         """VERSION_R10 = 0x00010008          # loupe 0.1.0-dev.8 (le qword @0x2E80 —
                                   # la retouche de l'Entrée 214 : [OFT-QWORD]
                                   # nommé sur les octets du run 9, les QUATRE
                                   # OFT compactés au pas DWORD du chargeur)""")

# 1h. LA MARCHE DES OFT au pas du chargeur — dans la boucle descripteur
remplace("""        vus += 1
        desc += 20""",
         """        # LA MARCHE DE L'OFT AU PAS DU CHARGEUR (la leçon de l'Entrée
        # 214 : [OFT-QWORD] — un OFT à pas de qword tue la vitrine sans
        # jamais toucher le scénario : le chargeur lit OFT[1] = 0, croit
        # la liste finie, laisse les slots périmés — l'entrée saute à
        # l'adresse du NOM. Le contrôle D54 marchait la FirstThunk ;
        # désormais L'OFT AUSTREMENT est marché au pas DWORD, arrêt au
        # premier NULL — ET chaque entrée doit être le préremplissage
        # du slot correspondant : le chargeur posera exactement le plan)
        j = 0
        while struct.unpack("<I", lire(oft + 4 * j, 4))[0] != 0:
            j += 1
            if j > 40:
                echec("D54-OFT", f"l'OFT @{oft:#x} marche au-delà de 40 — "
                     f"le terminateur DWORD est ABSENT")
                break
        if j != n_att:
            echec("D54-OFT", f"l'OFT @{oft:#x} du descripteur #{vus} "
                 f"({dll_att}) marche {j} entrées != {n_att} AU PAS DWORD "
                 f"DU CHARGEUR — [OFT-QWORD, l'Entrée 214] : le chargeur "
                 f"lirait OFT[1] = 0, croirait la liste finie, laisserait "
                 f"les slots à leur valeur fichier — l'entrée sauterait à "
                 f"l'adresse du NOM : 0xC0000005, module unknown — LA "
                 f"SIXIÈME MORT ne passera plus jamais ici")
        for i2 in range(j):
            if struct.unpack("<I", lire(oft + 4 * i2, 4))[0] != \\
                    struct.unpack("<Q", lire(ft + 8 * i2, 8))[0]:
                echec("D54-OFT", f"l'OFT[{i2}] @{oft + 4*i2:#x} != le "
                     f"préremplissage FT[{i2}] @{ft + 8*i2:#x} — le "
                     f"chargeur poserait un AUTRE nom que le plan au slot")
        vus += 1
        desc += 20""")

# 1i. la consigne D54 étendue
remplace("""    consigne("[T0] l'habillage d'import VÉRIFIÉ : QUATRE plages FirstThunk "
             "marchées au compte exact [10 · 18 · 6 · 3], les séparateurs "
             "NULL en place, les slots PRÉREMLIS du fichier — le motif D54 "
             "ENTIER (la leçon D97 entre au scénario — l'Entrée 210)")""",
         """    consigne("[T0] l'habillage d'import VÉRIFIÉ : QUATRE plages FirstThunk "
             "marchées au compte exact [10 · 18 · 6 · 3], les séparateurs "
             "NULL en place, les slots PRÉREMLIS du fichier — ET LES "
             "QUATRE OFT MARCHÉS AU PAS DWORD DU CHARGEUR [10 · 18 · 6 · "
             "3, chaque entrée == le préremplissage de son slot — la "
             "leçon de l'Entrée 214 : [OFT-QWORD] ne passera plus jamais]")""")

# 1j. la sonde 205 : FreeLibrary + inextinguible
remplace("""            k32.SetLastError(0)
            base = k32.LoadLibraryExW(chemin_sonde, None, 0x00000001)
            err = ctypes.get_last_error()
            etat = statut_nt()
            if base:
                lignes.append(f"[sonde] {nom} : cartographie VERTE @ "
                              f"{base:#x} — {description}")
            else:
                refus.append(nom)
                if nom.startswith("P0"):
                    p0_refus = True
                lignes.append(f"[sonde] {nom} : REFUS DU CHARGEUR — "
                              f"GetLastError {err}, NTSTATUS {etat:#010x} "
                              f"— {description}")
            os.remove(chemin_sonde)""",
         """            try:
                k32.SetLastError(0)
                base = k32.LoadLibraryExW(chemin_sonde, None, 0x00000001)
                err = ctypes.get_last_error()
                etat = statut_nt()
                if base:
                    lignes.append(f"[sonde] {nom} : cartographie VERTE @ "
                                  f"{base:#x} — {description}")
                else:
                    refus.append(nom)
                    if nom.startswith("P0"):
                        p0_refus = True
                    lignes.append(f"[sonde] {nom} : REFUS DU CHARGEUR — "
                                  f"GetLastError {err}, NTSTATUS "
                                  f"{etat:#010x} — {description}")
                if base:
                    k32.FreeLibrary(base)   # LA LEÇON DU RUN 9 : un module
                                            # CHARGÉ ne se supprime pas —
                                            # le PermissionError(13) du
                                            # neuvième run ne passera plus
                os.remove(chemin_sonde)
            except OSError as exc:
                lignes.append(f"[sonde] {nom} : ÉCHEC DE LA SONDE — "
                              f"{exc!r} — la cascade CONTINUE (l'essai "
                              f"est mort, PAS la pièce : le labo recoupe "
                              f"sur pièces)")""")

# 1k. LA NOUVELLE SONDE DE LIAISON — avant conclure()
remplace("def conclure(code):",
         '''def sonde_resolution_imports(k32, donnees):
    """LA SONDE DE L'ENTRÉE 214 — LA LIAISON VÉCUE : la sixième mort
    [OFT-QWORD] était invisible à la sonde 205 (sa cartographie est
    DONT_RESOLVE : le drapeau SAUTE la résolution des imports). ICI :
    une copie chargée SANS DONT_RESOLVE — l'entrée de la copie
    neutralisée d'un seul octet ret (la fenêtre n'y est jamais
    lancée), les 37 slots RELUS : le VRAI chargeur doit y avoir posé
    LES ADRESSES DES FONCTIONS — plus AUCUNE valeur fichier."""
    lignes = []
    dossier = tempfile.mkdtemp(prefix="loupe-sonde-214-")
    chemin = os.path.join(dossier, "loupe-sonde.exe")
    try:
        image = bytearray(donnees)
        image[0x4E00] = 0xC3            # l'entrée de la COPIE devient
                                         # ret — l'original n'est JAMAIS
                                         # écrit (même loi que la 205)
        with open(chemin, "wb") as f:
            f.write(bytes(image))
        k32.SetLastError(0)
        base = k32.LoadLibraryExW(chemin, None, 0)    # SANS DONT_RESOLVE
        err = ctypes.get_last_error()
        if not base:
            lignes.append(f"[sonde-214] LA LIAISON : REFUS DU CHARGEUR — "
                          f"GetLastError {err} — la copie n'est pas même "
                          f"liée (le témoin le consigne, le labo recoupe)")
            return lignes
        try:
            non_resolus = 0
            for ft, n in ((0x3100, 10), (0x3158, 18), (0x31F0, 6),
                          (0x3228, 3)):
                for i in range(n):
                    brut = ctypes.string_at(base + ft + 8 * i, 8)
                    slot, = struct.unpack("<Q", bytes(brut))
                    if slot == 0 or slot < 0x10000:   # NULL ou la valeur
                        non_resolus += 1              # fichier (un RVA)
            if non_resolus:
                lignes.append(f"[sonde-214] LA LIAISON : {non_resolus} "
                              f"slots NON résolus (NULL ou valeur fichier) "
                              f"— LE CHARGEUR N'A PAS POSÉ LES FONCTIONS "
                              f"([OFT-QWORD] ?) — la pièce mourrait à la "
                              f"vitrine : LE DÉFAUT EST NOMMÉ AU TÉMOIN")
            else:
                lignes.append("[sonde-214] LA LIAISON : les 37 slots "
                              "RELUS CHARGÉS — plus AUCUNE valeur fichier : "
                              "le VRAI chargeur a posé LES ADRESSES DES "
                              "FONCTIONS aux slots du plan — LA PIÈCE EST "
                              "LIÉE, la vitrine est LIBRE DE VIVRE")
        finally:
            k32.FreeLibrary(base)
        return lignes
    finally:
        try:
            os.remove(chemin)
            os.rmdir(dossier)
        except OSError:
            pass


def conclure(code):''')

# 1l. l'appel de la sonde de liaison — aux DEUX points de la cascade
remplace("""        for ligne in sonde_entree_205(k32, donnees):
            consigne(ligne)""",
         """        for ligne in sonde_entree_205(k32, donnees):
            consigne(ligne)
        for ligne in sonde_resolution_imports(k32, donnees):
            consigne(ligne)""")
remplace("""    for ligne in sonde_entree_205(k32, donnees):
        consigne(ligne)""",
         """    for ligne in sonde_entree_205(k32, donnees):
        consigne(ligne)
    for ligne in sonde_resolution_imports(k32, donnees):
        consigne(ligne)""")

open(os.path.join(DST, "scenario-loupe.py"), "w", encoding="utf-8").write(sc)
py_compile.compile(os.path.join(DST, "scenario-loupe.py"), doraise=True)
print("scenario-loupe.py dev.10 : ÉCRIT et COMPILÉ")

# vérification des constantes par import sûr (le module ne court pas ici)
sys.path.insert(0, DST)
os.environ["SCENARIO_IMPORT_TEST"] = "1"
import importlib.util
spec = importlib.util.spec_from_file_location("sc_dev10",
                                              os.path.join(DST, "scenario-loupe.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
assert mod.SHA_EXE == SHA_V8, "SHA_EXE != dev.8"
assert mod.VERSION_R10 == 0x00010008, "VERSION_R10 != dev.8"
assert mod.VERSION_TXT == "0.1.0-dev.8", "VERSION_TXT != dev.8"
print(f"  SHA_EXE {mod.SHA_EXE[:16]}… · VERSION_R10 {mod.VERSION_R10:#x} · "
      f"VERSION_TXT {mod.VERSION_TXT}")

# ═════════════════════════════════════════════════════════════════════
# 2. LE TÉMOIN VITRINE
# ═════════════════════════════════════════════════════════════════════
bat = open(os.path.join(SRC, "temoin-vitrine.bat"), encoding="utf-8").read()
bat = bat.replace("LE TEMOIN VITRINE DU KIT LOUPE (Entree 210)",
                  "LE TEMOIN VITRINE DU KIT LOUPE (Entree 214)")
bat = bat.replace(
    "echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.7 ^(kit dev.8, Entree 210^) ===",
    "echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.8 ^(kit dev.10, Entree 214^) ===")
assert "dev.10" in bat and "0.1.0-dev.8" in bat
open(os.path.join(DST, "temoin-vitrine.bat"), "w", encoding="utf-8").write(bat)
print("temoin-vitrine.bat dev.10 : ÉCRIT")

print("\n(le LISEZMOI-KIT-LOUPE.md est écrit par le script suivant)")
