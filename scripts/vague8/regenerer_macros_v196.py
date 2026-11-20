#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v196.py — LES MACROS DE L'ÉDITION v0.19.6 : la source
unique de vérité des comptes (journal, worklog, décisions), la plage de
décisions, le DOI, les canons M4 et les comptes d'arbres — GÉNÉRÉS des
journaux vivants, jamais tapés (l'instruction gq117wphb point 3 et 7)."""
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[2]
ED = REPO / "edition-v0196"

journal = (REPO / "docs/JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
worklog = (REPO / "worklog.md").read_text(encoding="utf-8")
decisions = (REPO / "docs/DECISIONS.md").read_text(encoding="utf-8")

n_j = journal.count("\n") + (0 if journal.endswith("\n") else 1)
n_w = worklog.count("\n") + (0 if worklog.endswith("\n") else 1)
n_d = decisions.count("\n") + (0 if decisions.endswith("\n") else 1)
derniere = max(int(m) for m in re.findall(r"^## D(\d+)", decisions, re.M))


def fr(n: int) -> str:
    s = str(n)
    return s[:-3] + "{,}" + s[-3:] if len(s) > 3 else s


macros = f"""% Fichier GÉNÉRÉ (v0.19.6) — les comptes EXACTS des journaux
% récupérés, la source unique de vérité partagée par les cinq pièces
% (l'instruction gq117wphb : macros générées, jamais tapées).
\\newcommand{{\\nbLignesJournal}}{{{fr(n_j)}}}
\\newcommand{{\\nbLignesWorklog}}{{{fr(n_w)}}}
\\newcommand{{\\nbLignesDecisions}}{{{fr(n_d)}}}
\\newcommand{{\\plageDecisions}}{{D1--D{derniere}}}
% LES DOI (réconciliés à l'instruction gq117wphb point 2 : le CONCEPT
% résout sur la dernière version — 24367343 ; les versions 24367344
% (v0.19.0) et 24379173 (v0.19.4) sont les dépôts datés, le courant
% étant 24382460 (v0.19.5) à la date de scellé de la présente)
\\newcommand{{\\doiConcept}}{{10.5281/zenodo.24367343}}
\\newcommand{{\\doiVersionCourante}}{{10.5281/zenodo.24382460}}
% LES CANONS M4 (mesurés, jamais recalculés à la main ici : les pièces
% preuves-pe6iv71fj — médianes lues des JSON)
\\newcommand{{\\mquatreAvantMediane}}{{39.1}}
\\newcommand{{\\mquatreChaudMediane}}{{6.6}}
\\newcommand{{\\mquatreBrasC}}{{1.9}}
\\newcommand{{\\mquatreRatioAvant}}{{20.4$\\times$}}
\\newcommand{{\\mquatreRatioChaud}}{{3.5$\\times$}}
% LE COMPTE D'ARBRES SIGNÉS (le sceau I — quatorze, D177)
\\newcommand{{\\nbArbresSignes}}{{14}}
"""
(ED / "donnees/macros_v196.tex").write_text(macros, encoding="utf-8")
print(f"journal={n_j} worklog={n_w} decisions={n_d} plage=D1--D{derniere}")
