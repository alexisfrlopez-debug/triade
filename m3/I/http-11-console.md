http-11 · console · révision 1
Intention : le thread console du proxy — réduire au minimum utile : lire
l'entrée standard ligne à ligne, « quit » pose le drapeau d'arrêt et ferme
la socket d'écoute pour débloquer l'acceptation de http-12, toute autre
ligne est journalisée puis ignorée ; le thread meurt en rendant la main.
Contrat :
  pre  : P1 rcx = 0 (argument opaque transmis par tcp-06 depuis http-12) ;
         P2 la section critique et stdout sont initialisés (http-12),
             stdin est caché en .data (R_STDIN) par http-12 ;
         P3 le drapeau d'arrêt .data (R_QUIT) est à 0 et la socket
             d'écoute .data (R_LISTEN) est posée par http-12 AVANT le
             lancement de ce thread ;
         P4 la pile du thread est vierge et alignée.
  post : Q1 boucle : ReadFile (stdin, tampon de cadre, 64 octets) ; ligne
             « quit\r\n » (6 octets exacts, comparaison libc-02) → pose du
             drapeau R_QUIT (écriture unique, 1), closesocket(R_LISTEN)
             pour réveiller l'acceptation bloquée de http-12, journal
             « arret », fin de boucle ;
         Q2 toute autre ligne (ou ligne plus longue, tronquée au tampon)
             → journal « commande inconnue », boucle ;
         Q3 ReadFile en échec ou EOF (console fermée) → fin de boucle SANS
             effet : une console morte n'arrête pas le serveur (miroir
             tcp-10) ;
         Q4 le thread se termine par ret — jamais ExitThread ; le
             drapeau et l'état .data ne sont écrits que par Q1.
  inv  : I1 appels système : IAT kernel32 ReadFile ; appels directs :
             tcp-05 (fermeture de l'écoute), tcp-11 (journal), libc-02
             (comparaison) — aucun autre ; I2 le tampon (64 octets) vit
             dans le cadre du thread ; I3 la comparaison « quit\r\n »
             porte sur 6 octets reçus (une ligne plus courte n'est jamais
             comparée au-delà du rempli) ; I4 aucun stockage sous rsp.
Échecs :
  E1 : ReadFile échoue → Q3 : fin propre du thread console, le serveur
       continue sans console (l'arrêt reste possible par fermeture de
       processus).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : sessions scriptées (oracle, shim ReadFile) : « quit\r\n » →
       drapeau posé UNE fois, closesocket sur l'écoute, journal exact ;
       « patch\r\n », « rollback\r\n », lignes vides, ligne de 64 octets
       pleine, EOF → aucune fermeture d'écoute, boucle (couvre P1-P4,
       Q1-Q4, I1-I4, E1).
  V3 : test de rejet : toute notation écrivant le drapeau hors Q1 ou
       appelant un bloc hors I1 est refusée (couvre I1, Q4).
Fixtures    : chaîne « quit\r\n » .rdata (6 octets — fixture de ce bloc) ;
              lignes de journal (« commande inconnue », « arret ») —
              fixtures partagées du journal.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D45, D46.
