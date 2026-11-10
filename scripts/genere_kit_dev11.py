#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le générateur du KIT dev.11 — la retouche [RET-NU] de l'Entrée 215.

LA VAGUE dev.10 ne courut JAMAIS : le kit fut déposé (Entrée 214), le
run attendait — et l'audit de reprise de la session suivante nomma UN
DÉFAUT À L'OCTET PRÈS DANS LE KIT LUI-MÊME, avant le geste du terrain :

  [RET-NU] — la sonde de liaison neutralisait l'entrée de sa copie
  d'UN SEUL OCTET ret (`image[0x4E00] = 0xC3`). Or SANS DONT_RESOLVE,
  le VRAI chargeur appelle l'entrée en sémantique DllMain (DLL_PROCESS_
  ATTACH) ET LIT SON RETOUR : « If the return value is FALSE when
  DllMain is called because the process uses the LoadLibrary function,
  LoadLibrary returns NULL » (Microsoft Learn). Un ret NU rend AL tel
  qu'il était à l'appel — l'octet de poids faible de l'adresse
  d'entrée (RVA 0x5C00, base 64 Kio-alignée) étant 0x00, le verdict le
  plus probable est FAUX : LE CHARGEUR AURAIT CROIT L'INITIALISATION
  ÉCHOUÉE → LoadLibraryExW rend NULL → la sonde eût consigné « REFUS
  DU CHARGEUR » DE FAUSSE CAUSE — ET LA RELECTURE DES 37 SLOTS, TOUT
  LE SENS DE LA LIAISON, EÛT ÉTÉ PERDUE AU RUN DE SCELLEMENT.

LA RETOUCHE : SIX OCTETS `mov eax, 1 ; ret` (B8 01 00 00 00 C3) AU
MÊME OFFSET — le verdict ATTACH VRAI PAR CONSTRUCTION, le DETACH
indifférent (le retour n'est lu qu'à l'ATTACH), la fenêtre toujours
jamais lancée. LA PIÈCE dev.8 N'A PAS BOUGÉ D'UN OCTET (sha256
054de960…, la carte demeure génération 16) — c'est une retouche DU
KIT SEUL : la vague dev.10 archivée versionnée, la vague dev.11 à la
racine du coffre.

Entrées du générateur : les quatre pièces du kit dev.10 (rapatriées
du coffre, recoupées) ; sorties : build-dev11/ + kit-loupe.zip.
"""
import hashlib
import os
import py_compile
import shutil
import sys
import zipfile

SRC = "/home/z/my-project/scripts"          # les pièces dev.10 recoupées
DST = "/home/z/my-project/build-dev11"

SHA_V8 = "054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69"
NEUTR = 'b"\\xb8\\x01\\x00\\x00\\x00\\xc3"'   # mov eax, 1 ; ret

os.makedirs(DST, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════
# 0. LA PIÈCE — dev.8 INTACTE (aucune retouche de pièce)
# ═════════════════════════════════════════════════════════════════════
piece = open(os.path.join(SRC, "loupe-kit10.exe"), "rb").read()
assert len(piece) == 127488, f"taille inattendue {len(piece)}"
assert hashlib.sha256(piece).hexdigest() == SHA_V8, "la pièce n'est pas dev.8 !"
open(os.path.join(DST, "loupe.exe"), "wb").write(piece)
print(f"[0] la pièce dev.8 INTACTE : {len(piece)} o, sha256 {SHA_V8[:16]}…")

# ═════════════════════════════════════════════════════════════════════
# 1. LE SCÉNARIO — la retouche [RET-NU]
# ═════════════════════════════════════════════════════════════════════
sc = open(os.path.join(SRC, "kit10-scenario-loupe.py"), encoding="utf-8").read()
md5_avant = hashlib.md5(sc.encode()).hexdigest()
print(f"[1] le scénario dev.10 lu : {len(sc)} octets, md5 {md5_avant[:8]}…")

def remplace(ancien, nouveau, combien=1):
    global sc
    n = sc.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:70]!r}"
    sc = sc.replace(ancien, nouveau)

# 1a. l'en-tête
remplace("NATURE (kit dev.10, l'Entrée 214).",
         "NATURE (kit dev.11, l'Entrée 215).")

# 1b. le kit dev.10 → dev.11 (la leçon institutionnalisée)
remplace("le présent scénario dev.10 MARCHE LUI-MÊME",
         "le présent scénario dev.11 MARCHE LUI-MÊME")

# 1c. LA RETOUCHE ELLE-MÊME — l'octet ret nu devient les six octets
remplace('''        image = bytearray(donnees)
        image[0x4E00] = 0xC3            # l'entrée de la COPIE devient
                                         # ret — l'original n'est JAMAIS
                                         # écrit (même loi que la 205)''',
         f'''        image = bytearray(donnees)
        image[0x4E00:0x4E06] = ({NEUTR}
            )                             # SIX OCTETS mov eax, 1 ; ret —
                                         # LA RETOUCHE [RET-NU, Entrée
                                         # 215] : sans DONT_RESOLVE le
                                         # VRAI chargeur appelle
                                         # l'entrée en sémantique DllMain
                                         # ET LIT SON RETOUR — un ret nu
                                         # eût rendu AL tel qu'il était
                                         # à l'appel (l'octet de poids
                                         # faible de l'adresse d'entrée
                                         # = 0x00) : REFUS FAUX DU
                                         # CHARGEUR, les 37 slots jamais
                                         # relus, la liaison PERDUE ;
                                         # mov eax, 1 rend le verdict
                                         # ATTACH VRAI PAR CONSTRUCTION
                                         # (le DETACH n'est pas lu) —
                                         # l'original n'est JAMAIS
                                         # écrit (même loi que la 205)''')

# 1d. le docstring de la sonde — l'histoire portée
remplace('''    une copie chargée SANS DONT_RESOLVE — l'entrée de la copie
    neutralisée d'un seul octet ret (la fenêtre n'y est jamais
    lancée), les 37 slots RELUS : le VRAI chargeur doit y avoir posé
    LES ADRESSES DES FONCTIONS — plus AUCUNE valeur fichier.''',
         '''    une copie chargée SANS DONT_RESOLVE — l'entrée de la copie
    neutralisée de SIX OCTETS (mov eax, 1 ; ret — [RET-NU, l'Entrée
    215] : le VRAI chargeur appelle l'entrée en sémantique DllMain et
    LIT SON RETOUR, le ret nu eût rendu un verdict FAUX ; la fenêtre
    n'y est jamais lancée), les 37 slots RELUS : le VRAI chargeur doit
    y avoir posé LES ADRESSES DES FONCTIONS — plus AUCUNE valeur
    fichier.''')

# 1e. le geste du docstring (la phrase « d'un seul octet ret »)
remplace('''214 COMPLÈTE LE TABLEAU : LA LIAISON VÉCUE — une copie chargée SANS
DONT_RESOLVE (l'entrée de la copie neutralisée d'un seul octet ret :
la fenêtre n'y est jamais lancée), les 37 slots RELUS — le VRAI''',
         '''214 COMPLÈTE LE TABLEAU : LA LIAISON VÉCUE — une copie chargée SANS
DONT_RESOLVE (l'entrée de la copie neutralisée de SIX octets, mov
eax, 1 ; ret : la fenêtre n'y est jamais lancée, et le verdict ATTACH
VRAI PAR CONSTRUCTION — [RET-NU] nommé avant le run, l'Entrée 215),
les 37 slots RELUS — le VRAI''')

# 1f. le refus de la sonde désormais SANS FAUSSE CAUSE POSSIBLE
remplace('''lignes.append(f"[sonde-214] LA LIAISON : REFUS DU CHARGEUR — "
                          f"GetLastError {err} — la copie n'est pas même "
                          f"liée (le témoin le consigne, le labo recoupe)")''',
         '''lignes.append(f"[sonde-214] LA LIAISON : REFUS DU CHARGEUR — "
                          f"GetLastError {err} — la copie n'est pas même "
                          f"liée (VRAI refus désormais : l'entrée rend "
                          f"VRAI par construction, un refus ici ne peut "
                          f"plus être [RET-NU] — le témoin le consigne, "
                          f"le labo recoupe)")''')

# 1g. l'histoire du kit — le bloc loupe.exe porte le récit dev.11
remplace('''              plus jamais], ET LA NOUVELLE SONDE DE LIAISON VIT LE
              VRAI CHARGEUR POSER LES FONCTIONS ; le qword version
              0x00010007 → 0x00010008) ;''',
         '''              plus jamais], ET LA NOUVELLE SONDE DE LIAISON VIT LE
              VRAI CHARGEUR POSER LES FONCTIONS ; le qword version
              0x00010007 → 0x00010008) ;
              (INCHANGÉ DEPUIS L'ENTRÉE 214 — la vague dev.11 est UNE
              RETOUCHE DU KIT SEUL : [RET-NU] NOMMÉ À L'OCTET PRÈS
              AVANT LE RUN, l'Entrée 215 — la sonde de liaison
              neutralisait l'entrée de sa copie d'un seul octet ret ;
              sans DONT_RESOLVE, le VRAI chargeur appelle l'entrée en
              sémantique DllMain ET LIT SON RETOUR : un ret nu rend
              AL tel qu'il fut à l'appel — l'octet de poids faible de
              l'adresse d'entrée étant 0x00, le chargeur eût cru
              l'initialisation ÉCHOUÉE : REFUS FAUX, LoadLibraryExW
              NULL, LES 37 SLOTS JAMAIS RELUS, LA LIAISON PERDUE AU
              RUN DE SCELLEMENT ; la retouche : SIX OCTETS mov eax, 1
              ; ret — le verdict ATTACH VRAI PAR CONSTRUCTION, le
              DETACH indifférent, la fenêtre toujours jamais lancée ;
              la pièce n'a pas bougé d'un octet, la carte demeure
              génération 16, la vague dev.10 archivée versionnée) ;''')

# 1h. vérification des invariants du scénario
assert sc.count('image[0x4E00] = 0xC3') == 0, "l'octet ret nu demeure !"
assert sc.count('image[0x4E00:0x4E06]') == 1
assert sc.count('kit dev.10') == 0, "littéral dev.10 résiduel"
assert sc.count('kit dev.11') >= 1 and sc.count('dev.11') >= 2
assert f'SHA_EXE = ("{SHA_V8}")' in sc, "SHA_EXE perdu"
assert 'VERSION_R10 = 0x00010008' in sc, "VERSION_R10 perdu"
assert 'génération 16' in sc, "la carte perdue"
chemin_sc = os.path.join(DST, "scenario-loupe.py")
open(chemin_sc, "w", encoding="utf-8", newline="\n").write(sc)
py_compile.compile(chemin_sc, doraise=True)
md5_apres = hashlib.md5(open(chemin_sc, "rb").read()).hexdigest()
print(f"[1] le scénario dev.11 NÉ : {len(sc)} octets, md5 {md5_apres[:8]}… "
      f"— py_compile VERT")

# ═════════════════════════════════════════════════════════════════════
# 2. LE TÉMOIN VITRINE — les littéraux portés à dev.11
# ═════════════════════════════════════════════════════════════════════
bat = open(os.path.join(SRC, "kit10-temoin-vitrine.bat"), encoding="latin-1").read()
assert bat.count("kit dev.10, Entree 214") == 1
assert bat.count("Entree 214") == 2
bat = bat.replace("rem temoin-vitrine.bat - LE TEMOIN VITRINE DU KIT LOUPE (Entree 214)",
                  "rem temoin-vitrine.bat - LE TEMOIN VITRINE DU KIT LOUPE (Entree 215)")
bat = bat.replace("echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.8 ^(kit dev.10, Entree 214^) ===",
                  "echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.8 ^(kit dev.11, Entree 215^) ===")
assert bat.count("kit dev.11, Entree 215") == 1
assert bat.count("dev.10") == 0
open(os.path.join(DST, "temoin-vitrine.bat"), "w", encoding="latin-1", newline="\n").write(bat)
print(f"[2] le témoin vitrine dev.11 : {len(bat)} octets — les deux littéraux portés")

# ═════════════════════════════════════════════════════════════════════
# 3. LE LISEZMOI — l'histoire dev.11 (le kit dev.10 pour base)
# ═════════════════════════════════════════════════════════════════════
lz = open(os.path.join(SRC, "kit10-LISEZMOI-KIT-LOUPE.md"), encoding="utf-8").read()

lz = lz.replace("loupe-kit-10/", "loupe-kit-11/")
lz = lz.replace("LE SCÉNARIO dev.10", "LE SCÉNARIO dev.11")
lz = lz.replace("LE TÉMOIN VITRINE dev.10", "LE TÉMOIN VITRINE dev.11")
lz = lz.replace("« loupe-kit-9b/ »", "« loupe-kit-11b/ »")
lz = lz.replace("celui de dev.1 à dev.9 par exemple", "celui de dev.1 à dev.10 par exemple")
lz = lz.replace("`loupe-kit-9/`", "`loupe-kit-11/`")
lz = lz.replace("`loupe-kit-10b/` si besoin", "`loupe-kit-11b/` si besoin")

# 3b. le fil narratif de tête — le récit de la liaison porte [RET-NU]
n1 = lz.count("l'entrée neutralisée d'un octet ret, les")
assert n1 == 1, f"ancre tête LISEZMOI {n1}x"
lz = lz.replace(
    "ET LA NOUVELLE SONDE DE LIAISON [une copie\n"
    "> chargée SANS DONT_RESOLVE, l'entrée neutralisée d'un octet ret, les\n",
    "ET LA NOUVELLE SONDE DE LIAISON [une copie\n"
    "> chargée SANS DONT_RESOLVE, l'entrée neutralisée de SIX OCTETS\n"
    "> mov eax, 1 ; ret — [RET-NU, l'Entrée 215] NOMMÉ AVANT LE RUN :\n"
    "> un ret nu eût rendu le verdict ATTACH FAUX (le chargeur appelle\n"
    "> l'entrée en sémantique DllMain ET LIT SON RETOUR : REFUS FAUX,\n"
    "> les 37 slots jamais relus, la liaison PERDUE), les\n")

# 3b'. le bloc du kit (section 1) — la même histoire pièce par pièce
n2 = lz.count("l'entrée\n\u2502                      neutralisée d'un octet ret")
assert n2 == 1, f"ancre kit LISEZMOI {n2}x"
lz = lz.replace(
    "LA NOUVELLE SONDE DE LIAISON [une\n"
    "\u2502                      copie chargée SANS DONT_RESOLVE, l'entrée\n"
    "\u2502                      neutralisée d'un octet ret, les 37 slots RELUS :",
    "LA NOUVELLE SONDE DE LIAISON [une\n"
    "\u2502                      copie chargée SANS DONT_RESOLVE, l'entrée\n"
    "\u2502                      neutralisée de SIX OCTETS mov eax, 1 ; ret\n"
    "\u2502                      — [RET-NU] NOMMÉ AVANT LE RUN, l'Entrée 215 :\n"
    "\u2502                      le verdict ATTACH VRAI PAR CONSTRUCTION\n"
    "\u2502                      (un ret nu eût rendu FAUX au chargeur qui\n"
    "\u2502                      LIT le retour DllMain — REFUS FAUX,\n"
    "\u2502                      liaison perdue), les 37 slots RELUS :")

# 3c. la phrase du geste (section 2) — l'entrée neutralisée d'un octet ret
n2 = lz.count("ET LES CASCADES DIAGNOSTIQUES se jouent toutes seules")
if n2 == 1:
    lz = lz.replace(
        "la 205 réparée ET la liaison de l'Entrée 214 :",
        "la 205 réparée ET la liaison de l'Entrée 214 RETOUCHÉE dev.11 :")
# 3d. la section 3 — la description de la liaison
lz = lz.replace(
    "une copie chargée SANS DONT_RESOLVE — l'entrée de la copie\n"
    "  neutralisée d'un seul octet ret (la fenêtre n'y est jamais\n"
    "  lancée) — LES 37 SLOTS RELUS",
    "une copie chargée SANS DONT_RESOLVE — l'entrée de la copie\n"
    "  neutralisée de SIX OCTETS (mov eax, 1 ; ret : le verdict ATTACH\n"
    "  VRAI PAR CONSTRUCTION, [RET-NU, l'Entrée 215] — un ret nu eût\n"
    "  rendu FAUX au chargeur qui LIT le retour DllMain, REFUS FAUX,\n"
    "  liaison perdue ; la fenêtre n'y est jamais lancée) — LES 37\n"
    "  SLOTS RELUS")

# 3e. le récit de tête — la DIXIÈME VAGUE ([RET-NU] avant le run)
ancre = "FONCTIONS — la pièce LIÉE, la vitrine LIBRE DE VIVRE].\n\n## 1. Ce que ce kit contient"
assert lz.count(ancre) == 1, "ancre tête manquante"
lz = lz.replace(
    ancre,
    "FONCTIONS — la pièce LIÉE, la vitrine LIBRE DE VIVRE].\n\n"
    "> **LA DIXIÈME VAGUE EST CELLE DE [RET-NU] NOMMÉ AVANT LE RUN**\n"
    "> (l'Entrée 215 : la vague dev.10 ne courut JAMAIS — l'audit de\n"
    "> reprise nomma le défaut À L'OCTET PRÈS dans le kit lui-même : la\n"
    "> sonde de liaison neutralisait l'entrée de sa copie d'un seul\n"
    "> octet `ret` — or sans DONT_RESOLVE, le VRAI chargeur appelle\n"
    "> l'entrée en sémantique DllMain **ET LIT SON RETOUR** : « If the\n"
    "> return value is FALSE when DllMain is called because the\n"
    "> process uses the LoadLibrary function, LoadLibrary returns\n"
    "> NULL » (Microsoft Learn) — un ret nu rend AL tel qu'il fut à\n"
    "> l'appel, et l'octet de poids faible de l'adresse d'entrée (RVA\n"
    "> 0x5C00, base 64 Kio-alignée) est 0x00 : le chargeur eût cru\n"
    "> l'initialisation ÉCHOUÉE → LoadLibraryExW NULL → « REFUS DU\n"
    "> CHARGEUR » DE FAUSSE CAUSE et les 37 slots jamais relus,\n"
    "> **LA LIAISON PERDUE AU RUN DE SCELLEMENT**. LA RETOUCHE : SIX\n"
    "> OCTETS `mov eax, 1 ; ret` (B8 01 00 00 00 C3) au même offset —\n"
    "> le verdict ATTACH VRAI PAR CONSTRUCTION, le DETACH indifférent\n"
    "> (son retour n'est jamais lu) ; **la pièce dev.8 INTACTE**\n"
    "> (sha256 054de960… inchangé, la carte demeure génération 16), la\n"
    "> vague dev.10 archivée versionnée — chaque défaut a été nommé,\n"
    "> chaque défaut a reçu sa retouche : **celui-ci AVANT le run, pas\n"
    "> après**.)\n\n## 1. Ce que ce kit contient")
lz = lz.replace("Entrées 202 → … → 211 → 213 → **214**",
               "Entrées 202 → … → 211 → 213 → 214 → **215**")

open(os.path.join(DST, "LISEZMOI-KIT-LOUPE.md"), "w", encoding="utf-8", newline="\n").write(lz)
print(f"[3] le LISEZMOI dev.11 : {len(lz)} octets — loupe-kit-11, [RET-NU] raconté")

# ═════════════════════════════════════════════════════════════════════
# 4. LE ZIP + le dossier visible — les QUATRE pièces du contrat
# ═════════════════════════════════════════════════════════════════════
QUATRE = ["loupe.exe", "scenario-loupe.py", "temoin-vitrine.bat",
          "LISEZMOI-KIT-LOUPE.md"]
zip_ch = os.path.join(DST, "kit-loupe.zip")
if os.path.exists(zip_ch):
    os.remove(zip_ch)
with zipfile.ZipFile(zip_ch, "w", zipfile.ZIP_DEFLATED) as z:
    for nom in QUATRE:
        z.write(os.path.join(DST, nom), nom)

# l'extraction vierge (le recoup du kit : le zip rend les QUATRE,
# chaque empreinte == l'originale)
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
      f"{hashlib.md5(zip_bytes).hexdigest()}…, sha256 "
      f"{hashlib.sha256(zip_bytes).hexdigest()}… — extraction VIERGE, "
      f"les QUATRE pièces du contrat")
print("\nLA VAGUE dev.11 EST NÉE : build-dev11/ + kit-loupe.zip")
print("la pièce dev.8 INTACTE ; la sonde de liaison VRAIE PAR CONSTRUCTION")
