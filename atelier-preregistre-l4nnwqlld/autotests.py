#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""autotests.py — LES AUTOTESTS DES KITS DE L'ATELIER l4nnwqlld (sur fixtures
synthétiques et pièces intactes — JAMAIS des mesures).

LA RÈGLE DE L'INSTRUCTION : « aucun résultat n'est produit sans le geste du
développeur » — les présents autotests éprouvent les MÉCANISMES des kits
sur des fixtures SYNTHÉTIQUES et l'INTÉGRITÉ des pièces copiées ; AUCUNE
mesure de terrain, AUCUN run matériel, AUCUN chiffre fabriqué :

  A1. LA SYNTAXE — chaque pièce Python des kits compile (py_compile) ;
  A2. L'AGRÉGATEUR FAIL-CLOSED (kit-dudect) — sur fixtures synthétiques :
      l'arbre complet s'agrège (les médianes et décisions CONSTRUITES),
      UN run manquant => REFUS, un témoin machine muet => REFUS, l'agrégat
      partiel IMPOSSIBLE ;
  A3. LE CALCULATEUR κ (kit-annotateur-fl) — quatre fixtures synthétiques
      à l'accord attendu EXACT par construction (+1 ; <0 ; +0,4 à la
      main ; +0,64 à n = 50), la garde de taille n ≥ 50 ;
  A4. LE GÉNÉRATEUR DE RANDOMISATION (kit-h7-stratifiee) — le plan de
      puissance se re-dérive (δ = 0,2385 ; σ = 0,2856 ; normale 11,25 →
      12 ; t itérée → 14 ; décision fail-closed 14 = les strates fixées),
      le déterminisme à la graine 20261120, le contraste garanti dans
      CHAQUE strate, la sensibilité à la graine ;
  A5. LES ENCODAGES DE LA SONDE fence.i (kit-fencei-rv64) — les QUATRE
      littéraux .word vérifiés par l'ASSEMBLEUR MAISON DU DÉPÔT
      (riscv/outils/as_rv64.py — le juge du jalon M7) : addi a0, zero, 11
      → 1305b000 ; addi a0, zero, 22 → 13056001 ; jalr x0, ra, 0 →
      67800000 ; addi x0, x0, 0 → 13000000 ; ET les trois formes vives de
      la séquence : fence rw, rw → 0f003003 ; fence.i → 0f100000 ;
      jalr ra, 0(t1) → e7000300 ;
  A6. L'INTÉGRITÉ DES COPIES — chaque pièce copiée du dépôt est
      OCTET POUR OCTET l'originale (corpus, demo, loupe.exe,
      scenario-loupe.py, temoin-vitrine.bat, dudect_v150.c, cibles/*,
      grille-fl.csv) ; les empreintes ASSERTÉES par les scénarios
      recoupées (corpus ec343b4e…, demo e57fc74b…, loupe.exe c1115105…) ;
  A7. LA TABLE DES EMPREINTES — chaque ligne d'EMPREINTES-KITS.txt
      recoupe le fichier qu'elle nomme (la table est VÉRIFIÉE, pas
      décrétée).

Usage : python3 autotests.py   (depuis la racine de l'atelier)
"""

from __future__ import annotations

import hashlib
import os
import py_compile
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(ICI)

SHA_CORPUS = "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799"
SHA_DEMO = "e57fc74be2ea67ab4c05351d0b5e0b93b6147ec34f2fb7aabbfd1ab7f141cde9"
SHA_LOUPE = ("c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb"
             "93e61d1")

COPIES = [
    ("kit-fencei-rv64/corpus", "riscv/corpus"),
    ("kit-fencei-rv64/demo", "riscv/demo"),
    ("kit-loupe-3e-machine/loupe.exe", "loupe/loupe.exe"),
    ("kit-loupe-3e-machine/scenario-loupe.py", "loupe/terrain/scenario-loupe.py"),
    ("kit-loupe-3e-machine/temoin-vitrine.bat", "loupe/terrain/temoin-vitrine.bat"),
    ("kit-dudect/dudect_v150.c",
     "scripts/kits_mesure_v150/kit_dudect/dudect_v150.c"),
    ("kit-dudect/cibles/proxy-image.bin",
     "scripts/kits_mesure_v150/kit_dudect/cibles/proxy-image.bin"),
    ("kit-dudect/cibles/manifeste-c.txt",
     "scripts/kits_mesure_v150/kit_dudect/cibles/manifeste-c.txt"),
    ("kit-dudect/cibles/manifeste.json",
     "scripts/kits_mesure_v150/kit_dudect/cibles/manifeste.json"),
    ("kit-annotateur-fl/grille-fl.csv", "scripts/replication_v150/grille_tx.csv"),
]

PIECES_PY = [
    "kit-fencei-rv64/scenario-fencei-rv64.py",
    "kit-dudect/agregateur_dudect.py",
    "kit-h7-stratifiee/generateur_randomisation.py",
    "kit-annotateur-fl/calculateur_kappa.py",
]

A_TOUT_VERT = []


def dire(ok, message):
    print(f"  [{'OK' if ok else 'ÉCART'}] {message}")
    A_TOUT_VERT.append(ok)
    return ok


def sha256_fichier(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def a1_syntaxe():
    print("A1. LA SYNTAXE — les pièces Python des kits compilent")
    for piece in PIECES_PY:
        chemin = os.path.join(ICI, piece)
        try:
            py_compile.compile(chemin, doraise=True)
            dire(True, f"{piece} : compile")
        except py_compile.PyCompileError as exc:
            dire(False, f"{piece} : {exc}")


def _sous_processus(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ICI)
    return r.returncode, r.stdout, r.stderr


def a2_agregateur():
    print("A2. L'AGRÉGATEUR FAIL-CLOSED (kit-dudect, fixtures synthétiques)")
    code, sortie, _ = _sous_processus(
        [sys.executable, "kit-dudect/agregateur_dudect.py", "--selftest"])
    for ligne in sortie.splitlines():
        if ligne.strip():
            print("      " + ligne)
    dire(code == 0 and "VERT" in sortie,
         "l'agrégateur : complétude AVANT tout calcul, un run manquant = REFUS")


def a3_kappa():
    print("A3. LE CALCULATEUR κ (kit-annotateur-fl, fixtures synthétiques)")
    code, sortie, _ = _sous_processus(
        [sys.executable, "kit-annotateur-fl/calculateur_kappa.py"])
    for ligne in sortie.splitlines():
        if ligne.strip():
            print("      " + ligne)
    dire(code == 0 and "VERT" in sortie,
         "le κ : quatre accords attendus exacts par construction + la garde n ≥ 50")


def a4_randomisation():
    print("A4. LE GÉNÉRATEUR DE RANDOMISATION (kit-h7-stratifiee, à la graine)")
    code, sortie, _ = _sous_processus(
        [sys.executable, "kit-h7-stratifiee/generateur_randomisation.py",
         "--autotest"])
    for ligne in sortie.splitlines():
        if ligne.strip():
            print("      " + ligne)
    dire(code == 0 and "VERT" in sortie,
         "la randomisation : le plan de puissance re-dérivé, le déterminisme, "
         "le contraste garanti par strate")


def a5_encodages_fencei():
    print("A5. LES ENCODAGES DE LA SONDE fence.i (l'assembleur maison du dépôt)")
    sys.path.insert(0, os.path.join(DEPOT, "riscv", "outils"))
    try:
        from as_rv64 import assembler
        tests = [
            ("addi a0, zero, 11", "1305b000"),
            ("addi a0, zero, 22", "13056001"),
            ("jalr x0, ra, 0", "67800000"),
            ("addi x0, x0, 0", "13000000"),
            ("fence rw, rw", "0f003003"),
            ("fence.i", "0f100000"),
            ("jalr ra, 0(t1)", "e7000300"),
        ]
        for texte, attendu in tests:
            octets = assembler(texte, 0x1000)
            dire(octets.hex() == attendu,
                 f"{texte!r:26} -> {octets.hex()} (attendu {attendu})")
    except Exception as exc:
        dire(False, f"l'assembleur maison du dépôt : {exc}")


def a6_integrite():
    print("A6. L'INTÉGRITÉ DES COPIES (octet pour octet, et les empreintes)")
    for kit_rel, depot_rel in COPIES:
        chemin_kit = os.path.join(ICI, kit_rel)
        chemin_depot = os.path.join(DEPOT, depot_rel)
        with open(chemin_kit, "rb") as f:
            a = f.read()
        with open(chemin_depot, "rb") as f:
            b = f.read()
        dire(a == b, f"{kit_rel} == {depot_rel} ({len(a)} octets)")
    dire(sha256_fichier(os.path.join(ICI, "kit-fencei-rv64/corpus")) == SHA_CORPUS,
         f"le corpus du kit-fencei : sha256 {SHA_CORPUS[:16]}… (le scellé 0.8.0-rc.1)")
    dire(sha256_fichier(os.path.join(ICI, "kit-fencei-rv64/demo")) == SHA_DEMO,
         f"le demo du kit-fencei : sha256 {SHA_DEMO[:16]}… (le démonstrateur f72001)")
    dire(sha256_fichier(os.path.join(ICI, "kit-loupe-3e-machine/loupe.exe"))
         == SHA_LOUPE,
         f"le loupe.exe du kit-3e-machine : sha256 {SHA_LOUPE[:16]}… (0.1.1-dev.1)")


def a7_empreintes():
    print("A7. LA TABLE DES EMPREINTES (chaque ligne recoupe son fichier)")
    chemin = os.path.join(ICI, "EMPREINTES-KITS.txt")
    if not os.path.exists(chemin):
        dire(False, "EMPREINTES-KITS.txt ABSENT à la racine de l'atelier")
        return
    lignes = [l.strip() for l in open(chemin, encoding="utf-8")
              if "sha256:" in l]
    if not lignes:
        dire(False, "EMPREINTES-KITS.txt : aucune ligne d'empreinte")
        return
    for ligne in lignes:
        try:
            nom = ligne.split("sha256:")[0].strip()
            empreinte = ligne.split("sha256:")[1].split()[0].strip()
            chemin_piece = os.path.join(ICI, nom)
            if not os.path.exists(chemin_piece):
                dire(False, f"{nom} : ABSENT (la ligne nomme un fantôme)")
                continue
            calculee = sha256_fichier(chemin_piece)
            dire(calculee == empreinte,
                 f"{nom} : {empreinte[:16]}… {'recoupé' if calculee == empreinte else 'DIVERGENT'}")
        except Exception as exc:
            dire(False, f"ligne illisible ({exc}) : {ligne[:60]}")


def main():
    print("=== LES AUTOTESTS DE L'ATELIER PRÉREGISTRE-l4nnwqlld "
          "(fixtures synthétiques — AUCUNE mesure, la règle) ===")
    print()
    a1_syntaxe()
    print()
    a2_agregateur()
    print()
    a3_kappa()
    print()
    a4_randomisation()
    print()
    a5_encodages_fencei()
    print()
    a6_integrite()
    print()
    a7_empreintes()
    print()
    verts = sum(1 for ok in A_TOUT_VERT if ok)
    total = len(A_TOUT_VERT)
    print(f"[autotests] {verts}/{total} constats VERTS — "
          + ("TOUT VERT" if verts == total else "DES ÉCARTS NOMMÉS CI-DESSUS"))
    return 0 if verts == total else 1


if __name__ == "__main__":
    sys.exit(main())
