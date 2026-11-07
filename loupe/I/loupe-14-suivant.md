loupe-14 · suivant : l'occurrence suivante au fichier, la FIN nommée · révision 1
Intention : l'occurrence suivante de la suite d'octets CHERCHÉE AU
FICHIER ENTIER — la barre-saisie en mode CHERCHER (Ctrl+F pose le
motif, octets hexa par paires), puis F3 enchaîne : chaque occurrence
trouvée amène le curseur, la vue suit (la règle de loupe-12), et
QUAND IL N'Y EN A PLUS la FIN EST NOMMÉE (verdict -1 : « plus
d'occurrence » à la barre — jamais un silence). La fenêtre glisse par
64 Kio AVEC LE RECOUVREMENT du motif : l'occurrence à cheval sur la
frontière n'est JAMAIS manquée — l'invariant du recouvrement, prouvé
par construction.
Contrat :
  pre  : P1 appelée par la procédure (loupe-09 Q3) : WM_KEYDOWN F3
             (ou Ctrl+F) et les WM_CHAR du mode CHERCHER ; P2 la
             zone MOTIF du plan (48 o) : motif[32] + longueur — le
             motif VIT AU PLAN : F3 reprend le dernier motif, la
             re-saisie n'est jamais exigée.
  post : Q1 LA SAISIE (mode CHERCHER ouvert par Ctrl+F) : paires
             hexa accumulées à la barre (la barre-saisie de loupe-12,
             le mode partagé — le tampon, la correction, l'échappée
             idem : RENVOI, jamais réécrit) ; le commit : le nombre
             de chiffres IMPAIR ou non hexa ou vide → verdict -5 (la
             barre nomme « paires hexa attendues ») ; SINON le motif
             posé à la zone (longueur = chiffres/2, ≤ 32) et LA
             RECHERCHE court depuis le curseur ;
         Q2 LA RECHERCHE AU FICHIER : depuis position (la première
             fois : le curseur ; F3 : le curseur + 1), les fenêtres
             de CUMUL_FENETRE lues à TAMPON_CUMUL (SetFilePointerEx +
             ReadFile), CHAQUE fenêtre confiée à loupe-13 (le départ
             relatif = la position − le bord de fenêtre, borné à 0) ;
             trouvée à l'absolue p → curseur = p, la vue recadrée
             (LA RÈGLE DE LOUPE-12 Q3 — renvoi), loupe-02 (la
             fenêtre relue), InvalidateRect, rax = 0 ;
         Q3 LE RECOUVREMENT : la fenêtre suivante commence à bord +
             CUMUL_FENETRE − (longueur − 1) — l'occurrence À CHEVAL
             sur la frontière est dans les DEUX fenêtres, loupe-13
             la trouve dans la seconde : JAMAIS manquée ;
         Q4 LA FIN : plus de fenêtre et plus d'occurrence → verdict
             -1 (LA FIN NOMMÉE : « plus d'occurrence » à la barre) ;
             le motif DEMEURE à la zone (le F3 suivant reprend — la
             fin n'efface pas la question) ;
         Q5 la lecture ne MODIFIE RIEN (le journal, les empreintes,
             la taille intacts) ; le pointeur fichier repositionné à
             CHAQUE fenêtre.
  inv  : I1 l'exclusion de famille : TAMPON_CUMUL est partagé (05/06/
             07/14 — jamais deux flux simultanés, l'application est
             monofile) ;
         I2 le motif BORNÉ (≤ 32 o — MOTIF_MAX, la borne du
             quotidien : un en-tête, une chaîne, une empreinte) ;
         I3 la recherche est LECTURE SEULE au fichier (aucune
             écriture — l'édition vit chez loupe-16/17) ;
         I4 l'IAT fermée du bloc (SetFilePointerEx, ReadFile,
             GetLastError — la composition loupe-13 PAR LA CARTE) ;
             registres non volatils rendus ; NOP, 0x90.
Échecs :
  E1 : la saisie mal formée (impairs, non hexa, vide) → verdict -5,
       mode = 0, la barre nomme « paires hexa attendues ».
  E2 : sans session ouverte → verdict -4 SESSION, mode = 0.
  E3 : le refus de lecture d'OS (ReadFile/SetFilePointerEx) →
       verdict -6 SYSTÈME relayé, le code consigné, la recherche
       STOPPÉE proprement (la position de départ DEMEURE — rien
       bougé).
Vecteurs :
  V1 : différentiel — sur proxy.exe scellé et les témoins : les
       motifs marqueurs (« MZ », « PEMax ») et 1 000 motifs
       aléatoires : chaque occurrence ET LA FIN comparées à
       bytes.find au fichier entier — l'égalité des positions
       successives (couvre Q2, Q4, Q5).
  V2 : LE RECOUVREMENT PAR CONSTRUCTION — un motif posé À CHEVAL sur
       chaque frontière de fenêtre de 64 Kio du témoin composé pour
       lui (l'occurrence existe uniquement à cheval) : TROUVÉE —
       le recouvrement d'un octet muté à la notation fait MANQUER
       l'occurrence, la différentielle échoue (couvre Q3 — LA
       FALSIFICATION DEMANDÉE).
  V3 : scénario — Ctrl+F « 4d5a », F3 enchaîne les occurrences (le
       curseur suit, la vue recadrée — les écrans attendus), la
       FIN nommée à la barre au dernier F3 (couvre Q1, Q2, Q4).
  V4 : rejet — « 4d5 » (impair), « zz », « » : -5 nommé ; sans
       session : -4 ; le shim ReadFile en échec : -6 relayé, la
       position intacte (couvre E1, E2, E3).
Fixtures    : proxy.exe scellé (les marqueurs de l'ère) + le témoin à
              frontières composées (la preuve du recouvrement).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT), D7 (la composition loupe-13
              PAR LA CARTE).
