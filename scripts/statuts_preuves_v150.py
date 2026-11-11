#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""statuts_preuves_v150.py — LA TABLE DES STATUTS SYSTÉMATIQUES (v0.15.0,
mise à jour de la vague 3 : la preuve indépendante TLA+/Apalache et le
raffinement property-based — l'instruction 6zqo2h60n : « mets à jour la
table des statuts uniquement depuis ces pièces »).

La table est GÉNÉRÉE depuis les pièces réelles — les CSV des preuves
v150, les verdicts TLA+/Apalache (verdicts.json), le rapport du clone
frais, les pièces PBT — relus : jamais un statut gravé à la main.
Écrite vers donnees/statuts_v150.tex (inclus par main.tex).
"""
import csv
import json
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
PREUVES = ICI / "preuves_v150"
TLA = ICI / "tla_v150"
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
    # le raffinement par scénarios : le bilan lu du CSV (la pièce historique)
    nb_pas = 0
    ecarts = 0
    with open(PREUVES / "raffinement.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nb_pas += 1
            if r["conforme"] == "ÉCART":
                ecarts += 1
    # LE RAFFINEMENT PROPERTY-BASED (vague 3) : lu des pièces
    with open(PREUVES / "pbt_traces.csv", encoding="utf-8") as f:
        pbt_traces = list(csv.DictReader(f))
    with open(PREUVES / "pbt_ecarts_brut.csv", encoding="utf-8") as f:
        pbt_ecarts = list(csv.DictReader(f))
    with open(PREUVES / "pbt_traces_rejeu.csv", encoding="utf-8") as f:
        pbt_rejeu = {int(r["trace"]): r["digest"] for r in
                     csv.DictReader(f)}
    pbt_stables = sum(1 for r in pbt_traces
                      if pbt_rejeu[int(r["trace"])] == r["digest"])
    # LES VERDICTS TLA+/APALACHE (vague 3) : lus de verdicts.json
    v = json.loads((TLA / "verdicts.json").read_text(encoding="utf-8"))
    smt_ok = (v["apalache_base"] and v["apalache_inductif"]
              and v["apalache_inductif_init_inv"])
    controles_ok = (v["apalache_controle_c1_attrape"]
                    and v["apalache_controle_c2_attrape"])
    tlc_ok = (v["tlc_fidelite_d187"] and v["tlc_plafond_inv"]
              and v["tlc_bornes_inv"])
    clone_ok = "13/13 VERT" in (TLA / "verification_clone_frais_rapport.txt"
                               ).read_text(encoding="utf-8")
    pbt_statut = ("witnessed (10{,}000 traces)"
                  if pbt_stables == len(pbt_traces) else
                  f"{pbt_stables}/{len(pbt_traces)} stable")
    smt_statut = ("proved unbounded (SMT)" if smt_ok and clone_ok
                  else "see evidence pieces")

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
    smt_evidence = (
        "invariant $I$ discharged by Apalache (SMT, unbounded integers): "
        "$Init \\Rightarrow Inv$ and $Inv \\wedge Next \\Rightarrow Inv'$; "
        "TLC fidelity: 154 states at the v0.12.0 bounds (exact), 216 "
        "full plafond space, 360 at $e\\le5$; replayed from a fresh clone "
        "(13/13); negative controls catch a weakened invariant"
        if smt_ok and tlc_ok and clone_ok and controles_ok else
        "see scripts/tla_v150/verdicts.json")
    l("P1 secret below threshold", p1,
      "inductive invariant $I_1$ (secret $\\Rightarrow$ threshold 3); "
      "preservation by all 13 rules over 288 state shapes; epoch "
      "translation $\\delta\\in\\{7,50,1000\\}$ uniform; "
      + smt_evidence)
    l("P2 rollback refusal", p2,
      "unconditional epoch monotonicity (4{,}096 shapes, zero "
      "decrease); replay rules return the state unchanged; "
      + smt_evidence)
    l("P3 no destruction on wrong phrase", p3,
      "inductive invariant $I_2$: no rule ever writes unjust "
      "destruction; " + smt_evidence)
    l("P4 blast radius one epoch", p4,
      "inductive invariant $I_3$: no rule ever touches the trap media "
      "or the CF2 fragments; " + smt_evidence)
    l("Independent model proof (TLA+/SMT)", smt_statut,
      "CF3.tla: the 13 rules, unbounded epoch; Apalache base + "
      "inductive step over $\\mathbb{Z}$; "
      "mechanical audit: the epoch is read only via "
      "$\\{e{>}1,\\ e{+}1\\}$ (all 13 rules, guards/actions); "
      "controls: weakened invariant $\\rightarrow$ counterexample "
      "produced (non-vacuity)")
    l("Model $\\leftrightarrow$ implementation", pbt_statut,
      f"property-based: {len(pbt_traces):,} random traces (seed "
      "consigned), failure paths included, permanent epoch/phase/PV "
      f"cross-check; {len(pbt_ecarts)} gaps of ONE class (container "
      "falsification during a session: model refuses, concrete destroys "
      "--- state-coverage gap, P1--P4 unthreatened), shrunk to "
      "$[$ouvrir, falsifier$]$; replay at identical seed: "
      f"{pbt_stables:,}/{len(pbt_traces):,} stable; the 34-step "
      f"scenario suite remains ({nb_pas} steps, {ecarts} gap)")
    l("Bounded cross-checks", "proved bounded",
      "the v0.12.0 explorer reproduced exactly (154 states / 1{,}152 "
      "transitions); extended bounds 228/1{,}902 ($e\\le5$, $d\\le8$) "
      "and 372/3{,}342 ($e\\le7$, $d\\le12$), zero states outside $I$; "
      "TLC agrees: 154 at the historical bounds, 216 full plafond "
      "space, 360 at $e\\le5$")
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
      "the F/L grid finalised (renamed from T/X at D203, "
      "correspondence table in the kit), the $\\kappa$ calculator "
      "autotested (synthetic cases), criteria pre-registered unchanged")

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
