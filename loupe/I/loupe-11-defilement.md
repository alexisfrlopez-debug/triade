loupe-11 · défilement : la molette et l'ascenseur, bornés à la fin réelle · révision 1
Intention : faire glisser la fenêtre de vue — la molette (TROIS lignes
par cran), l'ascenseur (la ligne, la page, la poignée glissée), le
recalage au redimensionnement — TOUJOURS BORNÉ : jamais un décalage au-
delà de la fin réelle du fichier, et la DERNIÈRE fenêtre VOIT le
dernier octet (la borne supérieure est l'arrondi au-dessus, pas en
dessous). L'alignement à 16 octets est inviolable : la grille reste
droite, les lignes demeurent des lignes.
Contrat :
  pre  : P1 appelée par la procédure (loupe-09 Q3) sur WM_SIZE,
             WM_VSCROLL ou WM_MOUSEWHEEL ; P2 la session peut être
             vide (le repli nommé, pas un échec).
  post : Q1 LE PAS : SB_LIGNE_HAUT/BAS = ±16 o ; SB_PAGE_HAUT/BAS =
             ±(GRILLE_LIGNES − 2) lignes = ±352 o ; SB_POIGNEE/
             SB_POIGNEE_COURSE = la position demandée × 16 (GetScroll-
             Info — l'ascenseur parle en LIGNES, le cadre en octets) ;
             WM_MOUSEWHEEL = ±(delta / MOLETTE_CRAN) × 48 o (TROIS
             lignes par cran, le signe du delta) ;
         Q2 LA BORNE : vue' = clamp16(vue ± pas) dans [0, vue_max] —
             vue_max = aligne16_sup(max(0, taille − 384)) : la
             DERNIÈRE fenêtre montre le DERNIER octet (le
             remplissage final peut être court — la fin n'est jamais
             cachée) ; les fichiers ≤ 384 o ne défilent PAS (vue = 0,
             le petit fichier tient entier) ;
         Q3 le GESTE : si vue' ≠ vue : loupe-02 (la fenêtre relue —
             le recouvrement du journal y vit), SetScrollInfo (min 0,
             max vue_max/16, pos vue'/16, page = lignes visibles —
             l'ascenseur TOUJOURS synchrone), InvalidateRect (le
             repaint demandé) ; si vue' = vue : RIEN (le geste au
             bout ne relit pas — l'OS au bout reste calme) ;
         Q4 WM_SIZE : les lignes visibles recalculées (client_h /
             ligne_h — les métriques de loupe-10), l'ascenseur remis,
             l'écran invalidé — la fenêtre rétrécie ou grandie
             n'affiche JAMAIS de lignes fantômes ;
         Q5 rax = 0 ; sans session (P2) : rax = 0 SANS AUCUN effet
             (l'écran vide ne défile pas — le repli documenté, le
             message rendu à DefWindowProcW).
  inv  : I1 TOUTE vue est multiple de 16 (l'alignement inviolable —
             la composition de loupe-08 l'exige, la grille le
             garde) ;
         I2 le clamp PRÉCÈDE la lecture (jamais une lecture hors
             fichier, jamais un remplissage négatif — la borne est un
             repli NOMMÉ, pas un échec : le geste au-delà de la fin
             S'ARRÊTE à la fin) ;
         I3 l'ascenseur ne ment JAMAIS (SetScrollInfo après CHAQUE
             mouvement réel — jamais une position affichée divergente
             du cadre) ;
         I4 le défilement ne touche NI le curseur (il suit sa vie à
             loupe-15 — le curseur peut sortir de l'écran par le
             défilement, jamais par lui-même) NI le journal NI les
             empreintes ; l'IAT fermée (GetScrollInfo, SetScrollInfo,
             InvalidateRect, GetClientRect, GetLastError) ; NOP, 0x90.
Échecs :
  E1 : GetScrollInfo en échec (la structure SCROLLINFO invalide) →
       verdict -6 SYSTÈME, le code consigné, le geste de poignée
       ABANDONNÉ proprement (vue inchangée, l'ascenseur non touché).
Vecteurs :
  V1 : différentiel — la règle vue_max rejouée en Python sur 10 000
       tailles aléatoires (0, 1, 384, 385, 3 × 64 Kio + 1, 2 Gio) :
       l'égalité des bornes et du clamp (couvre Q1, Q2).
  V2 : scénario — la molette au bout : la dernière fenêtre VOIT le
       dernier octet (le remplissage court), l'écran attendu au
       dernier décalage (couvre Q2, Q3).
  V3 : scénario — le petit fichier (≤ 384 o) : la molette et
       l'ascenseur SANS effet (vue = 0), rien relu (les appels
       comptés) (couvre Q2, Q5).
  V4 : scénario — WM_SIZE (la fenêtre rétrécie de moitié) : les
       lignes visibles recalculées, aucune ligne fantôme à la
       première peinture suivante (couvre Q4).
  V5 : rejet — le shim GetScrollInfo en échec : verdict -6, vue
       intacte (couvre E1).
Fixtures    : les témoins du kit (1 o, 384 o exactement, 3 × 64 Kio +
              1 — les trois formes de la borne).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT).
