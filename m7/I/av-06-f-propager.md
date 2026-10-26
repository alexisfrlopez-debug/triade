av-06 · passe de propagation de retenues f25519 · révision 1
Intention : une passe de réduction des membres : chaque membre est coupé à
51 bits, le trop-plein passe au suivant, et le débordement du cinquième
revient au premier multiplié par 19 (2^255 ≡ 19 mod p) — le gardien de
l'invariant radix 2^51. La valeur représentée est préservée MODULO p
(la passe est une réécriture équivalente : ΔV = −c·2^255 + 19c ≡ 0).
Contrat :
  pre  : P1 rdi pointe vers 5 membres u64 (40 o) ; P2 chaque membre est
             < 2^57 (borne d'entrée — respectée par tous les producteurs
             internes : additions < 2^53, fold de multiplication < 2^58) ;
         P3 pile alignée.
  post : Q1 membres 1..4 < 2^51 ; membre 0 < 2^51 + 19·2^6 < 2^52 (le
             retour du cinquième membre est borné : c4 < 2^57/2^51 = 2^6,
             19·2^6 = 1216) ;
         Q2 la valeur V' = Σ m'[i]·2^51i satisfait V' ≡ V (mod p) —
             la passe ne change QUE la représentation ;
         Q3 rax = rdi (chaînage libre).
  inv  : I1 l'ordre est SÉQUENTIEL 0→4 : le membre i est masqué AVANT que
             le membre i+1 ne reçoive sa retenue — à la fin de la passe,
             seuls le membre 0 (retour 19·c4) peut dépasser 2^51 ;
         I2 feuille : aucun appel, aucun syscall, aucun non-volatil,
             0 octet de pile ;
         I3 masque 0x7ffffffffffff en immédiat ; la constante 19 en
             immédiat (imul rdx, rdx, 19) — aucune donnée RIP.
Échecs :
  E1 : aucun (cinq coupes et quatre reports bornés).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété (oracle) : sur membres aléatoires < 2^57, la sortie
       satisfait Q1 (bornes par membre, mille vecteurs) et V' ≡ V mod p
       (recomposition arithmétique exacte).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La borne d'entrée 2^57 laisse 6 bits de marge au-dessus
              de 51 : c'est ce garde-fou qui autorise les appels UNIQUEMENT
              depuis des producteurs bornés (I2 des specs appelantes) —
              le contrat n'est pas une politesse, il est la preuve.
