#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit de la fenêtre mortelle demo.6 (post-terrain D40b).

Constat terrain demo.6 : journal gelé après « sonde1 avant echo » (écriture
complète, CRLF final), fenêtre disparue = mort du processus. La fenêtre
mortelle est EXACTEMENT : ECHO v1 (@0x4600) | MEMCMP (@0x1180) |
TCP_PATCH pose mode 0 (@0x4400).

Objet : désassembler ces trois appels dans le binaire LIVRÉ (md5 3f3067a3…)
en cherchant une 7e classe de défaut invisible à l'émulation — en priorité
ce que le shim Python de l'oracle ne peut pas reproduire :
  - alignement de pile (mod 16) au moment de chaque call (surtout IAT) ;
  - shadow space 32 o réservé avant les calls IAT ;
  - registres volatils détruits à travers les appels ;
  - lectures/écritures hors bornes des tampons ;
  - toute écriture en mémoire non inscrite au PE (page morte au chargement).

Usage : .venv/bin/python scripts/audit_fenetre_morte.py
"""

import hashlib
import pathlib
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]
EXE = REPO / "demo" / "demo.exe"
BASE = 0x140000000
ATTENDU_MD5 = "3f3067a32cc3d098b404643f8fae6a98"   # demo.6 livrée


def rva_to_off(pe, rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    raise ValueError(f"RVA {rva:#x} hors sections")


def main():
    data = EXE.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    print("=" * 74)
    print(f"[0] demo.exe : md5 {md5}"
          f" → {'CONFORME demo.6' if md5 == ATTENDU_MD5 else 'DIVERGENT !'}")

    pe = pefile.PE(str(EXE), fast_load=True)
    print("    sections :")
    for s in pe.sections:
        print(f"      {s.Name.decode().strip(chr(0)):<10} "
              f"RVA {s.VirtualAddress:#07x} vsize {s.Misc_VirtualSize:#06x} "
              f"raw {s.PointerToRawData:#07x}/{s.SizeOfRawData:#06x} "
              f"carac {s.Characteristics:#010x}")

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False

    def disas(rva, n, titre):
        print("=" * 74)
        print(f"[{titre}] RVA {rva:#x}..{rva + n:#x}")
        off = rva_to_off(pe, rva)
        code = data[off:off + n]
        for ins in md.disasm(code, BASE + rva):
            marque = ""
            if ins.mnemonic in ("call", "jmp"):
                marque = "   ◄◄◄"
            print(f"    {ins.address - BASE:#06x}: {ins.bytes.hex():<22} "
                  f"{ins.mnemonic} {ins.op_str}{marque}")

    # --- 1. La fenêtre mortelle elle-même : sonde1 → sonde2 ----------------
    disas(0x4ca5, 0x90, "1] scénario : J_LIBC_OK → sonde1 → écho → memcmp → "
                         "pose → sonde2")

    # --- 2. ECHO v1 : cible du patch, 1er appel jamais exécuté au terrain --
    disas(0x4600, 0x80, "2] ECHO v1 complet (@0x4600, jusqu'au ret)")

    # --- 3. TCP_PATCH pose : fonction complète ------------------------------
    disas(0x4400, 0x180, "3] TCP_PATCH (tcp-07:R2) complet (@0x4400)")

    # --- 4. MEMCMP (libc-02) : contrôle rapide ------------------------------
    disas(0x1180, 0x40, "4] MEMCMP (libc-02, prouvé par sceau 4/4)")

    # --- 5. JOURNAL_TRACE (0x5000, sonde1 a FONCTIONNÉ — étalon sain) -------
    disas(0x5000, 0x50, "5] JOURNAL_TRACE (win-05:R3 entrée trace — étalon)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
