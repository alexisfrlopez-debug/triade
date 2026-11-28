#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA LIVRAISON DU TERRAIN.12 au coffre — LA VOIE DU RELAIS (D263, le jeton du
maître : le compte de service n'a point de quota, la mesure du 28/11) :
  kit        — le kit v1062 téléversé au /livrables (recop byte-byte, l'id épinglé) ;
  notebooks  — les DEUX copies v1063 (VIVANTE + AVEUGLE) au /livrables ;
  archive    — les supersédées (les notebooks v1062 ×2 + le kit v1061) DÉPLACÉES
               au lot livrables_supersedes_20261128_terrain12 du dossier ARCHIVE ;
  inventaire — le /livrables inventorié."""
import hashlib
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

SA_PATH = "/home/z/my-project/upload/physichong-4b3b7222b48c.json"
TOKENS_FOLDER = "1EMxwHKkkfKROjFsHhu4vpKZpgqW-rgZL"
COFFRE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
ID_LIVRABLES = "1wF0p0g-OPdnL7fgnNsJb6D1rXhtyHqIZ"

# ── le jeton du relais (la voie éprouvée D263) ──
creds_ro = service_account.Credentials.from_service_account_file(
    SA_PATH, scopes=["https://www.googleapis.com/auth/drive.readonly"])
creds_ro.refresh(Request())
drive_ro = build("drive", "v3", credentials=creds_ro)
relais = json.loads(drive_ro.files().get_media(
    fileId=drive_ro.files().list(
        q=f"'{TOKENS_FOLDER}' in parents and name = 'oauth_token_relais.json' and trashed = false",
        fields="files(id)", pageSize=1).execute()["files"][0]["id"]).execute().decode("utf-8"))
data = urllib.parse.urlencode({
    "client_id": relais["client_id"], "client_secret": relais["client_secret"],
    "refresh_token": relais["refresh_token"], "grant_type": "refresh_token"}).encode()
with urllib.request.urlopen(urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=data), timeout=30) as r:
    TOK = json.loads(r.read().decode("utf-8"))["access_token"]
print("[relais] le jeton frappé.")


def api(url, method="GET", payload=None, octets=None, mime="application/json"):
    if octets is not None:
        req = urllib.request.Request(url, data=octets, method=method,
                                     headers={"Authorization": f"Bearer {TOK}",
                                              "Content-Type": mime})
    else:
        corps = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(url, data=corps, method=method,
                                     headers={"Authorization": f"Bearer {TOK}",
                                              "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        lu = r.read()
        return json.loads(lu.decode()) if lu else {}


def sha256f(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def deposer(chemin, mime):
    p = pathlib.Path(chemin)
    attendu = sha256f(p)
    doublons = api("https://www.googleapis.com/drive/v3/files?q=" + urllib.parse.quote(
        f"'{ID_LIVRABLES}' in parents and name = '{p.name}' and trashed = false"))
    if doublons.get("files"):
        raise SystemExit(f"DOUBLON au /livrables : {p.name}")
    frontieres = "tr312t3rrain12"
    corps = (f"--{frontieres}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
             + json.dumps({"name": p.name, "parents": [ID_LIVRABLES]})
             + f"\r\n--{frontieres}\r\nContent-Type: {mime}\r\n\r\n").encode("utf-8")
    corps += p.read_bytes() + f"\r\n--{frontieres}--\r\n".encode("utf-8")
    rep = api("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
              method="POST", octets=corps,
              mime=f"multipart/related; boundary={frontieres}")
    fid = rep["id"]
    time.sleep(2)
    relu = urllib.request.urlopen(urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media",
        headers={"Authorization": f"Bearer {TOK}"}), timeout=300).read()
    if hashlib.sha256(relu).hexdigest() != attendu:
        raise SystemExit(f"RECOP-ROUGE : {p.name}")
    print(f"  pièce créée : {p.name} ({p.stat().st_size} o) — id {fid} — RECOP VERT")
    return fid


def fichiers_au(nom, parent):
    return api("https://www.googleapis.com/drive/v3/files?q=" + urllib.parse.quote(
        f"'{parent}' in parents and name = '{nom}' and trashed = false")
        + "&fields=files(id,name,size)").get("files", [])


def patch_parents(file_id, remove=None, add=None):
    params = []
    if remove:
        params.append("removeParents=" + remove)
    if add:
        params.append("addParents=" + add)
    api(f"https://www.googleapis.com/drive/v3/files/{file_id}?" + "&".join(params),
        method="PATCH", payload={})


cmd = sys.argv[1] if len(sys.argv) > 1 else "inventaire"

if cmd == "kit":
    deposer("/home/z/my-project/work/TRIADE_kit_entrainement_v1062.zip",
            "application/zip")

elif cmd == "notebooks":
    deposer("/home/z/my-project/work/Entrainement-Colab-v1063-VIVANTE.ipynb",
            "application/x-ipynb+json")
    deposer("/home/z/my-project/work/Entrainement-Colab-v1063-AVEUGLE.ipynb",
            "application/x-ipynb+json")

elif cmd == "archive":
    archive = fichiers_au("ARCHIVE", COFFRE)
    if not archive:
        raise SystemExit("ARCHIVE-ABSENT")
    LOT = "livrables_supersedes_20261128_terrain12"
    lots = fichiers_au(LOT, archive[0]["id"])
    if lots:
        id_lot = lots[0]["id"]
        print(f"le lot existe : {LOT} → {id_lot}")
    else:
        id_lot = api("https://www.googleapis.com/drive/v3/files", method="POST", payload={
            "name": LOT, "mimeType": "application/vnd.google-apps.folder",
            "parents": [archive[0]["id"]]}).get("id")
        print(f"le lot créé : {LOT} → {id_lot}")
    for nom in ("Entrainement-Colab-v1062-VIVANTE.ipynb",
                "Entrainement-Colab-v1062-AVEUGLE.ipynb",
                "TRIADE_kit_entrainement_v1061.zip"):
        pieces = fichiers_au(nom, ID_LIVRABLES)
        if not pieces:
            print(f"  {nom} : déjà absente du /livrables")
            continue
        if len(pieces) > 1:
            raise SystemExit(f"DOUBLON au /livrables : {nom} ×{len(pieces)}")
        fid = pieces[0]["id"]
        patch_parents(fid, remove=ID_LIVRABLES)   # retirer d'abord (le 403 du combiné)
        time.sleep(2)
        patch_parents(fid, add=id_lot)            # puis ajouter au lot
        time.sleep(2)
        if fichiers_au(nom, id_lot) and not fichiers_au(nom, ID_LIVRABLES):
            print(f"  {nom} : DÉPLACÉE au lot — VERT")
        else:
            raise SystemExit(f"DÉPLACEMENT-ROUGE : {nom}")

print("── le /livrables au terme ──")
for f in sorted(api("https://www.googleapis.com/drive/v3/files?q=" + urllib.parse.quote(
        f"'{ID_LIVRABLES}' in parents and trashed = false")
        + "&fields=files(id,name,size,modifiedTime)&pageSize=100").get("files", []),
        key=lambda x: x["name"]):
    print(f"  {f['modifiedTime']}  {f['name']}  ({f.get('size', '?')} o)")
