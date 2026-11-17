#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_miroir_ciblee_337.py — LA MISE À JOUR CIBLÉE DU MIROIR DRIVE pour
la session 336+337 (le geste établi des livrer_* : les fonctions de
drive_sync, upload + recoup md5) : LE BUNDLE rafraîchi, les fichiers
NOUVEAUX du delta git 6602db5..HEAD, les fichiers d'instruction racine.
L'arriéré du miroir (les pièces d'époques passées jamais téléversées)
demeure nommé : la synchro complète (idempotente) le résorbera aux
gestes futurs — le présent geste livre la POINTE."""
import hashlib
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DEPUIS = "6602db5"  # la pointe GitHub avant la présente session (l'Entrée 335)


def md5_of(p):
    return ds.md5_of(p)


def main():
    # LE BUNDLE (l'historique restaurable)
    import tempfile
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="bundle337_"))
    bundle = ds.build_bundle(tmp)
    assert bundle is not None, "aucun commit — le bundle impossible"

    # LE DELTA : les fichiers nouveaux/modifiés de la présente session
    out = subprocess.run(["git", "diff", "--name-only", DEPUIS + "..HEAD"],
                         cwd=REPO, capture_output=True, check=True)
    delta = [n for n in out.stdout.decode().splitlines() if n.strip()]
    # le worklog et OU-TROUVER sont des fichiers suivis — déjà dans le delta

    cache = {}
    triade_id = ds.ensure_folder(ds.DRIVE_ROOT_ID, ds.PROJECT_FOLDER, cache)

    remote = {}

    def walk_remote(fid, prefix):
        for f in ds.list_folder(fid).values():
            if f["mimeType"] == ds.FOLDER_MIME:
                walk_remote(f["id"], prefix + f["name"] + "/")
            else:
                remote[prefix + f["name"]] = f

    walk_remote(triade_id, "")

    # 1· LE BUNDLE
    r = remote.get(ds.BUNDLE_NAME)
    md5_local = md5_of(bundle)
    if r and r.get("md5Checksum") == md5_local:
        print(f"[miroir] le bundle : DÉJÀ en place (md5 {md5_local[:8]}…)")
    else:
        if r:
            ds.upload_update(r["id"], bundle)
        else:
            ds.upload_create(triade_id, ds.BUNDLE_NAME, bundle)
        md5_distant = ds.list_folder(triade_id).get(
            ds.BUNDLE_NAME, {}).get("md5Checksum")
        print(f"[miroir] le bundle : {'MIS À JOUR' if r else 'TÉLÉVERSÉ'} "
              f"({bundle.stat().st_size} o), md5 local {md5_local[:8]}… / "
              f"distant {str(md5_distant)[:8]}… "
              f"{'MATCH' if md5_distant == md5_local else 'ÉCART'}")
        if md5_distant != md5_local:
            raise SystemExit("[miroir] ÉCART md5 au bundle")

    # 2· LES FICHIERS DU DELTA
    verts, ecarts = 0, []
    for rel in sorted(delta):
        p = REPO / rel
        if not p.is_file():
            continue
        md5_local = md5_of(p)
        r = remote.get(rel)
        if r and r.get("md5Checksum") == md5_local:
            verts += 1
            continue
        parts = pathlib.PurePosixPath(rel).parts[:-1]
        parent = triade_id
        for part in parts:
            parent = ds.ensure_folder(parent, part, cache)
        try:
            if r:
                ds.upload_update(r["id"], p)
            else:
                ds.upload_create(parent, pathlib.PurePosixPath(rel).name, p)
            verts += 1
            print(f"[miroir] {'mis à jour' if r else 'téléversé'} : {rel}")
        except Exception as e:
            ecarts.append(f"{rel} : {e}")
            print(f"[miroir] ERREUR {rel} : {e}")
    print(f"[miroir] le delta : {verts}/{len(delta)} fichiers en place, "
          f"{len(ecarts)} erreurs")

    # 3· LES FICHIERS D'INSTRUCTION À LA RACINE DU COFFRE
    root_entries = ds.list_folder(ds.DRIVE_ROOT_ID)
    for name in ds.ROOT_PUSH:
        path = REPO / name
        if not path.is_file():
            continue
        r = root_entries.get(name)
        if r and r.get("mimeType") != ds.FOLDER_MIME \
                and r.get("md5Checksum") == md5_of(path):
            print(f"[miroir] (racine) inchangé : {name}")
            continue
        if r and r.get("mimeType") != ds.FOLDER_MIME:
            ds.upload_update(r["id"], path)
            print(f"[miroir] (racine) mis à jour : {name}")
        else:
            ds.upload_create(ds.DRIVE_ROOT_ID, name, path)
            print(f"[miroir] (racine) téléversé : {name}")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
