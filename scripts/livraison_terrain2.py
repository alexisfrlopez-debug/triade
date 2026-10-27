#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livraison_terrain2.py — Livraison D49 : le kit UN-fichier.

  1. dossier test du développeur : pousse la variante LIVRAISON de
     superviseur.exe 0.5.0-terrain.2 (annexe de jetons intégrée — plus
     JAMAIS un fichier à part) + le LISEZMOI v2 ;
  2. nettoyage ciblé du dossier test : proxy.exe (le déclencheur de la
     fausse alerte Defender du 27/10 — désormais embarqué), terrain_jetons.bin
     (secret désormais intégré), LISEZMOI-proxy.txt (obsolète), les rc
     d'echo (bruit de zip) — demo.exe et echo-0.3.0.exe scellés RESTENT ;
  3. coffre racine : variante PUBLIQUE (dépôt, emplacement vide) + LISEZMOI.

Idempotent, vérifié par re-listing md5 après chaque téléversement.
"""

import os
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ICI / "scripts"))
import drive_sync as ds  # noqa: E402

RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"          # coffre « Triade »
DOSSIER_TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"    # dossier « test »

LIVRAISON_EXE = ICI / "terrain" / "livraison" / "superviseur.exe"
PUBLIC_EXE = ICI / "terrain" / "superviseur.exe"
LISEZMOI = ICI / "LISEZMOI-superviseur.txt"

A_RETIRER_TEST = ["proxy.exe", "terrain_jetons.bin", "LISEZMOI-proxy.txt",
                  "echo-0.3.0-rc.3.exe", "echo-0.3.0-rc.4.exe"]
A_GARDER_TEST = ["superviseur.exe", "LISEZMOI-superviseur.txt",
                 "demo.exe", "echo-0.3.0.exe"]


def pousser(dossier_id, nom_dossier: str, chemins: list) -> int:
    listing = ds.list_folder(dossier_id)
    erreurs = 0
    for p in chemins:
        md5 = ds.md5_of(p)
        r = listing.get(p.name)
        try:
            if r and r.get("md5Checksum") == md5:
                print(f"  [test] inchangé : {p.name}")
            elif r:
                ds.upload_update(r["id"], p)
                print(f"  [{nom_dossier}] mis à jour : {p.name} ({md5})")
            else:
                ds.upload_create(dossier_id, p.name, p)
                print(f"  [{nom_dossier}] téléversé : {p.name} ({md5})")
        except ds.SyncError as e:
            print(f"  [{nom_dossier}] ERREUR {p.name} : {e}", file=sys.stderr)
            erreurs += 1
    return erreurs


def retirer(dossier_id, noms: list) -> int:
    listing = ds.list_folder(dossier_id)
    erreurs = 0
    for nom in noms:
        r = listing.get(nom)
        if not r:
            print(f"  [test] déjà absent : {nom}")
            continue
        try:
            ds.api("DELETE", f"https://www.googleapis.com/drive/v3/files/{r['id']}")
            print(f"  [test] retiré : {nom} (id {r['id'][:12]}…)")
        except ds.SyncError as e:
            print(f"  [test] ERREUR retrait {nom} : {e}", file=sys.stderr)
            erreurs += 1
    return erreurs


def verifier_dossier(dossier_id, attendus: dict, nom: str) -> int:
    listing = ds.list_folder(dossier_id)
    erreurs = 0
    for nom_f, md5 in attendus.items():
        r = listing.get(nom_f)
        if not r or r.get("md5Checksum") != md5:
            print(f"  [{nom}] VÉRIFICATION ÉCHOUÉE : {nom_f}", file=sys.stderr)
            erreurs += 1
        else:
            print(f"  [{nom}] vérifié : {nom_f} md5 MATCH")
    return erreurs


def main() -> int:
    for p in (LIVRAISON_EXE, PUBLIC_EXE, LISEZMOI):
        if not p.is_file():
            print(f"[Livraison D49] ERREUR FATALE : absent : {p}", file=sys.stderr)
            return 2

    print("[Livraison D49] 1/3 — dossier test : la variante LIVRAISON (annexe intégrée)")
    erreurs = pousser(DOSSIER_TEST, "test", [LIVRAISON_EXE, LISEZMOI])

    print("[Livraison D49] 2/3 — dossier test : nettoyage ciblé du kit quatre-fichiers")
    erreurs += retirer(DOSSIER_TEST, A_RETIRER_TEST)

    print("[Livraison D49] 3/3 — coffre racine : la variante PUBLIQUE (dépôt)")
    erreurs += pousser(RACINE, "racine", [PUBLIC_EXE, LISEZMOI])

    attendus_test = {"superviseur.exe": ds.md5_of(LIVRAISON_EXE),
                     "LISEZMOI-superviseur.txt": ds.md5_of(LISEZMOI)}
    attendus_racine = {"superviseur.exe": ds.md5_of(PUBLIC_EXE),
                       "LISEZMOI-superviseur.txt": ds.md5_of(LISEZMOI)}
    erreurs += verifier_dossier(DOSSIER_TEST, attendus_test, "test")
    erreurs += verifier_dossier(RACINE, attendus_racine, "racine")

    listing = ds.list_folder(DOSSIER_TEST)
    for nom in A_RETIRER_TEST:
        if nom in listing:
            print(f"  [test] RÉSIDUEL INATTENDU : {nom}", file=sys.stderr)
            erreurs += 1
    print(f"[Livraison D49] bilan : {'TOUT OK' if not erreurs else f'{erreurs} erreur(s)'} "
          f"— dossier test = 1 exe (livraison) + LISEZMOI + scellés historiques")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
