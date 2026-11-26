# PLAN GELÉ — W29EXPANDEUR (le durcissement de la TCB de l'expandeur client)

> Vague 29, prompt 4 (dépôt du 27/11/2026, instructions.txt §10 Prompt 4 — suggestion
> C9 de l'évaluation). Le validateur client d'OPT-16 (l'expansion de la substitution à
> l'offset, la confrontation du diff exact, le round-trip keystone→capstone→keystone)
> est la TCB du chemin token-plancher. Le durcir SANS toucher au juge D264
> (scripts/vague19/expandeur_add.py sha256 9fc325e2… INTACT — JUGE-MODIFIÉ refusé).
> Le présent plan gèle l'atelier AVANT toute mesure.

## Geste
1. LE SECOND EXPANDEUR INDÉPENDANT : une implémentation DISTINCTE (une seconde
   écriture, un chemin de code différent — l'expansion par reconstruction ligne à
   ligne au triple-canal [keystone, capstone, diff ligne-à-ligne] au lieu du canal
   unique), le MÊME schéma fermé D264/OPT-16 (éditer : substituer à l'offset). La
   confrontation octet pour octet au premier expandeur sur : (a) CHAQUE diff de
   campagne (journal-opt16.jsonl rejoué — les 39 appels, les 18 tâches) ; (b) une
   BATTERIE GÉNÉRATIVE : ≥ 10 000 diffs valides et invalides, la graine consignée
   AVANT le tirage (graine 20261128), chaque classe de refus couverte (l'offset hors
   plage, la ligne vide, la clé hors schéma, l'op hors enum, la ligne mutée à
   l'octet, le diff multi-lignes, HORS-FORMAT la prose).
2. LA BATTERIE DE MUTATION DE L'EXPANDEUR LUI-MÊME : ≥ 64 mutants d'un octet du
   premier expandeur (le fichier du validateur client d'OPT-16, atelier-w28opt16/
   campagne_opt16.py — la cible : les zones de décision : les bornes, l'enum, la
   confrontation, l'offset), chacun TUÉ par la confrontation croisée (le second
   expandeur rend un verdict divergent) ou par le round-trip — un survivant est NOMMÉ
   avec sa cause (un survivant demeure un survivant, jamais maquillé).
3. LE LEMME DE SUBSTITUTION vérifié MÉCANIQUEMENT : l'offset borné à la plage du
   bloc, EXACTEMENT la ligne attendue remplacée, AUCUNE autre ligne changée —
   l'énumération bornée (l'objet énuméré : les lignes du bloc, l'offset, la src —
   chaque cas contrôlé par les deux expandeurs + le round-trip) ; le contrôle
   négatif : une substitution hors lemme attrapée (l'offset à ±1 de la plage, la
   ligne substituée à l'index voisin — le diff doit nommer la ligne EXACTE).
4. LA CONSIGNATION : les refus par classe, la couverture de la batterie (chaque
   classe nommée avec son compte), le taux des mutants tués ; l'écart zéro attendu
   entre les deux expandeurs sur les diffs honnêtes (tout écart NOMMÉ avec sa
   pièce).
5. LE REJEU bit-identique de la batterie (deux passes, la graine consignée) ; le
   journal jsonl de la confrontation.

## Critères d'acceptation
- Le juge D264 recoupé INTACT avant et après (9fc325e2…) ; sceau_I 14/14 avant et
  après.
- Zéro divergence entre les deux expandeurs sur les diffs honnêtes (ou l'écart nommé
  avec sa cause) ; chaque mutant tué ou nommé.
- La porte 32 classes zéro rouge (la chaîne existante) ; les refus nommés consignés
  par classe ; aucun chiffre fabriqué.
