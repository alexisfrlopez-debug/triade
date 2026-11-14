#!/usr/bin/env python3
"""TRIADE addenda-286 — 71 : rapatriement byte-byte de temoin-unite01C.txt
depuis /test/preuves-unite01C, avec re-téléchargement et comparaison
octet par octet (règle « jamais jeté, toujours revérifié »)."""
import hashlib
import pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

UPLOAD = "/home/z/my-project/upload"
FILE_ID = "1Vc7djUFjglqRaghQ1WU9ej7nY2b4rDii"
DEST = pathlib.Path("/home/z/my-project/download/nouveau-run/preuves-unite01C/temoin-unite01C.txt")

creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"],
)
svc = build("drive", "v3", credentials=creds, cache_discovery=False)

def telecharge(dest: pathlib.Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    meta = svc.files().get(fileId=FILE_ID, fields="name,size,md5Checksum,createdTime,modifiedTime").execute()
    with open(dest, "wb") as f:
        req = svc.files().get_media(fileId=FILE_ID)
        dl = MediaIoBaseDownload(f, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
    return meta

meta = telecharge(DEST)
b1 = DEST.read_bytes()
h1 = hashlib.sha256(b1).hexdigest()
print(f"[1er passage] {len(b1)} octets, sha256 {h1}")
print(f"[meta Drive] nom={meta['name']}, md5={meta.get('md5Checksum')}, né={meta.get('createdTime')}, modifié={meta.get('modifiedTime')}")

# re-téléchargement de contrôle
DEST2 = DEST.with_suffix(".ctrl.txt")
meta2 = telecharge(DEST2)
b2 = DEST2.read_bytes()
h2 = hashlib.sha256(b2).hexdigest()
print(f"[2e passage ] {len(b2)} octets, sha256 {h2}")
print(f"[CONTRÔLE  ] {'IDENTIQUES byte-byte' if b1 == b2 else 'DIFFÉRENTS !'}")
print(f"[md5 local ] {hashlib.md5(b1).hexdigest()}  (attendu Drive : {meta.get('md5Checksum')})")
DEST2.unlink()  # le double de contrôle est retiré, l'original reste

print("\n===== CONTENU temoin-unite01C.txt =====")
print(b1.decode("utf-8", errors="replace"))
