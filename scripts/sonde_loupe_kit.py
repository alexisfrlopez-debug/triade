#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_loupe_kit.py — sonde lecture seule du dossier /test/loupe-kit
(le dépôt frais du développeur, le run dev.4 attendu) : liste récursive
et télécharge chaque pièce < 2 Mo vers download/loupe-kit-depôt/ (md5
recoupé par pièce)."""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/loupe-kit-depot")
VUS = set()


def arpente(folder_id: str, chemin: str, profondeur: int = 0) -> None:
    if profondeur > 4 or folder_id in VUS:
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
            if taille <= 2_000_000:
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
                    local = hashlib.md5(corps).hexdigest()
                    attendu = (f.get("md5Checksum") or "").lower()
                    etat = "OK" if (not attendu or local == attendu) else "ÉCART"
                    print(f"{'  ' * profondeur}  → {cible} "
                          f"({len(corps)} o) [{etat}]")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    racine = ds.list_folder(TEST_ID)
    kit = racine.get("loupe-kit")
    if not kit or kit.get("mimeType") != ds.FOLDER_MIME:
        print("[sonde] loupe-kit/ introuvable au /test", file=sys.stderr)
        return 2
    print("[DOSSIER] /test/loupe-kit/")
    arpente(kit["id"], "/test/loupe-kit", 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
