#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE NOTEBOOK v1064 — L'AMENDEMENT TERRAIN.13 : TROIS cellules touchées (le
titre, le pin du kit, LA CELLULE 5), le reste BYTE-BYTE la v1063. La cellule
5 gagne LE REPLI NOMMÉ DU PLAN § 7 (l'exclusion de ajouter-v3-i26111705-t1
seul — le monstre refusé à SA SECONDE VISITE [pas 18, époque 2] : le
persistant AdamW + les gradients accumulés + la fragmentation mangeant la
marge ; le tampon refusé de 456.00 MiB = le [12 615 × 18 944] fp16, la
moitié exacte du pied fp32 du terrain.12 — l'autocast a MORDU), fail-closed
(EXCLUSION-NOMMÉE-DIVERGENTE), le corpus FICHIER byte-byte, la marche
3 × 16 = 48 pas / 12 pas d'optimiseur EXACTS — la mathématique du
terrain.11/12 TELLE QUELLE (logits_to_keep, les tronçons de 1024, la graine,
l'ordre des longs d'abord parmi les retenus, les hyperparams). Usage :
batir_v1064.py <id-drive-du-kit-v1063>"""
import hashlib
import json
import pathlib
import sys

VIVANTE = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1064-VIVANTE.ipynb")
V1063 = pathlib.Path("/home/z/my-project/work/Entrainement-Colab-v1063-VIVANTE.ipynb")
KIT_SHA = "992f9e6b893edbd2fd89701f61220a45664c951c2f32f5f297e52d76a4605b48"
KIT_ID = sys.argv[1]

nb = json.loads(V1063.read_text(encoding="utf-8"))

# ══════════ CELLULE 0 — LE TITRE ══════════
c0 = "".join(nb["cells"][0]["source"])
c0 = c0.replace(
    "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v1063)",
    "# TRIADE — LE KIT D'ENTRAÎNEMENT COLAB — **0 CLIC** (v1064)")
c0 = c0.replace(
    "**QLoRA SFT** sur les 17 VERTS du corpus",
    "**QLoRA SFT** sur les VERTS du corpus (16 à la marche — le repli nommé du plan § 7, terrain.13)")
c0 = c0.replace(
    "les amendements terrain.11/12 du kit — la perte à `logits_to_keep` "
    "(les logits du prompt jamais alloués), puis la cane du processus vierge "
    "et l'autocast fp16 du pas (le chemin fp32 de peft soigné, les 912 MiB "
    "du second refus nommés) — soignent les refus mémoire mesurés aux deux "
    "runs du 28/11, le plan et le corpus demeurent byte-byte).",
    "les amendements terrain.11/12/13 du kit — la perte à `logits_to_keep` "
    "(les logits du prompt jamais alloués), la cane du processus vierge et "
    "l'autocast fp16 du pas (le chemin fp32 de peft soigné), puis LE REPLI "
    "NOMMÉ du plan § 7 (le monstre refusé à sa seconde visite exclu par nom "
    "— le corpus fichier demeure byte-byte) — soignent les refus mémoire "
    "mesurés aux trois runs du 28/11, le plan gelé demeure LA LOI).")
nb["cells"][0]["source"] = [c0]

# ══════════ CELLULE 6 — LE PIN DU KIT ══════════
c6 = "".join(nb["cells"][6]["source"])
c6 = c6.replace(
    "# campagne 105) PUIS LE KIT D'ENTRAÎNEMENT v1062 (le corpus + le plan gelé\n"
    "# + les amendements terrain.11/12) —",
    "# campagne 105) PUIS LE KIT D'ENTRAÎNEMENT v1063 (le corpus + le plan gelé\n"
    "# + les amendements terrain.11/12/13) —")
c6 = c6.replace(
    '''    {   # le corpus + le plan gelé + LES AMENDEMENTS terrain.11/12 de l'entraînement
        "nom": "TRIADE_kit_entrainement_v1062.zip",
        "sha256": "ce8dbaecaf92604dcec71354f6e147c9208429d1c2dff7f4abbcf7179a628a55",
        "id_drive": "1_P3hsysyE6fZGAdDP3caPk_OWXxHq66e",
        "dest": pathlib.Path("/content/kit-entrainement"),
    },''',
    f'''    {{   # le corpus + le plan gelé + LES AMENDEMENTS terrain.11/12/13 de l'entraînement
        "nom": "TRIADE_kit_entrainement_v1063.zip",
        "sha256": "{KIT_SHA}",
        "id_drive": "{KIT_ID}",
        "dest": pathlib.Path("/content/kit-entrainement"),
    }},''')
nb["cells"][6]["source"] = [c6]

# ══════════ CELLULE 10 — LA CELLULE 5 (l'entraînement) ══════════
c10 = "".join(nb["cells"][10]["source"])

# (a) la première ligne : les 17 VERTS du corpus → les retenus du repli
c10 = c10.replace(
    "# CELLULE 5 — L'ENTRAÎNEMENT QLoRA SFT : les 17 VERTS du corpus, la perte sur",
    "# CELLULE 5 — L'ENTRAÎNEMENT QLoRA SFT : les VERTS du corpus (16 retenus — le\n"
    "# repli nommé du plan § 7, terrain.13), la perte sur")

# (b) l'en-tête : l'amendement terrain.13 nommé
c10 = c10.replace(
    """# (empty_cache, le pic mesuré à chaque pas).
import json""",
    """# (empty_cache, le pic mesuré à chaque pas).
# L'AMENDEMENT TERRAIN.13 (AMENDEMENT-V1064-TERRAIN13.md du kit) : le troisième
# refus du 28/11 — la v1063 au processus CUDA-vierge (la cane VERTE, l'allocateur
# né sous expandable_segments), l'époque 1 ENTIÈRE tenue (17/17, le monstre au
# pas 1 compris — les pics décroissants du journal le disent), le refus à LA
# SECONDE VISITE du monstre (le pas 18, l'époque 2 : le persistant AdamW
# [≈ 0,31 Gio, né au premier pas d'optimiseur] + les gradients accumulés +
# la fragmentation [1,16 Gio réservés-non-alloués] mangent la marge — le
# tampon refusé de 456.00 MiB est le [12 615 × 18 944] fp16, LA MOITIÉ du
# pied fp32 du terrain.12 : l'autocast a MORDU). LE GESTE : LE REPLI NOMMÉ DU
# PLAN § 7 — l'exclusion de l'unique nommé, la marche 48 pas / 12 pas
# d'optimiseur EXACTS (l'horloge identique au 51-pas), le corpus FICHIER
# byte-byte (l'exclusion vit à la cellule, PAR NOM, jamais au fichier).
import json""")

# (c) LE REPLI NOMMÉ — entre la tokenisation et le tri (les longs d'abord)
c10 = c10.replace(
    '''    exemples.append({"triple": d["triple"], "p": p, "c": c})
exemples.sort(key=lambda e: -(len(e["p"]) + len(e["c"])))   # les longs d'abord''',
    '''    exemples.append({"triple": d["triple"], "p": p, "c": c})

# ── LE REPLI NOMMÉ DU PLAN § 7 (l'amendement terrain.13) : l'exclusion de
# l'unique refusé — ajouter-v3-i26111705-t1 (12 615 jetons = P 8 293 + C 4 322),
# le monstre refusé à SA SECONDE VISITE (le pas 18, l'époque 2 : pic 13.58 Gio,
# 456.00 MiB refusés — le [12 615 × 18 944] fp16, la moitié exacte du pied fp32
# du terrain.12 : l'autocast a mordu). À la 1re visite (le bassin vierge, pas
# d'état) il tenait avec ~0,9 Gio de marge ; à la seconde, l'état AdamW (0,31
# Gio, que la marche porte désormais pour toujours) + les gradients accumulés +
# la fragmentation ont mangé la marge — et le plan (§ 3 : 3 époques) le
# revisite encore. LE NOMMÉ SEUL : t3/t2 (12 021/12 019) TENUS à leur 1re
# visite, jamais nommés par la mesure — le labo n'exclut pas ce que la mesure
# n'a pas refusé. Le corpus FICHIER demeure byte-byte (17 verts au fichier,
# 16 à la marche) — l'exclusion vit ICI, jamais au fichier.
EXCLUS_NOMMÉS = {"ajouter-v3-i26111705-t1"}   # le refus mesuré du pas 18 — jamais un autre
n_avant = len(exemples)
exemples = [e for e in exemples if e["triple"] not in EXCLUS_NOMMÉS]
if len(exemples) != n_avant - len(EXCLUS_NOMMÉS):
    raise SystemExit(
        "EXCLUSION-NOMMÉE-DIVERGENTE : le repli du plan § 7 exige le nommé au "
        "corpus (ajouter-v3-i26111705-t1, le refus mesuré au pas 18) — le corpus "
        "lu ne s'accorde pas à la mesure. Le repli ne peut pas courir sans son "
        "nommé : la mesure du terrain.13 demeure LA LOI du repli.")
print(f"[sft] LE REPLI DU PLAN § 7 (terrain.13) : {len(exemples)} exemples retenus — "
      f"{', '.join(sorted(EXCLUS_NOMMÉS))} EXCLU (le refus nommé : 12 615 jetons, "
      f"pic 13.58 Gio, 456.00 MiB refusés à la seconde visite — l'état de "
      f"l'optimiseur mangeant la marge) ; le corpus fichier demeure byte-byte "
      f"(17 verts au fichier, 16 à la marche).")
exemples.sort(key=lambda e: -(len(e["p"]) + len(e["c"])))   # les longs d'abord, PARMI LES RETENUS''')

# (d) le registre : l'amendement étendu + le repli consigné
c10 = c10.replace(
    '''    "amendement": {"terrain": "terrain.11 + terrain.12",
                   "perte": "logits_to_keep + CE par tronçons de 1024 — la réponse "
                   "seule, LA MÊME MATHÉMATIQUE (la preuve au bac : la perte au ulp "
                   "du fp32, EXACTEMENT égale au vrai modèle, le même signal)",
                   "memoire": "l'autocast fp16 du pas (le chemin LoRA de peft sans "
                   "casts fp32, les adaptateurs demeurés fp32 — la preuve au bac : "
                   "la perte 0,0 au réel, les gradients à 5e-03 relatif, cosinus "
                   "0,999998) + la cane NOYAU-SALE (l'allocateur né vierge sous "
                   "expandable_segments) + empty_cache par exemple, le pic mesuré "
                   "à chaque pas (pic_gio à la courbe)"},''',
    '''    "amendement": {"terrain": "terrain.11 + terrain.12 + terrain.13",
                   "perte": "logits_to_keep + CE par tronçons de 1024 — la réponse "
                   "seule, LA MÊME MATHÉMATIQUE (la preuve au bac : la perte au ulp "
                   "du fp32, EXACTEMENT égale au vrai modèle, le même signal)",
                   "memoire": "l'autocast fp16 du pas (le chemin LoRA de peft sans "
                   "casts fp32, les adaptateurs demeurés fp32 — la preuve au bac : "
                   "la perte 0,0 au réel, les gradients à 5e-03 relatif, cosinus "
                   "0,999998) + la cane NOYAU-SALE (l'allocateur né vierge sous "
                   "expandable_segments) + empty_cache par exemple, le pic mesuré "
                   "à chaque pas (pic_gio à la courbe)",
                   "repli": "l'exclusion nommée du plan § 7 (terrain.13) — "
                   "ajouter-v3-i26111705-t1 seul, le monstre refusé à sa seconde "
                   "visite (pas 18 : pic 13.58 Gio, 456.00 MiB refusés) ; le "
                   "corpus fichier byte-byte (17 verts au fichier, 16 retenus), "
                   "la marche 48 pas / 12 pas d'optimiseur exacts, l'horloge "
                   "identique, le fail-closed EXCLUSION-NOMMÉE-DIVERGENTE"},''')

nb["cells"][10]["source"] = [c10]
VIVANTE.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ══════════ LES ÉPREUVES ══════════
print("── LES ÉPREUVES DU v1064 ──")

# 1 · la structure du notebook + la compilation de chaque cellule de code
import nbformat
nbf = nbformat.reads(VIVANTE.read_text(encoding="utf-8"), as_version=4)
nbformat.validate(nbf)
for i, cell in enumerate(nbf.cells):
    if cell.cell_type == "code":
        compile(cell.source, f"<cellule {i}>", "exec")
print("[1] nbformat VALIDE · toutes les cellules compilent — VERT")

# 2 · l'invariant : SEULES les cellules [0, 6, 10] divergent de la v1063
v1063 = json.loads(V1063.read_text(encoding="utf-8"))
divergentes = [i for i, (a, b) in enumerate(zip(v1063["cells"], nb["cells"]))
               if "".join(a["source"]) != "".join(b["source"])]
if divergentes != [0, 6, 10]:
    raise SystemExit(f"INVARIANT-ROMPU : cellules divergentes {divergentes} != [0, 6, 10]")
if len(v1063["cells"]) != len(nb["cells"]):
    raise SystemExit("INVARIANT-ROMPU : le nombre de cellules a changé")
print("[2] l'invariant des cellules [0, 6, 10] TENU — le reste BYTE-BYTE la v1063")

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

# 4 · les marques du repli terrain.13 + le remède terrain.12 conservé
for marque in ('EXCLUS_NOMMÉS = {"ajouter-v3-i26111705-t1"}',
               'EXCLUSION-NOMMÉE-DIVERGENTE', 'LE REPLI DU PLAN § 7',
               'pic 13.58 Gio', '456.00 MiB', 'SECONDE VISITE',
               'n_pas = len(exemples) * EPOQUES', 'opt_pas = n_pas // ACCUM',
               'NOYAU-SALE', 'expandable_segments:True', 'allocated_bytes.all.peak',
               'with torch.autocast("cuda", dtype=torch.float16):',
               'torch.cuda.empty_cache()', 'reset_peak_memory_stats', 'pic_gio',
               'EXEMPLE-TROP-LONG', 'EXEMPLE-LONG-OOM', 'dtype=torch.float16'):
    if marque not in c10:
        raise SystemExit(f"REMÈDE-ABSENT : {marque} manque à la cellule 5")
print("[4] le repli nommé ET le remède terrain.12 présents — la cane, l'autocast, "
      "l'hygiène, la mesure, le fail-closed")

# 5 · LE REPLI NE NOMME QUE LE NOMMÉ : aucun autre triple au code
for autre in ("i26111705-t3", "i26111705-t2", "i26111709", "i26111714", "i26111718"):
    if autre in c10:
        raise SystemExit(f"REPLI-ÉLARGI : {autre} nommé au code — le repli exclut LE NOMMÉ seul")
print("[5] le repli nomme LE NOMMÉ SEUL — aucun autre triple au code")

# 6 · les pins : le poste v102 INTACT + le kit v1063 épinglé (sha + id)
if ('"sha256": "60962d74a06476b5746112d66ac94edfdf5f8b19d475cda30f5efe7e05d431b7"'
        not in c6):
    raise SystemExit("PIN-ROMPU : le poste v102 doit demeurer byte-byte")
if KIT_SHA not in c6 or KIT_ID not in c6 or "TRIADE_kit_entrainement_v1063.zip" not in c6:
    raise SystemExit("PIN-ROMPU : le kit v1063 mal épinglé")
if "TRIADE_kit_entrainement_v1062" in c6:
    raise SystemExit("PIN-ROMPU : le vieux pin v1062 demeure")
print("[5b] les pins TENU : le poste v102 INTACT, le kit v1063 épinglé (sha + id)")

# 7 · le registre étendu : le terrain.13 + le champ repli
if '"terrain": "terrain.11 + terrain.12 + terrain.13"' not in c10:
    raise SystemExit("REGISTRE-ROMPU : le champ terrain.13 manque")
if '"repli": "l\'exclusion nommée du plan § 7 (terrain.13)' not in c10:
    raise SystemExit("REGISTRE-ROMPU : le champ repli manque")
print("[6] le registre étendu : terrain.11 + terrain.12 + terrain.13, le repli consigné")

print()
sha = hashlib.sha256(VIVANTE.read_bytes()).hexdigest()
print(f"LE NOTEBOOK v1064 : {VIVANTE.name} ({VIVANTE.stat().st_size} o)")
print(f"sha256 : {sha}")
