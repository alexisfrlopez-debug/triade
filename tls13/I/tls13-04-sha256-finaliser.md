tls13-04 · SHA-256 : la finalisation et l'extraction · révision 1
Intention : clore le hachage — le bourrage FIPS (0x80, les zéros, la
longueur en BITS sur 64 octets gros-boutiste), les dernières compressions,
l'extraction des 32 octets du condensé en GROS-BOUTISTE. Le contrat ah-07
(M6) : le contexte finalisé n'est pas réutilisable sans réinitialisation —
la spec le nomme au lieu de le cacher.
Contrat :
  pre  : P1 rcx = le pointeur du contexte (initialisé, ayant absorbé) ;
         P2 rdx = le pointeur de sortie (32 o accessibles en écriture) ;
         P3 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 le bourrage posé DANS LE TAMPON du contexte : 0x80 puis des
             zéros jusqu'à ce que remplissage ∈ {56, 0}, puis la longueur
             totale en BITS (total × 8) en u64 GROS-BOUTISTE — le cas
             remplissage ≥ 56 AVANT le bourrage déclenche LA COMPRESSION
             DU BLOC PARTIEL D'ABORD (le second bloc du bourrage : la
             borne est nommée, jamais franchie en silence) ;
         Q2 les compressions finales jouées (le tampon vidé), H[0..7]
             sérialisés : rdx[0..31] = le condensé SHA-256 gros-boutiste
             (FIPS § 6.2.3 : la sérialisation EST le résultat) ;
         Q3 rax = 0 ; le contexte demeure LISIBLE mais son état est celui
             d'un hachage CLOS — la réutilisation exige tls13-01 (le
             contrat le nomme : un appel absorbé après finalisation est un
             comportement non défini REFUSÉ par le harnais, jamais
             toléré en silence) ;
         Q4 aucune écriture hors de rdx[0..31] et du contexte pointé.
  inv  : I1 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
         I2 le bourrage et la longueur ne dépendent QUE du total public —
             le temps est constant PAR CONSTRUCTION sur le contenu déjà
             absorbé (les secrets transitent par H, jamais par une
             branche) ;
         I3 aucun état détenu hors du contexte ; les transitoires sur la
             pile (charte § 6) ;
         I4 aucun registre non volatil détruit ; la croissance du slot est
             NOP, 0x90 ;
         I5 la preuve au chantier (b) : les vecteurs FIPS 180-4 § 6.3.1
             (le message d'un octet « a », « abc », les deux messages
             longs) — le condensé octet pour octet, la falsification
             (chaque bit du vecteur muté) ATTRAPÉE par la divergence.
