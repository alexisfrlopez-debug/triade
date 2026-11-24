# PLAN GELÉ — W20ORAC (vecteurs d'oracle des 50 blocs depuis la couche I)

> Prompt 2 de l'évaluation v0.26.0. R5 : l'oracle DÉRIVE de I, jamais de B. Aucun
> contrôle retiré ; aucun chiffre natif fabriqué dans le bac.

## Périmètre
1. `scripts/vague20/vecteurs_oracle_50.py` : pour chacun des 50 blocs résolus (exclus
   c30012 et c30014), dériver depuis la spécification I du bloc : vecteurs dorés (entrées
   et sorties attendues dérivées du contrat), propriétés différentielles contraintes par
   les pré-conditions, tests de rejet pour chaque cas d'échec nommé.
2. Audit de traçabilité : chaque exigence numérotée du contrat relie ≥ 1 vecteur ; aucun
   vecteur orphelin, aucune exigence sans vecteur (fail-closed).
3. Pré-enregistrement de la mesure native (T < 10 s, commandes fixes, chronomètre
   monotone, n ≥ 5, graine, agrégateur fail-closed) — hashé avant toute mesure.

## Contraintes
- Le natif exige mmap 0xC000 (refusé ici, vm.mmap_min_addr=65536) : la mesure native est
  un geste machine réelle ; le bac ne publie aucun temps natif.
- Les vecteurs dérivés de I ne peuvent pas être « mesurés » sur un moteur natif ici : ils
  sont produits, recomposés et recoupés (jumeau Unicorn), et le statut reste EN ATTENTE.

## Critères d'acceptation
- 50/50 blocs portent leurs vecteurs ; 2 exclus nommés.
- Audit 1-sur-10 rejoué (6/6), consoles du jumeau ligne-identiques, mémo 4/4.
- Aucun vecteur orphelin ; chaque échec nommé a son test de rejet.
- Pré-enregistrement hashé consigné avant mesure ; statut EN ATTENTE nommé.
