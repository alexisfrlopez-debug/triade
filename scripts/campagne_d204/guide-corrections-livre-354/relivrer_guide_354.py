#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-livraison du guide-354 au /test du coffre — MISE À JOUR du fichier
Déjà livré (id connu), jamais un doublon : le contenu corrigé remplace
l'octet du fichier existant, le md5 re-recoupé par les métadonnées.
Usage: python3 relivrer_guide_354.py
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_client import get_access_token, get_file_meta  # noqa: E402

import urllib.request  # noqa: E402

FICHIER_LOCAL = "/home/z/my-project/download/GUIDE-CORRECTIONS-LIVRE-354-20261118.txt"
FILE_ID = "1-majayvX5JhqFSrb2J88b_gf80znuJEJ"


def main() -> int:
    with open(FICHIER_LOCAL, "rb") as f:
        blob = f.read()
    at = get_access_token()
    url = ("https://www.googleapis.com/upload/drive/v3/files/%s"
           "?uploadType=media&supportsAllDrives=true" % FILE_ID)
    req = urllib.request.Request(url, data=blob, method="PATCH",
                                 headers={"Authorization": "Bearer " + at,
                                          "Content-Type": "text/plain"})
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    print("MIS À JOUR id=%s name=%s size=%d" % (resp["id"], resp["name"], len(blob)))
    meta = get_file_meta(FILE_ID)
    md5_local = hashlib.md5(blob).hexdigest()
    md5_drive = meta.get("md5Checksum")
    print("md5 local : %s" % md5_local)
    print("md5 drive : %s" % md5_drive)
    if md5_local != md5_drive:
        print("ROUGE — les condensés divergent")
        return 1
    print("VERT — le guide corrigé vit au /test, byte-byte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
