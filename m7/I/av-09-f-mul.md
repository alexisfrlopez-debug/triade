av-09 · multiplication modulaire f25519 · révision 1
Intention : multiplier deux valeurs du corps : école 5×5 sur les membres
(25 multiplications u64×u64→u128, accumulation en dix accumulateurs u128 —
l'emprunt sortant d'un accumulateur est IMPOSSIBLE : chaque accumulateur
reçoit < 5·2^104 < 2^107, la marge au 128 bits est 2^21), repli mod p des
cinq membres hauts (×19 : 2^255 ≡ 19), extraction des cinq membres avec
chaîne de retenues 51 bits et retour du débordement du haut, propagation,
freeze — le bloc le plus long du domaine, cœur arithmétique de l'échelon 2.
Contrat :
  pre  : P1 rdi (a) et rsi (b) : opérandes, membres < 2^52 (les VALEURS
             peuvent être lâches < 2^255 : l'école dépend des membres,
             le repli préserve l'équivalence mod p) ; P2 pile alignée.
  post : Q1 la valeur de sortie ≡ a·b (mod p) et est < p (réduite :
             après repli et chaîne, la valeur est < 2^255 + 2^206 < 2p,
             un freeze suffit — la démonstration est dans la spec
             av-07, même structure) ;
         Q2 membres de sortie < 2^52 ; résultat écrit à rdi ; Q3 rax = rdi.
  inv  : I1 les dix accumulateurs u128 vivent sur la pile (160 o) ;
             l'école est une double boucle bornée (i : 0→4, j : 0→4,
             k = i+j, adressage [rsp + k*16] par lea/shl — jamais
             d'index d'échelle 16 direct : l'adressage x86 n'a pas
             d'échelle 16, la notation le montre) ;
         I2 chaque accumulation : mul (rdx:rax = a[i]·b[j]), add lo,
             adc hi — le report au-delà du 128 bits n'est PAS géré car
             impossible (preuve : 2^107 + 2^104 < 2^128) ;
         I3 le repli : C[k] = T[k] + 19·T[k+5] en u128 (mul par 19,
             add/adc) ; l'extraction : r4 = C4 & M51, C0 += 19·(C4>>51),
             puis chaîne r0..r3 avec reports, r4 = C4'&M51, retour final
             r0 += 19·(C4'>>51) ;
         I4 appels directs : av-06 (propagation, UNE fois — le retour
             final laisse membre0 < 2^62, la passe le ramène < 2^52),
             av-10 (freeze, UNE fois) ;
         I5 aucun syscall, aucune donnée RIP (M51, 19 en immédiats) ;
         I6 prologue : non-volatils sauvegardés, sous-cadre 0xc0
             (accumulateurs 160 o + 32 marge), pile 16-alignée aux
             appels.
Échecs :
  E1 : aucun (calcul pur borné : 25 multiplications, 10 replis, 5
       extractions, 2 appels).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle différentiel : a·b mod p contre Python — mille paires
       aléatoires (membres et valeurs), plus les cas punitifs : 0·x,
       1·x, (p−1)·(p−1), x·x (carré), membres saturés (2^52−1 partout),
       a = b = 2^255−1 (valeurs lâches maximales).
  V3 : falsification intégrale (chaque octet de code) — zéro silence.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le choix structurel : accumulateurs u128 EXPLICITES sur
              pile plutôt que l'entrelacement donna par colonnes — la
              notation déroulée reste lisible, la preuve de non-emprunt
              (2^107 << 2^128) tient en une ligne, et l'oracle
              différentiel tranche. R11 (optimisation future) : carré
              dédié (economie de 10 multiplications), fenêtre du
              repli — mesuré, pas supposé.
