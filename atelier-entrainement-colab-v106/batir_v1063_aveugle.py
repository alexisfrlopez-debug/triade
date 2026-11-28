#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA COPIE AVEUGLE DU v1063 — l'invariant du v104 asserté : la SEULE
divergence vivante/aveugle = les TROIS constantes de la cellule des
identifiants (le reste byte-byte). La pièce publique du dépôt."""
import difflib
import hashlib
import json
import pathlib

VIVANTE = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1063-VIVANTE.ipynb")
AVEUGLE = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1063-AVEUGLE.ipynb")

nb = json.loads(VIVANTE.read_text(encoding="utf-8"))
src6 = "".join(nb["cells"][6]["source"])
for constante in ("CLIENT_ID", "CLIENT_SECRET", "REFRESH_TOKEN"):
    vieux = next(l for l in src6.splitlines() if l.startswith(constante + ' = "'))
    src6 = src6.replace(vieux, constante + ' = ""')
nb["cells"][6]["source"] = [src6]
AVEUGLE.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ── l'épreuve de l'invariant ──
v = json.loads(VIVANTE.read_text(encoding="utf-8"))
a = json.loads(AVEUGLE.read_text(encoding="utf-8"))
diffs = []
for i, (cv, ca) in enumerate(zip(v["cells"], a["cells"])):
    if "".join(cv["source"]) != "".join(ca["source"]):
        diffs.append(i)
if diffs != [6]:
    raise SystemExit(f"INVARIANT-ROMPU : cellules divergentes {diffs} != [6]")
sa = "".join(a["cells"][6]["source"])
for ligne in sa.splitlines():
    if ligne.startswith(("CLIENT_ID", "CLIENT_SECRET", "REFRESH_TOKEN")):
        assert ligne.endswith('= ""'), ligne
nb_lignes_diff = sum(1 for l in difflib.unified_diff(
    "".join(v["cells"][6]["source"]).splitlines(), sa.splitlines(), lineterm="", n=0)
    if l.startswith(("+", "-")) and not l.startswith(("+++", "---")))
if nb_lignes_diff != 6:   # 3 retirées + 3 posées
    raise SystemExit(f"INVARIANT-ROMPU : {nb_lignes_diff} lignes ≠ 6 (les TROIS constantes)")
tout = "\n".join("".join(c["source"]) for c in a["cells"])
for interdit in ("GOCSPX", "15826935491", "1//0e3minhW"):
    if interdit in tout:
        raise SystemExit(f"SECRET-PRESENT : {interdit}")
print(f"[aveugle] l'invariant TENU : la seule divergence = les TROIS constantes "
      f"(cellule 6) — {AVEUGLE.name} ({AVEUGLE.stat().st_size} o)")
print(f"[aveugle] sha256 : {hashlib.sha256(AVEUGLE.read_bytes()).hexdigest()}")
