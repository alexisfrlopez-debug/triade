libc-02 · comparaison mémoire normalisée · révision 2
Intention : comparer n octets de deux régions et retourner un verdict exactement
normalisé -1 / 0 / +1 — la magnitude du désaccord n'appartient pas au contrat,
seul son signe est observable.
Contrat :
  pre  : P1 ptr1 (argument 1) : région d'au moins n octets accessible en
             lecture ;
         P2 ptr2 (argument 2) : région d'au moins n octets accessible en
             lecture ;
         P3 n (argument 3) : nombre d'octets à comparer (u64) ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 la valeur de retour (eax) contient -1 si le premier octet
             divergent de ptr1 est strictement inférieur à celui de ptr2
             (comparaison non signée) ;
         Q2 eax contient +1 dans le cas strictement supérieur ;
         Q3 eax contient 0 si les n octets sont égaux (y compris n = 0) ;
         Q4 les octets supérieurs au premier désaccord n'influencent pas le
             verdict (comparaison lexicographique à l'octet).
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie ;
         I3 aucun registre non volatil du profil n'est modifié (frag-con) ;
         I4 les régions comparées ne sont jamais écrites.
Échecs :
  E1 : aucune condition d'échec — la comparaison est totale (n = 0 → verdict 0).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P4, Q1-Q4, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 cas à relations contrôlées
       (égalité, inférieur strict, supérieur strict, divergence en position
       aléatoire, n ∈ [0, 256]) — verdict exact -1/0/+1 contre la référence,
       régions recontrôlées, non volatils, rsp (couvre Q1-Q4, I2-I4).
  V3 : vecteurs dorés embarqués (autotest) : "TRIADE"/"TRIADE" → 0,
       "TRIADE"/"TRIADF" → -1, "TRIADF"/"TRIADE" → +1, préfixe "TRI" → 0
       (couvre Q1-Q4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture mémoire est refusée par l'oracle structurel (couvre I1, I4).
Fixtures    : chaînes SA/SB/SC/SD (référencées par libc-08, au plan de
              l'image).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D26, D28, D29, D149 (révision de granularité).
Historique  : R1 (m1/I, instance Windows scellée 0.2.0) révisée en R2 au
              chantier M6-(b) — granularité (D149-(3)) : arguments nommés
              ptr1/ptr2/n, convention d'appel et non-volatils en frag-con ;
              observables Q1-Q4, E1, vecteurs INVARIANTS ; l'instance Windows
              scellée demeure conforme.
