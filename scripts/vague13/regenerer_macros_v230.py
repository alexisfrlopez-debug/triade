#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v230.py — LES COMPTES COURANTS des journaux vivants
portés aux macros v0.23.0 (la source unique de vérité partagée par les
cinq pièces — le fichier macros_v230.tex porte les canons des vagues 9
à 13 ; le présent script recalcule les COMPTES des fichiers mêmes et le
DOI au jour de la rédaction, par remplacements ancrés — REFUS si une
ancre manque)."""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = REPO / "edition-v0230" / "donnees" / "macros_v230.tex"

DOI_COURANT = "10.5281/zenodo.24420007"  # la v0.22.1 au jour de la rédaction


def compte_lignes(p):
    return len(pathlib.Path(p).read_text(encoding="utf-8").splitlines())


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
    n_journal = compte_lignes(REPO / "docs" / "JOURNAL_TRAVAIL.md")
    n_worklog = compte_lignes(REPO / "worklog.md")
    n_decisions = compte_lignes(REPO / "docs" / "DECISIONS.md")
    ds = re.findall(r"^## D(\d+)",
                    (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8"),
                    re.M)
    plage = f"D1--D{max(int(d) for d in ds)}"
    print(f"les comptes : journal {n_journal} · worklog {n_worklog} · "
          f"décisions {n_decisions} · plage {plage}")

    t = OUT.read_text(encoding="utf-8")

    ancien_journal = re.search(r"\\newcommand\{\\nbLignesJournal\}\{([\d,]+)\}", t)
    ancien_worklog = re.search(r"\\newcommand\{\\nbLignesWorklog\}\{([\d,]+)\}", t)
    ancien_dec = re.search(r"\\newcommand\{\\nbLignesDecisions\}\{([\d,]+)\}", t)
    ancien_plage = re.search(r"\\newcommand\{\\plageDecisions\}\{(D1--D\d+)\}", t)
    ancien_doi = re.search(r"\\newcommand\{\\doiVersionCourante\}\{([\w./]+)\}", t)

    t = remplace(t, ancien_journal.group(0),
                 f"\\newcommand{{\\nbLignesJournal}}{{{n_journal:,}}}",
                 f"nbLignesJournal {ancien_journal.group(1)} → {n_journal:,}")
    t = remplace(t, ancien_worklog.group(0),
                 f"\\newcommand{{\\nbLignesWorklog}}{{{n_worklog:,}}}",
                 f"nbLignesWorklog {ancien_worklog.group(1)} → {n_worklog:,}")
    t = remplace(t, ancien_dec.group(0),
                 f"\\newcommand{{\\nbLignesDecisions}}{{{n_decisions:,}}}",
                 f"nbLignesDecisions {ancien_dec.group(1)} → {n_decisions:,}")
    t = remplace(t, ancien_plage.group(0),
                 f"\\newcommand{{\\plageDecisions}}{{{plage}}}",
                 f"plageDecisions {ancien_plage.group(1)} → {plage}")
    t = remplace(t, ancien_doi.group(0),
                 f"\\newcommand{{\\doiVersionCourante}}{{{DOI_COURANT}}}",
                 f"doiVersionCourante {ancien_doi.group(1)} → {DOI_COURANT} "
                 "(la v0.22.1 au jour de la rédaction)")

    # l'en-tête du fichier GÉNÉRÉ porté à la génération courante
    t = remplace(
        t,
        "% Fichier GÉNÉRÉ (v0.22.0) — les comptes EXACTS des journaux",
        "% Fichier GÉNÉRÉ (v0.23.0) — les comptes EXACTS des journaux",
        "l'en-tête du fichier généré (v0.23.0)")
    t = remplace(
        t,
        "% (régénéré par scripts/vague11/regenerer_macros_v220.py : les comptes\n"
        "% portés aux journaux APRÈS la vague 11 + les canons de la vague 11)",
        "% (les comptes et la plage recalculés par\n"
        "% scripts/vague13/regenerer_macros_v230.py à la génération v0.23.0 : les\n"
        "% journaux vivants APRÈS la vague 13, la plage à la dernière décision,\n"
        "% le DOI au jour de la rédaction ; les canons des vagues 9 à 13)",
        "la note de régénération (v230)")

    OUT.write_text(t, encoding="utf-8")
    print(f"[v230] les macros portées aux comptes courants ({OUT.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
