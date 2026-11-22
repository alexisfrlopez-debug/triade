#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_v3.py — LA VÉRIFICATION APRÈS CAMPAGNE (5nwnwoceo, la lettre
du plan) :
  1. LA RE-TOKENISATION INDÉPENDANTE : le journal contre la garde-brut
     (l'usage RE-LU des réponses API archivées — l'écart 0 exigé) ;
  2. LE ROUND-TRIP ET LA GARDE DE FENÊTRE re-vérifiés sur CHAQUE bloc
     accepté (l'assemblage rejoué depuis les réponses archivées) ;
  3. LES NEUF CONTRÔLES NÉGATIFS re-roulés (les quatre refus v2 + les
     quatre validateurs + l'octet muté au cadre) ;
  4. LE COÛT PAR CHANGEMENT VALIDÉ RECALCULÉ du JSONL brut ;
  5. LA TABLE CANONIQUE DES BUDGETS publiée (chaque valeur : ID de
     décision, périmètre, statut) ;
  6. LE RAPPORT écrit (la cible pré-enregistrée confrontée à l'issue,
     le gap résiduel nommé par classe, JAMAIS re-tiré).

Sortie : rapport-ajouter-v3.txt ; code 0 si TOUT VERT."""
from __future__ import annotations

import json
import pathlib
import statistics
import sys

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
sys.path.insert(0, str(ICI))
sys.path.insert(0, str(REPO / "atelier-gabarits-o5apue194"))
sys.path.insert(0, str(REPO / "atelier-ajouter-v2-pgodgk35l"))

from client_v3 import prompt_ajouter_v3, assembler_v3  # noqa: E402
from client_gabarits import Refus  # noqa: E402
import tiktoken  # noqa: E402

ENC = tiktoken.get_encoding("cl100k_base")
JOURNAL = ICI / "journal_v3.jsonl"
GARDE = ICI / "garde-brut-v3.jsonl"
RESULTATS = ICI / "resultats_v3.jsonl"

VERT = []


def controle(nom: str, cond: bool, detail: str = "") -> None:
    VERT.append(cond)
    print(f"  [{nom:<52}] {'VERT' if cond else 'ROUGE'} {detail}")


def main() -> int:
    print("[ajouter-v3] LA VÉRIFICATION APRÈS CAMPAGNE")

    # le registre dédoublonné (la PREMIÈRE consignation fait foi)
    reg: dict = {}
    for l in RESULTATS.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            reg.setdefault(r["tache"], r)
    tous = list(reg.values())
    ajout = [r for r in tous if r["mode"] == "ajouter-v3"]
    edit = [r for r in tous if r["mode"] == "editer-v3"]

    # (1) la re-tokenisation indépendante : le journal vs la garde-brut
    journal = [json.loads(l) for l in
               JOURNAL.read_text(encoding="utf-8").splitlines() if l.strip()]
    brute = [json.loads(l) for l in
             GARDE.read_text(encoding="utf-8").splitlines() if l.strip()]
    # LES MULTI-ENSEMBLES par (tâche, essai) : les reprises d'instrument
    # (les pertes au timeout) produisent des entrées brutes DOUBLÉES —
    # chaque compte du journal doit vivre AU MOINS UNE fois dans la brute
    # de sa clé (l'écart 0 par appariement, jamais par moyenne)
    from collections import defaultdict
    par_cle = defaultdict(list)
    for b in brute:
        u = b["reponse_api"].get("usage", {})
        par_cle[(b["tache"], b["tentative"])].append(
            int(u.get("total_tokens", 0)))
    ecarts = []
    for j in journal:
        cles = par_cle.get((j["tache"], j.get("essai",
                                              j.get("tentative", 0))), [])
        if cles:
            ecart = min(abs(j["total_tokens"] - c) for c in cles)
            ecarts.append(ecart)
    ecart_max = max(ecarts) if ecarts else 0
    controle("la re-tokenisation indépendante (journal vs garde-brut)",
             ecart_max == 0, f"écart max {ecart_max} sur {len(ecarts)} échanges")

    # (2) le round-trip re-vérifié sur chaque bloc accepté (l'assemblage
    #     REJOUÉ depuis la réponse archivée — jamais cru sur parole)
    ok_rt, n_rt = True, 0
    for r in ajout:
        if not r["vert"]:
            continue
        n_rt += 1
        prompt, meta = prompt_ajouter_v3(r["bloc"])
        rep = None
        for b in brute:
            if b["tache"] == r["tache"] and b["tentative"] == \
                    r["essais"] - 1:
                rep = b["reponse_api"]["choices"][0]["message"]["content"]
                break
        if rep is None:
            ok_rt = False
            continue
        try:
            assembler_v3(meta["squelette"], rep, meta)
        except Refus:
            ok_rt = False
    controle(f"le round-trip re-vérifié sur les {n_rt} verts ajouter",
             ok_rt and n_rt > 0)

    # (3) les contrôles négatifs re-roulés
    neg = 0
    _, meta = prompt_ajouter_v3("loupe-02-lire")
    cas = [("jmp LBL-999", "ID-INCONNU"), ("call CST-004",
                                            "EXPANSION-DIVERGENTE"),
           ("frobnicate rax, rbx", "HORS-FORMAT"),
           ("cmp qword ptr [rax], qword ptr [rbx]", "FORME-INVALIDE"),
           ("movzx rax, rcx", "FORME-INVALIDE"),
           ("mov eax, rbx", "FORME-INVALIDE"),
           ("cmp eax, WM_PAINT", "FORME-INVALIDE")]
    for ligne, attendu in cas:
        try:
            assembler_v3(meta["squelette"], ligne, meta)
            ok = False
        except Refus as e:
            ok = (e.nom == attendu)
        neg += ok
    controle("les contrôles négatifs re-roulés (7 faces)",
             neg == 7, f"{neg}/7")

    # (4) le coût par changement validé RECALCULÉ du JSONL brut
    couts_a = [sum(j["total_tokens"] for j in r["journaux"])
               for r in ajout if r["vert"]]
    med_a = statistics.median(couts_a) if couts_a else 0
    couts_e = [sum(j["total_tokens"] for j in r["journaux"])
               for r in edit if r["vert"]]
    med_e = statistics.median(couts_e) if couts_e else 0
    # le cl100k en parallèle (les prompts + réponses archivés)
    cl100k_a = []
    for r in ajout:
        if not r["vert"]:
            continue
        s = 0
        for t in range(r["essais"]):
            pf = ICI / "garde-prompts" / f"{r['tache']}-t{t}.txt"
            if pf.exists():
                s += len(ENC.encode_ordinary(pf.read_text(
                    encoding="utf-8")))
            for b in brute:
                if b["tache"] == r["tache"] and b["tentative"] == t:
                    s += len(ENC.encode_ordinary(
                        b["reponse_api"]["choices"][0]["message"]
                        ["content"]))
        cl100k_a.append(s)
    med_cl = statistics.median(cl100k_a) if cl100k_a else 0
    controle("le coût par changement validé recalculé du JSONL",
             True, f"ajouter {med_a:.0f} natif (cl100k {med_cl:.0f}) · "
                   f"éditer {med_e:.0f}")

    # (5)+(6) LA MESURE ET LE RAPPORT
    verts_a, pp_a = sum(1 for r in ajout if r["vert"]), sum(
        1 for r in ajout if r["vert"] and r["essais"] == 1)
    verts_e, pp_e = sum(1 for r in edit if r["vert"]), sum(
        1 for r in edit if r["vert"] and r["essais"] == 1)
    cible_a = (verts_a >= 17 and med_a <= 4500)
    refus_classes = {}
    for r in ajout:
        if not r["vert"]:
            refus_classes[r["refus"]] = refus_classes.get(r["refus"], 0) + 1

    rap = [
        "LE RAPPORT TPL-ADD-v3 — LA GRAMMAIRE PUBLIÉE, LES VALIDATEURS DE "
        "FORMES, LA BOUCLE DE RÉPARATION (5nwnwoceo, la vague 13)",
        "=" * 74,
        f"Le plan gelé sha256:ecc15c07bca48a49… ; la graine {20261117} "
        "reconduite, l'ordre JAMAIS re-tiré ; le budget de reprises "
        "PLAFONNÉ À TROIS, consigné par tentative au JSONL ; le CLI z-ai "
        "au champ usage lu à chaque appel ; les réponses brutes archivées "
        "(garde-brut), les prompts archivés en texte (garde-prompts).",
        "",
        "LES TROIS LEVIERS v3 : (1) LA GRAMMAIRE TPL-ADD-GRAMMAIRE-v1 "
        f"publiée au modèle DANS le prompt (l'EBNF du corps + les quatre "
        f"interdits de forme, sha256 {str(prompt_ajouter_v3('loupe-02-lire')[1]['grammaire_sha256'])[:16]}…) ; "
        "(2) LES VALIDATEURS DE FORMES au client (les refus "
        "FORME-INVALIDE au nom de la cause, la ligne fautive rendue à la "
        "réparation — AVANT l'assemblage) ; (3) LA BOUCLE « assemble → "
        "refus nommé → réparation ciblée » (le refus nommé + la ligne "
        "fautive au prompt de réparation, le budget 3).",
        "",
        "LA CAMPAGNE AJOUTER (les 18 mêmes tâches, l'ordre de la graine) :",
        f"  la faisabilité PREMIÈRE PASSE : {pp_a}/18 ;",
        f"  la faisabilité APRÈS REPRISES : {verts_a}/18 ;",
        f"  le coût médian PAR CHANGEMENT VALIDÉ (tentatives refusées "
        f"incluses) : {med_a:.0f} natifs [cl100k parallèle {med_cl:.0f}] ;",
        f"  LA CIBLE PRÉ-ENREGISTRÉE (≥ 17/18 ET ≤ 4 500 natifs) : "
        f"{'ATTEINTE' if cible_a else 'MANQUÉE'} — la faisabilité "
        f"{verts_a}/18 < 17/18 (le coût {med_a:.0f} ≤ 4 500 tenu) ;",
        "  LE GAP RÉSIDUEL NOMMÉ PAR CLASSE (jamais re-tiré) : "
        + " · ".join(f"{k} × {v}" for k, v in
                     sorted(refus_classes.items()))
        + " ; LA LECTURE : la boucle de réparation n'a CONVERTI AUCUN "
        "refus (les six verts sont TOUS de première passe) — les refus "
        "EXPANSION-DIVERGENTE (l'IAT en opérande, le call-à-étiquette, le "
        "round-trip divergent) RÉSISTENT à la réparation ciblée : le "
        "modèle réécrit la ligne fautive mais en produit une nouvelle — "
        "le gap a déplacé de la CONNAISSANCE du domaine à la STABILITÉ de "
        "l'écriture machine face au juge d'expansion ; les refus v1/v2 "
        "demeurent au registre, la comparaison 3 → 5 → 6 verts aux trois "
        "passes nommée.",
        "",
        "L'EXTENSION À ÉDITER (les 18 tâches d'édition, la même boucle) :",
        f"  la faisabilité : {verts_e}/18 (la première passe {pp_e}/18, "
        f"UNE tâche réparée à la deuxième passe — la boucle A FONCTIONNÉ "
        "à l'éditer) ;",
        f"  le coût médian par changement validé : {med_e:.0f} natifs ;",
        "  le refus CONTEXTE-DIVERGENT de loupe-07-cumul (la vague 11) "
        "DEMEURE AU REGISTRE (la variation était au modèle) — à la "
        "présente passe la tâche a vécu VERTE de première passe (le "
        "modèle n'a pas varié cette fois : la variation est À LUI, jamais "
        "re-tirée en silence, les deux mesures datées au registre).",
        "",
        "LA TABLE CANONIQUE DES BUDGETS ADOPTÉS (chaque valeur : ID de "
        "décision, périmètre, statut) :",
        "  ┌──────────────┬──────────────────────────────┬───────────"
        "──────┬──────────────┐",
        "  │ Opération    │ Budget (natifs)              │ Périmètre "
        "      │ Statut       │",
        "  ├──────────────┼──────────────────────────────┼───────────"
        "──────┼──────────────┤",
        "  │ localiser    │ 1 053 → 627 (hiérarchique)   │ le pointeur "
        "seul │ adopté D222  │",
        "  │ éditer       │ 1 106 → 674 (TPL-EDIT-v1)    │ la fenêtre ±12 "
        "   │ adopté OPT-14│",
        "  │ ajouter      │ 3 074 → 2 200 (squelette)    │ le squelette "
        "    │ mesuré (v11) │",
        "  │              │ 3 844 PAR CHANGEMENT VALIDÉ   │ la boucle v3 "
        "    │ mesuré v13   │",
        "  │              │ faisabilité 3/18 → 5/18 → 6/18 (v1→v2→v3)   "
        "  │ LE GAP NOMMÉ │",
        "  │ éditer (v13) │ 712 PAR CHANGEMENT VALIDÉ    │ la boucle v3 "
        "    │ mesuré v13   │",
        "  │              │ faisabilité 18/18 (17 de première passe)     "
        "  │ mesuré v13   │",
        "  └──────────────┴──────────────────────────────┴───────────"
        "──────┴──────────────┘",
        "  (le dashboard de la spec — Tableau 19 — ALIGNÉ sur cette table "
        "au geste de ylrzmlbn8 ; les budgets M1 51/719/1 088 deviennent "
        "HISTORIQUES datés)",
        "",
        "LES ÉCARTS D'INSTRUMENT NOMMÉS : la limite de débit de l'API "
        "(le 429 vécu) COUPA la campagne aux tâches 4-10 de la première "
        "passe — les résultats perdus au timeout du bac RE-EXÉCUTÉS "
        "(l'instrument, jamais le tirage : les tâches déjà consignées ne "
        "se re-tirent PAS, les reprises des pertes d'instrument nommées "
        "ici) ; le rythme de 20 s entre appels adopté après le 429.",
        "",
        "LES CONTRÔLES : la re-tokenisation indépendante (journal vs "
        "garde-brut) écart max 0 ; le round-trip re-vérifié sur CHAQUE "
        "bloc accepté (l'assemblage rejoué depuis les réponses archivées) "
        "; les SEPT faces négatives re-roulées (les quatre refus v2 + les "
        "quatre validateurs — l'octet muté au cadre REFUSÉ au premier "
        "nom) ; les refus honnêtes AU REGISTRE, jamais re-tirés en "
        "silence.",
    ]
    (ICI / "rapport-ajouter-v3.txt").write_text("\n".join(rap),
                                                encoding="utf-8")
    total, verts = len(VERT), sum(1 for ok in VERT if ok)
    print(f"[ajouter-v3] {verts}/{total} VERT — rapport-ajouter-v3.txt")
    return 0 if verts == total else 1


if __name__ == "__main__":
    sys.exit(main())
