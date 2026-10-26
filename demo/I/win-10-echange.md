win-10 · échange réseau vérifié · révision 1
Intention : UNE responsabilité réutilisée trois fois par le scénario — envoyer
la phrase d'échange (13 octets, boucle d'émission complète), recevoir la
réponse (13 octets, boucle de réception cumulative), puis la comparer octet à
octet à l'attendu par le memcmp scellé M1 ; le verdict est binaire et honnête.
Contrat :
  pre  : P1 rcx = socket cliente connectée ; P2 rdx pointe l'attendu ASCII de
         13 octets (.rdata : PHRASE ou PHRASE_MAJ) ; P3 WSA actif, serveur en
         écoute ; P4 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 succès : eax = 1 — la phrase a été intégralement émise, 13 octets
         reçus, reçus == attendu (memcmp scellé) ; Q2 échec (émission ≤ 0,
         réception ≤ 0 ou divergence) : eax = 0, socket laissée ouverte (la
         politique de fermeture appartient à l'appelant, Q4 de win-09) ;
         Q3 tampon de réception dans le cadre de pile, aucun .data touché.
  inv  : I1 appels : memcmp scellé (b20002) en direct, send/recv par IAT
         ws2_32 (mêmes slots que tcp-09) ; I2 la phrase émise est TOUJOURS
         PHRASE (minuscules) — c'est la RÉPONSE qui change avec l'état du
         patch : le bloc ne connaît pas la version active du serveur, il
         constate (le patch est l'affaire de tcp-07, pas de l'échange) ;
         I3 aucune journalisation ici (l'appelant journalise après verdict).
Échecs :
  E1 : émission partielle impossible à compléter (send ≤ 0) — eax = 0.
  E2 : réception fermée ou divergente (recv ≤ 0, memcmp ≠ 0) — eax = 0.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims send/recv — trois appels successifs avec les trois
       attendus (identité, MAJUSCULES, identité) → 1, 1, 1 ; shim recv
       renvoyant une réponse divergente → 0 (couvre Q1-Q3, E1-E2).
Fixtures    : PHRASE/PHRASE_MAJ (.rdata, partagées avec win-09).
Provenance  : écrite-avant-code.
Décisions   : D7, D8 ; factorisation du motif triplicé de win-09 (leçon de
              style : une responsabilité par bloc, trois usages).
