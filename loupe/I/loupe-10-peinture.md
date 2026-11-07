loupe-10 · peinture : WM_PAINT, l'unique peintre · révision 1
Intention : dessiner la fenêtre visible — composer l'écran (l'entête,
les lignes par loupe-08, la barre d'état avec le PANNEAU
D'EMPREINTES) puis le peindre (BeginPaint, la police à chasse fixe,
TextOutW ligne à ligne, la cellule active en inverse, EndPaint). La
mesure de la police a lieu UNE fois. L'expansion latin-1 octet→mot
est exacte. L'oracle à scénarios compare l'écran attendu OCTET PAR
OCTET — la peinture est la preuve visible du domaine.
Contrat :
  pre  : P1 appelée par la procédure (loupe-09 Q3) sur WM_PAINT —
             jamais ailleurs ; P2 la session peut être VIDE (la
             vitrine sans fichier peint l'usage : P2 n'est PAS une
             précondition d'état) ; P3 l'IAT gdi32/user32 du bloc
             résolue.
  post : Q1 LA COMPOSITION (l'ECRAIN, 2320 o) : l'entête posée (la
             chaîne .rdata, 65 o utiles) ; la grille : pour chaque
             ligne visible i de 0 à min(lignes_affichables − 1,
             remplissage/16 arrondi) : loupe-08(tampon + 16·i, min(16,
             remplissage − 16·i), grille + 80·i, vue + 16·i) — les
             lignes au-delà de la fin restent VIERGES (jamais une
             ligne fantôme) ; la barre ligne 1 : « Loupe 0.1.0-dev.1 —
             <chemin> · <taille> o · curseur 0xNNNNNNNN · MODIFIÉ »
             (ou l'usage si session vide) ; la barre ligne 2 (LE
             PANNEAU) : « md5 <32 hex> · sha256 <64 hex> » (ou « — »)
             — l'astérisque si la marque sale est posée (les
             empreintes du DISQUE, la divergence nommée) ;
         Q2 LA PEINTURE : BeginPaint (la PAINTSTRUCT sur la pile) ; la
             police ANSI_FIXED_FONT sélectionnée (GetStockObject +
             SelectObject), mesurée UNE fois (GetTextMetricsW →
             METRIQUES : char_w, ligne_h, lignes_visibles — jamais
             re-mesurée tant que la fenêtre vit) ; chaque ligne de
             l'ECRAIN expansée latin-1 octet→mot (le tampon pile de
             80 mots) puis TextOutW à (MARGE_X, MARGE_Y + ligne ·
             ligne_h) ; EndPaint ;
         Q3 LA CELLULE ACTIVE : la colonne du groupe hexa du curseur
             repeinte en INVERSE (SetTextColor/SetBkColor échangés
             autour de CE groupe seul, à l'abscisse exacte
             MARGE_X + (10 + 3·colonne + (colonne ≥ 8 ? 1 : 0)) ·
             char_w) — la surbrillance vit à la peinture, la position
             au cadre (loupe-15 ne peint RIEN) ;
         Q4 rax = 0.
  inv  : I1 L'UNIQUE PEINTRE : aucune goutte hors WM_PAINT, aucun
             autre bloc ne déclare TextOutW (la liste IAT fermée du
             plan — la contrebande de peinture est un refus de build) ;
         I2 le CLIPPING par lignes affichables : jamais un TextOutW
             au-delà du client (GetClientRect lu à CHAQUE peinture —
             la fenêtre peut rétrécir) ;
         I3 la police À CHASSE FIXE est une EXIGENCE (ANSI_FIXED_FONT
             — les colonnes hexa sinon se disloquent : le refus de la
             police proportionnelle est un choix de domaine) ;
         I4 l'expansion latin-1 EXACTE : chaque octet de l'ECRAIN →
             le mot UTF-16 de même valeur (0x00–0xFF → U+0000–U+00FF,
             la table est l'identité) — jamais un octet signé ;
         I5 la composition ne MODIFIE RIEN : le cadre, le journal, les
             empreintes LUS seuls (la peinture est pure lecture
             d'état) ; registres non volatils rendus ; NOP, 0x90.
Échecs :
  E1 : BeginPaint rend un DC nul → verdict -6 SYSTÈME (le code
       GetLastError consigné), RIEN peint, rax = -6 (jamais un
       dessin sur un contexte mort).
  E2 : GetStockObject ou GetTextMetricsW en échec (0 / le tm nul) →
       verdict -6 SYSTÈME, la peinture AVORTÉE proprement (EndPaint
       appelé quand même — le contexte se rend TOUJOURS).
Vecteurs :
  V1 : scénario — la vitrine sans session : l'ECRAIN composé (l'usage
       à la barre 1, les « — » au panneau) puis peint : l'écran
       attendu octet par octet (couvre Q1, Q2, Q4).
  V2 : scénario — le témoin ouvert (vue 0, curseur 0x22) : les 24
       lignes ou moins (le remplissage borne), la cellule active
       inversée à la colonne exacte, le panneau aux empreintes du
       disque — l'attendu intégral (couvre Q1, Q2, Q3).
  V3 : scénario — la marque sale : l'astérisque au panneau, « MODIFIÉ
       » à la barre 1 (la divergence nommée) (couvre Q1).
  V4 : rejet — le shim BeginPaint à 0 : verdict -6, rien peint,
       EndPaint déménagé jamais appelé sur DC nul — l'état demeure
       propre (couvre E1) ; le shim GetTextMetricsW muet : la
       peinture avortée proprement (couvre E2).
  V5 : falsification — une ligne de la grille mutée d'un octet dans
       l'ECRAIN : l'attendu diverge — l'oracle échoue (la
       falsification DEMANDÉE, charte § 3).
Fixtures    : les écrans attendus du kit (la vitrine vide, le témoin à
              la vue 0, la ligne finale incomplète, la marque sale) —
              les fixtures du dépôt, consignées au harnais.
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT), D134 (la balise peinte),
              D137 (la lignée).
