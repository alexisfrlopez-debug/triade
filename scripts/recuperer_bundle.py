#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Récupération du bundle d'historique git depuis le coffre Drive.

Contexte (D61) : l'environnement local a été restauré à un état antérieur
(ère D54) alors que le coffre Drive avait déjà été synchronisé à l'état
le plus récent par le hook post-commit. Le bundle triade-history.bundle
poussé dans le dossier TRIADE/ du coffre contient donc l'historique git
COMPLET jusqu'au dernier commit synchronisé — c'est la source de vérité
de secours.

Ce script :
  - localise triade-history.bundle dans le coffre Drive (dossier TRIADE/) ;
  - le télécharge vers upload/ (zone hors dépôt) ;
  - affiche taille + md5 pour vérification avant tout git fetch.

Usage :
  python3 scripts/recuperer_bundle.py
Code de sortie : 0 = succès, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DEST = pathlib.Path("/home/z/my-project/upload/triade-history-recup.bundle")


def main():
    try:
        cache = {}
        triade_id = ds.ensure_folder(ds.DRIVE_ROOT_ID, ds.PROJECT_FOLDER, cache)

        # recherche récursive du bundle sous TRIADE/
        trouve = None

        def walk(fid, prefix):
            nonlocal trouve
            for name, f in ds.list_folder(fid).items():
                if f["mimeType"] == ds.FOLDER_MIME:
                    walk(f["id"], prefix + name + "/")
                elif name == ds.BUNDLE_NAME:
                    trouve = (prefix + name, f)

        walk(triade_id, "")
        if not trouve:
            print("[Bundle] ERREUR FATALE : triade-history.bundle introuvable "
                  "dans le coffre Drive", file=sys.stderr)
            return 2

        chemin, f = trouve
        print(f"[Bundle] trouvé : TRIADE/{chemin}  "
              f"({int(f.get('size', 0)):,} o, modifié {f.get('modifiedTime', '?')})"
              .replace(",", " "))
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[Bundle] ERREUR FATALE : téléchargement impossible ({st})",
                  file=sys.stderr)
            return 2
        DEST.write_bytes(body)
        md5 = ds.md5_of(DEST)
        distant = f.get("md5Checksum", "-")
        etat = "MATCH" if md5 == distant else f"DIVERGE ({md5} != {distant})"
        print(f"[Bundle] téléchargé : {DEST}  "
              f"({DEST.stat().st_size:,} o, md5 {md5[:12]}…)".replace(",", " "))
        print(f"[Bundle] intégrité : {etat}")
        return 0
    except ds.SyncError as e:
        print(f"[Bundle] ERREUR FATALE : {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
