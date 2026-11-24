# PLAN GELÉ — BHQG73GZH — les aléas résiduels du rendez-vous de quiescence

## L'instruction, en une phrase
Étendre `kit_bascule.py` et la spécification (§ 7.6 du PDF) aux cinq aléas résiduels :
création de thread pendant le rendez-vous, retours de pile dans la plage, ±2 GiB du
rel32, réservation du slot 16 octets, deadlock SuspendThread.

## Les cinq cas (chacun = un refus nommé + un invariant d'état)
1. THREAD-CREE-PENDANT-RENDEZ-VOUS — gel de création ou ré-énumération, refus si un
   thread non vérifié apparaît ;
2. RETOUR-PILE-DANS-PLAGE — inspection de pile, refus (l'atomicité ne protège pas un
   retour) ;
3. HORS-PORTEE-REL32 — refus si la zone de croissance est à plus de ±2 GiB ;
4. SLOT-NON-RESERVE — refus si les 16 octets alignés ne sont pas réservés au build ;
5. LOCK-DETENU — ordre d'acquisition nommé, refus si un thread suspendu détient un
   verrou requis par le patcheur.

## Vérification exigée
L'autotest 10/10 existant reproduit à l'identique + 5 nouveaux cas ; contrôles
négatifs : chaque invariant violé → rollback, aucun état partiel exécutable.
Consigne « banc vert, métal EN ATTENTE (≥ 2 machines) ».
