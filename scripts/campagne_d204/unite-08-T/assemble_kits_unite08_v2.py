#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_kits_unite08_v2.py — LES DEUX KITS v2 DE L'UNITÉ 4, la gravure
stable (le correctif du 15/11 apr-midi : la boucle V3 du bras T — cast au
lieu du constructeur c_void_p — et la découverte du bras C — les arités
(base, rva) unifiées)). Chaque pièce hors scénario demeure BYTE-BYTE la
gravure du kit v1 (recoupée aux lignes de l'EMPREINTES v1 AVANT la copie) ;
le scénario seul change ; l'EMPREINTES régénérée couvre les NEUF pièces."""
import hashlib
import pathlib
import py_compile
import re
import shutil
import zipfile

ICI = pathlib.Path(__file__).resolve().parent
U_T = ICI                    # unite-08-T
U_C = ICI.parent / "unite-08-C"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def gravure_v1(kit: pathlib.Path, nom_emp: str) -> dict:
    """Les lignes « sha  pièce » de l'EMPREINTES v1 — la gravure à tenir."""
    lignes = (kit / nom_emp).read_text(encoding="utf-8-sig").splitlines()
    return {l.split(None, 1)[1].strip(): l.split(None, 1)[0]
            for l in lignes if re.match(r"^[0-9a-f]{64}  ", l)}


def assembler(unite: pathlib.Path, nom_kit: str, nom_scenario: str,
              nom_emp: str, suffixe: str) -> None:
    kit_v1 = unite / "kit"
    kit_v2 = unite / "kit-v2"
    gravure = gravure_v1(kit_v1, nom_emp)

    if kit_v2.exists():
        shutil.rmtree(kit_v2)
    kit_v2.mkdir()
    # les SEPT pièces stables (9 = 7 stables + le scénario + l'EMPREINTES) :
    # copiées du kit v1, RECROUPÉES à la gravure
    stables = [p for p in sorted(kit_v1.iterdir())
               if p.is_file() and p.name not in (nom_scenario, nom_emp)]
    assert len(stables) == 7, f"{nom_kit} : {len(stables)} pièces stables != 7"
    for p in stables:
        assert sha(p) == gravure[p.name], \
            f"{p.name} : la pièce v1 != sa propre gravure — rien ne bouge"
        shutil.copy2(p, kit_v2 / p.name)
    # le scénario CORRIGÉ (la source du kit v2 — la seule pièce qui bouge)
    shutil.copy2(unite / nom_scenario, kit_v2 / nom_scenario)
    py_compile.compile(str(kit_v2 / nom_scenario), doraise=True)

    # l'EMPREINTES régénérée (le format du kit v1 : BOM + CRLF, byte-byte)
    pieces = sorted(p for p in kit_v2.iterdir() if p.is_file() and p.name != nom_emp)
    lignes = [
        "\ufeffEMPREINTES — LE KIT DE L'UNITÉ 4 (loupe-08 LIGNE × bras "
        f"{suffixe}, la campagne D204)",
        "(chaque pièce sha256 — le GUI recoupe à l'onglet 1·KIT ; une "
        "divergence, rien ne court)",
        "",
    ]
    for p in pieces:
        lignes.append(f"{sha(p)}  {p.name}")
    (kit_v2 / nom_emp).write_text("\r\n".join(lignes) + "\r\n",
                                  encoding="utf-8", newline="")

    # le recoup : chaque pièce v2 == sa ligne de gravure (les stables == v1)
    gravure_v2 = gravure_v1(kit_v2, nom_emp)
    attendus = {p.name for p in kit_v2.iterdir()
                if p.is_file() and p.name != nom_emp}
    assert set(gravure_v2) == attendus == set(gravure), \
        f"la gravure v2 {sorted(gravure_v2)} != les pièces {sorted(attendus)}"
    for p in sorted(kit_v2.iterdir()):
        if p.is_file() and p.name in gravure_v2:
            assert sha(p) == gravure_v2[p.name], f"{p.name} != sa gravure v2"
    bougees = [n for n in gravure_v2 if gravure_v2[n] != gravure.get(n)]
    assert bougees == [nom_scenario], \
        f"les pièces bougées : {bougees} != le scénario seul"
    print(f"[gravure] {nom_kit}-v2 : {len(gravure_v2)} pièces gravées, "
          f"la seule bougée : {nom_scenario} "
          f"({gravure.get(nom_scenario, '')[:12]}… → {gravure_v2[nom_scenario][:12]}…)")

    # le zip (plat, comme le v1) + l'extraction vierge
    cible = unite / f"{nom_kit}-v2.zip"
    with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(kit_v2.iterdir()):
            if p.is_file():
                zf.write(p, p.name)
    with zipfile.ZipFile(cible) as zf:
        for p in sorted(kit_v2.iterdir()):
            if p.is_file():
                assert hashlib.sha256(zf.read(p.name)).hexdigest() == sha(p), \
                    f"l'extraction de {p.name} diverge"
    nb = sum(1 for p in kit_v2.iterdir() if p.is_file())
    print(f"[zip] {cible.name} : {nb} pièces, l'extraction vierge recoupée")


assembler(U_T, "kit-unite-loupe-08-T-20261115", "scenario-unite08.py",
          "EMPREINTES-KIT-UNITE-08-T.txt", "T")
assembler(U_C, "kit-unite-loupe-08-C-20261115", "scenario-unite08C.py",
          "EMPREINTES-KIT-UNITE-08-C.txt", "C")
print("=== LES DEUX KITS v2 ASSEMBLÉS, GRAVÉS, ZIPPÉS — prêts au coffre ===")
