#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 222 — rapatriement des preuves du douzième run (kit-loupe/ au /test).

Le développeur a déposé le dossier du run 12 — kit-loupe/ — avec ses
preuves (preuves-loupe/ : les deux témoins + temoin-fichier.bin né du
bat). Rapatriement par ID (le listing nom-clé cache les doublons), vers
upload/run-011-dev1/ (zone d'entrée terrain, jamais commitée).

Recoup en DEUX temps : (1) le md5 COMPLET des métadonnées Drive est
asserté == le md5 du corps téléchargé (l'intégrité du transport) ;
(2) l'identité des pièces aux canoniques de l'Entrée 221 (loupe.exe
c1115105…, scenario 77872b71…, bat 2a3f22f4…, LISEZMOI 70340163…)
se joue dans recouper_run12_011.py sur les corps arrivés.
"""

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DEST = pathlib.Path("/home/z/my-project/upload/run-011-dev1")
DEST.mkdir(parents=True, exist_ok=True)

# (id Drive, nom attendu) — les IDs du listing intégral de la session
PIECES = [
    # les QUATRE pièces du kit tel que couru (recoup pièce à pièce — Entrée 221)
    ("1K0ELMg2asdt3Gx5H1H7ejc6VFkcLZLvV", "loupe.exe"),
    ("149aMLyy01dB1VA-ZIbHttTiOUiHjTuJm", "scenario-loupe.py"),
    ("1XiA4y3tO-H1uRHcRofwVdwrJ7peRkHQX", "temoin-vitrine.bat"),
    ("1OgfAYPAxyeDmNPHfOMXCcoR_1ZFHzZEj", "LISEZMOI-KIT-LOUPE.md"),
    # la pièce née du run (le bat copie loupe.exe → temoin-fichier.bin)
    ("13hsoQ0N-a2R3KVnlp91P4ApqGtOBB7Bs", "temoin-fichier.bin"),
    # LES DEUX TÉMOINS — les preuves du run
    ("11Iqm3y7qzLBZvCN-JL1OBdHmNvMLz67i", "temoin-loupe.txt"),
    ("1qHgToh2Ov5n55JQrw79xMqXmKx-diR6o", "temoin-vitrine.txt"),
]


def main():
    erreurs = 0
    for fid, nom in PIECES:
        # (1) le md5 des métadonnées (le listing complet de la session)
        st, meta, _ = ds.api("GET", f"{ds.API}/files/{fid}"
                                  "?fields=id,name,md5Checksum,size")
        if st != 200:
            print(f"[Run12-0.1.1] ERREUR métadonnées {nom} : HTTP {st}",
                  file=sys.stderr)
            erreurs += 1
            continue
        meta = json.loads(meta)
        md5_attendu = (meta.get("md5Checksum") or "").lower()
        # (2) le corps
        st, body, _ = ds.api("GET", f"{ds.API}/files/{fid}?alt=media")
        if st != 200:
            print(f"[Run12-0.1.1] ERREUR {nom} : HTTP {st}", file=sys.stderr)
            erreurs += 1
            continue
        dest = DEST / nom
        dest.write_bytes(body)
        md5 = hashlib.md5(body).hexdigest()
        sha256 = hashlib.sha256(body).hexdigest()
        ok = "OK " if md5 == md5_attendu else "DIVERGE"
        if ok != "OK ":
            erreurs += 1
        print(f"[Run12-0.1.1] {ok} {nom} : {len(body):,} o, "
              f"md5 {md5}, sha256 {sha256}".replace(",", " "))
    print(f"[Run12-0.1.1] bilan : {len(PIECES) - erreurs}/{len(PIECES)} "
          f"pièces rapatriées et recoupées")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
