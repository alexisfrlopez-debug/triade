#!/usr/bin/env python3
"""Fusion couverture + corps pour l'article TRIADE v0.4.

Assemble cover.pdf (Template 03, 794x1123 px) et main.pdf (Tectonic, A4)
en un PDF final normalisé A4 avec métadonnées complètes.
Pipeline conforme au brief académique : la couverture est fusionnée en
page 0 via pypdf après normalisation.
"""
import os
import sys

from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
COVER = os.path.join(HERE, "cover.pdf")
BODY = os.path.join(HERE, "main.pdf")
OUT = os.path.join(HERE, "final.pdf")

A4_W, A4_H = 595.28, 841.89  # points

TITLE = ("Le protocole TRIADE : gouvernance vérifiable du développement "
         "logiciel assisté par IA — édition académique v0.4")
AUTHOR = "Alexis FR-LOPEZ ; Agent Z.ai (GLM)"
SUBJECT = ("Gouvernance du développement logiciel assisté par IA ; "
           "formalisation du protocole TRIADE ; étude de cas RoomEq")
KEYWORDS = ("développement assisté par IA, dette technique, conception par "
            "contrat, gouvernance logicielle, vérification, étude de cas")


def normalize_page_to_a4(page):
    """Met la page au format A4 si ses dimensions divergent."""
    box = page.mediabox
    w, h = float(box.width), float(box.height)
    if abs(w - A4_W) > 0.5 or abs(h - A4_H) > 0.5:
        page.scale_to(A4_W, A4_H)
    return page


def main():
    for path in (COVER, BODY):
        if not os.path.exists(path):
            sys.exit(f"manquant : {path}")

    writer = PdfWriter()
    writer.add_page(normalize_page_to_a4(PdfReader(COVER).pages[0]))
    for page in PdfReader(BODY).pages:
        writer.add_page(normalize_page_to_a4(page))

    writer.add_metadata({
        "/Title": TITLE,
        "/Author": AUTHOR,
        "/Creator": "Z.ai",
        "/Subject": SUBJECT,
        "/Keywords": KEYWORDS,
    })
    with open(OUT, "wb") as f:
        writer.write(f)

    n = len(PdfReader(OUT).pages)
    size = os.path.getsize(OUT) / 1024
    print(f"final OK -> {OUT} ({n} pages, {size:.1f} Kio)")


if __name__ == "__main__":
    main()
