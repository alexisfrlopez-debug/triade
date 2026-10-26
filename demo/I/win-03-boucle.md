win-03 · boucle de messages · révision 1
Intention : pomper la file de messages du thread GUI jusqu'à WM_QUIT — la
respiration de toute application Windows ; retourne ensuite à win-01 pour un
arrêt propre (ExitProcess 0), en laissant l'OS nettoyer threads et sockets.
Contrat :
  pre  : P1 la fenêtre principale existe (créée par win-02) ; P2 MSG (48 o)
         dans le cadre de pile ; P3 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 chaque itération : GetMessageW(&msg, 0, 0, 0) ; rax > 0 →
         TranslateMessage puis DispatchMessageW ; rax = 0 (WM_QUIT) ou
         rax = -1 (erreur) → sortie de boucle, rax du bloc = 0 ;
         Q2 aucune donnée .data touchée ; Q3 la file est drainée : aucun
         message restant traité après retour.
  inv  : I1 appels IAT exclusivement : GetMessageW, TranslateMessage,
         DispatchMessageW ; I2 MSG jamais persistée hors du cadre ; I3 le
         bloc ne connaît ni les contrôles ni le scénario (découplage win-04).
Échecs :
  E1 : GetMessageW = -1 (erreur, p.ex. hwnd invalide) — sortie immédiate, code
       de retour 0 : l'arrêt reste propre (E1 sans effet de bord).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shim GetMessageW scripté (2 messages puis 0) → les
       dispatches arrivent au shim DefWindowProcW via win-04, retour après le
       0 ; shim à -1 → sortie immédiate sans dispatch (couvre Q1-Q3, E1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT).
