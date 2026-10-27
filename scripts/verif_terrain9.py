#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_terrain9 — contrôle INDÉPENDANT de superviseur-terrain9.exe.

Aucune confiance accordée à patch_terrain9.py : tout est re-dérivé du
binaire (leçon D51 : jamais vérifier par le plan, toujours par l'en-tête ;
leçon D56 : lire les structures JUSQU'AU TERMINATEUR).

Contrôles :
  1. porte R10 : table relue jusqu'au terminateur rva==0, sommes u64
     recalculées par le même algorithme que win-06, 27/27 attendues ;
  2. versions : L00/S00 « terrain.9 » dans leurs contextes, VERSIONINFO
     binaire (2 x u16 == 9) et chaînes UTF-16 (« 9 ») ;
  3. kit embarqué : demo.10 (md5 cf72462d…) et proxy.exe (md5 8740e1ca…)
     extraits du .blob et empreintés ;
  4. correctif FindWindowW @0x544f : octets exacts ;
  5. diff vs terrain.8 : EXACTEMENT 7 octets, dans les zones autorisées ;
  6. cohérence chargeur : SizeOfHeaders >= fin de la table des sections.
"""
import hashlib
import pathlib
import struct
import sys

LIVR = pathlib.Path("/home/z/my-project/triade/terrain/livraison")
T8 = (LIVR / "superviseur-terrain8.exe").read_bytes()
T9 = (LIVR / "superviseur-terrain9.exe").read_bytes()

MD5_TERRAIN9 = "a59931db4e3bfc14a29e927a79cc73ca"
MD5_DEMO10 = "cf72462dc130aa4753a2fe5e78f06a08"
MD5_PROXY = "8740e1ca0dbd5967c27cf92bdf713be4"

def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if 0x2000 <= rva < 0x3000:
        return 0x1400 + (rva - 0x2000)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if 0x4000 <= rva < 0x6E00:
        return 0x2e00 + (rva - 0x4000)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None

def somme(data, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s

echecs = 0
def ok(nom, cond, detail=""):
    global echecs
    print(f"  [{'OK ' if cond else 'KO '}] {nom}" + (f" — {detail}" if detail else ""))
    if not cond:
        echecs += 1

print("[1] porte R10 (table jusqu'au terminateur)")
tbl = rva2off(0x2450)
k, vertes = 0, 0
while True:
    rva, ln, sm = struct.unpack_from("<IIQ", T9, tbl + 16 * k)
    if rva == 0:
        break
    if somme(T9, rva, ln) == sm:
        vertes += 1
    k += 1
    if k > 60:
        print("  [KO ] table sans terminateur")
        echecs += 1
        break
ok("27 entrées + terminateur", k == 27, f"{k} lues")
ok("27/27 sommes VERTES", vertes == 27, f"{vertes} vertes")
ok("version u64 @0x2628 >= 0x30000",
   struct.unpack_from("<Q", T9, rva2off(0x2628))[0] >= 0x30000,
   f"0x{struct.unpack_from('<Q', T9, rva2off(0x2628))[0]:x}")

print("[2] versions")
oL, oS = rva2off(0x2ADA), rva2off(0x4366)
ok("L00 « terrain.9 »", T9[oL - 8:oL + 1] == b"terrain.9" and T9[oL + 1:oL + 4] == b"L01")
ok("S00 « terrain.9 »", T9[oS - 8:oS + 1] == b"terrain.9" and T9[oS + 1:oS + 4] == b"S01")
ok("VERSIONINFO binaire 0.5.9.0",
   struct.unpack_from("<H", T9, 0x5CD4)[0] == 9 and struct.unpack_from("<H", T9, 0x5CDC)[0] == 9)
ok("VERSIONINFO chaînes « 9 »",
   T9[0x5DC4:0x5DC6] == "9".encode("utf-16-le") and T9[0x5ECC:0x5ECE] == "9".encode("utf-16-le"))

print("[3] kit embarqué (.blob)")
tailles = struct.unpack_from("<QQ", T9, 0x6400)
ok("en-tête blob 16384/19456", tailles == (16384, 19456))
demo = T9[0x6410:0x6410 + 16384]
proxy = T9[0x6410 + 16384:0x6410 + 16384 + 19456]
ok("demo.10 byte-exact", hashlib.md5(demo).hexdigest() == MD5_DEMO10, hashlib.md5(demo).hexdigest()[:12])
ok("proxy.exe byte-exact", hashlib.md5(proxy).hexdigest() == MD5_PROXY, hashlib.md5(proxy).hexdigest()[:12])
ok("annexe jetons présente", len(T9) - (0x6410 + 16384 + 19456) > 0,
   f"{len(T9) - (0x6410 + 16384 + 19456)} octets")

print("[4] correctif FindWindowW (D55)")
ok("sup-33 @0x544f par CLASSE",
   T9[rva2off(0x544F):rva2off(0x544F) + 9] == bytes.fromhex("488d0d3cd6ffff31d2"))

print("[5] diff terrain.8 -> terrain.9")
diffs = [i for i in range(len(T8)) if T8[i] != T9[i]]
zones = [(rva2off(0x2ADA), 1), (rva2off(0x4366), 1),
         (0x5CD4, 2), (0x5CDC, 2), (0x5DC4, 2), (0x5ECC, 2),
         (rva2off(0x2450) + 16 * 23 + 8, 8)]
bornes = all(any(a <= i < a + l for a, l in zones) for i in diffs)
ok("exactement 7 octets", len(diffs) == 7, f"{len(diffs)} : {[hex(i) for i in diffs]}")
ok("tous dans les zones autorisées", bornes)

print("[6] règle chargeur (D50)")
e_lfanew = struct.unpack_from("<I", T9, 0x3C)[0]
nsec = struct.unpack_from("<H", T9, e_lfanew + 6)[0]
so = e_lfanew + 24 + struct.unpack_from("<H", T9, e_lfanew + 20)[0]
fin_secs = so + 40 * nsec
soh = struct.unpack_from("<I", T9, e_lfanew + 24 + 60)[0]
ok("SizeOfHeaders couvre la table des sections", soh >= fin_secs,
   f"SizeOfHeaders=0x{soh:x}, fin sections=0x{fin_secs:x}")

ok("empreinte terrain.9", hashlib.md5(T9).hexdigest() == MD5_TERRAIN9,
   hashlib.md5(T9).hexdigest())

print()
if echecs:
    print(f"VERDICT : {echecs} contrôle(s) KO")
    sys.exit(1)
print("VERDICT : TOUT CONFORME — terrain.9 prêt à la livraison")
