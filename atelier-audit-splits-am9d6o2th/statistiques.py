#!/usr/bin/env python3
"""statistiques de la matiere — atelier AM9D6O2TH (lecture seule)."""
import json, os, re, sys, collections

ds = sys.argv[1]
RE = re.compile(r"^(loupe-\d+|tls13-\d+|sys-\d+)\s*·", re.MULTILINE)

def cid(e):
    m = RE.search(e.get("contrat", ""))
    if m: return m.group(1)
    m = re.match(r"^((?:loupe|tls13|sys)-\d+)", e.get("bloc", ""))
    return m.group(1) if m else None

stats = collections.defaultdict(lambda: collections.Counter())
verdicts = collections.Counter()
for split in ("train", "dev", "test"):
    with open(os.path.join(ds, split + ".jsonl"), encoding="utf-8") as f:
        for ligne in f:
            if not ligne.strip(): continue
            e = json.loads(ligne)
            c = cid(e)
            if c is None:
                stats["<canari>"][("sans-contrat", "-", split)] += 1
                verdicts["sans-contrat"] += 1
                continue
            stats[c][(e.get("vague", "?"), e.get("verdict", "?"), split)] += 1
            verdicts[e.get("verdict", "?")] += 1

print("=== LES VERDICTS AU CORPUS ===")
for v, n in verdicts.most_common():
    print(f"  {v:10s} {n}")
print()
print("=== PAR CONTRAT / CAMPAGNE / VERDICT / SPLIT ===")
for c in sorted(stats):
    print(f"  {c}")
    for (vg, vd, sp), n in sorted(stats[c].items()):
        print(f"      {vg:3s} {vd:8s} {sp:6s} {n}")
