tcp-13 · connexion cliente résolue · révision 1
Intention : la moitié cliente généralisée du réseau — résoudre un hôte
NOMMÉ (getaddrinfo : DNS ou littéral, IPv4) et connecter la première
adresse AF_INET au port demandé — le pendant client de tcp-01 pour une
cible ARBITRAIRE fournie par une entrée non fiable (l'autorité de la
requête) ; tout échec nettoie derrière lui, aucune fuite d'addrinfo.
Contrat :
  pre  : P1 rcx pointe le span hôte (crochets IPv6 déjà exclus par
             http-07 — octets quelconques, jamais supposés terminés par
             un NUL) ;
         P2 rdx contient la longueur du span hôte (u64) ;
         P3 r8d contient le port (u16, ordre hôte — la conversion en
             ordre réseau appartient à ce bloc) ;
         P4 WSA est actif (WSAStartup réussi par tcp-01 dans http-12) ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16) et au moins
             0x220 octets sont disponibles sous le cadre.
  post : Q1 succès : rax = socket amont connectée (non nulle) ;
         Q2 le span hôte est recopié dans le tampon de cadre (256 octets)
             et terminé par un NUL pour l'entrée système — getaddrinfo
             exige une chaîne C : la traduction span→chaîne est la
             propriété de CE bloc (aucun autre bloc du projet ne
             construit de chaîne C depuis un span réseau) ;
         Q3 getaddrinfo est appelé avec hints posés en pile : famille
             AF_INET, type SOCK_STREAM, protocole 0 — le premier
             résultat AF_INET est retenu (parcours défensif de la liste,
             les hints filtrent déjà), sa sockaddr (famille, port en
             ordre réseau — écrit par ce bloc depuis P3, adresse) est
             recopiée dans le cadre pour connect ;
         Q4 échec nommé — rax = 0 dans tous les cas suivants : hôte de
             longueur nulle ou > 255 (limite DNS, constante nommée de ce
             bloc) ; getaddrinfo non nul ; liste sans entrée AF_INET ;
             socket invalide ; connect non nul — et le nettoyage est
             COMPLET sur tout chemin : freeaddrinfo si résolu,
             closesocket si créée, AUCUN état persistant (.data intact),
             aucune ressource retenue ;
         Q5 WSACleanup n'est JAMAIS appelé par ce bloc (le cycle WSA
             appartient à tcp-01/http-12).
  inv  : I1 appels système : IAT ws2_32 getaddrinfo, freeaddrinfo,
             socket, connect, closesocket — jamais de syscall direct ;
         I2 le tampon hôte (256 o), les hints (48 o), la sockaddr (16 o)
             et les pointeurs de résultat vivent exclusivement dans le
             cadre (pile privée — discipline M2) ;
         I3 la conversion du port est une instruction de changement
             d'endianness du bloc (aucune dépendance htons — le plan
             d'adressage ne s'étend pas d'une entrée IAT pour cela) ;
         I4 la valeur de retour de chaque appel système est testée avant
             tout usage ultérieur (fail-closed, miroir tcp-01:I5) ;
         I5 le prologue alloue le cadre et sauvegarde rbx, r12-r15 ;
             l'épilogue restaure symétriquement ; aucun stockage sous
             rsp.
Échecs :
  E1 : tout échec de Q4 → rax = 0 : l'appelant (http-10) répond 502 et
       clôture la session — le proxy n'insiste jamais (pas de
       reconnexion, pas de basculement d'adresse : la première adresse
       suffit ou rien).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shims getaddrinfo/socket/
       connect enregistreurs) : 3 000 scénarios — résolution à 1/N
       résultats (dont familles non AF_INET en tête — le parcours
       défensif saute), getaddrinfo en échec, socket invalide, connect
       refusé APRÈS création (closesocket constaté), connectrefusé avec
       addrinfo non libéré dans un modèle fautif → l'oracle compte
       freeaddrinfo/closesocket exactement un-pour-un (couvre P1-P5,
       Q1-Q5, I1-I5, E1) ;
  V3 : hôtes non fiables : longueur 0/255/256/1000, octets binaires
       (recopie + NUL exact, jamais au-delà du tampon), ports 0/1/65535
       (mot réseau exact dans la sockaddr) (couvre Q2, Q3) ;
  V4 : test de rejet : toute notation appelant WSACleanup, laissant une
       addrinfo non libérée sur un chemin, ou écrivant hors du cadre est
       refusée (couvre I1, I2, Q4).
Fixtures    : néant (l'hôte vient de l'autorité parsée — fixtures de
              http-10).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D35 (FT = slots appelés), D45, D46.
