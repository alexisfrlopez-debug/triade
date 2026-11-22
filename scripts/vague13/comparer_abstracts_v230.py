#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""comparer_abstracts_v230.py — LES ABSTRACTS EN ET FR COMPARÉS CHAMP À
CHAMP PAR SCRIPT (la vérification de la tâche (d) de ylrzmlbn8 : les
DEUX abstracts générés des mêmes macros, ZÉRO écart de valeur). Chaque
champ canonique extrait de sa pièce par son motif propre (la langue
tranche la lecture : la virgule millier au manuscrit anglais, l'espace
au français) ; un champ présent à une seule pièce est NOMMÉ
(composition — jamais une divergence de valeur) ; un écart de valeur
est un REFUS (exit 2)."""
from __future__ import annotations

import re
import subprocess
import sys

PDF = "/home/z/my-project/depot/edition-v0230/main.pdf"


def texte():
    t = subprocess.run(["pdftotext", PDF, "-"], capture_output=True,
                       check=True).stdout.decode("utf-8", "replace")
    t = (t.replace("\u2013", "-").replace("\u2212", "-")
          .replace("\u2192", "->").replace("\u2019", "'"))
    return re.sub(r"\s+", " ", t)


def normalise(v: str):
    """la valeur au canon : la virgule millier EN et l'espace millier FR
    retirés, la virgule décimale FR en point ; « 6/18 » tel quel."""
    v = v.strip().replace(" ", "").replace("\u202f", "").replace("\u00a0", "")
    if re.fullmatch(r"\d+/\d+", v):
        return v
    if re.fullmatch(r"\d{1,3}(,\d{3})+\.\d+", v):   # 3,073.5 (millier EN + décimale)
        return float(v.replace(",", ""))
    if re.fullmatch(r"\d{1,3}(,\d{3})+", v):        # 13,650 (millier EN)
        return float(v.replace(",", ""))
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", v):       # 13.650 (millier point)
        return float(v.replace(".", ""))
    v = v.replace(",", ".")                          # 28,4 → 28.4 (décimale FR)
    return float(v)


# (nom, motif EN, motif FR) — chaque motif capture LA valeur canonique
CHAMPS = [
    ("le journal d'ingénierie (lignes)",
     r"an? ([\d,]+)-line (?:append-only )?engineering journal",
     r"journal d'ing[ée]nierie append-only de ([\d,\s]+) lignes"),
    ("le journal de tâches (lignes)",
     r"a ([\d,]+)-line (?:companion )?task log",
     r"journal de t[âa]ches compagnon de ([\d,\s]+) lignes"),
    ("le journal de décisions (lignes)",
     r"a ([\d,]+)-line (?:append-only )?decision log",
     r"journal de d[ée]cisions append-only de ([\d,\s]+) lignes"),
    ("la plage décisionnelle (dernière décision)",
     r"decision log, D1-D(\d+)\)",
     r"lignes \(D1-D(\d+)\)"),
    ("la médiane LOCALISER (adoptée)",
     r"median of ([\d,]+) native request tokens to locate",
     r"m[ée]diane de ([\d,\s]+) natifs pour localiser"),
    ("la médiane ÉDITER (adoptée)",
     r"([\d,]+) to edit",
     r"\), ([\d\s]+) pour [ée]diter"),
    ("la médiane AJOUTER (adoptée)",
     r"([\d,]+) to add\s*one",
     r"\), ([\d\s]+) pour ajouter"),
    ("le ratio LOCALISER (%)",
     r"adopted, -([\d.]+)\s?% \(operands",
     r"adopt[ée], -([\d,]+)\s?% \(op[ée]randes"),
    ("le ratio ÉDITER (%)",
     r"TPL-EDIT-v1 adopted, -([\d.]+)\s?%",
     r"TPL-EDIT-v1 adopt[ée], -([\d,]+)\s?%"),
    ("le ratio AJOUTER (%)",
     r"the skeleton, -([\d.]+)\s?% \(operands",
     r"le squelette, -([\d,]+)\s?% \(op[ée]randes"),
    ("les opérandes LOCALISER (avant)",
     r"operands ([\d,]+) -> 627\)",
     r"op[ée]randes ([\d,\s]+) -> 627\)"),
    ("les opérandes ÉDITER (avant)",
     r"operands ([\d,]+) -> 674\)",
     r"op[ée]randes ([\d,\s]+) -> 674\)"),
    ("les opérandes AJOUTER (avant, non arrondi)",
     r"operands ([\d,\.]+) -> 2,199\.5\)",
     r"op[ée]randes ([\d,\s]+) -> 2 199,5\)"),
    ("les opérandes AJOUTER (après, non arrondi)",
     r"operands 3,073\.5 -> ([\d,\.]+)\)",
     r"op[ée]randes 3 073,5 -> ([\d,\s]+)\)"),
    ("la faisabilité AJOUTER (vague 13)",
     r"feasibility 3/18 at waves 11-12 then ([\d]+/18) at the thirteenth",
     r"faisabilit[ée] 3/18 aux vagues 11-12 puis ([\d]+/18) [àa] la treizi[èe]me"),
    ("les mesures d'époque au pointeur seul (1 714 puis 1 103)",
     r"measurements ([\d,]+) then ([\d,]+) at pointer-alone",
     r"mesures d'[ée]poque ([\d\s]+) puis ([\d\s]+) au pointeur seul"),
    ("la campagne générative (traces)",
     r"([\d,]+) traces across three seeds",
     r"conformit[ée] de ([\d\s]+) traces aux trois graines"),
    ("la batterie de mutation (tués)",
     r"battery kills ([\d]+) of",
     r"batterie de fautes tue ([\d]+)"),
    ("la batterie de mutation (dénominateur brut)",
     r"kills \d+ of ([\d]+) mutants",
     r"tue \d+ sur ([\d]+)"),
    ("les constantes de l'oracle inter-familles",
     r"regenerates all ([\d]+) oracle constants",
     r"r[ée]g[ée]n[èe]re les ([\d]+) constantes"),
    ("la récitation pure de la seconde famille",
     r"fails at ([\d]+/64)",
     r"[ée]choue ([\d]+/64)"),
]


def main() -> int:
    t = texte()
    i_fr = t.find("Les agents de modèles de langage")
    if i_fr < 0:
        print("ROUGE — le résumé FR introuvable au manuscrit")
        return 2
    # l'abstract EN : du titre jusqu'au résumé FR (la page de garde et
    # l'abstract EN inclus)
    en, fr = t[:i_fr], t[i_fr:i_fr + 13000]

    verts, ecarts, compositions = 0, [], []
    for nom, men, mfr in CHAMPS:
        a = re.search(men, en)
        b = re.search(mfr, fr)
        if a and b:
            va = [normalise(x) for x in a.groups()]
            vb = [normalise(x) for x in b.groups()]
            if va == vb:
                verts += 1
                print(f"VERT  {nom} : {va}")
            else:
                ecarts.append((nom, va, vb))
                print(f"ROUGE {nom} : EN {va} ≠ FR {vb}")
        elif a or b:
            compositions.append(nom)
            print(f"NOTE  {nom} : présent à une seule pièce (composition)")
        else:
            ecarts.append((nom, None, None))
            print(f"ROUGE {nom} : ABSENT des deux abstracts")

    print()
    if ecarts:
        print(f"LES ABSTRACTS EN/FR : {verts} VERT, {len(ecarts)} ÉCART — "
              "REFUS")
        return 2
    print(f"LES ABSTRACTS EN/FR : {verts} champs comparés, ZÉRO écart de "
          f"valeur ; {len(compositions)} champ(s) de composition nommé(s) "
          "(présents à une seule pièce)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
