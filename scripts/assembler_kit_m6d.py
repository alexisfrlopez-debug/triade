#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_m6d.py — LE KIT TERRAIN M6-(d) : assemblage PAR SCRIPT,
modèle assembler_kit_e4.py (Task 57) — le kit Linux du patch en production.

Les pièces :
  1. LA CARTOUCHE PRÉ-ASSEMBLÉE : la MÊME source que l'instrument de
     l'oracle (unix/oracle_corpus.py — CARTOUCHE + CANARIS), assemblée par
     keystone POUR LA BASE 0 (le gabarit relocalisable : la cartouche
     n'embarque qu'UNE adresse absolue, l'imm64 « mov r11, .retour ») ;
     RECOUPÉE contre l'instrument VIVANT : le gabarit assemblé à
     l'adresse réelle d'une Cartouche en vie == les octets de la page,
     OCTET POUR OCTET (la preuve que le terrain exécutera le même
     instrument que l'oracle) ;
  2. LE SCÉNARIO GÉNÉRÉ : unix/terrain/scenario-m6d.py naît du gabarit
     .in (les placeholders substitués : octets hex, sha256, l'offset du
     fixup, l'offset de .retour, le sha du scellé) — py_compilé avant
     tout autre geste ;
  3. LE KIT : download/vague-m6d/kit-m6d.zip — m6-kit/ (corpus scellé
     0.7.0-rc.1 + scenario-m6d.py + LISEZMOI-KIT-M6D.md), le bit
     exécutable porté DANS le zip ;
  4. L'ÉPREUVE : le kit EXACT (celui qui sera déposé) est extrait dans
     un dossier VIERGE et EXÉCUTÉ au laboratoire — le run doit rendre
     VERT (rc 0, les trois pièces nées, le verdict sur pièces) ; un kit
     qui n'est pas vert au labo n'est pas déposé ;
  5. L'INTÉGRITÉ : le zip relu après construction (corpus relu ==
     scellé, scénario relu == généré), empreintes consignées pour le
     dépôt Drive (passeur séparé).

Usage : python3 scripts/assembler_kit_m6d.py
Code de sortie : 0 = kit assemblé, éprouvé, prêt au dépôt ; 2 = refus nommé."""

import ctypes
import hashlib
import os
import py_compile
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

REPO = "/home/z/my-project/triade"
UNIX = os.path.join(REPO, "unix")
SORTIE_DIR = "/home/z/my-project/download/vague-m6d"
GABARIT = os.path.join(UNIX, "terrain", "scenario-m6d.py.in")
SCENARIO = os.path.join(UNIX, "terrain", "scenario-m6d.py")
LISEZMOI = os.path.join(UNIX, "terrain", "LISEZMOI-KIT-M6D.md")
ARTEFACT = os.path.join(UNIX, "corpus")
ZIP_KIT = os.path.join(SORTIE_DIR, "kit-m6d.zip")

SHA_SCELLE = "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7"

sys.path.insert(0, UNIX)
sys.path.insert(0, os.path.join(UNIX, "outils"))
import layout as L  # noqa: E402
import oracle_corpus as OC  # noqa: E402
import auteur  # noqa: E402

import capstone  # noqa: E402
from keystone import KS_ARCH_X86, KS_MODE_64, Ks  # noqa: E402


class Refus(Exception):
    """Tout refus nommé de l'assembleur (fail-closed)."""


def lignes_cartouche():
    lignes = []
    for l in OC.CARTOUCHE.splitlines():
        l = l.strip()
        if not l:
            continue
        if l.startswith(".") and l.endswith(":"):
            lignes.append(("label", l[1:-1]))
        else:
            lignes.append(("instr", l))
    return lignes


def assembler_cartouche(ks, base):
    """La cartouche assemblée POUR `base` (mêmes symboles que l'oracle)."""
    symboles = {f"CAN{i + 1}": OC.CANARIS[i] for i in range(6)}
    resolues, adresses = auteur.resoudre(ks, base, symboles, lignes_cartouche())
    return b"".join(r["octets"] for r in resolues), resolues, adresses


# L'adresse factice du gabarit : HAUTE (une vraie adresse mmap), pour que
# keystone émette la forme imm64 « 49 BB <imm64> » du movabs r11 — la forme
# que le terrain relogera PAR LE FIXUP (une base 0 produirait la forme
# imm32 tronquée, inutilisable pour une vraie page)
A0 = 0x100000000000


def main() -> int:
    print("=== M6-(d) : assemblage du kit terrain ===")
    ks = Ks(KS_ARCH_X86, KS_MODE_64)

    # (1) LE GABARIT (assemblé à l'adresse factice HAUTE) + le fixup unique ---
    gabarit, resolues, adresses = assembler_cartouche(ks, A0)
    retour_off = adresses["retour"] - A0
    # l'imm64 « movabs r11, .retour » : trouvé PAR DÉSASSEMBLAGE (jamais cru)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    fixup_off = None
    for insn in cs.disasm(gabarit, A0):
        if insn.mnemonic == "movabs" and insn.op_str.startswith("r11,"):
            fixup_off = insn.address - A0 + 2       # 49 BB <imm64>
            imm = struct.unpack_from("<Q", gabarit, fixup_off)[0]
            if imm != A0 + retour_off:
                raise Refus(f"l'imm64 movabs ({imm:#x}) != .retour ({A0 + retour_off:#x}) "
                            "— le gabarit est incohérent")
            break
    if fixup_off is None:
        raise Refus("l'instruction « movabs r11, .retour » est introuvable dans la cartouche")
    print(f"[cartouche] gabarit {len(gabarit)} o (assemblé à l'adresse factice {A0:#x}) ; "
          f"le fixup unique @ +{fixup_off:#x} (movabs r11, imm64 -> .retour "
          f"@ +{retour_off:#x} de la page)")

    # (2) LE RECOUPEMENT contre l'instrument VIVANT -----------------------------
    cart = OC.Cartouche()                      # l'instrument de l'oracle, en vie
    vivant = ctypes.string_at(cart.code, len(gabarit))
    a_ladresse = assembler_cartouche(ks, cart.code)[0]
    if a_ladresse != vivant:
        raise Refus("le gabarit assemblé à l'adresse réelle != les octets de la "
                    "page vivante — la source a divergé de l'instrument")
    # et le gabarit + le fixup == l'instrument (l'identité du terrain)
    corrige = bytearray(gabarit)
    struct.pack_into("<Q", corrige, fixup_off, cart.code + retour_off)
    if bytes(corrige) != vivant:
        raise Refus("gabarit + fixup != instrument vivant — le fixup est faux")
    print(f"[cartouche] recoupée contre l'instrument VIVANT de l'oracle "
          f"(@{cart.code:#x}) : gabarit+fixup == la page, OCTET POUR OCTET")

    # (3) LE SCÉNARIO GÉNÉRÉ -----------------------------------------------------
    with open(GABARIT, encoding="utf-8") as f:
        src = f.read()
    for marque in ("@@CARTOUCHE_HEX@@", "@@CARTOUCHE_SHA@@@", "@@FIXUP_OFF@@",
                   "@@RETOUR_OFF@@", "@@SHA_SCELLE@@"):
        if marque.replace("@@@", "@@") not in src and marque not in src:
            raise Refus(f"le gabarit ne porte pas le placeholder {marque}")
    src = (src
           .replace("@@CARTOUCHE_HEX@@", gabarit.hex())
           .replace("@@CARTOUCHE_SHA@@", hashlib.sha256(gabarit).hexdigest())
           .replace("@@FIXUP_OFF@@", hex(fixup_off))
           .replace("@@RETOUR_OFF@@", hex(retour_off))
           .replace("@@SHA_SCELLE@@", SHA_SCELLE))
    if "@@" in src:
        raise Refus("un placeholder subsiste dans le scénario généré")
    with open(SCENARIO, "w", encoding="utf-8") as f:
        f.write(src)
    py_compile.compile(SCENARIO, doraise=True)
    print(f"[scenario] généré {SCENARIO} ({len(src)} o), py_compilé — "
          f"cartouche {hashlib.sha256(gabarit).hexdigest()[:16]}… embarquée")

    # (4) LE KIT -----------------------------------------------------------------
    with open(ARTEFACT, "rb") as f:
        artefact = f.read()
    if hashlib.sha256(artefact).hexdigest() != SHA_SCELLE:
        raise Refus("l'artefact n'est pas le scellé 0.7.0-rc.1 — le kit refuse")
    os.makedirs(SORTIE_DIR, exist_ok=True)
    if os.path.exists(ZIP_KIT):
        os.unlink(ZIP_KIT)
    with zipfile.ZipFile(ZIP_KIT, "w", zipfile.ZIP_DEFLATED) as z:
        zi = zipfile.ZipInfo("m6-kit/corpus")
        zi.external_attr = (0o755 << 16)
        z.writestr(zi, artefact)
        zi = zipfile.ZipInfo("m6-kit/scenario-m6d.py")
        zi.external_attr = (0o755 << 16)
        with open(SCENARIO, encoding="utf-8") as f:
            z.writestr(zi, f.read())
        with open(LISEZMOI, encoding="utf-8") as f:
            z.writestr("m6-kit/LISEZMOI-KIT-M6D.md", f.read())
    print(f"[kit] {ZIP_KIT} construit ({os.path.getsize(ZIP_KIT)} o)")

    # (5) L'INTÉGRITÉ RELUE --------------------------------------------------------
    with zipfile.ZipFile(ZIP_KIT) as z:
        if hashlib.sha256(z.read("m6-kit/corpus")).hexdigest() != SHA_SCELLE:
            raise Refus("le corpus relu dans le zip != le scellé")
        if z.read("m6-kit/scenario-m6d.py") != src.encode():
            raise Refus("le scénario relu dans le zip != le généré")
        nb = len(z.namelist())
        print(f"[kit] relu : corpus == scellé (sha256 {SHA_SCELLE[:16]}…), "
              f"scénario == généré, {nb} entrées")

    # (6) L'ÉPREUVE : le kit EXACT, extraction vierge + run ------------------------
    eprouve_dir = tempfile.mkdtemp(prefix="kit-m6d-epreuve-")
    try:
        with zipfile.ZipFile(ZIP_KIT) as z:
            z.extractall(eprouve_dir)
        p = subprocess.run([sys.executable, "scenario-m6d.py"],
                           cwd=os.path.join(eprouve_dir, "m6-kit"),
                           capture_output=True, text=True, timeout=180)
        journal = os.path.join(eprouve_dir, "m6-kit", "preuves-m6",
                               "scenario-m6d-journal.log")
        verdict = os.path.join(eprouve_dir, "m6-kit", "preuves-m6",
                               "VERDICT-run-m6d.txt")
        ok = (p.returncode == 0 and os.path.exists(journal)
              and os.path.exists(verdict))
        if not ok:
            print(p.stdout[-3000:])
            print(p.stderr[-2000:], file=sys.stderr)
            raise Refus(f"le kit n'est pas vert au labo (rc={p.returncode}) — "
                        "il n'est pas déposé")
        with open(verdict, encoding="utf-8") as f:
            v = f.read()
        if "VERDICT : VERT" not in v:
            raise Refus("le verdict du kit au labo n'est pas VERT — pas de dépôt")
        lignes_vertes = [l for l in v.splitlines() if l.startswith("[m6d]")]
        print(f"[épreuve] le kit EXACT, extraction vierge + run : rc=0, VERT "
              f"({len(lignes_vertes)} constats) — le kit déposé est le kit prouvé")
        for l in v.splitlines():
            if "constats PASS" in l or "VERDICT" in l:
                print(f"[épreuve]   {l}")
    finally:
        shutil.rmtree(eprouve_dir, ignore_errors=True)

    # (7) LES EMPREINTES pour le dépôt ----------------------------------------------
    with open(ZIP_KIT, "rb") as f:
        kit = f.read()
    print(f"[dépôt] kit-m6d.zip : {len(kit)} o, "
          f"sha256 {hashlib.sha256(kit).hexdigest()}, "
          f"md5 {hashlib.md5(kit).hexdigest()}")
    print("[dépôt] prêt : scripts/deposer_kit_m6d.py conduit le coffre /test "
          "(archivage e4 D143 + dépôt de la vague m6d + preuves-m6)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refus as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(2)
