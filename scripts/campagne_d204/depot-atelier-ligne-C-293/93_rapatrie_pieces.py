#!/usr/bin/env python3
"""Rapatrie les pièces de l'atelier — SANS indexation globale :
navigation directe racine → test → dossiers cibles."""
import json
import hashlib
import time
import urllib.request
import urllib.parse
import base64
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

UPLOAD = "/home/z/my-project/upload"
OUT = "/home/z/my-project/work/triade/preuves-depots-maj-2machines/DEPOT-ATELIER-LIGNE-C"
os.makedirs(f"{OUT}/depot-racine", exist_ok=True)
os.makedirs(f"{OUT}/miroir-ancien", exist_ok=True)
FOLDER_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"

with open(f"{UPLOAD}/physichong-4b3b7222b48c.json") as f:
    sa = json.load(f)

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

now = int(time.time())
header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
claims = b64url(json.dumps({
    "iss": sa["client_email"],
    "scope": "https://www.googleapis.com/auth/drive",
    "aud": sa["token_uri"],
    "iat": now, "exp": now + 3600,
}).encode())
signing_input = f"{header}.{claims}".encode()
key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
sig = key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
jwt = f"{header}.{claims}.{b64url(sig)}"

req = urllib.request.Request(sa["token_uri"],
    data=urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    access_token = json.loads(r.read())["access_token"]

def api(url, binary=False):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        return data if binary else json.loads(data)

def children(folder_id):
    items, token = [], ""
    while True:
        url = ("https://www.googleapis.com/drive/v3/files?q="
               + urllib.parse.quote(f"'{folder_id}' in parents and trashed = false")
               + "&fields=" + urllib.parse.quote(
                   "nextPageToken,files(id,name,mimeType,modifiedTime,size)")
               + "&pageSize=1000")
        if token:
            url += "&pageToken=" + token
        res = api(url)
        items.extend(res.get("files", []))
        token = res.get("nextPageToken", "")
        if not token:
            return items

def sub(folder_id, name):
    for it in children(folder_id):
        if it["name"] == name and it["mimeType"] == "application/vnd.google-apps.folder":
            return it
    return None

def telecharge(folder_id, dossier_local, pieces, etiquette):
    print(f"\n{etiquette}")
    mappe = {it["name"]: it for it in children(folder_id)}
    for nom in pieces:
        if nom not in mappe:
            print(f"    [ABSENT] {nom}")
            continue
        it = mappe[nom]
        data = api(f"https://www.googleapis.com/drive/v3/files/{it['id']}?alt=media",
                   binary=True)
        with open(f"{dossier_local}/{nom}", "wb") as f:
            f.write(data)
        h = hashlib.sha256(data).hexdigest()
        mt = it.get("modifiedTime", "")[:19].replace("T", " ")
        print(f"    [OK] {nom}  {len(data)} o  sha256 {h[:16]}…  (modifié {mt})")

PIECES = ["livraisons.csv", "carnet_temps_humain.csv", "defauts.csv",
          "journal-ouverture.txt"]

# racine → test
test = sub(FOLDER_ID, "test")
assert test is not None, "dossier test introuvable"
print(f"[OK] /test  id={test['id']}")

# A. le dépôt nouveau : /test/atelier-campagne-d204-20261114-013520
nouveau = sub(test["id"], "atelier-campagne-d204-20261114-013520")
if nouveau is None:
    print("[ERREUR] l'atelier 013520 n'est pas à la racine du /test")
else:
    telecharge(nouveau["id"], f"{OUT}/depot-racine", PIECES,
               "A. LE DÉPÔT NOUVEAU — /test/atelier-campagne-d204-20261114-013520 :")

# B. le miroir ancien : /test/Nouveau run/test/TRIADE_gui_tous_runs_v1/atelier-…-013520
nr = sub(test["id"], "Nouveau run")
ancien = None
if nr is not None:
    t2 = sub(nr["id"], "test")
    if t2 is not None:
        gui = sub(t2["id"], "TRIADE_gui_tous_runs_v1")
        if gui is not None:
            ancien = sub(gui["id"], "atelier-campagne-d204-20261114-013520")
if ancien is None:
    print("[ERREUR] le miroir ancien (Nouveau run) est introuvable")
else:
    telecharge(ancien["id"], f"{OUT}/miroir-ancien", PIECES,
               "B. LE MIROIR ANCIEN — /test/Nouveau run/…/atelier-…-013520 :")

# C. le gabarit scellé du kit GUI : /test/TRIADE_gui_tous_runs_v1/campagne-d204
gui_root = sub(test["id"], "TRIADE_gui_tous_runs_v1")
if gui_root is not None:
    gab = sub(gui_root["id"], "campagne-d204")
    if gab is not None:
        telecharge(gab["id"], OUT, ["livraisons.csv", "carnet_temps_humain.csv",
                                    "defauts.csv"],
                   "C. LE GABARIT SCELLÉ (le kit du GUI) — pour mémoire :")
