#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_coffre_test_221.py — sonde lecture seule du coffre /test ENTIER
après l'annonce du développeur (le dépôt /kit-loupe du douzième run
attendu) : listing récursif complet, aucune écriture, aucun téléchargement.
Le constat de l'état AVANT tout geste — la règle des sessions parallèles
(D178 : la pointe est la canonique, le coffre se constate avant de bouger)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
VUS = set()


def arpente(folder_id: str, chemin: str, profondeur: int = 0) -> None:
    if profondeur > 5 or folder_id in VUS:
        return
    VUS.add(folder_id)
    pieces = ds.list_folder(folder_id)
    for nom, f in sorted(pieces.items()):
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"{'  ' * profondeur}[DOSSIER] {chemin}/{nom}/")
            arpente(f["id"], f"{chemin}/{nom}", profondeur + 1)
        else:
            taille = int(f.get("size", 0) or 0)
            md5 = (f.get("md5Checksum") or "")[:8]
            print(f"{'  ' * profondeur}[fichier] {chemin}/{nom} — "
                  f"{taille} o, md5 {md5}…, id {f['id']}")


def main() -> int:
    print("[sonde] listing intégral du coffre /test — lecture seule")
    arpente(TEST_ID, "/test")
    print(f"[sonde] {len(VUS)} dossiers arpentés")
    return 0


if __name__ == "__main__":
    sys.exit(main())
