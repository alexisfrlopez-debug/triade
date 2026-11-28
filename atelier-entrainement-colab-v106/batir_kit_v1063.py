#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE KIT D'ENTRAÎNEMENT v1063 — LE REPLI NOMMÉ AU KIT : la pièce
AMENDEMENT-V1064-TERRAIN13.md AJOUTÉE (le troisième refus du 28/11 mesuré —
la v1063 au processus CUDA-vierge, l'époque 1 entière tenue, le monstre
refusé à SA SECONDE VISITE [pas 18] : le persistant AdamW + la fragmentation
mangeant la marge ; le geste : LE REPLI NOMMÉ DU PLAN § 7 — l'exclusion de
ajouter-v3-i26111705-t1 SEUL, la marche 48 pas / 12 pas d'optimiseur
exacts, l'horloge identique) ; le MANIFESTE regagne la pièce (le gate du
bord la recoupera) ; TOUT LE RESTE BYTE-BYTE le kit v1062 (le plan gelé sha
8a719580…, le corpus sha 39614077…, les amendements terrain.11/12, les
recettes, le LISEZMOI, la carte). Le zip : TRIADE_kit_entrainement_v1063.zip
— le nouveau pin du notebook v1064."""
import hashlib
import json
import pathlib
import zipfile

CONTENU = pathlib.Path("/home/z/my-project/work/kit-entrainement-v106/contenu")
DEST = pathlib.Path("/home/z/my-project/work/TRIADE_kit_entrainement_v1063.zip")

ORDRE = [
    "PLAN-ENTRAINEMENT-COLAB-V106.md",
    "AMENDEMENT-V106-TERRAIN11.md",
    "AMENDEMENT-V1063-TERRAIN12.md",
    "AMENDEMENT-V1064-TERRAIN13.md",
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


# ── 1 · l'invariant : les DIX pièces du v1062 BYTE-BYTE ──
vieux = json.loads((CONTENU / "MANIFESTE-KIT-ENTRAINEMENT.json").read_text("utf-8"))
vieux_shas = {p["chemin"]: p["sha256"] for p in vieux["pieces"]}
assert vieux["kit"] == "TRIADE_kit_entrainement_v1062", f"le manifeste lu n'est pas le v1062 : {vieux['kit']}"
for chemin in vieux_shas:
    if not (CONTENU / chemin).exists():
        raise SystemExit(f"PIÈCE-PERDUE : {chemin}")
    if sha256f(CONTENU / chemin) != vieux_shas[chemin]:
        raise SystemExit(f"PIÈCE-DIVERGENTE : {chemin} — le kit v1062 doit demeurer byte-byte")
print(f"[1] les {len(vieux_shas)} pièces du v1062 recoupées BYTE-BYTE — VERT")
PLAN_SHA = vieux_shas["PLAN-ENTRAINEMENT-COLAB-V106.md"]
CORPUS_SHA = vieux_shas["dataset/train.jsonl"]
assert PLAN_SHA.startswith("8a719580"), "le plan doit demeurer 8a719580…"
assert CORPUS_SHA.startswith("39614077"), "le corpus doit demeurer 39614077…"

# ── 2 · la pièce d'amendement présente et lisible ──
amend = CONTENU / "AMENDEMENT-V1064-TERRAIN13.md"
if not amend.exists():
    raise SystemExit("AMENDEMENT-ABSENT")
texte = amend.read_text("utf-8")
for marque in ("TERRAIN.13", "456.00 MiB", "SECONDE VISITE", "ajouter-v3-i26111705-t1",
               "13.58 Gio", "EXCLUSION-NOMMÉE-DIVERGENTE", "39614077", "20261128",
               "48 pas", "12 021", "ADAMW", "expandable_segments",
               "EXEMPLE-LONG-OOM", "REPLI"):
    if marque not in texte:
        raise SystemExit(f"AMENDEMENT-INCOMPLET : {marque} absent")
print(f"[2] l'amendement terrain.13 présent ({amend.stat().st_size} o) — "
      "la mesure, le geste, la preuve, les invariants")

# ── 3 · le manifeste régénéré (les pièces du v1062 + l'amendement terrain.13) ──
pieces = []
for chemin in ORDRE:
    p = CONTENU / chemin
    pieces.append({"chemin": chemin, "sha256": sha256f(p), "octets": p.stat().st_size})
manifeste = {
    "kit": "TRIADE_kit_entrainement_v1063",
    "verts_attendus": vieux["verts_attendus"],
    "sha_plan": PLAN_SHA,
    "amendements": [
        "terrain.11 (AMENDEMENT-V106-TERRAIN11.md — le T4 ne porte pas les "
        "logits du prompt ; la perte sur la réponse seule demeure, conduite à "
        "logits_to_keep + tronçons de 1024)",
        "terrain.12 (AMENDEMENT-V1063-TERRAIN12.md — le chemin fp32 de peft "
        "mesuré au second refus (les 912 MiB à bnb.py:549) et l'allocateur né "
        "sans segments extensibles sur le noyau recyclé ; la cane NOYAU-SALE + "
        "l'autocast fp16 du pas (la voie conçue par peft, les adaptateurs "
        "demeurés fp32) + l'hygiène — la même perte, le même signal, la "
        "preuve au bac en quatre passes)",
        "terrain.13 (AMENDEMENT-V1064-TERRAIN13.md — le monstre nommé refusé à "
        "SA SECONDE VISITE (le pas 18 : le persistant AdamW + la fragmentation "
        "mangeant la marge, le tampon fp16 de 456 MiB la marque de l'autocast "
        "mordu) ; LE REPLI NOMMÉ DU PLAN § 7 : l'exclusion de "
        "ajouter-v3-i26111705-t1 seul — le corpus fichier byte-byte, la marche "
        "48 pas / 12 pas d'optimiseur exacts, l'horloge identique, le "
        "fail-closed EXCLUSION-NOMMÉE-DIVERGENTE)",
    ],
    "pieces": pieces,
}
(CONTENU / "MANIFESTE-KIT-ENTRAINEMENT.json").write_text(
    json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"[3] le manifeste régénéré : {len(pieces)} pièces (le plan byte-byte "
      f"sha {PLAN_SHA[:16]}…, le corpus byte-byte sha {CORPUS_SHA[:16]}…, "
      "les TROIS amendements)")

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
