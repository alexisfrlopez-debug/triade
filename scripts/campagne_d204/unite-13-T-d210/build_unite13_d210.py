#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_unite13_d210.py — LE BUILD DE LA PIÈCE DE CAMPAGNE, l'unité 03
D210 (loupe-13 recherche × bras T — le plan pré-enregistré D204/D210 ; LE
MÊME MÉCANISME que les unités 1 et 2, build_unite02.py /
build_unite08_d210.py).

LA RECOMPOSITION DE LA PIÈCE DEPUIS LE PLAN (la commande M4 du bras T) :
les 18 blocs du domaine — les DIX-SEPT SCELLÉS lus à leurs arbres (LECTURE
SEULE, jamais touchés) + LOUPE-13 LA NOTATION DE CAMPAGNE (brouillon →
auteur → notation, la chaîne de vérité de la lignée) — les 8 héritages
extraits des scellés (R7, la double preuve), l'image composée aux quatre
sections, le PE écrit AU DOSSIER DE CAMPAGNE (jamais au loupe.exe
scellé), validé (l'en-tête, le marché des imports marché comme le
chargeur, les slots == notation + padding NOP, la porte R10).

LA MESURE D161 DE LA PIÈCE DE CAMPAGNE : les 17 scellés == leurs longueurs
d'arrêt ; loupe-13 == SA mesure de campagne (gravée à l'EMPREINTE du kit).

LE DIFFÉRENTIEL contre le scellé : la pièce ne diffère QUE au slot
loupe-13 (RVA 0x5740, 192 o : le code + le padding) et à la porte R10
(les sommes du bloc) — l'écart CONFINÉ, nommé.

Usage : python3 scripts/campagne_d204/unite-13-T-d210/build_unite13_d210.py
Sortie  : piece/loupe.exe + piece/MESURES-PIECE.txt ; code 0 ou 2 (refus nommé)
"""
from __future__ import annotations

import hashlib
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
if not os.path.basename(REPO) == "triade":
    REPO = "/home/z/my-project/triade/lab/repo2"
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-13-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import build_loupe as BL          # noqa: E402  (le module — la garde __main__)

import importlib.util as _ilu
_sys_layout = sys.modules.get("layout")
_spec_l = _ilu.spec_from_file_location(
    "layout", os.path.join(REPO, "loupe", "layout.py"))
L = _ilu.module_from_spec(_spec_l)
sys.modules["layout"] = L
_spec_l.loader.exec_module(L)
_spec = _ilu.spec_from_file_location(
    "auteur_loupe_campagne", os.path.join(REPO, "loupe", "outils",
                                          "auteur.py"))
AUTEUR = _ilu.module_from_spec(_spec)
sys.modules["auteur_loupe_campagne"] = AUTEUR
_spec.loader.exec_module(AUTEUR)
if _sys_layout is not None:
    sys.modules["layout"] = _sys_layout   # le monde tel qu'il était

L = BL.L
B4 = BL.B4

CAMPAGNE = "i110013"          # le bloc de campagne : loupe-13 recherche


def refus(nom: str, detail: str) -> None:
    print(f"[build-unite13-d210] REFUS {nom} : {detail}", file=sys.stderr)
    sys.exit(2)


def plages_raw(exe: bytes, rva: int, taille: int):
    """Le raw fichier d'une plage RVA (le parse minimal des sections)."""
    e = struct.unpack_from("<I", exe, 0x3C)[0]
    nb = struct.unpack_from("<H", exe, e + 6)[0]
    opt = struct.unpack_from("<H", exe, e + 20)[0]
    for k in range(nb):
        o = e + 24 + opt + k * 40
        va = struct.unpack_from("<I", exe, o + 12)[0]
        vs = struct.unpack_from("<I", exe, o + 8)[0]
        ra = struct.unpack_from("<I", exe, o + 20)[0]
        if va <= rva < va + vs:
            return ra + (rva - va), ra + (rva - va) + taille
    refus("RVA-INTROUVABLE", f"la RVA {rva:#x} hors des sections")


def construire() -> int:
    print("=== LE BUILD DE CAMPAGNE — l'unité 03 D210 (loupe-13 × bras T) : "
          "la recomposition de la pièce depuis le plan ===")

    # 1. LA RÉSOLUTION (auteur — les chemins de campagne, l'outil intact)
    AUTEUR.BROUILLONS = os.path.join(UNITE, "brouillons")
    AUTEUR.SORTIE = os.path.join(UNITE, "notation")
    rva13, slot13 = L.SLOTS_LOUPE[CAMPAGNE]
    deps13 = ("AUCUNE entrée IAT (la feuille pure — le miroir exact des "
              "feuilles tls13, charte § 9) ; libc-02 memcmp (LE BLOC "
              "SCELLÉ M1 PAR LA CARTE — I2 : chaque candidat testé par le "
              "scellé, jamais une boucle réécrite) ; le départ au slot "
              "msx64 [rsp+0x28] (P5, le 5e argument)")
    if not os.path.exists(os.path.join(AUTEUR.BROUILLONS,
                                       "loupe-13-recherche.asm")):
        refus("BROUILLON-ABSENT",
              "brouillons/loupe-13-recherche.asm — écrire la notation "
              "d'abord (la phase notation de la campagne)")
    try:
        total, n_ins, n_etq = AUTEUR.resoudre_bloc(
            BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64), "loupe-13-recherche",
            CAMPAGNE, "loupe-13:R1", rva13, slot13, deps13)
    except AUTEUR.ErreurAuteur as exc:
        refus("RÉSOLUTION-AUTEUR", str(exc))
    print(f"[auteur] loupe-13 de campagne résolu : {total} o, {n_ins} "
          f"instructions, {n_etq} étiquettes, {slot13 - total} o de padding "
          f"(slot {slot13:#x})")

    # 2. LES 18 BLOCS : le mien + les 17 scellés (lecture seule)
    ks = BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64)
    cs = BL.capstone.Cs(BL.capstone.CS_ARCH_X86, BL.capstone.CS_MODE_64)
    code, insns_par_bloc = {}, {}
    for bid, _sid, fichier, _famille in BL.BLOCS_LOUPE:
        rva, slot = L.SLOTS_LOUPE[bid]
        if bid == CAMPAGNE:
            chemin = os.path.join(UNITE, "notation", "loupe-13-recherche.asm")
        else:
            chemin = os.path.join(BL.ICI, "notation", fichier + ".asm")
        octets, metas = B4.assembler_bloc(ks, chemin, rva, slot)
        insns = B4.round_trip(cs, ks, chemin, rva, octets, metas)
        if len(insns) != len(metas):
            refus("ROUND-TRIP", f"{bid} : {len(insns)} != {len(metas)} "
                                f"instructions (R5)")
        if bid != CAMPAGNE and len(octets) != BL.MESURES_LOUPE[bid]:
            refus("MESURE-D161",
                  f"{bid} : {len(octets)} o != {BL.MESURES_LOUPE[bid]} o "
                  f"— la notation scellée a bougé ?")
        if slot - len(octets) < 16 or slot % 64:
            refus("SLOT-D8", f"{bid} : slot {slot:#x} (padding "
                             f"{slot - len(octets)} — multiple de 64, "
                             "padding >= 16)")
        code[bid] = octets
        insns_par_bloc[bid] = insns
    print(f"[assemblage] 18/18 notations : round-trip R5 vert — 17 scellées "
          f"aux mesures d'arrêt (D161 tenu) + loupe-13 de campagne "
          f"{len(code[CAMPAGNE])} o (LA mesure de la pièce)")

    # 3. LES VERROUS STRUCTURELS (le réseau des specs, l'ABI msx64)
    verrous = BL.oracle_structurel(code, insns_par_bloc)
    verrous += BL.audit_msx64(insns_par_bloc)

    # 4. LES HÉRITAGES SCELLÉS (R7 — la double preuve)
    m9, m1, demo = BL._lire_scelles()
    extraits = BL.heritage_scelle(m9, m1, demo, ks)

    # 5. L'IMAGE + LE PE (le plan, source unique)
    sections = BL.composer_image(code, extraits)
    exe = BL.ecrire_pe32plus(*sections[:4])
    BL.valider_pe(exe, code, extraits, sections[4], sections[5])

    # 6. L'ÉCRITURE AU DOSSIER DE CAMPAGNE (jamais au scellé)
    sortie = os.path.join(UNITE, "piece")
    os.makedirs(sortie, exist_ok=True)
    chemin_exe = os.path.join(sortie, "loupe.exe")
    with open(chemin_exe, "wb") as f:
        f.write(exe)
    sha = hashlib.sha256(exe).hexdigest()

    # LE DIFFÉRENTIEL contre le scellé : la pièce ne diffère QUE au slot
    # loupe-13 (le code + le padding) et à la porte R10 — l'écart CONFINÉ,
    # nommé (le miroir dev.6 de la lignée)
    scelle = open(os.path.join(BL.ICI, "loupe.exe"), "rb").read()
    if len(exe) != len(scelle):
        refus("TAILLE", f"la pièce {len(exe)} o != le scellé {len(scelle)} o")
    plages, courant = [], None
    for i, (a, b) in enumerate(zip(exe, scelle)):
        if a != b:
            if courant is None:
                courant = [i, i]
            else:
                courant[1] = i
        elif courant is not None:
            plages.append(tuple(courant))
            courant = None
    if courant is not None:
        plages.append(tuple(courant))
    z_slot = plages_raw(exe, rva13, slot13)
    z_r10 = plages_raw(exe, L.R_TAB_SUM, len(sections[5]))
    zones = [z_slot, z_r10]
    hors = [p for p in plages
            if not any(z[0] <= p[0] and p[1] < z[1] for z in zones)]
    if hors:
        refus("ÉCART-HORS-SLOT",
              f"la pièce diffère du scellé hors du slot loupe-13 et de la "
              f"porte R10 : {[(hex(a), hex(b)) for a, b in hors]}")
    n_oct = sum(p[1] - p[0] + 1 for p in plages)
    print(f"[différentiel] {len(plages)} plage(s) modifiée(s) ({n_oct} o en "
          f"tout), TOUTES au slot loupe-13 [0x{z_slot[0]:x}, 0x{z_slot[1]:x}) "
          f"et à la porte R10 — l'écart CONFINÉ, nommé")

    with open(os.path.join(sortie, "MESURES-PIECE.txt"), "w",
              encoding="utf-8") as f:
        f.write("MESURES DE LA PIÈCE DE CAMPAGNE — l'unité 03 D210 "
                "(loupe-13 × T)\n"
                f"loupe-13 (notation de campagne) : {len(code[CAMPAGNE])} o "
                f"de code, slot {slot13:#x} ({slot13} o), padding "
                f"{slot13 - len(code[CAMPAGNE])} o (NOP)\n"
                "les 17 scellées : == les mesures d'arrêt D161\n"
                f"loupe.exe : {len(exe)} o, sha256 {sha}\n"
                f"différentiel au scellé : {len(plages)} plages, {n_oct} o, "
                f"au slot loupe-13 et à la porte R10 seuls\n")
    print(f"[pièce] {chemin_exe} : {len(exe)} o, sha256 {sha}")
    print("=== LE BUILD DE CAMPAGNE VERT : la pièce recomposée du plan — "
          f"verrous {verrous}, l'écart au scellé confiné au slot loupe-13 ===")
    return 0


if __name__ == "__main__":
    sys.exit(construire())
