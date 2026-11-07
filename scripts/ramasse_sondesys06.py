#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ramasse_sondesys06.py — rapatrie les pièces du RUN DE LA SONDE SYS-06
(m9-(g)) depuis /test/preuves-sonde-sys06 (le coffre du développeur) vers
download/preuves-sonde-sys06/, md5 contrôlé par pièce contre les
métadonnées Drive (modèle ramasse_run6 / ramasse_run5, D99 : zéro
mélange — dossier dédié au run de la sonde ; lecture seule, AUCUNE
écriture Drive).

LA SONDE NOMMÉE D'AVANCE (le recoup-5, la passation 107), OUVERTE (le
recoup du run 6 : LE JUMEAU, le -7 reproduit identique, LE PASSAGER
ÉLIMINÉ SUR PIÈCES) — le développeur l'a JOUÉE et le message est venu :
« preuves déposées dans le dossier /test du drive ».

Le trio TOUJOURS écrit par le scénario (même ROUGE — le témoin consigne
chaque sortie) :
  temoin-sonde-sys06.txt, sonde-sys06-journal.log, VERDICT-sonde-sys06.txt

Les DEUX pièces conditionnelles (nées seulement si le run va assez
loin — SI LA CONTRE-ÉPREUVE S4 A TENU : LA PERCÉE) :
  ligne-recue.txt (la ligne applicative DÉCHIFFRÉE PAR LA MACHINE),
  journal-emissions.txt (tout ce que la machine a émis)
— leur absence N'EST PAS une erreur de rapatriement : elle est CONSTATÉE
et nommée (le témoin dit où le run s'est arrêté ; l'ordre
lexicographique de la maison).

Usage : python3 scripts/ramasse_sondesys06.py
Code de sortie : 0 = pièces présentes toutes conformes ; 1 = écart ;
2 = erreur fatale (réceptacle ou trio absent)."""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
DEST = pathlib.Path("/home/z/my-project/download/preuves-sonde-sys06")

TRIO = {"temoin-sonde-sys06.txt", "sonde-sys06-journal.log",
        "VERDICT-sonde-sys06.txt"}
CONDITIONNELLES = {"ligne-recue.txt", "journal-emissions.txt"}
ATTENDUES = TRIO | CONDITIONNELLES


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-sonde-sys06")
        if not preuves or preuves.get("mimeType") != ds.FOLDER_MIME:
            print("[preuves-sonde-sys06] ERREUR FATALE : le réceptacle "
                  "absent du coffre", file=sys.stderr)
            return 2
        entries = ds.list_folder(preuves["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"[preuves-sonde-sys06] ERREUR FATALE : listage impossible : "
              f"{exc}", file=sys.stderr)
        return 2

    deposees = {n for n, f in entries.items()
                if f.get("mimeType") != ds.FOLDER_MIME}
    pieces = {n: f for n, f in entries.items()
              if f.get("mimeType") != ds.FOLDER_MIME and n in ATTENDUES}
    manquantes_trio = TRIO - set(pieces)
    if manquantes_trio:
        print(f"[preuves-sonde-sys06] ERREUR FATALE : le trio de la sonde "
              f"absent du coffre : {sorted(manquantes_trio)}",
              file=sys.stderr)
        return 2

    total, ok = 0, 0
    for nom, f in sorted(pieces.items()):
        total += 1
        url = f"{ds.API}/files/{f['id']}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[preuves-sonde-sys06] ÉCHEC téléchargement {nom} "
                  f"(HTTP {st})")
            continue
        chemin = DEST / nom
        chemin.write_bytes(body)
        local = ds.md5_of(chemin)
        attendu = (f.get("md5Checksum") or "").lower()
        if attendu and local != attendu:
            print(f"[preuves-sonde-sys06] ÉCART md5 {nom} : local {local} "
                  f"!= drive {attendu}")
            continue
        ok += 1
        print(f"[preuves-sonde-sys06] {nom} : {len(body)} o, md5 "
              f"{local[:8]}… == drive — CONSTATÉ")

    absentes = ATTENDUES - set(pieces)
    if absentes:
        print(f"[preuves-sonde-sys06] NOTE : pièces NON DÉPOSÉES (le run "
              f"ne les a pas portées jusque-là) : {sorted(absentes)} — le "
              f"témoin dira où il s'est arrêté")
    extras = deposees - ATTENDUES - {"LISEZMOI-preuves.txt"}
    if extras:
        print(f"[preuves-sonde-sys06] note : entrées non-pièces ignorées : "
              f"{sorted(extras)}")
    if ok != total:
        print(f"[preuves-sonde-sys06] ÉCHEC : {ok}/{total} pièces conformes")
        return 1
    print(f"[preuves-sonde-sys06] {ok}/{total} pièces CONSTATÉES md5 dans "
          f"{DEST} — le recoup sur pièces peut commencer (D138/D145/D148)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
