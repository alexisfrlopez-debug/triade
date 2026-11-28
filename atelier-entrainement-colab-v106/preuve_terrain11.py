#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA PREUVE DU TERRAIN.11 AU BAC — l'équivalence de la perte.

  VOIE A : la cellule 5 du v106 TEL QUEL (labels masqués à -100, la perte
           pleine du modèle — ForCausalLMLoss, le « mean » aux non-ignorés) ;
  VOIE B : l'amendement (logits_to_keep = C+1 — le découpage AVANT le
           lm_head, constaté à la source slice_logits_to_keep — puis CE par
           tronçons de 1024 sous checkpoint, la somme divisée par C).

L'IDENTITÉ EST PAR POSITION : elle ne dépend NI des poids, NI de la longueur,
NI de la largeur du vocabulaire — c'est pourquoi le minuscule Qwen2 décide
(le même chemin de perte que le 7B du bord), et le 0.5B réel confirme.

Les passes (chacune en SON processus — la RAM du bac, 4 Go, exige la
séparation ; la VOIE A elle-même fait sauter le bac au-delà de ~L 1 100 au
vocabulaire réel — LA DÉMONSTRATION DU TERRAIN MÊME) :
  fp32 0 — minuscule Qwen2, VOCAB RÉEL 151 936, la vraie enveloppe du moteur
           sur le VRAI contrat/réponse du corpus, UN tronçon — la perte et
           les gradients au ulp du fp32 ;
  fp32 1 — minuscule Qwen2, vocab réduit 16 384 (la largeur ne change rien à
           l'alignement — le premier exemple porte le vocabulaire réel), le
           même extrait ×5 — DEUX tronçons, le réordonnancement des sommes
           NOMMÉ au ulp du fp32 ;
  bf16 0/1 — le même à l'arrondi du dtype du bord près ;
  reel 0 — Qwen2.5-0.5B-Instruct PRÉ-ENTRAÎNÉ + le MÊME LoRA (r16 α32, les
           sept projections), exemples courts (la RAM du bac).

Usage : preuve_terrain11.py <passe> <exemple>"""
import json
import sys

import torch
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
from torch.utils.checkpoint import checkpoint
from transformers import (AutoModelForCausalLM, AutoTokenizer, Qwen2Config,
                          Qwen2ForCausalLM)

PASSE, EXEMPLE = sys.argv[1], int(sys.argv[2])
TRONCON = 1024
FICHIER = f"/home/z/my-project/work/preuve-terrain11-{PASSE}-{EXEMPLE}.json"

# la VRAIE enveloppe du moteur + le VRAI corpus
sys.path.insert(0, "/home/z/my-project/work/kit-v102")
from moteur_campagne import enveloppe  # noqa: E402

corpus = []
with open("/home/z/my-project/work/kit-entrainement-v106/contenu/dataset/train.jsonl",
          encoding="utf-8") as f:
    for ligne in f:
        d = json.loads(ligne)
        if d["verdict"] == "VERT":
            corpus.append(d)
UN_VERT = corpus[0]   # ajouter-v3-i26111705-t1 — le monstre du refus du maître

EXTRAITS = {
    0: {"contrat": UN_VERT["contrat"][:1800],
        "reponse": UN_VERT["reponse"][:1500] + "\n",
        "marque": "le véritable extrait du corpus (UN tronçon)", "vocab": 151936},
    1: {"contrat": UN_VERT["contrat"][:1800],
        "reponse": (UN_VERT["reponse"][:1500] + "\n") * 5,
        "marque": "l'extrait ×5 (DEUX tronçons — le réordonnancement)", "vocab": 16384},
}
ex = EXTRAITS[EXEMPLE]

# ── le modèle de la passe ──
if PASSE == "reel":
    torch.manual_seed(20261128)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2.5-0.5B-Instruct", dtype=torch.bfloat16, low_cpu_mem_usage=True)
    cfgl = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.0, bias="none",
                      task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                      "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, cfgl)
    titre = "Qwen2.5-0.5B-Instruct PRÉ-ENTRAÎNÉ + LoRA r16 α32 (le vrai chemin)"
    # les exemples courts pour la RAM du bac
    ex = {"contrat": UN_VERT["contrat"][:150],
          "reponse": UN_VERT["reponse"][:800] + "\n",
          "marque": "le véritable extrait court (vocab réel 151 936)", "vocab": 151936}
    if EXEMPLE == 1:
        # l'exemple le plus court du corpus (ajouter-v4-i26111715-t0, C=52
        # — le plus court mesuré au tableau des longueurs)
        le_court = next(d for d in corpus if d["triple"] == "ajouter-v4-i26111715-t0")
        ex = {"contrat": le_court["contrat"][:600],
              "reponse": le_court["reponse"],
              "marque": "l'exemple le plus court du corpus (C=52, vocab réel)",
              "vocab": 151936}
else:
    dt = torch.float32 if PASSE == "fp32" else torch.bfloat16
    torch.manual_seed(20261128)
    torch.set_default_dtype(dt)
    cfg = Qwen2Config(vocab_size=ex["vocab"], hidden_size=64, intermediate_size=176,
                      num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=2, tie_word_embeddings=False)
    model = Qwen2ForCausalLM(cfg)
    torch.set_default_dtype(torch.float32)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    titre = (f"Qwen2 minuscule aléatoire (vocab {ex['vocab']}, dtype {dt}) — "
             "le même chemin de perte que le 7B")
model.train()
V = model.get_output_embeddings().weight.shape[0]
assert V == ex["vocab"] or PASSE == "reel", (V, ex["vocab"])
print(f"[preuve {PASSE} #{EXEMPLE}] le modèle : {titre}")
print(f"[preuve {PASSE} #{EXEMPLE}] l'exemple : {ex['marque']} · enveloppe du moteur")

# ── la tokenisation de la cellule 5 (l'enveloppe, la réponse + <|im_end|>) ──
torch.manual_seed(20261128)
p = tok(enveloppe(ex["contrat"]), add_special_tokens=False)["input_ids"]
c = tok(ex["reponse"] + "<|im_end|>", add_special_tokens=False)["input_ids"]
if PASSE in ("fp32", "bf16") and ex["vocab"] < 151936:
    # le minuscule au vocabulaire réduit : les ids ramenés DANS la plage (la
    # valeur des ids ne change rien à l'identité — elle est par position)
    p = [i % ex["vocab"] for i in p]
    c = [i % ex["vocab"] for i in c]
P, C, L = len(p), len(c), len(p) + len(c)
K = C + 1
print(f"[preuve {PASSE} #{EXEMPLE}] P={P} C={C} L={L} K={K} "
      f"({(C + TRONCON - 1) // TRONCON} tronçon(s) en voie B)")

# VOIE A — la cellule 5 du v106 TEL QUEL
t = torch.tensor([p + c])
labels = torch.tensor([[-100] * P + c])
outA = model(input_ids=t, labels=labels)
assert outA.logits.shape == (1, L, V)
perteA = outA.loss

# VOIE B — l'amendement terrain.11
outB = model(input_ids=t, logits_to_keep=K)
assert outB.logits.shape == (1, K, V), (outB.logits.shape, K)
lg = outB.logits[0, :-1, :]
assert lg.shape[0] == C
cibles = torch.tensor(c)


def ce_troncon(chunk, tgts):
    return F.cross_entropy(chunk.float(), tgts, reduction="sum")


somme = torch.zeros(())
for j in range(0, C, TRONCON):
    somme = somme + checkpoint(ce_troncon, lg[j:j + TRONCON],
                               cibles[j:j + TRONCON], use_reentrant=False)
perteB = somme / C

# les gradients (le signal d'entraînement)
model.zero_grad(set_to_none=True)
perteA.backward()
gA = {n: par.grad.detach().clone() for n, par in model.named_parameters()
      if par.grad is not None}
model.zero_grad(set_to_none=True)
perteB.backward()
gB = {n: par.grad.detach().clone() for n, par in model.named_parameters()
      if par.grad is not None}
memes = set(gA) == set(gB)
ecart_g = max((gA[n] - gB[n]).abs().max().item() for n in gA)
norme_g = max(gA[n].abs().max().item() for n in gA)

ecart = abs(float(perteA.detach()) - float(perteB.detach()))
print(f"  perte A (labels pleins)  = {float(perteA.detach()):.10f}")
print(f"  perte B (logits_to_keep) = {float(perteB.detach()):.10f}")
print(f"  écart = {ecart:.3e} · grads : {len(gA)} clefs identiques={memes} · "
      f"écart max = {ecart_g:.3e} (norme max {norme_g:.3e}, relatif "
      f"{ecart_g / max(norme_g, 1e-9):.2e})")

bornes = {"fp32": (1e-5, 1e-4), "bf16": (1e-1, 1e-1), "reel": (1e-1, 1e-1)}
seuil_p, seuil_g = bornes[PASSE]
ok = ecart < seuil_p and ecart_g < seuil_g and memes
json.dump({"passe": PASSE, "exemple": EXEMPLE, "modele": titre,
           "marque": ex["marque"], "P": P, "C": C, "L": L, "K": K, "V": V,
           "troncons": (C + TRONCON - 1) // TRONCON,
           "perteA": float(perteA.detach()), "perteB": float(perteB.detach()),
           "ecart_perte": ecart, "ecart_grads": ecart_g, "norme_grads": norme_g,
           "grads_identiques": memes, "nb_params_grad": len(gA), "ok": ok},
          open(FICHIER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if not ok:
    raise SystemExit(f"PREUVE-ROUGE ({PASSE} #{EXEMPLE})")
print(f"[preuve {PASSE} #{EXEMPLE}] VERT")
