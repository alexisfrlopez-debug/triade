#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Archivage du coffre de livraison Drive (racine → sous-dossier ARCHIVE/).

La racine du dossier Drive « Triade » est le coffre de livraison : elle ne doit
porter que des éléments COURANTS (instructions, miroir, jetons, coffre-fort,
livrables utiles, dossier test). Les livrables périmés y sont archivés — jamais
supprimés — dans le sous-dossier « ARCHIVE » (D76 : nettoyage demandé par le
développeur ; l'historique complet vit déjà dans git + TRIADE/triade-history.bundle,
l'archive Drive ne sert qu'à la lisibilité de la racine).

Propriétés :
  - idempotent : un fichier déjà archivé est constaté « inchangé » ;
  - prudent : DÉPLACEMENT uniquement (addParents/removeParents) — aucune
    suppression, aucun écrasement de contenu ; échec si collision de nom ;
  - vérifié : md5 d'entrée comparé au md5 constaté dans ARCHIVE/ après le
    déplacement (le déplacement Drive préserve le contenu, on le prouve) ;
  - sûr : les secrets de .gdrive/ ne sont jamais exposés (D12) ;
  - autonome : réutilise drive_sync.py (stdlib uniquement).

Usage :
  python3 scripts/drive_archiver.py FICHIER [FICHIER...]  archiver des éléments racine
  python3 scripts/drive_archiver.py --verifier           état racine + ARCHIVE
Code de sortie : 0 = succès, 1 = erreurs partielles, 2 = erreur fatale.
"""

import argparse
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

ARCHIVE_NAME = "ARCHIVE"


def trouver_dossier(parent_id, nom):
    """Retourne l'id du sous-dossier `nom` de `parent_id`, ou None."""
    ent = ds.list_folder(parent_id)
    for f in ent.values():
        if f["mimeType"] == ds.FOLDER_MIME and f["name"] == nom:
            return f["id"]
    return None


def deplacer(file_id, nom, archive_id, md5_avant):
    """Déplace un fichier de la racine vers ARCHIVE/ (aucun contenu modifié)."""
    url = (f"{ds.API}/files/{file_id}?"
           + "addParents=" + archive_id
           + "&removeParents=" + ds.DRIVE_ROOT_ID)
    st, body, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise ds.SyncError(f"déplacement de '{nom}' impossible (HTTP {st}) : {body[:200]!r}")
    # vérification : le contenu ne doit pas avoir bougé d'un octet
    ent = ds.list_folder(archive_id)
    apres = ent.get(nom)
    if not apres:
        raise ds.SyncError(f"'{nom}' absent de ARCHIVE/ après le déplacement")
    if apres.get("md5Checksum") != md5_avant:
        raise ds.SyncError(f"'{nom}' : md5 CHANGÉ au déplacement "
                           f"({md5_avant} → {apres.get('md5Checksum')}) — ABANDON")
    return apres["id"]


def verifier():
    """Affiche l'état de la racine et du dossier ARCHIVE."""
    try:
        racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    except ds.SyncError as e:
        print(f"[Archiver] ERREUR FATALE : {e}", file=sys.stderr)
        return 2
    print(f"[Archiver] racine du coffre ({len(racine)} entrées) :")
    for nom, f in sorted(racine.items()):
        if f["mimeType"] == ds.FOLDER_MIME:
            print(f"  [dossier] {nom}/")
        else:
            print(f"  {nom}  md5={f.get('md5Checksum', '-')}")
    arch = trouver_dossier(ds.DRIVE_ROOT_ID, ARCHIVE_NAME)
    if not arch:
        print(f"[Archiver] dossier ARCHIVE/ : ABSENT (rien n'est archivé)")
        return 0
    ent = ds.list_folder(arch)
    print(f"[Archiver] ARCHIVE/ ({len(ent)} entrées) :")
    for nom, f in sorted(ent.items()):
        if f["mimeType"] == ds.FOLDER_MIME:
            print(f"  [dossier] {nom}/")
        else:
            print(f"  {nom}  md5={f.get('md5Checksum', '-')}")
    return 0


def archiver(noms):
    """Archive chaque nom (basename) trouvé À LA RACINE du coffre."""
    try:
        racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    except ds.SyncError as e:
        print(f"[Archiver] ERREUR FATALE : {e}", file=sys.stderr)
        return 2

    # dossier ARCHIVE : créer s'il n'existe pas (une seule fois)
    archive_id = trouver_dossier(ds.DRIVE_ROOT_ID, ARCHIVE_NAME)
    if not archive_id:
        try:
            archive_id = ds.create_folder(ds.DRIVE_ROOT_ID, ARCHIVE_NAME)
            print(f"[Archiver] dossier ARCHIVE/ créé ({archive_id})")
        except ds.SyncError as e:
            print(f"[Archiver] ERREUR FATALE : création ARCHIVE/ : {e}", file=sys.stderr)
            return 2
    else:
        print(f"[Archiver] dossier ARCHIVE/ présent ({archive_id})")
    deja = ds.list_folder(archive_id)

    erreurs = 0
    for nom in noms:
        if "/" in nom or "\\" in nom or nom in (".", ".."):
            print(f"[Archiver] ERREUR {nom} : nom de fichier simple attendu", file=sys.stderr)
            erreurs += 1
            continue
        cible = deja.get(nom)
        src = racine.get(nom)
        if cible is not None and src is None:
            print(f"[Archiver] inchangé : {nom} (déjà archivé, absent de la racine)")
            continue
        if cible is not None and src is not None:
            print(f"[Archiver] ERREUR {nom} : présent ET à la racine ET dans ARCHIVE/ "
                  f"(collision — règlement manuel requis)", file=sys.stderr)
            erreurs += 1
            continue
        if cible is not None and src is None:
            continue
        if src is None:
            print(f"[Archiver] ERREUR {nom} : introuvable à la racine", file=sys.stderr)
            erreurs += 1
            continue
        if src.get("mimeType") == ds.FOLDER_MIME:
            print(f"[Archiver] ERREUR {nom} : c'est un dossier — refusé "
                  f"(l'archivage ne déplace que des fichiers)", file=sys.stderr)
            erreurs += 1
            continue
        md5_avant = src.get("md5Checksum")
        try:
            deplacer(src["id"], nom, archive_id, md5_avant)
            print(f"[Archiver] archivé : {nom} (md5 {md5_avant} préservé)")
        except ds.SyncError as e:
            print(f"[Archiver] ERREUR {nom} : {e}", file=sys.stderr)
            erreurs += 1
    if erreurs:
        return 1
    return 0


def main():
    p = argparse.ArgumentParser(description="Archivage du coffre de livraison Drive")
    p.add_argument("fichiers", nargs="*", help="noms de fichiers à archiver (racine → ARCHIVE/)")
    p.add_argument("--verifier", action="store_true", help="état de la racine et de ARCHIVE/")
    args = p.parse_args()
    if args.verifier:
        return verifier()
    if not args.fichiers:
        p.print_help()
        return 2
    return archiver(args.fichiers)


if __name__ == "__main__":
    sys.exit(main())
