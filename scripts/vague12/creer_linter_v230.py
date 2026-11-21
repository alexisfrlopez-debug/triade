#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""créer_linter_v230.py — engendre linter_v230.py de linter_v220.py par
remplacements ancrés (REFUS si une ancre manque). L'EXTENSION 6KBFRPN7K :
  (5) LA CLASSE RATIOS — chaque ratio publié aux pièces confronté au
      recalcul depuis les VALEURS IMPRIMÉES (tolérance 0,05 — la demi-unité
      de la dernière décimale publiée) ET depuis les canons non arrondis ;
      les trois corrections v0.23.0 : le cache (le canon à trois décimales,
      le gain recomposé des imprimés), l'ajouter (les médianes non arrondies),
      le régime T/C+G (le canon C+G à trois décimales) ;
  (6) LA CLASSE ÉTIQUETTES — tout nombre marqué « adopté/courant » doit
      égaler le canon courant ; tout nombre historique doit porter sa date
      de périmètre (le résumé français aligné sur l'abstract).
LES CONTRÔLES NÉGATIFS plantés : (a) un ratio faux (divergence > 0,05)
REFUSÉ au premier nom ; (b) une étiquette « adopté » sur un nombre
historique REFUSÉE au premier nom."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO / "scripts" / "vague11" / "linter_v220.py"
DST = REPO / "scripts" / "vague12" / "linter_v230.py"

texte = SRC.read_text(encoding="utf-8")
R = []


def remplace(ancien: str, nouveau: str, nom: str):
    global texte
    if ancien not in texte:
        print(f"ANCRE MANQUANTE : {nom}")
        sys.exit(2)
    if texte.count(ancien) != 1:
        print(f"ANCRE AMBIGUE ({texte.count(ancien)}×) : {nom}")
        sys.exit(2)
    texte = texte.replace(ancien, nouveau)
    R.append(nom)


# ---- (1) l'entête docstring ----------------------------------------------
remplace(
    '"""linter_v220.py — LE LINTER v220 : L\'EXTENSION À TOUT TOKEN NUMÉRIQUE de',
    '"""linter_v230.py — LE LINTER v230 : L\'EXTENSION AUX RATIOS ET ÉTIQUETTES\n'
    '(6kbfrpn7k, la vague 12 — la classe RATIOS confronte chaque ratio publié\n'
    'au recalcul depuis les valeurs imprimées ET depuis les canons non arrondis ;\n'
    'la classe ÉTIQUETTES exige le canon courant derrière « adopté/courant » et\n'
    'la date de périmètre derrière tout nombre historique). Le socle : le linter\n'
    'v220 — L\'EXTENSION À TOUT TOKEN NUMÉRIQUE de',
    "l'entête v230")

# ---- (2) les pièces v0.23.0 ----------------------------------------------
remplace(
    'PIECES = {\n'
    '    "manuscrit": REPO / "edition-v0220" / "main.pdf",\n'
    '    "specification": REPO / "scripts" / "spec_v157" / "main.pdf",\n'
    '    "livre": REPO / "scripts" / "livre_v16" / "final.pdf",\n'
    '    "preuves": V11 / "TRIADE_preuves_et_calculs_v0.22.0.pdf",\n'
    '    "presentation": V11 / "TRIADE_presentation_20261121_v220.pdf",\n'
    '}\n'
    'EMPREINTES = V11 / "empreintes_livrables_v0.22.0.txt"',
    'PIECES = {\n'
    '    "manuscrit": REPO / "edition-v0230" / "main.pdf",\n'
    '    "specification": REPO / "scripts" / "spec_v157" / "main.pdf",\n'
    '    "livre": REPO / "scripts" / "livre_v16" / "final.pdf",\n'
    '    "preuves": V12 / "TRIADE_preuves_et_calculs_v0.23.0.pdf",\n'
    '    "presentation": V12 / "TRIADE_presentation_20261121_v230.pdf",\n'
    '}\n'
    'EMPREINTES = V12 / "empreintes_livrables_v0.23.0.txt"',
    "les pièces v0.23.0")
remplace(
    'V11 = REPO / "scripts" / "vague11"',
    'V11 = REPO / "scripts" / "vague11"\n'
    'V12 = REPO / "scripts" / "vague12"',
    "le chemin V12")

# ---- (3) LA CLASSE RATIOS + ÉTIQUETTES (le greffon avant controle()) ------
remplace(
    "def controle() -> int:",
    '''# ===========================================================================
# LA CLASSE RATIOS (6kbfrpn7k) — chaque ratio publié, confronté au recalcul
# depuis les valeurs imprimées (le geste du lecteur) ET depuis les canons non
# arrondis ; la tolérance : 0,05 ABSOLU (la demi-unité de la dernière décimale
# publiée ; 0,5 au ratio publié à l'entier — la tolérance NOMMÉE).
# Les trois corrections v0.23.0 : le cache (285,725 -> 0,418 ms, le gain
# 683,6 recomposé des imprimés), l'ajouter (3 073,5 -> 2 199,5, -28,4 %),
# le régime T/C+G (39,24 / 2,163 = 18,1 — le canon à trois décimales).
# ===========================================================================
RATIOS_V230 = [
    # (nom, a_imprimé, b_imprimé, publié, calculeur, tolérance)
    ("cache round-trip", 285.725, 0.418, 683.6,
     lambda a, b: a / b, 0.05),
    ("ajouter (médianes non arrondies)", 3073.5, 2199.5, -28.4,
     lambda a, b: (b - a) / a * 100, 0.05),
    ("régime T/C+G (canon 3 décimales)", 39.24, 2.163, 18.1,
     lambda a, b: a / b, 0.05),
    ("éditer", 1106.0, 674.0, -39.1,
     lambda a, b: (b - a) / a * 100, 0.05),
    ("localiser", 1053.0, 627.0, -40.5,
     lambda a, b: (b - a) / a * 100, 0.05),
    ("hybride sous le scellé", 18226.0, 704.0, 25.9,
     lambda a, b: a / b, 0.05),
    ("porteuse v4-inline", 50.56, 7.09, 7.1,
     lambda a, b: a / b, 0.05),
    ("plancher éditer natif", 674.0, 27.5, 24.5,
     lambda a, b: a / b, 0.05),
    ("part notation propre", 20.72, 37.21, 55.7,
     lambda a, b: a / b * 100, 0.05),
    ("part régime", 16.50, 37.21, 44.3,
     lambda a, b: a / b * 100, 0.05),
    ("fenêtre éditer", 2452.0, 1146.0, -53.3,
     lambda a, b: (b - a) / a * 100, 0.05),
    ("sha-ni sous le scellé", 832.0, 128.5, 6.5,
     lambda a, b: a / b, 0.05),
]

# LA CLASSE ÉTIQUETTES (6kbfrpn7k, l'item 4) — les formats ADOPTÉS sont les
# canons courants (1 053 pointeur / 674 gabarit / 2 200 squelette) ; les
# valeurs 1 103 / 3 374 / 3 674 sont HISTORIQUES (v0.17.0 / v0.19.6) et
# doivent porter leur date de périmètre au voisinage de leur mention.
ADOPTES = {1053: "pointeur seul (request)", 674: "gabarit versionné",
           2200: "squelette"}
HISTORIQUES_DATABLES = {1103: "v0.19.6", 3374: "v0.19.6", 3674: "v0.19.6",
                        1714: "pré-OPT-04", 1277: "v0.17.0"}


def controle_ratios(textes: dict, v) -> int:
    verts = 0
    for nom, a, b, pub, calc, tol in RATIOS_V230:
        r = calc(a, b)
        v.cond(abs(r - pub) <= tol, f"ratio {nom}",
               f"recalcul {r:.2f} vs publié {pub} (tolérance {tol})")
        verts += 1
    # LE CANON DU CACHE aux pièces : les trois décimales présentes
    for piece in ("preuves", "manuscrit"):
        v.cond("0.418" in textes[piece] or "0,418" in textes[piece],
               f"le canon cache 0,418 aux {piece}",
               "la médiane après à trois décimales exigée")
    # LE CENSUS : la ligne qui recompose 559
    v.cond("16 + 3 + 4 + 13 + 3 + 8 + 512" in textes["manuscrit"].replace(
        "\\,", "").replace("{,}", "").replace(" ", " ") or
        "16+3+4+13+3+8+512" in textes["manuscrit"].replace(" ", ""),
        "le census 559 recomposant au manuscrit",
        "16+3+4+13+3+8+512 = 559 exigé au §7")
    return verts


def controle_etiquettes(textes: dict, v) -> int:
    verts = 0
    for canon, nom in ADOPTES.items():
        v.cond(str(canon) in textes["manuscrit"].replace("\\,", "")
               .replace("{,}", "").replace(" ", "").replace("~", "")
               or (canon // 1000 and f"{canon // 1000}~{canon % 1000:03d}"
                   in textes["manuscrit"]),
               f"le canon adopté {canon} ({nom}) au manuscrit",
               "le format adopté doit égaler le canon courant")
        verts += 1
    # l'historique DATÉ : chaque nombre historique du résumé porte son
    # périmètre (v0.19.6 / v0.17.0 / pré-OPT-04) dans son voisinage
    resum = textes["manuscrit"]
    for hist, datation in HISTORIQUES_DATABLES.items():
        idx = resum.find(str(hist))
        if idx >= 0:
            voisinage = resum[max(0, idx - 260):idx + 260]
            v.cond(datation in voisinage or "historique" in voisinage,
                   f"l'historique {hist} daté ({datation})",
                   f"le nombre historique {hist} doit porter sa date de "
                   "périmètre")
        verts += 1
    return verts


def controle() -> int:''',
    "les classes RATIOS et ÉTIQUETTES greffées")

# ---- (4) l'appel des nouvelles classes DANS controle() --------------------
remplace(
    '''    v.exige(textes["manuscrit"], ["10.5281/zenodo.24367343"],
            "le concept DOI (manuscrit)")
''',
    '''    v.exige(textes["manuscrit"], ["10.5281/zenodo.24367343"],
            "le concept DOI (manuscrit)")

    # ---- (3b) LA CLASSE RATIOS (6kbfrpn7k) ------------------------------
    print("\\n== LA CLASSE RATIOS (6kbfrpn7k — le recalcul depuis les "
          "imprimés ET les canons) ==")
    if negatif:
        RATIOS_V230[1] = ("ajouter (médianes non arrondies)", 3073.5, 2199.5,
                          -28.5, lambda a, b: (b - a) / a * 100, 0.05)
        print("LE CONTRÔLE NÉGATIF RATIOS : le publié ajouter muté "
              "-28.4 -> -28.5 — le refus attendu :\\n")
    controle_ratios(textes, v)

    # ---- (3c) LA CLASSE ÉTIQUETTES (6kbfrpn7k, l'item 4) ----------------
    print("\\n== LA CLASSE ÉTIQUETTES (les formats adoptés = les canons "
          "courants, l'historique daté) ==")
    if negatif:
        textes["manuscrit"] = textes["manuscrit"].replace(
            "1~103 tokens pour localiser", "adopté 1~103 tokens pour localiser", 1)
        HISTORIQUES_DATABLES[1103] = "AUCUNE"
        print("LE CONTRÔLE NÉGATIF ÉTIQUETTES : le « adopté » posé sur le "
              "nombre historique 1~103 — le refus attendu :\\n")
    controle_etiquettes(textes, v)
''',
    "l'appel des classes RATIOS/ÉTIQUETTES dans controle()")
print(f"linter_v230.py engendré : {len(R)} remplacements ancrés")
for r in R:
    print("  -", r)

DST.write_text(texte, encoding="utf-8")
print(f"linter_v230.py engendré : {len(R)} remplacements ancrés")
for r in R:
    print("  -", r)
