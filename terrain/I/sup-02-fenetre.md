sup-02 · fenêtre principale · révision 1
Intention : créer la vitrine du superviseur — la même coquille que la démo
M2 (classe dédiée, curseur flèche, fond bouton, fenêtre 780x560 visible),
mais à SON nom : classe "TRIADE_superviseur", titre "TRIADE superviseur
terrain", pour que FindWindowW("TRIADE_demo") de sup-33 trouve la fenêtre
DE LA DÉMO et jamais la nôtre. Les traces L00/L01/LKO_GUI passent par
win-05 scellé (miroir écran + fichier) — le journal terrain naît ici.
Contrat :
  pre  : P1 TAMPON_NOM déjà posé par sup-01 (sinon le journal s'ouvre sous
         un nom vide — P1 de sup-01) ; P2 IAT résolue (D35) ; P3 pile
         alignée.
  post : Q1 WNDCLASSEXW complète sur pile (cbSize 0x50, style 3, wndproc
         = win-04 scellé @0x1640, hInstance GetModuleHandleW(0), curseur
         IDC_ARROW, fond COLOR_BTNFACE+1, classe "TRIADE_superviseur") ;
         Q2 RegisterClassExW = 0 -> trace LKO_GUI (36 o, mode 1, valeur
         GetLastError) + MessageBoxW + rax = 0 ; Q3 CreateWindowExW
         (WS_OVERLAPPEDWINDOW|WS_VISIBLE, CW_USEDEFAULT x2, 780x560,
         titre "TRIADE superviseur terrain") : NULL -> même chemin d'échec
         que Q2 ; Q4 succès -> HWND_PRINCIPAL posé (.data 0x3860), trace
         L01 (28 o), rax = hwnd. Le WM_CREATE/WM_SIZE imbriqués créent les
         contrôles et journalisent L02/L4C/L4D par win-04 scellé.
  inv  : I1 aucune adresse absolue (position-indépendant, D33) — toutes
         les références RIP-relatives ; I2 traces via win-05 uniquement
         (jamais win-11 en direct — le jumeau muet de demo.2 ne revient
         pas) ; I3 chaînes UTF-16 posées aux adresses du plan (CLASSE
         0x29C0, TITRE 0x29E6, TXT_BOUTON 0x2A1E inchangé : win-04 scellé
         le lit).
Échecs :
  E1 : RegisterClassExW = 0 -> LKO_GUI + GetLastError + MessageBoxW +
       rax = 0 (sup-01 sort io-02(1)).
  E2 : CreateWindowExW = NULL -> même chemin (LKO_GUI, gle, boîte, 0).
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation : classe enregistrée ("TRIADE_superviseur", wndproc
       0x1640 vérifié dans l'image), WM_CREATE/WM_SIZE dispatchés pour de
       vrai, contrôles créés, L00/L02/L4C/L4D/L01 dans le fichier journal
       dans cet ordre, rax = hwnd.
  V3 : échec piloté RegisterClassExW = 0 -> MessageBoxW + sortie 1.
  V4 : anti-collision — le titre ET la classe diffèrent de ceux de la
       démo ("TRIADE_demo" / "TRIADE M2 — démonstration complète") :
       verrou de différenciation lexicale dans l'oracle.
Fixtures    : chaînes UTF-16 (CLASSE, TITRE, MSG_ECHEC_GUI) et ASCII
              (L00 50 o, L01, LKO_GUI) aux adresses du plan.
Provenance  : écrite-avant-code.
Décisions   : D48 ; gabarit win-02:R3 (coquille éprouvée au terrain) ;
              titre sans tiret cadratin (27 caractères — la pose séquentielle
              doit retomber sur TXT_BOUTON @0x2A1E, adresse scellée par
              win-04, D48 : contrainte de pose documentée).
