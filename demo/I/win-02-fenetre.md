win-02 · fenêtre principale (classe + création) · révision 3
Intention : enregistrer la classe de fenêtre TRIADE (UTF-16) et créer la fenêtre
principale visible — la vitrine de la démonstration ; tout échec ici est fatal et
expliqué à l'utilisateur (MessageBoxW), jamais silencieux — et tracé au fichier
ET à l'écran (win-05, D37) : la vitrine qui ne s'ouvre pas doit s'expliquer sur
les deux voies, et la vitrine OUVERTE doit montrer son démarrage.
Contrat :
  pre  : P1 IAT user32/kernel32 résolue (D35) ; P2 .data vierge côté GUI ;
         P3 pile alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès : rax = hwnd de la fenêtre (non nul), HWND_PRINCIPAL (.data
         0x3860) contient ce handle ; Q2 échec (classe ou création) :
         MessageBoxW(0, cause, titre, MB_ICONERROR) affichée, rax = 0, aucun
         handle partiel laissé en .data ; Q3 traces fichier (win-11) : entrée →
         « L00 demarrage » AVANT tout appel GUI (le fichier existe dès la pre-
         mière seconde, l'init paresseuse de win-11 est garantie antérieure à
         WM_CREATE) ; succès → « L01 fenetre principale creee » APRÈS pose du
         handle ; échec → « LKO creation fenetre impossible gle=NN » avec NN =
         GetLastError AVANT MessageBoxW ; Q4 chaque trace passe par win-05
         (JOURNAL_TRACE, mode 0/1) : fichier ET écran (si le contrôle
         existe — L00 précède WM_CREATE, l'écran la saute, E1 de win-05) ;
         rax du chemin succès = retour win-11 via win-05 (1 = fichier ok).
  inv  : I1 WNDCLASSEXW construite dans le cadre de pile (80 o), jamais en
         .data ; I2 lpfnWndProc = win-04, lpszClassName et titre
         depuis .rdata (UTF-16 statique) ; I3 hInstance obtenu par
         GetModuleHandleW(0) — aucune adresse absolue (image PI, ancre D33) ;
         I4 appels : GetModuleHandleW, LoadCursorW, RegisterClassExW,
         CreateWindowExW, MessageBoxW — exclusivement via l'IAT ; I5 les
         trois traces passent PAR win-05 (JOURNAL_TRACE — aucun WriteFile
         direct, aucun contournement de l'écran : D37).
Échecs :
  E1 : RegisterClassExW = 0 — cause affichée, gle tracé, rax = 0.
  E2 : CreateWindowExW = 0 — cause affichée, gle tracé, rax = 0.
  E3 : win-11 lui-même en échec (fichier impossible) — le retour 0 remonte
       par win-05 : sans fichier de trace, pas de démonstration fiable
       (décision D36) ; l'écran, lui, a reçu la ligne (I1 de win-05).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims RegisterClassExW/CreateWindowExW → hwnd factice
       non nul → HWND_PRINCIPAL posé + fichier = [L00, L01] + écran =
       [L01] (L00 sautée : HWND_JOURNAL nul) ; shim CreateWindowExW = 0 →
       MessageBoxW appelé, rax = 0, fichier = [L00, LKO…gle=NN] avec NN
       piloté par le shim GetLastError (couvre Q1-Q4, E1-E2).
       Anti-régression D37 : re-cibler une trace vers win-11 fait disparaî-
       tre L01 de l'ÉCRAN → l'oracle échoue.
Fixtures    : chaînes UTF-16 .rdata (classe, titre, message d'échec) + chaînes
              ASCII de trace (L00, L01, LKO_GUI).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT), D33 (PI), D35 (FT = slots), D36 (trace terrain),
              D37 (traces via win-05 : écran + fichier).
Historique  : R2 — journal fichier symétrique de l'affichage. R3 — les
              traces empruntent win-05 (JOURNAL_TRACE) : la capture
              terrain de demo.2 montrait une fenêtre VIDE au démarrage
              (traces fichier seulement) ; l'utilisateur voit désormais
              L01/L02 s'écrire dans la vitrine dès le lancement.
