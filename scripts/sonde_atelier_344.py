#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sonde_atelier_344.py — LA SONDE DE L'ATELIER DU TERRAIN au coffre /test
(l'Entrée 344, la session du guide de la ligne de carnet) : l'atelier
atelier-campagne-d204-20261114-013520/ à la racine du /test porte les
QUATRE registres du livre (carnet_temps_humain.csv M3, livraisons.csv M1,
defauts.csv D202, journal-ouverture.txt) — chaque registre RAPATRIÉ au bac
scripts/campagne_d204/guide-ligne-carnet-344/epreuves/ par DOUBLE
téléchargement byte-byte (md5 == la métadonnée Drive, échec fermé),
l'état constaté : AUCUNE ligne D210 ne vit au livre (la dernière livraison
C-app-it3 du 16/11, la dernière ligne M3 tag-backup du 16/11) — les DEUX
lignes des runs recoupés (Entrées 340 et 343) attendent le geste du
développeur (le présent guide)."""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
ATELIER = "atelier-campagne-d204-20261114-013520"
BAC = REPO / "scripts" / "campagne_d204" / "guide-ligne-carnet-344"
EPREUVES = BAC / "epreuves"

LIVRAISONS_2LIGNES = [
    "T-loupe-02-d210-it1,T,loupe-02-d210,1,2026-11-17,2026-11-17,VERT,en attente",
    "T-loupe-08-d210-it1,T,loupe-08-d210,1,2026-11-18,2026-11-18,VERT,en attente",
]


def telecharge(file_id):
    st, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    if st != 200:
        raise RuntimeError(f"téléchargement impossible ({st})")
    return body


def main():
    EPREUVES.mkdir(parents=True, exist_ok=True)
    racine = ds.list_folder(TEST_ID)
    atelier = racine.get(ATELIER)
    if atelier is None or atelier["mimeType"] != ds.FOLDER_MIME:
        print("[ÉCART] l'atelier " + ATELIER + " introuvable à la racine "
              "du /test")
        return 1
    print("[atelier] " + ATELIER + "/ (id " + atelier["id"][:16] + "…)")
    ent = ds.list_folder(atelier["id"])
    tout_vert = True
    for nom in ("carnet_temps_humain.csv", "livraisons.csv",
                "defauts.csv", "journal-ouverture.txt"):
        it = ent.get(nom)
        if it is None:
            print(f"[ÉCART] {nom} absent de l'atelier")
            tout_vert = False
            continue
        md5_meta = it.get("md5Checksum", "")
        # LE DOUBLE TÉLÉCHARGEMENT (le geste établi : deux voix, md5 == la
        # métadonnée Drive)
        b1 = telecharge(it["id"])
        b2 = telecharge(it["id"])
        md5_1 = hashlib.md5(b1).hexdigest()
        ok = (b1 == b2) and (md5_1 == md5_meta)
        sha = hashlib.sha256(b1).hexdigest()
        dst = EPREUVES / nom
        dst.write_bytes(b1)
        txt = b1.decode("utf-8", "replace")
        lignes = txt.rstrip("\n").split("\n")
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} : {len(b1)} o, "
              f"md5 {md5_1[:12]}…, sha256 {sha[:16]}…, "
              f"{len(lignes)} lignes, LF final "
              f"{'oui' if b1.endswith(chr(10).encode()) else 'NON'}")
        print(f"        la dernière ligne : {lignes[-1][:90]}")
        tout_vert &= ok

    # LE CONSTAT D'ÉTAT : aucune ligne D210 au livre
    liv = (EPREUVES / "livraisons.csv").read_text(encoding="utf-8")
    d210 = [l for l in liv.splitlines() if "d210" in l]
    msg = ("aucune — les DEUX runs recoupés (Entrées 340/343) attendent "
           "le geste" if not d210 else str(d210))
    print("[constat] livraisons.csv : " + str(len(d210))
          + " ligne(s) D210 (" + msg + ")")
    carnet = (EPREUVES / "carnet_temps_humain.csv").read_text(
        encoding="utf-8")
    d210c = [l for l in carnet.splitlines() if "d210" in l]
    print("[constat] carnet_temps_humain.csv : " + str(len(d210c))
          + " ligne(s) D210 ("
          + ("aucune" if not d210c else str(d210c)) + ")")

    # LA RÉFÉRENCE-APRÈS-GESTE (le § 5 du guide : le livre + les DEUX lignes)
    ref = BAC / "reference-apres-geste"
    ref.mkdir(parents=True, exist_ok=True)
    apres = liv
    if not apres.endswith("\n"):
        apres += "\n"
    for l in LIVRAISONS_2LIGNES:
        apres += l + "\n"
    (ref / "livraisons.csv").write_text(apres, encoding="utf-8",
                                        newline="")
    b = (ref / "livraisons.csv").read_bytes()
    print(f"[référence-après-geste] livraisons.csv : {len(b)} o, sha256 "
          f"{hashlib.sha256(b).hexdigest()}")
    print("[sonde] TOUT VERT — les QUATRE registres rapatriés byte-byte, "
          "l'état constaté, la référence-après-geste née"
          if tout_vert else "[sonde] ÉCARTS NOMMÉS ci-dessus")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
