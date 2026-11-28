#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE KIT D'ENTRAÎNEMENT v1061 — L'AMENDEMENT TERRAIN.11 AU KIT : la pièce
AMENDEMENT-V106-TERRAIN11.md AJOUTÉE (le T4 ne porte pas les logits du
prompt — la mesure du run du maître, le geste logits_to_keep + tronçons, la
preuve d'équivalence au bac en six passes) ; le MANIFESTE regagne la pièce
(le gate du bord la recoupera) ; TOUT LE RESTE BYTE-BYTE le kit v106 (le
plan gelé sha 8a719580…, le corpus, les recettes, le LISEZMOI, la carte).
Le zip : TRIADE_kit_entrainement_v1061.zip — le nouveau pin du notebook."""
import hashlib
import json
import pathlib
import zipfile

CONTENU = pathlib.Path("/home/z/my-project/work/kit-entrainement-v106/contenu")
DEST = pathlib.Path("/home/z/my-project/work/TRIADE_kit_entrainement_v1061.zip")

ORDRE = [
    "PLAN-ENTRAINEMENT-COLAB-V106.md",
    "AMENDEMENT-V106-TERRAIN11.md",
    "LISEZMOI-KIT-ENTRAINEMENT.txt",
    "RECETTES-GYM.md",
    "dataset/train.jsonl",
    "dataset/dev.jsonl",
    "dataset/test.jsonl",
    "dataset/DATASET-CARD.json",
    "dataset/MANIFESTE.json",
]


def sha256f(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# ── 1 · l'invariant : les pièces du v106 BYTE-BYTE ──
vieux = json.loads((CONTENU / "MANIFESTE-KIT-ENTRAINEMENT.json").read_text("utf-8"))
vieux_shas = {p["chemin"]: p["sha256"] for p in vieux["pieces"]}
for chemin in vieux_shas:
    if not (CONTENU / chemin).exists():
        raise SystemExit(f"PIÈCE-PERDUE : {chemin}")
    if sha256f(CONTENU / chemin) != vieux_shas[chemin]:
        raise SystemExit(f"PIÈCE-DIVERGENTE : {chemin} — le kit v106 doit demeurer byte-byte")
print(f"[1] les {len(vieux_shas)} pièces du v106 recoupées BYTE-BYTE — VERT")
PLAN_SHA = vieux_shas["PLAN-ENTRAINEMENT-COLAB-V106.md"]

# ── 2 · la pièce d'amendement présente et lisible ──
amend = CONTENU / "AMENDEMENT-V106-TERRAIN11.md"
if not amend.exists():
    raise SystemExit("AMENDEMENT-ABSENT")
texte = amend.read_text("utf-8")
for marque in ("TERRAIN.11", "logits_to_keep", "12 615", "7,15",
               "EXEMPLE-LONG-OOM", "39614077", "20261128"):
    if marque not in texte:
        raise SystemExit(f"AMENDEMENT-INCOMPLET : {marque} absent")
print(f"[2] l'amendement terrain.11 présent ({amend.stat().st_size} o) — "
      "la mesure, le geste, la preuve, les invariants")

# ── 3 · le manifeste régénéré (les pièces du v106 + l'amendement) ──
pieces = []
for chemin in ORDRE:
    p = CONTENU / chemin
    pieces.append({"chemin": chemin, "sha256": sha256f(p), "octets": p.stat().st_size})
manifeste = {
    "kit": "TRIADE_kit_entrainement_v1061",
    "verts_attendus": vieux["verts_attendus"],
    "sha_plan": PLAN_SHA,
    "amendements": ["terrain.11 (AMENDEMENT-V106-TERRAIN11.md — le T4 ne porte "
                    "pas les logits du prompt ; la perte sur la réponse seule "
                    "demeure, conduite à logits_to_keep + tronçons de 1024)"],
    "pieces": pieces,
}
( CONTENU / "MANIFESTE-KIT-ENTRAINEMENT.json").write_text(
    json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"[3] le manifeste régénéré : {len(pieces)} pièces (le plan byte-byte "
      f"sha {PLAN_SHA[:16]}…, l'amendement AJOUTÉ)")

# ── 4 · le zip ──
if DEST.exists():
    DEST.unlink()
with zipfile.ZipFile(DEST, "w", compresslevel=9) as z:
    for chemin in ORDRE + ["MANIFESTE-KIT-ENTRAINEMENT.json"]:
        z.write(CONTENU / chemin, chemin)
sha = sha256f(DEST)
print(f"[4] KIT : {DEST.name} ({DEST.stat().st_size} o)")
print(f"    sha256 : {sha}")

# ── 5 · l'épreuve du zip (le gate du bord rejoué au bac) ──
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(DEST) as z:
        z.extractall(tmp)
    m = json.loads(pathlib.Path(tmp, "MANIFESTE-KIT-ENTRAINEMENT.json").read_text("utf-8"))
    for piece in m["pieces"]:
        h = sha256f(pathlib.Path(tmp, piece["chemin"]))
        if h != piece["sha256"]:
            raise SystemExit(f"ZIP-ROUGE : {piece['chemin']}")
    if m["verts_attendus"] != 17:
        raise SystemExit("COMPTE-VERTS-ROMPU")
print(f"[5] le gate rejoué au bac : {len(m['pieces'])} pièces VERTES, "
      "17 verts attendus — le kit est PRÊT au pin")
