#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le générateur du KIT dev.12 — la retouche [FREE-SANS-TYPE] de l'Entrée 216.

LE DIXIÈME RUN (kit dev.11) : T0 → T7 TOUT VERT POUR LA TROISIÈME FOIS,
ET **LA VITRINE A VÉCU LA PREMIÈRE FOIS** (0 et 0, les deux fenêtres,
Alt+F4 chacune, aucun WER — après six morts, l'application née de
TRIADE a vécu chez son utilisateur) — MAIS le scénario n'était pas
ENTIER : la cascade 205 mourut à son PREMIER geste, et LA LIAISON ne
courut jamais. LA LIGNE D'ÉCHEC NOMMA LE DÉFAUT :

  [FREE-SANS-TYPE] — `k32.FreeLibrary(base)` (la leçon du run 9 :
  FreeLibrary AVANT la suppression) fut appelé SANS argtypes avec le
  HMODULE 64 bits rendu par `k32.LoadLibraryExW.restype = c_void_p`
  (posé au T0). Sans argtypes, ctypes convertit l'argument nu en
  C int 32 bits : le handle 0x7FF9… ne tient pas — ctypes lève
  `ArgumentError('argument 1: OverflowError: int too long to
  convert')` (le mécanisme recoupé : un int non typé transmis à une
  fonction est rogné/converti sur 32 bits — au run 10, Windows a
  REFUSÉ la conversion au lieu de roger). ET l'ArgumentError n'est
  PAS un OSError : l'essai isolé (`except OSError`) ne tenait que
  pour une classe — la promesse « chaque essai dans son try : la
  cascade ne meurt jamais sur son propre geste » fut écrite trop
  étroite ; l'exception traversa la sonde, tua le scénario au sommet
  (`echec("EXCEPTION", …)`), et LA LIAISON — tout le sens de la
  sonde de l'Entrée 214 — ne courut jamais.

LA RETOUCHE (DU KIT SEUL — la pièce n'a pas bougé d'un octet, sha256
054de960…, la carte demeure génération 16) :
  1. `k32.FreeLibrary.argtypes = [ctypes.c_void_p]` + `restype` posés
     au T0, auprès des autres argtypes — le HMODULE passe en POINTEUR,
     PAR CONSTRUCTION, aux DEUX sondes (205 et 214) d'un seul geste ;
  2. l'essai de la cascade 205 élargi : `except OSError` →
     `except Exception` — la promesse vaut pour TOUTE classe
     d'exception (l'essai meurt, JAMAIS la cascade) ;
  3. la sonde de liaison blindée de même : la lecture des 37 slots et
     le FreeLibrary vivent dans leur try, AUCUNE exception de sonde
     ne tue le run — le témoin consigne, le verdict se rend
     POST-MORTEM au labo ;
  4. le littéral périmé 13a869a3… (dev.6) du docstring T2 porté à
     054de960… (dev.8) — nommé au passage, l'assertion runtime est
     dynamique depuis l'Entrée 213.

Entrées : les QUATRE pièces du kit dev.11 (loupe/terrain/, le dépôt —
== le kit couru au run 10, recoupé md5 pièce à pièce) + loupe.exe
(sha256 054de960…) ; sorties : build-dev12/ + kit-loupe.zip.
"""
import hashlib
import os
import py_compile
import shutil
import sys
import zipfile

SRC = "/home/z/my-project/triade/loupe/terrain"   # le kit dev.11 du dépôt
PIECE = "/home/z/my-project/triade/loupe/loupe.exe"
DST = "/home/z/my-project/build-dev12"

SHA_V8 = "054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69"
MD5_SC11 = "f2766d6c964cf147a893574f5537c190"     # le scénario dev.11 couru
MD5_BAT11 = "2236af792a9bc85387aba8c016f0cc27"    # le bat dev.11 couru
MD5_LIV11 = "e9b8c6ab7fcc6aff04930ef30a0db7ba"    # le LISEZMOI dev.11 couru

os.makedirs(DST, exist_ok=True)


def md5(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


# ═════════════════════════════════════════════════════════════════════
# 0. LA PIÈCE — dev.8 INTACTE (aucune retouche de pièce)
# ═════════════════════════════════════════════════════════════════════
piece = open(PIECE, "rb").read()
assert len(piece) == 127488, f"taille inattendue {len(piece)}"
assert hashlib.sha256(piece).hexdigest() == SHA_V8, "la pièce n'est pas dev.8 !"
open(os.path.join(DST, "loupe.exe"), "wb").write(piece)
print(f"[0] la pièce dev.8 INTACTE : {len(piece)} o, sha256 {SHA_V8[:16]}…")

# ═════════════════════════════════════════════════════════════════════
# 1. LE SCÉNARIO — la retouche [FREE-SANS-TYPE]
# ═════════════════════════════════════════════════════════════════════
assert md5(os.path.join(SRC, "scenario-loupe.py")) == MD5_SC11, \
    "la source n'est pas le scénario dev.11 couru au run 10"
sc = open(os.path.join(SRC, "scenario-loupe.py"), encoding="utf-8").read()
print(f"[1] le scénario dev.11 lu : {len(sc)} octets, md5 {MD5_SC11[:8]}…")


def remplace(ancien, nouveau, combien=1):
    global sc
    n = sc.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:70]!r}"
    sc = sc.replace(ancien, nouveau)


# 1a. l'en-tête — la vague dev.12
remplace("NATURE (kit dev.11, l'Entrée 215).",
         "NATURE (kit dev.12, l'Entrée 216).")
remplace("le présent scénario dev.11 MARCHE LUI-MÊME",
         "le présent scénario dev.12 MARCHE LUI-MÊME")

# 1b. LA RETOUCHE ELLE-MÊME — l'argtypes du FreeLibrary posé au T0
remplace('''    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                   wt.DWORD, ctypes.POINTER(wt.DWORD)]''',
         '''    k32.LoadLibraryExW.restype = ctypes.c_void_p
    k32.LoadLibraryExW.argtypes = [wt.LPCWSTR, ctypes.c_void_p, wt.DWORD]
    k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                   wt.DWORD, ctypes.POINTER(wt.DWORD)]
    k32.FreeLibrary.argtypes = [ctypes.c_void_p]
    # ^ LA LEÇON DU RUN 10 [FREE-SANS-TYPE, l'Entrée 216] : le HMODULE
    #   64 bits (le restype c_void_p ci-dessus) ne passe PAS la
    #   conversion C int 32 bits de ctypes — ArgumentError('argument
    #   1: OverflowError: int too long to convert') : la cascade 205
    #   mourut à son PREMIER geste au dixième run ; le POINTEUR passe,
    #   par construction — aux DEUX sondes (205 et 214) d'un seul
    #   geste, l'argtypes étant posé ICI avant toute sonde.
    k32.FreeLibrary.restype = wt.BOOL''')

# 1c. la cascade 205 — la promesse élargie à TOUTE classe d'exception
remplace('''                if base:
                    k32.FreeLibrary(base)   # LA LEÇON DU RUN 9 : un module
                                            # CHARGÉ ne se supprime pas —
                                            # le PermissionError(13) du
                                            # neuvième run ne passera plus
                os.remove(chemin_sonde)
            except OSError as exc:''',
         '''                if base:
                    k32.FreeLibrary(base)   # LA LEÇON DU RUN 9 : un module
                                            # CHARGÉ ne se supprime pas —
                                            # le PermissionError(13) du
                                            # neuvième run ne passera plus ;
                                            # LA LEÇON DU RUN 10
                                            # [FREE-SANS-TYPE] : le HMODULE
                                            # passe désormais en POINTEUR
                                            # (argtypes posé au T0) —
                                            # l'ArgumentError du dixième
                                            # run ne passera plus
                os.remove(chemin_sonde)
            except Exception as exc:      # LA LEÇON DU RUN 10 : une
                                          # exception de sonde n'est pas
                                          # forcément un OSError
                                          # (l'ArgumentError n'en est pas)
                                          # — la promesse « chaque essai
                                          # dans son try » vaut pour
                                          # TOUTE classe : l'essai meurt,
                                          # JAMAIS la cascade''')

# 1d. la sonde de liaison blindée — AUCUNE exception de sonde ne tue le run
remplace('''        try:
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
        return lignes''',
         '''        try:
            try:
                non_resolus = 0
                for ft, n in ((0x3100, 10), (0x3158, 18), (0x31F0, 6),
                              (0x3228, 3)):
                    for i in range(n):
                        brut = ctypes.string_at(base + ft + 8 * i, 8)
                        slot, = struct.unpack("<Q", bytes(brut))
                        if slot == 0 or slot < 0x10000:   # NULL ou valeur
                            non_resolus += 1              # fichier (un RVA)
                if non_resolus:
                    lignes.append(f"[sonde-214] LA LIAISON : {non_resolus} "
                                  f"slots NON résolus (NULL ou valeur fichier) "
                                  f"— LE CHARGEUR N'A PAS POSÉ LES FONCTIONS "
                                  f"([OFT-QWORD] ?) — la pièce mourrait à la "
                                  f"vitrine : LE DÉFAUT EST NOMMÉ AU TÉMOIN")
                else:
                    lignes.append("[sonde-214] LA LIAISON : les 37 slots "
                                  "RELUS CHARGÉS — plus AUCUNE valeur "
                                  "fichier : le VRAI chargeur a posé LES "
                                  "ADRESSES DES FONCTIONS aux slots du "
                                  "plan — LA PIÈCE EST LIÉE, la vitrine "
                                  "est LIBRE DE VIVRE")
            finally:
                k32.FreeLibrary(base)   # [FREE-SANS-TYPE] : le HMODULE
                                        # passe en POINTEUR (argtypes au
                                        # T0) — la leçon du run 10,
                                        # aux DEUX sondes d'un seul geste
        except Exception as exc:        # LA LEÇON DU RUN 10 : AUCUNE
                                        # exception de la sonde ne tue
                                        # le run — la sonde meurt, le
                                        # témoin consigne, le verdict
                                        # se rend POST-MORTEM au labo
            lignes.append(f"[sonde-214] LA LIAISON : ÉCHEC DE LA SONDE — "
                          f"{exc!r} — la sonde meurt, PAS le run : le "
                          f"témoin le consigne, le labo recoupe sur pièces")
        return lignes''')

# 1e. le docstring de tête — le récit du run 10 porté à la pièce
remplace('''              la pièce n'a pas bougé d'un octet, la carte demeure
              génération 16, la vague dev.10 archivée versionnée) ;
  le présent script —''',
         '''              la pièce n'a pas bougé d'un octet, la carte demeure
              génération 16, la vague dev.10 archivée versionnée) ;
              (INCHANGÉ DEPUIS L'ENTRÉE 214 — la vague dev.12 est encore
              UNE RETOUCHE DU KIT SEUL : le DIXIÈME RUN VÉCUT LA
              VITRINE LA PREMIÈRE FOIS [0 et 0, les deux fenêtres,
              Alt+F4 chacune, aucun WER — après six morts, la vitrine
              A VÉCU] et tint T0 → T7 TOUT VERT POUR LA TROISIÈME
              FOIS, mais la cascade 205 mourut à son PREMIER geste :
              [FREE-SANS-TYPE] — k32.FreeLibrary appelé SANS argtypes
              avec le HMODULE 64 bits du restype c_void_p, ctypes
              convertissant l'argument nu en int 32 bits :
              ArgumentError('argument 1: OverflowError: int too long
              to convert') — et l'ArgumentError n'est PAS un OSError :
              l'essai isolé ne tenait que pour OSError, LA LIAISON ne
              courut jamais ; LA RETOUCHE : FreeLibrary.argtypes =
              [c_void_p] posé au T0 [le POINTEUR passe, aux DEUX
              sondes d'un seul geste], l'essai élargi à TOUTE classe
              d'exception, la sonde de liaison blindée de même ; la
              pièce n'a pas bougé d'un octet, la carte demeure
              génération 16, la vague dev.11 archivée versionnée) ;
  le présent script —''')

# 1f. la section 205 de tête — la leçon du run 10 portée
remplace('''plus. (Et la cascade 205 réparée de son propre nettoyage : le module
chargé se LIBÈRE avant sa suppression — le PermissionError du run 9.)''',
         '''plus. (Et la cascade 205 réparée de son propre nettoyage : le module
chargé se LIBÈRE avant sa suppression — le PermissionError du run 9 —
PUIS le run 10 nomma [FREE-SANS-TYPE] : le FreeLibrary SANS argtypes
ne passait pas le HMODULE 64 bits [ArgumentError, int too long to
convert] ; l'argtypes c_void_p est posé au T0 et l'essai isolé vaut
pour TOUTE classe d'exception : la cascade ne meurt JAMAIS sur son
propre geste, quelle que soit la classe.)''')

# 1g. le docstring T2 — le littéral périmé dev.6 porté à dev.8 (nommé)
remplace("loupe.exe LUI-MÊME rend son sha256_asserté\n                   13a869a3b31b41d6….",
         "loupe.exe LUI-MÊME rend son sha256_asserté\n                   054de960c31425d0….")

# 1h. le tableau du run — l'essai pour TOUTE classe + LA LIAISON au tableau
remplace('''  S0 LA SONDE      LA CASCADE DIAGNOSTIQUE DE L'ENTRÉE 205 : les axes
     (205)         de dev.2 reconstitués UN À UN sur des copies %TEMP%
                   (le trou de page, le BSS, le sous-système, la
                   géométrie entière) — le VRAI chargeur NOMME l'axe
                   fautif ; loupe.exe n'est jamais écrit.''',
         '''  S0 LA SONDE      LA CASCADE DIAGNOSTIQUE DE L'ENTRÉE 205 : les axes
     (205)         de dev.2 reconstitués UN À UN sur des copies %TEMP%
                   (le trou de page, le BSS, le sous-système, la
                   géométrie entière) — le VRAI chargeur NOMME l'axe
                   fautif ; chaque essai vit dans son try POUR TOUTE
                   classe d'exception (la leçon du run 10 :
                   [FREE-SANS-TYPE] — l'ArgumentError n'est pas un
                   OSError) ; loupe.exe n'est jamais écrit.
  LA LIAISON       LA SONDE DE L'ENTRÉE 214 : une copie chargée SANS
     (214)         DONT_RESOLVE, l'entrée neutralisée de SIX octets
                   (mov eax, 1 ; ret — [RET-NU, l'Entrée 215]) — les
                   37 slots RELUS : le VRAI chargeur doit y avoir posé
                   LES ADRESSES DES FONCTIONS ; JAMAIS courue à ce
                   jour (le run 10 mourut avant, à la cascade 205) ;
                   aucune exception de sonde ne tue le run.''')

# 1i. vérification des invariants du scénario
assert sc.count("except OSError as exc:") == 0, "un except OSError demeure !"
# les DEUX sondes élargies + le garde du sommet (préexistant)
assert sc.count("except Exception as exc:") == 3, "les DEUX essais élargis + le sommet"
assert sc.count("k32.FreeLibrary.argtypes") == 1, "l'argtypes du FreeLibrary"
assert sc.count("kit dev.11") == 0, "le littéral kit dev.11 demeure (l'histoire dit « la vague dev.11 »)"
assert sc.count("kit dev.12") == 1 and sc.count("dev.12") >= 2
assert f'SHA_EXE = ("{SHA_V8}")' in sc, "SHA_EXE perdu"
assert 'VERSION_R10 = 0x00010008' in sc, "VERSION_R10 perdu"
assert 'génération 16' in sc, "la carte perdue"
assert sc.count("13a869a3") == 0, "le littéral périmé dev.6 demeure"
chemin_sc = os.path.join(DST, "scenario-loupe.py")
open(chemin_sc, "w", encoding="utf-8", newline="\n").write(sc)
py_compile.compile(chemin_sc, doraise=True)
md5_apres = hashlib.md5(open(chemin_sc, "rb").read()).hexdigest()
print(f"[1] le scénario dev.12 NÉ : {len(sc)} octets, md5 {md5_apres[:8]}… "
      f"— py_compile VERT")

# ═════════════════════════════════════════════════════════════════════
# 2. LE TÉMOIN VITRINE — les littéraux portés à dev.12
# ═════════════════════════════════════════════════════════════════════
assert md5(os.path.join(SRC, "temoin-vitrine.bat")) == MD5_BAT11, \
    "la source n'est pas le bat dev.11 couru au run 10"
bat = open(os.path.join(SRC, "temoin-vitrine.bat"), encoding="latin-1").read()
assert bat.count("kit dev.11, Entree 215") == 1
assert bat.count("Entree 215") == 2
bat = bat.replace("rem temoin-vitrine.bat - LE TEMOIN VITRINE DU KIT LOUPE (Entree 215)",
                  "rem temoin-vitrine.bat - LE TEMOIN VITRINE DU KIT LOUPE (Entree 216)")
bat = bat.replace("echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.8 ^(kit dev.11, Entree 215^) ===",
                  "echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.8 ^(kit dev.12, Entree 216^) ===")
assert bat.count("kit dev.12, Entree 216") == 1
assert bat.count("dev.11") == 0
open(os.path.join(DST, "temoin-vitrine.bat"), "w", encoding="latin-1", newline="\n").write(bat)
print(f"[2] le témoin vitrine dev.12 : {len(bat)} octets — les deux littéraux portés")

# ═════════════════════════════════════════════════════════════════════
# 3. LE LISEZMOI — l'histoire dev.12 (le kit dev.11 pour base)
# ═════════════════════════════════════════════════════════════════════
assert md5(os.path.join(SRC, "LISEZMOI-KIT-LOUPE.md")) == MD5_LIV11, \
    "la source n'est pas le LISEZMOI dev.11 couru au run 10"
lz = open(os.path.join(SRC, "LISEZMOI-KIT-LOUPE.md"), encoding="utf-8").read()


def lz_remplace(ancien, nouveau, combien=1):
    global lz
    n = lz.count(ancien)
    assert n == combien, f"ancre LISEZMOI {n}x (attendu {combien}) : {ancien[:70]!r}"
    lz = lz.replace(ancien, nouveau)


# 3a. les littéraux de version
lz_remplace("le build est NÉ et a vécu NEUF RUNS\n> terrain.",
            "le build est NÉ et a vécu DIX RUNS\n> terrain.")
lz_remplace("— Entrées 202 → … → 211 → 213 →\n> **214**)",
            "— Entrées 202 → … → 211 → 213 → 214 →\n> 215 → **216**)")
n_kit11 = lz.count("loupe-kit-11/")
assert n_kit11 >= 2, f"le dossier loupe-kit-11/ n'apparaît que {n_kit11}x"
lz = lz.replace("loupe-kit-11/", "loupe-kit-12/")
lz_remplace("`loupe-kit-11b/` si besoin", "`loupe-kit-12b/` si besoin")
lz_remplace("celui de dev.1 à dev.10 par exemple", "celui de dev.1 à dev.11 par exemple")
lz_remplace("LE SCÉNARIO dev.11", "LE SCÉNARIO dev.12")
lz_remplace("LE TÉMOIN VITRINE dev.11", "LE TÉMOIN VITRINE dev.12")

# 3b. LE FIL NARRATIF DU DIXIÈME RUN — inséré après le récit [RET-NU]
ancre = "chaque défaut a reçu sa retouche : **celui-ci AVANT le run, pas\n> après**.)\n\n## 1. Ce que ce kit contient"
assert lz.count(ancre) == 1, "ancre [RET-NU] introuvable"
lz = lz.replace(ancre,
    "chaque défaut a reçu sa retouche : **celui-ci AVANT le run, pas\n"
    "> après**.)\n\n"
    "> **LE DIXIÈME RUN : LA VITRINE A VÉCU — ET LE SEPTIÈME DÉFAUT EST\n"
    "> CELUI DU KIT, NOMMÉ PAR LA LIGNE D'ÉCHEC** (l'Entrée 216, le\n"
    "> recoup sur pièces : T0 → T7 TOUT VERT POUR LA TROISIÈME FOIS,\n"
    "> ET **LA VITRINE VIVANTE LA PREMIÈRE FOIS — 0 et 0**, les deux\n"
    "> fenêtres vécues, Alt+F4 chacune, aucun WER, le [4/4] ne portant\n"
    "> que de vieux LiveKernelEvent — après six morts, **L'APPLICATION\n"
    "> NÉE DE TRIADE A VÉCU CHEZ SON UTILISATEUR** ; MAIS le scénario\n"
    "> n'était pas ENTIER : la cascade 205 mourut à son PREMIER geste\n"
    "> — **[FREE-SANS-TYPE]** : `k32.FreeLibrary(base)` appelé SANS\n"
    "> argtypes avec le HMODULE 64 bits du `restype c_void_p` — ctypes\n"
    "> convertit l'argument nu en int 32 bits :\n"
    "> `ArgumentError('argument 1: OverflowError: int too long to\n"
    "> convert')` — et l'ArgumentError n'est PAS un OSError : l'essai\n"
    "> isolé ne tenait que pour OSError, la cascade mourut, **LA\n"
    "> LIAISON ne courut jamais** ; LA PIÈCE EST ACQUITTÉE DE TOUTE\n"
    "> CHARGE [T7 la relut inchangée ; la vitrine vivante prouve la\n"
    "> liaison MIEUX que toute sonde — la fenêtre n'eût pas vécu d'un\n"
    "> import non résolu] ; LA RETOUCHE dev.12, DU KIT SEUL :\n"
    "> `FreeLibrary.argtypes = [c_void_p]` posé au T0 [le POINTEUR\n"
    "> passe, aux DEUX sondes d'un seul geste], l'essai élargi à TOUTE\n"
    "> classe d'exception [la cascade ne meurt JAMAIS sur son propre\n"
    "> geste, quelle que soit la classe], la sonde de liaison blindée\n"
    "> de même [aucune exception de sonde ne tue le run] ; la pièce\n"
    "> n'a pas bougé d'un octet — sha256 054de960…, la carte demeure\n"
    "> génération 16 ; la balise attend le vert ENTIER : le scénario\n"
    "> T0 → S0 → LA LIAISON ET la vitrine vivante.)\n\n"
    "## 1. Ce que ce kit contient")

# 3c. le geste — les cascades se jouent toutes seules (le récit porté)
lz_remplace(
    "la 205 réparée ET la liaison de l'Entrée 214 RETOUCHÉE dev.11 : laissez-les finir, le\n   témoin part au coffre QUEL QUE SOIT le verdict.",
    "la 205 réparée ET la liaison RETOUCHÉE dev.12 — [FREE-SANS-TYPE], la\n   leçon du run 10 : le FreeLibrary en POINTEUR, l'essai isolé pour\n   TOUTE classe — laissez-les finir, le témoin part au coffre QUEL\n   QUE SOIT le verdict.")

# 3d. la vitrine du geste — 0 et 0 attendus (le run 10 l'a déjà vécue)
lz_remplace(
    "— **0 et 0\n   sont attendus : la vitrine dev.8 est née pour VIVRE** (six morts\n   déjà —",
    "— **0 et 0\n   sont attendus : la vitrine dev.8 A DÉJÀ VÉCU AU DIXIÈME RUN** (0 et\n   0, la première fois après six morts — le onzième run la reverra\n   vivre, la dette du kit n'étant que le scénario ENTIER ; la pièce\n   est acquittée : le défaut [FREE-SANS-TYPE] fut celui du KIT —")

# 3e. la section 3 — la leçon du run 10 à la cascade 205
lz_remplace(
    "LIBÉRÉ avant sa suppression — la cascade ne meurt JAMAIS sur son\n  propre geste ;",
    "LIBÉRÉ avant sa suppression — la cascade ne meurt JAMAIS sur son\n  propre geste, l'essai isolé valant pour TOUTE classe d'exception\n  (la leçon du run 10 : [FREE-SANS-TYPE] — l'ArgumentError n'est\n  pas un OSError) ;")

# 3f. la section 5 — le fait du run 10 avant le critère
lz_remplace(
    "constats croisés contre le dépôt, les empreintes recalculées. **ET SI\nLE VERT TIENT",
    "constats croisés contre le dépôt, les empreintes recalculées — **LE\nDIXIÈME RUN A DÉJÀ VÉCU LA VITRINE (0 et 0, la première fois :\nl'application née de TRIADE a vécu chez son utilisateur) ; LA DETTE\nRESTANTE EST LE SCÉNARIO ENTIER : S0 ET LA LIAISON, jamais courus à\nce jour**. ET SI LE VERT TIENT")

# 3g. les invariants du LISEZMOI
assert lz.count("loupe-kit-12/") >= 2, "le dossier du kit"
assert lz.count("[FREE-SANS-TYPE]") >= 3, "le défaut raconté"
assert lz.count("A DÉJÀ VÉCU") >= 1, "le fait du run 10"
# les seuls « dev.11 » légitimes : l'histoire (« la vague dev.11 », la
# parenthèse 3a du geste) — tout autre est un littéral résiduel
reste = lz.replace("la vague dev.11", "").replace("à dev.11 par exemple", "")
assert "dev.11" not in reste, "littéral dev.11 résiduel inattendu"
open(os.path.join(DST, "LISEZMOI-KIT-LOUPE.md"), "w", encoding="utf-8", newline="\n").write(lz)
print(f"[3] le LISEZMOI dev.12 : {len(lz)} octets — loupe-kit-12, [FREE-SANS-TYPE] raconté")

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
    assert sorted(z.namelist()) == sorted(QUATRE), "le zip ne porte pas les QUATRE pièces"
for nom in QUATRE:
    a = open(os.path.join(DST, nom), "rb").read()
    b = open(os.path.join(extraction, nom), "rb").read()
    assert a == b, f"l'extraction diffère : {nom}"
shutil.rmtree(extraction)

zip_bytes = open(zip_ch, "rb").read()
print(f"[4] kit-loupe.zip : {len(zip_bytes)} o, md5 "
      f"{hashlib.md5(zip_bytes).hexdigest()}… — extraction VIERGE, "
      f"les QUATRE pièces du contrat")
print("\nLA VAGUE dev.12 EST NÉE : build-dev12/ + kit-loupe.zip")
print("la pièce dev.8 INTACTE ; le FreeLibrary en POINTEUR ; l'essai pour TOUTE classe")
