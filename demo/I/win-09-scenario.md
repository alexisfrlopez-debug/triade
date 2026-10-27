win-09 · scénario complet (thread de démonstration) · révision 4
Intention : LA démonstration en un clic — exécuter séquentiellement, en les
journalisant ligne à ligne : la porte R10 et les vecteurs libc (win-06), la
mécanique de patch à chaud hors réseau (tcp-07 bascule/rollback + effet v1→v2→v1
constaté par memcmp sur le bloc écho), puis la boucle § 5 EN PRODUCTION :
serveur (win-08) lancé dans son thread, client (win-07) connecté, échange
identité vérifié octet à octet, patch APPLIQUÉ PENDANT LE TRAFIC, réponse en
MAJUSCULES reçue et vérifiée, retour arrière et re-vérification, arrêt propre
(fermeture client, R_QUIT armé, écoute fermée). Chaque étape échoue PROPREMENT
(ligne d'échec + arrêt du scénario) : aucune fausse bannière de succès.

RÉVISION 4 (D43 — retrait de l'instrumentation mécanique, FINALE de lignée) :
le journal terrain demo.8 a fermé la boucle — 28/28 lignes jusqu'à « boucle
§ 5 complète — DÉMO OK », sondes 1/2/3 vertes, S1/S2 lues, sonde4/sonde5
autour de chacun des trois échanges. L'instrumentation D40/D42 a rempli son
devoir (trois défauts nommés en trois runs : DEP D39, zone d'accueil ABI D41,
section critique D42) et est retirée : R4 enlève les 12 instructions des
sondes 1/2/3 — le scénario journalise EXACTEMENT ses 11 lignes de preuve
(J_ENTETE → J_FINAL), chacune derrière un memcmp. Le correctif D42 (I0, init
R_CS en tête) RESTE : c'est un devoir d'héritage, pas une sonde — l'oracle le
garde par contrôle post-run du shim à état et par falsification V9 (tcp-09
sur CS vierge DOIT fauter).

RÉVISION 3 (D42 — reprise du devoir d'héritage de tcp-12) : le journal
terrain demo.7 franchit toute la mécanique (sondes 3/3, v1>v2>v1, serveur en
écoute, client connecté) puis meurt VIOLEMMENT sans ligne d'échec dans le
premier échange réseau. Diagnostic statique : la section critique R_CS
(0x3830, .data) — exigée par la pre-condition P5 de tcp-11 (journal console,
appelé par le fil d'écho tcp-09 à chaque réception) — est ZÉRO dans l'image
et JAMAIS initialisée : dans echo.exe, ce devoir appartenait à tcp-12-main
(NON embarqué dans la démo, remplacé par win-01/win-04) ; l'hôte démo a
repris le caching des handles (P4) mais pas la section critique. Sur
Windows 10/11, EnterCriticalSection sur une CS vierge (LockCount = 0 =
« verrouillée » au lieu de -1 « libre », OwningThread = 0) emprunte le
chemin de contention et termine en exception non gérée dans ntdll — le fil
d'écho meurt, le processus ENTIER meurt avec lui, la fenêtre disparaît sans
qu'aucune ligne n'ait pu être écrite : exactement le constat terrain. 8e
classe de défaut : pré-condition d'état hérité non reprise par l'hôte lors
du retrait d'un bloc orchestrateur scellé — invisible à l'oracle dont les
shims de section critique étaient sans état (D42 durcit : Enter sur CS
vierge DOIT fauter). R3 ajoute l'initialisation en tête de scénario, AVANT
tout spawn : InitializeCriticalSection(R_CS) par IAT kernel32 — le miroir
exact du devoir de tcp-12, placé le plus tôt possible du fil qui orchestre
toute la démonstration.
Contrat :
  pre  : P1 appelé une fois par win-04 (tcp-06, arg 0), la fenêtre et le
         journal existent ; P2 pile alignée ; P3 WSA non encore initialisé au
         démarrage du scénario (le serveur le fera) ; P4 les handles
         stdout/stdin sont mis en cache en .data (R_STDOUT/R_STDIN) dès
         l'entrée — lancé depuis une console, le journal serveur hérité
         (tcp-11) y paraît ; sans console, WriteFile échoue silencieusement
         (GUI, E3 de tcp-11) ; P5 la section critique R_CS est initialisée
         AVANT tout spawn de fil journalisant via tcp-11 (I0, D42).
  post : Q1 chaque étape franchie n'est journalisée qu'après sa vérification
         (memcmp exact — jamais de succès déclaré non prouvé) ; le journal
         nominal compte EXACTEMENT 11 lignes (R4 : les sondes sont
         retirées — toute ligne parasite fait échouer l'oracle) ; Q2
         mécanique : trois appels au bloc écho par SON ENTRÉE 0x4600
         (avant/après patch/après rollback) avec memcmp contre les attendus
         "salut triade\r\n"/"SALUT TRIADE\r\n" ; Q3 réseau : échanges
         complets (boucles send/recv cumulatives, miroir tcp-09), chaque
         réponse vérifiée par memcmp avant journalisation ; Q4 arrêt propre
         garanti sur TOUT chemin de sortie : si socket cliente ouverte →
         tcp-05 ; R_QUIT = 1 ; si écoute ouverte → tcp-05 ; le thread
         retourne 0 ; Q5 rax = 0 sur tout chemin (le verdict vit dans le
         journal).
  inv  : I0 (D42) InitializeCriticalSection(R_CS) est le PREMIER appel du
         scénario — avant GetStdHandle, avant tout journal, avant tout
         spawn : l'état hérité exigé par les blocs scellés (P5 tcp-11)
         existe avant que quelque fil que ce soit puisse y toucher ;
         I1 appels directs : win-05 (journal), win-06 (autotest), win-07
         (client), tcp-07 (patch), tcp-05 (close), bloc écho 0x4600,
         b20002 (memcmp) ; I2 send/recv par IAT ws2_32 directe (mêmes slots
         que tcp-09) ; I3 GetStdHandle, InitializeCriticalSection et
         CloseHandle seules IAT kernel32 ; I4 tampons sur pile (phrase 16 o,
         reçu 32 o), aucune écriture .data hors slots hérités + drapeaux
         GUI ; I5 le poll d'attente serveur est borné (40 M itérations max —
         pas de thread zombie bloqué).
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
       EXACTEMENT la séquence attendue (11 lignes au nominal — R4 : sondes
       retirées, toute ligne parasite = échec) ; le patch s'exécute
       RÉELLEMENT en émulation (VirtualProtect shim, memcpy scellé, qword
       de bascule écrit à 0x4600, trampoline exécuté vers 0x4680) ;
       rollback idem ; l'arrêt propre Q4 constaté (closesocket × 2,
       R_QUIT) ; la CS initialisée est CONSTATÉE par le shim à état (D42 :
       le scénario sans init échoue au contrôle post-run).
  V3 : falsification : corruption d'un octet de chaque bloc embarqué →
       détection quelque part (porte, vecteur, divergence de journal) —
       zéro silence (batterie exhaustive de l'oracle démo).
  V9 (D42) : tcp-09 exécuté sur CS VIERGE → EnterCriticalSection FAUTE —
       le défaut terrain demo.7 rejoué (8e classe) ; toute régression du
       correctif (init absente du scénario) est détectée par le contrôle
       post-run du shim à état.
Fixtures    : .rdata — "salut triade\r\n" (13 o), "SALUT TRIADE\r\n" (13 o),
              lignes du journal (UTF-16, 11 chaînes J_*) ; RIEN d'autre
              (R4 : les chaînes de sondes D40/D42 sont retirées, les
              interstices et la zone libre M2 qui les portaient reviennent
              à zéro).
Provenance  : écrite-avant-code.
Décisions   : D5, D7, D33, D35 ; R4 (contrat stable du bloc écho), boucle § 5 ;
              D40 (instrumentation temporaire — slot 0x380 → 0x3C0, trou libre
              0x4F80-0x4FFF, aucun bloc voisin déplacé) ; D41 (sondes
              conservées pour la lecture terrain du correctif) ; D42
              (correctif : reprise du devoir P5 de tcp-11 — init CS en tête
              de scénario) ; D43 (constat vert terrain demo.8 : 28/28 lignes
              « DÉMO OK » — retrait de TOUTES les sondes, R4 final ; le
              correctif D42 reste vivant, gardé par V9 et le contrôle
              post-run).
