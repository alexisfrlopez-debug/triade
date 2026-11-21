# PLAN GELÉ — 0G3400VQL (la vague 13)
> Le couloir GHASH en PCLMULQDQ, l'AES-GCM complet face à OpenSSL EVP, la propriété
> temps-constant structurelle des nouveaux corridors.
> Gelé AVANT toute mesure, cible pré-enregistrée falsifiable.

## Le mandat
Le GHASH demeure le hotspot GCM non descendu (I5 de la spec : chantier futur NOMMÉ,
mesuré, pas supposé). Trois gestes :

1. **Le couloir GHASH en PCLMULQDQ** : la multiplication GF(2^128) par CLMUL —
   réduction Karatsuba (3× pclmulqdq pour 128×128) et schoolbook (4×) NOTÉES TOUTES
   DEUX, LA MESURE TRANCHE ; le domaine gros-boutiste par bswap aux deux entrées et
   la sortie (le miroir exact du scellé tls13-17) ; contrat tls13-17:R1 TENU (R4) :
   rcx=Z sortie, rdx=X, r8=Y, chevauchement permis, X/Y intacts, commutatif, rax=0 ;
   repli au scellé GPR 0xDFC0 JAMAIS un chemin mort. Cible pré-enregistrée :
   **≤ 80 cycles/multiplication au rig virtualisé** (sinon l'écart nommé par mesure).
   Si keystone n'assemble pas pclmulqdq, les octets explicites (le précédent SHA-NI).

2. **Le dispatch CPUID hissé UNE fois par session pour TOUS les corridors** : la sonde
   de session (leaf 1 : AES ECX[25], PCLMUL ECX[1] ; leaf 7 : SHA-NI EBX[29] ;
   OSXSAVE→XGETBV) résolue AU CHARGEMENT, verdict porté sous r10 à l'appelant (la
   convention x705m50vl) ; les corridors AVX2 (loupe-13), SHA-NI (tls13-02) et GHASH
   ne sondent PLUS par appel — le comptage cpuid/session == 1 exigé.

3. **L'AES-GCM COMPLET et le SHA-256 complet face à OpenSSL EVP** : la composition de
   laboratoire (porteur tls13-16-ni-v4-inline + couloir GHASH + enveloppe miroir de
   tls13-18 : J0/CTR/H/étiquette, bornes nommées) et la composition SHA-256 (scellés
   01/03/04 + corps SHA-NI du couloir) contre EVP_aes_256_gcm ET EVP_aes_128_gcm
   (l'asymétrie nommée : la lignée scellée est AES-128, l'instruction nomme AES-256 —
   les DEUX publiés) et EVP_sha256 (SHA-NI activé par OpenSSL sur cette unité), même
   machine, RDTSCP cœur 1 épinglé, n≥20, médiane non arrondie + IQR + cycles bruts,
   fréquence et empreinte CPU consignées (la convention fnvan0zes/x705m50vl).
   AUCUNE cible sur les ratios OpenSSL : la référence externe publiée, jamais une
   promesse.

## Les gestes
1. Ce plan gelé AVANT toute mesure.
2. Atelier atelier-ghash-0g3400vql/ : notations ghash-pclmulqdq-karatsuba.asm et
   -schoolbook.asm à la marge vierge (0xD200/0xD400 vérifiées libres par code, le
   chevauchement des marges des vagues précédentes vérifié), la sonde-session à la
   marge, l'enveloppe GCM de laboratoire à la marge ; les scellés assemblés à leur
   slot canonique puis posés en copies (la convention 8z4hj76w4).
3. Les mesures : Unicorn pour les comptes et la différentielle ; le rig natif C
   (RDTSCP, sched_setaffinity cœur 1, n=20, tri par insertion, IQR publié) pour les
   cycles — LE BAC EST VIRTUALISÉ : les cycles publiés sont LES CYCLES DE CETTE
   MACHINE, le silicium nu au geste du développeur (nommé, jamais maquillé).
4. La parité : vecteurs McGrew–Viega TC1..TC4 (le harnais aead), transfert RFC 8448,
   cas punitifs GHASH (X=0, Y=0, X=Y=R, commutativité), différentielle 64/64 et
   256/256 octet pour octet contre le scellé tls13-17 appelé par bloc, contrôle
   négatif (un octet du corps muté) ATTRAPÉ au premier vecteur.

## La vérification après modifications
- temps constant STRUCTUREL : taint branche/adresse sur les secrets du couloir
  (l'interpréteur abstrait, les conventions de l'audit) ; hash de traces complètes à
  N=60/classe (les valeurs jamais hachées, une empreinte par cible sur 120 mesures,
  graines consignées) ; LA CONVENTION NEUVE : aucune instruction à latence variable
  (div/idiv, et les lectures non-temporelles) sur donnée secrète — la liste noire
  nommée, le vérificateur par code ;
- la différentielle contre le scellé à zéro divergence ; les scellés 14/14 et les
  quatre pièces aux ancres R7 AVANT et APRÈS chaque partie ;
- le comptage cpuid par session == 1 vérifié par code (le hoisting exigé) ;
- le round-trip 100 % à chaque notation ; OPT-17 au journal AVANT tout commit des
  blocs optimisés.

## Les refus
Aucun scellé modifié ; la marge vierge seule écrite ; les cycles virtualisés nommés
virtualisés ; l'écart à la cible publié par mesure, jamais ajusté ; OpenSSL la
référence publiée, jamais le juge du scellé.
