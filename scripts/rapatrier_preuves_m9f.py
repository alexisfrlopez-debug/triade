#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_preuves_m9f.py — rapatrie les pièces du run terrain M9-(f) depuis
/test/preuves-m9f (le coffre du développeur) vers download/preuves-run-m9f/,
md5 contrôlé par pièce contre les métadonnées Drive (modèle
rapatrier_preuves_m7d, D99 : zéro mélange — dossier dédié au run m9f ;
lecture seule, aucune écriture Drive).

Le trio TOUJOURS écrit par le scénario (même ROUGE — _verdict() l'écrit
sur chaque chemin de sortie après T0) :
  temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt

Les DEUX pièces conditionnelles (nées seulement si le run va assez loin) :
  ligne-recue.txt (T4, la ligne applicative), journal-emissions.txt (T6)
— leur absence N'EST PAS une erreur de rapatriement : elle est CONSTATÉE
et nommée (le journal dit où le run s'est arrêté ; un échec honnête vaut
plus qu'un vert muet — l'ordre lexicographique de la maison).

Usage : python3 scripts/rapatrier_preuves_m9f.py
Code de sortie : 0 = pièces présentes toutes conformes ; 1 = écart ;
2 = erreur fatale (réceptacle ou trio absent).
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m9f")

TRIO = {"temoin-m9f.txt", "scenario-m9f-journal.log",
        "VERDICT-run-m9f.txt"}
CONDITIONNELLES = {"ligne-recue.txt", "journal-emissions.txt"}
ATTENDUES = TRIO | CONDITIONNELLES


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m9f")
        if not preuves or preuves.get("mimeType") != ds.FOLDER_MIME:
            print("[preuves-m9f] ERREUR FATALE : /test/preuves-m9f absent",
                  file=sys.stderr)
            return 2
        entries = ds.list_folder(preuves["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-m9f] ERREUR FATALE : listage impossible : {exc}",
              file=sys.stderr)
        return 2

    deposees = {n for n, f in entries.items()
               if f.get("mimeType") != ds.FOLDER_MIME}
    pieces = {n: f for n, f in entries.items()
              if f.get("mimeType") != ds.FOLDER_MIME and n in ATTENDUES}
    manquantes_trio = TRIO - set(pieces)
    if manquantes_trio:
        print(f"[preuves-m9f] ERREUR FATALE : le trio du run absent du "
              f"coffre : {sorted(manquantes_trio)}", file=sys.stderr)
        return 2

    total, ok = 0, 0
    for nom, f in sorted(pieces.items()):
        total += 1
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[preuves-m9f] ÉCHEC téléchargement {nom} (HTTP {st})")
            continue
        chemin = DEST / nom
        chemin.write_bytes(body)
        local = ds.md5_of(chemin)
        attendu = (f.get("md5Checksum") or "").lower()
        if attendu and local != attendu:
            print(f"[preuves-m9f] ÉCART md5 {nom} : local {local} != "
                  f"drive {attendu}")
            continue
        ok += 1
        print(f"[preuves-m9f] {nom} : {len(body)} o, md5 {local[:8]}… "
              f"== drive — CONSTATÉ")

    absentes = ATTENDUES - set(pieces)
    if absentes:
        print(f"[preuves-m9f] NOTE : pièces NON DÉPOSÉES (le run ne les a "
              f"pas portées jusque-là) : {sorted(absentes)} — le journal "
              f"dira où il s'est arrêté")
    extras = deposees - ATTENDUES
    if extras:
        print(f"[preuves-m9f] note : entrées non-pièces ignorées : "
              f"{sorted(extras)}")
    if ok != total:
        print(f"[preuves-m9f] ÉCHEC : {ok}/{total} pièces conformes")
        return 1
    print(f"[preuves-m9f] {ok}/{total} pièces CONSTATÉES md5 — le recoup "
          f"sur pièces peut commencer (D138/D145/D148)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
