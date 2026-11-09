#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""autopsie_dev4.py — L'AUTOPSIE SUR PIÈCES de loupe.exe 0.1.0-dev.4
(sha256 1f2da283… — l'artefact authentique du dépôt terrain) :

LES TROIS CONSTATS ATTENDUS (la lecture des notations) :
  A. loupe-01 @0x4080 : CreateFileW — les arguments 5/6/7 écrits à
     [rsp]/[rsp+8]/[rsp+0x10] (LE HOME SPACE) au lieu de [rsp+0x20+] —
     le VRAI chargeur de fonctions lit dwCreationDisposition à
     [rsp+0x20] : au terrain le T1 a rendu -6 SYSTÈME (le témoin) ;
  B. loupe-05 @0x4540 : ReadFile — [rsp+0x20] contient l'état SHA
     (H0[0] 0x6A09E667… — UN POINTEUR FANTÔME) au moment de l'appel,
     lpOverlapped jamais posé à sa place ;
  C. loupe-06 @0x4700 : ReadFile — [rsp+0x20] contient l'état MD5
     (A 0x67452301…) — même classe ;
  D. loupe-09 @0x5c00 : l'entrée EST WinMain — GetModuleHandleW (la
     feuille réservée du plan, slot 0x2400) JAMAIS appelée : r12 = rcx =
     ce que le chargeur donne (le PEB au point d'entrée brut — l'axe
     jamais prouvé au terrain).

L'autopsie NE MODIFIE RIEN : elle NOMME sur la pièce.
"""

import struct
import sys

import capstone

EXE = "/home/z/my-project/triade/loupe/loupe.exe"
SHA_ATTENDU = "1f2da2833b47265e9b956ee83a5cc246b68455f06f5b7bb03a69045f03503e03"

# les IAT slots du plan (layout.py : l'ordre des feuilles)
SLOTS = {0x2400: "GetModuleHandleW", 0x2408: "GetCommandLineW",
         0x2410: "ExitProcess", 0x2418: "CreateFileW",
         0x2420: "GetFileSizeEx", 0x2428: "SetFilePointerEx",
         0x2430: "ReadFile", 0x2438: "WriteFile", 0x2440: "CloseHandle",
         0x2448: "GetLastError", 0x2818: "GetMessageW(démo)",
         0x2820: "TranslateMessage(démo)", 0x2828: "DispatchMessageW(démo)"}


def rva_vers_fichier(donnees):
    """→ (dict rva→(offset_fichier,), la table des sections)"""
    e = struct.unpack_from("<I", donnees, 0x3C)[0]
    n = struct.unpack_from("<H", donnees, e + 6)[0]
    opt = struct.unpack_from("<H", donnees, e + 20)[0]
    sections = {}
    for k in range(n):
        o = e + 24 + opt + k * 40
        va, vs = struct.unpack_from("<II", donnees, o + 12)
        ra = struct.unpack_from("<I", donnees, o + 20)[0]
        sections[va] = (va, vs, ra)
    def conv(rva):
        for va, vs, ra in sections.values():
            if va <= rva < va + vs:
                return ra + (rva - va)
        return None
    return conv, sections


def main():
    donnees = open(EXE, "rb").read()
    import hashlib
    sha = hashlib.sha256(donnees).hexdigest()
    assert sha == SHA_ATTENDU, f"pièce divergente : {sha}"
    print(f"la pièce : loupe.exe {len(donnees)} o, sha256 {sha[:16]}… — "
          "l'artefact authentique dev.4")
    conv, _ = rva_vers_fichier(donnees)

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True

    cibles = [
        ("A. loupe-01-ouvrir", 0x4080, 0x180),
        ("B. loupe-05-sha256", 0x4440, 0x130),
        ("C. loupe-06-md5", 0x4700, 0x100),
        ("D. loupe-09-ecran (l'entrée)", 0x5c00, 0x40),
    ]
    for nom, rva, taille in cibles:
        print(f"\n=== {nom} @{rva:#x} ===")
        code = donnees[conv(rva):conv(rva) + taille]
        rsp = 8          # l'entrée msx64 ≡ 8 (mod 16) — la simulation de pile
        for ins in md.disasm(code, rva):
            m = ins.mnemonic
            ops = ins.op_str
            if m == "push":
                rsp -= 8
            elif m == "pop":
                rsp += 8
            elif m == "sub" and ops.startswith("rsp,"):
                rsp -= int(ops.split(",")[1], 0)
            elif m == "add" and ops.startswith("rsp,"):
                rsp += int(ops.split(",")[1], 0)
            marque = ""
            if m == "call" and "rip" in ops:
                # la cible IAT : disp relatif — calcule la
                try:
                    import re
                    mm = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", ops)
                    if mm:
                        signe = 1 if mm.group(1) == "+" else -1
                        cible = ins.address + ins.size + signe * int(mm.group(2), 16)
                        feuille = SLOTS.get(cible, f"slot {cible:#x}")
                        marque = f"  ← IAT {feuille} · rsp≡{rsp % 16} (mod 16)"
                except Exception:
                    pass
            if m in ("mov", "movzx", "xor", "lea") and "rsp" in ops:
                marque += "  ·"
            print(f"  {ins.address:#x}: {m:<8} {ops}{marque}")


if __name__ == "__main__":
    sys.exit(main())
