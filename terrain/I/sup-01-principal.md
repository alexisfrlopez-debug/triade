sup-01 · principal (point d'entrée graphique) · révision 1
Intention : ouvrir le superviseur terrain en garantissant UNE chose avant
toute écriture de journal : l'horodatage du run. Le nom du fichier journal
(terrain_YYYYMMDD_HHMMSS.txt) dérive de l'heure locale ; la première ligne
de trace (L00, émise pendant la création de la fenêtre) ouvre déjà le
fichier — l'horodatage doit donc être posé AVANT sup-02, sans quoi le nom
du journal serait vide. Puis la fenêtre, la boucle de messages, la sortie
propre par io-02 scellé — le squelette de win-01 démo, allongé d'un appel.
Contrat :
  pre  : P1 appelé une fois par le chargeur (AddressOfEntryPoint), pile
         alignée par le chargeur ; P2 aucune donnée .data requise à l'entrée
         (l'horodatage écrit dans TAMPON_NOM/TAMPON_AFF, zones vierges).
  post : Q1 sup-21 appelé en premier (TAMPON_NOM = 28 o
         "terrain_YYYYMMDD_HHMMSS.txt\0", TAMPON_AFF = "S01 date
         YYYYMMDD_HHMMSS") ; Q2 sup-02 ensuite : rax = 0 -> MessageBoxW
         déjà affiché par sup-02, sortie io-02(1) ; Q3 rax != 0 -> win-03
         scellé (pompe Get/Translate/Dispatch) puis io-02(0) au WM_QUIT.
  inv  : I1 appels sup-21, sup-02, win-03, io-02 exclusivement — aucun
         appel IAT direct (l'entrée ne touche jamais le système elle-même) ;
         I2 zone d'accueil ABI réservée avant chaque appel (sub rsp, 0x28).
Échecs :
  E1 : sup-02 échoue (classe ou fenêtre impossible) -> sortie io-02(1)
       après MessageBoxW de sup-02 (fail-closed, miroir win-01).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation coquille : sup-21 AVANT sup-02 (ordre prouvé par l'ordre
       des appels observés), fenêtre créée, boucle vidée, ExitProcess(0).
  V3 : falsification — inverser l'ordre (sup-02 avant sup-21) fait échouer
       le verrou d'ordre de l'oracle (le journal s'ouvrirait sans nom).
Fixtures    : aucune (bloc d'orchestration pure).
Provenance  : écrite-avant-code.
Décisions   : D48 (superviseur terrain), héritage win-01:R1 (squelette) ;
              l'horodatage en tête est le devoir du point d'entrée, exactement
              comme l'init CS était le devoir de tcp-12 repris par win-09 (D42).
