#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_coffre_vague10.py — LA LIVRAISON AU COFFRE (la vague 10) :
LE PACK TRIADE_presentation_v0.21.0.zip à la RACINE (recoupé
byte-byte), LES DEUX ARCHIVES DE DÉPÔT à la racine (la soumission, le
complet), LES PIÈCES DE SESSION au /test (le rapport de vérification,
les rapports des ateliers) — la vue du relais."""
import hashlib
import json
import pathlib
import requests
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"

RELAIS = json.load(open("/home/z/my-project/depot/.gdrive/"
                        "oauth_token_relais.json"))
_tok = {"val": None, "exp": 0}


def hdr():
    import time
    if _tok["val"] is None or time.time() > _tok["exp"] - 120:
        r = requests.post(RELAIS["token_uri"], data={
            "client_id": RELAIS["client_id"],
            "client_secret": RELAIS["client_secret"],
            "refresh_token": RELAIS["refresh_token"],
            "grant_type": "refresh_token"}, timeout=30)
        r.raise_for_status()
        d = r.json()
        _tok["val"] = d["access_token"]
        _tok["exp"] = time.time() + d.get("expires_in", 3600)
    return {"Authorization": f"Bearer {_tok['val']}"}


def trouver(nom, parent):
    r = requests.get("https://www.googleapis.com/drive/v3/files",
                    headers=hdr(), params={
                        "q": f"'{parent}' in parents and name='{nom}' "
                             f"and trashed=false",
                        "fields": "files(id,name)", "pageSize": 5},
                    timeout=30)
    fs = r.json().get("files", [])
    return fs[0]["id"] if fs else None


def televerser(chemin, parent, remplacer=True):
    """L'upload (multipart) ; si le nom vit déjà au parent : la mise à
    jour (le média remplacé) — l'idempotence."""
    nom = pathlib.Path(chemin).name
    data = pathlib.Path(chemin).read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    fid = trouver(nom, parent)
    if fid:
        r = requests.patch(
            f"https://www.googleapis/upload/drive/v3/files/{fid}",
            headers=hdr(), params={"uploadType": "media",
                                    "supportsAllDrives": "true"},
            data=data, timeout=600)
        r.raise_for_status()
        print(f"  [mis à jour] {nom} [{len(data):,} o]")
    else:
        meta = {"name": nom, "parents": [parent]}
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files",
            headers=hdr(), params={"uploadType": "multipart",
                                    "supportsAllDrives": "true"},
            files={"metadata": (None, json.dumps(meta),
                                "application/json"),
                   "media": (nom, data,
                             "application/octet-stream")}, timeout=600)
        r.raise_for_status()
        fid = r.json()["id"]
        print(f"  [téléversé] {nom} [{len(data):,} o]")
    # LE RECOUP byte-byte
    r2 = requests.get(f"https://www.googleapis.com/drive/v3/files/{fid}",
                      headers=hdr(), params={"alt": "media",
                                             "supportsAllDrives": "true"},
                      timeout=600)
    r2.raise_for_status()
    ok = r2.content == data
    print(f"  {'VERT' if ok else 'ROUGE'} {nom} recoupé byte-byte : {ok}")
    if not ok:
        raise SystemExit(f"RECOUP ÉCHOUÉ : {nom}")
    return fid


def main():
    print("== (1) LE PACK v0.21.0 à la racine du coffre ==")
    televerser(REPO / "TRIADE_presentation_v0.21.0.zip", RACINE)
    print("== (2) LES DEUX ARCHIVES DE DÉPÔT à la racine ==")
    televerser(REPO / "depot-zenodo-v0210" / "TRIADE_soumission_v0.21.0.zip",
              RACINE)
    televerser(REPO / "depot-zenodo-v0210" / "TRIADE_complet_v0.21.0.zip",
               RACINE)
    print("== (3) LES PIÈCES DE SESSION au /test ==")
    for f in [REPO / "rapport_verification_v0.21.0.txt",
              REPO / "scripts" / "vague10" /
              "empreintes_livrables_v0.21.0.txt",
              REPO / "atelier-cg-3a91o5whb" / "rapport-cg-reconciliation.txt",
              REPO / "atelier-remesure-sse2-8z4hj76w4" /
              "rapport-temps-reel.txt",
              REPO / "atelier-fenetre-mqf258e4l" / "rapport-fenetre.txt",
              REPO / "atelier-gardes-ifqm1d1i4" /
              "rapport-non-interference-v210.txt"]:
        televerser(f, TEST)
    print("LA LIVRAISON AU COFFRE VÉCUE — les trois bords (racine, /test)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
