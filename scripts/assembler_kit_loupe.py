#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_loupe.py — LE KIT TERRAIN M10-(e) ASSEMBLÉ ET ÉPROUVÉ au labo.

Modèle : scripts/assembler_kit_m9f.py (D153) — le labo NE PEUT PAS
exécuter le scénario (Windows + les VRAIS kernel32/user32/gdi32 exigés,
le cœur même du run terrain) ; l'épreuve de labo est :

  1. L'ASSEMBLAGE : loupe-kit/ = loupe.exe (l'artefact 0.1.0-dev.4,
     sha256 1f2da283… ASSERTÉ — LA RETOUCHE DE L'ENTRÉE 206 : LE VRAI
     CHARGEUR A CARTOGRAPHIÉ dev.3, puis le témoin a nommé [CADRE-NÉ]
     — l'initialiseur .data devient LE MIROIR EXACT du CADRE_VIERGE du
     harnais, le sentinel à +528 par LA CHAÎNE DES TAILLES, jamais gravé
     de tête ; le scénario relit LE .data ENTIER contre le miroir) +
     scenario-loupe.py + LISEZMOI-KIT-LOUPE.md ;
  2. LE RECOUP DES CONSTANTES PAR AST : chaque constante du scénario (les
     adresses scellées, l'empreinte, la version R10, les listes IAT, la
     table K, les champs du cadre) relue DANS L'ARTEFACT ou DANS LE PLAN —
     la source unique est le dépôt, jamais une constante gravée de tête ;
  3. LA COMPILATION : py_compile du scénario (aucune erreur de syntaxe) ;
  4. L'ÉPREUVE D'EXTRACTION VIERGE : le zip extrait dans un répertoire
     temporaire NEUF, les empreintes re-constatées, la structure exacte ;
  5. LE ZIP : kit-loupe.zip (l'archive déposée au coffre /test).

Usage : python3 scripts/assembler_kit_loupe.py
Code de sortie : 0 = kit assemblé et éprouvé ; 2 = refus nommé."""

import ast
import hashlib
import importlib.util
import os
import pathlib
import py_compile
import shutil
import sys
import tempfile
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
KIT = "loupe-kit"
SORTIE = pathlib.Path("/home/z/my-project/download")
KIT_ZIP = SORTIE / "kit-loupe.zip"

SHA_EXE = ("1f2da2833b47265e9b956ee83a5cc246"
           "b68455f06f5b7bb03a69045f03503e03")
TAILLE_EXE = 127488
EXE = REPO / "loupe" / "loupe.exe"
SCENARIO = REPO / "loupe" / "terrain" / "scenario-loupe.py"
LISEZMOI = REPO / "loupe" / "terrain" / "LISEZMOI-KIT-LOUPE.md"

# le plan (la source unique — chargé par chemin nominatif, la leçon D158)
_spec = importlib.util.spec_from_file_location(
    "layout_loupe", REPO / "loupe" / "layout.py")
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)
_spec_t = importlib.util.spec_from_file_location(
    "layout_tls13", REPO / "tls13" / "layout.py")
LT = importlib.util.module_from_spec(_spec_t)
_spec_t.loader.exec_module(LT)


def refus(nom, detail):
    print(f"[assemblage] REFUS {nom} : {detail}")
    sys.exit(2)


def constantes_scenario():
    """Les affectations du scénario PARSÉES PAR AST (aucune exécution —
    le recoup lit le code, jamais il ne le joue). bytes.fromhex(…) est
    évalué à la main : un appel à constante unique, jamais du code."""
    arbre = ast.parse(SCENARIO.read_text(encoding="utf-8"))

    def evaluer(noeud):
        if isinstance(noeud, ast.Constant):
            return noeud.value
        if (isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute)
                and noeud.func.attr == "fromhex"
                and isinstance(noeud.func.value, ast.Name)
                and noeud.func.value.id == "bytes"
                and len(noeud.args) == 1
                and isinstance(noeud.args[0], ast.Constant)
                and isinstance(noeud.args[0].value, str)):
            return bytes.fromhex(noeud.args[0].value)
        if isinstance(noeud, (ast.Tuple, ast.List)):
            elems = [evaluer(e) for e in noeud.elts]
            if any(e is _SENTINELLE for e in elems):
                return _SENTINELLE
            return tuple(elems) if isinstance(noeud, ast.Tuple) else elems
        return _SENTINELLE

    valeurs = {}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name):
                    v = evaluer(noeud.value)
                    if v is not _SENTINELLE:
                        valeurs[cible.id] = v
    return valeurs


_SENTINELLE = object()


def recoup(kit_dir):
    """LE RECOUP : chaque constante du scénario == l'artefact ou le plan."""
    const = constantes_scenario()
    exe = (kit_dir / "loupe.exe").read_bytes()

    def attendu(nom, valeur, temoin, source):
        if valeur != temoin:
            refus(f"CONSTANTE-{nom}",
                  f"{valeur!r} != {temoin!r} ({source} — la source unique)")

    # l'artefact : l'empreinte et la taille (la carte génération 13 prouve
    # CES octets — le kit ne peut pas embarquer un autre build)
    attendu("SHA_EXE", const.get("SHA_EXE"), SHA_EXE, "l'artefact")
    attendu("TAILLE_EXE", const.get("TAILLE_EXE"), len(exe), "l'artefact")
    if hashlib.sha256(exe).hexdigest() != SHA_EXE:
        refus("ARTEFACT-DIVERGENT", "loupe.exe du kit != le sha256 asserté")

    # les adresses scellées : le plan (source unique)
    for nom, temoin in (("R_LIBC01", L.R_LIBC01), ("R_LIBC02", L.R_LIBC02),
                        ("R_LIBC07", L.R_LIBC07), ("R_WIN03", L.R_WIN03),
                        ("R_MD5_S", L.R_MD5_S), ("R_MD5_T", L.R_MD5_T),
                        ("R_IAT_K32", L.R_IAT_K32), ("R_IAT_U32", L.R_IAT_U32),
                        ("R_IAT_GDI", L.R_IAT_GDI),
                        ("R_IAT_DEMO", L.R_IAT_DEMO_GMW),
                        ("R_VERSION", L.R_VERSION), ("R_RELOC", L.R_RELOC),
                        ("R_K", L.R_K),
                        ("R_TLS01", L.R_TLS01), ("R_TLS02", L.R_TLS02),
                        ("R_TLS03", L.R_TLS03), ("R_TLS04", L.R_TLS04),
                        ("R_LOUPE01", L.LOUPE01_VA), ("R_LOUPE02", L.LOUPE02_VA),
                        ("R_LOUPE03", L.LOUPE03_VA), ("R_LOUPE07", L.LOUPE07_VA),
                        ("R_LOUPE08", L.LOUPE08_VA), ("R_LOUPE13", L.LOUPE13_VA),
                        ("R_LOUPE16", L.LOUPE16_VA), ("R_LOUPE17", L.LOUPE17_VA),
                        ("R_CADRE", L.R_CADRE)):
        attendu(nom, const.get(nom), temoin, "loupe/layout.py")

    # les champs du cadre (le layout nomme les TAILLES — les offsets se
    # CALCULENT par la chaîne des tailles, jamais gravés de tête) + la
    # version + les dimensions : le plan
    o_chemin = 0
    o_taille = L.CADRE_CHEMIN
    o_poignee = o_taille + L.CADRE_TAILLE_F
    o_vue = o_poignee + L.CADRE_POIGNEE
    o_curseur = o_vue + L.CADRE_VUE
    o_rempl = o_curseur + L.CADRE_CURSEUR
    o_sale = o_rempl + L.CADRE_REMPLISSAGE
    o_tampon = (o_sale + L.CADRE_SALE + L.CADRE_REFUS_QUITTER
                + L.CADRE_RESERVE)
    for nom, temoin in (("CADRE_CHEMIN", o_chemin),
                        ("CADRE_TAILLE", o_taille),
                        ("CADRE_POIGNEE", o_poignee),
                        ("CADRE_VUE", o_vue),
                        ("CADRE_CURSEUR", o_curseur),
                        ("CADRE_REMPLISSAGE", o_rempl),
                        ("CADRE_SALE", o_sale),
                        ("CADRE_TAMPON", o_tampon),
                        ("DATA_VSIZE", L.DATA_VSIZE),
                        ("VERSION_R10", L.VERSION_DEV),
                        ("LIGNE_TAILLE", L.LIGNE_TAILLE),
                        ("TAMPON_SESSION", L.TAMPON_SESSION),
                        ("WM_CHAR", L.WM_CARACT),
                        ("CTRL_S", L.CTRL_S)):
        attendu(nom, const.get(nom), temoin,
                "loupe/layout.py (les tailles, la chaîne des offsets)")

    # les listes IAT : l'ordre FIGÉ du geste (a)
    attendu("IAT_KERNEL32", tuple(const.get("IAT_KERNEL32", ())),
            tuple(L.IAT_KERNEL32), "le plan (l'ordre figé)")
    attendu("IAT_USER32", tuple(const.get("IAT_USER32", ())),
            tuple(L.IAT_USER32), "le plan (l'ordre figé)")
    attendu("IAT_GDI32", tuple(const.get("IAT_GDI32", ())),
            tuple(L.IAT_GDI32), "le plan (l'ordre figé)")
    attendu("IAT_DEMO", tuple(const.get("IAT_DEMO", ())),
            ("GetMessageW", "TranslateMessage", "DispatchMessageW"),
            "les TROIS slots scellés de win-03")

    # la table K : les constantes FIPS du plan tls13 (la table du scellé M9)
    attendu("K_TETE", tuple(const.get("K_TETE", ())), tuple(LT.K[:4]),
            "tls13/layout.py K (FIPS 180-4)")
    attendu("K_QUEUE", tuple(const.get("K_QUEUE", ())), tuple(LT.K[-4:]),
            "tls13/layout.py K (FIPS 180-4)")

    # les octets attendus des têtes scellées : LA DOUBLE ANCRE — relus
    # DANS L'ARTEFACT ET DANS LES SCELLÉS D'ORIGINE (jamais gravés de tête)
    import struct
    e_lfanew = struct.unpack_from("<I", exe, 0x3C)[0]
    n_sections = struct.unpack_from("<H", exe, e_lfanew + 6)[0]
    taille_opt = struct.unpack_from("<H", exe, e_lfanew + 20)[0]

    def rva_vers_raw(rva):
        for k in range(n_sections):
            o = e_lfanew + 24 + taille_opt + k * 40
            va, = struct.unpack_from("<I", exe, o + 12)
            vs, = struct.unpack_from("<I", exe, o + 8)
            ra, = struct.unpack_from("<I", exe, o + 20)
            if va <= rva < va + vs:
                return ra + (rva - va)
        refus("RVA-INTROUVABLE", f"{rva:#x} hors des sections de l'artefact")

    m1 = (REPO / "m1" / "selftest.exe").read_bytes()
    demo = (REPO / "demo" / "demo.exe").read_bytes()
    m9 = (REPO / "tls13" / "proxy.exe").read_bytes()

    def tranche_scelle(donnees, rva, n):
        e = struct.unpack_from("<I", donnees, 0x3C)[0]
        nb = struct.unpack_from("<H", donnees, e + 6)[0]
        opt = struct.unpack_from("<H", donnees, e + 20)[0]
        for k in range(nb):
            o = e + 24 + opt + k * 40
            va, = struct.unpack_from("<I", donnees, o + 12)
            vs, = struct.unpack_from("<I", donnees, o + 8)
            ra, = struct.unpack_from("<I", donnees, o + 20)
            if va <= rva < va + vs:
                raw = ra + (rva - va)
                return donnees[raw:raw + n]
        refus("RVA-INTROUVABLE", f"{rva:#x} hors du scellé")

    for nom, rva, origine, rva_origine in (
            ("TETE_LIBC01", L.R_LIBC01, m1, 0x1100),
            ("TETE_LIBC02", L.R_LIBC02, m1, 0x1180),
            ("TETE_LIBC07", L.R_LIBC07, m1, 0x13C0),
            ("TETE_WIN03", L.R_WIN03, demo, 0x15C0),
            ("TETE_TLS01", L.R_TLS01, m9, LT.TLS01_VA)):
        attendu(nom, bytes(const.get(nom, b"")),
                exe[rva_vers_raw(rva):rva_vers_raw(rva) + 6],
                "les octets de l'artefact")
        attendu(f"{nom} (l'origine scellée)",
                bytes(const.get(nom, b"")),
                tranche_scelle(origine, rva_origine, 6),
                "les octets du scellé d'origine")
    # le qword version dans l'image
    attendu("VERSION_R10 (le qword @0x2E80)",
            struct.unpack("<Q", exe[rva_vers_raw(L.R_VERSION):
                                    rva_vers_raw(L.R_VERSION) + 8])[0],
            L.VERSION_DEV, "les octets de l'artefact")
    print(f"[recoup] LES CONSTANTES DU SCÉNARIO RECOUPÉES : {36} adresses et "
          f"listes == le plan · l'empreinte == l'artefact · les têtes scellées "
          f"et la table K == les octets — la source unique est le dépôt")
    # LA SONDE DE L'ENTRÉE 205 : ses cibles se CALCULENT depuis l'image
    # (e_lfanew → l'Optional → le tableau des sections) : RIEN à recouper
    # contre le plan — les valeurs patchées (0x1000, 0x400, 3) sont LES
    # FAITS HISTORIQUES de la géométrie dev.2 refusée par le terrain


def main():
    print("=== LE KIT TERRAIN M10-(e) : l'assemblage et l'épreuve de labo ===")
    if not EXE.exists():
        refus("ARTEFACT-ABSENT", f"{EXE} introuvable — construire d'abord")
    racine = SORTIE / KIT
    if racine.exists():
        shutil.rmtree(racine)
    racine.mkdir(parents=True)
    shutil.copy2(EXE, racine / "loupe.exe")
    shutil.copy2(SCENARIO, racine / "scenario-loupe.py")
    shutil.copy2(LISEZMOI, racine / "LISEZMOI-KIT-LOUPE.md")
    print(f"[assemblage] {racine} : loupe.exe + scenario-loupe.py + "
          f"LISEZMOI-KIT-LOUPE.md")

    recoup(racine)

    # la compilation : aucune erreur de syntaxe
    py_compile.compile(str(racine / "scenario-loupe.py"), doraise=True)
    print("[compilation] py_compile : le scénario compile — aucune erreur")

    # le zip
    if KIT_ZIP.exists():
        KIT_ZIP.unlink()
    with zipfile.ZipFile(KIT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for nom in ("loupe.exe", "scenario-loupe.py", "LISEZMOI-KIT-LOUPE.md"):
            z.write(racine / nom, arcname=f"{KIT}/{nom}")
    taille = KIT_ZIP.stat().st_size
    md5 = hashlib.md5(KIT_ZIP.read_bytes()).hexdigest()
    sha = hashlib.sha256(KIT_ZIP.read_bytes()).hexdigest()
    print(f"[zip] {KIT_ZIP} : {taille} o, md5 {md5[:12]}…, sha256 {sha[:12]}…")

    # l'épreuve d'extraction vierge
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(KIT_ZIP) as z:
            z.extractall(tmp)
        extrait = pathlib.Path(tmp) / KIT
        attendus = {"loupe.exe": SHA_EXE, "scenario-loupe.py":
                    hashlib.sha256(SCENARIO.read_bytes()).hexdigest(),
                    "LISEZMOI-KIT-LOUPE.md":
                    hashlib.sha256(LISEZMOI.read_bytes()).hexdigest()}
        for nom, sha_attendu in attendus.items():
            donnees = (extrait / nom).read_bytes()
            if hashlib.sha256(donnees).hexdigest() != sha_attendu:
                refus("EXTRACTION-DIVERGENTE", f"{nom} extrait != l'original")
        recoup(extrait)      # le recoup JOUÉ SUR L'EXTRAIT (le kit réel)
    print("[extraction] l'épreuve VIERGE : le zip extrait dans un répertoire "
          "NEUF, les empreintes re-constatées, le recoup rejoué — VERT")

    print(f"=== LE KIT ASSEMBLÉ ET ÉPROUVÉ : {KIT_ZIP} ({taille} o, md5 "
          f"{md5[:12]}…, sha256 {sha[:12]}…) — prêt pour le coffre /test "
          f"(deposer_kit_loupe.py) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
