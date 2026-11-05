tls13-01 · SHA-256 : initialisation du contexte · révision 1
Intention : poser l'état initial du hachage FIPS 180-4 — les HUIT constantes
H0 de la § 5.3.1 dans le contexte donné, les compteurs à zéro. Le miroir win
du contrat ah-04 (M6) : la même sémantique, l'ABI msx64, et le contexte en
ARGUMENT (charte § 6 — TLS exige des hachages multiples simultanés, jamais
une adresse fixe).
Contrat :
  pre  : P1 rcx = le pointeur du contexte (112 o accessibles en écriture,
             aligné 8 — la disposition : H[8] u32 @ +0 [stockage natif
             petit-boutiste], tampon[64] @ +32, remplissage u32 @ +96 [octets
             valides du tampon], réservé u32 @ +100, total u64 @ +104 [octets
             absorbés cumulés] — la disposition de ah, l'adresse en plus) ;
         P2 la pile est alignée 16 à l'entrée, l'ombre msx64 0x20 fournie
             par l'appelant (le bloc est une fonction ordinaire de la
             lignée — aucune des contraintes de pile du domaine sys ne
             s'applique au calcul pur).
  post : Q1 H[0..7] = les HUIT constantes initiales de FIPS 180-4 § 5.3.1
             (1779033703, 3144134277, 1013904242, 2773480762, 1359893119,
             2600822924, 528734635, 1541459225 — les valeurs vivent au plan
             d'adressage, source unique) ;
         Q2 remplissage = 0, total = 0 (le tampon n'a pas besoin d'être
             effacé — remplissage le rend inerte) ;
         Q3 rax = 0 (le verdict OK de la table du domaine).
  inv  : I1 le bloc ne déclare AUCUNE entrée IAT, AUCUN site syscall
             (charte § 7 — calcul pur) ;
         I2 le bloc ne détient AUCUN état : rien en .data, rien en .bss,
             aucune écriture hors du contexte pointé (charte § 6) ;
         I3 les constantes H0 sont des DONNÉES PUBLIQUES en lecture seule
             (.rdata du domaine) — le temps constant n'a rien à sceller ici
             (la charte § 3 s'applique aux données secrètes : l'init n'en
             touche aucune) ;
         I4 aucun registre non volatil détruit (rbx, rbp, rdi, rsi, r12-r15,
             rsp — le bloc rend la main propre) ;
         I5 la croissance du slot est NOP, 0x90 (charte § 8).
