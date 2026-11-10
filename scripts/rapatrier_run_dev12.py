#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 217 — rapatriement des preuves du run dev.12 (kit-loupe/ au /test).

Le développeur a déposé le dossier du run 11 — kit-loupe/ — avec ses
preuves (preuves-loupe/ : les deux témoins + temoin-fichier.bin né du
bat). Rapatriement par ID (le listing nom-clé cache les doublons), vers
upload/run-dev12/ (zone d'entrée terrain, jamais commitée), empreintes
recoupées à l'arrivée.
"""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DEST = pathlib.Path("/home/z/my-project/upload/run-dev12")
DEST.mkdir(parents=True, exist_ok=True)

# (id Drive, nom attendu, md5 attendu — du listing intégral de la session)
PIECES = [
    # les QUATRE pièces du kit tel que couru (recoup pièce à pièce)
    ("1rm3269i957rPm28zY7XyRB2rv4nFdRcl", "loupe.exe",
     "074881be634119c2c3f6babeaeef9684"),
    ("1VKoNNxT4CWOuyqSgSqxmo8yDT7TsV4fI", "scenario-loupe.py",
     "7353e7342ff056eeb428f0d78445a7de"),
    ("1RM86XGWuSsQZegEb9iNYn0sZRoaWNVp2", "temoin-vitrine.bat",
     "2d3bc31f54c7140de1d931be0d80fb93"),
    ("1v_e9xFCekGeR_9R1sqUGhGhSjDs-wvtq", "LISEZMOI-KIT-LOUPE.md",
     "8ec9553b0b02fe7ecb25870a427e8e42"),
    # la pièce née du run (le bat copie loupe.exe → temoin-fichier.bin)
    ("1X5iksR9URheRvAU0jdK_kgCX3uVcm5ev", "temoin-fichier.bin",
     "074881be634119c2c3f6babeaeef9684"),
    # LES DEUX TÉMOINS — les preuves du run
    ("1YQdC4-YQzKFzN6wyoy3_fhoAEqIMxVAU", "temoin-loupe.txt", None),
    ("1uQ8VyPAzAQuQ5HWqM2doCoRH8C3jqd6E", "temoin-vitrine.txt", None),
]


def main():
    erreurs = 0
    for fid, nom, md5_attendu in PIECES:
        url = f"{ds.API}/files/{fid}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[Run12] ERREUR {nom} : HTTP {st}", file=sys.stderr)
            erreurs += 1
            continue
        dest = DEST / nom
        dest.write_bytes(body)
        md5 = hashlib.md5(body).hexdigest()
        sha256 = hashlib.sha256(body).hexdigest()
        ok = "OK " if (md5_attendu is None or md5 == md5_attendu) else "DIVERGE"
        if ok != "OK ":
            erreurs += 1
        print(f"[Run12] {ok} {nom} : {len(body):,} o, md5 {md5[:12]}…, "
              f"sha256 {sha256[:12]}…".replace(",", " "))
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
