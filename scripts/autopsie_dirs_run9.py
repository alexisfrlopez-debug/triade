#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Autopsie run 9 — parsing CORRECT de l'OptionalHeader PE32+.

Offsets PE32+ (depuis opt) : Magic@0, EP@16, BaseOfCode@20, ImageBase@24(Q),
SectionAlignment@32, FileAlignment@36, SizeOfImage@40, SizeOfHeaders@44,
CheckSum@48, Subsystem@52, DllCharacteristics@54, StackReserve@56(Q),
StackCommit@64(Q), HeapReserve@72(Q), HeapCommit@80(Q), LoaderFlags@88,
NumberOfRvaAndSizes@92, DataDirectory@96 (16×8).
"""
import struct

CHEMIN = "/home/z/my-project/run9/loupe.exe"
donnees = open(CHEMIN, "rb").read()
e_lfanew = struct.unpack_from("<I", donnees, 0x3C)[0]
opt = e_lfanew + 4 + 20
szopt = struct.unpack_from("<H", donnees, opt - 4)[0]

magic = struct.unpack_from("<H", donnees, opt)[0]
ep = struct.unpack_from("<I", donnees, opt + 16)[0]
basecode = struct.unpack_from("<I", donnees, opt + 20)[0]
imgbase = struct.unpack_from("<Q", donnees, opt + 24)[0]
sectal, fileal = struct.unpack_from("<II", donnees, opt + 32)
szimg, szhdr = struct.unpack_from("<II", donnees, opt + 40)
checksum = struct.unpack_from("<I", donnees, opt + 48)[0]
subsyst, dllchars = struct.unpack_from("<HH", donnees, opt + 52)
stackres, stackcom = struct.unpack_from("<QQ", donnees, opt + 56)
heapres, heapcom = struct.unpack_from("<QQ", donnees, opt + 72)
numdirs = struct.unpack_from("<I", donnees, opt + 92)[0]

print(f"magic {magic:#x}  EntryPoint RVA {ep:#x}  BaseOfCode {basecode:#x}")
print(f"ImageBase {imgbase:#x}  SectionAlignment {sectal:#x}  FileAlignment {fileal:#x}")
print(f"SizeOfImage {szimg:#x}  SizeOfHeaders {szhdr:#x}  CheckSum {checksum:#x}")
print(f"Subsystem {subsyst}  DllCharacteristics {dllchars:#06x}")
FLAGS = [(0x0020, "HIGHENTROPYVA"), (0x0040, "DYNAMICBASE"),
         (0x0100, "NXCOMPAT"), (0x0400, "NOSEH"), (0x1000, "APPCONTAINER"),
         (0x2000, "WDM_DRIVER"), (0x8000, "TERMINAL_SERVER_AWARE")]
print("  drapeaux :", " ".join(n for f, n in FLAGS if dllchars & f) or "AUCUN")
print(f"Stack {stackres:#x}/{stackcom:#x}  Heap {heapres:#x}/{heapcom:#x}")
print(f"NumberOfRvaAndSizes {numdirs}")

NOMS = ["EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY",
        "BASERELOC", "DEBUG", "ARCHITECTURE", "GLOBALPTR", "TLS",
        "LOAD_CONFIG", "BOUND_IMPORT", "IAT", "DELAY_IMPORT", "CLR", "RESERV"]
print("\nDataDirectory :")
dirs = {}
for i in range(min(numdirs, 16)):
    rva, taille = struct.unpack_from("<II", donnees, opt + 96 + 8 * i)
    dirs[NOMS[i]] = (rva, taille)
    if rva or taille:
        print(f"  [{i:2d}] {NOMS[i]:<13} rva {rva:#010x}  taille {taille:#x}")

# --- La table BASERELOC décortiquée -------------------------------------------
rva, taille = dirs["BASERELOC"]
print(f"\nBASERELOC @ rva {rva:#x}, {taille} octets :")
pr = None
for s in (".text", ".rdata", ".text2", ".data"):
    pass  # localisation par table des sections ci-dessous
off_sec = opt + szopt
nsec = struct.unpack_from("<H", donnees, e_lfanew + 6)[0]
sections = []
for i in range(nsec):
    b = off_sec + 40 * i
    nom = donnees[b:b + 8].rstrip(b"\0").decode()
    vs, va, srd, prd = struct.unpack_from("<IIII", donnees, b + 8)
    sections.append((nom, va, vs, srd, prd))
    if va <= rva < va + max(vs, srd):
        pr = prd + (rva - va)
print(f"  (fichier offset {pr:#x})" if pr else "  (HORS SECTION!)")
if pr:
    fin = pr + taille
    p = pr
    TYPES = {0: "ABSOLUTE", 1: "HIGH", 2: "LOW", 3: "HIGHLOW", 10: "DIR64"}
    while p < fin:
        pagerva, blocksize = struct.unpack_from("<II", donnees, p)
        if blocksize == 0:
            break
        print(f"  bloc : PageRVA {pagerva:#x}, taille {blocksize}")
        for j in range((blocksize - 8) // 2):
            e, = struct.unpack_from("<H", donnees, p + 8 + 2 * j)
            t, off = e >> 12, e & 0xFFF
            if t:
                cible = pagerva + off
                # que contient ce qword ?
                for nom, va, vs, srd, prd in sections:
                    if va <= cible < va + max(vs, srd):
                        fo = prd + (cible - va)
                        qword, = struct.unpack_from("<Q", donnees, fo)
                        print(f"    entrée {TYPES.get(t, t)} @rva {cible:#x}"
                              f" ({nom}) = {qword:#018x}")
                        break
                else:
                    print(f"    entrée {TYPES.get(t, t)} @rva {cible:#x} "
                          f"(HORS IMAGE)")
        p += blocksize

# --- La chasse aux pointeurs absolus : qwords dans l'enveloppe ImageBase -----
print(f"\nChasse aux qwords dans l'enveloppe [{imgbase:#x}, "
      f"{imgbase + szimg:#x}) :")
trouves = []
for nom, va, vs, srd, prd in sections:
    for fo in range(prd, prd + srd - 7, 8):
        q, = struct.unpack_from("<Q", donnees, fo)
        if imgbase <= q < imgbase + szimg:
            rva_q = va + (fo - prd)
            trouves.append((rva_q, nom, q))
            print(f"  {nom} @rva {rva_q:#x} = {q:#x} "
                  f"(→ rva {q - imgbase:#x})")
if not trouves:
    print("  AUCUN — mais vérifions aussi l'ANCIENNE enveloppe 0x7ff6…")
    for nom, va, vs, srd, prd in sections:
        for fo in range(prd, prd + srd - 7, 8):
            q, = struct.unpack_from("<Q", donnees, fo)
            if 0x7ff600000000 <= q < 0x7ff700000000:
                print(f"  {nom} @rva {va + (fo - prd):#x} = {q:#x} (7ff6!)")

# --- Et l'entrée réelle : que dit l'en-tête ? --------------------------------
print(f"\nAddressOfEntryPoint = {ep:#x} — dans quelle section ?")
for nom, va, vs, srd, prd in sections:
    if va <= ep < va + max(vs, srd):
        print(f"  → {nom} (offset fichier {prd + (ep - va):#x})")
        break
else:
    print("  → HORS DE TOUTE SECTION — LE CHARGEUR NE PEUT PAS DÉMARRER LÀ")
