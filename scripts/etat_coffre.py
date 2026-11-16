#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""etat_coffre.py — Liste l'état du coffre avant la livraison vague 5 :
racine, /instructions, /ARCHIVE, /test. Lecture seule (relais OAuth).
Aucune valeur de jeton affichée.
"""
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

LIEUX = [
    ("RACINE", "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"),
    ("/instructions", "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"),
    ("/ARCHIVE (instructions_20261116)", "1qqfk-yMNg3E5s1HVVeEkhmFceeDuPtNb"),
    ("/test", "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"),
]


def main():
    with open(JETON, encoding="utf-8-sig") as f:
        info = {}
        # lecture des clés sans afficher les valeurs
        import json
        info = json.load(f)
    creds = Credentials(
        token=None,
        refresh_token=info["refresh_token"],
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info["client_id"],
        client_secret=info["client_secret"],
        scopes=SCOPES,
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    for nom_lieu, dossier_id in LIEUX:
        page, items = None, []
        while True:
            resp = drive.files().list(
                q=f"'{dossier_id}' in parents and trashed = false",
                pageSize=200,
                fields="nextPageToken, files(id, name, mimeType, size, "
                       "modifiedTime, md5Checksum)",
                pageToken=page).execute()
            items += resp.get("files", [])
            page = resp.get("nextPageToken")
            if not page:
                break
        print(f"=== {nom_lieu} : {len(items)} entrées ===")
        for it in sorted(items, key=lambda x: x["name"]):
            taille = it.get("size", "")
            md5 = (it.get("md5Checksum") or "")[:8]
            genre = "D" if it.get("mimeType") == \
                "application/vnd.google-apps.folder" else "f"
            print(f"  [{genre}] {it['name']}  ({taille} o, "
                  f"mod={it.get('modifiedTime', '')[:10]}, md5={md5}…)")
        print()


if __name__ == "__main__":
    main()
