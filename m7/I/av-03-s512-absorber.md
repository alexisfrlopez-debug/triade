av-03 · absorption tamponnée SHA-512 · révision 1
Intention : absorber n octets pointés par rsi dans le contexte, en
découpant par blocs de 128 : remplir le tampon partiel, comprimer quand il
est plein, recommencer — miroir exact de ah-06:R1 en blocs de 128 (le
correctif jbe/jb du journal 20 est hérité : le test d'espace est jb
STRICT — un tampon rempli EXACTEMENT est comprimé avant de vider, jamais
laissé gonfler à 128 en attente).
Contrat :
  pre  : P1 rdi pointe vers le contexte (256 o) initialisé (av-01) ;
         P2 rsi pointe vers les données ; P3 rdx = n (octets, u64 ; la
             lecture ne va JAMAIS au-delà de n) ;
         P4 pile alignée.
  post : Q1 total est incrémenté de n ; remplissage = (remplissage + n)
             mod 128 ; ⌊(remplissage + n)/128⌋ compressions exécutées —
             la spécification FIPS est respectée À l'octet ;
         Q2 le tampon contient les remplissage derniers octets reçus
             (aux positions 0..remplissage−1) ;
         Q3 rax = total (chaînage libre) ; les registres non-volatils
             sont préservés.
  inv  : I1 appels directs : av-02 (compression) exclusivement — déclaré,
             cible vérifiée par l'oracle structurel ;
         I2 aucune donnée RIP, aucun syscall ; aucune lecture du contexte
             au-delà de remplissage/total/tampon ;
         I3 prologue : 5 pushes — pile 16-alignée aux appels de av-02
             (5×8 + 8 de retour ≡ 0 mod 16) ;
         I4 le test d'espace est jb STRICT (n == espace restant →
             remplir, comprimer, vider : le piège du journal 20, spec
             ah-06:R1 E1, ne doit JAMAIS renaître — vecteur V3 le
             surveille par tailles multiples de 128).
Échecs :
  E1 : aucun (absorption bornée ; les tailles nulles retournent
       immédiatement).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle natif) : tailles de transition
       0, 1, 111, 112, 127, 128, 129, 1000, 65535, 65536, 65537, 131072
       — digest octet-identique à sha512sum sur chaque taille (couvre
       Q1 : les frontières de bloc sont la faiblesse historique de ce
       bloc, miroir ah-06).
  V3 : falsification intégrale (chaque octet de code) — zéro silence.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Héritage direct du correctif frontière de hachoir : le
              contrat Q1 est l'énoncé FIPS re-copié mot pour mot (deux
              égalités), pas une paraphrase — la spec av-03 naît du défaut
              de sa soeur aînée, la boucle de rétroaction du protocole
              traverse les milestones.
