# REGISTRE DES CIBLES — la seule autorité (D276, la vague 26)

Une ligne par cible. Aucune cible n'est re-tirée ni ajustée ici : les verdicts sont PORTÉS
tels qu'ils ont été publiés. Toute pièce qui énonce un verdict de cible le prend d'ici ; la
classe C25 refuse tout écart.

| id | sujet exact | périmètre de mesure | cible | mesuré | verdict | décision | campagne |
|----|-------------|---------------------|-------|--------|---------|----------|----------|
| CIB-ADD-COUT-4500 | coût tokens d'UN changement « ajouter » validé | budget `usage` natif, n=18, graine 20261117, ordre jamais re-tiré | ≤ 4 500 tokens | 4 604 (médiane) | MANQUÉE (de 104) | D248/D264 | 5ᵉ campagne add |
| CIB-ADD-FAISAB | faisabilité d'un « ajouter » épinglé | mêmes 18 tâches, juge inchangé | ≥ 15/18 verts | 5/18 | MANQUÉE | D248 | 5ᵉ campagne add |
| CIB-ADD-STRUC | faisabilité d'un « ajouter » épinglé, décodage contraint | schema JSON fermé, boucle de réparation ≤ 3 tours | ≥ 15/18 | — | EN ATTENTE (SERVING-ABSENT — la sonde du 26/11 : le bord accepte response_format et n'applique pas le schéma ; le harnais est prêt, atelier-w27decco) | D264 | D264 |
| CIB-ADD-RATIO | ratio ajouter/éditer | 2 200 / 674 tokens médians | ≤ 3,0 | 3,264 | MANQUÉE (de 0,264) | D31/D34 | campagne ratio |
| CIB-EDIT-BUDGET | coût tokens d'UN changement « éditer » validé | budget `usage` natif | ≤ 3 000 | 674 (adopté, TPL-EDIT-v1 OPT-14) | TENUE | D31/D34 | campagne ratio |
| CIB-LOC-BUDGET | coût tokens d'UNE localisation | budget `usage` natif | ≤ 64 | 51 M1 (HISTORIQUE-DATÉ) vs 627 adopté / 1 053 pointeur-seul | TENUE (HISTORIQUE-DATÉ) | D31/D34 | M1 |
| CIB-ORACLE-T | temps du moteur d'oracle natif | T < 10 s, n ≥ 5, graine, chronomètre monotone | T < 10 s | 0,266 s (médiane n=5, la session des 235 vecteurs, graine 20261124) | TENUE (vague 27, atelier-w27vaes : mmap 0xC000 re-prouvé, la classification 235/235 == jumeau, le digeste 81/81) | D264 | ATT-ORACLE |
| CIB-HARNAIS-200 | vecteurs d'oracle exécutables | 235 exécutables sur 320 produits | ≥ 200/235 | 95/235 | MANQUÉE | D273 | harnais générique (delta nul) |
| CIB-AES-105 | AES-GCM, couloir VAES/VPCLMULQDQ | 4 Kio, cœur épinglé, n=20, ratio contre OpenSSL EVP au même volume | ≤ 1,05 × EVP | 5,66 × EVP (4 463 ns vs 787 ns médianes, VM fréquence non goupillée — le caveat nommé ; la décomposition à l'atelier) | MANQUÉE (vague 27 : porte verte d'abord — 20/20 CAVP, mutant refusé, round-trip VERT ; jamais re-tirée) | D273 | couloir VAES |
| CIB-AES-ENTRELACE | AES-GCM, couloir CTR×GHASH ENTRELACÉ (AVX2/AES-NI) — **hors sujet de CIB-AES-105** | 4 Kio, cœur épinglé, n=20 | (aucune cible propre) | 0,7271 c/B ; 2 978,2 cycles ; 1,26 × EVP | HORS SUJET (mesuré, sans cible relative) | D273 | couloir entrelacé |
| CIB-DIFF-PLANCHER | plancher irréductible d'UN diff réel | diff réel 27,5 tokens | (plancher, pas une cible) | 24,5 × le diff | REPÈRE | D275 | campagne tokens |

## Les ères des budgets — la colonne périmètre rendue visible (vague 27)

Un verdict TENUE cite la mesure du périmètre courant ou porte l'étiquette HISTORIQUE-DATÉ.
Les ères, côte à côte (D222/D241/D251 — les canons de la table canonique des budgets) :

| opération | ère M1 (historique, datée) | pointeur-seul | contenu seul | ADOPTÉ (périmètre courant) |
|-----------|-----------------------------|---------------|--------------|-----------------------------|
| localiser | 51 | 1 053 | 580 | 627 (hiérarchique, D222) |
| éditer | 719 | — | 2 143 | 674 (TPL-EDIT-v1, OPT-14) |
| ajouter | 1 088 | — | 3 510 | 2 200 (squelette, OPT-14) |

La cible de CIB-LOC-BUDGET (≤ 64) fut posée à l'ère M1 : sa mesure TENUE (51) est celle de
cette ère, étiquetée HISTORIQUE-DATÉ ; le périmètre courant mesure 627 (le pointeur-seul
valut 1 053 avant le localiser-hiérarchique). CIB-EDIT-BUDGET tient sur la mesure ADOPTÉE
(674) : aucune étiquette ne s'impose.

## Décisions de lecture

- **Le sujet de CIB-AES-105 est le couloir VAES à écrire**, pas le couloir entrelacé : celui-ci
  est MESURÉ (1,26 × EVP) et ne porte aucune cible relative. Son verdict contre 1,05 × n'est donc
  pas « manqué » — il est **hors sujet**, et le dire ainsi n'est pas une indulgence : la cible a
  été pré-enregistrée pour une autre pièce de code.
- **Les trois cibles « ajouter » ne sont pas contradictoires, elles sont à trois étages** : le
  budget de l'opération (CIB-ADD-COUT-4500, la campagne qui a tourné), la faisabilité
  (CIB-ADD-FAISAB), et la faisabilité sous décodage contraint (CIB-ADD-STRUC, jamais exécutée).
  Aucune ne remplace l'autre ; une seule est mesurée.
- **CIB-HARNAIS-200** reste la cible du harnais par bloc : le contexte générique l'a manquée
  (95 < 200), la cause est nommée (carte d'adresses absente).
