loupe-09 · écran : la vitrine entière et la disposition déclarée · révision 1
Intention : POSER L'ÉCRAN DE LOUPE — la vitrine entière : le point
d'entrée (WinMain : la ligne de commande lue à la main, le chemin cité
ou non), la fenêtre (classe + création — l'héritage du MODÈLE win-02 de
la démo, R3), LA PROCÉDURE qui route chaque message à son bloc, et les
TROIS ZONES DÉCLARÉES avant la première goutte de peinture (l'ECRAIN :
entête, grille, barre). La disposition est tenue DEUX FOIS : la
disposition DES ZONES (la structure déclarée au plan) et la disposition
DES MESSAGES (la table de routage fermée). TOUT refus nommé du domaine
monte à la barre — l'écran NOMME ce qu'il refuse, la vitrine qui ne
s'explique pas n'existe pas (D36/D37, le modèle démo).
Contrat :
  pre  : P1 l'IAT kernel32/user32/gdi32 résolue (D7/D35, les 34
             feuilles du plan) ; P2 .data vierge côté vitrine (HWND,
             ECRAIN, SAISIE) ; P3 la pile alignée 16 (WinMain).
  post : Q1 WinMain : la ligne de commande lue PAR GetCommandLineW À LA
             MAIN (le programme sauté, guillemets honorés — aucun
             shell32, aucune dépendance) : chemin cité → loupe-01 (la
             session naît, le refus nommé monte à la barre et la
             vitrine s'ouvre VIDE VRAIE) ; chemin absent → la vitrine
             s'ouvre avec l'usage à la barre (« loupe <fichier> ») —
             l'état nommé, pas un échec ;
         Q2 la CLASSE enregistrée (WNDCLASSEXW sur la pile — jamais en
             .data ; lpfnWndProc = LA PROCÉDURE, la classe et le titre
             UTF-16 de .rdata, le curseur flèche, l'icône ERREUR pour
             l'explication fatale) puis CreateWindowExW (STYLE_FENETRE
             — l'ascenseur vertical inclus, 640 × 480) puis ShowWindow
             — tout échec : MessageBoxW(MB_ICONERROR) PUIS ExitProcess(1)
             (la vitrine impossible s'explique PUIS meurt : D36) ;
         Q3 LA PROCÉDURE (le callback msx64 : rcx = hwnd, rdx = msg,
             r8 = wParam, r9 = lParam — D38 : les volatils sauvés avant
             tout appel) : WM_PAINT → loupe-10 ; WM_SIZE, WM_VSCROLL,
             WM_MOUSEWHEEL → loupe-11 ; WM_KEYDOWN → LA TABLE DE
             COMMANDES (F5 ou Ctrl+G → loupe-12 ; F3 → loupe-14 ;
             Ctrl+S → loupe-17 ; Alt+F4/WM_CLOSE → loupe-18 ; les
             flèches/PgUp/PgDn/Home/End → loupe-15 ; toute autre
             touche → DefWindowProcW) ; WM_CHAR → la saisie active ?
             loupe-12/loupe-14 : loupe-16 — LA LISTE EST FERMÉE ;
         Q4 la boucle HÉRITÉE win-03 (PAR LA CARTE — GetMessageW/
             TranslateMessage/DispatchMessageW jusqu'à WM_QUIT) puis
             ExitProcess(0) — le retour propre ;
         Q5 rax = 0 au retour de WinMain (le code d'ExitProcess).
  inv  : I1 L'ÉCRAN DÉCLARÉ AVANT LA PEINTURE : la zone ECRAIN du plan
             (2320 o — l'entête 80 @ +0, la grille 24 × 80 @ +80, la
             barre 2 × 160 @ +2000) est LA disposition : loupe-10 la
             remplit, la structure ne bouge plus JAMAIS ;
         I2 l'image PI (D33) : GetModuleHandleW(0), aucune adresse
             absolue — le callback, la classe, les chaînes : tout
             relatif ou résolu ;
         I3 AUCUNE goutte de peinture hors WM_PAINT (loupe-10 est
             L'UNIQUE peintre — la procédure ne peint jamais elle-
             même) ; l'invalidation passe par InvalidateRect (le
             repaint demandé, jamais volé) ;
         I4 TOUT verdict négatif des blocs routés monte à la barre
             (l'écran nomme le refus — la barre le porte au prochain
             WM_PAINT) : jamais un refus muet, jamais un crash ;
         I5 la balise à la barre (« Loupe 0.1.0-dev.1 — … » — charte
             § 6, D137) ; l'IAT fermée du bloc (D161) ; NOP, 0x90.
Échecs :
  E1 : RegisterClassExW = 0 → MessageBoxW(MB_ICONERROR) PUIS
       ExitProcess(1) — la classe impossible, expliquée puis morte
       (D36 : jamais silencieux).
  E2 : CreateWindowExW = 0 → idem E1 — la vitrine impossible.
Vecteurs :
  V1 : scénario — le témoin ouvert par la ligne de commande : la
       vitrine créée (classe + fenêtre + boucle), l'écran attendu à
       la première peinture, octet par octet (couvre Q1, Q2, Q5).
  V2 : scénario — la commande SANS chemin : la vitrine ouverte avec
       l'usage à la barre, AUCUNE session (le cadre vierge) (couvre
       Q1).
  V3 : émulation — les shims scriptent la file (WM_PAINT, WM_KEYDOWN
       des commandes, WM_CHAR, WM_CLOSE) : CHAQUE routage constaté
       chez son bloc (les appels comptés un à un), DefWindowProcW
       pour le reste (couvre Q3, Q4).
  V4 : rejet — le shim RegisterClassExW à 0 (puis CreateWindowExW à
       0) : MessageBoxW appelée, ExitProcess(1) — l'explication puis
       la mort, AUCUNE boucle lancée (couvre E1, E2).
  V5 : falsification — un routage muté (WM_CHAR dérouté vers
       loupe-16 hors mode saisie) : le scénario diverge — l'oracle à
       scénarios échoue.
Fixtures    : les chaînes UTF-16 .rdata (classe « LoupeHexa », titre
              « Loupe — l'éditeur hexadécimal ») + les libellés de la
              barre (l'usage, les refus, la balise).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT), D33 (PI), D36/D37 (le modèle
              démo : la vitrine s'explique), D38 (les volatils du
              callback), D137 (la balise à la barre).
