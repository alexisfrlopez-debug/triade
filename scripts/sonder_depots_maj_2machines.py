#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonder_depots_maj_2machines.py — lecture seule : construit le manifeste
récursif des DEUX dossiers déposés par le développeur dans /test du drive
après le run AUTO sur 2 ordis différents :
  - TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR   (id 1_w-…)
  - TRIADE_kits_terrain_v0150_MULTIMACHINES-MISE-A-JOUR2  (id 1htX…)

Usage : python3 scripts/sonder_depots_maj_2machines.py
Écrit : scripts/kits_mesure_v150/edition_mise_a_jour/sondage_depots_2machines.json
"""

import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DOSSIERS = {
    "MISE-A-JOUR": "1_w-LShQz74oyUQML8Us7DqoCQZ-ezqUp",
    "MISE-A-JOUR2": "1htXFaFA4lNcqwFd-QYDB3--EzCfNSSii",
}

SORTIE = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour" / "sondage_depots_2machines.json"


def lister(fid: str):
    """Liste un dossier Drive (nom -> métadonnées), gère la pagination."""
    import urllib.parse
    entrees, token = {}, None
    while True:
        params = {
            "q": f"'{fid}' in parents and trashed = false",
            "fields": "nextPageToken, files(id, name, mimeType, size, md5Checksum, modifiedTime)",
            "pageSize": "200",
        }
        if token:
            params["pageToken"] = token
        st, body, _ = ds.api("GET", ds.API + "/files?" + urllib.parse.urlencode(params))
        if st != 200:
            raise ds.SyncError(f"listage impossible ({st}) : {body[:120]!r}")
        obj = json.loads(body)
        for f in obj.get("files", []):
            entrees[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return entrees


def parcourir(fid: str, prefixe: str, sortie: list, prof: int = 0):
    for nom, meta in sorted(lister(fid).items()):
        chemin = f"{prefixe}/{nom}"
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"{'  ' * prof}[DIR] {chemin}")
            parcourir(meta["id"], chemin, sortie, prof + 1)
        else:
            sortie.append({
                "chemin": chemin,
                "id": meta["id"],
                "taille": int(meta.get("size", 0)),
                "md5": meta.get("md5Checksum", ""),
                "mtime": meta.get("modifiedTime", ""),
            })
            print(f"{'  ' * prof}      {chemin}  ({meta.get('size', 0)} o, md5={meta.get('md5Checksum', '-')[:8]}…, mtime={meta.get('modifiedTime', '-')})")
        time.sleep(0.05)


def main() -> int:
    manifeste = {}
    for nom, fid in DOSSIERS.items():
        print(f"=== {nom} ===", flush=True)
        pieces = []
        parcourir(fid, nom, pieces)
        manifeste[nom] = {"id_dossier": fid, "nb_pieces": len(pieces),
                          "octets": sum(p["taille"] for p in pieces),
                          "pieces": pieces}
        print(f"--- {nom} : {len(pieces)} fichiers, {sum(p['taille'] for p in pieces)} octets ---", flush=True)
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(manifeste, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Manifeste écrit : {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
