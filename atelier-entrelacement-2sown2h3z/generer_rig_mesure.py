#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generer_rig_mesure.py — prépare les données du rig natif (2sown2h3z) :
le calendrier de clés, les compteurs, le clair 4096 o, H et LA TABLE des
puissances DÉRIVÉE PAR LE SCELLÉ (255 appels chaînés), le tout vers un
fichier d'en-tête C pour le rig (mesurer_entrelacement.c)."""
import pathlib
import random
import struct
import sys

sys.path.insert(0, "/home/z/my-project/depot/atelier-entrelacement-2sown2h3z")
from piloter_entrelacement import (assembler, machine, table_puissances,
                                   SC16, SC17, GRAINE)
from piloter_entrelacement import expansion_cle

ICI = pathlib.Path("/home/z/my-project/depot/atelier-entrelacement-2sown2h3z")
N = 256

rng = random.Random(GRAINE)
cles = expansion_cle(bytes(rng.getrandbits(8) for _ in range(16)))
H = bytes(rng.getrandbits(8) for _ in range(16))
compteurs = bytes(rng.getrandbits(8) for _ in range(16 * N))
clair = bytes(rng.getrandbits(8) for _ in range(16 * N))

octets16 = assembler(SC16, 0xDF00)
octets17 = assembler(SC17, 0xDFC0)
octets_c = assembler(ICI / "notation" / "ctr-v4i-ghash-agrege4.asm", 0xF800)
uc = machine(octets16, octets17, octets_c)
table = table_puissances(uc, N, H)
assert len(table) == 16 * N, len(table)


def c_tab(nom: str, donnees: bytes) -> str:
    lignes = []
    for i in range(0, len(donnees), 16):
        morceau = donnees[i:i + 16]
        lignes.append(", ".join(f"0x{b:02x}" for b in morceau) + ",")
    return f"static unsigned char {nom}[{len(donnees)}] = {{\n" + \
        "\n".join(lignes) + "\n};"


entete = f"""/* les donnees du rig (2sown2h3z) — la graine {GRAINE}, la table
 * des puissances DERIVEE PAR LE SCELLÉ (255 appels chaînés tls13-17) */
#define N_BLOCS {N}
{c_tab('CLES', cles)}
{c_tab('H', H)}
{c_tab('COMPTEURS', compteurs)}
{c_tab('CLAIR', clair)}
{c_tab('TABLE', table)}
"""
(ICI / "native" / "donnees_rig.h").write_text(entete, encoding="utf-8")
print(f"OK : donnees_rig.h (cles 176 o, H 16 o, compteurs/clair "
      f"{16 * N} o, table {len(table)} o — la graine {GRAINE})")
