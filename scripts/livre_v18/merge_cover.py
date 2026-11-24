#!/usr/bin/env python3
"""TRIADE — fusion couverture + corps pour le Livre du Coffre (v1.0, D133).
(appelable depuis la racine : chemins absolus).

Miroir de spec_v060/merge_cover.py : normalisation A4 stricte de la couverture
et métadonnées posées au writer.

D134 — le bloc de constantes (HERE/COVER/BODY/OUT), perdu à la consignation
de 7c9a09c, est rétabli : le script redevient exécutable depuis la racine,
condition de la chaîne build_livre.sh (M5-a).
"""
import os
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
COVER = os.path.join(HERE, "cover.pdf")
BODY = os.path.join(HERE, "main.pdf")
OUT = os.path.join(HERE, "final.pdf")

A4_W, A4_H = 595.28, 841.89

writer = PdfWriter()
couverture = PdfReader(COVER).pages[0]
couverture.scale_to(A4_W, A4_H)
writer.add_page(couverture)
for page in PdfReader(BODY).pages:
    writer.add_page(page)

writer.add_metadata({
    "/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.14)",
    "/Author": "Alexis FR-LOPEZ ; Agent Z.ai (GLM)",
    "/Subject": "Le coffre-fort du protocole TRIADE : générations, cérémonies, runbook du maître",
    "/Creator": "TRIADE — chaîne LaTeX/Tectonic (D25/D81/D133)",
    "/Keywords": "TRIADE, coffre-fort, CF1, CF2, CF3, Shamir, piège, cérémonie, sachet, runbook",
})

with open(OUT, "wb") as f:
    writer.write(f)
print("final.pdf :", len(PdfReader(OUT).pages), "pages")
