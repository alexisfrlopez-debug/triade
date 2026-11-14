#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livraison_kits_unite02.py — LA LIVRAISON DES DEUX KITS DE L'UNITÉ 2 au
coffre /test (loupe-02 LIRE, la campagne D204) : les DEUX dossiers datés
montés pièce par pièce, chaque pièce recoupée par RE-TÉLÉCHARGEMENT
byte-byte (le double téléchargement, la règle du coffre), la carte
LISEZMOI-KITS-UNITES-D204.txt portée à jour (la ligne de l'unité 2) et
re-téléchargée identique."""
import base64
import hashlib
import json
import os
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
CAMP = pathlib.Path("/home/z/my-project/work/triade/scripts/campagne_d204")

# ---- 0) le relais OAuth du coffre (écriture) ----------------------------------
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
                  "fields": "nextPageToken,files(id,name,mimeType)"}
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

def trouver_ou_creer(nom, parent):
    for c in list_children(parent):
        if c["name"] == nom:
            return c["id"], False
    res = api(API + "/files", data=json.dumps(
        {"name": nom, "mimeType": "application/vnd.google-apps.folder",
         "parents": [parent]}).encode(), method="POST",
        headers={"Content-Type": "application/json; charset=UTF-8"})
    return res["id"], True

def patch_media(fid, contenu):
    api(f"https://www.googleapis.com/upload/drive/v3/files/{fid}"
        f"?uploadType=media", data=contenu, method="PATCH",
        headers={"Content-Type": "application/octet-stream"})

# ---- 1) les DEUX kits montés, chaque pièce recoupée ----------------------------
verts = 0
for bras, dossier in (("T", "kit-unite-loupe-02-T-20261114"),
                      ("C", "kit-unite-loupe-02-C-20261114")):
    source = CAMP / f"unite-02-{bras}" / "kit"
    fid_dossier, neuf = trouver_ou_creer(dossier, TEST_ID)
    print(f"[kit {bras}] /test/{dossier}/ {'créé' if neuf else 'trouvé'}")
    for nom in sorted(os.listdir(source)):
        contenu = (source / nom).read_bytes()
        fid = uploader(nom, contenu, fid_dossier)
        a, b = retelecharger(fid), retelecharger(fid)
        ok = a == b == contenu
        verts += ok
        print(f"[{'VERT' if ok else 'ROUGE'}] {dossier}/{nom} "
              f"({len(contenu):,} o, sha256 "
              f"{hashlib.sha256(contenu).hexdigest()[:16]}…) — "
              f"deux téléchargements == l'original")
        assert ok, nom
    # la gravure relue du coffre : les DIX empreintes du kit
    gravure = retelecharger(
        [c for c in list_children(fid_dossier)
         if c["name"].startswith("EMPREINTES")][0]["id"]).decode("utf-8-sig")
    attends = {}
    for ligne in gravure.splitlines():
        p = ligne.split()
        if len(p) == 2 and len(p[0]) == 64:
            attends[p[1]] = p[0]
    vg = 0
    for nom, h in attends.items():
        brut = retelecharger(
            [c for c in list_children(fid_dossier)
             if c["name"] == nom][0]["id"])
        vg += hashlib.sha256(brut).hexdigest() == h
    print(f"[gravure {bras}] {vg}/{len(attends)} pièces du coffre == "
          f"l'empreinte gravée")
    assert vg == len(attends)
print(f"\n[livraison] {verts} pièces montées et recoupées byte-byte")

# ---- 2) la carte LISEZMOI-KITS-UNITES-D204.txt portée à jour --------------------
racine = {c["name"]: c for c in list_children(TEST_ID)}
carte_id = racine["LISEZMOI-KITS-UNITES-D204.txt"]["id"]
carte = retelecharger(carte_id).decode("utf-8-sig")
NOTE = """

=== L'UNITÉ 2 LIVRÉE — LOUPE-02 LIRE, AUX DEUX BRAS — le 14/11/2026 (l'Entrée 290) ===
La DEUXIÈME tâche contrôlée du plan a78caf8c… (loupe-02 LIRE : la fenêtre d'octets au tampon de session, bornée par la taille réelle — la double borne — puis LE RECOUVREMENT du journal d'édition : l'écrit survit au défilement).
LE BRAS T : kit-unite-loupe-02-T-20261114/ — la pièce loupe.exe (127 488 o, 98354ff6…) : le build du plan où le slot loupe-02 (RVA 0x4240) porte LA NOTATION DE CAMPAGNE (292 o, 79 instructions, écrite à la main — trois fautes nommées en route : l'adressage à deux bases, le débordement du slot 325 > 320, la chute de boucle) ; les DIX-SEPT autres blocs scellés — loupe-01 scellé APPELLE la notation à chaque naissance de session ; la cristallisation DIX rebuilds identiques ; l'oracle du bloc 22 VERT 0 ROUGE (2 032 décalages, le scellé proxy.exe compris).
LE BRAS C : kit-unite-loupe-02-C-20261114/ — la pièce loupe-02-c.dll (95 413 o, 925cd019…) : le source écrit par l'agent (loupe_02_lire neuve + le bloc session repris TEL QUEL du kit 01 — l'écart nommé : sa première fenêtre est lue INLINE), compilée gcc -O2 croisée (la commande consignée) ; le contrat entier rejoué au POSIX 20 VERT 0 ROUGE ; les contrôles binaires 18 VERT 0 ROUGE (SetFilePointerEx PRÉSENTE aux imports : l'écart nommé du kit 01 n'existe plus).
LE GESTE (l'ordre de jeu inchangé) : 1·KIT choisir le dossier → 2·RUN lancer le LANCEUR → 3·TÉMOIN dater, signer de la main, renvoyer preuves-unite02[/ C]/ ENTIER au /test → onglets 4-7 (carnet, livraison, défauts, chrono). LA SUITE : loupe-05 sha256, aux deux bras.
"""
if "L'UNITÉ 2 LIVRÉE" not in carte:
    carte = carte.rstrip("\n") + "\n" + NOTE
patch_media(carte_id, carte.encode("utf-8-sig"))
ok_carte = retelecharger(carte_id) == carte.encode("utf-8-sig")
print(f"[{'VERT' if ok_carte else 'ROUGE'}] la carte LISEZMOI-KITS-UNITES-"
      f"D204.txt portée à jour ({len(carte.encode('utf-8-sig')):,} o) — "
      f"{'identique au re-téléchargement' if ok_carte else 'DIVERGE'}")
assert ok_carte

final = sorted(c["name"] for c in list_children(TEST_ID))
print("\n===== LA RACINE DU /test APRÈS LA LIVRAISON =====")
for n in final:
    print(f"  {n}")
print("\nLA LIVRAISON DE L'UNITÉ 2 EST RECOUPÉE VERT — les DEUX bras au "
      "coffre, la carte à jour.")
