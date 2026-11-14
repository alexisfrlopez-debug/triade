#!/usr/bin/env python3
"""TRIADE — compléments de la sonde 104 : les SIX pièces restantes du kit v2,
le scénario v1 (diff v1->v2), le témoin v1 archivé (vecteurs à comparer)."""
import json
import time
import hashlib
import urllib.request
import urllib.parse
import pathlib

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

UPLOAD = "/home/z/my-project/upload"
DEST = pathlib.Path("/home/z/my-project/work/test_mirror")

with open(f"{UPLOAD}/physichong-4b3b7222b48c.json") as f:
    sa = json.load(f)

def b64url(d): return base64.urlsafe_b64encode(d).rstrip(b"=").decode()
now = int(time.time())
header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
claims = b64url(json.dumps({"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/drive",
                            "aud": sa["token_uri"], "iat": now, "exp": now + 3600}).encode())
si = f"{header}.{claims}".encode()
key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
sig = key.sign(si, padding.PKCS1v15(), hashes.SHA256())
jwt = f"{header}.{claims}.{b64url(sig)}"
req = urllib.request.Request(sa["token_uri"], data=urllib.parse.urlencode(
    {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    tok = json.loads(r.read())["access_token"]

def api(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def list_children(fid):
    out, tk = [], None
    while True:
        url = (f"https://www.googleapis.com/drive/v3/files?q=%27{fid}%27+in+parents+and+trashed%3Dfalse"
               f"&fields=nextPageToken,files(id,name,mimeType,size,createdTime,modifiedTime)&pageSize=200&orderBy=name")
        if tk: url += f"&pageToken={tk}"
        d = api(url); out.extend(d.get("files", [])); tk = d.get("nextPageToken")
        if not tk: return out

def dl(file_id, path):
    req = urllib.request.Request(f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media",
                                 headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    p = DEST / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return data

top = list_children("105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp")
test = next(i for i in top if i["name"].strip().lower() == "test")
tl = list_children(test["id"])

# 1) les six pièces restantes du kit v2
v2 = next(d for d in tl if d["name"] == "kit-unite-loupe-02-T-20261114-v2")
for it in list_children(v2["id"]):
    p = DEST / "kit-T-v2" / it["name"]
    if not p.exists():
        data = dl(it["id"], f"kit-T-v2/{it['name']}")
        print(f"[DL] {it['name']} — {len(data)} o")

# 2) le scénario v1 (kit T v1 à la racine du /test)
v1 = next(d for d in tl if d["name"] == "kit-unite-loupe-02-T-20261114")
for it in list_children(v1["id"]):
    if it["name"] == "scenario-unite02.py":
        data = dl(it["id"], "kit-T-v1/scenario-unite02.py")
        print(f"[DL v1] scenario-unite02.py — {len(data)} o "
              f"(sha256 {hashlib.sha256(data).hexdigest()[:8]}…)")

# 3) le témoin v1 + la console v1 aux archives
arch = next(d for d in tl if d["name"] == "archives-livraisons")
u02 = next(d for d in list_children(arch["id"]) if d["name"] == "unite-02-loupe-20261114")
for kit in list_children(u02["id"]):
    print(f"\n[archives] {kit['name']}/")
    for it in list_children(kit["id"]):
        t = it.get("modifiedTime", "")[:19].replace("T", " ")
        if it["mimeType"] == "application/vnd.google-apps.folder":
            print(f"   [DIR] {it['name']}  (modifié {t})")
            for sub in list_children(it["id"]):
                print(f"      - {sub['name']}  ({int(sub.get('size',0) or 0)} o, modifié {sub.get('modifiedTime','')[:19]})")
                if "temoin-unite02" in sub["name"] or "console" in sub["name"]:
                    data = dl(sub["id"], f"archives-u02/{kit['name']}/{it['name']}/{sub['name']}")
                    print(f"           [DL] {len(data)} o -> archives-u02/…/{sub['name']}")
        else:
            print(f"   - {it['name']}  ({int(it.get('size',0) or 0)} o, modifié {t})")
