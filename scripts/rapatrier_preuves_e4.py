#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_preuves_e4.py — rapatrie les pièces du run e4 depuis
/test/preuves-m5b (vague courante) vers download/preuves-run-e4/, md5
contrôlé par pièce contre les métadonnées Drive (modèle rapatrier_preuves_e2,
D99 : zéro mélange — dossier dédié au run e4).

Lecture seule (aucune écriture Drive). Usage : python3 scripts/rapatrier_preuves_e4.py
Code de sortie : 0 = toutes pièces conformes, 1 = écart, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-e4")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m5b")
        if not preuves or preuves.get("mimeType") != ds.FOLDER_MIME:
            print("[preuves-e4] ERREUR FATALE : /test/preuves-m5b absent",
                  file=sys.stderr)
            return 2
        entries = ds.list_folder(preuves["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-e4] ERREUR FATALE : listage impossible : {exc}",
              file=sys.stderr)
        return 2
    total, ok = 0, 0
    for nom, f in sorted(entries.items()):
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"[preuves-e4] IGNORÉ (dossier) : {nom}/")
            continue
        total += 1
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[preuves-e4] ÉCHEC téléchargement {nom} (HTTP {st})")
            continue
        chemin = DEST / nom
        chemin.write_bytes(body)
        local = ds.md5_of(chemin)
        attendu = (f.get("md5Checksum") or "").lower()
        if local == attendu:
            ok += 1
            print(f"[preuves-e4] OK {nom} ({len(body)} o, md5 {local[:12]}…)")
        else:
            print(f"[preuves-e4] ÉCART {nom} : local {local} != drive {attendu}")
    print(f"[preuves-e4] BILAN : {ok}/{total} pièces conformes")
    return 0 if ok == total and total > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
