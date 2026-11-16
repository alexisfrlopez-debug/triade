#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""calcule_rq2_v2.py — les distributions de la re-mesure RQ2 v2 depuis
p4-mesures-brutes.jsonl (aucune valeur tapée à la main)."""
import json
import pathlib

BRUTES = pathlib.Path("/home/z/my-project/livraison-vague4/p4-mesures-brutes.jsonl")
rs = [json.loads(l) for l in BRUTES.read_text(encoding="utf-8").splitlines()]

def stats(valeurs):
    v = sorted(valeurs)
    n = len(v)
    def pct(p):
        k = (n - 1) * p
        f = int(k)
        c = min(f + 1, n - 1)
        return v[f] + (v[c] - v[f]) * (k - f)
    return {"n": n, "min": v[0], "q1": pct(0.25), "mediane": pct(0.5),
            "q3": pct(0.75), "max": v[-1]}

print(f"{len(rs)} lignes, opérations : " +
      ", ".join(sorted({r.get('operation','?') for r in rs})))
for op in ("localiser", "éditer", "ajouter"):
    sel = [r for r in rs if r.get("operation") == op and "erreur" not in r]
    tot = stats([r["total_tokens"] for r in sel])
    c1k = stats([r["cl100k_prompt"] + r["cl100k_completion"] for r in sel])
    lat = stats([r["latence_s"] for r in sel])
    print(f"\n{op.upper()} n={tot['n']}:")
    print(f"  total natif  : médiane {tot['mediane']:.1f} [q1 {tot['q1']:.0f} .. q3 {tot['q3']:.0f}] (min {tot['min']}, max {tot['max']})")
    print(f"  cl100k       : médiane {c1k['mediane']:.1f} rapport {c1k['mediane']/tot['mediane']:.3f}")
    print(f"  latence      : médiane {lat['mediane']:.1f}s")

# ratios demandés par l'instruction I1 : 300304/1277 et 300304/3674
meds = {}
for op in ("localiser", "éditer", "ajouter"):
    sel = [r for r in rs if r.get("operation") == op and "erreur" not in r]
    meds[op] = stats([r["total_tokens"] for r in sel])["mediane"]
BASE = 300304
print(f"\nratios baseline naïve : 300304/{meds['localiser']:.0f} = {BASE/meds['localiser']:.1f}x ; "
      f"300304/{meds['éditer']:.0f} = {BASE/meds['éditer']:.1f}x ; "
      f"300304/{meds['ajouter']:.0f} = {BASE/meds['ajouter']:.1f}x")

# §3.5 : audit benchmark signes
import csv
audit = list(csv.DictReader(open(
    "/home/z/my-project/gdrive/projet/triade-complet/preuves_historiques/preuves_v130/audit_benchmark.csv",
    encoding="utf-8-sig")))
par = {r["implementation"]: r for r in audit}
n_blocs = int(par["tls13-01..04 (blocs)"]["instructions_par_op"].replace(" ", "").replace(",", ""))
o2 = int(par["gcc -O2 (fonction)"]["instructions_par_op"].replace(" ", "").replace(",", ""))
os_ = int(par["gcc -Os (fonction)"]["instructions_par_op"].replace(" ", "").replace(",", ""))
print(f"\n§3.5 audit : notation {n_blocs} vs -O2 {o2} ({(n_blocs-o2)/o2*100:+.1f}%) vs -Os {os_} ({(n_blocs-os_)/os_*100:+.1f}%)")
