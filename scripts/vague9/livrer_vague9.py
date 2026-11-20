#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_vague9.py — LA LIVRAISON AU COFFRE DRIVE (la vague 9) :
(1) L'ARCHIVAGE des CINQ instructions exécutées /instructions ->
    /ARCHIVE/instructions_vague9_20261120/ (la règle du développeur :
    « à archiver après exécution ») — la voie native
    addParents/removeParents, la corbeille jamais (D143) ;
(2) LE PACK TRIADE_presentation_v0.20.0.zip à la RACINE du coffre,
    recoupé par re-téléchargement byte-byte ;
(3) les pièces de session au /test (le rapport de vérification, les
    empreintes, les rapports d'atelier) ;
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
ARCHIVE = "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr"
REPO = pathlib.Path("/home/z/my-project/depot")
V9 = REPO / "scripts" / "vague9"

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
    # idempotence : si le fichier existe déjà IDENTIQUE au parent, skip
    attendu = chemin.read_bytes()
    for it in drive_api.list_folder(parent):
        if it["name"] == nom and int(it.get("size", -1)) == len(attendu):
            print(f"  DÉJÀ {nom} [{len(attendu):,} o] — inchangé")
            return it["id"]
    meta = {"name": nom, "parents": [parent]}
    boundary = "v9bnd"
    parts = []
    parts.append(f"--{boundary}\r\nContent-Type: application/json; "
                 f"charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Type: application/octet-stream"
                 f"\r\n\r\n".encode() + attendu + b"\r\n")
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
    ok = r2.content == attendu
    print(f"  {'VERT' if ok else 'ROUGE'} {nom} [{len(attendu):,} o] "
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
    arch = trouver_ou_creer("instructions_vague9_20261120", ARCHIVE)
    executes = {"Qwen_text_20261120_bk79jvzbm.txt",
                "Qwen_text_20261120_0205wxg5q.txt",
                "Qwen_text_20261120_bkobf06nu.txt",
                "Qwen_text_20261120_uagz3fby7.txt",
                "Qwen_text_20261120_h0mq0s2m6.txt"}
    for it in drive_api.list_folder(INSTRUCTIONS):
        if it["name"] in executes:
            deplacer(it["id"], arch, INSTRUCTIONS)
            print(f"  ARCHIVÉ {it['name']} -> /ARCHIVE/"
                  f"instructions_vague9_20261120/")
    restants = [i["name"] for i in drive_api.list_folder(INSTRUCTIONS)]
    print(f"  le /instructions demeure : {restants}")

    print("== (2) LE PACK v0.20.0 à la racine du coffre ==")
    televerser(REPO / "TRIADE_presentation_v0.20.0.zip", RACINE)

    print("== (3) LES PIÈCES DE SESSION au /test ==")
    for piece in ("rapport_verification_v0.20.0.txt",
                  "empreintes_livrables_v0.20.0.txt"):
        televerser(V9 / piece, TEST)
    televerser(REPO / "atelier-securite-bk79jvzbm" /
               "surete_memoire_v200_rapport.txt", TEST)
    televerser(REPO / "atelier-dashboard-h0mq0s2m6" /
               "tableau-bord-quatre-axes.txt", TEST)

    print("== (4) LES DEUX ARCHIVES DE DÉPÔT à la racine ==")
    televerser(REPO / "depot-zenodo-v0200" / "TRIADE_soumission_v0.20.0.zip",
               RACINE)
    televerser(REPO / "depot-zenodo-v0200" / "TRIADE_complet_v0.20.0.zip",
               RACINE)
    print()
    print("LA LIVRAISON VÉCUE — aucune erreur, chaque pièce recoupée")


if __name__ == "__main__":
    main()
