loupe-02 · lire : la fenêtre d'octets au tampon de session · révision 1
Intention : lire la fenêtre de TAMPON_SESSION octets (384) à un décalage
donné — dans le tampon du cadre, BORNÉ par la taille réelle (jamais un
octet de trop, jamais un octet au-delà de la fin), puis recouvrir les
octets du journal d'édition : ce que l'utilisateur a écrit demeure
visible après le défilement — la cohérence de vue est un invariant, pas
une chance.
Contrat :
  pre  : P1 la session est ouverte (la poignée du cadre ≠ INVALIDE) ;
         P2 rcx = le décalage de fenêtre, MULTIPLE DE 16 (l'alignement
             de ligne — la grille reste droite) ;
         P3 décalage < taille du fichier (la fenêtre touche au moins un
             octet valide).
  post : Q1 remplissage = min(384, taille − décalage) — posé au cadre
             (+552) ; le tampon (+568) = les octets du fichier
             [décalage, décalage + remplissage) lus par SetFilePointerEx
             PUIS ReadFile (la position repositionnée à CHAQUE lecture —
             jamais une position héritée) ;
         Q2 LE RECOUVREMENT DU JOURNAL : pour chaque entrée du journal
             (loupe-16) dont le décalage ∈ [décalage, décalage +
             remplissage), l'octet du tampon REMPLACÉ par l'octet écrit
             — l'édition survit au défilement ;
         Q3 rax = 0 ; la vue et le curseur du cadre INTACTS (lire ne
             déplace rien — le défilement est à loupe-11).
  inv  : I1 la borne est LUE AU CADRE (la taille), jamais passée par
             l'appelant — un décalage faux est un refus, pas une
             confiance ;
         I2 la lecture ne touche QUE le tampon du cadre — jamais
             TAMPON_CUMUL (la fenêtre des empreintes et de la recherche,
             l'exclusion de famille), jamais l'ECRAIN (la composition
             est à loupe-10) ;
         I3 JAMAIS un octet au-delà de la fin : remplissage ≤ 384 ET
             décalage + remplissage ≤ taille — la double borne, la
             lecture s'arrête à la taille réelle ;
         I4 l'IAT déclarée (D161) : SetFilePointerEx, ReadFile,
             GetLastError — la liste fermée du bloc ; registres non
             volatils rendus ; NOP, 0x90.
Échecs :
  E1 : sans session ouverte (P1) → verdict -4 SESSION, rien lu, rax =
       -4.
  E2 : décalage non multiple de 16 (P2) → verdict -5 ENTRÉE, rien lu —
       la grille ne se penchera pas.
  E3 : décalage ≥ taille (P3) → verdict -3 HORS-BORNES, rien lu — la
       fenêtre au-delà de la fin n'existe pas.
  E4 : ReadFile ou SetFilePointerEx en échec → verdict -6 SYSTÈME, le
       code GetLastError consigné, remplissage = 0 (fail-closed : le
       tampon ne montre JAMAIS un octet non lu).
Vecteurs :
  V1 : différentiel — les témoins du kit + proxy.exe scellé : le tampon
       comparé octet par octet à la découpe Python à 1 000 décalages
       aléatoires valides (couvre Q1, Q3).
  V2 : différentiel du recouvrement — des écritures au journal aux
       décalages des bords de fenêtre (le premier, le dernier, le
       hors-fenêtre) : le tampon recouvert == le modèle Python (couvre
       Q2).
  V3 : rejet — sans session, décalage non aligné, décalage à la taille
       exacte, décalage au-delà : les QUATRE verdicts nommés, rien lu
       (couvre E1, E2, E3).
  V4 : rejet — le shim ReadFile en échec : verdict -6, remplissage 0,
       le code consigné par le harnais (couvre E4).
  V5 : falsification — un octet du tampon muté après lecture : la
       composition d'écran diverge de l'attendu, l'oracle échoue.
Fixtures    : les témoins du kit (1 o, 384 o, 3 × 64 Kio + 1) + proxy.exe
              scellé (446279f3…) — les découpes recoupées par hashlib.
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7/D35 (l'IAT).
