libc-05 · allocateur par zone · révision 2
Intention : allouer des blocs dans une arène statique par simple avancement de
curseur — l'allocation la plus déterministe possible : aucun tas extérieur,
aucune fragmentation, un coût constant, un échec propre et prévisible.
Contrat :
  pre  : P1 taille (argument 1) : le nombre d'octets demandés (u64) ;
         P2 alignement (argument 2) : l'alignement demandé ;
         P3 le curseur d'arène (qword à l'adresse déclarée au plan
             d'adressage de l'image — frag-loc) est dans [0, taille de
             l'arène] — initialisé à 0 par le chargement de l'image,
             maintenu par les seuls blocs libc-05/libc-06 ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 succès : la valeur de retour (rax) contient un pointeur dans
             l'arène, aligné sur l'alignement demandé, dont la borne basse
             est l'ancien curseur aligné ;
         Q2 succès : le curseur vaut l'offset du pointeur retourné augmenté de
             la taille demandée ;
         Q3 échec (taille strictement supérieure à l'arène, alignement nul, non
             puissance de deux ou strictement supérieur à 64, ou arène
             épuisée) : rax = 0 et le curseur est inchangé ;
         Q4 taille = 0 : pointeur valide retourné, curseur inchangé.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 aucun registre non volatil du profil n'est modifié (frag-con) ;
         I3 la seule écriture du bloc est le qword curseur (l'arène elle-même
             n'est jamais écrite par ce bloc) ;
         I4 l'arène est alignée sur 64 en adresse absolue (garantie du plan
             d'adressage de l'image — frag-loc), garantie de l'alignement
             contractuel pour tout alignement puissance de deux jusqu'à 64.
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
  V3 : vecteurs dorés embarqués (autotest) : allocation alignée, bornes
       disjointes consécutives, réutilisation déterministe après
       réinitialisation, dépassement → 0 (couvre Q1-Q4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture hors du qword curseur est refusée par l'oracle (couvre I1,
       I3).
Fixtures    : néant (l'arène est l'état propre du bloc, au plan de l'image).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28 (alignement absolu de l'arène sur 64), D29,
              D149 (révision de granularité).
Historique  : R1 (m1/I, instance Windows scellée 0.2.0) révisée en R2 au
              chantier M6-(b) — granularité (D149-(3)) : arguments nommés
              taille/alignement, le curseur quittte le RVA littéral (R1 :
              « à RVA 0x3000 ») pour « l'adresse déclarée au plan de
              l'image » (frag-loc — chaque image porte son plan, la sémantique
              est l'arène du bloc) ; convention d'appel en frag-con ;
              observables Q1-Q4, E1, vecteurs INVARIANTS.
