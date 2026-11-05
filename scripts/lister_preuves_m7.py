#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lister_preuves_m7.py — LISTE le coffre /test et son réceptacle preuves-m7/
(vague courante m7d), LECTURE SEULE : id, taille, md5, dates de chaque pièce
(modèle lister_preuves_e4_run / rapatrier_preuves_m6d — D99 : zéro mélange,
aucune écriture Drive).

Le trio attendu du run M7-(d) (LISEZMOI-preuves.txt du réceptacle) :
  temoin-m7d.txt, scenario-m7d-journal.log, VERDICT-run-m7d.txt
(LISEZMOI-preuves.txt n'est PAS une pièce).

Usage : python3 scripts/lister_preuves_m7.py
Code de sortie : 0 = trio complet constaté ; 1 = trio incomplet ; 2 = erreur.
"""

import sys

REPO = pathlib = __import__("pathlib")
REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
TRIO = {"temoin-m7d.txt", "scenario-m7d-journal.log", "VERDICT-run-m7d.txt"}


def affiche(titre, entries):
    print(f"--- {titre} ({len(entries)} entrées) ---")
    for nom, f in sorted(entries.items()):
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR ] {nom}  id={f.get('id', '-')}")
        else:
            print(f"  [{f.get('size', 0):>9} o] {nom}  "
                  f"md5={(f.get('md5Checksum') or '-')[:8]}…  "
                  f"mod={f.get('modifiedTime', '-')}  id={f.get('id', '-')}")


def main() -> int:
    try:
        racine = ds.list_folder(TEST_ID)
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-m7] ERREUR FATALE : /test inaccessible : {exc}",
              file=sys.stderr)
        return 2
    affiche("RACINE /test", racine)
    pm7 = racine.get("preuves-m7")
    if not pm7 or pm7.get("mimeType") != ds.FOLDER_MIME:
        print("[preuves-m7] ERREUR : le réceptacle /test/preuves-m7 est absent",
              file=sys.stderr)
        return 2
    try:
        entries = ds.list_folder(pm7["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-m7] ERREUR FATALE : listage impossible : {exc}",
              file=sys.stderr)
        return 2
    affiche("RÉCEPTACLE /test/preuves-m7", entries)
    presentes = {n for n, f in entries.items()
                 if f.get("mimeType") != ds.FOLDER_MIME}
    manquantes = TRIO - presentes
    if manquantes:
        print(f"[preuves-m7] TRIO INCOMPLET — manquant : {sorted(manquantes)}")
        return 1
    print("[preuves-m7] LE TRIO EST COMPLET — prêt au rapatriement "
          "(md5 contrôlés par pièce)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
