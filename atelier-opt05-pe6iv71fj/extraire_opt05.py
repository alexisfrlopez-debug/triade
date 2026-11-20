#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_opt05.py — L'EXTRACTION DES GAINS OPT-05 (le plan § 1.4) : le
gain lu des logs bruts, 1 − médiane(hunk)/médiane(avant), par opération
(éditer, ajouter), le total ET la réponse séparément — jamais tapé à la
main. LES DISTRIBUTIONS COMPLÈTES (n, médiane, q1, q3, min, max) par
cellule et par champ. Sortie : extraire_opt05.json + le tableau texte."""
from __future__ import annotations

import json
import pathlib
import statistics

ICI = pathlib.Path(__file__).resolve().parent


def dist(valeurs: list) -> dict:
    v = sorted(valeurs)
    n = len(v)
    return {
        "n": n,
        "mediane": statistics.median(v),
        "q1": v[n // 4] if n >= 4 else v[0],
        "q3": v[3 * n // 4] if n >= 4 else v[-1],
        "min": v[0], "max": v[-1],
    }


def main() -> int:
    journal = [json.loads(l) for l in
               (ICI / "journal_tokens.jsonl").read_text(encoding="utf-8").splitlines()
               if l.strip()]
    resultats = [json.loads(l) for l in
                 (ICI / "resultats_opt05.jsonl").read_text(encoding="utf-8").splitlines()
                 if l.strip()]
    verdicts = {r["tache"]: r["verdict"] for r in resultats}
    rq2 = [json.loads(l) for l in
           (ICI / "resultats_rq2.jsonl").read_text(encoding="utf-8").splitlines()
           if l.strip()]

    cellules = ["editer-A", "editer-H2", "ajouter-A2", "ajouter-H2"]
    rapport = {"cellules": {}, "gains": {}, "rq2": {}, "verdissement": {}}
    print("== LES DISTRIBUTIONS (le tokenizer natif lu du log d'usage) ==")
    print(f"{'cellule':12s} {'n':>3} {'médiane':>8} {'q1':>6} {'q3':>6} "
          f"{'min':>6} {'max':>6}   {'réponse':>7}   verts")
    for c in cellules:
        lignes = [j for j in journal if j["tache"].startswith(c + "-")]
        tot = [j["total_tokens"] for j in lignes]
        comp = [j["completion_tokens"] for j in lignes]
        verts = sum(1 for j in lignes if "OK" in verdicts.get(j["tache"], ""))
        d, dc = dist(tot), dist(comp)
        rapport["cellules"][c] = {"total": d, "reponse": dc, "verts": verts,
                                  "n": len(lignes)}
        print(f"{c:12s} {d['n']:>3} {d['mediane']:>8.0f} {d['q1']:>6.0f} "
              f"{d['q3']:>6.0f} {d['min']:>6.0f} {d['max']:>6.0f}   "
              f"{dc['mediane']:>7.0f}   {verts}/{len(lignes)}")

    print()
    print("== LES GAINS (1 − médiane hunk / médiane avant) ==")
    for op, avant, hunk in [("editer", "editer-A", "editer-H2"),
                            ("ajouter", "ajouter-A2", "ajouter-H2")]:
        ma = rapport["cellules"][avant]["total"]["mediane"]
        mh = rapport["cellules"][hunk]["total"]["mediane"]
        ra = rapport["cellules"][avant]["reponse"]["mediane"]
        rh = rapport["cellules"][hunk]["reponse"]["mediane"]
        gain_t = 1 - mh / ma
        gain_r = 1 - rh / ra
        rapport["gains"][op] = {"total": round(gain_t, 4), "reponse": round(gain_r, 4),
                                "avant_mediane": ma, "hunk_mediane": mh,
                                "avant_reponse": ra, "hunk_reponse": rh}
        print(f"{op:8s} total : {ma:8.0f} -> {mh:8.0f}  ({gain_t:+.1%})   "
              f"réponse : {ra:6.0f} -> {rh:6.0f}  ({gain_r:+.1%})")

    # les records v1 (la falsification, jamais effacés)
    for c in ("editer-H", "ajouter-A"):
        lignes = [j for j in journal if j["tache"].startswith(c + "-")]
        if lignes:
            verts = sum(1 for j in lignes if "OK" in verdicts.get(j["tache"], ""))
            rapport["verdissement"][c] = {"n": len(lignes), "verts": verts}
            print(f"\nrecord v1 {c}: n={len(lignes)} verts={verts} "
                  f"(l'ambiguïté de la spécification, les pièces au garde-brut)")

    # RQ2
    tot = [r["total_tokens"] for r in rq2]
    dr = dist(tot)
    rapport["rq2"] = {"post_opt04": dr,
                      "conformes": sum(1 for r in rq2 if r["verdict"] == "CONFORME"),
                      "n": len(rq2)}
    print(f"\n== RQ2 re-mesure (pointeur seul, la graine 20261117) ==")
    print(f"n={dr['n']} médiane={dr['mediane']:.0f} [{dr['q1']}..{dr['q3']}] "
          f"min={dr['min']} max={dr['max']} — "
          f"{rapport['rq2']['conformes']}/{dr['n']} conformes")

    (ICI / "extraire_opt05.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n-> extraire_opt05.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
