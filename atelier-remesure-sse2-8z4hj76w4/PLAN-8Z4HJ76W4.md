# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 10, L'INSTRUCTION 8z4hj76w4 : LA RE-MESURE SSE2 AUX BASELINES ÉQUITABLES (le temps réel sur matériel)

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE10.txt, le commit git qui précède toute donnée).
> Aucun chiffre attendu écrit avant mesure. Aucun artefact scellé touché :
> la variante vit en copie de laboratoire aux adresses de marge (le
> modèle OPT-01 reconduit).

## 1. LE CONSTAT DE DÉPART (sur pièces, la vague 9)

La mesure vague 9 du couloir A rapportait la variante SSE2 (recherche
d'octet, loupe-13) à 3 928 instructions/op contre le bras C gcc-O2 à
115 292 instructions/op SOUS ÉMULATION Unicorn (le compteur
d'instructions). L'instruction présent : (a) les baselines ÉQUITABLES —
gcc-O3 VECTORISÉ et la libc memchr/memmem (SIMD) EN PLUS du gcc-O2
scalaire ; (b) LE TEMPS RÉEL sur matériel (RDTSC, affinité de cœur
fixée, fréquence consignée, n≥10) — pas seulement le compteur sous
émulation ; (c) le sondage CPUID AES-NI HISSE hors de la boucle par
bloc (la variante dispatch mesurée 45 instr/bloc contre 26 au scellé).

## 2. LA MÉTHODE (gelée)

 (m1) LES QUATRE CONTENDANTS (à travail égal, les mêmes vecteurs, le
      même ordre, la même graine 20261120) :
      — LA VARIANTE SSE2 DE NOTATION : les octets assemblés de la vague 9
        (RVA 0xCC00, la copie de laboratoire — le scellé intact), exécutés
        SUR MATÉRIEL par page exécutable mmap, appelés par le juge C
        natif (la convention d'appel du bloc, les arguments posés aux
        registres du plan) ;
      — GCC-O2 SCALAIRE : l13.c compilé gcc -O2 natif (la même source que
        le bras C, la chaîne native de la machine de record) ;
      — GCC-O3 VECTORISÉ : l13.c compilé gcc -O3 natif (le maximum du
        compilateur sur la même source — la baseline équitable demandée) ;
      — LA LIBC memchr/memmem : les fonctions SIMD de la libc (memmem
        pour le multi-octets, memchr pour le mono-octet — la voie idiomatique
        du C, le SIMD de la bibliothèque nommé baseline ÉQUITABLE).
 (m2) LE TEMPS RÉEL : RDTSC (rdtscp/rdtsc par asm en ligne, la fréquence
      du TSC consignée de /proc/cpuinfo « MHz » et « Bogomips »), L'AFFINITÉ
      DE CŒUR FIXÉE (taskset/sched_setaffinity au cœur 1, la fréquence au
      gouverneur consigné), n≥10 répétitions par cellule, la MÉDIANE et
      l'IQR ; l'échauffement (warm-up) consigné ; l'horloge monotone en
      parallèle (la recoupe du TSC).
 (m3) LES MACHINES : la consigne « ≥2 machines, témoins signés » — CE BAC
      EST UNE MACHINE : l'écart EST NOMMÉ EN L'ÉTAT (une seule machine de
      record disponible à la session, aucune seconde machine au bac, le
      témoin signé attend le geste du maître) — JAMAIS simulé.
 (m4) LE CPUID HORS BOUCLE (couloir B) : la variante dispatch AES-NI
      reconstruite avec la sonde CPUID (feuille 1 ECX bit 25) HISSEE
      AVANT la boucle par bloc — le verdict porté en registre drapeau
      d'entrée, la boucle du bloc pure — le re-compte d'instructions
      par bloc sous Unicorn (le même rig que la vague 9), la
      confrontation au scellé (26) et au dispatch par-bloc (45).
 (m5) LA CONFRONTATION DE COMPORTEMENT : les 24 vecteurs (les 15 de la
      mesure avant + les 9 bords nommés : n ∈ {0,1,2,33,64,65,255,256,
      1000}, le motif ∈ {1,16,31,32}) — ZÉRO divergence exigée contre
      l'implémentation triviale (le juge Python) pour CHAQUE
      contender ; le round-trip capstone→keystone 100 % pour la
      variante (les octets inchangés) ; le contrôle négatif (la
      variante mutée à la première ligne — un octet d'opcode changé)
      ATTRAPÉ à la première divergence nommée.
 (m6) LES RAPPORTS : les ratios INSTRUCTIONS (Unicorn, la convention de
      parité de la vague 9 — la bibliothèque tenue égale) ET TEMPS RÉEL
      (RDTSC, médiane n≥10, l'IQR, la fréquence consignée) — la baseline
      équitable NOMMÉE pour chaque ratio ; la dette de cérémonie d'ère
      nommée pour tout embarquement (les copies de laboratoire aux
      adresses de marge, l'embarquement exige la cérémonie d'ère — la
      convention OPT-01/I3 reconduite).

## 3. LES HYPOTHÈSES (falsifiables, pré-enregistrées)

 H-A : la variante SSE2 de notation demeure ≤ au coût instruction des
 baselines équitables à travail égal (la convention de parité vague 9
 reconduite aux baselines étendues).
 H-B : au TEMPS RÉEL sur cette machine, la variante SSE2 et la libc
 memmem (SIMD) sont du même ordre de grandeur par octet balayé (les
 deux chemins balayent 16 octets par itération — l'écart attendu est
 l'échelle du facteur de boucle, pas un ordre de grandeur) ; gcc-O2/-O3
 scalaire (la boucle memcmp) du même ordre entre eux. AUCUN chiffre
 attendu écrit : la mesure tranche.
 H-C : le CPUID hissé hors boucle ramène le compte d'instructions/bloc
 du dispatch au voisinage du scellé (26) — l'écart résiduel nommé
 (les instructions de dispatch de tête, payées UNE FOIS par bloc
 plutôt que par itération).

## 4. LA VÉRIFICATION (gelée)

 zéro divergence aux 24 vecteurs + bords pour chaque contender ; le
 round-trip 100 % ; les variantes en copies de laboratoire aux
 adresses de marge, les scellés intacts (la garde du sceau 14/14
 avant/après) ; le contrôle négatif (la variante mutée) ATTRAPÉ à la
 première ligne ; les ratios instructions ET temps réel rapportés, la
 baseline équitable nommée ; la dette de cérémonie d'ère nommée pour
 tout embarquement ; la limite d'UNE SEULE MACHINE nommée en l'état
 (jamais une seconde machine simulée).
