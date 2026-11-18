#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_correctif_350.py — LA LIVRAISON DU CORRECTIF au coffre /test :
le kit v2 (le zip) + le LISEZMOI-RUN v2 + l'EMPREINTES-GUI v2 + le
CORRECTIF + le RAPPORT-RECEPTION — CINQ téléversements, chacun recoupé
par RE-TÉLÉCHARGEMENT byte-byte (md5 MATCH, échec fermé). D143 : le kit
v1 et son dépôt de refus JAMAIS recouverts.

Usage : python3 scripts/campagne_d204/livrer_correctif_350.py
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

CAMP = pathlib.Path(__file__).resolve().parent
KIT2 = CAMP / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v2"

PIECES = [
    (CAMP / "kit-gui-1clic-unite16-d210-v2-20261118.zip",
     "kit-gui-1clic-unite16-d210-v2-20261118.zip"),
    (KIT2 / "LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt",
     "LISEZMOI-RUN-UNITE16-D210-1CLIC-V2.txt"),
    (KIT2 / "EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt",
     "EMPREINTES-GUI-UNITE16-D210-1CLIC-V2.txt"),
    (CAMP / "CORRECTIF-UNITE16-D210-20261118.txt",
     "CORRECTIF-UNITE16-D210-20261118.txt"),
    (CAMP / "RAPPORT-RECEPTION-RUN-UNITE16-D210-TERRAIN-20261118.txt",
     "RAPPORT-RECEPTION-RUN-UNITE16-D210-TERRAIN-20261118.txt"),
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
    print("=== LA LIVRAISON DU CORRECTIF au /test (CINQ pièces) ===")
    echecs = 0
    for chemin, nom in PIECES:
        if not televerse_et_recoupe(test_id, chemin, nom):
            echecs += 1
    print(f"[BILAN] {'TOUT VERT — 5/5 MATCH byte-byte' if echecs == 0 else str(echecs) + ' ÉCHECS'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
