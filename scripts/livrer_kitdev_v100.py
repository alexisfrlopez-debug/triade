#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_kitdev_v100.py — LA LIVRAISON DU KIT DE DÉVELOPPEMENT v1.0.0 :
le miroir au commit (déjà roulé : 31 téléversés + 2 mis à jour, 0 erreur),
le kit D130 (déjà roulé : 60/60), LE ZIP à la racine du coffre (le motif des
packs), les pièces de la session au /test (recoupées byte-byte)."""
import hashlib
import pathlib
import sys
import urllib.request

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

ROOT_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"

LIVRABLES = [
    # (nom Drive, chemin local, dossier cible : "racine" ou "test")
    ("TRIADE_kit_developpement_v1.0.0.zip",
     REPO / "TRIADE_kit_developpement_v1.0.0.zip", "racine"),
    ("RAPPORT-KIT-DEV-V100-20261120.txt",
     REPO / "scripts" / "vague7" / "RAPPORT-KIT-DEV-V100-20261120.txt",
     "test"),
]


def md5_de(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def pose_recoupe(nom, chemin, dossier_id, dossier_avant):
    if nom in dossier_avant and \
            dossier_avant[nom].get("md5Checksum") == md5_de(chemin):
        return "DÉJÀ EN PLACE (md5 égal)"
    if nom in dossier_avant:
        ds.resumable_upload(
            f"https://www.googleapis.com/upload/drive/v3/files/"
            f"{dossier_avant[nom]['id']}?uploadType=resumable", {}, chemin,
            init_method="PATCH")
    else:
        ds.resumable_upload(
            "https://www.googleapis.com/upload/drive/v3/files"
            "?uploadType=resumable",
            {"name": nom, "parents": [dossier_id]}, chemin)
    fid = ds.list_folder(dossier_id)[nom]["id"]
    req = urllib.request.Request(
        f"{API}/files/{fid}?alt=media",
        headers={"Authorization": "Bearer " + ds.get_access_token()})
    with urllib.request.urlopen(req, timeout=180) as r:
        octets = r.read()
    assert hashlib.md5(octets).hexdigest() == md5_de(chemin), "recoup échoue"
    return f"posé et recoupé byte-byte ({chemin.stat().st_size:,} o)"


def main():
    racine = ds.list_folder(ROOT_ID)
    test_id = racine["test"]["id"]
    test = ds.list_folder(test_id)
    dossiers = {"racine": (ROOT_ID, racine), "test": (test_id, test)}
    bilan = []

    def geste(nom, fn):
        try:
            bilan.append(("VERT", nom))
            print(f"VERT  {nom} — {fn()}")
        except Exception as e:  # noqa: BLE001
            bilan.append(("ROUGE", nom))
            print(f"ROUGE {nom} — {str(e)[:220]}")

    for nom, chemin, cible in LIVRABLES:
        if not chemin.exists():
            print(f"ROUGE {nom} — absent localement : {chemin}")
            bilan.append(("ROUGE", nom))
            continue
        def g(nom=nom, chemin=chemin, cible=cible):
            return pose_recoupe(nom, chemin, *dossiers[cible])
        geste(f"le /{cible} : {nom}", g)

    verts = sum(1 for v, _ in bilan if v == "VERT")
    print(f"\nBILAN : {verts}/{len(bilan)} VERT")
    return 0 if verts == len(bilan) else 1


if __name__ == "__main__":
    sys.exit(main())
