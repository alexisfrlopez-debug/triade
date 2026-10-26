libc-06 · réinitialisation de zone · révision 1
Intention : remettre le curseur d'arène à zéro en une instruction de stockage —
la réinitialisation la plus rapide et la plus auditable qui soit, socle du
cycle allocation/réinitialisation de la mini-libc.
Contrat :
  pre  : P1 le curseur d'arène (qword à RVA 0x3000) est dans [0, taille de
         l'arène] ;
         P2 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 le curseur d'arène vaut 0 ;
         Q2 rax n'est pas une donnée du contrat (valeur indéterminée).
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie (aucun registre sauvegardé) ;
         I3 aucun registre non volatil n'est modifié ;
         I4 la seule écriture du bloc est le qword curseur ;
         I5 le contenu de l'arène devient indéfini après réinitialisation (la
             réinitialisation ne nettoie pas les octets — l'initialisation
             appartient aux propriétaires des nouvelles allocations).
Échecs :
  E1 : aucune condition d'échec — la réinitialisation est totale.
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P2, Q1-Q2, I1-I5).
  V2 : propriété différentielle (oracle) : 3 000 séquences allocation →
       réinitialisation → allocation — curseur nul constaté, réutilisation
       déterministe à l'identique du modèle de référence, non volatils, rsp,
       arène inchangée octet par octet (couvre Q1, I1-I5).
  V3 : vecteur doré embarqué (autotest b20008, via libc-05) : après
       réinitialisation, la prochaine allocation retourne la base de l'arène
       (couvre Q1).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture autre que le curseur est refusée par l'oracle (couvre I1,
       I4).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29.
