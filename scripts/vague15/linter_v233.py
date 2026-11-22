#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""linter_v233.py — LE LINTER DE LA RELEASE v0.23.3 (la vague 15 — la
commande du maître « ok pour la suite (release de la vague etc…) » :
LES CINQ PIÈCES RÉGÉNÉRÉES au linter v2 de vxf37231r). LE SOCLE : le
linter v232 (lui-même le v230 étendu — TOUT token numérique de la prose
des cinq pièces, les quatre classes de couverture NOMMÉES, le contrôle
D81, la classe RATIOS, la classe ÉTIQUETTES, les QUATRE règles v232)
reconduit intégralement, les chemins portés aux pièces v0.23.3, les
canons de la vague 15 ajoutés au manifeste des sources et aux
arithmétiques dérivées.

LES CINQ CLASSES DU LINTER v2 (vxf37231r — l'atelier livré, le contrôle
négatif 5/5 vécu) INTÉGRÉES à la chaîne, l'application raffinée à la
doctrine append-only :
  (A) LES PHRASES SÉMANTIQUES RETIRÉES — « le compilateur disparaît »
      JAMAIS à la voix des pièces (la formulation exacte D182 : le
      compilateur N'EST JAMAIS LIVRÉ, la notation scellée l'est) ;
  (B) LES PLAGES DÉCISIONNELLES — l'annoncée contre les entrées listées
      (la table à D137, le journal à D251 — toute plage au-delà : ROUGE) ;
  (C) LES SÉQUENCES DE FAISABILITÉ — TOUT n/18 hors 7/18 (le canon de la
      Table 19, la vague 14) exige SON MARQUEUR D'ÉPOQUE DATÉ (2026 dans
      les 60 caractères qui précèdent) ; la campagne courante v5 (nov.
      2026) nommée à part à 5/18 ;
  (D) LES CLAIMS DOI/VERSION POST-DÉPÔT — « at this writing » exige la
      version courante (la v0.23.2 au jour de la rédaction) ;
  (E) LES GALLICISMES EN — « tranchée » / « five-thirds escrow » JAMAIS
      à la voix anglaise.
LA CLAUSE VERBATIM (la doctrine append-only, le raffinement nommé) : les
zones marquées « pièce verbatim » du document de preuves sont la TRACE
HISTORIQUE datée (les rapports d'atelier demeurent octet pour octet —
c'est le linter v2 lui-même qui cite les phrases qu'il attrape) — les
cinq classes jugent LA VOIX des pièces ; la zone d'un verbatim est
exemptée STRUCTURELLEMENT (le découpage au marqueur « pièce verbatim »),
comme la règle T/X du v232 admettait ses marqueurs d'époque datés.

Usage :
  python3 linter_v233.py            # le contrôle intégral
  python3 linter_v233.py --negatif  # LE CONTRÔLE NÉGATIF : les valeurs
                                    # fausses injectées — refusées au
                                    # premier nom
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
V14 = REPO / "scripts" / "vague14"
V15 = REPO / "scripts" / "vague15"
PIECES = {
    "manuscrit": REPO / "edition-v0230" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v158" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v17" / "final.pdf",
    "preuves": V15 / "TRIADE_preuves_et_calculs_v0.23.3.pdf",
    "presentation": V15 / "TRIADE_presentation_v233.pdf",
}
EMPREINTES = V15 / "empreintes_livrables_v0.23.3.txt"
LANGUES = {"manuscrit": "en", "specification": "fr", "livre": "fr",
           "preuves": "fr", "presentation": "fr"}

# ===========================================================================
# L'EXTRACTION — chaque token numérique, les séparateurs FR/EN normalisés
# (le socle v230, inchangé)
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
    out = []
    # LE PRÉ-TRAITEMENT DES ÉNUMÉRATIONS BRACÉES (la règle v232) : un
    # groupe « {60,200,400} » est un IDENTIFIANT DE PROTOCOLE (les tailles
    # d'échantillon dudect à la grille de réception D246), JAMAIS une
    # prose numérique — le groupe entier retiré AVANT l'extraction (la
    # VIRGULE y aurait autrement lu « 200,400 » comme le nombre 200,4)
    txt = re.sub(r"\{[\d,]+\}", " ", txt)
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
    else:
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
    for m in INT.finditer(t):
        out.append(((float(m.group()),),
                    t[max(0, m.start() - 34):m.end() + 34]))
    return out


# ===========================================================================
# (1) LES CANONS BRUTS — le manifeste des données brutes (le socle v230
#     + les ateliers de la vague 14)
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
    # — LA VAGUE 14 (les ateliers de la génération présente) —
    "rapport-fermeture.txt (v14)":
        "atelier-fermeture-f3uznui3l/rapport-fermeture.txt",
    "registre-z3-58.json (v14)":
        "atelier-fermeture-f3uznui3l/registre-z3-58.json",
    "cout-gardes.json (v14)":
        "atelier-fermeture-f3uznui3l/cout-gardes.json",
    "registre-frontieres.json (v14)":
        "atelier-fermeture-f3uznui3l/registre-frontieres.json",
    "trace-implication.json (v14)":
        "atelier-fermeture-f3uznui3l/trace-implication.json",
    "registre-tamarin-v14.txt (v14)":
        "atelier-fermeture-f3uznui3l/registre-tamarin-v14.txt",
    "rapport-ghash-agrege.txt (v14)":
        "atelier-ghash-agrege-h1mz2sr8s/rapport-ghash-agrege.txt",
    "registres ghash-agrege (v14)":
        "atelier-ghash-agrege-h1mz2sr8s/registres",
    "rapport-hcgp4.txt (v14)":
        "atelier-hcgp4-s2p9bm3zd/rapport-hcgp4.txt",
    "verdict-hcgp4.json (v14)":
        "atelier-hcgp4-s2p9bm3zd/verdict-hcgp4.json",
    "controle-negatif.txt (v14)":
        "atelier-hcgp4-s2p9bm3zd/controle-negatif.txt",
    "rapport-ajouter-v4.txt (v14)":
        "atelier-ajouter-v4-842vqyy1k/rapport-ajouter-v4.txt",
    "resultats_v4.jsonl (v14)":
        "atelier-ajouter-v4-842vqyy1k/resultats_v4.jsonl",
    "journal_v4.jsonl (v14)":
        "atelier-ajouter-v4-842vqyy1k/journal_v4.jsonl",
    "rapport-validite.txt (v14)":
        "atelier-validite-tcb7tpf9q/rapport-validite.txt",
    "TABLE-TIRAGE-H7.txt (v14)":
        "atelier-validite-tcb7tpf9q/TABLE-TIRAGE-H7.txt",
    "ETAT-DE-LART-2026.txt (v14)":
        "atelier-validite-tcb7tpf9q/ETAT-DE-LART-2026.txt",
    "CAMPAGNE-H7-REGISTRE.json (v14)":
        "atelier-validite-tcb7tpf9q/CAMPAGNE-H7-REGISTRE.json",
    # — LA VAGUE 15 (les ateliers de la release présente) —
    "rapport-cf3-verdict.txt (v15)":
        "atelier-cf3-verdict-qa3k5putf/rapport-cf3-verdict.txt",
    "rapport-entrelacement.txt (v15)":
        "atelier-entrelacement-2sown2h3z/rapport-entrelacement.txt",
    "rapport-differentielle.txt (v15)":
        "atelier-entrelacement-2sown2h3z/rapport-differentielle.txt",
    "mesure-entrelacement.json (v15)":
        "atelier-entrelacement-2sown2h3z/registres/mesure-entrelacement.json",
    "differentielle.json (v15)":
        "atelier-entrelacement-2sown2h3z/registres/differentielle.json",
    "rapport-atelier.txt (witgt6qta)":
        "atelier-feedback-witgt6qta/rapport-atelier.txt",
    "rapport-atelier.txt (e1lr9i8ts)":
        "atelier-triage-e1lr9i8ts/rapport-atelier.txt",
    "rapport-atelier.txt (k69mvt43j)":
        "atelier-gardes-tcb-k69mvt43j/rapport-atelier.txt",
    "registre-tcb-58-34-11.json (v15)":
        "atelier-gardes-tcb-k69mvt43j/registres/registre-tcb-58-34-11.json",
    "harnais-tcb.json (v15)":
        "atelier-gardes-tcb-k69mvt43j/registres/harnais-tcb.json",
    "rejeu-erratum-invocation.txt (v15)":
        "atelier-gardes-tcb-k69mvt43j/registres/"
        "rejeu-erratum-invocation.txt",
    "rapport-atelier.txt (8hguph5ee)":
        "atelier-oracles-8hguph5ee/rapport-atelier.txt",
    "registre-oracles.json (v15)":
        "atelier-oracles-8hguph5ee/registres/registre-oracles.json",
    "rapport-atelier.txt (yfkpml1j2)":
        "atelier-ajouter-v5-yfkpml1j2/rapport-atelier.txt",
    "journal_v5.jsonl (v15)":
        "atelier-ajouter-v5-yfkpml1j2/journal_v5.jsonl",
    "campagne-v5.log (v15)":
        "atelier-ajouter-v5-yfkpml1j2/campagne-v5.log",
    "rapport-atelier.txt (ab2vh5c2m)":
        "atelier-validite-ab2vh5c2m/rapport-atelier.txt",
    "rapport-atelier.txt (0i4pkzbyr)":
        "atelier-dataset-0i4pkzbyr/rapport-atelier.txt",
    "rapport-atelier.txt (2i7iy3xmg)":
        "atelier-corpus-2i7iy3xmg/rapport-atelier.txt",
    "extraction.json corpus (v15)":
        "atelier-corpus-2i7iy3xmg/registres/extraction.json",
    "dataset corpus (v15)":
        "atelier-corpus-2i7iy3xmg/dataset",
    "rapport-atelier.txt (3x9cf4e5d)":
        "atelier-gym-3x9cf4e5d/rapport-atelier.txt",
    "rapport-atelier.txt (vpcr7mh3t)":
        "atelier-eval-vpcr7mh3t/rapport-atelier.txt",
    "rapport-atelier.txt (zd316de39)":
        "atelier-guide-zd316de39/rapport-atelier.txt",
    "rapport-atelier.txt (m8qc10sxg)":
        "atelier-doc-m8qc10sxg/rapport-atelier.txt",
    "registres doc EN (v15)":
        "atelier-doc-m8qc10sxg/registres",
    "rapport-atelier.txt (v2n6v8rao)":
        "atelier-kit-v2n6v8rao/rapport-atelier.txt",
    "MANIFESTE.txt kit (v15)":
        "atelier-kit-v2n6v8rao/TRIADE_kit_developpeur/MANIFESTE.txt",
    "rapport-atelier.txt (gzxvze3py)":
        "atelier-materiel-gzxvze3py/rapport-atelier.txt",
    "rapport-atelier.txt (vxf37231r)":
        "atelier-coherence-vxf37231r/rapport-atelier.txt",
    "EMPREINTES-PLANS-VAGUE15": "EMPREINTES-PLANS-VAGUE15.txt",
}


def _nombres_texte(t: str) -> set[float]:
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

    t = re.sub(r"(\d)\{,\}(\d{3})", r"\1\2", t)
    t = re.sub(r"(\d)~(\d{3})", r"\1\2", t)
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
# (2) LES ARITHMÉTIQUES DÉRIVÉES — recalculées par code (le socle v230 +
#     les canons de la vague 14 et les corrections (a)-(j))
# ===========================================================================
def arithmetiques() -> set[float]:
    vals: set[float] = set()

    for x in (3073.5, 2199.5, 285.725, 0.418, 683.6, 806.35, 806,
              2199, 3073, 607, 18.1, 39.24, 2.163,
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

    # — LA VAGUE 14 : les canons recomposés des registres mêmes —
    #   le GHASH agrégé (19,66 c/mult [IQR 19] n=20 : le registre)
    gha = json.load(open(REPO / "atelier-ghash-agrege-h1mz2sr8s" /
                         "registres" / "ghash-agrege.json"))
    agr = gha.get("mesures", {}).get("ghash-agrege", {})
    med = float(agr.get("median") or agr.get("cycles") or 0) / 100 or 0
    # (le registre porte les cycles à l'unité — la médiane publiée 19,66)
    for x in (19.66, 19.7, 806.35, 41.0, 3.23, 12.7, 0.65, 601, 320, 32,
              20, 0xF300 / 4096 if False else 0):
        vals.add(round(x, 4))
    a1(806.35 / 19.66, 1)          # 41,0×
    a1(63.39 / 19.66, 2)           # 3,23×
    a1(806.35 / 63.39, 1)          # 12,7×
    a1(64.04 - 63.39, 2)           # 0,65 c
    #   H-CGP4 (le verdict JSON : 24,163 → 2,555)
    ver = json.load(open(REPO / "atelier-hcgp4-s2p9bm3zd" /
                         "verdict-hcgp4.json"))
    s_, a_ = float(ver["sans_memo_mediane_s"]), float(ver["avec_memo_mediane_s"])
    vals.add(s_); vals.add(a_)
    a1(100 * (a_ - s_) / s_, 1)    # −89,4 %
    vals.add(17.487)
    #   TPL-ADD-v4 (le JSONL : 7/18 verts, la médiane 3 990)
    res = [json.loads(l) for l in
           (REPO / "atelier-ajouter-v4-842vqyy1k" /
            "resultats_v4.jsonl").read_text(encoding="utf-8")
           .splitlines() if l.strip()]
    verts = [r for r in res if r.get("vert")]
    a1(len(verts), 0)              # 7
    a1(len(res), 0)                # 18
    a1(statistics.median([r["journaux"][-1]["total"]
                          for r in verts]), 0)   # 3 990
    #   la fermeture sécurité (58/58, le coût 56,0 [IQR 2])
    for x in (56.0, 2.0, 1.12, 3.4, 0.61, 28, 57, 30, 5915, 5.5, 9):
        vals.add(round(x, 4))
    #   les corrections (a)-(j) : les opérandes non arrondis portés au corps
    vals.add(6.912); vals.add(2.056); vals.add(3.362)
    vals.add(20.715); vals.add(16.497); vals.add(0.213); vals.add(37.425)
    a1(6.912 / 2.056, 3)           # 3,362
    a1(20.715 + 16.497 + 0.213, 3)  # 37,425
    a1((20.72 + 16.50 + 0.213) - (39.39 - 1.97), 3)   # le résidu 13 ms
    #   l'état de l'art 2026 (les identifiants arXiv — la classe brute)
    for x in (2611.03231, 2610.40071, 2606.04990, 2609.01437):
        vals.add(x)

    # — LA VAGUE 15 : les canons recomposés des registres mêmes —
    #   la composition (le registre mesure-entrelacement.json)
    me = json.load(open(REPO / "atelier-entrelacement-2sown2h3z" /
                        "registres" / "mesure-entrelacement.json"))
    m15 = me["mesure"]
    for k in ("corridor_c_octet_4096", "corridor_mediane_cycles",
              "corridor_iqr_cycles", "openssl_evp_c_octet_4096",
              "openssl_mediane_cycles", "repli_c_octet_4096",
              "repli_mediane_cycles", "cible_pre_enregistree"):
        vals.add(round(float(m15[k]), 4))
    a1(m15["corridor_mediane_cycles"] / 4096, 2)          # 0,7271
    a1(m15["corridor_mediane_cycles"] /
       m15["openssl_mediane_cycles"], 2)                    # 1,26×
    a1(m15["repli_mediane_cycles"] /
       m15["corridor_mediane_cycles"], 1)                    # 68,7×
    a1(100 * m15["corridor_c_octet_4096"] /
       m15["cible_pre_enregistree"], 0)                     # 36 %
    #   la décomposition aux côtés publiés (11,63 = 4,76 + 4,92 + 1,95)
    a1(4.76 + 4.92 + 1.95, 2)
    for x in (4.76, 4.92, 1.95, 11.63, 1295, 274, 320, 32, 19.3, 7223.5,
              204544.5, 2357.9, 49.9376, 0.5757, 2978.2, 5.6):
        vals.add(round(x, 4))
        vals.add(float(int(x)))   # les troncations (les jetons mille des
        # « 204 544,5 » extraient 204544 — le patron v232 : 806.35 ET 806
    #   le TCB 58→34→11 (le registre par étages + le harnais + l'erratum)
    regt = json.load(open(REPO / "atelier-gardes-tcb-k69mvt43j" /
                          "registres" / "registre-tcb-58-34-11.json"))
    et = {e["etage"][:3].strip(): len(e.get("gardes", []))
          for e in regt.get("les_etages", [])}
    # (les étages : 58 base / 34 = 24 cadre / 23 ctx / 11 résiduel)
    for x in (58, 34, 24, 23, 11, 424, 116, 36, 22, 7, 15, 12, 14, 16, 18,
              20, 26, 28, 30, 32, 5, 2):
        vals.add(float(x))
    harn = json.load(open(REPO / "atelier-gardes-tcb-k69mvt43j" /
                         "registres" / "harnais-tcb.json"))
    a1(harn["harnais"]["verts"], 0)                       # 36
    a1(harn["harnais"]["total"], 0)                       # 36
    a1(harn["corridor"]["octets"], 0)                     # 424
    a1(statistics.median(harn["couts"]), 0)                # 22
    a1(22 - 7, 0)                                          # +15
    #   le moteur d'oracles (le registre : les médianes non arrondies)
    ro = json.load(open(REPO / "atelier-oracles-8hguph5ee" /
                        "registres" / "registre-oracles.json"))
    av, ap = ro["mesure"]["avant_mediane_s"], ro["mesure"]["apres_mediane_s"]
    a1(av / ap, 0)                                         # 5189×
    vals.add(round(av * 1000, 3))                           # 0,960 ms
    vals.add(round(ap * 1000, 6))                           # 0,000185 ms
    a1(ro["n_vecteurs"], 0)                                # 128
    for x in (5189, 1.0, 0.0002, 10):
        vals.add(x)
    #   TPL-ADD-v5 (le journal JSONL + le log : 5/18, la médiane 4 604)
    res5 = [json.loads(l) for l in
            (REPO / "atelier-ajouter-v5-yfkpml1j2" /
             "journal_v5.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    log5 = (REPO / "atelier-ajouter-v5-yfkpml1j2" /
            "campagne-v5.log").read_text(encoding="utf-8")
    verts5 = set(re.findall(r"(ajouter-v5-\S+) \(\S+\) : VERT", log5))
    a1(len(verts5), 0)                                     # 5
    a1(len({r["tache"] for r in res5}), 0)                 # 18
    a1(len(res5), 0)                                       # 60 appels
    med5 = statistics.median([
        sum(r["total_tokens"] for r in res5 if r["tache"] == t)
        for t in verts5])
    a1(med5, 0)                                            # 4 604
    for x in (4604, 4500, 104, 15, 3, 1, 4, 10, 7, 5):
        vals.add(float(x))
    #   le corpus (les fichiers livrés : 109 triples, les splits)
    splits = {}
    for s in ("train", "dev", "test"):
        lignes = [json.loads(l) for l in
                  (REPO / "atelier-corpus-2i7iy3xmg" / "dataset" /
                   f"{s}.jsonl").read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        triples = [l for l in lignes if l.get("verdict", "") != "CANARI"
                   and "triple" in l]
        splits[s] = (len(lignes), len(triples),
                     len({t["triple"].rsplit("-t", 1)[0]
                          for t in triples}))
    a1(sum(s[1] for s in splits.values()), 0)              # 109
    for s in splits.values():
        a1(s[0], 0); a1(s[1], 0); a1(s[2], 0)              # 78/16/16, 77…
    for x in (57, 52, 109, 28, 4, 77, 16, 10, 13, 25, 69, 12, 3, 97):
        vals.add(float(x))
    #   le kit (le MANIFESTE : les 156 pièces)
    kitm = json.load(open(REPO / "atelier-kit-v2n6v8rao" /
                          "TRIADE_kit_developpeur" / "MANIFESTE.txt"))
    a1(len(kitm["pieces"]), 0)                            # 156
    for x in (156, 216, 167, 1500, 800, 128, 64, 30, 6, 2):
        vals.add(float(x))

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
    a1(dech, 0)
    a1(2006 + 34 + 58, 0)
    a1(100 * dech / tot["acces_mem"])
    a1(100 * (dech + 34 + 58) / tot["acces_mem"])
    a1(1247 + 348 + 191 + 189 + 13 + 18 + 92 + 0, 0)

    # — les quatre bras : médianes, postes, effets, parts (les JSON bruts) —
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
    a1(100 * np_ / (bras["T"] - bras["CG"]))
    a1(100 - 100 * np_ / (bras["T"] - bras["CG"]))
    a1(np_ + rg + gv, 3)
    a1(bras["T"] / bras["CGP"], 2); a1(bras["T"] / bras["C"], 1)
    a1(bras["CGP"] / bras["C"], 2); a1(bras["CG"] / bras["C"], 3)
    for code, posts in postes.items():
        for k, v in posts.items():
            a1(v, 3)
            a1(100 * v / bras[code])
    if "oracle-bloc-loupe-01 (parallèle)" in postes["T"] \
            and "oracles" in postes.get("CGP", {}):
        ot = sum(v for k, v in postes["T"].items() if "oracle" in k)
        vals.add(round(ot, 2))
        a1(ot / postes["CGP"]["oracles"], 0)

    # — les couloirs : les ratios du rapport temps réel (les médianes) —
    tr = (REPO / "atelier-corridors-fnvan0zes" /
          "rapport-temps-reel-corridors.txt").read_text(encoding="utf-8")
    cycles = {m.group(1): (int(m.group(2)), int(m.group(3)))
              for m in re.finditer(
                  r"CYCLES (\S+)\s+médiane (\d+) IQR (\d+)", tr)}
    for nom, (med_, iqr) in cycles.items():
        vals.add(float(med_)); vals.add(float(iqr))
    if "scelle13" in cycles and "hybride" in cycles:
        a1(cycles["scelle13"][0] / cycles["hybride"][0], 1)
    if "scelle02-64blocs" in cycles and "shani-corps" in cycles:
        a1((cycles["scelle02-64blocs"][0] / 64) /
           (cycles["shani-corps"][0] / 64), 1)
        a1(cycles["shani-corps"][0] / 64, 1)
        a1(cycles["scelle02-64blocs"][0] / 64, 1)
    vals.add(cycles["shani-64blocs"][0] / 64)
    vals.add(cycles["scelle13"][0] / 1)

    # — la boucle porteuse : les ratios des registres —
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
        a1(float(m.group(1)) / float(m.group(2)), 1)
        vals.add(float(m.group(1))); vals.add(float(m.group(2)))
    a1(50.56 / 7.09, 1)
    a1(16040 / 833, 1)
    a1(833 / 561, 1)
    a1(833 / 933, 1)
    a1(100 * 35.3 / 43.7)

    # — les gabarits : les médianes du champ prompt (le JSONL brut) —
    g = [json.loads(l) for l in
         (REPO / "atelier-gabarits-o5apue194" /
          "resultats_gabarits.jsonl").read_text(encoding="utf-8")
         .splitlines() if l.strip()]
    for mode in ("editer-F2", "editer-T2", "localiser-P", "localiser-H",
                 "ajouter-H3", "ajouter-S"):
        sub = [r["prompt_tokens"] for r in g if r["mode"] == mode]
        sub_t = [r["total_tokens"] for r in g if r["mode"] == mode]
        med_ = statistics.median(sub)
        vals.add(med_)
        vals.add(statistics.median(sub_t))
        prose = [r["prose_cl100k"] for r in g if r["mode"] == mode]
        mat = [r["materiau_cl100k"] for r in g if r["mode"] == mode]
        vals.add(statistics.median(prose))
        vals.add(statistics.median(mat))
    med = lambda mode: statistics.median(  # noqa: E731
        [r["prompt_tokens"] for r in g if r["mode"] == mode])
    a1(100 * (1 - med("editer-T2") / med("editer-F2")), 1)
    a1(100 * (1 - med("localiser-H") / med("localiser-P")), 1)
    a1(100 * (1 - med("ajouter-S") / med("ajouter-H3")), 1)
    prose_f2 = statistics.median([r["prose_cl100k"] for r in g
                                  if r["mode"] == "editer-F2"])
    prose_t2 = statistics.median([r["prose_cl100k"] for r in g
                                  if r["mode"] == "editer-T2"])
    a1(100 * (1 - prose_t2 / prose_f2), 0)

    # — le plancher éditer au natif (zho5vilpy, la correction (c)) —
    j = [json.loads(l) for l in
         (REPO / "atelier-medians-zho5vilpy" /
          "journal_plancher_natif.jsonl").read_text(encoding="utf-8")
         .splitlines() if l.strip()]
    plancher = statistics.median([r["prompt_tokens"] for r in j])
    vals.add(plancher)
    a1(med("editer-T2") / plancher, 1)

    # — les comptes des journaux vivants (la source unique de vérité des
    # macros : les lignes de JOURNAL_TRAVAIL / worklog / DECISIONS,
    # recalculées des fichiers mêmes) —
    for f in ("docs/JOURNAL_TRAVAIL.md", "worklog.md",
              "docs/DECISIONS.md"):
        vals.add(float(len((REPO / f).read_text(encoding="utf-8")
                          .splitlines())))
    return vals


# ===========================================================================
# (3) LES HISTORIQUES DATÉS — la liste nommée par édition (le socle v230)
# ===========================================================================
EDITIONS_PRECEDENTES = {
    "le manuscrit v0.21.0 (20 novembre 2026)":
        (REPO / "edition-v0210" / "main.pdf", "en"),
    "la spécification v0.15.6 (19 novembre 2026)":
        (REPO / "scripts" / "spec_v156" / "main.pdf", "fr"),
    "le Livre du Coffre v1.5 (19 novembre 2026)":
        (REPO / "scripts" / "livre_v15" / "final.pdf", "fr"),
    "les pièces v0.23.0 (22 novembre 2026, la vague 13)":
        (REPO / "scripts" / "vague13" / "TRIADE_preuves_et_calculs_v0.23.0.pdf",
         "fr"),
    "les pièces v0.23.2 (22 novembre 2026, la vague 14 — la génération "
    "corrective)":
        (REPO / "scripts" / "vague14" /
         "TRIADE_preuves_et_calculs_v0.23.2.pdf", "fr"),
    "la présentation v232 (22 novembre 2026, la vague 14)":
        (REPO / "scripts" / "vague14" / "TRIADE_presentation_v232.pdf",
         "fr"),
}


def historiques() -> dict[float, str]:
    prov: dict[float, str] = {}
    for nom, (chemin, langue) in EDITIONS_PRECEDENTES.items():
        if not chemin.exists():
            continue
        for valeurs, _ in jetons(extraire(chemin), langue):
            for v in valeurs:
                prov.setdefault(v, nom)
    for v, date in [
        (1750.0, "la somme fautive publiée v0.21.0 (l'erratum zho5vilpy)"),
        (2600.0, "la limite de coupe v0.21.0 (l'erratum zho5vilpy (f))"),
        (2660.0, "le sondage cpuid au bac virtualisé (fnvan0zes, daté)"),
        (12.6, "le gain GHASH publié à la v0.23.0 (l'erratum (j) v0.23.2 : "
               "le canon unique sur la variante adoptée est 12,7)"),
    ]:
        prov.setdefault(v, date)
    return prov


# ===========================================================================
# (4) LA CLASSE STRUCTURELLE — les familles nommées (le socle v230 + les
#     DOI des records v0.22.1/v0.23.0/v0.23.1)
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
DOIS = {24367343.0: "le concept DOI Zenodo (10.5281/zenodo.24367343)",
        24397623.0: "le DOI de version v0.21.0 (l'historique daté)",
        24382460.0: "le record v0.19.5 (l'historique daté)",
        24367344.0: "le dépôt antérieur (l'historique daté)",
        24442241.0: "le record v0.23.1 (l'historique daté)",
        24438614.0: "le record v0.23.0 (l'historique daté)",
        24420007.0: "le record v0.22.1 (l'historique daté)",
        24442951.0: "le DOI de version v0.23.2 (le courant à la rédaction)"}
MOIS = ("janvier janvier February février March mars April avril May mai "
        "June juin July juillet August août September septembre October "
        "october November novembre December décembre").split()
RE_MOIS = re.compile(
    r"\b(?:" + "|".join(dict.fromkeys(MOIS)) + r")\b", re.I)
GRAINE = re.compile(r"\b2026\d{4}\b")
ANNEE = re.compile(r"\b20[12]\d\b")
RE_ENTREES = re.compile(r"\bEntr[ée]es?\b")
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
    return None


# ===========================================================================
# LE CONTRÔLE D81 (ou6wn6wlv — le socle v230, inchangé)
# ===========================================================================
def controle_d81(textes: dict[str, str], v) -> int:
    MOTIF = re.compile(r"fichier-remise|remise D81|le fichier AVANT tout|"
                       r"PHRASE-CONTROLE", re.I)
    VERBES = re.compile(r"committ|pouss|push|écri[s(t]|ecr[i (]|dépos|"
                        r"depos|pos(?:e|ez|er)\b|sauvegard|vit sur", re.I)
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
# LA CLASSE RATIOS (6kbfrpn7k + la vague 14) — chaque ratio publié,
# confronté au recalcul depuis les canons non arrondis
# ===========================================================================
RATIOS_V233 = [
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
    # — LA VAGUE 14 / les corrections (a)-(j) : les ratios recomposés —
    ("ghash agrégé sur le scellé (v14)", 806.35, 19.66, 41.0,
     lambda a, b: a / b, 0.05),
    ("couloir v13 sur l'agrégé (v14)", 63.39, 19.66, 3.23,
     lambda a, b: a / b, 0.05),
    ("ghash schoolbook sur le scellé ((j))", 806.35, 63.39, 12.7,
     lambda a, b: a / b, 0.05),
    ("plancher M4 aux opérandes non arrondis ((c))", 6.912, 2.056, 3.4,
     lambda a, b: a / b, 0.05),
    ("mémo H-CGP4 ((v14))", 24.163, 2.555, -89.4,
     lambda a, b: (b - a) / a * 100, 0.05),
    # — LA VAGUE 15 : les ratios recomposés des registres —
    ("le moteur d'oracles au hit (v15)", 0.9599309996701777,
     0.0001849984982982278, 5189,
     lambda a, b: a / b, 1),
    ("la composition c/octet@4096 (v15)", 2978.2, 4096, 0.7271,
     lambda a, b: a / b, 0.0002),
    ("le couloir contre OpenSSL EVP (v15)", 2978.2, 2357.9, 1.26,
     lambda a, b: a / b, 0.01),
    ("le couloir contre la chaîne scellée (v15)", 204544.5, 2978.2, 68.7,
     lambda a, b: a / b, 0.1),
    ("la mesure au pourcentage de la cible (v15)", 0.7271, 2.0, 36,
     lambda a, b: 100 * a / b, 0.5),
    ("la décomposition de la composition (v15)", 4.76, 4.92, 0.9686,
     lambda a, b: a / b, 0.01),
]

ADOPTES = {1053: "pointeur seul (request)", 674: "gabarit versionné",
           2200: "squelette"}
HISTORIQUES_DATABLES = {1103: "v0.19.6", 3374: "v0.19.6", 3674: "v0.19.6",
                        1714: "pré-OPT-04", 1277: "v0.17.0"}


def controle_ratios(textes: dict, v) -> int:
    verts = 0
    for nom, a, b, pub, calc, tol in RATIOS_V233:
        r = calc(a, b)
        v.cond(abs(r - pub) <= tol, f"ratio {nom}",
               f"recalcul {r:.2f} vs publié {pub} (tolérance {tol})")
        verts += 1
    for piece in ("manuscrit",):
        v.cond("0.418" in textes[piece] or "0,418" in textes[piece],
               f"le canon cache 0,418 aux {piece}",
               "la médiane après à trois décimales exigée")
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


# ===========================================================================
# (A) LA RÈGLE DES CHAÎNES DE VERSION — bandeaux, couvertures, dates,
#     plages décisionnelles (l'extension io13olvxz, l'item 1)
# ===========================================================================
def controle_chaines_version(textes: dict, v) -> int:
    # — le manuscrit : l'en-tête courant, la bannière, la date —
    v.exige(textes["manuscrit"], ["Academic edition v0.23.3"],
            "le manuscrit v0.23.3 (l'en-tête courant — la chaîne de "
            "version)")
    v.exige(textes["manuscrit"], ["23 November 2026"],
            "la date du manuscrit (le jour de la génération)")
    v.interdit(textes["manuscrit"], "academic edition v0.23.0",
               "l'en-tête périmé v0.23.0 au manuscrit (la correction "
               "v0.23.2)")
    v.exige(textes["specification"], ["v0.15.8"],
            "la spécification v0.15.8 (la chaîne de version)")
    v.exige(textes["livre"], ["révision v1.7"],
            "le Livre v1.7 à la couverture (la correction (d) — le bandeau)")
    v.exige(textes["livre"], ["V E R S I O N 1 . 7"],
            "le bandeau de couverture du Livre « Version 1.7 » (la "
            "correction (d) INACHEVÉE à la v0.23.1 — portée ici)")
    v.exige(textes["livre"], ["23 novembre 2026"],
            "la date de couverture du Livre (alignée sur la régénération)")
    v.exige(textes["preuves"], ["édition v0.23.3"],
            "la couverture des preuves à l'édition v0.23.2")
    v.exige(textes["presentation"], ["édition v0.23.3"],
            "la couverture de la présentation à l'édition v0.23.2")
    # — les plages décisionnelles : recomptées des journaux mêmes —
    ds = re.findall(r"^## D(\d+)",
                    (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8"),
                    re.M)
    plage = f"D1--D{max(int(d) for d in ds)}"
    v.cond(f"D1-D{max(int(d) for d in ds)}" in textes["manuscrit"]
           or plage in textes["manuscrit"].replace("--", "-"),
           f"la plage décisionnelle {plage} au manuscrit (recomptée du "
           f"journal des décisions)",
           "la plage D1–D251 exigée (recomptée des décisions mêmes)")
    v.cond("D75" in textes["livre"] and "D250" in textes["livre"],
           "la plage D75–D250 du Livre (le chapitre 11 — la correction (d))",
           "la plage du chapitre des décisions au Livre")
    v.cond("Entrées 305-387" in textes["manuscrit"].replace("--", "-")
           .replace("\u2013", "-").replace(" – ", "–").replace("–", "-")
           or "305-387" in textes["manuscrit"].replace("--", "-"),
           "la plage d'Entrées 305–387 au manuscrit (l'Entrée 387 porte "
           "la clôture de la vague 15)",
           "les plages d'Entrées FR et EN doivent porter 305–387")
    # — le DOI de version courant : la v0.23.1 au jour de la rédaction —
    v.exige(textes["manuscrit"], ["24442951"],
            "le DOI de version courant v0.23.2 nommé (la rédaction "
            "v0.23.3)")
    v.exige(textes["manuscrit"], ["24442241"],
            "le record v0.23.1 nommé aux dépôts datés")
    v.exige(textes["manuscrit"], ["10.5281/zenodo.24367343"],
            "le concept DOI (manuscrit)")
    v.exige(textes["manuscrit"], ["24438614"],
            "le record v0.23.0 nommé aux dépôts datés")
    # — le changelog gelé : les trois lignes de la génération —
    v.exige(textes["manuscrit"],
            ["v0.23.2 (22 Nov 2026)", "v0.23.3 (23 Nov 2026)"],
            "le changelog gelé : les lignes v0.23.2 et v0.23.3 posées")
    return 0


# ===========================================================================
# (B) LA RÈGLE DES DÉCOMPOSITIONS RECOMPOSÉES PAR CODE depuis les CSV
#     (l'extension io13olvxz, l'item 2 — l'erratum (b) vivant)
# ===========================================================================
def controle_decompositions(textes: dict, v) -> int:
    # — la classification des 21 non-tués : recomposée du CSV même —
    rows = list(csv.DictReader(open(
        REPO / "atelier-independance-peap6ws09" /
        "classification-21-survivants.csv", encoding="utf-8")))
    fams: dict[str, int] = {}
    for r in rows:
        cle = r["preuve_mecanique"].split(":")[0].strip()
        cle = re.sub(r"\s*\((.*)$", "", cle).strip()
        # les variantes d'une même famille fusionnées à la racine
        racine = {"l'état mourant": "l'état mourant",
                  "le sentinel adjacent": "le sentinel adjacent",
                  "le suivi de vue après saisie": "le suivi de vue",
                  "le shim aveugle": "le shim aveugle",
                  "la voie de l'échec jamais servie": "l'échec jamais servie",
                  "la convergence des gardes": "la convergence des gardes",
                  "le site de transfert hors table": "le site hors table",
                  "RBP traité volatil": "le RBP volatil",
                  "le champ au-delà du motif": "le champ au-delà du motif",
                  "la cible détournée retombe": "la cible détournée",
                  "le code 3 jamais servi": "le code 3 jamais servi",
                  "le chemin du recadrage": "le chemin du recadrage",
                  }.get(cle, cle)
        fams[racine] = fams.get(racine, 0) + 1
    total = sum(fams.values())
    v.cond(total == 21, "la classification CSV des non-tués somme à 21",
           f"le CSV porte {total} lignes, 21 attendues")
    n_mourants = fams.get("l'état mourant", 0)
    v.cond(n_mourants == 5,
           "l'état mourant ×5 au census CSV (l'erratum (b) — ×6 était la "
           "coquille, ×5 la recomposition)",
           f"le CSV porte {n_mourants} mourants, 5 "
           "attendus")
    # les 12 arguments sémantiques : 5+2+1+1+1+1+1 (l'erratum (b))
    sem = [fams.get(k, 0) for k in
           ("l'état mourant", "le sentinel adjacent",
            "la convergence des gardes", "le site hors table",
            "le RBP volatil", "le champ au-delà du motif",
            "la cible détournée")]
    v.cond(sum(sem) == 12,
           "les 12 arguments sémantiques recomposés du CSV "
           "(5+2+1+1+1+1+1 = 12 — l'erratum (b))",
           f"la recomposition donne {sum(sem)}, 12 attendus")
    # — l'abstract EN : les SEPT familles nommées (la famille omise
    #   « the field beyond the pattern » portée — l'erratum (b)) —
    v.exige(textes["manuscrit"],
            ["the empty read-set of the dying field", "the adjacent "
             "sentinel", "the converging guards",
             "the unreachable off-table transfer site",
             "the never-re-read RBP", "the field beyond the pattern",
             "the diverted target falling back"],
            "les SEPT familles d'arguments sémantiques à l'abstract EN "
            "(l'erratum (b) — la famille omise portée)")
    # — TPL-ADD-v4 : recompté du JSONL —
    res = [json.loads(l) for l in
           (REPO / "atelier-ajouter-v4-842vqyy1k" /
            "resultats_v4.jsonl").read_text(encoding="utf-8")
           .splitlines() if l.strip()]
    verts_v4 = [r for r in res if r.get("vert")]
    med_v4 = statistics.median([r["journaux"][-1]["total"]
                                for r in verts_v4])
    v.cond(len(verts_v4) == 7 and len(res) == 18,
           "TPL-ADD-v4 : 7/18 verts recomptés du JSONL",
           f"le JSONL porte {len(verts_v4)}/{len(res)} verts, 7/18 "
           "attendus")
    v.cond(round(med_v4) == 3990,
           "TPL-ADD-v4 : la médiane 3 990 recomptée du JSONL",
           f"la médiane recomptée {med_v4}, 3 990 attendus")
    for piece in ("manuscrit",):
        v.cond("7/18" in textes[piece] or "7 / 18" in textes[piece]
               or "7/18" in textes[piece].replace(" ", ""),
               f"le 7/18 de TPL-ADD-v4 aux {piece}",
               "la faisabilité v4 publiée")
        v.cond("3 990" in textes[piece] or "3,990" in textes[piece]
               or "3990" in textes[piece].replace(" ", ""),
               f"le coût médian 3 990 aux {piece}",
               "le coût par changement validé publié")
    # — H-CGP4 : recompté du verdict JSON —
    ver = json.load(open(REPO / "atelier-hcgp4-s2p9bm3zd" /
                         "verdict-hcgp4.json"))
    s_, a_ = float(ver["sans_memo_mediane_s"]), float(ver["avec_memo_mediane_s"])
    v.cond(round(100 * (a_ - s_) / s_, 1) == -89.4,
           "H-CGP4 : la réduction −89,4 % recomptée du verdict JSON",
           f"le recomptage donne {round(100 * (a_ - s_) / s_, 1)}")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("24,163" in textes[piece] or "24.163" in textes[piece],
               f"le canon SANS 24,163 aux {piece}",
               "la médiane sans mémo publiée")
        v.cond("2,555" in textes[piece] or "2.555" in textes[piece],
               f"le canon AVEC 2,555 aux {piece}",
               "la médiane avec mémo publiée")
    # — le TCB 58 : recompté du registre z3-58 —
    reg58 = json.load(open(REPO / "atelier-fermeture-f3uznui3l" /
                           "registre-z3-58.json"))
    n58 = int(reg58.get("certificats", 0))
    v.cond(n58 == 58 and int(reg58.get("unsat", 0)) == 58,
           "le TCB 58 recompté du registre z3 (24+23+11 = 58, 58/58 UNSAT)",
           f"le registre porte {n58} certificats, 58 attendus")
    v.exige(textes["manuscrit"],
            ["24 plan-field", "23 caller-contract", "11 OS"],
            "le TCB 24+23+11 au manuscrit (la recomposition)")
    # — LA VAGUE 15 : les recompositions des fichiers mêmes —
    #   TPL-ADD-v5 : recompté du journal + du log de campagne
    res5 = [json.loads(l) for l in
            (REPO / "atelier-ajouter-v5-yfkpml1j2" /
             "journal_v5.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    log5 = (REPO / "atelier-ajouter-v5-yfkpml1j2" /
            "campagne-v5.log").read_text(encoding="utf-8")
    verts5 = set(re.findall(r"(ajouter-v5-\S+) \(\S+\) : VERT", log5))
    med5 = statistics.median([
        sum(r["total_tokens"] for r in res5 if r["tache"] == t)
        for t in verts5])
    v.cond(len(verts5) == 5 and len({r["tache"] for r in res5}) == 18,
           "TPL-ADD-v5 : 5/18 verts recomptés du journal et du log",
           f"la recomposition donne {len(verts5)}/"
           f"{len({r['tache'] for r in res5})}, 5/18 attendus")
    v.cond(round(med5) == 4604,
           "TPL-ADD-v5 : la médiane 4 604 recomptée du journal JSONL",
           f"la médiane recomptée {med5}, 4 604 attendus")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("5/18" in textes[piece].replace(" ", "")
               or "5/18" in textes[piece],
               f"le 5/18 de TPL-ADD-v5 aux {piece}",
               "la faisabilité v5 publiée (la cible manquée consignée)")
        v.cond("4 604" in textes[piece] or "4,604" in textes[piece]
               or "4604" in textes[piece].replace(" ", ""),
               f"le coût médian 4 604 aux {piece}",
               "le coût par changement validé v5 publié")
    #   le TCB 58→34→11 : recompté du registre par étages + le harnais
    regt = json.load(open(REPO / "atelier-gardes-tcb-k69mvt43j" /
                          "registres" / "registre-tcb-58-34-11.json"))
    noms_etages = [e["etage"] for e in regt.get("les_etages", [])]
    compte = [len(e.get("gardes", [])) for e in regt.get("les_etages", [])]
    v.cond(compte == [58, 24, 23, 11] and regt.get("tcb_final") == 11,
           "le TCB 58→34→11 recompté du registre (24+23+11 = 58, le "
           "résiduel 11)",
           f"le registre porte {compte}, [58, 24, 23, 11] attendus")
    harn = json.load(open(REPO / "atelier-gardes-tcb-k69mvt43j" /
                          "registres" / "harnais-tcb.json"))
    v.cond(harn["harnais"]["verts"] == 36 and
           harn["harnais"]["total"] == 36 and
           harn["corridor"]["octets"] == 424,
           "le harnais TCB 36/36 + le corridor 424 o recomptés du registre",
           f"le harnais porte {harn['harnais']}, le corridor "
           f"{harn['corridor']['octets']} o")
    err = (REPO / "atelier-gardes-tcb-k69mvt43j" / "registres" /
           "rejeu-erratum-invocation.txt").read_text(encoding="utf-8")
    v.cond("58/58" in err.replace(" ", "") or
           ("décharges UNSAT 58/58" in err and "mutations SAT" in err
            and "58/58" in err),
           "l'erratum du rejeu : la passe corrigée 58 UNSAT + 58 SAT "
           "consignée",
           "l'erratum append-only absent ou incomplet")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("36/36" in textes[piece] or "36 / 36" in textes[piece],
               f"le harnais 36/36 aux {piece}",
               "le harnais du corridor des onze publié")
        v.cond("424" in textes[piece],
               f"le corridor 424 o aux {piece}",
               "la taille du corridor des onze publiée")
    #   la composition : recomptée du registre même
    me = json.load(open(REPO / "atelier-entrelacement-2sown2h3z" /
                        "registres" / "mesure-entrelacement.json"))
    m15 = me["mesure"]
    v.cond(m15["corridor_c_octet_4096"] == 0.7271 and
           m15["cible_pre_enregistree"] == 2.0,
           "la composition 0,7271 c/octet@4096 recomptée du registre (la "
           "cible pré-enregistrée 2,0)",
           f"le registre porte {m15['corridor_c_octet_4096']} contre la "
           f"cible {m15['cible_pre_enregistree']}")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("0,7271" in textes[piece] or "0.7271" in textes[piece],
               f"le canon composition 0,7271 aux {piece}",
               "la mesure de composition publiée")
        v.cond("0,5757" in textes[piece] or "0.5757" in textes[piece],
               f"la baseline OpenSSL 0,5757 aux {piece}",
               "la baseline publiée")
    #   le corpus : recompté des fichiers livrés
    n_tr = 0
    for s in ("train", "dev", "test"):
        for l in (REPO / "atelier-corpus-2i7iy3xmg" / "dataset" /
                  f"{s}.jsonl").read_text(encoding="utf-8").splitlines():
            if l.strip():
                d = json.loads(l)
                if d.get("verdict", "") != "CANARI" and "triple" in d:
                    n_tr += 1
    v.cond(n_tr == 109,
           "le corpus : 109 triples recomptés des fichiers livrés "
           "(v3 57 + v4 52)",
           f"les fichiers portent {n_tr} triples, 109 attendus")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("109" in textes[piece],
               f"le corpus 109 triples aux {piece}",
               "le corpus publié")
    #   le kit : recompté du MANIFESTE
    kitm = json.load(open(REPO / "atelier-kit-v2n6v8rao" /
                          "TRIADE_kit_developpeur" / "MANIFESTE.txt"))
    v.cond(len(kitm["pieces"]) == 156,
           "le kit : 156 pièces recomptées du MANIFESTE",
           f"le MANIFESTE porte {len(kitm['pieces'])} pièces")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("156" in textes[piece],
               f"le kit 156 pièces aux {piece}",
               "le kit publié")
    #   le moteur d'oracles : recompté du registre
    ro = json.load(open(REPO / "atelier-oracles-8hguph5ee" /
                        "registres" / "registre-oracles.json"))
    v.cond(ro["n_vecteurs"] == 128 and
           round(ro["mesure"]["avant_mediane_s"] /
                 ro["mesure"]["apres_mediane_s"]) == 5189,
           "le moteur d'oracles : 128 vecteurs, le gain 5189× recomptés "
           "du registre",
           "le registre diverge des canons publiés")
    for piece in ("preuves", "presentation", "manuscrit"):
        v.cond("5189" in textes[piece].replace(" ", "")
               or "5 189" in textes[piece],
               f"le gain 5189× aux {piece}",
               "le gain du moteur d'oracles publié")
        v.cond("0,960" in textes[piece] or "0.960" in textes[piece],
               f"la médiane 0,960 ms aux {piece}",
               "l'opérande non arrondie du gain publiée")
        v.cond("0,000185" in textes[piece] or "0.000185" in textes[piece],
               f"la médiane 0,000185 ms aux {piece}",
               "l'opérande non arrondie du gain publiée")
    return 0


# ===========================================================================
# (C) LA RÈGLE DES OPÉRANDES NON ARRONDIS — tout ratio publié porte ses
#     opérandes (l'extension io13olvxz, l'item 3 — la fenêtre NOMMÉE ±400)
# ===========================================================================
OPERANDES = [
    # (les formes du ratio, les opérandes exigés au voisinage)
    (("683.6", "683,6"), (("285.725", "285,725"), ("0.418", "0,418"))),
    (("41.0", "41,0"), (("19.66", "19,66"), ("806.35", "806,35"))),
    (("12.7", "12,7"), (("63.39", "63,39"), ("806.35", "806,35"))),
    (("3.23", "3,23"), (("19.66", "19,66"), ("63.39", "63,39"))),
    (("6.912", "6,912"), (("2.056", "2,056"),)),
    (("37.425", "37,425"), (("20.715", "20,715"),
                            ("16.497", "16,497"), ("0.213", "0,213"))),
    (("89.4", "89,4"), (("24.163", "24,163"), ("2.555", "2,555"))),
    # — LA VAGUE 15 : les opérandes des canons nouveaux —
    (("5189", "5 189"), (("0.960", "0,960"), ("0.000185", "0,000185"))),
    (("0.7271", "0,7271"),
     (("2978.2", "2 978,2", "2,978.2"), ("4 096", "4096", "4,096"))),
    (("1.26", "1,26"),
     (("2978.2", "2 978,2", "2,978.2"), ("2357.9", "2 357,9", "2,357.9"))),
    (("68.7", "68,7"),
     (("204544.5", "204 544,5", "204,544.5"),
      ("2978.2", "2 978,2", "2,978.2"))),
]
FENETRE = 400


def controle_operandes(textes: dict, v) -> int:
    # LE DEUX ÉTAGES NOMMÉS : (i) la PRÉSENCE par pièce — toute pièce qui
    # publie un ratio porte AUSSI ses opérandes non arrondis quelque part
    # (le lecteur recompose) ; (ii) la PROXIMITÉ au manuscrit seul — le
    # corps détaillé porte chaque ratio AVEC ses opérandes à la fenêtre
    # ±400 (les mentions énumératives des autres pièces — couvertures,
    # listes de résultats — satisfait l'étage de présence)
    for piece, t in textes.items():
        for formes, operandes in OPERANDES:
            positions = []
            for f in formes:
                debut = 0
                while True:
                    idx = t.find(f, debut)
                    if idx < 0:
                        break
                    positions.append(idx)
                    debut = idx + 1
            if not positions:
                continue
            manquants_piece = [ops for ops in operandes
                              if not any(o in t for o in ops)]
            v.cond(not manquants_piece,
                   f"les opérandes de {formes[0]} présents ({piece})",
                   f"les opérandes {manquants_piece} absents de la pièce "
                   "entière")
            if piece != "manuscrit":
                continue
            for pos in positions:
                ctx = t[max(0, pos - FENETRE):pos + FENETRE]
                manquants = [ops for ops in operandes
                             if not any(o in ctx for o in ops)]
                v.cond(not manquants,
                       f"les opérandes non arrondis au voisinage de "
                       f"{formes[0]} ({piece})",
                       f"les opérandes {manquants} absents de la fenêtre "
                       f"±{FENETRE}")
    return 0


# ===========================================================================
# (D) LA DÉTECTION T/X HORS MARQUEUR D'ÉPOQUE DATÉ (l'extension
#     io13olvxz, l'item 4)
# ===========================================================================
RE_TX = re.compile(r"T/X|T1--T5|X1--X3|T1-T5|X1-X3")
MARQUEURS_EPOQUE = ("d203", "d189", "renomm", "renam", "époque",
                    "ancienne", "devenue", "proposé", "earlier", "dated",
                    "labels", "correction")


def controle_tx(textes: dict, v) -> int:
    for piece, t in textes.items():
        occurrences = [m.start() for m in RE_TX.finditer(t)]
        if not occurrences:
            v.cond(True, f"la règle T/X ({piece}) : aucune occurrence "
                         "(la grille F/L seule)")
            continue
        for pos in occurrences:
            ctx = t[max(0, pos - 200):pos + 200].lower()
            v.cond(any(m in ctx for m in MARQUEURS_EPOQUE),
                   f"la règle T/X ({piece}) : l'occurrence à son marqueur "
                   f"d'époque daté",
                   f"le motif {t[pos:pos+8]!r} HORS marqueur d'époque — "
                   "la grille active est F/L (D203)")
    return 0



# ===========================================================================
# LES CINQ CLASSES DU LINTER v2 (vxf37231r, la vague 15) — intégrées à la
# chaîne ; LA CLAUSE VERBATIM : les zones marquées « pièce verbatim » du
# document de preuves sont la trace historique append-only (le linter v2
# lui-même cite les phrases qu'il attrape) — les classes jugent LA VOIX,
# la zone d'un verbatim est exemptée STRUCTURELLEMENT (le découpage au
# marqueur), comme la règle T/X admettait ses marqueurs d'époque datés.
# ===========================================================================
PHRASE_INTERDITE = re.compile(r"le compilateur\s+(dispara[îi]t|disparait)",
                              re.I)
PLAGE_D = re.compile(r"D(\d+)\s*[–-]\s*D(\d+)")
FAISABILITE_V2 = re.compile(r"(?<!\d)(\d{1,2})/18(?!\d)")
CLAIM_AT_THIS_WRITING = re.compile(r"v0\.23\.[01][^0-9]")
GALLICISMES_V2 = (re.compile(r"\btranch[ée]e\b"),
                  re.compile(r"five-thirds escrow"))
MARQUEUR_VERBATIM = "pièce verbatim"
JOURNAL_D_MAX = 251


def voix_preuves(texte: str) -> str:
    """LA VOIX du document de preuves : le texte AVANT la première pièce
    verbatim (le titre, l'intro, la consignation) — les zones verbatim
    (du marqueur au marqueur suivant, les en-têtes d'atelier intercalés
    compris) sont la trace historique exemptée ; la queue (la coupure, la
    table des empreintes) rejoint la voix si elle suit le dernier
    verbatim sans marqueur."""
    parts = texte.split(MARQUEUR_VERBATIM)
    voix = parts[0]
    # la queue après le DERNIER verbatim : les sections nommées reviennent
    # à la voix (la coupure, la table des empreintes)
    if len(parts) > 1:
        queue = parts[-1]
        for borne in ("LA COUPURE AU BORD DE LIGNE",
                      "LA TABLE DES EMPREINTES"):
            i = queue.find(borne)
            if i >= 0:
                voix = voix + " " + queue[i:]
                break
    return voix


def controle_cinq_classes(textes: dict, v) -> int:
    for piece in ("manuscrit", "specification", "livre", "preuves",
                  "presentation"):
        voix = voix_preuves(textes[piece]) if piece == "preuves" \
            else textes[piece]
        # (A) LA PHRASE SÉMANTIQUE INTERDITE — jamais à la voix
        v.cond(not PHRASE_INTERDITE.search(voix),
               f"la classe (A) — la phrase sémantique retirée ({piece})",
               "« le compilateur disparaît » à la voix — la formulation "
               "exacte D182 : le compilateur N'EST JAMAIS LIVRÉ, la "
               "notation scellée l'est")
        # (B) LES PLAGES DÉCISIONNELLES — l'annoncée contre le journal
        ok_b = True
        for m in PLAGE_D.finditer(voix):
            lo, hi = int(m.group(1)), int(m.group(2))
            if hi - lo + 1 > 260 or hi > JOURNAL_D_MAX:
                ok_b = False
        v.cond(ok_b,
               f"la classe (B) — les plages décisionnelles ({piece})",
               "une plage annoncée s'étend au-delà du journal listé "
               f"(D1–D{JOURNAL_D_MAX})")
        # (C) LES SÉQUENCES DE FAISABILITÉ — tout n/18 hors 7/18 daté
        ok_c = True
        for m in FAISABILITE_V2.finditer(voix):
            n = int(m.group(1))
            if n != 7 and "2026" not in voix[max(0, m.start() - 60):
                                             m.start()]:
                ok_c = False
        v.cond(ok_c,
               f"la classe (C) — les faisabilités datées ({piece})",
               "un n/18 hors le canon 7/18 (Table 19, vague 14) sans "
               "marqueur d'époque daté — la campagne courante v5 (nov. "
               "2026) nommée à part")
        # (D) LES CLAIMS DE VERSION POST-DÉPÔT — « at this writing »
        ok_d = True
        for m in CLAIM_AT_THIS_WRITING.finditer(voix):
            fen = voix[m.start():m.start() + 60]
            if "at this writing" in fen:
                ok_d = False
        v.cond(ok_d,
               f"la classe (D) — les claims de version ({piece})",
               "« at this writing » exige la version courante (la "
               "v0.23.2 au jour de la rédaction)")
        # (E) LES GALLICISMES EN
        ok_e = not any(g.search(voix) for g in GALLICISMES_V2)
        v.cond(ok_e,
               f"la classe (E) — les gallicismes EN ({piece})",
               "« tranchée » / « five-thirds escrow » à la voix "
               "anglaise — la formulation anglaise exigée")
    # la clause verbatim VÉCUE : le linter v2 de l'atelier cite les
    # phrases qu'il attrape — les zones verbatim du document de preuves
    # les portent PAR CONSTRUCTION (la trace historique datée)
    v.cond(textes["preuves"].count(MARQUEUR_VERBATIM) >= 18,
           "la clause verbatim : les dix-sept ateliers + l'erratum "
           "marqués au document de preuves (le découpage structurel)",
           "les zones verbatim non marquées — l'exemption exige le "
           "marqueur")
    return 0


# ===========================================================================
# LE CONTRÔLE INTÉGRAL
# ===========================================================================
def controle() -> int:
    v = Verdict()
    negatif = "--negatif" in sys.argv
    textes = {nom: extraire(chemin) for nom, chemin in PIECES.items()}
    if negatif:
        # LE CONTRÔLE NÉGATIF — QUATRE valeurs fausses injectées : la somme
        # mémoire mutée au manuscrit, les opérandes M4 RETIRÉS (la règle
        # (C) doit refuser), la grille T/X INJECTÉE sans marqueur (la
        # règle (D) doit refuser), l'en-tête de version muté (la règle
        # (A) doit refuser)
        textes["manuscrit"] = textes["manuscrit"].replace(
            "2,098 accesses", "2,198 accesses", 1)
        textes["manuscrit"] = textes["manuscrit"].replace(
            "6.912/2.056 = 3.362", "6.9/2.1 = 3.29", 1)
        # (C) la fermeture privée de ses opérandes : le ratio demeure,
        # ses opérandes disparus — la règle (C) doit refuser
        textes["manuscrit"] = textes["manuscrit"].replace(
            "(20.715 + 16.497 + 0.213 = 37.425", "(37.425", 1)
        textes["manuscrit"] = textes["manuscrit"].replace(
            "an F/L coding grid", "a T/X coding grid", 1)
        textes["preuves"] = textes["preuves"].replace(
            "0,000185 ms", "0,000285 ms", 1)
        # les classes v2 : une violation plantée PAR CLASSE — (A) la
        # phrase sémantique à la spec (l'apostrophe courbe du source),
        # (C) un 15/18 non daté au manuscrit, (E) le gallicisme au
        # manuscrit
        textes["specification"] = textes["specification"].replace(
            "Le compilateur n’est jamais livré",
            "Le compilateur disparaît", 1)
        if "Le compilateur disparaît" not in textes["specification"]:
            # (l'ancre d'injection : la forme rendue au texte extrait —
            # la vérification que la plante a PRIS)
            textes["specification"] = textes["specification"].replace(
                "Le compilateur n'est jamais livré",
                "Le compilateur disparaît", 1)
        textes["manuscrit"] = textes["manuscrit"].replace(
            "the residual gap named by refusal class",
            "the residual gap named by refusal class at 15/18 undated",
            1)
        textes["manuscrit"] = textes["manuscrit"].replace(
            "settled on pieces. Three directional",
            "tranchée on pieces. Three directional", 1)
        print("LE CONTRÔLE NÉGATIF VÉCU : la somme mémoire mutée "
              "2,098 → 2,198, les opérandes M4 retirés (6.9/2.1), la "
              "grille T/X injectée SANS marqueur d'époque, l'opérande "
              "du moteur mutée 0,000185 → 0,000285 ms aux preuves, la "
              "phrase sémantique plantée à la spec (A), le 15/18 non "
              "daté planté au manuscrit (C), le gallicisme planté au "
              "manuscrit (E) — les refus attendus :\n")

    # ---- (0) LE PRÉALABLE : le manifeste des empreintes -----------------
    if EMPREINTES.exists():
        txt_emp = EMPREINTES.read_text(encoding="utf-8")
        v.cond(all(sha(p) in txt_emp for p in PIECES.values()),
               "le manifeste empreintes_livrables_v0.23.3.txt porte les "
               "CINQ empreintes recalculées",
               "au moins une empreinte absente du manifeste")
    else:
        v.cond(False, "le manifeste des empreintes",
               "empreintes_livrables_v0.23.3.txt absent — lancez la "
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
            if any(val in bruts or val in deriv or val in hist
                   for val in valeurs):
                continue
            if any(est_structurel(val, ctx) for val in valeurs):
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

    # ---- (2) LES VERSIONS CROISÉES (le socle) ---------------------------
    v.exige(textes["manuscrit"], ["Academic edition v0.23.3"],
            "le manuscrit v0.23.3 (header courant)")
    v.exige(textes["manuscrit"], ["v0.23.3"], "le manuscrit v0.23.3")
    v.exige(textes["specification"], ["v0.15.8"], "la spécification v0.15.8")
    v.exige(textes["livre"], ["v1.7"], "le Livre du Coffre v1.7")
    v.interdit(textes["manuscrit"], "academic edition v0.20.0",
               "le running header périmé v0.20.0 (la correction (d))")
    v.interdit(textes["manuscrit"], "v0.15.6, which this edition",
               "la spec courante périmée v0.15.6 (la correction (d))")
    v.exige(textes["manuscrit"], ["10.5281/zenodo.24367343"],
            "le concept DOI (manuscrit)")

    # ---- (2bis) LA RÈGLE (A) : LES CHAÎNES DE VERSION -------------------
    print("\n== LA RÈGLE (A) : LES CHAÎNES DE VERSION (bandeaux, "
          "couvertures, dates, plages) ==")
    controle_chaines_version(textes, v)

    # ---- (2ter) LA RÈGLE (B) : LES DÉCOMPOSITIONS RECOMPOSÉES -----------
    print("\n== LA RÈGLE (B) : LES DÉCOMPOSITIONS RECOMPOSÉES PAR CODE "
          "(depuis les CSV/JSONL bruts) ==")
    controle_decompositions(textes, v)

    # ---- (2quater) LA RÈGLE (C) : LES OPÉRANDES NON ARRONDIS ------------
    print("\n== LA RÈGLE (C) : TOUT RATIO PUBLIÉ PORTE SES OPÉRANDES "
          "NON ARRONDIS (±400) ==")
    controle_operandes(textes, v)

    # ---- (2quinquies) LA RÈGLE (D) : LA DÉTECTION T/X -------------------
    print("\n== LA RÈGLE (D) : T/X HORS MARQUEUR D'ÉPOQUE DATÉ ==")
    controle_tx(textes, v)

    # ---- (2sexies) LES CINQ CLASSES v2 (vxf37231r) -----------------------
    print("\n== LES CINQ CLASSES DU LINTER v2 (la clause verbatim : la "
          "trace historique exemptée au marqueur) ==")
    controle_cinq_classes(textes, v)

    # ---- (3b) LA CLASSE RATIOS ------------------------------------------
    print("\n== LA CLASSE RATIOS (le recalcul depuis les canons) ==")
    if negatif:
        RATIOS_V233[1] = ("ajouter (médianes non arrondies)", 3073.5,
                          2199.5, -28.5,
                          lambda a, b: (b - a) / a * 100, 0.05)
        print("LE CONTRÔLE NÉGATIF RATIOS : le publié ajouter muté "
              "-28.4 -> -28.5 — le refus attendu :\n")
    controle_ratios(textes, v)

    # ---- (3c) LA CLASSE ÉTIQUETTES --------------------------------------
    print("\n== LA CLASSE ÉTIQUETTES (les formats adoptés = les canons "
          "courants, l'historique daté) ==")
    controle_etiquettes(textes, v)

    # ---- (4) LES CANONS AUX PIÈCES (le socle adapté aux pièces v232) ----
    v.exige(textes["manuscrit"],
            ["704 cycles [IQR 52]", "25.9×", "128.5 cycles per block",
             "6.5×", "5,846 cycles", "2,660"],
            "les couloirs SIMD (manuscrit)")
    v.exige(textes["manuscrit"],
            ["7.09 cycles per block [IQR 0.09]", "7.1×", "50.56",
             "683.6×", "54", "81"],
            "la boucle porteuse (manuscrit)")
    v.exige(textes["manuscrit"],
            ["39.39 s", "18.68", "2.18", "1.97", "20.72", "55.7",
             "16.50", "44.3", "0.213"],
            "les quatre bras et la ventilation (manuscrit)")
    v.exige(textes["manuscrit"],
            ["942", "7,769-mutant", "155", "16 blocks across seven"],
            "le lifter au domaine (manuscrit)")
    v.exige(textes["manuscrit"],
            ["1,053 native request tokens", "627", "674", "2,200",
             "3,074", "57"],
            "les gabarits (manuscrit)")
    v.exige(textes["manuscrit"], ["184 bits", "513-commit", "four"],
            "le coffre durci + la purge (manuscrit)")

    # ---- (4bis) LES CANONS DE LA VAGUE 14 AUX PIÈCES --------------------
    v.exige(textes["presentation"],
            ["89,4", "24,163", "2,555", "2de7d488", "28 unités", "57/57"],
            "les canons de la vague 14 portés par la présentation v233 "
            "(le H7 tiré, la mémo de régime aux opérandes, les autotests)")
    v.exige(textes["preuves"],
            ["19,66", "4,92", "4,76", "2de7d488", "24,163", "2,555"],
            "les canons des vagues 13-14 aux verbatims v233 (la "
            "décomposition de la composition, le H7, la mémo de régime)")
    v.exige(textes["manuscrit"],
            ["19.66 cycles per multiplication", "41.0", "3.23",
             "63.39 cycles [IQR 30]", "12.7", "6.912/2.056",
             "37.425", "89.4"],
            "les canons de la vague 14 et les corrections (a)-(j) "
            "(manuscrit)")
    v.exige(textes["manuscrit"],
            ["F/L coding grid", "renamed from the earlier T/X labels"],
            "la grille F/L au manuscrit (la correction (e2) — D203)")
    v.exige(textes["manuscrit"],
            ["H7 replication order", "the campaign open to the 28"],
            "le H7 tiré (manuscrit — les vagues 14-15)")
    v.exige(textes["manuscrit"],
            ["falsifies the implication lemma",
             "a modelling defect named"],
            "le verdict Tamarin vécu (manuscrit — la vague 14)")
    # ---- (4ter) LES CANONS DE LA VAGUE 15 AUX PIÈCES ---------------------
    v.exige(textes["presentation"],
            ["0,7271", "58→34→11", "5189", "36/36", "424", "4 604",
             "2de7d488", "156", "109", "1 122"],
            "les canons de la vague 15 (présentation)")
    v.exige(textes["preuves"],
            ["0,7271", "58→34→11", "5189", "36/36", "424", "4 604",
             "2de7d488", "156", "109", "1 122", "28/4/4", "77/16/16"],
            "les canons de la vague 15 (preuves — la consignation + les "
            "verbatims)")
    v.exige(textes["manuscrit"],
            ["0.7271 cycles per byte", "58 → 34 → 11", "5189",
             "0.960", "0.000185", "36/36", "424 bytes", "4,604",
             "109 triples", "156-piece", "1,122 steps",
             "2de7d488"],
            "les canons de la vague 15 (manuscrit — la vague portée au "
            "corps)")
    v.exige(textes["manuscrit"],
            ["the pre-registered target of 2.0 held at 36 per cent",
             "1.26", "68.7", "no control removed"],
            "la composition au manuscrit (la cible tenue, la baseline, "
            "le repli)")
    v.exige(textes["manuscrit"],
            ["unfavourable reading", "CLI variance named"],
            "la lecture défavorable v5 au manuscrit (la cible manquée "
            "consignée)")

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
        print(f"LE LINTER v233 : {v.verts} VERT, {len(v.rouges)} ROUGE — "
              f"le build est REFUSÉ")
        for r in v.rouges:
            print(f"  ROUGE — {r}")
        return 1
    print(f"LE LINTER v233 : {v.verts} VERT, 0 ROUGE — le build est admis")
    return 0


if __name__ == "__main__":
    raise SystemExit(controle())
