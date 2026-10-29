#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.5 — le chargeur ignore encore kernel32#3/user32#2 : réplication
EXACTE du motif .rdata de demo.exe (INT + hints dans .rdata, FT pré-remplie).

CONSTAT TERRAIN (terrain_20261027_162717.txt) :
  terrain.4 ouvre sa fenêtre, S00-S03 loggés (GetLocalTime via kernel32#2
  corrigé fonctionne), puis MORT à l'appel kernel32#3 n°1 du programme :
  DeleteFileA @FT 0x2330 pendant l'extraction (suppression de l'ancienne
  annexe terrain_jetons.bin). Le log s'arrête EXACTEMENT avant S04.

  Les 15 WER de terrain.3 disaient BEX64/c0000005/data 8/+0x0 = saut sur 0.
  terrain.4 a déplacé GetLocalTime mais laissé les OFT de kernel32#3 et
  user32#2 dans une section .idata AVEC des slots FT À ZÉRO dans le fichier.

  demo.exe (référence QUI MARCHE sur cette machine) : 5 descripteurs, TOUS
  avec INT dans .rdata et FT PRÉ-REMPLIE des RVA hints. Les descripteurs
  [0]-[3] du superviseur suivent ce motif et marchent. Les [4]/[5] non.

CORRECTIF terrain.5 (patch chirurgical, ZÉRO octet de code touché) :
  1. INT kernel32#3 (10 qwords) et INT user32#2 (4 qwords) déménagent de
     .idata vers .rdata @0x2B40/0x2B90 (zone libre vérifiée, 832 o à zéro) ;
  2. les hints (0xCB octets) déménagent @0x2BB0, lookups réécrits ;
  3. les FT @0x2300/0x2360 sont PRÉ-REMPLIES avec les RVA hints (le motif
     demo exact — résolution possible par OFT OU par FT) ;
  4. descripteurs [4]/[5] retargetés sur les nouveaux OFT .rdata ;
  5. contenu .idata zéroé (section conservée, plus référencée) ;
  6. VERSIONINFO bumpé 0.5.4.0 -> 0.5.5.0 (4 champs) pour traçabilité WER.

Les zones R10 (.text, .text2 code+données sup, .blob) sont INTACTES par
construction — la porte reste VERTE sans re-scellage.
"""

import hashlib
import pathlib
import struct
import sys

LIVR = pathlib.Path("/home/z/my-project/triade/terrain/livraison")
SRC = LIVR / "superviseur-terrain4.exe"
DST = LIVR / "superviseur-terrain5.exe"

MD5_TERRAIN4 = "283895dbede5245deddffcfd84c1ec32"

# --- géométrie PE (constantes vérifiées par audit indépendant) --------------
RDATA_RVA, RDATA_FILE = 0x2000, 0x1400
TEXT2_RVA, TEXT2_FILE = 0x4000, 0x2e00
BLOB_RVA, BLOB_FILE = 0x8000, 0x6400
IDATA_FILE = 0xF200                      # section .idata raw (0x200 octets)
DESC_FILE = 0x1780                       # tableau descripteurs @RVA 0x2380

FT_K32C = 0x2300                         # 9 slots + terme
FT_U32B = 0x2360                         # 3 slots + terme
INT_K32C_OLD, INT_U32B_OLD = 0x11000, 0x11050   # .idata (terrain.4)
HINTS_OLD, HINTS_END_OLD = 0x11070, 0x1113C     # .idata (terrain.4)
INT_K32C_NEW, INT_U32B_NEW = 0x2B40, 0x2B90     # .rdata libre
HINTS_NEW = 0x2BB0
N_K32C, N_U32B = 9, 3

SLOTS_ATTENDUS = {
    0x2300: "CreateProcessA", 0x2308: "CreatePipe",
    0x2310: "WaitForSingleObject", 0x2318: "GetExitCodeProcess",
    0x2320: "TerminateProcess", 0x2328: "GetLocalTime",
    0x2330: "DeleteFileA", 0x2338: "PeekNamedPipe", 0x2340: "Sleep",
    0x2360: "FindWindowW", 0x2368: "FindWindowExW",
    0x2370: "SendMessageTimeoutW",
    0x2ea0: "GetLocalTime",   # le correctif terrain.4 (kernel32#2)
}


def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if RDATA_RVA <= rva < 0x3000:
        return RDATA_FILE + (rva - RDATA_RVA)
    if TEXT2_RVA <= rva < 0x6E00:
        return TEXT2_FILE + (rva - TEXT2_RVA)
    if BLOB_RVA <= rva < 0x10D10:
        return BLOB_FILE + (rva - BLOB_RVA)
    return None


def mot(data, off):
    return struct.unpack_from("<Q", data, off)[0]


def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)


# =============================================================================
# 1. GARDES-FOUS sur terrain.4 (le binaire source doit être EXACTEMENT attendu)
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(base).hexdigest() != MD5_TERRAIN4:
    erreur("terrain4 : md5 inattendu")

for i, (oft_att, iat_att) in enumerate(((0x11000, 0x2300), (0x11050, 0x2360))):
    oft, _, _, nom, iat = struct.unpack_from("<IIIII", base, DESC_FILE + 20 * (4 + i))
    if (oft, iat) != (oft_att, iat_att):
        erreur(f"descripteur[{4+i}] terrain4 : oft={oft:#x} iat={iat:#x}")

ints_k32c = [mot(base, IDATA_FILE + 8 * j) for j in range(N_K32C + 1)]
ints_u32b = [mot(base, IDATA_FILE + 0x50 + 8 * j) for j in range(N_U32B + 1)]
if ints_k32c[-1] != 0 or ints_u32b[-1] != 0:
    erreur("terminateurs INT manquants dans .idata")
for v in ints_k32c[:N_K32C] + ints_u32b[:N_U32B]:
    if not (HINTS_OLD <= v < HINTS_END_OLD):
        erreur(f"lookup .idata hors hints : {v:#x}")

libre = bytes(base[rva2off(INT_K32C_NEW):rva2off(HINTS_NEW) + (HINTS_END_OLD - HINTS_OLD)])
if libre != b"\x00" * len(libre):
    erreur("zone .rdata cible NON libre")
for rva, n in ((FT_K32C, N_K32C + 1), (FT_U32B, N_U32B + 1)):
    z = bytes(base[rva2off(rva):rva2off(rva) + 8 * n])
    if z != b"\x00" * len(z):
        erreur(f"FT @{rva:#x} non vierge dans terrain4")

hints_old = bytes(base[IDATA_FILE + (HINTS_OLD - 0x11000):
                      IDATA_FILE + (HINTS_OLD - 0x11000) + (HINTS_END_OLD - HINTS_OLD)])
if b"DeleteFileA\x00" not in hints_old or b"SendMessageTimeoutW" not in hints_old:
    erreur("blob hints .idata inattendu")

if struct.unpack_from("<4H", base, 0x5cc8 + 8) != (0, 5, 4, 0):
    erreur("champs FileVersion inattendus")

# =============================================================================
# 2. LE PATCH (copie -> écritures bornées)
# =============================================================================
img = bytearray(base)


def ecrire_rva(rva, blob, nom):
    off = rva2off(rva)
    img[off:off + len(blob)] = blob


def reecris(v):
    return HINTS_NEW + (v - HINTS_OLD) if v else 0


# (a) INT + hints dans .rdata ; FT pré-remplies du même contenu (motif demo)
ecrire_rva(INT_K32C_NEW, b"".join(struct.pack("<Q", reecris(v)) for v in ints_k32c), "INT k32c")
ecrire_rva(INT_U32B_NEW, b"".join(struct.pack("<Q", reecris(v)) for v in ints_u32b), "INT u32b")
ecrire_rva(HINTS_NEW, hints_old, "hints")
ecrire_rva(FT_K32C, b"".join(struct.pack("<Q", reecris(v)) for v in ints_k32c), "FT k32c")
ecrire_rva(FT_U32B, b"".join(struct.pack("<Q", reecris(v)) for v in ints_u32b), "FT u32b")

# (b) descripteurs [4]/[5] : OFT retargetés vers .rdata
struct.pack_into("<I", img, DESC_FILE + 20 * 4 + 0, INT_K32C_NEW)
struct.pack_into("<I", img, DESC_FILE + 20 * 5 + 0, INT_U32B_NEW)

# (c) .idata zéroée (section conservée, plus aucun descripteur ne pointe dessus)
img[IDATA_FILE:IDATA_FILE + 0x200] = b"\x00" * 0x200

# (d) VERSIONINFO 0.5.4.0 -> 0.5.5.0 (4 champs)
struct.pack_into("<H", img, 0x5cd4, 5)              # FileVersion   binaire
struct.pack_into("<H", img, 0x5cdc, 5)              # ProductVersion binaire
img[0x5dc4:0x5dc6] = "5".encode("utf-16-le")        # FileVersion    chaine
img[0x5ecc:0x5ece] = "5".encode("utf-16-le")        # ProductVersion chaine

DST.write_bytes(bytes(img))
print(f"[patch] {DST.name} ecrit ({len(img)} octets)")

# =============================================================================
# 3. POST-VÉRIFICATIONS (fail-closed)
# =============================================================================
# 3a. diff octet à octet : seules les zones autorisées bougent
autorisées = [
    (rva2off(FT_K32C), rva2off(FT_K32C) + 8 * (N_K32C + 1)),          # FT k32c
    (rva2off(FT_U32B), rva2off(FT_U32B) + 8 * (N_U32B + 1)),          # FT u32b
    (DESC_FILE + 80, DESC_FILE + 84), (DESC_FILE + 100, DESC_FILE + 104),  # OFT
    (rva2off(INT_K32C_NEW), rva2off(HINTS_NEW) + len(hints_old)),     # INT+hints
    (IDATA_FILE, IDATA_FILE + 0x200),                                  # .idata
    (0x5cd4, 0x5cd6), (0x5cdc, 0x5cde), (0x5dc4, 0x5dc6), (0x5ecc, 0x5ece),
]
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorisées)]
if hors:
    erreur(f"{len(hors)} octets modifies hors zones autorisees : {[hex(i) for i in hors[:8]]}")
print(f"[verif] diff : {len(diffs)} octets modifies, tous dans les zones autorisees")

# 3b. zones R10 (code .text/.text2 + blob) INTACTES — bornes INCLUSES au
# dernier octet utile (rva2off est à bornes exclusives : passer fin-1)
for rva_debut, rva_fin, nom in ((0x1000, 0x2000, ".text"), (0x4000, 0x6E00, ".text2"),
                                (0x8000, 0x10D10, ".blob")):
    a, b = rva2off(rva_debut), rva2off(rva_fin - 1) + 1
    if bytes(base[a:b]) != bytes(img[a:b]):
        erreur(f"zone R10 {nom} modifiee !")
print("[verif] zones R10 (.text/.text2/.blob) byte-identiques a terrain4 : porte VERTE garantie")

# 3c. re-parse PE complet de terrain5 : resolution depuis l'IMAGE MAPPÉE
data = bytes(img)
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
optsz = struct.unpack_from("<H", data, e_lfanew + 24)[0] + 16 * 2 - 4 - 2
optsz = struct.unpack_from("<H", data, e_lfanew + 20)[0]
nsec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
sec_off = e_lfanew + 24 + optsz
sections = []
for i in range(nsec):
    o = sec_off + 40 * i
    nom_sec = data[o:o + 8].rstrip(b"\0").decode()
    vsz, va, rsz, roff = struct.unpack_from("<IIII", data, o + 8)
    sections.append((nom_sec, va, max(vsz, rsz), roff))

def mappa(rva):
    for nom, va, et, roff in sections:
        if va <= rva < va + et:
            return roff + (rva - va)
    return None

def cstr(off):
    return data[off:data.index(b"\0", off)].decode()

dd = e_lfanew + 24 + 112
imp_rva = struct.unpack_from("<I", data, dd + 8)[0]
slots_resolus, desc_liste = {}, []
off = mappa(imp_rva)
while True:
    oft, ts, fwc, nrva, iat = struct.unpack_from("<IIIII", data, off)
    if oft == 0 and nrva == 0 and iat == 0:
        break
    nom_dll = cstr(mappa(nrva))
    sect_iat = next(n for n, v, e, r in sections if v <= iat < v + e)
    sect_oft = next(n for n, v, e, r in sections if v <= oft < v + e)
    cur = mappa(oft)
    n = 0
    while mot(data, cur) != 0:
        lrva = mot(data, cur) & 0xFFFFFFFF
        nom_fn = cstr(mappa(lrva) + 2)
        slot = iat + 8 * n
        slots_resolus[slot] = nom_fn
        n += 1
        cur += 8
    desc_liste.append((nom_dll, n, sect_oft, sect_iat, iat))
    off += 20

print(f"[verif] {len(desc_liste)} descripteurs :")
for nom_dll, n, so, si, iat in desc_liste:
    print(f"        {nom_dll:14s} n={n:2d} OFT dans {so:7s} FT dans {si} @0x{iat:x}")

for slot, nom in SLOTS_ATTENDUS.items():
    obtenu = slots_resolus.get(slot)
    if obtenu != nom:
        erreur(f"slot {slot:#x} : attendu {nom}, obtenu {obtenu}")
print(f"[verif] les {len(SLOTS_ATTENDUS)} slots appeles par le code resolvent correctement")

# FT pre-remplies == INT (resolution possible par l'un OU l'autre chemin)
for ft, int_rva, n in ((FT_K32C, INT_K32C_NEW, N_K32C + 1),
                       (FT_U32B, INT_U32B_NEW, N_U32B + 1)):
    for j in range(n):
        if mot(data, rva2off(ft) + 8 * j) != mot(data, rva2off(int_rva) + 8 * j):
            erreur(f"FT {ft:#x}[{j}] != INT — pre-remplissage incoherent")
print("[verif] FT pre-remplies coherentes avec les INT (double chemin de resolution)")

# 3d. audit des call-sites : toute indirection rip-relative doit tomber sur un slot couvert
zones_code = ((0x1000, 0x2000, ".text"), (0x4000, 0x6E00, ".text2"))
appelés, inconnus = {}, []
for zrva, zfin, zn in zones_code:
    off_z, fin_z = rva2off(zrva), rva2off(zfin - 1) + 1
    for i in range(off_z, fin_z - 6):
        if data[i] == 0xFF and data[i + 1] in (0x15, 0x25):
            rva_ins = zrva + (i - off_z)
            disp = struct.unpack_from("<i", data, i + 2)[0]
            cible = rva_ins + 6 + disp
            if cible in slots_resolus:
                appelés.setdefault(slots_resolus[cible], []).append(hex(rva_ins))
            else:
                inconnus.append((hex(rva_ins), hex(cible)))
if inconnus:
    erreur(f"call-sites vers slots non couverts : {inconnus[:6]}")
print(f"[verif] {sum(len(v) for v in appelés.values())} call-sites indirects, "
      f"tous sur des slots couverts :")
for fn in sorted(appelés):
    print(f"        {fn:22s} x{len(appelés[fn])}")

# 3e. version
fv = struct.unpack_from("<4H", data, 0x5cc8 + 8)
print(f"[verif] FileVersion terrain5 = {'.'.join(map(str, fv))} (attendu 0.5.5.0)")
if fv != (0, 5, 5, 0):
    erreur("version non bumpée")

# 3f. empreintes
md5 = hashlib.md5(data).hexdigest()
sha = hashlib.sha256(data).hexdigest()
print(f"[final] superviseur-terrain5.exe  md5={md5}")
print(f"[final] superviseur-terrain5.exe  sha256={sha}")
print("OK — terrain5 prete pour la livraison")
