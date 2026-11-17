#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resoudre_loupe08_d210.py — LA RÉSOLUTION AUTEUR de la notation de
campagne loupe-08 (l'unité 02 D210 × bras T) : le brouillon symbolique
de la main → la notation explicite (keystone assemble, l'arithmétique
d'adresses à l'outil — le même partage que l'unité 1, resoudre_unite02.py)."""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
if not os.path.basename(REPO) == "triade":
    REPO = "/home/z/my-project/triade/lab/repo2"
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-08-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import build_loupe as BL          # noqa: E402

import importlib.util as _ilu
_sys_layout = sys.modules.get("layout")
_spec_l = _ilu.spec_from_file_location(
    "layout", os.path.join(REPO, "loupe", "layout.py"))
L = _ilu.module_from_spec(_spec_l)
sys.modules["layout"] = L
_spec_l.loader.exec_module(L)
_spec = _ilu.spec_from_file_location(
    "auteur_loupe_campagne", os.path.join(REPO, "loupe", "outils", "auteur.py"))
AUTEUR = _ilu.module_from_spec(_spec)
sys.modules["auteur_loupe_campagne"] = AUTEUR
_spec.loader.exec_module(AUTEUR)
if _sys_layout is not None:
    sys.modules["layout"] = _sys_layout   # le monde tel qu'il était

AUTEUR.BROUILLONS = os.path.join(UNITE, "brouillons")
AUTEUR.SORTIE = os.path.join(UNITE, "notation")
rva08, slot08 = L.SLOTS_LOUPE["i110008"]
deps08 = ("AUCUNE entrée IAT (la feuille pure — le miroir exact des "
          "feuilles tls13, charte § 9) ; la table hexa « 0123456789"
          "ABCDEF » du plan (I4 — R_HEX .rdata, lue par déplacement "
          "RIP)")
ks = BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64)
total, n_ins, n_etq = AUTEUR.resoudre_bloc(
    ks, "loupe-08-ligne", "i110008", "loupe-08:R1", rva08, slot08, deps08)
print(f"[auteur] loupe-08 de campagne résolu : {total} o, {n_ins} "
      f"instructions, {n_etq} étiquettes, {slot08 - total} o de padding "
      f"(slot {slot08:#x})")
