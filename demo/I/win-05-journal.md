win-05 · journal (miroir universel écran + fichier) · révision 3
Intention : ajouter une ligne au journal — à l'écran (contrôle EDIT du thread
GUI, SendMessageW) ET au fichier de trace terrain (win-11). R3 : le bloc
devient le point de passage UNIQUE de toutes les lignes de la démo. Constat
fondateur (capture terrain demo.2, 26/10/2026 20:56) : les traces de
démarrage (L00/L01/L02/L03/LKO) appelaient win-11 en direct — le fichier
était complet, l'écran RESTAIT VIDE jusqu'au clic (l'edit est créé avec un
texte initial vide) : la vitrine paraissait morte alors que tout
fonctionnait. D37 : toutes les traces passent désormais par win-05, écran
d'abord. Deux entrées, un seul corps :
  — entrée scénario (0x19C0, symbole JOURNAL_GUI) : contrat historique
    (ptr UTF-16, nchars) inchangé — win-08/win-09 ne bougent pas ; elle
    force le mode 2 (shim « mov r8d, 2 ; jmp ») ;
  — entrée trace (0x19D0, symbole JOURNAL_TRACE) : contrat 4 arguments
    (ptr ASCII, longueur, mode, valeur) — la signature de win-11, que les
    appelants (win-02, win-04) posent déjà : re-ciblage pur, zéro octet
    d'argumentation supplémentaire.
Contrat :
  pre  : P1 entrée trace : rcx pointe une chaîne ASCII (terminaison libre,
         longueur portée par rdx), rdx = octets (> 0, ≤ 43), r8d ∈ {0, 1},
         r9d = valeur numérique si mode 1 ; P2 entrée scénario : rcx pointe
         une chaîne UTF-16LE (≤ 60 chars), rdx = chars ; P3 HWND_JOURNAL
         (0x3868) peut être NUL (avant WM_CREATE) — le miroir écran est
         alors sauté, la voie fichier reste ; P4 pile alignée.
  post : Q1 si HWND_JOURNAL ≠ 0 : le contrôle a reçu EM_SETSEL(-1, -1) puis
         EM_REPLACESEL(TRUE, texte) — mode 0/1 : texte = conversion
         ASCII→UTF-16 de la ligne (valeur décimale itoa appendée si mode 1,
         CRLF final) construite dans BUF_MIROIR (0x3A50) ; mode 2 : texte =
         ptr tel quel (chaînes .rdata, \r\n inclus) ; Q2 win-11 est appelé
         en queue (jmp, pile restaurée) avec les arguments D'ORIGINE
         (ptr, longueur, mode, valeur) — le comportement fichier de win-11
         est inchangé octet par octet ; Q3 rax = retour de win-11 (1 = ok,
         0 = échec fichier) ; Q4 appelable depuis n'importe quel thread
         (SendMessageW marshalle ; win-11 atomique).
  inv  : I1 l'écran d'abord, le fichier ensuite — dans TOUS les modes (la
         démonstration reste regardable même si le fichier est impossible) ;
         I2 BUF_MIROIR (128 o, .data) est le SEUL état nouveau — la
         conversion ne touche ni BUF_CONV ni BUF_CHEMIN (propriété de
         win-11) ; I3 la longueur ORIGINALE (rdx) est restituée à win-11 :
         les compteurs internes de conversion ne fuient pas dans le
         contrat ; I4 aucune dépendance directe à kernel32 : le fichier
         passe PAR win-11 (I3 de win-04:R2) ; I5 l'entrée scénature ne
         modifique QUE r8d (le shim 0x19C0) — les autres registres
         traversent intacts.
Échecs :
  E1 : HWND_JOURNAL nul (P3, démarrage avant WM_CREATE) — miroir écran
       sauté silencieusement, L00 n'apparaît qu'au fichier : la vitrine
       n'existe pas encore, il n'y a rien à peindre — comportement voulu.
  E2 : win-11 en échec (fichier impossible) — retour 0 propagé à l'appelant
       (win-02 l'interprète : sans fichier, pas de démo) ; l'écran, lui, a
       déjà reçu la ligne (I1).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation entrée scénario : paire EM_SETSEL/EM_REPLACESEL avec le
       texte UTF-16 exact + fichier Latin-1 (miroir, zéro tolérance).
  V3 : émulation entrée trace : mode 0 → écran « ligne\r\n » + fichier
       « ligne\r\n » ; mode 1 → écran et fichier « texte valeur\r\n » —
       l'oracle reconstruit les deux journaux et compare.
  V4 : coquille GUI : les lignes de démarrage L02/L4C/L4D/L01 apparaissent
       AUSSI à l'écran (L00 non : HWND nul, E1) — anti-régression D37 : un
       re-routage vers win-11 fait échouer l'oracle.
Fixtures    : chaînes UTF-16 du journal (16 lignes) + chaînes ASCII de
              trace + BUF_MIROIR (.data, 128 o).
Provenance  : écrite-avant-code (R3 : spec avant reconstruction).
Décisions   : D7, D8 ; miroir GUI de tcp-11 ; D36 (jumeau fichier) ;
              D37 (point de passage unique, écran d'abord partout).
Historique  : R1 : journal écran seul. R2 : ajout du miroir fichier
              (contrat 2 args UTF-16). R3 : entrée trace 4 args pour les
              lignes ASCII de win-02/win-04 — le défaut D37 (traces de
              démarrage contournant l'écran, fenêtre vide jusqu'au clic)
              est impossible à réintroduire sans échouer V4.
