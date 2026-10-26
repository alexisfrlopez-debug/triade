libc-05 · allocateur par zone · révision 1
Intention : allouer des blocs dans une arène statique par simple avancement de
curseur — l'allocation la plus déterministe possible : aucun tas extérieur,
aucune fragmentation, un coût constant, un échec propre et prévisible.
Contrat :
  pre  : P1 rcx contient la taille demandée (u64) ;
         P2 rdx contient l'alignement demandé ;
         P3 le curseur d'arène (qword à RVA 0x3000) est dans [0, taille de
             l'arène] — initialisé à 0 par le chargeur, maintenu par les
             seuls blocs libc-05/libc-06 ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 succès : rax contient un pointeur dans l'arène, aligné sur
         l'alignement demandé, dont la borne basse est l'ancien curseur aligné ;
         Q2 succès : le curseur vaut l'offset du pointeur retourné augmenté de
             la taille demandée ;
         Q3 échec (taille strictement supérieure à l'arène, alignement nul, non
             puissance de deux ou strictement supérieur à 64, ou arène
             épuisée) : rax = 0 et le curseur est inchangé ;
         Q4 taille = 0 : pointeur valide retourné, curseur inchangé.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 aucun registre non volatil n'est modifié ;
         I3 la seule écriture du bloc est le qword curseur (l'arène elle-même
             n'est jamais écrite par ce bloc) ;
         I4 l'arène est alignée sur 64 en adresse absolue (base de section
             .data + 0x40), garantie de l'alignement contractuel pour tout
             alignement puissance de deux jusqu'à 64.
Échecs :
  E1 : demande invalide ou arène épuisée → retour 0, curseur inchangé, aucun
       autre effet (échec propre — l'appelant décide de la sanction).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P4, Q1-Q4, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 séquences aléatoires
       d'allocations et de réinitialisations — pointeur, alignement exact,
       non-chevauchement des bornes, curseur, et échec propre (y compris
       taille 0x7D1, alignements 0, 3, 65, 128) contre un modèle de référence ;
       non volatils, rsp, arène hors zone allouée inchangée (couvre Q1-Q4,
       I1-I4).
  V3 : vecteurs dorés embarqués (autotest b20008) : allocation alignée,
       bornes disjointes consécutives, réutilisation déterministe après
       réinitialisation, dépassement → 0 (couvre Q1-Q4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture hors du qword curseur est refusée par l'oracle (couvre I1,
       I3).
Fixtures    : néant (l'arène .data est l'état propre du bloc).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28 (alignement absolu de l'arène sur 64), D29.
