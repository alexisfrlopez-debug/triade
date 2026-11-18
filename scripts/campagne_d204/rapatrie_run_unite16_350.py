#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrie_run_unite16_350.py — le rapatriement du refus : le dépôt
kit-unite-04-d210-20261118/ du /test (les pièces nées du run) + les QUATRE
registres de l'atelier re-déposé. DOUBLE téléchargement byte-byte (md5 ==
la métadonnée Drive, échec fermé). Lecture seule du coffre.

Usage : python3 scripts/campagne_d204/rapatrie_run_unite16_350.py
"""

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = pathlib.Path(__file__).resolve().parent / "depot-run-unite16-d210-350" / "epreuves"


def telecharge(file_id: str, dest: pathlib.Path, md5_attendu: str) -> bool:
    st, body, _ = ds.api("GET", ds.API + f"/files/{file_id}?alt=media")
    if st != 200:
        print(f"  [ÉCHEC] {dest.name} : HTTP {st}", file=sys.stderr)
        return False
    m1 = hashlib.md5(body).hexdigest()
    st2, body2, _ = ds.api("GET", ds.API + f"/files/{file_id}?alt=media")
    if st2 != 200 or body2 != body:
        print(f"  [ÉCHEC] {dest.name} : le second téléchargement diverge", file=sys.stderr)
        return False
    m2 = hashlib.md5(body2).hexdigest()
    if m1 != md5_attendu or m2 != m1:
        print(f"  [ÉCHEC] {dest.name} : md5 {m1[:10]}… != métadonnée {md5_attendu[:10]}…",
              file=sys.stderr)
        return False
    dest.write_bytes(body)
    print(f"  [OK] {dest.relative_to(BAC)}  {len(body):>7} o  md5={m1[:10]}…")
    return True


def main() -> int:
    BAC.mkdir(parents=True, exist_ok=True)
    (BAC / "atelier").mkdir(exist_ok=True)
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    test = ds.list_folder(racine["test"]["id"])

    cibles = [
        ("kit-unite-04-d210-20261118", [
            "run-console-unite16-d210-20261118-121219.txt",
            "etat-run-unite16-d210.json",
            "Capture.JPG",
        ], BAC),
        ("kit-unite-04-d210-20261118", ["TRIADE_logs/session-20261118-121155.txt"],
         BAC / "TRIADE_logs"),
        ("atelier-campagne-d204-20261114-013520", [
            "livraisons.csv", "carnet_temps_humain.csv",
            "defauts.csv", "journal-ouverture.txt",
        ], BAC / "atelier"),
    ]

    echecs = 0
    for dossier, chemins, dest_dir in cibles:
        entrees = ds.list_folder(test[dossier]["id"])
        for chemin in chemins:
            if "/" in chemin:  # sous-dossier (TRIADE_logs)
                sous, nom = chemin.split("/", 1)
                sous_ent = ds.list_folder(entrees[sous]["id"])
                if nom not in sous_ent:
                    print(f"  [ABSENT] {dossier}/{chemin}", file=sys.stderr)
                    echecs += 1
                    continue
                dest_dir.mkdir(parents=True, exist_ok=True)
                meta = sous_ent[nom]
                if not telecharge(meta["id"], dest_dir / nom, meta.get("md5Checksum", "")):
                    echecs += 1
                continue
            if chemin not in entrees:
                print(f"  [ABSENT] {dossier}/{chemin}", file=sys.stderr)
                echecs += 1
                continue
            dest_dir.mkdir(parents=True, exist_ok=True)
            meta = entrees[chemin]
            if not telecharge(meta["id"], dest_dir / chemin, meta.get("md5Checksum", "")):
                echecs += 1

    print(f"[BILAN] {'TOUT VERT' if echecs == 0 else str(echecs) + ' ÉCHECS'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
