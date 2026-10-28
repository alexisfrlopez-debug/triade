#!/usr/bin/env python3
"""Fusion couverture + corps pour la spécification TRIADE v0.4.0."""
import os
import sys

from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
COVER = os.path.join(HERE, "cover.pdf")
BODY = os.path.join(HERE, "main.pdf")
OUT = os.path.join(HERE, "final.pdf")

A4_W, A4_H = 595.28, 841.89

TITLE = "Protocole TRIADE v0.4.0 — spécification technique"
AUTHOR = "Alexis FR-LOPEZ ; Agent Z.ai (GLM)"
SUBJECT = ("Gouvernance vérifiable du développement logiciel assisté par IA — "
           "spécification v0.4.0")
KEYWORDS = ("TRIADE, agent-first, contrat, vérification, gouvernance, profils, "
            "traçabilité, tableau de bord")


def normalize_page_to_a4(page):
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
    print(f"final OK -> {OUT} ({n} pages, {os.path.getsize(OUT)/1024:.1f} Kio)")


if __name__ == "__main__":
    main()
