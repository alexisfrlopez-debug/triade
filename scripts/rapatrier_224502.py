#!/usr/bin/env python3
"""D66 — Rapatriement direct (API Drive v3, sans flux de changements) de la
pièce manquante terrain_20261027_224502.txt + empreintes des demo_journal.txt.

drive_recuperer.py travaille en delta (jeton de changement) : le journal
22:45 a été consommé par la session D65 sans rapatriement. Le fichier est
pourtant présent dans le dossier (vu par files.list direct à 23:16 UTC).
"""
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

UPLOAD = "/home/z/my-project/upload/terrain_jetons.bin"
URL_TOKEN = "https://oauth2.googleapis.com/token"
DOSSIER = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
CIBLE = "terrain_20261027_224502.txt"


def http_json(url, jeton=None, timeout=30):
    req = urllib.request.Request(url)
    if jeton:
        req.add_header("Authorization", "Bearer " + jeton)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


# 1) jeton (annexe — chaîne éprouvée)
data = open(UPLOAD, "rb").read()
champs = [c for c in data.split(b"\x00") if c]
corps = urllib.parse.urlencode({
    "client_id": champs[0].decode(), "client_secret": champs[1].decode(),
    "refresh_token": champs[2].decode(), "grant_type": "refresh_token",
}).encode()
r = urllib.request.urlopen(urllib.request.Request(
    URL_TOKEN, data=corps,
    headers={"Content-Type": "application/x-www-form-urlencoded"}), timeout=30)
jeton = json.load(r)["access_token"]

# 2) listage complet (pas de delta) : id + md5 de chaque candidat
q = urllib.parse.urlencode({
    "q": f"'{DOSSIER}' in parents and trashed = false",
    "fields": "files(id,name,size,modifiedTime)",
    "pageSize": 100})
rep = http_json("https://www.googleapis.com/drive/v3/files?" + q, jeton)
fichiers = rep.get("files", [])
print(f"{len(fichiers)} fichiers dans le dossier test.")

cibles = [f for f in fichiers if f["name"] == CIBLE]
if not cibles:
    print(f"« {CIBLE} » : ABSENT (supprimé entre-temps ?)")
else:
    for c in cibles:
        print(f"candidat : {c['name']} id={c['id']} "
              f"taille={c.get('size')} modifié={c.get('modifiedTime')}")
        req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{c['id']}?alt=media",
            headers={"Authorization": "Bearer " + jeton})
        with urllib.request.urlopen(req, timeout=60) as rr:
            contenu = rr.read()
        dest = f"/home/z/my-project/upload/{CIBLE}"
        if len(cibles) > 1:  # doublons de nom → suffixe par id court
            dest = f"/home/z/my-project/upload/{CIBLE[:-4]}-{c['id'][:8]}.txt"
        open(dest, "wb").write(contenu)
        print(f"  → rapatrié : {dest} ({len(contenu)} o, "
              f"md5 {hashlib.md5(contenu).hexdigest()})")

# 3) empreintes de tous les demo_journal.txt (déduplication)
print("\ndemo_journal.txt présents :")
for f in sorted((x for x in fichiers if x["name"] == "demo_journal.txt"),
                key=lambda x: x.get("modifiedTime", "")):
    print(f"  id={f['id']}  taille={f.get('size')}  "
          f"modifié={f.get('modifiedTime')}")
