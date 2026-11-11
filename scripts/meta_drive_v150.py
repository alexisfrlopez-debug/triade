#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — métadonnées Drive des fichiers d'instruction (ysddxpk0o, ic09ydeli).

Interroge files.get (name, md5Checksum, modifiedTime, createdTime, size)
pour dater précisément les dépôts / modifications. Aucun jeton affiché.
"""
import json
import sys
import urllib.request

sys.path.insert(0, "/home/z/my-project/triade/scripts")
import drive_api as dapi

FICHIERS = {
    "ysddxpk0o (/instructions)": "1n4vVoSBxJES5mNeUAjTMOx4aPfMbfWio",
    "ic09ydeli (/ARCHIVE)": "1PgMdDhsVKwk-RUgLTNML3g3GGHC89vL0",
    "f3q3x9i7n (/ARCHIVE)": "14lTRTQ4vMMZEZa68YVhU4tzGqzp5afDS",
}

tok = dapi.obtenir_token()
for nom, fid in FICHIERS.items():
    url = (f"{dapi.API}/files/{fid}"
           "?fields=name,md5Checksum,modifiedTime,createdTime,size")
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {tok}", "Accept": "application/json"})
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    print(f"{nom}: name={d.get('name')} size={d.get('size')} "
          f"md5={d.get('md5Checksum')}\n  created={d.get('createdTime')} "
          f"modified={d.get('modifiedTime')}")
