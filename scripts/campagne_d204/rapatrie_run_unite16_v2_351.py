#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrie_run_unite16_v2_351.py — le rapatriement COMPLET du dépôt du re-run
refusé : les entrées de kit-unite-04-d210-20261118-v2/ (les pièces du kit v2
livré + les pièces nées du run v2 refusé), DOUBLE téléchargement byte-byte
(md5 == la métadonnée Drive, échec fermé). Puis le recoup des pièces du kit
contre le staging du labo (le bac unite-16-T-d210/kit/…-v2) — la règle R10
« la même pièce ». Et le recoup de L'ATELIER du coffre (les QUATRE registres
INCHANGÉS depuis la 348 — le GUI s'arrêta au refus AVANT le livre).

Usage : python3 scripts/campagne_d204/rapatrie_run_unite16_v2_351.py
"""

import hashlib
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = pathlib.Path(__file__).resolve().parent / "depot-run-unite16-d210-v2-351" / "epreuves"
KIT_LABO = pathlib.Path(__file__).resolve().parent / "unite-16-T-d210" / "kit" / "kit-unite-04-d210-20261118-v2"


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
    depot = ds.list_folder(test["kit-unite-04-d210-20261118-v2"]["id"])
    logs = ds.list_folder(depot["TRIADE_logs"]["id"])

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
    print(f"[RAPATRIEMENT] {n} fichiers — {'TOUT VERT' if echecs == 0 else str(echecs) + ' ÉCHECS'}")

    # LE RECOUP des pièces du kit v2 contre le staging du labo (R10)
    print("[RECOUP] les pièces du kit v2 livré == le staging du labo :")
    vert = 0
    total = 0
    for p in sorted(KIT_LABO.iterdir()):
        if not p.is_file():
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

    # LE RECOUP DE L'ATELIER DU COFFRE (R7 — le GUI s'arrêta AVANT le livre :
    # les QUATRE registres doivent demeurer l'état de la 348, byte-byte)
    print("[ATELIER] les QUATRE registres du coffre == l'état de la 348 :")
    ref_348 = pathlib.Path(__file__).resolve().parent / \
        "depot-run-unite13-d210-348" / "epreuves" / "atelier"
    atelier = ds.list_folder(test["atelier-campagne-d204-20261114-013520"]["id"])
    verts_atelier = 0
    for nom in ("livraisons.csv", "carnet_temps_humain.csv",
                "defauts.csv", "journal-ouverture.txt"):
        meta = atelier.get(nom)
        if not meta:
            print(f"  [ABSENT] {nom}")
            continue
        st, body, _ = ds.api("GET", ds.API + f"/files/{meta['id']}?alt=media")
        if st != 200:
            print(f"  [ÉCHEC] {nom} : HTTP {st}")
            continue
        ref = ref_348 / nom
        if ref.exists() and body == ref.read_bytes():
            verts_atelier += 1
            print(f"  [INCHANGÉ] {nom} : {len(body)} o == l'état de la 348 "
                  f"byte-byte (le GUI n'a RIEN écrit — le refus précède le livre)")
        else:
            print(f"  [DIVERGE] {nom} : {len(body)} o contre la référence 348")
    print(f"[ATELIER] {verts_atelier}/4 registres INCHANGÉS depuis la 348")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
