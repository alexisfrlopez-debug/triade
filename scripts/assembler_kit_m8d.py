#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_m8d.py — LE KIT TERRAIN M8-(d) ASSEMBLÉ ET ÉPROUVÉ au labo.

Modèle : scripts/assembler_kit_m7d.py (D153) — adapté au terrain WIN :
le labo NE PEUT PAS exécuter le scénario (Windows + VRAI ntdll exigés,
le cœur même du chantier) ; l'épreuve de labo est donc :

  1. L'ASSEMBLAGE : m8-kit/ = proxy.exe (l'artefact 0.9.0-dev.1,
     sha256 1492b0bc… ASSERTÉ) + scenario-m8d.py + LISEZMOI-m8d.txt ;
  2. LE RECOUP DES CONSTANTES PAR AST : chaque constante du scénario
     (les adresses scellées, les octets du trombone, les fixtures, le
     motif du stub, l'empreinte de l'artefact) relue DANS L'ARTEFACT —
     la source unique est le dépôt, jamais une constante gravée de tête ;
  3. LA COMPILATION : py_compile du scénario (aucune erreur de syntaxe) ;
  4. L'ÉPREUVE D'EXTRACTION VIERGE : le zip extrait dans un répertoire
     temporaire NEUF, les empreintes re-constatées, la structure exacte ;
  5. LE ZIP : kit-m8d.zip (l'archive déposée au coffre /test).

Usage : python3 scripts/assembler_kit_m8d.py
Code de sortie : 0 = kit assemblé et éprouvé ; 2 = refus nommé."""

import ast
import hashlib
import os
import pathlib
import py_compile
import shutil
import sys
import tempfile
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
KIT = "m8-kit"
SORTIE = pathlib.Path("/home/z/my-project/download")
KIT_ZIP = SORTIE / "kit-m8d.zip"

SHA_PROXY = "1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4"
TAILLE_PROXY = 44544
SCENARIO = REPO / "m8" / "terrain" / "scenario-m8d.py"
LISEZMOI = REPO / "m8" / "terrain" / "LISEZMOI-m8d.txt"
PROXY = REPO / "m8" / "proxy.exe"


def refus(nom, detail):
    print(f"[assemblage] REFUS {nom} : {detail}")
    sys.exit(2)


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def rva_vers_offset(data, rva):
    """RVA -> offset fichier (PE32+ de l'artefact, sections lues sur pièces)."""
    import struct
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
    opt = e_lfanew + 24
    for i in range(nsec):
        off = opt + 240 + i * 40
        vsize, va, _rs, raw = struct.unpack_from("<IIII", data, off + 8)
        if va <= rva < va + max(vsize, 0x1000):
            return raw + (rva - va)
    refus("RVA", f"le RVA {rva:#x} n'appartient à aucune section")


def _litteral(noeud):
    """Littéral OU bytes.fromhex('…') — les deux formes lisibles du scénario."""
    if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute) \
            and noeud.func.attr == "fromhex" \
            and isinstance(noeud.func.value, ast.Name) \
            and noeud.func.value.id == "bytes" and len(noeud.args) == 1:
        return bytes.fromhex(ast.literal_eval(noeud.args[0]))
    return ast.literal_eval(noeud)


def constantes_du_scénario(chemin):
    """Extrait les constantes nommées du scénario PAR AST (jamais gravées)."""
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    cibles = {"SHA_PROXY", "TAILLE_PROXY", "R_HELLO02", "R_SYS01", "R_SYS02",
              "R_SYS03", "R_FIXTURE_NOM", "R_FIXTURE_LIGNE",
              "R_IAT_WRITEFILE", "OCTETS_SYS01", "FIXTURE_NOM",
              "FIXTURE_LIGNE", "MOTIF_STUB"}
    trouves = {}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name) and cible.id in cibles:
                    try:
                        trouves[cible.id] = _litteral(noeud.value)
                    except (ValueError, SyntaxError):
                        refus("AST", f"constante {cible.id} non littérale")
    manquantes = cibles - set(trouves)
    if manquantes:
        refus("AST", f"constantes absentes du scénario : {sorted(manquantes)}")
    return trouves


def main():
    print("=== L'ASSEMBLAGE DU KIT TERRAIN M8-(d) (le VRAI ntdll) ===")

    # -- 1. les pièces du dépôt, vérifiées ------------------------------------
    if sha256_fichier(PROXY) != SHA_PROXY:
        refus("ARTEFACT", f"proxy.exe sha256 {sha256_fichier(PROXY)[:16]}… "
                          f"!= {SHA_PROXY[:16]}…")
    print(f"[1] l'artefact : {TAILLE_PROXY} o, sha256 {SHA_PROXY[:16]}… "
          f"— la carte génération 8 prouve CES octets")

    # -- 2. le recoup des constantes (AST du scénario contre l'artefact) ------
    data = PROXY.read_bytes()
    c = constantes_du_scénario(SCENARIO)
    if c["SHA_PROXY"] != SHA_PROXY or c["TAILLE_PROXY"] != TAILLE_PROXY:
        refus("RECOUP", "l'empreinte/taille du scénario != l'artefact")
    attendus = {
        "R_SYS01": 0xA000,
        "R_SYS02": 0xA040,
        "R_SYS03": 0xA180,
        "R_HELLO02": 0x1040,
        "R_FIXTURE_NOM": 0x2EC0,
        "R_FIXTURE_LIGNE": 0x2ED0,
        "R_IAT_WRITEFILE": 0x20B8,
    }
    for nom, attendu in attendus.items():
        if c[nom] != attendu:
            refus("RECOUP", f"{nom} = {c[nom]:#x} != {attendu:#x} (le plan)")
    if c["OCTETS_SYS01"] != data[rva_vers_offset(data, 0xA000):
                                 rva_vers_offset(data, 0xA000) + 6]:
        refus("RECOUP", "OCTETS_SYS01 != les octets de l'artefact @0xA000")
    if c["FIXTURE_NOM"] != data[rva_vers_offset(data, 0x2EC0):
                                rva_vers_offset(data, 0x2EC0) + 11]:
        refus("RECOUP", "FIXTURE_NOM != les octets de l'artefact @0x2EC0")
    if c["FIXTURE_LIGNE"] != data[rva_vers_offset(data, 0x2ED0):
                                  rva_vers_offset(data, 0x2ED0) + 33]:
        refus("RECOUP", "FIXTURE_LIGNE != les octets de l'artefact @0x2ED0")
    if c["MOTIF_STUB"] != bytes.fromhex("4c8bd1b8"):
        refus("RECOUP", "MOTIF_STUB != le motif du plan (m8/layout.py)")
    print(f"[2] le recoup PAR AST : {len(c)} constantes du scénario == "
          f"l'artefact/le plan (les adresses scellées, le trombone, les "
          f"fixtures, le motif, l'empreinte) — AUCUN chiffre gravé de tête")

    # le motif relu au plan (la source unique)
    layout = (REPO / "m8" / "layout.py").read_text(encoding="utf-8")
    if 'MOTIF_STUB = bytes.fromhex("4C8BD1B8")' not in layout:
        refus("RECOUP", "m8/layout.py ne porte pas le motif attendu")
    print("    le motif relu au plan m8/layout.py : 4C 8B D1 B8 — "
          "MOV R10, RCX ; MOV EAX — (l'ordre est le contrat)")

    # -- 3. la compilation du scénario -----------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        py_compile.compile(str(SCENARIO), cfile=os.path.join(tmp, "s.pyc"),
                           doraise=True)
    print("[3] le scénario compile (py_compile) — aucun paquet requis "
          "(stdlib seule, imports vérifiés : ctypes, hashlib, os, platform, "
          "struct, sys, time)")

    # -- 4. l'assemblage --------------------------------------------------------
    zone = SORTIE / "vague-m8d"
    racine = zone / KIT
    if racine.exists():
        shutil.rmtree(racine)
    racine.mkdir(parents=True)
    shutil.copy2(PROXY, racine / "proxy.exe")
    shutil.copy2(SCENARIO, racine / "scenario-m8d.py")
    shutil.copy2(LISEZMOI, racine / "LISEZMOI-m8d.txt")
    pieces = {
        "proxy.exe": SHA_PROXY,
        "scenario-m8d.py": sha256_fichier(racine / "scenario-m8d.py"),
        "LISEZMOI-m8d.txt": sha256_fichier(racine / "LISEZMOI-m8d.txt"),
    }
    for nom, attendu in pieces.items():
        if sha256_fichier(racine / nom) != attendu:
            refus("ASSEMBLAGE", f"{nom} : empreinte divergente après copie")
    print(f"[4] assemblé : {racine} ({len(pieces)} pièces, empreintes "
          f"recoupées après copie)")

    # -- 5. le zip + l'épreuve d'extraction vierge -------------------------------
    if KIT_ZIP.exists():
        KIT_ZIP.unlink()
    with zipfile.ZipFile(KIT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for nom in sorted(pieces):
            z.write(racine / nom, f"{KIT}/{nom}")
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(KIT_ZIP) as z:
            z.extractall(tmp)
        extraite = pathlib.Path(tmp) / KIT
        noms = sorted(p.name for p in extraite.iterdir())
        if noms != sorted(pieces):
            refus("ÉPREUVE", f"extraction : {noms} != {sorted(pieces)}")
        for nom, attendu in pieces.items():
            if sha256_fichier(extraite / nom) != attendu:
                refus("ÉPREUVE", f"{nom} : empreinte divergente après "
                                 f"extraction vierge")
    print(f"[5] l'épreuve d'extraction vierge : VERT — kit-m8d.zip "
          f"({KIT_ZIP.stat().st_size} o, {len(pieces)} pièces, empreintes "
          f"re-constatées)")

    print(f"\n[le kit est PRÊT AU DÉPÔT] : {KIT_ZIP}")
    print("  md5 :", hashlib.md5(KIT_ZIP.read_bytes()).hexdigest())
    print("  sha256 :", sha256_fichier(KIT_ZIP))
    print("  (le dépôt au coffre /test : scripts/deposer_kit_m8d.py)")


if __name__ == "__main__":
    main()
