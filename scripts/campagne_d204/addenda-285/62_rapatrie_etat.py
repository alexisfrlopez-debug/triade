#!/usr/bin/env python3
"""TRIADE — le rapatriement de l'état courant (après le rollback du bac local) :
- le miroir du dépôt (journal, worklog, carte OU-TROUVER, bundle courant)
- le « Nouveau run » (les pièces texte < 200 Ko)
- les trois kits loupe-01 (T v1, T v2, C)
- la carte LISEZMOI-KITS-UNITES-D204, le MANIFESTE de la Cérémonie
Chaque pièce : sha256 + md5 portés au manifeste du bac."""
import hashlib
import pathlib
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

UPLOAD = "/home/z/my-project/upload"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
BAC = pathlib.Path("/home/z/my-project/download")
WORK = pathlib.Path("/home/z/my-project/work")

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
            fields="nextPageToken,files(id,name,mimeType,size)",
            pageSize=200, orderBy="name", pageToken=token,
        ).execute()
        items.extend(res.get("files", []))
        token = res.get("nextPageToken")
        if not token:
            return items

def telecharge(file_id) -> bytes:
    for essai in range(4):
        try:
            req = svc.files().get_media(fileId=file_id)
            buf = io.BytesIO()
            dl = MediaIoBaseDownload(buf, req)
            fin = False
            while not fin:
                _, fin = dl.next_chunk(num_retries=3)
            return buf.getvalue()
        except Exception as e:
            if essai == 3:
                raise
            time.sleep(2 * (essai + 1))

def empreintes(corps: bytes):
    return (hashlib.sha256(corps).hexdigest(),
            hashlib.md5(corps).hexdigest())

# ---- la sélection -----------------------------------------------------------
def a_prendre(namespace, path, size):
    if namespace == "R":
        return path in {
            "/OU-TROUVER-LES-LIVRABLES.md",
            "/Cérémonie/MANIFESTE.txt",
            "/TRIADE-sauvegarde-git/docs/JOURNAL_TRAVAIL.md",
            "/TRIADE-sauvegarde-git/worklog.md",
            "/TRIADE-sauvegarde-git/OU-TROUVER-LES-LIVRABLES.md",
        }
    if namespace == "BUNDLE":
        return True  # /TRIADE-sauvegarde-git/triade-history.bundle seul
    # namespace == "T" (le /test)
    if path == "/LISEZMOI-KITS-UNITES-D204.txt":
        return True
    for prefixe in ("/kit-unite-loupe-01-C-20261114/",
                    "/kit-unite-loupe-01-T-20261114-v2/",
                    "/kit-unite-loupe-01-T-20261114/"):
        if path.startswith(prefixe):
            return True
    if path.startswith("/Nouveau run/"):
        return size < 200000 and not path.endswith(".zip")
    return False

def destination(namespace, path):
    p = path.lstrip("/")
    if namespace == "R":
        if "sauvegarde-git" in p:
            return BAC / "miroir-etat" / p.split("/", 1)[1]
        if p == "OU-TROUVER-LES-LIVRABLES.md":
            return BAC / "miroir-etat" / "OU-TROUVER-LES-LIVRABLES-racine.md"
        if p.startswith("Cérémonie/"):
            return BAC / "miroir-etat" / "MANIFESTE-ceremonie.txt"
    if namespace == "BUNDLE":
        return WORK / "triade-history.bundle"
    return BAC / "nouveau-run" / p  # namespace T

def walk(namespace, folder_id, path):
    for it in list_folder(folder_id):
        p = f"{path}/{it['name']}"
        if it["mimeType"] == "application/vnd.google-apps.folder":
            walk(namespace, it["id"], p)
        else:
            size = int(it.get("size", 0) or 0)
            if not a_prendre(namespace, p, size):
                continue
            dest = destination(namespace, p)
            dest.parent.mkdir(parents=True, exist_ok=True)
            corps = telecharge(it["id"])
            dest.write_bytes(corps)
            s, m = empreintes(corps)
            print(f"[{len(corps):>7} o] {p}  sha256 {s[:16]}…  md5 {m[:12]}…")
            MANIFESTE.append(f"{p}\t{len(corps)}\t{s}\t{m}")

MANIFESTE = []

# le bundle courant du miroir (75 Mo) — à part, timeout long
print("===== LE BUNDLE COURANT DU MIROIR =====")
for it in list_folder(ROOT):
    if it["name"] == "TRIADE-sauvegarde-git":
        for sous in list_folder(it["id"]):
            if sous["name"] == "triade-history.bundle":
                dest = WORK / "triade-history.bundle"
                corps = telecharge(sous["id"])
                dest.write_bytes(corps)
                s, m = empreintes(corps)
                print(f"[{len(corps):>7} o] triade-history.bundle  sha256 {s[:16]}…  md5 {m[:12]}…")
                MANIFESTE.append(f"/TRIADE-sauvegarde-git/triade-history.bundle\t{len(corps)}\t{s}\t{m}")
        break

print("\n===== LA RACINE (pièces choisies) =====")
walk("R", ROOT, "")
print("\n===== LE /test (pièces choisies) =====")
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
walk("T", TEST, "")

bac = BAC / "nouveau-run" / "MANIFESTE-RAPATRIEMENT.txt"
bac.parent.mkdir(parents=True, exist_ok=True)
bac.write_text("\n".join(MANIFESTE) + "\n", encoding="utf-8")
print(f"\n[OK] {len(MANIFESTE)} pièces rapatriées — manifeste : {bac}")
