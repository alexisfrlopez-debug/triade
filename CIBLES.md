# REGISTRE DES CIBLES — la seule autorité (D276, la vague 26)

Une ligne par cible. Aucune cible n'est re-tirée ni ajustée ici : les verdicts sont PORTÉS
tels qu'ils ont été publiés. Toute pièce qui énonce un verdict de cible le prend d'ici ; la
classe C25 refuse tout écart.

| id | sujet exact | périmètre de mesure | cible | mesuré | verdict | décision | campagne |
|----|-------------|---------------------|-------|--------|---------|----------|----------|
| CIB-ADD-COUT-4500 | coût tokens d'UN changement « ajouter » validé | budget `usage` natif, n=18, graine 20261117, ordre jamais re-tiré | ≤ 4 500 tokens | 4 604 (médiane) | MANQUÉE (de 104) | D248/D264 | 5ᵉ campagne add |
| CIB-ADD-FAISAB | faisabilité d'un « ajouter » épinglé | mêmes 18 tâches, juge inchangé | ≥ 15/18 verts | 5/18 | MANQUÉE | D248 | 5ᵉ campagne add |
| CIB-ADD-STRUC | faisabilité d'un « ajouter » épinglé, décodage contraint | schema JSON fermé, boucle de réparation ≤ 3 tours | ≥ 15/18 | — | EN ATTENTE (aucun serving à structured output) | D264 | D264 |
| CIB-ADD-RATIO | ratio ajouter/éditer | 2 200 / 674 tokens médians | ≤ 3,0 | 3,264 | MANQUÉE (de 0,264) | D31/D34 | campagne ratio |
| CIB-EDIT-BUDGET | coût tokens d'UN changement « éditer » validé | budget `usage` natif | ≤ 3 000 | 674 | TENUE | D31/D34 | campagne ratio |
| CIB-LOC-BUDGET | coût tokens d'UNE localisation | budget `usage` natif | ≤ 64 | 51 | TENUE | D31/D34 | M1 |
| CIB-ORACLE-T | temps du moteur d'oracle natif | T < 10 s, n ≥ 5, graine, chronomètre monotone | T < 10 s | — | EN ATTENTE (mmap 0xC000 refusé : `vm.mmap_min_addr`) | D264 | ATT-ORACLE |
| CIB-HARNAIS-200 | vecteurs d'oracle exécutables | 235 exécutables sur 320 produits | ≥ 200/235 | 95/235 | MANQUÉE | D273 | harnais générique (delta nul) |
| CIB-AES-105 | AES-GCM, couloir VAES/VPCLMULQDQ | 4 Kio, cœur épinglé, n=20, ratio contre OpenSSL EVP au même volume | ≤ 1,05 × EVP | — | EN ATTENTE (aucun code VAES écrit) | D273 | couloir VAES |
| CIB-AES-ENTRELACE | AES-GCM, couloir CTR×GHASH ENTRELACÉ (AVX2/AES-NI) — **hors sujet de CIB-AES-105** | 4 Kio, cœur épinglé, n=20 | (aucune cible propre) | 0,7271 c/B ; 2 978,2 cycles ; 1,26 × EVP | HORS SUJET (mesuré, sans cible relative) | D273 | couloir entrelacé |
| CIB-DIFF-PLANCHER | plancher irréductible d'UN diff réel | diff réel 27,5 tokens | (plancher, pas une cible) | 24,5 × le diff | REPÈRE | D275 | campagne tokens |

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
