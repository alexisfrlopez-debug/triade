#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts/construire_kit_shani.py — LE KIT TERRAIN DE LA MESURE AVANT/APRÈS
SHA-NI (le paquet 6/6, l'instruction lfh49a1xf, D205) : l'image de laboratoire
POSÉE en un seul fichier + le scénario qui la mesure.

L'IMAGE (image-shani.bin) : la plage RVA 0x2000-0xE000 (48 Kio) — la table K
DU SCELLÉ @0x2F00 (extraite de loupe.exe, les octets DÉPLOYÉS), le masque BE
@0x2800, la famille sha SCELLÉE @0xC000-0xC3C0 (extraite de loupe.exe — LE
REPLI, R7), les TROIS blocs de la variante @0xD000-0xD4C0 (les notations
assemblées par keystone). TOUTES les références internes sont RELATIVES
(les déplacements RIP et les appels rel32 du plan) : l'image vit à N'IMPORTE
QUELLE base — le scénario la pose dans la mémoire exécutable qu'il alloue.

LE SCÉNARIO (shani/terrain/scenario-shani.py) : la mesure du DÉVELOPPEUR sur
SA machine — la MÊME entrée (8 Mio de PRNG déterministe), la MÊME machine,
le condensé VÉRIFIÉ à hashlib AVANT comptage, les opérations COMPLÈTES
init+absorb+final, 15 répétitions par bras, les médianes et IQR — le témoin
temoin-shani.txt.

AUCUN SCELLAGE : l'image du kit est une PIÈCE DE LABORATOIRE (jamais la
carte, jamais la cérémonie — charte § 3 du domaine) ; la source des octets
est CONSIGNÉE (chaque plage citée avec sa provenance).

Usage : python3 scripts/construire_kit_shani.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import struct
import sys

TRIADE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHANI = os.path.join(TRIADE, "shani")
TERRAIN = os.path.join(SHANI, "terrain")

from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

KS = Ks(KS_ARCH_X86, KS_MODE_64)

_spec = importlib.util.spec_from_file_location(
    "layout_shani", os.path.join(SHANI, "layout.py"))
LSH = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(LSH)

DEBUT, FIN = 0x2000, 0xE000      # la plage RVA de l'image du kit


def extraire_section(donnees: bytes, rva: int, taille: int) -> bytes:
    e = struct.unpack_from("<I", donnees, 0x3C)[0]
    nb = struct.unpack_from("<H", donnees, e + 6)[0]
    opt = struct.unpack_from("<H", donnees, e + 20)[0]
    for i in range(nb):
        o = e + 24 + opt + i * 40
        va, = struct.unpack_from("<I", donnees, o + 12)
        vs, = struct.unpack_from("<I", donnees, o + 8)
        ra, = struct.unpack_from("<I", donnees, o + 20)
        if va <= rva < va + vs:
            raw = ra + (rva - va)
            return donnees[raw:raw + taille]
    raise ValueError(f"RVA {rva:#x} introuvable")


def lire_notation(chemin: str) -> bytes:
    corps, rva, slot = [], None, None
    for brut in open(chemin, encoding="utf-8").read().splitlines():
        if brut.startswith(";"):
            if "slot RVA" in brut:
                rva = int(brut.split("slot RVA ")[1].split(",")[0], 16)
            if "taille" in brut and "octets" in brut and "slot RVA" in brut:
                slot = int(brut.split("taille ")[1].split(" octets")[0])
            continue
        l = brut.split(";")[0].strip()
        if l:
            corps.append(l)
    octets, a = b"", rva
    for l in corps:
        e, _ = KS.asm(l, a)
        octets += bytes(e)
        a += len(e)
    if slot and len(octets) < slot:
        octets += b"\x90" * (slot - len(octets))
    return octets


def main() -> int:
    print("=== scripts/construire_kit_shani.py — L'IMAGE DU KIT POSÉE ===")
    loupe = open(os.path.join(TRIADE, "loupe", "loupe.exe"), "rb").read()
    emp_loupe = hashlib.sha256(loupe).hexdigest()
    assert emp_loupe.startswith("c111510535767a40"), "loupe.exe a divergé"

    image = bytearray(FIN - DEBUT)      # la plage 0x2000-0xE000

    def poser(rva: int, donnees: bytes, provenance: str) -> None:
        assert DEBUT <= rva and rva + len(donnees) <= FIN
        image[rva - DEBUT:rva - DEBUT + len(donnees)] = donnees
        print(f"  0x{rva:05x}-0x{rva + len(donnees):05x} "
              f"({len(donnees):>4} o)  {provenance}")

    # LA TABLE K DU SCELLÉ (jamais re-déclarée — les octets déployés)
    poser(LSH.R_K, extraire_section(loupe, LSH.R_K, 256),
          "K[64] du scellé loupe.exe (la source unique)")
    # LE MASQUE BE de la variante
    poser(LSH.R_MASQUE, LSH.MASQUE_BE, "le masque BE (shani/layout.py)")
    # LA FAMILLE SHA SCELLÉE — LE REPLI (R7)
    for nom, rva, taille in (("tls13-01", LSH.R_TLS01, 0x80),
                             ("tls13-02", LSH.R_TLS02, 0x1C0),
                             ("tls13-03", LSH.R_TLS03, 0xC0),
                             ("tls13-04", LSH.R_TLS04, 0xC0)):
        poser(rva, extraire_section(loupe, rva, taille),
              f"{nom} DU SCELLÉ loupe.exe (le repli, R7)")
    # LA VARIANTE (les notations assemblées — keystone, rien d'autre)
    for nom, rva in (("shani-01-sonde", LSH.SHANI01_VA),
                     ("shani-02-comprimer", LSH.SHANI02_VA),
                     ("shani-03-absorber", LSH.SHANI03_VA)):
        octets = lire_notation(os.path.join(SHANI, "notation", nom + ".asm"))
        poser(rva, octets, f"{nom} — la notation assemblée (la variante)")

    chemin_image = os.path.join(TERRAIN, "image-shani.bin")
    with open(chemin_image, "wb") as f:
        f.write(bytes(image))
    empreinte = hashlib.sha256(bytes(image)).hexdigest()
    print(f"\nL'IMAGE : {chemin_image}")
    print(f"  {len(image)} o (RVA 0x{DEBUT:x}-0x{FIN:x}) · sha256 {empreinte}")

    # le manifeste du kit (les empreintes des pièces — le scénario les recoupe)
    chemin_manifeste = os.path.join(TERRAIN, "manifeste-kit-shani.txt")
    with open(chemin_manifeste, "w") as f:
        f.write("KIT TERRAIN SHA-NI — LE MANIFESTE (D205, le paquet 6/6)\n")
        f.write("=======================================================\n\n")
        f.write(f"image-shani.bin  {len(image)} o  sha256 {empreinte}\n")
        f.write("  la plage RVA 0x2000-0xE000 : K du scellé @0x2F00, le\n")
        f.write("  masque BE @0x2800, la famille sha scellée @0xC000-0xC3C0\n")
        f.write("  (extraite de loupe.exe c1115105…, LE REPLI R7), la\n")
        f.write("  variante @0xD000-0xD4C0 (les notations shani assemblées)\n")
        f.write("\nAUCUN SCELLAGE : pièce de laboratoire — la cérémonie\n")
        f.write("d'ère et le run terrain appartiennent au développeur.\n")
    print(f"  manifeste : {chemin_manifeste}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
