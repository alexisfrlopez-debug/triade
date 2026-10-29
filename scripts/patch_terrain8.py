#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.8 — le superviseur embarque demo.10 DIAGNOSTIQUE (D57).

LE CONSTAT TERRAIN (terrain_20261027_180007.txt + demo_journal.txt, run
terrain.7 de 18:00) : S02 porte R10 VERTE (correctif D56 validé), S03-S06
kit conforme, S11 fenetre demo DETECTEE, S12 clic BM_CLICK envoye — TOUTE
la mécanique superviseur VIT. Puis le journal demo coupe sur « client :
connecté » -> « réseau : échange en échec » (ligne E5 de win-09) — 2e
reproduction PROPRE (la 1re : run manuel terrain.5, 16:52) — et le
scénario s'arrête PROPREMENT (E5 = ligne + nettoyage + arrêt, fenêtre
ouverte, le demo ne meurt pas). Le journal superviseur s'arrête à S12 :
le processus a été interrompu pendant le sondage 30 s du marqueur final
(fermeture manuelle probable — l'utilisateur a reconnu la ligne d'échec
de son run manuel).

L'ANALYSE STATIQUE (diag_echange/diag_reseau, ce dépôt) : chaîne réseau
byte-identique demo.8/demo.9, win-10 sain, CS D42 vivante, tcp-11
propre — l'échec est un fait d'exécution INVISIBLE en statique. La
méthode du projet (D40-D42) : INSTRUMENTER. demo.10 = demo.8 (28/28
lignes VERTES sur CETTE machine le 26/10, sondes S1/S2/sonde4/sonde5
encadrant EXACTEMENT l'intervalle mort) + identification « 0.3.0-demo10 »
(md5 cf72462d…, patch_demo10.py : 3 octets de version, porte 28/28).

LE PATCH SUPERVISEUR (base terrain.7, md5 1e72811c…) :
  1. .blob : demo.exe (16 384 o @rva 0x8010) remplacé par demo.10 ;
  2. md5 hex affiché (S04C, zone données sup 3) : 73c064fb… ->
     cf72462d… (32 o, même longueur — l'affichage terrain dira la
     VÉRITÉ ; la conformité S04 reste la comparaison octets extraits
     vs blob, inchangée) ;
  3. version : L00/S00 « terrain.7 » -> « terrain.8 », VERSIONINFO
     0.5.8.0 (4 champs) ;
  4. sommes R10 des entrées couvrantes recalculées sur l'image finale
     (table lue JUSQU'AU TERMINATEUR — méthode D56).

NON-PATCHÉ (délibéré) : le seuil 17 lignes et la limite 640 o du sondage
journal (TAMPON_CMD @0x3D50 = 688 o max, .text2 derrière — la limite est
PHYSIQUE). Le journal d'échec attendu (≤ 550 o, sondes incluses) est
entièrement couvert ; un éventuel succès 28 lignes dira NON conforme et
attendra 30 s — ACCEPTÉ pour un build diagnostique, le LISEZMOI le dit.
"""

import hashlib
import pathlib
import struct
import sys

SRC = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain7.exe")
DEMO10 = pathlib.Path("/home/z/my-project/triade/demo/livraison/demo10-diagnostique.exe")
DST = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain8.exe")

MD5_TERRAIN7 = "1e72811c22522901b3ca2ff2f07f73c0"
MD5_DEMO9 = "73c064fbaf4610a167bc6434dee400e4"
MD5_DEMO10 = "cf72462dc130aa4753a2fe5e78f06a08"

RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
R10_TABLE_RVA = 0x2450
BLOB_DEMO_OFF = 0x6410                    # demo.exe @rva 0x8010, 16 384 o
TAILLE_DEMO = 16384

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
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s

def lire_table(data):
    table_off = rva2off(R10_TABLE_RVA)
    entrees = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            return entrees, k
        entrees.append((rva, ln, sm))
        k += 1
        if k > 60:
            raise ValueError("table R10 sans terminateur")

def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)

# =============================================================================
# 1. GARDES-FOUS
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(base).hexdigest() != MD5_TERRAIN7:
    erreur("terrain.7 : md5 inattendu")

demo10 = DEMO10.read_bytes()
if hashlib.md5(demo10).hexdigest() != MD5_DEMO10 or len(demo10) != TAILLE_DEMO:
    erreur("demo.10 : empreinte ou taille inattendue")

# le blob contient demo.9 byte-exact à l'offset attendu
if bytes(base[BLOB_DEMO_OFF:BLOB_DEMO_OFF + TAILLE_DEMO]) != open("/tmp/demo9.exe", "rb").read():
    erreur("le .blob ne contient pas demo.9 à 0x6410 — géométrie inattendue")
# l'en-tête blob (longueurs) : 16 384 / 19 456
if struct.unpack_from("<QQ", base, 0x6400) != (TAILLE_DEMO, 19456):
    erreur("en-tête .blob : longueurs inattendues")

# le md5 hex affiché (S04C) présent une seule fois
hex_old = MD5_DEMO9.encode()
if base.count(hex_old) != 1:
    erreur(f"md5 hex demo.9 : {base.count(hex_old)} occurrence(s), 1 attendue")
OFF_MD5 = base.find(hex_old)
RVA_MD5 = 0x6A5F                        # zone données sup 3 (couverture R10[25])
if rva2off(RVA_MD5) != OFF_MD5:
    erreur(f"md5 hex @file {OFF_MD5:#x} != RVA {RVA_MD5:#x} attendue")

# versions courantes = 7 / terrain.7
OFF_L00 = rva2off(0x2ADA)
OFF_S00 = rva2off(0x4366)
if base[OFF_L00 - 8:OFF_L00 + 1] != b"terrain.7" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if base[OFF_S00 - 8:OFF_S00 + 1] != b"terrain.7" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b, off_s in ((0x5CD4, 0x5DC4), (0x5CDC, 0x5ECC)):
    if struct.unpack_from("<H", base, off_b)[0] != 7:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 7")
    if base[off_s:off_s + 2] != "7".encode("utf-16-le"):
        erreur(f"VERSIONINFO chaîne @{off_s:#x} != '7'")

# le correctif FindWindowW de terrain.6 en place
OFF_SUP33 = rva2off(0x544F)
if bytes(base[OFF_SUP33:OFF_SUP33 + 9]) != bytes.fromhex("488d0d3cd6ffff31d2"):
    erreur("sup-33 @0x544f : correctif FindWindowW absent")

# la table : 27 entrées + terminateur, toutes vertes sur terrain.7
table_off = rva2off(R10_TABLE_RVA)
entrees, idx_term = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"terrain.7 : R10[{k}] ROUGE avant patch")

# quelles entrées couvrent les octets qu'on va toucher ?
touches = [(0x8010, TAILLE_DEMO, "demo.10 dans .blob"),
           (RVA_MD5, 32, "md5 hex S04C"),
           (0x2ADA, 1, "L00 '8'"), (0x4366, 1, "S00 '8'")]
couvreurs = set()
for k, (rva, ln, sm) in enumerate(entrees):
    for (arva, aln, lab) in touches:
        if not (rva + ln <= arva or arva + aln <= rva):
            print(f"[couv] R10[{k}] (rva={rva:#x} len={ln:#x}) couvre {lab}")
            couvreurs.add(k)
if couvreurs != {23, 25, 26}:
    erreur(f"couvreurs {sorted(couvreurs)} != {{23, 25, 26}} attendus")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# (a) .blob : demo.9 -> demo.10 (16 384 o byte-exact)
img[BLOB_DEMO_OFF:BLOB_DEMO_OFF + TAILLE_DEMO] = demo10

# (b) md5 hex affiché (S04C)
img[OFF_MD5:OFF_MD5 + 32] = MD5_DEMO10.encode()

# (c) versions : terrain.7 -> terrain.8 (un octet chacun) + VERSIONINFO 0.5.8.0
img[OFF_L00] = ord("8")
img[OFF_S00] = ord("8")
struct.pack_into("<H", img, 0x5CD4, 8)
struct.pack_into("<H", img, 0x5CDC, 8)
img[0x5DC4:0x5DC6] = "8".encode("utf-16-le")
img[0x5ECC:0x5ECE] = "8".encode("utf-16-le")

# (d) sommes R10 des entrées couvrantes, recalculées sur l'image finale
for k in sorted(couvreurs):
    rva, ln, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8, somme_zone(img, rva, ln))

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné
autorise = [(BLOB_DEMO_OFF, BLOB_DEMO_OFF + TAILLE_DEMO),
            (OFF_MD5, OFF_MD5 + 32),
            (OFF_L00, OFF_L00 + 1), (OFF_S00, OFF_S00 + 1),
            (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
            (0x5DC4, 0x5DC6), (0x5ECC, 0x5ECE)]
for k in sorted(couvreurs):
    autorise.append((table_off + 16 * k + 8, table_off + 16 * k + 16))
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorise)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés (blob + md5 + versions + "
      f"{len(couvreurs)} sommes), tous bornés")

# 3b. la porte ENTIÈRE verte + terminateur
entrees_f, idx_term_f = lire_table(img)
if idx_term_f != 27:
    erreur(f"table finale : {idx_term_f} entrées")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(img, rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
if struct.unpack_from("<IIQ", img, table_off + 16 * 27) != (0, 0, 0):
    erreur("le terminateur a bougé")
print("[porte] R10 : 27/27 entrées VERTES + terminateur intact")

# 3c. le correctif FindWindowW intact + désassemblage
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    code = bytes(img[OFF_SUP33:OFF_SUP33 + 15])
    obtenu = [f"{i.mnemonic} {i.op_str}" for i in md.disasm(code, 0x544F)]
    attendu = ["lea rcx, [rip - 0x29c4]", "xor edx, edx",
               "call qword ptr [rip - 0x30fe]"]
    if obtenu != attendu:
        erreur(f"désassemblage sup-33 inattendu : {obtenu}")
    print(f"[code] FindWindowW par CLASSE intact : {' ; '.join(attendu)}")
except ImportError:
    print("[code] capstone absent (FAIBLE)")

# 3d. le blob : demo.10 byte-exact, proxy + annexe intacts
if bytes(img[BLOB_DEMO_OFF:BLOB_DEMO_OFF + TAILLE_DEMO]) != demo10:
    erreur("demo.10 embarqué non conforme")
if img[0x6400:BLOB_DEMO_OFF] != base[0x6400:BLOB_DEMO_OFF]:
    erreur("en-tête .blob modifié")
if img[BLOB_DEMO_OFF + TAILLE_DEMO:] != base[BLOB_DEMO_OFF + TAILLE_DEMO:]:
    erreur("proxy.exe ou annexe modifiés dans le .blob")
print("[blob] demo.10 embarqué byte-exact ; en-tête, proxy, annexe : intacts")

# 3e. identité
if img[OFF_L00 - 8:OFF_L00 + 1] != b"terrain.8" or img[OFF_S00 - 8:OFF_S00 + 1] != b"terrain.8":
    erreur("versions L00/S00 finales inattendues")
if bytes(img[OFF_MD5:OFF_MD5 + 32]) != MD5_DEMO10.encode():
    erreur("md5 hex final inattendu")
print("[ident] L00/S00 « terrain.8 », VERSIONINFO 0.5.8.0, S04C md5 demo.10")

# 3f. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
