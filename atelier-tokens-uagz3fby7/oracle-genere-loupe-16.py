#!/usr/bin/env python3
# ORACLE GÉNÉRÉ PAR SCRIPT — loupe-16 (le compilateur d'oracle, la vague 9)
# LA SOURCE : loupe/I/loupe-16-saisie.md (le gabarit structuré — la forme machine du
# contrat I ; l'oracle est DÉRIVÉ DE I, jamais de B)
# LES VERDICTS NOMMÉS :
#   -4 : SESSION (sans session ouverte)
#   -3 : HORS-BORNES (la cellule fantôme / le journal plein — 256 DISTINCTS)
# LE POST : Q1 le premier chiffre (l'attente au nibble) ; Q2 l'octet au journal PAR DÉCALAGE (la réécriture REMPLACE) ; Q3 l'octet au tampon — visible immédiatement ; Q4 la marque sale ; Q5 VK_SUPPR à l'attente
# LES VECTEURS : les vecteurs_16 de la campagne (l'école et les bords)


def oracle_loupe_16(touche, journal, curseur, remplissage):
    """L'implémentation triviale, lente, sûre — LE JUGE."""
    if touche non hexa: ignorer (E4)
    if l'attente au premier nibble: stocker, attendre le second
    else: octet = (premier << 4) | second ; journal PAR DÉCALAGE ; la marque sale
