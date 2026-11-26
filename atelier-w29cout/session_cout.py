#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_cout.py — LA LECTURE ÉCONOMIQUE UNIFIÉE (W29COUT, prompt 5 de la
vague 29 — le plan gelé PLAN-W29COUT.md, sha256 2cb546b6… consigné à
EMPREINTES-PLANS-VAGUE29.txt AVANT toute mesure).

AUCUNE valeur mesurée existante n'est modifiée ; aucune cible re-tirée. Les
grandeurs du présent atelier sont des RECALCULS depuis les journaux vivants
(les sources canoniques — la recomposition depuis les fichiers, jamais la
restitution de mémoire) :

1. LA TABLE UNIFIÉE : par opération (localiser / éditer / ajouter) et par ère
   (M1 historique-datée, pointeur-seul, contenu-seul, ADOPTÉE, OPT-16, la
   voie structurée EN ATTENTE), la médiane par tentative, la FAISABILITÉ
   (vertes/n), LE COÛT PAR CHANGEMENT VALIDÉ (la somme des tokens de tous les
   tours et tentatives ÷ vertes — lu du journal usage, jamais une estimation).
2. LES IC BOOTSTRAP 95 % SUR LES MÉDIANES token (B = 10 000 rééchantillonnages,
   la graine 20261128 consignée AVANT le tirage).
3. LES TESTS EXACTS (Fisher bilatéral) sur les différences de FAISABILITÉ :
   9/18 (OPT-16) contre 18/18 (le gabarit adopté) ; 5/18 (ajouter 5ᵉ) contre
   15/18 (la cible CIB-ADD-FAISAB).
4. LES CIBLES NOUVELLES PRÉ-ENREGISTRÉES (jamais un re-tirage) :
   CIB-EDIT-FAISAB ≥ 15/18 et CIB-EDIT-AMORTI ≤ 150 tokens — EN ATTENTE de
   la campagne contrainte (le plan w29decco), AUCUN chiffre fabriqué.
5. LE TEST DU LECTEUR étendu d'un cas par nouvelle grandeur (l'IC, la
   p-value, l'amorti) : un lecteur recompose chacun depuis les opérandes
   imprimés.
6. LE REGISTRE DE PROVENANCE : chaque grandeur → sa source canonique.

Écrit : cout-registre.json
"""
import json
import pathlib
import random

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
JOURNAL = R / "atelier-w28opt16/journal-opt16.jsonl"
GRAINE = 20261128
B = 10000
IC_NIVEAU = 0.95

# LA TABLE DES ÈRES — les valeurs PUBLIÉES (CIBLES.md, la table canonique des
# budgets D222/D241/D251) portées avec leur provenance (jamais re-mesurées) ;
# la ligne OPT-16 RECALCULÉE ici depuis le journal vivant.
ERES = [
    ("localiser", "M1 (historique-datée)", 51, None, "CIBLES.md — la table des ères"),
    ("localiser", "pointeur-seul", 1053, None, "CIBLES.md — la table des ères"),
    ("localiser", "ADOPTÉE (hiérarchique D222)", 627, None, "CIBLES.md — la table des ères"),
    ("éditer", "M1 (historique-datée)", 719, None, "CIBLES.md — la table des ères"),
    ("éditer", "ADOPTÉE (TPL-EDIT-v1 OPT-14)", 674, "18/18", "CIBLES.md — la table des ères"),
    ("éditer", "OPT-16 (diff structuré)", None, None, "RECALCUL — le journal vivant"),
    ("ajouter", "M1 (historique-datée)", 1088, None, "CIBLES.md — la table des ères"),
    ("ajouter", "ADOPTÉE (squelette OPT-14)", 2200, "18/18", "CIBLES.md — la table des ères"),
    ("ajouter", "contenu-seul", 3510, None, "CIBLES.md — la table des ères"),
    ("ajouter", "5ᵉ campagne", 4604, "5/18", "CIBLES.md — CIB-ADD-COUT-4500 (mesurée)"),
    ("ajouter", "voie structurée D264", None, None, "EN ATTENTE — le plan w29decco"),
]


def fisher_exact(a, b, c, d):
    """Le test exact de Fisher bilatéral (la loi hypergéométrique)."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c
    def p(x):
        return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    obs = p(a)
    tot = 0
    lo = max(0, c1 - (n - r1))
    hi = min(r1, c1)
    for x in range(lo, hi + 1):
        px = p(x)
        if px <= obs * (1 + 1e-9):
            tot += px
    return min(1.0, tot)


def mediane(l):
    s = sorted(l)
    n = len(s)
    return (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else s[n // 2]


def main():
    rng = random.Random(GRAINE)          # consignée AVANT le tirage
    journal = [json.loads(l) for l in JOURNAL.read_text(encoding="utf-8").splitlines()]
    par_tache = {}
    for j in journal:
        par_tache.setdefault(j["tache"], []).append(j["completion_tokens"])
    sommes = [sum(v) for v in par_tache.values()]
    med = mediane(sommes)
    res = json.loads((R / "atelier-w28opt16/resultats-opt16.json").read_text(encoding="utf-8"))
    verts = res["verts"]                      # 9 (le verdict publié)
    n_taches = res["n"]                       # 18
    total = sum(j["total_tokens"] for j in journal)
    amorti = total / verts
    plancher = 27.5
    ratio_plancher = med / plancher

    # ---- L'IC BOOTSTRAP 95 % SUR LA MÉDIANE (B = 10 000, graine consignée) --
    boots = []
    for _ in range(B):
        echant = [rng.choice(sommes) for _ in range(len(sommes))]
        boots.append(mediane(echant))
    boots.sort()
    ic_lo = boots[int((1 - IC_NIVEAU) / 2 * B)]
    ic_hi = boots[min(B - 1, int((1 + IC_NIVEAU) / 2 * B))]

    # ---- L'IC BOOTSTRAP sur le coût amorti (la même graine, la même B) ------
    par_tache_total = {}
    for j in journal:
        par_tache_total.setdefault(j["tache"], 0)
        par_tache_total[j["tache"]] += j["total_tokens"]
    boots_a = []
    for _ in range(B):
        echant = [rng.choice(list(par_tache_total.values())) for _ in range(n_taches)]
        tot_e = sum(echant)
        verts_e = round(verts * (len(echant) / n_taches))
        boots_a.append(tot_e / verts_e if verts_e else 0)
    boots_a.sort()
    ic_a_lo = boots_a[int((1 - IC_NIVEAU) / 2 * B)]
    ic_a_hi = boots_a[min(B - 1, int((1 + IC_NIVEAU) / 2 * B))]

    # ---- LES TESTS EXACTS DE FISHER ------------------------------------------
    p1 = fisher_exact(verts, n_taches - verts, 18, 0)          # 9/18 vs 18/18
    p2 = fisher_exact(5, 13, 15, 3)                             # 5/18 vs 15/18

    # ---- LE TEST DU LECTEUR : recomposer depuis les opérandes ---------------
    lecteur = {
        "mediane_opt16": {"operandes": "la médiane des 18 sommes de tours par tâche (le journal)",
                          "attendu": med},
        "amorti": {"operandes": f"{total} ÷ {verts}",
                   "attendu": round(amorti, 2)},
        "ic_mediane": {"operandes": f"B={B}, graine {GRAINE}, niveau {IC_NIVEAU}",
                       "attendu": [ic_lo, ic_hi]},
        "p_fisher_9_18_vs_18_18": {"operandes": "9/18 vs 18/18 (bilatéral)",
                                    "attendu": round(p1, 4)},
        "p_fisher_5_18_vs_15_18": {"operandes": "5/18 vs 15/18 (bilatéral)",
                                    "attendu": round(p2, 4)},
    }

    provenance = {
        "mediane_par_tentative_opt16": "atelier-w28opt16/journal-opt16.jsonl — le champ completion_tokens sommé par tâche, la médiane sur 18",
        "faisabilite_opt16": "atelier-w28opt16/resultats-opt16.json — le champ vert",
        "cout_amorti_opt16": "journal-opt16.jsonl — total_tokens (39 appels) ÷ les vertes",
        "plancher": "CIBLES.md — CIB-DIFF-PLANCHER : 27,5 tokens (le diff réel, REPÈRE)",
        "eres_publiees": "CIBLES.md — la table canonique des budgets (D222/D241/D251), AUCUNE valeur re-mesurée",
        "ic_bootstrap": f"le journal vivant, B={B}, graine {GRAINE}",
        "tests_exacts": "les effectifs publiés (CIBLES.md, resultats-opt16.json)",
    }

    registre = {
        "graine": GRAINE, "B": B, "niveau": IC_NIVEAU,
        "table_eres": [
            {"opération": o, "ère": e,
             "médiane": (med if "OPT-16" in e and o == "éditer" else m),
             "faisabilité": (("9/18" if "OPT-16" in e and o == "éditer" else f)),
             "coût_par_validé": (round(amorti, 2) if "OPT-16" in e and o == "éditer" else None),
             "provenance": ("le journal vivant (recalculé)" if "OPT-16" in e else p)}
            for (o, e, m, f, p) in ERES
        ],
        "opt16": {
            "mediane": med, "ic95": [ic_lo, ic_hi],
            "faisabilite": f"{verts}/{n_taches}",
            "total_tokens": total,
            "cout_amorti": round(amorti, 2),
            "ic95_amorti": [round(ic_a_lo, 2), round(ic_a_hi, 2)],
            "ratio_plancher": round(ratio_plancher, 2),
        },
        "tests_exacts": {
            "fisher_9sur18_vs_18sur18": round(p1, 6),
            "fisher_5sur18_vs_15sur18": round(p2, 6),
        },
        "cibles_nouvelles_pre-enregistrees": {
            "CIB-EDIT-FAISAB": "≥ 15/18 — EN ATTENTE de la campagne contrainte (le plan w29decco)",
            "CIB-EDIT-AMORTI": "≤ 150 tokens par changement validé — EN ATTENTE de la campagne contrainte",
        },
        "lecteur": lecteur,
        "provenance": provenance,
    }
    (ICI / "cout-registre.json").write_text(
        json.dumps(registre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"[opt16] médiane {med} tokens natifs · IC95 bootstrap [{ic_lo}, {ic_hi}] (B={B}, graine {GRAINE})")
    print(f"[opt16] faisabilité {verts}/{n_taches} · amorti {amorti:.2f} tokens "
          f"({total} ÷ {verts}) · IC95 [{ic_a_lo:.2f}, {ic_a_hi:.2f}]")
    print(f"[opt16] ratio plancher {ratio_plancher:.2f}× (médiane {med} / {plancher})")
    print(f"[fisher] 9/18 vs 18/18 : p = {p1:.6f} · 5/18 vs 15/18 : p = {p2:.6f}")
    print("[ères] la table unifiée :")
    for (o, e, m, f, p) in ERES:
        val = (f"{med}" if "OPT-16" in e and o == "éditer" else m)
        fa = ("9/18" if "OPT-16" in e and o == "éditer" else f) or "—"
        am = (f" · amorti {amorti:.2f}" if "OPT-16" in e and o == "éditer" else "")
        print(f"  {o:10s} {e:28s} médiane {val} · faisabilité {fa}{am}")


if __name__ == "__main__":
    main()
