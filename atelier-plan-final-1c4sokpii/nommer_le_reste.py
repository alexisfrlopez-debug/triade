#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nommer_le_reste.py — LE CONTEXTE DE CHAQUE SURVIVANT RESTANT : les ±10
instructions autour du point muté (l'instruction ET ses gardes), le bloc, la
cause candidate lue du contexte — la matière du RESTE NOMMÉ."""
from __future__ import annotations

import csv
import importlib.util
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
ICI = pathlib.Path(__file__).resolve().parent

MUT = importlib.util.spec_from_file_location(
    "mutation_v110_nommer", REPO / "scripts" / "mutation_v110.py")
MUT.module = importlib.util.module_from_spec(MUT)
sys.modules["mutation_v110_nommer"] = MUT.module
MUT.loader.exec_module(MUT.module)


def main():
    reste = list(csv.DictReader(open(ICI / "reste_nomme.csv", encoding="utf-8")))
    blocs = {b["bid"]: b for d in MUT.module.blocs_domaines().values()
             for b in d}
    out = []
    for r in reste:
        bid = r["bid"]
        pos = int(r["offset"], 16)
        b = blocs[bid]
        octets = b["octets"]
        insns = MUT.module.decoder(octets, b["rva"])
        # la fenêtre : les 10 instructions autour
        idx = next(i for i, ins in enumerate(insns)
                   if ins.address - b["rva"] <= pos < ins.address - b["rva"] + ins.size)
        fenetre = insns[max(0, idx - 6):idx + 5]
        lignes_ctx = []
        for ins in fenetre:
            marque = " <<MUTÉ<<" if ins.address - b["rva"] <= pos < ins.address - b["rva"] + ins.size else ""
            lignes_ctx.append(f"  +{ins.address - b['rva']:#06x}  {ins.mnemonic} {ins.op_str}{marque}")
        out.append(f"### {bid} {r['offset']}: {r['octet']}\n" + "\n".join(lignes_ctx))
    (ICI / "reste_contexte.txt").write_text(
        "\n\n".join(out) + "\n", encoding="utf-8")
    print(f"le contexte de {len(reste)} survivants écrit : reste_contexte.txt")


if __name__ == "__main__":
    main()
