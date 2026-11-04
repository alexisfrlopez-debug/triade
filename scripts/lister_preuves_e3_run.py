#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lister_preuves_e3_run.py — lecture seule : liste le coffre /test/preuves-m5b
(run e3 attendu) avec id/taille/md5. Aucune écriture, aucun secret affiché.

Usage : python3 /home/z/my-project/scripts/lister_preuves_e3_run.py
"""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade-repo")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402


def main() -> int:
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    test = racine.get("test")
    if not test or test.get("mimeType") != ds.FOLDER_MIME:
        print("ERREUR : /test absent de la racine", file=sys.stderr)
        return 1
    entrees_test = ds.list_folder(test["id"])
    preuves = entrees_test.get("preuves-m5b")
    if not preuves or preuves.get("mimeType") != ds.FOLDER_MIME:
        print("ERREUR : /test/preuves-m5b absent", file=sys.stderr)
        return 1
    entrees = ds.list_folder(preuves["id"])
    print(f"=== /test/preuves-m5b ({len(entrees)} entrées) ===")
    for nom_f, meta in sorted(entrees.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR ] {nom_f}  id={meta['id']}")
        else:
            print(f"  [{meta.get('size', '?'):>7} o] {nom_f}  "
                  f"md5={meta.get('md5Checksum', '-')[:8]}…  id={meta['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
