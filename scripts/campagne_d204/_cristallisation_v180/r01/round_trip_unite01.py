#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""round_trip_unite01.py — LE ROUND-TRIP DE LA NOTATION LIVRÉE (R5), la
commande M4 n° 2 du bras T (le plan D204) : la notation de campagne
assemblée (keystone), désassemblée (capstone), ré-assemblée — l'octet juge,
la notation vérité ; l'égalité PARFAITE des deux assemblages et le compte
des instructions.

Usage : python3 scripts/campagne_d204/unite-01-T/round_trip_unite01.py
Sortie : 0 = R5 VERT ; 2 = refus nommé.
"""
from __future__ import annotations

import hashlib
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-01-T")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import harnais_noyau as HN   # noqa: E402  (B4 : le lecteur canonique)

L = HN.L
B4 = HN.B4
NOTATION = os.path.join(UNITE, "notation", "loupe-01-ouvrir.asm")


def main() -> int:
    print("=== LE ROUND-TRIP R5 — la notation de campagne livrée "
          "(loupe-01 × T) ===")
    if not os.path.exists(NOTATION):
        print(f"[round-trip] REFUS NOTATION-ABSENTE : {NOTATION}",
              file=sys.stderr)
        return 2
    ks = HN.Ks(HN.KS_ARCH_X86, HN.KS_MODE_64)
    cs = HN.capstone.Cs(HN.capstone.CS_ARCH_X86, HN.capstone.CS_MODE_64)
    rva, slot = L.SLOTS_LOUPE["i110001"]
    octets, metas = B4.assembler_bloc(ks, NOTATION, rva, slot)
    insns = B4.round_trip(cs, ks, NOTATION, rva, octets, metas)
    if len(insns) != len(metas):
        print(f"[round-trip] REFUS R5 : {len(insns)} instructions "
              f"désassemblées != {len(metas)} assemblées", file=sys.stderr)
        return 2
    sha = hashlib.sha256(octets).hexdigest()
    print(f"[R5] {len(octets)} o, {len(metas)} instructions — keystone == "
          f"capstone == keystone, l'octet juge ; sha256 {sha}")
    print("=== LE ROUND-TRIP R5 VERT ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
