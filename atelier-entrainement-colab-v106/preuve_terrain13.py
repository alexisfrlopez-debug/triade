#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA PREUVE AU BAC DU TERRAIN.13 — LE REPLI NOMMÉ DU PLAN § 7 : le troisième
refus du 28/11 (la v1063, processus CUDA-vierge) nomme UN SEUL exemple —
ajouter-v3-i26111705-t1 (12 615 jetons, refusé à SA SECONDE VISITE, pas 18,
pic 13.58 Gio, 456.00 MiB refusés = le [12 615 × 18 944] fp16, LA MOITIÉ du
pied fp32 du terrain.12 — la preuve que l'autocast a mordu). LE GESTE :
l'exclusion NOMMÉE du refusé seul ; le corpus FICHIER demeure byte-byte ;
la marche 3 × 16 = 48 pas (12 pas d'optimiseur EXACTS — la même horloge
cosine que le 51-pas du plan). LA PREUVE : le corpus recoupé byte-byte, la
re-mesure au tokenizer réel recoupée au tableau consigné de l'Entrée 462,
LE REPLI rejoué (le fail-closed éprouvé : un nom absent = le refus), l'ordre
des 16 = l'ordre des 17 privé du premier, la marche et l'horloge construites
et comparées, les totaux recalculés, la pente ∝ L des monstres restants."""
import hashlib
import json
import pathlib
import sys

import torch
from transformers import AutoTokenizer, get_cosine_schedule_with_warmup

CONTENU = pathlib.Path("/home/z/my-project/work/kit-entrainement-v106/contenu")
CORPUS = CONTENU / "dataset/train.jsonl"
TABLEAU = pathlib.Path("/home/z/my-project/work/mesures-corpus-v106.json")
PREUVES = pathlib.Path("/home/z/my-project/work/preuves-terrain13")

# ── les constantes du plan gelé (§ 3) ──
EPOQUES, ACCUM, LR, SEED, MAX_LEN = 3, 4, 1.5e-5, 20261128, 13000
LE_NOMMÉ = "ajouter-v3-i26111705-t1"          # le refus du pas 18 — l'unique nommé
# les constantes du Qwen2.5-Coder-7B (config.json constaté à l'Entrée 463)
Couches, CACHE, INTER = 28, 3584, 18944

print("── LA PREUVE AU BAC DU TERRAIN.13 (le repli nommé) ──")

# 1 · le corpus BYTE-BYTE (la loi des recettes § 2)
sha_corpus = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
assert sha_corpus == "39614077e5c6d9feb94eb528ae19d9f948d67c531a2ac26daa17229023bb3eb7", \
    f"CORPUS-DIVERGENT : {sha_corpus}"
lignes = [json.loads(l) for l in CORPUS.read_text(encoding="utf-8").splitlines() if l]
verts = [d for d in lignes if d.get("verdict") == "VERT"]
print(f"[1] le corpus BYTE-BYTE (sha 39614077…) : {len(lignes)} triples, "
      f"{len(verts)} VERTS — la loi § 2 intacte.")

# 2 · la re-mesure au tokenizer réel (l'enveloppe du moteur, la pièce vivante)
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
sys.path.insert(0, "/home/z/my-project/work/kit-v102")
from moteur_campagne import enveloppe  # noqa: E402
mesure = {}
for d in verts:
    p = tok(enveloppe(d["contrat"]), add_special_tokens=False)["input_ids"]
    c = tok(d["reponse"] + "<|im_end|>", add_special_tokens=False)["input_ids"]
    mesure[d["triple"]] = (len(p), len(c), len(p) + len(c))
tableau = {r["triple"]: (r["P"], r["C"], r["L"]) for r in json.loads(TABLEAU.read_text("utf-8"))}
assert set(mesure) == set(tableau), "le tableau consigné diverge du corpus"
for t, (P, C, L) in mesure.items():
    assert (P, C, L) == tableau[t], f"la re-mesure diverge du tableau consigné : {t}"
print(f"[2] la re-mesure au tokenizer réel recoupe le tableau consigné "
      f"(l'Entrée 462) — {len(mesure)}/17 BYTE-BYTE.")

# 3 · LE REPLI NOMMÉ — le bloc de la cellule 5 v1064, TEL QUEL
def repli(exemples, exclus):
    n_avant = len(exemples)
    retenus = [e for e in exemples if e["triple"] not in exclus]
    if len(retenus) != n_avant - len(exclus):
        raise SystemExit(
            "EXCLUSION-NOMMÉE-DIVERGENTE : le repli du plan § 7 exige le nommé "
            "au corpus — le refus mesuré ne s'accorde pas au corpus lu.")
    return retenus

exemples = [{"triple": t, "P": P, "C": C, "L": L} for t, (P, C, L) in mesure.items()]
retenus = repli(exemples, {LE_NOMMÉ})
assert len(retenus) == 16 and LE_NOMMÉ not in {e["triple"] for e in retenus}
try:  # le fail-closed éprouvé : un nom absent = le refus nommé
    repli(exemples, {"nom-qui-nexiste-pas"})
    raise AssertionError("le fail-closed n'a pas mordu")
except SystemExit as exc:
    assert "EXCLUSION-NOMMÉE-DIVERGENTE" in str(exc)
print(f"[3] LE REPLI : {LE_NOMMÉ} EXCLU (le nommé du pas 18) — 16 retenus ; "
      "le fail-closed éprouvé (un nom absent = EXCLUSION-NOMMÉE-DIVERGENTE).")

# 4 · l'ordre : les longs d'abord PARMI LES RETENUS (la clé du plan § 3 inchangée)
ordre17 = sorted(exemples, key=lambda e: -e["L"])
ordre16 = sorted(retenus, key=lambda e: -e["L"])
assert [e["triple"] for e in ordre17][1:] == [e["triple"] for e in ordre16]
assert all(ordre16[i]["L"] >= ordre16[i + 1]["L"] for i in range(15))
assert ordre16[0]["triple"] == "ajouter-v3-i26111705-t3" and ordre16[0]["L"] == 12021
for e in ordre16:  # la garde EXEMPLE-TROP-LONG (le plan § 2) : aucun retenu ne dépasse
    assert e["L"] <= MAX_LEN, f"EXEMPLE-TROP-LONG : {e['triple']}"
print(f"[4] l'ordre des 16 = l'ordre des 17 privé du premier (t3 12 021 en tête, "
      f"v4 3 351 en queue) — la clé du plan § 3 inchangée, aucun retenu > {MAX_LEN}.")

# 5 · LA MARCHE : 48 pas, 12 pas d'optimiseur EXACTS — L'HORLOGE IDENTIQUE
n_pas = len(retenus) * EPOQUES
opt_pas = n_pas // ACCUM
assert (n_pas, opt_pas) == (48, 12) and n_pas % ACCUM == 0
opt_pas_51 = (len(exemples) * EPOQUES) // ACCUM      # le plan : 51 pas → 12 steps
assert opt_pas_51 == 12
torch.manual_seed(SEED)
def horloge(nb_micro):
    op = torch.optim.AdamW([torch.zeros((), requires_grad=True)], lr=LR, weight_decay=0.0)
    total = nb_micro // ACCUM
    sc = get_cosine_schedule_with_warmup(op, max(1, int(0.05 * total)), total)
    lrs = []
    for _ in range(total):
        op.step(); sc.step(); lrs.append(op.param_groups[0]["lr"])
    return lrs
h48, h51 = horloge(48), horloge(51)
assert len(h48) == len(h51) == 12 and h48 == h51
assert h48[0] == LR and all(a == b for a, b in zip(h48, h51))
print(f"[5] LA MARCHE : {n_pas} pas, {opt_pas} pas d'optimiseur EXACTS (48 % 4 = 0 — "
      "les 3 micro-pas orphelins du 51 disparaissent) ; l'horloge cosine du 48-pas "
      "est IDENTIQUE à celle du 51-pas (12 steps, échauffement 1, lr égaux pas à pas).")

# 6 · les totaux recalculés (le registre de la cellule 5 v1064)
P17, C17 = sum(e["P"] for e in exemples), sum(e["C"] for e in exemples)
P16, C16 = sum(e["P"] for e in retenus), sum(e["C"] for e in retenus)
assert (P17, C17) == (78343, 20906)                  # les totaux du plan § 2
exclu = mesure[LE_NOMMÉ]
assert (P16, C16) == (P17 - exclu[0], C17 - exclu[1]) == (70050, 16584)
Ls = sorted(e["L"] for e in retenus)
mediane = (Ls[7] + Ls[8]) / 2
print(f"[6] les totaux : P {P17} → {P16} · C {C17} → {C16} (l'exclu portait "
      f"P {exclu[0]} + C {exclu[1]}) ; le max retenu 12 021 · le min 3 351 · "
      f"la médiane {mediane:.1f} (4 527 aux 17).")

# 7 · LA PENTE DES MONSTRES RESTANTS (l'estimation nommée estimation)
pente_bornes = Couches * CACHE * 2 / 2**30            # Gio par jeton (fp16)
pente_mlp = INTER * 2 / 2**30                          # Gio par jeton par tampon fp16
dL = mesure[LE_NOMMÉ][2] - mesure["ajouter-v3-i26111705-t3"][2]
dpic = dL * (pente_bornes + 2 * pente_mlp)             # ~2 tampons MLP au pic
tampon_refuse = mesure[LE_NOMMÉ][2] * INTER * 2 / 2**20
print(f"[7] LA PENTE (estimation, NON mesure) : le refus du pas 18 = "
      f"{tampon_refuse:.2f} Mio — le [{mesure[LE_NOMMÉ][2]} × {INTER}] fp16, la "
      f"moitié exacte du pied fp32 du terrain.12 (l'autocast A MORDU) ; t3/t2 : "
      f"{dL} jetons plus courts (−{dL / mesure[LE_NOMMÉ][2] * 100:.1f} %) → "
      f"~{dpic:.2f} Gio rendus au pic (bornes {pente_bornes:.2e} Gio/jeton + "
      f"tampons MLP {pente_mlp:.2e}/pièce) ; leur 1re visite TENUE (le run du "
      f"maître, les pas 2-3) — la mesure ne les a JAMAIS nommés ; si la 2e visite "
      f"les refuse, le refus reviendra AU LABO avec le pic mesuré.")

# ── la pièce de preuve ──
PREUVES.mkdir(exist_ok=True)
preuve = {
    "passe": "repli-0",
    "terrain": "terrain.13",
    "corpus_sha256": sha_corpus,
    "verts_17": len(exemples),
    "recoup_tableau_entree462": "byte-byte 17/17",
    "exclusion_nommee": LE_NOMMÉ,
    "exclu": {"P": exclu[0], "C": exclu[1], "L": exclu[2]},
    "retenus": 16,
    "ordre": [e["triple"] for e in ordre16],
    "longueurs": {e["triple"]: e["L"] for e in ordre16},
    "marche": {"pas": n_pas, "pas_optimiseur": opt_pas, "exact_48_mod_4": True,
               "horloge": "IDENTIQUE au 51-pas (12 steps, échauffement 1, lr égaux)",
               "lr_premier": h48[0], "lr_dernier": h48[-1]},
    "totaux": {"P_16": P16, "C_16": C16, "P_17": P17, "C_17": C17,
               "max_retenu": 12021, "min_retenu": 3351, "mediane_16": mediane,
               "mediane_17": 4527},
    "garde_exemple_trop_long": "aucun retenu > 13000",
    "fail_clos_eprouve": "EXCLUSION-NOMMÉE-DIVERGENTE (un nom absent = le refus)",
    "pente_monstres_restants": {
        "tampon_refuse_mio": round(tampon_refuse, 2),
        "classe": f"[{mesure[LE_NOMMÉ][2]} × {INTER}] fp16 — la moitié du pied fp32 du terrain.12",
        "dL_t1_t3": dL, "dpic_estime_gio": round(dpic, 2),
        "statut": "ESTIMATION nommée estimation — la mesure seule dira ; le refus éventuel de t3/t2 reviendra AU LABO",
    },
}
sortie = PREUVES / "preuve-terrain13-repli-0.json"
sortie.write_text(json.dumps(preuve, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"── la pièce : {sortie} ({sortie.stat().st_size} o) ──")
print("LA PREUVE EST VERTE : le repli nommé est prêt à vivre à la cellule 5.")
