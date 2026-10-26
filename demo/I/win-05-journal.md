win-05 · journal (écran + fichier) · révision 2
Intention : ajouter une ligne au journal — DEUX fois le même texte, deux
voies complémentaires : à l'écran (contrôle EDIT possédé par le thread GUI,
SendMessageW = marshalling inter-thread sûr) et au fichier de trace terrain
(win-11, mode 2 : conversion UTF-16 → octet Latin-1). L'équivalent GUI du
bloc tcp-11 (journal console), désormais avec jumeau persistant (D36).
Contrat :
  pre  : P1 rcx pointe une chaîne UTF-16LE (terminaison libre, longueur
         portée par rdx) ; P2 rdx = nombre de CHARS UTF-16 (> 0, ≤ 60 —
         borne BUF_CONV de win-11) ; P3 HWND_JOURNAL (0x3868) contient le
         handle du contrôle (posé par win-04 au WM_CREATE) ; P4 pile
         alignée (rsp ≡ 8 mod 16).
  post : Q1 le contrôle a reçu EM_SETSEL(-1, -1) puis EM_REPLACESEL(TRUE,
         rcx) — le texte est ajouté à la fin, le point de défilement suit ;
         Q2 la MÊME ligne est soumise à win-11 mode 2 (ptr, nchars)
         — conversion Latin-1 : 0x2192 (→) devient '>', tout point ≥ 0x100
         devient '-', sinon octet bas ; CRLF ajouté par win-11 ; Q3 rax = 0 ;
         Q4 appelable depuis N'IMPORTE QUEL THREAD (SendMessageW marshalle
         vers le thread GUI ; win-11/FILE_APPEND_DATA est atomique).
  inv  : I1 exactement deux SendMessageW, dans cet ordre, PUIS un appel
         win-11 — jamais l'inverse (l'écran d'abord : la démonstration
         reste regardable même si le fichier est impossible) ; I2 les
         chaînes affichées vivent en .rdata statique (UTF-16, \r\n final
         inclus) — aucune construction dynamique ici ; I3 aucune
         dépendance directe à ws2_32/kernel32 : le fichier passe PAR
         win-11 (I3 de win-04 R2, même discipline).
Échecs :
  E1 : HWND_JOURNAL nul ou invalide (P3 rompue) — SendMessageW échoue
       proprement (retour ignoré) SANS interrompre la voie fichier : la
       ligne survit dans demo_journal.txt (c'est précisément le rôle du
       jumeau — l'écran peut manquer, la trace non).
  E2 : win-11 en échec (fichier impossible) — ignoré : l'écran reste la
       voie principale, la poursuite du scénario est intacte (E2/E3 de
       win-11).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shim SendMessageW capture la paire de messages et le
       texte ; shim WriteFile (handle journal) capture la conversion —
       l'oracle démo reconstruit le journal ÉCRAN et le journal FICHIER et
       les compare ligne à ligne au déroulé attendu (zéro tolérance : une
       ligne manquante d'un côté ou de l'autre = échec).
Fixtures    : chaînes UTF-16 du journal (16 lignes, .rdata).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT user32), D8 ; miroir GUI de tcp-11 (I2) ; D36 (jumeau
              fichier via win-11, ordre écran-avant-fichier).
Historique  : R1→R2 : ajout du miroir fichier (demande terrain : obtenir les
              logs de l'exécution) ; la voie écran et la séquence
              EM_SETSEL/EM_REPLACESEL sont inchangées.
