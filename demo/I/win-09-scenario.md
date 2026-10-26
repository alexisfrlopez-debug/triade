win-09 · scénario complet (thread de démonstration) · révision 2
Intention : LA démonstration en un clic — exécuter séquentiellement, en les
journalisant ligne à ligne : la porte R10 et les vecteurs libc (win-06), la
mécanique de patch à chaud hors réseau (tcp-07 bascule/rollback + effet v1→v2→v1
constaté par memcmp sur le bloc écho), puis la boucle § 5 EN PRODUCTION :
serveur (win-08) lancé dans son thread, client (win-07) connecté, échange
identité vérifié octet à octet, patch APPLIQUÉ PENDANT LE TRAFIC, réponse en
MAJUSCULES reçue et vérifiée, retour arrière et re-vérification, arrêt propre
(fermeture client, R_QUIT armé, écoute fermée). Chaque étape échoue PROPREMENT
(ligne d'échec + arrêt du scénario) : aucune fausse bannière de succès.

RÉVISION 2 (D40 — instrumentation mécanique, TEMPORAIRE) : le journal terrain
demo.5 (10 lignes) gèle encore après « libc M1 scellée : 4/4 verts » alors que
l'audit octet (brouillons, notation, binaire) et l'oracle différentiel (79 cas
verts, permissions réellement appliquées) sont sans défaut — la mort est une
6e classe de défaut invisible sans exécution terrain, localisée quelque part
entre la fin du journal libc et J_MEC_OK. R2 ajoute TROIS SONDES de trace
(win-05 entrée trace, mode 0) qui encadrent exactement chaque étape non
encore exécutée sur le terrain : sonde1 avant le premier appel écho (entrée
mécanique), sonde2 après le retour 0 du patch pose (tcp-07 mode 0 COMPLET),
sonde3 après la vérification memcmp de l'écho patché (v2 confirmé). Chaque
sonde écrit le fichier journal AVANT l'étape suivante : la dernière sonde
visible localise l'instruction mortelle à un intervalle de quelques octets.
Les sondes seront retirées (R3) une fois le défaut identifié et corrigé.
Contrat :
  pre  : P1 appelé une fois par win-04 (tcp-06, arg 0), la fenêtre et le
         journal existent ; P2 pile alignée ; P3 WSA non encore initialisé au
         démarrage du scénario (le serveur le fera) ; P4 les handles
         stdout/stdin sont mis en cache en .data (R_STDOUT/R_STDIN) dès
         l'entrée — lancé depuis une console, le journal serveur hérité
         (tcp-11) y paraît ; sans console, WriteFile échoue silencieusement
         (GUI, E3 de tcp-11).
  post : Q1 chaque étape franchie n'est journalisée qu'après sa vérification
         (memcmp exact — jamais de succès déclaré non prouvé) ; les sondes R2
         ne journalisent que des FAITS (position d'exécution / retours
         vérifiés), jamais un succès non prouvé ; Q2 mécanique :
         trois appels au bloc écho par SON ENTRÉE 0x4600 (avant/après
         patch/après rollback) avec memcmp contre les attendus "salut
         triade\r\n"/"SALUT TRIADE\r\n" ; Q3 réseau : échanges complets
         (boucles send/recv cumulatives, miroir tcp-09), chaque réponse
         vérifiée par memcmp avant journalisation ; Q4 arrêt propre garanti
         sur TOUT chemin de sortie : si socket cliente ouverte → tcp-05 ;
         R_QUIT = 1 ; si écoute ouverte → tcp-05 ; le thread retourne 0 ;
         Q5 rax = 0 sur tout chemin (le verdict vit dans le journal).
  inv  : I1 appels directs : win-05 (journal), win-06 (autotest), win-07
         (client), tcp-07 (patch), tcp-05 (close), bloc écho 0x4600,
         b20002 (memcmp) ; I2 send/recv par IAT ws2_32 directe (mêmes slots
         que tcp-09) ; I3 GetStdHandle seule autre IAT (cache P4) ; I4
         tampons sur pile (phrase 16 o, reçu 32 o), aucune écriture .data
         hors slots hérités + drapeaux GUI ; I5 le poll d'attente serveur
         est borné (40 M itérations max — pas de thread zombie bloqué).
Échecs :
  E1 : porte R10 KO (win-06 = -1) — ligne dédiée, arrêt : rien d'autre ne
       s'exécute (fail-closed au chargement, R10).
  E2 : vecteur libc en échec — ligne dédiée, arrêt.
  E3 : patch refusé (tcp-07 ≠ 0 : état incohérent, staging corrompu…) —
       ligne dédiée, arrêt (jamais de bascule non prouvée).
  E4 : serveur impossible (port occupé / tcp-01 échoue / timeout d'attente)
       — ligne dédiée (la cause lisible), arrêt réseau, nettoyage Q4.
  E5 : client ou échange en échec (connect, send ≤ 0, recv ≤ 0, memcmp
       divergent) — ligne dédiée, nettoyage Q4, arrêt.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation complète : shims réseau (recv scripté REFLET de l'état réel
       du patch : identité / majuscules selon R_ETAT_PATCH — la cohérence
       bascule→réponse est ainsi prouvée) ; le journal capturé doit être
       EXACTEMENT la séquence attendue (14 lignes au nominal : 11 + les 3
       sondes R2 intercalées après J_LIBC_OK) ; le patch
       s'exécute RÉELLEMENT en émulation (VirtualProtect shim, memcpy scellé,
       qword de bascule écrit à 0x4600, trampoline exécuté vers 0x4680) ;
       rollback idem ; l'arrêt propre Q4 constaté (closesocket × 2, R_QUIT).
  V3 : falsification : corruption d'un octet de chaque bloc embarqué →
       détection quelque part (porte, vecteur, divergence de journal) —
       zéro silence (batterie exhaustive de l'oracle démo).
Fixtures    : .rdata — "salut triade\r\n" (13 o), "SALUT TRIADE\r\n" (13 o),
              lignes du journal (UTF-16) ; sondes R2 en ASCII dans les
              interstices libres (0x2748/0x276C/0x22F1, jamais lus par le
              chargeur ni les INT/IAT) : "sonde1 avant echo" (17 o),
              "sonde2 patch pose" (17 o), "sonde3 v2 ok" (12 o).
Provenance  : écrite-avant-code.
Décisions   : D5, D7, D33, D35 ; R4 (contrat stable du bloc écho), boucle § 5 ;
              D40 (instrumentation temporaire — slot 0x380 → 0x3C0, trou libre
              0x4F80-0x4FFF, aucun bloc voisin déplacé).
