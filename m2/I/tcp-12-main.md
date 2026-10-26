tcp-12 · orchestration du serveur écho · révision 1
Intention : le point d'entrée d'echo.exe — d'abord la porte R10 (contrôle
d'intégrité de TOUS les blocs scellés embarqués et monotonie de version,
AVANT tout effet réseau), puis l'initialisation (handles, section critique,
WSA, écoute, thread console), puis la boucle d'acceptation : chaque
connexion reçoit son thread ; l'arrêt demandé (drapeau quit posé par
tcp-10) ou tout échec structural termine proprement avec un code distinct.
Contrat :
  pre  : P1 le bloc est le point d'entrée PE d'echo.exe ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16, convention
             chargeur) ;
         P3 l'état .data est à l'état image (handles nuls, drapeaux nuls,
             version active v1) — la section critique n'est PAS encore
             initialisée.
  post : Q1 [porte R10] AVANT tout appel ws2_32, tout appel de journal et
             toute pose de handle : la table d'intégrité .rdata est parcourue
             — pour chaque entrée de taille non nulle, la somme additive 64
             bits des qwords du bloc visé (base d'image calculée par ancre
             RIP-relative, entrées en RVA — image position-indépendante)
             doit égaler la somme attendue, et le qword version .rdata doit
             être >= 0x00030000 (monotonie, anti-rollback) ; tout écart :
             ligne unique « TRIADE M2 : integrite KO, arret » émise par
             hello-02 directement (la section critique n'existe pas encore),
             ExitProcess(1), AUCUN appel réseau ;
         Q2 initialisation dans l'ordre : GetStdHandle(-11) puis (-10)
             cachés en .data, InitializeCriticalSection(R_CS), journal de la
             bannière « TRIADE M2 : serveur echo demarre (port 25000) »
             (une ligne), tcp-01 (écoute) avec échec → journal « erreur
             reseau, arret » et ExitProcess(2), lancement du thread console
             (tcp-06 sur tcp-10) avec échec identique, handles de threads
             fermés immédiatement après restitution ;
         Q3 boucle : tcp-02 (acceptation) ; socket valide → journal
             « connexion entrante », tcp-06 sur tcp-09 avec la socket en
             argument, handle fermé, boucle ; acceptation en échec : si le
             drapeau quit est posé → journal « arret », ExitProcess(0) ;
             sinon → journal « erreur reseau, arret », ExitProcess(2)
             (fail-closed : un serveur qui n'accepte plus refuse tout) ;
         Q4 le processus se termine TOUJOURS par ExitProcess (0 arrêt
             demandé, 1 intégrité, 2 erreur structurale) — les threads
             serviteurs sont terminés par le système (drainage des
             connexions en cours reporté, limite M2 documentée).
  inv  : I1 appels système : IAT kernel32 GetStdHandle,
             InitializeCriticalSection, CloseHandle, ExitProcess ;
             appels directs : tcp-01, tcp-02, tcp-06, tcp-11, hello-02,
             hello-03 ;
         I2 la porte R10 précède STRICTEMENT tout appel de I1 autre que
             rien : le premier GetStdHandle suit la porte (la ligne d'échec
             de Q1 utilise GetStdHandle APRÈS le verdict négatif — c'est un
             chemin d'arrêt, pas le chemin d'exécution) ;
         I3 le prologue alloue 0x60 octets et sauvegarde rbx, r12-r15 ;
             l'épilogue restaure symétriquement (le bloc ne retourne jamais
             — il sort par ExitProcess) ;
         I4 aucun stockage sous rsp ; la loge [rsp+0x20] sert d'argument 5
             aux appels de journal ;
         I5 la table d'intégrité et la version sont lues en RVA + base
             (ancre RIP-relative) : aucune adresse absolue n'est chargée —
             l'image reste indépendante en position (aucune relocalisation
             réelle nécessaire, D33).
Échecs :
  E1 : intégrité douteuse (Q1) → arrêt immédiat code 1 avant tout effet :
       c'est la clause R10 — mieux vaut un serveur mort qu'un serveur
       corrompu.
  E2 : erreur structurale (WSA, écoute, thread, acceptation hors arrêt
       demandé) → arrêt code 2 après journal : fail-closed assumé.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation du binaire ENTIER (oracle, shims) : chemin nominal —
       bannière exacte, écoute dressée, thread console lancé, une connexion
       acceptée (journal + thread connexion lancé), arrêt demandé (drapeau
       + acceptation en échec) → « arret », ExitProcess(0) ; chemins
       d'échec — WSA/socket en échec → code 2 ; acceptation en échec sans
       quit → code 2 (couvre Q2-Q4, E2).
  V3 : porte R10 : corruption d'UN octet quelconque d'un bloc embarqué →
       sortie « integrite KO » et code 1, AUCUN appel ws2_32 constaté ;
       version < plancher → idem (couvre Q1, E1 — falsification R10).
  V4 : test de rejet : toute notation du bloc touchant ws2_32 avant la
       porte R10, ou chargeant une adresse absolue, est refusée (couvre I2,
       I5).
Fixtures    : table d'intégrité et qword version .rdata (calculées par le
              builder, scellées dans l'image) ; chaînes de journal .rdata.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33 ; R10 (porte au lancement), R7 (base par ancre).
