#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""round_trip_vite — le round-trip exact (client_hunks.round_trip reconduit en
appel local) : les lignes de code assemblées par keystone, désassemblées par
capstone, re-notées — tout écart est un refus."""
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from keystone import Ks, KS_ARCH_X86, KS_MODE_64


def round_trip_vite(notation_texte: str) -> tuple:
    code = []
    for l in notation_texte.split("\n"):
        s = l.strip()
        if not s or s.startswith(";"):
            continue
        s = s.split(";", 1)[0].strip()
        if not s:
            continue
        if re.match(r"^(db|dw|dd|dq)\b", s):
            continue
        if any(ord(c) > 127 for c in s):
            return False, f"caractère non-ASCII : {s[:60]!r}"
        code.append(s)
    if not code:
        return False, "aucune instruction"
    try:
        ks = Ks(KS_ARCH_X86, KS_MODE_64)
        octets, _ = ks.asm("\n".join(code))
        b1 = bytes(octets)
    except Exception as e:
        return False, f"keystone refuse : {str(e)[:120]}"
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    lignes2 = []
    pos = 0
    for ins in md.disasm(b1, 0):
        lignes2.append(f"{ins.mnemonic} {ins.op_str}".rstrip())
    try:
        octets2, _ = ks.asm("\n".join(lignes2))
        b2 = bytes(octets2)
    except Exception as e:
        return False, f"keystone re-refuse : {str(e)[:120]}"
    if b1 != b2:
        return False, "le re-assemblage diverge"
    return True, f"{len(b1)} octets, {len(code)} instructions, re-noté identique"
