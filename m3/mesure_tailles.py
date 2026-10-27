#!/usr/bin/env python3
"""mesure_tailles.py — Mesure des tailles de code des brouillons M3 (jetable).

Assemble chaque brouillon à son RVA avec le point fixe d'étiquettes (même
logique qu'auteur.py) SANS contrainte de slot — pour arrêter le plan
d'adressage (layout.py) en connaissance de cause.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "outils"))

from keystone import Ks, KS_ARCH_X86, KS_MODE_64
import auteur

ks = Ks(KS_ARCH_X86, KS_MODE_64)

ICI = os.path.dirname(os.path.abspath(__file__))
BROUILLONS = os.path.join(ICI, "notation", "brouillons")

for fichier, bid, spec, rva, slot, deps in auteur.BLOCS:
    chemin = os.path.join(BROUILLONS, fichier + ".asm")
    instructions, etiquettes_lignes = auteur.lire_brouillon(chemin)
    etiquettes = {nom: rva + 0x800 for nom, _ in etiquettes_lignes}
    for _ in range(6):
        tailles, adresse = [], rva
        ok = True
        for ligne, _ in instructions:
            try:
                t = auteur.taille_ligne(ks, ligne, adresse, etiquettes, rva)
            except Exception:
                ok = False
                break
            tailles.append(t)
            adresse += t
        if not ok:
            print(f"[inassemblable] {fichier}")
            break
        nouvelles = {nom: rva + sum(tailles[:i]) for nom, i in etiquettes_lignes}
        if nouvelles == etiquettes:
            break
        etiquettes = nouvelles
    else:
        print(f"[pas de point fixe] {fichier}")
        continue
    total = sum(tailles)
    print(f"{fichier}: {total} o (slot actuel {slot:#x} → "
          f"{'OK' if total <= slot - 16 else 'DÉPASSE'}, "
          f"padding {slot - total})")
