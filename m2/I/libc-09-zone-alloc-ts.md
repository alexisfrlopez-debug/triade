libc-09 · allocateur par zone thread-safe · révision 1
Intention : sérialiser l'allocateur d'arène hérité (libc-05) par une section
critique kernel32 — la réponse à la limite M1 documentée (« arène non
thread-safe », m1/README) : le bloc hérite du contrat de libc-05 à
l'identique (mêmes pré/post-conditions sur le curseur et l'arène) et y
ajoute l'exclusion mutuelle ; c'est le primitive d'allocation partagée des
jalons suivants (tunnels M3+, tampons M4+).
Contrat :
  pre  : P1 rcx contient la taille demandée (u64) ;
         P2 rdx contient l'alignement demandé (héritage libc-05 : puissance
             de deux dans [1, 64]) ;
         P3 le curseur d'arène (qword à RVA 0x3000) est cohérent — maintenu
             par libc-05/libc-06 sous verrou ;
         P4 la section critique .data (R_CS) est initialisée (tcp-12) et le
             bloc s'exécute dans un artefact qui embarque libc-05 @ 0x1300 ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès : rax contient le pointeur retourné par libc-05 ;
             Q2 échec : rax = 0 (propagation exacte de libc-05) ;
         Q3 EnterCriticalSection est pris AVANT l'appel de libc-05 et
             LeaveCriticalSection rendu APRÈS le retour, sur tout chemin.
  inv  : I1 appels système : IAT kernel32 EnterCriticalSection,
             LeaveCriticalSection exclusivement ; appel direct : libc-05
             (0x1300) exclusivement — l'allocateur scellé n'est PAS
             modifié (R7), il est emballé ;
         I2 le bloc n'écrit RIEN lui-même : le curseur reste l'affaire
             exclusive de libc-05 (le verrou, pas la mémoire) ;
         I3 le bloc alloue 0x28 octets de pile et ne touche aucun
             non-volatil ; I4 aucun stockage sous rsp.
Échecs :
  E1 : demande invalide ou arène épuisée → rax = 0 par libc-05, verrou
       rendu (Q3) — l'échec de l'allocateur n'est pas un échec du verrou.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, image synthétique libc-05+libc-09) :
       12 000 séquences contraintes contre le modèle de référence hérité de
       libc-05 — pointeur, curseur, échec propre ; Enter/Leave appariés
       exactement un-pour-un sur tous les chemins (couvre Q1-Q3).
  V3 : sérialisation : deux suites d'allocation exécutées en alternance par
       l'oracle (interverrouillage simulé) — aucun chevauchement de bornes,
       curseur toujours conforme au modèle séquentiel (couvre Q1, Q3).
  V4 : test de rejet : toute notation du bloc écrivant le curseur
       directement, appelant libc-06, ou quittant sans Leave après Enter,
       est refusée (couvre I1, I2).
Fixtures    : néant (l'arène .data est l'état propre du bloc).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33.
Historique  : R1. Analyse M2 (D33) : la discipline d'allocation du serveur
              écho est la pile privée par thread (tcp-09/tcp-10/tcp-11
              composent dans leurs cadres — zéro contention, zéro état
              partagé) ; le présent bloc est livré comme primitive scellée
              pour les jalons suivants (premiers appelants : M3) et n'est
              pas embarqué dans echo.exe (aucun appelant — la carte
              l'indexe, l'oracle le vérifie contre sa notation).
