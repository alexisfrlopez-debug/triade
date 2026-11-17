#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cristallisation_08_d210.py — LA CRISTALLISATION de la notation de
campagne loupe-08 (l'unité 02 D210 × bras T) : DIX rebuilds consécutifs
depuis le brouillon — la résolution auteur (le point fixe des
étiquettes) PUIS l'assemblage keystone — chaque rebuild BYTE-IDENTIQUE
(le cristal, la discipline D204/D210 : dix fois le même, la pièce
reproductible)."""
import hashlib
import os
import sys

REPO = "/home/z/my-project/triade/lab/repo2"
UNITE = os.path.join(REPO, "scripts", "campagne_d204", "unite-08-T-d210")
sys.path.insert(0, os.path.join(REPO, "loupe"))

import build_loupe as BL          # noqa: E402

import importlib.util as _ilu
_spec_l = _ilu.spec_from_file_location(
    "layout", os.path.join(REPO, "loupe", "layout.py"))
L = _ilu.module_from_spec(_spec_l)
sys.modules["layout"] = L
_spec_l.loader.exec_module(L)
_spec = _ilu.spec_from_file_location(
    "auteur_loupe_campagne",
    os.path.join(REPO, "loupe", "outils", "auteur.py"))
AUTEUR = _ilu.module_from_spec(_spec)
sys.modules["auteur_loupe_campagne"] = AUTEUR
_spec.loader.exec_module(AUTEUR)

AUTEUR.BROUILLONS = os.path.join(UNITE, "brouillons")
AUTEUR.SORTIE = os.path.join(UNITE, "notation")
rva, slot = L.SLOTS_LOUPE["i110008"]
deps = ("AUCUNE entrée IAT (la feuille pure — le miroir exact des "
        "feuilles tls13, charte § 9) ; la table hexa « 0123456789"
        "ABCDEF » du plan (I4 — R_HEX .rdata, lue par déplacement RIP)")
ks = BL.Ks(BL.KS_ARCH_X86, BL.KS_MODE_64)

empreintes = []
for tour in range(1, 11):
    total, n_ins, n_etq = AUTEUR.resoudre_bloc(
        ks, "loupe-08-ligne", "i110008", "loupe-08:R1", rva, slot, deps)
    octets, metas = BL.B4.assembler_bloc(
        ks, os.path.join(UNITE, "notation", "loupe-08-ligne.asm"),
        rva, slot)
    empreintes.append((hashlib.sha256(octets).hexdigest(),
                       hashlib.sha256(
                           open(os.path.join(UNITE, "notation",
                                             "loupe-08-ligne.asm"),
                                "rb").read()).hexdigest(), len(octets)))
    print(f"[cristal {tour:2d}] {len(octets)} o, code sha256 "
          f"{empreintes[-1][0][:16]}…, notation {empreintes[-1][1][:16]}…")

tous = all(e == empreintes[0] for e in empreintes[1:])
print(f"[cristallisation] {'VERT — 10/10 BYTE-IDENTIQUES' if tous else 'ROUGE — divergence'} "
      f"({empreintes[0][2]} o, cristal sha256 {empreintes[0][0]})")
sys.exit(0 if tous else 1)
