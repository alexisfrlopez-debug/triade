#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v190.py — régénère les macros des comptes (v0.19.0)
depuis les sources vivantes du dépôt (docs/JOURNAL_TRAVAIL.md, worklog.md,
docs/DECISIONS.md). Aucune valeur tapée à la main."""
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[2]
ED = REPO / "edition-v0190"

journal = (REPO / "docs/JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
worklog = (REPO / "worklog.md").read_text(encoding="utf-8")
decisions = (REPO / "docs/DECISIONS.md").read_text(encoding="utf-8")

n_j = journal.count("\n") + (0 if journal.endswith("\n") else 1)
n_w = worklog.count("\n") + (0 if worklog.endswith("\n") else 1)
n_d = decisions.count("\n") + (0 if decisions.endswith("\n") else 1)
derniere = max(int(m) for m in re.findall(r"^## D(\d+)", decisions, re.M))

def fr(n: int) -> str:
    s = str(n)
    if len(s) > 3:
        return s[:-3] + "{,}" + s[-3:]
    return s

macros = f"""% Fichier GÉNÉRÉ (v0.19.0) — les comptes EXACTS des journaux récupérés.
\\newcommand{{\\nbLignesJournal}}{{{fr(n_j)}}}
\\newcommand{{\\nbLignesWorklog}}{{{fr(n_w)}}}
\\newcommand{{\\nbLignesDecisions}}{{{fr(n_d)}}}
\\newcommand{{\\plageDecisions}}{{D1--D{derniere}}}
"""
(ED / "donnees/macros_v190.tex").write_text(macros, encoding="utf-8")
print(f"journal={n_j}  worklog={n_w}  decisions={n_d}  plage=D1--D{derniere}")
print(macros)
