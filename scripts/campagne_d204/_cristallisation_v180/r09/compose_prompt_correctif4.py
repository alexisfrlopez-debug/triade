#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif4.py — le tour chirurgical : UN écart (D23)."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

prompt = """Tu es l'auteur du domaine Loupe au laboratoire TRIADE. Ton quatrième
brouillon du bloc loupe-01 · ouvrir (ci-dessous) ne porte PLUS QU'UN SEUL
écart — mais il est FATAL (toutes les ouvertures échoueraient) :

D23 — « mov r12, rcx » est TOUJOURS APRÈS « call LOUPE04 » (l'écart D21,
     déplacé mais pas réparé). loupe-04 UTILISE rcx (son appel à libc-07
     memset pose rcx = le cadre) : à ton « mov r12, rcx », le chemin est
     DÉJÀ ÉCRASÉ. L'ORDRE EXIGÉ, Trois LIGNES, dans cet ordre EXACT :

         mov r12, rcx
         call LOUPE04
         mov rcx, r12

     (le chemin sauvé en r12 D'ABORD ; le cadre posé ; le chemin REMIS en
     rcx pour l'appel CreateFileW qui vient). Ne change RIEN d'autre.

================================================================================
TON QUATRIÈME BROUILLON (un seul écart : D23 — trois lignes à réordonner)
================================================================================

"""

brouillon = pathlib.Path(UNITE, "brouillons", "loupe-01-ouvrir.asm").read_text(
    encoding="utf-8")

consigne = """

================================================================================
LA CONSIGNE : le brouillon complet, cinquième édition, D23 corrigé (les
trois lignes dans l'ordre exact ci-dessus), TOUT LE RESTE DEMEURE À
L'IDENTIQUE. Réponds par le BROUILLON SEUL. AUCUN texte avant ou après,
AUCUN bloc markdown.
"""

sortie = pathlib.Path(UNITE, "prompts", "correctif-4.txt")
sortie.write_text(prompt + brouillon + consigne, encoding="utf-8")
print(f"[prompt] {sortie} : {sortie.stat().st_size} o")
