tcp-09 · thread par connexion · révision 1
Intention : servir UNE connexion de bout en bout dans son thread — boucle
bloquante recv / écho / send-complet, journal de chaque écho, fermeture
propre à la fin (pair parti, erreur ou socket morte) puis retour de thread :
le thread meurt en rendant la main, jamais par appel de terminaison.
Contrat :
  pre  : P1 rcx contient la socket cliente connectée (argument transmis par
             tcp-06 depuis tcp-12) ;
         P2 la section critique du journal et le handle stdout sont
             initialisés par tcp-12 (démarrage complet) ;
         P3 la pile du thread (défaut système, ~1 Mio) est vierge ;
         P4 la version active de echo-01 (tcp-08) peut changer À TOUT MOMENT
             pendant la boucle (patch à chaud par tcp-07 via le thread
             console) — chaque appel d'écho utilise la version active à
             CET instant.
  post : Q1 pour chaque réception de n > 0 octets : l'écho est calculé par
             le bloc tcp-08 (entrée 0x4600), émis INTÉGRALEMENT sur la
             socket (boucle d'émission : les envois partiels de tcp-04 sont
             rejoués jusqu'à n total), et une ligne de journal « echo <n> »
             est émise via tcp-11 ;
         Q2 réception 0 (fermeture du pair) ou -1 (erreur), ou échec
             d'émission : la boucle s'arrête, la socket est fermée (tcp-05),
             la ligne « fin connexion » est journalisée, le thread rend la
             main (ret) — la socket cliente n'est JAMAIS fermée deux fois ;
         Q3 le tampon de réception (1024 octets) vit exclusivement dans le
             cadre du thread (pile privée) — aucune allocation d'arène, la
             discipline M2 est la pile (voir libc-09 pour l'analyse).
  inv  : I1 appels autorisés (tous DIRECTS, aucun IAT) : tcp-03 (recv),
             tcp-04 (send), tcp-05 (close), tcp-08 (echo), tcp-11 (journal) ;
         I2 le prologue alloue un cadre de 0x460 octets (shadow + tampon
             1024 à [rsp+0x30]) et sauvegarde rbx, r12-r15 ; l'épilogue
             restaure symétriquement — le thread se termine par ret, jamais
             par ExitThread ;
         I3 les compteurs vivent dans les non-volatils sauvegardés (rbx
             socket, r12 longueur, r13 envoyé) ;
         I4 aucun stockage sous rsp ; I5 la source de l'écho et la
             destination sont le même tampon (sur place, P4 de tcp-08).
Échecs :
  E1 : recv/send en échec → fin de session propre (Q2) : la disponibilité
       des AUTRES connexions n'est jamais engagée (isolation par thread).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : sessions scriptées (oracle, shims recv/send) : échanges multiples
       d'affilée ; émission partielle fragmentée (3+2) complétée sans perte
       ni doublement ; fermeture pair (n=0) ; erreur (n=-1) ; échec d'émission
       en cours de boucle — chaque scénario ferme exactement une fois et
       journalise la séquence exacte attendue (couvre Q1-Q3, E1).
  V3 : patch EN SESSION : bascule tcp-07 appliquée entre deux réceptions
       d'une même session émulée — la réponse suivante porte la
       transformation v2, la connexion n'est pas interrompue (critère M2,
       continuité de service) (couvre P4).
  V4 : test de rejet : toute notation du bloc appelant un IAT direct, un
       bloc hors I1, ou écrivant sous rsp, est refusée (couvre I1, I4).
Fixtures    : chaînes .rdata du journal (« echo « , « \r\n », « fin
              connexion ») — copie unique référencée (D20).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D20, D33.
