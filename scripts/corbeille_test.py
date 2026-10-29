#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Corbeille du dossier Drive « test » (mono-génération D69).

Met à la corbeille les fichiers nommés du dossier test du développeur
(les livraisons obsolètes ne doivent jamais rester en circulation à côté
de la génération courante). Prudent : noms exacts exigés, empreinte md5
affichée avant mise à la corbeille, rien d'autre n'est touché.

Usage : python3 scripts/corbeille_test.py FICHIER [FICHIER…]
Code de sortie : 0 = fait, 1 = erreur partielle, 2 = erreur fatale.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"  # dossier « test » du développeur


def main() -> int:
    noms = sys.argv[1:]
    if not noms:
        print("usage : corbeille_test.py FICHIER [FICHIER…]", file=sys.stderr)
        return 2
    try:
        entries = ds.list_folder(TEST_ID)
    except ds.SyncError as e:
        print(f"[Test] ERREUR FATALE : {e}", file=sys.stderr)
        return 2
    erreurs = 0
    for nom in noms:
        f = entries.get(nom)
        if not f:
            print(f"[Test] ERREUR : « {nom} » absent du dossier test", file=sys.stderr)
            erreurs += 1
            continue
        st, body, _ = ds.api("PATCH", f"{ds.API}/files/{f['id']}",
                             body={"trashed": True})
        if st != 200:
            print(f"[Test] ERREUR {nom} : corbeille impossible ({st}) : "
                  f"{body[:120]!r}", file=sys.stderr)
            erreurs += 1
        else:
            print(f"[Test] à la corbeille : {nom}  "
                  f"(md5 {f.get('md5Checksum', '-')[:12]}…)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
