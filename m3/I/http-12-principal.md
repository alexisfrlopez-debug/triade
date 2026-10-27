http-12 · orchestration du proxy · révision 1
Intention : le point d'entrée de proxy.exe — d'abord la porte R10
(intégrité de TOUS les blocs scellés embarqués et monotonie de version,
AVANT tout effet réseau), puis l'initialisation DANS L'ORDRE CONTRACTUEL
(handles, section critique EN TÊTE — leçon D42, WSA/écoute, thread
console), puis la boucle d'acceptation : chaque connexion reçoit son
thread session http-10 ; l'arrêt demandé ou tout échec structural
termine proprement avec un code distinct.
Contrat :
  pre  : P1 le bloc est le point d'entrée PE de proxy.exe ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16, convention
             chargeur) ;
         P3 l'état .data est à l'état image (handles nuls, drapeaux
             nuls, section critique NON initialisée).
  post : Q1 [porte R10] AVANT tout appel ws2_32, tout appel de journal et
             toute pose de handle : la table d'intégrité .rdata est
             parcourue — pour chaque entrée de taille non nulle, la somme
             additive 64 bits des qwords du bloc visé (base d'image par
             ancre RIP-relative, entrées en RVA) doit égaler la somme
             attendue, et le qword version .rdata doit être >=
             0x00040000 (plancher M3, monotonie anti-rollback) ; tout
             écart : ligne unique « TRIADE M3 : integrite KO, arret »
             émise par hello-02 directement, ExitProcess(1), AUCUN appel
             réseau ;
         Q2 initialisation dans l'ordre : GetStdHandle(-11) puis (-10)
             cachés en .data, InitializeCriticalSection(R_CS) — AVANT
             toute émission de journal (D42 : l'ordre est un contrat, la
             section critique précède ses utilisateurs), journal de la
             bannière « TRIADE M3 : proxy demarre (port 25000) », tcp-01
             (écoute au port 25000 — socket posée en .data R_LISTEN)
             avec échec → journal « erreur reseau, arret » et
             ExitProcess(2), lancement du thread console (tcp-06 sur
             http-11) avec échec identique, handle fermé immédiatement
             après restitution ;
         Q3 boucle : tcp-02 (acceptation) ; socket valide → journal
             « connexion entrante » délégué à http-10 (Q6 de sa spec),
             tcp-06 sur http-10 avec la socket en argument, handle
             fermé, boucle ; acceptation en échec : si le drapeau R_QUIT
             est posé → journal « arret », ExitProcess(0) ; sinon →
             journal « erreur reseau, arret », ExitProcess(2)
             (fail-closed : un serveur qui ne peut plus accepter refuse
             tout) ;
         Q4 le processus se termine TOUJOURS par ExitProcess (0 arrêt
             demandé, 1 intégrité, 2 erreur structurale) — les threads
             session sont drainés par le système (miroir tcp-12:Q4) ;
             WSACleanup est appelé avant ExitProcess(0) uniquement (sur
             le chemin propre — les chemins d'erreur terminent sans
             cérémonie).
  inv  : I1 appels système : IAT kernel32 GetStdHandle,
             InitializeCriticalSection, ExitProcess, CloseHandle ; IAT
             ws2_32 WSACleanup ; appels directs : hello-02 (écriture
             directe de la ligne d'intégrité), libc-02 (comparaison de
             la version plancher), tcp-01, tcp-02, tcp-06, tcp-11 ;
         I2 l'ordre d'initialisation de Q2 est un invariant : handle →
             section critique → bannière → écoute → console ; toute
             permutation qui existerait dans la notation est un défaut
             (leçon D42 : le devoir d'initialisation de l'hôte) ;
         I3 la porte R10 précède TOUT autre effet (aucune écriture .data
             avant elle, hors son propre cadre) ; I4 les handles de
             threads sont fermés immédiatement (jamais conservés —
             miroir tcp-12) ; I5 aucun stockage sous rsp.
Échecs :
  E1 : intégrité KO → ExitProcess(1) avant tout effet (fail-closed
       explicite, R10 renforcée) ;
  E2 : échec d'écoute ou de lancement de console → ExitProcess(2) avec
       journal ;
  E3 : acceptation en échec sans arrêt demandé → ExitProcess(2)
       (disponibilité refusée plutôt que dégradée).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation complète (oracle, shims) : démarrage nominal (ordre
       exact des appels Q2 constaté — GetStdHandle AVANT
       InitializeCriticalSection AVANT la première écriture journal),
       intégrité corrompue (un octet de bloc retourné → ligne KO,
       ExitProcess(1), zéro appel réseau), version sous plancher → KO,
       accept successifs (sessions http-10 lancées avec la socket
       exacte), quit (drapeau + fermeture d'écoute → accept en échec →
       ExitProcess(0)), échec accept hors quit → ExitProcess(2)
       (couvre P1-P3, Q1-Q4, I1-I5, E1-E3).
  V3 : test de rejet : toute notation dont l'ordre d'initialisation
       viole I2, ou appelant un IAT hors I1, est refusée (couvre I1,
       I2).
Fixtures    : bannière « TRIADE M3 : proxy demarre (port 25000) », ligne
              d'intégrité « TRIADE M3 : integrite KO, arret », « erreur
              reseau, arret », « arret » (chaînes .rdata — copie unique,
              discipline tcp-12) ; table d'intégrité .rdata (une entrée
              par bloc scellé embarqué — générée par le build, propriété
              de la carte).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D19, D42, D45, D46.
