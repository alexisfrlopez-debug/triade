#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chronometre_verification.py — LE CHRONOMÈTRE DU TEMPS DE CALCUL DE
VÉRIFICATION (métrique M4 du plan pré-enregistré de la comparaison des
workflows, paquet 5 de la vague 3 ; D204).

LA COMMANDE : « temps de calcul de vérification ». L'instrument mesure
le TEMPS MURAL (horloge monotone) des COMMANDES DE VÉRIFICATION dont la
liste est FIXÉE PAR LE PLAN, par bras :

  bras T (TRIADE), par livraison d'un bloc :
    1. le garde des arbres signés (python3 v06/sceau_I.py verifier) ;
    2. le round-trip de la notation livrée (keystone == capstone, R5) ;
    3. l'oracle du bloc (le harnais du domaine au périmètre livré) ;
    4. le build (la recomposition de la pièce depuis le plan).
  bras C (standard), par livraison d'un bloc :
    1. la compilation (gcc -O2, la commande consignée) ;
    2. la suite de tests du camp C (la même entrée, le même verdict) ;
    3. les contrôles binaires (empreintes, format).

Le présent outil exécUTE UNE COMMANDE À LA FOIS et journalise
(label, bras, tâche, commande, code de retour, secondes) en JSONL — le
journal de campagne vit avec celui des tokens (CA1 : créé par la
première mesure). TOUTE commande hors liste est un ÉCART NOMMÉ.

LE DRY-RUN (la preuve de l'instrument, AVANT toute mesure) :
  --calibration   une pause de durée connue — l'écart mesuré/connu doit
                  être sous la tolérance (l'horloge prouvée) ; la pause vit
                  EN PROCESSUS (time.sleep, l'édition v2 du 14/11/2026) :
                  le « sleep » externe faute sous Windows (cmd.exe n'a pas
                  de commande sleep — l'écart nommé des runs 1 clic du
                  13/11 : code 1, 0,031 puis 0,028 s) ;
  --command ...   une commande réelle de vérification, chronométrée et
                  journalisée (avec --dryrun, au journal du dry-run).

Usage :
  python3 chronometre_verification.py --calibration 1.5 \
      --journal preuves_v150/comparaison_dryrun/dryrun_verifications.jsonl
  python3 chronometre_verification.py --command "python3 v06/sceau_I.py \
verifier" --label garde --bras T --tache six-blocs --dryrun
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time

JOURNAL_DEFAUT = (pathlib.Path(__file__).resolve().parents[1]
                  / "preuves_v150" / "comparaison_resultats"
                  / "journal_verifications.jsonl")
JOURNAL_DRYRUN = (pathlib.Path(__file__).resolve().parents[1]
                  / "preuves_v150" / "comparaison_dryrun"
                  / "dryrun_verifications.jsonl")
TOLERANCE_CALIBRATION = 0.05  # s — la preuve de l'horloge au dry-run


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mesurer(commande: str, label: str, bras: str, tache: str,
            journal: pathlib.Path, dryrun: bool) -> dict:
    """Exécute LA commande, mesure le temps mural, journalise."""
    debut = time.monotonic()
    proc = subprocess.run(commande, shell=True, capture_output=True,
                          text=True, timeout=3600)
    secondes = time.monotonic() - debut
    ligne = {
        "horodatage": horodatage(),
        "dryrun": dryrun,
        "bras": bras, "tache": tache, "label": label,
        "commande": commande,
        "code_retour": proc.returncode,
        "secondes": round(secondes, 3),
    }
    journal.parent.mkdir(parents=True, exist_ok=True)
    with open(journal, "a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--calibration", type=float,
                    help="une pause de durée connue (la preuve d'horloge)")
    ap.add_argument("--command",
                    help="UNE commande de vérification, chronométrée")
    ap.add_argument("--label", default="verification")
    ap.add_argument("--bras", choices=("T", "C", "X"), default="X")
    ap.add_argument("--tache", default="")
    ap.add_argument("--journal", type=pathlib.Path, default=None)
    ap.add_argument("--dryrun", action="store_true",
                    help="au journal du DRY-RUN (la preuve d'instrument, "
                         "PAS une mesure de campagne)")
    args = ap.parse_args()

    journal = args.journal or (JOURNAL_DRYRUN if (args.dryrun
                                                  or args.calibration
                                                  is not None)
                               else JOURNAL_DEFAUT)
    # la calibration est TOUJOURS une preuve d'instrument (dry-run) :
    # elle ne peut JAMAIS écrire au journal de campagne — le dossier des
    # résultats ne naît que d'une mesure réelle (CA1)
    if args.calibration is not None:
        # v2 (l'édition du 14/11/2026) — LA PAUSE PORTABLE : time.sleep EN
        # PROCESSUS, mesuré par time.monotonic — la MÊME horloge monotone
        # que les mesures M4. Le « sleep » externe faute sous Windows
        # (cmd.exe n'a pas de commande sleep — l'écart nommé des runs
        # 1 clic du 13/11 : code 1, 0,031 puis 0,028 s) ; le kit exige
        # déjà Python 3, la pause y vit partout pareil. Le label
        # « calibration-sleep » demeure (la clé du vérificateur) ; le
        # champ commande nomme la vérité. Une pause interrompue LÈVE —
        # rien n'est journalisé (fail-closed par l'exception même).
        debut = time.monotonic()
        time.sleep(args.calibration)
        secondes = time.monotonic() - debut
        ligne = {
            "horodatage": horodatage(),
            "dryrun": True,
            "bras": "X", "tache": "dryrun",
            "label": "calibration-sleep",
            "commande": f"time.sleep({args.calibration}) en processus [pause portable v2]",
            "code_retour": 0,
            "secondes": round(secondes, 3),
        }
        journal.parent.mkdir(parents=True, exist_ok=True)
        with open(journal, "a", encoding="utf-8") as f:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        ecart = abs(secondes - args.calibration)
        ok = ecart <= TOLERANCE_CALIBRATION
        print(f"[calibration] pause demandée {args.calibration:.2f} s, "
              f"mesurée {secondes:.3f} s — écart "
              f"{ecart:.3f} s {'≤' if ok else '>'} tolérance "
              f"{TOLERANCE_CALIBRATION:.2f} s -> "
              f"{'VERT' if ok else 'ROUGE'}")
        return 0 if ok else 1
    if args.command:
        if not args.dryrun and args.bras == "X":
            ap.error("une mesure de campagne exige --bras T ou C "
                     "(le dry-run excepté)")
        ligne = mesurer(args.command, args.label, args.bras, args.tache,
                        journal, args.dryrun)
        print(f"[chronometre] {ligne['label']} ({ligne['bras']}): "
              f"{ligne['secondes']:.3f} s, code {ligne['code_retour']} "
              f"{'(DRY-RUN, pas une mesure)' if args.dryrun else ''}")
        return 0 if ligne["code_retour"] == 0 else 2
    ap.error("--calibration DURÉE ou --command COMMANDE requis")
    return 3


if __name__ == "__main__":
    sys.exit(main())
