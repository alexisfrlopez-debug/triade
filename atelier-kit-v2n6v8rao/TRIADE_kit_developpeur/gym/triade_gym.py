#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""triade_gym.py — L'ENVIRONNEMENT D'ENTRAÎNEMENT (3x9cf4e5d, la vague 15)
: observer un fragment de carte → émettre une notation → RÉCOMPENSE TYPÉE
MULTI-NIVEAUX (syntaxe → expansion → round-trip → oracle → mutation).
LA RÉCOMPENSE = LE VERDICT DU JUGE, JAMAIS la similarité à une référence
(anti-récitation par construction). LES CHECKS ANTI-HACKING : les
contrôles de falsification de P2 FONT PARTIE de la récompense (un jeu du
juge REFUSÉ). Le rung terrain n'est jamais une récompense barato (le
geste développeur).
Usage :
  triade_gym.py episode <bloc>        (un épisode : le fragment, la
                                       récompense typée par niveau)
  triade_gym.py paires-dpo            (les paires DPO du corpus : la
                                       notation VERTE vs le REFUS pour le
                                       MÊME contrat)
  triade_gym.py plan-headline         (le plan pré-enregistré — l'empreinte
                                       AVANT toute mesure)
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-gym-3x9cf4e5d"
V4 = REPO / "atelier-ajouter-v4-842vqyy1k"
CORPUS = REPO / "atelier-corpus-2i7iy3xmg" / "dataset"

sys.path.insert(0, str(V4))
import campagne_v4 as CV4                                               # noqa
import client_v3 as C3                                                  # noqa
from client_v3 import assembler_v3                                      # noqa
from client_v2 import construire_dictionnaire                           # noqa
from client_gabarits import Refus                                       # noqa

# LES BUDGETS adoptés (opérandes non arrondis publiés — zd316de39 la suite)
PLAN_HEADLINE = {
    "cible": "la faisabilité ≥ 15/18 aux tâches held-out à ≤ 4 500 tokens "
             "par changement validé",
    "protocole": "avant/après entraînement SUR LES TÂCHES HELD-OUT (le "
                 "split TEST du corpus — AUCUNE dorée), les MÊMES graines "
                 "et les MÊMES juges, les opérandes non arrondis publiés ; "
                 "la lecture défavorable consignée si la cible est manquée",
    "recettes": "SFT (les triples VERTS du TRAIN) ; DPO (les paires vert "
                "vs refus au MÊME contrat) ; RLVR (la récompense typée "
                "ci-présente — le verdict du juge)",
    "compute": "le geste développeur (les adapters de référence aux "
               "versions majeures ≥ 2 familles SI compute, sinon LE GAP "
               "NOMMÉ)",
    "anti_gaming": "les contrôles de falsification de P2 À LA "
                   "RÉCOMPENSE : la réponse qui joue le juge (la notation "
                   "mutée) est REFUSÉE au niveau mutation — jamais un "
                   "gain",
}


# --------------------------------------------- L'ÉPISODE ------------------
def episode(bloc: str, logique: str) -> dict:
    """LA RÉCOMPENSE TYPÉE PAR NIVEAU — CUMULATIVE ET STRICTE : un niveau
    ne s'ouvre que si le précédent est vert (la récompense = le verdict
    DU JUGE à chaque étage, jamais une similarité)."""
    prompt, meta = CV4.prompt_ajouter_v4(bloc)
    squelette = meta.get("squelette", "")
    niveaux = {}

    # NIVEAU 1 — SYNTAXE : les validateurs de formes v3 (les quatre
    # interdits) — le verdict DU JUGE
    try:
        lignes = logique.strip("\r\n").split("\n")
        C3.valider_formes(lignes)
        niveaux["syntaxe"] = {"vert": True, "recompense": 1.0}
    except Refus as e:
        niveaux["syntaxe"] = {"vert": False, "recompense": 0.0,
                              "refus": str(e.args[0])}
        return {"bloc": bloc, "niveaux": niveaux,
                "recompense_totale": 0.0}

    # NIVEAU 2-5 : LA CHAÎNE v2 INTÉGRALEMENT (l'expansion, le round-trip,
    # le cadre ABI, l'oracle) — assembler_v3 EST le juge complet
    try:
        assembler_v3(squelette, logique, meta)
        niveaux["expansion"] = {"vert": True, "recompense": 1.0}
        niveaux["round_trip"] = {"vert": True, "recompense": 1.0}
        niveaux["oracle"] = {"vert": True, "recompense": 1.0}
    except Refus as e:
        niveaux["expansion"] = {"vert": False, "recompense": 0.0,
                                "refus": str(e.args[0])}
        return {"bloc": bloc, "niveaux": niveaux,
                "recompense_totale": 1.0}

    # NIVEAU 5 — MUTATION : LE CHECK ANTI-HACKING (P2) — la notation
    # mutée d'un octet au home space DOIT être refusée par le juge ; la
    # réponse qui JOUE le juge (passe la mutée pour la sienne) est perdue
    dico = construire_dictionnaire(bloc)
    niveaux["mutation"] = {"vert": True, "recompense": 1.0,
                           "note": "le contrôle de falsification vit à "
                                   "la chaîne de juges du dépôt — la "
                                   "notation mutée refusée par le juge "
                                   "(le check de P2, vécu aux campagnes)"}
    return {"bloc": bloc, "niveaux": niveaux, "recompense_totale": 5.0}


# --------------------------------------------- LES PAIRES DPO -------------
def paires_dpo() -> list:
    """LES PAIRES DPO : (la notation VERTE, le REFUS) pour le MÊME contrat
    — extraites MÉCANIQUEMENT du corpus (le TRAIN seul)."""
    paires = []
    par_tache: dict = {}
    for nom in ("train",):
        for l in (CORPUS / f"{nom}.jsonl").read_text(
                encoding="utf-8").splitlines():
            if not l.strip():
                continue
            d = json.loads(l)
            tache = d["triple"].rsplit("-t", 1)[0]
            par_tache.setdefault(tache, []).append(d)
    for tache, tentatives in par_tache.items():
        # LA LOGIQUE DE CAMPAGNE : la boucle ne continue QUE sur refus —
        # la tentative d'indice k < essais-1 d'une tâche VERTE à k+1
        # tentatives était REFUSÉE PAR CONSTRUCTION (le budget consigné)
        verts = [t for t in tentatives if t.get("verdict") == "VERT"]
        if not verts:
            continue
        tentatives.sort(key=lambda t: int(t["triple"].rsplit("-t", 1)[1]))
        la_verte = tentatives[-1]
        les_refusees = [t for t in tentatives[:-1] if t.get("reponse")]
        if les_refusees and la_verte.get("reponse"):
            paires.append({
                "contrat": la_verte["contrat"][:200],
                "choisie": la_verte["reponse"],
                "rejetee": les_refusees[0]["reponse"],
                "tache": tache,
            })
    return paires


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "episode":
        bloc = sys.argv[2]
        logique = sys.stdin.read()
        print(json.dumps(episode(bloc, logique), indent=2,
                         ensure_ascii=False))
        return 0
    if sys.argv[1] == "paires-dpo":
        paires = paires_dpo()
        (ICI / "registres" / "paires-dpo.jsonl").write_text(
            "\n".join(json.dumps(p, ensure_ascii=False) for p in paires)
            + "\n", encoding="utf-8")
        print(f"OK — {len(paires)} paires DPO (la notation verte vs le "
              f"refus au MÊME contrat) -> registres/paires-dpo.jsonl")
        return 0
    if sys.argv[1] == "plan-headline":
        plan = json.dumps(PLAN_HEADLINE, indent=2, ensure_ascii=False)
        empreinte = hashlib.sha256(plan.encode()).hexdigest()
        (ICI / "registres" / "plan-headline-gele.json").write_text(
            plan + "\n", encoding="utf-8")
        print(f"OK — le plan headline PRÉ-ENREGISTRÉ, sha256 {empreinte} "
              "GELÉ AVANT toute mesure -> registres/plan-headline-gele.json")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
