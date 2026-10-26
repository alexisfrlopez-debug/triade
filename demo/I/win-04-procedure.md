win-04 · procédure de fenêtre · révision 4
Intention : le cœur interactif — créer les contrôles au WM_CREATE (journal
multiligne + bouton unique), suivre le redimensionnement, et sur le clic du
bouton lancer EXACTEMENT UNE fois le scénario complet (win-09) dans son thread,
via le bloc scellé M2 tcp-06 (spawn) ; les autres messages sont délégués.
R2 : géométrie WM_SIZE corrigée (RECT.right), défaillances fail-closed.
R3 : les traces passent par win-05 (D37, écran + fichier) et WM_SIZE
journalise les RETOURS des deux MoveWindow — preuves d'exécution terrain
(L4C/L4D).
R4 : largeur/hauteur client vivent en r14d/r15d (sauvegardés-callee) —
D38. Le terrain demo.3 a tranché le mystère du bouton invisible : L4D=1
(MoveWindow bouton VRAI) et bouton ABSENT de l'écran, car w/h étaient
conservés dans r10d/r11d, REGISTRES VOLATILES relus après le premier appel
MoveWindow — l'instruction syscall écrit RFLAGS dans r11 par matériel, le
bouton partait hors client (y=0x246-44=538 dans un client de 516) avec un
retour VRAI : Win32 accepte un enfant hors zone parent. La correction est
invisible en statique (notation, octet, oracle R3 tous verts) — seul le
terrain possédait la vérité, et l'oracle est durci en conséquence (shims
qui clobbent les volatiles à chaque retour IAT).
Contrat :
  pre  : P1 appelée par le système (msx64 callback : rcx=hwnd, rdx=msg,
         r8=wParam, r9=lParam), pile alignée ; P2 WM_CREATE précède tout
         WM_COMMAND/WM_SIZE utile ; P3 IAT user32/gdi32 résolue (D35).
  post : Q1 WM_CREATE : journal (EDIT, ES_MULTILINE|ES_READONLY|WS_VSCROLL)
         et bouton (BS_PUSHBUTTON, id 1) créés enfants, handles posés en
         .data (HWND_JOURNAL 0x3868, HWND_BOUTON 0x3870), police système
         appliquée aux deux (WM_SETFONT, GetStockObject(DEFAULT_GUI_FONT)),
         trace « L02 controles crees », retour 0 ;
         Q2 WM_SIZE : GetClientRect + MoveWindow — la LARGEUR est lue dans
         RECT.right ([rsp+0x28], champ 3 du RECT posé à [rsp+0x20] — jamais
         dans RECT.top, toujours nul côté client : défaut D36 corrigé) —
         journal (8, 8, w-16, h-56), bouton (8, h-44, w-16, 36), retour 0 ;
         w = RECT.right et h = RECT.bottom sont posés UNE fois dans
         r14d/r15d AVANT tout appel et relus tels quels par les DEUX
         MoveWindow ; PUIS traces « L4C move journal=NN » et
         « L4D move bouton=NN » où NN = retour BOOL de chaque MoveWindow
         (1 = succès) — inscrites APRÈS les deux appels, via win-05 mode 1
         (écran + fichier) ;
         Q3 WM_COMMAND (id 1) : si DRAPEAU_WORKER (0x3878) = 0 → passe à 1,
         trace « L03 clic : lancement du scenario », bouton désactivé
         (EnableWindow FALSE), thread scénario lancé par tcp-06(proc=win-09,
         arg=0), handle fermé (CloseHandle) dès retour, retour 0 ; si drapeau
         ≠ 0 → retour 0 sans rien faire (clic unique) ;
         Q4 WM_CLOSE → DestroyWindow(hwnd), retour 0 ; WM_DESTROY →
         PostQuitMessage(0), retour 0 ; tout autre message → rax =
         DefWindowProcW(hwnd, msg, wParam, lParam).
  inv  : I1 wParam/lParam sauvegardés avant tout appel (volatile) — le défaut
         du code par défaut est alimenté par les valeurs d'origine ; I2 le
         lancement du scénario passe PAR tcp-06 scellé (aucun CreateThread
         direct — réutilisation M2) ; I3 aucune logique de démonstration ici :
         win-04 est du pur habillage GUI (la preuve vit dans win-05..09) ;
         I4 toutes les traces passent PAR win-05 (JOURNAL_TRACE — D37,
         écran + fichier, jamais de WriteFile direct) ; I5 les retours
         MoveWindow sont capturés AVANT tout appel suivant (rax volatile)
         dans des registres sauvegardés-callee libres (r12d/r13d — uMsg/
         wParam déjà consommés à ce point du handler WM_SIZE) ;
         I6 (R4, D38) AUCUN registre volatile (rax, rcx, rdx, r8-r11) ne
         survit à un appel IAT — w/h vivent en r14d/r15d (sauvegardés-callee,
         morts dans WM_SIZE : r14 portait lParam d'entrée, seule la branche
         .defaut — jamais atteinte depuis WM_SIZE — en a besoin ; r15 est
         libre hors WM_CREATE) ; relire r10/r11 après un appel est le défaut
         D38 : légal en notation, mort au terrain (syscall écrit RFLAGS dans
         r11 par matériel), invisible à l'oracle R3 dont les shims
         présumaient les volatiles intacts.
Échecs :
  E1 : création d'un contrôle échoue (rax = 0) — fail-closed depuis R2 :
       trace « LKO creation du journal/bouton echouee gle=NN » (GetLastError
       AVANT tout autre appel) puis retour -1 — la création de la fenêtre
       est avortée, win-02 affiche la cause (MessageBoxW) et la démo
       s'arrête proprement : une vitrine sans contrôle est un mensonge
       muet, R1 la tolérait, D36 la refuse.
  E2 : tcp-06 échoue (handle 0) — trace « LKO lancement thread scenario
       echoue gle=NN », drapeau remis à 0, bouton réactivé : l'utilisateur
       peut réessayer (échec transitoire, pas fatal).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : WM_CREATE → deux CreateWindowExW enfants + deux
       WM_SETFONT + trace L02 ; WM_COMMAND id 1 → UN appel CreateThread
       (tcp-06) et un seul (second WM_COMMAND ignoré, Q3) ; WM_CLOSE/
       WM_DESTROY → DestroyWindow + PostQuitMessage ; défaut →
       DefWindowProcW (Q4).
  V3 : géométrie anti-régression D36 : WM_SIZE avec client (0,0,780,560)
       → MoveWindow journal = (8, 8, 764, 504), bouton = (8, 516, 764, 36)
       — l'oracle REJETTE toute largeur ≤ 0 (le shim MoveWindow est durci :
       invariant géométrique, pas seulement appel constaté) ; puis fichier
       reçoit « L4C move journal=1 » et « L4D move bouton=1 » (le shim
       retourne 1) — et l'ÉCRAN les reçoit aussi (miroir D37). Depuis R4,
       les shims CLOBBENT rcx/rdx/r8-r11 à chaque retour IAT (r10=0,
       r11=0x246 : un retour kernel réaliste) — la géométrie ne passe
       QUE si w/h vivent en callee-saved (I6) ;
  V4 : falsification binaire : l'octet de déplacement de la lecture RECT
       (0x28) réécrit en 0x24 (le défaut D36 originel) → l'oracle ÉCHOUE
       (V3 ne passe plus) — le défaut est impossible à réintroduire
       silencieusement.
  V5 : falsification binaire D38 : les deux lectures r14d/r15d du SECOND
       MoveWindow (mov r8d, r15d / mov r9d, r14d) réécrites en r11d/r10d
       (44 8B F8→D8, 45 8B CE→CA) — le défaut demo.3 exact : volatiles
       relus après l'appel → l'oracle ÉCHOUE (géométrie invalide :
       largeur = 0-16 = -16) — le bouton invisible est impossible à
       réintroduire silencieusement.
Fixtures    : chaînes UTF-16 .rdata (classes "EDIT"/"BUTTON", libellés) +
              chaînes ASCII de trace (L02, L03, L4C, L4D, LKO_EDIT,
              LKO_BOUTON, LKO_SPAWN).
Provenance  : écrite-avant-code (R2 : correction avant reconstruction ; R3 :
              miroir + diagnostics avant reconstruction ; R4 : volatiles →
              callee-saved avant reconstruction — le terrain demo.3 a parlé :
              L4D=1 + bouton absent).
Décisions   : D7 (IAT), D8 (bloc d'habillage), D35 ; clic unique par drapeau ;
              D36 (correctif RECT.right + fail-closed contrôles + trace) ;
              D37 (traces via win-05, diagnostics L4C/L4D) ;
              D38 (volatiles ne survivent pas à un appel IAT — w/h en
              callee-saved, oracle durci : clobber des volatiles à chaque
              retour de shim).
Historique  : R1→R2 : divergence notation/spec RECT.top/RECT.right (fenêtre
              vide terrain), oracle durci (invariant + falsification).
              R2→R3 : re-ciblage des traces vers win-05 (capture demo.2 :
              écran vide au démarrage — D37) + preuves d'exécution L4C/L4D.
              R3→R4 : capture demo.3 — écran vivant (L02/L4C/L4D/L01
              affichés, miroir D37 validé terrain) mais bouton ABSENT avec
              L4D=1 : w/h en r10d/r11d volatiles relus après l'appel
              MoveWindow (D38) → r14d/r15d callee-saved, oracle durci
              (clobber des volatiles), falsification V5.
