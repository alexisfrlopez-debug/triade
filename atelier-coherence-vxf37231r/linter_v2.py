#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v2.py — LE LINTER ÉTENDU (vxf37231r, la vague 15) : LES CINQ
CLASSES nommées à l'instruction — les phrases sémantiques retirées, les
plages décisionnelles annoncées vs les entrées listées, les séquences de
faisabilité, les claims DOI/version post-dépôt, les gallicismes EN.
LE CONTRÔLE NÉGATIF : une violation plantée PAR CLASSE DOIT être
attrapée (le drapeau --negatif).
Usage : linter_v2.py <piece.txt>... [--negatif]"""
from __future__ import annotations

import re
import sys

# (A) LES PHRASES SÉMANTIQUES RETIRÉES (le compilateur « disparaît » —
# spec §1 vs D182 : la phrase interdite, la formulation exacte exigée)
PHRASES_INTERDITES = [
    (re.compile(r"le compilateur\s+(disparaît|disparait)", re.I),
     "la phrase sémantique « le compilateur disparaît » (D182) — la "
     "formulation exacte : le compilateur N'EST JAMAIS LIVRÉ, la "
     "notation scellée l'est"),
]
# (B) LES PLAGES DÉCISIONNELLES : l'annoncée vs la liste (la table à
# D137 vs le journal — la forme « D1–D251 » confrontée au compte)
PLAGE = re.compile(r"D(\d+)\s*[–-]\s*D(\d+)")
# (C) LES SÉQUENCES DE FAISABILITÉ (Table 19 : ajouter 7/18 — la forme
# n/18 aux côtés de la campagne courante v5 : TOUTE valeur périmée
# sans marqueur d'époque daté est ROUGE)
FAISABILITE = re.compile(r"(?<!\d)(\d{1,2})/18(?!\d)")
# (D) LES CLAIMS DOI/VERSION POST-DÉPÔT (le manuscrit « v0.23.1 at this
# writing » vs le dépôt v0.23.2 : la version COURANTE vérifiée)
CLAIM_VERSION = re.compile(r"v0\.23\.[01][^0-9]")
VERSION_COURANTE = "v0.23.2"
# (E) LES GALLICISMES EN (le texte anglais)
GALLICISMES = [(re.compile(r"\btranchée\b"), "« tranchée » — l'anglais : "
               "« settled by » / « decided by »"),
               (re.compile(r"five-thirds escrow"), "« five-thirds "
                "escrow » — le gallicisme : la formulation anglaise "
                "exigée")]


def linter(texte: str) -> list:
    rouges = []
    for motif, message in PHRASES_INTERDITES:
        if motif.search(texte):
            rouges.append(("A", message))
    for m in PLAGE.finditer(texte):
        lo, hi = int(m.group(1)), int(m.group(2))
        if hi - lo + 1 > 260 or hi > 251:
            rouges.append(("B", f"la plage D{lo}–D{hi} annoncée "
                           "s'étend au-delà du journal listé (D137) — "
                           "la confrontation à la table exigée"))
    for m in FAISABILITE.finditer(texte):
        v = int(m.group(1))
        if v != 7 and "2026" not in texte[max(0, m.start()-60):m.start()]:
            rouges.append(("C", f"la faisabilité {v}/18 sans marqueur "
                           "d'époque daté — la Table 19 porte 7/18 "
                           "(vague 14) ; la campagne courante v5 nommée "
                           "à part"))
    for m in CLAIM_VERSION.finditer(texte):
        if "at this writing" in texte[m.start():m.start() + 60]:
            rouges.append(("D", "le claim de version post-dépôt — « at "
                           "this writing » exige la version courante "
                           + VERSION_COURANTE))
    for motif, message in GALLICISMES:
        if motif.search(texte):
            rouges.append(("E", message))
    return rouges


def main() -> int:
    negatif = "--negatif" in sys.argv
    fichiers = [a for a in sys.argv[1:] if not a.startswith("--")]
    total_rouges = []
    for f in fichiers:
        texte = open(f, encoding="utf-8").read()
        rouges = linter(texte)
        total_rouges.extend((f, c, m) for c, m in rouges)
        print(f"{f} : {'VERT' if not rouges else str(len(rouges)) + ' ROUGE'}"
              + ("".join("\n  [" + c + "] " + m for c, m in rouges)
                 if rouges else ""))
    if negatif:
        # LE CONTRÔLE NÉGATIF : UNE VIOLATION PLANTÉE PAR CLASSE DOIT
        # ÊTRE ATTRAPÉE
        plante = {
            "A": "le compilateur disparaît au moment de la livraison",
            "B": "les décisions D1–D999 au journal",
            "C": "la faisabilité 15/18 (sans marqueur d'époque)",
            "D": "v0.23.1 at this writing",
            "E": "the question was tranchée by the median",
        }
        attendus = set(plante)
        attrapes = {c for c, _ in linter("\n".join(plante.values()))}
        print(f"LE CONTRÔLE NÉGATIF (une violation plantée par classe) : "
              f"{len(attrapes)}/{len(attendus)} ATTRAPÉES "
              + ("— le linter est PORTANT" if attrapes == attendus
                 else "— ROUGE : " + str(attendus - attrapes)))
        if attrapes != attendus:
            return 2
    return 1 if total_rouges else 0


if __name__ == "__main__":
    sys.exit(main())
