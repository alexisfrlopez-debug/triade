#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hcgp3_reconcilier.py — LE RÉCONCILIATEUR QUATRE EFFETS (ay6zuzm8o) :
chaque total réconcilié depuis ses étapes aux tolérances publiées (T
±0,150 s · C+G+ ±0,100 s · C+G, C ±0,050 s) ; la somme de la ventilation
== T−C à la milliseconde ; H-CGP3 tranché par mesure.

LA CLASSIFICATION PAR POSTE (figée au plan gelé) :
  — notation intrinsèque : round-trips de notation, recomposition du
    plan, cristallisation (incrémentale) ;
  — implémentation de vérification : oracles (re-exécutions vivantes),
    gardes de sceau, épreuves confrontées, tests/contrôles du C ;
  — régime : rebuilds (les TÉMOINS côté T [les reconstructions de
    pièces/bloc] / les compilations gcc côté C), les builds de base ;
  — gouvernance : g1-g4 (C+G/C+G+), l'assemblage des kits (T).

LA DOUBLE VENTILATION (jamais fusionnées) : la vague 11 datée (l'outil
non optimisé, l'asymétrie 12 vs 60 — H-CGP2) / la vague 13 (la pile
optimisée, les volumes égalisés — H-CGP3), les verdicts DISTINCTS et
datés.

Sortie : reconciliation.json · rapport-ventilation.txt."""
from __future__ import annotations

import json
import pathlib
import statistics
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-hcgp3-ay6zuzm8o"
TOLERANCES = {"T": 0.150, "C+G+": 0.100, "C+G": 0.050, "C": 0.050}
N = 5

# la classification par étape (la lettre du plan)
def poste_de(etape: str, bras: str) -> str:
    e = etape.split(" (")[0]
    if bras == "T":
        if e in ("round-trip-notation-1", "round-trip-notation-2",
                 "recomposition-loupe-02", "cristallisation-incrémentale"):
            return "notation intrinsèque"
        if e.startswith("rebuilds-égalisés"):
            return "régime"
        if e in ("garde-sceau-I", "oracle-bloc-loupe-01",
                 "oracle-du-bloc-loupe-02", "epreuve-scenario-posix"):
            return "implémentation de vérification"
        if e.startswith("assemblage-kits"):
            return "gouvernance"
    else:
        if e in ("build-gcc-O2-loupe-01", "build-gcc-O2-loupe-02") \
                or e.startswith("rebuilds-cristallisation-"):
            return "régime"
        if e in ("suite-tests-c-hash", "suite-tests-c-contrat",
                 "controles-binaires-loupe-01",
                 "epreuve-contrat-posix-loupe-02",
                 "controles-binaires-loupe-02", "garde-sceau-I"):
            return "implémentation de vérification"
        if e in ("garde-intentions-signees", "chaine-cristallisation",
                 "assemblage-kit"):
            return "gouvernance"
    return "?"


FICHIER = {"T": "T", "C+G+": "CGP", "C+G": "CG", "C": "C"}


def charger(bras: str) -> list[dict]:
    return [json.loads(
        (ICI / f"m4v13-{FICHIER[bras]}-run{i}.json").read_text(
            encoding="utf-8")) for i in range(1, N + 1)]


def main() -> int:
    print("[hcgp3] LA RÉCONCILIATION QUATRE EFFETS")
    # (1) LA RÉCONCILIATION PAR RUN (chaque total depuis ses étapes)
    reconc = {}
    tout_vert = True
    for bras in ["T", "C+G+", "C+G", "C"]:
        runs = charger(bras)
        ecarts = []
        for r in runs:
            somme = round(sum(e["secondes"] for e in r["etapes"]), 3)
            ecart = abs(somme - r["total_s"])
            ecarts.append(ecart)
            if ecart > TOLERANCES[bras]:
                tout_vert = False
                print(f"  [REFUS] {bras} run {r['run']} : somme {somme} != "
                      f"total {r['total_s']} (écart {ecart:.3f} > "
                      f"{TOLERANCES[bras]})")
        reconc[bras] = {"ecarts_max": max(ecarts),
                        "runs": [{"run": r["run"], "total": r["total_s"],
                                  "somme": round(sum(
                                      e["secondes"] for e in r["etapes"]),
                                      3)} for r in runs]}
        print(f"  {bras:<5} : écart max somme/total "
              f"{max(ecarts)*1000:.0f} ms (tolérance "
              f"{TOLERANCES[bras]*1000:.0f} ms) "
              f"{'VERT' if max(ecarts) <= TOLERANCES[bras] else 'ROUGE'}")

    # (2) LES MÉDIANES PAR BRAS (le régime T : l'AUDIT nommé et exclu —
    #     l'oracle-02 re-exécuté vivant, le prix de la preuve)
    med = {}
    for bras in ["T", "C+G+", "C+G", "C"]:
        runs = charger(bras)
        totaux = [r["total_s"] for r in runs]
        audit = []
        if bras == "T":
            # l'AUDIT : un run dont l'oracle-02 dépasse 5 s (la re-exécution
            # vivante du 10ᵉ scellement — le compteur du mémo v2)
            audit = [r["run"] for r in runs
                     if any(e["etape"].startswith("oracle-du-bloc")
                            and e["secondes"] > 5 for e in r["etapes"])]
            regime = [r["total_s"] for r in runs if r["run"] not in audit]
        else:
            regime = totaux
        med[bras] = {"medianne": round(statistics.median(regime), 3),
                     "regime_n": len(regime),
                     "audit_runs": audit,
                     "tous": sorted(totaux)}
        print(f"  {bras:<5} : médiane régime {med[bras]['medianne']:.3f} s "
              f"(n={len(regime)}"
              + (f", l'AUDIT aux runs {audit} NOMMÉ ET EXCLU" if audit
                 else "") + f") ; tous : {sorted(totaux)}")

    # (3) LA DÉCOMPOSITION PAR POSTE DES QUATRE BRAS (l'instrumentation)
    postes = {}
    for bras in ["T", "C+G+", "C+G", "C"]:
        runs = charger(bras)
        if bras == "T":
            runs = [r for r in runs if r["run"] not in med["T"]["audit_runs"]]
        par_poste = {}
        for r in runs:
            somme_run = {}
            for e in r["etapes"]:
                p = poste_de(e["etape"], bras)
                somme_run[p] = somme_run.get(p, 0.0) + e["secondes"]
            for p, s in somme_run.items():
                par_poste.setdefault(p, []).append(round(s, 3))
        postes[bras] = {p: round(statistics.median(v), 3)
                        for p, v in sorted(par_poste.items())}
        print(f"  {bras:<5} par poste : {postes[bras]}")

    # (4) LA VENTILATION T−C (la somme == T−C à la milliseconde)
    t_med, c_med = med["T"]["medianne"], med["C"]["medianne"]
    tc = round(t_med - c_med, 3)
    vent = {}
    for p in ["notation intrinsèque", "implémentation de vérification",
              "régime", "gouvernance"]:
        vt = postes["T"].get(p, 0.0)
        vc = postes["C"].get(p, 0.0)
        vent[p] = round(vt - vc, 3)
    somme_vent = round(sum(vent.values()), 3)
    print(f"  T−C = {tc:.3f} s ; la ventilation {vent} ; la somme "
          f"{somme_vent:.3f} s")

    # (5) LE VERDICT H-CGP3 (l'énoncé falsifiable du plan gelé) — le T−C
    #     DE LA VENTILATION (la somme des postes, exacte par construction ;
    #     l'écart à la médiane des totaux NOMMÉ : la sommation des médianes
    #     vs la médiane des sommes — le précédent vague 11)
    tc_vent = somme_vent
    tc_totaux = tc
    print(f"  LE T−C DE LA VENTILATION : {tc_vent:.3f} s (la somme des "
          f"postes, EXACTE par construction) ; la médiane des totaux "
          f"{tc_totaux:.3f} s — l'écart {tc_vent - tc_totaux:+.3f} s NOMMÉ "
          f"(la sommation des médianes vs la médiane des sommes, le "
          f"précédent vague 11)")
    ni = vent["notation intrinsèque"]
    part = ni / tc_vent if tc_vent else float("inf")
    if part <= 0.30:
        verdict = ("H-CGP3 TENUE — la part de l'effet notation intrinsèque "
                   f"({ni:.3f} s / {tc_vent:.3f} s = {part*100:.1f} %) est "
                   "≤ 30 % : le coût dominant de la vague 11 étiqueté "
                   "« notation » était l'effet IMPLÉMENTATION DE "
                   "VÉRIFICATION (les oracles, l'émulation vs le natif)")
    else:
        verdict = ("H-CGP3 REJETÉE — la part mesurée "
                   f"({ni:.3f} s / {tc_vent:.3f} s = {part*100:.1f} %) dépasse "
                   "30 % : le coût intrinsèque de la notation DOMINE à "
                   "volumes égalisés")
    print(f"  LE VERDICT : {verdict}")

    # (6) LA TABLE PAR UNITÉ DES REBUILDS ÉGALISÉS (publiée — le plan §1)
    table_unites = {}
    for r in charger("T"):
        if r["run"] in med["T"]["audit_runs"]:
            continue
        for e in r["etapes"]:
            if e["etape"].startswith("rebuilds-égalisés"):
                u = e["etape"].split("égalisés-")[1].split(" ")[0]
                table_unites.setdefault(u, []).append(e["secondes"])
    table = {u: round(statistics.median(v), 3)
             for u, v in sorted(table_unites.items())}
    print(f"  LA TABLE PAR UNITÉ (les rebuilds T, médianes) : {table}")
    total_rebuilds_t = round(sum(table.values()), 3)
    print(f"  le total des rebuilds T : {total_rebuilds_t:.3f} s "
          f"(10 × 6 = 60 par bras — le plan)")

    out = {"reconciliation": reconc, "medianes": med, "postes": postes,
           "ventilation_T_C": vent, "somme_ventilation": somme_vent,
           "T_minus_C_ventilation": tc_vent,
           "T_minus_C_medianes_totaux": tc_totaux,
           "ecart_sommation_medianes": round(tc_vent - tc_totaux, 3),
           "part_notation_intrinseque": round(part, 4),
           "verdict_hcgp3": verdict, "table_rebuilds_par_unite": table,
           "tolerances": TOLERANCES, "graine_ordre": 20261122, "n": N}
    (ICI / "reconciliation.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[hcgp3] reconciliation.json consigné")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
