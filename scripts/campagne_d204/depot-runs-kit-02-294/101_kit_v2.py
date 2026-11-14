#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""101_kit_v2.py — LE KIT v2 DE L'UNITÉ 2 × BRAS T : LE JUGE CORRIGÉ, LA
PIÈCE INTACTE. La seule faute était au scénario (R_JOURNAL 0xE4E0, +0x40
au-dessus du layout 0xE4A0 — les DEUX vecteurs V2 ROUGE du terrain,
rejoués au script 100). La v2 change UNE constante au scénario ; les NEUF
autres pièces demeurent OCTET POUR OCTET celles de la v1 (D143 : la v1
demeure au coffre) ; la gravure regravée ; le LISEZMOI porte l'écart
nommé et la reprise ; le zip v2 assemblé.

LES ÉPREUVES (tout au POSIX, D122) : py_compile ; l'audit des constantes
du fichier v2 LIVRÉ (le garde de la 294) ; la faute rejouée à la constante
corrigée ; le modèle du juge extrait par AST contre le contre-modèle
(2 000 cas + les décalées du terrain) ; la gravure == les pièces
assemblées ; les NEUF pièces == la v1 byte-byte ; le zip miroir."""
import ast
import hashlib
import pathlib
import py_compile
import random
import shutil
import struct
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/work/triade")
CAMP = REPO / "scripts" / "campagne_d204"
KIT1 = CAMP / "unite-02-T" / "kit"
KIT2 = CAMP / "unite-02-T" / "kit-v2"
sys.path.insert(0, str(REPO / "loupe"))
import layout as L  # noqa: E402

VERT, ROUGE = 0, 0


def vert(nom):
    global VERT
    VERT += 1
    print(f"  [VERT] {nom}")


def rouge(nom, detail=""):
    global ROUGE
    ROUGE += 1
    print(f"  [ROUGE] {nom} {detail}")


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


KIT2.mkdir(parents=True, exist_ok=True)

# -- 1. LE SCÉNARIO v2 : la constante remise à la vérité ----------------------
v1 = (KIT1 / "scenario-unite02.py").read_text(encoding="utf-8")
assert v1.count("R_JOURNAL = 0xE4E0") == 1, "la ligne fautive introuvable"
assert "0xE4E0" not in v1.replace("R_JOURNAL = 0xE4E0", ""), "un autre 0xE4E0 ?"

NOTE = """RÉVISION v2 (14/11/2026, l'Entrée 294 — L'ÉCART DU JUGE NOMMÉ) : le run
terrain de la v1 (16:46:34Z, 18 VERT 2 ROUGE) révéla que le présent
scénario posait le journal à R_JOURNAL = 0xE4E0 — SOIXANTE-QUATRE octets
au-dessus de la vérité du layout (loupe/layout.py : R_JOURNAL = 0xE4A0,
l'adresse même que le lea de la pièce vise, lue à l'octet près au
scripts/campagne_d204/depot-runs-kit-02-294/99_preuve_lea_exe.py). LA
PIÈCE ÉTAIT DROITE : le compte qu'elle lisait tombait à l'entrée #156 de
la zone zéroée du juge → compte 0 → AUCUN recouvrement → les DEUX
vecteurs V2 ROUGE (les-bords-de-fenetre, cinq-entrees-dont-une-non-
alignee) — rejoués octet par octet au labo (100_epreuves_juge.py). LE
SEUL CHANGEMENT de la v2 : la constante remise à la vérité du layout
(0xE4A0) ; la pièce et les HUIT autres pièces du kit demeurent INTACTES
octet pour octet celles de la v1 (D143 : le kit v1 demeure au coffre)."""

v2 = v1.replace(
    "R_JOURNAL = 0xE4E0",
    "R_JOURNAL = 0xE4A0            # loupe-16 : la vérité du layout (D161) ; la v1\n"
    "                               # portait 0xE4E0 (+0x40) — l'écart du juge,\n"
    "                               # nommé à l'Entrée 294", 1)
assert "R_JOURNAL = 0xE4A0" in v2, "la constante n'est pas corrigée"
# la note de révision APRÈS : elle cite la faute nommée, aucun replace ne la touche
v2 = v2.replace(
    "campagne de comparaison des workflows D204).\n\nLe kit porte UNE pièce et UN scénario :",
    "campagne de comparaison des workflows D204).\n\n" + NOTE + "\n\n"
    "Le kit porte UNE pièce et UN scénario :", 1)
assert v2 != v1 and "0xE4E0" in v2  # la faute demeure NOMMÉE (la note + le commentaire)
(KIT2 / "scenario-unite02.py").write_text(v2, encoding="utf-8")

# -- 2. LES NEUF PIÈCES INTACTES ----------------------------------------------
INTACTES = ["loupe.exe", "notation-loupe-02-lire.asm", "brouillon-loupe-02-lire.asm",
            "temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin",
            "LANCEUR-UNITE-02-T.bat"]
for nom in INTACTES:
    shutil.copyfile(KIT1 / nom, KIT2 / nom)
    assert sha256(KIT1 / nom) == sha256(KIT2 / nom)

# -- 3. LE LISEZMOI v2 ---------------------------------------------------------
lis1 = (KIT1 / "LISEZMOI-KIT-UNITE-02-T.txt").read_text(encoding="utf-8")
lis2 = lis1.replace(
    "LISEZMOI — LE KIT DE L'UNITÉ 2 : LOUPE-02 LIRE × BRAS T\n",
    "LISEZMOI — LE KIT DE L'UNITÉ 2 : LOUPE-02 LIRE × BRAS T — RÉVISION v2\n"
    "(le juge corrigé, la pièce INTACTE ; la v1 courue au terrain le 14/11\n"
    "16:46:34Z revint 18 VERT 2 ROUGE — les DEUX ROUGE étaient la faute du\n"
    "JUGE, nommée ci-dessous)\n", 1)
lis2 = lis2.replace(
    "LE GESTE (tout au clic, l'ordre de jeu d'une unité) :",
    """LA RÉVISION v2 (l'Entrée 294 — l'écart du juge nommé, la pièce
reconnue DROITE) : le scénario v1 posait le journal d'édition à
R_JOURNAL = 0xE4E0 — soixante-quatre octets au-dessus de la vérité du
layout (loupe/layout.py : 0xE4A0, l'adresse que le lea de la pièce
vise). La pièce lisait son compte à la bonne adresse et tombait sur la
zone zéroée : compte 0, AUCUN recouvrement — les DEUX vecteurs V2
(les-bords-de-fenetre, cinq-entrees-dont-une-non-alignee) revinrent
ROUGE alors que la pièce était DROITE (le bras C, le même contrat juge
par les exports de la dll, revint 20 VERT 0 ROUGE). LE SEUL CHANGEMENT :
la constante du scénario remise à la vérité ; loupe.exe et les HUIT
autres pièces INTACTES octet pour octet (comparez les EMPREINTES : une
seule ligne bouge — scenario-unite02.py).

LE GESTE (tout au clic, l'ordre de jeu d'une unité) :""", 1)
lis2 = lis2.replace(
    "1. AU GUI (TRIADE_gui_campagne_v1 ou TRIADE_gui_tous_runs_v1), onglet\n"
    "     1·KIT de l'unité loupe-02 × T : CHOISIR CE DOSSIER\n"
    "     (kit-unite-loupe-02-T-20261114) — le GUI recoupe les EMPREINTES\n"
    "     gravées (une divergence, rien ne court) ;",
    "1. AU GUI (TRIADE_gui_campagne_v1 ou TRIADE_gui_tous_runs_v1), onglet\n"
    "     1·KIT de l'unité loupe-02 × T : CHOISIR CE DOSSIER\n"
    "     (kit-unite-loupe-02-T-20261114-v2) — le GUI recoupe les EMPREINTES\n"
    "     gravées (une divergence, rien ne court) ;", 1)
lis2 = lis2.replace(
    "  scenario-unite02.py           le scénario (le chargeur + le juge) ;",
    "  scenario-unite02.py           le scénario (le chargeur + le juge) —\n"
    "                                v2 : LA CONSTANTE DU JOURNAL remise à\n"
    "                                la vérité du layout (0xE4A0) ; le reste\n"
    "                                du texte INTACT ;", 1)
lis2 = lis2.replace(
    "*La consignation vit au journal de travail (l'Entrée 290) ; le détail du",
    "*La consignation vit au journal de travail (les Entrées 290 et 294) ; le détail du", 1)
assert lis2 != lis1
# la convention d'écriture de la 290 : le double BOM
(KIT2 / "LISEZMOI-KIT-UNITE-02-T.txt").write_bytes(
    b"\xef\xbb\xbf\xef\xbb\xbf" + lis2.encode("utf-8"))

# -- 4. LA GRAVURE REGRAVÉE ----------------------------------------------------
lignes = [
    ("loupe.exe", sha256(KIT2 / "loupe.exe")),
    ("notation-loupe-02-lire.asm", sha256(KIT2 / "notation-loupe-02-lire.asm")),
    ("brouillon-loupe-02-lire.asm", sha256(KIT2 / "brouillon-loupe-02-lire.asm")),
    ("scenario-unite02.py", sha256(KIT2 / "scenario-unite02.py")),
    ("temoin-1.bin", sha256(KIT2 / "temoin-1.bin")),
    ("temoin-384.bin", sha256(KIT2 / "temoin-384.bin")),
    ("temoin-3f.bin", sha256(KIT2 / "temoin-3f.bin")),
    ("vide.bin", sha256(KIT2 / "vide.bin")),
    ("LANCEUR-UNITE-02-T.bat", sha256(KIT2 / "LANCEUR-UNITE-02-T.bat")),
    ("LISEZMOI-KIT-UNITE-02-T.txt", sha256(KIT2 / "LISEZMOI-KIT-UNITE-02-T.txt")),
]
corps = ("EMPREINTES — LE KIT DE L'UNITÉ 2 (loupe-02 LIRE × bras T, la campagne D204)"
         " — RÉVISION v2 (le juge corrigé, la pièce INTACTE)\n"
         "(chaque pièce sha256 — le GUI recoupe à l'onglet 1·KIT ; une divergence, "
         "rien ne court ; la v1 demeure au coffre, D143)\n\n"
         + "".join(f"{h}  {n}\n" for n, h in lignes))
(KIT2 / "EMPREINTES-KIT-UNITE-02-T.txt").write_bytes(
    b"\xef\xbb\xbf\xef\xbb\xbf" + corps.encode("utf-8"))

# -- 5. LE ZIP v2 ---------------------------------------------------------------
ZIP2 = KIT2 / "kit-unite-loupe-02-T-20261114-v2.zip"
with zipfile.ZipFile(ZIP2, "w", zipfile.ZIP_DEFLATED) as z:
    for nom in ["EMPREINTES-KIT-UNITE-02-T.txt", "LANCEUR-UNITE-02-T.bat",
                "LISEZMOI-KIT-UNITE-02-T.txt", "brouillon-loupe-02-lire.asm",
                "loupe.exe", "notation-loupe-02-lire.asm", "scenario-unite02.py",
                "temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin"]:
        z.write(KIT2 / nom, f"kit-unite-loupe-02-T-20261114-v2/{nom}")

# ===========================================================================
print("LES ÉPREUVES DU KIT v2 (tout au POSIX, D122)")
# ===========================================================================

# E1 — py_compile
py_compile.compile(str(KIT2 / "scenario-unite02.py"), doraise=True)
vert("E1 py_compile du scénario v2")

# E2 — l'audit des constantes du fichier v2 LIVRÉ
arbre = ast.parse((KIT2 / "scenario-unite02.py").read_text(encoding="utf-8"))
consts, iat = {}, None
for noeud in arbre.body:
    if isinstance(noeud, ast.Assign) and len(noeud.targets) == 1 \
            and isinstance(noeud.targets[0], ast.Name):
        if isinstance(noeud.value, ast.Constant):
            consts[noeud.targets[0].id] = noeud.value.value
        elif isinstance(noeud.value, ast.Dict) and noeud.targets[0].id == "IAT_SLOTS":
            iat = {ast.literal_eval(k): ast.literal_eval(v)
                   for k, v in zip(noeud.value.keys, noeud.value.values)}
verite = {"R_LOUPE01": L.LOUPE01_VA, "R_LOUPE02": L.LOUPE02_VA,
          "R_LOUPE03": L.LOUPE03_VA, "R_CADRE": L.R_CADRE,
          "R_JOURNAL": L.R_JOURNAL, "ZONE_JOURNAL": L.ZONE_JOURNAL}
ecarts = [f"{k} 0x{consts[k]:X} ≠ 0x{v:X}" for k, v in verite.items()
          if k in consts and consts[k] != v]
ecarts += [f"IAT {f} 0x{s:X} ≠ 0x{L.IAT_SLOTS[f]:X}" for f, s in (iat or {}).items()
           if L.IAT_SLOTS.get(f) != s]
if ecarts:
    rouge("E2 l'audit des constantes", str(ecarts))
else:
    vert(f"E2 l'audit des constantes du v2 : {len(verite)} R_* + "
         f"{len(iat or {})} IAT == le layout (R_JOURNAL 0x{consts['R_JOURNAL']:X})")

# E3 — la faute rejouée : le juge v2 pose à SA constante, la pièce lit à
# SON LEA À ELLE (0xE4A0, FIXE — le script 99) ; les deux doivent coïncider
FEN = 65536
LEA_PIECE = 0xE4A0
DONNEES = (KIT2 / "temoin-3f.bin").read_bytes()
for nom_v, entrees in [("les-bords-de-fenetre",
                        [(FEN, 0xAA), (FEN + 383, 0xBB), (FEN + 384, 0xCC), (FEN - 16, 0xDD)]),
                       ("cinq-entrees-dont-une-non-alignee",
                        [(FEN + 5, 0x11), (FEN + 100, 0x22), (FEN + 200, 0x33),
                         (FEN + 300, 0x44), (FEN + 383, 0x55)])]:
    memoire = bytearray(0x20000)
    zone = bytearray(L.ZONE_JOURNAL)
    for i, (dec, octet) in enumerate(entrees):
        zone[16 * i:16 * i + 16] = struct.pack("<QB7x", dec, octet)
    zone[4096:4100] = struct.pack("<I", len(entrees))
    memoire[consts["R_JOURNAL"]:consts["R_JOURNAL"] + L.ZONE_JOURNAL] = zone
    rempl = min(384, len(DONNEES) - FEN)
    compte = struct.unpack_from("<I", memoire, LEA_PIECE + 4096)[0]
    tampon = bytearray(DONNEES[FEN:FEN + rempl])
    for i in range(compte):
        pos = struct.unpack_from("<Q", memoire, LEA_PIECE + 16 * i)[0]
        if FEN <= pos < FEN + rempl:
            tampon[pos - FEN] = memoire[LEA_PIECE + 16 * i + 8]
    attendu = bytearray(DONNEES[FEN:FEN + rempl])
    for dec, octet in entrees:
        if FEN <= dec < FEN + rempl:
            attendu[dec - FEN] = octet
    if bytes(tampon) == bytes(attendu) and compte == len(entrees) \
            and consts["R_JOURNAL"] == LEA_PIECE:
        vert(f"E3 faute rejouée, {nom_v} : le juge pose à 0x{consts['R_JOURNAL']:X} == "
             f"le lea de la pièce — compte {compte}/{len(entrees)}, le recouvrement VIT")
    else:
        rouge(f"E3 faute rejouée, {nom_v} : le juge pose à "
              f"0x{consts['R_JOURNAL']:X} ≠ le lea 0x{LEA_PIECE:X}")

# E4 — le modèle du juge v2 (AST) contre le contre-modèle
source = (KIT2 / "scenario-unite02.py").read_text(encoding="utf-8")
a = ast.parse(source)
gardes = [n for n in ast.walk(a) if isinstance(n, ast.FunctionDef)
          and n.name in ("modele_tampon", "decales_terrain")]
assert len(gardes) == 2
ns = {"min": min, "random": random, "GRAINE": 20261114}
exec(compile(ast.Module(body=gardes, type_ignores=[]), "scenario-v2", "exec"), ns)
modele_tampon, decales_terrain = ns["modele_tampon"], ns["decales_terrain"]


def contre(donnees, dec, journal):
    if dec % 16 or dec >= len(donnees):
        raise ValueError("hors contrat")
    r = min(384, len(donnees) - dec)
    t = bytearray(donnees[dec:dec + r])
    for d, o in journal:
        if dec <= d < dec + r:
            t[d - dec] = o
    return r, bytes(t)


rng = random.Random(42)
cas = 0
for _ in range(2000):
    taille = rng.choice([1, 16, 384, 385, 196609, rng.randrange(16, 5000)])
    donnees = rng.randbytes(taille)
    dec = rng.choice(list(range(0, (taille + 15) // 16 * 16, 16)))
    if dec >= taille:
        continue
    journal = [(rng.randrange(0, taille + 800), rng.randrange(256))
               for _ in range(rng.randrange(6))]
    assert modele_tampon(donnees, dec, journal) == contre(donnees, dec, journal)
    cas += 1
for t in (1, 16, 384, 385, 196609):
    ds = decales_terrain(t)
    assert all(d % 16 == 0 and d < t for d in ds) and len(ds) == len(set(ds))
    assert 0 in ds and (t - 1) // 16 * 16 in ds
vert(f"E4 le modèle du juge v2 == le contre-modèle : {cas} cas + les décalées "
     f"du terrain aux CINQ tailles")

# E5 — la gravure == les pièces assemblées
gravure_ok = True
for nom, h in lignes:
    if sha256(KIT2 / nom) != h:
        gravure_ok = False
        rouge(f"E5 gravure {nom}")
if gravure_ok:
    vert("E5 la gravure regravée == les DIX pièces assemblées (sha256 par sha256)")

# E6 — les HUIT pièces intactes == la v1 byte-byte
tous = all(sha256(KIT1 / n) == sha256(KIT2 / n) for n in INTACTES)
if tous:
    vert("E6 les HUIT pièces du kit v2 == la v1 OCTET POUR OCTET "
         "(loupe.exe 98354ff6…, la notation, le brouillon, les QUATRE "
         "témoins, le LANCEUR)")
else:
    rouge("E6 une pièce diverge de la v1")

# E7 — le zip miroir
avec = zipfile.ZipFile(ZIP2)
membres = {n.split("/", 1)[1]: avec.read(n) for n in avec.namelist()}
zip_ok = all(membres[n] == (KIT2 / n).read_bytes() for n in membres) \
    and len(membres) == 11
if zip_ok:
    vert(f"E7 le zip miroir : {len(membres)} pièces == les fichiers "
         f"libres ({ZIP2.stat().st_size} o)")
else:
    rouge("E7 le zip miroir diverge")

print(f"\n[KIT v2] {VERT} VERT, {ROUGE} ROUGE")
print(f"[KIT v2] scenario-unite02.py v2 : {lignes[3][1][:16]}…")
print(f"[KIT v2] LISEZMOI v2            : {lignes[9][1][:16]}…")
print(f"[KIT v2] la pièce INTACTE       : loupe.exe {lignes[0][1][:16]}…")
for nom, h in lignes:
    print(f"    {h[:16]}…  {nom}")
sys.exit(1 if ROUGE else 0)
