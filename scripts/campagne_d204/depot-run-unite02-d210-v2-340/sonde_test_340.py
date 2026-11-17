#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_test_340.py — LA SONDE DU COFFRE /test (l'Entrée 340) — ÉDITION
CIBLÉE : la racine + le dépôt preuves-unite02/ NEUVE (le re-run au juge v2
réparé annoncé : « preuves du run dans le drive /test ») + l'archive du
run v1 (unite-02-d210-20261118/). Tout est calculé depuis les métadonnées
Drive, aucun chiffre recopié."""
import json
import pathlib
import sys
import urllib.parse

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"

# les dossiers à ouvrir au-delà de la racine (le dépôt annoncé + l'archive v1)
OUVRIR = {"preuves-unite02", "archives-livraisons"}


def lister(fid):
    """files.list paginé -> {nom: f} avec size/modifiedTime inclus."""
    out = {}
    token = None
    while True:
        params = {
            "q": f"'{fid}' in parents and trashed = false",
            "pageSize": "500",
            "fields": ("nextPageToken,files(id,name,mimeType,md5Checksum,"
                       "size,modifiedTime,createdTime)"),
        }
        if token:
            params["pageToken"] = token
        st, body, _ = ds.api("GET", ds.API + "/files?"
                             + urllib.parse.urlencode(params))
        if st != 200:
            raise RuntimeError(f"listing impossible ({st}) : {body[:200]!r}")
        obj = json.loads(body)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def afficher(prefix, ent):
    items = sorted(ent.values(),
                   key=lambda f: f.get("modifiedTime", ""), reverse=True)
    for f in items:
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR ] {prefix + f['name']}/  [{f['id']}] "
                  f"né {f.get('createdTime', '?')}")
        else:
            print(f"  {f.get('modifiedTime', '?'):26s} "
                  f"{str(f.get('size', '?')):>9s} o  "
                  f"{str(f.get('md5Checksum', ''))[:10]:10s}  "
                  f"{prefix + f['name']}  [{f['id']}]")


def main():
    print("[sonde] LA RACINE du /test (les plus récentes d'abord) :")
    racine = lister(TEST_ID)
    afficher("", racine)
    for nom in sorted(OUVRIR):
        if nom in racine and racine[nom].get("mimeType") == ds.FOLDER_MIME:
            print(f"[sonde] LE DOSSIER {nom}/ :")
            sous = lister(racine[nom]["id"])
            afficher(nom + "/", sous)
            if nom == "archives-livraisons":
                u2 = sous.get("unite-02-d210-20261118")
                if u2 and u2.get("mimeType") == ds.FOLDER_MIME:
                    print("[sonde] L'ARCHIVE DU RUN V1 "
                          "(unite-02-d210-20261118/) :")
                    afficher("archives-livraisons/unite-02-d210-20261118/",
                             lister(u2["id"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
