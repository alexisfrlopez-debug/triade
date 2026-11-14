#!/usr/bin/env python3
"""98_rapatrie_pieces.py — LE RAPATRIEMENT du dépôt « kit 02 C et T dans
/test du drive » : les DEUX copies datées nées au sein des kits (le run
1-clic du LANCEUR : la console + le témoin signé + les pièces du kit),
rangées au bac epreuves/ ; le LIVRE (l'atelier 013520, rangé à
archives-livraisons/unite-01-loupe-20261114/) rapatrié aussi — la question
M1 : les lignes loupe-02 y vivent-elles ?

Chaque pièce du kit de la copie datée est recoupée TROIS fois : la copie
déposée == le kit parent AU COFFRE (re-téléchargé) == le bac local du
labo (la vérité de la construction 290). Byte-byte, sha256."""
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

UPLOAD = "/home/z/my-project/upload"
FOLDER_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
BAC = pathlib.Path("/home/z/my-project/work/triade/scripts/campagne_d204")
SORTIE = BAC / "depot-runs-kit-02-294" / "epreuves"

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
si = f"{header}.{claims}".encode()
key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
jwt = f"{header}.{claims}.{b64url(key.sign(si, padding.PKCS1v15(), hashes.SHA256()))}"
req = urllib.request.Request(
    sa["token_uri"],
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
                   "nextPageToken,files(id,name,mimeType,modifiedTime,createdTime,size)")
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


def telecharge(item, dossier):
    data = api(f"https://www.googleapis.com/drive/v3/files/{item['id']}?alt=media",
               binary=True)
    chemin = dossier / item["name"]
    with open(chemin, "wb") as f:
        f.write(data)
    return data


def sha256(data):
    return hashlib.sha256(data).hexdigest()


# -- 0. navigation : racine → test → les kits --------------------------------
test = sub(FOLDER_ID, "test")
assert test, "dossier test introuvable"
kitT = sub(test["id"], "kit-unite-loupe-02-T-20261114")
kitC = sub(test["id"], "kit-unite-loupe-02-C-20261114")
assert kitT and kitC, "kits loupe-02 introuvables au /test"

# -- 1. LA COPIE DATÉE T (le dépôt du run du bras T) --------------------------
depT = sub(kitT["id"], "kit-unite-loupe-02-T-20261114")
assert depT, "la copie datée T introuvable"
outT = SORTIE / "T-depot"
(outT / "preuves-unite02").mkdir(parents=True, exist_ok=True)
print(f"=== A. LE DÉPÔT T — /test/kit-unite-loupe-02-T-20261114/kit-unite-loupe-02-T-20261114/")
print(f"    (né au coffre {depT['createdTime'][:19]}Z, {len(children(depT['id']))} entrées)")
piecesT = {}
for it in sorted(children(depT["id"]), key=lambda x: x["name"]):
    if it["mimeType"] == "application/vnd.google-apps.folder":
        for it2 in sorted(children(it["id"]), key=lambda x: x["name"]):
            data = telecharge(it2, outT / it["name"])
            piecesT[f"{it['name']}/{it2['name']}"] = data
            print(f"    [OK] {it['name']}/{it2['name']}  {len(data)} o  "
                  f"sha256 {sha256(data)[:16]}…  (modifié {it2['modifiedTime'][:19]}Z)")
    else:
        data = telecharge(it, outT)
        piecesT[it["name"]] = data
        print(f"    [OK] {it['name']}  {len(data)} o  sha256 {sha256(data)[:16]}…  "
              f"(modifié {it['modifiedTime'][:19]}Z)")

# -- 2. LA COPIE DATÉE C ------------------------------------------------------
depC = sub(kitC["id"], "kit-unite-loupe-02-C-20261114")
assert depC, "la copie datée C introuvable"
outC = SORTIE / "C-depot"
(outC / "preuves-unite02C").mkdir(parents=True, exist_ok=True)
print(f"\n=== B. LE DÉPÔT C — /test/kit-unite-loupe-02-C-20261114/kit-unite-loupe-02-C-20261114/")
print(f"    (né au coffre {depC['createdTime'][:19]}Z, {len(children(depC['id']))} entrées)")
piecesC = {}
for it in sorted(children(depC["id"]), key=lambda x: x["name"]):
    if it["mimeType"] == "application/vnd.google-apps.folder":
        for it2 in sorted(children(it["id"]), key=lambda x: x["name"]):
            data = telecharge(it2, outC / it["name"])
            piecesC[f"{it['name']}/{it2['name']}"] = data
            print(f"    [OK] {it['name']}/{it2['name']}  {len(data)} o  "
                  f"sha256 {sha256(data)[:16]}…  (modifié {it2['modifiedTime'][:19]}Z)")
    else:
        data = telecharge(it, outC)
        piecesC[it["name"]] = data
        print(f"    [OK] {it['name']}  {len(data)} o  sha256 {sha256(data)[:16]}…  "
              f"(modifié {it['modifiedTime'][:19]}Z)")

# -- 3. LE RECOURS TROIS FOIS : copie == parent au coffre == bac local --------
print("\n=== C. LE RECOUP TROIS FOIS (la copie déposée == le kit parent au coffre == le bac local)")
def recoup_trois(depot_pieces, kit_parent_id, bac_local, etiquette, nouvelles):
    parent = {it["name"]: it for it in children(kit_parent_id)
              if it["mimeType"] != "application/vnd.google-apps.folder"}
    verts, ecarts = 0, []
    for nom, data_depot in sorted(depot_pieces.items()):
        if nom in nouvelles:
            continue  # la console et le témoin : les pièces NOUVELLES, pas au kit
        h_depot = sha256(data_depot)
        # (a) le parent au coffre, re-téléchargé
        if nom not in parent:
            ecarts.append(f"{nom} : ABSENT du kit parent")
            continue
        data_parent = api(
            f"https://www.googleapis.com/drive/v3/files/{parent[nom]['id']}?alt=media",
            binary=True)
        # (b) le bac local
        chemin_bac = bac_local / nom
        if not chemin_bac.exists():
            ecarts.append(f"{nom} : ABSENT du bac local {bac_local}")
            continue
        data_bac = chemin_bac.read_bytes()
        if h_depot == sha256(data_parent) == sha256(data_bac):
            verts += 1
            print(f"    [VERT] {nom} : copie == parent == bac  ({h_depot[:16]}…)")
        else:
            ecarts.append(f"{nom} : copie {h_depot[:8]}… parent {sha256(data_parent)[:8]}… "
                          f"bac {sha256(data_bac)[:8]}…")
    for nom in nouvelles:
        print(f"    [NOUVEAU] {nom} : la pièce née du run (recoup à part)")
    print(f"    → {etiquette} : {verts} VERT, {len(ecarts)} ÉCART")
    for e in ecarts:
        print(f"    [ÉCART] {e}")
    return verts, ecarts

vT, eT = recoup_trois(piecesT, kitT["id"], BAC / "unite-02-T" / "kit",
                      "bras T", {"run-console-unite02.txt",
                                 "preuves-unite02/temoin-unite02.txt"})
vC, eC = recoup_trois(piecesC, kitC["id"], BAC / "unite-02-C" / "kit",
                      "bras C", {"run-console-unite02C.txt",
                                 "preuves-unite02C/temoin-unite02C.txt"})

# -- 4. LE LIVRE : l'atelier rangé — les lignes loupe-02 y vivent-elles ? -----
print("\n=== D. LE LIVRE (l'atelier 013520, rangé à archives-livraisons/unite-01-loupe-20261114/)")
arch = sub(test["id"], "archives-livraisons")
u1 = sub(arch["id"], "unite-01-loupe-20261114")
atelier = sub(u1["id"], "atelier-campagne-d204-20261114-013520")
assert atelier, "l'atelier 013520 introuvable à sa place rangée"
outL = SORTIE / "atelier-le-livre"
outL.mkdir(parents=True, exist_ok=True)
for it in sorted(children(atelier["id"]), key=lambda x: x["name"]):
    data = telecharge(it, outL)
    print(f"    [OK] {it['name']}  {len(data)} o  sha256 {sha256(data)[:16]}…  "
          f"(modifié {it['modifiedTime'][:19]}Z)")
    if it["name"] == "livraisons.csv":
        texte = data.decode("utf-8-sig", errors="replace")
        print("    ---- livraisons.csv, le contenu :")
        for ligne in texte.splitlines():
            print(f"    | {ligne}")
        loupe02 = [l for l in texte.splitlines() if "loupe-02" in l]
        print(f"    ---- lignes loupe-02 : {len(loupe02)}"
              + (" — LE LIVRE PORTE L'UNITÉ 2" if loupe02 else
                 " — ÉCART NOMMÉ : le livre ne porte PAS encore l'unité 2"))

print(f"\n[RÉSUMÉ] kits recoupés trois fois : T {vT} VERT / {len(eT)} écart ; "
      f"C {vC} VERT / {len(eC)} écart")
