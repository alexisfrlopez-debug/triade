ah-05 · compression d'un bloc de 64 octets · révision 1
Intention : exécuter la fonction de compression SHA-256 du FIPS 180-4
§ 6.2.2 sur le tampon du contexte — le cœur algorithmique de l'artefact
et le bloc le plus volumineux jamais écrit par l'agent pour lui-même :
annexe de message W[64] sur pile, 64 tours de mélange, addition dans H.
C'est ici que l'expérience d'auto-hébergement pousse le plus loin la
méthode : l'agent écrit à la main ce que le matériel saura faire demain
en instructions SHA-NI (constaté au CPUID du terrain, D34) — la version
scalaire d'abord, mesurée, optimisée ensuite si la mesure l'exige (R11).
Contrat :
  pre  : P1 rdi pointe vers le contexte (112 o, aligné 8) initialisé
             par ah-04 ;
         P2 remplissage == 64 : le tampon contient exactement 64 octets
             valides à comprimer (contrat de coopération — ah-06 et ah-07
             ne l'appellent que dans cet état) ;
         P3 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 pour chaque i : H'[i] = H[i] + f(H, W)[i] au sens exact du
             FIPS (addition modulo 2^32, W dérivé du tampon par
             annexage : 16 mots gros-boutistes chargés, 48 étendus par
             σ0/σ1) ;
         Q2 le tampon et remplissage sont inchangés (== 64) : le bloc
             est une fonction pure de (H, tampon) ;
         Q3 rax n'est pas spécifié (valeur interne).
  inv  : I1 lectures : contexte (H, tampon) et table K[64] @ 0x2000
             (.rodata, 256 o, constantes FIPS § 4.2.2) exclusivement ;
             W[64] vit SUR LA PILE (288 o de cadre) — aucune écriture
             .bss/.data : le bloc est réentrant par construction ;
         I2 feuille : aucun call, la pile descend de 0x150 (48 o de
             non-volatils + 0x120 de cadre) et remontre exactement ;
             les six non-volatils utilisés (rbx, rbp, r12, r13, r14,
             r15) sont poussés et dépilés dans l'ordre strictement
             inverse ;
         I3 la zone rouge de 128 o sous rsp n'est jamais touchée (le
             cadre est alloué par sub, pas par des push implicites) ;
         I4 aucun déplacement RIP hors la table K (donnée pure, adresse
             figée par le plan d'adressage).
Échecs :
  E1 : aucun — la pré-condition P2 est un contrat de coopération : un
       appel avec remplissage ≠ 64 est un défaut de l'APPELANT (ah-06,
       ah-07), pas de ce bloc.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, granularité bloc) : la
       compression du premier bloc du message « abc » (bourré) depuis
       H0 produit l'état intermédiaire exact de la référence FIPS
       dérivée de I (couvre Q1 sur les 64 tours — un seul tour faux
       brise le digest final, détecté par avalanches) ;
  V3 : invariance : comprimer un même tampon depuis deux contextes
       distincts donne des H conformes à la référence sur chacun (pureté
       Q2 — aucune écriture hors H).
Fixtures    : la table K @ 0x2000 (256 o, FIPS § 4.2.2 — donnée pure du
              profil, adressée par déplacement RIP documenté).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Version scalaire : 48 instructions par tour, trois
              boucles (chargement, extension, tours) — la notation
              explicite est produite par l'outil d'arithmétique
              d'adresses de l'auteur depuis un brouillon étiqueté.
              SHA-NI (échelon d'optimisation, R11) ne sera écrit qu'avec
              une mesure qui le justifie — l'optimisation prématurée
              reste interdite sur le terrain de l'auto-hébergement.
