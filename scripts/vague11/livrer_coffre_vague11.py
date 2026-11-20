#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_coffre_vague11.py — LA LIVRAISON AU COFFRE (la vague 11) :
LE PACK TRIADE_presentation_v0.22.0.zip + LES DEUX ARCHIVES DE DÉPÔT + LE
RAPPORT DE VÉRIFICATION à la RACINE, L'OU-TROUVER à l'Entrée 381 — le
tout RECOUPÉ byte-byte par re-téléchargement ; LES PIÈCES DE SESSION au
/test (le rapport de vérification, les empreintes du manifeste, les
rapports des neuf ateliers) recoupées. Les écritures au RELAIS (le
compte de service demeure LECTEUR seul — D101), les lectures et le
recoup au SERVICE (le bord froid), la voie urllib du module
drive_sa_v220.py."""
import pathlib
import sys

sys.path.insert(0, "/home/z/my-project/depot/scripts/vague11")
from drive_sa_v220 import televerse  # noqa: E402

REPO = pathlib.Path("/home/z/my-project/depot")
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"

RACINE_PIECES = [
    REPO / "TRIADE_presentation_v0.22.0.zip",
    REPO / "depot-zenodo-v0220" / "TRIADE_soumission_v0.22.0.zip",
    REPO / "depot-zenodo-v0220" / "TRIADE_complet_v0.22.0.zip",
    REPO / "scripts" / "vague11" / "rapport_verification_v0.22.0.txt",
    REPO / "OU-TROUVER-LES-LIVRABLES.md",
]

TEST_PIECES = [
    REPO / "scripts" / "vague11" / "rapport_verification_v0.22.0.txt",
    REPO / "scripts" / "vague11" / "empreintes_livrables_v0.22.0.txt",
    REPO / "atelier-sequestre-ou6wn6wlv" / "rapport-purge.txt",
    REPO / "atelier-corridors-fnvan0zes" / "rapport-corridors.txt",
    REPO / "atelier-corridors-fnvan0zes" /
    "rapport-temps-reel-corridors.txt",
    REPO / "atelier-porteuse-ahult8jgd" / "rapport-porteuse.txt",
    REPO / "atelier-gabarits-o5apue194" / "rapport-gabarits.txt",
    REPO / "atelier-coffre-vr9n3s3l7" / "rapport-coffre.txt",
    REPO / "atelier-quatrebras-3lmyfb2xa" / "rapport-cgp-m4.txt",
    REPO / "atelier-preregistre-l4nnwqlld" / "rapport-preregistre.txt",
    REPO / "atelier-lifter-hrbdfy6i4" / "rapport-lifter.txt",
    REPO / "atelier-medians-zho5vilpy" / "rapport-plancher-natif.txt",
    REPO / "atelier-medians-zho5vilpy" / "rapport-recompte.txt",
]


def main():
    print("== (1) LA RACINE DU COFFRE : le pack, les deux archives, le "
          "rapport, l'OU-TROUVER à l'Entrée 381 ==")
    for f in RACINE_PIECES:
        televerse(f, RACINE)
    print("== (2) LE /test : le rapport, les empreintes, les rapports "
          "des ateliers ==")
    for f in TEST_PIECES:
        televerse(f, TEST)
    print("LA LIVRAISON AU COFFRE VÉCUE — la racine et le /test, chaque "
          "pièce recoupée byte-byte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
