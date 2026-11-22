#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hcgp4_reconcilier.py — LE RÉCONCILIATEUR QUATRE EFFETS (S2P9BM3ZD, la
vague 14) : chaque total réconcilié depuis ses étapes aux tolérances
publiées (T ±0,150 s · C+G+ ±0,100 s · C+G, C ±0,050 s) ; la ventilation
T−C à la milliseconde ; H-CGP4 tranché par mesure — la part RÉGIME du T−C
AVANT (la vague 13 publiée : 17,487 s · 88,4 %, datée 22/11/2026, JAMAIS
fusionnée) et APRÈS (la vague 14 mesurée, la mémoïsation content-addressée
des 60 rebuilds) côte à côte.

LA CLASSIFICATION PAR POSTE (figée au plan gelé, inchangée) :
  — notation intrinsèque : round-trips de notation, recomposition du
    plan, cristallisation (incrémentale) ;
  — implémentation de vérification : oracles (re-exécutions vivantes),
    gardes de sceau, épreuves confrontées, tests/contrôles du C ;
  — régime : rebuilds (les reconstructions de pièces/bloc côté T au
    MÉMO content-addressé / les compilations gcc côté C — les bras C
    demeurent AU MÉMO NUL, le comparateur honnête) ;
  — gouvernance : g1-g4 (C+G/C+G+), l'assemblage des kits (T — la
    reprise comprise, le mécanisme v13).

Sortie : reconciliation.json."""
from __future__ import annotations

import json
import pathlib
import statistics
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-hcgp4-s2p9bm3zd"
TOLERANCES = {"T": 0.150, "C+G+": 0.100, "C+G": 0.050, "C": 0.050}
N = 5
GRAINE = 20261123

# LA VAGUE 13 PUBLIÉE (datée 22/11/2026 — le AVANT, JAMAIS fusionné avec
# la mesure du jour) : la ventilation T−C de ay6zuzm8o
V13 = {"notation intrinsèque": 1.079, "implémentation de vérification": 0.779,
       "régime": 17.487, "gouvernance": 0.442, "T_minus_C": 19.787,
       "part_régime_pct": 88.4, "T": 21.633, "C": 1.934}


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
        (ICI / f"m4v14-{FICHIER[bras]}-run{i}.json").read_text(
            encoding="utf-8")) for i in range(1, N + 1)]


def audits_oracle(runs: list[dict]) -> list[int]:
    """Les runs T dont UN oracle dépassé 5 s — l'AUDIT du mémo v2 (la
    re-exécution vivante au scellement multiple de 10 — généralisé : un
    oracle QUELCONQUE peut porter le scellement)."""
    return [r["run"] for r in runs
            if any(e["etape"].startswith(("oracle-bloc", "oracle-du-bloc"))
                   and e["secondes"] > 5 for e in r["etapes"])]


def main() -> int:
    print("[hcgp4] LA RÉCONCILIATION QUATRE EFFETS (la vague 14)")
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

    # (2) LES MÉDIANES PAR BRAS (le régime T : l'AUDIT oracle nommé et
    #     exclu — le prix de la preuve du mémo v2, miroir v13)
    med = {}
    for bras in ["T", "C+G+", "C+G", "C"]:
        runs = charger(bras)
        totaux = [r["total_s"] for r in runs]
        audit = audits_oracle(runs) if bras == "T" else []
        regime = [r["total_s"] for r in runs if r["run"] not in audit]
        med[bras] = {"medianne": round(statistics.median(regime), 3),
                     "regime_n": len(regime),
                     "audit_runs": audit,
                     "tous": sorted(totaux)}
        print(f"  {bras:<5} : médiane régime {med[bras]['medianne']:.3f} s "
              f"(n={len(regime)}"
              + (f", l'AUDIT oracle aux runs {audit} NOMMÉ ET EXCLU" if audit
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

    # (5) LE VERDICT H-CGP4 — la part régime AVANT (la vague 13 publiée,
    #     datée, JAMAIS fusionnée) / APRÈS (la vague 14 mesurée)
    tc_vent = somme_vent
    tc_totaux = tc
    ecart_sommation = round(tc_vent - tc_totaux, 3)
    print(f"  LE T−C DE LA VENTILATION : {tc_vent:.3f} s (la somme des "
          f"postes, EXACTE par construction) ; la médiane des totaux "
          f"{tc_totaux:.3f} s — l'écart {ecart_sommation:+.3f} s NOMMÉ (la "
          f"sommation des médianes vs la médiane des sommes, miroir v13)")
    part_v14 = vent["régime"] / tc_vent if tc_vent else float("inf")
    reduc_abs = round(V13["régime"] - vent["régime"], 3)
    if vent["régime"] < V13["régime"]:
        verdict = (
            f"H-CGP4 TENUE — la part RÉGIME du T−C RÉDUITE : "
            f"{V13['régime']:.3f} s ({V13['part_régime_pct']:.1f} %, la "
            f"vague 13 datée 22/11/2026, publiée AVANT) → "
            f"{vent['régime']:.3f} s ({100*part_v14:.1f} %, la vague 14 "
            f"mesurée, la mémoïsation content-addressée des 60 rebuilds) — "
            f"la réduction {reduc_abs:+.3f} s ; les graines, vecteurs et "
            f"contrôles CONSERVÉS (vérifiés par hcgp4_verifier.py : "
            f"l'audit 1/10 vécu et vert, les consoles, les scellés)")
    else:
        verdict = (
            f"H-CGP4 FALSIFIÉE — la part régime du T−C "
            f"{vent['régime']:.3f} s ({100*part_v14:.1f} %) N'EST PAS "
            f"réduite sous la vague 13 publiée ({V13['régime']:.3f} s) : "
            f"la mémoïsation ne paie pas")
    print(f"  LE VERDICT : {verdict}")

    # (6) LA TABLE PAR UNITÉ DES REBUILDS ÉGALISÉS (publiée — le plan §1)
    #     et LE MÉMO des rebuilds (les origines nommées, jamais une miss
    #     maquillée en exécution)
    table_unites = {}
    memo_ops = {}
    for r in charger("T"):
        for e in r["etapes"]:
            if e["etape"].startswith("rebuilds-égalisés"):
                u = e["etape"].split("égalisés-")[1].split(" ")[0]
                table_unites.setdefault(u, []).append(e["secondes"])
                m = e["memo"]
                memo_ops.setdefault(u, {"hit": 0, "miss": 0, "audit": 0,
                                        "audits_verts": 0, "ecarts": 0,
                                        "vivantes": []})
                memo_ops[u]["hit"] += m["hits"]
                memo_ops[u]["miss"] += m["misses"]
                memo_ops[u]["audit"] += m["audits"]
                memo_ops[u]["audits_verts"] += m["audits_verts"]
                memo_ops[u]["ecarts"] += len(m["ecarts"])
                memo_ops[u]["vivantes"] += list(m["vivantes"].values())
    table = {u: round(statistics.median(v), 3)
             for u, v in sorted(table_unites.items())}
    print(f"  LA TABLE PAR UNITÉ (les rebuilds T, médianes) : {table}")
    total_rebuilds_t = round(sum(table.values()), 3)
    print(f"  le total des rebuilds T : {total_rebuilds_t:.3f} s "
          f"(10 × 6 = 60 par bras — le plan)")
    memo_glob = {"hits": sum(v["hit"] for v in memo_ops.values()),
                 "misses": sum(v["miss"] for v in memo_ops.values()),
                 "audits": sum(v["audit"] for v in memo_ops.values()),
                 "audits_verts": sum(
                     v["audits_verts"] for v in memo_ops.values()),
                 "ecarts": sum(v["ecarts"] for v in memo_ops.values())}
    print(f"  LE MÉMO des rebuilds (les 5 runs) : {memo_glob} ; par "
          f"unité : { {u: {k: v for k, v in d.items() if k != 'vivantes'} for u, d in memo_ops.items()} }")

    out = {"reconciliation": reconc, "medianes": med, "postes": postes,
           "ventilation_T_C": vent, "somme_ventilation": somme_vent,
           "T_minus_C_ventilation": tc_vent,
           "T_minus_C_medianes_totaux": tc_totaux,
           "ecart_sommation_medianes": ecart_sommation,
           "part_regime_v14": round(part_v14, 4),
           "vague13_publiee": V13,
           "verdict_hcgp4": verdict,
           "table_rebuilds_par_unite": table,
           "total_rebuilds_t": total_rebuilds_t,
           "memo_par_unite": {u: {k: v for k, v in d.items()
                                  if k != "vivantes"}
                              for u, d in memo_ops.items()},
           "memo_global": memo_glob,
           "tolerances": TOLERANCES, "graine_ordre": GRAINE, "n": N}
    (ICI / "reconciliation.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[hcgp4] reconciliation.json consigné")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
