win-05 · journal graphique (ajout de ligne) · révision 1
Intention : ajouter une ligne UTF-16 au journal à l'écran — l'équivalent GUI du
bloc tcp-11 (journal console) : une seule responsabilité, la même discipline
(une entrée critique, un appel effectif), mais la sortie est le contrôle EDIT
possédé par le thread GUI (SendMessageW = marshalling inter-thread sûr).
Contrat :
  pre  : P1 rcx pointe une chaîne UTF-16LE (terminaison libre, longueur
         portée par rdx) ; P2 rdx = nombre de CHARS UTF-16 à afficher (> 0) ;
         P3 HWND_JOURNAL (0x3868) contient le handle du contrôle (posé par
         win-04 au WM_CREATE) ; P4 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 le contrôle a reçu EM_SETSEL(-1, -1) puis EM_REPLACESEL(TRUE,
         rcx) — le texte est ajouté à la fin, le point de défilement suit ;
         Q2 rax = 0 ; Q3 aucun octet .data modifié ; Q4 appelable depuis
         N'IMPORTE QUEL THREAD (SendMessageW marshalle vers le thread GUI).
  inv  : I1 exactement deux SendMessageW, dans cet ordre ; I2 les chaînes
         affichées vivent en .rdata statique (UTF-16, \r\n final inclus) —
         aucune construction dynamique ici (le scénario n'affiche que du
         statique : les attentes sont connues à l'avance) ; I3 aucune
         dépendance à ws2_32/kernel32.
Échecs :
  E1 : HWND_JOURNAL nul ou invalide (P3 rompue) — SendMessageW échoue
       proprement (retour ignoré), la ligne est perdue à l'écran SANS crash :
       le journal console (tcp-11, si une console existe) et la poursuite du
       scénario restent intacts.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shim SendMessageW capture la paire de messages et le texte
       — l'oracle démo reconstruit le journal complet et le compare ligne à
       ligne au déroulé attendu du scénario (preuve d'affichage, zéro
       tolérance : une ligne manquante = échec).
Fixtures    : chaînes UTF-16 du journal (16 lignes, .rdata).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT user32), D8 ; miroir GUI de tcp-11 (I2).
