#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ASSEMBLEUR DU KIT D'ENTRAÎNEMENT v106 (le patron des assembleurs du
dépôt, la vague 14+) : bâtit le kit (le plan gelé + le corpus byte-byte +
les recettes) PUIS le notebook 0-clic (les cellules du v105 reconduites aux
amendements NOMMÉS + les cellules neuves de l'entraînement), en DEUX copies
(aveugle au dépôt public, vivante au coffre), avec LES ÉPREUVES DU BAC.

Usage :
  assembler_kit_entrainement_v106.py kit                → le zip du kit + son sha256
  assembler_kit_entrainement_v106.py notebook <id-drive> <sha-kit>  → les notebooks
"""
import hashlib
import json
import pathlib
import py_compile
import shutil
import subprocess
import sys
import zipfile

LABO = pathlib.Path("/home/z/my-project")
DEPOT = LABO / "depot"
V105_CELLS = LABO / "work" / "v105-cells"
DOS_BUILD = LABO / "work" / "kit-entrainement-v106"
DOS_CORPUS = DEPOT / "atelier-corpus-2i7iy3xmg" / "dataset"

sys.path.insert(0, str(LABO / "scripts"))
from cellules_v106 import CELL_GATE, CELL_KITS, CELL_POST, CELL_RETOUR, CELL_SFT


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def cmd_kit():
    """Le kit : le plan gelé + le corpus byte-byte + les recettes + le manifeste."""
    dos = DOS_BUILD / "contenu"
    if dos.exists():
        shutil.rmtree(dos)
    (dos / "dataset").mkdir(parents=True)
    # 1 · le plan gelé (déjà écrit à la main — la loi)
    shutil.copy2(DOS_BUILD / "PLAN-ENTRAINEMENT-COLAB-V106.md", dos / "PLAN-ENTRAINEMENT-COLAB-V106.md")
    # 2 · le corpus byte-byte (les CINQ pièces de l'atelier 2i7iy3xmg)
    pieces_dataset = ["train.jsonl", "dev.jsonl", "test.jsonl",
                      "DATASET-CARD.json", "MANIFESTE.json"]
    for nom in pieces_dataset:
        src = DOS_CORPUS / nom
        if not src.exists():
            raise SystemExit(f"CORPUS-ABSENT : {src}")
        shutil.copy2(src, dos / "dataset" / nom)
    # 3 · les recettes du gym (byte-byte) + le compte des verts au manifeste
    shutil.copy2(DEPOT / "atelier-gym-3x9cf4e5d" / "RECETTES.md", dos / "RECETTES-GYM.md")
    verts = sum(1 for l in open(dos / "dataset" / "train.jsonl", encoding="utf-8")
                if json.loads(l)["verdict"] == "VERT")
    # 4 · le LISEZMOI du kit
    (dos / "LISEZMOI-KIT-ENTRAINEMENT.txt").write_text(
        "LE KIT D'ENTRAÎNEMENT TRIADE v106 (0 clic, la voie Colab)\n"
        "=" * 64 + "\n\nLE CONTENU : le plan gelé PLAN-ENTRAINEMENT-COLAB-V106.md (LA LOI\n"
        "du run — sha256 consigné au manifeste) ; le corpus de l'atelier\n"
        "2i7iy3xmg byte-byte (train 78 / dev 16 / test 16 — les VERTS SEULS à\n"
        "l'entraînement, la recette SFT du gym 3x9cf4e5d) ; RECETTES-GYM.md (les\n"
        "recettes SFT/DPO/RLVR, byte-byte du dépôt).\n\nLA LOI : aucune cible gelée touchée ;"
        " l'instrument de la batterie est LE\nKIT POSTE v101 byte-byte (son ID épinglé au"
        " notebook) ; les verdicts\nTELS QUELS, jamais habillés ; les gaps nommés au plan"
        " § 6.\n", encoding="utf-8")
    # 5 · le manifeste (chaque pièce à son empreinte)
    chemins = (["PLAN-ENTRAINEMENT-COLAB-V106.md", "LISEZMOI-KIT-ENTRAINEMENT.txt",
                "RECETTES-GYM.md"] + [f"dataset/{n}" for n in pieces_dataset])
    manifeste = {
        "kit": "TRIADE_kit_entrainement_v106",
        "verts_attendus": verts,
        "sha_plan": sha256f(dos / "PLAN-ENTRAINEMENT-COLAB-V106.md"),
        "pieces": [{"chemin": c, "sha256": sha256f(dos / c), "octets": (dos / c).stat().st_size}
                   for c in chemins],
    }
    (dos / "MANIFESTE-KIT-ENTRAINEMENT.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=2), encoding="utf-8")
    # 6 · le zip
    zip_path = DOS_BUILD / "TRIADE_kit_entrainement_v106.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compresslevel=9) as z:
        for c in chemins + ["MANIFESTE-KIT-ENTRAINEMENT.json"]:
            z.write(dos / c, c)
    print(f"KIT : {zip_path} ({zip_path.stat().st_size} o)")
    print(f"sha256 : {sha256f(zip_path)}")
    print(f"verts_attendus : {verts}")
    return zip_path


def cellule_v105(idx, remplacements=None, titre=None):
    """Une cellule du v105 reconduite — les amendements NOMMÉS (chaque
    remplacement doit s'appliquer, jamais silencieusement)."""
    src = (V105_CELLS / f"cell-{idx:02d}-code.txt").read_text(encoding="utf-8")
    for ancien, nouveau in (remplacements or []):
        if ancien not in src:
            raise SystemExit(f"AMENDEMENT-ROMPU : « {ancien[:60]}… » introuvable à la "
                             f"cellule v105 #{idx} — le patron a changé, VERIFIER.")
        src = src.replace(ancien, nouveau)
    return src


def md(titre, corps):
    return {"cell_type": "markdown", "metadata": {}, "source": [corps]}


def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": [src]}


def cmd_notebook(id_kit, sha_kit):
    """Le notebook v106 — les cellules v105 aux amendements nommés + les neuves."""
    # ── CELLULE 1 (poste) : le plan du run d'ENTRAÎNEMENT, la garde disque 40 Gio ──
    c_poste = cellule_v105(2, [
        ("# CELLULE 1 — LE POSTE COLAB : le verdict de l'environnement + LE PLAN DU RUN.",
         "# CELLULE 1 — LE POSTE COLAB : le verdict de l'environnement + LE PLAN DU RUN\n"
         "# (v106 — LA CAMPAGNE D'ENTRAÎNEMENT : QLoRA SFT puis LA MÊME BATTERIE que la 105)."),
        ("kit Colab v105 (0 clic)", "kit Colab v106 ENTRAÎNEMENT (0 clic)"),
        ('print("[plan] le kit v101 : L\'ENVELOPPE DE CHAT AU TRANSPORT (l\'Entrée 451 portée à la")',
         'print("[plan] LE RUN D\'ENTRAÎNEMENT : les 17 VERTS du corpus au QLoRA SFT (le plan gelé")'),
        ('print("[plan] conséquence) — les tests ratés du v104 y repassent au même geste unique ;")',
         'print("[plan] v106), PUIS LA MÊME BATTERIE que la 105 au modèle affiné (le --lora du")'),
        ('print("[plan] LA PORTE DE PAROLE garde le serving (BORD-MUET), LA SONDE DES DEUX")',
         'print("[plan] delta sur le GGUF Q6_K byte-byte — la seule différence du bord, nommée).")'),
        ('print("[plan] ENVELOPPES ouvre la batterie. Les plans gelés demeurent LA LOI.")',
         'print("[plan] L\'ADAPTER est téléversé au coffre AVANT l\'éval (l\'œuvre sauvée d\'abord).")'),
        ('"[plan] le kit v101 — l\'enveloppe de chat au transport (l\'Entrée 451), les plans gelés INTACTS"):',
         '"[plan] le run d\'entraînement v106 — QLoRA SFT puis la batterie de la 105 (le plan gelé"):'),
        ("if disque < 12:", "if disque < 40:"),
        ('raise SystemExit(f"DISQUE-INSUFFISANT : {disque:.1f} Gio libres — le GGUF seul en prend ~5-8 ; "',
         'raise SystemExit(f"DISQUE-INSUFFISANT : {disque:.1f} Gio libres — le modèle 4 bits + le GGUF "'),
        ('"change de runtime (le refus vient AVANT la marche, jamais deux heures après).")',
         '"+ l\'adapter + le cache HF en prennent ~25 ; change de runtime (le refus vient AVANT la marche).")'),
        ("[plan] le bord du run : {'GPU' if MODE_GPU else 'CPU'} · le GGUF : {QUANT}",
         "[plan] le bord du run : {'GPU' if MODE_GPU else 'CPU'} (le T4 est LA VOIE conseillée)"),
    ])
    # ── CELLULE 2 (deps) : + peft/bitsandbytes/accelerate/gguf ──
    c_deps = cellule_v105(4, [
        ('"llguidance", "tokenizers", "keystone-engine", "capstone"],',
         '"llguidance", "tokenizers", "keystone-engine", "capstone",\n'
         '                      "peft", "bitsandbytes", "accelerate", "gguf"],'),
        ('print(f"[deps] llguidance {getattr(llguidance, \'__version__\', \'?\')} · "',
         'import peft, bitsandbytes, accelerate, gguf\n'
         'print(f"[deps] peft {peft.__version__} · bitsandbytes {bitsandbytes.__version__} · "\n'
         '      f"accelerate {accelerate.__version__} · gguf OK — l\'entraînement armé · "\n'
         '      f"llguidance {getattr(llguidance, \'__version__\', \'?\')} · "'),
    ])
    # ── CELLULE 7 (serving) : le --lora du delta (la SEULE différence du bord) ──
    c_serving = cellule_v105(10, [
        ("# CELLULE 5 — LE SERVING SELON L'ENVIRONNEMENT : llama.cpp au runtime + le GGUF",
         "# CELLULE 7 — LE SERVING DU MODÈLE AFFINÉ : llama.cpp au runtime + le GGUF Q6_K"),
        ("# du bord. La commande consignée au LISEZMOI-CAMPAGNE-POSTE § 1 (llama-server",
         "# byte-byte la 105 + LE DELTA --lora (l'adapter né à la cellule 5). La commande"),
        ('    if GPU:\n        args_serving += ["-ngl", "99"]',
         '    if GPU:\n        args_serving += ["-ngl", "99"]\n'
         '    args_serving += ["--lora", str(pathlib.Path("/content/adapter-entrainement-v106.gguf"))]'),
    ])
    # ── CELLULE 8 (batterie) : le titre ──
    c_batterie = cellule_v105(12, [
        ("# CELLULE 6 — LA BATTERIE 0 CLIC : les SIX étapes du plan gelé courent",
         "# CELLULE 8 — LA BATTERIE 0 CLIC DU MODÈLE AFFINÉ : les SIX étapes du plan gelé"),
        ("la cellule 5 (le serving) d'abord.", "la cellule 7 (le serving affiné) d'abord."),
        ("la cellule 3 (le kit au coffre) d'abord.", "la cellule 3 (les kits au coffre) d'abord."),
        ("la cellule 7 porte le zip au coffre (0 clic).",
         "la cellule 9 porte le zip au coffre (0 clic)."),
    ])
    # ── CELLULE 10 (bilan) : le titre + les pièces d'entraînement ──
    c_bilan = cellule_v105(16, [
        ("# CELLULE 8 — LE BILAN DU RUN 0 CLIC : le tableau de l'horloge, les pièces",
         "# CELLULE 10 — LE BILAN DU RUN 0 CLIC : le tableau de l'horloge, les pièces"),
        ("LE BILAN DU RUN 0 CLIC (kit Colab v105) — l'horloge de la batterie :",
         "LE BILAN DU RUN 0 CLIC (kit Colab v106 ENTRAÎNEMENT) — l'horloge de la batterie :"),
        ('print("[bilan] LE RUN 0 CLIC EST CLOSE : le zip de preuves + le rapport du poste vivent")',
         'print("[bilan] LE RUN D\'ENTRAÎNEMENT EST CLOSE : le zip (l\'adapter + la mesure) + le rapport")'),
        ('print("[bilan] au /test du coffre. Les verdicts (tenue ou manquée, jamais habillée) y sont")',
         'print("[bilan] du poste vivent au /test du coffre. Les verdicts (tenue ou manquée, jamais")'),
        ('print("[bilan] portés TELS QUELS — le labo les lira.")',
         'print("[bilan] habillée) y sont TELS QUELS — le labo les lira ; la comparaison pré/post")\n'
         'print("[bilan] s\'y conduira (la campagne 105 est la ligne de base).")'),
    ])

    # ── les cellules neuves : les identifiants injectés (vivante) ou vides (aveugle) ──
    def kits_vivante():
        return (CELL_KITS
                .replace("%%CLIENT_ID%%", "%%-LUS-DU-JETON-DU-LABO-AU-RUNTIME-%%")
                .replace("%%CLIENT_SECRET%%", "%%-JAMAIS-AU-DÉPÔT-%%")
                .replace("%%REFRESH_TOKEN%%", "%%-JAMAIS-AU-DÉPÔT-%%")
                .replace("%%SHA_KIT_ENTRAINEMENT%%", sha_kit)
                .replace("%%ID_KIT_ENTRAINEMENT%%", id_kit))

    def kits_aveugle():
        return (CELL_KITS
                .replace("%%CLIENT_ID%%", "")
                .replace("%%CLIENT_SECRET%%", "")
                .replace("%%REFRESH_TOKEN%%", "")
                .replace("%%SHA_KIT_ENTRAINEMENT%%", sha_kit)
                .replace("%%ID_KIT_ENTRAINEMENT%%", id_kit))

    # le squelette commun des DEUX copies (les cellules communes IDENTIQUES)
    def squelette(c_kits):
        return [
            md(0, "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v106)\n\n"
                  "La campagne d'**entraînement** de Qwen2.5-Coder-7B avec TRIADE : "
                  "**QLoRA SFT** sur les 17 VERTS du corpus, puis **LA MÊME BATTERIE** "
                  "que la campagne 105 au modèle affiné — le `--lora` du delta sur le "
                  "GGUF Q6_K byte-byte. `Exécution → Tout exécuter` — c'est tout. "
                  "Au terme le zip (l'adapter + la mesure) + le rapport vivent au "
                  "`/test` du coffre. **Le T4 est la voie conseillée** (le plan gelé "
                  "du kit est LA LOI du run)."),
            md(1, "## 1 · LE POSTE COLAB — le verdict de l'environnement + LE PLAN DU RUN"),
            code(c_poste),
            md(2, "## 2 · LES DÉPENDANCES — le harnais + l'entraînement (peft, bitsandbytes)"),
            code(c_deps),
            md(3, "## 3 · LES DEUX KITS AU COFFRE — **0 CLIC** : le poste v101 (l'instrument) "
                  "+ le kit d'entraînement v106 (le corpus + le plan gelé)"),
            code(c_kits),
            md(4, "## 4 · LE GATE DE L'ENTRAÎNEMENT — le manifeste recoupé, LE COMPTE DES "
                  "VERTS, l'enveloppe du moteur"),
            code(CELL_GATE),
            md(5, "## 5 · L'ENTRAÎNEMENT — QLoRA SFT sur les 17 VERTS (la perte sur la "
                  "réponse seule, l'enveloppe du moteur, les hyperparams du plan gelé)"),
            code(CELL_SFT),
            md(6, "## 6 · LE POST-ENTRAÎNEMENT — l'adapter converti au GGUF **puis téléversé "
                  "au coffre AVANT l'éval** (l'œuvre sauvée d'abord)"),
            code(CELL_POST),
            md(7, "## 7 · LE SERVING DU MODÈLE AFFINÉ — le GGUF Q6_K byte-byte de la 105 + "
                  "LE DELTA `--lora` (la seule différence du bord) + LA PORTE DE PAROLE"),
            code(c_serving),
            md(8, "## 8 · LA BATTERIE 0 CLIC DU MODÈLE AFFINÉ — les SIX étapes du plan gelé, "
                  "l'instrument de la 105 TEL QUEL"),
            code(c_batterie),
            md(9, "## 9 · LE RETOUR AU COFFRE — **0 CLIC** : le zip d'entraînement (l'adapter "
                  "+ le registre + la mesure du moteur) téléversé au `/test`, recopé byte-byte"),
            code(CELL_RETOUR),
            md(10, "## 10 · LE BILAN DU RUN — le tableau de l'horloge, les pièces rendues, le run clos"),
            code(c_bilan),
        ]

    notebooks = {}
    for nom, c_kits in (("VIVANTE", kits_vivante()), ("AVEUGLE", kits_aveugle())):
        nb = {"nbformat": 4, "nbformat_minor": 5,
              "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"},
                           "language_info": {"name": "python"}},
              "cells": squelette(c_kits)}
        chemin = DOS_BUILD / f"Entrainement-Colab-v106-{nom}.ipynb"
        chemin.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        notebooks[nom] = chemin
        print(f"notebook {nom} : {chemin.name} ({chemin.stat().st_size} o)")

    # ── LES ÉPREUVES DU BAC ──
    print("\n=== LES ÉPREUVES DU BAC (v106) ===")
    for nom, chemin in notebooks.items():
        # 1 · la structure : nbformat strict, chaque code compile
        nb = json.loads(chemin.read_text(encoding="utf-8"))
        code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
        md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
        for i, c in enumerate(code_cells):
            src = "".join(c["source"])
            compile(src, f"cellule-{i}", "exec")  # la syntaxe, TOUTE
        print(f"[épreuve 1 · {nom}] la structure : {len(nb['cells'])} cellules "
              f"({len(code_cells)} code + {len(md_cells)} markdown), chaque code compile — VERT")
        # 2 · la loi 0 clic : aucun widget/input/eval_js/montage
        for c in code_cells:
            src = "".join(c["source"])
            for interdit in ("ipywidgets", "input(", "eval_js", "google.colab.drive",
                             "from google.colab import drive", "tkinter", "display("):
                if interdit in src:
                    raise SystemExit(f"[épreuve 2 · {nom}] LOI-0-CLIC-ROMPUE : « {interdit} » "
                                     "à une cellule — le kit ne le demande jamais au runtime.")
        print(f"[épreuve 2 · {nom}] la loi 0 clic (aucun widget/montage/autorisation) — VERT")
    # 3 · l'invariant : la SEULE divergence vivante/aveugle = les TROIS constantes
    viv = json.loads(notebooks["VIVANTE"].read_text(encoding="utf-8"))
    ave = json.loads(notebooks["AVEUGLE"].read_text(encoding="utf-8"))
    if len(viv["cells"]) != len(ave["cells"]):
        raise SystemExit("[épreuve 3] INVARIANT-ROMPU : les copies n'ont pas le même squelette.")
    divergences = []
    for i, (cv, ca) in enumerate(zip(viv["cells"], ave["cells"])):
        sv, sa = "".join(cv["source"]), "".join(ca["source"])
        if sv != sa:
            divergences.append(i)
    if divergences != [6]:
        raise SystemExit(f"[épreuve 3] INVARIANT-ROMPU : les cellules divergentes = {divergences} "
                         "— la SEULE divergence permise est la cellule 6 (les identifiants).")
    sv, sa = ("".join(viv["cells"][6]["source"]), "".join(ave["cells"][6]["source"]))
    # (la vérification vive — les préfixes des TROIS constantes — vit au labo
    #  seul ; la copie du dépôt porte la garde structurelle : les TROIS
    #  chaînes de la cellule des identifiants doivent être VIDES à l'aveugle)
    for ligne in sa.splitlines():
        st = ligne.strip()
        if st.startswith(("CLIENT_ID =", "CLIENT_SECRET =", "REFRESH_TOKEN =")):
            valeur = st.split("=", 1)[1].strip()
            if valeur not in ('""', "''"):
                raise SystemExit("[épreuve 3] INVARIANT-ROMPU : un identifiant vit à la copie aveugle !")
    print("[épreuve 3] l'invariant : la SEULE divergence vivante/aveugle = la cellule 6 "
          "(les TROIS constantes), aucun identifiant à l'aveugle — VERT")
    # 4 · les gardes nommées présentes
    src_viv = "\n".join("".join(c["source"]) for c in viv["cells"] if c["cell_type"] == "code")
    for garde in ("DISQUE-INSUFFISANT", "JETON-ROUGE", "KIT-DIVERGENT", "COMPTE-VERTS-DIVERGENT",
                  "EXEMPLE-TROP-LONG", "EXEMPLE-LONG-OOM", "ADAPTER-CONVERSION-ROUGE",
                  "BORD-MUET", "ZIP-ABSENT", "ORDRE-ROMPU", "IDENTIFIANTS-ABSENTS",
                  "RECOP-ROUGE"):
        if garde not in src_viv:
            raise SystemExit(f"[épreuve 4] GARDE-ABSENTE : {garde}")
    print("[épreuve 4] les ONZE gardes nommées présentes — VERT")
    # 5 · le pilotage : le pilote attend preuves-campagne-* au /content/kit + rapport-poste.txt
    if "preuves-campagne-entrainement-v106-" not in src_viv or "rapport-poste.txt" not in src_viv:
        raise SystemExit("[épreuve 5] PILOTAGE-ROMPU : les conventions du pilote ne sont pas tenues.")
    print("[épreuve 5] les conventions du pilote (preuves-campagne-* au kit, rapport-poste.txt) — VERT")
    print("\nLES ÉPREUVES TOUT VERT — les DEUX copies sont nées.")
    return notebooks


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "kit":
        cmd_kit()
    elif mode == "notebook":
        cmd_notebook(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
