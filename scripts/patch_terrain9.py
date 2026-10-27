#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.9 — même image que terrain.8, seule la génération change (D59).

LE VERDICT DU RUN 19:23 (relance D58, terrain_20261027_192346.txt, 1 525 o —
le journal terrain le plus long jamais produit) :
  - S02 porte R10 VERTE (3e validation D56), S03-S06 kit conforme,
    S11 fenêtre DETECTÉE (3e validation D55), S12 clic envoyé ;
  - S13 code=0, S14 lignes=26, fragment « re » à l'octet 640 : LES TROIS
    PRÉDICTIONS PRÉ-ENREGISTRÉES (journal 47) SE VÉRIFIENT À L'OCTET PRÈS ;
  - S15 NON conforme + S16 VERDICT KO : la machinerie T1 ENTIÈRE a vécu
    (première fois sur le terrain) ;
  - S20/S21 : le proxy est lancé, la bannière est reçue — puis MORT au
    premier curl de T2, 2e fois EXACTEMENT au même point (terrain.5 16:52).

LE DIAGNOSTIC (cette session) : le superviseur a été TUÉ DE L'EXTÉRIEUR
pendant l'attente WaitForSingleObject du premier curl. Preuves :
  (1) le chemin .curl est statiquement sain : IAT 100 % couverte
      (43 slots / 6 descripteurs, WaitForSingleObject 0x2310 et
      GetExitCodeProcess 0x2318 inclus — scripts/diag_iat_curl_terrain8.py) ;
  (2) chacun de ses appels API est DÉJÀ passÉ sur le terrain au run 19:23
      par T1 (sup-33 utilise les MÊMES slots — S13 « code=0 » en sort) ;
  (3) pendant .curl le fil du scénario est bloqué dans WaitForSingleObject :
      une croix ne serait traitée qu'au RETOUR du gestionnaire — l'absence
      de S22A est impossible par un chemin interne propre ;
  (4) « tout s'est fermé tout seul » = arbre entier tué d'un coup — la
      signature d'un antivirus, pas d'un crash (un crash laisse une fenêtre
      WER et ne ferme pas les enfants) ;
  (5) Defender : RealTimeProtection + BehaviorMonitor ACTIFS (diagnostic 2),
      proxy.exe DÉJÀ détecté le 27/10 à 12:55:32, et le kill survient au
      moment précis où la chaîne curl -> proxy(25000) -> neverssl.com
      s'établit (relais réseau externe = motif comportemental classique).
      L'utilisateur n'a RIEN fermé (demo_journal 706 o propre, aucune ligne
      L4C/L4D post-DÉMO OK — le protocole a été respecté à la lettre).

LA DÉCISION D59 : l'exclusion Defender du dossier d'exécution est la seule
variable de cette itération (falsifiable : sans exclusion mort 2/2 au
premier curl ; avec exclusion, si le run va au bout, la cause est prouvée).
Le binaire ne change PAS fonctionnellement — la génération seule
s'identifie : L00/S00 « terrain.9 », VERSIONINFO 0.5.9.0.

LE PATCH (base terrain.8, md5 d64304bd…) :
  1. L00 @rva 0x2ADA et S00 @rva 0x4366 : « terrain.8 » -> « terrain.9 »
     (1 octet chacun, même longueur) ;
  2. VERSIONINFO 0.5.9.0 (2 champs binaires + 2 chaînes UTF-16 : 8 -> 9) ;
  3. somme R10[23] (l'unique entrée couvrant S00 @0x4366) recalculée sur
     l'image finale — table relue JUSQU'AU TERMINATEUR (méthode D56).

HORS COUVERTURE R10 (vérifié par balayage, aucune somme à toucher) : L00
@0x2ADA et les 4 octets VERSIONINFO en .rsrc.
"""

import hashlib
import pathlib
import struct
import sys

SRC = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain8.exe")
DST = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain9.exe")

MD5_TERRAIN8 = "d64304bd1c567bfe801e6e90ad1bf67c"

RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
R10_TABLE_RVA = 0x2450

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
if hashlib.md5(base).hexdigest() != MD5_TERRAIN8:
    erreur("terrain.8 : md5 inattendu")

# versions courantes = 8 / terrain.8
OFF_L00 = rva2off(0x2ADA)
OFF_S00 = rva2off(0x4366)
if base[OFF_L00 - 8:OFF_L00 + 1] != b"terrain.8" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if base[OFF_S00 - 8:OFF_S00 + 1] != b"terrain.8" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b, off_s in ((0x5CD4, 0x5DC4), (0x5CDC, 0x5ECC)):
    if struct.unpack_from("<H", base, off_b)[0] != 8:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 8")
    if base[off_s:off_s + 2] != "8".encode("utf-16-le"):
        erreur(f"VERSIONINFO chaîne @{off_s:#x} != '8'")

# le correctif FindWindowW de terrain.6 en place
OFF_SUP33 = rva2off(0x544F)
if bytes(base[OFF_SUP33:OFF_SUP33 + 9]) != bytes.fromhex("488d0d3cd6ffff31d2"):
    erreur("sup-33 @0x544f : correctif FindWindowW absent")

# la table : 27 entrées + terminateur, toutes vertes sur terrain.8
table_off = rva2off(R10_TABLE_RVA)
entrees, idx_term = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(base, rva, ln) != sm:
        erreur(f"terrain.8 : R10[{k}] ROUGE avant patch")

# quelles entrées couvrent les octets qu'on va toucher ?
touches = [(0x2ADA, 1, "L00 '9'"), (0x4366, 1, "S00 '9'"),
           (0x70D4, 2, "VERSIONINFO bin 1"), (0x70DC, 2, "VERSIONINFO bin 2"),
           (0x71C4, 2, "VERSIONINFO str 1"), (0x72CC, 2, "VERSIONINFO str 2")]
couvreurs = set()
for k, (rva, ln, sm) in enumerate(entrees):
    for (arva, aln, lab) in touches:
        if not (rva + ln <= arva or arva + aln <= rva):
            print(f"[couv] R10[{k}] (rva={rva:#x} len={ln:#x}) couvre {lab}")
            couvreurs.add(k)
if couvreurs != {23}:
    erreur(f"couvreurs {sorted(couvreurs)} != {{23}} attendu (S00 seul)")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# (a) génération : terrain.8 -> terrain.9 (un octet chacun)
img[OFF_L00] = ord("9")
img[OFF_S00] = ord("9")

# (b) VERSIONINFO 0.5.9.0
struct.pack_into("<H", img, 0x5CD4, 9)
struct.pack_into("<H", img, 0x5CDC, 9)
img[0x5DC4:0x5DC6] = "9".encode("utf-16-le")
img[0x5ECC:0x5ECE] = "9".encode("utf-16-le")

# (c) somme R10[23] recalculée sur l'image finale
rva23, ln23, _ = entrees[23]
struct.pack_into("<Q", img, table_off + 16 * 23 + 8, somme_zone(img, rva23, ln23))

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné (6 octets de version + 8 octets de somme)
autorise = [(OFF_L00, OFF_L00 + 1), (OFF_S00, OFF_S00 + 1),
            (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
            (0x5DC4, 0x5DC6), (0x5ECC, 0x5ECE),
            (table_off + 16 * 23 + 8, table_off + 16 * 23 + 16)]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorise)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés (6 version + somme R10[23]), tous bornés")

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

# 3d. le kit embarqué inchangé byte pour byte (hors octets de version)
if img[0x6400:] != base[0x6400:]:
    erreur("le .blob (demo.10 + proxy + annexe jetons) a bougé")
print("[blob] demo.10 + proxy.exe + annexe jetons : inchangés byte pour byte")

# 3e. identité
if img[OFF_L00 - 8:OFF_L00 + 1] != b"terrain.9" or img[OFF_S00 - 8:OFF_S00 + 1] != b"terrain.9":
    erreur("versions L00/S00 finales inattendues")
for off_b, off_s in ((0x5CD4, 0x5DC4), (0x5CDC, 0x5ECC)):
    if struct.unpack_from("<H", img, off_b)[0] != 9 or img[off_s:off_s + 2] != "9".encode("utf-16-le"):
        erreur(f"VERSIONINFO finale inattendue @{off_b:#x}")
print("[ident] L00/S00 « terrain.9 », VERSIONINFO 0.5.9.0")

# 3f. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
