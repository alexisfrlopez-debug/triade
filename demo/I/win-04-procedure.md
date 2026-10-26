win-04 · procédure de fenêtre · révision 1
Intention : le cœur interactif — créer les contrôles au WM_CREATE (journal
multiligne + bouton unique), suivre le redimensionnement, et sur le clic du
bouton lancer EXACTEMENT UNE fois le scénario complet (win-09) dans son thread,
via le bloc scellé M2 tcp-06 (spawn) ; les autres messages sont délégués.
Contrat :
  pre  : P1 appelée par le système (msx64 callback : rcx=hwnd, rdx=msg,
         r8=wParam, r9=lParam), pile alignée ; P2 WM_CREATE précède tout
         WM_COMMAND/WM_SIZE utile ; P3 IAT user32/gdi32 résolue (D35).
  post : Q1 WM_CREATE : journal (EDIT, ES_MULTILINE|ES_READONLY|WS_VSCROLL)
         et bouton (BS_PUSHBUTTON, id 1) créés enfants, handles posés en
         .data (HWND_JOURNAL 0x3868, HWND_BOUTON 0x3870), police système
         appliquée aux deux (WM_SETFONT, GetStockObject(DEFAULT_GUI_FONT)),
         retour 0 ;
         Q2 WM_SIZE : GetClientRect + MoveWindow — journal (8, 8, w-16, h-56),
         bouton (8, h-44, w-16, 36), retour 0 ;
         Q3 WM_COMMAND (id 1) : si DRAPEAU_WORKER (0x3878) = 0 → passe à 1,
         bouton désactivé (EnableWindow FALSE), thread scénario lancé par
         tcp-06(proc=win-09, arg=0), handle fermé (CloseHandle) dès retour,
         retour 0 ; si drapeau ≠ 0 → retour 0 sans rien faire (clic unique) ;
         Q4 WM_CLOSE → DestroyWindow(hwnd), retour 0 ; WM_DESTROY →
         PostQuitMessage(0), retour 0 ; tout autre message → rax =
         DefWindowProcW(hwnd, msg, wParam, lParam).
  inv  : I1 wParam/lParam sauvegardés avant tout appel (volatile) — le défaut
         du code par défaut est alimenté par les valeurs d'origine ; I2 le
         lancement du scénario passe PAR tcp-06 scellé (aucun CreateThread
         direct — réutilisation M2) ; I3 aucune logique de démonstration ici :
         win-04 est du pur habillage GUI (la preuve vit dans win-05..09).
Échecs :
  E1 : création d'un contrôle échoue (rax = 0) — toléré : le handle nul est
       posé, la démonstration le constatera via win-05 (SendMessageW sur NULL
       échoue proprement, journal muet) ; pas de crash.
  E2 : tcp-06 échoue (handle 0) — drapeau remis à 0, bouton réactivé :
       l'utilisateur peut réessayer (échec transitoire, pas fatal).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : WM_CREATE → deux CreateWindowExW enfants + deux
       WM_SETFONT ; WM_COMMAND id 1 → UN appel CreateThread (tcp-06) et un
       seul (second WM_COMMAND ignoré, Q3) ; WM_CLOSE/WM_DESTROY →
       DestroyWindow + PostQuitMessage ; défaut → DefWindowProcW (Q4).
Fixtures    : chaînes UTF-16 .rdata (classes "EDIT"/"BUTTON", libellés).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT), D8 (bloc d'habillage), D35 ; clic unique par drapeau.
