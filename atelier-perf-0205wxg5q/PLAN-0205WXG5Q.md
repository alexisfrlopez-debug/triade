# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 9, L'INSTRUCTION 0205wxg5q : LA PERFORMANCE À DEUX COULOIRS (la parité baseline SSE2, les chemins chauds descendus à l'ISA)

> Pré-enregistré AVANT toute mesure (R11 à la lettre : hot path identifié
> PAR MESURE, avant/après consigné, contrat stable R4, adresses scellées
> R7 — la règle D205/OPT-01 reconduite). Aucun chiffre attendu écrit
> avant mesure. Aucun artefact scellé touché : les variantes vivent en
> copies de laboratoire aux adresses du plan (le modèle OPT-01).

## 1. LES HYPOTHÈSES (falsifiables, pré-enregistrées)

H1 — LE COULOIR A (la parité baseline) : les SIX BLOCS CONTRÔLÉS de la
campagne D210 (loupe-01, loupe-02, loupe-05, loupe-08, loupe-13,
loupe-16 — les unités instrumentées aux deux bras) contiennent des
BOUCLES où la référence compilée (gcc -O2, le bras C, la chaîne mingw
TRIXIE aux versions exactes : gcc 14.2.0, binutils 2.44, mingw-w64
12.0.0) emploie des mouvements SSE2 du baseline x86-64 (movdqa/movdqu/
movq/paddb…) que la notation GPR pure n'emploie pas. L'HYPOTHÈSE : les
chemins SSE2 baseline écrits en notation (recherche d'octet : loupe-13 ;
composition de ligne : loupe-08 ; saisie : loupe-16 ; et les trois
autres là où la mesure le nomme) rapprochent le coût instructions/op
du gcc-O2 — OBJECTIF : coût inférieur ou égal à gcc-O2 sur les six
blocs à travail égal, SANS AUCUNE extension au-delà du baseline SSE2
(le CPUID du repli : SSE2 est le baseline x86-64, AUCUN dispatch requis
— la garantie constructeur, nommée telle quelle).

H2 — LE COULOIR B (les chemins chauds de production) : les hot paths
MESURÉS du projet — sha-256 (tls13-02 : 98,11 % des instructions au
hachage — OPT-01 CONSACRÉ, 5,84×) ; aes-gcm (le chemin critique crypto
de la session M4 : ~10 s/196 Kio avant mémo — le GHASH et les tours
AES) ; x25519 (O(1) par session — l'ordre de grandeur NOMMÉ par la
mesure, la pertinence tranchée par elle) ; les transformations de rendu
(loupe-08/10 au volume du million fuzzé). L'HYPOTHÈSE : le chemin
aes-gcm descendu à l'ISA (AES-NI : aesenc/aesenclast/aeskeygenassist ;
PCLMULQDQ : le GHASH) achète un ordre de grandeur au volume — attente
directionnelle ≥ 4× sur le chemin AES-GCM complet à entrée égale
(l'ordre de grandeur de la littérature, jamais un chiffre attendu : la
mesure tranche). LE DISPATCH CPUID (feuille 1 ECX bit 25 AES ∧ bit 1
PCLMUL ; feuille 7 EBX bit 29 SHA — la sonde shani-01 reconduite) avec
REPLI BASELINE OBLIGATOIRE (le scellé À SON ADRESSE, le modèle OPT-01).

H3 — LA DETTE DE CÉRÉMONIE : si une spécification de couche I est
révisée par le présent chantier (un nouveau bloc = une NOUVELLE
spécification, pas une révision ; une révision de contrat = la
cérémonie), la dette est NOMMÉE À LA NAISSANCE — AUCUN build avant la
cérémonie. Les nouveaux blocs du présent chantier naissent
ÉCRITS-AVANT-CODE (le gabarit § 2 de la spec : intention, contrat,
cas d'échec, vecteurs) — le modèle shani/I de l'OPT-01.

## 2. LE COULOIR A — LE PROTOCOLE (H1)

LA MESURE AVANT : les SIX blocs au GPR pur (les notations scellées
TELLES QUELLES — lecture seule) exécutés au harnais Unicorn (le même
moteur que la campagne, le compteur d'instructions par opération, n=15
répétitions, la médiane et l'IQR) ; la RÉFÉRENCE : le bras C des SIX
blocs (les sources C de la campagne D210, la chaîne mingw EXACTE,
-O2, AUCUN drapeau supplémentaire) exécuté au MÊME harnais au même
travail (les mêmes vecteurs dorés). LE COMPTE : instructions/op par
bloc, la taille du code, le comportement aux vecteurs (l'identité des
observables exigée — zéro divergence comportementale).
L'ÉCRITURE : les chemins SSE2 baseline en notation (keystone, le
round-trip capstone 100 %, le temps constant STRUCTUREL : zéro saut
nouveau dépendant des données, les accès à déplacement fixe) ; la
CONFRONTATION : le comportement aux MÊMES vecteurs (zéro divergence),
le coût re-mesuré APRÈS (le même protocole). LE VERDICT PAR BLOC :
coût(après) ≤ coût(gcc-O2) ? — VERT/ROUGE par bloc, les six rapportés
SÉPARÉMENT (aucune moyenne fondue : la convention de parité préservée).

## 3. LE COULOIR B — LE PROTOCOLE (H2)

LA MESURE AVANT : le profil du chemin aes-gcm (les blocs tls13 du
domaine, le hachage du témoin 196 609 o — le protocole D214) : le
compteur par bloc, les instructions/op, le temps émulé ; x25519 et le
rendu : le même profil, la pertinence NOMMÉE par la mesure. L'ÉCRITURE
(là où la mesure fonde) : aes-gcm-NI (les tours AES-NI + le GHASH
PCLMULQDQ, la contre-mesure de l'ordre des tours, le contrat de
tls13-AEAD À LA LETTRE — R4), le dispatch + le repli au SCELLÉ (R7,
l'appel À SON ADRESSE). LA CONFRONTATION : les vecteurs dorés NIST
GCM (les vecteurs de validation), l'égalité scalaire/NI sur 1 000
tampons aux bords, l'invariance de découpage, le round-trip 100 %, le
temps constant STRUCTUREL (zéro saut sur données secrètes, tout accès
à déplacement fixe — la sonde audit_temps_constant reconduite), LE
REPLI exercé sur une machine SANS l'extension (l'émulation qemu64 —
la sonde naturelle rend 0 : le repli vécu, le modèle OPT-01 V2).
LA MESURE APRÈS : le même protocole, la même entrée, n=15, les
médianes et IQR. LE VERDICT : le rapport avant/après par chemin, les
chemins rapportés SÉPARÉMENT (le couloir B est la mesure de
production, JAMAIS fondue avec la parité du couloir A).

## 4. LES RÈGLES DE VERDICT PRÉ-ENREGISTRÉES (fail-closed)

  - ZÉRO divergence comportementale aux vecteurs dorés et aux oracles
    différentiels, sur les DEUX chemins (extension et repli) ;
  - round-trip 100 % sur tous les nouveaux blocs ; cristallisation
    10/10 (dix rebuilds byte-identiques) ; empreintes des artefacts
    scellés antérieurs INTACTES ;
  - la batterie de mutation REJOUÉE sur les nouveaux blocs aux mêmes
    graines : AUCUN tueur affaibli, les survivants NOMMÉS ;
  - le temps constant re-vérifié sur chaque nouveau chemin (le hash
    de trace complet, une empreinte par cible) ;
  - le repli baseline EXERCÉ sur une machine sans l'extension :
    verdict IDENTIQUE, refus nommé si l'environnement est non conforme ;
  - le rapport de mesure avant/après avec conditions identiques,
    horloge monotone (RDTSC lfence au natif, compteur d'instructions à
    l'émulation), n consigné ;
  - la dette de cérémonie nommée à la naissance si une spécification
    I est révisée — AUCUN build avant la cérémonie.

## 5. LA CONSIGNATION

OPT-08 (le couloir A : la parité SSE2 ; le couloir B : l'ISA aux chemins
mesurés) au journal d'optimisation (format D205) ; la décision
append-only (les deux couloirs, la convention de parité préservée, la
voie de production mesurée) ; les gains avant/après consignés avec les
conditions ; la présente empreinte au journal AVANT la première donnée.
