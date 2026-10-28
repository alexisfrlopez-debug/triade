http-12 · orchestration du proxy · révision 2 — LE CÂBLAGE
Intention : la pièce exigée par le terrain (c) avant le scellage 0.5.0 —
l'orchestrateur scellé lance encore http-10:R1 @0x5580 (la session 0.4.0,
qui ne connaît pas le tunnel) ; la révision câble la boucle
d'acceptation sur http-10:R2 @0x74C0 (la session révisée D92 : routage
https → tls-08, 502 « certificat rejete ») et porte avec elle la porte
R10 .text3 : la table d'intégrité est PLEINE (27 entrées + terminateur
@0x2810, R_VERSION scellé @0x2820 immovable R7), l'entrée .text3 prend
la place du terminateur et la marche s'arrête à la BORNE — la couche
M4 entière devient gardée AU LANCEMENT (elle ne l'était qu'à la carte +
l'oracle + le verrou croisé depuis D94).
Ancêtre : http-12:R1 (D45, scellé 0.4.0 — spec m3/I/http-12-principal.md,
citée non recopiée T5 ; balise immuable § 9). La révision câble et
ferme, elle ne touche à RIEN d'autre : l'initialisation est l'héritage
octet pour octet (à la géométrie près du plan d'adressage).
Contrat :
  pre  : P1 le bloc est le point d'entrée PE de proxy.exe — DÉSORMAIS
             0x7DC0 (.text3, delta PE documenté ; l'ancêtre @0x1800 reste
             embarqué octet pour octet, R7, indexé par la carte — mort
             au lancement, vivant à la preuve d'héritage) ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16, convention
             chargeur) ;
         P3 l'état .data est à l'état image (handles nuls, drapeaux
             nuls, section critique NON initialisée) — repris de R1.
  post : Q1 [porte R10 RÉVISÉE] avant tout effet : la table .rdata est
             parcourue de R_TAB_SUM (0x2660) à la BORNE — l'adresse de
             R_VERSION (0x2820), JAMAIS son contenu — 28 entrées
             exactement (26 héritage + libc-07 + LA PORTE .text3
             [0x6000, 0x2000] @0x2810, l'ancien terminateur remplacé) ;
             pour CHAQUE entrée : rva nul → ÉCHEC, taille nulle →
             ÉCHEC (la table est PLEINE : un trou nomme une corruption —
             fail-closed renforcé, la troncature silencieuse du
             terminateur M3 n'existe plus), somme additive 64 bits des
             qwords du bloc visé == somme attendue (base d'image par
             ancre RIP-relative) ; puis version >= 0x00040000 (plancher
             M3 inchangé, monotonie anti-rollback) ; tout écart : ligne
             unique « TRIADE M3 : integrite KO, arret » par hello-02,
             ExitProcess(1), AUCUN appel réseau ;
         Q2 initialisation dans l'ordre — l'héritage R1 TEL QUEL :
             GetStdHandle(-11) puis (-10) cachés en .data,
             InitializeCriticalSection(R_CS) AVANT toute émission (D42),
             bannière, tcp-01 (écoute), thread console (tcp-06 sur
             http-11 @0x5D80), échecs → ExitProcess(2) avec journal ;
         Q3 boucle : tcp-02 (acceptation) ; socket valide → tcp-06 sur
             http-10:R2 (0x74C0) avec la socket en argument — LE
             CÂBLAGE, l'unique différence fonctionnelle avec R1 —,
             handle fermé, boucle ; acceptation en échec : R_QUIT posé
             → journal « arret », WSACleanup, ExitProcess(0) ; sinon →
             journal « erreur reseau, arret », ExitProcess(2) ;
         Q4 le processus se termine TOUJOURS par ExitProcess (0 arrêt
             demandé, 1 intégrité, 2 erreur structurale) — repris tel
             quel.
  inv  : I1 appels système : IAT kernel32 GetStdHandle,
             InitializeCriticalSection, ExitProcess, CloseHandle ; IAT
             ws2_32 WSACleanup ; appels directs : hello-02, tcp-01,
             tcp-02, tcp-06, tcp-11 ; cibles de CODE par lea (pointeurs
             de fonctions passés à tcp-06) : http-11 @0x5D80,
             http-10:R2 @0x74C0 — JAMAIS http-10:R1 (le contre-câblage
             est la falsification nominale de V4) ;
         I2 l'ordre d'initialisation de Q2 est un invariant (leçon
             D42) ; I3 la porte précède TOUT autre effet — la marche
             aux bornes comprise : la borne est une ADRESSE (R_VERSION
             @0x2820), jamais une lecture de version avant la fin de
             marche ; I4 handles de threads fermés immédiatement ;
         I5 la couche .text3 est gardée par SA PROPRE entrée dans la
             table (0x6000, 0x2000 — le bloc 0x7DC0 est DANS la plage
             gardée : la porte se garde elle-même, miroir de http-12:R1
             gardé par la table M3) ; aucun stockage sous rsp.
Échecs :
  E1 : intégrité KO (somme divergente, entrée trouée, version sous
       plancher) → ExitProcess(1) avant tout effet ;
  E2 : échec d'écoute ou de lancement de console → ExitProcess(2) ;
  E3 : acceptation en échec sans arrêt demandé → ExitProcess(2).
Vecteurs :
  V1 : round-trip de notation 100 % (R2 ET l'ancêtre R1 assemblé à
       0x1800 — le préalable du différentiel) ;
  V2 : différentiel d'ancêtre — R1 émulé contre R2 émulé sur les mêmes
       scénarios (démarrage nominal avec ordre exact Q2, intégrité
       corrompue squelette, version sous plancher, accepts successifs,
       quit, échecs E2/E3) : traces IDENTIQUES sauf la cible du spawn
       session (0x5580 → 0x74C0) — la divergence LÉGITIME unique ; la
       corruption .text3 diverge légitimement (R1 ne la garde pas, R2
       la nomme KO) — miroir du domaine https de D91 ;
  V3 : fuzz de la table R10 — toute mutation d'un champ d'entrée (rva,
       taille, somme) ou tout octet retourné dans une plage gardée →
       KO, jamais de passage silencieux (la propriété est calculée par
       le modèle de marche, jamais par la notation) ;
  V4 : falsification — mutations d'un point stables en taille (leçon
       D82) attrapées : le contre-câblage (lea → 0x5580), la borne
       décalée (±0x10 — l'entrée .text3 sautée ou la version lue comme
       entrée), le plancher abaissé, l'ordre d'initialisation, le code
       de sortie E3, le sens du test d'arrêt ; témoin vert.
Fixtures    : héritage R7 intégral (bannière 40 o, « erreur reseau,
              arret » 22 o, « arret » 7 o, ligne KO 33 o — aucunes
              nouvelles) ; l'entrée R10 .text3 est propriété du build
              (somme recalculée du binaire final, table générée).
Provenance  : écrite-avant-code (D95).
Décisions   : D8, D42, D45, D63, D77, D94, D95.
