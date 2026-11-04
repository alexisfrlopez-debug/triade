#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_preuves_e2.py — lecture seule : rapatrie les pièces du run e2
depuis /test/preuves-m5b et les documents de la vague e2 depuis /test
(LISEZMOI, scénario, kit), md5 recoupés par relecture.

Usage : python3 scripts/rapatrier_preuves_e2.py
Code de sortie : 0 = tout conforme, 1 = écart nommé, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST_PREUVES = REPO / "upload" / "preuves-e2"
DEST_VAGUE = REPO / "upload" / "vague-e2"


def telecharger(file_id: str, destination: pathlib.Path) -> str:
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)
    return ds.md5_of(destination)


def rapatrie(dossier_id: str, noms: list, dest: pathlib.Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    entrees = ds.list_folder(dossier_id)
    ecarts = 0
    for nom in noms:
        f = entrees.get(nom)
        if not f:
            print(f"[e2] PIÈCE ABSENTE : {nom} (attendue)", file=sys.stderr)
            ecarts += 1
            continue
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"[e2] ignoré (dossier) : {nom}")
            continue
        md5_distant = f.get("md5Checksum", "-")
        destination = dest / nom
        md5_local = telecharger(f["id"], destination)
        ok = md5_local == md5_distant
        print(f"[e2] {nom} : {f.get('size', '?')} o, "
              f"md5 {md5_local[:8]}… {'MATCH' if ok else 'ÉCART'}")
        if not ok:
            ecarts += 1
    return ecarts


def main() -> int:
    try:
        test = ds.list_folder(TEST_ID)
        preuves_id = test["preuves-m5b"]["id"]
    except Exception as exc:  # noqa: BLE001
        print(f"[e2] ERREUR FATALE : listage impossible : {exc}", file=sys.stderr)
        return 2
    ecarts = 0
    # Les pièces du run (tout ce qui traîne dans preuves-m5b)
    pieces = sorted(n for n, m in ds.list_folder(preuves_id).items()
                    if m.get("mimeType") != ds.FOLDER_MIME)
    print(f"[e2] preuves-m5b : {len(pieces)} pièce(s) à rapatrier")
    ecarts += rapatrie(preuves_id, pieces, DEST_PREUVES)
    # Les documents de la vague e2
    ecarts += rapatrie(TEST_ID,
                       ["LISEZMOI-m5b-e2.txt", "scenario-m5b-e2.ps1",
                        "m5b-kit-e2.zip"], DEST_VAGUE)
    if ecarts == 0:
        print("[e2] RAPATRIEMENT CONFORME — pièces disponibles localement")
        return 0
    print(f"[e2] {ecarts} écart(s) nommé(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
