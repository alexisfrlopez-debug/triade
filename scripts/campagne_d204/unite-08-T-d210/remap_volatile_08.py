#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""remap_volatile_08.py — LE GESTE MÉCANIQUE DU LABO (l'unité loupe-08 ×
bras T, la campagne D210) : LA REMappe BIJECTIVE des registres de la
phase 1 vers LE PLAN VOLATIL. Le précédent consigné (la reprise de
l'atelier : « le lab re-pose l'equ et le prologue — le geste
mécanique ») : le lab ne corrige JAMAIS les fautes de fond (celles des
phases 3/4 demeurent à la rig), seulement les gestes mécaniques — la
présente remappe est BIJECTIVE (aucune sémantique changée) :
  r12 (curseur) → r8 (r8 jamais lu ailleurs après l'alias)
  r13 (longueur) → rdx (rdx jamais modifié)
  r14 (compteur) → r9d (r9 = le décalage d'appel, mort après « mov r10, r9 »)
  r15 (égratignure) → rax (le chantier)
  les deux lignes d'alias (mov r12, r8 / mov r13, rdx) DISPARAISSENT —
  l'alias n'est plus (l'élimination d'alias, mécanique).
"""
import pathlib
import re

ICI = pathlib.Path("/home/z/my-project/triade/lab/atelier-d210-p39uklsca")
src = (ICI / "bras-T" / "loupe-08-it6.asm").read_text(encoding="utf-8")

# la zone : de l'initialisation à la fin de la phase 2 (les deux espaces)
debut = src.index("    ; --- Initialisation des registres et pointeurs ---")
fin = src.index("    ; --- Écriture des 16 groupes hexadécimaux")
zone = src[debut:fin]

# ① l'élimination des alias (les lignes mov r12, r8 / mov r13, rdx)
zone = re.sub(r"^\s*mov r12, r8.*\n", "", zone, flags=re.M)
zone = re.sub(r"^\s*mov r13, rdx.*\n", "", zone, flags=re.M)
zone = re.sub(r"^\s*xor rax, rax.*\n", "", zone, flags=re.M)  # le chantier s'initialise

# ② la remappe bijective (ordre : r15 d'abord — jamais ne collide)
zone = zone.replace("r15", "rax_").replace("r14", "r9d_")
zone = zone.replace("r12", "r8").replace("r13", "rdx")
zone = zone.replace("rax_", "rax").replace("r9d_", "r9d")

# ③ la re-forme : le compteur en r9d (l'écriture 64 bits « mov r9d, 8 »)
zone = zone.replace("mov rax, 8", "mov r9d, 8").replace("dec rax", "dec r9d")
# (les compteurs vivaient en r14 → r9d_ → déjà r9d)

# l'en-tête du geste, visible à la pièce
zone = ("    ; --- le plan volatile : rcx la source, rdx la longueur, "
        "r8 le curseur, r10 le décalage, r11 la table, rax/r9 le chantier ---\n"
        + zone)

(ICI / "bras-T" / "loupe-08-it6b.asm").write_text(
    src[:debut] + zone + src[fin:], encoding="utf-8")
print("[remap] it6b écrit — la phase 1+2 remappée au plan volatile "
      "(le geste mécanique du labo, bijectif, nommé)")
