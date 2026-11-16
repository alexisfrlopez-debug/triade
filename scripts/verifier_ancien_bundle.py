#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_ancien_bundle.py — Télécharge l'ancien triade-history.bundle du
coffre (319 Mo), liste ses pointes, et vérifie CONTRE le miroir GitHub si
chaque pointe est atteignable dans l'historique actuel (le préalable
fail-closed à tout remplacement : rien ne doit se perdre).
"""
import json
import subprocess
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
BUNDLE_ID = "1YwYXkoSFC9GnnTgCK0FRT0GO-3hSxMix"   # triade-history.bundle
DEST = "/tmp/ancien-triade-history.bundle"
MIROIR = "/tmp/triade-mirror.git"


def main():
    with open(JETON, encoding="utf-8-sig") as f:
        info = json.load(f)
    creds = Credentials(
        token=None, refresh_token=info["refresh_token"],
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info["client_id"], client_secret=info["client_secret"],
        scopes=["https://www.googleapis.com/auth/drive"])
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    meta = drive.files().get(fileId=BUNDLE_ID,
                             fields="name, size, md5Checksum, "
                                    "modifiedTime").execute()
    print(f"l'ancien bundle au coffre : {meta['name']} "
          f"({int(meta['size']):,} o, mod={meta['modifiedTime'][:16]}, "
          f"md5={meta.get('md5Checksum', '')[:8]}…)".replace(",", " "))

    with open(DEST, "wb") as fh:
        telechargeur = MediaIoBaseDownload(
            fh, drive.files().get_media(fileId=BUNDLE_ID))
        fini = False
        while not fini:
            progres, fini = telechargeur.next_chunk()
            if progres:
                print(f"  téléchargement {progres.progress() * 100:5.1f} %",
                      end="\r")
    print("\n  [téléchargé] " + DEST)

    r = subprocess.run(["git", "bundle", "list-heads", DEST],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ROUGE] list-heads : {r.stderr.strip()[:300]}")
        return 1
    print("\n=== les pointes de l'ancien bundle ===")
    tètes = [l.split() for l in r.stdout.strip().splitlines() if l]
    tous_contenus = True
    for hache, ref in tètes:
        # la pointe est-elle un objet connu du miroir ET atteignable ?
        connu = subprocess.run(
            ["git", "-C", MIROIR, "cat-file", "-e", hache],
            capture_output=True).returncode == 0
        if connu and ref in ("refs/heads/main", "HEAD"):
            ancetre = subprocess.run(
                ["git", "-C", MIROIR, "merge-base", "--is-ancestor",
                 hache, "main"], capture_output=True).returncode == 0
            print(f"  {ref} : {hache[:12]}… — "
                  f"{'ANCÊTRE de main actuel' if ancetre else 'CONNU mais PAS ancêtre'}")
            tous_contenus = tous_contenus and ancetre
        else:
            print(f"  {ref} : {hache[:12]}… — "
                  f"{'objet CONNU du miroir' if connu else 'ABSENT du miroir (!)'}")
            tous_contenus = tous_contenus and connu
    if tous_contenus:
        verdict = "TOUT CONTENU : le remplacement ne perd rien"
    else:
        verdict = "DIVERGENCES : le remplacement perdrait de l'histoire — REFUS"
    print(f"\n=== {verdict} ===")
    return 0 if tous_contenus else 1


if __name__ == "__main__":
    sys.exit(main())
