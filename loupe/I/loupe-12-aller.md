loupe-12 · aller : la saisie hexadécimale à la barre, le refus nommé · révision 1
Intention : aller à un décalage tapé en hexadécimal — LA BARRE-SAISIE :
aucun contrôle enfant, la barre d'état DEVIENT le champ (l'écran
appartient à Loupe). Le saut est EXACT (le curseur à la valeur) et
ENCADRÉ : la saisie mal formée est refusée nommément, la valeur hors
bornes est refusée nommément — JAMAIS un saut silencieux, jamais un
recalage deviné. La règle de recadrage de la vue est déclarée ICI (les
blocs 14 et 15 la citent — la source unique).
Contrat :
  pre  : P1 appelée par la procédure (loupe-09 Q3) : WM_KEYDOWN F5 ou
             Ctrl+G OUVERT le mode, puis les WM_CHAR du mode lui
             reviennent ; P2 la zone SAISIE du plan (96 o : mode,
             actif, nibble, tampon[80]).
  post : Q1 L'OUVERTURE : mode = ALLER, le tampon vide, la barre
             montre « ALLER (hexa) : » — la vitrine vit, la barre
             écoute ;
         Q2 LA FRAPPE : chiffre hexa (0-9A-Fa-f) → accumulé (au plus
             8 chiffres — le 9e IGNORÉ proprement, la borne du
             format 0x7FFFFFFF à 8 chiffres) ; VK_SUPPR → le dernier
             chiffre retiré ; VK_ECHAP → mode = 0, la barre revient
             (l'annulation PROPRE, rien arrivé) ;
         Q3 LE COMMIT (VK_RETOUR) : le tampon VIDE ou non hexa →
             verdict -5 (la barre nomme « saisie mal formée ») ; la
             valeur ≥ taille → verdict -3 (la barre nomme « hors
             bornes » — LE REFUS NOMMÉ du README) ; SINON : curseur =
             la valeur, ET LA RÈGLE DE RECADRAGE : si le curseur
             sort de la fenêtre visible, vue = min(recadre(curseur),
             vue_max) — la ligne active posée à la 12e ligne quand la
             place se trouve, le bord sinon (la règle EXÉCUTABLE du
             plan d'adressage), loupe-02 (la fenêtre relue), mode =
             0, InvalidateRect — LE SAUT EXACT ;
         Q4 rax = 0 au saut ; les refus rendent leur verdict ET
             SORTENT du mode (la barre porte le nom, l'oracle le
             constate).
  inv  : I1 la barre-saisie N'EST PAS un contrôle : aucun EDIT enfant,
             aucun focus à rendre — les frappes reviennent par la
             procédure, l'écran reste à Loupe ;
         I2 la saisie ne touche NI le tampon de vue NI le journal NI
             les empreintes (le saut est une navigation, pas une
             édition) ;
         I3 le curseur reste BORNÉ [0, taille−1] (l'invariant du
             cadre — le saut y passe, jamais au travers) ;
         I4 AUCUNE entrée IAT propre (le bloc est pur état + la
             composition : loupe-02 et l'invalidation vivent chez
             leurs propriétaires — la liste IAT du plan, la barre de
             loupe-10 peint) ; NOP, 0x90.
Échecs :
  E1 : le commit d'une saisie vide ou non hexa → verdict -5 ENTRÉE,
       mode = 0, la barre nomme « saisie mal formée ».
  E2 : la valeur ≥ taille → verdict -3 HORS-BORNES, mode = 0, la
       barre nomme « hors bornes » — JAMAIS un saut silencieux.
  E3 : sans session ouverte → verdict -4 SESSION, mode = 0 (la barre
       nomme « aucun fichier ouvert »).
Vecteurs :
  V1 : scénario — le saut au milieu (0x1000) : le curseur exact, la
       vue recalée à la 12e ligne, l'écran attendu octet par octet ;
       le saut à 0 et au dernier octet : la règle de recadrage au
       bord (couvre Q1, Q3, Q4).
  V2 : scénario — la frappe : 8 chiffres max (le 9e ignoré, le
       tampon inchangé — le différentiel le constate), VK_SUPPR
       retire, VK_ECHAP annule TOUT proprement (la barre revient,
       rien bougé) (couvre Q2).
  V3 : rejet — « », « 12Z4 », « 0x10 » (le x n'est pas hexa) :
       verdict -5 nommé ; 0x7FFFFFFF sur un témoin de 100 o :
       verdict -3 nommé ; sans session : -4 (couvre E1, E2, E3).
  V4 : différentiel — la règle recadre(curseur) rejouée en Python
       sur 10 000 curseurs aléatoires : l'égalité des vues (couvre
       Q3).
  V5 : falsification — le recadrage muté d'une ligne : l'écran
       attendu du saut diverge — l'oracle échoue.
Fixtures    : le témoin de 3 × 64 Kio + 1 (les sauts aux bords des
              fenêtres de lecture).
Provenance  : écrite-avant-code.
Décisions   : D171, D161 (la zone SAISIE déclarée), D7 (aucune IAT
              propre — la barre appartient à l'écran).
