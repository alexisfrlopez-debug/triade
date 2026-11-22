#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aligner_abstracts_v230.py — L'ALIGNEMENT DES ABSTRACTS EN ET FR SUR LES
MÊMES MACROS (la tâche (d) de ylrzmlbn8, le complément de reprise) : la
passe morte avait réécrit le résumé FR aux canons, l'abstract EN
demeurait à l'état v0.22.0 (la médiane de localiser titrée 1 053, la
faisabilité « 0 to 3 greens » de la vague 11) — le présent aligne l'EN
aux mêmes macros ; le corps porte les états courants (le canon du cache
RECOMPOSÉ 285,725 → 0,418 ms = ×683,6 — la ligne 283,7 → 0,4/×680,6 de
la v0.22.0 laissait le lecteur à ×709 ; la faisabilité de l'ajout aux
trois passes 3 → 5 → 6 avec le gap DÉPLACÉ nommé par classe de refus) ;
le qualificatif périmé du résumé FR (« au format pointeur seul adopté »
— les formats adoptés sont trois) corrigé. Les macros d'opérandes
anglaises ajoutées au fichiers généré (les MÊMES canons, la mise en
forme EN). Remplacements ancrés — REFUS si une ancre manque."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
ED = REPO / "edition-v0230"
MAIN = ED / "main.tex"
MACROS = ED / "donnees" / "macros_v230.tex"


def remplace(t: str, ancien: str, nouveau: str, nom: str) -> str:
    if ancien not in t:
        print(f"ANCRE MANQUANTE : {nom}")
        sys.exit(2)
    if t.count(ancien) != 1:
        print(f"ANCRE AMBIGUE {t.count(ancien)}x : {nom}")
        sys.exit(2)
    print(f"  — {nom}")
    return t.replace(ancien, nouveau)


def main() -> int:
    # ---- (0) LES MACROS D'OPÉRANDES ANGLAISES (les MÊMES canons que les
    #      \gabarit*Op françaises — la mise en forme EN : le point
    #      décimal, la virgule millier)
    m = MACROS.read_text(encoding="utf-8")
    m = remplace(
        m,
        "\\newcommand{\\batteriePartition}{16 + 3 + 4 + 13 + 3 + 8 + 512}",
        "\\newcommand{\\batteriePartition}{16 + 3 + 4 + 13 + 3 + 8 + 512}\n"
        "% les opérandes non arrondis, la mise en forme ANGLAISE (les mêmes\n"
        "% canons que les \\gabarit*Op — l'abstract EN aligné, la tâche (d))\n"
        "\\newcommand{\\gabaritLocaliserOpEN}{\\% (operands 1{,}053 $\\to$ 627)}\n"
        "\\newcommand{\\gabaritEditerOpEN}{\\% (operands 1{,}106 $\\to$ 674)}\n"
        "\\newcommand{\\gabaritAjouterOpEN}{\\% (operands 3{,}073.5 $\\to$ 2{,}199.5)}",
        "les macros d'opérandes anglaises")
    MACROS.write_text(m, encoding="utf-8")

    t = MAIN.read_text(encoding="utf-8")

    # ---- (1) L'ABSTRACT EN ALIGNÉ AUX MÊMES MACROS — la médiane titrée
    #      \gabaritLocaliserApres (627, le localisateur hiérarchique
    #      ADOPTÉ), les opérandes aux macros EN, la faisabilité aux trois
    #      passes, LA TABLE CANONIQUE nommée (le miroir exact du résumé FR)
    t = remplace(
        t,
        "per validated change --- under the adopted formats a median of 1{,}053\n"
        "native request tokens to locate a block ($n{=}18$; the hierarchical\n"
        "locator at 627), 674 to edit one (the versioned template carrying the\n"
        "format grammar once, the prescription prose down 57\\,\\%) and 2{,}200\n"
        "to add one (the skeleton format, its feasibility 0 to 3 greens --- the\n"
        "gap named), against a naive whole-disassembly baseline of 300{,}304,\n"
        "with the historical perimeters (M1, v0.14.0 content-only, v0.17.0\n"
        "round-trip, the v0.21.0 window perimeter) explicitly labelled;",
        "per validated change --- under the adopted formats a median of\n"
        "\\gabaritLocaliserApres{} native request tokens to locate a block (the\n"
        "hierarchical locator adopted, $-40.5\\,\\%$ \\gabaritLocaliserOpEN{};\n"
        "the epoch measurements 1{,}714 then 1{,}103 at pointer-alone remain\n"
        "labelled history), \\gabaritEditerApres{} to edit one (the versioned\n"
        "template TPL-EDIT-v1 adopted, $-39.1\\,\\%$ \\gabaritEditerOpEN{}, the\n"
        "prescription prose down 57\\,\\%) and \\gabaritAjouterApres{} to add\n"
        "one (the skeleton, $-28.4\\,\\%$ \\gabaritAjouterOpEN{}, its\n"
        "feasibility 3/18 at waves 11-12 then 6/18 at the thirteenth --- the\n"
        "gap named by refusal class), every perimeter labelled --- every value\n"
        "carrying its decision ID, scope and status at the canonical\n"
        "adopted-budgets table, against a naive whole-disassembly baseline of\n"
        "300{,}304, with the historical perimeters (M1, v0.14.0 content-only,\n"
        "v0.17.0 round-trip, the v0.21.0 window perimeter) explicitly\n"
        "labelled;",
        "l'abstract EN aligné aux mêmes macros (la tâche (d))")

    # ---- (2) LE CORPS : LE CANON DU CACHE RECOMPOSÉ (la correction (c)
    #      portée au corps — les opérandes non arrondis publiés, le lecteur
    #      recompose : 285,725 → 0,418 ms = ×683,6)
    t = remplace(
        t,
        "the session-opening re-verification 283.7 to 0.4\\,ms, a 680.6$\\times$\n"
        "gain, every key divergence forcing the complete re-verification\n"
        "back)",
        "the session-opening re-verification 285.725 to 0.418\\,ms, a\n"
        "683.6$\\times$ gain (the recomposed canon, the unrounded operands\n"
        "published --- the reader recomputes), every key divergence forcing\n"
        "the complete re-verification back)",
        "le canon du cache recomposé au corps (285,725 → 0,418 ms = ×683,6)")

    # ---- (3) LE CORPS : LA FAISABILITÉ DE L'AJOUT À L'ÉTAT COURANT (les
    #      trois passes 3 → 5 → 6, la boucle de réparation convertissant
    #      AUCUN refus, le gap DÉPLACÉ nommé par classe)
    t = remplace(
        t,
        "perimeter, its feasibility 0 to 3 greens --- the fifteen honest\n"
        "out-of-format refusals remain, the gap named: the model must still\n"
        "learn the label and constant domain); the edit floor ratio is",
        "perimeter, its feasibility 3 to 6 greens across the three passes\n"
        "(the skeleton, then the domain dictionary, then the grammar with its\n"
        "repair loop --- the loop converts none of the honest refusals; the\n"
        "third pass measures 3{,}844 tokens per validated change at 6/18,\n"
        "18/18 for the edit operation at 712), the residual gap named by\n"
        "refusal class at the third pass (nine expansion-divergent, two\n"
        "out-of-format, one unknown-id): the gap has moved from domain\n"
        "knowledge to the stability of the model's machine writing against\n"
        "the expansion judge); the edit floor ratio is",
        "la faisabilité de l'ajout aux trois passes (le gap déplacé nommé)")

    # ---- (4) LE RÉSUMÉ FR : LE QUALIFICATIF PÉRIMÉ (« au format pointeur
    #      seul adopté » — les formats adoptés sont TROIS : le
    #      localisateur hiérarchique, le gabarit versionné, le squelette)
    t = remplace(
        t,
        "changement validé — au format pointeur seul adopté, une médiane de",
        "changement validé — aux formats adoptés, une médiane de",
        "le qualificatif périmé du résumé FR (aux formats adoptés)")

    MAIN.write_text(t, encoding="utf-8")
    print("[alignement] les abstracts EN/FR aux mêmes macros, le corps à "
          "l'état courant")
    return 0


if __name__ == "__main__":
    sys.exit(main())
