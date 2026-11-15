#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_kits_unite08.py — LES DEUX KITS DE L'UNITÉ 4 assemblés et gravés
(la campagne D204, loupe-08 ligne × T et C). Chaque kit porte SES pièces —
la gravure EMPREINTES couvre chaque pièce livrée, la génération FIXE des
témoins recoupée aux gravures des kits 01/02/05 AVANT toute copie."""
import hashlib
import pathlib
import py_compile
import shutil
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[3]
U_T = pathlib.Path(__file__).resolve().parents[1] / "unite-08-T"
U_C = pathlib.Path(__file__).resolve().parents[1] / "unite-08-C"
sys.path.insert(0, str(REPO / "loupe"))
import harnais_noyau as HN          # noqa: E402  (les témoins de la FIXE)


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---- LES FIXTURES DE GÉNÉRATION FIXE (recoupées aux gravures connues) ------
temoins = HN.composer_temoins()
assert hashlib.sha256(temoins["temoin-3f.bin"]).hexdigest() == \
    "c5fc1f28e471059d56a892ba82df1e215f5263aafd8c43fdb0e76e110d1d5ca3", \
    "temoin-3f.bin != la gravure des kits 01/02/05 — la génération FIXE a bougé"
proxy = REPO / "tls13" / "proxy.exe"
assert hashlib.sha256(proxy.read_bytes()).hexdigest() == HN.SCELLE_M9_SHA256, \
    "proxy.exe != l'ancre scellée M9 du harnais"
print("[fixtures] temoin-3f.bin == la gravure c5fc1f28…, proxy.exe == "
      "l'ancre scellée M9 — la génération FIXE tient")

# ---- LA PIÈCE T : la cristallisée ------------------------------------------
piece_T = U_T / "piece" / "loupe.exe"
assert sha(piece_T) == "eec890a4cdc3f6a50c733157bad5a228292efb49b587f46043357e7542ca8b6e", \
    "loupe.exe != la cristallisation — rebuild d'abord"

# ---- LA PIÈCE C : la compilée ----------------------------------------------
piece_C = U_C / "source" / "loupe-08-c.dll"
assert sha(piece_C) == "9a51be684e2dec304d3324eaa5c3a069e7f2676166c789f3b2d2763f13312a73", \
    "loupe-08-c.dll != la compilation recoupée au POSIX"

# ---- LE KIT T (9 pièces) ----------------------------------------------------
KIT_T = U_T / "kit"
for f in KIT_T.iterdir():
    if f.name != "LISEZMOI-KIT-UNITE-08-T.txt":
        f.unlink()
for nom, source in (
        ("loupe.exe", piece_T),
        ("notation-loupe-08-ligne.asm", U_T / "notation" / "loupe-08-ligne.asm"),
        ("brouillon-loupe-08-ligne.asm",
         U_T / "brouillons" / "loupe-08-ligne.asm"),
        ("scenario-unite08.py", U_T / "scenario-unite08.py"),
        ("LANCEUR-UNITE-08-T.bat",
         U_T / "LANCEUR-UNITE-08-T.bat"),
        ("proxy.exe", proxy)):
    shutil.copy2(source, KIT_T / nom)
(KIT_T / "temoin-3f.bin").write_bytes(temoins["temoin-3f.bin"])
py_compile.compile(str(KIT_T / "scenario-unite08.py"), doraise=True)
shutil.rmtree(KIT_T / "__pycache__", ignore_errors=True)

# ---- LE KIT C (9 pièces) ----------------------------------------------------
KIT_C = U_C / "kit"
for f in KIT_C.iterdir():
    if f.name != "LISEZMOI-KIT-UNITE-08-C.txt":
        f.unlink()
for nom, source in (
        ("loupe-08-c.dll", piece_C),
        ("loupe-08-c.c", U_C / "source" / "loupe-08-c.c"),
        ("loupe-08-c.def", U_C / "source" / "loupe-08-c.def"),
        ("scenario-unite08C.py", U_C / "scenario-unite08C.py"),
        ("LANCEUR-UNITE-08-C.bat",
         U_C / "LANCEUR-UNITE-08-C.bat"),
        ("proxy.exe", proxy)):
    shutil.copy2(source, KIT_C / nom)
(KIT_C / "temoin-3f.bin").write_bytes(temoins["temoin-3f.bin"])
py_compile.compile(str(KIT_C / "scenario-unite08C.py"), doraise=True)
shutil.rmtree(KIT_C / "__pycache__", ignore_errors=True)
print("[kits] les pièces posées, les DEUX scénarios py_compile OK")

# ---- LES GRAVURES (EMPREINTES) ---------------------------------------------
for kit, entete in (
        (KIT_T, "T"), (KIT_C, "C")):
    pieces = sorted(p for p in kit.iterdir()
                    if p.is_file()
                    and p.name != f"EMPREINTES-KIT-UNITE-08-{entete}.txt")
    lignes = [
        "\ufeffEMPREINTES — LE KIT DE L'UNITÉ 4 (loupe-08 LIGNE × bras "
        f"{entete}, la campagne D204)",
        "(chaque pièce sha256 — le GUI recoupe à l'onglet 1·KIT ; une "
        "divergence, rien ne court)",
        "",
    ]
    for p in pieces:
        lignes.append(f"{sha(p)}  {p.name}")
    (kit / f"EMPREINTES-KIT-UNITE-08-{entete}.txt").write_text(
        "\r\n".join(lignes) + "\r\n", encoding="utf-8", newline="")
    nb = len(pieces) + 1
    print(f"[gravure] kit {entete} : {nb} pièces gravées "
          f"({', '.join(p.name for p in sorted(pieces))[:70]}…)")
    # le recoup : chaque pièce du kit == sa ligne de gravure
    gravure = {}
    for ligne in (kit / f"EMPREINTES-KIT-UNITE-08-{entete}.txt") \
            .read_text(encoding="utf-8-sig").splitlines():
        parts = ligne.strip().split(None, 1)
        if len(parts) == 2 and len(parts[0]) == 64:
            gravure[parts[1]] = parts[0]
    for p in kit.iterdir():
        if p.name in gravure:
            assert sha(p) == gravure[p.name], f"{p.name} != sa gravure"
    print(f"[recoup] kit {entete} : {len(gravure)}/{len(gravure)} pièces "
          "== la gravure")

# ---- LES ZIPS (l'extraction vierge) ----------------------------------------
for kit, nom_zip in ((KIT_T, "kit-unite-loupe-08-T-20261115.zip"),
                     (KIT_C, "kit-unite-loupe-08-C-20261115.zip")):
    cible = kit.parent / nom_zip
    with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(kit.iterdir()):
            if p.is_file():
                zf.write(p, p.name)
    # l'extraction vierge : chaque octet relu == l'original
    with zipfile.ZipFile(cible) as zf:
        for p in sorted(kit.iterdir()):
            if p.is_file():
                assert hashlib.sha256(zf.read(p.name)).hexdigest() == sha(p), \
                    f"l'extraction de {p.name} diverge"
    nb_z = sum(1 for p in kit.iterdir() if p.is_file())
    print(f"[zip] {cible.name} : {nb_z} pièces, "
          f"l'extraction vierge recoupée")
print("=== LES DEUX KITS ASSEMBLÉS, GRAVÉS, ZIPPÉS — prêts au coffre ===")
