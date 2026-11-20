#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_vague8.py — LA LIVRAISON AU COFFRE DRIVE (la vague 8) :
(1) L'ARCHIVAGE des CINQ instructions exécutées /instructions ->
    /ARCHIVE/instructions_20261120/ (la règle du développeur : « à
    archiver après exécution ») — la voie native addParents/removeParents,
    la corbeille jamais (D143) ;
(2) LE PACK TRIADE_presentation_v0.19.6_20261120.zip à la RACINE du
    coffre, recoupé par re-téléchargement byte-byte ;
(3) les pièces de session au /test (le rapport de vérification, les
    empreintes, les deux rapports d'atelier) ;
(4) les DEUX archives de dépôt à la racine (soumission, complet).
Le relais OAuth du /tokens (la ré-autorisation du maître, 19/11 20:26)."""
import json
import pathlib
import sys
import time

import requests

sys.path.insert(0, "/home/z/my-project/scripts")
import drive_api  # noqa: E402

RELAIS = json.load(open("/home/z/my-project/work/tokens_drive/"
                        "oauth_token_relais.json"))
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
REPO = pathlib.Path("/home/z/my-project/depot")

_tok = {"val": None, "exp": 0}


def hdr():
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


def creer_dossier(nom, parent):
    r = requests.post("https://www.googleapis.com/drive/v3/files",
                      headers=hdr(),
                      json={"name": nom,
                            "mimeType": "application/vnd.google-apps.folder",
                            "parents": [parent]}, timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def trouver_ou_creer(nom, parent):
    for it in drive_api.list_folder(parent):
        if it["name"] == nom and it["mimeType"] == \
                "application/vnd.google-apps.folder":
            return it["id"]
    return creer_dossier(nom, parent)


def televerser(chemin, parent, nom=None):
    nom = nom or chemin.name
    meta = {"name": nom, "parents": [parent]}
    boundary = "v8bnd"
    parts = []
    parts.append(f"--{boundary}\r\nContent-Type: application/json; "
                 f"charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Type: application/octet-stream"
                 f"\r\n\r\n".encode() + chemin.read_bytes() + b"\r\n")
    parts.append(f"--{boundary}--".encode())
    body = b"".join(parts)
    r = requests.post("https://www.googleapis.com/upload/drive/v3/files"
                      "?uploadType=multipart&supportsAllDrives=true",
                      headers={**hdr(),
                               "Content-Type": f"multipart/related; "
                                               f"boundary={boundary}"},
                      data=body, timeout=300)
    r.raise_for_status()
    fid = r.json()["id"]
    # LE RECOUP : re-téléchargement byte-byte
    r2 = requests.get(f"https://www.googleapis.com/drive/v3/files/{fid}",
                      headers=hdr(),
                      params={"alt": "media", "supportsAllDrives": True},
                      timeout=120)
    r2.raise_for_status()
    ok = r2.content == chemin.read_bytes()
    print(f"  {'VERT' if ok else 'ROUGE'} {nom} [{chemin.stat().st_size:,} o] "
          f"recoupé byte-byte : {ok}")
    if not ok:
        raise SystemExit(f"RECOUP ÉCHOUÉ : {nom}")
    return fid


def deplacer(fid, add_parent, remove_parent):
    r = requests.patch(f"https://www.googleapis.com/drive/v3/files/{fid}",
                       headers=hdr(), params={
                           "addParents": add_parent,
                           "removeParents": remove_parent,
                           "supportsAllDrives": True}, timeout=30)
    r.raise_for_status()


def main():
    print("== (1) L'ARCHIVAGE des cinq instructions exécutées ==")
    arch = trouver_ou_creer("instructions_20261120",
                            "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr")
    executes = {"Qwen_text_20261120_gq117wphb.txt", "Qwen_text_20261120_ansz8lvdf.txt",
                "Qwen_text_20261120_nunsmzmrm.txt", "Qwen_text_20261120_peap6ws09.txt",
                "Qwen_text_20261120_pe6iv71fj.txt"}
    for it in drive_api.list_folder(INSTRUCTIONS):
        if it["name"] in executes:
            deplacer(it["id"], arch, INSTRUCTIONS)
            print(f"  ARCHIVÉ {it['name']} -> /ARCHIVE/instructions_20261120/")
    restants = [i["name"] for i in drive_api.list_folder(INSTRUCTIONS)]
    print(f"  le /instructions demeure : {restants} (la vague 9 : jamais "
          f"archivées avant exécution)")

    print("== (2) LE PACK v0.19.6 à la racine du coffre ==")
    televerser(REPO / "TRIADE_presentation_v0.19.6_20261120.zip", RACINE)

    print("== (3) LES PIÈCES DE SESSION au /test ==")
    v8 = REPO / "scripts" / "vague8"
    for piece in ("rapport_verification_v0.19.6.txt",
                  "empreintes_livrables_v0.19.6.txt"):
        televerser(v8 / piece, TEST)
    televerser(REPO / "atelier-opt05-pe6iv71fj" / "RAPPORT-OPT05.txt", TEST)
    televerser(REPO / "atelier-independance-peap6ws09" / "RAPPORT-PEAP6WS09.txt",
               TEST)

    print("== (4) LES DEUX ARCHIVES DE DÉPÔT à la racine ==")
    televerser(REPO / "depot-zenodo-v0196" / "TRIADE_soumission_v0.19.6.zip",
               RACINE)
    televerser(REPO / "depot-zenodo-v0196" / "TRIADE_complet_v0.19.6.zip",
               RACINE)
    print()
    print("LA LIVRAISON VÉCUE — aucune erreur, chaque pièce recoupée")


if __name__ == "__main__":
    main()
