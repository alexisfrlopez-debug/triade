#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v196.py — LE LINTER INTER-PIÈCES de l'édition v0.19.6 (D218
reconduit, étendu à la vague 8 : la cohérence, la gouvernance vécue,
l'intégrité pré-enregistrée, la dérivation-outillée, OPT-05).

Fail-closed : toute divergence d'une valeur partagée entre les CINQ
pièces du pack v0.19.6 REFUSE le build. Usage : python3 linter_v196.py"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
PIECES = {
    "manuscrit": REPO / "edition-v0196" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v155" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v14" / "final.pdf",
    "preuves": REPO / "scripts" / "vague8"
    / "TRIADE_preuves_et_calculs_v0.19.6.pdf",
    "presentation": REPO / "scripts" / "vague8"
    / "TRIADE_presentation_20261120_v196.pdf",
}


def extraire(chemin):
    txt = subprocess.run(["pdftotext", str(chemin), "-"],
                         capture_output=True, check=True).stdout.decode(
                             "utf-8", "replace")
    return re.sub(r"\s+", " ",
                  txt.replace("\u2013", "-").replace("\u2014", "-")
                     .replace("\u2009", " ").replace("\u202f", " ")
                     .replace("\u00a0", " ").replace("\u2212", "-"))


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


def controle():
    v = Verdict()
    v.textes = {nom: extraire(chemin) for nom, chemin in PIECES.items()}

    # ---- les versions croisées --------------------------------------------
    v.exige("manuscrit", ["Academic edition v0.19.6"], "le manuscrit v0.19.6")
    v.exige("specification", ["v0.15.5"], "la spécification v0.15.5")
    v.exige("livre", ["v1.4"], "le Livre du Coffre v1.4")
    v.exige("presentation", ["v0.19.6"], "la présentation v0.19.6")
    v.exige("manuscrit", ["v0.15.5"], "la référence courante à la spec")
    v.exige("livre", ["v0.15.5"], "le Livre à la spec courante")

    # ---- les DOI réconciliés (gq117wphb 2) ---------------------------------
    for piece in ("manuscrit", "preuves", "presentation"):
        v.exige(piece, ["10.5281/zenodo.24367343"],
                f"le concept DOI partout ({piece})")
    v.exige("manuscrit", ["24382460"], "le DOI de version courant nommé")
    v.interdit("presentation", "10.5281/zenodo.24367344",
               "le DOI v0.19.0 plus cité comme référence (présentation)")

    # ---- la probabilité du tirage (gq117wphb 4) -----------------------------
    v.exige("manuscrit", ["one-in-sixteen"], "le tirage à 1/16 (manuscrit)")
    v.interdit("manuscrit", "one-in-eight", "le 1/8 périmé (manuscrit)")

    # ---- H5 : deux verdicts distincts (nunsmzmrm 1) --------------------------
    v.exige("manuscrit", ["H5-D204", "H5-amended"],
            "H5 en deux verdicts distincts et datés")
    v.exige("presentation", ["H5-D204", "H5-amendée-OPT04"],
            "H5 en deux verdicts distincts (présentation)")

    # ---- les canons M4 re-mesurés (pe6iv71fj + gq117wphb 3) ------------------
    v.exige("preuves", ["39,1", "6,6", "1,9"],
            "les médianes M4 re-mesurées (preuves)")
    v.exige("presentation", ["39,1", "3,5"],
            "les médianes M4 (présentation)")
    v.interdit("presentation", "39,7 s",
               "le « avant 39,7 s » périmé (présentation)")

    # ---- RQ2 : le pointeur seul adopté (nunsmzmrm 6) -------------------------
    v.exige("manuscrit", ["1,103"], "la médiane localiser adoptée (manuscrit)")
    v.exige("presentation", ["1 103"], "la médiane localiser (présentation)")
    v.exige("preuves", ["1 103"], "la re-mesure RQ2 (preuves)")

    # ---- OPT-05 : les gains mesurés ------------------------------------------
    v.exige("preuves", ["34,3", "97,7"], "les gains OPT-05 (preuves)")
    v.exige("presentation", ["34,3", "97,7"], "les gains OPT-05 (présentation)")

    # ---- la dérivation-outillée (peap6ws09) -----------------------------------
    v.exige("preuves", ["128 constantes".replace(" ", " "), "zéro divergence"],
            "la dérivation-outillée (preuves)")
    v.exige("presentation", ["128 constantes"],
            "la dérivation-outillée (présentation)")
    v.exige("manuscrit", ["128"],
            "l'indépendance par dérivation (manuscrit, l'abstract)")
    v.exige("preuves", ["1983/2011"], "le bras C loupe-13 (preuves)")

    # ---- les 21 survivants et le score ajusté ----------------------------------
    v.exige("preuves", ["811/820", "98,9"], "le score ajusté (preuves)")
    v.exige("presentation", ["811/820", "98,9"], "le score ajusté (présentation)")
    v.exige("manuscrit", ["811/820 = 98.9"], "le score ajusté (manuscrit)")

    # ---- la gouvernance vécue (ansz8lvdf) ---------------------------------------
    v.exige("specification", ["D223", "EST VÉCUE"],
            "la cérémonie vécue (spec)")
    v.exige("livre", ["VÉCUE le 19 novembre 2026"], "le runbook VÉCU (livre)")
    v.interdit("livre", "demeure PRIVÉ", "le dépôt privé périmé (livre)")
    v.interdit("specification", "demeure PRIVÉ tant que la",
               "le dépôt privé périmé (spec)")
    v.interdit("manuscrit", "D183 escrow ceremony, prepared and waiting",
               "la ligne stale D183 (manuscrit — l'attente des kits matériels "
               "fence.i/troisième machine demeure légitime, jamais confondue)")
    v.exige("specification", ["D75-D223"],
            "le titre de l'annexe B à la plage réelle")
    v.exige("livre", ["quatorze arbres"], "quatorze arbres (livre)")

    # ---- la plage de décisions et les comptes (gq117wphb 3) --------------------
    v.exige("manuscrit", ["D1-D223"], "la plage de décisions D1-D223")

    # ---- la batterie intacte ---------------------------------------------------
    v.exige("preuves", ["811/832"], "la batterie brute 811/832 (preuves)")

    print()
    if v.rouges:
        print(f"LE LINTER v196 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              f"le build est REFUSÉ")
        return 1
    print(f"LE LINTER v196 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    raise SystemExit(controle())
