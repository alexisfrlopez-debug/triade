#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree.py — insère UNE entrée numérotée au journal de travail.

La règle du marqueur (D134) : les entrées numérotées s'insèrent TOUJOURS
AVANT la première ligne « <!-- m5a:journal-des-builds » ; les lignes de
build s'ajoutent SOUS le marqueur, la plus récente en tête. L'insertion
est REFUSÉE si une entrée de même numéro existe déjà (append-only, la
consignation ne réécrit jamais l'histoire).

Usage : python3 scripts/consigner_entree.py <fichier_entree.md>
Code de sortie : 0 = insérée ; 2 = refus nommé.
"""
import pathlib
import re
import sys

CHEMIN = pathlib.Path(__file__).resolve().parents[1] / "docs" / "JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds"


def refus(nom, detail):
    print(f"[consigner] REFUS {nom} : {detail}")
    sys.exit(2)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    source = pathlib.Path(sys.argv[1])
    if not source.is_file():
        refus("FICHIER", f"{source} absent")
    entree = source.read_text(encoding="utf-8").strip()
    m = re.match(r"^## Entrée (\d+)", entree)
    if not m:
        refus("FORMAT", "le fichier doit commencer par « ## Entrée NNN »")
    numero = m.group(1)

    journal = CHEMIN.read_text(encoding="utf-8")
    if f"## Entrée {numero} " in journal or f"## Entrée {numero} —" in journal:
        refus("DOUBLON", f"l'Entrée {numero} est déjà consignée (append-only)")
    pos = journal.find(MARQUEUR)
    if pos <= 0:
        refus("MARQUEUR", "le marqueur m5a est introuvable — le journal est-il "
                          "entier ?")
    nouveau = journal[:pos] + entree + "\n\n" + journal[pos:]
    CHEMIN.write_text(nouveau, encoding="utf-8")
    print(f"[consigner] OK : l'Entrée {numero} insérée avant le marqueur "
          f"({len(entree)} caractères)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
