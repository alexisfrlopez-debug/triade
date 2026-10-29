#!/usr/bin/env python3
"""D66 (suite) — Désassemblage comparatif demo.9 vs demo10 sur les blocs
d'échange : win-08-serveur (RVA 0x1D00, 256 o) et win-10-echange (RVA 0x4980,
384 o). Met en évidence TOUT écart d'instructions au-delà des sondes.
"""
import pathlib

import capstone

D9 = pathlib.Path("/home/z/my-project/triade/demo/demo.exe")
D10 = pathlib.Path("/home/z/my-project/triade/demo/livraison/demo10-diagnostique.exe")

SECTIONS = {  # nom : (raw, vsize_rva_base, rva)
    ".text": (0x0200, 0x1000),
    ".rdata": (0x1200, 0x2000),
    ".data": (0x2200, 0x3000),
    ".text2": (0x2C00, 0x4000),
}


def rva_to_off(rva):
    for nom, (raw, base) in SECTIONS.items():
        if base <= rva < base + 0x2000:
            return raw + (rva - base)
    raise ValueError(hex(rva))


def desasm(binaire, rva, taille, nom):
    off = rva_to_off(rva)
    code = binaire[off:off + taille]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False
    print(f"\n===== {nom} — RVA 0x{rva:X} (fichier 0x{off:X}) =====")
    lignes = []
    for i in md.disasm(code, rva):
        lignes.append(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}")
    return lignes


def cote_a_cote(rva, taille, nom):
    b9 = open(D9, "rb").read()
    b10 = open(D10, "rb").read()
    l9 = desasm(b9, rva, taille, f"demo.9 — {nom}")
    l10 = desasm(b10, rva, taille, f"demo10-diagnostique — {nom}")
    # affichage intercalé simple : d'abord les deux, puis un résumé des écarts
    import difflib
    sm = difflib.SequenceMatcher(None, l9, l10, autojunk=False)
    print(f"\n----- écarts d'instructions ({nom}) -----")
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        print(f"[{tag}] demo.9 :")
        for x in l9[i1:i2]:
            print(f"    {x}")
        print(f"[{tag}] demo10 :")
        for x in l10[j1:j2]:
            print(f"    {x}")
        print("    " + "-" * 40)


cote_a_cote(0x1D00, 0x100, "win-08-serveur")
cote_a_cote(0x4980, 0x180, "win-10-echange")
