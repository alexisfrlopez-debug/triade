#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Archiver le CINQUIÈME fichier (Qwen_text_20261111_ic09ydeli.txt, exécuté
— le programme empirique v0.14.0 MENÉ À TERME) : DÉPLACEMENT vers ARCHIVE/
(md5 recoupé), puis DÉPÔT des livrables à la racine du coffre."""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

FICHIER = "Qwen_text_20261111_ic09ydeli.txt"
LIVRABLES = [
    ("TRIADE_soumission_v0.14.0.zip",
     REPO / "download" / "edition_v0140" / "TRIADE_soumission_v0.14.0.zip"),
    ("TRIADE_complet_v0.14.0.zip",
     REPO / "download" / "edition_v0140" / "TRIADE_complet_v0.14.0.zip"),
    ("empreintes_livrables_v0.14.0.txt",
     REPO / "download" / "edition_v0140" / "empreintes_livrables.txt"),
]
INSTR_ID = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"

racine_instr = ds.list_folder(INSTR_ID)
instr_id = racine_instr.get(FICHIER, {}).get("id")
if not instr_id:
    print(f"[archive] {FICHIER} introuvable à /instructions (déjà archivé ?)")
else:
    md5_avant = racine_instr[FICHIER].get("md5Checksum")
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    archive_id = next(m["id"] for n, m in racine.items()
                      if m.get("mimeType") == ds.FOLDER_MIME and n == "ARCHIVE")
    url = (f"{ds.API}/files/{instr_id}?addParents={archive_id}"
           f"&removeParents={INSTR_ID}")
    st, corps, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise SystemExit(f"[archive] déplacement impossible (HTTP {st})")
    md5_apres = ds.list_folder(archive_id).get(FICHIER, {}).get("md5Checksum")
    print(f"[archive] {FICHIER} -> ARCHIVE/ : md5 "
          f"{str(md5_avant)[:8]}…/{str(md5_apres)[:8]}… "
          f"{'MATCH' if md5_avant == md5_apres else 'ÉCART'}")
    if md5_avant != md5_apres:
        raise SystemExit("[archive] ÉCART md5")
    restants = ds.list_folder(INSTR_ID)
    print(f"[archive] /instructions demeure : {sorted(restants)}")


def upload_update_or_create(parent_id, chemin, nom):
    ent = ds.list_folder(parent_id)
    if nom in ent:
        ds.upload_update(ent[nom]["id"], chemin)
    else:
        ds.upload_create(parent_id, nom, chemin)


for nom, chemin in LIVRABLES:
    upload_update_or_create(ds.DRIVE_ROOT_ID, chemin, nom)
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    md5_local = ds.md5_of(chemin)
    md5_distant = racine.get(nom, {}).get("md5Checksum")
    print(f"[livraison] {nom} : {chemin.stat().st_size} o, "
          f"md5 {md5_local[:8]}… / distant {str(md5_distant)[:8]}… "
          f"{'MATCH' if md5_local == md5_distant else 'ÉCART'}")
