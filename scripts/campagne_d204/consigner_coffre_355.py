#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consignation d355 au coffre Drive : la carte OU-TROUVER portée à 355
(racine + miroir TRIADE-sauvegarde-git) et le worklog consolidé (miroir) —
MISE À JOUR des fichiers existants (ids connus, jamais un doublon), chaque
pose recoupée par re-téléchargement byte-byte (md5 == la métadonnée).
Ne JAMAIS imprimer les jetons."""
import hashlib, json, os, sys, urllib.request

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_client import get_access_token, get_file_meta

BAC = "/home/z/my-project/scripts/campagne_d204/reception-355"
POSES = [
    ("OU-TROUVER (racine)", os.path.join(BAC, "OU-TROUVER-LES-LIVRABLES-355.md"), "1tcumyuCxXGGq5IkXSY5y9CL0fCPdvQBu"),
    ("OU-TROUVER (miroir)", os.path.join(BAC, "OU-TROUVER-LES-LIVRABLES-355.md"), "1TnzKqAJGmn6Rh8kQ7EDZutB5LDGOwn7w"),
    ("worklog consolidé (miroir)", os.path.join(BAC, "worklog-consolide.md"), "1IjBk84S81ioBMASehROG3UsdJkO6JEBY"),
]


def md5b(b):
    return hashlib.md5(b).hexdigest()


def main() -> int:
    ok = True
    for label, local, fid in POSES:
        with open(local, "rb") as f:
            blob = f.read()
        at = get_access_token()
        url = ("https://www.googleapis.com/upload/drive/v3/files/%s"
               "?uploadType=media&supportsAllDrives=true" % fid)
        rq = urllib.request.Request(url, data=blob, method="PATCH",
                                    headers={"Authorization": "Bearer " + at,
                                             "Content-Type": "text/plain; charset=utf-8"})
        with urllib.request.urlopen(rq, timeout=180) as r:
            resp = json.loads(r.read().decode())
        m = get_file_meta(fid)
        md_local, md_api = md5b(blob), m.get("md5Checksum", "-")
        # re-téléchargement byte-byte
        rq2 = urllib.request.Request(
            "https://www.googleapis.com/drive/v3/files/%s?alt=media&supportsAllDrives=true" % fid,
            headers={"Authorization": "Bearer " + get_access_token()})
        with urllib.request.urlopen(rq2, timeout=180) as r:
            back = r.read()
        same = back == blob
        vert = same and md_local == md_api and int(m.get("size", -1)) == len(blob)
        ok = ok and vert
        print("%s : %s — %d o, md5 %s… == API %s… : %s | retour byte-byte : %s" % (
            label, "VERT" if vert else "ROUGE", len(blob), md_local[:8], md_api[:8],
            "OUI" if md_local == md_api else "NON", "OUI" if same else "NON"))
    print("CONSIGNATION AU COFFRE :", "TOUT VERT" if ok else "ROUGE")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
