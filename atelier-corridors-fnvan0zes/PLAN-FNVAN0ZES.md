# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION fnvan0zes : LA DIFFÉRENTIELLE DURCIE, LA VARIANTE HYBRIDE, LES COULOIRS AVX2 ET SHA-NI

> Pré-enregistré AVANT toute mesure (l'empreinte sha256 consignée à
> EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT la première donnée).

## 1. LA BATTERIE ÉLARGIE (la différentielle durcie — la v2 SSE2 de 8z4hj76w4)

La confrontation v2 (88 vecteurs) s'étend : (a) OCCURRENCES PLANTÉES EN QUEUE
de tampon — le dernier bloc de 16 octets (positions len-16…len-1, chaque
alignement) ; (b) OCCURRENCES CHEVAUCHANTES (le motif recouvert par lui-même,
périodes 1 à 4) ; (c) LONGUEURS DE MOTIF 1 à >16 octets (1, 2, 3, 15, 16, 17,
18, 33 — les bornes du vecteur et du masque) ; (d) FRANCHISSEMENT DE PAGE
(le tampon à cheval sur deux pages Unicorn, l'occurrence aux deux bords) ;
(e) MULTI-OCCURRENCES (1 à 8 occurrences, la première ET la dernière
rapportées) ; (f) TIRAGES PROPERTY-BASED à positions aléatoires — la graine
20261120 consignée, 512 tirages, juge trivial en Python. ZÉRO divergence
exigée sur TOUTE la batterie ; le contrôle négatif (mutation du premier octet
du motif) ATTRAPÉ à la première divergence.

## 2. LA VARIANTE HYBRIDE (l'idiome memchr + memcmp scellé)

Notation hybride en COPIE DE LABORATOIRE à la marge : la boucle externe à
l'idiome memchr (la recherche du premier octet au mot SIMD), la confirmation
par le memcmp scellé (0x1180) — le même idiome que la classe libc mesurée au
temps réel. Round-trip 100 % ; la batterie élargie complète ; la mesure aux
instructions (Unicorn, la bibliothèque tenue égale) et le TEMPS RÉEL (RDTSCP,
cœur fixé, n≥20, médiane + IQR). LE SCELLÉ INTACT — la marge vierge.

## 3. LES COULOIRS AVX2 (recherche) ET SHA-NI (tls13-02)

- AVX2 (loupe-13, la recherche d'octets) : la variante à registres ymm
  (vmovdqu + vpcmpeqb + vpmovmskb), le dispatch runtime AU CPUID (une fois
  par flot — la leçon du hissage v2), le repli baseline SSE2. Round-trip,
  batterie élargie complète (zéro divergence), mesure instructions + cycles.
- SHA-NI (tls13-02, la compression SHA-256) : la variante sha256rnds2/
  sha256msg1/sha256msg2 à la marge, le dispatch runtime, le repli au scellé
  GPR. Les vecteurs du scellé (les diagnostics FIPS + les vecteurs de la
  convention) à zéro divergence ; mesure instructions + cycles réels.
- LES SCELLÉS INTACTS (14/14 avant et après — la garde du sceau re-vérifiée).

## 4. LES MESURES (le protocole, gelé)

- INSTRUCTIONS : le même émulateur (Unicorn, modèle fixé), LA BIBLIOTHÈQUE
  TENUE ÉGALE, la même série (4096/16, la graine 20261120), n≥15, médiane.
- CYCLES RÉELS : RDTSCP, l'affinité de cœur fixée, la fréquence et
  l'empreinte CPU consignées, n≥20, MÉDIANE + IQR rapportés. La machine du
  bac (UNE SEULE — la limite nommée, jamais simulée).
- LE JOURNAL OPT conforme R11 (le hot path mesuré avant, la mesure
  avant/après consignée AVANT le commit).

## 5. LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

Zéro divergence contre le juge trivial sur toute la batterie élargie ; le
contrôle négatif attrapé à la première divergence ; round-trip 100 % ; les
empreintes des pièces scellées intactes avant/après ; les cellules existantes
re-mesurées non régressées ; journal OPT + décision consignés.
