#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_relais_ecriture.py — LA SONDE DU RELAIS OAUTH (lecture seule).

Charge tokens/oauth_token_relais.json (le /Tokens du coffre, rapatrié par
gdrive_tokens.py — AUCUNE valeur de jeton affichée) et tente LA LECTURE de
la racine du coffre, du /instructions et du /ARCHIVE/instructions_20261116.
Le refresh token est exercé à la première requête : si le relais est mort
(invalid_grant), la sonde le nomme et s'arrête — AUCUNE écriture ici
(D143 : rien ne se jette au coffre ; fail-closed avant tout geste).
"""
import json
import sys

from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ARCHIVE = "1qqfk-yMNg3E5s1HVVeEkhmFceeDuPtNb"


def charger():
    with open(JETON, encoding="utf-8-sig") as f:
        info = json.load(f)
    return Credentials(
        token=None,
        refresh_token=info["refresh_token"],
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        scopes=SCOPES,
    )


def lister(drive, parent, etiquette):
    page, items = None, []
    while True:
        resp = drive.files().list(
            q=f"'{parent}' in parents and trashed = false",
            pageSize=200,
            fields=("nextPageToken, files(id, name, mimeType, size, "
                    "md5Checksum, modifiedTime)"),
            pageToken=page).execute()
        items += resp.get("files", [])
        page = resp.get("nextPageToken")
        if not page:
            break
    print(f"=== {etiquette} : {len(items)} entrées ===")
    for it in sorted(items, key=lambda x: x["name"]):
        print(f"  {it['name']}  ({it.get('size', '?')} o, "
              f"md5={str(it.get('md5Checksum', '—'))[:8]}…, "
              f"mod={it.get('modifiedTime', '?')})")
    return items


if __name__ == "__main__":
    drive = build("drive", "v3", credentials=charger(),
                  cache_discovery=False)
    try:
        racine = lister(drive, RACINE, "la racine du coffre")
        instructions = lister(drive, INSTRUCTIONS, "/instructions")
        archive = lister(drive, ARCHIVE, "/ARCHIVE/instructions_20261116")
    except RefreshError as e:
        print(f"SONDE : ROUGE — le refresh du relais est REFUSÉ "
              f"({type(e).__name__}) : jeton mort (invalid_grant attendu).")
        sys.exit(2)
    print("SONDE : VERT — le relais OAuth vit (lecture au coffre). "
          "La voie d'écriture est praticable.")
