tcp-02 · acceptation d'une connexion · révision 1
Intention : accepter une connexion entrante sur la socket d'écoute — le plus
fin des wrappers ws2_32 : l'argument passe, la socket cliente revient, aucun
état, aucune décision.
Contrat :
  pre  : P1 rcx contient la socket d'écoute (valeur retournée par tcp-01,
             non nulle) ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 rax contient la socket cliente retournée par accept, ou
             INVALID_SOCKET (-1) en cas d'échec — la valeur est propagée
             telle quelle, sans interprétation ;
         Q2 accept est appelé avec addr = NULL et addrlen = NULL (l'adresse
             du pair n'est pas journalisée à M2).
  inv  : I1 unique appel système : IAT ws2_32 accept ; I2 le bloc alloue
             0x28 octets de pile (shadow space) et n'écrit rien dedans ;
         I3 bloc sans état : aucune donnée .rdata/.data n'est touchée.
Échecs :
  E1 : accept échoue → rax = -1 propagé ; l'appelant (tcp-12) distingue
       l'arrêt demandé (drapeau quit) de l'échec inattendu (fail-closed).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shim accept scripté) : la socket
       scriptée est retournée inchangée ; -1 propagé tel quel ; arguments
       constatés (socket d'écoute, NULL, NULL) (couvre Q1, Q2).
  V3 : émulation binaire (tcp-12) : deux accept successifs — connexion puis
       arrêt (couvre E1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33.
