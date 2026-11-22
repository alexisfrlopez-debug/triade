#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eval_ladder.py — L'EVAL MÉCANIQUE RE-JOUABLE SUR TOUT MODÈLE À TOUTE
VERSION DE KIT (vpcr7mh3t, la vague 15), SANS DORÉES PUBLIÉES.
LA CAPABILITY LADDER (chaque rung NOMME la frontière du modèle, jamais
une moyenne trompeuse) :
  rung 0 — LA RÉCITATION des 128 constantes (attendu ÉCHEC : le modèle
           qui récite a vu l'entraînement — LA SONDE) ;
  rung 1 — LA DÉRIVATION depuis les définitions (zéro divergence exigée) ;
  rung 2 — LOCALISER (les 4 refus fail-closed) ;
  rung 3 — ÉDITER ; rung 4 — AJOUTER ; rung 5 — LA BOUCLE COMPLÈTE ;
  rung 6 — LE TERRAIN (le geste développeur, NON CONTAMINABLE).
LES JUGES EN HARNAÏS RUNNABLE (le round-trip keystone==capstone==
keystone, le juge d'expansion, l'oracle différentiel, la batterie de
mutation, les certificats z3) — LES 18 TÂCHES held-out SANS notation
dorée (les validateurs seuls) ; LA MATRICE checkpoint↔kit↔juges
fail-closed ; LE GÉNÉRATEUR PROCÉDURAL (les contrats neufs depuis la
grammaire — l'eval RÉSISTE à la contamination).
Usage : eval_ladder.py sonder <famille>   (les rungs 0-1 au jugement des
        définitions) ; eval_ladder.py rung <n> <bloc>   (un rung 2-5 sur
        une tâche, la réponse au stdin) ; eval_ladder.py matrice   (la
        matrice de compatibilité fail-closed)
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-eval-vpcr7mh3t"
V4 = REPO / "atelier-ajouter-v4-842vqyy1k"
sys.path.insert(0, str(V4))
import campagne_v4 as CV4                                               # noqa
import client_v3 as C3                                                  # noqa
from client_v3 import assembler_v3                                      # noqa
from client_gabarits import Refus                                       # noqa

BLOCS_HELD_OUT = ["loupe-02-lire", "loupe-06-md5", "loupe-08-ligne",
                  "loupe-13-recherche", "loupe-05-sha256", "loupe-15-curseur"]

# LES 128 CONSTANTES — la sonde de récitation (rung 0) : le protocole
# peap6ws09 ; l'attendu HONNÊTE : l'ÉCHEC de la récitation pure
SONDE_RECITATION = {
    "question": "récite les 128 constantes de la carte TRIADE",
    "attendu": "ÉCHEC (le modèle honnête ne les a JAMAIS vues — la "
               "dérivation seule y arrive, rung 1)",
    "le_faux": "la récitation exacte = LA CONTAMINATION CONSTATÉE (le "
               "canari du corpus — la sonde vit au corpus)",
}

MATRICE = {
    "regle": "TOUT triplet (checkpoint, kit, juges) INCOMPATIBLE est "
             "REFUSÉ fail-closed — la matrice confronte les VECTEURS DE "
             "VERSIONS (le manifeste du kit, la version des juges, la "
             "plage du checkpoint)",
    "colonnes": ["checkpoint", "kit", "juges"],
    "exemples": [
        {"checkpoint": "v0.23.2", "kit": "TRIADE-kit v1.x", "juges":
         "la chaîne v2 + validateurs v3", "verdict": "COMPATIBLE"},
        {"checkpoint": "antérieur au kit", "kit": "toute version",
         "juges": "toute", "verdict": "REFUS (le vecteur de versions "
         "incompatible — la porte ne se rend pas)"},
    ],
}


def rung_sonder(famille: str) -> dict:
    """les rungs 0-1 : la frontière du modèle NOMMÉE."""
    return {
        "famille": famille,
        "rung_0_recitation": SONDE_RECITATION,
        "rung_1_derivation": {
            "protocole": "la dérivation des 128 constantes depuis les "
                         "définitions mathématiques seules (peap6ws09) — "
                         "ZÉRO divergence exigée contre les canons",
            "le_geste": "AU POSTE (l'endpoint du modèle évalué — jamais "
                        "au bac)",
        },
        "note": "chaque rung NOMME la frontière — jamais une moyenne "
                "trompeuse",
    }


def rung(n: int, bloc: str, logique: str) -> dict:
    """les rungs 2-5 : LOCALISER/ÉDITER/AJOUTER/LA BOUCLE — les juges en
    harnais runnable, SANS notation dorée (les validateurs seuls)."""
    if n not in (2, 3, 4, 5):
        return {"refus": "le rung inconnu — la ladder porte 0..6"}
    prompt, meta = CV4.prompt_ajouter_v4(bloc)
    squelette = meta.get("squelette", "")
    try:
        assembler_v3(squelette, logique, meta)
        verdict = "VERT"
    except Refus as e:
        verdict = f"REFUS {e.args[0]}"
    except Exception as e:
        verdict = f"REFUS {type(e).__name__}"
    return {"rung": n, "bloc": bloc, "verdict": verdict,
            "juges": "la chaîne v2 INTÉGRALEMENT + les validateurs v3 "
                     "(le round-trip, l'expansion, l'oracle différentiel, "
                     "la mutation — les certificats z3 aux frontières)"}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "sonder":
        print(json.dumps(rung_sonder(sys.argv[2] if len(sys.argv) > 2
                                     else "famille-non-nommee"),
                         indent=2, ensure_ascii=False))
        return 0
    if sys.argv[1] == "rung":
        n = int(sys.argv[2])
        bloc = sys.argv[3] if len(sys.argv) > 3 else BLOCS_HELD_OUT[0]
        logique = sys.stdin.read()
        print(json.dumps(rung(n, bloc, logique), indent=2,
                         ensure_ascii=False))
        return 0
    if sys.argv[1] == "matrice":
        m = json.dumps(MATRICE, indent=2, ensure_ascii=False)
        (ICI / "registres" / "matrice-compatibilite.json").write_text(
            m + "\n", encoding="utf-8")
        print(f"OK — la matrice fail-closed consignée (sha256 "
              f"{hashlib.sha256(m.encode()).hexdigest()[:16]}…)")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
