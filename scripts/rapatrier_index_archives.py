#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_index_archives.py — lecture seule : rapatrie l'index
LISEZMOI-archives-preuves.txt (pour mise à jour par archiver_run_e2.py).

Usage : python3 scripts/rapatrier_index_archives.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


def main() -> int:
    test = ds.list_folder(TEST_ID)
    arch = ds.list_folder(test["archives-preuves"]["id"])
    f = arch.get("LISEZMOI-archives-preuves.txt")
    if not f:
        print("[index] ABSENT", file=sys.stderr)
        return 2
    url = f"{ds.API}/files/{f['id']}?alt=media"
    st, corps, _ = ds.api("GET", url)
    dest = REPO / "upload" / "LISEZMOI-archives-preuves.txt"
    dest.write_bytes(corps)
    md5 = ds.md5_of(dest)
    print(f"[index] rapatrié : {dest} ({len(corps)} o, md5 {md5[:8]}…, "
          f"distant {f.get('md5Checksum', '-')[:8]}…)")
    return 0 if md5 == f.get("md5Checksum") else 1


if __name__ == "__main__":
    sys.exit(main())
