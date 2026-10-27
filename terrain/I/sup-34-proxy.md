sup-34 · test T2 — proxy M3 (run terrain étape c) · révision 1
Intention : le run terrain que M3 attend (étape c de D47) : curl traverse
le proxy. Le superviseur lance proxy.exe avec TUYAUX (stdin/stdout captés),
lit la bannière, lance curl en HTTP simple puis en HTTPS CONNECT (tunnel),
vérifie les événements console DU PROXY (connexion entrante, tunnel, fin
connexion — la voix du proxy, pas celle de curl), envoie « quit » sur
stdin, vérifie « arret » et le code de sortie 0. Les pages reçues sont
comptées (octets) — jamais journalisées (ce qui traverse n'est pas à nous,
le proxy non plus : discipline M3, journal d'événements, pas d'octets).
Contrat :
  pre  : P1 proxy.exe présent (sinon S20 ABSENT + rax = 0) ; P2 curl.exe
         résoluble (composant système ; sinon S22 « curl.exe ABSENT » +
         proxy arrêté proprement + rax = 0) ; P3 port 25000 libre (sinon
         l'écoute proxy échouera — bannière d'erreur réseau visible dans
         le flux capté, verdict NON conforme) ; P4 pile alignée.
  post : Q1 lancement proxy.exe par sup-31 MODE 1 (tuyaux) ; Q2 bannière :
         sondage PeekNamedPipe (Sleep 50 ms, 300 essais = 15 s) puis
         ReadFile du disponible — 40 premiers octets == fixture
         "TRIADE M3 : proxy demarre (port 25000)\r\n" -> S21 ; sinon S21
         KO + fermeture (quit envoyé quand même, process fermé) + rax = 0 ;
         Q3 curl HTTP : cmdline "curl.exe -s --fail --max-time 20 -o
         terrain_page_http.txt -x http://127.0.0.1:25000
         http://neverssl.com/" -> attente (25 s) -> code -> S22 ; page
         lue (comptage EOF, <= 600 o gardés) -> S23 octets ; Q4 événements
         attendus : "connexion entrante\r\nfin connexion\r\n" (35 o
         exacts, sondage 15 s) — embarqués bruts ; Q5 curl HTTPS : même
         discipline (-x ... https://example.com/), code -> S24, octets ->
         S25, événements "connexion entrante\r\ntunnel\r\nfin
         connexion\r\n" (43 o exacts) embarqués ; Q6 arrêt : WriteFile
         "quit\r\n" (6 o) sur TUYAU_IN_WR, sondage « arret\r\n » (7 o),
         WaitForSingleObject (10 s) + GetExitCodeProcess -> S26 lignes
         (total des lignes captées : bannière + événements + arret) ;
         Q7 verdict : codes curl == 0, pages >= 1 octet, bannière exacte,
         2 + 3 événements exacts, arret exact, exit proxy == 0 -> S27
         conforme + S28 OK + rax = 1 ; sinon S27 NON conforme + S28 KO +
         rax = 0 (avec tout le flux capté embarqué : la dernière ligne
         visible localise l'intervalle, leçon demo.3) ; Q8 nettoyage :
         extrémités parent fermées, handle processus fermé, pages
         temporaires supprimées (DeleteFileA) — tout chemin.
  inv  : I1 les événements sont comparés par memcmp EXACT sur le flux
         brut (l'ordre des événements du proxy est séquentiel par
         construction — une connexion à la fois, la divergence est une
         trouvaille, pas un bruit) ; I2 rien du contenu des pages n'est
         journalisé (taille seule) ; I3 toutes les attentes bornées par
         timeout (PeekNamedPipe + Sleep) — aucun ReadFile bloquant sans
         garantie de disponibilité : le superviseur ne peut pas GELER ;
         I4 zéro fuite de handle (fermetures sur tout chemin, I3 de
         sup-31 complété).
Échecs :
  E1 : proxy muet (port occupé, intégrité KO) -> bannière divergeante
       captée + embarquée, verdict KO, arrêt propre tenté.
  E2 : curl absent -> S22 ABSENT, proxy fermé proprement (quit + attente),
       rax = 0.
  E3 : réseau terrain coupé -> curl code != 0 journalisé, événements
       manquants, verdict NON conforme (le constat veut exactement ça).
  E4 : proxy ne répond pas à quit -> WaitForSingleObject timeout ->
       TerminateProcess, verdict KO, flux embarqué.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation nominale COMPLÈTE — tuyaux scriptés : bannière 40 o,
       pages 1 268 / 1 256 octets, codes 0/0, événements exacts 35 o puis
       43 o, quit capté (« quit\r\n » écrit sur le tuyau stdin — le shim
       le prouve), « arret\r\n » servi, exit 0 -> séquence S20..S28 avec
       valeurs exactes (itoa), flux embarqué, rax = 1.
  V3 : curl code 22 (HTTP erreur) -> S22 code=22, verdict KO, rax = 0,
       le reste exécuté (pas de court-circuit : chaque test vit ses
       étapes pour le constat).
  V4 : événement tunnel manquant (43 o -> 27 o servis) -> S27 NON
       conforme, flux partiel embarqué, rax = 0.
  V5 : falsification — changer 43 en 42 fait échouer V2 ; changer le
       timeout d'arrêt (quit non écrit) fait échouer le verrou « quit
       écrit avant arret » de l'oracle.
Fixtures    : bannière 40 o, "connexion entrante\r\n" 20 o, "tunnel\r\n"
              8 o, "fin connexion\r\n" 15 o, "arret\r\n" 7 o, "quit\r\n"
              6 o, 2 cmdlines curl, noms des pages temporaires, lignes
              S20..S28.
Provenance  : écrite-avant-code.
Décisions   : D48 ; LISEZMOI-proxy.txt (procédure manuelle) transposée en
              machine ; curl en relais (D48 : composant système, comme
              ws2_32) ; pages comptées pas copiées (discipline M3).
