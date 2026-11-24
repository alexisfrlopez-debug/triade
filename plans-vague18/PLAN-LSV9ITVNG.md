# PLAN GELÉ — LSV9ITVNG — l'expansion sous contrainte de grammaire (campagne TPL-ADD v6)

## L'instruction, en une phrase
Remplacer l'expansion en texte libre de l'opération « ajouter » par une expansion
sous schéma structuré (opcode/opérande/offset), ajouter la boucle de réparation par
contre-exemple minimal (ddmin, ≤ 3 tours), pré-enregistrer la cible AVANT mesure,
mesurer sur les mêmes 18 tâches et la même graine, sans toucher aux juges.

## Pré-enregistrement (AVANT toute mesure — consigné ici, hashé au commit)
- cible de faisabilité : ≥ 15/18 verts sur la campagne v6 (la cible de la vague 15,
  manquée à 5/18) ;
- périmètre : 18 tâches TPL-ADD, graines consignées des campagnes v2–v5, juges
  (expansion, round-trip, oracle, mutation) INCHANGÉS ;
- métrique principale : verts/18 ; secondaire : médiane de tokens par changement
  validé (deux conventions nommées) ;
- lecture défavorable imposée si la cible est manquée.

## Ce qui sera livré
(a) l'instrument `expansion_structuree.py` : schéma opcode/opérande/offset, validation
à la génération, refus nommé HORS-SCHEMA ; (b) la boucle ddmin bornée à 3 tours ;
(c) l'autotest déterministe (schéma, ddmin, borne) ; (d) la campagne : EN ATTENTE
d'un serving qui expose le structured output (aucun chiffre fabriqué).

## Ce qui est interdit dans cet atelier
Toucher un juge ; re-tirer les graines ; annoncer un vert non mesuré ; modifier un
octet scellé.
