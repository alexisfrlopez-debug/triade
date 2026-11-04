#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_vagues_m5b.py — lecture seule : liste archives-livraisons/
vagues-m5b et rapatrie les scénarios/kits des vagues archivées (v8 et
autres) pour COMPARAISON avec le scénario e2.

Usage : python3 scripts/rapatrier_vagues_m5b.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"           # /test
DEST = REPO / "upload" / "vagues-archivees"


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
        archives = ds.list_folder(test["archives-livraisons"]["id"])
        vagues = ds.list_folder(archives["vagues-m5b"]["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[vagues] ERREUR FATALE : {exc}", file=sys.stderr)
        return 2
    print(f"[vagues] archives-livraisons/vagues-m5b : {len(vagues)} entrées")
    for nom, meta in sorted(vagues.items()):
        taille = meta.get("size", "DIR" if meta.get("mimeType") == ds.FOLDER_MIME else "?")
        print(f"  {nom} : {taille} o  md5={meta.get('md5Checksum', '-')[:8]}…  id={meta['id']}")
    DEST.mkdir(parents=True, exist_ok=True)
    ecarts = 0
    # Tout ce qui est fichier (LISEZMOI, scénarios, zips) — les pièces de
    # cérémonie consommées incluses
    for nom, meta in sorted(vagues.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            continue
        destination = DEST / nom
        md5_local = telecharger(meta["id"], destination)
        ok = md5_local == meta.get("md5Checksum", "-")
        print(f"[vagues] {nom} : {meta.get('size', '?')} o "
              f"{'MATCH' if ok else 'ÉCART'}")
        if not ok:
            ecarts += 1
    return 0 if ecarts == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
