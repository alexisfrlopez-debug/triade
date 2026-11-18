#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Livraison d355 : le rapport de réception posé au /test du coffre Drive
par le jeton relais (le précédent relivrer_guide_354), recoupé par
re-téléchargement byte-byte (md5 ==). Ne JAMAIS imprimer les jetons."""
import hashlib, os, sys, json, urllib.request, urllib.parse

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_client import get_access_token, get_file_meta  # OAuth relais

TEST_ROOT = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"  # /test du coffre
BAC = "/home/z/my-project/scripts/campagne_d204/reception-355"
REPORT = os.path.join(BAC, "RAPPORT-RECEPTION-LIGNES-LIVRE-D210-355-20261119.txt")


def md5b(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    at = get_access_token()
    name = os.path.basename(REPORT)
    with open(REPORT, "rb") as f:
        blob = f.read()

    # pose multipart au /test
    boundary = "TRIADE-labo-355"
    meta = json.dumps({"name": name, "parents": [TEST_ROOT]})
    body = (("--%s\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n%s\r\n"
             "--%s\r\nContent-Type: text/plain\r\n\r\n" % (boundary, meta, boundary)).encode()
            + blob + ("\r\n--%s--" % boundary).encode())
    rq = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true",
        data=body, method="POST",
        headers={"Authorization": "Bearer " + at,
                 "Content-Type": "multipart/related; boundary=" + boundary})
    with urllib.request.urlopen(rq, timeout=120) as r:
        resp = json.loads(r.read().decode())
    fid = resp["id"]
    print("POSÉ au /test : %s [id %s, %d o]" % (resp["name"], fid, len(blob)))

    # recoup par re-téléchargement byte-byte + md5 == métadonnée
    dest = os.path.join(BAC, "reception-retour-" + name)
    rq2 = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/files/%s?alt=media&supportsAllDrives=true" % fid,
        headers={"Authorization": "Bearer " + get_access_token()})
    with urllib.request.urlopen(rq2, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    same = open(REPORT, "rb").read() == open(dest, "rb").read()
    m = get_file_meta(fid)
    md_local, md_api = md5b(REPORT), m.get("md5Checksum", "-")
    ok = same and md_local == md_api and int(m.get("size", -1)) == len(blob)
    print("RETOUR byte-byte : %s | md5 local %s == md5 API %s : %s | taille API %s" % (
        "OUI" if same else "NON", md_local, md_api, "OUI" if md_local == md_api else "NON", m.get("size")))
    print("LIVRAISON :", "TOUT VERT" if ok else "ROUGE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
