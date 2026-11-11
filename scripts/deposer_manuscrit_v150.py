#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_manuscrit_v150.py — LE MANUSCRIT v0.15.0 DÉPOSÉ EN CLAIR À LA
RACINE DU COFFRE (la demande du développeur « je ne trouve pas le manuscrit
v0.15 dans le drive » — le constat : la chaîne d'édition v0.15.0 fit vivre
le PDF sous le nom générique scripts/manuscrit_v150/main.pdf, la convention
docs/TRIADE_manuscrit_vX.pdf des cinq versions précédentes ROMPUE ; au
coffre le manuscrit n'existait qu'À L'INTÉRIEUR des zips).

Le geste : (1) l'empreinte sha256 recoupée AVANT tout (== la consignée à
empreintes_livrables_v0.15.0.txt : e8e075df… — le PDF de docs/ recopie
VÉRIFIÉE de scripts/manuscrit_v150/main.pdf) ; (2) le dépôt à la racine du
coffre (upload create, JAMAIS un écrasement silencieux — un doublon existant
serait REFUSÉ) ; (3) le recoup md5 APRÈS dépôt (list_folder relue).
Lecture seule partout ailleurs.
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

SOURCE = REPO / "docs" / "TRIADE_manuscrit_v0.15.0.pdf"
SHA_ATTENDU = ("e8e075df81fafd06ce0ab1799bceb83a014484507"
               "fc4e4a00edbc6b7dd986ec6")
NOM_DRIVE = "TRIADE_manuscrit_v0.15.0.pdf"


def sha256_fichier(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with chemin.open("rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def main() -> int:
    # (1) l'empreinte AVANT tout geste Drive
    sha = sha256_fichier(SOURCE)
    print(f"[déposer] sha256 local : {sha}")
    if sha != SHA_ATTENDU:
        sys.exit("[déposer] ÉCHEC : le PDF local ≠ l'empreinte consignée "
                 "(e8e075df…) — geste refusé")
    print("[déposer] empreinte == la consignée (empreintes_livrables_v0.15.0)")

    # (2) la racine ne doit PAS déjà porter le fichier (aucun écrasement)
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    if NOM_DRIVE in racine:
        meta = racine[NOM_DRIVE]
        md5_local = hashlib.md5(SOURCE.read_bytes()).hexdigest()
        if meta.get("md5Checksum") == md5_local:
            print(f"[déposer] DÉJÀ PRÉSENT au coffre avec le même md5 "
                  f"{md5_local[:8]}… — rien à faire (idempotent)")
            return 0
        sys.exit(f"[déposer] ÉCHEC : {NOM_DRIVE} existe au coffre avec un "
                 f"md5 DIFFÉRENT ({meta.get('md5Checksum', '?')[:8]}…) — "
                 "geste refusé (aucun écrasement silencieux)")

    # (3) le dépôt
    ds.upload_create(ds.DRIVE_ROOT_ID, NOM_DRIVE, SOURCE)
    print(f"[déposer] déposé : {NOM_DRIVE} ({SOURCE.stat().st_size} o)")

    # (4) le recoup APRÈS dépôt
    racine2 = ds.list_folder(ds.DRIVE_ROOT_ID)
    meta = racine2.get(NOM_DRIVE)
    if not meta:
        sys.exit("[déposer] ÉCHEC : le fichier absent après le dépôt")
    md5_local = hashlib.md5(SOURCE.read_bytes()).hexdigest()
    md5_drive = meta.get("md5Checksum", "")
    print(f"[déposer] recoup : md5 local {md5_local[:8]}… / "
          f"drive {md5_drive[:8]}…")
    if md5_local != md5_drive:
        sys.exit("[déposer] ÉCHEC : md5 divergent après le dépôt")
    print(f"[déposer] VERT — {NOM_DRIVE} en clair à la racine du coffre "
          f"(id={meta['id']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
