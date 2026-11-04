libc-06 · réinitialisation de zone · révision 2
Intention : remettre le curseur d'arène à zéro en une instruction de stockage —
la réinitialisation la plus rapide et la plus auditable qui soit, socle du
cycle allocation/réinitialisation de la mini-libc.
Contrat :
  pre  : P1 le curseur d'arène (qword à l'adresse déclarée au plan
             d'adressage de l'image — frag-loc) est dans [0, taille de
             l'arène] ;
         P2 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 le curseur d'arène vaut 0 ;
         Q2 la valeur de retour n'est pas une donnée du contrat (valeur
             indéterminée).
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie (aucun registre sauvegardé) ;
         I3 aucun registre non volatil du profil n'est modifié (frag-con) ;
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
  V3 : vecteur doré embarqué (autotest, via libc-05) : après réinitialisation,
       la prochaine allocation retourne la base de l'arène (couvre Q1).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture autre que le curseur est refusée par l'oracle (couvre I1,
       I4).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29, D149 (révision de granularité).
Historique  : R1 (m1/I, instance Windows scellée 0.2.0) révisée en R2 au
              chantier M6-(b) — granularité (D149-(3)) : le curseur quitte le
              RVA littéral pour le plan de l'image (frag-loc) ; observables
              Q1-Q2, E1, vecteurs INVARIANTS.
