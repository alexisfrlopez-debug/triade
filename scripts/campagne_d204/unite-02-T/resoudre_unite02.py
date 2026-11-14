#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resoudre_unite02.py — LA RÉSOLUTION AUTEUR de la notation de campagne
loupe-02 (l'unité 2 × bras T) : le brouillon de la main → la notation
explicite (keystone assemble, l'arithmétique d'adresses à l'outil — le même
partage que l'unité 1)."""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))   # .../work/triade
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-02-T")
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
    sys.modules["layout"] = _sys_layout

AUTEUR.BROUILLONS = os.path.join(UNITE, "brouillons")
AUTEUR.SORTIE = os.path.join(UNITE, "notation")
rva02, slot02 = L.SLOTS_LOUPE["i110002"]
deps02 = ("IAT kernel32 : SetFilePointerEx, ReadFile, GetLastError — la "
          "liste fermée du bloc (D161) ; AUCUN appelé (lire ne déplace "
          "rien — Q3, le défilement est à loupe-11)")
ks = BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64)
total, n_ins, n_etq = AUTEUR.resoudre_bloc(
    ks, "loupe-02-lire", "i110002", "loupe-02:R1", rva02, slot02, deps02)
print(f"[auteur] loupe-02 de campagne résolu : {total} o, {n_ins} "
      f"instructions, {n_etq} étiquettes, {slot02 - total} o de padding "
      f"(slot {slot02:#x})")
