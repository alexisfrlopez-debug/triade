#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Diagnostic du dossier Drive « test » du développeur.

Le développeur travaille dans un sous-dossier « test » du coffre Drive
(1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0) : c'est là qu'il dépose ses constats
terrain (captures, journaux) et que les livrables de proximité sont poussés.

Ce script :
  1. identité du dossier (nom, parent, date de création/modification) ;
  2. liste complète du contenu (nom, taille, md5, modifiedTime) ;
  3. comparaison des livrables connus (demo.exe, LISEZMOI-demo.txt) avec
     les copies locales — détection de version (demo.2 vs demo.3) ;
  4. détection de FICHIERS NOUVEAUX déposés par le développeur
     (journaux terrain, captures d'écran) : empreinte inconnue ;
  5. racine du coffre listée en regard, pour situer la livraison.

Usage : python3 scripts/diag_dossier_test.py
Code de sortie : 0 (aucun fichier nouveau), 1 (fichiers nouveaux détectés),
2 (erreur fatale API).
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"  # dossier « test » du développeur

# Empreintes md5 des livrables connus (historique des versions demo)
MD5_CONNUS = {
    "demo.exe": {
        "fa50bf6af53a3e412b346f9f24d68f01": "demo.3 (16 384 o, sha256 933e216e…) — ACTUELLE",
        "9b857b0b30b4e5da07eb49d98c2f4497": "demo.2 (15 360 o, sha256 1fed2a52…) — OBSOLÈTE",
    },
    "demo_journal.txt": {
        # journal demo.2 déjà analysé (L00/L02/L01, 111 o) — tout autre contenu est NOUVEAU
        "inconnu": "contenu à analyser",
    },
}


def info_fichier(file_id):
    """Métadonnées complètes d'un fichier (nom, parents, dates)."""
    st, body, _ = ds.api(
        "GET", f"{ds.API}/files/{file_id}"
               "?fields=id,name,mimeType,size,md5Checksum,createdTime,"
               "modifiedTime,parents")
    if st != 200:
        return None
    return json.loads(body)


def lister_avec_dates(folder_id):
    """Liste un dossier avec dates et tailles (pagination incluse)."""
    out = {}
    token = None
    while True:
        params = {"q": f"'{folder_id}' in parents and trashed = false",
                  "pageSize": "200",
                  "fields": "nextPageToken,files(id,name,mimeType,md5Checksum,"
                            "size,createdTime,modifiedTime)"}
        if token:
            params["pageToken"] = token
        import urllib.parse
        st, body, _ = ds.api("GET", ds.API + "/files?" + urllib.parse.urlencode(params))
        if st != 200:
            raise ds.SyncError(f"listing impossible ({st}) : {body[:200]!r}")
        obj = json.loads(body)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def octets(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "?"
    return f"{n:,} o".replace(",", " ")


def main():
    # ---- identité du dossier lié
    try:
        info = info_fichier(TEST_ID)
    except ds.SyncError as e:
        print(f"[Test] ERREUR FATALE : {e}", file=sys.stderr)
        return 2
    if info is None:
        print(f"[Test] ERREUR FATALE : dossier {TEST_ID} introuvable/inaccessible",
              file=sys.stderr)
        return 2
    print(f"[Test] dossier : « {info['name']} »  (id {TEST_ID})")
    print(f"[Test] créé le {info['createdTime']} — modifié {info['modifiedTime']}")
    parents = info.get("parents", [])
    if parents:
        try:
            p = info_fichier(parents[0])
            if p:
                print(f"[Test] parent : « {p['name']} »  (id {parents[0]})")
        except ds.SyncError:
            pass
    print()

    # ---- contenu du dossier test
    try:
        entries = lister_avec_dates(TEST_ID)
    except ds.SyncError as e:
        print(f"[Test] ERREUR FATALE : {e}", file=sys.stderr)
        return 2
    print(f"[Test] CONTENU ({len(entries)} entrées) :")
    md5_locaux = {}
    for candidat in [REPO / "demo" / "demo.exe",
                     pathlib.Path("/home/z/my-project/download/demo.exe"),
                     REPO / "LISEZMOI-demo.txt",
                     pathlib.Path("/home/z/my-project/download/LISEZMOI-demo.txt")]:
        if candidat.is_file():
            md5_locaux[ds.md5_of(candidat)] = str(candidat)

    nouveaux = []
    for name, f in sorted(entries.items()):
        md5 = f.get("md5Checksum", "-")
        if f["mimeType"] == ds.FOLDER_MIME:
            print(f"  [dossier] {name}/")
            continue
        ligne = f"  {name}  ({octets(f.get('size'))})  md5={md5[:12]}…  modifié {f.get('modifiedTime', '?')}"
        # identification
        notes = []
        if name == "demo.exe" and md5 in MD5_CONNUS["demo.exe"]:
            notes.append(MD5_CONNUS["demo.exe"][md5])
        elif name == "demo.exe":
            notes.append("VERSION INCONNUE")
        if md5 in md5_locaux:
            notes.append(f"== local ({md5_locaux[md5]})")
        # fichiers terrain connus (journal demo.2 déjà analysé) vs nouveaux
        if name not in ("demo.exe", "LISEZMOI-demo.txt") and md5 not in md5_locaux:
            nouveaux.append((name, f))
            notes.append("NOUVEAU / À ANALYSER")
        print(ligne + ("  → " + " ; ".join(notes) if notes else ""))
    print()

    # ---- racine du coffre en regard
    try:
        racine = lister_avec_dates(ds.DRIVE_ROOT_ID)
        print(f"[Coffre] racine « {ds.DRIVE_ROOT_ID} » ({len(racine)} entrées) :")
        for name, f in sorted(racine.items()):
            if f["mimeType"] == ds.FOLDER_MIME:
                print(f"  [dossier] {name}/")
            else:
                marq = ""
                if name == "demo.exe":
                    marq = ("  → demo.3 ACTUELLE"
                            if f.get("md5Checksum") == "fa50bf6af53a3e412b346f9f24d68f01"
                            else f"  → md5={f.get('md5Checksum', '-')[:12]}…")
                print(f"  {name}  ({octets(f.get('size'))})  md5={f.get('md5Checksum', '-')[:12]}…{marq}")
    except ds.SyncError as e:
        print(f"[Coffre] avertissement : racine non listée ({e})", file=sys.stderr)
    print()

    # ---- verdict
    demo = entries.get("demo.exe")
    if not demo:
        print("[Verdict] demo.exe ABSENT du dossier test")
    else:
        m = demo.get("md5Checksum")
        if m == "fa50bf6af53a3e412b346f9f24d68f01":
            print("[Verdict] demo.exe = demo.3 (ACTUELLE) PRÉSENTE dans le dossier test — livraison confirmée")
        elif m == "9b857b0b30b4e5da07eb49d98c2f4497":
            print("[Verdict] demo.exe = demo.2 (OBSOLÈTE) dans le dossier test — à remplacer")
        else:
            print(f"[Verdict] demo.exe de version inconnue (md5 {m})")
    if nouveaux:
        print(f"[Verdict] {len(nouveaux)} fichier(s) NOUVEAUX déposés par le développeur :")
        for name, f in nouveaux:
            print(f"  - {name} ({octets(f.get('size'))}, modifié {f.get('modifiedTime')})")
        return 1
    print("[Verdict] aucun fichier nouveau du développeur en attente d'analyse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
