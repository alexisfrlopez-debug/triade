#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_1c4sokpii.py — LA LIVRAISON DE LA SESSION 1c4sokpii : le miroir au
commit, le kit, les rapports au /test (recoupés byte-byte), l'instruction
archivée (le motif établi — la voie PATCH documentée)."""
import hashlib
import json
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
ATELIER = REPO / "atelier-plan-final-1c4sokpii"

PIECES_TEST = [
    ("RAPPORT-1C4SOKPII.txt", ATELIER / "RAPPORT-1C4SOKPII.txt"),
    ("RAPPORT-INDEPENDANCE-FAMILLES.txt",
     ATELIER / "RAPPORT-INDEPENDANCE-FAMILLES.txt"),
    ("RAPPORT-REJEU-FAUTES-1C4SOKPII.txt", ATELIER / "rejeu_fautes_rapport.txt"),
]
INSTRUCTION = "Qwen__20261118_1c4sokpii.txt"


def md5_de(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


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

    # (1) les rapports au /test
    for nom, chemin in PIECES_TEST:
        def g(nom=nom, chemin=chemin, test=test, test_id=test_id):
            if nom in test and test[nom].get("md5Checksum") == md5_de(chemin):
                return "DÉJÀ EN PLACE (md5 égal)"
            if nom in test:
                ds.resumable_upload(
                    f"https://www.googleapis.com/upload/drive/v3/files/"
                    f"{test[nom]['id']}?uploadType=resumable", {}, chemin,
                    init_method="PATCH")
            else:
                ds.resumable_upload(
                    "https://www.googleapis.com/upload/drive/v3/files"
                    "?uploadType=resumable",
                    {"name": nom, "parents": [test_id]}, chemin)
            req = urllib.request.Request(
                f"{API}/files/{ds.list_folder(test_id)[nom]['id']}?alt=media",
                headers={"Authorization": "Bearer " + ds.get_access_token()})
            with urllib.request.urlopen(req, timeout=120) as r:
                octets = r.read()
            assert hashlib.md5(octets).hexdigest() == md5_de(chemin), "recoup échoue"
            return f"posé et recoupé byte-byte ({chemin.stat().st_size} o)"
        geste(f"le /test : {nom}", g)

    # (2) l'instruction 1c4sokpii archivée (la règle du développeur — la
    # vague 7 close, la dernière instruction descend à l'archive)
    def g_archive():
        instructions = ds.list_folder(racine["instructions"]["id"])
        if INSTRUCTION not in instructions:
            dest = ds.list_folder(racine["ARCHIVE"]["id"])
            if INSTRUCTION in ds.list_folder(
                    dest["instructions_20261119"]["id"]):
                return "DÉJÀ ARCHIVÉE"
            raise RuntimeError("l'instruction introuvable au /instructions")
        fid = instructions[INSTRUCTION]["id"]
        dest = ds.list_folder(racine["ARCHIVE"]["id"])
        dest_id = dest["instructions_20261119"]["id"]
        st, body, _ = ds.api("PATCH",
                             f"{API}/files/{fid}?addParents={dest_id}"
                             f"&fields=parents", {})
        assert st == 200, (st, body[:200])
        st, body, _ = ds.api("GET", f"{API}/files/{fid}?fields=parents")
        for p in json.loads(body).get("parents", []):
            if p != dest_id:
                st, body, _ = ds.api(
                    "PATCH", f"{API}/files/{fid}?removeParents={p}"
                    f"&fields=parents", {})
                assert st == 200, (st, body[:200])
        assert INSTRUCTION not in ds.list_folder(racine["instructions"]["id"]), \
            "encore au /instructions"
        assert INSTRUCTION in ds.list_folder(dest_id), "absente de l'archive"
        return "déplacée /instructions → /ARCHIVE/instructions_20261119/ " \
               "(la vague 7 close)"
    geste("l'archivage de l'instruction 1c4sokpii", g_archive)

    verts = sum(1 for v, _ in bilan if v == "VERT")
    print(f"\nBILAN : {verts}/{len(bilan)} VERT")
    return 0 if verts == len(bilan) else 1


if __name__ == "__main__":
    sys.exit(main())
