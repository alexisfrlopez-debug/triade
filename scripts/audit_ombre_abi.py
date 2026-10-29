#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — D97quater : audit ABI ombre (shadow space) des notations terrain.

Règle (leçon D98, miroir terrain16-sur-machine) :
  une fenêtre de pile « sub rsp, IMM ... add rsp, IMM » où IMM < 0x28 ne doit
  contenir AUCUN appel externe (call qword ptr [rip ±x] = IAT) — les appels
  internes directs (call 0x...) sont tolérés (les blocs internes ne touchent
  jamais les maisons d'arguments, convention prouvée machine par terrain16).

Sortie : violations nommées (bloc, RVA, fenêtre, appel fautif).
"""
import pathlib
import re
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

NOTATIONS = pathlib.Path("/home/z/my-project/triade/terrain/notation")


def audit_fichier(chemin):
    lignes = [l.rstrip("\n") for l in chemin.read_text(encoding="utf-8")
              .splitlines() if l and not l.startswith(";")]
    # adresse de début : première ligne d'instruction — les notations sont
    # séquentielles ; on reconstitue les adresses par désassemblage depuis le
    # slot connu via l'en-tête (on lit « slot RVA 0x…, taille N octets »)
    entete = chemin.read_text(encoding="utf-8").splitlines()
    rva = None
    for l in entete:
        m = re.search(r"slot RVA 0x([0-9a-f]+), taille (\d+) octets", l)
        if m:
            rva = int(m.group(1), 16)
            break
    if rva is None:
        return []
    code = "\n".join(lignes)
    # keystone n'est pas nécessaire : capstone désassemble la notation ?
    # NON — la notation est du texte asm. On demande à keystone de l'assembler.
    from keystone import Ks, KS_ARCH_X86, KS_MODE_64
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    enc, _ = ks.asm(code, rva)
    if not enc:
        return [(f"{chemin.name}: inassemblable",)]
    buf = bytes(enc)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = list(md.disasm(buf, rva))
    violations = []
    # fenêtres de pile : suivre la profondeur et le dernier sub rsp < 0x28
    fenetre_sub = []  # pile de (début_index, imm, possede_appel_ext)
    for i, ins in enumerate(insns):
        if ins.mnemonic == "sub" and ins.op_str.startswith("rsp,"):
            imm = int(ins.op_str.split(",")[1].strip(), 16)
            if imm < 0x28:
                fenetre_sub.append([i, imm, None])
        elif ins.mnemonic == "add" and ins.op_str.startswith("rsp,"):
            imm = int(ins.op_str.split(",")[1].strip(), 16)
            # ferme la fenêtre correspondante si elle existe
            if fenetre_sub and fenetre_sub[-1][1] == imm:
                debut, im, ext = fenetre_sub.pop()
                if ext is not None:
                    violations.append(
                        (f"{chemin.name}", f"0x{insns[debut].address:X}",
                         f"sub rsp, {im:#x}",
                         f"appel externe 0x{ext.address:X} ({ext.mnemonic} "
                         f"{ext.op_str}) dans la fenêtre"))
        elif ins.mnemonic == "call":
            if fenetre_sub and fenetre_sub[-1][2] is None \
                    and "ptr [rip" in ins.op_str:
                fenetre_sub[-1][2] = ins
    return violations


def main():
    total = 0
    for chemin in sorted(NOTATIONS.glob("sup-*.asm")):
        for v in audit_fichier(chemin):
            print(f"[VIOLATION] {v[0]} @ {v[1]} : fenêtre {v[2]} — {v[3]}")
            total += 1
    if not total:
        print("[audit] aucune violation d'ombre ABI dans les notations terrain")
    else:
        print(f"[audit] {total} violation(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
