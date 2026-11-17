#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reprise_b.py — le complément de la campagne : les appels B manquants
(l'échec nommé de la première passe : l'instrument a refusé un appel —
la reprise respecte l'ORDRE DE LA GRAINE, un appel à la fois, espacés).

Chaque appel reste INSTRUMENTÉ (compter_tokens) — jamais reconstitué."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time

ICI = pathlib.Path(__file__).resolve().parent
RIG = ICI.parent / "atelier-baseline-20261117" / "rig" / "compter_tokens.py"
journal = ICI / "journal_tokens.jsonl"
garde = ICI / "garde-brut.jsonl"
prompts = ICI / "garde-prompts"

# l'ordre de la graine (le plan § 4 — relu de verites-terrain.json)
vt = json.loads((ICI / "verites-terrain.json").read_text(encoding="utf-8"))
ordre = vt["ordre"]

deja = set()
for l in journal.read_text(encoding="utf-8").splitlines():
    if l.strip():
        deja.add(json.loads(l)["tache"])

manquants = [f"localiser-B-{bid}" for bid in ordre
             if f"localiser-B-{bid}" not in deja]
print(f"[reprise] {len(manquants)} appel(s) B manquant(s) : {manquants}")

for i, tache in enumerate(manquants):
    pfile = prompts / f"{tache}.txt"
    assert pfile.exists(), f"le prompt du geste manquant : {pfile}"
    for essai in (1, 2, 3):
        time.sleep(45 if essai > 1 else 20)
        r = subprocess.run(
            ["python3", str(RIG), "--bras", "T", "--phase", "analyse",
             "--tache", tache, "--prompt-file", str(pfile),
             "--journal", str(journal), "--garde-brut", str(garde)],
            capture_output=True, text=True, timeout=600)
        if r.returncode == 0:
            ligne = [l for l in r.stderr.splitlines() if "tokens" in l]
            print(f"[{tache}] (essai {essai}) {ligne[-1] if ligne else 'OK'}")
            break
        print(f"[{tache}] (essai {essai}) ÉCHEC : "
              f"{(r.stderr or r.stdout).strip().splitlines()[-1][:200]}")
    else:
        print(f"[{tache}] ÉCHEC DÉFINITIF — un écart nommé, jamais reconstitué")
        sys.exit(2)

print(f"\n[reprise] le journal porte désormais "
      f"{sum(1 for l in journal.read_text().splitlines() if l.strip())} lignes")
