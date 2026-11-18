#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recoupement d355 : DOUBLE téléchargement des QUATRE registres de l'atelier,
md5 == la métadonnée Drive (échec fermé), comparaison byte-byte des deux passes.
Ne JAMAIS imprimer les jetons."""
import json, os, subprocess, sys, hashlib, urllib.request, urllib.parse

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_api import get_access_token, api  # réutilise le jeton SA caché

ATELIER = "1U7ZPEvETn6MwBEq5cDUbEsVQ8Lx7Jn2k"  # /test/atelier-campagne-d204-20261114-013520
BAC = "/home/z/my-project/scripts/campagne_d204/reception-355"
PASS1 = os.path.join(BAC, "registres-recus")     # première passe (déjà rapatriée)
PASS2 = os.path.join(BAC, "registres-recus-passe2")

REGISTRES = [
    ("1S9njFvRZ6xa_PodU34Qw-aCqh17axzz7", "livraisons.csv"),
    ("1q4mM0n0Np572IFMgf3ZTjFGxCVKYYMzP", "defauts.csv"),
    ("1sxGV6uibd_pL96Z3inCBIPht5R4qtBTh", "journal-ouverture.txt"),
    ("1kJJytxPdhE66UnWb7tCHI9iVNhNY7rpt", "carnet_temps_humain.csv"),
]

def download(fid, dest):
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media"
    rq = urllib.request.Request(url, headers={"Authorization": "Bearer " + get_access_token()})
    with urllib.request.urlopen(rq, timeout=120) as r, open(dest, "wb") as f:
        while True:
            c = r.read(1 << 16)
            if not c:
                break
            f.write(c)
    return os.path.getsize(dest)

def md5b(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()

def sha256b(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()

os.makedirs(PASS2, exist_ok=True)
ok = True
for fid, name in REGISTRES:
    q = urllib.parse.urlencode({"fields": "id,name,size,md5Checksum,modifiedTime"})
    meta = api(f"https://www.googleapis.com/drive/v3/files/{fid}?{q}")
    p1 = os.path.join(PASS1, name)
    p2 = os.path.join(PASS2, name)
    n = download(fid, p2)
    same = open(p1, "rb").read() == open(p2, "rb").read()
    m1, m2 = md5b(p1), md5b(p2)
    md_api = meta.get("md5Checksum", "-")
    verdict = "VERT" if (same and m1 == m2 == md_api and n == int(meta.get("size", -1))) else "ROUGE"
    if verdict == "ROUGE":
        ok = False
    print(f"{verdict}  {name}: {n} o  md5 passe1={m1[:8]}…  md5 passe2={m2[:8]}…  md5-API={md_api[:8]}…  double-téléchargement byte-byte={'OUI' if same else 'NON'}  mod={meta.get('modifiedTime')}")

print("RECOUPEMENT GLOBAL :", "TOUT VERT" if ok else "ROUGE — ÉCHEC FERMÉ")
sys.exit(0 if ok else 1)
