tcp-08 · écho du serveur (transformation par octet) · révision 2
Intention : transformer le tampon reçu en tampon émis, octet par octet, même
longueur — le cœur métier du serveur écho ET la cible du patch à chaud : le
bloc est conçu dès R1 pour être remplacé à chaud (entrée alignée 16, contrat
stable R4), sa transformation déclarée étant le seul élément versionné.
Contrat :
  pre  : P1 rcx pointe le tampon de destination (au moins r8 octets en
             écriture) ;
         P2 rdx pointe le tampon source (au moins r8 octets en lecture) ;
         P3 r8 contient le nombre d'octets (0 autorisé — aucune écriture) ;
         P4 destination et source peuvent se chevaucher exactement
             (transformation sur place : dst = src) ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 rax = r8 (la longueur est préservée, quel que soit le
             comportement) ;
         Q2 les r8 octets de la destination contiennent la transformation
             déclarée de la version active appliquée aux r8 octets de la
             source : R2 (v2, courante) — majuscules ASCII : tout octet dans
             [0x61, 0x7A] est émis diminué de 0x20, tout autre octet est émis
             tel quel ; R1 (v1, historique) — transformation identité,
             dst[i] = src[i] ;
         Q3 aucun octet au-delà de dst+r8 n'est écrit ; la source n'est
             jamais écrite ;
         Q4 r8 = 0 : rax = 0, aucune écriture, aucun accès mémoire.
  inv  : I1 le bloc est une FEUILLE : aucun appel, aucun accès système, aucune
             donnée .rdata/.data — il ne dépend de rien, donc il est
             remplaçable à chaud sans invalidé d'appelant (R4) ;
         I2 seuls des registres volatils sont utilisés (rax, rcx, rdx, r8,
             r9, r10, r11) — aucun push, aucun non-volatil touché ;
         I3 le premier octet du bloc est une frontière d'instruction à
             l'adresse 0x4600, alignée 16 : les 8 premiers octets constituent
             la zone trampolinable (R7) — la notation ne place JAMAIS une
             cible de saut dans les 8 premiers octets qui ne survive pas à
             la bascule (le trampoline E9 les remplace) ;
         I4 la boucle parcourt les octets dans l'ordre croissant des index —
             la transformation sur place (P4) est ainsi bien définie pour
             toute version dont la lecture précède l'écriture au même index.
Échecs :
  E1 : aucun échec défini — la transformation est totale (aucun octet
       n'échappe à la version déclarée) ; une entrée invalide (P1-P3 rompues)
       est un défaut de l'appelant, hors contrat.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) par version active : 12 000
       tampons aléatoires — identité exacte (v1) / majuscules a-z et autres
       octets intacts (v2), rax = n, bornes intactes (sentinelle au-delà de
       dst+n), source inchangée, sur place et séparées, n = 0 (couvre
       Q1-Q4, I2, I4).
  V3 : patch à chaud (tcp-07 V2/V5) : la même entrée 0x4600 sert v1 avant
       bascule, v2 après, v1 après rollback — le contrat (signature, clauses
       stables) est honoré par les deux versions (R4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un push,
       un accès .data/.rdata ou un stockage sous rsp est refusée par
       l'oracle structurel (couvre I1, I2).
Fixtures    : néant (tampons fournis par l'appelant ; l'oracle génère les
              entrées contraintes).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33 ; R4 (contrat stable), R7 (entrée trampolinable).
Historique  : R1 (dev.1, identité) révisée en R2 (dev.2) pour la boucle de
              mise à jour § 5 — le diff se limite à la transformation
              déclarée en Q2 (identité -> majuscules) ; signature, clauses
              et invariants inchangés (R4) ; le remplaçant est assemblé POUR
              la croissance 0x4680, servi par staging .rdata et basculé à
              chaud par tcp-07 — AUCUN octet de code existant ne bouge
              (démonstration R7 sur code vivant).
