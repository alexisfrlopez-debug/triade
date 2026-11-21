# PLAN GELÉ — 5NWNWOCEO (la vague 13)
> TPL-ADD-v3 : fermer le gap de format SANS retirer de contrôle, mesurer le coût PAR
> CHANGEMENT VALIDÉ, étendre le protocole à éditer.
> Gelé AVANT toute mesure ; la graine de l'ordre jamais re-tirée.

## Le mandat
Le gap de la vague 12 a déplacé vers la validité de l'écriture machine (7 HORS-FORMAT,
3 ID-INCONNU, 3 EXPANSION-DIVERGENTE). Fermer par la grammaire et la boucle de
réparation, jamais par la relaxation d'un contrôle :

1. **La grammaire publiée** : TPL-ADD-GRAMMAIRE-v1 (EBNF du squelette : définition
   d'étiquette, ligne d'instruction, ligne ID, opérandes — registres, immédiats,
   adresses, IDs), sha256 gravée au matériau et recoupée ; les VALIDATEURS DE FORMES
   au client (le levier nommé par OPT-15) : cmp mémoire-à-mémoire proscrit, movzx
   r64/r64 proscrit, désalignement de taille proscrit, symboles en clair proscrits
   (IDs seuls). Le CLI z-ai n'expose pas de décodage contraint → **la boucle client
   « assemble→refus nommé→réparation ciblée »**, budget de reprises **plafonné à 3**
   (consigné par tentative au JSONL), la réparation porte le REFUS NOMMÉ et la ligne
   fautive.
2. **Le gabarit du domaine dans le squelette** : les étiquettes LBL et constantes CST
   admissibles (dérivées de la couche I et de la carte, le DICT-DOMAINE-v1 reconduit)
   fournis AU MODÈLE dans le squelette même ; l'agent n'émet QUE le delta non
   dérivable (le client dérive cadre ABI, shadow space, signature, ancres).
3. **La mesure aux 18 tâches** (l'ordre de verites-terrain.json, graine 20261117,
  jamais re-tiré) : faisabilité première passe, faisabilité après reprises, coût
   bout-en-bout PAR CHANGEMENT VALIDÉ (tentatives refusées incluses), au tokenizer
   natif LU DU CHAMP USAGE, cl100k en parallèle. **Cible pré-enregistrée
   falsifiable : faisabilité après reprises ≥ 17/18 (94,4 % — 18/18 seul atteint le
   seuil 95 %) ET coût médian par changement validé ≤ 4 500 natifs** ; si manquée,
   le gap résiduel nommé par classe de refus, JAMAIS re-tiré.
4. **L'extension à éditer** : la même boucle sur les 18 tâches d'édition
   (taches-edition.json), le refus CONTEXTE-DIVERGENT de loupe-07-cumul demeurant au
   registre ; la table canonique des budgets adoptés PUBLIÉE (localiser 627
   hiérarchique / éditer 674 TPL-EDIT-v1 / ajouter 2 200 squelette AVEC faisabilité
   3/18 AU MÊME RANG — les statuts vague 13 ajoutés à côté), chaque valeur portant
   ID de décision, périmètre et statut (adopté/mesuré/historique).

## Les gestes
1. Ce plan gelé AVANT toute mesure.
2. Atelier atelier-ajouter-v3-5nwnwoceo/ : client_v3.py (grammaire + validateurs +
   boucle de reprise + quatre refus reconduits), campagne_v3.py (18 ajouter + 18
   éditer, journal par tentative), les JSONL bruts (usage, verdicts, réponses API).
3. Les contrôles négatifs AVANT campagne : un octet muté au cadre → refus nommé
   exigé ; chaque refus re-roulé (ID-INCONNU, DICT-DIVERGENT, EXPANSION-DIVERGENTE,
   HORS-FORMAT, GABARIT-DIVERGENT, CONTEXTE-DIVERGENT).
4. La table canonique des budgets portée au manuscrit v0.23.0 et au dashboard de la
   spec (le geste de ylrzmlbn8).

## La vérification après modifications
- re-tokenisation indépendante des valeurs citées (écart ≤ 1 token) ; le coût par
  changement validé RECALCULÉ du JSONL brut par le linter ;
- round-trip 100 % et garde sha256 de fenêtre re-vérifiées sur CHAQUE bloc accepté ;
  les quatre refus fail-closed du pointeur demeurés ;
- sceau 14/14 avant et après ; les refus honnêtes AU REGISTRE, jamais re-tirés en
  silence ; la décision d'adoption append-only.

## Les refus
Aucun contrôle retiré ; aucun vert obtenu par relaxation ; la variation au modèle
consignée telle quelle ; les réponses brutes archivées (garde-brut), les prompts
archivés en texte (garde-prompts — le retour de la convention v1).
