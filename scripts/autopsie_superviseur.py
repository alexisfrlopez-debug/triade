#!/usr/bin/env python3
"""Autopsie PE : superviseur.exe (livraison terrain.2) vs demo.exe (éprouvé terrain).

But : trouver pourquoi superviseur.exe « ne fait rien » au double-clic,
alors que demo.exe (même lignée d'outils, terrain.8 validé) démarre.

Compare : en-têtes optionnels, sections, répertoires de données,
relocations, IAT, ressources, point d'entrée.
"""
import pefile
import sys

LIVR = "/home/z/my-project/triade/terrain/livraison/superviseur.exe"
PUBL = "/home/z/my-project/triade/terrain/superviseur.exe"
DEMO = "/home/z/my-project/triade/demo/demo.exe"

def dump(chemin, nom):
    pe = pefile.PE(chemin)
    print("=" * 78)
    print(f"FICHIER : {chemin}  ({nom})")
    print("=" * 78)
    oh = pe.OPTIONAL_HEADER
    print(f"Machine={hex(pe.FILE_HEADER.Machine)}  NbSections={pe.FILE_HEADER.NumberOfSections}"
          f"  Caract(fichier)={hex(pe.FILE_HEADER.Characteristics)}")
    print(f"Point d'entree RVA={hex(oh.AddressOfEntryPoint)}  ImageBase={hex(oh.ImageBase)}")
    print(f"SectionAlign={hex(oh.SectionAlignment)}  FileAlign={hex(oh.FileAlignment)}")
    print(f"SizeOfImage={hex(oh.SizeOfImage)}  SizeOfHeaders={hex(oh.SizeOfHeaders)}")
    print(f"Checksum={hex(oh.CheckSum)}  Subsystem={oh.Subsystem} (2=GUI 3=CUI)")
    print(f"DllCharacteristics={hex(oh.DllCharacteristics)}"
          f"  (bit 0x0040=DYNAMIC_BASE, 0x0100=NX_COMPAT, 0x0020=HIGH_ENTROPY)")
    print(f"SizeOfStackRes={hex(oh.SizeOfStackReserve)} Commit={hex(oh.SizeOfStackCommit)}"
          f"  Heap R/C={hex(oh.SizeOfHeapReserve)}/{hex(oh.SizeOfHeapCommit)}")
    print(f"NbRvaAndSizes={oh.NumberOfRvaAndSizes}")
    print("\n-- Sections --")
    for s in pe.sections:
        nom_s = s.Name.rstrip(b"\x00").decode(errors="replace")
        print(f"  {nom_s:<10} RVA={hex(s.VirtualAddress):>8} VSize={hex(s.Misc_VirtualSize):>8}"
              f"  RawPtr={hex(s.PointerToRawData):>8} RawSize={hex(s.SizeOfRawData):>8}"
              f"  Caract={hex(s.Characteristics)}")
    print("\n-- Répertoires de données --")
    for i, d in enumerate(oh.DATA_DIRECTORY):
        if d.VirtualAddress or d.Size:
            print(f"  [{i:2d}] {d.name:<24} RVA={hex(d.VirtualAddress):>8} Taille={hex(d.Size)}")
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        print("\n-- Imports --")
        for e in pe.DIRECTORY_ENTRY_IMPORT:
            fns = [imp.name.decode() if imp.name else f"ord{imp.ordinal}"
                   for imp in e.imports]
            print(f"  {e.dll.decode():<14} {len(fns)} fns : {', '.join(fns)}")
    # IAT
    d_iat = oh.DATA_DIRECTORY[12]
    print(f"\n  DIR_IAT : RVA={hex(d_iat.VirtualAddress)} taille={hex(d_iat.Size)}")
    # reloc
    d_rel = oh.DATA_DIRECTORY[5]
    print(f"  DIR_BASERELOC : RVA={hex(d_rel.VirtualAddress)} taille={hex(d_rel.Size)}")
    if d_rel.VirtualAddress and hasattr(pe, "DIRECTORY_ENTRY_BASERELOC"):
        n = sum(len(r.entries) for r in pe.DIRECTORY_ENTRY_BASERELOC)
        print(f"    -> {n} entrées de relocation (ASLR patchera ces octets au chargement)")
    # ressources
    d_rsrc = oh.DATA_DIRECTORY[2]
    print(f"  DIR_RESOURCE : RVA={hex(d_rsrc.VirtualAddress)} taille={hex(d_rsrc.Size)}")
    print()
    return pe

pe_l = dump(LIVR, "LIVRAISON — celui qui « ne fait rien »")
pe_d = dump(DEMO, "demo.exe — éprouvé sur le terrain (demo.8)")

print("=" * 78)
print("ECARTS EN-TETES superviseur(livraison) vs demo :")
print("=" * 78)
h1, h2 = pe_l.OPTIONAL_HEADER, pe_d.OPTIONAL_HEADER
for champ in ("AddressOfEntryPoint", "ImageBase", "SectionAlignment", "FileAlignment",
              "SizeOfImage", "SizeOfHeaders", "CheckSum", "Subsystem",
              "DllCharacteristics", "SizeOfStackReserve", "SizeOfStackCommit",
              "SizeOfHeapReserve", "SizeOfHeapCommit", "NumberOfRvaAndSizes"):
    a, b = getattr(h1, champ), getattr(h2, champ)
    marque = "   <<< DIFF" if a != b else ""
    print(f"  {champ:<24} sup={a:#x}  demo={b:#x}{marque}")
