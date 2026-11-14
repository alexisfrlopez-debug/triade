#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compose_prompt_correctif6.py — le correctif-6 de la phase source-c
(bras C) : la table S du MD5 est TRANSPOSÉE (chaque rangée concatène les
quatre groupes au lieu de répéter UN groupe — la ronde 1 lirait les
rotations des rondes suivantes aux pas 4-15), et la portée de i au NUL
du chemin (déclaré DANS le for, invisible après lui — la compilation
même refuse)."""
import pathlib

UNITE = pathlib.Path(__file__).resolve().parent

prompt = """Tu es le même auteur du domaine Loupe au laboratoire TRIADE — le bras C de
la campagne D204. L'épreuve du labo rend : SHA-256 66/66 VERT ; MD5 0/66.
L'audit nomme DEUX défauts — dont la racine du MD5.

================================================================================
L'AUDIT — LES DEUX DÉFAUTS NOMMÉS
================================================================================
D28 (LA TABLE S EST TRANSPOSÉE — la racine du MD5 faux) : la table livrée
    met les QUATRE groupes dans CHAQUE rangée :
        7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21,  ← FAUX
    or la ronde 1 (les pas 0-15) répète SON groupe quatre fois : les pas
    4-7 de la ronde 1 liraient 5, 9, 14, 20 (les rotations de la ronde
    2 !). LA TABLE JUSTE (RFC 1321 — chaque rangée RÉPÈTE son groupe) :
        ronde 1 (pas 0-15)   : 7, 12, 17, 22 × 4
        ronde 2 (pas 16-31)  : 5, 9, 14, 20 × 4
        ronde 3 (pas 32-47)  : 4, 11, 16, 23 × 4
        ronde 4 (pas 48-63)  : 6, 10, 15, 21 × 4
D29 (la portée de i — la compilation refuse) : la correction du NUL du
    chemin écrivit « ((uint16_t*)(cadre + 0))[i] = 0; » APRÈS la boucle
    « for (int i = 0; ...) » — le i déclaré DANS le for meurt AVEC lui
    (la portée C) : « 'i' undeclared ». Le compteur se déclare AVANT.

================================================================================
TON TRAVAIL (le correctif-6) — LE FORMAT PATCH
================================================================================
Réponds UNIQUEMENT par les remplacements, au format EXACT :

###REMPLACEMENTS
AVANT=<la ou les lignes fautives, copiées au caractère près>
APRÈS=<la ou les lignes corrigées>
###FIN REMPLACEMENTS

Les DEUX remplacements attendus :
1. LA TABLE S (D28) : les quatre lignes de valeurs de la table (de « 7,
   12, 17, 22, 5, 9, ... » à « 6, 10, 15, 21, 7, 12, ... ») → les
   quatre lignes de la table juste :
       7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
       5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
       4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
       6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
2. LE NUL DU CHEMIN (D29) : les trois lignes de la copie du chemin
   (le for, sa copie, le NUL) → le compteur déclaré avant la boucle :
       int i_chemin = 0;
       while (i_chemin < 259 && chemin_w[i_chemin] != L'\\0') {
           ((uint16_t*)(cadre + 0))[i_chemin] = (uint16_t)chemin_w[i_chemin];
           ++i_chemin;
       }
       ((uint16_t*)(cadre + 0))[i_chemin] = 0;

Aucun texte avant ###REMPLACEMENTS, aucun texte après ###FIN
REMPLACEMENTS.
"""

(UNITE / "prompts" / "correctif-6.txt").write_text(prompt, encoding="utf-8")
print(f"[composé] prompts/correctif-6.txt : {len(prompt.encode())} o")
