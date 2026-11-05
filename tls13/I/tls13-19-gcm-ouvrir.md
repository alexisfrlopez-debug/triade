tls13-19 · GCM : ouvrir · révision 1
Intention : l'inverse EXACT de tls13-18 — avec LA DISCIPLINE DU VERDICT :
l'étiquette est RECALCULÉE sur le chiffré reçu et CONFRONTÉE AVANT TOUTE
restitution (RFC 8446 § 5.2 : l'enregistrement entier doit être
authentifié avant de rendre un octet — jamais l'inverse). La comparaison
est TEMPS CONSTANT (charte § 3 : le OU cumulatif des 16 différences
octet par octet, AUCUNE court-circuit — un arrêt précoce serait une
fuite).
Contrat :
  pre  : P1 rcx = les clés de tour (176 o) ; P2 rdx = le nonce (12 o) ;
         P3 r8 = le chiffré reçu (N octets) ; P4 r9 = N (0 ≤ N ≤ 2^14) ;
         P5 [rsp+0x28] = l'AAD (A octets) ; P6 [rsp+0x30] = A (0 ≤ A ≤
             2^14) ; P7 [rsp+0x38] = l'étiquette REÇUE (16 o) ;
         P8 [rsp+0x40] = la sortie clair (N o — ÉCRITE SEULEMENT SI
             l'étiquette est CONFORME) ; la pile alignée 16.
  post : Q1 l'étiquette recalculée (la même recette que tls13-18 — H,
             GHASH du chiffré, E(K, J0) ⊕ GHASH) CONFRONTÉE en temps
             constant : si elle DIFFÈRE, rax = -4 NOMMÉ
             (cryptographie divergente — la table du domaine) et la
             sortie clair demeure INTACTE : AUCUN octet restitué,
             fail-closed ;
         Q2 si l'étiquette est CONFORME : la sortie = le clair (le CTR
             du chiffré — la brique d'inversion AES n'existe pas :
             tls13-16 re-chiffre les compteurs) ; rax = 0 ;
         Q3 le chiffré reçu, l'AAD et l'étiquette reçue INTACTS ;
         Q4 la preuve : les vecteurs de tls13-18 en sens inverse
             (CAVP/McGrew–Viega ouverts) ET LA FALSIFICATION INVITÉE
             (chaque octet du chiffré muté → -4, chaque octet de
             l'étiquette muté → -4 — la garde constatée sur pièces, le
             chantier (b) l'exige mutation par mutation).
  inv  : I1 le OU cumulatif : les 16 différences octet par octet
             accumulées en UN seul drapeau (charte § 3 — le branch
             final se prononce sur LE drapeau, jamais sur un octet
             isolé) ;
         I2 l'ordre : H, GHASH, confrontation, PUIS le CTR — la
             restitution est la DERNIÈRE opération du bloc ;
         I3 le temps constant hérité de tls13-16/17 ; AUCUNE entrée
             IAT, AUCUN site syscall (charte § 7) ; aucun état détenu
             (charte § 6) ;
         I4 aucun registre non volatil détruit ; NOP, 0x90 (charte § 8).
