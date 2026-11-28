#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE NOTEBOOK v1063 — L'AMENDEMENT TERRAIN.12 : TROIS cellules touchées (le
titre, le pin du kit, LA CELLULE 5), le reste BYTE-BYTE la v1062. La cellule
5 gagne LA CANE (fail-closed NOYAU-SALE : un processus CUDA-vierge exigé —
l'allocateur ne lit sa configuration qu'à sa naissance), L'AUTOCAST fp16 du
pas (la voie conçue par peft : requires_conversion faux, AUCUN cast fp32,
les adaptateurs demeurés fp32, la CE fp32), L'HYGIÈNE (empty_cache après la
charge + par exemple, le pic mesuré à chaque pas, le refus portant sa
mesure) — la mathématique du terrain.11 TELLE QUELLE (logits_to_keep, les
tronçons de 1024, la graine, l'ordre, les hyperparams). Usage :
batir_v1063.py <id-drive-du-kit-v1062>"""
import hashlib
import json
import pathlib
import sys

VIVANTE = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1063-VIVANTE.ipynb")
V1062 = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1062-VIVANTE.ipynb")
KIT_SHA = "ce8dbaecaf92604dcec71354f6e147c9208429d1c2dff7f4abbcf7179a628a55"
KIT_ID = sys.argv[1]

nb = json.loads(V1062.read_text(encoding="utf-8"))

# ══════════ CELLULE 0 — LE TITRE ══════════
c0 = "".join(nb["cells"][0]["source"])
c0 = c0.replace(
    "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v1062)",
    "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v1063)")
c0 = c0.replace(
    "l'amendement terrain.11 du kit — la perte à `logits_to_keep`, les logits "
    "du prompt jamais alloués — soigne le refus mémoire mesuré au run du "
    "28/11, le plan et le corpus demeurent byte-byte).",
    "les amendements terrain.11/12 du kit — la perte à `logits_to_keep` "
    "(les logits du prompt jamais alloués), puis la cane du processus vierge "
    "et l'autocast fp16 du pas (le chemin fp32 de peft soigné, les 912 MiB "
    "du second refus nommés) — soignent les refus mémoire mesurés aux deux "
    "runs du 28/11, le plan et le corpus demeurent byte-byte).")
nb["cells"][0]["source"] = [c0]

# ══════════ CELLULE 6 — LE PIN DU KIT ══════════
c6 = "".join(nb["cells"][6]["source"])
c6 = c6.replace(
    "# campagne 105) PUIS LE KIT D'ENTRAÎNEMENT v106 (le corpus + le plan gelé) —",
    "# campagne 105) PUIS LE KIT D'ENTRAÎNEMENT v1062 (le corpus + le plan gelé\n"
    "# + les amendements terrain.11/12) —")
c6 = c6.replace(
    '''    {   # le corpus + le plan gelé + L'AMENDEMENT TERRAIN.11 de l'entraînement
        "nom": "TRIADE_kit_entrainement_v1061.zip",
        "sha256": "f5a2382b0204d9872a1f44695bfa1f83c9b79adc53754102924c61e144a64b1f",
        "id_drive": "1oFnEsGy6JV_JRw2h6MugHurxfeNCuH3T",
        "dest": pathlib.Path("/content/kit-entrainement"),
    },''',
    f'''    {{   # le corpus + le plan gelé + LES AMENDEMENTS terrain.11/12 de l'entraînement
        "nom": "TRIADE_kit_entrainement_v1062.zip",
        "sha256": "{KIT_SHA}",
        "id_drive": "{KIT_ID}",
        "dest": pathlib.Path("/content/kit-entrainement"),
    }},''')
nb["cells"][6]["source"] = [c6]

# ══════════ CELLULE 10 — LA CELLULE 5 (l'entraînement) ══════════
c10 = "".join(nb["cells"][10]["source"])

# (a) l'en-tête : l'amendement terrain.12 nommé
c10 = c10.replace(
    """# signal), le plan gelé demeure LA LOI.
import json""",
    """# signal), le plan gelé demeure LA LOI.
# L'AMENDEMENT TERRAIN.12 (AMENDEMENT-V1063-TERRAIN12.md du kit) : le second
# refus du 28/11 décomposé — les 912 MiB à la ligne du matmul LoRA, LE CHEMIN
# FP32 DE PEFT (l'entrée de chaque couche LoRA castée au fp32 des adaptateurs
# : le [12 615 × 18 944] fp32) et l'allocateur né sans ses segments
# extensibles sur le noyau recyclé (1,64 Gio réservés-non-alloués, la marge
# mangée). LE GESTE : LA CANE (un processus CUDA-vierge exigé, NOYAU-SALE le
# refus nommé) + l'AUTOCAST fp16 du pas (LA VOIE CONÇUE PAR PEFT — aucun
# cast fp32, les adaptateurs demeurés fp32, la CE fp32) + l'hygiène
# (empty_cache, le pic mesuré à chaque pas).
import json""")

# (b) la variable d'environnement POSÉE (plus setdefault — le deterministic)
c10 = c10.replace(
    'os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")',
    'os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"')

# (c) LA CANE juste après l'import de l'enveloppe (avant toute allocation CUDA)
c10 = c10.replace(
    '''from moteur_campagne import enveloppe  # noqa: E402  (la pièce vivante)

# ── les constantes du plan gelé (§ 3) ──''',
    '''from moteur_campagne import enveloppe  # noqa: E402  (la pièce vivante)

# ── LA CANE DU TERRAIN.12 (fail-closed) : l'allocateur ne lit sa configuration
# qu'à SA NAISSANCE — la première allocation CUDA du processus. Un noyau
# recyclé (le run précédent) porte un allocateur né SANS segments extensibles
# et ne relira JAMAIS sa configuration : la mesure du second refus du 28/11 —
# 1,64 Gio réservés-non-alloués, 0,34 Gio libre, 912 MiB refusés — la marge
# du budget mangée par la fragmentation. Le refus AVANT la marche, jamais
# deux heures après.
if torch.cuda.memory_stats().get("allocated_bytes.all.peak", 0) > 0:
    raise SystemExit(
        "NOYAU-SALE : CUDA a déjà alloué dans CE processus (le run précédent) — "
        "l'allocateur est né sans segments extensibles et ne relira jamais sa "
        "configuration. Exécution → Redémarrer la session, PUIS Tout exécuter "
        "(le cache du modèle demeure au disque, aucun re-téléchargement). "
        "La mesure : 1,64 Gio réservés-non-alloués au refus du 28/11.")
print("[sft] la cane : le processus est CUDA-vierge — l'allocateur naîtra sous "
      "expandable_segments (le second refus du 28/11 nommé au kit).")

# ── les constantes du plan gelé (§ 3) ──''')

# (d) la charge : dtype (la dépréciation nommée) + l'hygiène après la charge
c10 = c10.replace(
    """    MODELE, quantization_config=bnb, device_map={"": 0},
    torch_dtype=torch.float16, attn_implementation="sdpa")""",
    """    MODELE, quantization_config=bnb, device_map={"": 0},
    dtype=torch.float16, attn_implementation="sdpa")   # dtype — la dépréciation de torch_dtype nommée au terrain.12""")
c10 = c10.replace(
    "model.print_trainable_parameters()\n",
    "model.print_trainable_parameters()\n"
    "torch.cuda.empty_cache()   # le charge du modèle fragmente le bassin — rendu au GPU (terrain.12)\n")

# (e) LA BOUCLE : l'autocast + l'hygiène + le pic — la mathématique TELLE QUELLE
c10 = c10.replace(
    '''            ids = e["p"] + e["c"]
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
                           "triple": e["triple"], "perte": round(val, 5)})''',
    '''            torch.cuda.reset_peak_memory_stats()
            torch.cuda.empty_cache()   # terrain.12 : la marge rendue au GPU avant chaque exemple
            ids = e["p"] + e["c"]
            t = torch.tensor([ids], device="cuda")
            cibles = torch.tensor(e["c"], device="cuda")
            # L'AUTOCAST DU TERRAIN.12 : LA VOIE CONÇUE PAR PEFT (bnb.py:500,
            # requires_conversion = not is_autocast_enabled() — FAUX sous autocast) :
            # le chemin LoRA court au fp16 du bord, AUCUN [S × 18 944] fp32 n'est
            # plus alloué (le 912 MiB du refus), les ADAPTATEURS DEMEURENT fp32
            # (les gradients fp32, l'entraînement stable) ; la CE demeure fp32
            # (le .float() explicite) ; le checkpoint REJOUE l'autocast à la
            # recomputation (prouvé au bac). La mathématique TELLE QUELLE.
            with torch.autocast("cuda", dtype=torch.float16):
                out = model(input_ids=t, logits_to_keep=len(e["c"]) + 1)
                lg = out.logits[0, :-1, :]   # [C, V] — prédit exactement les cibles
                somme = torch.zeros((), device="cuda")
                for j in range(0, lg.shape[0], TRONCON):
                    somme = somme + checkpoint(ce_troncon, lg[j:j + TRONCON],
                                               cibles[j:j + TRONCON], use_reentrant=False)
                perte = somme / len(e["c"])   # le « mean » aux non-ignorés (la même perte)
            (perte / ACCUM).backward()
            val = float(perte)
            pic = torch.cuda.max_memory_allocated() / 2**30
            courbe.append({"pas": len(courbe) + 1, "epoque": epo + 1,
                           "triple": e["triple"], "perte": round(val, 5),
                           "pic_gio": round(pic, 2)})''')

# (f) le journal vivant porte le pic + le socle rendu
c10 = c10.replace(
    '''            if len(courbe) % 4 == 0 or len(courbe) == n_pas:
                print(f"[sft] époque {epo + 1}/{EPOQUES} · pas {len(courbe)}/{n_pas} · "
                      f"perte {val:.4f} · {time.time() - t0:.0f} s", flush=True)''',
    '''            if len(courbe) % 4 == 0 or len(courbe) == n_pas:
                print(f"[sft] époque {epo + 1}/{EPOQUES} · pas {len(courbe)}/{n_pas} · "
                      f"perte {val:.4f} · pic {pic:.2f} Gio · {time.time() - t0:.0f} s",
                      flush=True)
            del t, cibles, out, lg, somme, perte   # terrain.12 : le socle rendu avant l'exemple suivant''')

# (g) le refus porte SA MESURE (le pic au message même)
c10 = c10.replace(
    '''except torch.cuda.OutOfMemoryError:
    raise SystemExit(f"EXEMPLE-LONG-OOM : le T4 n'a pas tenu l'exemple "
                     f"{e['triple']} ({len(ids)} jetons) — le plan gelé nomme le refus ; "
                     f"la voie de repli (l'exclusion nommée) est AU LABO, jamais au bord.")''',
    '''except torch.cuda.OutOfMemoryError:
    pic = torch.cuda.max_memory_allocated() / 2**30
    raise SystemExit(f"EXEMPLE-LONG-OOM : le T4 n'a pas tenu l'exemple "
                     f"{e['triple']} ({len(ids)} jetons, le pic {pic:.2f} Gio) — le plan "
                     f"gelé nomme le refus ; la voie de repli (l'exclusion nommée) est "
                     f"AU LABO, jamais au bord.")''')

# (h) le registre : l'amendement étendu + la courbe porte le pic
c10 = c10.replace(
    '''    "amendement": {"terrain": "terrain.11", "perte": "logits_to_keep + CE par "
                   "tronçons de 1024 — la réponse seule, LA MÊME MATHÉMATIQUE "
                   "(la preuve au bac : la perte au ulp du fp32, EXACTEMENT "
                   "égale au vrai modèle, le même signal)"},''',
    '''    "amendement": {"terrain": "terrain.11 + terrain.12",
                   "perte": "logits_to_keep + CE par tronçons de 1024 — la réponse "
                   "seule, LA MÊME MATHÉMATIQUE (la preuve au bac : la perte au ulp "
                   "du fp32, EXACTEMENT égale au vrai modèle, le même signal)",
                   "memoire": "l'autocast fp16 du pas (le chemin LoRA de peft sans "
                   "casts fp32, les adaptateurs demeurés fp32 — la preuve au bac : "
                   "la perte 0,0 au réel, les gradients à 5e-03 relatif, cosinus "
                   "0,999998) + la cane NOYAU-SALE (l'allocateur né vierge sous "
                   "expandable_segments) + empty_cache par exemple, le pic mesuré "
                   "à chaque pas (pic_gio à la courbe)"},''')

nb["cells"][10]["source"] = [c10]
VIVANTE.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ══════════ LES ÉPREUVES ══════════
print("── LES ÉPREUVES DU v1063 ──")

# 1 · la structure du notebook + la compilation de chaque cellule de code
import nbformat
nbf = nbformat.reads(VIVANTE.read_text(encoding="utf-8"), as_version=4)
nbformat.validate(nbf)
for i, cell in enumerate(nbf.cells):
    if cell.cell_type == "code":
        compile(cell.source, f"<cellule {i}>", "exec")
print("[1] nbformat VALIDE · toutes les cellules compilent — VERT")

# 2 · l'invariant : SEULES les cellules [0, 6, 10] divergent de la v1062
v1062 = json.loads(V1062.read_text(encoding="utf-8"))
divergentes = [i for i, (a, b) in enumerate(zip(v1062["cells"], nb["cells"]))
               if "".join(a["source"]) != "".join(b["source"])]
if divergentes != [0, 6, 10]:
    raise SystemExit(f"INVARIANT-ROMPU : cellules divergentes {divergentes} != [0, 6, 10]")
if len(v1062["cells"]) != len(nb["cells"]):
    raise SystemExit("INVARIANT-ROMPU : le nombre de cellules a changé")
print("[2] l'invariant des cellules [0, 6, 10] TENU — le reste BYTE-BYTE la v1062")

# 3 · la mathématique du plan INCHANGÉE (les constantes et les lignes de perte)
for marque in ('MAX_LEN = 13000', 'R, ALPHA, DROPOUT = 16, 32, 0.05',
               'EPOQUES, ACCUM, LR = 3, 4, 1.5e-5', 'SEED = 20261128',
               'TRONCON = 1024', 'logits_to_keep=len(e["c"]) + 1',
               'perte = somme / len(e["c"])', '(perte / ACCUM).backward()',
               'exemples.sort(key=lambda e: -(len(e["p"]) + len(e["c"])))',
               'CIBLES = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]'):
    if marque not in c10:
        raise SystemExit(f"MATH-ROMPUE : {marque} absent de la cellule 5")
print("[3] la mathématique du plan gelé INCHANGÉE — les constantes, la perte, l'ordre")

# 4 · les marques du remède terrain.12 présentes
for marque in ('torch.autocast("cuda", dtype=torch.float16)', 'NOYAU-SALE',
               'expandable_segments:True', 'torch.cuda.empty_cache()',
               'reset_peak_memory_stats', 'max_memory_allocated', 'pic_gio',
               'EXEMPLE-TROP-LONG', 'EXEMPLE-LONG-OOM', 'dtype=torch.float16',
               'allocated_bytes.all.peak'):
    if marque not in c10:
        raise SystemExit(f"REMÈDE-ABSENT : {marque} manque à la cellule 5")
print("[4] les marques du remède TOUTES PRÉSENTES — la cane, l'autocast, l'hygiène, la mesure")

# 5 · les pins : le poste v102 INTACT + le kit v1062 épinglé (sha + id)
if ('"sha256": "60962d74a06476b5746112d66ac94edfdf5f8b19d475cda30f5efe7e05d431b7"'
        not in c6):
    raise SystemExit("PIN-ROMPU : le poste v102 doit demeurer byte-byte")
if KIT_SHA not in c6 or KIT_ID not in c6 or "TRIADE_kit_entrainement_v1062.zip" not in c6:
    raise SystemExit("PIN-ROMPU : le kit v1062 mal épinglé")
if "TRIADE_kit_entrainement_v1061" in c6:
    raise SystemExit("PIN-ROMPU : le vieux pin v1061 demeure")
print("[5] les pins TENU : le poste v102 INTACT, le kit v1062 épinglé (sha + id)")

# 6 · le vieux chemin mort, le nouveau vivant
if "torch_dtype=" in c10:
    raise SystemExit("VIEUX-CHEMIN : torch_dtype demeure (la dépréciation nommée)")
if 'with torch.autocast("cuda", dtype=torch.float16):' not in c10:
    raise SystemExit("NOUVEAU-CHEMIN : le geste d'autocast manque à la boucle")
if "L'AUTOCAST DU TERRAIN.12" not in c10:
    raise SystemExit("NOUVEAU-CHEMIN : le commentaire d'autocast manque à la boucle")
print("[6] le vieux chemin MORT (torch_dtype), le nouveau VIVANT (l'autocast)")

print()
sha = hashlib.sha256(VIVANTE.read_bytes()).hexdigest()
print(f"LE NOTEBOOK v1063 : {VIVANTE.name} ({VIVANTE.stat().st_size} o)")
print(f"sha256 : {sha}")
