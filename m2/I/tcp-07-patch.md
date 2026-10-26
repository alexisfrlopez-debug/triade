tcp-07 · moteur de patch à chaud · révision 3
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
             PAGE_EXECUTE_READWRITE (0x40, VirtualProtect), puis restaurée
             en PAGE_EXECUTE_READ (0x20) après la bascule — l'image reste
             exécutable en continu (I6, D39 : la page protégée contient le
             présent bloc lui-même, slot 0x4400) ;
         Q5 refus fail-closed (rax = code, AUCUN octet de .text/.text2
             modifié, état inchangé) : code 1 mode invalide ; code 2
             staging absent (taille 0) ; code 3 somme du staging divergente
             (intégrité douteuse — l'installation d'un remplaçant corrompu
             est interdite, R10) ; code 4 état incohérent avec la demande
             (appliquer alors que v2 actif, retour alors que v1 actif) ;
             code 5 VirtualProtect refusé (avant toute écriture) ;
         Q6 en cas d'échec de la restauration de protection APRÈS bascule
             réussie (mode 0), rax = 5 mais la bascule est effective et
             l'état est mis à jour (défaut documenté : image laissée RWX —
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
         I4 le prologue alloue 0x40 octets et sauvegarde rbx, r12-r15 ;
             l'épilogue restaure symétriquement ;
         I5 aucun stockage sous rsp au moment d'un appel ; la loge
             old-protect vit dans la réserve de .protger ([rsp+0x20], R3)
             pour les deux VirtualProtect ;
         I6 D39 (R2) : toute protection appliquée à une page contenant du
             code en cours d'exécution RETIENT le bit execute — les phases
             d'écriture passent par PAGE_EXECUTE_READWRITE (0x40), jamais
             PAGE_READWRITE (4) : en x86-64 le DEP est permanent (image
             NX_COMPAT), une page sans bit execute faute à l'instruction
             suivante et tue le processus (constat terrain démo.4 : journal
             gelé après J_LIBC_OK, mort au retour du premier VirtualProtect) ;
         I7 D41 (R3) : .protger réserve 0x28 octets avant l'appel IAT
             VirtualProtect — 0x20 de zone d'accueil ABI msx64 (shadow
             space : l'appelé est en DROIT d'y ranger rcx/rdx/r8/r9 ; le
             code système Windows est compilé /homeparams et le fait
             TOUJOURS) + 0x8 d'alignement (rsp ≡ 0 mod 16 au call). La
             zone d'accueil ne peut jamais recouvrir l'adresse de retour
             de .protger ni le qword old-protect (constat terrain démo.6 :
             sub rsp,8 seul → kernel32 range rdx=0x700 sur l'adresse de
             retour → ret vers 0x700 → processus mort, fenêtre disparue,
             journal gelé après sonde1).
Échecs :
  E1 : staging absent ou corrompu → refus AVANT toute écriture (Q5) : le
       serveur continue de servir en v1 — la disponibilité prime (ordre
       lexicographique : sécurité d'abord, service ensuite).
  E2 : état incohérent (double application, rollback à vide) → refus code 4
       sans effet — les commandes console répétées sont légitimes, le moteur
       est idempotent par refus.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : scénario d'émulation complet (oracle, shims VirtualProtect qui
       APPLIQUENT les permissions réelles — D39 : un fetch depuis une page
       sans bit execute est une faute — ET rangent leurs 4 arguments dans
       la zone d'accueil de l'appelant, modélisation /homeparams D41) :
       appliquer → croissance = staging
       octet pour octet, entrée = E9 rel32 + NOP x3 (cible exacte 0x4680),
       original sauvegardé, état 1, appels VirtualProtect appariés RWX puis
       RX ; l'entrée APPELÉE retourne le comportement du remplaçant
       (majuscules) — LE PATCH EST EFFECTIF ; rollback → entrée restaurée
       octet pour octet, état 0, comportement v1 (identité) de retour
       (couvre Q1-Q4, I6, I7).
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
  V7 : falsification DEP (D39, R2) : la constante de phase d'écriture
       réécrite de 0x40 en 0x04 (le défaut terrain exact) → l'émulation
       FAUTE (fetch depuis page non exécutable au retour du VirtualProtect)
       — zéro silence ; le journal s'arrête après J_LIBC_OK, signature
       identique au constat terrain (couvre I6) ;
  V8 : falsification shadow space (D41, R3) : la réserve de .protger
       réécrite 0x28 → 0x08 (le défaut terrain démo.6 exact) → le shim
       range rdx (0x700) sur l'adresse de retour de .protger → l'émulation
       FAUTE au ret (saut vers 0x700, adresse non mappée) — zéro silence ;
       journal gelé après sonde1, processus mort : signature identique au
       constat terrain (couvre I7).
Fixtures    : staging et table d'intégrité .rdata (dev.2 : bloc echo-01:R2
              assemblé pour 0x4680 ; dev.1 : taille 0).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33 (croissance/staging), D39 (protection RWX : DEP
              permanent x64), D41 (zone d'accueil ABI msx64 : .protger
              réserve 0x28 avant l'appel IAT), R4 (contrat stable echo),
              R7 (entrée seule trampolinable), R10 (somme avant effet).
Historique  : R1 (dev.1) révisée en R2 (terrain démo.4, D39) : les phases
              d'écriture passaient la page 0x4000 — qui contient le présent
              bloc — en PAGE_READWRITE (4), valeur sans bit execute : au
              retour du premier VirtualProtect, le fetch de l'instruction
              suivante violait DEP/NX et tuait le processus (cinquième
              classe de défaut invisible sans exécution : protection non
              modélisée par l'oracle). Le diff se limite aux constantes de
              protection 4 → 0x40 aux deux sites (application et rollback)
              et à Q4/I6/V2/V7 ; signature, codes d'échec et effets
              inchangés (R4). L'oracle applique désormais réellement les
              permissions (D39).
              R2 révisée en R3 (terrain démo.6, D41) : les sondes D40 ont
              localisé la mort après « sonde1 avant echo » — l'écho v1 (11
              instructions pures) et le memcmp (prouvé par le sceau libc
              4/4) étaient innocents ; restait la pose. .protger appelait
              VirtualProtect avec sub rsp,8 : aligné au bit près, mais
              SANS les 0x20 octets de zone d'accueil ABI — kernel32
              (/homeparams) range rdx (0x700) exactement sur l'adresse de
              retour de .protger, le ret saute à 0x700 et tue le processus
              (septième classe de défaut invisible sans exécution :
              obligation ABI côté appelant, non modélisée par le shim ; le
              correctif D39 la masquait — la faute NX survenait avant le
              ret empoisonné). Diff limité à .protger : sub rsp 8 → 0x28,
              lea r9 [rsp+0x38] → [rsp+0x20], add rsp 8 → 0x28 (3 octets,
              aucun déplacement déplacé) ; I4/I5 précisés, I7/V8 ajoutés,
              V2 amendé ; signature, codes d'échec et effets inchangés
              (R4). L'oracle range désormais les arguments dans la zone
              d'accueil de l'appelant (D41).
