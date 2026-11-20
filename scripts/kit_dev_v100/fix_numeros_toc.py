#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remplace les numéros de page estimés du sommaire par les numéros réels.

add_toc_placeholders.py injecte des numéros approximatifs dans les entrées du
sommaire ; ce script mesure les numéros réels sur le PDF rendu (le corps
commence à la page PDF 4 = page 1 du corps) et met à jour les entrées stylées
du TOC ainsi que le numéro en cache du PAGEREF de la première entrée.

Usage : python3 fix_numeros_toc.py <fichier.docx> <fichier.pdf>
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def normaliser(texte: str) -> str:
    texte = texte.replace("\u2019", "'").replace("\u00a0", " ")
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()


def pages_pdf(pdf: Path) -> dict[int, set[str]]:
    nb_pages = 0
    infos = subprocess.run(
        ["pdfinfo", str(pdf)], capture_output=True, text=True, check=True
    ).stdout
    for ligne in infos.splitlines():
        if ligne.startswith("Pages:"):
            nb_pages = int(ligne.split(":", 1)[1])
    pages: dict[int, set[str]] = {}
    for page in range(1, nb_pages + 1):
        texte = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
            capture_output=True, text=True, check=True
        ).stdout
        pages[page] = {normaliser(l) for l in texte.splitlines() if l.strip()}
    return pages


def trouver_page(pages: dict[int, set[str]], titre: str) -> int | None:
    titre_norm = normaliser(titre)
    for page in sorted(pages):
        if page < 4:  # le corps commence à la page PDF 4
            continue
        if titre_norm in pages[page]:
            return page
    return None


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage : python3 fix_numeros_toc.py <fichier.docx> <fichier.pdf>", file=sys.stderr)
        return 2
    chemin_docx, chemin_pdf = Path(sys.argv[1]), Path(sys.argv[2])
    if not chemin_docx.is_file() or not chemin_pdf.is_file():
        print("Erreur : fichier introuvable.", file=sys.stderr)
        return 2

    pages = pages_pdf(chemin_pdf)
    corrections: dict[str, str] = {}
    introuvables: list[str] = []

    motif_paragraphe = re.compile(
        r'<w:p>(?:(?!</w:p>).)*?<w:pStyle w:val="TOC[12]"/>(?:(?!</w:p>).)*?</w:p>',
        re.S,
    )

    temporaire = chemin_docx.with_suffix(".docx.tmp")
    with zipfile.ZipFile(chemin_docx, "r") as entree, zipfile.ZipFile(temporaire, "w", zipfile.ZIP_DEFLATED) as sortie:
        for info in entree.infolist():
            donnees = entree.read(info.filename)
            if info.filename == "word/document.xml":
                xml = donnees.decode("utf-8")

                # Première passe : mesurer les numéros réels.
                for candidat in motif_paragraphe.finditer(xml):
                    paragraphe = candidat.group(0)
                    textes = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', paragraphe)
                    if len(textes) < 2:
                        continue
                    titre = html.unescape("".join(textes[:-1]))
                    page = trouver_page(pages, titre)
                    if page is None:
                        introuvables.append(titre)
                        continue
                    corrections[titre] = str(page - 3)  # corps = page PDF - 3

                # Seconde passe : appliquer les numéros réels.
                def remplacer(candidat: re.Match) -> str:
                    paragraphe = candidat.group(0)
                    textes = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', paragraphe)
                    if len(textes) < 2:
                        return paragraphe
                    titre = html.unescape("".join(textes[:-1]))
                    if titre not in corrections:
                        return paragraphe
                    numero = corrections[titre]
                    # Le numéro de page est le dernier run du paragraphe dont
                    # le texte est purement numérique : on remplace la
                    # dernière occurrence <w:t>chiffres</w:t>.
                    occurrences = list(re.finditer(r'<w:t>(\d+)</w:t>', paragraphe))
                    if not occurrences:
                        return paragraphe
                    derniere = occurrences[-1]
                    return (
                        paragraphe[: derniere.start()]
                        + f"<w:t>{numero}</w:t>"
                        + paragraphe[derniere.end():]
                    )

                xml = motif_paragraphe.sub(remplacer, xml)

                # Numéro en cache du PAGEREF de la première entrée (hyperlien).
                hyperlien = re.search(
                    r'<w:hyperlink[^>]*w:anchor="_Toc\d+"[^>]*>(.*?)</w:hyperlink>', xml, re.S
                )
                if hyperlien:
                    titre = html.unescape("".join(re.findall(
                        r'<w:t[^>]*>([^<]*)</w:t>', hyperlien.group(1)
                    ))).strip()
                    titre_propre = re.sub(r"\d+$", "", titre).strip()
                    if titre_propre in corrections:
                        numero = corrections[titre_propre]
                        xml = re.sub(
                            r'(<w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>)\d+(</w:t>)',
                            r"\g<1>" + numero + r"\g<2>", xml, count=1
                        )

                donnees = xml.encode("utf-8")
            sortie.writestr(info, donnees)

    shutil.move(str(temporaire), str(chemin_docx))
    print(f"{len(corrections)} entrées du sommaire recalculées sur les numéros réels.")
    if introuvables:
        print("Titres introuvables dans le PDF (numéro estimé conservé) :")
        for titre in introuvables:
            print("  -", titre[:70])
    return 0


if __name__ == "__main__":
    sys.exit(main())
