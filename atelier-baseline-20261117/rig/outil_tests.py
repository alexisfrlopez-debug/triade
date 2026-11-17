#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outil_tests.py — L'OUTIL DE TESTS (le troisième des trois outils
auteurs câblés par la rig L6) : les phases de VÉRIFICATION de la
construction — l'oracle dérivé du contrat (ORACLE, écrit-avant-code),
la suite de tests du flux standard (TESTS-C au bras C), la revue de
la pièce livrée (REVUE).

LA LOI R5 (vérifie-puis-écris) : l'oracle se dérive DU CONTRAT avant
que le code n'existe — l'outil porte la dérivée, le juge demeure le
modèle indépendant (jamais la pièce jugeant la pièce).

LA LOI (le chantier L6) : chaque appel au modèle passe PAR LA RIG —
rig_auteur.appeler_modele -> compter_tokens -> le journal naît de
l'outil. L'outil de tests n'a AUCUN autre chemin vers le modèle.

Usage :
  python3 outil_tests.py --bras T --tache loupe-05 --phase oracle \
      --contrat mini-contrat.md --sortie oracle.md --journal journal.jsonl
  python3 outil_tests.py --bras C --tache loupe-05 --phase tests-c \
      --contrat mini-contrat.md --sortie tests-c.md --journal journal.jsonl
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from rig_auteur import appeler_modele, cablage

CONSIGNES = {
    "oracle":
        "Tu es le juge d'un bloc de code machine selon le protocole "
        "TRIADE. Du CONTRAT seul (écrit-avant-code — la pièce n'existe "
        "pas encore), dérive L'ORACLE : les vecteurs attendus nommés "
        "(les cas nominaux, les bords, les rejets), l'attendu de chacun "
        "EN TERMES DE CONTRAT (jamais d'octets — la sémantique du "
        "contrat). Rien d'autre : la dérivée qui jugera la pièce.\n\n"
        "=== LE CONTRAT (couche I) ===\n",
    "tests-c":
        "Tu es l'auteur au FLUX STANDARD C (gcc -O2). Du CONTRAT, écris "
        "LA SUITE DE TESTS du bloc : les cas nominaux, les bords, les "
        "rejets — chaque test avec son attendu (le juge indépendant, "
        "jamais la pièce jugeant la pièce). La suite seule, rien "
        "d'autre.\n\n"
        "=== LE CONTRAT (couche I) ===\n",
    "revue":
        "Tu es le relecteur d'un bloc de code machine selon le protocole "
        "TRIADE (la revue de cérémonie). Du CONTRAT et de la NOTATION "
        "LIVRÉE, rends LA REVUE : la conformité au contrat (chaque "
        "exigence honorée, citée), les écarts nommés s'il y en a, le "
        "verdict CONFORME ou ÉCART. Rien d'autre.\n\n"
        "=== LE CONTRAT ===\n",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="l'outil de tests câblé "
                                             "(rig L6)")
    ap.add_argument("--cablage", action="store_true",
                    help="la preuve du câblage : un appel MOQUÉ, aucun "
                         "réseau, un journal éphémère — puis quitter")
    ap.add_argument("--bras", choices=("T", "C"))
    ap.add_argument("--tache", default="")
    ap.add_argument("--phase", choices=("oracle", "tests-c", "revue"))
    ap.add_argument("--contrat", help="le fichier du contrat (couche I)")
    ap.add_argument("--piece",
                    help="la notation livrée (la phase revue seule)")
    ap.add_argument("--sortie", help="le fichier où écrire la réponse")
    ap.add_argument("--journal", type=pathlib.Path)
    ap.add_argument("--garde-brut", type=pathlib.Path)
    args = ap.parse_args()

    if args.cablage:
        phase = args.phase or "tests-c"
        bras = args.bras or "C"
        ok, ligne = cablage("outil_tests.py", phase, bras,
                            args.tache or "cablage-l6")
        print(f"[cablage] outil_tests phase {phase} bras {bras} : "
              f"{'VERT' if ok else 'ROUGE'}")
        return 0 if ok else 1

    manquants = [n for n, v in (("bras", args.bras), ("phase", args.phase),
                                ("contrat", args.contrat),
                                ("sortie", args.sortie))
                 if not v]
    if manquants:
        ap.error(f"arguments manquants : {manquants}")
    if args.phase == "revue" and not args.piece:
        ap.error("la phase revue exige --piece (la notation livrée)")

    contrat = pathlib.Path(args.contrat).read_text(encoding="utf-8")
    prompt = CONSIGNES[args.phase] + contrat
    if args.piece:
        prompt += ("\n\n=== LA NOTATION LIVRÉE ===\n"
                   + pathlib.Path(args.piece).read_text(encoding="utf-8"))

    texte, ligne = appeler_modele(
        bras=args.bras, phase=args.phase, tache=args.tache,
        prompt=prompt, journal=args.journal, garde_brut=args.garde_brut)

    pathlib.Path(args.sortie).write_text(texte, encoding="utf-8")
    print(f"[tests] la réponse écrite : {args.sortie} ({len(texte)} car.)")
    print(f"[tests] la ligne née : {ligne['prompt_tokens']}+"
          f"{ligne['completion_tokens']}={ligne['total_tokens']} tokens "
          f"(lus du log) — bras {args.bras}, phase {args.phase}, "
          f"tâche {args.tache}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
