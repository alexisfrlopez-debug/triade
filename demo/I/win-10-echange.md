win-10 · échange réseau vérifié · révision 3
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
         I3 (R3) AUCUNE journalisation ici, ni verdict ni position : le
         bloc est muet, l'appelant journalise après retour — le journal
         nominal du scénario (11 lignes) capture toute ligne parasite ;
         I4 (R3) le tampon de réception [rsp+0x20, rsp+0x40) vit dans le
         cadre de pile du bloc, au-dessus du rsp de l'appelant ; socket
         (rbx), attendu (r12) et compteur (r13) en registres préservés —
         aucune donnée du bloc ne dépend d'un volatile à travers un appel
         (leçon D38).
Échecs :
  E1 : émission partielle impossible à compléter (send ≤ 0) — eax = 0.
  E2 : réception fermée ou divergente (recv ≤ 0, memcmp ≠ 0) — eax = 0.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims send/recv — trois appels successifs avec les trois
       attendus (identité, MAJUSCULES, identité) → 1, 1, 1 ; shim recv
       renvoyant une réponse divergente → 0 (couvre Q1-Q3, E1-E2) ; le
       journal du scénario appelant reste à EXACTEMENT 11 lignes (R3 :
       sondes retirées — une sonde oubliée ferait échouer l'oracle).
Fixtures    : PHRASE/PHRASE_MAJ (.rdata, partagées avec win-09) — RIEN
              d'autre (R3 : les chaînes de sondes SONDE_4/SONDE_5 sont
              retirées avec l'instrumentation, D43).
Provenance  : écrite-avant-code.
Décisions   : D7, D8 ; factorisation du motif triplicé de win-09 (leçon de
              style : une responsabilité par bloc, trois usages) ; D42
              (instrumentation bilatérale de l'échange — TEMPORAIRE) ;
              D43 (constat vert terrain demo.8 : sonde4/sonde5 lues autour
              de chacun des trois échanges — retrait, R3 final).

RÉVISION 2 (D42 — instrumentation client, TEMPORAIRE) : le journal terrain
demo.7 meurt sans ligne E5 après « client : connecté » — l'échange s'est
journalisé de l'EXTÉRIEUR (win-09 avant/après l'appel), laissant un intervalle
aveugle couvrant send, recv et memcmp. R2 ajoute sonde4 (boucle d'émission
complète — avant la première réception) et sonde5 (boucle de réception
complète — avant le memcmp) : la dernière sonde visible localise la mort à
l'instruction près côté client, en complément des sondes serveur S1/S2 de
win-08:R2. Le tampon de réception et les registres préservés traversent les
sondes intacts (I4) — le verdict memcmp reste exactement celui de R1.

RÉVISION 3 (D43 — retrait de l'instrumentation, FINALE de lignée) : le
journal terrain demo.8 a lu « sonde4 envoye ok »/« sonde5 recu ok » autour de
chacun des trois échanges (identité, MAJUSCULES après patch en production,
identité après retour arrière) puis « boucle § 5 complète — DÉMO OK » — le
bloc est ACQUITTÉ : émission et réception complètes prouvées au terrain,
verdict memcmp exact trois fois. R3 retire les 8 instructions des sondes 4/5
et rend au bloc son silence de R1 (I3) : la preuve de l'échange vit dans les
lignes J_ECHO_OK/J_PROD_OK/J_RB_OK du scénario, chacune derrière le verdict
1/0 de CE bloc — jamais ailleurs.
