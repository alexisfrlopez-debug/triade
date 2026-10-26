tcp-03 · réception d'octets · révision 1
Intention : recevoir n octets au plus depuis une socket connectée dans un
tampon fourni par l'appelant — wrapper recv sans fanion, sans état, la
sémantique de la socket Blocking étant portée par l'appelant.
Contrat :
  pre  : P1 rcx contient une socket connectée ;
         P2 rdx pointe un tampon d'au moins r8 octets en écriture ;
         P3 r8 > 0 ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 rax contient le nombre d'octets reçus (> 0), 0 si le pair a
             fermé proprement, ou SOCKET_ERROR (-1) en échec — valeur
             propagée telle quelle ;
         Q2 recv est appelé avec flags = 0 et exactement (socket, tampon,
             capacité) transmis par l'appelant.
  inv  : I1 unique appel système : IAT ws2_32 recv ; I2 le bloc alloue 0x28
             octets de pile et n'écrit rien dedans ; I3 aucun état.
Échecs :
  E1 : recv échoue → rax = -1 propagé ; l'appelant (tcp-09) ferme la socket
       et termine son thread (échec propre).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shim recv scripté) : les octets
       scriptés sont écrits dans le tampon de l'appelant, rax = n ; n = 0 et
       n = -1 propagés ; arguments constatés ; le tampon n'est jamais écrit
       au-delà de n octets par le shim (couvre Q1, Q2).
  V3 : sessions scriptées de tcp-09 (messages, fermeture, échec) (couvre E1).
Fixtures    : néant (tampon fourni par l'appelant).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33.
