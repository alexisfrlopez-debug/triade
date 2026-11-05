#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corriger_kit_m8d.py — LA CORRECTION DU KIT TERRAIN M8-(d) APRÈS LE CRASH
du premier run développeur (le 05/11, Python 3.13.9/Windows : ligne 207,
« ValueError: memoryview assignment: lvalue and rvalue have different
structures » — la tranche 0x2A0:0x2B0 [16 octets] face à la valeur
« NtWriteFile\\x00 » [12 octets] : la LONGUEUR fait partie de la structure,
jamais de tacite).

La correction (m8/terrain/scenario-m8d.py) : v[0x2A0:0x2AC] = la valeur —
la tranche == la valeur, le motif déjà suivi par les voisins (MZ sur 2,
PE\\x00\\x00 sur 4, le stub crocheté sur 5). Le kit CORRIGÉ est réassemblé
et rééprouvé (assembler_kit_m8d.py : recoup AST 13 constantes == l'artefact,
py_compile, extraction vierge VERT) ; le contrat du forgé vérifié au labo :
la marche EAT trouve « NtWriteFile » au RVA 0x300, le motif 4C 8B D1 B8
ABSENT du stub b8 44 33 22 11 → le refus -4 NOMMÉ attendu de sys-02.

  1. le zip local CORRIGÉ vérifié (empreintes attendues ci-dessous) ;
  2. kit-m8d.zip du coffre /test MIS À JOUR EN PLACE (upload_update : le
     contenu remplacé, le fichier même conservé — aucune entrée nouvelle,
     rien jeté ; l'ancien scénario vit dans l'historique git) ;
  3. la relecture md5 MATCH (l'aller-retour, la preuve du dépôt).

Usage : python3 scripts/corriger_kit_m8d.py
Code de sortie : 0 = coffre corrigé ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-m8d.zip"

# le kit CORRIGÉ (assembler_kit_m8d.py rejoué le 05/11 après la correction)
KIT_SHA = "3e777013e433a666830709a278f3e743c4e6138516876535adb902e7ce7699e3"
KIT_MD5 = "ad6cbffe70e48695495d1073e149e580"

# le kit défectueux d'origine (b5d5018) — le témoin de ce qu'on remplace
ANCIEN_MD5 = "117eb10aa7aba703d684f4329d0e3064"


def refus(nom, detail):
    print(f"[correction] REFUS {nom} : {detail}")
    sys.exit(2)


def main():
    print("=== M8-(d) : LA CORRECTION DU KIT au coffre /test "
          "(la ligne 207 du scénario) ===")

    # -- 1. le zip local corrigé, vérifié ----------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_m8d.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-m8d.zip sha256 divergent — réassembler le kit corrigé")
    if hashlib.md5(octets).hexdigest() != KIT_MD5:
        refus("KIT", "kit-m8d.zip md5 divergent — réassembler le kit corrigé")
    print(f"[1] le kit corrigé : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    # -- 2. l'état du coffre ------------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    piece = racine.get("kit-m8d.zip")
    if not piece:
        refus("ÉTAT", "kit-m8d.zip introuvable à la racine du /test — "
                      "deposer_kit_m8d.py d'abord")
    md5_distant = piece.get("md5Checksum", "")
    if md5_distant == KIT_MD5:
        print("[2] kit-m8d.zip porte DÉJÀ le md5 corrigé — idempotent")
        return 0
    if md5_distant != ANCIEN_MD5:
        refus("ÉTAT", f"kit-m8d.zip distant d'un md5 INATTENDU "
                      f"({md5_distant[:8]}…) — ni l'original {ANCIEN_MD5[:8]}… "
                      f"ni le corrigé {KIT_MD5[:8]}… : constater avant geste")
    print(f"[2] le kit distant porte l'original défectueux "
          f"(md5 {md5_distant[:8]}…) — remplacé en place :")

    # -- 3. la mise à jour en place + l'aller-retour --------------------------------
    ds.upload_update(piece["id"], pathlib.Path(KIT_ZIP))
    apres = ds.list_folder(TEST_ID).get("kit-m8d.zip")
    if not apres or apres.get("md5Checksum") != KIT_MD5:
        refus("DÉPÔT", f"kit-m8d.zip md5 divergent après mise à jour "
                      f"({(apres or {}).get('md5Checksum', 'ABSENT')[:8]}…)")
    print(f"[3] kit-m8d.zip MIS À JOUR au coffre /test — md5 "
          f"{KIT_MD5[:8]}… MATCH par relecture (le contenu remplacé, "
          f"le fichier même conservé, rien jeté)")

    # -- 4. les résidents intacts ---------------------------------------------------
    final = ds.list_folder(TEST_ID)
    attendus = {"kit-m8d.zip", "LISEZMOI-m8d.txt", "preuves-m8d",
                "archives-livraisons", "archives-preuves"}
    manquants = attendus - set(final)
    if manquants:
        refus("VÉRIFICATION", f"entrées attendues absentes : {sorted(manquants)}")
    print(f"[4] la racine demeure en ordre ({len(final)} entrées, les "
          f"résidents intacts)")

    print("\n=== LE COFFRE /test PORTE LE KIT CORRIGÉ : le geste du "
          "développeur peut reprendre (python scenario-m8d.py — la finale "
          "0.9.0 attend toujours le vert) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
