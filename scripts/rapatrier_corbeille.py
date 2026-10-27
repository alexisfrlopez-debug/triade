#!/usr/bin/env python3
"""D66 — Récupérer depuis la CORBEILLE Drive la pièce terrain_20261027_224502.txt
(déposée puis nettoyée par le développeur avec le reste des anciens fichiers),
et rapatrier le demo_journal.txt (410 o) du run 23:07.

Lecture seule — l'application a le scope drive complet, la corbeille est
lisible tant que le fichier n'est pas définitivement purgé.
"""
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request

UPLOAD = "/home/z/my-project/upload/terrain_jetons.bin"
URL_TOKEN = "https://oauth2.googleapis.com/token"
DOSSIER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


def jeton_oauth():
    data = open(UPLOAD, "rb").read()
    champs = [c for c in data.split(b"\x00") if c]
    corps = urllib.parse.urlencode({
        "client_id": champs[0].decode(), "client_secret": champs[1].decode(),
        "refresh_token": champs[2].decode(), "grant_type": "refresh_token",
    }).encode()
    r = urllib.request.urlopen(urllib.request.Request(
        URL_TOKEN, data=corps,
        headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=30)
    return json.load(r)["access_token"]


def telecharge(jeton, file_id, dest):
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media",
        headers={"Authorization": "Bearer " + jeton})
    with urllib.request.urlopen(req, timeout=60) as rr:
        contenu = rr.read()
    open(dest, "wb").write(contenu)
    print(f"  → {dest} ({len(contenu)} o, md5 {hashlib.md5(contenu).hexdigest()})")
    return contenu


jeton = jeton_oauth()

# 1) fichiers À LA CORBEILLE du dossier test
q = urllib.parse.urlencode({
    "q": f"'{DOSSIER}' in parents and trashed = true",
    "fields": "files(id,name,size,modifiedTime)",
    "pageSize": 100})
req = urllib.request.Request("https://www.googleapis.com/drive/v3/files?" + q,
                             headers={"Authorization": "Bearer " + jeton})
trash = json.load(urllib.request.urlopen(req, timeout=30)).get("files", [])
print(f"corbeille du dossier test : {len(trash)} fichiers")
for f in sorted(trash, key=lambda x: x.get("modifiedTime", "")):
    if f["name"].startswith("terrain_2026"):
        print(f"  [journal] {f['name']}  taille={f.get('size')}  "
              f"modifié={f.get('modifiedTime')}")
    elif f["name"].startswith("demo_journal"):
        print(f"  [demo]   {f['name']}  taille={f.get('size')}  "
              f"modifié={f.get('modifiedTime')}")

# 2) la pièce ciblée
cible = [f for f in trash if f["name"] == "terrain_20261027_224502.txt"]
if cible:
    print("\nrapatriement du journal 22:45 (corbeille) :")
    telecharge(jeton, cible[0]["id"], "/home/z/my-project/upload/terrain_20261027_224502.txt")
else:
    print("\njournal 22:45 INTROUVABLE même en corbeille")

# 3) demo_journal.txt vivant (410 o, run 23:07) — déjà vu à l'étape listing
q2 = urllib.parse.urlencode({
    "q": f"'{DOSSIER}' in parents and trashed = false and name = 'demo_journal.txt'",
    "fields": "files(id,name,size,modifiedTime)"})
req = urllib.request.Request("https://www.googleapis.com/drive/v3/files?" + q2,
                             headers={"Authorization": "Bearer " + jeton})
vifs = json.load(urllib.request.urlopen(req, timeout=30)).get("files", [])
if vifs:
    print("\nrapatriement du demo_journal.txt vivant (run 23:07) :")
    telecharge(jeton, vifs[0]["id"], "/home/z/my-project/upload/demo_journal_2307.txt")

# 4) demo_journal.txt à la corbeille aussi ? (les 410 o du run 22:45)
old = [f for f in trash if f["name"] == "demo_journal.txt"]
for i, f in enumerate(sorted(old, key=lambda x: x.get("modifiedTime", ""))):
    print(f"\ndemo_journal corbeille #{i + 1} ({f.get('size')} o, "
          f"{f.get('modifiedTime')}) :")
    telecharge(jeton, f["id"],
               f"/home/z/my-project/upload/demo_journal_corbeille_{i}.txt")
