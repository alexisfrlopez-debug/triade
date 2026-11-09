#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""autopsie_loupe.py — recoupement de pièces : le PE dev.5 ( Entrée 208 ).

Le labo relit l'artefact SANS l'exécuter : en-têtes, sections, imports,
relocations — les constats T0 du témoin croisés contre la pièce — puis
désassemble les blocs visés (loupe-16/17, la vitrine) aux adresses
scellées du plan.
"""
import sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = "/home/z/my-project/upload/triade/loupe.exe"
R_LOUPE16 = 0x6240
R_LOUPE17 = 0x6500
R_CADRE = 0xE000
R_VERSION = 0x2E80
R_RELOC = 0x2E90

pe = pefile.PE(EXE, fast_load=True)
pe.parse_data_directories(directories=[
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_BASERELOC'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IAT'],
])

print("=== EN-TÊTES ===")
fh = pe.FILE_HEADER
oh = pe.OPTIONAL_HEADER
print(f"Machine {fh.Machine:#06x} (8664 = AMD64) · sections {fh.NumberOfSections}")
print(f"Magic {oh.Magic:#x} (20B = PE32+) · subsystem {oh.Subsystem} "
      f"(3 = CUI) · DLL characteristics {oh.DllCharacteristics:#x}")
print(f"Image base {oh.ImageBase:#x} · align fichier {oh.FileAlignment:#x} "
      f"· align sections {oh.SectionAlignment:#x}")
print(f"EntryPoint RVA {oh.AddressOfEntryPoint:#x}")
for d in oh.DATA_DIRECTORY:
    if d.VirtualAddress or d.Size:
        print(f"  dir[{d.name}] VA {d.VirtualAddress:#x} taille {d.Size}")

print("\n=== SECTIONS ===")
for s in pe.sections:
    print(f"  {s.Name.decode().rstrip(chr(0)):8s} VA {s.VirtualAddress:#8x} "
          f"VSize {s.Misc_VirtualSize:#8x} RawPtr {s.PointerToRawData:#8x} "
          f"RawSize {s.SizeOfRawData:#8x} chars {s.Characteristics:#010x}")

print("\n=== IMPORTS (l'IAT du plan) ===")
total = 0
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        n = len(entry.imports)
        total += n
        print(f"  {entry.dll.decode()}: {n} feuilles")
        for imp in entry.imports:
            print(f"    {imp.address - oh.ImageBase:#7x}  {imp.name.decode() if imp.name else imp.ordinal}")
print(f"  TOTAL feuilles: {total}")

print("\n=== BASERELOC ===")
if hasattr(pe, 'DIRECTORY_ENTRY_BASERELOC'):
    for br in pe.DIRECTORY_ENTRY_BASERELOC:
        print(f"  bloc VA {br.struct.VirtualAddress:#x} taille {br.struct.SizeOfBlock}")
        for e in br.entries:
            print(f"    type {e.type} rva {e.rva:#x}")
else:
    print("  (aucune)")

data = pe.get_memory_mapped_image()
print("\n=== LE QWORD VERSION @0x2E80 ===")
import struct
v = struct.unpack_from("<Q", data, R_VERSION)[0]
print(f"  {v:#x} (attendu 0x00010005 = dev.5)")

print("\n=== BASERELOC minimal @0x2E90 (12 o) — octets bruts ===")
print("  " + data[R_RELOC:R_RELOC + 12].hex(" "))


def disasm(rva, length, titre):
    print(f"\n=== {titre} @ RVA {rva:#x} ({length} o) ===")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = False
    code = data[rva:rva + length]
    for i in md.disasm(code, rva):
        print(f"  {i.address:#7x}: {i.bytes.hex():24s} {i.mnemonic} {i.op_str}")


if __name__ == "__main__":
    quoi = sys.argv[1] if len(sys.argv) > 1 else "entetes"
    if quoi == "loupe17":
        disasm(R_LOUPE17, 0x300, "loupe-17 LA SAUVEGARDE")
    elif quoi == "loupe16":
        disasm(R_LOUPE16, 0x2C0, "loupe-16 LA SAISIE")
    elif quoi == "entetes":
        pass  # déjà imprimé ci-dessus
