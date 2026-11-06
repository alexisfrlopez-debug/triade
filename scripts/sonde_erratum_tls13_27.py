#!/usr/bin/env python3
"""sonde_erratum_tls13_27.py — LA PIÈCE de l'erratum n° 4 (le chantier du
build M9, 06/11) : assemble les notations tls13-27 et tls13-28 à leurs RVA
du plan, calcule les bornes réelles du code, et NOMME le chevauchement.

LE CONSTAT sur pièces (AVANT la réparation) : tls13-27 mesuré 2906 o (la
re-mesure après les DOUZE fautes corrigées du geste poignée — la première
mesure disait 2864 o -> slot 0xB40), le slot ré-arrêté 0xB80 SANS DÉPLACER
tls13-28 (demeuré 0x10A80) : la fin du code [0x10A80, 0x10A9A) recouvrait
le socle posé à 0x10A80 — .refus_pre_taille @0x10A80 (le verdict -2) et
.refus_contexte_nul @0x10A92 (le verdict -1) de la machine d'états vivaient
DANS tls13-28. Le harnais n'a pas vu : la pose n'écrit que le code, et les
chemins -1/-2 n'étaient jamais exercés.

LA RÉPARATION (la source unique) : tls13/layout.py — TLS28_VA 0x10A80 ->
0x10AC0 (la fin du slot ré-arrêté de 27), les notations 27/28 re-générées
par outils/auteur.py, harnais_poignee.py re-joué VERT 52/52 × 3 graines.
Rejouer la sonde APRÈS réparation : plus AUCUN chevauchement.
"""

import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))          # scripts/
T = os.path.dirname(ICI)                                   # triade/
TLS = os.path.join(T, "tls13")
sys.path.insert(0, os.path.join(T, "m4"))
sys.path.insert(0, os.path.join(T, "m4", "outils"))

spec = importlib.util.spec_from_file_location(
    "layout_tls13", os.path.join(TLS, "layout.py"))
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

spec_b4 = importlib.util.spec_from_file_location(
    "build_m4", os.path.join(T, "m4", "build_m4.py"))
B4 = importlib.util.module_from_spec(spec_b4)
sys.modules["build_m4"] = B4
spec_b4.loader.exec_module(B4)

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

ks = Ks(KS_ARCH_X86, KS_MODE_64)

for bid, nom in (("h100027", "tls13-27-principal-machine-etats"),
                 ("h100028", "tls13-28-socle-appel")):
    rva, slot = L.SLOTS_TLS13[bid]
    chemin = os.path.join(TLS, "notation", nom + ".asm")
    octets, metas = B4.assembler_bloc(ks, chemin, rva, slot)
    print(f"{bid} ({nom}) : RVA {rva:#x}, slot {slot:#x}, "
          f"code {len(octets)} o -> bornes [{rva:#x}, {rva + len(octets):#x})")
    # les dernières instructions (capstone)
    import capstone
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    insns = list(cs.disasm(octets, rva))
    for i in insns[-8:]:
        print(f"    {i.address:#x}: {i.mnemonic} {i.op_str}")

rva27, slot27 = L.SLOTS_TLS13["h100027"]
rva28, slot28 = L.SLOTS_TLS13["h100028"]
print(f"\ntls13-27 slot fin : {rva27 + slot27:#x} ; tls13-28 RVA : {rva28:#x}")
if rva27 + slot27 > rva28:
    print(f"CHEVAUCHEMENT DU SLOT : {rva27 + slot27 - rva28} o recouvrent tls13-28")
    sys.exit(1)
print("SLOTS DISJOINTS — l'erratum n° 4 réparé (le socle à la fin du slot du principal)")
