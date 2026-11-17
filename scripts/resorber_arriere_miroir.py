#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resorber_arriere_miroir.py — LA RÉSORPTION DE L'ARRIÉRÉ DU MIROIR Drive
(602 fichiers d'époques passées jamais téléversés — l'état NOMMÉ de la
session 337 : la pointe est livrée, l'arriéré se résorbe au présent
geste). Reprise-sur-état : l'arbre distant et le curseur vivent à
/tmp/etat_arriere.json — chaque invocation reprend OÙ elle était, sans
re-parcourir le miroir. Idempotent : un fichier dont le md5 recoupe est
SAUTÉ."""
import json
import pathlib
import sys
import time

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

ETAT = pathlib.Path("/tmp/etat_arriere.json")
DUREE_TRAVAIL = 480   # secondes d'upload par invocation


def main():
    files = ds.git_tracked_files()
    if ETAT.exists():
        st = json.loads(ETAT.read_text())
        remote = {k: v for k, v in st["remote"].items()}
        faits = st["faits"]
    else:
        remote, faits = {}, []
        triade_id = ds.ensure_folder(ds.DRIVE_ROOT_ID, ds.PROJECT_FOLDER, {})
        ds.list_folder.cache = {}

        def walk(fid, prefix):
            for f in ds.list_folder(fid).values():
                if f["mimeType"] == ds.FOLDER_MIME:
                    walk(f["id"], prefix + f["name"] + "/")
                else:
                    remote[prefix + f["name"]] = f
        walk(triade_id, "")
    cache = {}

    def sauver():
        ETAT.write_text(json.dumps({"remote": remote, "faits": faits}))

    manquants = [rel for rel in sorted(files)
                 if rel not in faits
                 and (rel not in remote
                      or remote[rel].get("md5Checksum") != ds.md5_of(files[rel]))]
    debut = time.time()
    print(f"[arriéré] {len(faits)} déjà faits cette série ; "
          f"{len(manquants)} à téléverser ({len(files) - len(manquants) - len([f for f in faits if f in files])}/{len(files)} en place)")
    envoyes, erreurs = 0, 0
    for rel in manquants:
        if time.time() - debut > DUREE_TRAVAIL:
            print(f"[arriéré] la tranche est pleine — {envoyes} envoyés, "
                  f"reprenez le script (l'état est sauvé)")
            break
        p = files[rel]
        try:
            parts = pathlib.PurePosixPath(rel).parts[:-1]
            parent = ds.ensure_folder(ds.DRIVE_ROOT_ID, ds.PROJECT_FOLDER,
                                      cache)
            for part in parts:
                parent = ds.ensure_folder(parent, part, cache)
            r = remote.get(rel)
            if r:
                ds.upload_update(r["id"], p)
            else:
                # le dossier parent : ensure_folder par cascade (le cache
                # global marche car ensure_folder liste le parent direct)
                ds.upload_create(parent, pathlib.PurePosixPath(rel).name, p)
                # rafraîchir l'entrée locale de l'arbre pour les suivants
            faits.append(rel)
            remote[rel] = {"md5Checksum": ds.md5_of(p), "id": "?",
                           "name": pathlib.PurePosixPath(rel).name}
            envoyes += 1
        except Exception as e:
            erreurs += 1
            print(f"[arriéré] ERREUR {rel} : {e}")
        sauver()
    print(f"[arriéré] bilan de la tranche : {envoyes} téléversés, "
          f"{erreurs} erreurs ; {len(faits)} faits au total")
    restants = len(manquants) - envoyes
    print(f"[arriéré] restants : {max(restants, 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
