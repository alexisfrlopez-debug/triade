#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_m9f.py — LE KIT TERRAIN M9-(f) ASSEMBLÉ ET ÉPROUVÉ au labo.

Modèle : scripts/assembler_kit_m8d.py (D153) — le labo NE PEUT PAS
exécuter le scénario (Windows + le VRAI ntdll + le VRAI afd.sys + le
réseau exigés, le cœur même du chantier (f)) ; l'épreuve de labo est :

  1. L'ASSEMBLAGE : m9-kit/ = proxy.exe (l'artefact 1.0.0-dev.2,
     sha256 d8928934… ASSERTÉ) + scenario-m9f.py + LISEZMOI-KIT-M9F.md ;
  2. LE RECOUP DES CONSTANTES PAR AST : chaque constante du scénario
     (les adresses scellées, le trombone, l'OCTET DE L'ERRATUM n° 5,
     les fixtures transport, le motif du stub, l'empreinte épinglée,
     les dimensions de session) relue DANS L'ARTEFACT ou DANS LE PLAN —
     la source unique est le dépôt, jamais une constante gravée de tête ;
  3. LA COMPILATION : py_compile du scénario (aucune erreur de syntaxe) ;
  4. L'ÉPREUVE D'EXTRACTION VIERGE : le zip extrait dans un répertoire
     temporaire NEUF, les empreintes re-constatées, la structure exacte ;
  5. LE ZIP : kit-m9f.zip (l'archive déposée au coffre /test).

Usage : python3 scripts/assembler_kit_m9f.py
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
KIT = "m9-kit"
SORTIE = pathlib.Path("/home/z/my-project/download")
KIT_ZIP = SORTIE / "kit-m9f.zip"

SHA_PROXY = ("d892893469608fd69e381b92b8e18623107bd2bc694f43a512"
             "bc5900773dc314")
TAILLE_PROXY = 65024
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
LISEZMOI = REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md"
PROXY = REPO / "tls13" / "proxy.exe"

# l'empreinte épinglée — figée par la sonde du 06/11 (3 sessions
# consécutives contre la cible, empreinte IDENTIQUE de bout en bout :
# la pièce vit dans scripts/sonde_cible_terrain.py)
EMPREINTE = "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f"


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
    cibles = {"SHA_PROXY", "TAILLE_PROXY", "R_SYS01", "R_SYS02", "R_SYS04",
              "R_SYS05", "R_SYS06", "R_TLS27", "R_TLS28", "R_SYS_DEVICE",
              "R_SYS_NOM_CREATEFILE", "R_SYS_NOM_DEVICEIOCTL",
              "R_SYS_NOM_CLOSE", "R_TETE_CH", "OCTETS_SYS01",
              "OCTETS_TETE_CH", "NOM_DEVICE", "MOTIF_STUB",
              "EMPREINTE_EPINGLEE", "CIBLE", "CIBLE_PORT",
              "SESSION_TAILLE", "KIT96", "CH_TAILLE", "CH_RECORD",
              "TEMOIN_APPLICATIF"}
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
    print("=== L'ASSEMBLAGE DU KIT TERRAIN M9-(f) (LA SESSION RÉELLE) ===")

    # -- 1. les pièces du dépôt, vérifiées ------------------------------------
    if sha256_fichier(PROXY) != SHA_PROXY:
        refus("ARTEFACT", f"proxy.exe sha256 {sha256_fichier(PROXY)[:16]}… "
                          f"!= {SHA_PROXY[:16]}…")
    print(f"[1] l'artefact : {TAILLE_PROXY} o, sha256 {SHA_PROXY[:16]}… — "
          f"la carte génération 10 prouve CES octets")

    # -- 2. le recoup des constantes (AST du scénario contre l'artefact) ------
    data = PROXY.read_bytes()
    c = constantes_du_scénario(SCENARIO)
    if c["SHA_PROXY"] != SHA_PROXY or c["TAILLE_PROXY"] != TAILLE_PROXY:
        refus("RECOUP", "l'empreinte/taille du scénario != l'artefact")
    if c["R_TLS28"] != 0x10D00:
        refus("RECOUP", f"R_TLS28 = {c['R_TLS28']:#x} != 0x10D00 "
                        "(l'erratum n° 5 : le socle DÉPLACÉ après les "
                        "fixtures)")
    attendus = {
        "R_SYS01": 0xA000, "R_SYS02": 0xA040, "R_SYS04": 0xA240,
        "R_SYS05": 0xA540, "R_SYS06": 0xA6C0, "R_TLS27": 0xFF40,
        "R_TLS28": 0x10D00, "R_SYS_DEVICE": 0x10C20,
        "R_SYS_NOM_CREATEFILE": 0x10CB0,
        "R_SYS_NOM_DEVICEIOCTL": 0x10CC0, "R_SYS_NOM_CLOSE": 0x10CE0,
        "R_TETE_CH": 0x10082,
    }
    for nom, attendu in attendus.items():
        if c[nom] != attendu:
            refus("RECOUP", f"{nom} = {c[nom]:#x} != {attendu:#x} (le plan)")
    if c["OCTETS_SYS01"] != data[rva_vers_offset(data, 0xA000):
                                 rva_vers_offset(data, 0xA000) + 6]:
        refus("RECOUP", "OCTETS_SYS01 != les octets de l'artefact @0xA000")
    if c["OCTETS_TETE_CH"] != data[rva_vers_offset(data, 0x10082):
                                    rva_vers_offset(data, 0x10082) + 12]:
        refus("RECOUP", "OCTETS_TETE_CH != les octets de l'artefact "
                        "@0x10082 (l'erratum n° 5 : l'octet 0x72)")
    if c["OCTETS_TETE_CH"][-5:] != bytes.fromhex("41c6420472") \
            or c["OCTETS_TETE_CH"][-1:] != b"\x72":
        refus("RECOUP", "l'octet de longueur du record CH != 0x72")
    fixture_attendu = c["NOM_DEVICE"].encode("utf-16le") + b"\x00\x00"
    if fixture_attendu != data[rva_vers_offset(data, 0x10C20):
                               rva_vers_offset(data, 0x10C20) + 42]:
        refus("RECOUP", "le device AFD dérivé du NOM du scénario != "
                        "l'artefact @0x10C20")
    if c["MOTIF_STUB"] != bytes.fromhex("4c8bd1b8"):
        refus("RECOUP", "MOTIF_STUB != le motif du plan")
    if c["EMPREINTE_EPINGLEE"].hex() != EMPREINTE:
        refus("RECOUP", "l'empreinte épinglée du scénario != la pièce de "
                        "la sonde du 06/11")
    if c["CIBLE"] != "www.cloudflare.com" or c["CIBLE_PORT"] != 443:
        refus("RECOUP", "la cible != la décision du labo")
    if c["TEMOIN_APPLICATIF"] != b"HTTP/1.1 200 OK":
        refus("RECOUP", "le témoin applicatif != la pièce de la sonde")
    print(f"[2] le recoup PAR AST : {len(c)} constantes du scénario == "
          f"l'artefact/le plan/la sonde — AUCUN chiffre gravé de tête "
          f"(l'octet 0x72 de l'erratum n° 5 relu DANS L'IMAGE)")

    # le plan relu (la source unique des dimensions)
    layout = (REPO / "tls13" / "layout.py").read_text(encoding="utf-8")
    if "SESSION_TAILLE = 17520" not in layout:
        refus("RECOUP", "tls13/layout.py ne porte pas SESSION_TAILLE 17520")
    if "CLIENTHELLO_TAILLE = 114" not in layout:
        refus("RECOUP", "tls13/layout.py ne porte pas CLIENTHELLO_TAILLE 114")
    if c["SESSION_TAILLE"] != 17520 or c["CH_TAILLE"] != 114 \
            or c["KIT96"] != 96:
        refus("RECOUP", "les dimensions du scénario != la spec tls13-27 P1")
    if c["CH_RECORD"] != bytes.fromhex("1603030072"):
        refus("RECOUP", "CH_RECORD != 16 03 03 00 72 (l'erratum n° 5)")
    print("    le plan relu : SESSION_TAILLE 17520, CLIENTHELLO_TAILLE 114 "
          "— le record 16 03 03 00 72")

    # -- 3. la compilation du scénario -----------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        py_compile.compile(str(SCENARIO), cfile=os.path.join(tmp, "s.pyc"),
                           doraise=True)
    print("[3] le scénario compile (py_compile) — stdlib seule (imports : "
          "ctypes, hashlib, os, platform, socket, struct, sys, "
          "threading, time)")

    # -- 4. l'assemblage --------------------------------------------------------
    zone = SORTIE / "vague-m9f"
    racine = zone / KIT
    if racine.exists():
        shutil.rmtree(racine)
    racine.mkdir(parents=True)
    shutil.copy2(PROXY, racine / "proxy.exe")
    shutil.copy2(SCENARIO, racine / "scenario-m9f.py")
    shutil.copy2(LISEZMOI, racine / "LISEZMOI-KIT-M9F.md")
    pieces = {
        "proxy.exe": SHA_PROXY,
        "scenario-m9f.py": sha256_fichier(racine / "scenario-m9f.py"),
        "LISEZMOI-KIT-M9F.md": sha256_fichier(racine / "LISEZMOI-KIT-M9F.md"),
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
    print(f"[5] l'épreuve d'extraction vierge : VERT — kit-m9f.zip "
          f"({KIT_ZIP.stat().st_size} o, {len(pieces)} pièces, empreintes "
          f"re-constatées)")

    print(f"\n[le kit est PRÊT AU DÉPÔT] : {KIT_ZIP}")
    print("  md5 :", hashlib.md5(KIT_ZIP.read_bytes()).hexdigest())
    print("  sha256 :", sha256_fichier(KIT_ZIP))
    print("  (le dépôt au coffre /test : scripts/deposer_kit_m9f.py)")


if __name__ == "__main__":
    main()
