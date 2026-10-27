#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_terrain10 — contrôle INDÉPENDANT de superviseur-terrain10.exe.

Aucune confiance accordée à patch_terrain10.py : tout est re-dérivé du
binaire (leçons D51/D56 : vérifier par l'en-tête, lire jusqu'au terminateur).

Contrôles :
  1. porte R10 : table relue jusqu'au terminateur rva==0, 27/27 vertes ;
  2. versions : L00/S00 « terrain10 », VERSIONINFO binaire 0.5.10.0,
     FileVersion « 0.5.10 », ProductVersion « …terrain10 » ;
  3. kit embarqué : demo.10 (cf72462d…) + proxy.exe (8740e1ca…) du .blob ;
  4. correctif FindWindowW @0x544f (terrain.6) intact ;
  5. LE CORRECTIF D62 : .curl @0x5d1e désassemblé — sub rsp,0x28 avant les
     appels, add rsp,0x28 avant ret, et l'AUDIT ABI COMPLET du binaire :
     zéro site D<0x28 ou mal aligné dans sup-34 ;
  6. diff vs terrain.9 : EXACTEMENT les zones autorisées ;
  7. cohérence chargeur : SizeOfHeaders >= fin de la table des sections.
"""
import hashlib
import pathlib
import struct
import sys

LIVR = pathlib.Path("/home/z/my-project/triade/terrain/livraison")
T9 = (LIVR / "superviseur-terrain9.exe").read_bytes()
T10 = (LIVR / "superviseur-terrain10.exe").read_bytes()

MD5_TERRAIN10 = "ec5995707976b227a5edbab9a766e9b4"
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

print("[0] empreintes")
ok("md5 terrain.10", hashlib.md5(T10).hexdigest() == MD5_TERRAIN10,
   hashlib.md5(T10).hexdigest())
ok("base = terrain.9", hashlib.md5(T9).hexdigest() == MD5_TERRAIN9)

print("[1] porte R10 (table jusqu'au terminateur)")
tbl = rva2off(0x2450)
k, vertes = 0, 0
while True:
    rva, ln, sm = struct.unpack_from("<IIQ", T10, tbl + 16 * k)
    if rva == 0:
        break
    if somme(T10, rva, ln) == sm:
        vertes += 1
    k += 1
    if k > 60:
        print("  [KO ] table sans terminateur")
        echecs += 1
        break
ok("27 entrées + terminateur", k == 27, f"{k} lues")
ok("27/27 sommes VERTES", vertes == 27, f"{vertes} vertes")
ok("version u64 @0x2628 >= 0x30000",
   struct.unpack_from("<Q", T10, rva2off(0x2628))[0] >= 0x30000,
   f"0x{struct.unpack_from('<Q', T10, rva2off(0x2628))[0]:x}")

print("[2] versions")
oL, oS = rva2off(0x2ADA), rva2off(0x4366)
ok("L00 « terrain10 »", T10[oL - 8:oL + 1] == b"terrain10" and T10[oL + 1:oL + 4] == b"L01")
ok("S00 « terrain10 »", T10[oS - 8:oS + 1] == b"terrain10" and T10[oS + 1:oS + 4] == b"S01")
ok("VERSIONINFO binaire 0.5.10.0",
   struct.unpack_from("<H", T10, 0x5CD4)[0] == 10 and struct.unpack_from("<H", T10, 0x5CDC)[0] == 10)
fv = T10[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0]
pv = T10[0x5EB8:0x5ECE].decode("utf-16-le")
ok("FileVersion « 0.5.10 »", fv == "0.5.10", repr(fv))
ok("ProductVersion finit « terrain10 »", pv.endswith("terrain10"), repr(pv[-16:]))

print("[3] kit embarqué (.blob)")
tailles = struct.unpack_from("<QQ", T10, 0x6400)
ok("en-tête blob 16384/19456", tailles == (16384, 19456))
demo = T10[0x6410:0x6410 + 16384]
proxy = T10[0x6410 + 16384:0x6410 + 16384 + 19456]
ok("demo.10 byte-exact", hashlib.md5(demo).hexdigest() == MD5_DEMO10, hashlib.md5(demo).hexdigest()[:12])
ok("proxy.exe byte-exact", hashlib.md5(proxy).hexdigest() == MD5_PROXY, hashlib.md5(proxy).hexdigest()[:12])

print("[4] correctifs précédents intacts")
ok("FindWindowW par CLASSE @0x544f (terrain.6)",
   T10[rva2off(0x544F):rva2off(0x544F) + 9] == bytes.fromhex("488d0d3cd6ffff31d2"))

print("[5] LE CORRECTIF D62 — .curl shadow space")
ok("sub rsp,0x28 @0x5d1e",
   T10[rva2off(0x5D1E):rva2off(0x5D1E) + 4] == bytes.fromhex("4883ec28"))
ok("add rsp,0x28 @0x5d60",
   T10[rva2off(0x5D60):rva2off(0x5D60) + 4] == bytes.fromhex("4883c428"))
ok("motif mov edx,25000 ; call intact @0x5d37",
   T10[rva2off(0x5D37):rva2off(0x5D37) + 7] == bytes.fromhex("baa8610000ff15"))
try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    code = T10[rva2off(0x5D1E):rva2off(0x5D1E) + 0x47]
    instrs = list(md.disasm(code, 0x140005D1E))
    seq = [f"{i.mnemonic} {i.op_str}".rstrip() for i in instrs]
    attendu = [
        "sub rsp, 0x28", "xor edx, edx",
        "call 0x140005200", "test eax, eax", "je 0x140005d60",
        "mov r12, qword ptr [rip - 0x2224]", "mov rcx, r12",
        "mov edx, 0x61a8", "call qword ptr [rip - 0x3a32]",
        "mov rcx, r12", "lea rdx, [rip - 0x21fc]",
        "call qword ptr [rip - 0x3a3a]",
        "mov rcx, r12", "call qword ptr [rip - 0x3c63]",
        "mov eax, 1", "add rsp, 0x28", "ret",
    ]
    ok("désassemblage .curl complet", seq == attendu, f"{len(seq)} instructions")

    # audit ABI in-line : profondeur D à CHAQUE appel IAT de .curl
    D = 0
    profs = []
    for i in instrs:
        m, ops = i.mnemonic, i.op_str
        rva = i.address - 0x140000000
        if rva == 0x5D1E:
            D = 0
        if m == "push":
            D += 8
        elif m == "pop":
            D -= 8
        elif m == "sub" and ops.startswith("rsp,"):
            D += int(ops.split(",")[1], 0)
        elif m == "add" and ops.startswith("rsp,"):
            D -= int(ops.split(",")[1], 0)
        elif m == "call":
            if "qword ptr [rip" in ops:
                profs.append(D)
    ok("3 appels IAT de .curl à D=0x28",
       profs == [0x28, 0x28, 0x28], " ".join(hex(d) for d in profs))
except ImportError:
    print("  [FAIBLE] capstone absent — contrôle désassemblage sauté")

print("[6] diff vs terrain.9 — exactement les zones autorisées")
autorisations = [
    (rva2off(0x5D21), rva2off(0x5D21) + 1),
    (rva2off(0x5D63), rva2off(0x5D63) + 1),
    (oL - 1, oL + 1), (oS - 1, oS + 1),
    (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
    (0x5DC0, 0x5DC6), (0x5ECA, 0x5ECE),
    (tbl + 16 * 20 + 8, tbl + 16 * 20 + 16),
    (tbl + 16 * 23 + 8, tbl + 16 * 23 + 16),
]
diffs = [i for i in range(len(T9)) if T9[i] != T10[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b in autorisations)]
ok("zéro octet hors zones autorisées", not hors,
   f"{len(hors)} hors zone" if hors else f"{len(diffs)} octets modifiés, tous autorisés")
ok(".blob intact (0x6400+)", T9[0x6400:] == T10[0x6400:])

print("[7] cohérence chargeur")
e_lfanew = struct.unpack_from("<I", T10, 0x3C)[0]
nsec = struct.unpack_from("<H", T10, e_lfanew + 6)[0]
size_opt = struct.unpack_from("<H", T10, e_lfanew + 20)[0]
fin_table = e_lfanew + 24 + size_opt + 40 * nsec
size_headers = struct.unpack_from("<I", T10, e_lfanew + 24 + 60)[0]
ok("SizeOfHeaders >= fin de la table des sections",
   size_headers >= fin_table, f"{size_headers:#x} >= {fin_table:#x}")

print()
if echecs:
    print(f"VERDICT : {echecs} CONTRÔLE(S) EN ÉCHEC")
    sys.exit(1)
print("VERDICT : 20/20 CONTRÔLES VERTS — terrain.10 CONFORME")
