#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — la sonde du coffre /test après l'annonce du développeur (« j'ai
déposé ce que tu m'as demandé ») : l'arborescence entière, le DIFF contre la
sonde 60 (état 285), et TOUT ce qui est né après le dépôt du témoin C
(14/11 12:57 UTC) — pour nommer les pièces neuves AVANT tout nettoyage."""
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
TEST_FOLDER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
OUT = pathlib.Path("/home/z/my-project/scripts/77_arborescence_test.txt")
ANCIEN = pathlib.Path("/home/z/my-project/scripts/60_arborescence_test.txt")

creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"],
)
svc = build("drive", "v3", credentials=creds, cache_discovery=False)

def list_folder(folder_id):
    items, token = [], None
    while True:
        res = svc.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime)",
            pageSize=200, orderBy="name", pageToken=token,
        ).execute()
        items.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return items

lignes = []
recents = []   # tout ce qui est né après le dépôt du témoin C (14/11 12:57 UTC)
fichiers = {}  # chemin -> ligne (pour le diff)

def walk(folder_id, path):
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        ne = (it.get("createdTime") or "?")[:19]
        if it["mimeType"] == "application/vnd.google-apps.folder":
            lignes.append(f"[DIR ] {p}  (né {ne})")
            fichiers[p] = f"[DIR ] {p}  (né {ne})"
            if ne >= "2026-11-14T12:57":
                recents.append(f"[DIR ] {p}  (né {ne})")
            walk(it["id"], p)
        else:
            size = int(it.get("size", 0) or 0)
            ligne = f"[FILE] {p}  ({size} o, né {ne})  [id={it['id']}]"
            lignes.append(ligne)
            fichiers[p] = ligne
            if ne >= "2026-11-14T12:57":
                recents.append(ligne)

root = svc.files().get(fileId=TEST_FOLDER, fields="id,name").execute()
lignes.append(f"[RACINE] {root['name']} (id {TEST_FOLDER})")
walk(TEST_FOLDER, "")
OUT.write_text("\n".join(lignes), encoding="utf-8")
print(f"[OK] {len(lignes)} lignes — arborescence sauvée : {OUT}")

# ---- le DIFF contre la sonde 60 (état 285) ------------------------------------
anciens = {}
for l in ANCIEN.read_text(encoding="utf-8").splitlines():
    if l.startswith(("[DIR ", "[FILE]")):
        chemin = l.split("  (")[0].replace("[DIR ] ", "").replace("[FILE] ", "")
        anciens[chemin] = l

neufs = [p for p in fichiers if p not in anciens]
perdus = [p for p in anciens if p not in fichiers]
print(f"\n===== PIÈCES NEUVES depuis la sonde 60 ({len(neufs)}) =====")
for p in sorted(neufs):
    print(fichiers[p])
print(f"\n===== PIÈCES DISPARUES depuis la sonde 60 ({len(perdus)}) =====")
for p in sorted(perdus):
    print(anciens[p])

print(f"\n===== NÉS APRÈS le dépôt du témoin C 12:57 UTC ({len(recents)}) =====")
for l in recents:
    print(l)
