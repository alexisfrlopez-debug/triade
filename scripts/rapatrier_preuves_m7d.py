#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_preuves_m7d.py — rapatrie les pièces du run M7-(d) depuis
/test/preuves-m7 (vague courante) vers download/preuves-run-m7d/, md5
contrôlé par pièce contre les métadonnées Drive (modèle rapatrier_preuves_m6d,
D99 : zéro mélange — dossier dédié au run m7d ; lecture seule, aucune
écriture Drive).

Le trio du run (LISEZMOI-preuves.txt du réceptacle n'est pas une pièce) :
  temoin-m7d.txt, scenario-m7d-journal.log, VERDICT-run-m7d.txt

Usage : python3 scripts/rapatrier_preuves_m7d.py
Code de sortie : 0 = toutes pièces conformes, 1 = écart, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m7d")

PIECES_ATTENDUES = {"temoin-m7d.txt", "scenario-m7d-journal.log",
                    "VERDICT-run-m7d.txt"}


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m7")
        if not preuves or preuves.get("mimeType") != ds.FOLDER_MIME:
            print("[preuves-m7d] ERREUR FATALE : /test/preuves-m7 absent",
                  file=sys.stderr)
            return 2
        entries = ds.list_folder(preuves["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-m7d] ERREUR FATALE : listage impossible : {exc}",
              file=sys.stderr)
        return 2
    pieces = {n: f for n, f in entries.items()
              if f.get("mimeType") != ds.FOLDER_MIME
              and n in PIECES_ATTENDUES}
    manquantes = PIECES_ATTENDUES - set(pieces)
    if manquantes:
        print(f"[preuves-m7d] ERREUR FATALE : pièces absentes du coffre : "
              f"{sorted(manquantes)}", file=sys.stderr)
        return 2
    total, ok = 0, 0
    for nom, f in sorted(pieces.items()):
        total += 1
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[preuves-m7d] ÉCHEC téléchargement {nom} (HTTP {st})")
            continue
        chemin = DEST / nom
        chemin.write_bytes(body)
        local = ds.md5_of(chemin)
        attendu = (f.get("md5Checksum") or "").lower()
        if attendu and local != attendu:
            print(f"[preuves-m7d] ÉCART md5 {nom} : local {local} != "
                  f"drive {attendu}")
            continue
        ok += 1
        print(f"[preuves-m7d] {nom} : {len(body)} o, md5 {local[:8]}… "
              f"== drive — CONSTATÉ")
    extras = ({n for n, f in entries.items()
               if f.get("mimeType") != ds.FOLDER_MIME}
              - PIECES_ATTENDUES)
    if extras:
        print(f"[preuves-m7d] note : entrées non-pièces ignorées : "
              f"{sorted(extras)}")
    if ok != total:
        print(f"[preuves-m7d] ÉCHEC : {ok}/{total} pièces conformes")
        return 1
    print(f"[preuves-m7d] LES TROIS PIÈCES SONT LÀ, md5 contrôlés "
          f"({ok}/{total}) — le recoup sur pièces peut commencer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
