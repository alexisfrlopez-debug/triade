#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 216 (complément) — le résidu loupe-kit/ nommé et nettoyé.

LE FAIT : la racine du /test porte un résidu — loupe-kit/ (sans
numéro), le dossier du SIXIÈME RUN (l'Entrée 209 : « déposé kit et
preuves ENSEMBLE — la première fois »). Ses preuves furent archivées
par DÉPLACEMENT à l'Entrée 211 (preuves-run-loupe-dev6/) MAIS le
dossier lui-même demeura — ET temoin-edition.bin (LA PREUVE de
l'Entrée 209 : « la preuve était dans le fichier : temoin-edition.bin
portait 0x4D à l'octet 0 — LA SAUVEGARDE AVAIT EU LIEU ») n'était
NULLE PART AUX ARCHIVES : le dossier du run en était la SEULE
demeure.

LE GESTE : la preuve rapatriée et archivée à preuves-run-loupe-dev6/
(recoupée) PUIS le dossier du run corbeillé (D99 : un dossier neuf par
run, l'ancien meurt archivé) — ses pièces de kit sont la vague dev.6
versionnée [LISEZMOI 671af4da… == vagues-m10/LISEZMOI-loupe-dev.6.txt],
temoin-fichier.bin et temoin-session.bin == loupe.exe dev.6 octet pour
octet (l'identité, consignée au verdict), la racine purgée du résidu.
"""
import hashlib
import json
import pathlib
import sys
import urllib.request

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
MD5_EDITION = "57f4cd461ad5"          # temoin-edition.bin (le témoin du run 6)
DEST = pathlib.Path("/home/z/my-project/upload/run-dev11")


def main():
    racine = ds.list_folder(TEST)
    lk = racine.get("loupe-kit")
    assert lk, "le résidu loupe-kit/ est déjà absent"
    pieces = ds.list_folder(lk["id"])
    edition = pieces["temoin-edition.bin"]
    assert edition["md5Checksum"].startswith(MD5_EDITION), \
        f"temoin-edition.bin diverge : {edition['md5Checksum']}"
    print(f"[complément] temoin-edition.bin : md5 {MD5_EDITION}… — LA PREUVE du run 6")

    # 1. la preuve rapatriée (l'octet recoupé à l'arrivée)
    st, body, _ = ds.api("GET", f"{ds.API}/files/{edition['id']}?alt=media")
    assert st == 200, f"téléchargement impossible ({st})"
    chemin = DEST / "temoin-edition-run6.bin"
    chemin.write_bytes(body)
    assert hashlib.md5(body).hexdigest().startswith(MD5_EDITION), "md5 diverge !"
    print(f"[complément] la preuve rapatriée : {len(body):,} o".replace(",", " "))

    # 2. la preuve archivée à preuves-run-loupe-dev6/ (recoupée)
    ap = ds.list_folder(racine["archives-preuves"]["id"])
    dev6 = ap["preuves-run-loupe-dev6"]
    courants = ds.list_folder(dev6["id"])
    if "temoin-edition.bin" not in courants:
        import uuid
        frontiere = uuid.uuid4().hex
        meta = json.dumps({"name": "temoin-edition.bin", "parents": [dev6["id"]]})
        payload = (f"--{frontiere}\r\n"
                   f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
                   f"{meta}\r\n"
                   f"--{frontiere}\r\n"
                   f"Content-Type: application/octet-stream\r\n\r\n").encode() \
            + body + f"\r\n--{frontiere}--".encode()
        req = urllib.request.Request(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            data=payload, method="POST",
            headers={"Authorization": "Bearer " + ds.get_access_token(),
                     "Content-Type": f"multipart/related; boundary={frontiere}"})
        with urllib.request.urlopen(req) as r:
            json.load(r)
    apres = ds.list_folder(dev6["id"])
    assert apres["temoin-edition.bin"]["md5Checksum"].startswith(MD5_EDITION), \
        "le recoup de la preuve archivée échoue"
    print("[complément] temoin-edition.bin archivé à preuves-run-loupe-dev6/ — recoupé")

    # 3. le dossier du run corbeillé (D99) — ses pièces : la vague dev.6
    #    versionnée, les témoins fichiers == loupe.exe dev.6 (l'identité)
    assert pieces["LISEZMOI-KIT-LOUPE.md"]["md5Checksum"].startswith("671af4da"), \
        "le LISEZMOI du résidu n'est pas la vague dev.6 versionnée"
    for temoin in ("temoin-fichier.bin", "temoin-session.bin"):
        assert pieces[temoin]["md5Checksum"] == pieces["loupe.exe"]["md5Checksum"], \
            f"{temoin} != loupe.exe (l'identité du run 6)"
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{lk['id']}",
        method="PATCH",
        data=json.dumps({"trashed": True}).encode(),
        headers={"Authorization": "Bearer " + ds.get_access_token(),
                 "Content-Type": "application/json"})
    urllib.request.urlopen(req)
    racine2 = ds.list_folder(TEST)
    assert "loupe-kit" not in racine2, "le résidu demeure !"
    noms = [f["name"] for f in ds.list_folder(TEST).values()]
    doubles = sorted({n for n in noms if noms.count(n) > 1})
    assert not doubles, f"DOUBLONS : {doubles}"
    print(f"[complément] loupe-kit/ corbeillé — la racine : {len(racine2)} entrées, "
          f"aucun résidu, aucun doublon")
    return 0


if __name__ == "__main__":
    sys.exit(main())
