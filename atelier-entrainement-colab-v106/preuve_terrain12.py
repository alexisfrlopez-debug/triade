#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA PREUVE DU TERRAIN.12 AU BAC — l'autocast du pas d'entraînement.

  VOIE A : la cellule 5 du v1062 TEL QUEL (pas d'autocast — peft caste
           l'entrée de chaque couche LoRA au dtype fp32 des adaptateurs :
           le [12 615 × 18 944] fp32 = 911,63 Mio, la classe du refus du
           maître « Tried to allocate 912.00 MiB » à bnb.py:549) ;
  VOIE B : l'amendement (torch.autocast autour du pas — LA VOIE CONÇUE PAR
           PEFT : bnb.py:500 `requires_conversion = not torch.is_autocast_
           enabled()` = False sous autocast CUDA — AUCUN cast, les matmuls
           LoRA au dtype du bord, les adaptateurs DEMEURÉS fp32).

Les passes (chacune en SON processus — la RAM du bac exige la séparation) :
  structure — LA SOURCE : le compteur de _cast_input_dtype (VOIE A : des
           casts au fp32 — la classe des 912 Mio ; le dtype des adaptateurs
           ASSERTÉ fp32 — la cible du cast), le REPLAY du checkpoint
           (l'autocast rejoué à la recomputation — le drapeau lu dedans) ;
  bf16     — le minuscule Qwen2 (adaptateurs fp32, LE RÉGIME DU TERRAIN) :
           la perte et les gradients LoRA VOIE A vs VOIE B — la classe de
           bruit du dtype, la direction du signal inchangée ;
  reel 0/1 — Qwen2.5-0.5B-Instruct bf16 + LoRA r16 α32 aux sept projections
           + gradient checkpointing + LE MÔME PATTERN QUE LA CELLULE 5
           (logits_to_keep + tronçons de 1024 sous checkpoint) : VOIE A vs
           VOIE B sur le VRAI texte du corpus.

L'ACCEPTATION (le précédent de l'Entrée 462 : « l'écart relatif ~2,5e-02
est L'ARRONDI DU MATMUL — la classe de bruit du dtype même, la direction du
signal inchangée ») : |Δperte|/perte ≤ 5e-2 · écart gradients relatif ≤
5e-2 · cosinus ≥ 0,999.

Usage : preuve_terrain12.py <passe> <exemple>"""
import json
import sys

import torch
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
from torch.utils.checkpoint import checkpoint
from transformers import AutoModelForCausalLM, AutoTokenizer, Qwen2Config, Qwen2ForCausalLM

PASSE, EXEMPLE = sys.argv[1], int(sys.argv[2])
TRONCON = 1024
FICHIER = f"/home/z/my-project/work/preuve-terrain12-{PASSE}-{EXEMPLE}.json"

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
LE_COURT = next(d for d in corpus if d["triple"] == "ajouter-v4-i26111715-t0")

# ── l'instrument : le compteur de _cast_input_dtype (la source de peft) ──
import peft.tuners.lora.layer as peft_layer  # noqa: E402

CASTS = {"appels": 0, "dtypes": set(), "rec_compute": []}
_vieux_cast = peft_layer.Linear._cast_input_dtype


def cast_compte(self, x, dtype):
    CASTS["appels"] += 1
    CASTS["dtypes"].add(str(dtype))
    return _vieux_cast(self, x, dtype)


peft_layer.Linear._cast_input_dtype = cast_compte


def ce_troncon(chunk, tgts):
    assert chunk.dtype == torch.float32 or chunk.dtype == torch.bfloat16
    return F.cross_entropy(chunk.float(), tgts, reduction="sum")   # LE .float() EXPLICITE — la CE demeure fp32


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
    if EXEMPLE == 0:
        ex = {"contrat": UN_VERT["contrat"][:150],
              "reponse": UN_VERT["reponse"][:800] + "\n",
              "marque": "le véritable extrait du monstre (vocab réel 151 936)"}
    else:
        ex = {"contrat": LE_COURT["contrat"][:600],
              "reponse": LE_COURT["reponse"],
              "marque": "l'exemple le plus court du corpus (C=52, vocab réel)"}
else:
    dt = torch.bfloat16 if PASSE in ("bf16", "structure") else torch.float32
    torch.manual_seed(20261128)
    torch.set_default_dtype(dt)
    cfg = Qwen2Config(vocab_size=16384, hidden_size=64, intermediate_size=176,
                      num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=2, tie_word_embeddings=False)
    model = Qwen2ForCausalLM(cfg)
    torch.set_default_dtype(torch.float32)
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    titre = f"Qwen2 minuscule aléatoire (dtype {dt}) — le même chemin que le 7B"
    ex = {"contrat": UN_VERT["contrat"][:800],
          "reponse": UN_VERT["reponse"][:600] + "\n",
          "marque": "le véritable extrait du corpus"}
if PASSE in ("bf16", "structure"):   # les SEPT projections, le régime exact du bord
    cfgl = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.0, bias="none",
                      task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                      "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, cfgl)
model.train()
model.gradient_checkpointing_enable()
model.enable_input_require_grads()
model.config.use_cache = False

# ── les adaptateurs : LE RÉGIME DU TERRAIN ASSERTÉ ──
dtypes_adaptateurs = {str(p.dtype) for n, p in model.named_parameters()
                      if "lora_" in n and p.requires_grad}
print(f"[preuve {PASSE} #{EXEMPLE}] le modèle : {titre}")
print(f"[preuve {PASSE} #{EXEMPLE}] l'exemple : {ex['marque']} · enveloppe du moteur")
print(f"[preuve {PASSE} #{EXEMPLE}] le dtype des adaptateurs (la cible du cast "
      f"de la VOIE A) : {sorted(dtypes_adaptateurs)}")

# ── la tokenisation de la cellule 5 (l'enveloppe, la réponse + <|im_end|>) ──
torch.manual_seed(20261128)
p = tok(enveloppe(ex["contrat"]), add_special_tokens=False)["input_ids"]
c = tok(ex["reponse"] + "<|im_end|>", add_special_tokens=False)["input_ids"]
if PASSE != "reel":
    p = [i % 16384 for i in p]
    c = [i % 16384 for i in c]
P, C, L, K = len(p), len(c), len(p) + len(c), len(c) + 1
V = model.get_output_embeddings().weight.shape[0]
print(f"[preuve {PASSE} #{EXEMPLE}] P={P} C={C} L={L} K={K} "
      f"({(C + TRONCON - 1) // TRONCON} tronçon(s))")


def un_pas(autocast):
    """LE PAS DE LA CELLULE 5 — VOIE A (v1062, nu) vs VOIE B (v1063, autocast)."""
    model.zero_grad(set_to_none=True)
    t = torch.tensor([p + c])
    cibles = torch.tensor(c)
    if autocast:
        with torch.autocast("cpu", dtype=torch.bfloat16):
            out = model(input_ids=t, logits_to_keep=K)
            lg = out.logits[0, :-1, :]
            somme = torch.zeros(())
            for j in range(0, C, TRONCON):
                somme = somme + checkpoint(ce_troncon, lg[j:j + TRONCON],
                                           cibles[j:j + TRONCON], use_reentrant=False)
            perte = somme / C
    else:
        out = model(input_ids=t, logits_to_keep=K)
        lg = out.logits[0, :-1, :]
        somme = torch.zeros(())
        for j in range(0, C, TRONCON):
            somme = somme + checkpoint(ce_troncon, lg[j:j + TRONCON],
                                       cibles[j:j + TRONCON], use_reentrant=False)
        perte = somme / C
    perte.backward()   # HORS du contexte — le checkpoint rejoue l'autocast lui-même
    grads = {n: par.grad.detach().clone() for n, par in model.named_parameters()
             if par.grad is not None}
    return float(perte.detach()), grads


resultat = {"passe": PASSE, "exemple": EXEMPLE, "modele": titre, "marque": ex["marque"],
            "P": P, "C": C, "L": L, "K": K, "V": V,
            "adaptateurs_dtypes": sorted(dtypes_adaptateurs)}

if PASSE == "structure":
    # ── (a) VOIE A : les casts au fp32 — la classe des 912 Mio du refus ──
    CASTS["appels"], CASTS["dtypes"] = 0, set()
    perteA, gA = un_pas(autocast=False)
    castsA, dtypesA = CASTS["appels"], sorted(CASTS["dtypes"])
    print(f"  VOIE A : {castsA} casts d'entrée au {dtypesA} — la classe du refus "
          f"(le [12 615 × 18 944] fp32 = 911,63 Mio au bord)")

    # ── (b) VOIE B : le matmul au dtype du bord — les casts demeurent au bac
    #         (layer.py caste sans garde ; la garde vit à bnb.py:500 — LE BORD),
    #         le SIGNAL du matmul change de classe, le drapeau du replay lu ──
    CASTS["appels"], CASTS["dtypes"] = 0, set()
    perteB, gB = un_pas(autocast=True)
    castsB, dtypesB = CASTS["appels"], sorted(CASTS["dtypes"])

    # ── (c) LE REPLAY : l'autocast rejoué à la recomputation du checkpoint ──
    drapeaux = []

    def sonde(x):
        drapeaux.append(("fwd" if not drapeaux else "rec", torch.is_autocast_enabled("cpu")))
        return x

    vieux_lin = torch.nn.Linear.forward

    def lin_sonde(self, x):
        return vieux_lin(self, x)

    # la sonde directe : le drapeau lu DANS le fn checkpointé, au forward puis à la recomputation
    drapeaux.clear()
    lin_probe = torch.nn.Linear(64, 64)

    def fn_sonde(v):
        drapeaux.append(torch.is_autocast_enabled("cpu"))
        return lin_probe(v).pow(2).mean()

    v = torch.randn(4, 64, requires_grad=True)
    with torch.autocast("cpu", dtype=torch.bfloat16):
        s = checkpoint(fn_sonde, v, use_reentrant=False)
    s.backward()
    print(f"  LE REPLAY : le drapeau autocast au forward {drapeaux[0]}, "
          f"à la recomputation {drapeaux[1]} — {'REJOUÉ' if all(drapeaux) else 'PERDU'}")

    ok = (castsA > 0 and "torch.float32" in dtypesA and all(drapeaux)
          and set(gA) == set(gB))
    resultat.update({"casts_voieA": castsA, "dtypes_voieA": dtypesA,
                     "perteA": perteA, "perteB": perteB,
                     "replay_autocast": {"forward": drapeaux[0], "recompute": drapeaux[1]},
                     "ok": ok})
    json.dump(resultat, open(FICHIER, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    if not ok:
        raise SystemExit("PREUVE-ROUGE (structure)")
    print(f"[preuve structure #{EXEMPLE}] VERT — la source entendue : VOIE A "
          f"caste au fp32 ({castsA} casts), le checkpoint rejoue l'autocast")
    raise SystemExit(0)

# ── LES PASSES SIGNAL : la perte + les gradients LoRA, VOIE A vs VOIE B ──
perteA, gA = un_pas(autocast=False)
perteB, gB = un_pas(autocast=True)
ecart_rel = abs(perteA - perteB) / max(abs(perteA), 1e-9)

# les gradients : l'écart relatif + LE COSINUS (la direction du signal)
num = denA = denB = 0.0
rel_max = 0.0
for n in gA:
    a, b = gA[n].flatten(), gB[n].flatten()
    num += float(torch.dot(a, b))
    denA += float(torch.dot(a, a))
    denB += float(torch.dot(b, b))
    rel = (a - b).abs().max().item() / max(a.abs().max().item(), 1e-12)
    rel_max = max(rel_max, rel)
cosinus = num / max((denA * denB) ** 0.5, 1e-30)

print(f"  perte A (v1062, nu)      = {perteA:.10f}")
print(f"  perte B (v1063, autocast)= {perteB:.10f}")
print(f"  |Δperte|/perte = {ecart_rel:.3e} · écart grads relatif max = {rel_max:.3e} "
      f"· cosinus = {cosinus:.8f}")

ok = ecart_rel <= 5e-2 and rel_max <= 5e-2 and cosinus >= 0.999 and set(gA) == set(gB)
resultat.update({"perteA": perteA, "perteB": perteB, "ecart_perte_rel": ecart_rel,
                 "ecart_grads_rel_max": rel_max, "cosinus_grads": cosinus,
                 "nb_params_grad": len(gA), "ok": ok})
json.dump(resultat, open(FICHIER, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
if not ok:
    raise SystemExit(f"PREUVE-ROUGE ({PASSE} #{EXEMPLE})")
print(f"[preuve {PASSE} #{EXEMPLE}] VERT — la classe de bruit du dtype, "
      "la direction du signal inchangée")
