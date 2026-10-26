tcp-01 · initialisation serveur TCP · révision 1
Intention : dresser la table d'écoute du serveur écho — WSAStartup, création de
la socket, bind sur toutes les interfaces au port 25000, mise en écoute — et
retourner la socket d'écoute ; tout échec nettoie derrière lui (échec propre,
aucun état WSA orphelin).
Contrat :
  pre  : P1 le bloc n'est appelé qu'une fois par exécution, avant toute autre
             utilisation de ws2_32 ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16) ;
         P3 0x210 octets de pile sont disponibles sous le cadre du bloc.
  post : Q1 succès : rax contient la socket d'écoute (valeur non nulle,
             différente de INVALID_SOCKET) ; Q2 WSAStartup a été appelé avec
             la version 0x0202, la socket créée en AF_INET/SOCK_STREAM/
             IPPROTO_TCP, liée à INADDR_ANY:25000 (port en ordre réseau),
             et listen a été appelé avec une file de 8 ;
         Q3 échec (WSAStartup ≠ 0, socket invalide, bind ≠ 0 ou listen ≠ 0) :
             rax = 0 et le contexte WSA est nettoyé — si la socket était
             créée, closesocket ; si WSAStartup avait réussi, WSACleanup ;
             l'appelant décide de la sanction ;
         Q4 WSADATA (>= 408 octets) et sockaddr_in (16 octets) vivent
             exclusivement dans le cadre du bloc (pile privée).
  inv  : I1 seules fonctions système appelées : IAT ws2_32 WSAStartup, socket,
             bind, listen, closesocket, WSACleanup — jamais de syscall direct ;
         I2 le mot sockaddr vaut famille AF_INET (2) puis port 0x61A8 en ordre
             réseau (mot little-endian 0xA861), adresse INADDR_ANY (0) ;
         I3 le prologue alloue un cadre de 0x210 octets et sauvegarde rbx,
             r12-r15 ; l'épilogue les restaure symétriquement ;
         I4 aucun stockage sous rsp ; I5 la valeur de retour de chaque appel
             système est testée avant tout usage ultérieur (fail-closed).
Échecs :
  E1 : WSAStartup/socket/bind/listen en échec → nettoyage (Q3) et retour 0 —
       l'orchestrateur journalise « erreur reseau » et termine le processus
       (code 2) : un serveur qui ne peut pas écouter ne sert rien.
Vecteurs :
  V1 : round-trip de notation 100 % (couvre la fidélité générale du bloc).
  V2 : propriété différentielle (oracle, shims ws2_32) : chemin nominal —
       ordre exact des appels et arguments (0x0202 ; 2/1/6 ; sockaddr
       little-endien 02 00 61 A8 00 00 00 00 ; backlog 8), socket retournée ;
       chaque chemin d'échec (WSAStartup≠0, socket=INVALID, bind≠0, listen≠0)
       retourne 0 avec exactement le nettoyage attendu (closesocket et/ou
       WSACleanup appelés, jamais d'appel réseau au-delà) (couvre Q1-Q3, I1,
       I5).
  V3 : émulation binaire (tcp-12) : le serveur complet démarre, journalise la
       bannière et atteint la boucle d'acceptation (couvre P1).
  V4 : test de rejet : toute notation du bloc appelant une fonction hors I1,
       ou écrivant sous rsp, est refusée par l'oracle structurel.
Fixtures    : néant (sockaddr et WSADATA sont construits dans le cadre).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D10, D33.
