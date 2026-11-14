#!/usr/bin/env python3
"""TRIADE — la sonde de la RACINE du coffre Drive (le miroir du dépôt y vit) :
où en est le miroir ? quelle est la dernière Entrée consignée ?"""
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"

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

def walk(folder_id, path, depth=0):
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        if it["mimeType"] == "application/vnd.google-apps.folder":
            print(f"{'  '*depth}[DIR ] {p}  (né {(it.get('createdTime') or '?')[:19]})")
            if depth < 2:
                walk(it["id"], p, depth + 1)
        else:
            size = int(it.get("size", 0) or 0)
            print(f"{'  '*depth}[FILE] {p}  ({size/1024:.1f} Ko, modifié {(it.get('modifiedTime') or '?')[:19]})  [id={it['id']}]")

root = svc.files().get(fileId=ROOT, fields="id,name").execute()
print(f"[RACINE] {root['name']}")
walk(ROOT, "")
