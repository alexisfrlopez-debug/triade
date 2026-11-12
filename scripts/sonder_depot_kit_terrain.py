#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonder_depot_kit_terrain.py — lecture seule : sonde le dossier /test du
coffre Drive à la réception de l'annonce du développeur « dossier kit terrain
avec preuves déposé dans /test du drive ».

Sert :
  - le premier niveau (nom, type, taille, md5, créé/modifié) ;
  - le recompte récursif (à comparer au 496 du geste A + les dépôts des
    Entrées 246/247) ;
  - le détail daté de toute entrée créée après la livraison du paquet AUTO
    (12:29 UTC, 12/11/2026).

Aucune écriture Drive. Aucun secret affiché (D12).

Usage : python3 scripts/sonder_depot_kit_terrain.py
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"  # dossier « test » du développeur
FOLDER_MIME = ds.FOLDER_MIME
SEUIL_AUTO = "2026-11-12T12:25:00Z"   # livraison du paquet AUTO au coffre

CHAMPS = "files(id, name, mimeType, size, md5Checksum, createdTime, modifiedTime)"


def lister(fid):
    """Liste un dossier avec pagination (champs datés)."""
    params = {
        "q": f"'{fid}' in parents and trashed = false",
        "fields": "nextPageToken," + CHAMPS,
        "pageSize": 200,
    }
    st, body, _ = ds.api("GET", f"{ds.API}/files?"
                         + urllib.parse.urlencode(params))
    if st != 200:
        raise ds.SyncError(f"listage impossible ({st}) : {body[:120]!r}")
    rep = json.loads(body)
    fichiers = rep.get("files", [])
    while rep.get("nextPageToken"):
        params["pageToken"] = rep["nextPageToken"]
        st, body, _ = ds.api("GET", f"{ds.API}/files?"
                             + urllib.parse.urlencode(params))
        if st != 200:
            raise ds.SyncError(f"page suivante impossible ({st})")
        rep = json.loads(body)
        fichiers += rep.get("files", [])
    return fichiers


def parcourir(fid, prefixe, sortie, profondeur=0):
    """Parcours récursif : chaque fichier daté, chaque dossier descendu."""
    for f in sorted(lister(fid), key=lambda x: x["name"]):
        chemin = f"{prefixe}/{f['name']}"
        if f["mimeType"] == FOLDER_MIME:
            sortie.append({"chemin": chemin + "/", "dossier": True,
                           "id": f["id"], "cree": f.get("createdTime", ""),
                           "modifie": f.get("modifiedTime", "")})
            if profondeur < 8:
                parcourir(f["id"], chemin, sortie, profondeur + 1)
        else:
            sortie.append({"chemin": chemin, "dossier": False,
                           "id": f["id"],
                           "taille": int(f.get("size", 0)),
                           "md5": f.get("md5Checksum", ""),
                           "cree": f.get("createdTime", ""),
                           "modifie": f.get("modifiedTime", "")})


def main() -> int:
    print("=== PREMIER NIVEAU de /test ===")
    entrees = lister(TEST_ID)
    print(f"[{len(entrees)} entrées de premier niveau]")
    for f in sorted(entrees, key=lambda x: x["name"]):
        if f["mimeType"] == FOLDER_MIME:
            print(f"  [DIR ] {f['name']}/  id={f['id']}  "
                  f"créé={f.get('createdTime', '-')}")
        else:
            print(f"  [{f.get('size', '?'):>9} o] {f['name']}  "
                  f"md5={f.get('md5Checksum', '-')[:8]}…  "
                  f"créé={f.get('createdTime', '-')}")

    print()
    print("=== RECOMPTE RÉCURSIF ===")
    tout = []
    parcourir(TEST_ID, "", tout)
    fichiers = [e for e in tout if not e["dossier"]]
    total = sum(e["taille"] for e in fichiers)
    print(f"[{len(tout)} entrées totales dont {len(fichiers)} fichiers, "
          f"{total} octets]")

    print()
    print(f"=== ENTRÉES CRÉÉES APRÈS {SEUIL_AUTO} (le dépôt attendu) ===")
    tardives = [e for e in tout if e["cree"] > SEUIL_AUTO]
    for e in sorted(tardives, key=lambda x: x["chemin"]):
        if e["dossier"]:
            print(f"  [DIR ] {e['chemin']}  créé={e['cree']}")
        else:
            print(f"  [{e['taille']:>9} o] {e['chemin']}  "
                  f"md5={e['md5'][:12]}…  créé={e['cree']}  "
                  f"modifié={e['modifie']}")
    print(f"[{len(tardives)} entrées tardives]")

    # sortie machine pour la suite
    sortie = pathlib.Path(REPO / "scripts" / "sondage_depot_kit_terrain.json")
    sortie.write_text(json.dumps(tout, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"\n[manifeste daté : {sortie}]")
    return 0


import json  # noqa: E402
import urllib.parse  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
