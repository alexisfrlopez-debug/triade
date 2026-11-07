#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonder_run6_m9f.py — SONDE lecture seule du réceptacle /test/preuves-m9f
avant le geste du SIXIÈME run M9-(f) : liste les pièces déposées (nom,
taille, md5, modifiedTime) SANS rien écrire, SANS rien télécharger.

La question de la sonde est LA question du geste (la rangée (f) du PLAN) :
  - le trio du run est-il déposé (temoin-m9f.txt, scenario-m9f-journal.log,
    VERDICT-run-m9f.txt) ?
  - les pièces conditionnelles sont-elles nées (ligne-recue.txt T4,
    journal-emissions.txt T6) — LE VERT les porterait ?
  - le réceptacle porte-t-il autre chose que son LISEZMOI + le run ?

Usage : python3 scripts/sonder_run6_m9f.py
Code de sortie : 0 = sondé ; 2 = erreur fatale (réceptacle inaccessible).
"""

import pathlib
import sys
import urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test »
RECEPTACLE = "preuves-m9f"

TRIO = {"temoin-m9f.txt", "scenario-m9f-journal.log", "VERDICT-run-m9f.txt"}
CONDITIONNELLES = {"ligne-recue.txt", "journal-emissions.txt"}
VIVANTES = {"ligne-recue.txt"}


def lister_avec_dates(folder_id):
    out = {}
    token = None
    while True:
        params = {"q": f"'{folder_id}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,md5Checksum,"
                            "size,createdTime,modifiedTime)"}
        if token:
            params["pageToken"] = token
        st, body, _ = ds.api("GET", ds.API + "/files?"
                             + urllib.parse.urlencode(params))
        if st != 200:
            raise ds.SyncError(f"listing impossible ({st}) : {body[:200]!r}")
        obj = __import__("json").loads(body)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def main() -> int:
    try:
        racine = ds.list_folder(TEST_ID)
        pm9 = racine.get(RECEPTACLE)
        if not pm9 or pm9.get("mimeType") != ds.FOLDER_MIME:
            print(f"[sonde] ERREUR FATALE : /test/{RECEPTACLE} absent",
                  file=sys.stderr)
            return 2
        print(f"[sonde] réceptacle /test/{RECEPTACLE} (id {pm9['id']})")
        entrees = lister_avec_dates(pm9["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[sonde] ERREUR FATALE : {exc}", file=sys.stderr)
        return 2

    print(f"[sonde] CONTENU ({len(entrees)} entrées) :")
    for nom, f in sorted(entrees.items()):
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR ] {nom}/  id={f['id']}")
            continue
        taille = f.get("size", "?")
        print(f"  [{str(taille):>7} o] {nom}  md5={f.get('md5Checksum', '-')[:8]}…"
              f"  modifié {f.get('modifiedTime', '?')}")

    deposees = {n for n, f in entrees.items()
                if f.get("mimeType") != ds.FOLDER_MIME}
    print()
    if TRIO <= deposees:
        print(f"[sonde] LE TRIO DU RUN EST DÉPOSÉ : {sorted(TRIO)}")
    else:
        print(f"[sonde] le trio INCOMPLET : manquant "
              f"{sorted(TRIO - deposees)}")
    nees = deposees & CONDITIONNELLES
    if nees:
        print(f"[sonde] PIÈCES CONDITIONNELLES NÉES : {sorted(nees)} — "
              "le run est allé jusque-là")
        if VIVANTES <= nees:
            print("[sonde] ligne-recue.txt EST LÀ : T4 a rendu la ligne "
                  "applicative — la lecture A VÉCU ?")
    else:
        print("[sonde] aucune pièce conditionnelle — le journal dira où "
              "le run s'est arrêté")
    autres = deposees - TRIO - CONDITIONNELLES - {"LISEZMOI-preuves.txt"}
    if autres:
        print(f"[sonde] ENTRÉES INATTENDUES : {sorted(autres)}")
    print("[sonde] fini — lecture seule, aucun geste")
    return 0


if __name__ == "__main__":
    sys.exit(main())
