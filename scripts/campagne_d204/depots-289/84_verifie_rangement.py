#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA VÉRIFICATION de l'état après le recoup 83 : la racine du /test,
les DEUX dépôts à leur place d'archive, les pièces re-téléchargées."""
import base64
import hashlib
import json
import pathlib
import time
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from google.oauth2 import service_account
from googleapiclient.discovery import build

UPLOAD = "/home/z/my-project/upload"
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
API = "https://www.googleapis.com/drive/v3"
RELAI_ID = "1RKV_5dN1qtp_H7A_3kyPBOKIrrpIG8rP"
BAC = pathlib.Path("/home/z/my-project/download")

svc_creds = service_account.Credentials.from_service_account_file(
    f"{UPLOAD}/physichong-4b3b7222b48c.json",
    scopes=["https://www.googleapis.com/auth/drive"])
svc = build("drive", "v3", credentials=svc_creds, cache_discovery=False)
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
req = urllib.request.Request(f"{API}/files/{RELAI_ID}?alt=media",
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
    req = urllib.request.Request(f"{API}/files/{fid}?alt=media",
        headers={"Authorization": f"Bearer {ACCESS}"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()

racine = {c["name"]: c for c in list_children(TEST_ID)}
print("===== LA RACINE DU /test =====")
for n in sorted(racine):
    print(f"  {n}")
attendu = {"Nouveau run", "archives-livraisons", "archives-preuves",
           "LISEZMOI-CORRECTIF-ENCODAGE.txt", "LISEZMOI-GUI-TOUS-RUNS.txt",
           "LISEZMOI-KITS-UNITES-D204.txt", "LISEZMOI-campagne-GUI.txt",
           "LISEZMOI-NETTOYAGE-TEST-20261114.txt",
           "TRIADE-1CLIC-CAMPAGNE-D204-v3.bat",
           "TRIADE_gui_campagne_v1_CORRECTIF-encodage.zip",
           "TRIADE_gui_tous_runs_v1.zip"}
print(f"\n[{'VERT' if set(racine) == attendu else 'ROUGE'}] "
      f"la racine == l'attendu ({len(racine)} entrées)")

archives = {c["name"]: c for c in list_children(racine["archives-livraisons"]["id"])}
u01 = {c["name"]: c for c in list_children(archives["unite-01-loupe-20261114"]["id"])}
print("\n===== /archives-livraisons/unite-01-loupe-20261114/ =====")
for n in sorted(u01):
    print(f"  {n}/")

wc = {c["name"]: c for c in list_children(u01["console-refus-v1-terrain-20261114"]["id"])}
print(f"\n[console-refus] {sorted(wc)}")
kt = {c["name"]: c for c in list_children(wc["kit-unite-loupe-01-C-20261114"]["id"])}
brut = retelecharger(kt["run-console-unite01C.txt"]["id"]) \
    if "run-console-unite01C.txt" in kt else b""
bac_console = (BAC / "preuves-refus-C-v1" / "run-console-unite01C-refus-v1-terrain.txt")
ok_c = brut == bac_console.read_bytes() if brut else False
sha = hashlib.sha256(brut).hexdigest() if brut else "?"
print(f"[{'VERT' if ok_c else 'ROUGE'}] la console du refus à l'archive : "
      f"{len(brut):,} o, sha256 {sha[:16]}… == le bac")
dll = retelecharger(kt["loupe-01-c.dll"]["id"])
ok_d = hashlib.sha256(dll).hexdigest().startswith("85b34ed4c243e977")
print(f"[{'VERT' if ok_d else 'ROUGE'}] loupe-01-c.dll à l'archive : 85b34ed4… "
      f"({'tenu' if ok_d else 'ROMPU'})")

wa = {c["name"]: c for c in list_children(u01["atelier-retour-ligne-C-20261114"]["id"])}
print(f"\n[atelier-retour] {sorted(wa)}")
wa_test = {c["name"]: c for c in list_children(wa["test"]["id"])}
wa_gui = {c["name"]: c for c in list_children(wa_test["TRIADE_gui_tous_runs_v1"]["id"])}
wa_at = {c["name"]: c for c in list_children(wa_gui["atelier-campagne-d204-20261114-013520"]["id"])}
livr_arch = retelecharger(wa_at["livraisons.csv"]["id"])
ok_l = livr_arch == (BAC / "atelier-retour-C-20261114" / "livraisons.csv").read_bytes()
print(f"[{'VERT' if ok_l else 'ROUGE'}] livraisons.csv à l'archive == le bac")
etat_arch = retelecharger(wa_gui["etat-tous-runs.json"]["id"])
ok_e = etat_arch == (BAC / "atelier-retour-C-20261114" / "etat-tous-runs.json").read_bytes()
print(f"[{'VERT' if ok_e else 'ROUGE'}] etat-tous-runs.json à l'archive == le bac")
print(f"\n[recoup] le kit terrain porte {len(kt)} pièces ; "
      f"l'archive unité-01 porte {len(u01)} entrées")
