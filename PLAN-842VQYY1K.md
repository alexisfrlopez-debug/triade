# PLAN GELÉ — 842VQYY1K (la vague 14)
> L'atelier pré-enregistré de fermeture du gap de faisabilité AJOUTER : quatre
> leviers cumulables contre 6/18 (refus EXPANSION-DIVERGENTE ×9, HORS-FORMAT ×2,
> ID-INCONNU ×1), sans affaiblir aucun juge.
> Graines 20261117 reconduites, ordre JAMAIS re-tiré, budget reprises plafonné 3
> consigné par tentative au JSONL. Gelé AVANT toute mesure.

## Le mandat
Objectif : fermer le gap AJOUTER sans affaiblir un seul juge. Quatre leviers,
chacun mesuré isolément puis composés :
(1) **CONTRAINTE DE GRAMMAIRE AU DÉCODAGE** : la grammaire TPL-ADD-GRAMMAIRE-v1
impose la forme à l'échantillonnage (masque de logits ou schéma de sortie
structurée côté client), pas seulement en validation post-hoc — l'instrument est
sondé (response_format côté service) et l'écart éventuel NOMMÉ au registre ;
(2) **SQUELETTE À TROUS TYPÉS** : l'agent émet le squelette avec trous typés
(registre, offset, cible), chaque trou rempli par un patch court validé
LOCALEMENT (assemble + round-trip du fragment) AVANT composition ;
(3) **RÉPARATION GUIDÉE PAR CONTRE-EXEMPLE** : au refus EXPANSION-DIVERGENTE,
rendre au prompt le diff exact attendu/obtenu (octets, instruction, opérande) et
la ligne fautive, plus UN exemplaire canonique du motif fautif corrigé ;
(4) **EXEMPLAIRE PAR PROCHE CONTRAT** : récupérer dans la carte le bloc scellé au
contrat le plus proche de la tâche et l'injecter comme few-shot (référence
littérale, jamais de calcul).

## La mesure
Aux 18 mêmes tâches AJOUTER (graine 20261117, ordre jamais re-tiré) : faisabilité
première passe et après reprises, coût médian PAR TENTATIVE et PAR CHANGEMENT
VALIDÉ (les deux publiés côte à côte), tokenizer natif au champ usage + cl100k
parallèle, re-tokenisation indépendante ±1. **Cibles pré-enregistrées : AJOUTER
≥15/18 ET ≤4 500 natifs par changement validé ; ÉDITER 18/18 maintenu.**

## L'extension ÉDITER
Format diff structuré ancré par lignes (l'agent n'émet que lignes changées +
ancres ; le client applique, recompose, round-trip) — cible médiane ≤300 natifs,
plancher 27,5 nommé.

## Les contrôles
Aucun artefact scellé touché ; les refus honnêtes au registre append-only, jamais
re-tirés ; toute perte d'instrument (429, timeout) nommée et re-exécutée sans
re-tirer les tâches consignées.

## La vérification après modifications
Re-tokenisation indépendante journal vs garde-brut (écart max 0) ; round-trip
re-vérifié sur CHAQUE bloc accepté depuis les réponses archivées ; les faces
négatives re-roulées (octet muté au cadre REFUSÉ au premier nom, validateurs de
forme, quatre refus v2) ; rejeu bit-identique à la graine ; comparer v3→v4 par
classe de refus (le déplacement du gap nommé, jamais masqué) ; consigner la
décision et la table canonique des budgets avec ID, périmètre, statut.

## Les refus
Jamais une tâche re-tirée ; jamais un juge affaibli ; jamais un refus converti
hors boucle consignée ; jamais un coût deviné (le log fait foi).
