tcp-05 · fermeture de socket · révision 1
Intention : fermer une socket (écoute ou cliente) — la seule hygiène réseau
du jalon : toute socket que le serveur n'utilise plus est fermée, qu'elle
provienne de tcp-01 (arrêt demandé) ou de tcp-02 (fin de connexion).
Contrat :
  pre  : P1 rcx contient la socket à fermer (non nulle) ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 closesocket a été appelé une fois avec la socket transmise ; la
             valeur de retour (int ws2_32) n'est pas interprétée — rax la
             transporte telle quelle, l'appelant l'ignore.
  inv  : I1 unique appel système : IAT ws2_32 closesocket ; I2 le bloc
             alloue 0x28 octets de pile et n'écrit rien dedans ; I3 aucun
             état, aucun effet en dehors de l'appel.
Échecs :
  E1 : closesocket échoue → propagation silencieuse documentée (la socket
       est potentiellement déjà morte — par exemple pair déconnecté) :
       l'appelant ne décide rien sur cette base.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shim enregistreur) : closesocket
       appelé exactement une fois avec l'argument transmis, pour la socket
       d'écoute (arrêt) comme pour une socket cliente (fin de connexion)
       (couvre Q1).
  V3 : émulation binaire : l'arrêt demandé ferme la socket d'écoute avant
       le verdict final ; les sessions tcp-09 ferment leur socket cliente
       (couvre Q1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33.
