#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entrée 215 — rapatriement des preuves du run dev.11 (kit-loupe/ au /test).

Le développeur a déposé le dossier du run — kit-loupe/ — avec ses
preuves (preuves-loupe/ : les deux témoins + temoin-fichier.bin né du
bat). Rapatriement par ID (le listing nom-clé cache les doublons), vers
upload/run-dev11/ (zone d'entrée terrain, jamais commitée), empreintes
recoupées à l'arrivée.
"""
import hashlib
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DEST = pathlib.Path("/home/z/my-project/upload/run-dev11")
DEST.mkdir(parents=True, exist_ok=True)

# (id Drive, nom attendu, md5 attendu — du listing de la session)
PIECES = [
    # les QUATRE pièces du kit tel que couru (recoup pièce à pièce)
    ("1js5BLgHJC7aQWcMRrr6Iv56I36NfV9fF", "loupe.exe",
     "074881be634119c2c3f6babeaeef9684"),
    ("151EZntMK7ERJJGX2-l3xSff3GZSW2ODV", "scenario-loupe.py",
     "f2766d6c964cf147a893574f5537c190"),
    ("1jPltaWT_qljebV_Z2pMkoGDLVufWs5V1", "temoin-vitrine.bat",
     "2236af792a9bc85387aba8c016f0cc27"),
    ("194BxiAxHhT7PZdjkO0Kb9YkiqC3_f1Y2", "LISEZMOI-KIT-LOUPE.md",
     "e9b8c6ab7fcc6aff04930ef30a0db7ba"),
    # la pièce née du run (le bat copie loupe.exe → temoin-fichier.bin)
    ("1YLxUji8DoN-YHR3NcIbkcr4Xeed2CdxV", "temoin-fichier.bin",
     "074881be634119c2c3f6babeaeef9684"),
    # LES DEUX TÉMOINS — les preuves du run
    ("1TrimpFXDgxAZnScnlPQtM7b4z6Nhygkt", "temoin-loupe.txt", None),
    ("1yGci3aAx2ucRHuuy42BgGuV7xFhvBR5u", "temoin-vitrine.txt", None),
]


def main():
    erreurs = 0
    for fid, nom, md5_attendu in PIECES:
        url = f"{ds.API}/files/{fid}?alt=media"
        st, body, _ = ds.api("GET", url)
        if st != 200:
            print(f"[Run11] ERREUR {nom} : HTTP {st}", file=sys.stderr)
            erreurs += 1
            continue
        dest = DEST / nom
        dest.write_bytes(body)
        md5 = hashlib.md5(body).hexdigest()
        sha256 = hashlib.sha256(body).hexdigest()
        ok = "OK " if (md5_attendu is None or md5 == md5_attendu) else "DIVERGE"
        if ok != "OK ":
            erreurs += 1
        print(f"[Run11] {ok} {nom} : {len(body):,} o, md5 {md5[:12]}…, "
              f"sha256 {sha256[:12]}…".replace(",", " "))
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
