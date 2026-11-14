#!/usr/bin/env python3
"""Re-rapatrie LA VÉRITÉ du miroir Drive après le recyclage du conteneur
(la répétition de l'Entrée 285) : JOURNAL_TRAVAIL.md, worklog.md, et le
bundle courant triade-history.bundle (l'état 290/291)."""
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
    with urllib.request.urlopen(req, timeout=300) as r:
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

svg = sub(FOLDER_ID, "TRIADE-sauvegarde-git")
docs = sub(svg["id"], "docs")
print(f"[OK] miroir docs/ (id={docs['id']})")

cibles = []
journal = next((it for it in children(docs["id"]) if it["name"] == "JOURNAL_TRAVAIL.md"), None)
worklog = next((it for it in children(svg["id"]) if it["name"] == "worklog.md"), None)
bundle = next((it for it in children(svg["id"]) if it["name"] == "triade-history.bundle"), None)

for it, local, etiquette in [
    (journal, f"{OUT}/VERITE-JOURNAL_TRAVAIL.md", "JOURNAL_TRAVAIL.md"),
    (worklog, f"{OUT}/VERITE-worklog.md", "worklog.md"),
]:
    if it is None:
        print(f"[ABSENT] {etiquette}")
        continue
    data = api(f"https://www.googleapis.com/drive/v3/files/{it['id']}?alt=media", binary=True)
    with open(local, "wb") as f:
        f.write(data)
    h = hashlib.sha256(data).hexdigest()
    n = data.count(b"\n")
    print(f"[OK] {etiquette}  {len(data)} o  {n} lignes  sha256 {h[:16]}…  "
          f"(modifié {it.get('modifiedTime','')[:19]})")

if bundle is None:
    print("[ABSENT] triade-history.bundle")
else:
    local = "/home/z/my-project/work/triade-history-VRAI.bundle"
    print(f"[…] triade-history.bundle  {int(bundle.get('size',0))/1024:.0f} Ko — téléchargement…")
    data = api(f"https://www.googleapis.com/drive/v3/files/{bundle['id']}?alt=media", binary=True)
    with open(local, "wb") as f:
        f.write(data)
    md5 = hashlib.md5(data).hexdigest()
    print(f"[OK] bundle  {len(data)} o  md5 {md5}  (modifié {bundle.get('modifiedTime','')[:19]})")
