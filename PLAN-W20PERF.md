# PLAN GELÉ — W20PERF (couloirs performance et gardes spécialisées)

> Prompt 4 de l'évaluation v0.26.0. R11 (mesure avant/après au hot path identifié), R4
> (contrat stable), R7 (aucune adresse scellée ne bouge).

## Périmètre
1. `scripts/vague20/couloirs_perf.py` : le harnais pré-enregistré (cœur épinglé, fréquence
   mesurée, n ≥ 20, IQR, graine) et les trois couloirs demandés — AES-GCM (CPUID hissé,
   GHASH 8 blocs Karatsuba, entrelacement), recherche AVX2 à CPUID hissé (cible ≤ 561 c),
   spécialisation des 11 gardes (22→7 instructions/appel).
2. Si le silicium du bac ne porte pas VAES/VPCLMULQDQ, le couloir est REFUSÉ nommément
   (détection CPUID consignée), jamais simulé ; la recherche AVX2 est mesurée si AVX2
   présent, contre la variante scellée.

## Contraintes
- Aucune valeur antérieure modifiée ; les ratios publiés sont des MESURES du bac
  (machine virtuelle), nommées comme telles ; les cibles restent des cibles.
- Aucun octet scellé touché.

## Critères d'acceptation
- Empreintes des pièces scellées avant/après identiques.
- Chaque couloir : CPUID consigné, mesure ou refus nommé, IQR publié, ratios recomposés.
- Pré-enregistrement hashé AVANT mesure ; journal OPT consigné ; contrôle négatif attrapé.
