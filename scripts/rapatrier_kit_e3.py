#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_kit_e3.py — rapatrie le kit e3 COURANT du coffre /test
(m5b-kit-e3.zip) vers download/vague-e4/base/, md5 contrôlé contre la valeur
CONSIGNÉE par l'assembleur e3 (Entrée 139 : 981b1a5b…) — la base du kit e4
est le kit e3 LIVRÉ, le coffre fait foi.

Lecture seule. Usage : python3 scripts/rapatrier_kit_e3.py
Code de sortie : 0 = base conforme ; 1 = écart nommé ; 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur
DEST = pathlib.Path("/home/z/my-project/download/vague-e4/base")

MD5_ATTESTE = "981b1a5b14e75a77207df32ca7c8d4c9"  # Entrée 139 (assembleur e3)


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        entries = ds.list_folder(TEST_ID)
    except Exception as exc:  # noqa: BLE001
        print(f"[kit-e3] ERREUR FATALE : listage /test impossible : {exc}",
              file=sys.stderr)
        return 2
    f = entries.get("m5b-kit-e3.zip")
    if not f:
        print("[kit-e3] ERREUR : m5b-kit-e3.zip ABSENT de la racine /test "
              "(la vague e3 n'est plus courante ?)", file=sys.stderr)
        return 2
    md5_distant = (f.get("md5Checksum") or "").lower()
    print(f"[kit-e3] racine /test : m5b-kit-e3.zip {f.get('size', '?')} o, "
          f"md5 distant {md5_distant[:12]}…")
    if not md5_distant.startswith(MD5_ATTESTE):
        print(f"[kit-e3] ÉCART NOMMÉ : md5 distant {md5_distant} != "
              f"attesté {MD5_ATTESTE} — la base a divergé", file=sys.stderr)
        return 1
    st, body, _ = ds.api("GET", f"{ds.API}/files/{f['id']}?alt=media")
    if st != 200:
        print(f"[kit-e3] ERREUR : téléchargement impossible (HTTP {st})",
              file=sys.stderr)
        return 2
    chemin = DEST / "m5b-kit-e3.zip"
    chemin.write_bytes(body)
    local = ds.md5_of(chemin)
    if local != MD5_ATTESTE:
        print(f"[kit-e3] ÉCART : md5 local {local} != attesté {MD5_ATTESTE}",
              file=sys.stderr)
        return 1
    print(f"[kit-e3] OK : {chemin} ({len(body)} o, md5 {local[:12]}… — "
          f"la base du kit e4 est le kit e3 LIVRÉ, recoupé)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
