#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE NOTEBOOK v1061 — LE DÉFAUT DU v106 CORRIGÉ : la cellule serving du v106
livré fut assemblée sur la cellule du v105 ORIGINAL — elle porte les DEUX
bugs du jour (le terrain.9 : le choix cudart sans binaires ; le terrain.10 :
la porte lit [\"probs\"]) que le v1051/v1052 ont corrigés pour la campagne
105. La conséquence pour le run du maître (lancé au navigateur) :
l'entraînement et l'adapter SONT SAUVÉS (la cellule 6 téléverse AVANT
l'éval — la loi du plan gelé § 4), MAIS l'éval eût REFUSÉ à la porte de
parole (faux BORD-MUET, KeyError 'probs' à b12823).

L'AMENDEMENT v1061 : la cellule serving REMPLACÉE par celle du v1052 (qui
porte le terrain.9 bins_cuda + le terrain.10 bivalent) + l'injection --lora
(l'adapter né à la cellule 5) — le reste du notebook DEMEURE BYTE-BYTE le
v106 livré (l'épreuve l'asserte)."""
import hashlib
import json
import pathlib

V106 = pathlib.Path("/home/z/my-project/work/kit-entrainement-v106/Entrainement-Colab-v106-VIVANTE.ipynb")
V1052 = pathlib.Path("/home/z/my-project/work/Campagne-Colab-v1052-VIVANTE.ipynb")
DEST = pathlib.Path("/home/z/my-project/work/kit-entrainement-v106/Entrainement-Colab-v1061-VIVANTE.ipynb")

nb = json.loads(V106.read_text(encoding="utf-8"))
v1052 = json.loads(V1052.read_text(encoding="utf-8"))

# la cellule serving du v1052 (les DEUX correctifs du jour)
src_1052 = next("".join(c["source"]) for c in v1052["cells"]
                if c["cell_type"] == "code" and "asset_de_la_release" in "".join(c["source"]))

# les TROIS amendements v106 (le titre, la commande, l'injection --lora)
for vieux, nouveau in (
    ("# CELLULE 5 — LE SERVING SELON L'ENVIRONNEMENT (v1051 — LE TERRAIN.9 DU",
     "# CELLULE 7 — LE SERVING DU MODÈLE AFFINÉ (v1061 — la cellule du v1052 : les\n"
     "# DEUX correctifs du jour, le terrain.9 bins_cuda + le terrain.10 bivalent\n"
     "# — le v1051 — LE TERRAIN.9 DU"),
    ("# du bord. La commande consignée au LISEZMOI-CAMPAGNE-POSTE § 1 (llama-server",
     "# byte-byte la 105 + LE DELTA --lora (l'adapter né à la cellule 5). La commande"),
    ('    if GPU:\n        args_serving += ["-ngl", "99"]',
     '    if GPU:\n        args_serving += ["-ngl", "99"]\n'
     '    args_serving += ["--lora", str(pathlib.Path("/content/adapter-entrainement-v106.gguf"))]'),
):
    if vieux not in src_1052:
        raise SystemExit(f"AMENDEMENT-ROMPU : {vieux[:60]!r}")
    src_1052 = src_1052.replace(vieux, nouveau)

# la cellule serving du v106 (l'index)
idx = next(i for i, c in enumerate(nb["cells"])
           if c["cell_type"] == "code" and "asset_de_la_release" in "".join(c["source"]))
nb["cells"][idx]["source"] = [src_1052]
DEST.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ── LES ÉPREUVES ──
compile(src_1052, "cellule-serving-v1061", "exec")
print("[épreuve 1] la cellule serving v1061 compile — VERT")
orig = json.loads(V106.read_text(encoding="utf-8"))
nb2 = json.loads(DEST.read_text(encoding="utf-8"))
div = [i for i, (a, b) in enumerate(zip(orig["cells"], nb2["cells"]))
       if "".join(a["source"]) != "".join(b["source"])]
if div != [idx]:
    raise SystemExit(f"[épreuve 2] INVARIANT-ROMPU : cellules divergentes {div} ≠ [{idx}]")
print(f"[épreuve 2] la SEULE cellule touchée = la serving (#{idx}) — VERT")
for marque in ("bins_cuda", "top_logprobs", "--lora", "adapter-entrainement-v106.gguf"):
    if marque not in src_1052:
        raise SystemExit(f"[épreuve 3] MARQUE-ABSENTE : {marque}")
print("[épreuve 3] bins_cuda + top_logprobs + --lora présents — VERT")
# le pin v102 demeure (la cellule des kits intacte)
src_kits = "".join(nb2["cells"][6]["source"])
if "poste_v102" not in src_kits or "60962d74" not in src_kits:
    raise SystemExit("[épreuve 4] PIN-V102-PERDU")
print("[épreuve 4] le pin v102 (le moteur bivalent) intact — VERT")
# les identifiants vivants présents (la copie vivante)
tout = "\n".join("".join(c["source"]) for c in nb2["cells"] if c["cell_type"] == "code")
if "GOCSPX" not in tout:
    raise SystemExit("[épreuve 5] IDENTIFIANTS-PERDUS (la vivante doit les porter)")
print("[épreuve 5] les identifiants du relais présents (la copie VIVANTE) — VERT")
print(f"\nv1061 VIVANTE : {DEST} ({DEST.stat().st_size} o)")
print(f"sha256 : {hashlib.sha256(DEST.read_bytes()).hexdigest()}")
