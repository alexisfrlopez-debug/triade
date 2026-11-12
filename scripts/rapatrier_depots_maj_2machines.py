#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_depots_maj_2machines.py — rapatrie et recoupe les dépôts du
développeur « j'ai lancé le run auto sur 2 ordis différents, j'ai tout mis
dans /test du drive » (12/11/2026, le quatrième geste de la journée) :
  - MISE-A-JOUR  (machine 1) : preuves kit-1 shani + kit-3 loupe
  - MISE-A-JOUR2 (machine 2) : preuves voie 1 M7D (qemu-riscv64 embarqué)

Phase 1 : télécharge les preuves de run fraîches (md5 vérifié contre les
métadonnées Drive).
Phase 2 : recoupe les 46 pièces du paquet de CHAQUE dépôt (md5 Drive) contre
l'arbre local du paquet livré — la chaîne de garde par le contenu.
Phase 3 : lit les preuves rapatriées et écrit le rapport de recoupement.

Usage : python3 scripts/rapatrier_depots_maj_2machines.py
"""

import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

SONDAGE = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour" / "sondage_depots_2machines.json"
PAQUET_LOCAL = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour" / "paquet"
DEST = REPO / "preuves-depots-maj-2machines"

# Les preuves de run fraîches (mtimes postérieurs à l'upload du paquet).
PREUVES_RUN = [
    "pc-windows/kit-1-shani/preuves-shani/VERDICT-run-shani.txt",
    "pc-windows/kit-1-shani/preuves-shani/scenario-shani-journal.log",
    "pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/preuves-loupe/temoin-loupe.txt",
    "qemu-wsl2/kit-m7d/preuves-m7/VERDICT-run-m7d.txt",
    "qemu-wsl2/kit-m7d/preuves-m7/scenario-m7d-journal.log",
    "qemu-wsl2/kit-m7d/preuves-m7/temoin-m7d.txt",
]


def telecharger(file_id: str, destination: pathlib.Path):
    url = f"{ds.API}/files/{file_id}?alt=media"
    st, body, _ = ds.api("GET", url)
    if st != 200:
        raise ds.SyncError(f"téléchargement impossible ({st}) : {body[:120]!r}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(body)
    return hashlib.md5(body).hexdigest()


def md5_local(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def main() -> int:
    manifeste = json.loads(SONDAGE.read_text())
    rapport, verts, rouges = [], 0, 0

    def check(nom: str, ok: bool, detail: str):
        nonlocal verts, rouges
        rapport.append(f"[{'VERT' if ok else 'ROUGE'}] {nom} — {detail}")
        if ok:
            verts += 1
        else:
            rouges += 1

    # ------------------------------------------------------------------
    # PHASE 1 — la chaîne des pièces du paquet (md5 Drive vs md5 local)
    # ------------------------------------------------------------------
    print("=== PHASE 1 : la chaîne des 46 pièces (md5 Drive vs paquet livré) ===")
    locaux = {str(p.relative_to(PAQUET_LOCAL)).replace("\\", "/"): p
              for p in PAQUET_LOCAL.rglob("*") if p.is_file()}
    check("C0", len(locaux) == 46, f"l'arbre local du paquet MISE À JOUR : {len(locaux)} pièces (l'Entrée 249)")

    for depot, info in manifeste.items():
        pieces = info["pieces"]
        index = {p["chemin"].split("/", 1)[1]: p for p in pieces}  # sans le préfixe du dépôt
        # le paquet complet ?
        check(f"{depot}/C1", set(index) == set(locaux),
              f"le dépôt porte les {len(index)} pièces — l'arbre du paquet livré "
              f"{'COMPLET' if set(index) == set(locaux) else 'INCOMPLET OU SURCOMPLET'}")
        # chaque pièce octet pour octet ?
        ecarts = [c for c, p in index.items()
                  if c in locaux and p["md5"] != md5_local(locaux[c])]
        check(f"{depot}/C2", not ecarts,
              f"les {len(index)} pièces vs le paquet livré par md5 : "
              f"{'TOUTES IDENTIQUES' if not ecarts else 'ÉCARTS : ' + ', '.join(ecarts)}")

    # les deux dépôts entre eux
    m1 = {p["chemin"].split("/", 1)[1]: p["md5"] for p in manifeste["MISE-A-JOUR"]["pieces"]}
    m2 = {p["chemin"].split("/", 1)[1]: p["md5"] for p in manifeste["MISE-A-JOUR2"]["pieces"]}
    communs = set(m1) & set(m2)
    divergents = [c for c in communs if m1[c] != m2[c]]
    check("C3", not divergents,
          f"les DEUX machines déposent le MÊME paquet : {len(communs)} pièces communes, "
          f"{len(divergents)} divergentes — {'AUCUNE' if not divergents else ', '.join(divergents)}")

    # ------------------------------------------------------------------
    # PHASE 2 — rapatriement des preuves de run (md5 vérifié)
    # ------------------------------------------------------------------
    print("=== PHASE 2 : rapatriement des preuves de run ===")
    for chemin_rel in PREUVES_RUN:
        for depot, info in manifeste.items():
            piece = next((p for p in info["pieces"] if p["chemin"].endswith(chemin_rel)), None)
            if piece is None:
                continue
            dest = DEST / depot / chemin_rel
            md5_calc = telecharger(piece["id"], dest)
            ok = md5_calc == piece["md5"]
            check(f"{depot}/{chemin_rel}", ok,
                  f"rapatriée ({piece['taille']} o, md5 {'== Drive' if ok else 'DIVERGE'}, "
                  f"mtime Drive {piece['mtime']})")
            print(f"  {'OK ' if ok else 'ÉCART'} {depot}/{chemin_rel}")

    # ------------------------------------------------------------------
    # PHASE 3 — lecture des preuves (les faits, mot pour mot)
    # ------------------------------------------------------------------
    print("=== PHASE 3 : lecture des preuves ===")
    for depot in manifeste:
        for chemin_rel in PREUVES_RUN:
            p = DEST / depot / chemin_rel
            if p.exists():
                print(f"\n----- {depot} :: {chemin_rel} -----")
                texte = p.read_text(encoding="utf-8", errors="replace")
                print(texte[:4000])

    rapport_path = DEST / "rapport-etape-recoupement.txt"
    DEST.mkdir(parents=True, exist_ok=True)
    rapport_path.write_text(
        "RAPPORT INTermÉDIAIRE — rapatriement des dépôts 2 machines (phase 1-2)\n"
        + "=" * 70 + "\n" + "\n".join(rapport)
        + f"\n\nBILAN : {verts} VERT / {rouges} ROUGE\n", encoding="utf-8")
    print(f"\n=== BILAN : {verts} VERT / {rouges} ROUGE — rapport : {rapport_path} ===")
    return 0 if rouges == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
