#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_v0195.py — LA LIVRAISON DE L'ÉDITION v0.19.5 : le miroir au
commit, le kit, le pack à la racine (le motif des Task 232/233), les
pièces de la session au /test (recoupées byte-byte)."""
import hashlib
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

REPO = pathlib.Path("/home/z/my-project/depot")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

ROOT_ID = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
API = "https://www.googleapis.com/drive/v3"
V7 = REPO / "scripts" / "vague7"

PACK = V7 / "TRIADE_presentation_v0.19.5_20261120.zip"
PIECES_TEST = [
    ("TRIADE_manuscrit_v0.19.5.pdf", REPO / "edition-v0195" / "main.pdf"),
    ("TRIADE_preuves_et_calculs_v0.19.5.pdf",
     V7 / "TRIADE_preuves_et_calculs_v0.19.5.pdf"),
    ("TRIADE_presentation_20261120_v195.pdf",
     V7 / "TRIADE_presentation_20261120_v195.pdf"),
    ("rapport_verification_v0.19.5.txt",
     V7 / "rapport_verification_v0.19.5.txt"),
]


def md5_de(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def pose_recoupe(nom, chemin, dossier_id, dossier_avant):
    if nom in dossier_avant and dossier_avant[nom].get("md5Checksum") == md5_de(chemin):
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
    print("=== (0) le miroir puis le kit ===")
    r1 = subprocess.run([sys.executable, str(REPO / "scripts/drive_sync.py")],
                        cwd=REPO, capture_output=True, text=True, timeout=2400)
    print(r1.stdout.strip().splitlines()[-1] if r1.stdout.strip() else "(…)")
    assert r1.returncode in (0, 1), r1.stderr[-200:]
    r2 = subprocess.run([sys.executable, str(REPO / "scripts/maj_kit.py")],
                        cwd=REPO, capture_output=True, text=True, timeout=2400)
    print(r2.stdout.strip().splitlines()[-1] if r2.stdout.strip() else "(…)")
    assert r2.returncode in (0, 1), r2.stderr[-200:]

    racine = ds.list_folder(ROOT_ID)
    test_id = racine["test"]["id"]
    test = ds.list_folder(test_id)
    bilan = []

    def geste(nom, fn):
        try:
            bilan.append(("VERT", nom))
            print(f"VERT  {nom} — {fn()}")
        except Exception as e:  # noqa: BLE001
            bilan.append(("ROUGE", nom))
            print(f"ROUGE {nom} — {str(e)[:220]}")

    # (1) le pack à la racine (le motif des packs)
    def g_pack():
        return pose_recoupe(PACK.name, PACK, ROOT_ID, racine)
    geste(f"la racine : {PACK.name}", g_pack)

    # (2) les pièces de la session au /test
    for nom, chemin in PIECES_TEST:
        def g(nom=nom, chemin=chemin, test=test, test_id=test_id):
            return pose_recoupe(nom, chemin, test_id, test)
        geste(f"le /test : {nom}", g)

    verts = sum(1 for v, _ in bilan if v == "VERT")
    print(f"\nBILAN : {verts}/{len(bilan)} VERT")
    return 0 if verts == len(bilan) else 1


if __name__ == "__main__":
    sys.exit(main())
