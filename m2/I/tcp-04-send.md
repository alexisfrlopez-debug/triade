tcp-04 · émission d'octets · révision 1
Intention : émettre des octets depuis un tampon fourni sur une socket
connectée — wrapper send sans fanion ; la boucle d'émission complète
(l'envoi partiel est légitime sur TCP) vit chez l'appelant tcp-09.
Contrat :
  pre  : P1 rcx contient une socket connectée ;
         P2 rdx pointe les octets à émettre ;
         P3 r8 > 0 ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 rax contient le nombre d'octets effectivement émis (> 0) ou
             SOCKET_ERROR (-1) — valeur propagée telle quelle ; l'appelant
             boucle tant que le total n'est pas atteint ;
         Q2 send est appelé avec flags = 0 et exactement (socket, tampon,
             longueur) transmis par l'appelant.
  inv  : I1 unique appel système : IAT ws2_32 send ; I2 le bloc alloue 0x28
             octets de pile et n'écrit rien dedans ; I3 aucun état.
Échecs :
  E1 : send échoue → rax = -1 propagé ; l'appelant ferme et termine.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shim send capturant) : les octets
       capturés sont exactement les n du tampon ; retour partiel k < n
       propagé ; -1 propagé ; arguments constatés (couvre Q1, Q2).
  V3 : sessions scriptées de tcp-09 avec émissions partielles (send
       fragmenté en 3 puis 2) — la boucle de l'appelant complète le total
       sans perte ni doublement (couvre Q1, E1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33.
