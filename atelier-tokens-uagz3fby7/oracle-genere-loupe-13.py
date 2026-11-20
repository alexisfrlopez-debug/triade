#!/usr/bin/env python3
# ORACLE GÉNÉRÉ PAR SCRIPT — loupe-13 (le compilateur d'oracle, la vague 9)
# LA SOURCE : loupe/I/loupe-13-recherche.md (le gabarit structuré — la forme machine du
# contrat I ; l'oracle est DÉRIVÉ DE I, jamais de B)
# LES VERDICTS NOMMÉS :
#   -5 : ENTRÉE (motif > 32 ou départ > taille)
#   -1 : FIN (l'absence — la plage épuisée)
# LE POST : Q1 la position de la PREMIÈRE occurrence ; Q2 l'absence -1 ; le motif plus long que la plage restante -1 IMMÉDIAT ; Q3 la plage vide -1 ; Q4 l'occurrence VRAIE
# LES VECTEURS : les 64 de la campagne v200 (la graine 20261120)


def oracle_loupe_13(fenetre, taille, motif, taille_motif, depart):
    """L'implémentation triviale, lente, sûre — LE JUGE."""
    for i in range(depart, taille - taille_motif + 1):
        if fenetre[i:i+taille_motif] == motif:
            return i
    return -1
