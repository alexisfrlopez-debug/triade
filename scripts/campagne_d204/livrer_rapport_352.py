#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_rapport_352.py — LA LIVRAISON DU RAPPORT DE RÉCEPTION du run v3 au
coffre /test : le RAPPORT-RECEPTION-RUN-UNITE16-D210-TERRAIN-V3-20261118.txt —
UN téléversement, recoupé par RE-TÉLÉCHARGEMENT byte-byte (md5 MATCH, échec
fermé). D143 : les kits v1/v2/v3 et leurs dépôts, les rapports précédents et
les livraisons de la 351 JAMAIS recouverts.

Usage : python3 scripts/campagne_d204/livrer_rapport_352.py
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

CAMP = pathlib.Path(__file__).resolve().parent
BAC = CAMP / "depot-run-unite16-d210-v3-352"

PIECES = [
    (BAC / "RAPPORT-RECEPTION-RUN-UNITE16-D210-TERRAIN-V3-20261118.txt",
     "RAPPORT-RECEPTION-RUN-UNITE16-D210-TERRAIN-V3-20261118.txt"),
]


def televerse_et_recoupe(parent_id: str, chemin: pathlib.Path,
                         nom_distant: str) -> bool:
    md5 = hashlib.md5(chemin.read_bytes()).hexdigest()
    entrees = ds.list_folder(parent_id)
    existant = entrees.get(nom_distant)
    if existant:
        if existant.get("md5Checksum") == md5:
            print(f"  [DÉJÀ VERT] {nom_distant} — md5 identique, rien à "
                  f"retéléverser")
            return True
        st = ds.upload_update(existant["id"], chemin)
        if st not in (200, 201):
            print(f"  [ÉCHEC] {nom_distant} : HTTP {st}", file=sys.stderr)
            return False
    else:
        ds.upload_create(parent_id, nom_distant, chemin)
    # LE RECOUP : re-téléchargement byte-byte
    entrees2 = ds.list_folder(parent_id)
    meta = entrees2.get(nom_distant)
    if not meta or meta.get("md5Checksum") != md5:
        print(f"  [ÉCHEC] {nom_distant} : le re-téléchargement diverge",
              file=sys.stderr)
        return False
    st, body, _ = ds.api("GET", ds.API + f"/files/{meta['id']}?alt=media")
    if st != 200 or hashlib.md5(body).hexdigest() != md5 \
            or body != chemin.read_bytes():
        print(f"  [ÉCHEC] {nom_distant} : le corps diverge", file=sys.stderr)
        return False
    print(f"  [MATCH] {nom_distant}  {chemin.stat().st_size} o  "
          f"md5={md5[:10]}… — re-téléchargé byte-byte")
    return True


def main() -> int:
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    test_id = racine["test"]["id"]
    print("=== LA LIVRAISON DU RAPPORT DE RÉCEPTION V3 au /test (UNE pièce) ===")
    echecs = 0
    for chemin, nom in PIECES:
        if not chemin.exists():
            print(f"  [ABSENT] {chemin}", file=sys.stderr)
            echecs += 1
            continue
        if not televerse_et_recoupe(test_id, chemin, nom):
            echecs += 1
    print(f"[BILAN] {'TOUT VERT — 1/1 MATCH byte-byte' if echecs == 0 else str(echecs) + ' ÉCHECS'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
