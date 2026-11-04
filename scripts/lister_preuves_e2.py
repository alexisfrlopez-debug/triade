#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lister_preuves_e2.py — lecture seule : liste /test/preuves-m5b, /test/archives-*
avec createdTime, pour situer le run e2. Aucune écriture.

Usage : python3 scripts/lister_preuves_e2.py
"""

import json
import pathlib
import sys
import urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"  # dossier /test du Drive


def liste_detaillee(folder_id: str) -> dict:
    out = {}
    token = None
    while True:
        params = {
            "q": f"'{folder_id}' in parents and trashed = false",
            "pageSize": "200",
            "fields": ("nextPageToken,files(id,name,mimeType,md5Checksum,"
                       "size,createdTime,modifiedTime)"),
        }
        if token:
            params["pageToken"] = token
        st, body, _ = ds.api(
            "GET", ds.API + "/files?" + urllib.parse.urlencode(params))
        if st != 200:
            raise ds.SyncError(f"listing impossible ({st}) : {body[:200]!r}")
        obj = json.loads(body)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def affiche(nom: str, dossier_id: str) -> None:
    try:
        entrees = liste_detaillee(dossier_id)
    except Exception as exc:  # noqa: BLE001
        print(f"[{nom}] ERREUR : {exc}", file=sys.stderr)
        return
    print(f"=== {nom} ({len(entrees)} entrées) ===")
    for nom_f, meta in sorted(entrees.items(), key=lambda x: x[1].get("createdTime", "")):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR        ] {nom_f}  id={meta['id']}")
        else:
            print(f"  [{meta.get('size', '?'):>7} o] {nom_f}  "
                  f"cree={meta.get('createdTime', '?')}  "
                  f"md5={meta.get('md5Checksum', '-')[:8]}…")


def main() -> int:
    test = liste_detaillee(TEST_ID)
    for cible in ("preuves-m5b", "archives-livraisons", "archives-preuves"):
        if cible in test and test[cible].get("mimeType") == ds.FOLDER_MIME:
            affiche(f"/test/{cible}", test[cible]["id"])
        else:
            print(f"=== /test/{cible} : ABSENT ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
