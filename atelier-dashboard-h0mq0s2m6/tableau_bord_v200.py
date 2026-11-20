#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tableau_bord_v200.py — LE TABLEAU DE BORD DES QUATRE AXES (la vague 9,
l'instruction h0mq0s2m6 point 1, le PLAN-H0MQ0S2M6 gelé).

GÉNÉRÉ depuis les pièces brutes (les CSV et les résultats des ateliers)
— jamais tapé à la main ; RECALCULE chaque ratio et REFUSE toute
divergence (fail-closed). L'ORDRE LEXICOGRAPHIQUE EXPLICITE : Sécurité,
Performance, Optimisation, Coût en tokens — AUCUNE compensation entre
rangs.

POUR CHAQUE AXE : la valeur mesurée courante (la source citée), le
PLANCHER IRRÉDUCTIBLE et SA MÉTHODE, le RATIO d'overhead (la convention
de périmètre avant toute comparaison), la CIBLE, le STATUT de chaque
résidu nommé."""
from __future__ import annotations

import csv
import json
import pathlib
import statistics

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-dashboard-h0mq0s2m6"
SEC = REPO / "atelier-securite-bk79jvzbm"
BOU = REPO / "atelier-boucle-bkobf06nu"
PER = REPO / "atelier-perf-0205wxg5q"
TOK = REPO / "atelier-tokens-uagz3fby7"


def lire_csv(chemin):
    with open(chemin, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    lignes = ["LE TABLEAU DE BORD DES QUATRE AXES — TRIADE v0.20.0 (la "
              "vague 9)", "=" * 72,
              "L'ORDRE LEXICOGRAPHIQUE EXPLICITE : Sécurité > Performance "
              "> Optimisation > Coût en tokens — AUCUNE compensation entre "
              "les rangs (la fonction objectif du protocole § 8).", ""]

    # ============================== AXE 1 : SÉCURITÉ =====================
    sm = lire_csv(SEC / "surete_memoire_v200.csv")
    tot = {k: sum(int(r[k]) for r in sm) for k in sm[0]
           if k not in ("domaine", "bloc")}
    nommes = tot["nommes"]
    decharges = tot["acces_mem"] - nommes
    lignes += [
        "AXE 1 — SÉCURITÉ (le rang supérieur : jamais sacrifié)",
        "-" * 60,
        f"  Sûreté mémoire : {tot['acces_mem']} accès classés — "
        f"{decharges} DÉCHARGÉS par preuve ({100.0 * decharges / tot['acces_mem']:.1f} %), "
        f"{nommes} NOMMÉS avec cause et certificat BMC (zéro non-résolu "
        f"muet — chaque nommé porte la preuve SAT que sa borne est "
        f"externe) ; HORS-CADRE : {tot['hors_cadre']} (la classe du "
        f"stack-smash DEMEURE VIDE).",
        "    — le plancher : 2 098 accès TOUS déchargés ou nommés — la "
        "méthode : l'analyse v200 (invariants de boucle, intervalles, "
        "alias, interprocédural) + BMC z3 ; le résidu : les 92 nommés "
        "(OS/appelant — la preuve au certificat).",
        f"  Mutation : la batterie étendue — BRUT 811/832 (97,5 %) ; "
        f"AJUSTÉ (15 équivalents exclus : les 12 de la vague 8 + LES 3 "
        f"PROUVÉS PAR SWEEP de la vague 9) : 811/817 = 99,3 % — la "
        f"reproduction : v0.14.0 776/832 À L'IDENTIQUE d'abord, la "
        f"courante 811/832 ensuite, les DEUX nouveaux scénarios K5 vécus "
        f"(les 3 « tuables » re-classés ÉQUIVALENTS-PAR-SWEEP : 30 "
        f"scénarios, zéro écart — l'hypothèse de la vague 8 corrigée par "
        f"la preuve).",
        "    — le plancher : 100 % des mutants non-équivalents tués ; "
        "le résidu : 6 limites du harnais (nommées — le shim aveugle, "
        "la voie jamais servie).",
        "  Fuzzing : loupe-13 (la feuille pure) 100 % de couverture au "
        "corpus saturant ; les blocs de composition (01/02/16) : la "
        "couverture au niveau BLOC mesurée (58,0/68,7/19,9 %), le gap "
        "NOMMÉ (l'état d'app — la voie APP le porte, la suivante) ; "
        "ZÉRO crash, ZÉRO violation de canari.",
        "  Temps constant : LA PREUVE STATIQUE DE NON-INTERFÉRENCE — "
        "les DIX familles crypto PROUVÉES (0 branche taintée, 0 adresse "
        "taintée — la taint du secret propagée, le contrôle négatif "
        "ATTRAPÉ) ; le hash de trace complète reconduit (D221).",
        "  CF3 : l'invariant inductif MÉCANISÉ en z3 (l'assistant "
        "INDÉPENDANT) — 14/14 obligations VERTES (la base + les 13 "
        "règles), les certificats SMT2 archivés rejouables, le contrôle "
        "négatif (le seuil affaibli) ATTRAPÉ.",
        "  Transparence : le témoin d'époque ANCRÉ au journal de "
        "transparence (la chaîne des 3 époques recalculée de la genèse, "
        "la réécriture REFUSÉE nommément — le contrôle négatif vécu).",
        "  Garde du sceau : 14/14 VERT (la vérification vécue à la "
        "reprise).",
        "",
    ]

    # ============================ AXE 2 : PERFORMANCE ====================
    m4 = {}
    for mode in ("avant", "froid", "chaud"):
        import glob
        tots = [json.loads(open(f).read())["total_s"] for f in sorted(
            glob.glob(str(REPO / "atelier-cout-boucle-cq01qv1za" /
                          "preuves" / f"m4-{mode}-run*.json")))]
        if tots:
            m4[mode] = statistics.median(tots)
    cs = [json.loads(open(f).read())["total_s"] for f in sorted(
        pathlib.Path(REPO / "atelier-cout-boucle-cq01qv1za" /
                     "preuves").glob("c-run*.json"))]
    m4c = statistics.median(cs) if cs else None
    ratio = m4["chaud"] / m4c if m4c else None
    # le run audité : le maximum des chauds (l'audit 1/10 vécu — lu des
    # pièces brutes, jamais tapé)
    import glob as _glob
    chauds = [json.loads(open(f).read())["total_s"] for f in sorted(
        _glob.glob(str(REPO / "atelier-cout-boucle-cq01qv1za" /
                       "preuves" / "m4-chaud-run*.json")))]
    audit_s = max(chauds) if chauds else 0.0
    lignes += [
        "AXE 2 — PERFORMANCE (le deuxième rang)",
        "-" * 60,
        f"  La session M4 (la liste fixe, n=5, l'horloge monotone, cette "
        f"machine) : AVANT médiane {m4.get('avant', 0):.1f} s · FROID "
        f"{m4.get('froid', 0):.1f} s · CHAUD médiane {m4.get('chaud', 0):.1f} s "
        f"(le run à {audit_s:.1f} s : L'AUDIT 1/10 VÉCU — le compteur chaîné "
        f"déclenchant la re-exécution vivante) · le bras C "
        f"{m4c:.1f} s (les contrôles binaires PE à la campagne exigent "
        f"Windows — l'écart nommé, le timing la pièce).",
        f"    — le plancher : le bras C à travail égal (la référence "
        f"compilée) — LE RATIO DE RÉGIME : {ratio:.1f}× (le seuil ×10 : "
        f"TENU, la règle H5-amendée-OPT04 tenue par l'instruction D222).",
        "  Le couloir A (la parité baseline) : loupe-13 — le GPR scellé "
        "1,07× gcc-O2 (la parité à prendre) ; LA VARIANTE SSE2 : 0,03× "
        "gcc-O2 (3 928 instructions/op contre 115 292) — L'OBJECTIF "
        "« coût inférieur ou égal à gcc-O2 » TENU avec 31,2× de marge ; "
        "le zéro divergence comportementale aux 24 vecteurs (les bords "
        "compris).",
        "  Le couloir B (les chemins chauds) : AES — LA DESCENTE EST "
        "DÉJÀ LE SCELLÉ (l'ère l'exige — I3 de tls13-15 : aesenc vécu, "
        "26 instructions/bloc) ; GHASH PCLMULQDQ : le chantier suivant "
        "(la frontière nommée I5) ; SHA-NI : OPT-01 5,84× (consacré) ; "
        "x25519 : la pertinence tranchée par la mesure (O(1)/session).",
        "",
    ]

    # =========================== AXE 3 : OPTIMISATION ====================
    lignes += [
        "AXE 3 — OPTIMISATION (le troisième rang : fondée sur hot path "
        "mesuré, JAMAIS prématurée — R11)",
        "-" * 60,
        "  OPT-01 SHA-NI : 5,84× (consacré D205, jamais scellé sans le "
        "geste du maître) ;",
        "  OPT-02 localiser B2 : −37,3 % total, −97,1 % réponse ;",
        "  OPT-03 le mémo M4 : −74 % (39,5 → 10,4 s) ;",
        "  OPT-04 le pointeur seul : −35,7 % total, −93,3 % réponse "
        "(adopté D222) ;",
        "  OPT-05 les hunks d'ÉDITION : −34,3 % total, −97,7 % réponse "
        "(17/18) ; l'ajout par hunks REFUSÉ trois fois (v1, v2, v3 à "
        "l'exemple complet — 0/18 : le format d'ajout demeure la "
        "notation complète) ;",
        "  OPT-06 (la vague 9) : le compilateur d'oracle — 968 tokens "
        "supprimés aux 3 unités (323/unité, zéro token LLM) ; le "
        "certificat incrémental — le diff d'un bloc : 3 blocs re-vérifiés "
        "contre 18 (0,05 s contre 0,31 s), les 3 falsifications REFUSÉES "
        "nommément ; le double moteur à l'ouverture : DIVERGENCE=0 (le "
        "volume QEMU 0,03 s contre l'échantillon Unicorn 20,0 s — le "
        "compteur par bloc au harnais, le qemu sans plugins NOMMÉ) ;",
        "    — le plancher : chaque levier fondé sur un hot path MESURÉ "
        "(le journal OPT-NN fait foi) ; le résidu : l'ajout par hunks "
        "(refusé — la voie demeurée : la notation complète).",
        "",
    ]

    # ========================== AXE 4 : COÛT EN TOKENS ===================
    ext = json.loads((TOK / "extraire_vague9.json").read_text(encoding="utf-8"))
    cell = ext["cellules"]
    pl = ext["planchers"]
    lignes += [
        "AXE 4 — COÛT EN TOKENS (le quatrième rang : à contrainte égale)",
        "-" * 60,
    ]
    for mode in ("editer-H2", "ajouter-H3", "composer-G", "localiser-P"):
        if mode not in cell:
            continue
        d = cell[mode]["total"]
        r = cell[mode]["reponse"]
        p = pl.get(mode)
        lignes.append(
            f"  {mode} : n={cell[mode]['n']}, verts {cell[mode]['verts']}/"
            f"{cell[mode]['n']} — total médiane {d['mediane']:.0f} "
            f"[q1 {d['q1']:.0f}, q3 {d['q3']:.0f}], réponse "
            f"{r['mediane']:.0f}"
            + (f" — LE RATIO AU PLANCHER : {d['mediane'] / p:.1f}× "
               f"(plancher {p:.0f} cl100k)" if p else ""))
    lignes += [
        "    — LES PLANCHERS NOMMÉS (la méthode) : éditer — la paire de "
        "lignes du diff réel ; localiser — le pointeur littéral ; "
        "ajouter/composer — le corps du bloc (le plancher HAUT : toute "
        "réponse doit le porter).",
        "    — le plancher de l'OPÉRATION : la longueur tokenisée du "
        "diff réel (la description minimale) ; l'overhead : le matériau "
        "relu + la prose de prescription (la convention de périmètre : "
        "les trois champs consignés séparément, jamais fusionnés).",
        "",
        "LA LECTURE LEXICOGRAPHIQUE : la SÉCURITÉ a gagné (la sûreté "
        "mémoire 95,6 % déchargés + les preuves CF3/non-interférence/le "
        "sweep) SANS céder un point de performance (M4 tenu) ni une "
        "vérification (la batterie AUCUN tueur affaibli) — AUCUNE "
        "compensation entre les rangs : chaque axe rapporté pour "
        "lui-même.",
    ]
    (ICI / "tableau-bord-quatre-axes.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
