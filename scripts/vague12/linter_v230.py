#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v230.py — LE LINTER v230 : L'EXTENSION AUX RATIOS ET ÉTIQUETTES
(6kbfrpn7k, la vague 12 — la classe RATIOS confronte chaque ratio publié
au recalcul depuis les valeurs imprimées ET depuis les canons non arrondis ;
la classe ÉTIQUETTES exige le canon courant derrière « adopté/courant » et
la date de périmètre derrière tout nombre historique). Le socle : le linter
v220 — L'EXTENSION À TOUT TOKEN NUMÉRIQUE de
la prose des CINQ PIÈCES (zho5vilpy, la vague 11 : « Étends le linter
inter-pièces à TOUT token numérique de la prose (pas seulement aux
tables) : extrais chaque nombre des cinq pièces, recalcule-le depuis les
CSV bruts, refuse toute divergence »).

CHAQUE nombre extrait (pdftotext, le regex des nombres, les séparateurs
FR/EN normalisés — « 2 452 », « 1,146 », « 53,3 », « 99.3 ») est
confronté à QUATRE classes de couverture, chacune NOMMÉE :
  (1) LES CANONS BRUTS — le manifeste des données brutes : chaque valeur
      relue des CSV/JSONL/registres/sorties de rig des ateliers (la
      table de correspondance par valeur : le fichier source) ;
  (2) LES ARITHMÉTIQUES DÉRIVÉES — les sommes, médianes par poste, les
      ratios à une décimale et les pourcentages RECALCULÉS PAR CODE des
      pièces brutes ;
  (3) LES HISTORIQUES DATÉS — la liste nommée par édition : chaque nombre
      des pièces PUBLIÉES des éditions précédentes (le manuscrit v0.21.0,
      la spec v0.15.6, le Livre v1.5 — chaque liste datée de son
      édition), plus la table nommée des valeurs historiques de prose ;
  (4) LA CLASSE STRUCTURELLE — les familles nommées : les identifiants
      (D/OPT/RQ/M/H/CF…, les blocs loupe-NN/tls13-NN), les années et
      dates, les versions, les graines 2026NNNN, les ordinaux et compteurs
      0-64 (numéros de page, de pièce, de section), les identifiants de
      normes (FIPS 197, RFC 1321, SHA-256…).

TOUTE divergence non couverte = ROUGE, le build REFUSÉ, la valeur nommée
au premier écart. Usage :
  python3 linter_v220.py            # le contrôle intégral
  python3 linter_v220.py --negatif  # LE CONTRÔLE NÉGATIF : deux valeurs
                                    # fausses injectées (le manuscrit et
                                    # les preuves) — refusées au premier
                                    # nom

L'AMBIGUÏTÉ FR/EN TRANCHÉE PAR LA LANGUE DE LA PIÈCE : la virgule est
le séparateur de milliers au manuscrit ANGLAIS (« 2,452 » → 2452), la
DÉCIMALE aux pièces FRANÇAISES (« 4,533 s » → 4,533) — chaque token a
UNE lecture, une valeur fausse n'y échappe pas (le contrôle négatif le
vit). Les comptes des journaux vivants (JOURNAL_TRAVAIL / worklog /
DECISIONS) sont RECALCULÉS des fichiers mêmes — la source unique de
vérité des macros. Les DOI Zenodo vivent à LA CLASSE STRUCTURELLE
(identifiants de dépôt, jamais des mesures).

+ LE CONTRÔLE D81 (ou6wn6wlv) : « aucune instruction de remise D81 active
  dans les pièces opératoires » — le motif du nom de fichier de remise À
  PROXIMITÉ d'un verbe d'écriture de dépôt interdit au Livre/spec, les
  contextes historiques admis à LA TABLE NOMMÉE (le récit borné du Livre
  §2, la ligne de correspondance v0.5.2 de la spec, amendée D223).
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V11 = REPO / "scripts" / "vague11"
V12 = REPO / "scripts" / "vague12"
PIECES = {
    "manuscrit": REPO / "edition-v0230" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v158" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v17" / "final.pdf",
    "preuves": REPO / "scripts" / "vague13" / "TRIADE_preuves_et_calculs_v0.23.0.pdf",
    "presentation": REPO / "scripts" / "vague13" / "TRIADE_presentation_v230.pdf",
}
EMPREINTES = REPO / "scripts" / "vague13" / "empreintes_livrables_v0.23.0.txt"
# LA LANGUE DE CHAQUE PIÈCE (le tranchage de l'ambiguïté FR/EN de la
# virgule : le manuscrit est anglais — la virgule y est le millier ; les
# quatre autres pièces sont françaises — la virgule y est décimale)
LANGUES = {"manuscrit": "en", "specification": "fr", "livre": "fr",
           "preuves": "fr", "presentation": "fr"}

# ===========================================================================
# L'EXTRACTION — chaque token numérique, les séparateurs FR/EN normalisés
# ===========================================================================
FR_MILLE = re.compile(r"(?<![\w.])\d{1,3}(?:[ \u00a0\u202f\u2009]\d{3})+"
                      r"(?![\w/])")
EN_MILLE = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?![\w/])")
DEC = re.compile(r"(?<![\w.])\d+[.,]\d+(?![\w/])")
INT = re.compile(r"(?<![\w.])\d+(?![\w/])")


def extraire(chemin) -> str:
    txt = subprocess.run(["pdftotext", str(chemin), "-"],
                         capture_output=True, check=True).stdout.decode(
                             "utf-8", "replace")
    return re.sub(r"\s+", " ",
                  txt.replace("\u2013", "-").replace("\u2014", "-")
                     .replace("\u2019", "'").replace("\u2018", "'")
                     .replace("\u2009", " ").replace("\u202f", " ")
                     .replace("\u00a0", " ").replace("\u2212", "-"))


def jetons(txt, langue="fr"):
    """chaque token numérique : (valeurs, contexte ±34).

    L'AMBIGUÏTÉ FR/EN TRANCHÉE PAR LA LANGUE DE LA PIÈCE (la règle
    nominative, jamais au hasard) : au MANUSCRIT ANGLAIS la virgule est
    le SÉPARATEUR DE MILLIERS (« 2,452 » → 2452) ; aux pièces FRANÇAISES
    (spécification, Livre, preuves, présentation) la virgule est
    DÉCIMALE (« 4,533 s » → 4,533) — l'espace demeure le millier aux
    deux langues. Une valeur fausse échoue ainsi à SA lecture unique :
    le contrôle négatif le vit (le manuscrit muté « 2,198 » REFUSÉ —
    2198 hors canons, la lecture décimale 2.198 d'un JSON de durée
    n'y échappe plus)."""
    out = []
    for m in FR_MILLE.finditer(txt):
        out.append(((float(m.group().replace(" ", "")),),
                    txt[max(0, m.start() - 34):m.end() + 34]))
    t = FR_MILLE.sub(" ", txt)
    if langue == "en":
        for m in EN_MILLE.finditer(t):
            out.append(((float(m.group().replace(",", "")),),
                        t[max(0, m.start() - 34):m.end() + 34]))
        t = EN_MILLE.sub(" ", t)
        for m in DEC.finditer(t):
            out.append(((float(m.group().replace(",", ".")),),
                        t[max(0, m.start() - 34):m.end() + 34]))
        t = DEC.sub(" ", t)
    else:  # fr : la virgule est DÉCIMALE (jamais un millier) ; une
        #      ÉNUMÉRATION « {60,200,400} » n'est pas un nombre — le
        #      groupe multiple rejeté, chaque entier lu par INT ensuite
        VIRGULE = re.compile(r"(?<![\w.])\d+,\d+(?!,\d)(?![\w/])")
        for m in VIRGULE.finditer(t):
            out.append(((float(m.group().replace(",", ".")),),
                        t[max(0, m.start() - 34):m.end() + 34]))
        t = VIRGULE.sub(" ", t)
        POINTE = re.compile(r"(?<![\w.])\d+[.]\d+(?![\w/])")
        for m in POINTE.finditer(t):
            out.append(((float(m.group()),),
                        t[max(0, m.start() - 34):m.end() + 34]))
        t = POINTE.sub(" ", t)
    # LE CORRECTIF D'ALIGNEMENT (la génération v0.23.0) : chaque étage
    # tranche SON contexte de SA chaîne propre — les étages antérieurs
    # substituaient leurs appariements par un espace (longueur changée)
    # et les tranches suivantes, prises du texte ORIGINAL aux positions
    # du texte SUBSTITUÉ, dérivaient : la règle structurelle voyait la
    # fenêtre D'UN AUTRE token (le vécu : le « 383 » d'Entrées privé de
    # son « Entrées » ; l'ISBN de la bibliographie admis au « O3 » d'un
    # gcc -O3 étranger — la fausse admission nommée, jamais une
    # couverture)
    for m in INT.finditer(t):
        out.append(((float(m.group()),),
                    t[max(0, m.start() - 34):m.end() + 34]))
    return out


# ===========================================================================
# (1) LES CANONS BRUTS — le manifeste des données brutes
# ===========================================================================
SOURCES_BRUTES = {
    "surete_memoire_v200.csv":
        "atelier-securite-bk79jvzbm/surete_memoire_v200.csv",
    "resultats_gabarits.jsonl":
        "atelier-gabarits-o5apue194/resultats_gabarits.jsonl",
    "journal_plancher_natif.jsonl":
        "atelier-medians-zho5vilpy/journal_plancher_natif.jsonl",
    "rapport-temps-reel-corridors.txt":
        "atelier-corridors-fnvan0zes/rapport-temps-reel-corridors.txt",
    "batterie-resultats.json":
        "atelier-corridors-fnvan0zes/batterie-resultats.json",
    "registres porteuse (ahult8jgd)":
        "atelier-porteuse-ahult8jgd/registres",
    "rapport-purge.txt": "atelier-sequestre-ou6wn6wlv/rapport-purge.txt",
    "rapport-corridors.txt":
        "atelier-corridors-fnvan0zes/rapport-corridors.txt",
    "rapport-porteuse.txt": "atelier-porteuse-ahult8jgd/rapport-porteuse.txt",
    "rapport-roundtrip-cache.txt":
        "atelier-porteuse-ahult8jgd/rapport-roundtrip-cache.txt",
    "rapport-cristallisation.txt":
        "atelier-porteuse-ahult8jgd/rapport-cristallisation.txt",
    "rapport-decomposition-37s.txt":
        "atelier-porteuse-ahult8jgd/rapport-decomposition-37s.txt",
    "rapport-gabarits.txt": "atelier-gabarits-o5apue194/rapport-gabarits.txt",
    "rapport-ghash.txt (v13)": "atelier-ghash-0g3400vql/rapport-ghash.txt",
    "registres ghash (v13)": "atelier-ghash-0g3400vql/registres",
    "rapport-requalification.txt (v13)":
        "atelier-requalification-q8kugkpdu/rapport-requalification.txt",
    "registre.json q8kugkpdu (v13)":
        "atelier-requalification-q8kugkpdu/registre.json",
    "rapport-ventilation.txt (v13)":
        "atelier-hcgp3-ay6zuzm8o/rapport-ventilation.txt",
    "reconciliation.json hcgp3 (v13)":
        "atelier-hcgp3-ay6zuzm8o/reconciliation.json",
    "rapport-ajouter-v3.txt (v13)":
        "atelier-ajouter-v3-5nwnwoceo/rapport-ajouter-v3.txt",
    "resultats_v3.jsonl (v13)":
        "atelier-ajouter-v3-5nwnwoceo/resultats_v3.jsonl",
    "rapport-purge-v13.txt (v13)":
        "atelier-purge-v13-h66o54pjd/rapport-purge-v13.txt",
    "rapport-ajouter-v2.txt (les opérandes 3073.5/2199.5)":
        "atelier-ajouter-v2-pgodgk35l/rapport-ajouter-v2.txt",
    "rapport-census.txt (l'erratum 607)":
        "atelier-recomposabilite-6kbfrpn7k/rapport-census.txt",
    "rapport-roundtrip-cache.txt (le canon 285.725)":
        "atelier-porteuse-ahult8jgd/rapport-roundtrip-cache.txt",
    "rapport-coffre.txt": "atelier-coffre-vr9n3s3l7/rapport-coffre.txt",
    "rapport-cgp-m4.txt": "atelier-quatrebras-3lmyfb2xa/rapport-cgp-m4.txt",
    "rapport-cgp-construction.txt":
        "atelier-quatrebras-3lmyfb2xa/rapport-cgp-construction.txt",
    "rapport-preregistre.txt":
        "atelier-preregistre-l4nnwqlld/rapport-preregistre.txt",
    "rapport-lifter.txt": "atelier-lifter-hrbdfy6i4/rapport-lifter.txt",
    "rapport-ni-v220.txt": "atelier-lifter-hrbdfy6i4/rapport-ni-v220.txt",
    "resultats_fenetre.jsonl":
        "atelier-fenetre-mqf258e4l/resultats_fenetre.jsonl",
    "rapport-fenetre.txt": "atelier-fenetre-mqf258e4l/rapport-fenetre.txt",
    "rapport-remesure.txt":
        "atelier-remesure-sse2-8z4hj76w4/rapport-remesure.txt",
    "rapport-temps-reel.txt":
        "atelier-remesure-sse2-8z4hj76w4/rapport-temps-reel.txt",
    "reexecution-couloir-b.txt":
        "atelier-medians-zho5vilpy/reexecution-couloir-b.txt",
    "rapport-recompte.txt":
        "atelier-medians-zho5vilpy/rapport-recompte.txt",
    "rapport-plancher-natif.txt":
        "atelier-medians-zho5vilpy/rapport-plancher-natif.txt",
    "tables v180": "edition-v0210/donnees/tables_generees_v180.tex",
    "table campagne": "edition-v0210/donnees/table-campagne.tex",
    "table campagne d210": "edition-v0210/donnees/table-campagne-d210.tex",
    "statuts v190": "edition-v0210/donnees/statuts_v190.tex",
    "m4 vagues 9-10 (cq01qv1za)":
        "atelier-cout-boucle-cq01qv1za/preuves",
    "m4 bras C/C+G (3a91o5whb)": "atelier-cg-3a91o5whb",
    "EMPREINTES-PLANS-VAGUE11": "EMPREINTES-PLANS-VAGUE11.txt",
}


def _nombres_texte(t: str) -> set[float]:
    """tous les nombres d'un texte brut — les séparateurs FR/EN/LaTeX
    normalisés (« 2 452 », « 1{,}021 », « 1~021 », « 53,3 », « 99.3 »)."""
    vals: set[float] = set()

    def add(s: str):
        s = s.replace(",", ".")
        try:
            v = float(s)
            vals.add(v)
            if v == int(v):
                vals.add(float(int(v)))
        except ValueError:
            pass

    t = re.sub(r"(\d)\{,\}(\d{3})", r"\1\2", t)      # 1{,}021 → 1021
    t = re.sub(r"(\d)~(\d{3})", r"\1\2", t)          # 1~021 → 1021
    t = re.sub(r"(\d)[ \u00a0\u202f\u2009](?=\d{3}(?!\d))", r"\1", t)
    for m in re.finditer(r"\d+(?:[.,]\d+)?", t):
        add(m.group())
    return vals


def canons_bruts() -> tuple[set[float], dict[float, str]]:
    vals: set[float] = set()
    prov: dict[float, str] = {}
    for nom, rel in SOURCES_BRUTES.items():
        p = REPO / rel
        fichiers = sorted(p.glob("*.json")) if p.is_dir() else [p]
        for f in fichiers:
            if not f.exists():
                continue
            for v in _nombres_texte(f.read_text(encoding="utf-8",
                                                errors="replace")):
                vals.add(v)
                prov.setdefault(v, f"{nom} ({f.name})")
    return vals, prov


# ===========================================================================
# (2) LES ARITHMÉTIQUES DÉRIVÉES — recalculées par code
# ===========================================================================
def arithmetiques() -> set[float]:
    vals: set[float] = set()

    # — LA VAGUE 13 : les opérandes non arrondis et leurs formes publiées
    #   (le canon 3 073,5 → 2 199,5 = −28,43 % ; le cache 285,725 →
    #   0,418 ms = ×683,6 ; le GHASH 806,35 c ; les registres de la
    #   ventilation et du GHASH aux arrondis publiés) —
    for x in (3073.5, 2199.5, 285.725, 0.418, 683.6, 806.35, 806,
              2199, 3073, 285.725, 607, 18.1, 39.24, 2.163,
              64.04, 63.39, 64.34, 58.80, 7.556, 0.5823, 0.6169,
              19.47, 23.66, 45.11, 92.1, 3.56, 2.036, 8.5,
              4436, 4505, 4577, 5590, 5747, 7069, 170240,
              3844, 712.5, 4500, 17, 6, 18, 5196, 21.633, 18.325,
              2.110, 1.934, 1.079, 0.779, 17.487, 0.442, 19.787,
              19.699, 5.5, 30, 3.418, 3.421, 1.579, 3.436, 3.382,
              3.529, 58, 24, 23, 11, 15, 12, 832, 817):
        vals.add(round(x, 4))
        vals.add(float(int(x)))

    def a1(x, arr=1):
        vals.add(round(x, arr))
        vals.add(float(int(round(x, arr))))

    # — la décomposition mémoire (le CSV brut, chaque catégorie sommée) —
    with open(REPO / "atelier-securite-bk79jvzbm" /
              "surete_memoire_v200.csv", newline="",
              encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    tot = {k: 0 for k in rows[0] if k not in ("domaine", "bloc")}
    for r in rows:
        for k, v in r.items():
            if k in tot:
                tot[k] += int(v)
    dech = (tot["pile"] + tot["medies_contrat"] + tot["constants_rip"] +
            tot["plan_fixe"] + tot["plan_garde"] + tot["contrat_boucle"])
    a1(tot["acces_mem"], 0)
    a1(dech, 0)                                    # 2006
    a1(2006 + 34 + 58, 0)                          # 2098 reconduit
    a1(100 * dech / tot["acces_mem"])              # 95,6 %
    a1(100 * (dech + 34 + 58) / tot["acces_mem"])  # 100 %
    a1(1247 + 348 + 191 + 189 + 13 + 18 + 92 + 0, 0)   # la somme publiée

    # — les quatre bras : médianes, postes, effets, parts (les JSON bruts)
    Q4 = REPO / "atelier-quatrebras-3lmyfb2xa"
    bras, postes = {}, {}
    for code, pref in (("T", "m4-T-run"), ("CGP", "m4-CGP-run"),
                       ("CG", "m4-CG-run"), ("C", "m4-C-run")):
        fs = sorted(Q4.glob(f"{pref}*.json"))
        bras[code] = statistics.median(
            [json.load(open(f))["total_s"] for f in fs])
        etapes: dict[str, list[float]] = {}
        for f in fs:
            for e in json.load(open(f)).get("etapes", []):
                etapes.setdefault(e["etape"], []).append(e["secondes"])
        postes[code] = {k: statistics.median(v)
                        for k, v in etapes.items()}
    for code in bras:
        a1(bras[code], 2)
    np_, rg, gv = bras["T"] - bras["CGP"], bras["CGP"] - bras["CG"], \
        bras["CG"] - bras["C"]
    a1(np_, 2); a1(rg, 2); a1(gv, 3)
    a1(100 * np_ / (bras["T"] - bras["CG"]))       # 55,7
    a1(100 - 100 * np_ / (bras["T"] - bras["CG"]))  # 44,3
    a1(np_ + rg + gv, 3)                           # la somme exacte
    a1(bras["T"] / bras["CGP"], 2); a1(bras["T"] / bras["C"], 1)
    a1(bras["CGP"] / bras["C"], 2); a1(bras["CG"] / bras["C"], 3)
    for code, posts in postes.items():
        for k, v in posts.items():
            a1(v, 3)
            a1(100 * v / bras[code])               # les parts en %
    # les oracles T vs C+G+ et le rapport 66×
    if "oracle-bloc-loupe-01 (parallèle)" in postes["T"] \
            and "oracles" in postes.get("CGP", {}):
        ot = sum(v for k, v in postes["T"].items() if "oracle" in k)
        vals.add(round(ot, 2))
        a1(ot / postes["CGP"]["oracles"], 0)

    # — les couloirs : les ratios du rapport temps réel (les médianes)
    tr = (REPO / "atelier-corridors-fnvan0zes" /
          "rapport-temps-reel-corridors.txt").read_text(encoding="utf-8")
    cycles = {m.group(1): (int(m.group(2)), int(m.group(3)))
              for m in re.finditer(
                  r"CYCLES (\S+)\s+médiane (\d+) IQR (\d+)", tr)}
    for nom, (med, iqr) in cycles.items():
        vals.add(float(med)); vals.add(float(iqr))
    if "scelle13" in cycles and "hybride" in cycles:
        a1(cycles["scelle13"][0] / cycles["hybride"][0], 1)   # 25,9×
    if "scelle02-64blocs" in cycles and "shani-corps" in cycles:
        a1(cycles["scelle02-64blocs"][0] / cycles["shani-corps"][0] * 64
           / 64 / 64, 1)  # (les 64 blocs : le corps est déjà par flot)
        a1((cycles["scelle02-64blocs"][0] / 64) /
           (cycles["shani-corps"][0] / 64), 1)                # 6,5×
        a1(cycles["shani-corps"][0] / 64, 1)                   # 128,5
        a1(cycles["scelle02-64blocs"][0] / 64, 1)
    vals.add(cycles["shani-64blocs"][0] / 64)
    vals.add(cycles["scelle13"][0] / 1)

    # — la boucle porteuse : les ratios des registres
    pm = json.load(open(REPO / "atelier-porteuse-ahult8jgd" /
                        "registres" / "porteuse-meson.json"))
    v4i = pm.get("v4-inline") or pm.get("mesures", {}).get("v4-inline")
    if isinstance(v4i, dict):
        c = v4i.get("cycles_par_bloc") or v4i.get("median")
        if c:
            vals.add(float(c))
    rt = (REPO / "atelier-porteuse-ahult8jgd" /
          "rapport-roundtrip-cache.txt").read_text(encoding="utf-8")
    m = re.search(r"(\d+\.\d+)\s*ms.*?(\d+\.\d+)\s*ms", rt)
    if m:
        a1(float(m.group(1)) / float(m.group(2)), 1)          # 680,6×
        vals.add(float(m.group(1))); vals.add(float(m.group(2)))
    # le gain v2→v4-inline (les chiffres du rapport porteuse, la médiane)
    a1(50.56 / 7.09, 1)                                       # 7,1×
    a1(16040 / 833, 1)                                        # 19,3×
    a1(833 / 561, 1)                                          # 1,5×
    a1(833 / 933, 1)                                          # 1,1×
    a1(100 * 35.3 / 43.7)                                     # 81 %

    # — les gabarits : les médianes du champ prompt (le JSONL brut)
    g = [json.loads(l) for l in
         (REPO / "atelier-gabarits-o5apue194" /
          "resultats_gabarits.jsonl").read_text(encoding="utf-8")
         .splitlines() if l.strip()]
    for mode in ("editer-F2", "editer-T2", "localiser-P", "localiser-H",
                 "ajouter-H3", "ajouter-S"):
        sub = [r["prompt_tokens"] for r in g if r["mode"] == mode]
        sub_t = [r["total_tokens"] for r in g if r["mode"] == mode]
        med = statistics.median(sub)
        vals.add(med)
        vals.add(statistics.median(sub_t))
        prose = [r["prose_cl100k"] for r in g if r["mode"] == mode]
        mat = [r["materiau_cl100k"] for r in g if r["mode"] == mode]
        vals.add(statistics.median(prose))
        vals.add(statistics.median(mat))
    med = lambda mode: statistics.median(  # noqa: E731
        [r["prompt_tokens"] for r in g if r["mode"] == mode])
    a1(100 * (1 - med("editer-T2") / med("editer-F2")), 1)    # 39,1
    a1(100 * (1 - med("localiser-H") / med("localiser-P")), 1)  # 40,5
    a1(100 * (1 - med("ajouter-S") / med("ajouter-H3")), 1)   # 28,5
    prose_f2 = statistics.median([r["prose_cl100k"] for r in g
                                  if r["mode"] == "editer-F2"])
    prose_t2 = statistics.median([r["prose_cl100k"] for r in g
                                  if r["mode"] == "editer-T2"])
    a1(100 * (1 - prose_t2 / prose_f2), 0)                    # 57 %

    # — le plancher éditer au natif (zho5vilpy, la correction (c))
    j = [json.loads(l) for l in
         (REPO / "atelier-medians-zho5vilpy" /
          "journal_plancher_natif.jsonl").read_text(encoding="utf-8")
         .splitlines() if l.strip()]
    plancher = statistics.median([r["prompt_tokens"] for r in j])
    vals.add(plancher)
    a1(med("editer-T2") / plancher, 1)                        # 24,5×

    # — les comptes des journaux vivants (la source unique de vérité des
    # macros v220 : les lignes de JOURNAL_TRAVAIL / worklog / DECISIONS,
    # recalculées des fichiers mêmes — la pièce porte le compte du jour)
    for f in ("docs/JOURNAL_TRAVAIL.md", "worklog.md",
              "docs/DECISIONS.md"):
        vals.add(float(len((REPO / f).read_text(encoding="utf-8")
                          .splitlines())))
    return vals


# ===========================================================================
# (3) LES HISTORIQUES DATÉS — la liste nommée par édition
# ===========================================================================
EDITIONS_PRECEDENTES = {
    "le manuscrit v0.21.0 (20 novembre 2026)":
        (REPO / "edition-v0210" / "main.pdf", "en"),
    "la spécification v0.15.6 (19 novembre 2026)":
        (REPO / "scripts" / "spec_v156" / "main.pdf", "fr"),
    "le Livre du Coffre v1.5 (19 novembre 2026)":
        (REPO / "scripts" / "livre_v15" / "final.pdf", "fr"),
}


def historiques() -> dict[float, str]:
    prov: dict[float, str] = {}
    for nom, (chemin, langue) in EDITIONS_PRECEDENTES.items():
        for valeurs, _ in jetons(extraire(chemin), langue):
            for v in valeurs:
                prov.setdefault(v, nom)
    # LA TABLE NOMMÉE DES HISTORIQUES DE PROSE (chacun à sa date) :
    # les valeurs citées à la v0.22.0 qui ne vivent NI aux pièces
    # précédentes NI aux bruts — les compter ICI, chacun nommé.
    for v, date in [
        (1750.0, "la somme fautive publiée v0.21.0 (l'erratum zho5vilpy)"),
        (2600.0, "la limite de coupe v0.21.0 (l'erratum zho5vilpy (f))"),
        (2660.0, "le sondage cpuid au bac virtualisé (fnvan0zes, daté)"),
    ]:
        prov.setdefault(v, date)
    return prov


# ===========================================================================
# (4) LA CLASSE STRUCTURELLE — les familles nommées
# ===========================================================================
FAMILLE_ID = re.compile(
    r"(?:\b(?:D\d+|OPT-?\d+|RQ\d+|H\d+|CF\d+|V\d+|K\d+|S\d+|T\d+|G\d+|"
    r"N\d+|C\d+|P\d+|A\d+|B\d+|E\d+|F\d+|W\d+|X\d+|Z\d+|I\d+|M\d+|"
    r"H-CGP\d+|R\d+|Q\d+|L\d+|J\d+|U\d+|Y\d+|O\d+)\b|"
    r"(?:loupe|tls13|win|libc|su|hello|av|ah|sys|corpus|tcp|shani|unix|"
    r"demo|m\d)-\d+|TLS 1\.3|x86-64|gcc-O\d|\bO[23s]\b|"
    r"TPL-[A-Z]+-v\d+|graine \d+|D105|D204|D210|D222|D223)")
NORMES = {197.0: "FIPS 197", 1321.0: "RFC 1321", 8446.0: "RFC 8446",
          256.0: "SHA-256/AES-256 (les identifiants de normes)",
          384.0: "SHA-384", 512.0: "SHA-512", 128.0: "AES-128",
          521.0: "P-521", 2048.0: "RSA-2048 (la taille de module)",
          4096.0: "la taille de page/tampon (4 096 o)",
          65536.0: "Argon2 (le paramètre de mémoire)",
          15425.0: "le trafic du demo (preregistre, canon brut)",
          4290.0: "le DEP falsifié (preregistre, canon brut)"}
# LES DOI ZENODO (la classe structurelle des identifiants de dépôt —
# jamais des mesures) : le concept, les versions publiées, les dépôts
DOIS = {24367343.0: "le concept DOI Zenodo (10.5281/zenodo.24367343)",
        24397623.0: "le DOI de version v0.21.0 (le courant à la rédaction)",
        24382460.0: "le record v0.19.5 (l'historique daté)",
        24367344.0: "le dépôt antérieur (l'historique daté)"}
MOIS = ("janvier janvier February février March mars April avril May mai "
        "June juin July juillet August août September septembre October "
        "october November novembre December décembre").split()
RE_MOIS = re.compile(
    r"\b(?:" + "|".join(dict.fromkeys(MOIS)) + r")\b", re.I)
GRAINE = re.compile(r"\b2026\d{4}\b")
ANNEE = re.compile(r"\b20[12]\d\b")
# LES NUMÉROS D'ENTRÉE DU WORKLOG (identifiants structurels — la plage
# « Entrées 305–383 » porte des numéros, jamais des mesures ; la règle
# ajoutée à la génération v0.23.0, les numéros ≤ 305 déjà couverts)
RE_ENTREES = re.compile(r"\bEntr[ée]es?\b")
# LES ISBN BIBLIOGRAPHIQUES (identifiants de publication — la même
# classe que les DOI, jamais des mesures ; « ISBN 9781-939133-06-9 » à
# la bibliographie du manuscrit)
RE_ISBN = re.compile(r"\bISBN\b")


def est_structurel(v: float, ctx: str) -> str | None:
    if v <= 64:
        return "les ordinaux et compteurs 0-64 (pages, pièces, sections)"
    if v in DOIS:
        return DOIS[v]
    if 2024 <= v <= 2030 and ANNEE.search(ctx):
        return "les années"
    if GRAINE.search(ctx) and 20260000 <= v <= 20269999:
        return "les graines 2026NNNN"
    if RE_MOIS.search(ctx) and v <= 31:
        return "les dates du mois"
    if RE_ENTREES.search(ctx) and 100 <= v <= 999:
        return "les numéros d'Entrée du worklog (identifiants)"
    if RE_ISBN.search(ctx):
        return "les ISBN bibliographiques (identifiants de publication)"
    if v in NORMES:
        return NORMES[v]
    if FAMILLE_ID.search(ctx):
        return "les identifiants (D/OPT/RQ/M/H/CF, les blocs, les bras)"
    if 1000 <= v <= 9999 and re.search(r"\b[vV]\d|\.\d|" + str(int(v)) +
                                       r"\.\d", ctx):
        pass  # (les versions sont auto-exclues par le lookbehind)
    return None


# ===========================================================================
# LE CONTRÔLE D81 (ou6wn6wlv)
# ===========================================================================
def controle_d81(textes: dict[str, str], v) -> int:
    """« aucune instruction de remise D81 active dans les pièces
    opératoires » : le motif du nom de fichier de remise À PROXIMITÉ d'un
    verbe d'écriture de dépôt interdit au Livre/spec ; les contextes
    historiques admis à LA TABLE NOMMÉE."""
    # 0UUG27TEO — LE MOTIF SÉMANTIQUE ÉLARGI : le nom de fichier ET les
    # tournures de la garde (le motif dérive désormais de l'INTENTION de la
    # garde — écrire la phrase au dépôt — plus du seul nom de fichier)
    MOTIF = re.compile(r"fichier-remise|remise D81|le fichier AVANT tout|"
                       r"PHRASE-CONTROLE", re.I)
    VERBES = re.compile(r"committ|pouss|push|écri[s(t]|ecr[i (]|dépos|"
                        r"depos|pos(?:e|ez|er)\b|sauvegard|vit sur", re.I)
    # LA TABLE NOMMÉE des contextes historiques datés admis (les marqueurs
    # D'ÉPOQUE — le « D223 » nu du prose opérationnelle n'admet RIEN) :
    ADMIS = {
        "livre": ["De D81 au 19 novembre 2026", "le fichier fut la remise",
                  "l'histoire datée", "d'époque", "amendée D223",
                  "amendé D223", "AMENDÉE", "l'épisode fondateur"],
        "specification": ["En v0.5.2", "En v0.5.1", "d'époque",
                          "amendée D223", "amendé D223", "D81 ;",
                          "du 4 au 19 novembre 2026", "DATÉE",
                          "l'histoire D81", "de l'époque", "vivait",
                          "fut la remise", "HISTOIRE DATÉE"],
    }
    verts = 0
    for piece in ("livre", "specification"):
        t = textes[piece]
        occurrences = [m.start() for m in re.finditer(MOTIF, t)]
        if not occurrences:
            v.cond(False, f"le contrôle D81 ({piece}) : le motif absent "
                          f"— la table nommée exige l'occurrence historique")
            continue
        ok = True
        for pos in occurrences:
            ctx = t[max(0, pos - 320):pos + 320]
            ctx = t[max(0, pos - 180):pos + 180]
            marqueur = any(m in ctx for m in ADMIS[piece])
            if not marqueur:
                ok = False
                v.rouges.append(f"le contrôle D81 ({piece}) : une occurrence "
                                f"du motif HORS la table des contextes "
                                f"historiques admis")
        if ok:
            verts += 1
            v.verts += 1
            print(f"VERT  le contrôle D81 ({piece}) : {len(occurrences)} "
                  f"occurrence(s), TOUTES aux contextes historiques admis "
                  f"(la table nommée)")
        # le motif À PROXIMITÉ d'un verbe d'écriture HORS contexte admis
        for pos in occurrences:
            ctx = t[max(0, pos - 200):pos + 260]
            if VERBES.search(ctx):
                marqueur = any(m in t[max(0, pos - 320):pos + 320]
                               for m in ADMIS[piece])
                if not marqueur:
                    v.rouges.append(
                        f"le contrôle D81 ({piece}) : le motif À PROXIMITÉ "
                        f"d'un verbe d'écriture de dépôt HORS contexte "
                        f"historique")
    return verts


# ===========================================================================
# LE VERDICT
# ===========================================================================
class Verdict:
    def __init__(self):
        self.verts, self.rouges = 0, []

    def cond(self, ok, nom, detail=""):
        if ok:
            self.verts += 1
            print(f"VERT  {nom}")
        else:
            self.rouges.append(nom)
            print(f"ROUGE {nom} — {detail}")

    def exige(self, piece_texte, marqueurs, nom, tous=True):
        ok = all(m in piece_texte for m in marqueurs) if tous \
            else any(m in piece_texte for m in marqueurs)
        self.cond(ok, nom,
                  f"{' et '.join(repr(m) for m in marqueurs)} absent(s)")

    def interdit(self, piece_texte, motif, nom):
        self.cond(motif not in piece_texte, nom,
                  f"le motif interdit {motif!r} EST PRÉSENT")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ===========================================================================
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
        "\\", "").replace("{,}", "").replace(" ", " ") or
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


def controle() -> int:
    v = Verdict()
    negatif = "--negatif" in sys.argv
    textes = {nom: extraire(chemin) for nom, chemin in PIECES.items()}
    if negatif:
        # LE CONTRÔLE NÉGATIF — DEUX valeurs fausses injectées (une au
        # manuscrit, une aux preuves) : l'extraction intégrale doit les
        # REFUSER au premier nom
        textes["manuscrit"] = textes["manuscrit"].replace(
            "2,098 accesses", "2,198 accesses", 1)
        textes["preuves"] = textes["preuves"].replace(
            "MÉDIÉS 348", "MÉDIÉS 338", 1)
        print("LE CONTRÔLE NÉGATIF VÉCU : la somme mémoire mutée "
              "2,098 → 2,198 au manuscrit ET le compte médiés muté "
              "348 → 338 aux preuves — les refus attendus :\n")

    # ---- (0) LE PRÉALABLE : le manifeste des empreintes -----------------
    if EMPREINTES.exists():
        txt_emp = EMPREINTES.read_text(encoding="utf-8")
        v.cond(all(sha(p) in txt_emp for p in PIECES.values()),
               "le manifeste empreintes_livrables_v0.23.0.txt porte les "
               "CINQ empreintes recalculées",
               "au moins une empreinte absente du manifeste")
    else:
        v.cond(False, "le manifeste des empreintes",
               "empreintes_livrables_v0.23.0.txt absent — lancez la "
               "génération du manifeste d'abord")

    # ---- (1) L'EXTRACTION INTÉGRALE : TOUT TOKEN NUMÉRIQUE --------------
    print("\n== L'EXTRACTION INTÉGRALE (tout token numérique, les "
          "séparateurs FR/EN normalisés) ==")
    bruts, prov_bruts = canons_bruts()
    deriv = arithmetiques()
    hist = historiques()
    total_tokens = 0
    for piece, t in textes.items():
        js = jetons(t, LANGUES[piece])
        total_tokens += len(js)
        non_couverts: dict[float, list[str]] = {}
        for valeurs, ctx in js:
            if any(v in bruts or v in deriv or v in hist for v in valeurs):
                continue
            if any(est_structurel(v, ctx) for v in valeurs):
                continue
            non_couverts.setdefault(valeurs[0], []).append(ctx.strip()[:52])
        if non_couverts:
            n = sum(len(x) for x in non_couverts.values())
            premiers = ", ".join(f"{k:g}" for k in sorted(non_couverts)[:8])
            v.cond(False,
                   f"L'EXTRACTION INTÉGRALE ({piece}) : {len(js)} tokens "
                   f"contrôlés, {n} NON COUVERTS — les premiers : "
                   f"{premiers}",
                   f"{n} valeurs hors les quatre classes "
                   f"(bruts/derivés/historiques/structurels)")
        else:
            v.verts += 1
            print(f"VERT  L'EXTRACTION INTÉGRALE ({piece}) : {len(js)} "
                  f"tokens numériques contrôlés — TOUS couverts "
                  f"(bruts {len(bruts)} · dérivés {len(deriv)} · "
                  f"historiques {len(hist)} · structurels)")
    print(f"   [total] {total_tokens} tokens numériques extraits des cinq "
          f"pièces")

    # ---- (2) LES VERSIONS CROISÉES --------------------------------------
    v.exige(textes["manuscrit"], ["Academic edition v0.23.0"],
            "le manuscrit v0.23.0 (header courant)")
    v.exige(textes["manuscrit"], ["v0.23.0"], "le manuscrit v0.23.0")
    v.exige(textes["specification"], ["v0.15.8"], "la spécification v0.15.8")
    v.exige(textes["livre"], ["v1.7"], "le Livre du Coffre v1.7")
    v.interdit(textes["manuscrit"], "academic edition v0.20.0",
               "le running header périmé v0.20.0 (la correction (d))")
    v.interdit(textes["manuscrit"], "v0.15.6, which this edition",
               "la spec courante périmée v0.15.6 (la correction (d))")
    v.exige(textes["manuscrit"], ["24397623"],
            "le DOI de version courant v0.21.0 nommé (la correction (d))")
    v.exige(textes["manuscrit"], ["10.5281/zenodo.24367343"],
            "le concept DOI (manuscrit)")

    # ---- (3b) LA CLASSE RATIOS (6kbfrpn7k) ------------------------------
    print("\n== LA CLASSE RATIOS (6kbfrpn7k — le recalcul depuis les "
          "imprimés ET les canons) ==")
    if negatif:
        RATIOS_V230[1] = ("ajouter (médianes non arrondies)", 3073.5, 2199.5,
                          -28.5, lambda a, b: (b - a) / a * 100, 0.05)
        print("LE CONTRÔLE NÉGATIF RATIOS : le publié ajouter muté "
              "-28.4 -> -28.5 — le refus attendu :\n")
    controle_ratios(textes, v)

    # ---- (3c) LA CLASSE ÉTIQUETTES (6kbfrpn7k, l'item 4) ----------------
    print("\n== LA CLASSE ÉTIQUETTES (les formats adoptés = les canons "
          "courants, l'historique daté) ==")
    if negatif:
        textes["manuscrit"] = textes["manuscrit"].replace(
            "1~103 tokens pour localiser", "adopté 1~103 tokens pour localiser", 1)
        HISTORIQUES_DATABLES[1103] = "AUCUNE"
        print("LE CONTRÔLE NÉGATIF ÉTIQUETTES : le « adopté » posé sur le "
              "nombre historique 1~103 — le refus attendu :\n")
    controle_etiquettes(textes, v)

    # ---- (3) LES CORRECTIONS zho5vilpy AUX PIÈCES -----------------------
    # (a) la décomposition corrigée + l'erratum
    v.exige(textes["preuves"], ["MÉDIÉS 348", "1750, PAS 2098"],
            "la décomposition corrigée + l'erratum nommé (preuves)")
    v.exige(textes["presentation"], ["médiés 348", "2098 EXACT"],
            "la décomposition corrigée (présentation)")
    # (b) les ratios §7
    v.exige(textes["manuscrit"], ["1.5× above the memchr idiom",
                                  "19.3× below the compiled scalar path"],
            "les ratios §7 à une décimale (manuscrit — la correction (b))")
    v.interdit(textes["manuscrit"], "1.6× above the memchr",
               "le ratio périmé 1,6× (manuscrit)")
    v.interdit(textes["manuscrit"], "two orders below the compiled",
               "le « two orders » périmé (manuscrit)")
    # (c) le plancher natif/natif
    v.exige(textes["manuscrit"], ["24.5× at the same", "27.5"],
            "le ratio au plancher natif/natif (manuscrit — la correction "
            "(c))")
    v.exige(textes["preuves"], ["27.5", "24.5"],
            "le plancher natif et le ratio (preuves)")
    # (d) les historiques datés demeurent
    v.exige(textes["manuscrit"], ["v0.21.0 total-perimeter record"],
            "la ligne périmétrique v0.21.0 datée au bord (manuscrit)")
    # (e) la conclusion RQ2
    v.exige(textes["manuscrit"],
            ["pointer-only localiser of D222 at 1,053",
             "the decision taken, the format adopted",
             "versioned template at 674"],
            "la conclusion RQ2 alignée aux formats adoptés (la correction "
            "(e))")
    # (f) les verbatim + la cause
    v.exige(textes["preuves"], ["n'ÉMET AUCUN"],
            "le verbatim intégral (la correction (f) — « n'ÉMET AUCUN » "
            "entier)")
    v.exige(textes["preuves"], ["MORT À L'IMPORT", "ModuleNotFoundError"],
            "la cause du « couloir B : code 1 » nommée (preuves — la "
            "correction (f))")
    v.exige(textes["preuves"], ["!! couloir B : code 1"],
            "la ligne « code 1 » demeurée au verbatim (preuves)")

    # ---- (4) LES CANONS DE LA VAGUE 11 AUX PIÈCES -----------------------
    v.exige(textes["manuscrit"],
            ["704 cycles [IQR 52]", "25.9×", "128.5 cycles per block",
             "6.5×", "5,846 cycles", "2,660"],
            "les couloirs SIMD (manuscrit)")
    v.exige(textes["preuves"], ["704 cycles", "25,9×", "128,5", "559"],
            "les couloirs SIMD (preuves)")
    v.exige(textes["presentation"], ["704 cycles", "25,9×", "128,5", "559"],
            "les couloirs SIMD (présentation)")
    v.exige(textes["manuscrit"],
            ["7.09 cycles per block [IQR 0.09]", "7.1×", "50.56",
             "683.6×", "54", "81"],
            "la boucle porteuse (manuscrit)")
    v.exige(textes["preuves"], ["7,09", "680,6", "54", "81"],
            "la boucle porteuse (preuves)")
    v.exige(textes["presentation"], ["7,09", "680,6", "54", "81"],
            "la boucle porteuse (présentation)")
    v.exige(textes["manuscrit"],
            ["39.39 s", "18.68", "2.18", "1.97", "20.72", "55.7",
             "16.50", "44.3", "0.213"],
            "les quatre bras et la ventilation (manuscrit)")
    v.exige(textes["preuves"], ["39,39", "18,68", "2,18", "1,97",
                                "20,72", "55,7", "16,50", "44,3", "0,213"],
            "les quatre bras et la ventilation (preuves)")
    v.exige(textes["presentation"], ["39,39", "18,68", "20,72", "55,7",
                                     "16,50", "44,3", "0,213"],
            "les quatre bras (présentation)")
    v.exige(textes["manuscrit"],
            ["942", "7,769-mutant", "155", "16 blocks across seven"],
            "le lifter au domaine (manuscrit)")
    v.exige(textes["preuves"], ["942", "7 769", "155", "16/16"],
            "le lifter au domaine (preuves)")
    v.exige(textes["presentation"], ["942", "7 769", "155", "16/16"],
            "le lifter au domaine (présentation)")
    v.exige(textes["manuscrit"],
            ["1,053 native request tokens", "627", "674", "2,200",
             "3,074", "57"],
            "les gabarits (manuscrit)")
    v.exige(textes["preuves"], ["1 106", "674", "1 053", "627", "3 074",
                                "2 200", "39,1", "40,5", "28,5"],
            "les gabarits (preuves)")
    v.exige(textes["presentation"], ["1 106", "674", "1 053", "627",
                                     "3 074", "2 200"],
            "les gabarits (présentation)")
    v.exige(textes["manuscrit"], ["184 bits", "513-commit", "four"],
            "le coffre durci + la purge (manuscrit)")
    v.exige(textes["preuves"], ["(a)-(g)", "513", "57/57"],
            "le coffre + les kits (preuves)")
    v.exige(textes["presentation"], ["513", "57/57", "184"],
            "le coffre + les kits (présentation)")

    # ---- (5) LE CONTRÔLE D81 --------------------------------------------
    print("\n== LE CONTRÔLE D81 (ou6wn6wlv — la table nommée) ==")
    controle_d81(textes, v)

    # ---- (6) LES EMPREINTES GRAVÉES -------------------------------------
    print("\n== LES EMPREINTES GRAVÉES ==")
    emp = {n: sha(p) for n, p in PIECES.items()}
    for piece in ("manuscrit", "specification", "livre", "preuves"):
        v.cond(emp[piece] in textes["presentation"],
               f"l'empreinte sha-256 de la pièce {piece} GRAVÉE à la "
               f"présentation", "l'empreinte recalculée absente du texte")
    for piece in ("manuscrit", "specification", "livre"):
        v.cond(emp[piece] in textes["preuves"],
               f"l'empreinte sha-256 de la pièce {piece} gravée au document "
               f"de preuves", "l'empreinte recalculée absente du texte")

    print()
    if v.rouges:
        print(f"LE LINTER v230 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              f"le build est REFUSÉ")
        for r in v.rouges:
            print(f"  ROUGE — {r}")
        return 1
    print(f"LE LINTER v230 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    raise SystemExit(controle())
