#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit le manifeste récursif d'un dossier Drive (chemin, id, taille, md5).

Usage: drive_tree.py <folder_id> <fichier_manifeste>
"""
import json
import sys
import urllib.parse

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_api import _get  # noqa: E402

FOLDER_MIME = "application/vnd.google-apps.folder"


def parcourir(fid, prefixe, sortie, profondeur=0):
    rep = _get("https://www.googleapis.com/drive/v3/files/", {
        "q": f"'{fid}' in parents and trashed = false",
        "fields": "nextPageToken, files(id, name, mimeType, size, md5Checksum)",
        "pageSize": 200,
    })
    fichiers = rep.get("files", [])
    while rep.get("nextPageToken"):
        rep = _get("https://www.googleapis.com/drive/v3/files/", {
            "q": f"'{fid}' in parents and trashed = false",
            "fields": "nextPageToken, files(id, name, mimeType, size, md5Checksum)",
            "pageSize": 200, "pageToken": rep["nextPageToken"],
        })
        fichiers += rep.get("files", [])
    for f in sorted(fichiers, key=lambda x: x["name"]):
        chemin = f"{prefixe}/{f['name']}"
        if f["mimeType"] == FOLDER_MIME:
            parcourir(f["id"], chemin, sortie, profondeur + 1)
        else:
            sortie.append({"chemin": chemin, "id": f["id"],
                           "taille": int(f.get("size", 0)),
                           "md5": f.get("md5Checksum", "")})
            print(chemin, flush=True)


def main():
    racine = sys.argv[1]
    sortie_fichier = sys.argv[2]
    lignes = []
    parcourir(racine, "", lignes)
    json.dump(lignes, open(sortie_fichier, "w"), ensure_ascii=False, indent=0)
    total = sum(l["taille"] for l in lignes)
    print(f"--- {len(lignes)} fichiers, {total} octets ---", file=sys.stderr)


if __name__ == "__main__":
    main()
