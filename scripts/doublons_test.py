#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 215 — détection de DOUBLONS Drive (même nom, IDs distincts).

list_folder() indexe par nom : deux fichiers « kit-loupe.zip » au même
dossier ne montrent qu'une entrée. Cette passe affiche TOUTES les
entrées (id, nom, md5, heure) pour nommer un éventuel doublon.
"""
import json
import pathlib
import sys
import urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


def lister_tout(folder_id):
    out = []
    token = None
    while True:
        params = {"q": f"'{folder_id}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,md5Checksum,"
                            "createdTime,modifiedTime)"}
        if token:
            params["pageToken"] = token
        st, body, _ = ds.api("GET", ds.API + "/files?" +
                             urllib.parse.urlencode(params))
        if st != 200:
            raise ds.SyncError(f"listing impossible ({st})")
        obj = json.loads(body)
        out.extend(obj.get("files", []))
        token = obj.get("nextPageToken")
        if not token:
            return out


def main():
    vus = {}
    for f in lister_tout(TEST_ID):
        if f["mimeType"] == ds.FOLDER_MIME:
            continue
        vus.setdefault(f["name"], []).append(f)
    for nom in sorted(vus):
        entrees = vus[nom]
        marque = "  <<< DOUBLON" if len(entrees) > 1 else ""
        for f in entrees:
            print(f"{nom}  md5={f.get('md5Checksum','-')[:12]}…  "
                  f"id={f['id']}  mod={f.get('modifiedTime','?')}{marque}")
    # dossiers et leurs éventuels doublons
    dd = {}
    for f in lister_tout(TEST_ID):
        if f["mimeType"] != ds.FOLDER_MIME:
            continue
        dd.setdefault(f["name"], []).append(f)
    for nom in sorted(dd):
        entrees = dd[nom]
        if len(entrees) > 1:
            for f in entrees:
                print(f"[dossier] {nom}/  id={f['id']}  mod={f.get('modifiedTime','?')}  <<< DOUBLON")
    return 0


if __name__ == "__main__":
    sys.exit(main())
