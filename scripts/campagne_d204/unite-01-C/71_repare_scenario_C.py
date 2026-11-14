#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA RÉPARATION DU SCÉNARIO DU BRAS C (v2, le refus du 14/11 nommé) :
le terminateur de la table d'imports se lit au CHAMP Name (l'RVA NUL), JAMAIS
à la chaîne (à l'RVA 0 vit l'en-tête DOS « MZ ») ; gardes fail-closed : au
plus 64 descripteurs, aucun Name hors image. La pièce, le source C, le
lanceur et les témoins demeurant INTACTS octet pour octet."""
import ast
import hashlib
import pathlib
import py_compile
import textwrap

KIT_V1 = pathlib.Path("/home/z/my-project/download/nouveau-run/"
                      "kit-unite-loupe-01-C-20261114")
V1 = KIT_V1 / "scenario-unite01C.py"
SORTIE = pathlib.Path("/home/z/my-project/work/kit_v2")
SORTIE.mkdir(parents=True, exist_ok=True)

src = V1.read_text(encoding="utf-8")
sha_v1 = hashlib.sha256(V1.read_bytes()).hexdigest()
assert sha_v1.startswith("a21c5e19636b5489"), f"la pièce v1 a divergé : {sha_v1}"
print(f"[v1] scenario-unite01C.py {len(src)} o, sha256 {sha_v1[:16]}… — la base")

# ---- LE PATCH 1 : l'ouverture de la boucle -----------------------------------
AVANT_1 = """    # ---- LA RÉSOLUTION AUX SLOTS RÉELS de la table d'imports ---------------
    h_k32 = ctypes.c_void_p(k32.GetModuleHandleW("kernel32.dll"))
    slots = {}                                    # nom → l'adresse du slot
    desc = rva_imports
    while True:
        nom_dll = lire_chaine(base, lire_u32(base, desc + 12))
        if not nom_dll:
            break
        if "kernel32" in nom_dll.lower():
"""
APRES_1 = """    # ---- LA RÉSOLUTION AUX SLOTS RÉELS de la table d'imports ---------------
    # (v2 — LA RÉPARATION DU REFUS DU 14/11 : le terminateur se lit au CHAMP
    #  Name (l'RVA NUL), JAMAIS à la chaîne — à l'RVA 0 vit l'en-tête DOS
    #  « MZ », et la boucle v1 dérivait hors table jusqu'à l'access violation
    #  0x7ffa23900094 du terrain ; gardes fail-closed : au plus 64
    #  descripteurs, aucun Name hors image — REFUS nommé, jamais un plantage)
    h_k32 = ctypes.c_void_p(k32.GetModuleHandleW("kernel32.dll"))
    slots = {}                                    # nom → l'adresse du slot
    taille_image = lire_u32(base, opt + 56)       # SizeOfImage (PE32+ : +56)
    desc = rva_imports
    for _garde in range(64):
        nom_rva = lire_u32(base, desc + 12)
        if not nom_rva:                           # LE TERMINATEUR : Name NUL
            break
        if nom_rva >= taille_image:               # la garde fail-closed
            consigne(f"[T0] REFUS : un descripteur d'import pointe hors "
                     f"image (@+{nom_rva:#x}) — la pièce a divergé, rien "
                     f"ne court")
            return 2
        nom_dll = lire_chaine(base, nom_rva)
        if not nom_dll:
            break
        if "kernel32" in nom_dll.lower():
"""
assert src.count(AVANT_1) == 1, "le bloc 1 doit vivre UNE fois"
src = src.replace(AVANT_1, APRES_1)
print("[patch 1] la boucle ouverte au for gardé — le terminateur au champ Name")

# ---- LE PATCH 2 : la clôture for/else ----------------------------------------
AVANT_2 = """                j += 1
        desc += 20
    manquantes = [f for f in FEUILLES_KIT if f not in slots]
"""
APRES_2 = """                j += 1
        desc += 20
    else:
        consigne("[T0] REFUS : la table d'imports sans terminateur — la "
                 "pièce a divergé, rien ne court")
        return 2
    manquantes = [f for f in FEUILLES_KIT if f not in slots]
"""
assert src.count(AVANT_2) == 1, "le bloc 2 doit vivre UNE fois"
src = src.replace(AVANT_2, APRES_2)
print("[patch 2] la clôture for/else — la table sans terminateur = REFUS nommé")

# ---- l'écriture + les audits --------------------------------------------------
v2 = SORTIE / "scenario-unite01C.py"
v2.write_text(src, encoding="utf-8", newline="\n")
sha_v2 = hashlib.sha256(v2.read_bytes()).hexdigest()
print(f"[v2] {v2} — {len(src)} o, sha256 {sha_v2}")

py_compile.compile(str(v2), doraise=True)
print("[audit] py_compile VERT")

arbre = ast.parse(src)
boucles_gardees = [n for n in ast.walk(arbre)
                   if isinstance(n, ast.For) and isinstance(n.target, ast.Name)
                   and n.target.id == "_garde"]
assert len(boucles_gardees) == 1, \
    f"UNE boucle for _garde attendue, {len(boucles_gardees)} trouvées"
assert boucles_gardees[0].orelse, "la clause else du for (la table sans terminateur) manque"
assert isinstance(boucles_gardees[0].iter, ast.Call) \
    and boucles_gardees[0].iter.args[0].value == 64, "la garde de 64 manque"
texte_source = src
assert 'if not nom_rva:' in texte_source, "le terminateur au champ manque"
assert 'lire_chaine(base, lire_u32(base, desc + 12))' not in texte_source, \
    "la lecture-chaîne-avant-champ du v1 demeure !"
print("[audit] AST : UNE boucle for gardée, sa clause else, le champ avant la chaîne — VERT")

# ---- le diff pour la consignation ---------------------------------------------
lignes_avant = V1.read_text(encoding="utf-8").splitlines()
lignes_apres = src.splitlines()
import difflib
diff = list(difflib.unified_diff(lignes_avant, lignes_apres,
                                 "scenario-unite01C.py (v1)",
                                 "scenario-unite01C.py (v2)", lineterm=""))
(SORTIE / "DIFF-scenario-v1-v2.txt").write_text("\n".join(diff) + "\n",
                                                encoding="utf-8")
print(f"[diff] {sum(1 for l in diff if l.startswith('+') and not l.startswith('+++'))} lignes +, "
      f"{sum(1 for l in diff if l.startswith('-') and not l.startswith('---'))} lignes - "
      f"— DIFF-scenario-v1-v2.txt")
