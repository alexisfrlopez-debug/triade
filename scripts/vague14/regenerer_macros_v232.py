#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v232.py — LES COMPTES COURANTS des journaux vivants
portés aux macros à la génération v0.23.2 (la session de génération promise
à l'Entrée 384 — les comptes RECALCULÉS des fichiers mêmes et le DOI au
jour de la rédaction [la v0.23.1, le record 24442241], par remplacements
ancrés — REFUS si une ancre manque)."""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = REPO / "edition-v0230" / "donnees" / "macros_v230.tex"

DOI_COURANT = "10.5281/zenodo.24442241"  # la v0.23.1 au jour de la rédaction


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
    n_journal = len((REPO / "docs" / "JOURNAL_TRAVAIL.md")
                   .read_text(encoding="utf-8").splitlines())
    n_worklog = len((REPO / "worklog.md")
                    .read_text(encoding="utf-8").splitlines())
    n_decisions = len((REPO / "docs" / "DECISIONS.md")
                      .read_text(encoding="utf-8").splitlines())
    ds = re.findall(r"^## D(\d+)",
                    (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8"),
                    re.M)
    plage = f"D1--D{max(int(d) for d in ds)}"
    print(f"les comptes : journal {n_journal:,} · worklog {n_worklog:,} · "
          f"décisions {n_decisions:,} · plage {plage}")

    t = OUT.read_text(encoding="utf-8")

    t = remplace(
        t,
        "\\newcommand{\\nbLignesWorklog}{14,027}",
        f"\\newcommand{{\\nbLignesWorklog}}{{{n_worklog:,}}}",
        f"nbLignesWorklog 14,027 → {n_worklog:,}")
    t = remplace(
        t,
        "\\newcommand{\\doiVersionCourante}{10.5281/zenodo.24420007}",
        f"\\newcommand{{\\doiVersionCourante}}{{{DOI_COURANT}}}",
        f"doiVersionCourante 24420007 → 24442241 (la v0.23.1 au jour de "
        "la rédaction)")
    # l'en-tête du fichier GÉNÉRÉ porté à la génération courante
    t = remplace(
        t,
        "% Fichier GÉNÉRÉ (v0.23.0) — les comptes EXACTS des journaux",
        "% Fichier GÉNÉRÉ (v0.23.2) — les comptes EXACTS des journaux",
        "l'en-tête du fichier généré (v0.23.2)")
    t = remplace(
        t,
        "% (les comptes et la plage recalculés par\n"
        "% scripts/vague13/regenerer_macros_v230.py à la génération v0.23.0 : les\n"
        "% journaux vivants APRÈS la vague 13, la plage à la dernière décision,\n"
        "% le DOI au jour de la rédaction ; les canons des vagues 9 à 13)",
        "% (le worklog et le DOI recalculés par\n"
        "% scripts/vague14/regenerer_macros_v232.py à la génération "
        "corrective v0.23.2 :\n"
        "% les journaux vivants APRÈS la vague 14, la plage à la dernière "
        "décision,\n"
        "% le DOI au jour de la rédaction ; les canons des vagues 9 à 14)",
        "la note de régénération (v232)")

    OUT.write_text(t, encoding="utf-8")
    print(f"[v232] les macros portées aux comptes courants ({OUT.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
