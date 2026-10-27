#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recon_terrain14 — inspection du binaire terrain.13 pour préparer le
correctif T3 « la preuve survit » (D67b).

Faits établis (D66 + run 23:07 + capture 23:47) :
  - S33 ÉCHEC : 4 branches distinctes convergent vers .jeton_ko (0x6113)
    sans qu'aucune ne dise LAQUELLE a échoué (spawn ? code≠0 ? json absent ?
    jeton introuvable ?).
  - Le nettoyage sup-35 (.nettoyage, r13d=5 noms depuis NOM_REQ) supprime
    terrain_req.txt ET terrain_jeton.json sur TOUT chemin de sortie — la
    commande fallback du LISEZMOI-terrain13 (curl --data @terrain_req.txt)
    était donc IMPOSSIBLE à exécuter après un run.
Ce script RELIT le binaire livré (md5 8d1938b1…) pour :
  R1. sections + caractéristiques (la zone 0x4000-0x6E00 est-elle exécutable ?) ;
  R2. désassembler le slot sup-35 (rva 0x5e00..0x62c0) — confirmer les 4
      branches vers 0x6113, le bloc .jeton_ko, .nettoyage (mov r13d,5), les
      lea des noms (jeton/meta/session) ;
  R3. dumper le bloc des noms (rva 0x6300..0x6370) ;
  R4. cartographier l'espace libre (plages de zéros/NOP) dans 0x62b0..0x6e00 ;
  R5. relire la table R10 (entrées couvrant les zones à toucher) ;
  R6. valeur image initiale du slot code-sortie curl (rva 0x3b50).
Aucune modification — lecture seule.
"""

import hashlib
import pathlib
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

REPO = pathlib.Path("/home/z/my-project/triade")
EXE = REPO / "terrain/livraison/superviseur-terrain13.exe"
MD5_ATTENDU = "8d1938b179d0dd8779fb8b2a82b17921"

data = EXE.read_bytes()
md5 = hashlib.md5(data).hexdigest()
print(f"[id] {EXE.name} : {len(data)} octets, md5 {md5}"
      f" {'OK' if md5 == MD5_ATTENDU else 'INATTENDU !'}")

# ---------------------------------------------------------------- R1 sections
pe = pefile.PE(data=bytes(data), fast_load=True)
print("\n[R1] sections :")
for s in pe.sections:
    name = s.Name.rstrip(b"\x00").decode(errors="replace")
    flags = []
    if s.Characteristics & 0x20000000:
        flags.append("EXEC")
    if s.Characteristics & 0x40000000:
        flags.append("READ")
    if s.Characteristics & 0x80000000:
        flags.append("WRITE")
    print(f"  {name:<10} rva {s.VirtualAddress:#08x}.."
          f"{s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):#08x}"
          f"  vsize {s.Misc_VirtualSize:#x}  raw {s.SizeOfRawData:#x}"
          f"  [{'/'.join(flags)}]")

# ------------------------------------------------------------------ rva -> off
def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.SizeOfRawData:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None

# ------------------------------------------------------------- R2 sup-35 slot
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

LABELS = {0x6113: ".jeton_ko", 0x612c: ".session_ko", 0x6145: ".jetons_absents",
          0x615c: ".ko", 0x6176: ".nettoyage", 0x6183: ".nettoie",
          0x619a: ".nom_len", 0x618e: ".compte_nom", 0x61b8: ".gab",
          0x627b: ".fin", 0x6268: ".append"}

print("\n[R2] sup-35 slot rva 0x5e00..0x62c0 — branches vers .jeton_ko + nettoyage :")
cur = 0x5e00
off = rva2off(cur)
code = data[off:off + (0x62c0 - 0x5e00)]
branches_vers_ko = []
for insn in md.disasm(code, cur):
    tag = ""
    if insn.address in LABELS:
        tag = f"  <<< {LABELS[insn.address]}"
    # repérer les sauts vers 0x6113
    if insn.mnemonic in ("je", "jne", "jmp", "jb", "jae") :
        try:
            cible = int(insn.op_str.split()[-1], 16)
        except ValueError:
            cible = None
        if cible == 0x6113:
            branches_vers_ko.append((insn.address, insn.mnemonic, insn.bytes.hex()))
            tag += f"   *** BRANCHE -> .jeton_ko (classe {len(branches_vers_ko)})"
    if insn.mnemonic == "mov" and "r13d, 5" in insn.op_str:
        tag += "   *** NETTOYAGE : 5 fichiers"
    # n'afficher que la zone utile : tout le slot, compact
    print(f"  {insn.address:#06x}: {insn.bytes.hex():<20} "
          f"{insn.mnemonic:<8} {insn.op_str}{tag}")

print(f"\n[R2b] branches vers .jeton_ko : {[(hex(a), m) for a, m, _ in branches_vers_ko]}")

# ------------------------------------------------------------ R3 bloc de noms
print("\n[R3] bloc de noms rva 0x6300..0x6370 :")
off = rva2off(0x6300)
blob = data[off:off + 0x70]
cur = 0x6300
for nom in blob.split(b"\x00"):
    if nom:
        print(f"  rva {cur:#06x} (+{len(nom) + 1:2d}) : {nom.decode(errors='replace')}")
    cur += len(nom) + 1

# ------------------------------------------------------------- R4 espace libre
print("\n[R4] plages >= 24 octets de zéros dans rva 0x62b0..0x6e00 :")
off = rva2off(0x62b0)
zone = data[off:off + (0x6e00 - 0x62b0)]
run = 0
debut = 0
for i, b in enumerate(zone):
    if b == 0:
        if run == 0:
            debut = i
        run += 1
    else:
        if run >= 24:
            print(f"  rva {0x62b0 + debut:#06x}..{0x62b0 + i - 1:#06x} : {run} zéros")
        run = 0
if run >= 24:
    print(f"  rva {0x62b0 + debut:#06x}..{0x62b0 + len(zone) - 1:#06x} : {run} zéros")

# NOP runs dans le slot sup-35 (padding)
print("[R4b] plages >= 8 octets de NOP (0x90) dans le slot sup-35 :")
off = rva2off(0x5e00)
code_zone = data[off:off + 0x4c0]
run = 0
debut = 0
for i, b in enumerate(code_zone):
    if b == 0x90:
        if run == 0:
            debut = i
        run += 1
    else:
        if run >= 8:
            print(f"  rva {0x5e00 + debut:#06x}..{0x5e00 + i - 1:#06x} : {run} NOP")
        run = 0

# ------------------------------------------------------------------- R5 table
R10_TABLE_RVA = 0x2450
print(f"\n[R5] table R10 @rva {R10_TABLE_RVA:#x} :")
toff = rva2off(R10_TABLE_RVA)
k = 0
entrees = []
while True:
    rva, ln, sm = struct.unpack_from("<IIQ", data, toff + 16 * k)
    if rva == 0:
        break
    entrees.append((rva, ln, sm))
    k += 1
print(f"  {k} entrées")
# zones que terrain.14 toucherait potentiellement
ZONES = {"nettoyage (r13d 5->4)": (0x6176, 0x61b8),
         "bloc noms (réordonnancement)": (0x6313, 0x636b),
         "lea jeton (0x5efc)": (0x5efc, 0x5f04),
         "lea meta (0x5f83)": (0x5f83, 0x5f8b),
         "lea session (0x5ff8)": (0x5ff8, 0x6000),
         "padding fin slot (0x627b..)": (0x627b, 0x62c0),
         "S33 chaîne (0x470e)": (0x470e, 0x4727)}
for lab, (zr, zl) in ZONES.items():
    cov = [i for i, (r, l, _) in enumerate(entrees)
           if not (r + l <= zr or zr + zl <= r)]
    print(f"  {lab:<34} couvert par R10[{cov}]")

# ------------------------------------------------------- R6 slot code sortie
print("\n[R6] slot code-sortie curl sup-35 (rva 0x3b50) :")
off = rva2off(0x3b50)
print(f"  octets image : {data[off:off + 16].hex()}")

# --------------------------------------------------------- annexes : chaînes
print("\n[R7] chaîne S33 exacte @0x470e :")
off = rva2off(0x470e)
fin = data.index(b"\x00", off)
print(f"  {data[off:fin]!r} ({fin - off} octets)")
