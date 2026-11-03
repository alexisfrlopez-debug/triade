#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_coffre_cf1.py — rapatrie le conteneur TRIADE-CF1 (coffre_fort.bin)
de la RACINE du coffre Drive « Triade » vers upload/, md5 contrôlé contre la
valeur ATTESTÉE au journal (Entrée « La question du terrain », 0323029a…) —
la relève après recyclage du labo, modèle LISEZMOI-PHRASE-CONTROLE.txt
(« RESTAURATION APRÈS UNE PANNE D'INFRA »).

Lecture seule : ne touche ni au Drive, ni à .keys/ (le dépôt du coffre dans
.keys/ est un geste distinct, par coffre_fort.py importer). Aucun secret
n'est affiché.

Usage : python3 scripts/rapatrier_coffre_cf1.py
Code de sortie : 0 = rapport conforme, 1 = écart nommé, 2 = erreur fatale.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

MD5_ATTESTE = "23a2987a9817"       # D144 (04/11) : graine-ed25519-cartes
                                   # entrée ajoutée (1158 o -> 1906 o) ; la
                                   # valeur D80 0323029a… vit à l'Entrée 135
TAILLE_ATTENDUE = 1906             # 3 entrées : D74 + D80 + graine cartes
DEST = REPO / "upload"


def telecharger(file_id: str, destination: pathlib.Path) -> str:
    """Télécharge le contenu binaire d'un fichier Drive (authentifié)."""
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)
    return ds.md5_of(destination)


def main() -> int:
    DEST.mkdir(exist_ok=True)
    try:
        entries = ds.list_folder(ds.DRIVE_ROOT_ID)
    except Exception as exc:  # noqa: BLE001
        print(f"[coffre] ERREUR FATALE : listage racine impossible : {exc}",
              file=sys.stderr)
        return 2
    f = entries.get("coffre_fort.bin")
    if not f or f.get("mimeType") == ds.FOLDER_MIME:
        print("[coffre] ERREUR : coffre_fort.bin ABSENT de la racine du Drive",
              file=sys.stderr)
        return 2
    md5_distant = f.get("md5Checksum", "-")
    taille = f.get("size", "?")
    print(f"[coffre] racine Drive : coffre_fort.bin {taille} o, "
          f"md5 distant {md5_distant[:12]}…")
    ecarts = 0
    if not md5_distant.startswith(MD5_ATTESTE):
        print(f"[coffre] ÉCART NOMMÉ : md5 distant {md5_distant} != "
              f"attesté {MD5_ATTESTE}… (le conteneur a-t-il changé ? "
              f"— ne rien conclure, rapporter)")
        ecarts += 1
    if taille != TAILLE_ATTENDUE:
        print(f"[coffre] ÉCART NOMMÉ : taille {taille} != {TAILLE_ATTENDUE} o")
        ecarts += 1
    destination = DEST / "coffre_fort.bin"
    md5_local = telecharger(f["id"], destination)
    print(f"[coffre] rapatrié : {destination} ({destination.stat().st_size} o, "
          f"md5 {md5_local[:12]}…)")
    if md5_local != md5_distant:
        print(f"[coffre] ÉCART NOMMÉ : md5 local {md5_local} != distant "
              f"{md5_distant} (téléchargement corrompu ?)")
        ecarts += 1
    if ecarts == 0:
        print("[coffre] CONFORME : le conteneur D80 attesté est bien là, "
              "intact — la relève peut suivre (coffre_fort.py importer)")
        return 0
    print(f"[coffre] {ecarts} écart(s) nommé(s) — le fichier local reste "
          "disponible pour analyse, RIEN n'est conclu ni écrit ailleurs")
    return 1


if __name__ == "__main__":
    sys.exit(main())
