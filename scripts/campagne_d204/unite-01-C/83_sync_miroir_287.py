#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA SYNCHRONISATION à L'ÉTAT 287 : le push GitHub (au jeton ghp_
du /tokens — jamais imprimé), le bundle D141 (le courant 286-db5b02f versé à
archives-bundles/), le bundle courant rafraîchi au nouveau commit, les trois
textes PATCHés au miroir — chaque geste recoupé par re-téléchargement."""
import base64
import hashlib
import json
import pathlib
import re
import subprocess
import time
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
WORK = pathlib.Path("/home/z/my-project/work")
REPO = WORK / "triade"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"
RELAI_ID = "1RKV_5dN1qtp_H7A_3kyPBOKIrrpIG8rP"

# ---- 0) le jeton git du /tokens (jamais imprimé) ---------------------------
svc_creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"])
svc = build("drive", "v3", credentials=svc_creds, cache_discovery=False)
tokens_dir = svc.files().list(
    q=f"'{ROOT}' in parents and trashed=false and name='Tokens'",
    fields="files(id,name)").execute()["files"][0]
jeton_fichier = svc.files().list(
    q=f"'{tokens_dir['id']}' in parents and trashed=false and name='token_git.txt'",
    fields="files(id,name)").execute()["files"][0]
m = re.search(rb"(ghp_[A-Za-z0-9]+)",
              svc.files().get_media(fileId=jeton_fichier["id"]).execute())
assert m, "jeton ghp_ introuvable au /tokens"
JETON_GIT = m.group(1).decode()
print("[jeton] le ghp_ du /tokens est lu (jamais imprimé)")

# ---- 1) le push GitHub -------------------------------------------------------
sha_local = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                           capture_output=True, text=True).stdout.strip()
url_push = f"https://x-access-token:{JETON_GIT}@github.com/alexisfrlopez-debug/triade.git"
r = subprocess.run(["git", "push", url_push, "main"], cwd=REPO,
                   capture_output=True, text=True)
sortie = re.sub(r"ghp_[A-Za-z0-9]+", "ghp_…", (r.stdout + r.stderr))
print(f"[push] code {r.returncode}")
print("  " + sortie.strip().replace("\n", "\n  ")[:600])
if r.returncode != 0:
    print("[!] LE PUSH A REFUSÉ — l'écart sera nommé (le miroir Drive demeure la référence)")
    raise SystemExit(1)

req = urllib.request.Request(
    "https://api.github.com/repos/alexisfrlopez-debug/triade/commits?per_page=1",
    headers={"Authorization": f"Bearer {JETON_GIT}",
             "Accept": "application/vnd.github+json",
             "User-Agent": "triade-labo"})
with urllib.request.urlopen(req, timeout=30) as resp:
    distant = json.loads(resp.read())[0]["sha"]
ok_push = distant == sha_local
print(f"[{'VERT' if ok_push else 'ROUGE'}] GitHub main @ {distant[:9]} == le local {sha_local[:9]}")

# ---- 2) le relais OAuth du coffre (écriture) ---------------------------------
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
with urllib.request.urlopen(req, timeout=30) as r2:
    token_sa = json.loads(r2.read())["access_token"]
req = urllib.request.Request(
    f"{API}/files/{RELAI_ID}?alt=media",
    headers={"Authorization": f"Bearer {token_sa}"})
with urllib.request.urlopen(req, timeout=30) as r2:
    relais = json.loads(r2.read())
req = urllib.request.Request(
    relais["token_uri"],
    data=urllib.parse.urlencode({
        "client_id": relais["client_id"],
        "client_secret": relais["client_secret"],
        "refresh_token": relais["refresh_token"],
        "grant_type": "refresh_token"}).encode(), method="POST")
with urllib.request.urlopen(req, timeout=30) as r2:
    ACCESS = json.loads(r2.read())["access_token"]
print("[jeton] le relais OAuth du coffre est rafraîchi")

def api(url, data=None, method="GET", headers=None):
    h = {"Authorization": f"Bearer {ACCESS}"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=600) as r2:
        corps = r2.read()
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
    with urllib.request.urlopen(req, timeout=600) as r2:
        return r2.read()

def patch_media(fid, contenu):
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

# ---- 3) les cibles du miroir --------------------------------------------------
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

# ---- 4) D141 : le courant 286-db5b02f archivé versionné -----------------------
bundle_d141 = (WORK / "triade-history-286-db5b02f.bundle").read_bytes()
sha_d141 = hashlib.sha256(bundle_d141).hexdigest()
archives = n1["archives-bundles"]
deja = [c for c in list_children(archives["id"])
        if c["name"] == "triade-history-286-db5b02f.bundle"]
if deja:
    fid = deja[0]["id"]
    patch_media(fid, bundle_d141)
else:
    fid = uploader("triade-history-286-db5b02f.bundle", bundle_d141,
                   archives["id"])
ok = hashlib.sha256(retelecharger(fid)).hexdigest() == sha_d141
print(f"[{'VERT' if ok else 'ROUGE'}] D141 triade-history-286-db5b02f.bundle "
      f"({len(bundle_d141):,} o, sha256 {sha_d141[:16]}…) versé à archives-bundles/")

# ---- 5) le bundle courant rafraîchi au nouveau commit --------------------------
nouveau = WORK / "triade-history-287.bundle"
if nouveau.exists():
    nouveau.unlink()
r = subprocess.run(["git", "bundle", "create", str(nouveau), "--all"],
                   cwd=REPO, capture_output=True, text=True)
assert r.returncode == 0, r.stderr
contenu_bundle = nouveau.read_bytes()
sha_bundle = hashlib.sha256(contenu_bundle).hexdigest()
patch_media(cibles["triade-history.bundle"], contenu_bundle)
ok_b = hashlib.sha256(retelecharger(
    cibles["triade-history.bundle"])).hexdigest() == sha_bundle
print(f"[{'VERT' if ok_b else 'ROUGE'}] triade-history.bundle rafraîchi "
      f"({len(contenu_bundle):,} o, sha256 {sha_bundle[:16]}…, "
      f"l'état 287-{sha_local[:7]})")

# ---- 6) les trois textes PATCHés ------------------------------------------------
FICHIERS = {
    "worklog.md": REPO / "worklog.md",
    "docs/JOURNAL_TRAVAIL.md": REPO / "docs" / "JOURNAL_TRAVAIL.md",
    "OU-TROUVER-LES-LIVRABLES.md": REPO / "OU-TROUVER-LES-LIVRABLES.md",
}
tout_ok = ok and ok_b and ok_push
for chemin, local in FICHIERS.items():
    contenu = local.read_bytes()
    patch_media(cibles[chemin], contenu)
    distant_txt = retelecharger(cibles[chemin])
    vert = distant_txt == contenu
    tout_ok &= vert
    print(f"[{'VERT' if vert else 'ROUGE'}] {chemin} PATCHé "
          f"({len(contenu):,} o) — "
          f"{'identique octet pour octet' if vert else 'DIVERGE !'}")

print("\n" + ("LA SYNCHRONISATION à L'ÉTAT 287 EST RECOUPÉE VERT — le push GitHub, "
              "le bundle D141, le courant et les trois textes" if tout_ok
              else "ÉCHEC — un recoup a rougi"))
