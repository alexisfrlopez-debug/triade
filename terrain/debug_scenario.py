#!/usr/bin/env python3
"""debug_scenario.py — Diagnostique le scénario sup-09 en émulation."""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util as ilu
_spec = ilu.spec_from_file_location("layout_terrain", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "layout.py"))
L = ilu.module_from_spec(_spec)
_spec.loader.exec_module(L)

import oracle_terrain as od
import build_terrain as bt

blocs, specs, code, verrous = bt.assembler_tout()
texte, rdata, data, text2 = bt.composer_sections(code, blocs)
exe = bt.ecrire_pe32plus(texte, rdata, data, text2)

demo17 = od._journal_demo_17()
em = od.Emulateur(exe)
em.installer_shims()
em.uc.mem_write(od.IMAGE + L.HWND_JOURNAL, struct.pack("<Q", od.FAKE_HWND_EDIT))
od.preparer_scenario(em, demo17)

# exécuter T1 seul, T2 seul, T3 seul pour isoler
for nom, rva in (("T1", L.ZONE_T1[0]), ("T2", L.ZONE_T2[0]), ("T3", L.ZONE_T3[0])):
    em2 = od.Emulateur(exe)
    em2.installer_shims()
    em2.uc.mem_write(od.IMAGE + L.HWND_JOURNAL, struct.pack("<Q", od.FAKE_HWND_EDIT))
    od.preparer_scenario(em2, demo17)
    r = em2.appeler(rva)
    print(f"--- {nom} : rax = {r} ---")
    for ligne in em2.journal_fichier:
        print("   ", ligne[:76])
    print("    processus:", [(p['cmdline'][:40], p.get('hproc')) for p in em2.processus])
    print("    stdin:", em2.stdin_proxy, "| suppressions:", [s.split(chr(92))[-1] for s in em2.suppressions])
