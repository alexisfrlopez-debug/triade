#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v194.py — LE LINTER INTER-PIÈCES de l'édition v0.19.4 (D218
reconduit, ÉTENDU à l'instruction cq01qv1za : « nouvelles assertions
M4/tokens au linter, base d'arrondi canonisée »).

Fail-closed : toute divergence d'une valeur partagée entre les CINQ
pièces du pack v0.19.4 REFUSE le build. LES NOUVELLES ASSERTIONS
OPT-04/M4 :
  — le canon M4 17,9× (la base d'arrondi consignée — l'écart 17,8× de
    la pièce R11 verbatim demeurant NOMMÉ à côté au manuscrit) ;
  — LE NOUVEAU CANON OPT-04 : le ratio de régime 3,0×, le régime 6,8 s,
    H5 TENUE — la falsification D204 (×23,9) demeurant consignée au
    manuscrit comme MESURÉE ET DATÉE ;
  — les chiffres du pointeur seul : −35,7 % au total, −93,3 % à la
    réponse (le manuscrit ET la présentation) ;
  — les versions croisées : manuscrit v0.19.4 ↔ spécification v0.15.4 ↔
    Livre v1.3 ;
  — LA VISIBILITÉ AU STATUT EXACT (depuis l'Entrée 369) : le dépôt
    PUBLIC (D220) porté par la présentation ; le DOI Zenodo vivant.

Usage : python3 linter_v194.py   # exit 1 si ROUGE"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
PIECES = {
    "manuscrit": REPO / "edition-v0194" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v154" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v13" / "final.pdf",
    "preuves": REPO / "scripts" / "vague7"
    / "TRIADE_preuves_et_calculs_v0.19.4.pdf",
    "presentation": REPO / "scripts" / "vague7"
    / "TRIADE_presentation_20261120_v194.pdf",
}


def extraire(chemin):
    txt = subprocess.run(["pdftotext", str(chemin), "-"],
                         capture_output=True, check=True).stdout.decode(
                             "utf-8", "replace")
    return re.sub(r"\s+", " ",
                  txt.replace("\u2013", "-").replace("\u2014", "-")
                     .replace("\u2009", " ").replace("\u202f", " ")
                     .replace("\u00a0", " "))


class Verdict:
    def __init__(self):
        self.verts, self.rouges = 0, []

    def exige(self, piece, marqueurs, nom, tous=True):
        t = self.textes[piece]
        ok = all(m in t for m in marqueurs) if tous \
            else any(m in t for m in marqueurs)
        if ok:
            self.verts += 1
            print(f"VERT  {nom}")
        else:
            self.rouges.append(nom)
            print(f"ROUGE {nom} — {' et '.join(repr(m) for m in marqueurs)}"
                  f" absent(s) de la pièce {piece}")

    def interdit(self, piece, motif, nom):
        t = self.textes[piece]
        if motif in t:
            self.rouges.append(nom)
            print(f"ROUGE {nom} — le motif interdit {motif!r} EST PRÉSENT "
                  f"({piece})")
        else:
            self.verts += 1
            print(f"VERT  {nom}")


def controle(verbeux=True):
    v = Verdict()
    v.textes = {nom: extraire(chemin) for nom, chemin in PIECES.items()}

    # ---- les versions croisées ------------------------------------------
    v.exige("manuscrit", ["v0.19.4"], "le manuscrit v0.19.4")
    v.exige("specification", ["v0.15.4"], "la spécification v0.15.4")
    v.exige("livre", ["v1.3"], "le Livre v1.3 (inchangé)")

    # ---- LE CANON M4 (la base d'arrondi consignée, D218 reconduit) -------
    v.exige("manuscrit", ["17.9"], "le canon M4 17,9x (manuscrit)")
    v.exige("presentation", ["17,9"], "le canon M4 17,9x (présentation)")

    # ---- LES NOUVELLES ASSERTIONS OPT-04 ---------------------------------
    v.exige("manuscrit", ["3.0", "6.8", "held as of v0.19.4"],
            "H5 TENUE depuis OPT-04 — le ratio 3,0x et le régime 6,8 s "
            "(manuscrit)")
    v.exige("manuscrit", ["falsified - 52.5"],
            "la falsification D204 DEMEURE consignée (jamais effacée)")
    v.exige("preuves", ["3,0", "6,8", "H5 DEVIENT TENUE"],
            "le canon OPT-04 (preuves)")
    v.exige("presentation", ["3,0", "6,8", "TENUE depuis OPT-04"],
            "le canon OPT-04 (présentation)")
    v.exige("manuscrit", ["35.7", "93.3", "POINTEUR SEUL"],
            "les chiffres du pointeur seul (manuscrit — la ligne de date "
            "les porte, l'adoption au RQ2 français)")
    v.exige("presentation", ["35,7", "93,3"],
            "les chiffres du pointeur seul (présentation)")
    v.exige("preuves", ["35,7", "93,3"], "les chiffres du pointeur (preuves)")
    v.exige("specification", ["POINTEUR SEUL", "35,7"],
            "le pointeur seul à la spécification (règle additive D222)")

    # ---- LA VISIBILITÉ AU STATUT EXACT (l'Entrée 369) --------------------
    v.exige("presentation", ["PUBLIC (D220", "10.5281/zenodo.24367344"],
            "le dépôt PUBLIC (D220) et le DOI vivant (présentation)")

    # ---- les motifs interdits (D182/D190, la visibilité prématurée) ------
    v.interdit("presentation",
               "sans compilateur ni langage de programmation",
               "la formulation D182/D190 (jamais la forme interdite)")
    v.interdit("manuscrit", "sans compilateur ni langage de programmation",
               "la formulation D182/D190 (manuscrit)")

    print()
    if v.rouges:
        print(f"LE LINTER v194 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              "LE BUILD EST REFUSÉ")
        return 1
    print(f"LE LINTER v194 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    sys.exit(controle())
