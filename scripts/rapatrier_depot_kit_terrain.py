#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_depot_kit_terrain.py — rapatrie les pièces du dépôt du développeur
« dossier kit terrain avec preuves déposé dans /test du drive » : l'arbre du
paquet AUTO retéléversé avec les preuves de run (kit-1 shani, kit-3 loupe).

S'appuie sur le manifeste daté du sondage (sondage_depot_kit_terrain.json).
Vérifie le md5 de chaque pièce téléchargée contre les métadonnées Drive.

Usage : python3 scripts/rapatrier_depot_kit_terrain.py
"""

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DEST = REPO / "preuves-depot-auto-terrain"

# Les pièces du dépôt : les TROIS preuves de run + les pièces de recoupement
# (scénario, moteur, cibles, loupe) pour la chaîne de garde.
PIECES = [
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/preuves-shani/VERDICT-run-shani.txt",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/preuves-shani/scenario-shani-journal.log",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/preuves-loupe/temoin-loupe.txt",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/scenario-shani.py",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/moteur-shani.bin",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/cibles/manifeste.json",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/cibles/proxy-image.bin",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/LISEZMOI-shani.txt",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/loupe.exe",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/scenario-loupe.py",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/temoin-vitrine.bat",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/LISEZMOI-KIT-LOUPE.md",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/LISEZMOI-terrain-tiers.txt",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-2-dudect/dudect_v150.c",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-2-dudect/test_appel.c",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-2-dudect/dudect_v150.exe",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-2-dudect/test_appel.exe",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-2-dudect/LANCER-KIT-2-DUDECT.bat",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-1-shani/LANCER-KIT-1-SHANI.bat",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/pc-windows/kit-3-terrain-tiers-loupe/LANCER-KIT-3-LOUPE.bat",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/COMMENCER-ICI.bat",
    "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO/A-LIRE-AUTOMATISATION.txt",
]


def telecharger(file_id, destination):
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.write_bytes(body)


def empreintes(p: pathlib.Path):
    md5 = hashlib.md5(p.read_bytes()).hexdigest()
    sha256 = hashlib.sha256(p.read_bytes()).hexdigest()
    return md5, sha256


def main() -> int:
    manifeste = json.loads(
        (REPO / "scripts" / "sondage_depot_kit_terrain.json").read_text())
    index = {e["chemin"]: e for e in manifeste if not e["dossier"]}
    DEST.mkdir(parents=True, exist_ok=True)
    erreurs = 0
    for chemin in PIECES:
        e = index.get(chemin)
        if not e:
            print(f"[Dépôt] ABSENT du manifeste : {chemin}", file=sys.stderr)
            erreurs += 1
            continue
        nom_local = chemin.strip("/").replace("/", "_")
        dest = DEST / nom_local
        try:
            telecharger(e["id"], dest)
            md5, sha256 = empreintes(dest)
            ok = "VERT" if md5 == e["md5"] else "ROUGE"
            if md5 != e["md5"]:
                erreurs += 1
            print(f"[{ok}] {nom_local}  {e['taille']} o  "
                  f"md5={md5[:12]}…  sha256={sha256[:12]}…  "
                  f"créé={e['cree'][:19]}  modifié={e['modifie'][:19]}")
        except ds.SyncError as exc:
            print(f"[ROUGE] {chemin} : {exc}", file=sys.stderr)
            erreurs += 1
    print(f"\n[{len(PIECES) - erreurs}/{len(PIECES)} rapatriées, "
          f"{erreurs} erreur(s)]")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
