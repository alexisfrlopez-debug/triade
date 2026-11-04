#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lister_drive.py — lecture seule : liste la racine du coffre Drive « Triade »,
le dossier /test et (s'il existe) le coffre preuves-m5b, avec id/taille/md5.
Aucune écriture, aucun secret affiché.

Usage : python3 scripts/lister_drive.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402


def affiche(nom: str, dossier_id: str) -> dict:
    try:
        entrees = ds.list_folder(dossier_id)
    except Exception as exc:  # noqa: BLE001
        print(f"[{nom}] ERREUR : {exc}", file=sys.stderr)
        return {}
    print(f"=== {nom} ({len(entrees)} entrées) ===")
    for nom_f, meta in sorted(entrees.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR ] {nom_f}  id={meta['id']}")
        else:
            print(f"  [{meta.get('size', '?'):>7} o] {nom_f}  "
                  f"md5={meta.get('md5Checksum', '-')[:8]}…  id={meta['id']}")
    return entrees


def main() -> int:
    racine = affiche("RACINE /Triade", ds.DRIVE_ROOT_ID)
    for cible in ("test", "preuves-m5b", "preuves-samu"):
        if cible in racine and racine[cible].get("mimeType") == ds.FOLDER_MIME:
            affiche(f"/{cible}", racine[cible]["id"])
        else:
            print(f"=== /{cible} : ABSENT de la racine ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
