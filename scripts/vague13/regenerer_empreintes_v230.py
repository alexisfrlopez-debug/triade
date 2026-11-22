#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_empreintes_v230.py — LE MANIFESTE des empreintes sha256 des
CINQ pièces de l'édition v0.23.0 (chaque empreinte RECALCULÉE du fichier
même ; le manifeste fait foi — les générateurs de présentation et de
preuves gravent les mêmes empreintes, le linter les recoupe)."""
from __future__ import annotations

import hashlib
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]
V13 = REPO / "scripts" / "vague13"
OUT = V13 / "empreintes_livrables_v0.23.0.txt"

PIECES = [
    ("TRIADE_manuscrit_v0.23.0.pdf",
     REPO / "edition-v0230" / "main.pdf"),
    ("Protocole_TRIADE_v0.15.8_Specification.pdf",
     REPO / "scripts" / "spec_v158" / "main.pdf"),
    ("Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf",
     REPO / "scripts" / "livre_v17" / "final.pdf"),
    ("TRIADE_preuves_et_calculs_v0.23.0.pdf",
     V13 / "TRIADE_preuves_et_calculs_v0.23.0.pdf"),
    ("TRIADE_presentation_v230.pdf",
     V13 / "TRIADE_presentation_v230.pdf"),
]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


lignes = [
    "LES EMPREINTES DES LIVRABLES — la vague 13, l'édition v0.23.0",
    "(chaque pièce sha256 ; le manifeste fait foi)",
    "",
]
for nom, chemin in PIECES:
    if not chemin.exists():
        raise SystemExit(f"PIÈCE ABSENTE : {chemin}")
    lignes.append(f"{nom}  sha256:{sha(chemin)}")

OUT.write_text("\n".join(lignes) + "\n", encoding="utf-8")
print(f"[empreintes v230] le manifeste : {OUT}")
for nom, chemin in PIECES:
    print(f"  {sha(chemin)[:16]}…  {nom}")
