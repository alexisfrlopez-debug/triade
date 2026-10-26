av-07 · addition modulaire f25519 · révision 1
Intention : additionner deux valeurs du corps : cinq additions membres à
membres, une passe de propagation, une réduction conditionnelle (freeze) —
le résultat est TOUJOURS fortement réduit (< p).
Contrat :
  pre  : P1 rdi et rsi pointent vers les deux opérandes (5 membres
             chacun, membres < 2^52 — l'invariant du domaine) ;
         P2 les zones peuvent se chevaucher partiellement (aucune
             écriture avant la fin des lectures membre à membre :
             l'addition se fait dans un tampon local de 5 u64) ;
         P3 pile alignée.
  post : Q1 la valeur de sortie ≡ a + b (mod p) et est < p (réduite :
             a + b < 2·2^255 < 2^256, une soustraction conditionnelle
             de p suffit — démontré : après propagation la valeur est
             < 2^255 + 2^206 < 2p) ;
         Q2 membres de sortie < 2^52 (invariant) ; le résultat est
             écrit à l'adresse rdi (premier opérande) ;
         Q3 rax = rdi.
  inv  : I1 appels directs : av-06 (propagation, une fois), av-10
             (freeze, une fois) — déclarés, pile 16-alignée aux appels ;
         I2 aucun syscall, aucune donnée RIP ;
         I3 le tampon local (5 u64) vit sur la pile (sous-cadre 40 +
             alignement : prologue 2 pushes + sub 8, miroir ah-07).
Échecs :
  E1 : aucun (bornes garanties par contrat d'entrée).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle différentiel : (a + b) mod p contre Python sur mille
       paires aléatoires + cas limites (0+0, p−1+1 → 0, p−1+p−1,
       2^255−19+0, membres maximaux 2^52−1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La réduction FORTE à la sortie de chaque opération
              arithmétique est la décision structurelle du domaine : elle
              coûte un freeze par opération mais ferme TOUTES les questions
              de bornes des specs aval (sub exige des entrées réduites,
              mul s'en moque — les contrats le disent).
