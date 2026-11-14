#!/usr/bin/env python3
"""Sonde du coffre /test — où vit l'atelier déposé (la réponse au
« atelier depose dans /test du drive »)."""
import json
import time
import urllib.request
import urllib.parse
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

UPLOAD = "/home/z/my-project/upload"
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
               + "&pageSize=1000&orderBy=" + urllib.parse.quote("folder,name"))
        if token:
            url += "&pageToken=" + token
        res = api(url)
        items.extend(res.get("files", []))
        token = res.get("nextPageToken", "")
        if not token:
            return items

def show(folder_id, depth=0, max_depth=4):
    for it in children(folder_id):
        t = it.get("modifiedTime", "")[:19].replace("T", " ")
        if it["mimeType"] == "application/vnd.google-apps.folder":
            print(f"{'  '*depth}[DIR] {it['name']}  (modifié {t})")
            if depth < max_depth:
                show(it["id"], depth + 1, max_depth)
        else:
            size = int(it.get("size", 0) or 0)
            print(f"{'  '*depth}- {it['name']}  ({size/1024:.1f} Ko, {t})")

root = children(FOLDER_ID)
print("=== RACINE DU COFFRE (", FOLDER_ID[:8], "…) ===")
for it in root:
    t = it.get("modifiedTime", "")[:19].replace("T", " ")
    if it["mimeType"] == "application/vnd.google-apps.folder":
        print(f"[DIR] {it['name']}  (modifié {t})")
    else:
        print(f"- {it['name']}  ({int(it.get('size',0) or 0)/1024:.1f} Ko, {t})")

# le dossier /test
tests = [it for it in root if it["mimeType"] == "application/vnd.google-apps.folder"
         and it["name"].strip().lower() == "test"]
if not tests:
    print("\n[ABSENT] pas de dossier 'test' à la racine")
else:
    print(f"\n=== /test (id={tests[0]['id']}) ===")
    show(tests[0]["id"], depth=0, max_depth=4)
