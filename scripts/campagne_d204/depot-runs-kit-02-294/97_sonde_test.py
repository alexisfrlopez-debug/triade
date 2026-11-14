#!/usr/bin/env python3
"""Sonde du /test — QUELCHOSE de neuf depuis l'état 293 (bfb20e0, 14/11
16:23:44Z) ? L'annonce du développeur : « kit 02 C et T dans /test du
drive ». État de la racine, des kits loupe-02, et de TOUT ce qui bouge
après 16:23:44Z le 14/11."""
import json
import time
import urllib.request
import urllib.parse
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

UPLOAD = "/home/z/my-project/upload"
FOLDER_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
SEUIL = "2026-11-14T16:23:44"  # l'instant du commit 293

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
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        return data if binary else json.loads(data)

def children(folder_id):
    items, token = [], ""
    while True:
        url = ("https://www.googleapis.com/drive/v3/files?q="
               + urllib.parse.quote(f"'{folder_id}' in parents and trashed = false")
               + "&fields=" + urllib.parse.quote(
                   "nextPageToken,files(id,name,mimeType,modifiedTime,createdTime,size,md5Checksum)")
               + "&pageSize=1000")
        if token:
            url += "&pageToken=" + token
        res = api(url)
        items.extend(res.get("files", []))
        token = res.get("nextTokenToken", res.get("nextPageToken", ""))
        if not token:
            return items

def sub(folder_id, name):
    for it in children(folder_id):
        if it["name"] == name and it["mimeType"] == "application/vnd.google-apps.folder":
            return it
    return None

def aff(it, pfx=""):
    t = it.get("modifiedTime", "")[:19].replace("T", " ")
    c = it.get("createdTime", "")[:19].replace("T", " ")
    if it["mimeType"] == "application/vnd.google-apps.folder":
        print(f"{pfx}[DIR] {it['name']}  (créé {c}, modifié {t})")
    else:
        print(f"{pfx}- {it['name']}  ({int(it.get('size',0) or 0)} o, créé {c}, modifié {t})")

test = sub(FOLDER_ID, "test")
print(f"=== /test (id={test['id']}) — RACINE, {len(children(test['id']))} entrées ===")
racine = sorted(children(test["id"]),
                key=lambda x: (x["mimeType"] != "application/vnd.google-apps.folder", x["name"]))
for it in racine:
    aff(it, "  ")

# ce qui est NOUVEAU ou TOUCHÉ après le commit 293
print(f"\n=== TOUT ce qui porte created/modified > {SEUIL} (récursion 5 niveaux depuis /test) ===")
def recents(folder_id, chemin, depth=0):
    for it in children(folder_id):
        mt = it.get("modifiedTime", "")[:19]
        ct = it.get("createdTime", "")[:19]
        if mt > SEUIL or ct > SEUIL:
            print(f"  {chemin}/{it['name']}  "
                  f"(créé {ct}, modifié {mt}, "
                  f"{'DOSSIER' if it['mimeType']=='application/vnd.google-apps.folder' else str(it.get('size','?'))+' o'})")
        if it["mimeType"] == "application/vnd.google-apps.folder" and depth < 5:
            recents(it["id"], f"{chemin}/{it['name']}", depth + 1)
recents(test["id"], "/test")

# les kits loupe-02 s'ils sont encore à la racine
for nom in ["kit-unite-loupe-02-T-20261114", "kit-unite-loupe-02-C-20261114"]:
    k = sub(test["id"], nom)
    if k is None:
        print(f"\n[kit] {nom} : ABSENT de la racine du /test")
    else:
        print(f"\n[kit] {nom} (id={k['id']}, créé {k.get('createdTime','')[:19]}, "
              f"modifié {k.get('modifiedTime','')[:19]}) :")
        for it in sorted(children(k["id"]), key=lambda x: x["name"]):
            aff(it, "    ")

# le bac du miroir (scripts/campagne_d204/unite-02-*) n'est pas concerné :
# on vérifie juste que l'atelier rangé n'a pas bougé
arch = sub(test["id"], "archives-livraisons")
if arch:
    u1 = sub(arch["id"], "unite-01-loupe-20261114")
    if u1:
        at = sub(u1["id"], "atelier-campagne-d204-20261114-013520")
        print(f"\n[atelier] rangé à archives-livraisons/unite-01-loupe-20261114/…-013520 : "
              f"{'PRÉSENT' if at else 'ABSENT'} (modifié {u1.get('modifiedTime','')[:19]} pour unite-01)")
