#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_iat_curl_terrain8 — la couverture IAT du chemin .curl est-elle réelle ?

Hypothèse (après WER c0000005 data=8 x15 + mort 2/2 au 1er curl T2) :
les slots IAT utilisés par .curl (WaitForSingleObject 0x2310,
GetExitCodeProcess 0x2318) ne sont couverts par AUCUN descripteur
d'importation -> le chargeur Windows ne les résout JAMAIS -> leur valeur
pré-remplie (0 ou RVA hint) est appelée -> exécution mémoire non
exécutable -> c0000005 data=8, RIP=0/« unknown ».

L'oracle ne peut pas voir ce défaut : l'émulateur peuple l'IAT par sa
propre table de noms (leçon D51/D52), pas en marchant les descripteurs.

Ce script parse le PE LIVRÉ (upload/superviseur-terrain8.exe) :
  1. tous les descripteurs d'import (OFT/FT/noms), plages FT couvertes ;
  2. la valeur PRÉ-CHARGEMENT de chaque slot FT (hint-RVA ou 0) ;
  3. la couverture des slots utilisés par .curl / .arret / .attendre ;
  4. les slots appelés par l'image mais hors couverture (le piège).
"""
import pathlib
import struct
import sys

EXE = pathlib.Path("/home/z/my-project/upload/superviseur-terrain8.exe")
data = EXE.read_bytes()
print(f"[exe] {EXE.name} {len(data):,} o")

# --- en-têtes PE ---
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
machine, nsec = struct.unpack_from("<HH", data, e_lfanew + 4)
opt = e_lfanew + 24
magic = struct.unpack_from("<H", data, opt)[0]
assert magic == 0x20B, "pas PE32+"
imp_dir_rva, imp_dir_size = struct.unpack_from("<II", data, opt + 120 - 8 + 8)[:1][0], None
# data directory : import = index 1 (offset 96+8*1 dans les dirs ; optionnel
# commence à opt+112 pour PE32+ ... recalcul propre ci-dessous)
dd_off = opt + 112  # PE32+ : data directories commencent à +112
imp_rva, imp_size = struct.unpack_from("<II", data, dd_off + 8 * 1)
iat_rva, iat_size = struct.unpack_from("<II", data, dd_off + 8 * 12)
print(f"[pe] sections={nsec} import dir rva=0x{imp_rva:x} taille=0x{imp_size:x} "
      f"IAT dir rva=0x{iat_rva:x} taille=0x{iat_size:x}")

# --- sections (rva -> fichier) ---
secs = []
so = e_lfanew + 24 + struct.unpack_from("<H", data, e_lfanew + 20)[0]
for i in range(nsec):
    b = so + 40 * i
    nom = data[b:b + 8].rstrip(b"\0").decode()
    vsz, vrva, rsz, rraw = struct.unpack_from("<IIII", data, b + 8)
    secs.append((nom, vrva, vsz, rraw, rsz))
    print(f"[sec] {nom:10} rva=0x{vrva:05x} vsize=0x{vsz:05x} "
          f"file=0x{rraw:05x} rawsize=0x{rsz:05x}")

def rva2off(rva):
    for nom, vrva, vsz, rraw, rsz in secs:
        if vrva <= rva < vrva + max(vsz, rsz):
            return rraw + (rva - vrva)
    raise ValueError(f"rva 0x{rva:x} hors sections")

def cstr(off):
    fin = data.index(b"\0", off)
    return data[off:fin].decode("latin1")

# --- descripteurs d'import ---
print("\n[imports] descripteurs (jusqu'au terminateur nul) :")
descs = []
off = rva2off(imp_rva)
while True:
    oft, ts, fc, name_rva, ft = struct.unpack_from("<IIIII", data, off)
    if oft == 0 and ft == 0:
        break
    dll = cstr(rva2off(name_rva))
    descs.append((dll, oft, ft))
    off += 20

slots = {}  # rva slot -> (dll, nom, index)
for dll, oft, ft in descs:
    o = rva2off(oft)
    of = rva2off(ft)
    n = 0
    prem, der = None, None
    while True:
        v = struct.unpack_from("<Q", data, o + 8 * n)[0]
        if v == 0:
            break
        nom = None
        if v & (1 << 63):
            nom = f"ord#{v & 0xFFFF}"
        else:
            ho = rva2off(v)
            hint = struct.unpack_from("<H", data, ho)[0]
            nom = cstr(ho + 2)
        s_rva = ft + 8 * n
        slots[s_rva] = (dll, nom, n)
        prem = s_rva if prem is None else prem
        der = s_rva
        n += 1
    print(f"  {dll:16} OFT=0x{oft:x} FT=0x{ft:x} n={n} "
          f"plage FT=0x{prem:x}..0x{der:x}" if prem else f"  {dll} VIDE")

# --- slots utilisés par les chemins T2 (.curl, .arret, .attendre, sup-31) ---
print("\n[chemin .curl / T2] couverture des slots appelés :")
cibles = {
    0x2300: "CreateProcessA (sup-31, prouvé S10/S20)",
    0x2310: "WaitForSingleObject (.curl/.arret)",
    0x2318: "GetExitCodeProcess (.curl)",
    0x20f8: "CloseHandle (sup-31, prouvé)",
    0x2320: "TerminateProcess (.arret)",
    0x2338: "MsgWaitForMultipleObjects (.attendre)",
    0x2340: "Sleep (.attendre)",
}
for rva, role in sorted(cibles.items()):
    if rva in slots:
        dll, nom, idx = slots[rva]
        pre = struct.unpack_from("<Q", data, rva2off(rva))[0]
        print(f"  0x{rva:04x} {nom:28} COUVERT ({dll}#{idx})  "
              f"pré-charge=0x{pre:x}")
    else:
        pre = struct.unpack_from("<Q", data, rva2off(rva))[0]
        print(f"  0x{rva:04x} *** HORS DES DESCRIPTEURS ***  "
              f"pré-charge=0x{pre:x}   <- {role}")

# --- balayage exhaustif : tous les call [rip+disp] de .text/.text2,
#     cibles IAT hors couverture ---
print("\n[exhaustif] call qword ptr [rip+disp] vers un slot IAT NON couvert :")
hmm = 0
for nom_sec, vrva, vsz, rraw, rsz in secs:
    if nom_sec not in (".text", ".text2"):
        continue
    blob = data[rraw:rraw + rsz]
    for i in range(len(blob) - 6):
        if blob[i] == 0xFF and blob[i + 1] == 0x15:  # call [rip+disp32]
            disp = struct.unpack_from("<i", blob, i + 2)[0]
            cible = vrva + i + 6 + disp
            if cible in slots or not (0x2000 <= cible < 0x2400):
                continue
            ctx = blob[max(0, i - 16):i + 8].hex()
            print(f"  {nom_sec}+0x{i:x} (rva 0x{vrva + i:x}) -> slot 0x{cible:x} "
                  f"HORS couverture, pré-charge=0x{struct.unpack_from('<Q', data, rva2off(cible))[0]:x} ctx={ctx}")
            hmm += 1
if not hmm:
    print("  (aucun)")
print(f"\n[total] {len(slots)} slots couverts, {hmm} call-sites vers slots non couverts")
