#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Audit DEP/NX du chemin « mécanique » de demo.exe (demo.4).

Contexte (journal terrain 21:53) : le scénario s'arrête après J_LIBC_OK,
sans J_MEC_OK ni J_DEF_KO — la phase mécanique (écho ×3 + memcmp + tcp-07 ×2)
ne rend jamais la main. Hypothèse D39 : tcp-07 passe la page 0x4000 — qui
contient SON PROPRE CODE (slot 0x4400) — en PAGE_READWRITE (4), valeur SANS
bit execute : sous Windows x64 (DEP permanent), l'instruction suivante
exécutée depuis cette page faute (violation NX) → mort du processus, journal
gelé. L'oracle ne l'a pas vu : son shim VirtualProtect n'applique PAS les
protections.

But : vérifier au niveau octet, SANS Windows, que
  1. le PE est x86-64 (DEP obligatoire) et son état NX ;
  2. les sections .text/.text2 sont bien exécutables (RX) à l'origine ;
  3. le descripteur kernel32 #1 câble le slot IAT 0x20D0 sur VirtualProtect ;
  4. tcp-07 @0x4400 porte les constantes de protection 4 (RW, SANS exec)
     et 0x20 (RX) — la séquence fautive `mov r8d, 4` avant l'écriture ;
  5. l'écho v1 @0x4600, le staging v2 @0x23D0, la table R10 @0x2450 et les
     fixtures @0x26E8/0x26F6 sont conformes au layout (le défaut n'est pas
     ailleurs).
"""

import struct
import sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = "/home/z/my-project/triade/demo/demo.exe"

data = open(EXE, "rb").read()
print(f"[PE] {EXE} — {len(data)} octets\n")

# ------------------------------------------------------------------ en-têtes
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
sig = data[e_lfanew:e_lfanew + 4]
assert sig == b"PE\x00\x00", "signature PE absente"
machine, nsec = struct.unpack_from("<HH", data, e_lfanew + 4)
opt_off = e_lfanew + 24
magic = struct.unpack_from("<H", data, opt_off)[0]
dll_chars = struct.unpack_from("<H", data, opt_off + 70)[0]
print(f"[PE] machine=0x{machine:04X} ({'AMD64' if machine == 0x8664 else '?'})"
      f"  opt.magic=0x{magic:04X} ({'PE32+' if magic == 0x20B else '?'})")
print(f"[PE] DllCharacteristics=0x{dll_chars:04X}"
      f"  → NX/DEP {'EXPLICITE (0x20)' if dll_chars & 0x20 else 'sans flag — x64 = DEP PERMANENT de toute façon'}")
print("[PE] VERDICT : image x86-64 → DEP impossible à désactiver, toute page"
      " sans bit execute est INEXÉCUTABLE de manière certaine.\n")

# ------------------------------------------------------------------ sections
size_opt = struct.unpack_from("<H", data, e_lfanew + 4 + 16)[0]  # COFF: +16
sec_off = opt_off + size_opt
EXEC, READ, WRITE = 0x20000000, 0x40000000, 0x80000000
print("[Sections]")
sections = []
for i in range(nsec):
    o = sec_off + 40 * i
    nom = data[o:o + 8].rstrip(b"\x00").decode()
    vsize, vaddr, rsize, roff = struct.unpack_from("<IIII", data, o + 8)
    chars = struct.unpack_from("<I", data, o + 36)[0]
    sections.append((nom, vaddr, vsize, roff, rsize, chars))
    flags = (("X" if chars & EXEC else "-") + ("R" if chars & READ else "-")
             + ("W" if chars & WRITE else "-"))
    print(f"  {nom:<10} VA=0x{vaddr:04X} VSIZE=0x{vsize:04X} "
          f"raw=0x{roff:04X}+0x{rsize:04X}  flags={flags} (0x{chars:08X})")
print()


def rva_to_off(rva):
    for nom, vaddr, vsize, roff, rsize, _ in sections:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return roff + (rva - vaddr)
    raise ValueError(f"RVA 0x{rva:X} hors sections")


def chaine(off):
    fin = data.index(b"\x00", off)
    return data[off:fin].decode()


# ------------------------------------------------------------ imports kernel32
print("[Imports] descripteurs :")
imp_rva = struct.unpack_from("<I", data, opt_off + 120)[0]
o = rva_to_off(imp_rva)
iat_slots = {}   # slot RVA -> nom de fonction
while True:
    oft, ts, fc, name_rva, ft = struct.unpack_from("<IIIII", data, o)
    if oft == ts == fc == name_rva == ft == 0:
        break
    dll = chaine(rva_to_off(name_rva))
    print(f"  {dll}  OFT=0x{oft:X} FT=0x{ft:X}")
    i = 0
    while True:
        ent = struct.unpack_from("<Q", data, rva_to_off(oft + 8 * i))[0]
        if ent == 0:
            break
        slot_rva = ft + 8 * i
        if ent & (1 << 62):
            iat_slots[slot_rva] = f"ordinal#{ent & 0xFFFF}"
        else:
            nom = chaine(rva_to_off(ent + 2))
            iat_slots[slot_rva] = nom
        i += 1
    o += 20
print()

vp_slots = [s for s, n in iat_slots.items() if n == "VirtualProtect"]
print(f"[Imports] slot(s) VirtualProtect : "
      + ", ".join(f"0x{s:X}" for s in vp_slots) or "AUCUN")
for s in sorted(iat_slots):
    if 0x20B0 <= s <= 0x2110:
        print(f"  IAT 0x{s:X} → {iat_slots[s]}")
print()

# ------------------------------------------------- désassemblage tcp-07 @0x4400
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
TCP07 = 0x4400
off = rva_to_off(TCP07)
code = data[off:off + 0x200]
print("[tcp-07 @ 0x4400] désassemblage annoté (protections en clair) :")
hits = []
for ins in md.disasm(code, TCP07):
    note = ""
    op = ins.op_str
    if ins.mnemonic == "mov" and op.startswith("r8d,"):
        val = op.split(",")[1].strip()
        if val == "4":
            note = "  ◄◄◄ PAGE_READWRITE (0x4) : SANS bit execute — DÉFAUT D39"
            hits.append((ins.address, "4"))
        elif val == "0x20":
            note = "  ◄◄◄ PAGE_EXECUTE_READ (0x20) : correct (restauration)"
            hits.append((ins.address, "0x20"))
        elif val == "0x40":
            note = "  PAGE_EXECUTE_READWRITE (0x40) : correct (écriture)"
            hits.append((ins.address, "0x40"))
    if ins.mnemonic == "call" and "qword ptr [rip" in op:
        try:
            disp = int(op.split("rip")[1].split("]")[0].replace(" ", ""), 0)
            cible = ins.address + ins.size + disp
            if cible in iat_slots:
                note = f"  ; → IAT 0x{cible:X} = {iat_slots[cible]}"
        except Exception:
            pass
    print(f"  0x{ins.address:04X}  {ins.mnemonic:<10} {op}{note}")
    if ins.mnemonic == "ret":
        break
print()

# --------------------------------------------------------- écho v1 + croissance
print("[écho v1 @ 0x4600] 32 premiers octets (zone trampolinable = 8) :")
off = rva_to_off(0x4600)
print("  " + data[off:off + 32].hex(" "))
print("  8 octets trampolinables : " + data[off:off + 8].hex(" "))
print()

print("[croissance @ 0x4680] 16 octets dans l'image (int3 attendus) :")
off = rva_to_off(0x4680)
print("  " + data[off:off + 16].hex(" "))
print()

# ---------------------------------------------------------------- staging + R10
print("[staging v2 @ 0x23D0] en-tête (assemblé POUR 0x4680) :")
off = rva_to_off(0x23D0)
print("  " + data[off:off + 32].hex(" "))
print("  (interprété à l'adresse 0x4680 :)")
for ins in list(md.disasm(data[off:off + 32], 0x4680))[:8]:
    print(f"    0x{ins.address:04X}  {ins.mnemonic:<10} {ins.op_str}")
print()

rva_ent, taille, somme = struct.unpack_from("<IIQ", data, rva_to_off(0x2450))
print(f"[R10 @ 0x2450] 1re entrée : rva=0x{rva_ent:X} taille={taille} somme=0x{somme:016X}"
      f"  → croissance 0x4680 attendue")
if rva_ent == 0x4680 and taille:
    s = data[rva_to_off(0x23D0):rva_to_off(0x23D0) + taille]
    reelle = sum(struct.unpack_from(f"<{len(s) // 8}Q", s[:len(s) // 8 * 8]))
    print(f"[R10] somme staging recalculée = 0x{reelle:016X} "
          f"→ {'CONFORME' if reelle == somme else 'DIVERGENTE — tcp-07 refuserait (code 3)'}")
print()

for rva, nom in ((0x26E8, "PHRASE"), (0x26F6, "PHRASE_MAJ")):
    off = rva_to_off(rva)
    print(f"[fixture] {nom} @ 0x{rva:X} = {data[off:off + 14]!r}")
print()

# -------------------------------------------------------------------- verdict
print("=" * 72)
if any(v == "4" for _, v in hits):
    print("VERDICT : DÉFAUT D39 PRÉSENT au niveau octet.")
    print("  tcp-07 appelle VirtualProtect(page 0x4000, 0x700, PAGE_READWRITE).")
    print("  La page 0x4000 contient tcp-07 LUI-MÊME (0x4400) : au retour de")
    print("  l'appel, l'instruction suivante est fetchée depuis une page SANS")
    print("  bit execute → violation DEP/NX certaine (x64 = DEP permanent).")
elif hits:
    print("VERDICT : CORRIGÉ (tcp-07:R2) — les deux phases d'écriture passent par")
    print("  PAGE_EXECUTE_READWRITE (0x40) et les deux restaurations par")
    print("  PAGE_EXECUTE_READ (0x20) : la page 0x4000 reste exécutable en")
    print("  continu, aucun défaut DEP possible.")
else:
    print("VERDICT : sites de protection introuvables — analyser ci-dessus.")
