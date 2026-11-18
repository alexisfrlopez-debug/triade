#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_test_351.py — la sonde du refus v2 : liste le /test du coffre et le dépôt
du re-run de l'unité 4 D210 (kit-unite-04-d210-20261118-v2/) — lecture seule,
récursive, avec id/taille/md5. Aucun secret affiché.

Usage : python3 scripts/campagne_d204/sonde_test_351.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402


def parcourt(nom: str, dossier_id: str, prefix: str = "", profondeur: int = 0):
    try:
        entrees = ds.list_folder(dossier_id)
    except Exception as exc:  # noqa: BLE001
        print(f"[{nom}] ERREUR : {exc}", file=sys.stderr)
        return
    print(f"=== {nom} ({len(entrees)} entrées) ===")
    for nom_f, meta in sorted(entrees.items()):
        rel = prefix + nom_f
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR ] {rel}  id={meta['id']}")
            if profondeur < 3:
                parcourt(rel, meta["id"], rel + "/", profondeur + 1)
        else:
            print(f"  [{meta.get('size', '?'):>8} o] {rel}  "
                  f"md5={meta.get('md5Checksum', '-')[:10]}…  id={meta['id']}")


def main() -> int:
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    test_id = racine["test"]["id"]
    parcourt("/test", test_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
