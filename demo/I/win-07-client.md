win-07 · client TCP (connexion locale) · révision 1
Intention : la moitié cliente de la démonstration réseau — créer un socket et
connecter à 127.0.0.1:25000 (le port du serveur écho scellé tcp-01) ; sockaddr
construite dans le cadre (famille, port en ordre réseau, adresse littérale —
aucune dépendance htonl/inet_addr : les octets sont connus du plan).
Contrat :
  pre  : P1 WSAStartup a été exécuté (par tcp-01 dans le thread serveur, lancé
         AVANT le client par le scénario) ; P2 pile alignée (rsp ≡ 8 mod 16) ;
         P3 IAT ws2_32 résolue — socket, connect, closesocket (D35 : FT =
         slots appelés).
  post : Q1 succès : rax = socket cliente (non nulle), la sockaddr (16 o)
         restait dans le cadre ; Q2 échec (socket = -1 OU connect ≠ 0) :
         socket fermée par closesocket si créée, rax = 0, aucun effet
         persistant (.data intact).
  inv  : I1 appels ws2_32 exclusivement via l'IAT ; I2 sockaddr sur pile,
         jamais en .data ; I3 le port 25000 est celui du bloc scellé tcp-01
         (0xA861 en ordre réseau, cuit dans ses octets) — le client épouse le
         plan d'adressage du serveur, il ne le redéfinit pas.
Échecs :
  E1 : socket() = -1 (WSA épuisée) — rax = 0.
  E2 : connect() ≠ 0 (serveur absent/port occupé par un tiers) — closesocket,
       rax = 0 : le scénario affichera l'échec réseau sans crash.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims socket/connect → succès (socket factice, connect 0)
       ; connect = -1 → closesocket appelé puis rax = 0 ; socket = -1 →
       rax = 0 sans connect (couvre Q1-Q2, E1-E2).
Fixtures    : néant (sockaddr construite en pile depuis constantes du plan).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT ws2_32), D35 (FT = slots) ; port hérité tcp-01.
