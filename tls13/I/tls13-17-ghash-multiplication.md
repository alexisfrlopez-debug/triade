tls13-17 · GHASH : la multiplication GF(2^128) · révision 1
Intention : la multiplication du corps de GCM (SP 800-38D § 6.3) — la
convention réfléchie de GCM : la chaîne de 16 octets, la constante de
réduction R = 0xE1 suivi de quinze octets nuls. La marche de
l'algorithme 1 de la § 6.3, MOT POUR MOT : Z ← 0, V ← Y ; pour chaque
bit de X (du premier au dernier de la chaîne) : si le bit est à 1,
Z ← Z ⊕ V ; V est décalé d'un bit, le bit sortant déclenche le repli
V ← V ⊕ R. SANS TABLE PAR DONNÉE (la table de Shoup indexée par les
octets de H est la faille classique que la charte § 3 interdit : la
marche est lente ET constante — le choix minimal auditable).
Contrat :
  pre  : P1 rcx = la sortie Z (16 o) ; P2 rdx = X (16 o) ; P3 r8 = Y
             (16 o — les trois zones peuvent se chevaucher : le bloc
             charge X et Y AVANT d'écrire) ;
         P4 la pile alignée 16.
  post : Q1 Z = X • Y dans GF(2^128) — SP 800-38D § 6.3 ; la
             multiplication est COMMUTATIVE (le harnais du chantier (b)
             vérifie les DEUX ordres) ; prouvée par l'ORACLE
             DIFFÉRENTIEL (Python, mille paires aléatoires + les cas
             X = 0, Y = 0, X = Y = 1, X = Y = R) ET en bout en bout par
             les vecteurs GCM (tls13-18/19 : la valeur de H et les
             étiquettes des Test Cases McGrew–Viega/CAVP) ;
         Q2 X et Y INTACTS ; Q3 rax = 0.
  inv  : I1 LE SANS-BRANCHE NOMMÉ (charte § 3) : le bit de X devient un
             MASQUE 0/−1 (la diffusion arithmétique du bit par sar), la
             sélection Z ← Z ⊕ (V ET masque) — AUCUNE instruction de
             branch ne lit X, Y ni V ; les 128 itérations s'exécutent
             TOUJOURS ;
         I2 le décalage de V et le repli : le bit sortant (le bit 0 de
             l'octet 15) devient LE MASQUE du repli (V ← (V décalé) ⊕
             (R ET masque-sortant)) — le repli est sans branche lui
             aussi ; R est une CONSTANTE du plan d'adressage (16 o
             publics) ;
         I3 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6 — les transitoires en registres
             xmm/généraux et sur la pile) ;
         I4 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8) ;
         I5 frontière nommée : PCLMULQDQ (la multiplication matérielle
             sans retenue) est un CHANTIER FUTUR NOMMÉ d'optimisation —
             mesuré, pas supposé (le miroir R11 de av-09) ; la marche
             binaire est la transcription EXACTE de la norme.
