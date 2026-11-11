#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Archiver le QUATRIÈME fichier d'instruction (Qwen_text_20261111_f3q3x9i7n.txt,
exécuté — les corrections de l'édition v0.13.0) : DÉPLACEMENT de /instructions
vers ARCHIVE/ (le modèle D76 : aucune suppression, le md5 recoupé après le
déplacement), puis DÉPÔT des deux livrables de l'édition à la racine du
coffre (le coffre de livraison ne porte que les courants)."""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

FICHIER = "Qwen_text_20261111_f3q3x9i7n.txt"
LIVRABLES = [
    ("TRIADE_soumission_v0.13.0.zip",
     REPO / "download" / "edition_v0130" / "TRIADE_soumission_v0.13.0.zip"),
    ("TRIADE_complet_v0.13.0.zip",
     REPO / "download" / "edition_v0130" / "TRIADE_complet_v0.13.0.zip"),
    ("empreintes_livrables_v0.13.0.txt",
     REPO / "download" / "edition_v0130" / "empreintes_livrables.txt"),
]

INSTR_ID = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
racine_instr = ds.list_folder(INSTR_ID)
instr_id = racine_instr.get(FICHIER, {}).get("id")
if not instr_id:
    print(f"[archive] {FICHIER} introuvable à /instructions (déjà archivé ?)")
else:
    md5_avant = racine_instr[FICHIER].get("md5Checksum")
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    archive_id = None
    for nom, meta in racine.items():
        if meta.get("mimeType") == ds.FOLDER_MIME and nom == "ARCHIVE":
            archive_id = meta["id"]
    if not archive_id:
        raise SystemExit("[archive] dossier ARCHIVE/ introuvable")
    url = (f"{ds.API}/files/{instr_id}?addParents={archive_id}"
           f"&removeParents={INSTR_ID}")
    st, corps, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise SystemExit(f"[archive] déplacement impossible (HTTP {st})")
    apres = ds.list_folder(archive_id).get(FICHIER, {})
    md5_apres = apres.get("md5Checksum")
    print(f"[archive] {FICHIER} -> ARCHIVE/ : md5 avant "
          f"{str(md5_avant)[:8]}… / après {str(md5_apres)[:8]}… "
          f"{'MATCH' if md5_avant == md5_apres else 'ÉCART'}")
    if md5_avant != md5_apres:
        raise SystemExit("[archive] ÉCART md5 — le déplacement a bougé un octet")
    restants = ds.list_folder(INSTR_ID)
    print(f"[archive] /instructions demeure : {sorted(restants)} "
          "(les instructions restantes)")


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
