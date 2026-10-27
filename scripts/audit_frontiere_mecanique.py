#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Audit de la frontière mécanique (post-demo.5, journal gelé après
J_LIBC_OK alors que D39 a corrigé le DEP).

Objet : confronter les octets RÉELS de demo.exe (md5 221f4578…) à la
notation, désassembler la chaîne exacte exécutée entre J_LIBC_OK et
J_MEC_OK, et vérifier chaque hypothèse de mort silencieuse :
  1. .protger (0x4531) : encodage du and rcx,~0xFFF, params VirtualProtect,
     alignement pile, sauvegarde des octets, retour vérifié ;
  2. écho v1 (0x4600) + payload v2 (table .rdata) : position-indépendance,
     bornes, cohérence checksum ;
  3. jmp de patch : E9 rel32 → cible exactement 0x4680 ;
  4. scénario win-09 : séquence écho#1/memcmp/patch/écho#2/... et
     chemins d'échec (tous journalisés — donc incompatibles avec la
     mort silencieuse observée).

Usage : .venv/bin/python scripts/audit_frontiere_mecanique.py
"""

import pathlib
import sys

import capstone
import pefile

REPO = pathlib.Path(__file__).resolve().parents[1]
EXE = REPO / "demo" / "demo.exe"

BASE = 0x140000000


def rva_to_off(pe, rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.Misc_VirtualSize:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    raise ValueError(f"RVA {rva:#x} hors sections")


def main():
    data = EXE.read_bytes()
    pe = pefile.PE(str(EXE), fast_load=True)

    print("=" * 72)
    print("[0] Empreinte du binaire audité")
    import hashlib
    md5 = hashlib.md5(data).hexdigest()
    sha = hashlib.sha256(data).hexdigest()
    print(f"    taille {len(data):,} o — md5 {md5}")
    print(f"    sha256 {sha}")
    attendu = "221f4578a6f6059dacf94dd66ea242db"
    print(f"    attendu demo.5 : {attendu} → {'CONFORME' if md5 == attendu else 'DIVERGENT !'}")

    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False

    def disas(rva, n, titre):
        print("=" * 72)
        print(f"[{titre}] RVA {rva:#x}..{rva + n:#x}")
        off = rva_to_off(pe, rva)
        code = data[off:off + n]
        for ins in md.disasm(code, BASE + rva):
            print(f"    {ins.address - BASE:#06x}: {ins.bytes.hex():<20} {ins.mnemonic} {ins.op_str}")

    # --- 1. .protger (moteur VirtualProtect) -----------------------------
    disas(0x4531, 0x28, "1] .protger (VirtualProtect) — octets réels")

    # --- 2. applique (mode 0) : de la somme au retour --------------------
    disas(0x4451, 0x4A, "2] tcp-07 applique : somme → patch → re-protect")

    # --- 3. écho v1 cible du patch ---------------------------------------
    disas(0x4600, 0x30, "3] écho v1 (cible du patch)")

    # --- 4. croissance (destination du payload v2, état initial) ---------
    disas(0x4680, 0x30, "4] croissance 0x4680 (état initial avant patch)")

    # --- 5. table .rdata : taille, somme attendue, payload ----------------
    off = rva_to_off(pe, 0x2454)
    taille = int.from_bytes(data[off:off + 4], "little")
    somme = int.from_bytes(data[off + 4:off + 12], "little")
    print("=" * 72)
    print(f"[5] table @0x23d0 : taille={taille} o, somme attendue={somme:#x}")
    off_t = rva_to_off(pe, 0x23d0)
    payload = data[off_t:off_t + max(taille, 44)]
    calc = 0
    for i in range(0, (taille // 8) * 8, 8):
        calc += int.from_bytes(data[off_t + i:off_t + i + 8], "little")
    print(f"    somme calculée={calc:#x} → {'CONFORME' if calc == somme else 'DIVERGENTE !'}")
    print(f"    payload ({len(payload)} o) : {payload[:64].hex()}")
    print("    désassemblage du payload (exécuté à 0x4680 après patch) :")
    for ins in md.disasm(payload, BASE + 0x4680):
        print(f"    0x{ins.address - BASE:#06x}: {ins.bytes.hex():<18} {ins.mnemonic} {ins.op_str}")
        if ins.mnemonic == "ret":
            break

    # --- 6. scénario : de .libc_ok à J_MEC_OK ------------------------------
    disas(0x4ca5, 0x60, "6] scénario win-09 : .libc_ok → mécanique (octets réels)")

    # --- 7. chaînes attendues v1/v2 ---------------------------------------
    print("=" * 72)
    print("[7] chaînes du scénario (entrée, attendu v1, attendu v2)")
    for rva, nom in [(0x26ca, "entrée écho (14 o)"),
                     (0x26e8, "attendu v1"),
                     (0x26f6, "attendu v2")]:
        off = rva_to_off(pe, rva)
        brut = data[off:off + 16]
        print(f"    {nom} @ {rva:#x} : {brut[:14]!r}  hex={brut[:14].hex()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
