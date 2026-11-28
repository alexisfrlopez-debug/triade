#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE LECTEUR DE CAMPAGNE : tire la pièce la plus récente du /test (zip de
preuves + rapport du poste), l'extrait au bac et rapporte LES VERDICTS TELS
QUELS (le verdict_global du registre, la sonde des enveloppes, le gate,
l'horloge du rapport). Usage : lire_campagne.py [prefixe-zip]"""
import io
import json
import pathlib
import sys
import zipfile

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SA_PATH = "/home/z/my-project/upload/physichong-4b3b7222b48c.json"
ID_TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
prefixe = sys.argv[1] if len(sys.argv) > 1 else "preuves-campagne-"

creds = service_account.Credentials.from_service_account_file(
    SA_PATH, scopes=["https://www.googleapis.com/auth/drive.readonly"])
creds.refresh(Request())
drive = build("drive", "v3", credentials=creds)
fichiers = drive.files().list(
    q=f"'{ID_TEST}' in parents and trashed = false",
    fields="files(id, name, size, modifiedTime)", pageSize=100).execute().get("files", [])
candidats = sorted([f for f in fichiers if f["name"].startswith(prefixe)],
                   key=lambda f: f["modifiedTime"])
if not candidats:
    raise SystemExit(f"PIÈCE-ABSENTE : aucun {prefixe}* au /test")
pieces = []
for f in candidats[-3:]:  # le zip ET les rapports récents
    pieces.append(f)
for f in pieces:
    print(f"pièce : {f['name']} ({f['size']} o, {f['modifiedTime']})")

# la pièce la plus récente qui est un ZIP
zip_ent = next((f for f in reversed(candidats) if f["name"].endswith(".zip")), None)
if zip_ent is None:
    raise SystemExit("ZIP-ABSENT au /test")
buf = io.BytesIO()
dl = MediaIoBaseDownload(buf, drive.files().get_media(fileId=zip_ent["id"]))
done = False
while not done:
    _, done = dl.next_chunk()
dest = pathlib.Path("/home/z/my-project/work/lecture-campagne")
dest.mkdir(parents=True, exist_ok=True)
chemin_zip = dest / zip_ent["name"]
chemin_zip.write_bytes(buf.getvalue())
with zipfile.ZipFile(chemin_zip) as z:
    z.extractall(dest / "contenu")
    noms = z.namelist()
print(f"extrait : {len(noms)} pièces → {dest / 'contenu'}")

# LES VERDICTS TELS QUELS
c = dest / "contenu"
for nom_reg in ("registre-campagne.json", "registre.json"):
    p = c / nom_reg
    if p.exists():
        reg = json.loads(p.read_text(encoding="utf-8"))
        print("\n=== LE VERDICT GLOBAL (tel quel) ===")
        print(json.dumps(reg.get("verdict_global", reg), ensure_ascii=False, indent=1))
        break
for nom_s in ("sonde-verdict.json",):
    p = c / nom_s
    if p.exists():
        print("\n=== LA SONDE DES ENVELOPPES ===")
        print(p.read_text(encoding="utf-8")[:800])
p = c / "gate-verdict.json"
if p.exists():
    g = json.loads(p.read_text(encoding="utf-8"))
    print("\n=== LE GATE ===")
    print(json.dumps(g, ensure_ascii=False)[:400])
# les rapports du poste récents
for f in sorted(candidats, key=lambda x: x["modifiedTime"]):
    if f["name"].startswith("rapport-poste"):
        print(f"\n=== LE RAPPORT DU POSTE ({f['name']}) ===")
        buf2 = io.BytesIO()
        dl2 = MediaIoBaseDownload(buf2, drive.files().get_media(fileId=f["id"]))
        done = False
        while not done:
            _, done = dl2.next_chunk()
        print(buf2.getvalue().decode("utf-8", errors="replace")[:2500])
        break
