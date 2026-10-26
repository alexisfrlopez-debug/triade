#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit final demo.7 (D41 : zone d'accueil ABI dans .protger).

Vérifie sur les OCTETS RÉELS du binaire fraîchement construit :
  1. empreintes (md5/sha256) ;
  2. les 3 sondes posées aux interstices (0x2748/0x276C/0x22F1) — CONSERVÉES
     pour la lecture terrain du correctif ;
  3. L00 = 0.3.0-demo.7 ; version u64 0x00030107 @0x2628 ;
  4. les 3 appels de sonde dans win-09 (lea + mov edx + xor r8d + call 0x5000)
     aux bons emplacements (avant écho#1 / après patch(0) / après memcmp#2) ;
  5. héritage DEP intact : constantes 0x40 aux deux sites tcp-07, ZÉRO
     « mov r8d, 4 » résiduel ;
  6. correctif D41 : .protger réserve 0x28 (sub rsp,0x28 / lea r9,[rsp+0x20] /
     add rsp,0x28), ZÉRO « sub rsp, 8 » résiduel — la zone d'accueil ABI
     (0x20) + alignement (0x8) couvre l'adresse de retour ;
  7. win-05 (0x5000) hors des pages VirtualProtect ; win-09 reste en 0x4C00 ;
  8. diff demo.6 → demo.7 CHIRURGICAL : exactement 3 octets de code tcp-07
     + version u64 + L00 + 2 octets de somme R10.

Usage : .venv/bin/python scripts/audit_demo7.py
"""

import hashlib
import pathlib
import re
import struct
import subprocess
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "demo"))
import layout as L  # noqa: E402

EXE = REPO / "demo" / "demo.exe"
BASE = 0x140000000


def rva_to_off(pe, rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    raise ValueError(rva)


def main():
    data = EXE.read_bytes()
    pe = pefile.PE(str(EXE), fast_load=True)
    md5 = hashlib.md5(data).hexdigest()
    sha = hashlib.sha256(data).hexdigest()
    ok = True

    print("=" * 72)
    print(f"[1] demo.exe : {len(data):,} o — md5 {md5}")
    print(f"    sha256 {sha}")

    # 2. sondes posées
    print("=" * 72)
    print("[2] sondes .rdata (interstices) — conservées pour lecture terrain")
    for nom in ("SONDE_1", "SONDE_2", "SONDE_3"):
        adr, octets, n = L.CHAINES_SONDES[nom]
        off = rva_to_off(pe, adr)
        lu = data[off:off + n]
        bon = lu == octets
        ok &= bon
        print(f"    {nom} @ {adr:#x} : {lu.decode('ascii')!r} "
              f"{'CONFORME' if bon else 'DIVERGENT !'}")

    # 3. version
    print("=" * 72)
    print("[3] version")
    off = rva_to_off(pe, 0x2EA8)
    l00 = data[off:off + 40].decode("ascii")
    u64 = struct.unpack("<Q", data[rva_to_off(pe, L.R_VERSION):rva_to_off(pe, L.R_VERSION) + 8])[0]
    bon = l00 == "L00 demarrage demonstration 0.3.0-demo.7" and u64 == 0x00030107
    ok &= bon
    print(f"    L00 : {l00!r} {'CONFORME' if 'demo.7' in l00 else 'DIVERGENT !'}")
    print(f"    u64 version : {u64:#x} {'CONFORME' if u64 == 0x00030107 else 'DIVERGENT !'}")

    # 4. sondes dans win-09
    print("=" * 72)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    off9 = rva_to_off(pe, 0x4C00)
    code9 = data[off9:off9 + 889]
    insns = list(md.disasm(code9, BASE + 0x4C00))
    print(f"[4] win-09 : {len(insns)} instructions, 889 o attendus")
    attendus = {0x2748: 17, 0x276C: 17, 0x22F1: 12}
    trouves = 0
    for i in range(len(insns) - 3):
        a, b, c, d = insns[i:i + 4]
        if (a.mnemonic == "lea" and b.mnemonic == "mov" and
                c.mnemonic == "xor" and d.mnemonic == "call"):
            m = re.match(r"rcx, \[rip ([+-]) (0x[0-9a-f]+)\]", a.op_str)
            if not m:
                continue
            disp = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
            cible = a.address + a.size + disp - BASE
            mlen = re.match(r"edx, (0x[0-9a-f]+|\d+)", b.op_str)
            n = int(mlen.group(1), 0) if mlen else -1
            if cible in attendus and attendus[cible] == n and \
                    c.op_str == "r8d, r8d" and d.op_str == "0x140005000":
                trouves += 1
                print(f"    sonde @ {a.address - BASE:#x} → chaîne {cible:#x}, "
                      f"len {n}, xor r8d, call 0x5000 ✓")
    ok &= (trouves == 3)
    print(f"    séquences complètes trouvées : {trouves}/3 "
          f"{'CONFORME' if trouves == 3 else 'DIVERGENT !'}")

    # 5. héritage DEP intact
    print("=" * 72)
    off7 = rva_to_off(pe, 0x4400)
    code7 = data[off7:off7 + 512]
    n40 = code7.count(bytes.fromhex("41b840000000"))
    n04 = code7.count(bytes.fromhex("41b804000000"))
    ok &= (n40 == 2 and n04 == 0)
    print(f"[5] tcp-07 DEP : mov r8d,0x40 × {n40} (attendu 2) ; mov r8d,4 × {n04} "
          f"(attendu 0) {'CONFORME' if (n40 == 2 and n04 == 0) else 'DIVERGENT !'}")

    # 6. correctif D41 : zone d'accueil ABI dans .protger
    print("=" * 72)
    p28 = code7.count(bytes.fromhex("4883ec28"))   # sub rsp, 0x28
    a28 = code7.count(bytes.fromhex("4883c428"))   # add rsp, 0x28
    l20 = code7.count(bytes.fromhex("4c8d4c2420"))  # lea r9, [rsp+0x20]
    s08 = code7.count(bytes.fromhex("4883ec08"))   # sub rsp, 8 — résiduel DÉFAUT
    l38 = code7.count(bytes.fromhex("4c8d4c2438"))  # lea r9, [rsp+0x38] — résiduel
    bon = (p28 == 1 and a28 == 1 and l20 == 1 and s08 == 0 and l38 == 0)
    ok &= bon
    print(f"[6] tcp-07 zone d'accueil (D41) : sub rsp,0x28 × {p28} ; "
          f"add rsp,0x28 × {a28} ; lea r9,[rsp+0x20] × {l20} ; "
          f"sub rsp,8 résiduel × {s08} ; lea r9,[rsp+0x38] résiduel × {l38} "
          f"{'CONFORME' if bon else 'DIVERGENT !'}")
    print(f"    géométrie : 0x20 zone d'accueil ([rsp..rsp+0x1F]) + 0x8 marge ; "
          f"loge old-protect @ [rsp+0x20] hors zone ; adresse de retour @ [rsp+0x28] "
          f"jamais recouverte")
    # audit chirurgical : désassembler .protger depuis 0x4531
    offp = rva_to_off(pe, 0x4531)
    protger = list(md.disasm(data[offp:offp + 0x28], BASE + 0x4531))
    seq = [(i.mnemonic, i.op_str) for i in protger]
    attendu = [("sub", "rsp, 0x28"), ("mov", "rcx, r15"),
               ("and", "rcx, 0xfffffffffffff000"), ("mov", "rdx, 0x700"),
               ("lea", "r9, [rsp + 0x20]")]
    bon = seq[:5] == attendu and seq[5] == ("call", "qword ptr [rip - 0x2481]") \
        and seq[6] == ("add", "rsp, 0x28") and seq[7] == ("ret", "")
    ok &= bon
    print(f"    .protger @0x4531 désassemblé : "
          f"{'SÉQUENCE EXACTE (I7) CONFORME' if bon else 'DIVERGENT !'}")

    # 7. géographie des pages
    print("=" * 72)
    for s in pe.sections:
        if b".text2" in s.Name:
            print(f"[7] .text2 VA {s.VirtualAddress:#x} VSize {s.Misc_VirtualSize:#x} "
                  f"— win-09 0x4C00-0x4FBF (page patch 0x4000-0x4FFF) ; "
                  f"win-05 0x5000 (hors page patch ✓)")
    d = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
    print(f"    BASERELOC {d.VirtualAddress:#x}/{d.Size:#x} intact")

    # 8. diff chirurgical demo.6 -> demo.7
    print("=" * 72)
    ancien = subprocess.run(
        ["git", "-C", str(REPO), "show", "HEAD:demo/demo.exe"],
        capture_output=True).stdout
    if len(ancien) == len(data):
        diffs = [i for i in range(len(data)) if ancien[i] != data[i]]
        bornes_code = (rva_to_off(pe, 0x4531), rva_to_off(pe, 0x4556))
        hors_code = [i for i in diffs
                     if not (bornes_code[0] <= i < bornes_code[1])]
        print(f"[8] diff demo.6 → demo.7 : {len(diffs)} octets "
              f"({len(diffs) - len(hors_code)} dans .protger, "
              f"{len(hors_code)} ailleurs : version u64 + L00 + somme R10)")
        bon = len(diffs) == 7 and len(diffs) - len(hors_code) == 3
        ok &= bon
        print(f"    {'CHIRURGICAL CONFORME (3 octets de code)' if bon else 'ÉTENDUE INATTENDUE !'}")
    else:
        print("[8] demo.6 introuvable dans git — diff ignoré")

    print("=" * 72)
    print(f"VERDICT : {'TOUT CONFORME — demo.7 prête pour le terrain' if ok else 'DIVERGENCES !'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
