#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Récupération de fichiers depuis le dossier Drive « test ».

Le développeur dépose ses constats terrain (journaux, captures) dans son
dossier « test » du coffre Drive. Ce script rapatrie ces fichiers localement
dans upload/ (zone d'entrée terrain, jamais commitée) pour analyse.

Propriétés :
  - prudent : n'écrase jamais un fichier local différent sans --forcer ;
  - sûr : les secrets de .gdrive/ ne sont jamais exposés (D12) ;
  - autonome : réutilise drive_sync.py (stdlib uniquement).

Usage :
  python3 scripts/drive_recuperer.py --lister           voir le dossier test
  python3 scripts/drive_recuperer.py FICHIER [FICHIER…]  rapatrier vers upload/
  python3 scripts/drive_recuperer.py --forcer FICHIER    écraser si divergent
Code de sortie : 0 = succès, 1 = erreurs partielles, 2 = erreur fatale.
"""

import argparse
import pathlib
import sys
import urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"  # dossier « test » du développeur
DEST = pathlib.Path("/home/z/my-project/upload")  # zone d'entrée terrain


def telecharger(file_id, destination):
    """Télécharge le contenu binaire d'un fichier Drive (authentifié)."""
    url = (f"{ds.API}/files/{file_id}?alt=media")
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)
    return ds.md5_of(destination)


def main():
    ap = argparse.ArgumentParser(
        description="Rapatrier les fichiers du dossier Drive « test » vers upload/")
    ap.add_argument("fichiers", nargs="*",
                    help="noms exacts des fichiers à rapatrier")
    ap.add_argument("--lister", action="store_true",
                    help="lister le dossier test (noms, tailles, md5, dates)")
    ap.add_argument("--forcer", action="store_true",
                    help="écraser un fichier local existant mais divergent")
    args = ap.parse_args()

    try:
        if args.lister or not args.fichiers:
            entries = ds.list_folder(TEST_ID)
            print(f"[Test] {len(entries)} entrées :")
            for name, f in sorted(entries.items()):
                if f["mimeType"] == ds.FOLDER_MIME:
                    print(f"  [dossier] {name}/")
                else:
                    print(f"  {name}  md5={f.get('md5Checksum', '-')[:12]}…")
            if not args.fichiers:
                return 0

        entries = ds.list_folder(TEST_ID)
        erreurs = 0
        for nom in args.fichiers:
            f = entries.get(nom)
            if not f or f["mimeType"] == ds.FOLDER_MIME:
                print(f"[Test] ERREUR : « {nom} » absent du dossier test",
                      file=sys.stderr)
                erreurs += 1
                continue
            dest = DEST / nom
            if dest.exists() and ds.md5_of(dest) == f.get("md5Checksum"):
                print(f"[Test] déjà à jour : {dest}")
                continue
            if dest.exists() and not args.forcer:
                print(f"[Test] ERREUR : {dest} existe et diverge "
                      "(--forcer pour écraser)", file=sys.stderr)
                erreurs += 1
                continue
            DEST.mkdir(parents=True, exist_ok=True)
            try:
                md5 = telecharger(f["id"], dest)
                if md5 != f.get("md5Checksum"):
                    print(f"[Test] ERREUR : {nom} téléchargé mais md5 diverge "
                          f"({md5} != {f.get('md5Checksum')})", file=sys.stderr)
                    erreurs += 1
                else:
                    print(f"[Test] rapatrié : {dest}  "
                          f"({dest.stat().st_size:,} o, md5 {md5[:12]}…)".replace(",", " "))
            except ds.SyncError as e:
                print(f"[Test] ERREUR {nom} : {e}", file=sys.stderr)
                erreurs += 1
        return 1 if erreurs else 0
    except ds.SyncError as e:
        print(f"[Test] ERREUR FATALE : {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
