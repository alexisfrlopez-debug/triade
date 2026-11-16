#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cloture_vague5.py — LA CLÔTURE DE LA VAGUE 5 : les DEUX failles de
cohérence de l'état livré, fermées. (1) Le rapport d'exécution livré citait
les empreintes SHA-256 d'une génération intermédiaire des archives
(59567916…/629229ba… — un build qui n'existe plus) : la ligne CORRIGÉE vers
les empreintes réelles du scellage final (990d7cb6…/cab4d688…), le rapport
REMPLACÉ à la racine ET aux côtés des instructions archivées. (2) Rien au
coffre ne consignait les empreintes réelles des deux zips livrés : la preuve
p10 finale (celle qui les consigne) et les métadonnées Zenodo DÉPOSÉES à la
racine. Fail-closed : recoup AVANT (les empreintes locales), écriture,
relecture recoupée (re-téléchargement + sha256). La voie d'écriture : le
relais OAuth de tokens/ (JAMAIS affiché). D143 : les remplacements créent
des révisions Drive (aucun octet perdu).
"""
import hashlib
import io
import json
import pathlib
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

JETON = "/home/z/my-project/tokens/oauth_token_relais.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
ARCHIVE = "1qqfk-yMNg3E5s1HVVeEkhmFceeDuPtNb"
V5 = pathlib.Path("/home/z/my-project/livraison-vague5")
RECOUP = V5 / "recoup-coffre"
RECOUP.mkdir(parents=True, exist_ok=True)


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


drive = build("drive", "v3", credentials=charger(), cache_discovery=False)


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def lister(parent):
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
    return items


def trouver_fichier(nom, parent):
    for it in lister(parent):
        if it["name"] == nom and it.get("mimeType") != (
                "application/vnd.google-apps.folder"):
            return it["id"]
    return None


def trouver_dossier(nom, parent):
    for it in lister(parent):
        if it["name"] == nom and it.get("mimeType") == (
                "application/vnd.google-apps.folder"):
            return it["id"]
    return None


def televerser(chemin, nom, parent):
    """Crée ou REMPLACE (jamais de doublon) — retourne l'id."""
    existant = trouver_fichier(nom, parent)
    media = MediaFileUpload(str(chemin), resumable=True)
    if existant:
        drive.files().update(fileId=existant, media_body=media).execute()
        print(f"  [remplacé] {nom} (id={existant[:12]}…, "
              f"{pathlib.Path(chemin).stat().st_size} o)")
        return existant
    cree = drive.files().create(
        body={"name": nom, "parents": [parent]},
        media_body=media, fields="id").execute()
    print(f"  [livré] {nom} (id={cree['id'][:12]}…, "
          f"{pathlib.Path(chemin).stat().st_size} o)")
    return cree["id"]


def recouper(nom, fid, chemin_local):
    """Re-télécharge et confronte sha256 — la relecture recoupée."""
    destination = RECOUP / f"recoup-{nom}"
    with io.FileIO(destination, "wb") as fh:
        t = MediaIoBaseDownload(fh, drive.files().get_media(fileId=fid))
        fini = False
        while not fini:
            _, fini = t.next_chunk()
    if sha256(destination) == sha256(chemin_local):
        print(f"  [VERT] {nom} — re-téléchargé, sha256 IDENTIQUE au local")
        return True
    print(f"  [ROUGE] {nom} — sha256 DIVERGE du local !")
    return False


rouges = 0

print("=== 1. LE RAPPORT D'EXÉCUTION CORRIGÉ (racine du coffre) ===")
fid = televerser(V5 / "rapport-execution-vague5.txt",
                 "rapport-execution-vague5.txt", RACINE)
rouges += 0 if recouper("rapport-execution-vague5.txt", fid,
                        V5 / "rapport-execution-vague5.txt") else 1

print("=== 2. LE RAPPORT D'EXÉCUTION CORRIGÉ (aux côtés des instructions) ===")
fid = televerser(V5 / "rapport-execution-vague5.txt",
                 "rapport-execution-vague5.txt", ARCHIVE)
rouges += 0 if recouper("ARCHIVE-rapport-execution-vague5.txt", fid,
                        V5 / "rapport-execution-vague5.txt") else 1

print("=== 3. LA PREUVE p10 FINALE (racine) — les empreintes réelles "
      "des deux archives ===")
fid = televerser(V5 / "p10-table5-octets.txt", "p10-table5-octets.txt",
                 RACINE)
rouges += 0 if recouper("p10-table5-octets.txt", fid,
                        V5 / "p10-table5-octets.txt") else 1

print("=== 4. LES MÉTADONNÉES ZENODO (racine) ===")
fid = televerser(V5 / "zenodo-metadata-v0180.json",
                 "zenodo-metadata-v0180.json", RACINE)
rouges += 0 if recouper("zenodo-metadata-v0180.json", fid,
                        V5 / "zenodo-metadata-v0180.json") else 1

print("=== 5. TRIADE-sauvegarde-git (métadonnées seulement) ===")
dossier = trouver_dossier("TRIADE-sauvegarde-git", RACINE)
if dossier:
    for it in sorted(lister(dossier), key=lambda x: x["name"]):
        print(f"  {it['name']}  ({it.get('size', '?')} o, "
              f"mod={it.get('modifiedTime', '?')})")
else:
    print("  [ROUGE] le dossier TRIADE-sauvegarde-git introuvable à la racine")
    rouges += 1

print("=== BILAN DE LA CLÔTURE : "
      f"{'TOUT VERT' if rouges == 0 else str(rouges) + ' ROUGE'} ===")
sys.exit(0 if rouges == 0 else 1)
