#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52b — Forensique ASLR vs relocations + desassemblement de l'entree.

Theorie a confondre : DllCharacteristics=0x160 (DYNAMIC_BASE + HIGH_ENTROPY_VA)
force l'ASLR, mais BASERELOC ne couvre qu'UNE entree -> toute adresse absolue
0x1400xxxx non relogee pointe dans le vide apres rebasage -> 0xC0000005
module unknown (RIP hors modules). L'emulateur mappe a la base preferee
(0x140000000) -> tout parait vert. demo.exe (qui MARCHE) n'a pas DYNAMIC_BASE.

Etapes :
  A. dump BASERELOC complet superviseur + demo + DllCharacteristics demo ;
  B. inventaire de TOUTES les adresses absolues 0x1400xxxxx presentes dans
     .text/.text2 (via capstone) et .data/.rdata (QWORDs) ;
  C. couverture reloc : combien sont protegees ;
  D. desassemblement de l'entree (RVA 0x1400, 0x120 octets) instruction
     par instruction, avec annotation des adresses absolues ;
  E. detail des 6 descripteurs : noms, slots, recouvrements FT/OFT.
"""

import pathlib
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SUP = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe")
DEM = pathlib.Path("/home/z/my-project/triade/demo/demo.exe")


def pe_info(path):
    d = path.read_bytes()
    e = struct.unpack_from("<I", d, 0x3C)[0]
    coff = e + 4
    machine, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", d, coff)
    opt = coff + 20
    entry = struct.unpack_from("<I", d, opt + 16)[0]
    base = struct.unpack_from("<Q", d, opt + 24)[0]
    dllc = struct.unpack_from("<H", d, opt + 70)[0]
    ndirs = struct.unpack_from("<I", d, opt + 108)[0]
    dirs = {}
    for i in range(ndirs):
        rva, sz = struct.unpack_from("<II", d, opt + 112 + 8 * i)
        dirs[i] = (rva, sz)
    secs = []
    so = opt + opt_sz
    for i in range(nsec):
        o = so + 40 * i
        nom = d[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        fl = struct.unpack_from("<I", d, o + 36)[0]
        secs.append((nom, va, vs, ra, rs, fl))
    return d, base, entry, dllc, dirs, secs


def rva2off(secs, rva):
    for nom, va, vs, ra, rs, _ in secs:
        if va <= rva < va + max(vs, rs):
            return ra + (rva - va)
    return None


def dump_relocs(nom_f, d, dirs, secs):
    print(f"\n=== [{nom_f}] BASERELOC ===")
    rva, sz = dirs[5]
    if not rva:
        print("  (aucune table de relocations)")
        return set()
    off = rva2off(secs, rva)
    fin = off + sz
    patchs = set()
    while off < fin:
        page, bloc = struct.unpack_from("<II", d, off)
        if bloc == 0:
            break
        n = (bloc - 8) // 2
        for i in range(n):
            e16 = struct.unpack_from("<H", d, off + 8 + 2 * i)[0]
            typ, ofs = e16 >> 12, e16 & 0xFFF
            if typ == 0:
                continue
            patchs.add(page + ofs)
            print(f"  page {page:#x} +{ofs:#04x} -> RVA {page + ofs:#x} "
                  f"type {typ} ({'DIR64' if typ == 10 else 'HIGHLOW' if typ == 3 else '?'})")
        off += bloc
    print(f"  => {len(patchs)} adresses relogees au total")
    return patchs


def dump_dllchars(nom_f, dllc):
    bits = {0x0020: "HIGH_ENTROPY_VA", 0x0040: "DYNAMIC_BASE",
            0x0100: "NX_COMPAT", 0x0400: "NO_SEH", 0x4000: "GUARD_CF",
            0x8000: "TERMINAL_SERVER_AWARE"}
    actifs = [n for b, n in bits.items() if dllc & b]
    print(f"[{nom_f}] DllCharacteristics={dllc:#06x} -> {', '.join(actifs) if actifs else 'aucun'}")


# ============ A. comparison superviseur vs demo ============
d_sup, b_sup, e_sup, dc_sup, dirs_sup, secs_sup = pe_info(SUP)
d_dem, b_dem, e_dem, dc_dem, dirs_dem, secs_dem = pe_info(DEM)
print("=== A. comparaison des drapeaux chargeur ===")
dump_dllchars("superviseur", dc_sup)
dump_dllchars("demo      ", dc_dem)
patchs_sup = dump_relocs("superviseur", d_sup, dirs_sup, secs_sup)
patchs_dem = dump_relocs("demo", d_dem, dirs_dem, secs_dem)

print(f"[superviseur] base={b_sup:#x} entry={e_sup:#x}")
print(f"[demo       ] base={b_dem:#x} entry={e_dem:#x}")

# ============ B. adresses absolues dans le code ============
print("\n=== B. inventaire des adresses absolues 0x1400xxxxx ===")


def scan_absolu(nom_f, d, secs, base, size_img):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = False
    total = []
    for snom, va, vs, ra, rs, fl in secs:
        if not (fl & 0x20000000):  # pas executable -> pas du code
            continue
        code = d[ra:ra + rs]
        for ins in md.disasm(code, va):
            txt = ins.op_str
            if "0x140" not in txt:
                continue
            for tok in txt.replace(",", " ").split():
                if tok.startswith("0x14"):
                    try:
                        v = int(tok, 16)
                    except ValueError:
                        continue
                    if base <= v < base + size_img:
                        total.append((ins.address, v, ins.mnemonic + " " + txt))
    return total


def scan_data(nom_f, d, secs, base, size_img):
    """QWORDs dans .data/.rdata pointant dans l'image."""
    res = []
    for snom, va, vs, ra, rs, fl in secs:
        if fl & 0x20000000:  # executable -> ignore ici
            continue
        for o in range(0, rs - 7, 8):
            v = struct.unpack_from("<Q", d, ra + o)[0]
            if base <= v < base + size_img:
                res.append((va + o, v))
    return res


img_sup = struct.unpack_from("<I", d_sup, 0)  # placeholder
_, _, _, _, _, _, opt_sz_sup = struct.unpack_from("<HHIIIHH", d_sup,
                                                  struct.unpack_from("<I", d_sup, 0x3C)[0] + 4)
size_img_sup = struct.unpack_from(
    "<I", d_sup, struct.unpack_from("<I", d_sup, 0x3C)[0] + 24 + 56)[0]

abs_code = scan_absolu("superviseur", d_sup, secs_sup, b_sup, size_img_sup)
abs_data = scan_data("superviseur", d_sup, secs_sup, b_sup, size_img_sup)
print(f"  code : {len(abs_code)} instructions avec operande absolu dans l'image")
for ad, v, t in abs_code[:40]:
    reloc = "RELOC" if ad in patchs_sup else "!!! NON-RELOGEE"
    print(f"    RVA {ad:#07x}: {t:<44} -> {v:#x}  {reloc}")
if len(abs_code) > 40:
    print(f"    ... et {len(abs_code) - 40} autres")
print(f"  data : {len(abs_data)} QWORDs pointant dans l'image")
couv_d = sum(1 for ad, _ in abs_data if ad in patchs_sup)
print(f"           dont {couv_d} relogees / {len(abs_data)} "
      f"({len(abs_data) - couv_d} NON relogees)")
for ad, v in abs_data[:25]:
    reloc = "RELOC" if ad in patchs_sup else "!!! NON-RELOGEE"
    print(f"    RVA {ad:#07x} -> {v:#x}  {reloc}")
if len(abs_data) > 25:
    print(f"    ... et {len(abs_data) - 25} autres")

# ============ D. desassemblement entree superviseur ============
print(f"\n=== D. entree superviseur (RVA {e_sup:#x}) ===")
md = Cs(CS_ARCH_X86, CS_MODE_64)
ra_text = None
for snom, va, vs, rao, rs, fl in secs_sup:
    if va <= e_sup < va + vs:
        ra_text = rao + (e_sup - va)
        break
code_entree = d_sup[ra_text:ra_text + 0x140]
for ins in md.disasm(code_entree, e_sup):
    marque = ""
    if "0x140" in ins.op_str:
        marque = "   <== ABSOLU"
    print(f"  {ins.address:#07x}: {ins.mnemonic:<10} {ins.op_str}{marque}")
    if ins.address - e_sup > 0x120:
        break

sys.exit(0)
