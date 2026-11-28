# -*- coding: utf-8 -*-
"""LES CELLULES NOUVELLES du notebook ENTRAÎNEMENT v106 (les sources).
Les cellules reconduites du v105 sont lues de work/v105-cells/ et patchées
par l'assembleur (les amendements NOMMÉS) ; les cellules ci-dessous sont les
pièces neuves de l'entraînement (gate, SFT, post-entraînement, kits)."""

# ── CELLULE 3 (v106) — LES DEUX KITS AU COFFRE (v101 épinglé + entraînement v106 épinglé) ──
CELL_KITS = r'''# CELLULE 3 — LES DEUX KITS AU COFFRE, 0 CLIC : le relais embarqué tire LE KIT
# POSTE v101 TEL QUEL (l'instrument épreuvé de la batterie — byte-byte la
# campagne 105) PUIS LE KIT D'ENTRAÎNEMENT v106 (le corpus + le plan gelé) —
# chacun à SON ID Drive et SON empreinte ÉPINGLÉS (KIT-DIVERGENT le refus
# nommé, fail-closed). AUCUN montage du Drive, AUCUNE fenêtre, AUCUN clic.
# LE JETON RELAIS du labo (le /Tokens du coffre, la voie éprouvée D263).
# LA COPIE AVEUGLE : le dépôt git est PUBLIC — sa copie porte les TROIS
# chaînes VIDES (IDENTIFIANTS-ABSENTS le refus nommé) ; la copie vivante vit
# au /livrables du coffre.
import hashlib
import json
import pathlib
import shutil
import time
import urllib.parse
import urllib.request
import zipfile

# LES IDENTIFIANTS DU COFFRE (la voie 0 clic — aucune fenêtre, aucun clic) :
CLIENT_ID = "%%CLIENT_ID%%"
CLIENT_SECRET = "%%CLIENT_SECRET%%"
REFRESH_TOKEN = "%%REFRESH_TOKEN%%"

# LES DEUX KITS ÉPINGLÉS (le plan gelé PLAN-ENTRAINEMENT-COLAB-V106 § 5) :
KITS = [
    {   # l'instrument de la batterie — byte-byte la campagne 105
        "nom": "TRIADE_kit_campagne_poste_v101.zip",
        "sha256": "3b78b544bfe6a6b102666ddba3d8d53af2d04e65b5ffcf963dbd2418d9f4f348",
        "id_drive": "1pa_FCF6GP5jkbCVEWg6BOtgAB2dW3T-Z",
        "dest": pathlib.Path("/content/kit"),
    },
    {   # le corpus + le plan gelé de l'entraînement
        "nom": "TRIADE_kit_entrainement_v106.zip",
        "sha256": "%%SHA_KIT_ENTRAINEMENT%%",
        "id_drive": "%%ID_KIT_ENTRAINEMENT%%",
        "dest": pathlib.Path("/content/kit-entrainement"),
    },
]

if not (CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN):
    raise SystemExit("IDENTIFIANTS-ABSENTS : la présente est LA COPIE AVEUGLE du dépôt "
                     "public — les identifiants n'y vivent jamais. La copie vivante vit "
                     "au /livrables du coffre (Entrainement-Colab-v106.ipynb).")


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for morceau in iter(lambda: f.read(1 << 20), b""):
            h.update(morceau)
    return h.hexdigest()


def jeton_relais(essais=3):
    """Le jeton frappé au relais — la voie éprouvée D263, les ratés réessayés."""
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"}).encode()
    derniere = None
    for i in range(essais):
        try:
            req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))["access_token"]
        except Exception as e:
            derniere = e
            print(f"[coffre] le relais a manqué ({e.__class__.__name__}) — "
                  f"le réessai {i + 2}/{essais} dans 10 s")
            time.sleep(10)
    raise SystemExit(f"JETON-ROUGE : le relais n'a pas donné son jeton "
                     f"({derniere.__class__.__name__}) — le journal ci-dessus TEL QUEL.")


def tirer_la_piece(tok, id_drive, nom):
    """La pièce tirée du coffre à l'ID épinglé — le compte à voix haute."""
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{id_drive}?alt=media",
        headers={"Authorization": f"Bearer {tok}"})
    dest = pathlib.Path("/content") / nom
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        vu = 0
        while True:
            morceau = r.read(1 << 20)
            if not morceau:
                break
            f.write(morceau)
            vu += len(morceau)
            if total:
                print(f"[coffre] {nom} : {100 * vu // total} %", end="\r")
    print()
    return dest


print("[coffre] LE JETON RELAIS se frappe — AUCUNE fenêtre, AUCUN clic (la voie 0 clic).")
tok = jeton_relais()
for kit in KITS:
    zip_kit = tirer_la_piece(tok, kit["id_drive"], kit["nom"])
    empreinte = sha256f(zip_kit)
    print(f"[coffre] {kit['nom']} : {zip_kit.stat().st_size} o — sha256 {empreinte[:16]}…")
    if empreinte != kit["sha256"]:
        raise SystemExit(f"KIT-DIVERGENT : {kit['nom']} — {empreinte} != {kit['sha256']} "
                         "(l'empreinte épinglée) — le kit NE COURT PAS (fail-closed).")
    if kit["dest"].exists():
        shutil.rmtree(kit["dest"])
    with zipfile.ZipFile(zip_kit) as z:
        z.extractall(kit["dest"])
    pieces = [p for p in kit["dest"].rglob("*") if p.is_file()]
    print(f"[coffre] l'empreinte recoupée VERT — extrait à {kit['dest']} : {len(pieces)} pièces")
'''

# ── CELLULE 4 (v106) — LE GATE DE L'ENTRAÎNEMENT ──
CELL_GATE = r'''# CELLULE 4 — LE GATE DE L'ENTRAÎNEMENT : le manifeste du kit recoupé, LE
# COMPTE DES VERTS (17 — la loi des recettes), l'enveloppe du moteur importée
# (le MÊME langage que la batterie), le tokenizer du modèle chargé. Chaque
# écart = refus nommé AVANT la marche (fail-closed).
import hashlib
import json
import pathlib
import sys

DOS_KIT_ENT = pathlib.Path("/content/kit-entrainement")
DOS_KIT = pathlib.Path("/content/kit")

# 1 · le manifeste du kit — chaque pièce recoupée à son empreinte
manifeste = json.loads((DOS_KIT_ENT / "MANIFESTE-KIT-ENTRAINEMENT.json").read_text("utf-8"))
for piece in manifeste["pieces"]:
    p = DOS_KIT_ENT / piece["chemin"]
    if not p.exists():
        raise SystemExit(f"PIÈCE-ABSENTE : {piece['chemin']} — le kit est incomplet.")
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != piece["sha256"]:
        raise SystemExit(f"PIÈCE-DIVERGENTE : {piece['chemin']} — {h} != {piece['sha256']}")
print(f"[gate] le manifeste recoupé : {len(manifeste['pieces'])} pièces VERTES.")

# 2 · le plan gelé présent (la loi du kit)
if not (DOS_KIT_ENT / "PLAN-ENTRAINEMENT-COLAB-V106.md").exists():
    raise SystemExit("PLAN-ABSENT : le plan gelé vit au kit — AUCUNE mesure sans lui.")
print(f"[gate] le plan gelé : sha256 {manifeste['sha_plan']} (consigné au manifeste).")

# 3 · LE COMPTE DES VERTS (la loi des recettes : les VERTS seuls)
verts, total = [], 0
with open(DOS_KIT_ENT / "dataset" / "train.jsonl", encoding="utf-8") as f:
    for ligne in f:
        d = json.loads(ligne)
        total += 1
        if d["verdict"] == "VERT":
            verts.append(d)
ATTENDUS = manifeste["verts_attendus"]
print(f"[gate] le corpus : {total} triples — {len(verts)} VERTS (les REFUS exclus).")
if len(verts) != ATTENDUS:
    raise SystemExit(f"COMPTE-VERTS-DIVERGENT : {len(verts)} verts != {ATTENDUS} attendus "
                     "(le manifeste) — le corpus a changé, le plan ne court plus.")

# 4 · l'enveloppe du moteur — la pièce vivante importée (jamais une copie)
sys.path.insert(0, str(DOS_KIT))
from moteur_campagne import enveloppe  # noqa: E402
e = enveloppe("ESSAI")
assert e.startswith("<|im_start|>user\n") and e.endswith("<|im_start|>assistant\n")
print("[gate] l'enveloppe du moteur importée — le MÊME langage que la batterie (l'Entrée 451).")

# 5 · le tokenizer du modèle
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
probe = tok(enveloppe("probe"), add_special_tokens=False)["input_ids"]
print(f"[gate] le tokenizer vivant : {len(tok)} jetons au vocabulaire, la sonde {len(probe)} ids.")
print("[gate] LE GATE DE L'ENTRAÎNEMENT EST VERT — la cellule 5 (LE SFT) peut courir.")
'''

# ── CELLULE 5 (v106) — L'ENTRAÎNEMENT QLoRA SFT ──
CELL_SFT = r'''# CELLULE 5 — L'ENTRAÎNEMENT QLoRA SFT : les 17 VERTS du corpus, la perte sur
# LA RÉPONSE SEULE, l'enveloppe VERBATIM du moteur, les hyperparams du plan
# gelé (§ 3) — chaque pas imprimé (le journal vit en direct, la courbe au
# registre). Les longs exemples d'ABORD (l'échec OOM vient tôt, jamais à la
# fin) ; EXEMPLE-TROP-LONG et EXEMPLE-LONG-OOM les refus nommés.
import json
import pathlib
import time

import torch
from peft import LoraConfig, get_peft_model
from transformers import (AutoModelForCausalLM, BitsAndBytesConfig,
                          get_cosine_schedule_with_warmup)

import sys
sys.path.insert(0, "/content/kit")
from moteur_campagne import enveloppe  # noqa: E402  (la pièce vivante)

# ── les constantes du plan gelé (§ 3) ──
MODELE = "Qwen/Qwen2.5-Coder-7B-Instruct"
SEED = 20261128
EPOQUES, ACCUM, LR = 3, 4, 1.5e-5
MAX_LEN = 13000          # AUCUNE troncature (le plan gelé § 2)
R, ALPHA, DROPOUT = 16, 32, 0.05
CIBLES = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

torch.manual_seed(SEED)
DOS_ADAPTER = pathlib.Path("/content/adapter-entrainement-v106")
REGISTRE = pathlib.Path("/content/registre-entrainement-v106.json")

# ── les données : les VERTS seuls, l'enveloppe du moteur ──
verts = []
with open("/content/kit-entrainement/dataset/train.jsonl", encoding="utf-8") as f:
    for ligne in f:
        d = json.loads(ligne)
        if d["verdict"] == "VERT":
            verts.append(d)
print(f"[sft] {len(verts)} VERTS — la tokenisation court (l'enveloppe du moteur)…")
exemples = []
for d in verts:
    p = tok(enveloppe(d["contrat"]), add_special_tokens=False)["input_ids"]
    c = tok(d["reponse"] + "<|im_end|>", add_special_tokens=False)["input_ids"]
    if len(p) + len(c) > MAX_LEN:
        raise SystemExit(f"EXEMPLE-TROP-LONG : {d['triple']} à {len(p) + len(c)} jetons > "
                         f"{MAX_LEN} — le plan gelé refuse la troncature (fail-closed).")
    exemples.append({"triple": d["triple"], "p": p, "c": c})
exemples.sort(key=lambda e: -(len(e["p"]) + len(e["c"])))   # les longs d'abord
l_max = max(len(e["p"]) + len(e["c"]) for e in exemples)
print(f"[sft] le plus long exemple : {l_max} jetons ; le plus court : "
      f"{min(len(e['p']) + len(e['c']) for e in exemples)} — AUCUNE troncature.")

# ── le modèle 4 bits (le T4 porte le fp16, pas le bf16) ──
print("[sft] le modèle se charge en 4 bits NF4 (double quantification)…")
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.float16,
                         bnb_4bit_use_double_quant=True)
model = AutoModelForCausalLM.from_pretrained(
    MODELE, quantization_config=bnb, device_map={"": 0},
    torch_dtype=torch.float16, attn_implementation="sdpa")
model.gradient_checkpointing_enable()
model.enable_input_require_grads()
model.config.use_cache = False
lora_cfg = LoraConfig(r=R, lora_alpha=ALPHA, lora_dropout=DROPOUT, bias="none",
                      task_type="CAUSAL_LM", target_modules=CIBLES)
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()

# ── la boucle : batch 1 × accumulation 4, la perte sur la réponse seule ──
params = [p for p in model.parameters() if p.requires_grad]
opt = torch.optim.AdamW(params, lr=LR, weight_decay=0.0)
n_pas = len(exemples) * EPOQUES
opt_pas = n_pas // ACCUM
sched = get_cosine_schedule_with_warmup(opt, max(1, int(0.05 * opt_pas)), opt_pas)
courbe, t0 = [], time.time()
print(f"[sft] LA MARCHE : {EPOQUES} époques × {len(exemples)} exemples = {n_pas} pas "
      f"({opt_pas} pas d'optimiseur) — le journal vit en direct ci-dessous.")
model.train()
try:
    for epo in range(EPOQUES):
        for i, e in enumerate(exemples):
            ids = e["p"] + e["c"]
            t = torch.tensor([ids], device="cuda")
            labels = torch.tensor([[-100] * len(e["p"]) + e["c"]], device="cuda")
            out = model(input_ids=t, labels=labels)
            (out.loss / ACCUM).backward()
            courbe.append({"pas": len(courbe) + 1, "epoque": epo + 1,
                           "triple": e["triple"], "perte": round(float(out.loss), 5)})
            if len(courbe) % ACCUM == 0:
                torch.nn.utils.clip_grad_norm_(params, 1.0)
                opt.step()
                sched.step()
                opt.zero_grad()
            if len(courbe) % 4 == 0 or len(courbe) == n_pas:
                print(f"[sft] époque {epo + 1}/{EPOQUES} · pas {len(courbe)}/{n_pas} · "
                      f"perte {out.loss:.4f} · {time.time() - t0:.0f} s", flush=True)
except torch.cuda.OutOfMemoryError:
    raise SystemExit(f"EXEMPLE-LONG-OOM : le T4 n'a pas tenu l'exemple "
                     f"{e['triple']} ({len(ids)} jetons) — le plan gelé nomme le refus ; "
                     f"la voie de repli (l'exclusion nommée) est AU LABO, jamais au bord.")
model.eval()

# ── l'adapter sauvé + le registre né (la pièce d'œuvre du run) ──
model.save_pretrained(str(DOS_ADAPTER))
duree = time.time() - t0
REGISTRE.write_text(json.dumps({
    "modele": MODELE, "methode": "QLoRA-SFT", "quantisation": "NF4-double-fp16",
    "lora": {"r": R, "alpha": ALPHA, "dropout": DROPOUT, "cibles": CIBLES},
    "optimisation": {"lr": LR, "horloge": "cosine+5%", "epoques": EPOQUES,
                     "accumulation": ACCUM, "clip": 1.0, "graine": SEED,
                     "max_len": MAX_LEN, "troncature": "AUCUNE"},
    "donnees": {"verts": len(exemples), "jetons_prompt": sum(len(e["p"]) for e in exemples),
                "jetons_reponse": sum(len(e["c"]) for e in exemples),
                "exemple_max": l_max},
    "pas": n_pas, "duree_s": round(duree, 1),
    "perte_premier": courbe[0]["perte"], "perte_dernier": courbe[-1]["perte"],
    "courbe": courbe,
}, ensure_ascii=False, indent=2), encoding="utf-8")
taille = sum(p.stat().st_size for p in DOS_ADAPTER.rglob("*") if p.is_file())
print(f"[sft] L'ENTRAÎNEMENT EST CLOSE : {n_pas} pas en {duree / 60:.1f} min — "
      f"perte {courbe[0]['perte']:.4f} → {courbe[-1]['perte']:.4f}.")
print(f"[sft] l'adapter : {DOS_ADAPTER} ({taille / 2**20:.1f} Mio) — "
      f"le registre : {REGISTRE} (la courbe y vit).")
'''

# ── CELLULE 6 (v106) — LE POST-ENTRAÎNEMENT : adapter → GGUF + le coffre AVANT l'éval ──
CELL_POST = r'''# CELLULE 6 — LE POST-ENTRAÎNEMENT : l'adapter converti au GGUF (le
# convertisseur du dépôt llama.cpp, à la MÊME release que le binaire du
# serving), puis LA PIÈCE TÉLÉVERSÉE AU COFFRE AVANT L'ÉVALUATION (le plan
# gelé § 4 : l'œuvre vit au coffre quand l'éval court — aucune perte si le
# runtime meurt en batterie). ADAPTER-CONVERSION-ROUGE le refus nommé.
import json
import pathlib
import subprocess
import sys
import time
import urllib.request

DOS_ADAPTER = pathlib.Path("/content/adapter-entrainement-v106")
GGUF_ADAPTER = pathlib.Path("/content/adapter-entrainement-v106.gguf")
REGISTRE = pathlib.Path("/content/registre-entrainement-v106.json")
CONVERTISSEUR = pathlib.Path("/content/convert_lora_to_gguf.py")

# 1 · le convertisseur — à la release du serving (la MÊME, la cohérence du bord)
def tag_de_la_release():
    with urllib.request.urlopen("https://api.github.com/repos/ggml-org/llama.cpp/releases/latest",
                                timeout=60) as r:
        return json.loads(r.read().decode())["tag_name"]

TAG = tag_de_la_release()
print(f"[post] la release du jour : {TAG} — le convertisseur y est tiré.")
urllib.request.urlretrieve(
    f"https://raw.githubusercontent.com/ggml-org/llama.cpp/{TAG}/convert_lora_to_gguf.py",
    CONVERTISSEUR)
rep = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "gguf"],
                     capture_output=True, text=True)
if rep.returncode != 0:
    raise SystemExit(f"PIP-ROUGE (gguf) : {rep.stderr[-400:]}")

# 2 · la conversion (f16 — le delta, l'échelle α/r appliquée par le convertisseur)
r = subprocess.run([sys.executable, "-X", "utf8", str(CONVERTISSEUR),
                    str(DOS_ADAPTER), "--outfile", str(GGUF_ADAPTER), "--outtype", "f16"],
                   capture_output=True, text=True)
if r.returncode != 0 or not GGUF_ADAPTER.exists():
    print(r.stdout[-1500:])
    print(r.stderr[-1500:])
    raise SystemExit("ADAPTER-CONVERSION-ROUGE : le convertisseur a refusé — le journal "
                     "ci-dessus TEL QUEL (l'adapter safetensors demeure, la voie de "
                     "repli — la fusion — est nommée au plan gelé § 6.4).")
print(f"[post] l'adapter GGUF né : {GGUF_ADAPTER} ({GGUF_ADAPTER.stat().st_size / 2**20:.1f} Mio, f16).")

# 3 · LA PIÈCE AU COFFRE AVANT L'ÉVAL (le plan gelé § 4 — le relais embarqué)
try:
    CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
except NameError:
    raise SystemExit("ORDRE-ROMPU : les identifiants du relais vivent à la cellule 3.")
ID_TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"    # le /test du coffre (recoupé au labo le 27/11)
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())


def jeton_relais(essais=3):
    import urllib.parse
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"}).encode()
    derniere = None
    for i in range(essais):
        try:
            req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
            with urllib.request.urlopen(req, timeout=30) as rr:
                return json.loads(rr.read().decode("utf-8"))["access_token"]
        except Exception as e:
            derniere = e
            time.sleep(10)
    raise SystemExit(f"JETON-ROUGE : le relais n'a pas donné son jeton "
                     f"({derniere.__class__.__name__}).")


def televerse_multipart(tok, nom, parent, octets_):
    import urllib.parse
    frontieres = "tr314d3k1t"
    meta = {"name": nom, "parents": [parent]}
    corps = ("--" + frontieres + "\r\n"
             "Content-Type: application/json; charset=UTF-8\r\n\r\n"
             + json.dumps(meta) + "\r\n"
             + "--" + frontieres + "\r\n"
             "Content-Type: application/octet-stream\r\n\r\n").encode("utf-8")
    corps += octets_ + ("\r\n--" + frontieres + "--\r\n").encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=corps, method="POST",
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": f"multipart/related; boundary={frontieres}"})
    with urllib.request.urlopen(req, timeout=900) as rr:
        return json.loads(rr.read().decode("utf-8"))["id"]


tok = jeton_relais()
for piece in (GGUF_ADAPTER, REGISTRE):
    nom = f"{piece.stem}-{TS}{piece.suffix}"
    idp = televerse_multipart(tok, nom, ID_TEST, piece.read_bytes())
    print(f"[post] LA PIÈCE AU COFFRE (avant l'éval) : {nom} — id {idp}")
print("[post] L'ŒUVRE EST AU COFFRE — l'évaluation peut courir (la pièce est sauvée).")
'''

# ── CELLULE 9 (v106) — LE RETOUR AU COFFRE (le zip d'entraînement + les pièces du moteur) ──
CELL_RETOUR = r'''# CELLULE 9 — LE RETOUR AU COFFRE, 0 CLIC : LE ZIP D'ENTRAÎNEMENT (l'adapter
# safetensors + le registre + la courbe + LE ZIP DU MOTEUR + le rapport du
# poste) téléversé au /test du coffre par LE RELAIS EMBARQUÉ, RECOPÉ
# byte-byte PAR RELECTURE. Le pilote du labo rapatrie le preuves-campagne-*
# le plus récent du kit — le présent porte TOUT (l'œuvre ET la mesure).
import hashlib
import json
import pathlib
import time
import urllib.parse
import urllib.request
import zipfile

try:
    CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
except NameError:
    raise SystemExit("ORDRE-ROMPU : les identifiants du relais vivent à la cellule 3.")
ID_TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOS_KIT = pathlib.Path("/content/kit")
DOS_ADAPTER = pathlib.Path("/content/adapter-entrainement-v106")
GGUF_ADAPTER = pathlib.Path("/content/adapter-entrainement-v106.gguf")
REGISTRE = pathlib.Path("/content/registre-entrainement-v106.json")
RAPPORT = pathlib.Path("/content/rapport-poste.txt")
HORLOGE = pathlib.Path("/content/horloge-batterie.txt")


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for morceau in iter(lambda: f.read(1 << 20), b""):
            h.update(morceau)
    return h.hexdigest()


def jeton_relais(essais=3):
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"}).encode()
    derniere = None
    for i in range(essais):
        try:
            req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))["access_token"]
        except Exception as e:
            derniere = e
            time.sleep(10)
    raise SystemExit(f"JETON-ROUGE ({derniere.__class__.__name__}).")


def televerse_multipart(tok, nom, parent, octets_):
    frontieres = "tr314d3k1t"
    meta = {"name": nom, "parents": [parent]}
    corps = ("--" + frontieres + "\r\n"
             "Content-Type: application/json; charset=UTF-8\r\n\r\n"
             + json.dumps(meta) + "\r\n"
             + "--" + frontieres + "\r\n"
             "Content-Type: application/octet-stream\r\n\r\n").encode("utf-8")
    corps += octets_ + ("\r\n--" + frontieres + "--\r\n").encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=corps, method="POST",
        headers={"Authorization": f"Bearer {tok}",
                 "Content-Type": f"multipart/related; boundary={frontieres}"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.loads(r.read().decode("utf-8"))["id"]


def relit_le_coffre(tok, file_id):
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media",
        headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        return r.read()


# 1 · le zip du moteur (la batterie l'a rendu à la cellule 8)
zips_moteur = sorted(DOS_KIT.glob("preuves-campagne-2*.zip"), key=lambda p: p.stat().st_mtime)
if not zips_moteur:
    raise SystemExit("ZIP-ABSENT : aucun preuves-campagne du moteur au kit — "
                     "la cellule 8 (LA BATTERIE) d'abord.")
zip_moteur = zips_moteur[-1]

# 2 · le rapport du poste clos (l'horloge de la batterie y vit)
if not RAPPORT.exists():
    raise SystemExit("ORDRE-ROMPU : aucun rapport-poste.txt — la cellule 1 d'abord.")
if HORLOGE.exists():
    with open(RAPPORT, "a", encoding="utf-8") as f:
        f.write("\nL'HORLOGE DE LA BATTERIE (les six étapes du plan gelé) :\n")
        for l in HORLOGE.read_text(encoding="utf-8").strip().splitlines():
            titre_etape, secondes = l.split("\t")
            f.write(f"  {titre_etape} — {float(secondes) / 60:.1f} min\n")

# 3 · LE ZIP D'ENTRAÎNEMENT (l'œuvre ET la mesure, une seule pièce)
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
NOM_ZIP = f"preuves-campagne-entrainement-v106-{TS}.zip"
CHEMIN_ZIP = DOS_KIT / NOM_ZIP
with zipfile.ZipFile(CHEMIN_ZIP, "zip", compresslevel=6) as z:
    z.write(zip_moteur, "moteur/" + zip_moteur.name)
    z.write(RAPPORT, "rapport-poste.txt")
    z.write(REGISTRE, "registre-entrainement-v106.json")
    for p in sorted(DOS_ADAPTER.rglob("*")):
        if p.is_file():
            z.write(p, "adapter-safetensors/" + str(p.relative_to(DOS_ADAPTER)))
    if GGUF_ADAPTER.exists():
        z.write(GGUF_ADAPTER, GGUF_ADAPTER.name)
empreinte = sha256f(CHEMIN_ZIP)
print(f"[retour] la pièce : {NOM_ZIP} ({CHEMIN_ZIP.stat().st_size / 2**20:.1f} Mio)")
print(f"[retour] sha256 : {empreinte}")
with open(RAPPORT, "a", encoding="utf-8") as f:
    f.write(f"\nLE ZIP D'ENTRAÎNEMENT : {NOM_ZIP}\nsha256 : {empreinte}\n")

# 4 · LE TÉLÉVERSEMENT 0 CLIC + LE RECOP byte-byte
print("[retour] LE JETON RELAIS se frappe — le téléversement court (aucune fenêtre).")
tok = jeton_relais()
id_zip = televerse_multipart(tok, NOM_ZIP, ID_TEST, CHEMIN_ZIP.read_bytes())
print(f"[retour] le zip téléversé au /test du coffre : id {id_zip}")
time.sleep(3)
relu = relit_le_coffre(tok, id_zip)
if hashlib.sha256(relu).hexdigest() != empreinte:
    raise SystemExit("RECOP-ROUGE : la pièce relue du coffre diverge — le journal TEL QUEL.")
print(f"[retour] RECOP byte-byte VERT — {NOM_ZIP} vit au /test du coffre.")
id_rapport = televerse_multipart(tok, f"rapport-poste-entrainement-v106-{TS}.txt",
                                 ID_TEST, RAPPORT.read_bytes())
print(f"[retour] le rapport du poste téléversé : id {id_rapport}")
print(f"[retour] LE RUN D'ENTRAÎNEMENT EST CLOSE — les liens vivent ci-dessus, "
      f"les verdicts TELS QUELS au /test (le labo les lira).")
'''
