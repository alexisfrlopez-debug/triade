av-01 · initialisation du contexte SHA-512 · révision 1
Intention : mettre un contexte SHA-512 à l'état initial FIPS 180-4 § 5.3.5
(les huit mots H0 u64 dérivés des racines carrées des huit premiers nombres
premiers) — le bloc d'entrée de la famille de hachage sceau : tout calcul
commence ici. Miroir exact de ah-04:R1 en mots 64 bits ; le contexte est la
structure partagée av-01→04 (m7/I/README) : H[8] @ +0, tampon[128] @ +64,
remplissage @ +192, total @ +200.
Contrat :
  pre  : P1 rdi pointe vers un contexte de 256 octets inscriptible
             (alignement 8 exigé — H et total sont des mots machine) ;
         P2 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 les huit mots H[i] contiennent exactement les constantes
             initiales du FIPS (6a09e667f3bcc908, bb67ae8584caa73b,
             3c6ef372fe94f82b, a54ff53a5f1d36f1, 510e527fade682d1,
             9b05688c2b3e6c1f, 1f83d9abfb41bd6b, 5be0cd19137e2179 —
             ordre natif) ;
         Q2 remplissage = 0, total = 0 (contexte prêt à absorber) ;
         Q3 rax = rdi (le contexte se rend en retour — chaînage libre).
  inv  : I1 pureté : aucune lecture du contexte au-delà de l'écriture
             (le bloc écrase, il ne consulte pas) ; aucune donnée externe
             (les constantes vivent dans les octets du bloc — immédiats) ;
         I2 feuille : 0 octet de pile, aucun non-volatil, aucun stockage
             sous rsp ;
         I3 les octets 64..191 (tampon) ne sont PAS initialisés — la
             validité du tampon est gouvernée par remplissage (Q2), le
             contenu au-delà est indéterminé par contrat.
Échecs :
  E1 : aucun (le bloc ne peut échouer : huit écritures et un retour).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : après initialisation, la
       séquence finaliser immédiate sur contexte vierge produit le
       digest du message vide cf83e1357eefb8bd…e7d3 (vecteur doré FIPS
       180-4 SHA-512 n° 1, couvre Q1/Q2 ensemble — toute constante H0
       fausse le brise).
Fixtures    : néant (le contexte est l'état propre de la famille).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Les constantes H0 en immédiats plutôt qu'en .rodata :
              huit mov qword [rdi+N], imm64 — pas de déplacement RIP, pas
              de dépendance de données : le bloc est autoporteur (critère
              de réutilisation, R7). Transposition directe du savoir-faire
              ah-04 (échalonnage 1 de l'échelle : la notation SHA-256
              devient la matrice de SHA-512).
