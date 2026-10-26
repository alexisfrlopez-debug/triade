tcp-10 · thread console · révision 1
Intention : lire les commandes de l'opérateur sur l'entrée standard — patch,
rollback, quit — et les exécuter : c'est la main de l'opérateur sur le code
vivant ; toute commande inconnue est journalisée et ignorée, la boucle
survit à tout, y compris à la fermeture du flux d'entrée.
Contrat :
  pre  : P1 le handle stdin est caché en .data (R_STDIN) par tcp-12 ;
         P2 la section critique du journal est initialisée ;
         P3 la socket d'écoute est cachée en .data (R_LISTEN) par tcp-12 ;
         P4 le moteur tcp-07 et le staging sont dans l'état livré par le
             build (v1 active, staging selon dev.1/dev.2) ;
         P5 la pile du thread est vierge et alignée.
  post : Q1 pour chaque ligne lue (n octets > 0) : « patch\r\n » (n=7) →
             tcp-07 mode 0, journal « patch applique (majuscules) » si
             code 0, sinon « commande refusee » ; « rollback\r\n » (n=9) →
             tcp-07 mode 1, journal « retour arriere (identite) » si code 0,
             sinon « commande refusee » ; « quit\r\n » (n=6) → drapeau
             d'arrêt .data (R_QUIT) posé à 1, socket d'écoute fermée
             (tcp-05) pour débloquer l'acceptation, fin du thread console ;
             toute autre entrée → journal « commande inconnue », boucle ;
         Q2 ReadFile échoue ou retourne 0 octet (fin de flux) : le thread
             console se termine proprement — le serveur CONTINUE de servir
             (perte du contrôle opérateur, documentée) ;
         Q3 les comparaisons de commandes sont exactes : longueur ET contenu
             (memcmp libc-02 sur la totalité des octets lus) — « patchx »
             n'est pas « patch ».
  inv  : I1 appels système : IAT kernel32 ReadFile exclusivement ; appels
             directs : libc-02 (memcmp), tcp-07 (patch), tcp-11 (journal),
             tcp-05 (close) ;
         I2 le tampon de lecture (64 octets) et le qword d'octets lus
             vivent dans le cadre du thread ([rsp+0x30], [rsp+0x28]) — pile
             privée, aucune allocation d'arène ;
         I3 le prologue alloue 0x70 octets et sauvegarde rbx, r12-r15 ;
             l'épilogue restaure symétriquement ; sortie par ret uniquement ;
         I4 le drapeau d'arrêt et la fermeture de la socket d'écoute sont
             les SEULES écritures .data du bloc (R_QUIT) — l'état du patch
             vit dans tcp-07.
Échecs :
  E1 : commande refusée par tcp-07 (staging absent/corrompu, état
       incohérent) → journal « commande refusee », boucle : l'opérateur
       voit le refus, le service continue (fail-closed, pas de crash).
  E2 : fin de flux stdin → Q2 : le serveur devient incontrôlable depuis la
       console mais reste serveur ; l'arrêt reste possible en tuant le
       processus (documenté : garder la console ouverte pendant l'essai).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : séquences scriptées (oracle, shim ReadFile) : les trois commandes en
       ordres variés, doublons (double patch → refus), commandes inconnues
       (« status », « patchx », ligne vide), fin de flux — journal exact et
       effets .data/socket constatés à chaque étape (couvre Q1-Q3, E1, E2).
  V3 : émulation de bout en bout avec tcp-07 : « patch » → état 1 + entrée
       basculée ; « rollback » → état 0 + entrée restaurée (couvre Q1).
  V4 : test de rejet : toute notation du bloc appelant un IAT autre que
       ReadFile est refusée (couvre I1).
Fixtures    : chaînes de commandes .rdata (« patch\r\n », « rollback\r\n »,
              « quit\r\n ») et chaînes de journal associées — copie unique
              référencée (D20).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D20, D33.
