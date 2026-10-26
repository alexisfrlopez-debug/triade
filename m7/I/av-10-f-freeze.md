av-10 · réduction conditionnelle f25519 (freeze) · révision 1
Intention : retrancher p si et seulement si la valeur représentée est ≥ p —
la réduction forte qui clôt chaque opération du domaine. La comparaison est
membre à membre du cinquième au premier (ordre big-endian de la valeur),
la soustraction est une chaîne sub/sbb avec les cinq membres de p en
immédiats.
Contrat :
  pre  : P1 rdi pointe vers 5 membres (40 o) ; P2 la valeur représentée
             est < 2p = 2^256 − 38 (borne garantie par les appelants :
             add/sub/mul démontrent leur sortie < 2p avant l'appel) ;
             P3 membres < 2^52 ; P4 pile alignée.
  post : Q1 la valeur de sortie est < p : si l'entrée était < p, la
             sortie est OCTET-IDENTIQUE à l'entrée (aucune écriture) ;
             sinon la sortie est l'entrée − p (valeur, la représentation
             membres suit) ;
         Q2 rax = rdi (chaînage libre).
  inv  : I1 la comparaison part du membre 4 (poids fort) : cmp puis
             jb (inférieur strict : sorti, la valeur est < p — les
             membres égaux contincent vers le poids faible), ja (le
             membre est plus grand : la valeur est > p — soustraction),
             égalité au membre 0 : jae (≥ p : soustraction, le cas
             d'égalité p exact rend 0) ;
         I2 la soustraction : cinq sub/sbb chaînés, membres de p en
             immédiats (0x7ffffffffffedc, 0x7ffffffffffff ×4) — aucune
             donnée RIP ;
         I3 feuille : aucun appel, aucun syscall, aucun non-volatil,
             0 octet de pile.
Échecs :
  E1 : aucun (la borne P2 rend la soustraction sans emprunt sortant :
       valeur ≥ p garantit le résultat ≥ 0).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle : valeurs 0, p−1 (inchangées), p (→ 0), p+1 (→ 1),
       2p−1 (→ p−1), plus 500 valeurs aléatoires dans [0, 2p) — la
       sortie comparée à v mod p en Python, et l'invariance
       octet-identique pour v < p vérifiée membre à membre.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le freeze à soustraction UNIQUE (pas de boucle) est
              rendu possible par la démonstration de borne < 2p dans les
              specs appelantes — c'est le contrat P2 qui porte la preuve,
              la notation ne fait que l'exécuter.
