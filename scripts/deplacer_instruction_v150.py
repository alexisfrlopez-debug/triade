#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Correction du croisement d'attribution ic09ydeli ↔ ysddxpk0o (12/11).

Faits constatés (métadonnées Drive, jamais modifiés depuis le dépôt du 11/11
13:21 UTC) :
  - Qwen_text_20261111_ysddxpk0o.txt  contient le programme v0.14.0 (bras de
    référence, RQ2, indépendance, survivants) — programme EXÉCUTÉ (E227/E228,
    D193–D195) ;
  - Qwen_text_20261111_ic09ydeli.txt  contient le programme v0.15.0 (modèle
    formel non borné, kits matériels, réplication, statuts) — programme OUVERT
    (E229/D196), NON achevé.

Gestes correctifs (déplacement uniquement, empreinte recoupée, aucune
suppression — la règle du développeur : l'instruction s'archive APRÈS
exécution) :
  1. ysddxpk0o : /instructions → /ARCHIVE   (programme exécuté, archive dûe) ;
  2. ic09ydeli : /ARCHIVE     → /instructions (programme en cours, rappel de
     l'archive prématurée d'hier — il sera archivé à la clôture v0.15.0).
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

INSTR_ID = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"   # dossier /instructions
ARCHIVE_ID = "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr"  # dossier /ARCHIVE

GESTES = [
    # (file_id, nom, parent_source, parent_dest, md5 attendu, libellé)
    ("1n4vVoSBxJES5mNeUAjTMOx4aPfMbfWio",
     "Qwen_text_20261111_ysddxpk0o.txt",
     INSTR_ID, ARCHIVE_ID,
     "c33b2c70ba07e6e8a1730704a2b29fcc",
     "ysddxpk0o : /instructions → /ARCHIVE (programme v0.14.0 exécuté)"),
    ("1PgMdDhsVKwk-RUgLTNML3g3GGHC89vL0",
     "Qwen_text_20261111_ic09ydeli.txt",
     ARCHIVE_ID, INSTR_ID,
     "0970bbeabf230c9d6908930150c9bd86",
     "ic09ydeli : /ARCHIVE → /instructions (programme v0.15.0 en cours, "
     "rappel de l'archivage prématuré)"),
]


def verifier_dossier(folder_id, nom_attendu, md5_attendu):
    """Recoupe la présence du fichier et son empreinte dans folder_id."""
    ent = ds.list_folder(folder_id)
    f = ent.get(nom_attendu)
    if not f:
        raise ds.SyncError(f"'{nom_attendu}' INTROUVABLE après déplacement")
    md5 = f.get("md5Checksum", "")
    if md5 != md5_attendu:
        raise ds.SyncError(
            f"empreinte divergente pour '{nom_attendu}' : {md5} != {md5_attendu}")
    return f["id"]


def main():
    ok = 0
    for file_id, nom, src, dst, md5_att, libelle in GESTES:
        # 0) l'empreinte AVANT le geste (dans le dossier source)
        fid_avant = verifier_dossier(src, nom, md5_att)
        assert fid_avant == file_id, f"id divergent pour {nom}"
        # 1) déplacement (aucun contenu modifié)
        url = (f"{ds.API}/files/{file_id}?"
               + "addParents=" + dst
               + "&removeParents=" + src)
        st, body, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            raise ds.SyncError(f"déplacement '{nom}' impossible "
                               f"(HTTP {st}) : {body[:200]!r}")
        # 2) recoup APRÈS le geste (dans le dossier destination)
        verifier_dossier(dst, nom, md5_att)
        # 3) le fichier ne doit plus être dans le dossier source
        ent_src = ds.list_folder(src)
        if nom in ent_src:
            raise ds.SyncError(f"'{nom}' demeure dans le dossier source")
        print(f"OK  {libelle}")
        print(f"    md5 recoupé avant/après : {md5_att}")
        ok += 1
    print(f"--- {ok}/{len(GESTES)} gestes exécutés ---")


if __name__ == "__main__":
    main()
