#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Livraison terrain à la racine du dossier Google Drive.

Le miroir TRIADE/ reflète le dépôt git (scripts/drive_sync.py), mais les
livrables destinés au développeur (binaires terrain, LISEZMOI, conteneurs
de continuité) se posent À LA RACINE du dossier Drive « Triade » — le
« coffre de livraison » — pour rester immédiatement visibles sans naviguer
l'arborescence du miroir. Constat fondateur (session du 27/10/2026) :
demo.2 était correctement synchronisée dans TRIADE/demo/ mais introuvable
pour le développeur, qui ne parcourt que la racine.

Propriétés :
  - idempotent : md5 comparé à l'entrée distante, PATCH si différent,
    création si absent, aucun téléversement si identique ;
  - prudent : ne supprime jamais rien côté Drive ;
  - sûr : les secrets de .gdrive/ ne sont jamais exposés (D12) ;
  - autonome : réutilise drive_sync.py (stdlib uniquement).

Usage :
  python3 scripts/drive_livraison.py FICHIER [FICHIER...]   pousser des livrables
  python3 scripts/drive_livraison.py --verifier             état du coffre racine
  python3 scripts/drive_livraison.py --dossier-test FICHIER pousser dans le dossier
                                                            « test » du développeur
                                                            (1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0)
Code de sortie : 0 = succès, 1 = erreurs partielles, 2 = erreur fatale.
"""

import argparse
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur


def verifier():
    """Liste la racine du Drive et vérifie les livrables locaux de même nom."""
    try:
        entries = ds.list_folder(CIBLE[0])
    except ds.SyncError as e:
        print(f"[Livraison] ERREUR FATALE : {e}", file=sys.stderr)
        return 2
    print(f"[Livraison] racine du dossier Drive ({len(entries)} entrées) :")
    for name, f in sorted(entries.items()):
        if f["mimeType"] == ds.FOLDER_MIME:
            print(f"  [dossier] {name}/")
            continue
        local = pathlib.Path(name)
        etat = ""
        if local.is_file():
            etat = ("  == local" if ds.md5_of(local) == f.get("md5Checksum")
                    else "  != local (divergent)")
        print(f"  {name}  md5={f.get('md5Checksum', '-')}{etat}")
    return 0


def pousser(chemins):
    """Pousse chaque fichier (basename) à la racine du Drive, idempotent."""
    fichiers = []
    for c in chemins:
        p = pathlib.Path(c)
        if not p.is_file():
            print(f"[Livraison] ERREUR FATALE : fichier absent : {c}", file=sys.stderr)
            return 2
        fichiers.append(p)

    try:
        racine = ds.list_folder(CIBLE[0])
    except ds.SyncError as e:
        print(f"[Livraison] ERREUR FATALE : {e}", file=sys.stderr)
        return 2

    erreurs = 0
    for p in fichiers:
        nom = p.name
        md5 = ds.md5_of(p)
        r = racine.get(nom)
        if r and r.get("mimeType") == ds.FOLDER_MIME:
            print(f"[Livraison] ERREUR {nom} : un dossier porte déjà ce nom à la racine",
                  file=sys.stderr)
            erreurs += 1
            continue
        try:
            if r and r.get("md5Checksum") == md5:
                print(f"[Livraison] inchangé : {nom} (md5 identique)")
                continue
            if r:
                ds.upload_update(r["id"], p)
                print(f"[Livraison] mis à jour : {nom} ({md5})")
            else:
                ds.upload_create(CIBLE[0], nom, p)
                print(f"[Livraison] téléversé : {nom} ({md5})")
        except ds.SyncError as e:
            print(f"[Livraison] ERREUR {nom} : {e}", file=sys.stderr)
            erreurs += 1

    # vérification post-téléversement (re-listing, empreinte contre re-épreuve)
    try:
        apres = ds.list_folder(CIBLE[0])
        for p in fichiers:
            r = apres.get(p.name)
            if not r or r.get("md5Checksum") != ds.md5_of(p):
                print(f"[Livraison] VERIFICATION ÉCHOUÉE : {p.name} "
                      "absent ou divergent après téléversement", file=sys.stderr)
                erreurs += 1
            else:
                print(f"[Livraison] vérifié : {p.name} md5 MATCH")
    except ds.SyncError as e:
        print(f"[Livraison] avertissement : vérification impossible ({e})",
              file=sys.stderr)

    print(f"[Livraison] bilan : {len(fichiers) - erreurs}/{len(fichiers)} "
          f"vers {CIBLE[1]}, {erreurs} erreur(s)")
    return 1 if erreurs else 0


def main():
    ap = argparse.ArgumentParser(
        description="Livraison terrain à la racine du dossier Drive « Triade »")
    ap.add_argument("--dossier-test", action="store_true",
                    help="viser le dossier « test » du développeur (pas la racine)")
    ap.add_argument("fichiers", nargs="*",
                    help="fichiers à pousser (leur basename devient le nom Drive)")
    ap.add_argument("--verifier", action="store_true",
                    help="lister la racine du Drive et comparer aux fichiers locaux")
    args = ap.parse_args()
    global CIBLE
    CIBLE = (TEST_ID, "dossier test") if args.dossier_test \
        else (ds.DRIVE_ROOT_ID, "racine du coffre")
    if args.verifier:
        sys.exit(verifier())
    if not args.fichiers:
        ap.error("aucun fichier fourni (ou utiliser --verifier)")
    sys.exit(pousser(args.fichiers))


if __name__ == "__main__":
    main()
