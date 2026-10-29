sup-33 · test T1 — démo M2 (regression scellée) · révision 2
Intention : rejouer la démo M2 SANS main humaine : lancer demo.exe, trouver
sa fenêtre (classe "TRIADE_demo" — la nôtre s'appelle autrement, V4 de
sup-02), cliquer SON bouton « TOUT DÉMARRER » à sa place (BM_CLICK),
attendre la fin du scénario en SONDANT le journal (le marqueur final
« boucle § 5 complète - DÉMO OK » — pas de sommeil fixe : la fin est un
ÉVÉNEMENT, pas une durée), fermer proprement (WM_CLOSE), lire le journal
complet, le VÉRIFIER (17 lignes exactes, dernière ligne = fixture) et
l'EMBARQUER dans le journal du superviseur (le constat § 8.4 veut les
preuves brutes, pas un résumé).
Contrat :
  pre  : P1 demo.exe présent à côté du superviseur (sinon chemin
         d'échec F1 journalisé « S10 T1 demo.exe ABSENT ») ; P2 pile
         alignée ; P3 journal (win-05) opérationnel.
  post : Q1 lancement par sup-31 (mode 0, cmdline "demo.exe") ; échec ->
         S10 ABSENT + rax = 0 ; Q2 fenêtre cherchée par FindWindowW
         ("TRIADE_demo", NULL) — la CLASSE en premier argument, NULL en
         second (le contrat Win32 : lpClassName = rcx, lpWindowName = rdx —
         la fenêtre démo porte la classe "TRIADE_demo" et le titre
         "TRIADE M2 — démonstration complète" : chercher le titre rend
         NULL à jamais, la régression R1/terrain.17) — avec re-sondage
         (Sleep 50 ms, 200 essais = 10 s) :
         trouvée -> S11 ; introuvable -> S11 timeout + TerminateProcess +
         CloseHandle + rax = 0 ; Q3 bouton = FindWindowExW(fenêtre, 0,
         "BUTTON", 0) ; BM_CLICK envoyé par SendMessageTimeoutW (SMTO_
         ABORTIFHUNG, 90 s) : délivré -> S12 ; timeout -> S12 KO +
         TerminateProcess + nettoyage + rax = 0 ; Q4 boucle de sondage du
         journal : chemin construit dans TAMPON_CMD (répertoire de l'exe +
         "demo_journal.txt"), relecture complète à chaque tour (Open +
         ReadFile jusqu'à EOF, <= 640 o, Close), test « fin == fixture
         finale (31 o : ligne + CRLF) » — succès dès que le marqueur est
         posé (Sleep 200 ms entre tours, 150 tours = 30 s) ; Q5 fermeture
         SendMessageTimeoutW(WM_CLOSE, 10 s) puis WaitForSingleObject
         (10 s) puis GetExitCodeProcess -> S13 « termine code= » ; Q6
         relecture finale : lignes comptées (CRLF), embarquées brutes
         (mode 0, une ligne par appel) -> S14 « lignes= » ; Q7 verdict :
         exit code 0 ET exactement 17 lignes ET 31 derniers octets ==
         fixture -> S15 conforme + S16 OK + rax = 1 ; toute dérive -> S15
         NON conforme + S16 KO + rax = 0 ; Q8 TOUT chemin ferme le handle
         processus (zéro fuite) et journalise son issue (aucune branche
         muette).
  inv  : I1 aucune durée codée en dur comme condition de succès — les
         attentes sont des événements (fenêtre, marqueur, exit) bornés par
         des timeouts ; I2 le journal de la démo n'est JAMAIS modifié —
         lecture seule, embarquement par copie ; I3 les handles processus
         fermés exactement une fois par chemin ; I4 comparaisons par
         memcmp scellé (17 lignes : compte ; marqueur : 31 o exact) — le
         verdict est une preuve, pas une impression.
Échecs :
  E1 : demo.exe absent -> S10 ABSENT, rax = 0 (test SAUTÉ honnête).
  E2 : fenêtre jamais créée (crash précoce) -> 10 s, S11 KO, process tué,
       rax = 0.
  E3 : scénario démo gelé -> marqueur jamais posé -> 30 s, fermeture
       quand même tentée (WM_CLOSE), exit code lu, lignes comptées :
       verdict NON conforme (le journal PARTIEL embarqué localise
       l'intervalle — leçon demo.3).
  E4 : clic non délivré (fenêtre gelée) -> S12 KO, process tué, rax = 0.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation nominale COMPLÈTE — shims : fenêtre trouvée au 3e sondage,
       clic délivré, journal servi avec exactement 17 lignes (6 démarrage +
       11 preuve) finissant par la fixture -> séquence S10/S11/S12/S13
       code=0/S14 lignes=17/S15 conforme/S16 OK + les 17 lignes embarquées
       dans l'ordre, rax = 1.
  V3 : journal NON conforme servi (16 lignes, marqueur absent) -> S14
       lignes=16, S15 NON conforme, S16 KO, rax = 0, lignes embarquées
       quand même (preuve du défaut).
  V4 : demo.exe absent -> S10 ABSENT, rax = 0, aucun autre appel process.
  V5 : falsification — changer la constante 17 (18) fait échouer V2 ;
       raccourcir la fixture d'un octet fait échouer V2 (marqueur reconnu
       sur 30 o : une ligne non finale acceptée à tort).
Fixtures    : CLASSE_DEMO "TRIADE_demo" (UTF-16 .rdata), "demo_journal.txt",
              fixture finale 31 o CP1252 ("boucle § 5 complète - DÉMO OK"
              + CRLF), lignes S10..S16.
Provenance  : écrite-avant-code.
Décisions   : D48 ; le clic est un BM_CLICK sur le bouton trouvé par classe
              (pas de coordonnées — la géométrie appartient à la démo) ;
              le marqueur final comme condition de fin (héritage de la
              sagesse terrain : les durées mentent, les événements non).
Historique  : R1→R2 (D103) : la Q2 de R1 décrivait l'appel FindWindowW(NULL,
              "TRIADE_demo") — chaine en lpWindowName : recherche par TITRE.
              Le binaire terrain.6 avait été corrigé par patch direct (9 octets)
              mais JAMAIS reporté à la notation : la reconstruction terrain.17
              a ressuscité le défaut originel de terrain.5 — S11 « fenetre demo
              ABSENTE » sur TOUS les runs 17-C→17-G pendant que la fenêtre
              vivait à l'écran (journal démo : L01 posée), la fenêtre démo
              orpheline jamais cliquée puis tuée après 10 s — le « doublon »
              constaté par le développeur. R2 porte la classe en rcx : 9
              octets, même taille, et l'oracle apprend le VRAI contrat (le
              shim rend un handle SI ET SEULEMENT SI la classe cherchée est
              "TRIADE_demo" — une recherche par titre échoue désormais en
              émulation comme sur la vraie machine ; leçon D102 appliquée à
              user32 : le modèle ne doit jamais être d'accord avec le code
              faux).
