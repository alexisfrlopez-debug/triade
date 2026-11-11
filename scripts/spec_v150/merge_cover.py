#!/usr/bin/env python3
"""TRIADE — fusion couverture + corps (chemins absolus, appelable de la racine).

Miroir de scripts/spec_v070/merge_cover.py : normalisation A4 stricte de la
couverture (écart 794px/A4) et métadonnées posées au writer (hyperref ne
traverse pas PdfWriter). Chemins ABSOLUS : build_pdf.sh appelle depuis la racine.
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
couverture.scale_to(A4_W, A4_H)          # normalisation SANS seuil
writer.add_page(couverture)
for page in PdfReader(BODY).pages:
    writer.add_page(page)

writer.add_metadata({
    "/Title": "Protocole TRIADE v0.15.0 — spécification technique",
    "/Author": "Alexis FR-LOPEZ ; Agent Z.ai (GLM)",
    "/Subject": "Gouvernance vérifiable du développement logiciel assisté par IA",
    "/Creator": "TRIADE — chaîne LaTeX/Tectonic (D25/D81/D133/D137/D169/D176)",
    "/Keywords": "TRIADE, agent-first, contrat, vérification, gouvernance, "
                 "profils, souveraineté cryptographique, coffre-fort",
})

with open(OUT, "wb") as f:
    writer.write(f)
print("final.pdf :", len(PdfReader(OUT).pages), "pages")
