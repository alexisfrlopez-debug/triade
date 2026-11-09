#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_loupe_arborescence.py — sonde lecture seule : arpente /test
sous-dossier par sous-dossier (loupe-kit/ surtout — le dépôt frais du
développeur), télécharge chaque pièce de moins de 2 Mo vers
download/sonde-arborescence/ (md5 recoupé)."""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/sonde-arborescence")
VUS = set()


def arpente(folder_id: str, chemin: str, profondeur: int = 0) -> None:
    if profondeur > 3 or folder_id in VUS:
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
                  f"{taille} o, md5 {md5}…")
            if taille <= 2_000_000 and profondeur > 0:
                url = f"{ds.API}/files/{f['id']}?alt=media"
                try:
                    st, corps, _ = ds.api("GET", url)
                except Exception as exc:  # noqa: BLE001
                    print(f"{'  ' * profondeur}  ÉCHEC : {exc}")
                    continue
                if st == 200:
                    safe = chemin.strip("/").replace("/", "_")
                    local_dir = DEST / safe
                    local_dir.mkdir(parents=True, exist_ok=True)
                    cible = local_dir / nom
                    cible.write_bytes(corps)
                    ok = hashlib.md5(corps).hexdigest() == (f.get("md5Checksum") or "").lower()
                    print(f"{'  ' * profondeur}  → {cible} "
                          f"[{'OK' if ok else 'ÉCART'}]")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    racine = ds.list_folder(TEST_ID)
    for nom, f in sorted(racine.items()):
        if f.get("mimeType") == ds.FOLDER_MIME and nom in (
                "loupe-kit", "preuves-loupe", "archives-preuves",
                "archives-livraisons"):
            print(f"[DOSSIER] /test/{nom}/")
            arpente(f["id"], f"/test/{nom}", 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
