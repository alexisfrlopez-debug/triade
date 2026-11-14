#!/usr/bin/env python3
"""TRIADE — la sonde du coffre /test : l'arborescence entière avec dates de
naissance, pour situer le « Nouveau run » (14/11 08:58 UTC) et TOUT ce qui
est né après lui. Sortie sauvée + résumé des plus récents."""
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
TEST_FOLDER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
OUT = pathlib.Path("/home/z/my-project/scripts/60_arborescence_test.txt")

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
recents = []  # tout ce qui est né après le 14/11 08:00 UTC

def walk(folder_id, path):
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        ne = (it.get("createdTime") or "?")[:19]
        if it["mimeType"] == "application/vnd.google-apps.folder":
            lignes.append(f"[DIR ] {p}  (né {ne})")
            if ne >= "2026-11-14T08:00":
                recents.append(f"[DIR ] {p}  (né {ne})")
            walk(it["id"], p)
        else:
            size = int(it.get("size", 0) or 0)
            lignes.append(f"[FILE] {p}  ({size} o, né {ne})  [id={it['id']}]")
            if ne >= "2026-11-14T08:00":
                recents.append(f"[FILE] {p}  ({size} o, né {ne})")

root = svc.files().get(fileId=TEST_FOLDER, fields="id,name").execute()
lignes.append(f"[RACINE] {root['name']} (id {TEST_FOLDER})")
walk(TEST_FOLDER, "")
OUT.write_text("\n".join(lignes), encoding="utf-8")
print(f"[OK] {len(lignes)} lignes — arborescence sauvée : {OUT}")
print(f"\n===== NÉS APRÈS le 14/11 08:00 UTC ({len(recents)}) =====")
for l in recents:
    print(l)
print("\n===== PREMIERS 40 du /test (niveau racine) =====")
for l in lignes[:40]:
    print(l)
