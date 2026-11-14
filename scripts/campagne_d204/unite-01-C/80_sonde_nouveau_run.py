#!/usr/bin/env python3
"""TRIADE addenda-287 (sonde) — 73 : le dossier « Nouveau run » ENTIER
(l'atelier, livraisons.csv, preuves-unite01 du bras T) pour situer le geste
du développeur au GUI. LECTURE SEULE."""
import io
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

UPLOAD = "/home/z/my-project/upload"
NR_ID = "10gEa_uykB_v9m46hJJvxjweME5jPA7Jl"
OUT = pathlib.Path("/home/z/my-project/scripts/73_nouveau_run.txt")

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
            fields="nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime,md5Checksum)",
            pageSize=200, orderBy="name", pageToken=token,
        ).execute()
        items.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return items

lignes = []

def walk(folder_id, path, prof=0):
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        ne = (it.get("createdTime") or "?")[:19]
        if it["mimeType"] == "application/vnd.google-apps.folder":
            lignes.append(f"{'  '*prof}[DIR ] {it['name']}  (né {ne})")
            walk(it["id"], p, prof+1)
        else:
            lignes.append(f"{'  '*prof}[FILE] {it['name']}  ({int(it.get('size',0) or 0)} o, né {ne})  [id={it['id']}]")

walk(NR_ID, "/test/Nouveau run")

# lire les CSV/textes clés rencontrés (livraisons.csv et tout .csv/.txt < 20 Ko)
print("\n".join(lignes))
OUT.write_text("\n".join(lignes), encoding="utf-8")

def lire(fid):
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, svc.files().get_media(fileId=fid))
    done = False
    while not done:
        _, done = dl.next_chunk()
    return buf.getvalue().decode("utf-8", errors="replace")

def walk_lis(folder_id):
    for it in list_folder(folder_id):
        if it["mimeType"] == "application/vnd.google-apps.folder":
            walk_lis(it["id"])
        else:
            nom = it["name"].lower()
            if (nom.endswith(".csv") or "livraison" in nom or "temoin" in nom and int(it.get("size",0) or 0) < 8000) and int(it.get("size",0) or 0) < 20000:
                try:
                    txt = lire(it["id"])
                    print(f"\n===== {it['name']} ({int(it.get('size',0) or 0)} o, né {(it.get('createdTime') or '?')[:19]}) =====")
                    print(txt[:3000])
                except Exception as e:
                    print(f"[!] {it['name']}: {e}")

print("\n########## CONTENUS ##########")
walk_lis(NR_ID)
