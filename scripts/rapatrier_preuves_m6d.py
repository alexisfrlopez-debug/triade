#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_preuves_m6d.py — rapatrie les pièces du run M6-(d) depuis
/test/preuves-m6 (vague courante) vers download/preuves-run-m6d/, md5
contrôlé par pièce contre les métadonnées Drive (modèle rapatrier_preuves_e4,
D99 : zéro mélange — dossier dédié au run m6d).

Lecture seule (aucune écriture Drive). Usage : python3 scripts/rapatrier_preuves_m6d.py
Code de sortie : 0 = toutes pièces conformes, 1 = écart, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m6d")

# les trois pièces du run (LISEZMOI-preuves.txt du réceptacle : pas une pièce)
PIECES_ATTENDUES = {"temoin-m6d.txt", "scenario-m6d-journal.log",
                    "VERDICT-run-m6d.txt"}


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m6")
        if not preuves or preuves.get("mimeType") != ds.FOLDER_MIME:
            print("[preuves-m6d] ERREUR FATALE : /test/preuves-m6 absent",
                  file=sys.stderr)
            return 2
        entries = ds.list_folder(preuves["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-m6d] ERREUR FATALE : listage impossible : {exc}",
              file=sys.stderr)
        return 2
    pieces = {n: f for n, f in entries.items()
              if f.get("mimeType") != ds.FOLDER_MIME
              and n in PIECES_ATTENDUES}
    manquantes = PIECES_ATTENDUES - set(pieces)
    if manquantes:
        print(f"[preuves-m6d] ERREUR FATALE : pièces absentes du coffre : "
              f"{sorted(manquantes)}", file=sys.stderr)
        return 2
    total, ok = 0, 0
    for nom, f in sorted(pieces.items()):
        total += 1
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[preuves-m6d] ÉCHEC téléchargement {nom} (HTTP {st})")
            continue
        chemin = DEST / nom
        chemin.write_bytes(body)
        local = ds.md5_of(chemin)
        attendu = (f.get("md5Checksum") or "").lower()
        if local == attendu:
            ok += 1
            print(f"[preuves-m6d] OK {nom} ({len(body)} o, md5 {local[:12]}…)")
        else:
            print(f"[preuves-m6d] ÉCART {nom} : local {local} != drive {attendu}")
    print(f"[preuves-m6d] BILAN : {ok}/{total} pièces conformes")
    return 0 if ok == total and total > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
