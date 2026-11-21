#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""annoter_historiques.py — LES QUATRE ANNOTATIONS des contextes historiques
datés (0uug27teo : « les contextes historiques datés DEMEURENT intacts et
annotés amendé D223 »). Les récits de terrain (31/10), la chronologie du
terrain et la FAQ explicative portent l'annotation d'époque."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
R = []


def remplace(chemin: pathlib.Path, ancien: str, nouveau: str, nom: str):
    t = chemin.read_text(encoding="utf-8")
    if ancien not in t or t.count(ancien) != 1:
        print(f"ANCRE MANQUANTE/AMBIGUE ({chemin.name}) : {nom}")
        sys.exit(2)
    chemin.write_text(t.replace(ancien, nouveau), encoding="utf-8")
    R.append(f"{chemin.name} : {nom}")


# (1) le Livre §7.4 — le récit de terrain du refus nommé (31/10, DATÉ)
remplace(
    REPO / "scripts/livre_v16/sec-4.tex",
    "divergente ». La remise D81 n'était pas encore remplacée. Le refus est NOMMÉ, rien",
    "divergente ». La remise D81 n'était pas encore remplacée (la garde d'époque, "
    "amendée D223). Le refus est NOMMÉ, rien",
    "le récit de terrain du refus nommé : l'annotation d'époque")

# (2) le Livre §9.3 — la chronologie du terrain (30/10 soir, DATÉE)
remplace(
    REPO / "scripts/livre_v16/sec-5.tex",
    "changée (D110), un premier \\code{migrer} refusé (phrase divergente — remise D81 à\n"
    "faire), le second VERT",
    "changée (D110), un premier \\code{migrer} refusé (phrase divergente — remise D81 à\n"
    "faire, la garde d'époque amendée D223), le second VERT",
    "la chronologie du terrain : l'annotation d'époque")

# (3) le Livre annexe C — la FAQ explicative (la mention d'époque annotée)
remplace(
    REPO / "scripts/livre_v16/sec-6.tex",
    "fail-closed qui travaille : la remise D81 n'était pas encore remplacée. Rien n'a été",
    "fail-closed qui travaille : la remise D81 d'époque n'était pas encore remplacée\n"
    "(amendée D223). Rien n'a été",
    "la FAQ de l'annexe C : la mention d'époque annotée")

# (4) la spec §12 — le récit de terrain du coffre réel (31/10, DATÉ)
remplace(
    REPO / "scripts/spec_v157/sec-cf.tex",
    "refusé nommément (« phrase de contrôle divergente » — la remise D81 n'était pas encore\n"
    "remplacée : le fail-closed a travaillé",
    "refusé nommément (« phrase de contrôle divergente » — la remise D81 n'était pas encore\n"
    "remplacée, la garde d'époque amendée D223 : le fail-closed a travaillé",
    "le récit de terrain de la spec : l'annotation d'époque")

print(f"LES ANNOTATIONS : {len(R)} remplacements ancrés vécus —")
for r in R:
    print("  -", r)
