#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_gui_unite02_d210.py — LA LIVRAISON AU COFFRE /test (le geste
établi de la 331 : upload + recoup md5 par re-téléchargement, échec
fermé). Livre : le kit zip, le LISEZMOI, les EMPREINTES, le CORRECTIF-T0."""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER = pathlib.Path("/home/z/my-project/download")
LIVRAISON = [
    ("kit-gui-1clic-unite02-d210-20261118.zip",
     DOSSIER / "kit-gui-1clic-unite02-d210-20261118.zip"),
    ("LISEZMOI-RUN-UNITE02-D210-1CLIC.txt",
     DOSSIER / "TRIADE_gui_unite02_d210_v1"
     / "LISEZMOI-RUN-UNITE02-D210-1CLIC.txt"),
    ("EMPREINTES-GUI-UNITE02-D210-1CLIC.txt",
     DOSSIER / "TRIADE_gui_unite02_d210_v1"
     / "EMPREINTES-GUI-UNITE02-D210-1CLIC.txt"),
    ("CORRECTIF-T0-UNITE01-D210-20261118.txt",
     DOSSIER / "TRIADE_gui_unite02_d210_v1"
     / "CORRECTIF-T0-UNITE01-D210-20261118.txt"),
]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def main():
    print("=== LA LIVRAISON AU COFFRE /test (recoup md5, échec fermé) ===")
    ent = ds.list_folder(TEST_ID)
    for nom, chemin in LIVRAISON:
        md5_local = md5(chemin)
        if nom in ent:
            if ent[nom].get("md5Checksum") == md5_local:
                print(f"[livraison] {nom} : DÉJÀ LIVRÉ byte-byte (md5 "
                      f"{md5_local[:8]}…)")
                continue
            ds.upload_update(ent[nom]["id"], chemin)
            action = "mis à jour"
        else:
            ds.upload_create(TEST_ID, nom, chemin)
            action = "téléversé"
        # LE RECOUP : la fiche relue doit porter le md5 local
        ent2 = ds.list_folder(TEST_ID)
        md5_distant = ent2.get(nom, {}).get("md5Checksum")
        ok = md5_distant == md5_local
        print(f"[livraison] {nom} : {action} ({chemin.stat().st_size} o), "
              f"md5 local {md5_local[:8]}… / distant "
              f"{str(md5_distant)[:8]}… {'MATCH' if ok else 'ÉCART'}")
        if not ok:
            raise SystemExit(f"[livraison] ÉCART md5 pour {nom}")
    print("[livraison] l'état final du /test (les entrées récentes) :")
    ent3 = ds.list_folder(TEST_ID)
    for nom in sorted(ent3):
        if "unite02-d210" in nom or "T0" in nom:
            print("  -", nom)


if __name__ == "__main__":
    main()
