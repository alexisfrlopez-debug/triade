#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_journal_v8.py — lecture seule : rapatrie les pièces du run v8
(archives-preuves/preuves-run-v8) pour COMPARAISON avec le run e2 (journal
proxy, témoin, journal du scénario). md5 recoupés par relecture.

Usage : python3 scripts/rapatrier_journal_v8.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"           # /test
DEST = REPO / "upload" / "preuves-run-v8"


def telecharger(file_id: str, destination: pathlib.Path) -> str:
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)
    return ds.md5_of(destination)


def main() -> int:
    try:
        test = ds.list_folder(TEST_ID)
        archives = ds.list_folder(test["archives-preuves"]["id"])
        v8 = ds.list_folder(archives["preuves-run-v8"]["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[v8] ERREUR FATALE : {exc}", file=sys.stderr)
        return 2
    DEST.mkdir(parents=True, exist_ok=True)
    print(f"[v8] preuves-run-v8 : {len(v8)} entrées")
    ecarts = 0
    for nom, meta in sorted(v8.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            continue
        md5_distant = meta.get("md5Checksum", "-")
        destination = DEST / nom
        md5_local = telecharger(meta["id"], destination)
        ok = md5_local == md5_distant
        print(f"[v8] {nom} : {meta.get('size', '?')} o "
              f"{'MATCH' if ok else 'ÉCART'}")
        if not ok:
            ecarts += 1
    return 0 if ecarts == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
