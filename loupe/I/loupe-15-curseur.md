loupe-15 · curseur : la cellule active, jamais perdue hors écran · révision 1
Intention : la cellule active du curseur — le déplacement clavier
(flèches, page, début et fin de ligne) BORNÉ au fichier réel, et LA VUE
SUIT : le curseur ne sort JAMAIS de l'écran sans que la fenêtre ne le
rattrape (l'invariant du README). Les bords sont des arrêts NOMMÉS (le
clamp, jamais un rebond) ; la surbrillance, elle, vit à la peinture
(loupe-10 Q3) — 15 ne peint RIEN, la séparation
navigation/peinture est un invariant.
Contrat :
  pre  : P1 appelée par la procédure (loupe-09 Q3) sur WM_KEYDOWN des
             flèches/PgUp/PgDn/Home/End (hors mode saisie — la table
             de routage en décide) ; P2 la session peut être vide (le
             repli nommé).
  post : Q1 LE PAS : VK_GAUCHE/DROITE = ±1 ; VK_HAUT/BAS = ±16 (une
             ligne) ; VK_PRECEDENT/SUIVANT = ±(GRILLE_LIGNES − 2)
             lignes = ±352 (la page, la même unité que loupe-11) ;
             VK_DEBUT = l'aligne16_inf du curseur (le début de
             ligne) ; VK_FIN = min(aligne16_inf + 15, taille − 1)
             (la fin de ligne réelle) ;
         Q2 LA BORNE : curseur' = clamp(curseur ± pas, 0, taille − 1)
             — les bords SONT DES ARRÊTS (à 0, VK_GAUCHE reste à 0 ;
             à taille−1, VK_DROITE/BAS restent : le clamp nommé,
             rax = 0 QUAND MÊME — le bord n'est pas un échec) ;
         Q3 LA VUE SUIT : si le curseur' sort de [vue, vue + lignes
             visibles × 16) : vue = min(recadre(curseur'), vue_max)
             (la règle de recadrage de loupe-12 Q3 — renvoi, la source
             unique) et loupe-02 (la fenêtre relue) + InvalidateRect —
             le curseur JAMAIS perdu hors écran ;
         Q4 rax = 0 ; sans session (P2) : rax = 0 SANS effet (les
             flèches dans la vitrine vide ne bougent rien — le
             repli documenté, rendu à DefWindowProcW).
  inv  : I1 le curseur TOUJOURS dans [0, taille − 1] (l'invariant dur
             du cadre — le clamp PRÉCÈDE tout, la borne est lue au
             cadre, jamais crue de l'appelant) ;
         I2 la vue ne bouge QUE POUR SUIVRE (jamais un défilement
             spontané : curseur dans la fenêtre → la vue est INTACTE
             — le harnais compte les lectures) ;
         I3 le bloc ne peint RIEN, ne touche NI le journal NI les
             empreintes NI le tampon (la navigation est pure
             position) ;
         I4 AUCUNE entrée IAT propre (le recadrage compose loupe-02 —
             la liste fermée du plan) ; registres non volatils
             rendus ; NOP, 0x90.
Échecs :
  E1 : AUCUN échec dur — les bords sont des REPLIS NOMMÉS (le clamp
       de Q2, l'invariant de l'arrêt) ; la justification vit au
       champ Intention : la navigation ne peut pas échouer, elle
       peut S'ARRÊTER — et l'oracle constate l'arrêt.
Vecteurs :
  V1 : différentiel — le modèle Python (pas + clamp + recadrage)
       rejoué sur 10 000 séquences aléatoires de touches : la
       position ET la vue à l'identique (couvre Q1, Q2, Q3, Q4).
  V2 : scénario — le curseur au bord de la fenêtre visible, VK_BAS :
       la vue suit (la ligne active au recadrage), l'écran attendu
       octet par octet ; VK_HAUT en retour : la vue re-suit (couvre
       Q3).
  V3 : scénario — les bords du fichier : à 0 et à taille−1, les pas
       dehors restent (le clamp), rax = 0, la vue INTACTE (aucune
       lecture — les appels comptés) (couvre Q2).
  V4 : scénario — VK_DEBUT/VK_FIN à la ligne finale incomplète : la
       fin de ligne RÉELLE (min(aligne16 + 15, taille−1) — jamais un
       curseur sur un octet qui n'existe pas) (couvre Q1).
  V5 : falsification — la règle de suivi mutée (la vue ne suit pas) :
       le curseur sort de l'écran attendu — l'oracle à scénarios
       échoue (JAMAIS PERDU HORS ÉCRAN est une exigence, pas un
       espoir).
Fixtures    : le témoin de 3 × 64 Kio + 1 (la ligne finale
              incomplète — le cas VK_FIN) + proxy.exe scellé.
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7 (aucune IAT propre — la composition
              seule).
