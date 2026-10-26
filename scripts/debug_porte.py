#!/usr/bin/env python3
"""debug_porte.py — Reproduit porte_r10 cible par cible et diagnostique."""
import sys

sys.path.insert(0, "/home/z/my-project/triade/m2")
import layout as L
import oracle_m2 as O
import build_m2 as B
from unicorn import UcError
from unicorn.x86_const import (UC_X86_REG_RIP, UC_X86_REG_RBX, UC_X86_REG_R12,
                               UC_X86_REG_R13, UC_X86_REG_R14)

blocs, specs, code, verrous = B.assembler_tout(1)
texte, rdata, data, text2, staging = B.composer_sections(code, blocs, 1)
exe = B.ecrire_pe32plus(texte, rdata, data, text2)

for cible in [L.ECHO_ENTREE, 0x4400, 0x4800, 0x4980, 0x4B00, 0x1800]:
    m = bytearray(exe)
    m[O._base_fichier(cible) + 11] ^= 0xFF
    em = O.Emulateur(bytes(m))
    em.installer_shims()
    try:
        em.appeler(0x1800, limite=10_000_000)
        print(f"cible {cible:#x} : sortie={bytes(em.sortie)!r} code={em.code_sortie} "
              f"ws2={len(em.appels_ws2)}")
    except UcError as e:
        rip = em.uc.reg_read(UC_X86_REG_RIP)
        rbx = em.uc.reg_read(UC_X86_REG_RBX)
        print(f"cible {cible:#x} : CRASH {e} rip={rip:#x} (RVA {rip - O.IMAGE:#x}) "
              f"rbx={rbx:#x} octets={em.uc.mem_read(rip, 8).hex()}")
