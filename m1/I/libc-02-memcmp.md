libc-02 · comparaison mémoire normalisée · révision 1
Intention : comparer n octets de deux régions et retourner un verdict exactement
normalisé -1 / 0 / +1 — la magnitude du désaccord n'appartient pas au contrat,
seul son signe est observable.
Contrat :
  pre  : P1 rcx contient ptr1, région d'au moins n octets accessible en lecture ;
         P2 rdx contient ptr2, région d'au moins n octets accessible en lecture ;
         P3 r8 contient n, nombre d'octets à comparer (u64) ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 eax contient -1 si le premier octet divergent de ptr1 est
         strictement inférieur à celui de ptr2 (comparaison non signée) ;
         Q2 eax contient +1 dans le cas strictement supérieur ;
         Q3 eax contient 0 si les n octets sont égaux (y compris n = 0) ;
         Q4 les octets supérieurs au premier désaccord n'influencent pas le
             verdict (comparaison lexicographique à l'octet).
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie ;
         I3 aucun registre non volatil n'est modifié ;
         I4 les régions comparées ne sont jamais écrites.
Échecs :
  E1 : aucune condition d'échec — la comparaison est totale (n = 0 → verdict 0).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P4, Q1-Q4, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 cas à relations contrôlées
       (égalité, inférieur strict, supérieur strict, divergence en position
       aléatoire, n ∈ [0, 256]) — verdict exact -1/0/+1 contre la référence,
       régions recontrôlées, non volatils, rsp (couvre Q1-Q4, I2-I4).
  V3 : vecteurs dorés embarqués (autotest b20008) : "TRIADE"/"TRIADE" → 0,
       "TRIADE"/"TRIADF" → -1, "TRIADF"/"TRIADE" → +1, préfixe "TRI" → 0
       (couvre Q1-Q4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture mémoire est refusée par l'oracle structurel (couvre I1, I4).
Fixtures    : chaînes .rdata SA/SB/SC/SD (référencées par libc-08).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29.
