tcp-07 · moteur de patch à chaud · révision 1
Intention : basculer le bloc echo-01 entre sa version installée (v1, entrée
0x4600) et son remplaçant en zone de croissance (0x4680), SANS JAMAIS écrire
un bloc pendant qu'il s'exécute — le remplaçant est d'abord intégralement
copié dans la croissance, puis l'entrée bascule par UNE écriture alignée
unique de qword (E9 rel32 + NOP x3), atomique sur x86-64 ; le rollback
réécrit le qword original sauvegardé. C'est l'instanciation M2 du mécanisme
de patch du profil (manuel § 7.4) et la première exécution de la boucle de
mise à jour § 5 sur du code vivant.
Contrat :
  pre  : P1 rcx contient le mode : 0 = appliquer le remplaçant, 1 = retour
             arrière ; tout autre valeur est refusée (code 1) ;
         P2 le staging .rdata (R_STAGING) contient, pour le mode 0, le bloc
             remplaçant assemblé POUR l'adresse de croissance 0x4680 (les
             déplacements relatifs de sa notation y sont résolus) ;
         P3 la table d'intégrité R10 (.rdata, R_TAB_SUM) porte le staging en
             première entrée — (rva, taille u32, somme u64) : taille 0 =
             staging absent, la somme attendue est celle des qwords du
             staging ;
         P4 l'état .data (R_ETAT_PATCH) reflète la version active : 0 = v1,
             1 = v2 — maintenu par le seul présent bloc ;
         P5 l'entrée echo (0x4600) est alignée 16 et ses 8 premiers octets
             constituent la zone trampolinable (R7) ;
         P6 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 mode 0 réussi : la croissance (0x4680, taille du staging)
             contient octet pour octet le staging ; les 8 premiers octets de
             l'entrée echo contiennent E9 <rel32 vers la croissance> suivi
             de trois NOP ; l'original de ces 8 octets est conservé en .data
             (R_ENTREE_SAUVEE) ; l'état passe à 1 ; rax = 0 ;
         Q2 mode 1 réussi : les 8 premiers octets de l'entrée echo sont
             restaurés à l'identique de R_ENTREE_SAUVEE ; l'état passe à 0 ;
             rax = 0 ; la croissance n'est pas effacée (le remplaçant y
             dort, réactivable) ;
         Q3 l'écriture de bascule et celle de rollback sont chacune UNE
             seule écriture alignée de qword à l'entrée echo (atomicité
             x86-64) — jamais deux écritures partielles observables ;
         Q4 pendant les écritures, la page 0x4000 est passée en
             PAGE_READWRITE (VirtualProtect), puis restaurée en
             PAGE_EXECUTE_READ après la bascule — l'image redevient RX ;
         Q5 refus fail-closed (rax = code, AUCUN octet de .text/.text2
             modifié, état inchangé) : code 1 mode invalide ; code 2
             staging absent (taille 0) ; code 3 somme du staging divergente
             (intégrité douteuse — l'installation d'un remplaçant corrompu
             est interdite, R10) ; code 4 état incohérent avec la demande
             (appliquer alors que v2 actif, retour alors que v1 actif) ;
             code 5 VirtualProtect refusé (avant toute écriture) ;
         Q6 en cas d'échec de la restauration de protection APRÈS bascule
             réussie (mode 0), rax = 5 mais la bascule est effective et
             l'état est mis à jour (défaut documenté : image laissée RW —
             le processus est dans un état incohérent, l'appelant journalise
             le refus).
  inv  : I1 appels système : IAT kernel32 VirtualProtect exclusivement
             (deux par opération réussie, jamais plus) ; appels internes :
             libc-01 memcpy (copie staging -> croissance) exclusivement ;
         I2 aucune autre zone de .text/.text2 n'est écrite que l'entrée
             echo (8 octets) et la croissance (taille staging) ;
         I3 le qword de bascule est construit hors de l'image (registre),
             puis posé par mov qword ptr [entrée], reg — l'écriture n'est
             jamais décomposée ;
         I4 le prologue alloue 0x40 octets (shadow + qword old-protect) et
             sauvegarde rbx, r12-r15 ; l'épilogue restaure symétriquement ;
         I5 aucun stockage sous rsp ; la loge [rsp+0x30] sert de qword
             old-protect pour les deux VirtualProtect.
Échecs :
  E1 : staging absent ou corrompu → refus AVANT toute écriture (Q5) : le
       serveur continue de servir en v1 — la disponibilité prime (ordre
       lexicographique : sécurité d'abord, service ensuite).
  E2 : état incohérent (double application, rollback à vide) → refus code 4
       sans effet — les commandes console répétées sont légitimes, le moteur
       est idempotent par refus.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : scénario d'émulation complet (oracle, shims VirtualProtect) :
       appliquer → croissance = staging octet pour octet, entrée = E9
       rel32 + NOP x3 (cible exacte 0x4680), original sauvegardé, état 1,
       appels VirtualProtect appariés RW puis RX ; l'entrée APPELÉE
       retourne le comportement du remplaçant (majuscules) — LE PATCH EST
       EFFECTIF ; rollback → entrée restaurée octet pour octet, état 0,
       comportement v1 (identité) de retour (couvre Q1-Q4).
  V3 : falsification du staging (un octet corrompu) → code 3, entrée
       inchangée, comportement v1 préservé (couvre Q5, E1, R10).
  V4 : états incohérents (appliquer x2, rollback x2, rollback sans
       application) → code 4, aucun effet (couvre E2).
  V5 : patch EN SESSION : bascule appliquée entre deux recv d'une même
       connexion émulée (tcp-09) — la connexion continue, le comportement
       change à la réception suivante, sans interruption de service
       (critère de sortie M2).
  V6 : test de rejet : toute notation écrivant ailleurs que l'entrée/la
       croissance pendant la bascule, ou basculant par écritures
       partielles, est refusée par l'oracle structurel (couvre I2, I3).
Fixtures    : staging et table d'intégrité .rdata (dev.2 : bloc echo-01:R2
              assemblé pour 0x4680 ; dev.1 : taille 0).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33 (croissance/staging), R4 (contrat stable echo),
              R7 (entrée seule trampolinable), R10 (somme avant effet).
