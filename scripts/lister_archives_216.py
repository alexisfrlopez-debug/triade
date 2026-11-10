#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 216 — lister archives-preuves/ et vagues-m10/ (le patron de nommage)."""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


def main():
    racine = ds.list_folder(TEST_ID)
    for nom in ("archives-preuves", "archives-livraisons"):
        f = racine.get(nom)
        print(f"=== {nom}/ (id={f['id'] if f else 'ABSENT'}) ===")
        if not f:
            continue
        for n, e in sorted(ds.list_folder(f["id"]).items()):
            if e["mimeType"] == ds.FOLDER_MIME:
                print(f"  [dossier] {n}/  id={e['id']}")
            else:
                print(f"  {n}  md5={e.get('md5Checksum','-')[:12]}…  id={e['id']}")
    v = ds.list_folder(racine["archives-livraisons"]["id"])
    vg = v.get("vagues-m10")
    print(f"=== vagues-m10/ (id={vg['id'] if vg else 'ABSENT'}) ===")
    if vg:
        for n, e in sorted(ds.list_folder(vg["id"]).items()):
            print(f"  {n}  md5={e.get('md5Checksum','-')[:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
