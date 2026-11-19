#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v195.py — LE LINTER INTER-PIÈCES de l'édition v0.19.5 (D218
reconduit, étendu à l'instruction 1c4sokpii : la clôture de la vague 7).

Fail-closed : toute divergence d'une valeur partagée entre les CINQ
pièces du pack v0.19.5 REFUSE le build. LES ASSERTIONS :

  — les canons reconduits : M4 17,9× ; OPT-04 (3,0× / 6,8 s / H5 tenue ;
    le pointeur −35,7 % / −93,3 %) ; les versions croisées ;
  — LES NOUVELLES ASSERTIONS 1c4sokpii : le critère d'échantillon N = 7
    sans nouveau tirage ; la batterie d'injection 811/832 (97,5 %) ;
    le reste de 21 nommé à treize familles de causes ; le gap nommé de
    l'indépendance inter-familles (jamais simulé) ; le protocole du
    second annotateur pré-enregistré ;
  — LA GOUVERNANCE À L'ÉTAT VÉCU (le correctif v0.19.5) : la cérémonie
    D183 VÉCUE le 19/11 au manuscrit (les lignes « prepared and
    waiting » de la v0.19.4 étaient devenues stales à son scellage) ;
  — LA VISIBILITÉ AU STATUT EXACT : le dépôt PUBLIC (D220) et le DOI
    Zenodo vivant portés par la présentation.

Usage : python3 linter_v195.py   # exit 1 si ROUGE"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
PIECES = {
    "manuscrit": REPO / "edition-v0195" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v154" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v13" / "final.pdf",
    "preuves": REPO / "scripts" / "vague7"
    / "TRIADE_preuves_et_calculs_v0.19.5.pdf",
    "presentation": REPO / "scripts" / "vague7"
    / "TRIADE_presentation_20261120_v195.pdf",
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
    v.exige("manuscrit", ["v0.19.5"], "le manuscrit v0.19.5")
    v.exige("specification", ["v0.15.4"], "la spécification v0.15.4")
    v.exige("livre", ["v1.3"], "le Livre v1.3 (inchangé)")
    v.exige("presentation", ["v0.19.5"], "la présentation v0.19.5")

    # ---- les canons reconduits (M4 / OPT-04) ----------------------------
    v.exige("manuscrit", ["17.9"], "le canon M4 17,9x (manuscrit)")
    v.exige("presentation", ["17,9"], "le canon M4 17,9x (présentation)")
    v.exige("manuscrit", ["3.0", "6.8", "held as of v0.19.4"],
            "H5 TENUE depuis OPT-04 — le ratio 3,0x et le régime 6,8 s "
            "(manuscrit)")
    v.exige("manuscrit", ["falsified - 52.5"],
            "la falsification D204 DEMEURE consignée (jamais effacée)")
    v.exige("presentation", ["3,0", "6,8", "TENUE depuis OPT-04"],
            "le canon OPT-04 (présentation)")
    v.exige("manuscrit", ["35.7", "93.3"],
            "les chiffres du pointeur seul (manuscrit)")
    v.exige("presentation", ["35,7", "93,3"],
            "les chiffres du pointeur seul (présentation)")
    v.exige("specification", ["POINTEUR SEUL", "35,7"],
            "le pointeur seul à la spécification (règle additive D222)")

    # ---- LES NOUVELLES ASSERTIONS 1c4sokpii ------------------------------
    v.exige("manuscrit", ["811/832", "97.5", "thirteen cause families"],
            "la batterie d'injection — 811/832 (97,5 %), le reste nommé "
            "(manuscrit)")
    v.exige("preuves", ["811/832", "97,5"],
            "la batterie d'injection (preuves)")
    v.exige("presentation", ["811/832", "97,5"],
            "la batterie d'injection (présentation)")
    v.exige("manuscrit", ["N =7"],
            "le critère d'échantillon N = 7 (manuscrit)")
    v.exige("preuves", ["N = 7"], "le critère d'échantillon N = 7 (preuves)")
    v.exige("presentation", ["N = 7"],
            "le critère d'échantillon N = 7 (présentation)")
    v.exige("manuscrit", ["1984/2011"],
            "l'épreuve POSIX du bras C (manuscrit)")
    v.exige("preuves", ["1984/2011"], "l'épreuve POSIX du bras C (preuves)")
    v.exige("manuscrit", ["0/64"],
            "la récitation pure 0/64 (manuscrit)")
    v.exige("preuves", ["GAP NOMMÉ", "JAMAIS SIMULÉ", "LA COPIE"],
            "l'indépendance inter-familles au gap nommé (preuves)")
    v.exige("manuscrit", ["without a new draw"],
            "sans nouveau tirage (manuscrit)")

    # ---- LA GOUVERNANCE À L'ÉTAT VÉCU (le correctif v0.19.5) -------------
    v.exige("manuscrit", ["lived end-to-end", "D220"],
            "la cérémonie D183 VÉCUE au manuscrit (le statut exact)")
    v.interdit("manuscrit", "prepared and waiting for the developer's",
               "la ligne stale « prepared and waiting » (plus jamais)")

    # ---- LA VISIBILITÉ AU STATUT EXACT (l'Entrée 369) --------------------
    v.exige("presentation", ["PUBLIC (D220", "10.5281/zenodo.24367344"],
            "le dépôt PUBLIC (D220) et le DOI vivant (présentation)")
    v.exige("presentation", ["D183 VÉCUE"],
            "la gouvernance vécue (présentation)")

    # ---- les motifs interdits (D182/D190, la visibilité prématurée) ------
    v.interdit("presentation",
               "sans compilateur ni langage de programmation",
               "la formulation D182/D190 (jamais la forme interdite)")
    v.interdit("manuscrit", "sans compilateur ni langage de programmation",
               "la formulation D182/D190 (manuscrit)")

    print()
    if v.rouges:
        print(f"LE LINTER v195 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              "LE BUILD EST REFUSÉ")
        return 1
    print(f"LE LINTER v195 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    sys.exit(controle())
