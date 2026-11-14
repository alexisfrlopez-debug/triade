#!/usr/bin/env python3
"""TRIADE addenda-286 — 70 : sonde du dossier « preuves-unite01C » dans /test.
Le développeur a fait tourner le kit C (scénario crashé, code 1) puis déposé
ses preuves dans /test/preuves-unite01C. On liste l'arborescence entière,
tailles, dates de naissance, ids — sans rien écrire."""
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
TEST_FOLDER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
OUT = pathlib.Path("/home/z/my-project/scripts/70_arborescence_preuves_unite01C.txt")

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

# 1) retrouver le dossier preuves-unite01C à la racine de /test
racine = list_folder(TEST_FOLDER)
cible = [it for it in racine if it["name"].lower().startswith("preuves")]
if not cible:
    print("[ERREUR] aucun dossier « preuves* » à la racine de /test ; contenu racine :")
    for it in racine:
        print(f"  - {it['name']} ({it['mimeType']}, né {(it.get('createdTime') or '?')[:19]})")
    raise SystemExit(1)

lignes = []
for d in cible:
    lignes.append(f"[CIBLE] {d['name']} (id {d['id']}, né {(d.get('createdTime') or '?')[:19]})")

def walk(folder_id, path):
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        ne = (it.get("createdTime") or "?")[:19]
        mod = (it.get("modifiedTime") or "?")[:19]
        if it["mimeType"] == "application/vnd.google-apps.folder":
            lignes.append(f"[DIR ] {p}  (né {ne}, modifié {mod})")
            walk(it["id"], p)
        else:
            size = int(it.get("size", 0) or 0)
            md5 = it.get("md5Checksum", "-")
            lignes.append(f"[FILE] {p}  ({size} o, né {ne}, md5 {md5})  [id={it['id']}]")

for d in cible:
    walk(d["id"], f"/test/{d['name']}")

OUT.write_text("\n".join(lignes), encoding="utf-8")
print(f"[OK] {len(lignes)} lignes — sauvé : {OUT}\n")
for l in lignes:
    print(l)
