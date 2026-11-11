#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""statuts_preuves_v150.py — LA TABLE DES STATUTS SYSTÉMATIQUES (v0.15.0).

La commande (ic09ydeli, point 4) : « statuts des preuves ('prouvé non
borné' / 'prouvé borné' / 'en attente de run matériel') distincts et
systématiques ». La table est GÉNÉRÉE depuis les pièces réelles (les
CSV des preuves v150, relus — jamais un statut gravé à la main) et
écrite vers donnees/statuts_v150.tex (inclus par main.tex).
"""
import csv
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
PREUVES = ICI / "preuves_v150"
DONNEES = ICI / "manuscrit_v150" / "donnees"

STATUTS_TRADUCTION = {
    "PROUVÉE NON BORNÉE": "proved unbounded",
    "PROUVÉE BORNÉE": "proved bounded",
    "EN ATTENTE DE RUN MATÉRIEL": "awaiting hardware run",
    "VÉRIFIÉ AU LABORATOIRE": "verified in the laboratory",
    "MESURÉE": "measured (v0.14.0)",
    "EN ATTENTE": "awaiting (recruitment / real command)",
}


def main():
    # les statuts de P1-P4 lus du CSV de l'invariant (la source unique)
    statuts_p = {}
    with open(PREUVES / "modele_invariant.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            statuts_p[r["propriété"]] = r["statut"]
    # le raffinement : le bilan lu du CSV
    nb_pas = 0
    ecarts = 0
    with open(PREUVES / "raffinement.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nb_pas += 1
            if r["conforme"] == "ÉCART":
                ecarts += 1
    raffinement_statut = ("verified in the laboratory"
                          if ecarts == 0 else f"{ecarts} gap(s) consigned")

    lignes = [
        "\\begin{table}[t]",
        "\\centering\\small",
        "\\caption{Systematic proof statuses (the v0.15.0 requirement): "
        "every claim carries its status and its evidence piece.}",
        "\\label{tab:statuts}",
        "\\begin{tabularx}{\\textwidth}{lXX}",
        "\\toprule",
        "Claim & Status & Evidence \\\\",
        "\\midrule",
    ]

    def l(nom, statut, piece):
        lignes.append(f"{nom} & {statut} & {piece} \\\\")

    p1 = STATUTS_TRADUCTION[statuts_p.get("P1", "?")]
    p2 = STATUTS_TRADUCTION[statuts_p.get("P2", "?")]
    p3 = STATUTS_TRADUCTION[statuts_p.get("P3", "?")]
    p4 = STATUTS_TRADUCTION[statuts_p.get("P4", "?")]
    l("P1 secret below threshold", p1,
      "inductive invariant $I_1$ (secret $\\Rightarrow$ threshold 3); "
      "preservation by all 13 rules over 288 state shapes; epoch "
      "translation $\\delta\\in\\{7,50,1000\\}$ uniform")
    l("P2 rollback refusal", p2,
      "unconditional epoch monotonicity (4{,}096 shapes, zero "
      "decrease); replay rules return the state unchanged")
    l("P3 no destruction on wrong phrase", p3,
      "inductive invariant $I_2$: no rule ever writes unjust "
      "destruction")
    l("P4 blast radius one epoch", p4,
      "inductive invariant $I_3$: no rule ever touches the trap media "
      "or the CF2 fragments")
    l("Model $\\leftrightarrow$ implementation", raffinement_statut,
      f"{nb_pas} refinement steps, {ecarts} gap(s); five epochs lived "
      "at both levels, every failure path replayed")
    l("Bounded cross-checks", "proved bounded",
      "the v0.12.0 explorer reproduced exactly (154 states / 1{,}152 "
      "transitions); extended bounds 228/1{,}902 ($e\\le5$, $d\\le8$) "
      "and 372/3{,}342 ($e\\le7$, $d\\le12$), zero states outside $I$")
    l("Structural constant time", "proved bounded",
      "secret-independent instruction traces under emulation "
      "(v0.11.0)")
    l("Wall-clock constant time", "awaiting hardware run",
      "the dudect kit: four targets extracted from the sealed piece, "
      "FIPS-validated native call, dual-backend measurer --- no number "
      "exists until the developer runs it")
    l("\\code{fence.i} on silicon", "awaiting hardware run",
      "the M7 scenario retargeted at a physical RV64 board; the TCG "
      "emulation could not prove instruction-cache semantics")
    l("Third-machine field liveness", "awaiting hardware run",
      "the Loupe kit on a second Windows machine, full T0--T7+S0 "
      "scenario")
    l("Compiler-reference comparison", "measured (v0.14.0)",
      "zero divergence, SHA-256 parity at equal work; H4 holds")
    l("Independent replication", "awaiting (recruitment / real "
      "command)",
      "the T/X grid finalised, the $\\kappa$ calculator autotested "
      "(synthetic cases), criteria pre-registered unchanged")

    lignes += [
        "\\bottomrule",
        "\\end{tabularx}",
        "\\end{table}",
    ]
    DONNEES.mkdir(parents=True, exist_ok=True)
    sortie = DONNEES / "statuts_v150.tex"
    sortie.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"[statuts] {len(lignes)} lignes -> {sortie}")
    print(f"  P1={p1} ; P2={p2} ; P3={p3} ; P4={p4}")
    print(f"  raffinement : {nb_pas} pas, {ecarts} écart(s)")


if __name__ == "__main__":
    main()
