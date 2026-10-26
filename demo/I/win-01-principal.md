win-01 · principal (point d'entrée graphique) · révision 1
Intention : point d'entrée de demo.exe — créer la fenêtre principale (win-02),
pomper les messages (win-03) puis terminer proprement (code 0) ; l'orchestration
de la démonstration vit dans win-09, lancée par la procédure de fenêtre (win-04).
Contrat :
  pre  : P1 le processus démarre : pile alignée par le chargeur (rsp ≡ 8 mod 16),
         .data vierge, IAT résolue par le chargeur (D35 : FirstThunk = slots) ;
         P2 aucune ressource n'est encore créée.
  post : Q1 en cas de succès : retour après WM_QUIT, ExitProcess(0) via io-02
         scellé M0 (a10003) — rax de win-03 ignoré ;
         Q2 en cas d'échec de création (win-02 → 0) : ExitProcess(1) sans boucle
         de messages (la cause a déjà été affichée par win-02 via MessageBoxW).
  inv  : I1 appels directs limités à win-02, win-03 et io-02 (a10003) ; I2 aucun
         état .data lu ou écrit (le point d'entrée ne porte pas d'état) ; I3 la
         porte R10 n'est PAS ici : elle vit dans win-06, appelée par le scénario
         APRÈS que la fenêtre existe (échec affiché dans le journal graphique,
         pas de sortie silencieuse).
Échecs :
  E1 : fenêtre non créée (win-02 = 0) — propagation immédiate, code 1 ; aucun
       message supplémentaire (win-02 a déjà affiché la cause).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation (oracle démo) : shims user32 simulés — win-02 réussit, win-03
       reçoit WM_QUIT immédiat → ExitProcess(0) ; win-02 échoue → ExitProcess(1)
       sans appel à win-03 (couvre Q1-Q2, E1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D10, D33, D35 ; sous-système WINDOWS_GUI (point d'entrée ≠ tcp-12).
