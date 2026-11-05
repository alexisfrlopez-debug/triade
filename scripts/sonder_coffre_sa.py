#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Sondage LECTURE SEULE du coffre Drive par le relais compte de service.

Contexte (constat 05/11) : le jeton OAuth du relais (oauth_token_relais.json,
émis le 04/11 10:53) est à nouveau mort (HTTP 400 invalid_grant au
rafraîchissement) — même symptôme que le 29/10, déjà résolu par le relais
compte de service (relais_service_account.py). Le présent script reprend ce
mécanisme pour SONDER (aucune écriture, aucun secret affiché) :

  - la racine /Triade (105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp) ;
  - le dossier /test du développeur (1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0),
    RÉCURSIVEMENT (une profondeur) — c'est là que le développeur dépose
    ses pièces (signatures de cérémonie au moment de l'écriture) ;
  - le kit /Cérémonie (sous-dossier de la racine, D130) récursivement
    (une profondeur).

Si l'accès échoue, l'échec est NOMMÉ : le dossier n'est sans doute pas
partagé au compte de service z-ai-811@physichong.iam.gserviceaccount.com ;
la reprise OAuth interactive reste alors la voie propre.

Usage : python3 scripts/sonder_coffre_sa.py
Code de sortie : 0 = sondé, 2 = accès impossible.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import relais_service_account as rsa  # noqa: E402  (l'import SURGIE le jeton)
import drive_sync as ds  # noqa: E402


def affiche(nom: str, dossier_id: str, recurse=()) -> dict:
    try:
        entrees = ds.list_folder(dossier_id)
    except Exception as exc:  # noqa: BLE001
        print(f"[{nom}] ERREUR D'ACCÈS : {exc}", file=sys.stderr)
        return {}
    print(f"=== {nom} ({len(entrees)} entrées) ===")
    for nom_f, meta in sorted(entrees.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"  [DIR     ] {nom_f}  id={meta['id']}")
        else:
            taille = meta.get("size", "?")
            md5 = (meta.get("md5Checksum") or "-")[:12]
            print(f"  [{taille:>8} o] {nom_f}  md5={md5}…  id={meta['id']}")
    for sous in recurse:
        if sous in entrees and entrees[sous].get("mimeType") == ds.FOLDER_MIME:
            print()
            affiche(f"{nom}/{sous}", entrees[sous]["id"])
    return entrees


def main() -> int:
    print("[Sondage par compte de service — LECTURE SEULE]")
    racine = affiche("RACINE /Triade", ds.DRIVE_ROOT_ID,
                     recurse=("Cérémonie", "TRIADE-sauvegarde-git"))
    print()
    if "test" in racine and racine["test"].get("mimeType") == ds.FOLDER_MIME:
        affiche("/test", racine["test"]["id"])
    else:
        print("=== /test absent de la racine affichée — sondage par id direct ===")
        affiche("/test", rsa.TEST_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
