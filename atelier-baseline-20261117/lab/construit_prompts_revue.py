#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construit les prompts de revue des pièces corrigées (bras T et C)."""
import pathlib

ATELIER = pathlib.Path("/home/z/my-project/triade/atelier-baseline-20261117")

# --- bras T ---
demande_t = """Tu es le réviseur d'un bloc de code machine selon le protocole
TRIADE (l'ABI msx64, l'héritage PAR LA CARTE des blocs scellés tls13).
Voici la notation de loupe-05 APRÈS la boucle corrective de l'épreuve
d'exécution V1-V5 : les cinq défauts nommés D-T1 (la signature de
tls13-04 : rdx posé au créneau), D-T2 (l'absorption au TAMPON_CUMUL par
le courrier rbp), D-T3 (le vide par la composition init+final, le
littéral supprimé), D-T4 (la copie depuis le créneau), D-T5 (le cadre
0xe0, la sauvegarde de rdi/rsi) — puis le tour 11 (le courrier rbp
manquant). L'épreuve rejouée par le harnais : V1, V2, V3, V4, V5 et I5
tous VERT contre hashlib (la graine 20261117).

Revu la conformité AU CONTRAT, clause par clause (P1-P4, Q1-Q4, I1-I5,
E1-E4) : cite l'instruction à l'appui pour chaque clause, nomme les
écarts éventuels, conclus par « Verdict : CONFORME » ou « Verdict :
ÉCART ». Rien d'autre.

=== LA NOTATION (loupe-05-it10.asm, 394 octets cristallisés) ===

"""
piece_t = (ATELIER / "bras-T" / "loupe-05-it10.asm").read_text(encoding="utf-8")
(ATELIER / "bras-T" / "prompt-revue-reprise.txt").write_text(
    demande_t + piece_t, encoding="utf-8")

# --- bras C ---
demande_c = """Tu es le réviseur d'un code C selon le protocole TRIADE (gcc
-O2 -std=c11 contre le shim windows.h du labo). Voici la pièce du bras C
de loupe-05 APRÈS le correctif D-C1 de l'épreuve d'exécution V1-V5 (les
huit affectations inversées : la longueur en GRAND-boutiste au bloc
final). L'épreuve rejouée : V1, V2, V3, V4, V5 tous VERT contre hashlib
(la graine 20261117, le juge externe).

NOTE D'ARBITRAGE (le précédent nommé à la consignation de la baseline) :
les invariants I1/I2 (l'héritage PAR LA CARTE des blocs scellés tls13)
sont ARBITRÉS pour le bras C — le bras C compile du C gcc, il ne lie pas
les blocs machine : la redéclaration des fonctions SHA au bras C est
l'écart NOMMÉ et ARBITRÉ par le précédent de la pièce C scellée de
l'unité 3 — ne le compte pas comme écart nouveau.

Revu la conformité AU CONTRAT, clause par clause (P1-P4, Q1-Q4, E1-E4,
I3-I5) : cite la ligne à l'appui, nomme les écarts éventuels, conclus
par « Verdict : CONFORME » ou « Verdict : ÉCART ». Rien d'autre.

=== LA PIÈCE (loupe-05-it4.c) ===

"""
piece_c = (ATELIER / "bras-C" / "loupe-05-it4.c").read_text(encoding="utf-8")
(ATELIER / "bras-C" / "prompt-revue-reprise.txt").write_text(
    demande_c + piece_c, encoding="utf-8")

print("prompts écrits :",
      ATELIER / "bras-T" / "prompt-revue-reprise.txt",
      ATELIER / "bras-C" / "prompt-revue-reprise.txt")
