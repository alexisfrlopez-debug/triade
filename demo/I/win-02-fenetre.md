win-02 · fenêtre principale (classe + création) · révision 1
Intention : enregistrer la classe de fenêtre TRIADE (UTF-16) et créer la fenêtre
principale visible — la vitrine de la démonstration ; tout échec ici est fatal et
expliqué à l'utilisateur (MessageBoxW), jamais silencieux.
Contrat :
  pre  : P1 IAT user32/kernel32 résolue (D35) ; P2 .data vierge côté GUI ;
         P3 pile alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès : rax = hwnd de la fenêtre (non nul), HWND_PRINCIPAL (.data
         0x3860) contient ce handle ; Q2 échec (classe ou création) :
         MessageBoxW(0, cause, titre, MB_ICONERROR) affichée, rax = 0, aucun
         handle partiel laissé en .data.
  inv  : I1 WNDCLASSEXW construite dans le cadre de pile (80 o), jamais en
         .data ; I2 lpfnWndProc = win-04 (0x1600), lpszClassName et titre
         depuis .rdata (UTF-16 statique) ; I3 hInstance obtenu par
         GetModuleHandleW(0) — aucune adresse absolue (image PI, ancre D33) ;
         I4 appels : GetModuleHandleW, LoadCursorW, RegisterClassExW,
         CreateWindowExW, MessageBoxW — exclusivement via l'IAT.
Échecs :
  E1 : RegisterClassExW = 0 — cause affichée, rax = 0.
  E2 : CreateWindowExW = 0 — cause affichée, rax = 0.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims RegisterClassExW/CreateWindowExW → hwnd factice
       non nul → HWND_PRINCIPAL posé ; shim CreateWindowExW = 0 → MessageBoxW
       appelé, rax = 0 (couvre Q1-Q2, E1-E2).
Fixtures    : chaînes UTF-16 .rdata (classe, titre, message d'échec).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT), D33 (PI), D35 (FT = slots).
