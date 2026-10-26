win-04 · procédure de fenêtre · révision 2
Intention : le cœur interactif — créer les contrôles au WM_CREATE (journal
multiligne + bouton unique), suivre le redimensionnement, et sur le clic du
bouton lancer EXACTEMENT UNE fois le scénario complet (win-09) dans son thread,
via le bloc scellé M2 tcp-06 (spawn) ; les autres messages sont délégués.
R2 : la géométrie WM_SIZE est corrigée (RECT.right lu, plus RECT.top) et les
défaillances de contrôles deviennent fail-closed tracées (win-11).
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
         I4 toutes les traces passent PAR win-11 (jamais de WriteFile direct).
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
       invariant géométrique, pas seulement appel constaté).
  V4 : falsification binaire : l'octet de déplacement de la lecture RECT
       (0x28) réécrit en 0x24 (le défaut D36 originel) → l'oracle ÉCHOUE
       (V3 ne passe plus) — le défaut est impossible à réintroduire
       silencieusement.
Fixtures    : chaînes UTF-16 .rdata (classes "EDIT"/"BUTTON", libellés) +
              chaînes ASCII de trace (L02, L03, LKO_EDIT, LKO_BOUTON,
              LKO_SPAWN).
Provenance  : écrite-avant-code (R2 : correction avant reconstruction).
Décisions   : D7 (IAT), D8 (bloc d'habillage), D35 ; clic unique par drapeau ;
              D36 (correctif RECT.right + fail-closed contrôles + trace).
Historique  : R1→R2 : la notation lisait RECT.top ([rsp+0x24], toujours 0)
              comme largeur — la spec R1 exigeait déjà « w-16 » avec
              w = largeur client : c'est une DIVERGENCE NOTATION/SPEC, la
              fenêtre s'ouvrait vide (contrôles de largeur -16) sur le
              terrain. Correctif : lecture [rsp+0x28] (RECT.right). L'écart
              avait échappé à l'oracle R1 : le shim MoveWindow ne vérifiait
              aucune géométrie (V3/V2 durcis en conséquence, D36).
