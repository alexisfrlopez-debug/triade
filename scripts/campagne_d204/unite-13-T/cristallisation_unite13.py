#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cristallisation_unite13.py — LA CRISTALLISATION DE LA PIÈCE (l'unité 5,
loupe-13 × bras T) : DIX rebuilds complets, chacun la recomposition entière
depuis le plan (le brouillon → l'auteur → l'assemblage des 18 blocs → le
PE) — les DIX sha256 IDENTIQUES, la pièce est DÉTERMINISTE du plan au
byte près (le miroir des cristallisations des unités 1-4)."""
import hashlib
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-13-T")
BUILD = os.path.join(UNITE, "build_unite13.py")

empreintes = []
for k in range(10):
    r = subprocess.run([sys.executable, BUILD], capture_output=True,
                       text=True, timeout=600)
    if r.returncode != 0:
        print(r.stdout[-2000:])
        print(r.stderr[-2000:], file=sys.stderr)
        sys.exit(2)
    ligne = [l for l in r.stdout.splitlines()
             if l.startswith("[pièce]")][0]
    sha = ligne.split("sha256 ")[1].strip()
    empreintes.append(sha)
    print(f"  rebuild {k + 1}/10 : {sha[:16]}… ({len(empreintes)} "
          f"{'IDENTIQUE' if len(set(empreintes)) == 1 else 'DIVERGE !'})")

assert len(set(empreintes)) == 1, \
    f"LA CRISTALLISATION ROMPUE : {set(empreintes)}"
piece = os.path.join(UNITE, "piece", "loupe.exe")
assert hashlib.sha256(open(piece, "rb").read()).hexdigest() == empreintes[0]
print(f"=== LA CRISTALLISATION VERTE : DIX rebuilds identiques — "
      f"loupe.exe {os.path.getsize(piece)} o, sha256 {empreintes[0]} ===")
