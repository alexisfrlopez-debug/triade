win-10 · échange réseau vérifié · révision 2
Intention : UNE responsabilité réutilisée trois fois par le scénario — envoyer
la phrase d'échange (13 octets, boucle d'émission complète), recevoir la
réponse (13 octets, boucle de réception cumulative), puis la comparer octet à
octet à l'attendu par le memcmp scellé M1 ; le verdict est binaire et honnête.
Contrat :
  pre  : P1 rcx = socket cliente connectée ; P2 rdx pointe l'attendu ASCII de
         13 octets (.rdata : PHRASE ou PHRASE_MAJ) ; P3 WSA actif, serveur en
         écoute ; P4 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 succès : eax = 1 — la phrase a été intégralement émise, 13 octets
         reçus, reçus == attendu (memcmp scellé) ; Q2 échec (émission ≤ 0,
         réception ≤ 0 ou divergence) : eax = 0, socket laissée ouverte (la
         politique de fermeture appartient à l'appelant, Q4 de win-09) ;
         Q3 tampon de réception dans le cadre de pile, aucun .data touché.
  inv  : I1 appels : memcmp scellé (b20002) en direct, send/recv par IAT
         ws2_32 (mêmes slots que tcp-09) ; I2 la phrase émise est TOUJOURS
         PHRASE (minuscules) — c'est la RÉPONSE qui change avec l'état du
         patch : le bloc ne connaît pas la version active du serveur, il
         constate (le patch est l'affaire de tcp-07, pas de l'échange) ;
         I3 aucune journalisation de VERDICT ici (l'appelant journalise
         après verdict) — les sondes R2 journalisent des POSITIONS (émission
         complète / réception complète), jamais un succès non prouvé ;
         I4 les sondes appellent l'entrée trace de win-05 (0x5000) avec
         rcx/rdx/r8 volatils — le tampon de réception [rsp+0x20, rsp+0x40)
         vit AU-DESSUS du rsp de l'appelant, hors de portée du cadre du
         callee ; rbx/r12/r13 (socket, attendu, compteur) survivent aux
         sondes (préservés par win-05).
Échecs :
  E1 : émission partielle impossible à compléter (send ≤ 0) — eax = 0.
  E2 : réception fermée ou divergente (recv ≤ 0, memcmp ≠ 0) — eax = 0.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims send/recv — trois appels successifs avec les trois
       attendus (identité, MAJUSCULES, identité) → 1, 1, 1 ; shim recv
       renvoyant une réponse divergente → 0 (couvre Q1-Q3, E1-E2) ; les
       sondes 4/5 apparaissent dans le journal à chaque échange (fichier +
       écran, six lignes au nominal des trois échanges).
Fixtures    : PHRASE/PHRASE_MAJ (.rdata, partagées avec win-09) ; chaînes
              de sondes SONDE_4/SONDE_5 (.rdata, zone libre M2 0x266E-0x26D8,
              jamais lue par le chargeur — D42).
Provenance  : écrite-avant-code.
Décisions   : D7, D8 ; factorisation du motif triplicé de win-09 (leçon de
              style : une responsabilité par bloc, trois usages) ; D42
              (instrumentation bilatérale de l'échange — TEMPORAIRE,
              retirée en R3 après constat vert terrain).

RÉVISION 2 (D42 — instrumentation client, TEMPORAIRE) : le journal terrain
demo.7 meurt sans ligne E5 après « client : connecté » — l'échange s'est
journalisé de l'EXTÉRIEUR (win-09 avant/après l'appel), laissant un intervalle
aveugle couvrant send, recv et memcmp. R2 ajoute sonde4 (boucle d'émission
complète — avant la première réception) et sonde5 (boucle de réception
complète — avant le memcmp) : la dernière sonde visible localise la mort à
l'instruction près côté client, en complément des sondes serveur S1/S2 de
win-08:R2. Le tampon de réception et les registres préservés traversent les
sondes intacts (I4) — le verdict memcmp reste exactement celui de R1.

