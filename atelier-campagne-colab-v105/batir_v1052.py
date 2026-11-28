#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE NOTEBOOK v1052 — le v1051 (terrain.9 du serving) PORTÉ AU TERRAIN.10 :
(a) le kit au coffre pointe LE KIT v102 (l'ID et l'empreinte épinglés — le
moteur bivalent aux formats probs/top_logprobs) ;
(b) LA PORTE DE PAROLE de la cellule serving admet les DEUX formats (la clé
« probs » est devenue « top_logprobs » à b12823 — mesuré au bord).
AUCUNE AUTRE cellule touchée (l'épreuve l'asserte contre le v105)."""
import hashlib
import json
import pathlib

V1051 = pathlib.Path("/home/z/my-project/work/Campagne-Colab-v1051-VIVANTE.ipynb")
DEST = pathlib.Path("/home/z/my-project/work/Campagne-Colab-v1052-VIVANTE.ipynb")

ID_KIT_V102 = "1eEBGMND8d9pB2-41ybyXmoNpTdg-pkRz"
SHA_KIT_V102 = "60962d74a06476b5746112d66ac94edfdf5f8b19d475cda30f5efe7e05d431b7"

nb = json.loads(V1051.read_text(encoding="utf-8"))

# ── (a) la cellule des kits : le pin v101 → v102 ──
idx_kits = next(i for i, c in enumerate(nb["cells"])
                if c["cell_type"] == "code" and "NOM_KIT" in "".join(c["source"]))
src_kits = "".join(nb["cells"][idx_kits]["source"])
for vieux, nouveau in (
    ('NOM_KIT = "TRIADE_kit_campagne_poste_v101.zip"', 'NOM_KIT = "TRIADE_kit_campagne_poste_v102.zip"'),
    ('SHA256_KIT = "3b78b544bfe6a6b102666ddba3d8d53af2d04e65b5ffcf963dbd2418d9f4f348"',
     f'SHA256_KIT = "{SHA_KIT_V102}"'),
    ('ID_KIT_DRIVE = "1pa_FCF6GP5jkbCVEWg6BOtgAB2dW3T-Z"    # le /livrables du coffre (l\'Entrée 452)',
     f'ID_KIT_DRIVE = "{ID_KIT_V102}"    # le /livrables du coffre (le v102 — le terrain.10 du 28/11)'),
    ('# CELLULE 3 — LE KIT AU COFFRE, 0 CLIC : le relais embarqué tire le kit poste',
     '# CELLULE 3 — LE KIT AU COFFRE, 0 CLIC (v1052 : le kit v102 — le moteur\n'
     '# bivalent aux formats probs/top_logprobs, le terrain.10 du 28/11) : le\n'
     '# relais embarqué tire le kit poste'),
):
    if vieux not in src_kits:
        raise SystemExit(f"AMENDEMENT-ROMPU (kits) : {vieux[:60]!r}")
    src_kits = src_kits.replace(vieux, nouveau)
src_kits = src_kits.replace("le kit poste v101 TEL QUEL", "le kit poste v102 TEL QUEL")
src_kits = src_kits.replace("l'empreinte recoupée VERT — le kit poste v101 TEL QUEL, byte-byte",
                            "l'empreinte recoupée VERT — le kit poste v102 TEL QUEL, byte-byte")
nb["cells"][idx_kits]["source"] = [src_kits]

# ── (b) la porte de parole : le parse bivalent ──
idx_serv = next(i for i, c in enumerate(nb["cells"])
                if c["cell_type"] == "code" and "asset_de_la_release" in "".join(c["source"]))
src_serv = "".join(nb["cells"][idx_serv]["source"])
VIEUX_PORTE = '''    probs_essai = rep_essai["completion_probabilities"][0]["probs"]'''
NOUVEAU_PORTE = '''    # LE TERRAIN.10 (28/11) : la clé « probs » est devenue « top_logprobs » à
    # b12823 (mesuré au bord au diagnostic du 28/11) — les DEUX formats admis.
    entree_essai = rep_essai["completion_probabilities"][0]
    probs_essai = (entree_essai.get("probs") or entree_essai.get("top_logprobs") or [])'''
if VIEUX_PORTE not in src_serv:
    raise SystemExit("AMENDEMENT-ROMPU (porte) : la ligne des probs introuvable.")
src_serv = src_serv.replace(VIEUX_PORTE, NOUVEAU_PORTE)
nb["cells"][idx_serv]["source"] = [src_serv]

DEST.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ── LES ÉPREUVES ──
compile(src_kits, "cellule-kits-v1052", "exec")
compile(src_serv, "cellule-serving-v1052", "exec")
print("[épreuve 1] les DEUX cellules amendées compilent — VERT")
orig = json.loads(pathlib.Path("/home/z/my-project/work/Campagne-Colab-v105-VIVANTE.ipynb")
                  .read_text(encoding="utf-8"))
nb2 = json.loads(DEST.read_text(encoding="utf-8"))
div = [i for i, (a, b) in enumerate(zip(orig["cells"], nb2["cells"]))
       if "".join(a["source"]) != "".join(b["source"])]
if not {idx_kits, idx_serv} <= set(div) or any(i not in (idx_kits, idx_serv) for i in div):
    raise SystemExit(f"[épreuve 2] INVARIANT-ROMPU : cellules divergentes {div}")
print(f"[épreuve 2] les cellules divergentes = {div} (les kits #{idx_kits} + le serving #{idx_serv}) — VERT")
if ID_KIT_V102 not in src_kits or SHA_KIT_V102 not in src_kits:
    raise SystemExit("[épreuve 3] PIN-ABSENT")
if "top_logprobs" not in src_serv:
    raise SystemExit("[épreuve 3] BIVALENCE-ABSENTE")
print("[épreuve 3] le pin v102 + la bivalence présents — VERT")
print(f"\nv1052 VIVANTE : {DEST} ({DEST.stat().st_size} o)")
print(f"sha256 : {hashlib.sha256(DEST.read_bytes()).hexdigest()}")
