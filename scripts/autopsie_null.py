#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52 — Autopsie du crash 0xC0000005 / RIP=0 de superviseur-terrain3.exe.

Hypothese centrale : un slot IAT appele par la chaine de demarrage n'est pas
couvert par un descripteur d'import (FirstThunk) -> le chargeur Windows le
laisse a 0 -> CALL [slot] saute a l'adresse NULL.

Ce script fait la croisee COMPLETE :
  1. dump des 16 data directories (TLS, LOAD_CONFIG, GUARD...) ;
  2. extraction de TOUS les descripteurs d'import et de la couverture
     exacte de slots que le chargeur remplit ;
  3. balayage du code executable (.text) a la recherche de chaque
     CALL/JMP [rip+disp] indirect et resolution du slot vise ;
  4. verdict par slot : COUVERT / NON-COUVERT (reste 0 -> RIP=0) / hors IAT ;
  5. focus sur la chaine de demarrage (offsets < 0x1000 du point d'entree).

100% stdlib, zero pefile (independant des validateurs du projet).
"""

import struct
import sys
import pathlib

CHEMIN = pathlib.Path(
    "/home/z/my-project/triade/terrain/livraison/superviseur-terrain3.exe")
if not CHEMIN.exists():
    CHEMIN = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe")

data = CHEMIN.read_bytes()
print(f"[autopsie] fichier : {CHEMIN} ({len(data):,} octets)".replace(",", " "))

# ---------------- PE headers ----------------
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[e_lfanew:e_lfanew + 4] == b"PE\x00\x00", "signature PE absente"
coff = e_lfanew + 4
machine, nsec, tds, psym, nsym, opt_sz, chars = struct.unpack_from(
    "<HHIIIHH", data, coff)
opt = coff + 20
magic = struct.unpack_from("<H", data, opt)[0]
assert magic == 0x20B, f"magic {magic:#x} != PE32+"
entry_rva = struct.unpack_from("<I", data, opt + 16)[0]
image_base = struct.unpack_from("<Q", data, opt + 24)[0]
sect_align = struct.unpack_from("<I", data, opt + 32)[0]
file_align = struct.unpack_from("<I", data, opt + 36)[0]
size_img = struct.unpack_from("<I", data, opt + 56)[0]
size_hdr = struct.unpack_from("<I", data, opt + 60)[0]
dll_chars = struct.unpack_from("<H", data, opt + 70)[0]
num_dirs = struct.unpack_from("<I", data, opt + 108)[0]

print(f"[PE] machine={machine:#x} sections={nsec} entry RVA={entry_rva:#x} "
      f"base={image_base:#x}")
print(f"[PE] SizeOfImage={size_img:#x} SizeOfHeaders={size_hdr:#x} "
      f"DllCharacteristics={dll_chars:#04x}")
GUARD, DYNBASE, NX = 0x4000, 0x0040, 0x0100
print(f"[PE] GUARD_CF={'OUI' if dll_chars & GUARD else 'non'} "
      f"DYNAMIC_BASE={'OUI' if dll_chars & DYNBASE else 'non'} "
      f"NX_COMPAT={'OUI' if dll_chars & NX else 'non'}")

DIRS = ["EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY", "BASERELOC",
        "DEBUG", "ARCHITECTURE", "GLOBALPTR", "TLS", "LOAD_CONFIG", "BOUND",
        "IAT", "DELAY_IMPORT", "CLR", "RESERVED"]
print("\n[directories]")
dirs = {}
for i in range(num_dirs):
    rva, sz = struct.unpack_from("<II", data, opt + 112 + 8 * i)
    dirs[DIRS[i]] = (rva, sz)
    if rva:
        nom = DIRS[i]
        alerte = "  <-- !!!" if nom in ("TLS", "LOAD_CONFIG") else ""
        print(f"  {nom:<13} RVA={rva:#010x} taille={sz:#x}{alerte}")

# ---------------- sections ----------------
sec_off = opt + opt_sz
sections = []
for i in range(nsec):
    o = sec_off + 40 * i
    nom = data[o:o + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", data, o + 8)
    schars = struct.unpack_from("<I", data, o + 36)[0]
    sections.append((nom, vaddr, vsize, raddr, rsize, schars))
    print(f"[section] {nom:<8} VA={vaddr:#06x} VS={vsize:#06x} "
          f"RAW={raddr:#06x} RS={rsize:#06x} flags={schars:#010x}")

def rva_to_off(rva):
    for nom, vaddr, vsize, raddr, rsize, _ in sections:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    return None

# ---------------- descripteurs d'import ----------------
print("\n[imports] couverture exacte du chargeur Windows")
imp_rva, imp_sz = dirs["IMPORT"]
off = rva_to_off(imp_rva)
slots_couverts = {}   # slot_rva -> (dll, index, nom_fonction)
n_desc = 0
while True:
    oft, tds_, fchain, nomrva, firstthunk = struct.unpack_from(
        "<IIIII", data, off + 20 * n_desc)
    if oft == tds_ == fchain == nomrva == firstthunk == 0:
        break
    dll = data[rva_to_off(nomrva):].split(b"\x00")[0].decode("ascii", "replace")
    print(f"  descripteur #{n_desc}: {dll}  OriginalFirstThunk={oft:#x} "
          f"TimeDateStamp={tds_:#x} Forwarder={fchain:#x} FirstThunk={firstthunk:#x}")
    # le chargeur remplit a partir de FirstThunk (ou OFT si FT=0)
    thunk_rva = oft if firstthunk == 0 else firstthunk
    walk = thunk_rva
    idx = 0
    while True:
        val = struct.unpack_from("<Q", data, rva_to_off(walk))[0]
        if val == 0:
            break
        slot_rva = (firstthunk if firstthunk else oft) + 8 * idx
        if val & (1 << 63):
            fname = f"ordinal#{val & 0xFFFF}"
        else:
            no = rva_to_off(val)
            hint = struct.unpack_from("<H", data, no)[0]
            fname = data[no + 2:].split(b"\x00")[0].decode(
                "ascii", "replace") + f" (hint {hint})"
        slots_couverts[slot_rva] = (dll, idx, fname)
        idx += 1
        walk += 8
    n_desc += 1
print(f"  => {n_desc} descripteurs, {len(slots_couverts)} slots remplis par "
      f"le chargeur")

# ---------------- zone IAT declaree ----------------
iat_rva, iat_sz = dirs["IAT"]
if iat_rva:
    print(f"\n[IAT declaree] RVA={iat_rva:#x} taille={iat_sz:#x} "
          f"(slots {iat_rva:#x}..{iat_rva + iat_sz:#x})")
    couverts_dans_iat = [s for s in slots_couverts
                         if iat_rva <= s < iat_rva + iat_sz]
    print(f"  slots couverts par descripteurs DANS la zone IAT : "
          f"{len(couverts_dans_iat)}")
    trous = [s for s in range(iat_rva, iat_rva + iat_sz, 8)
             if s not in slots_couverts]
    if trous:
        print(f"  !!! TROUS non remplis par le chargeur : "
              f"{[hex(t) for t in trous]}")
        for t in trous:
            # contenu actuel du slot dans le fichier
            o = rva_to_off(t)
            val = struct.unpack_from("<Q", data, o)[0] if o else None
            print(f"     slot {t:#x} : octets fichier = {val:#x}")

# ---------------- balayage du code : CALL/JMP [rip+disp] ----------------
print("\n[code] resolution de tous les appels indirects rip-relatifs")
text = next(s for s in sections if s[0] == ".text")
tva, tsize, traw, trsz = text[1], text[2], text[3], text[4]
code = data[traw:traw + trsz]

appels = []          # (off_fichier, rva, slot_rva, mnemonique)
i = 0
n_null = 0
while i < len(code) - 7:
    b = code[i]
    # FF 15 disp32        call [rip+disp32]
    # FF 25 disp32        jmp  [rip+disp32]
    if b == 0xFF and code[i + 1] in (0x15, 0x25):
        disp = struct.unpack_from("<i", code, i + 2)[0]
        rva_instr = tva + i
        slot = rva_instr + 7 + disp
        mn = "call" if code[i + 1] == 0x15 else "jmp"
        appels.append((traw + i, rva_instr, slot, mn))
        i += 7
        continue
    # 41 FF 15 disp32     call [rip+disp32] avec prefixe REX.B (registre base r8+)
    if b == 0x41 and code[i + 1] == 0xFF and code[i + 2] in (0x15, 0x25):
        disp = struct.unpack_from("<i", code, i + 3)[0]
        rva_instr = tva + i
        slot = rva_instr + 8 + disp
        mn = "call" if code[i + 2] == 0x15 else "jmp"
        appels.append((traw + i, rva_instr, slot, mn))
        i += 8
        continue
    i += 1

print(f"  {len(appels)} appels indirects [rip+disp] trouves dans .text")

def zone(rva):
    for nom, vaddr, vsize, _, _, _ in sections:
        if vaddr <= rva < vaddr + vsize:
            return nom
    return "?hors-sections?"

problemes = []
for off_f, rva, slot, mn in appels:
    z = zone(slot)
    if z in (".idata", "IAT") or (iat_rva and iat_rva <= slot < iat_rva + iat_sz):
        if slot not in slots_couverts:
            problemes.append((off_f, rva, slot, mn, z))
            print(f"  !!! {mn} @RVA {rva:#06x} -> slot {slot:#06x} "
                  f"({z}) NON COUVERT par les descripteurs -> [slot]=0 -> RIP=0")
            n_null += 1

if not problemes:
    print("  tous les slots vises par .text sont couverts par les descripteurs")

# ---------------- chaine de demarrage ----------------
print(f"\n[demarrage] entree = RVA {entry_rva:#x}")
# appels proches de l'entree (les 0x300 premiers octets apres l'entree)
chain = [(o, r, s, m, z) for (o, r, s, m) in appels
         if entry_rva <= r < entry_rva + 0x100]
for off_f, rva, slot, mn in appels:
    if entry_rva <= rva < entry_rva + 0x100:
        couv = slots_couverts.get(slot)
        if couv:
            print(f"  entree+{rva - entry_rva:#04x} {mn} {couv[0]}!"
                  f"{couv[2].split(' (hint')[0]}")
        else:
            print(f"  entree+{rva - entry_rva:#04x} {mn} slot {slot:#x} "
                  f"zone={zone(slot)} NON-COUVERT")

# ---------------- slots dans .data/.idata references hors couverture ----------------
print("\n[verdict] slots IAT NON couverts mais PRESENTS dans le fichier :")
finaux = 0
for slot in sorted(set(s for _, _, s, _ in appels)):
    if slot in slots_couverts:
        continue
    z = zone(slot)
    o = rva_to_off(slot)
    if o is None:
        continue
    val = struct.unpack_from("<Q", data, o)[0]
    ref = sum(1 for _, r, s, _ in appels if s == slot)
    print(f"  slot {slot:#06x} zone={z} valeur-fichier={val:#x} "
          f"references-code={ref}")
    finaux += 1
if finaux == 0 and not problemes:
    print("  aucun — hypothese IAT non confirmee, elargir le diagnostic")

print(f"\n[resume] appels={len(appels)}  problemes-IAT={len(problemes)}")
sys.exit(0)
