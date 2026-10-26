ah-04 · initialisation du contexte SHA-256 · révision 1
Intention : mettre un contexte SHA-256 à l'état initial FIPS 180-4 § 5.3.3
(les huit mots H0 dérivés des racines carrées des huit premiers nombres
premiers) — le bloc d'entrée de la famille de hachage : tout calcul
commence ici. Le contexte est la structure partagée ah-04→07 (m6/I/README) :
H[8] @ +0, tampon[64] @ +32, remplissage @ +96, réservé @ +100, total @ +104.
Contrat :
  pre  : P1 rdi pointe vers un contexte de 112 octets inscriptible
             (alignement 8 exigé — H et total sont des mots machine) ;
         P2 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 les huit mots H[i] contiennent exactement les constantes
             initiales du FIPS (6a09e667, bb67ae85, 3c6ef372, a54ff53a,
             510e527f, 9b05688c, 1f83d9ab, 5be0cd19 — ordre natif) ;
         Q2 remplissage = 0, total = 0 (contexte prêt à absorber) ;
         Q3 rax = rdi (le contexte se rend en retour — chaînage libre).
  inv  : I1 pureté : aucune lecture du contexte au-delà de l'écriture
             (le bloc écrase, il ne consulte pas) ; aucune donnée externe
             (les constantes vivent dans les octets du bloc — immédiats) ;
         I2 feuille : 0 octet de pile, aucun non-volatil, aucun stockage
             sous rsp ;
         I3 les octets 32..95 (tampon) ne sont PAS initialisés — la
             validité du tampon est gouvernée par remplissage (Q2), le
             contenu au-delà est indéterminé par contrat.
Échecs :
  E1 : aucun (le bloc ne peut échouer : huit écritures et un retour).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : après initialisation, la
       séquence finaliser immédiate sur contexte vierge produit le
       digest du message vide e3b0c442…b855 (vecteur doré FIPS n° 1,
       couvre Q1/Q2 ensemble — toute constante H0 fausse le brise).
Fixtures    : néant (le contexte est l'état propre de la famille).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Les constantes H0 en immédiats plutôt qu'en .rodata :
              huit mov dword [rdi+N], imm32 — pas de déplacement RIP, pas
              de dépendance de données : le bloc est autoporteur (critère
              de réutilisation, R7).
