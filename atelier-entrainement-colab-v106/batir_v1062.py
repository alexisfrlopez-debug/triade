#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE NOTEBOOK v1062 — LE TERRAIN.11 CORRIGÉ À LA CELLULE 5 : le run du
maître du 28/11 refusa au premier exemple (EXEMPLE-LONG-OOM, 12 615 jetons —
« Tried to allocate 7.15 GiB » = 12 615 × 151 936 × 4 : LA COPIE FP32 DES
LOGITS PLEINS que fait ForCausalLMLoss). Le seuil du T4 (~4 500 jetons) est
SOUS la médiane du corpus (4 527) — l'exclusion du plan eût vidé le corpus.

L'AMENDEMENT v1062 (trois cellules, le reste DEMEURE BYTE-BYTE le v1061) :
  · la cellule 5 (LE SFT) : la perte demandée à logits_to_keep = C+1 (les
    logits du prompt JAMAIS alloués — le découpage AVANT le lm_head) puis
    conduite par tronçons de 1024 sous checkpoint — LA MÊME MATHÉMATIQUE
    (la preuve au bac en six passes : la perte au ulp du fp32, EXACTEMENT
    égale au vrai modèle, le même signal) ;
  · la cellule 3 (LES KITS) : le pin du kit v1061 (l'amendement
    AMENDEMENT-V106-TERRAIN11.md y vit, le plan et le corpus byte-byte) ;
  · la cellule titre : la version nommée."""
import hashlib
import json
import pathlib

V1061 = pathlib.Path("/home/z/my-project/work/kit-entrainement-v106/Entrainement-Colab-v1061-VIVANTE.ipynb")
DEST = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1062-VIVANTE.ipynb")

PIN_KIT = {
    "nom": "TRIADE_kit_entrainement_v1061.zip",
    "sha256": "f5a2382b0204d9872a1f44695bfa1f83c9b79adc53754102924c61e144a64b1f",
    "id_drive": "1oFnEsGy6JV_JRw2h6MugHurxfeNCuH3T",
}

nb = json.loads(V1061.read_text(encoding="utf-8"))


def remplacer(src, vieux, nouveau, marque):
    if vieux not in src:
        raise SystemExit(f"AMENDEMENT-ROMPU [{marque}] : {vieux[:60]!r}")
    return src.replace(vieux, nouveau)


# ── la cellule titre (0) ──
src0 = "".join(nb["cells"][0]["source"])
src0 = remplacer(src0,
    "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v106)",
    "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v1062)", "titre-1")
src0 = remplacer(src0,
    "**Le T4 est la voie conseillée** (le plan gelé du kit est LA LOI du run).",
    "**Le T4 est la voie conseillée** (le plan gelé du kit est LA LOI du run ; "
    "l'amendement terrain.11 du kit — la perte à `logits_to_keep`, les logits "
    "du prompt jamais alloués — soigne le refus mémoire mesuré au run du 28/11, "
    "le plan et le corpus demeurent byte-byte).", "titre-2")
nb["cells"][0]["source"] = [src0]

# ── la cellule des kits (6) : le pin v1061 ──
src6 = "".join(nb["cells"][6]["source"])
src6 = remplacer(src6,
    """    {   # le corpus + le plan gelé de l'entraînement
        "nom": "TRIADE_kit_entrainement_v106.zip",
        "sha256": "07edabb05b051abcc0c4eeffbbdb6ca83158bacdfe086db02eff6dadc0da40ea",
        "id_drive": "1U93jzav1XntOWp0wNFlUnpLwx5the1uE",
        "dest": pathlib.Path("/content/kit-entrainement"),
    },""",
    """    {   # le corpus + le plan gelé + L'AMENDEMENT TERRAIN.11 de l'entraînement
        "nom": "TRIADE_kit_entrainement_v1061.zip",
        "sha256": "f5a2382b0204d9872a1f44695bfa1f83c9b79adc53754102924c61e144a64b1f",
        "id_drive": "1oFnEsGy6JV_JRw2h6MugHurxfeNCuH3T",
        "dest": pathlib.Path("/content/kit-entrainement"),
    },""", "pin-kit")
nb["cells"][6]["source"] = [src6]

# ── la cellule 5 (10) : l'amendement terrain.11 ──
src10 = "".join(nb["cells"][10]["source"])
src10 = remplacer(src10,
    """# fin) ; EXEMPLE-TROP-LONG et EXEMPLE-LONG-OOM les refus nommés.
import json
import pathlib
import time

import torch
from peft import LoraConfig, get_peft_model
from transformers import (AutoModelForCausalLM, BitsAndBytesConfig,
                          get_cosine_schedule_with_warmup)""",
    """# fin) ; EXEMPLE-TROP-LONG et EXEMPLE-LONG-OOM les refus nommés.
# L'AMENDEMENT TERRAIN.11 (AMENDEMENT-V106-TERRAIN11.md du kit) : la perte
# demandée à logits_to_keep (les logits du prompt JAMAIS alloués — le T4 ne
# les porte pas, mesuré au refus du 28/11 : 7,15 Gio pour la copie fp32 des
# logits pleins) puis conduite par tronçons de 1024 rangées — LA MÊME
# MATHÉMATIQUE (la preuve au labo : la même perte au ulp du fp32, le même
# signal), le plan gelé demeure LA LOI.
import json
import os
import pathlib
import time

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import torch
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
from torch.utils.checkpoint import checkpoint
from transformers import (AutoModelForCausalLM, BitsAndBytesConfig,
                          get_cosine_schedule_with_warmup)""", "entête-sft")

src10 = remplacer(src10,
    """print(f"[sft] LA MARCHE : {EPOQUES} époques × {len(exemples)} exemples = {n_pas} pas "
      f"({opt_pas} pas d'optimiseur) — le journal vit en direct ci-dessous.")
model.train()""",
    """print(f"[sft] LA MARCHE : {EPOQUES} époques × {len(exemples)} exemples = {n_pas} pas "
      f"({opt_pas} pas d'optimiseur) — le journal vit en direct ci-dessous.")

# ── l'amendement terrain.11 : la CE par tronçons (la mémoire du T4) ──
TRONCON = 1024


def ce_troncon(logits_bf16, cibles):
    return F.cross_entropy(logits_bf16.float(), cibles, reduction="sum")


model.train()""", "tronçon")

src10 = remplacer(src10,
    """            ids = e["p"] + e["c"]
            t = torch.tensor([ids], device="cuda")
            labels = torch.tensor([[-100] * len(e["p"]) + e["c"]], device="cuda")
            out = model(input_ids=t, labels=labels)
            (out.loss / ACCUM).backward()
            courbe.append({"pas": len(courbe) + 1, "epoque": epo + 1,
                           "triple": e["triple"], "perte": round(float(out.loss), 5)})""",
    """            ids = e["p"] + e["c"]
            t = torch.tensor([ids], device="cuda")
            cibles = torch.tensor(e["c"], device="cuda")
            out = model(input_ids=t, logits_to_keep=len(e["c"]) + 1)
            lg = out.logits[0, :-1, :]   # [C, V] — prédit exactement les cibles
            somme = torch.zeros((), device="cuda")
            for j in range(0, lg.shape[0], TRONCON):
                somme = somme + checkpoint(ce_troncon, lg[j:j + TRONCON],
                                           cibles[j:j + TRONCON], use_reentrant=False)
            perte = somme / len(e["c"])   # le « mean » aux non-ignorés (la même perte)
            (perte / ACCUM).backward()
            val = float(perte)
            courbe.append({"pas": len(courbe) + 1, "epoque": epo + 1,
                           "triple": e["triple"], "perte": round(val, 5)})""", "boucle")

src10 = remplacer(src10,
    """                print(f"[sft] époque {epo + 1}/{EPOQUES} · pas {len(courbe)}/{n_pas} · "
                      f"perte {out.loss:.4f} · {time.time() - t0:.0f} s", flush=True)""",
    """                print(f"[sft] époque {epo + 1}/{EPOQUES} · pas {len(courbe)}/{n_pas} · "
                      f"perte {val:.4f} · {time.time() - t0:.0f} s", flush=True)""", "journal")

src10 = remplacer(src10,
    """                     "max_len": MAX_LEN, "troncature": "AUCUNE"},""",
    """                     "max_len": MAX_LEN, "troncature": "AUCUNE"},
    "amendement": {"terrain": "terrain.11", "perte": "logits_to_keep + CE par "
                   "tronçons de 1024 — la réponse seule, LA MÊME MATHÉMATIQUE "
                   "(la preuve au bac : la perte au ulp du fp32, EXACTEMENT "
                   "égale au vrai modèle, le même signal)"},""", "registre")
nb["cells"][10]["source"] = [src10]

DEST.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ══ LES ÉPREUVES ══
print("══ LES ÉPREUVES DU v1062 ══")
compile(src10, "cellule-sft-v1062", "exec")
print("[épreuve 1] la cellule 5 v1062 compile — VERT")

orig = json.loads(V1061.read_text(encoding="utf-8"))
nb2 = json.loads(DEST.read_text(encoding="utf-8"))
div = [i for i, (a, b) in enumerate(zip(orig["cells"], nb2["cells"]))
       if "".join(a["source"]) != "".join(b["source"])]
if div != [0, 6, 10]:
    raise SystemExit(f"[épreuve 2] INVARIANT-ROMPU : cellules divergentes {div} ≠ [0, 6, 10]")
print("[épreuve 2] les SEULES cellules touchées = le titre (0), les kits (6), "
      "le SFT (10) — VERT")

for marque in ("logits_to_keep=len(e[\"c\"]) + 1", "TRONCON = 1024", "ce_troncon",
               "use_reentrant=False", "expandable_segments:True",
               "EXEMPLE-LONG-OOM", "EXEMPLE-TROP-LONG", "MAX_LEN = 13000",
               "SEED = 20261128", "EPOQUES, ACCUM, LR = 3, 4, 1.5e-5",
               "somme / len(e[\"c\"])", "amendement"):
    if marque not in src10:
        raise SystemExit(f"[épreuve 3] MARQUE-ABSENTE : {marque}")
for mort in ("labels=labels", "out.loss", "labels = torch.tensor"):
    if mort in src10:
        raise SystemExit(f"[épreuve 3] LE VIEUX CHEMIN VIT : {mort}")
print("[épreuve 3] le chemin neuf présent (logits_to_keep, tronçons, la garde "
      "mémoire), le vieux chemin MORT (labels pleins, out.loss) — VERT")

if (PIN_KIT["sha256"] not in src6 or PIN_KIT["id_drive"] not in src6
        or "poste_v102" not in src6 or "60962d74" not in src6):
    raise SystemExit("[épreuve 4] PIN-ROMPU")
print("[épreuve 4] le pin du kit v1061 (f5a2382b…) + le pin poste v102 "
      "(60962d74…) intacts — VERT")

tout = "\n".join("".join(c["source"]) for c in nb2["cells"] if c["cell_type"] == "code")
if "GOCSPX" not in tout:
    raise SystemExit("[épreuve 5] IDENTIFIANTS-PERDUS (la vivante doit les porter)")
print("[épreuve 5] les identifiants du relais présents (la copie VIVANTE) — VERT")

nbaveugle = json.loads(DEST.read_text(encoding="utf-8"))
print(f"\nv1062 VIVANTE : {DEST} ({DEST.stat().st_size} o)")
print(f"sha256 : {hashlib.sha256(DEST.read_bytes()).hexdigest()}")
