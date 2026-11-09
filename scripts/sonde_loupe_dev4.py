#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_loupe_dev4.py — sonde lecture seule du coffre /test : liste
preuves-loupe/ (le dépôt du développeur, run dev.4 attendu) et télécharge
les pièces vers download/preuves-run-loupe-dev4/ (md5 recoupé par pièce).
Modèle rapatrier_preuves_m9f.py — aucune écriture Drive."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-loupe-dev4")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    test = ds.list_folder(TEST_ID)
    print("== /test (racine) ==")
    for nom, f in sorted(test.items()):
        typ = "DOSSIER" if f.get("mimeType") == ds.FOLDER_MIME else "fichier"
        taille = f.get("size", "")
        print(f"  [{typ}] {nom} {taille}")
    receptacle = test.get("preuves-loupe")
    if not receptacle or receptacle.get("mimeType") != ds.FOLDER_MIME:
        print("[sonde] ERREUR : preuves-loupe/ introuvable au /test",
              file=sys.stderr)
        return 2
    pieces = ds.list_folder(receptacle["id"])
    print("\n== /test/preuves-loupe (le réceptacle) ==")
    if not pieces:
        print("  (vide)")
    for nom, f in sorted(pieces.items()):
        typ = "DOSSIER" if f.get("mimeType") == ds.FOLDER_MIME else "fichier"
        md5 = (f.get("md5Checksum") or "")[:8]
        print(f"  [{typ}] {nom} — {f.get('size', '?')} o, md5 {md5}…")
        if typ == "fichier":
            url = f"{ds.API}/files/{f['id']}?alt=media"
            st, corps, _ = ds.api("GET", url)
            if st != 200:
                print(f"    ÉCHEC téléchargement (HTTP {st})")
                continue
            chemin = DEST / nom
            chemin.write_bytes(corps)
            local = __import__("hashlib").md5(corps).hexdigest()
            attendu = (f.get("md5Checksum") or "").lower()
            etat = "OK" if (not attendu or local == attendu) else "ÉCART"
            print(f"    rapatrié → {chemin} ({len(corps)} o, "
                  f"md5 {local[:8]}…) [{etat}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
