#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_unite01.py — LE KIT DE L'UNITÉ 1 ASSEMBLÉ ET ÉPROUVÉ au
labo (le modèle assembler_kit_loupe.py, D153 : le labo NE PEUT PAS
exécuter le scénario — Windows + les VRAIS kernel32 exigés, le cœur même
du run terrain, D122).

  1. L'ASSEMBLAGE : kit-unite-loupe-01-T/ = loupe.exe (la pièce, sha256
     recoupé contre le build cristallisé) + la notation livrée + le
     brouillon + scenario-unite01.py + LANCEUR-UNITE-01-T.bat + les
     QUATRE témoins (la génération FIXE du harnais, graine 20261107) +
     le LISEZMOI + EMPREINTES-KIT-UNITE-01-T.txt (la gravure) ;
  2. LA COMPILATION : py_compile du scénario (aucune erreur de syntaxe) ;
  3. L'ÉPREUVE D'EXTRACTION VIERGE : le zip extrait dans un répertoire
     NEUF, chaque empreinte re-constatée ;
  4. LE ZIP : kit-unite-loupe-01-T-20261114.zip (l'archive déposée au
     coffre /test).
"""
from __future__ import annotations

import hashlib
import os
import py_compile
import shutil
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "loupe"))
import harnais_noyau as HN   # noqa: E402  (la génération FIXE des témoins)

UNITE = os.path.dirname(os.path.abspath(__file__))
KIT = "kit-unite-loupe-01-T-20261114"
SORTIE = os.path.join(UNITE, "kit")
ZIP = os.path.join(UNITE, KIT + ".zip")

SHA_EXE = "4d119b22273c8fe140a2b74d5f8fe3f8eef5457540cbc9e178529e13fee244a5"


def refus(nom, detail):
    print(f"[assemblage] REFUS {nom} : {detail}")
    sys.exit(2)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main() -> int:
    print("=== LE KIT DE L'UNITÉ 1 (loupe-01 × T) : l'assemblage et "
          "l'épreuve de labo ===")
    piece = os.path.join(UNITE, "piece", "loupe.exe")
    if not os.path.exists(piece):
        refus("PIÈCE-ABSENTE", "piece/loupe.exe — construire d'abord")
    if sha(piece) != SHA_EXE:
        refus("PIÈCE-DIVERGENTE", "piece/loupe.exe != le sha cristallisé "
              f"{SHA_EXE[:12]}…")

    if os.path.exists(SORTIE):
        shutil.rmtree(SORTIE)
    os.makedirs(SORTIE)

    # les témoins : la génération FIXE du harnais (jamais une autre)
    temoins = HN.composer_temoins()
    with open(os.path.join(SORTIE, "temoin-1.bin"), "wb") as f:
        f.write(temoins["temoin-1.bin"])
    with open(os.path.join(SORTIE, "temoin-384.bin"), "wb") as f:
        f.write(temoins["temoin-384.bin"])
    with open(os.path.join(SORTIE, "temoin-3f.bin"), "wb") as f:
        f.write(temoins["temoin-3f.bin"])
    open(os.path.join(SORTIE, "vide.bin"), "wb").close()

    for source, nom in (
            (piece, "loupe.exe"),
            (os.path.join(UNITE, "notation", "loupe-01-ouvrir.asm"),
             "notation-loupe-01-ouvrir.asm"),
            (os.path.join(UNITE, "brouillons", "loupe-01-ouvrir.asm"),
             "brouillon-loupe-01-ouvrir.asm"),
            (os.path.join(UNITE, "scenario-unite01.py"),
             "scenario-unite01.py"),
            (os.path.join(UNITE, "LANCEUR-UNITE-01-T.bat"),
             "LANCEUR-UNITE-01-T.bat"),
            (os.path.join(UNITE, "LISEZMOI-KIT-UNITE-01-T.txt"),
             "LISEZMOI-KIT-UNITE-01-T.txt")):
        shutil.copy2(source, os.path.join(SORTIE, nom))

    # la compilation du scénario : aucune erreur de syntaxe
    py_compile.compile(os.path.join(SORTIE, "scenario-unite01.py"),
                       doraise=True)
    print("[compilation] py_compile : le scénario compile — aucune erreur")

    # LA GRAVURE : chaque pièce, sha256 (le format du GUI : sha  nom  (…))
    pieces = ["loupe.exe", "notation-loupe-01-ouvrir.asm",
              "brouillon-loupe-01-ouvrir.asm", "scenario-unite01.py",
              "LANCEUR-UNITE-01-T.bat", "temoin-1.bin", "temoin-384.bin",
              "temoin-3f.bin", "vide.bin", "LISEZMOI-KIT-UNITE-01-T.txt"]
    gravure = ["EMPREINTES — LE KIT DE L'UNITÉ 1 (loupe-01 × bras T, la "
               "campagne D204)",
               "(chaque pièce sha256 — le GUI recoupe à l'onglet 1·KIT ; "
               "une divergence, rien ne court)", ""]
    for nom in pieces:
        gravure.append(f"{sha(os.path.join(SORTIE, nom))}  {nom}")
    with open(os.path.join(SORTIE, "EMPREINTES-KIT-UNITE-01-T.txt"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("\n".join(gravure) + "\n")
    print(f"[gravure] EMPREINTES-KIT-UNITE-01-T.txt : {len(pieces)} pièces "
          "gravées")

    # LE ZIP
    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for nom in pieces + ["EMPREINTES-KIT-UNITE-01-T.txt"]:
            z.write(os.path.join(SORTIE, nom), arcname=f"{KIT}/{nom}")

    # L'ÉPREUVE D'EXTRACTION VIERGE
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ZIP) as z:
            z.extractall(tmp)
        extrait = os.path.join(tmp, KIT)
        for nom in pieces + ["EMPREINTES-KIT-UNITE-01-T.txt"]:
            attendu = sha(os.path.join(SORTIE, nom))
            if sha(os.path.join(extrait, nom)) != attendu:
                refus("EXTRACTION-DIVERGENTE", f"{nom} extrait != l'original")
        # le parse du GUI relit la gravure : chaque ligne sha  nom
        lignes = [l for l in open(os.path.join(
            extrait, "EMPREINTES-KIT-UNITE-01-T.txt"),
            encoding="utf-8").read().splitlines()
            if l and l[0] in "0123456789abcdef"]
        if len(lignes) != len(pieces):
            refus("GRAVURE-ILLISIBLE", f"{len(lignes)} lignes parsables != "
                  f"{len(pieces)} pièces")
    taille = os.path.getsize(ZIP)
    sha_zip = sha(ZIP)
    print(f"[extraction] l'épreuve VIERGE : {len(pieces) + 1} pièces "
          "re-constatées, la gravure lisible au format du GUI — VERT")
    print(f"=== LE KIT ASSEMBLÉ ET ÉPROUVÉ : {ZIP} ({taille} o, sha256 "
          f"{sha_zip[:12]}…) — prêt pour le coffre /test ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
