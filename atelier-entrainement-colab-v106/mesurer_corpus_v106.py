#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA MESURE DES LONGUEURS DU CORPUS v106 AU BAC — la reproduction EXACTE de la
tokenisation de la cellule 5 (l'enveloppe du moteur du kit v102 appliquée au
contrat, la réponse + <|im_end|>), par exemple : prompt, réponse, total.
Sortie : le tableau complet + le pire cas mémoire (logits pleins vs logits_to_keep)."""
import json
import pathlib
import sys

from transformers import AutoTokenizer

# l'enveloppe du moteur — la pièce vivante du kit v102 (byte-byte la 105 close)
sys.path.insert(0, "/home/z/my-project/work/kit-v102")
from moteur_campagne import enveloppe  # noqa: E402

CORPUS = pathlib.Path(
    "/home/z/my-project/work/kit-entrainement-v106/contenu/dataset/train.jsonl")

tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")

verts = []
with open(CORPUS, encoding="utf-8") as f:
    for ligne in f:
        d = json.loads(ligne)
        if d["verdict"] == "VERT":
            verts.append(d)

mesures = []
for d in verts:
    p = tok(enveloppe(d["contrat"]), add_special_tokens=False)["input_ids"]
    c = tok(d["reponse"] + "<|im_end|>", add_special_tokens=False)["input_ids"]
    mesures.append({"triple": d["triple"], "P": len(p), "C": len(c),
                    "L": len(p) + len(c)})

mesures.sort(key=lambda m: -m["L"])

VOCAB = 151936  # Qwen2.5 (mesuré au refus du maître : 7,15 GiB = 12615×151936×4)
GiB = 1024 ** 3
print(f"{'triple':<34} {'P':>6} {'C':>6} {'L':>6}  {'fp32-L':>7} {'fp32-C':>7}")
print("-" * 78)
for m in mesures:
    fp32_L = m["L"] * VOCAB * 4 / GiB          # la copie float32 des logits PLEINS
    fp32_C = (m["C"] + 1) * VOCAB * 4 / GiB    # la copie float32 avec logits_to_keep
    print(f"{m['triple']:<34} {m['P']:>6} {m['C']:>6} {m['L']:>6}  "
          f"{fp32_L:>6.2f}G {fp32_C:>6.2f}G")

totaux = {"P": sum(m["P"] for m in mesures), "C": sum(m["C"] for m in mesures),
          "L": sum(m["L"] for m in mesures)}
print("-" * 78)
print(f"TOTAUX : P={totaux['P']}  C={totaux['C']}  L={totaux['L']}  (n={len(mesures)})")
print(f"max L = {mesures[0]['L']} · max C = {max(m['C'] for m in mesures)} · "
      f"min L = {min(m['L'] for m in mesures)}")

# le budget du T4, dérivé du refus mesuré au bord du maître :
# au moment du .float() : 12,89 GiB occupés dont les logits bf16 pleins (0,27×L GiB)
# → le socle (modèle+bornes+divers) ≈ 12,89 − 3,57 − 1,23(réservé) ≈ 8,1 GiB ;
# la copie fp32 devait tenir dans 14,56 − 12,89 = 1,67 GiB → L_max ≈ 1,67 / 0,000557 ≈ 3000
socle = 8.1
for m in mesures[:5]:
    libre = 14.56 - socle - m["L"] * VOCAB * 2 / GiB - m["L"] * 3584 * 28 * 2 / GiB
    besoin = m["L"] * VOCAB * 4 / GiB
    besoin_k = (m["C"] + 1) * VOCAB * 4 / GiB + (m["C"] + 1) * VOCAB * 2 / GiB
    print(f"[budget] {m['triple']}: pleine={besoin:.2f}G (libre≈{libre:.2f}G) "
          f"→ {'TIENT' if besoin < libre else 'REFUS'} · "
          f"keep={besoin_k:.2f}G → {'TIENT' if besoin_k < libre else 'REFUS'}")

with open("/home/z/my-project/work/mesures-corpus-v106.json", "w", encoding="utf-8") as f:
    json.dump(mesures, f, ensure_ascii=False, indent=1)
print("\nmesures écrites : work/mesures-corpus-v106.json")
