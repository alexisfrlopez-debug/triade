#!/usr/bin/env python3
# ORACLE GÉNÉRÉ PAR SCRIPT — loupe-02 (le compilateur d'oracle, la vague 9)
# LA SOURCE : loupe/I/loupe-02-lire.md (le gabarit structuré — la forme machine du
# contrat I ; l'oracle est DÉRIVÉ DE I, jamais de B)
# LES VERDICTS NOMMÉS :
#   -5 : ENTRÉE (le décalage non multiple de 16)
#   -3 : HORS-BORNES (le décalage ≥ la taille)
# LE POST : Q1 remplissage = min(384, taille − décalage), la fenêtre lue ; Q2 LE RECOUVREMENT du journal (l'octet écrit replace) ; Q3 rax = 0
# LES VECTEURS : les vecteurs_02 de la campagne (la graine 20261115)


def oracle_loupe_02(decalage, taille_fichier, journal):
    """L'implémentation triviale, lente, sûre — LE JUGE."""
    remplissage = min(384, taille_fichier - decalage)
    fenetre = fichier[decalage:decalage+remplissage]
    for (dec, oct) in journal:
        if decalage <= dec < decalage + remplissage:
            fenetre[dec - decalage] = oct
