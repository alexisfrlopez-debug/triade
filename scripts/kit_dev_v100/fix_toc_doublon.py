#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige le doublon de la première entrée du sommaire (champ TOC).

Problème : la première entrée du champ TOC existe deux fois — une fois sous
forme d'hyperlien dont le PAGEREF est fusionné dans un seul run (rendu sans
numéro de page), et une fois sous forme d'entrée stylée TOC1 avec numéro.

Correctif :
1. reconstruire le PAGEREF de l'hyperlien en runs séparés, avec le numéro
   de page en cache repris de l'entrée dupliquée ;
2. supprimer l'entrée stylée TOC1 qui duplique le même titre.

Usage : python3 fix_toc_doublon.py <fichier.docx>
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path


def reconstruire_pageref(xml: str) -> tuple[str, str | None]:
    """Reconstruit le PAGEREF fusionné de l'hyperlien ; renvoie (xml, numéro)."""
    motif = re.compile(
        r'<w:r><w:fldChar w:fldCharType="begin"[^/]*/>'
        r'<w:instrText[^>]*> ?PAGEREF (_Toc\d+)[^<]*</w:instrText>'
        r'<w:fldChar w:fldCharType="separate"/>'
        r'(?:<w:r><w:t>(\d+)</w:t></w:r>)?'
        r'<w:fldChar w:fldCharType="end"/></w:r>'
    )
    correspondance = motif.search(xml)
    if not correspondance:
        return xml, None
    ancre = correspondance.group(1)
    numero = correspondance.group(2) or "1"

    def construire(m: re.Match) -> str:
        return (
            '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            f'<w:r><w:instrText xml:space="preserve">PAGEREF {ancre} \\h</w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r><w:t>{numero}</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        )

    return motif.sub(construire, xml, count=1), numero


def supprimer_doublon_stylé(xml: str, titre: str) -> tuple[str, bool]:
    """Supprime l'entrée stylée TOC1 portant le même titre que l'hyperlien."""
    motif_paragraphe = re.compile(
        r'<w:p>(?:(?!</w:p>).)*?<w:pStyle w:val="TOC1"/>(?:(?!</w:p>).)*?</w:p>',
        re.S,
    )
    for candidat in motif_paragraphe.finditer(xml):
        paragraphe = candidat.group(0)
        if "w:hyperlink" in paragraphe:
            continue
        texte = "".join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', paragraphe)).strip()
        if texte == titre or texte == titre + "1":
            return xml[: candidat.start()] + xml[candidat.end():], True
    return xml, False


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage : python3 fix_toc_doublon.py <fichier.docx>", file=sys.stderr)
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
            if info.filename == "word/document.xml":
                xml = donnees.decode("utf-8")

                xml, numero = reconstruire_pageref(xml)
                if numero is not None:
                    rapports.append(f"PAGEREF de la première entrée reconstruit (numéro {numero})")

                hyperlien = re.search(
                    r'<w:hyperlink[^>]*w:anchor="_Toc\d+"[^>]*>(.*?)</w:hyperlink>', xml, re.S
                )
                if hyperlien:
                    titre = "".join(re.findall(
                        r'<w:t[^>]*>([^<]*)</w:t>', hyperlien.group(1)
                    )).strip()
                    xml, supprime = supprimer_doublon_stylé(xml, titre)
                    if supprime:
                        rapports.append("entrée stylée dupliquée supprimée")

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
