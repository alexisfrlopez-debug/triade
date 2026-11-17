#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""splice_tour.py — LE GESTE MÉCANIQUE DU LABO : applique le fragment
corrigé (le retour de l'outil de correctif) à la pièce, selon les bornes
du fragment original et le geste nommé. Rien d'intelligent : le labo
remplace les bornes, le geste fait foi."""
from __future__ import annotations

import re
import sys

piece, corrige = sys.argv[1], sys.argv[2]
# les lignes du fragment original (bornes [debut, fin] INCLUSES, 1-based)
debut, fin = int(sys.argv[3]), int(sys.argv[4])
sortie = sys.argv[5]
# le geste nommé : des lignes à retirer HORS fragment (ex. l'equ supprimée)
retirer = [int(x) for x in sys.argv[6].split(",")] if len(sys.argv) > 6 else []

lignes = open(piece, encoding="utf-8").read().splitlines()
nouveau = open(corrige, encoding="utf-8").read().splitlines()

# le bloc corrigé : tout ce qui précède la ligne « le geste : »
bloc = []
for l in nouveau:
    if re.match(r"^le geste\s*:", l.strip()):
        break
    bloc.append(l)
while bloc and not bloc[-1].strip():
    bloc.pop()

# la substitution par bornes (les lignes retirées tombent avant le fragment)
resultat = []
for no, l in enumerate(lignes, 1):
    if no in retirer:
        continue
    if no == debut:
        resultat.extend(bloc)
    elif debut < no <= fin:
        continue
    else:
        resultat.append(l)

open(sortie, "w", encoding="utf-8").write("\n".join(resultat) + "\n")
print(f"[splice] {sortie} : lignes {debut}-{fin} remplacées "
      f"({fin - debut + 1} -> {len(bloc)}), {len(retirer)} retirée(s) "
      f"hors fragment")
