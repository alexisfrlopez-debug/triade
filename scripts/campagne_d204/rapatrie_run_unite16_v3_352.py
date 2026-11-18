#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrie_run_unite16_v3_352.py — le rapatriement COMPLET du dépôt du re-run
v3 : les entrées de kit-unite-04-d210-20261118-v3/ (les pièces du kit v3 livré
à la 351 + les pièces nées du run : la console racine, l'état, la session, et
preuves-unite16/ [DEPOT, falsifie-16.bin, la console copiée, temoin-unite16]),
DOUBLE téléchargement byte-byte (md5 == la métadonnée Drive, échec fermé).
Puis le recoup des pièces du kit contre le staging du labo (le bac
unite-16-T-d210/kit/…-v3) — la règle R10 « la même pièce ». Et le rapatriement
de L'ATELIER re-déposé (les QUATRE registres — le livre mis à jour DURANT le
run attendu : la ligne it3 au verdict recopié, la ligne M3 aux bornes observées,
et la chirurgie prescrite it1/it2 à la main du développeur).

Usage : python3 scripts/campagne_d204/rapatrie_run_unite16_v3_352.py
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = pathlib.Path(__file__).resolve().parent / "depot-run-unite16-d210-v3-352" / "epreuves"
KIT_LABO = pathlib.Path(__file__).resolve().parent / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v3"


def telecharge(file_id: str, dest: pathlib.Path, md5_attendu: str) -> bool:
    st, body, _ = ds.api("GET", ds.API + f"/files/{file_id}?alt=media")
    if st != 200:
        print(f"  [ÉCHEC] {dest.name} : HTTP {st}", file=sys.stderr)
        return False
    if hashlib.md5(body).hexdigest() != md5_attendu:
        print(f"  [ÉCHEC] {dest.name} : md5 diverge de la métadonnée", file=sys.stderr)
        return False
    st2, body2, _ = ds.api("GET", ds.API + f"/files/{file_id}?alt=media")
    if st2 != 200 or body2 != body:
        print(f"  [ÉCHEC] {dest.name} : le second téléchargement diverge", file=sys.stderr)
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)
    return True


def main() -> int:
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    test = ds.list_folder(racine["test"]["id"])
    depot = ds.list_folder(test["kit-unite-04-d210-20261118-v3"]["id"])
    logs = ds.list_folder(depot["TRIADE_logs"]["id"])
    preuves = ds.list_folder(depot["preuves-unite16"]["id"])

    echecs = 0
    n = 0
    for nom, meta in sorted(depot.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            continue
        if not telecharge(meta["id"], BAC / nom, meta.get("md5Checksum", "")):
            echecs += 1
        n += 1
    for nom, meta in sorted(logs.items()):
        if not telecharge(meta["id"], BAC / "TRIADE_logs" / nom,
                          meta.get("md5Checksum", "")):
            echecs += 1
        n += 1
    for nom, meta in sorted(preuves.items()):
        if not telecharge(meta["id"], BAC / "preuves-unite16" / nom,
                          meta.get("md5Checksum", "")):
            echecs += 1
        n += 1
    print(f"[RAPATRIEMENT] {n} fichiers — {'TOUT VERT' if echecs == 0 else str(echecs) + ' ÉCHECS'}")

    # LE RECOUP des pièces du kit v3 contre le staging du labo (R10)
    print("[RECOUP] les pièces du kit v3 livré == le staging du labo :")
    vert = 0
    total = 0
    for p in sorted(KIT_LABO.iterdir()):
        if not p.is_file() or p.name == "__pycache__":
            continue
        total += 1
        distant = BAC / p.name
        if not distant.exists():
            print(f"  [ABSENT du dépôt] {p.name}")
            continue
        m_loc = hashlib.md5(p.read_bytes()).hexdigest()
        m_dep = hashlib.md5(distant.read_bytes()).hexdigest()
        if m_loc == m_dep:
            vert += 1
        else:
            print(f"  [DIVERGE] {p.name} : labo {m_loc[:8]}… != dépôt {m_dep[:8]}…")
    print(f"[RECOUP] {vert}/{total} pièces du staging INTACTES au dépôt "
          f"(les pièces nées du run exclues)")

    # LA CONSOLE RACINE == LA CONSOLE DU RÉCEPTACLE (le geste établi de la 348)
    import re
    console_racine = None
    for nom in depot:
        if nom.startswith("run-console-unite16-d210-"):
            console_racine = nom
    if console_racine and (BAC / "preuves-unite16" / console_racine).exists():
        a = (BAC / console_racine).read_bytes()
        b = (BAC / "preuves-unite16" / console_racine).read_bytes()
        print(f"[CONSOLE] racine == preuves-unite16/ : "
              f"{'IDENTIQUES byte-byte' if a == b else 'DIVERGENT'} "
              f"(md5 {hashlib.md5(a).hexdigest()[:8]}…)")

    # LE RAPATRIEMENT DE L'ATELIER RE-DÉPOSÉ (les QUATRE registres)
    print("[ATELIER] les QUATRE registres re-déposés :")
    atelier = ds.list_folder(test["atelier-campagne-d204-20261114-013520"]["id"])
    (BAC / "atelier").mkdir(parents=True, exist_ok=True)
    for nom in ("livraisons.csv", "carnet_temps_humain.csv",
                "defauts.csv", "journal-ouverture.txt"):
        meta = atelier.get(nom)
        if not meta:
            print(f"  [ABSENT] {nom}")
            echecs += 1
            continue
        if not telecharge(meta["id"], BAC / "atelier" / nom,
                          meta.get("md5Checksum", "")):
            echecs += 1
        else:
            print(f"  [OK] {nom} : {(BAC / 'atelier' / nom).stat().st_size} o")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
