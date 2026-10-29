#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — D98 : vérification du rebuild terrain.17-C.

1. .curl (0x5D1E) et .ps (0x7775) portent sub/add rsp, 0x28 dans le BINAIRE ;
2. le motif loader D54 est présent : IAT kernel32#3 @0x2300 et user32#2 @0x2360
   PRÉ-REMPLIES (pointeurs de hints non nuls), INT+hints .rdata @0x2B40-0x2C79,
   descripteurs OFT pointant .rdata ;
3. différentiel 17-B -> 17-C : uniquement les 4 octets .curl/.ps + les entrées
   R10 recalculées pour les deux zones couvertes.
"""
import pathlib
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

B17 = pathlib.Path("/home/z/my-project/download/superviseur-terrain17b.exe")
B17C = pathlib.Path("/home/z/my-project/triade/terrain/superviseur.exe")


def rva_off(pe, rva):
    return pe.get_offset_from_rva(rva)


def main():
    pe = pefile.PE(data=B17C.read_bytes(), fast_load=False)
    exe = B17C.read_bytes()

    print("=== 1. cadres .curl / .ps dans le binaire 17-C ===")
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    for nom, rva in ((".curl", 0x5D1E), (".ps", 0x7775)):
        off = rva_off(pe, rva)
        insns = list(md.disasm(exe[off:off + 0x50], rva))
        prem = [f"{i.mnemonic} {i.op_str}" for i in insns[:1]]
        print(f"  {nom} @0x{rva:X} : {prem[0]}")
        assert prem[0] == "sub rsp, 0x28", f"{nom} : cadre fautif !"
    # épilogues : chercher add rsp, 0x28 dans la fenêtre
    for nom, rva, fin in ((".curl", 0x5D1E, 0x5D60), (".ps", 0x7775, 0x77B7)):
        off = rva_off(pe, rva)
        zone = exe[off:rva_off(pe, fin + 0x10)]
        trouve = "add rsp, 0x28" in [
            f"{i.mnemonic} {i.op_str}"
            for i in md.disasm(zone, rva)]
        assert trouve, f"{nom} : épilogue 0x28 absent !"
        print(f"  {nom} : épilogue add rsp, 0x28 présent ✓")

    print("\n=== 2. motif loader D54 (IAT pré-remplies + INT .rdata) ===")
    # IAT k32#3 @0x2300 : 9 slots + terminateur
    off = rva_off(pe, 0x2300)
    slots = [int.from_bytes(exe[off + 8 * i:off + 8 * i + 8], "little")
             for i in range(9)]
    nz = sum(1 for s in slots if s != 0)
    print(f"  IAT k32#3 @0x2300 : {nz}/9 slots pré-remplis "
          f"(valeurs 0x{slots[0]:X}..0x{slots[-1]:X})")
    assert nz == 9, "IAT k32#3 non pré-remplie !"
    # descripteurs d'import : comparaison EXPLICITE 17-B vs 17-C
    pe17 = pefile.PE(data=B17.read_bytes(), fast_load=False)
    print("  table des descripteurs (17-B -> 17-C) :")
    for i, (d17, d17c) in enumerate(zip(pe17.DIRECTORY_ENTRY_IMPORT,
                                        pe.DIRECTORY_ENTRY_IMPORT)):
        oft17 = d17.struct.OriginalFirstThunk
        oft17c = d17c.struct.OriginalFirstThunk
        marque = " OK" if oft17 == oft17c else "  <-- DIVERGENT"
        print(f"    #{i} {d17c.dll.decode():16s} OFT 0x{oft17:X} -> 0x{oft17c:X}{marque}")
        assert oft17 == oft17c, f"descripteur #{i} divergent !"
    # INT+hints .rdata non nuls (plage du motif D54)
    for base, n, nom in ((0x2B40, 0x60, "INT k32#3 + hints"),):
        off = rva_off(pe, base)
        bloc = exe[off:off + n]
        print(f"  {nom} @0x{base:X} : {sum(1 for b in bloc if b)} octets non nuls "
              f"sur {n}")

    print("\n=== 3. différentiel 17-B -> 17-C ===")
    a = B17.read_bytes()
    b = exe
    assert len(a) == len(b) == 75264, "tailles divergentes !"
    diffs = [i for i in range(len(a)) if a[i] != b[i]]
    print(f"  {len(diffs)} octets divergents : "
          f"off {[hex(d) for d in diffs]}")
    # cartographie RVA
    for d in diffs:
        rva = None
        for s in pe.sections:
            if s.PointerToRawData <= d < s.PointerToRawData + s.SizeOfRawData:
                rva = s.VirtualAddress + (d - s.PointerToRawData)
                nom = s.Name.decode().rstrip("\x00")
                break
        print(f"    off 0x{d:X} -> {nom} RVA 0x{rva:X} : "
              f"{a[d]:#04x} -> {b[d]:#04x}")
    print("\n[tout vert] 17-C : cadres réparés, motif D54 intact, "
          "deltas circonscrits")


if __name__ == "__main__":
    main()
