#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debug_double_moteur.py — l'échantillon réduit, le bac fixe, les flux
complets à la loupe."""
import json
import pathlib
import sys

sys.path.insert(0, "/home/z/my-project/depot/atelier-cout-boucle-cq01qv1za")
from moteur_qemu import (ReferenceUnicorn, VolumeQEMU, echantillon_ops)

bac = pathlib.Path("/tmp/dbl-debug")
bac.mkdir(exist_ok=True)

ops, fichiers = echantillon_ops()
ops = [op for op in ops if op[0] != "lire" or True]
# réduit : temoin-384 seulement — ouvrir + 3 lire + fermer + etat
reduit: list[tuple] = []
nom = "temoin-384.bin"
reduit.append(("ouvrir", nom))
for dec in (0, 16, 368):
    reduit.append(("lire", dec))
reduit.append(("fermer",))
reduit.append(("etat",))

ref = ReferenceUnicorn()
ref.declarer_temoins({k: v for k, v in fichiers.items()})
flux_ref = ref.executer(reduit)
(bac / "flux-unicorn.jsonl").write_text("\n".join(flux_ref) + "\n")

vol = VolumeQEMU(bac / "qemu")
vol.construire_image()
flux_qemu = vol.executer(reduit, fichiers)
(bac / "flux-qemu.jsonl").write_text("\n".join(flux_qemu) + "\n")

for nom_flux, flux in (("UNICORN", flux_ref), ("QEMU", flux_qemu)):
    print(f"===== {nom_flux} =====")
    for l in flux:
        d = json.loads(l)
        print(f"  op={d['op']} detail={d.get('detail','')} rax={d.get('rax')} "
              f"propre={d.get('propre')} poignee={d.get('poignee')} "
              f"taille={d.get('taille')} rempl={d.get('remplissage')} "
              f"crash={d.get('crash','')!r} tampon[:24]={d.get('tampon','')[:24]}")
print()
for i, (a, b) in enumerate(zip(flux_ref, flux_qemu)):
    if a != b:
        print(f"PREMIÈRE DIVERGENCE ligne {i} :")
        print("  U:", a)
        print("  Q:", b)
        break
else:
    print("DIVERGENCE=0 sur l'échantillon réduit")
