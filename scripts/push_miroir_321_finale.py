#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""push_miroir_321_finale.py — LE GESTE FINAL DU PUSH MIROIR (les DEUX à
chaque push — la règle permanente) :
  1. le slot générique triade-history.bundle (id de la règle) : le contenu
     REMPLACÉ par l'histoire canonique complète (le bundle 321) ;
  2. D143 : l'ancien contenu (la lignée orpheline, 319 Mo) PRÉSERVÉ —
     copié aux archives-bundles/ renommé triade-history-319-3d94489.bundle ;
  3. le nom versionné triade-history-321-ee65b6a.bundle posé à côté
     (le précédent 308/311/312) ;
  4. le worklog.md REMPLACÉ (l'Entrée 321 corrigée).
Chaque geste RECROUPÉ au md5Checksum servi par Drive (recoup byte-byte).
"""
import hashlib
import json
import os
import sys
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

SAUVEGARDE = "1ZzvJjLlGyVW4YKnXWdAgZO0IjFETKOZY"      # TRIADE-sauvegarde-git
ARCHIVES_BUNDLES = "1D2MJl2_1lQbDU6oUWjun6rLyS-RrKle9"
BUNDLE_ID = "1YwYXkoSFC9GnnTgCK0FRT0GO-3hSxMix"        # triade-history.bundle
WORKLOG_ID = "1IjBk84S81ioBMASehROG3UsdJkO6JEBY"       # worklog.md

NOUVEAU_BUNDLE = "/tmp/triade-history-321-ee65b6a.bundle"
ANCIEN_BUNDLE = "/tmp/ancien-triade-history.bundle"
WORKLOG_LOCAL = "/tmp/triade-work/worklog.md"

ROUGES = 0


def coup(rouge: bool, message: str):
    global ROUGES
    if rouge:
        ROUGES += 1
    print(f"  [{'ROUGE' if rouge else 'VERT'}] {message}")


def md5_local(chemin):
    h = hashlib.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def envoyer(drive, chemin, file_id=None, parent=None, nom=None):
    taille = os.path.getsize(chemin)
    media = MediaFileUpload(chemin, resumable=True, mimetype=None,
                            chunksize=8 * 1024 * 1024)
    if file_id:
        demande = drive.files().update(fileId=file_id, media_body=media,
                                       fields="id, size, md5Checksum, "
                                              "modifiedTime")
    else:
        demande = drive.files().create(
            body={"name": nom, "parents": [parent]},
            media_body=media,
            fields="id, size, md5Checksum, modifiedTime")
    debut = time.time()
    reponse = None
    while reponse is None:
        statut, reponse = demande.next_chunk()
        if statut and statut.progress() * 100 % 20 < 1:
            print(f"    {statut.progress() * 100:5.1f} % "
                  f"({time.time() - debut:.0f} s)", end="\r")
    print(f"    envoyé : {int(reponse['size']):,} o en "
          f"{time.time() - debut:.0f} s".replace(",", " "))
    return reponse


def main():
    with open(JETON, encoding="utf-8-sig") as f:
        info = json.load(f)
    creds = Credentials(
        token=None, refresh_token=info["refresh_token"],
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info["client_id"], client_secret=info["client_secret"],
        scopes=SCOPES)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    # ---- le recoup PRÉALABLE : l'ancien md5 du slot, l'ancien bundle local
    ancien = drive.files().get(fileId=BUNDLE_ID,
                               fields="size, md5Checksum").execute()
    ancien_md5_drive = ancien.get("md5Checksum")
    ancien_md5_local = md5_local(ANCIEN_BUNDLE)
    coup(ancien_md5_drive != ancien_md5_local,
         f"l'ancien bundle local == l'ancien du coffre "
         f"(md5 {ancien_md5_drive[:12]}…, "
         f"{int(ancien['size']):,} o)".replace(",", " "))

    # ---- 1) le slot générique : l'histoire canonique
    print("\n=== 1. LE SLOT GÉNÉRIQUE triade-history.bundle : "
          "l'histoire canonique ===")
    attendu = md5_local(NOUVEAU_BUNDLE)
    r = envoyer(drive, NOUVEAU_BUNDLE, file_id=BUNDLE_ID)
    coup(r.get("md5Checksum") != attendu,
         f"le slot remplacé : md5 Drive {r.get('md5Checksum', '')[:12]}… "
         f"== local {attendu[:12]}… "
         f"({int(r['size']):,} o)".replace(",", " "))

    # ---- 2) D143 : l'ancien (la lignée orpheline) préservé aux archives
    print("\n=== 2. D143 : L'ANCIEN (la lignée orpheline) PRÉSERVÉ ===")
    r2 = envoyer(drive, ANCIEN_BUNDLE, parent=ARCHIVES_BUNDLES,
                 nom="triade-history-319-3d94489.bundle")
    coup(r2.get("md5Checksum") != ancien_md5_drive,
         f"triade-history-319-3d94489.bundle aux archives-bundles : "
         f"md5 {r2.get('md5Checksum', '')[:12]}… == l'ancien du coffre "
         f"{ancien_md5_drive[:12]}…")

    # ---- 3) le nom versionné à côté (le précédent 308/311/312)
    print("\n=== 3. LE NOM VERSIONNÉ (le précédent 308/311/312) ===")
    r3 = envoyer(drive, NOUVEAU_BUNDLE, parent=SAUVEGARDE,
                 nom="triade-history-321-ee65b6a.bundle")
    coup(r3.get("md5Checksum") != attendu,
         f"triade-history-321-ee65b6a.bundle : md5 "
         f"{r3.get('md5Checksum', '')[:12]}… == local {attendu[:12]}…")

    # ---- 4) le worklog REMPLACÉ (l'Entrée 321 corrigée)
    print("\n=== 4. LE WORKLOG REMPLACÉ ===")
    attendu_w = md5_local(WORKLOG_LOCAL)
    r4 = envoyer(drive, WORKLOG_LOCAL, file_id=WORKLOG_ID)
    coup(r4.get("md5Checksum") != attendu_w,
         f"worklog.md remplacé : md5 {r4.get('md5Checksum', '')[:12]}… "
         f"== local {attendu_w[:12]}… "
         f"({int(r4['size']):,} o)".replace(",", " "))

    # ---- la relecture finale du dossier
    print("\n=== LA RELECTURE FINALE DU TRIADE-sauvegarde-git ===")
    page, items = None, []
    while True:
        resp = drive.files().list(
            q=f"'{SAUVEGARDE}' in parents and trashed = false",
            pageSize=200,
            fields="nextPageToken, files(name, size, modifiedTime)",
            pageToken=page).execute()
        items += resp.get("files", [])
        page = resp.get("nextPageToken")
        if not page:
            break
    noms = {it["name"]: it for it in items}
    for attendu_nom, attendu_taille in (
            ("triade-history.bundle", os.path.getsize(NOUVEAU_BUNDLE)),
            ("triade-history-321-ee65b6a.bundle",
             os.path.getsize(NOUVEAU_BUNDLE)),
            ("worklog.md", os.path.getsize(WORKLOG_LOCAL))):
        it = noms.get(attendu_nom)
        coup(not it or str(attendu_taille) != it.get("size"),
             f"{attendu_nom} : {it and it.get('size')} o au coffre "
             f"(attendu {attendu_taille:,} o)".replace(",", " "))
    ab = drive.files().list(
        q=f"'{ARCHIVES_BUNDLES}' in parents and trashed = false "
          "and name = 'triade-history-319-3d94489.bundle'",
        fields="files(name, size)").execute().get("files", [])
    coup(not ab or str(os.path.getsize(ANCIEN_BUNDLE)) != ab[0].get("size"),
         f"archives-bundles/triade-history-319-3d94489.bundle : "
         f"{ab and ab[0].get('size')} o (attendu "
         f"{os.path.getsize(ANCIEN_BUNDLE):,} o)".replace(",", " "))

    print(f"\n=== BILAN : {'TOUT VERT' if ROUGES == 0 else str(ROUGES) + ' ROUGE'} ===")
    return 0 if ROUGES == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
