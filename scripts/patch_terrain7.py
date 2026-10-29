#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.7 — la porte R10 tuait le run : SOMME de l'entrée [23] périmée.

CONSTAT TERRAIN (terrain_20261027_174338.txt, le run terrain.6 de 17:43) :
  L00→L03 OK, S00 « 0.5.0-terrain.6 », S01 date, puis
  S02 porte R10 : KO - arret   S91 SUPERVISEUR : ECHEC
  Le superviseur fonctionne (fenêtre, clic, scénario, verdict S91 écrit) :
  c'est la PORTE qui refuse l'image — fail-closed, exactement comme prévu.

LA CAUSE (preuve binaire, diag_r10_terrain6.py) :
  La table R10 @rva 0x2450 compte 27 entrées + terminateur (0,0,0) —
  23 blocs + 4 zones données (build_terrain.py l.438-455). Le patch
  terrain.6 supposait N=20 et ne vérifiait/ajustait que les entrées 0..19.
  L'entrée [23] (rva=0x4340 len=0x8C0 — zone données S* de .text2) COUVRE
  l'octet version S00 @0x4366 : le changement 'terrain.3' -> 'terrain.6'
  a périmé sa somme (0xbfedbfef9637a937 -> 0xbff0bfef9637a937, delta
  3<<48 = '3'->'6' à l'octet 6 du mot @+32). Sur machine réelle, la boucle
  de la porte (win-06 : TANT QUE rva != 0) atteint [23], somme divergente,
  retour -1, S02 KO. (Le README terrain « 18 entrées » était également
  périmé — le binaire fait foi : 27.)

LE CORRECTIF (base = terrain.6 livré, md5 2e582a64b04a…) :
  1. somme R10[23] recalculée SUR L'IMAGE FINALE (après le bump version) ;
  2. L00 @0x2ada et S00 @0x4366 : « terrain.6 » -> « terrain.7 » (un octet
     chacun, même longueur) ;
  3. VERSIONINFO 0.5.6.0 -> 0.5.7.0 (4 champs, traçabilité WER).
  AUCUN autre octet ne bouge : le correctif FindWindowW de terrain.6
  (sup-33 @0x544f, somme R10[19] déjà verte) est conservé tel quel.

MÉTHODE CORRIGÉE (la leçon de terrain.6) :
  - la table est lue JUSQU'AU TERMINATEUR rva==0 (aucun compte codé en dur) ;
  - pré-contrôle : les 27 entrées vérifiées, exactement UNE rouge attendue
    ([23], la somme périmée) — toute autre divergence = abandon ;
  - post-contrôle : les 27 entrées + terminateur TOUTES VERTES, diff borné,
    désassemblage du correctif terrain.6 intact, zones critiques intactes.
"""

import hashlib
import pathlib
import struct
import sys

SRC = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain6.exe")
DST = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain7.exe")

MD5_TERRAIN6 = "2e582a64b04a2acf05e874cfc97a8caa"

# --- géométrie PE (identique aux builds précédents) --------------------------
RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
R10_TABLE_RVA = 0x2450
ENTREE_S = 23                          # rva=0x4340 len=0x8C0 (zone données S*)

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if RDATA_RVA <= rva < 0x3000:
        return RDATA_FILE + (rva - RDATA_RVA)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if TEXT2_RVA <= rva < 0x6E00:
        return TEXT2_FILE + (rva - TEXT2_RVA)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None

def somme_zone(data, rva, ln):
    """Somme tronquée de mots u64 LE — l'algorithme exact de la porte (win-06)."""
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s

def lire_table(data):
    """Lit la table JUSQU'AU TERMINATEUR rva==0 — la vraie boucle de la porte."""
    table_off = rva2off(R10_TABLE_RVA)
    entrees = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            return entrees, k          # entrées + indice du terminateur
        entrees.append((rva, ln, sm))
        k += 1
        if k > 60:
            raise ValueError("table R10 sans terminateur — corrompue ?")

def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)

# =============================================================================
# 1. GARDES-FOUS sur terrain.6 (le binaire source doit être EXACTEMENT attendu)
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(base).hexdigest() != MD5_TERRAIN6:
    erreur("terrain.6 : md5 inattendu")

table_off = rva2off(R10_TABLE_RVA)

# 1a. la table : 27 entrées + terminateur, EXACTEMENT une rouge : [23]
entrees, idx_term = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées avant terminateur, 27 attendues")
rouges = [k for k, (rva, ln, sm) in enumerate(entrees)
          if somme_zone(base, rva, ln) != sm]
if rouges != [ENTREE_S]:
    erreur(f"entrées rouges {rouges} sur terrain.6 — [23] seule attendue "
           f"(la somme périmée du patch terrain.6)")
rva23, ln23, sm23 = entrees[ENTREE_S]
if (rva23, ln23) != (0x4340, 0x8C0):
    erreur(f"entrée [23] : rva={rva23:#x} len={ln23:#x}, zone données S* attendue")
calc23 = somme_zone(base, rva23, ln23)
if calc23 - sm23 != 3 << 48:
    erreur(f"delta inattendu sur [23] : {calc23 - sm23:#x} (3<<48 attendu — "
           f"l'octet '3'->'6' de S00 @0x4366)")
print(f"[pre] 27 entrées + terminateur ; seule [23] rouge, delta {calc23 - sm23:#x} "
      f"conforme au constat")

# 1b. le correctif FindWindowW de terrain.6 est en place (intouché)
OFF_SUP33 = rva2off(0x544F)
if bytes(base[OFF_SUP33:OFF_SUP33 + 9]) != bytes.fromhex("488d0d3cd6ffff31d2"):
    erreur("sup-33 @0x544f : le lea/xor de terrain.6 est absent")
if bytes(base[OFF_SUP33 + 9:OFF_SUP33 + 15]) != bytes.fromhex("ff1502cfffff"):
    erreur("le call FindWindowW après le lea a bougé")

# 1c. les chaînes version disent « terrain.6 » (contexte borné)
OFF_L00 = rva2off(0x2ADA)
OFF_S00 = rva2off(0x4366)
if base[OFF_L00 - 8:OFF_L00 + 1] != b"terrain.6" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 @0x2ad2 : contexte inattendu")
if base[OFF_S00 - 8:OFF_S00 + 1] != b"terrain.6" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 @0x435e : contexte inattendu")

# 1d. VERSIONINFO à 6 (0.5.6.0)
if struct.unpack_from("<H", base, 0x5CD4)[0] != 6:
    erreur("FileVersion binaire @0x5cd4 != 6")
if struct.unpack_from("<H", base, 0x5CDC)[0] != 6:
    erreur("ProductVersion binaire @0x5cdc != 6")
if base[0x5DC4:0x5DC6] != "6".encode("utf-16-le"):
    erreur("FileVersion chaîne @0x5dc4 != '6'")
if base[0x5ECC:0x5ECE] != "6".encode("utf-16-le"):
    erreur("ProductVersion chaîne @0x5ecc != '6'")

# 1e. couverture : quelles entrées couvrent les octets qu'on va toucher ?
#     (la vérification que terrain.6 N'A PAS FAITE — désormais systématique)
zones_a_toucher = [(OFF_L00, 1, "L00 '7'"), (OFF_S00, 1, "S00 '7'"),
                   (0x5CD4, 2, "FileVersion binaire"),
                   (0x5CDC, 2, "ProductVersion binaire"),
                   (0x5DC4, 2, "FileVersion chaîne"),
                   (0x5ECC, 2, "ProductVersion chaîne")]
for k, (rva, ln, sm) in enumerate(entrees):
    for (arva, aln, lab) in [(0x2ADA, 1, "L00"), (0x4366, 1, "S00"),
                             (0x70D4, 2, "FVb"), (0x70DC, 2, "PVb"),
                             (0x71C4, 2, "FVs"), (0x72CC, 2, "PVs")]:
        if not (rva + ln <= arva or arva + aln <= rva):
            print(f"[couv] R10[{k}] (rva={rva:#x} len={ln:#x}) couvre {lab} "
                  f"@{arva:#x} — sa somme DOIT être recalculée")

# =============================================================================
# 2. LE PATCH (copie -> écritures bornées, ordre : octets PUIS sommes)
# =============================================================================
img = bytearray(base)

# (a) L00 / S00 : « terrain.6 » -> « terrain.7 » (un octet chacun)
img[OFF_L00] = ord("7")
img[OFF_S00] = ord("7")

# (b) VERSIONINFO 0.5.6.0 -> 0.5.7.0 (4 champs)
struct.pack_into("<H", img, 0x5CD4, 7)                # FileVersion binaire
struct.pack_into("<H", img, 0x5CDC, 7)                # ProductVersion binaire
img[0x5DC4:0x5DC6] = "7".encode("utf-16-le")          # FileVersion chaîne
img[0x5ECC:0x5ECE] = "7".encode("utf-16-le")          # ProductVersion chaîne

# (c) somme R10[23] recalculée SUR L'IMAGE FINALE (S00 @0x4366 est DANS la zone)
nouvelle_somme = somme_zone(img, rva23, ln23)
struct.pack_into("<Q", img, table_off + 16 * ENTREE_S + 8, nouvelle_somme)

# =============================================================================
# 3. POST-VÉRIFICATIONS (fail-closed)
# =============================================================================
# 3a. diff octet à octet : seules les zones autorisées bougent
off_somme23 = table_off + 16 * ENTREE_S + 8
autorisees = [
    (OFF_L00, OFF_L00 + 1),                           # L00 '7'
    (OFF_S00, OFF_S00 + 1),                           # S00 '7'
    (off_somme23, off_somme23 + 8),                   # somme R10[23]
    (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),               # versions binaires
    (0x5DC4, 0x5DC6), (0x5ECC, 0x5ECE),               # versions chaînes
]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorisees)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés, tous dans les zones autorisées")

# 3b. LA PORTE ENTIÈRE : toutes les entrées + terminateur, TOUTES VERTES
#     (boucle jusqu'au terminateur — plus aucun compte codé en dur)
entrees_f, idx_term_f = lire_table(img)
if idx_term_f != 27 or len(entrees_f) != 27:
    erreur(f"table finale : {idx_term_f} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}] "
               f"(rva={rva:#x} len={ln:#x})")
term_rva, term_ln, term_sm = struct.unpack_from("<IIQ", img, table_off + 16 * 27)
if (term_rva, term_ln, term_sm) != (0, 0, 0):
    erreur("le terminateur (0,0,0) @entrée 27 a bougé")
print("[porte] R10 : 27/27 entrées VERTES + terminateur intact")

# 3c. le correctif FindWindowW de terrain.6 se désassemble exactement
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    code = bytes(img[OFF_SUP33:OFF_SUP33 + 15])
    attendu = ["lea rcx, [rip - 0x29c4]", "xor edx, edx",
               "call qword ptr [rip - 0x30fe]"]
    obtenu = [f"{i.mnemonic} {i.op_str}" for i in md.disasm(code, 0x544F)]
    if obtenu != attendu:
        erreur(f"désassemblage inattendu : {obtenu}")
    print(f"[code] 0x544f intact : {' ; '.join(attendu)}  "
          f"(= FindWindowW(L\"TRIADE_demo\", NULL))")
except ImportError:
    print("[code] capstone absent — vérification désassemblage sautée (FAIBLE)")

# 3d. les sections critiques inchangées : en-têtes PE + .blob + .idata
for a, b in ((0, 0x400), (0x6400, len(img))):
    if any(base[i] != img[i] for i in range(a, b) if not any(
            x <= i < y for x, y in [(0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
                                    (0x5DC4, 0x5DC6), (0x5ECC, 0x5ECE)])):
        erreur(f"zone critique [{a:#x}..{b:#x}] modifiée hors VERSIONINFO")
print("[zones] en-têtes PE, .blob (demo/proxy embarqués), .idata : intacts")

# 3e. md5 final + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
