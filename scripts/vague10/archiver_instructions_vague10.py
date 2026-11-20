#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_instructions_vague10.py — L'ARCHIVAGE DES SIX INSTRUCTIONS
après exécution (la règle du maître : « nouvelles instructions ici, à
archiver après exécution ») : le /instructions du coffre (la vue du
relais) → /ARCHIVE/instructions_vague10_20261120/ ; la copie au dépôt
(instructions_vague10_20261120/) ; le /instructions LAISSÉ VIDE — la
vague 11 attend ses instructions au commandement du maître."""
import pathlib
import shutil
import sys

sys.path.insert(0, "/home/z/my-project/scripts")
from sa_token import api  # noqa: E402

REPO = pathlib.Path("/home/z/my-project/depot")
DOSSIER_INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ARCHIVE = "1uJ5yU7ma5dYQM1GuWzm9Fx1I1U3Ywepr"       # le dossier ARCHIVE


def main() -> int:
    # (1) LA COPIE AU DÉPÔT (la pièce du geste)
    dest_repo = REPO / "instructions_vague10_20261120"
    if dest_repo.exists():
        shutil.rmtree(dest_repo)
    dest_repo.mkdir()
    for f in sorted(pathlib.Path("/home/z/my-project/work/instructions")
                    .glob("*.txt")):
        shutil.copy2(f, dest_repo / f.name)
        print(f"  [dépôt] {f.name}")

    # (2) LE DOSSIER D'ARCHIVE AU COFFRE (créé si absent)
    r = api("GET", "/drive/v3/files", params={
        "q": f"'{ARCHIVE}' in parents and name='instructions_vague10_"
             f"20261120' and trashed=false",
        "fields": "files(id,name)", "pageSize": 10})
    dossiers = r.json().get("files", [])
    if dossiers:
        id_arch = dossiers[0]["id"]
        print(f"  [coffre] le dossier d'archive existe : {id_arch}")
    else:
        r = api("POST", "/drive/v3/files",
            params={"supportsAllDrives": "true"},
            json_body={
                "name": "instructions_vague10_20261120",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [ARCHIVE]})
        id_arch = r.json()["id"]
        print(f"  [coffre] le dossier d'archive créé : {id_arch}")

    # (3) LE DÉPLACEMENT : chaque fichier /instructions → l'archive
    r = api("GET", "/drive/v3/files", params={
        "q": f"'{DOSSIER_INSTRUCTIONS}' in parents and trashed=false",
        "fields": "files(id,name)", "pageSize": 100})
    fichiers = r.json().get("files", [])
    if not fichiers:
        print("  [coffre] le /instructions est DÉJÀ vide")
    for f in sorted(fichiers, key=lambda x: x["name"]):
        # LE GESTE EN DEUX ÉTAPES (l'appel combiné add+remove reçoit
        # « Increasing the number of parents is not allowed » pour les
        # pièces du déposant — le retrait PUIS l'ajout, chacun admis :
        # l'écart vécu nommé, la séquence corrigée)
        r = api("PATCH",
                f"/drive/v3/files/{f['id']}",
                params={"removeParents": DOSSIER_INSTRUCTIONS,
                        "supportsAllDrives": "true"},
                json_body={})
        r = api("PATCH",
                f"/drive/v3/files/{f['id']}",
                params={"addParents": id_arch,
                        "supportsAllDrives": "true"},
                json_body={})
        if r.status_code not in (200, 204):
            print(f"  !! ÉCHEC {f['name']} : {r.status_code} {r.text[:120]}")
            return 2
        print(f"  [archivé] {f['name']} → instructions_vague10_20261120/")

    # (4) LA VÉRIFICATION : le /instructions vide, l'archive à six
    r = api("GET", "/drive/v3/files", params={
        "q": f"'{DOSSIER_INSTRUCTIONS}' in parents and trashed=false",
        "fields": "files(id,name)", "pageSize": 100})
    reste = r.json().get("files", [])
    r2 = api("GET", "/drive/v3/files", params={
        "q": f"'{id_arch}' in parents and trashed=false",
        "fields": "files(id,name)", "pageSize": 100})
    archives = r2.json().get("files", [])
    print(f"  [vérification] le /instructions porte {len(reste)} fichier(s) ;"
          f" l'archive en porte {len(archives)}")
    if reste:
        print("  !! le /instructions n'est pas vide — refus")
        return 2
    if len(archives) != 6:
        print("  !! l'archive ne porte pas les six — refus")
        return 2
    print("LES SIX INSTRUCTIONS ARCHIVÉES — le /instructions VIDE : la "
          "vague 11 attend ses instructions au commandement du maître")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
