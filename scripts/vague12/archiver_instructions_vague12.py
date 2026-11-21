#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_instructions_vague12.py — L'ARCHIVAGE DES SIX INSTRUCTIONS DE
LA VAGUE 12 après exécution (la règle du maître : « nouvelles instructions
ici, à archiver après exécution ») : LE GESTE EN DEUX ÉTAPES au coffre —
le retrait du /instructions PUIS l'ajout au dossier ARCHIVE du coffre
(l'appel combiné add+remove reçoit « Increasing the number of parents is
not allowed » pour les pièces du déposant — l'écart vécu aux vagues 10-11,
la séquence corrigée reconduite). Le dépôt a vécu son git mv au commit
3f64781 ; le /instructions LAISSÉ VIDE — la vague 13 attend ses
instructions au commandement du maître."""
import json
import sys

sys.path.insert(0, "/home/z/my-project/depot/scripts/vague11")
from drive_sa_v220 import api, liste  # noqa: E402
# les écritures au RELAIS (le compte de service demeure
# LECTEUR seul — la limite D101) : qui="relais" aux gestes

PROJET = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
DOSSIER_INSTRUCTIONS = "1uL8fMoXDW9tSsG0L2RoniBYKIjJTLVI6"
ATTENDUES = ["Qwen__20261120_0uug27teo.txt",
             "Qwen__20261120_14n3k8gd7.txt",
             "Qwen__20261120_6kbfrpn7k.txt",
             "Qwen__20261120_alhmpl35u.txt",
             "Qwen__20261120_pgodgk35l.txt",
             "Qwen__20261120_x705m50vl.txt"]


def main() -> int:
    # (1) le dossier ARCHIVE du coffre (son ID cherché au projet)
    st, body = api("GET", "/files", {
        "q": f"'{PROJET}' in parents and name='ARCHIVE' and trashed=false",
        "fields": "files(id,name)", "pageSize": 5})
    assert st == 200, f"le projet : HTTP {st}"
    archives = json.loads(body).get("files", [])
    assert archives, "le dossier ARCHIVE introuvable au projet"
    ARCHIVE = archives[0]["id"]
    print(f"  [coffre] le dossier ARCHIVE : {ARCHIVE}")

    # (2) le sous-dossier instructions_vague12_20261121 (créé si absent)
    st, body = api("GET", "/files", {
        "q": f"'{ARCHIVE}' in parents and "
             f"name='instructions_vague12_20261121' and trashed=false",
        "fields": "files(id,name)", "pageSize": 10})
    dossiers = json.loads(body).get("files", [])
    if dossiers:
        id_arch = dossiers[0]["id"]
        print(f"  [coffre] le dossier d'archive existe : {id_arch}")
    else:
        st, body = api("POST", "/files", qui="relais",
                       params={"supportsAllDrives": "true"},
                       json_body={
                           "name": "instructions_vague12_20261121",
                           "mimeType":
                               "application/vnd.google-apps.folder",
                           "parents": [ARCHIVE]})
        assert st == 200, f"la création : HTTP {st} {body[:200]}"
        id_arch = json.loads(body)["id"]
        print(f"  [coffre] le dossier d'archive créé : {id_arch}")

    # (3) LE GESTE EN DEUX ÉTAPES : chaque fichier /instructions → archive
    fichiers = liste(DOSSIER_INSTRUCTIONS)
    noms = sorted(f["name"] for f in fichiers)
    if not fichiers:
        print("  [coffre] le /instructions est DÉJÀ vide")
    assert noms == sorted(ATTENDUES), \
        f"le /instructions ne porte pas les six attendues : {noms}"
    for f in sorted(fichiers, key=lambda x: x["name"]):
        st, _ = api("PATCH", f"/files/{f['id']}", qui="relais",
                    params={"removeParents": DOSSIER_INSTRUCTIONS,
                            "supportsAllDrives": "true"},
                    json_body={})
        assert st in (200, 204), f"le retrait {f['name']} : HTTP {st}"
        st, body2 = api("PATCH", f"/files/{f['id']}", qui="relais",
                        params={"addParents": id_arch,
                                "supportsAllDrives": "true"},
                        json_body={})
        assert st in (200, 204), \
            f"l'ajout {f['name']} : HTTP {st} {body2[:120]}"
        print(f"  [archivé] {f['name']} → instructions_vague12_20261121/")

    # (4) LA VÉRIFICATION : le /instructions vide, l'archive à six
    reste = liste(DOSSIER_INSTRUCTIONS)
    archives6 = liste(id_arch)
    print(f"  [vérification] le /instructions porte {len(reste)} "
          f"fichier(s) ; l'archive en porte {len(archives6)}")
    if reste:
        print("  !! le /instructions n'est pas vide — refus")
        return 2
    if len(archives6) != 6:
        print("  !! l'archive ne porte pas les six — refus")
        return 2
    print("LES SIX INSTRUCTIONS ARCHIVÉES AU COFFRE — le /instructions "
          "VIDE : la vague 13 attend ses instructions au commandement "
          "du maître")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
