#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""outil_builder.py — LE BUILDER (le premier des trois outils auteurs
câblés par la rig L6) : les phases de MISE EN ŒUVRE de la construction
d'un bloc — la lecture du contrat (SPEC) puis la rédaction à la main
(NOTATION au bras T, SOURCE-C au bras C).

LA LOI (le chantier L6) : chaque appel au modèle passe PAR LA RIG —
rig_auteur.appeler_modele -> compter_tokens -> le journal naît de
l'outil. Le builder n'a AUCUN autre chemin vers le modèle (l'épreuve
L6 l'inspecte : « z-ai » et « subprocess » n'y vivent pas).

LES PHASES (le vocabulaire du plan a78caf8c…) :
  --phase spec      le contrat lu (les notes d'auteur : les exigences,
                    les pièges nommés, les invariants) — la phase qui
                    ouvrit chaque unité de la campagne ;
  --phase notation  le brouillon écrit à la main (bras T) — la notation
                    au slot, le round-trip viendra ensuite (les outils
                    mécaniques du labo, hors modèle) ;
  --phase source-c  le source C écrit au flux standard (bras C).

Usage :
  python3 outil_builder.py --bras T --tache loupe-05 --phase spec \
      --contrat mini-contrat.md --sortie notes.md --journal journal.jsonl
  python3 outil_builder.py --bras T --tache loupe-05 --phase notation \
      --contrat mini-contrat.md --notes notes.md --sortie brouillon.asm \
      --journal journal.jsonl

L'option --garde-brut conserve la réponse brute de l'API à côté du
journal (la pièce de l'épreuve : la ligne == le log, à l'unité près).
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from rig_auteur import appeler_modele, cablage

CONSIGNES = {
    "spec":
        "Tu es l'auteur d'un bloc de code machine selon le protocole "
        "TRIADE (la notation à la main, jamais un compilateur entre "
        "l'intention et les octets). Lis CE CONTRAT et rends les NOTES "
        "D'AUTEUR : les exigences et la signature, les pièges nommés, "
        "les invariants à tenir, les cas d'échec. Rien d'autre — pas de "
        "code, pas de bavardage : les notes qui prépareront la notation.\n\n"
        "=== LE CONTRAT (couche I) ===\n",
    "notation":
        "Tu es l'auteur d'un bloc de code machine selon le protocole "
        "TRIADE. Des NOTES D'AUTEUR et du CONTRAT, écris LE BROUILLON DE "
        "NOTATION x86-64 (assembleur, ABI msx64, adresses explicites — "
        "les étiquettes locales sont permises, l'outil d'arithmétique "
        "d'adresses les résoudra). Écris-avant-code : dérive du contrat, "
        "jamais d'un exemple. Le brouillon seul, rien d'autre.\n\n"
        "=== LE CONTRAT ===\n",
    "source-c":
        "Tu es l'auteur au FLUX STANDARD C (gcc -O2) du MÊME contrat. "
        "Des NOTES D'AUTEUR, écris LE SOURCE C complet de la fonction "
        "(une fonction pure, testable, lisible). Le source seul, rien "
        "d'autre.\n\n"
        "=== LE CONTRAT ===\n",
}


def composer(phase: str, contrat: str, notes: str | None) -> str:
    if phase not in CONSIGNES:
        raise SystemExit(f"phase inconnue du builder : {phase!r}")
    prompt = CONSIGNES[phase] + contrat
    if notes is not None:
        prompt += "\n\n=== LES NOTES D'AUTEUR (la phase spec) ===\n" + notes
    return prompt


def main() -> int:
    ap = argparse.ArgumentParser(description="le builder câblé (rig L6)")
    ap.add_argument("--cablage", action="store_true",
                    help="la preuve du câblage : un appel MOQUÉ, aucun "
                         "réseau, un journal éphémère — puis quitter")
    ap.add_argument("--bras", choices=("T", "C"))
    ap.add_argument("--tache", default="")
    ap.add_argument("--phase", choices=("spec", "notation", "source-c"))
    ap.add_argument("--contrat", help="le fichier du contrat (couche I)")
    ap.add_argument("--notes", help="les notes de la phase spec "
                                    "(phase notation / source-c)")
    ap.add_argument("--sortie", help="le fichier où écrire la réponse")
    ap.add_argument("--journal", type=pathlib.Path)
    ap.add_argument("--garde-brut", type=pathlib.Path)
    args = ap.parse_args()

    if args.cablage:
        phase = args.phase or "spec"
        bras = args.bras or "T"
        ok, ligne = cablage("outil_builder.py", phase, bras,
                            args.tache or "cablage-l6")
        print(f"[cablage] outil_builder phase {phase} bras {bras} : "
              f"{'VERT' if ok else 'ROUGE'}")
        return 0 if ok else 1

    manquants = [n for n, v in (("bras", args.bras), ("phase", args.phase),
                                ("contrat", args.contrat),
                                ("sortie", args.sortie))
                 if not v]
    if manquants:
        ap.error(f"arguments manquants : {manquants}")
    if args.phase in ("notation", "source-c") and not args.notes:
        ap.error(f"la phase {args.phase} exige --notes (la phase spec "
                 f"d'abord — écrit-avant-code)")

    contrat = pathlib.Path(args.contrat).read_text(encoding="utf-8")
    notes = (pathlib.Path(args.notes).read_text(encoding="utf-8")
             if args.notes else None)
    prompt = composer(args.phase, contrat, notes)

    texte, ligne = appeler_modele(
        bras=args.bras, phase=args.phase, tache=args.tache,
        prompt=prompt, journal=args.journal, garde_brut=args.garde_brut)

    pathlib.Path(args.sortie).write_text(texte, encoding="utf-8")
    print(f"[builder] la réponse écrite : {args.sortie} "
          f"({len(texte)} car.)")
    print(f"[builder] la ligne née : {ligne['prompt_tokens']}+"
          f"{ligne['completion_tokens']}={ligne['total_tokens']} tokens "
          f"(lus du log) — bras {args.bras}, phase {args.phase}, "
          f"tâche {args.tache}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
