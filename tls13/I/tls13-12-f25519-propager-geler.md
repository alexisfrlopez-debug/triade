tls13-12 · f25519 : la propagation des retenues et le gel modulo p · révision 1
Intention : le gardien de l'invariant radix 2^51 — UNE passe séquentielle
0→4 (chaque membre coupé à 51 bits, le trop-plein passe au suivant, le
débordement du cinquième REVIENT au premier multiplié par 19 : 2^255 ≡ 19),
PUIS le gel (retrancher p si et seulement si la valeur représentée est
≥ p). Le miroir win FUSIONNÉ des contrats av-06 et av-10 (M7) : le M9
n'a qu'UNE frontière d'appel pour les deux.
Contrat :
  pre  : P1 rcx = la valeur (5 membres, 40 o — la sortie ÉCRASE) ;
         P2 chaque membre < 2^57 avant la passe (la borne d'entrée
             d'av-06, respectée par tous les producteurs internes :
             additions < 2^53, repli de multiplication < 2^58) ET la
             valeur représentée < 2p après la passe (la borne du gel
             d'av-10 — les producteurs tls13-09/10/11 la démontrent
             avant l'appel) ;
         P3 la pile alignée 16.
  post : Q1 après la passe : membres 1..4 < 2^51, membre 0 < 2^51 +
             19·2^6 < 2^52 (le retour du cinquième est borné — av-06
             Q1) ; la valeur est préservée MODULO p ;
         Q2 après le gel : la valeur < p — si elle était déjà < p, les
             membres sont OCTET-IDENTIQUES (aucune écriture — av-10
             Q1) ; si elle valait exactement p, la sortie est zéro ;
         Q3 rax = 0.
  inv  : I1 l'ordre de la passe est SÉQUENTIEL 0→4 : le membre i masqué
             AVANT que le membre i+1 ne reçoive sa retenue (av-06 I1) ;
             le masque 2^51 − 1 et la constante 19 en IMMÉDIATS —
             aucune donnée RIP ;
         I2 LE GEL EST SANS BRANCHE DE DONNÉES (charte § 3 —
             L'AMÉLIORATION NOMMÉE sur le miroir av-10 : le M7
             branchait jb/ja, le M9 SÉLECTIONNE) : la comparaison
             membre à membre du cinquième au premier produit le
             drapeau « ≥ p » en registre SANS écrire, le masque 0/−1
             diffusé par sar, la soustraction conditionnelle par ET
             logique — le résultat est l'entrée inchangée si < p
             (octet-identique, la même Q2), l'entrée − p sinon ;
         I3 les membres de p sont des CONSTANTES du plan d'adressage
             DÉRIVÉES PAR ARITHMÉTIQUE (p = 2^255 − 19 : (2^51 − 19)
             puis (2^51 − 1)×4 — tls13/layout.py, source unique).
             *Erratum (M9, sur pièces, AVANT la notation — le modèle
             M8-(b) libc-02)* : la spec av-10 (M7) écrit « 0x7ffffffffffedc »
             pour le membre 0 de p — coquille d'ÉCRITURE : quatorze
             chiffres hexadécimaux feraient 55 bits, un membre de 51
             bits en a treize, et le membre 0 de p est 2^51 − 19 =
             0x7ffffffffffed ; l'oracle différentiel d'av-10 (V2 : « p
             → 0 ») ne pouvait passer QU'avec la valeur juste —
             l'écriture seule est fautive, jamais la notation prouvée.
             Le miroir M9 ne copie JAMAIS l'hexadécimal d'une spec : il
             re-dérive par arithmétique, l'oracle du chantier (b)
             confronte les membres contre Python sur mille vecteurs ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; feuille
             dépourvue d'état détenu (charte § 6) ;
         I5 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
