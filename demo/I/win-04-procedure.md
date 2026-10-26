win-04 · procédure de fenêtre · révision 3
Intention : le cœur interactif — créer les contrôles au WM_CREATE (journal
multiligne + bouton unique), suivre le redimensionnement, et sur le clic du
bouton lancer EXACTEMENT UNE fois le scénario complet (win-09) dans son thread,
via le bloc scellé M2 tcp-06 (spawn) ; les autres messages sont délégués.
R2 : géométrie WM_SIZE corrigée (RECT.right), défaillances fail-closed.
R3 : les traces passent par win-05 (D37, écran + fichier) et WM_SIZE
journalise les RETOURS des deux MoveWindow — preuves d'exécution terrain
(L4C/L4D) : la capture demo.2 montrait un bouton non rendu alors que la
notation, l'octet et l'oracle sont corrects — la prochaine exécution
terrain dira si MoveWindow(bouton) réussit (1) ou échoue (0).
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
         PUIS traces « L4C move journal=NN » et « L4D move bouton=NN » où
         NN = retour BOOL de chaque MoveWindow (1 = succès) — inscrites
         APRÈS les deux appels, via win-05 mode 1 (écran + fichier) ;
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
         wParam déjà consommés à ce point du handler WM_SIZE).
Échecs :
  E1 : création d'un contrôle échoue (rax = 0) — DEPUIS R2 fail-closed :
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
       retourne 1) — et l'ÉCRAN les reçoit aussi (miroir D37) ;
  V4 : falsification binaire : l'octet de déplacement de la lecture RECT
       (0x28) réécrit en 0x24 (le défaut D36 originel) → l'oracle ÉCHOUE
       (V3 ne passe plus) — le défaut est impossible à réintroduire
       silencieusement.
Fixtures    : chaînes UTF-16 .rdata (classes "EDIT"/"BUTTON", libellés) +
              chaînes ASCII de trace (L02, L03, L4C, L4D, LKO_EDIT,
              LKO_BOUTON, LKO_SPAWN).
Provenance  : écrite-avant-code (R2 : correction avant reconstruction ; R3 :
              miroir + diagnostics avant reconstruction).
Décisions   : D7 (IAT), D8 (bloc d'habillage), D35 ; clic unique par drapeau ;
              D36 (correctif RECT.right + fail-closed contrôles + trace) ;
              D37 (traces via win-05, diagnostics L4C/L4D MoveWindow).
Historique  : R1→R2 : divergence notation/spec RECT.top/RECT.right (fenêtre
              vide terrain), oracle durci (invariant + falsification).
              R2→R3 : re-ciblage des traces vers win-05 (capture demo.2 :
              écran vide au démarrage — D37) + preuves d'exécution L4C/L4D :
              le bouton non rendu sur le terrain, inexorablement correct en
              statique, sera jugé par ses retours réels.
