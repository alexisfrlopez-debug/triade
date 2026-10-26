av-08 · soustraction modulaire f25519 · révision 1
Intention : calculer a − b mod p : additionner 2p membre à membre à a,
retrancher b par soustraction chaînée avec emprunt (l'emprunt final est
IMPOSSIBLE : a + 2p ≥ 2p > b), propager, réduire conditionnellement — le
résultat est toujours fortement réduit.
Contrat :
  pre  : P1 rdi (a) et rsi (b) pointent vers les opérandes (5 membres,
         membres < 2^52) ; la valeur de a est RÉDUITE (< p) ou lâche
         < 2^255 (les deux bornes sont démontrées : a + 2p − b <
         2^257 dans le pire cas, une passe ramène < 2^255 + 2^206) ;
         P2 b est < 2^255 (valeur lâche admise) ;
         P3 pile alignée.
  post : Q1 la valeur de sortie ≡ a − b (mod p) et est < p (réduite) ;
         Q2 membres de sortie < 2^52 ; résultat écrit à rdi ;
         Q3 rax = rdi.
  inv  : I1 les cinq membres de 2p sont chargés par immédiats (2p =
             2^256 − 38 : membres 0xfffffffffffffb8, 0xfffffffffffffe ×4)
             — aucune donnée RIP ;
         I2 appels directs : av-06 (une passe), av-10 (freeze) ;
         I3 la soustraction chaînée utilise sub/sbb : l'emprunt sortant
             du cinquième membre est TESTÉ NUL (verrou du contrat — un
             emprunt sortant serait une violation de P1, le bloc s'arrête
             en échec E1) ;
         I4 prologue 2 pushes + sub 8 (pile locale : 5 u64 de travail).
Échecs :
  E1 : emprunt sortant au cinquième membre (pré-condition violée par
       l'appelant) : le bloc retourne rax = 0 SANS écrire — l'appelant
       contrôlé (specs internes) ne peut pas le provoquer ; l'oracle le
       vérifie par construction sur tous les vecteurs.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle différentiel : (a − b) mod p contre Python — mille paires
       aléatoires réduites, plus a = 0 (→ p − b), a = b (→ 0),
       b = 0 (→ a), a = 1, b = p − 1.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le pré-chargement de 2p en immédiats plutôt qu'une
              rodata : cinq mov imm64 = 50 octets, pas de déplacement RIP,
              le bloc reste autoporteur (R7) — le même choix que av-01
              pour H0.
