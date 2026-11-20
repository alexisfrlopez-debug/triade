#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correctif de pieds de page WPS — Protocole Triade (manuel développeur).

1. Identifie les pieds de page par leur marqueur de couleur :
   - 888888 → section sommaire → champ PAGE avec \\* ROMAN
   - 666666 → section corps   → champ PAGE avec \\* arabic
2. Supprime les <w:pgNumType/> vides du document.xml (section couverture).

Usage : python3 patch_pieds.py <fichier.docx>
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path


def corriger_xml(xml: str, format_page: str) -> tuple[str, int]:
    motif = re.compile(r"(<w:instrText[^>]*>)\s*PAGE\s*(</w:instrText>)")
    compteur = 0

    def remplacer(correspondance: re.Match) -> str:
        nonlocal compteur
        compteur += 1
        return correspondance.group(1) + f" PAGE \\* {format_page} \\* MERGEFORMAT " + correspondance.group(2)

    return motif.sub(remplacer, xml), compteur


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage : python3 patch_pieds.py <fichier.docx>", file=sys.stderr)
        return 2
    chemin = Path(sys.argv[1])
    if not chemin.is_file():
        print(f"Erreur : {chemin} introuvable.", file=sys.stderr)
        return 2

    temporaire = chemin.with_suffix(".docx.tmp")
    rapports = []

    with zipfile.ZipFile(chemin, "r") as entree, zipfile.ZipFile(temporaire, "w", zipfile.ZIP_DEFLATED) as sortie:
        for info in entree.infolist():
            donnees = entree.read(info.filename)
            nom = info.filename
            if nom.startswith("word/footer") and nom.endswith(".xml"):
                xml = donnees.decode("utf-8")
                if "888888" in xml:
                    xml, nb = corriger_xml(xml, "ROMAN")
                    if nb:
                        rapports.append(f"{nom} : {nb} champ(s) PAGE → ROMAN")
                elif "666666" in xml:
                    xml, nb = corriger_xml(xml, "arabic")
                    if nb:
                        rapports.append(f"{nom} : {nb} champ(s) PAGE → arabic")
                donnees = xml.encode("utf-8")
            elif nom == "word/document.xml":
                xml = donnees.decode("utf-8")
                avant = xml.count("<w:pgNumType/>")
                xml = xml.replace("<w:pgNumType/>", "")
                if avant:
                    rapports.append(f"document.xml : {avant} <w:pgNumType/> vide(s) supprimé(s)")
                donnees = xml.encode("utf-8")
            sortie.writestr(info, donnees)

    shutil.move(str(temporaire), str(chemin))
    for rapport in rapports:
        print(rapport)
    if not rapports:
        print("Aucune correction nécessaire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
