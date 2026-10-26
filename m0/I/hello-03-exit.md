hello-03 · bloc de sortie · révision 1
Intention : terminer le processus proprement par ExitProcess, bloc sans retour —
le dernier mot du processus appartient au contrat, pas au hasard du chargeur.
Contrat :
  pre  : P1 rcx contient le code de sortie du processus (u32, attendu : 0) ;
         P2 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 le processus est terminé à l'appel de ExitProcess — le bloc ne retourne
         jamais à son appelant.
  inv  : I1 aucun chemin d'exécution au-delà de l'appel : `ud2` défensif immédiat,
         materialisant l'inaccessibilité (fail-closed, esprit R10).
Échecs :
  E1 : ExitProcess est interceptée ou échoue (chemin réputé inaccessible) → arrêt
       dur par `ud2` plutôt que poursuite d'exécution en état indéterminé.
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1, P2, Q1, I1).
  V2 : propriété structurelle (oracle) : aucune instruction `ret` dans le bloc,
       `ud2` présent après l'appel IAT unique (couvre Q1, I1).
  V3 : test de rejet : toute notation du bloc contenant un `ret`, ou retournant à
       son appelant après l'appel, est refusée par l'oracle (couvre Q1, I1).
  V4 : exécution sur Windows 11 — le code de sortie du processus est 0
       (couvre Q1 ; critère de sortie M0, validation terrain).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT), D8 (granularité/padding), D26 (M0).
