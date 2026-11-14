#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA SYNCHRONISATION DU MIROIR DRIVE à l'état 284 :
  1. le bundle D141 (le courant 283-7678421) versé à archives-bundles/ ;
  2. le bundle courant triade-history.bundle rafraîchi au commit b6b8469
     (PATCH en place — aucun doublon) ;
  3. worklog.md, docs/JOURNAL_TRAVAIL.md, OU-TROUVER-LES-LIVRABLES.md
     PATCHés au contenu du dépôt (l'état 284) ;
  4. chaque geste recoupé par re-téléchargement."""
import base64
import hashlib
import json
import pathlib
import subprocess
import time
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

UPLOAD = "/home/z/my-project/upload"
WORK = pathlib.Path("/home/z/my-project/work")
REPO = WORK / "triade"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"
RELAI_ID = "1RKV_5dN1qtp_H7A_3kyPBOKIrrpIG8rP"

with open(f"{UPLOAD}/physichong-4b3b7222b48c.json") as f:
    sa = json.load(f)


def b64url(d):
    return base64.urlsafe_b64encode(d).rstrip(b"=").decode()


now = int(time.time())
header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
claims = b64url(json.dumps(
    {"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/drive",
     "aud": sa["token_uri"], "iat": now, "exp": now + 3600}).encode())
si = f"{header}.{claims}".encode()
key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
jwt = f"{header}.{claims}.{b64url(key.sign(si, padding.PKCS1v15(), hashes.SHA256()))}"
req = urllib.request.Request(
    sa["token_uri"],
    data=urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    token_sa = json.loads(r.read())["access_token"]
req = urllib.request.Request(
    f"{API}/files/{RELAI_ID}?alt=media",
    headers={"Authorization": f"Bearer {token_sa}"})
with urllib.request.urlopen(req, timeout=30) as r:
    relais = json.loads(r.read())
req = urllib.request.Request(
    relais["token_uri"],
    data=urllib.parse.urlencode({
        "client_id": relais["client_id"],
        "client_secret": relais["client_secret"],
        "refresh_token": relais["refresh_token"],
        "grant_type": "refresh_token"}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    ACCESS = json.loads(r.read())["access_token"]
print("[jeton] le relais OAuth du coffre est rafraîchi")


def api(url, data=None, method="GET", headers=None):
    h = {"Authorization": f"Bearer {ACCESS}"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=600) as r:
        corps = r.read()
        return json.loads(corps) if corps else {}


def list_children(fid):
    out, token = [], None
    while True:
        params = {"q": f"'{fid}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,size)"}
        if token:
            params["pageToken"] = token
        obj = api(API + "/files?" + urllib.parse.urlencode(params))
        out += obj.get("files", [])
        token = obj.get("nextPageToken")
        if not token:
            return out


def retelecharger(fid):
    req = urllib.request.Request(
        f"{API}/files/{fid}?alt=media",
        headers={"Authorization": f"Bearer {ACCESS}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()


def patch_media(fid, contenu, nom):
    """remplace le contenu du fichier Drive EN PLACE (aucun doublon)"""
    api(f"https://www.googleapis.com/upload/drive/v3/files/{fid}"
        f"?uploadType=media", data=contenu, method="PATCH",
        headers={"Content-Type": "application/octet-stream"})


def uploader(nom, contenu, parent):
    limite = "trk8c2f1a3"
    metadonnees = json.dumps({"name": nom, "parents": [parent]})
    corps = (f"--{limite}\r\n"
             "Content-Type: application/json; charset=UTF-8\r\n\r\n"
             f"{metadonnees}\r\n"
             f"--{limite}\r\n"
             "Content-Type: application/octet-stream\r\n\r\n").encode() \
        + contenu + f"\r\n--{limite}--".encode()
    res = api("https://www.googleapis.com/upload/drive/v3/files"
              "?uploadType=multipart&fields=id,name",
              data=corps, method="POST",
              headers={"Content-Type":
                       f"multipart/related; boundary={limite}"})
    return res["id"]


# --- où vivent les pièces au miroir ---------------------------------------
racine = {c["name"]: c for c in list_children(ROOT)}
miroir = racine["TRIADE-sauvegarde-git"]
n1 = {c["name"]: c for c in list_children(miroir["id"])}
docs = {c["name"]: c for c in list_children(n1["docs"]["id"])}
cibles = {
    "worklog.md": n1["worklog.md"]["id"],
    "docs/JOURNAL_TRAVAIL.md": docs["JOURNAL_TRAVAIL.md"]["id"],
    "OU-TROUVER-LES-LIVRABLES.md": n1["OU-TROUVER-LES-LIVRABLES.md"]["id"],
    "triade-history.bundle": n1["triade-history.bundle"]["id"],
}
print("[miroir] les cibles trouvées")

# --- 1. le bundle D141 (le courant 283) ------------------------------------
bundle_d141 = (WORK / "triade-history-283-7678421.bundle").read_bytes()
sha_d141 = hashlib.sha256(bundle_d141).hexdigest()
archives = n1["archives-bundles"]
deja = [c for c in list_children(archives["id"])
        if c["name"] == "triade-history-283-7678421.bundle"]
if deja:
    fid = deja[0]["id"]
    patch_media(fid, bundle_d141, "bundle D141")
else:
    fid = uploader("triade-history-283-7678421.bundle", bundle_d141,
                   archives["id"])
ok = hashlib.sha256(retelecharger(fid)).hexdigest() == sha_d141
print(f"[{'VERT' if ok else 'ROUGE'}] D141 triade-history-283-7678421"
      f".bundle ({len(bundle_d141):,} o, sha256 {sha_d141[:16]}…) "
      f"versé à archives-bundles/")

# --- 2. le bundle courant rafraîchi au commit b6b8469 -----------------------
nouveau_bundle = WORK / "triade-history-284.bundle"
if nouveau_bundle.exists():
    nouveau_bundle.unlink()
r = subprocess.run(["git", "bundle", "create", str(nouveau_bundle), "--all"],
                   cwd=REPO, capture_output=True, text=True)
assert r.returncode == 0, r.stderr
contenu_bundle = nouveau_bundle.read_bytes()
sha_bundle = hashlib.sha256(contenu_bundle).hexdigest()
patch_media(cibles["triade-history.bundle"], contenu_bundle,
            "triade-history.bundle")
ok_b = hashlib.sha256(retelecharger(
    cibles["triade-history.bundle"])).hexdigest() == sha_bundle
print(f"[{'VERT' if ok_b else 'ROUGE'}] triade-history.bundle rafraîchi "
      f"({len(contenu_bundle):,} o, sha256 {sha_bundle[:16]}…, "
      f"l'état 284-b6b8469)")

# --- 3. les trois fichiers du journal PATCHés -------------------------------
FICHIERS = {
    "worklog.md": REPO / "worklog.md",
    "docs/JOURNAL_TRAVAIL.md": REPO / "docs" / "JOURNAL_TRAVAIL.md",
    "OU-TROUVER-LES-LIVRABLES.md": REPO / "OU-TROUVER-LES-LIVRABLES.md",
}
tout_ok = ok and ok_b
for chemin, local in FICHIERS.items():
    contenu = local.read_bytes()
    patch_media(cibles[chemin], contenu, chemin)
    distant = retelecharger(cibles[chemin])
    vert = distant == contenu
    tout_ok &= vert
    print(f"[{'VERT' if vert else 'ROUGE'}] {chemin} PATCHé "
          f"({len(contenu):,} o) — "
          f"{'identique octet pour octet' if vert else 'DIVERGE !'}")

print("\n" + ("MIROIR SYNCHRONISÉ À L'ÉTAT 284 — recoupé par "
              "re-téléchargement" if tout_ok else "ÉCHEC — un recoup a rougi"))
