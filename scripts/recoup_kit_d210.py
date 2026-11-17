#!/usr/bin/env python3
"""Recoupe les pièces du kit D210 unité-01 contre EMPREINTES gravées."""
import hashlib, pathlib, sys

KIT = pathlib.Path("/home/z/my-project/download/triade-d210-unite-01/"
                   "kit-unite-01-d210-20261117")
EMP = KIT / "EMPREINTES-KIT-UNITE-01-D210.txt"

gravures = {}
for ligne in EMP.read_text(encoding="utf-8").splitlines():
    parts = ligne.strip().split(None, 2)
    if len(parts) >= 2 and len(parts[0]) == 64:
        gravures[parts[1]] = parts[0].lower()

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()

ok, ecart = 0, []
for nom, att in sorted(gravures.items()):
    p = KIT / nom
    if not p.is_file():
        ecart.append((nom, "ABSENT"))
        continue
    v = sha256(p)
    if v == att:
        ok += 1
    else:
        ecart.append((nom, f"{v[:16]}… != {att[:16]}…"))
print(f"{ok}/{len(gravures)} pièces recoupées VERT")
for nom, d in ecart:
    print("ÉCART:", nom, d)
sys.exit(0 if not ecart else 1)
