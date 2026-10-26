#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit octet ciblé win-04 de demo.exe (demo.3) — le bouton invisible.

Le terrain (capture 2026-10-26 221352.png) montre : edit journal conforme
(w-16, h-56 — prouvé par les flèches de scrollbar), L4D=1 (MoveWindow bouton
VRAI), mais AUCUN bouton rendu. La notation win-04:R3 paraît correcte
(WS_CHILD|WS_VISIBLE, id 1, parent rbx, (8, h-44, w-16, 36)).

But : vérifier sur les OCTETS RÉELS du binaire livré que
  1. les deux CreateWindowExW de WM_CREATE portent bien les styles
     0x50200844 (edit) et 0x50000001 (bouton) ;
  2. les pointeurs de classe/libellé (RIP-relatifs) désignent bien
     « EDIT » / « BUTTON » / libellé bouton / chaîne vide ;
  3. les parents (rsp+0x40) et id (rsp+0x48) sont rbx et 1 pour le bouton ;
  4. WM_SIZE calcule bien journal (8, 8, w-16, h-56) et bouton
     (8, h-44, w-16, 36) depuis RECT.right/bottom ;
  5. les handles sont stockés/relus aux bonnes adresses .data.
Toute divergence notation/binaire est la cause du bouton invisible.
"""
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = "/home/z/my-project/triade/demo/demo.exe"
WIN04_RVA, WIN04_TAILLE = 0x1640, 0x380

data = open(EXE, "rb").read()
pe = struct.unpack_from("<I", data, 0x3C)[0]
nsec = struct.unpack_from("<H", data, pe + 6)[0]
opt = struct.unpack_from("<H", data, pe + 20)[0]
secs = []
for i in range(nsec):
    off = pe + 24 + opt + i * 40
    nom = data[off:off + 8].rstrip(b"\0").decode()
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", off=data,
                                                    src=off)[0:4] if False else struct.unpack_from("<IIII", data, off + 8)
    secs.append((nom, vaddr, vsize, raddr, rsize))
    print(f"section {nom:10s} RVA 0x{vaddr:05X} vsize 0x{vsize:05X} "
          f"fichier 0x{raddr:05X} taille 0x{rsize:05X}")


def rva_vers_fichier(rva):
    for nom, vaddr, vsize, raddr, rsize in secs:
        if vaddr <= rva < vaddr + max(vsize, rsize):
            return raddr + (rva - vaddr)
    raise ValueError(f"RVA {rva:#x} hors sections")


def chaine_utf16(rva, maxo=80):
    o = rva_vers_fichier(rva)
    bout = data[o:o + maxo * 2]
    s = ""
    for i in range(0, len(bout), 2):
        u = struct.unpack_from("<H", bout, i)[0]
        if u == 0:
            break
        s += chr(u)
    return s


def chaine_ascii(rva, maxo=80):
    o = rva_vers_fichier(rva)
    bout = data[o:o + maxo]
    return bout.split(b"\0")[0].decode(errors="replace")


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
debut = rva_vers_fichier(WIN04_RVA)
code = data[debut:debut + WIN04_TAILLE]

IAT_NOMS = {0x2808: "user32!CreateWindowExW", 0x2810: "user32!SendMessageW",
            0x2840: "user32!SendMessageW(gdi?)", 0x2850: "kernel32!CloseHandle",
            0x2858: "user32!MoveWindow", 0x2860: "user32!GetClientRect"}

print("\n=== désassemblage annoté win-04 (RVA 0x1640) ===")
instrs = list(md.disasm(code, WIN04_RVA))
for ins in instrs:
    rva = ins.address
    note = ""
    # RIP-relatif
    if "rip" in ins.op_str:
        for part in ins.op_str.split(","):
            part = part.strip()
            if part.startswith("[rip"):
                try:
                    disp = int(part.split("+")[-1].rstrip("]"), 16) if "+" in part \
                        else -int(part.split("-")[-1].rstrip("]"), 16)
                except ValueError:
                    continue
                cible = rva + ins.size + disp
                if cible in IAT_NOMS:
                    note = f"  ; IAT {IAT_NOMS[cible]}"
                elif 0x2000 <= cible < 0x3000:
                    note = f"  ; .rdata 0x{cible:x} « {chaine_utf16(cible, 24)} » / « {chaine_ascii(cible, 24)} »"
                elif 0x3000 <= cible < 0x4000:
                    note = f"  ; .data 0x{cible:x}"
                else:
                    note = f"  ; → 0x{cible:x}"
    if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
        note += "  ; (appel direct interne)"
    print(f"  0x{rva:04x}: {ins.mnemonic:12s} {ins.op_str}{note}")

print("\n=== chaînes clés .rdata ===")
for rva in (0x2a1e, 0x2a3a, 0x2a44, 0x2a52):
    print(f"  0x{rva:04x}: UTF16 « {chaine_utf16(rva, 40)} »   ASCII « {chaine_ascii(rva, 40)} »")
