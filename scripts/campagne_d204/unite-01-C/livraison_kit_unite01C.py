#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livraison_kit_unite01C.py — LA LIVRAISON DU KIT DE L'UNITÉ 1 × BRAS C
au coffre :
  1. /test/kit-unite-loupe-01-C-20261114/ — les 12 fichiers (11 pièces +
     le zip), via le relais OAuth du coffre ;
  2. le bac du miroir TRIADE-sauvegarde-git/download/
     kit_unite_loupe_01_C/ — les mêmes 12 fichiers ;
  3. CHAQUE dépôt recoupé par re-téléchargement (sha256).
Le résumé (ids, empreintes) est gravé à work/livraison_kit_unite01C.json
pour la consignation."""
import base64
import hashlib
import json
import mimetypes
import pathlib
import time
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

UPLOAD = "/home/z/my-project/upload"
ROOT = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"
RELAI_ID = "1RKV_5dN1qtp_H7A_3kyPBOKIrrpIG8rP"
KIT = pathlib.Path("/home/z/my-project/download/kit_unite_loupe_01_C"
                   "/kit-unite-loupe-01-C-20261114")

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

# le relais OAuth du coffre (le compte propriétaire)
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
print("[jeton] le relais OAuth du coffre est rafraîchi (compte propriétaire)")


def api(url, data=None, method="GET", headers=None):
    h = {"Authorization": f"Bearer {ACCESS}"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    for essai in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                corps = r.read()
                return json.loads(corps) if corps else {}
        except Exception as e:
            if essai == 2:
                raise
            print(f"  [retry {essai + 1}] {e}")
            time.sleep(3)


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


def creer_dossier(nom, parent):
    res = api(API + "/files", data=json.dumps(
        {"name": nom, "mimeType": "application/vnd.google-apps.folder",
         "parents": [parent]}).encode(), method="POST",
        headers={"Content-Type": "application/json; charset=UTF-8"})
    return res["id"]


def uploader(chemin: pathlib.Path, nom: str, parent: str) -> str:
    limite = "trk8c2f1a3"
    contenu = chemin.read_bytes()
    mime = mimetypes.guess_type(str(chemin))[0] or "application/octet-stream"
    metadonnees = json.dumps({"name": nom, "parents": [parent]})
    corps = (f"--{limite}\r\n"
             "Content-Type: application/json; charset=UTF-8\r\n\r\n"
             f"{metadonnees}\r\n"
             f"--{limite}\r\n"
             f"Content-Type: {mime}\r\n\r\n").encode() + contenu + \
            f"\r\n--{limite}--".encode()
    res = api("https://www.googleapis.com/upload/drive/v3/files"
              "?uploadType=multipart&fields=id,name",
              data=corps, method="POST",
              headers={"Content-Type":
                       f"multipart/related; boundary={limite}"})
    return res["id"]


def retelecharger(fid):
    req = urllib.request.Request(
        f"{API}/files/{fid}?alt=media",
        headers={"Authorization": f"Bearer {ACCESS}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


PIECES = ["EMPREINTES-KIT-UNITE-01-C.txt", "LANCEUR-UNITE-01-C.bat",
          "LISEZMOI-KIT-UNITE-01-C.txt", "kit-unite-loupe-01-C-20261114.zip",
          "loupe-01-c.c", "loupe-01-c.def", "loupe-01-c.dll",
          "scenario-unite01C.py", "temoin-1.bin", "temoin-384.bin",
          "temoin-3f.bin", "vide.bin"]
resume = {"pieces": {}, "dossiers": {}}

# --- 1. le dossier du kit au /test ---------------------------------------
racine = {c["name"]: c for c in list_children(ROOT)}
test = racine["test"]
deja = [c for c in list_children(test["id"])
        if c["name"] == "kit-unite-loupe-01-C-20261114"]
if deja:
    id_kit = deja[0]["id"]
    print(f"[dossier] kit-unite-loupe-01-C-20261114 existait déjà ({id_kit})")
else:
    id_kit = creer_dossier("kit-unite-loupe-01-C-20261114", test["id"])
    print(f"[dossier] kit-unite-loupe-01-C-20261114 créé au /test ({id_kit})")
resume["dossiers"]["test"] = id_kit

tout_ok = True
for nom in PIECES:
    attendu = hashlib.sha256((KIT / nom).read_bytes()).hexdigest()
    fid = uploader(KIT / nom, nom, id_kit)
    obtenu = hashlib.sha256(retelecharger(fid)).hexdigest()
    ok = obtenu == attendu
    tout_ok &= ok
    print(f"  [{'VERT' if ok else 'ROUGE'}] /test/{nom} "
          f"({(KIT / nom).stat().st_size} o, {attendu[:16]}…)")
    resume["pieces"][nom] = {"id": fid, "sha256": attendu,
                             "taille": (KIT / nom).stat().st_size}

# --- 2. le bac du miroir ---------------------------------------------------
miroir = racine["TRIADE-sauvegarde-git"]
n1 = {c["name"]: c for c in list_children(miroir["id"])}
download = n1["download"]
bac_deja = [c for c in list_children(download["id"])
            if c["name"] == "kit_unite_loupe_01_C"]
if bac_deja:
    id_bac = bac_deja[0]["id"]
else:
    id_bac = creer_dossier("kit_unite_loupe_01_C", download["id"])
print(f"[bac] miroir download/kit_unite_loupe_01_C ({id_bac})")
resume["dossiers"]["miroir_bac"] = id_bac

for nom in PIECES:
    attendu = hashlib.sha256((KIT / nom).read_bytes()).hexdigest()
    fid = uploader(KIT / nom, nom, id_bac)
    obtenu = hashlib.sha256(retelecharger(fid)).hexdigest()
    ok = obtenu == attendu
    tout_ok &= ok
    print(f"  [{'VERT' if ok else 'ROUGE'}] miroir/{nom}")
    resume["pieces"][nom]["id_miroir"] = fid

resume["tout_recoupe"] = tout_ok
pathlib.Path("/home/z/my-project/work/livraison_kit_unite01C.json").write_text(
    json.dumps(resume, ensure_ascii=False, indent=1))
print("\n" + ("LIVRAISON RECOUPÉE VERT — le kit du bras C vit au coffre "
              "/test et au bac du miroir" if tout_ok else
              "ÉCHEC — un recoup a rougi"))
