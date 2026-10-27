http-09 · pompe unidirectionnelle · révision 1
Intention : pomper des octets d'une socket source vers une socket
destination jusqu'à la fin — la brique de relais du tunnel et de la
réponse — SANS JAMAIS fermer une socket (la fermeture appartient à la
session, http-10, miroir exact de la discipline tcp-06:Q4 sur les handles)
et sans jamais perdre un octet sur émission partielle.
Contrat :
  pre  : P1 rcx contient la socket source (connectée, bloquante — la
             sémantique bloquante est portée par l'appelant) ;
         P2 rdx contient la socket destination (connectée, bloquante) ;
         P3 r8 pointe le tampon d'attente (pile du thread appelant), r9
             contient sa capacité (u64 > 0 — la taille de lecture est la
             capacité, jamais au-delà) ;
         P4 les deux sockets restent ouvertes pendant tout l'appel — la
             fermeture concurrente par le propriétaire (http-10) est un
             chemin d'échec NOMMÉ, pas une violation ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 boucle : n = tcp-03 (recv, capacité du tampon) ; n > 0 →
             émission INTÉGRALE par tcp-04 en boucle (les envois partiels
             sont rejoués jusqu'à n total — miroir de tcp-09:Q1), total
             pompé cumulé ; n = 0 → rax = 0 (fin normale : le pair a
             fermé proprement) ; n = -1 → rax = 1 (erreur source) ;
         Q2 échec d'émission (tcp-04 en échec) → rax = 2 (erreur
             destination) : la boucle s'arrête immédiatement, sans
             reprise, sans fermeture ;
         Q3 rdx = total des octets pompés (u64, sur tout verdict) ;
         Q4 AUCUNE socket n'est fermée par ce bloc (ni source, ni
             destination, jamais — tcp-05 n'est PAS dans les appels
             autorisés) : la fermeture de chaque socket arrive exactement
             une fois, par http-10, dans le thread session.
  inv  : I1 appels directs : tcp-03 (réception), tcp-04 (émission) —
             AUCUN autre, aucun IAT ; I2 le tampon est celui de l'appelant
             (aucune allocation propre — le cadre du bloc est ABI
             uniquement) ; I3 les compteurs vivent dans les non-volatils
             sauvegardés (socket, envoyé, total) ; I4 aucun stockage sous
             rsp ; I5 le bloc rend la main sur le premier verdict
             tranchant — aucune boucle sans progression garantie (chaque
             itération reçoit au moins un octet ou retourne).
Échecs :
  E1 : verdict 1 (erreur source) ou 2 (erreur destination) → la session
       (http-10) ferme les deux sockets et termine : une pompe morte
       n'interrompt jamais l'autre branche du tunnel par elle-même.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shims recv/send scriptés) :
       5 000 scénarios (flux 1/N octets, émissions partielles 3+2+1,
       fin en EOF, erreur source en cours, erreur destination au k-ième
       envoi, zéro octet reçu — verdict immédiat 0) — verdict, total
       exact, ordre des appels, AUCUN closesocket constaté (couvre P1-P5,
       Q1-Q4, I1-I5).
  V3 : fuzz P1-P5 avec shims réseau non fiables (D45) : réceptions
       tronquées, émissions capricieuses — survie, terminaison, aucune
       fermeture de socket, aucun octet inventé (l'émission est
       l'exacte concaténation des réceptions) (couvre Q1-Q3).
  V4 : test de rejet : toute notation appelant tcp-05, un IAT, ou
       écrivant hors du tampon d'appelant est refusée (couvre I1, I2).
Fixtures    : néant (les flux viennent des shims de l'oracle).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D45, D46.
