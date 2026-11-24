# PLAN GELÉ — W19METAL (kit métal de bascule concurrente, pré-enregistré, agrégateur fail-closed)

> Instruction source : Prompt 3 du message du maître du 24/11/2026 12:42. **Aucun résultat
> n'est fabriqué** : le kit part EN ATTENTE ; le statut « mesuré » n'est acquis qu'au
> recoupement sur pièces. Aucune machine réelle n'est atteinte depuis ce bac.

## Périmètre
1. `scripts/vague19/kit_metal_bascule.py` — le protocole pré-enregistré du run métal de la
   transaction D253 :
   - ≥ 2 machines : empreinte CPUID (vendor/family/model/stepping, drapeaux utiles : CMPXCHG16B),
     fréquence effective consignée PAR machine, cœur épinglé (`taskset`/affinité) ;
   - N ≥ 30 exécutions par configuration ;
   - injection d'interruption à chacun des SEPT états (0 à 6), et rollback exercé sous trafic
     depuis publication / invalidation / vérification ;
   - les CINQ aléas D261 exercés (thread créé pendant le rendez-vous, retour de pile dans la
     plage, rel32 hors portée ±2 GiB, slot de 16 octets non réservé, verrou détenu).
2. `scripts/vague19/agregeur_metal.py` — l'agrégateur FAIL-CLOSED : un run manquant = REFUS,
   un run corrompu (empreinte ou schéma) = REFUS ; jamais de verdict partiel ; le verdict
   global n'est VERT que si le jeu est complet et cohérent.
3. Pré-enregistrement : `atelier-w19-metal/preregistrement.json` (graine, N, machines attendues,
   liste des états, liste des aléas, commande, convention de mesure) consigné AVANT tout run ;
   son sha256 au rapport.

## Contraintes
- Aucun chiffre avant le geste du développeur : le kit ne rend que EN ATTENTE.
- Banc sur copies de laboratoire uniquement ; aucun coffre réel approché (D105).
- Le chronomètre est monotone ; la graine et l'ordre des exécutions sont consignés.

## Critères d'acceptation
- Autotest de l'agrégateur : run manquant → REFUS nommé ; run corrompu → REFUS nommé ;
  jeu complet et cohérent → VERT.
- Rejeu bit-identique deux fois à graine consignée.
- Empreintes des journaux bruts consignées AVANT tout agrégat.
- Les sorties confrontées aux états attendus (aucun état partiel exécutable observable).
- Statut publié : EN ATTENTE (aucun run matériel dans ce bac), nommé au rapport.
