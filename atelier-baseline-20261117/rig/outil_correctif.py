#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outil_correctif.py — L'OUTIL DE CORRECTIF (le deuxième des trois
outils auteurs câblés par la rig L6) : la phase CORRECTIF de la
construction — le tour de correction d'un défaut NOMMÉ.

LA LOI DU BUNDLE-DÉFAUT (le chantier, levier L1 — le format anticipé
par la rig) : un tour de correction ne porte QUE TROIS choses —
  ① le défaut NOMMÉ (la classe, le mécanisme, la pièce à l'appui) ;
  ② le fragment touché (le bloc de la notation, ses bornes) ;
  ③ le vecteur d'oracle qui a échoué (l'attendu contre le vécu).
JAMAIS la rédaction entière — le portage circonsrit est l'économie
visée du chantier ; la rig l'installe comme LE format de correctif.

LA LOI (le chantier L6) : chaque appel au modèle passe PAR LA RIG —
rig_auteur.appeler_modele -> compter_tokens -> le journal naît de
l'outil. L'outil de correctif n'a AUCUN autre chemin vers le modèle.

Usage :
  python3 outil_correctif.py --bras T --tache loupe-05 \
      --defaut "la syntaxe RIP+offset : le lea visait l'étiquette avant
                sa définition — la pièce : brouillon.asm ligne 12" \
      --fragment fragment.asm \
      --vecteur "attendu 32 octets lus, vécu 0 (la fenêtre jamais lue)" \
      --sortie fragment-corrigee.asm --journal journal.jsonl
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from rig_auteur import appeler_modele, cablage

CONSIGNE = (
    "Tu es l'auteur d'un bloc de code machine selon le protocole "
    "TRIADE, en tour de CORRECTION d'un défaut nommé. Voici LE "
    "BUNDLE-DÉFAUT : le défaut nommé, le fragment touché, le vecteur "
    "d'oracle qui a échoué. Corrige LE FRAGMENT (le reste du bloc est "
    "intact — ne le réécris pas) : rends le fragment corrigé ENTIER, "
    "puis une ligne « le geste : … » qui nomme la correction. Rien "
    "d'autre — le bundle est le voisinage de vérification (R5).\n\n"
    "=== ① LE DÉFAUT NOMMÉ ===\n"
)


def main() -> int:
    ap = argparse.ArgumentParser(description="l'outil de correctif câblé "
                                             "(rig L6)")
    ap.add_argument("--cablage", action="store_true",
                    help="la preuve du câblage : un appel MOQUÉ, aucun "
                         "réseau, un journal éphémère — puis quitter")
    ap.add_argument("--bras", choices=("T", "C"))
    ap.add_argument("--tache", default="")
    ap.add_argument("--defaut", required=False,
                    help="le défaut nommé : la classe, le mécanisme, la "
                         "pièce à l'appui")
    ap.add_argument("--fragment",
                    help="le fichier du fragment touché (le bloc, ses "
                         "bornes)")
    ap.add_argument("--vecteur",
                    help="le vecteur d'oracle qui a échoué : l'attendu "
                         "contre le vécu")
    ap.add_argument("--sortie", help="le fichier du fragment corrigé")
    ap.add_argument("--journal", type=pathlib.Path)
    ap.add_argument("--garde-brut", type=pathlib.Path)
    args = ap.parse_args()

    if args.cablage:
        bras = args.bras or "T"
        ok, ligne = cablage("outil_correctif.py", "correctif", bras,
                            args.tache or "cablage-l6")
        print(f"[cablage] outil_correctif phase correctif bras {bras} : "
              f"{'VERT' if ok else 'ROUGE'}")
        return 0 if ok else 1

    manquants = [n for n, v in (("bras", args.bras), ("defaut", args.defaut),
                                ("fragment", args.fragment),
                                ("vecteur", args.vecteur),
                                ("sortie", args.sortie))
                 if not v]
    if manquants:
        ap.error(f"arguments manquants : {manquants}")

    fragment = pathlib.Path(args.fragment).read_text(encoding="utf-8")
    prompt = (CONSIGNE + args.defaut
              + "\n\n=== ② LE FRAGMENT TOUCHÉ ===\n" + fragment
              + "\n\n=== ③ LE VECTEUR QUI A ÉCHOUÉ ===\n" + args.vecteur
              + "\n")

    texte, ligne = appeler_modele(
        bras=args.bras, phase="correctif", tache=args.tache,
        prompt=prompt, journal=args.journal, garde_brut=args.garde_brut)

    pathlib.Path(args.sortie).write_text(texte, encoding="utf-8")
    print(f"[correctif] le fragment corrigé écrit : {args.sortie} "
          f"({len(texte)} car.)")
    print(f"[correctif] la ligne née : {ligne['prompt_tokens']}+"
          f"{ligne['completion_tokens']}={ligne['total_tokens']} tokens "
          f"(lus du log) — bras {args.bras}, phase correctif, "
          f"tâche {args.tache}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
