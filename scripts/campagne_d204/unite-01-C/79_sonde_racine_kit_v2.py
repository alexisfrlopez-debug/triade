#!/usr/bin/env python3
"""TRIADE addenda-287 (sonde) — 72 : le /test ENTIER à la racine + le kit v2
recoupé : naissances, EMPREINTES du kit C v2, présence ou absence de la
console du refus. LECTURE SEULE."""
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
TEST_FOLDER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
OUT = pathlib.Path("/home/z/my-project/scripts/72_racine_test_et_kit_v2.txt")

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
racine = list_folder(TEST_FOLDER)
lignes.append("===== RACINE /test =====")
for it in racine:
    ne = (it.get("createdTime") or "?")[:19]
    if it["mimeType"] == "application/vnd.google-apps.folder":
        lignes.append(f"[DIR ] {it['name']}  (né {ne})  [id={it['id']}]")
    else:
        lignes.append(f"[FILE] {it['name']}  ({int(it.get('size',0) or 0)} o, né {ne})  [id={it['id']}]")

# le kit v2 : arborescence + EMPREINTES
kits = [it for it in racine if it["name"] == "kit-unite-loupe-01-C-20261114-v2"]
if kits:
    lignes.append("\n===== KIT v2 (arborescence) =====")
    for it in list_folder(kits[0]["id"]):
        ne = (it.get("createdTime") or "?")[:19]
        md5 = it.get("md5Checksum", "-")
        if it["mimeType"] == "application/vnd.google-apps.folder":
            lignes.append(f"[DIR ] {it['name']}  (né {ne})")
            for s in list_folder(it["id"]):
                lignes.append(f"      [FILE] {s['name']} ({int(s.get('size',0) or 0)} o) md5 {s.get('md5Checksum','-')}")
        else:
            lignes.append(f"[FILE] {it['name']}  ({int(it.get('size',0) or 0)} o, né {ne})  md5 {md5}")
    # télécharger EMPREINTES pour lecture
    emp = [f for f in list_folder(kits[0]["id"]) if f["name"].startswith("EMPREINTES")]
    if emp:
        import io
        from googleapiclient.http import MediaIoBaseDownload
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, svc.files().get_media(fileId=emp[0]["id"]))
        done = False
        while not done:
            _, done = dl.next_chunk()
        lignes.append(f"\n===== EMPREINTES du kit v2 ({emp[0]['name']}, {emp[0].get('size')} o) =====")
        lignes.append(buf.getvalue().decode("utf-8", errors="replace"))
else:
    lignes.append("\n[!] le kit v2 INTROUVABLE à la racine du /test")

OUT.write_text("\n".join(lignes), encoding="utf-8")
print("\n".join(lignes))
print(f"\n[OK] sauvé : {OUT}")
