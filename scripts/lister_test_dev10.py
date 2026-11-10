#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 215 — lister les dossiers du /test Drive autour du run dev.10.

Liste récursivement : kit-loupe/, preuves-loupe/, loupe-kit-10/,
loupe-kit-11/ (max 3 niveaux) — pour situer les preuves du run
annoncées par le développeur (« dossier kit-loupe avec les preuves »).
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
CIBLES = ["kit-loupe", "preuves-loupe", "loupe-kit-10", "loupe-kit-11",
          "kit-loupe.zip"]


def liste(nom_ou_id, profondeur=0, prefix=""):
    entries = ds.list_folder(nom_ou_id)
    for name, f in sorted(entries.items()):
        if f["mimeType"] == ds.FOLDER_MIME:
            print(f"{prefix}[dossier] {name}/  (id={f['id']})")
            if profondeur < 3:
                liste(f["id"], profondeur + 1, prefix + "    ")
        else:
            md5 = f.get("md5Checksum", "-")
            print(f"{prefix}{name}  md5={md5[:12]}…  id={f['id']}")


def main():
    racine = ds.list_folder(TEST_ID)
    for cible in CIBLES:
        f = racine.get(cible)
        if not f:
            print(f"=== {cible} : ABSENT du /test ===")
            continue
        if f["mimeType"] == ds.FOLDER_MIME:
            print(f"=== {cible}/ (id={f['id']}) ===")
            liste(f["id"])
        else:
            print(f"=== {cible} (fichier, md5={f.get('md5Checksum','-')[:12]}…) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
