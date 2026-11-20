# JOURNAL D'OPTIMISATION — le format OPT-NN (R11)

> L'instrument exigé par R11 : toute optimisation exige un hot path identifié
> PAR MESURE, une mesure avant/après consignée et un contrat stable (R4) ;
> l'optimisation prématurée est interdite — sa demande refusée et consignée
> (D-… la règle, § 259 des décisions : « format OPT-NN, versionné avec la
> couche I »). Chaque entrée porte : le hot path MESURÉ (la pièce citée),
> les mesures avant/après (les conditions nommées), le contrat tenu, et le
> sort de la demande. Le journal naît avec OPT-01 — le paquet 6/6 de la
> vague 3 (D205).

---

## OPT-01 — LA VARIANTE SHA-NI DE LA COMPRESSION SHA-256 (le paquet 6/6 de la vague 3, l'instruction lfh49a1xf, D205 — 12/11/2026)

**Le hot path, MESURÉ AVANT TOUT (R11 à la lettre).** Le hachage de fichiers
volumineux instrumenté DANS LE HARNAIS LOUPE (mesure_hotpath_shani.py) :
**tls13-02 — la compression d'un bloc de 64 o — = 98,11 % des instructions
exécutées** (64 Kio : 4 489 500/4 575 760 ; 256 Kio : 17 944 860/18 289 327
— le profil STABLE aux deux tailles, chaque condensé VÉRIFIÉ à hashlib
avant le verdict). La pièce consignée AVANT le premier octet de la variante :
`scripts/preuves_v150/hotpath_shani/mesure_hotpath.txt` (sha256
3f8678b3cd86f34b…) + `comptage_instructions.csv` (eb3038c04972ece7…) —
l'ORDRE constaté sur les heures des fichiers par le vérificateur (V6.a).
L'initialisation et la finalisation sont O(1) (12 et 144 instructions), le
corps de loupe-05 et les shims ne vivent qu'aux fenêtres : le hot path est
la compression, NI un autre périmètre NI un découpage partiel.

**La demande.** L'instruction lfh49a1xf : une variante de profil sha256
utilisant les instructions SHA-NI, sélectionnée par dispatch CPUID avec
repli scalaire sur les blocs scellés existants, contrat I inchangé (R4),
adresses scellées intactes (R7), notation round-trip vérifiée — le kit de
mesure terrain avant/après dans des conditions identiques, AUCUN scellement.
La demande N'EST PAS refusée : le hot path est mesuré, l'optimisation est
FONDÉE.

**Les sémantiques, épinglées par le code AVANT la notation** (le juge est
le code, jamais la documentation lue sur parole) : l'épreuve
`experience_semantique_shani.py` trancha les hypothèses sur le CPU SHA-NI
natif du laboratoire — sha256rnds2 : l'opérande implicite vit dans XMM0
[63:0] (les sommes W+K), dst = (C,D,G,H) reçoit le nouvel (A,B,E,F), src
demeure ; sha256msg1 : dst += σ0([dst1, dst2, dst3, src0]) ; sha256msg2 :
dst += σ1 CHAÎNÉ ([src2, src3, dst0', dst1'] — les éléments 2-3 lisent les
éléments 0-1 DÉJÀ CALCULÉS). La structure ENTIÈRE éprouvée à la main
(`epreuve_compression_shani.py`) : 100/100 blocs contre le juge Python pur,
les QUATRE vecteurs FIPS 180-4 § 6.3.1 verts, le corpus aux bords vert —
AVANT la notation (le miroir de la contre-preuve AES tls13-15/16).

**Le contrat, tenu (R4/R7).** shani-02 porte EXACTEMENT le contrat de
tls13-02, shani-03 EXACTEMENT celui de tls13-03 (mêmes signatures, mêmes
pré/post, la disposition du contexte 112 o inchangée) ; le repli APPELLE
tls13-02 À SON ADRESSE SCELLÉE 0xC080 (les octets extraits de loupe.exe,
byte-identiques aux notations — le double constat V1.f) ; la table K
@0x2F00 est CELLE DU SCELLÉ, lue par seize mouvements alignés, JAMAIS
re-déclarée ; la sonde shani-01 (CPUID feuille 7 EBX bit 29 SHA ∧ feuille 1
ECX bit 9 SSSE3) est rappelée UNE FOIS PAR APPEL d'absorption (le sondage
par bloc eût mangé le gain). L'ARRÊT des slots sur les longueurs réelles
(D161) : 0xD000/0x40 (42 o), 0xD080/0x380 (856 o), 0xD400/0xC0 (159 o) —
la marge .text2 vierge du scellé, AUCUN octet du scellé touché.

**Les mesures avant/après (le laboratoire, 12/11 — la pièce
`preuves_v150/shani/mesures_avant_apres.csv`, sha256 4ca633c417e67049…).**
La MÊME machine (le CPU SHA-NI du labo), la MÊME entrée (8 Mio de PRNG
déterministe, graine 20261112), le condensé VÉRIFIÉ à hashlib AVANT
comptage ET à CHAQUE répétition (une répétition fausse ABORTE), les
opérations COMPLÈTES init+absorb+final, 15 répétitions par bras, les
médianes et IQR en cycles RDTSC (lfence+rdtsc) :

| Bras | Médiane | cycles/octet | IQR |
|---|---|---|---|
| AVANT — la composition scellée tls13-01/03/04 | 115 858 402 | 13,811 | 115 106 742..116 246 490 |
| APRÈS — la variante, dispatch réel SHA-NI | 19 848 520 | 2,366 | 19 746 148..19 948 298 |
| la variante à repli FORCÉ scalaire | 115 058 992 | 13,716 | 114 634 654..115 734 636 |

**LE GAIN : 5,84×** (13,811 → 2,366 cycles/octet) ; **la surcharge du
dispatch : ±1 %** (le repli forcé == la composition scellée au bruit de
mesure près — deux courses du vérificateur donnèrent +0,15 % et −0,69 % :
le prix de la sonde et de la branche est SOUS le seuil de bruit). La
contre-mesure de référence : le gain mesuré par le kit lui-même au
dry-run du laboratoire (temoin_dryrun_kit.txt) : 6,52× sur la même machine
à charge différente — l'ordre de grandeur est STABLE.

**La vérification (verifier_shani_v150.py, la pièce
`preuves_v150/shani/rapport_verification.txt`, 18 contrôles VERTS).**
V1 la notation (round-trip 100 % — 345 instructions ré-assemblées de leur
transcription capstone ; le temps constant STRUCTUREL : shani-02 ZÉRO saut,
tout accès mémoire à déplacement fixe, les 64 tours s'exécutent toujours ;
les sauts de shani-03 sur registres PUBLICS uniquement — la longueur, le
complément, le verdict CPU ; la concordance au plan — les 20 déplacements
RIP == le masque et les 16 groupes K ; l'héritage byte-identique) ; V2
l'émulation (la sonde NATURELLE rend 0 sous qemu64 — le repli vécu sans
intervention ; les vecteurs FIPS, le corpus et l'invariance au chemin
scalaire ; LE ROUTAGE NOMMÉ aux deux sens : le compteur prouve que le
verdict 0 exécute LE SCELLÉ, le verdict 1 forcé meurt DANS LE SLOT de la
variante) ; V3 le natif (la sonde réelle rax = 1 recroisée aux drapeaux
/proc/cpuinfo ; les QUATRE vecteurs dorés aux TROIS compositions ; l'égalité
scalaire/SHA-NI sur 1 000 tampons aux bords 0..65 537 ; l'invariance de
découpage au chemin SHA-NI) ; V4 la mesure (ci-dessus) ; V5 les scellés
INTACTS (les quatre pièces, sha256 identiques avant/après ; le garde
sceau-I 14/14) ; V6 l'ORDRE de R11 (la mesure consignée avant la notation,
constaté sur les heures des fichiers).

**Le kit terrain (la mesure du développeur — `shani/terrain/`).**
L'image `image-shani.bin` (48 Kio, sha256 df851b7c0041d700… — la plage RVA
0x2000-0xE000 : la K du scellé, le masque, la famille sha SCELLÉE extraite
de loupe.exe à ses RVA d'origine, la variante assemblée) + le scénario
`scenario-shani.py` (bifteau : msx64 direct sous Windows, trampoline sous
POSIX — les gabarits pré-assemblés par keystone au labo, AUCUN outil exigé
du terrain) + le LISEZMOI et le manifeste. La discipline à la lettre de
l'instruction : la même machine, la même entrée, le condensé vérifié avant
comptage, les opérations complètes init+absorb+final — jamais un périmètre
partiel. Le dry-run du labo (l'instrument prouvé, PAS la mesure terrain) :
temoin_dryrun_kit.txt, les vecteurs verts, 6,52× à cette charge.

**Le sort.** L'OPTIMISATION EST CONSACRÉE au laboratoire — fondée sur un
hot path mesuré (98,11 %), un contrat stable (R4/R7), des mesures
avant/après consignées (5,84×, surcharge sous le bruit). Elle N'EST PAS
EMBARQUÉE : aucun scellement, aucune carte, aucune cérémonie — la variante
vit en copies de laboratoire aux adresses du plan ; l'embarquement dans un
futur build loupe exigera la cérémonie d'ère du développeur (le sceau-I,
la clé hors-ligne) et le témoin de SON run terrain (temoin-shani.txt).

---

---

## OPT-06 — LA VAGUE 9, LE BILAN DES TROIS LEVIERS DU CERTIFICAT, DU DOUBLE MOTEUR ET DE L'OUVERTURE (l'instruction bkobf06nu, D225 — 20/11/2026)

**Le hot path, MESURÉ AVANT TOUT.** La session complète de vérification :
18/18 round-trip + l'oracle loupe-13 64/64 vecteurs = 0,31 s (le harnais,
cette machine) — le chemin chaud : LA RE-VÉRIFICATION des blocs INCHANGÉS
à chaque geste (la cristallisation 12 rebuilds, les oracles re-joués).

**Les leviers.** (a) LE CERTIFICAT DE CRISTALLISATION : le graphe de
dépendances lu des notations (les arêtes d'appel — jamais déclaré à la
main) ; le diff d'UN bloc (loupe-08) re-vérifie 3 blocs (lui + loupe-09/10
ses dépendants transitifs) en 0,05 s contre 0,31 s la complète — les 15
inchangés portent leur certificat chaîné-signé (Ed25519, clé de test
publique — le modèle D214) ; les TROIS falsifications REFUSÉES nommément
(CERTIFICAT-DIVERGENT — le rejeu complet forcé). (b) LE DOUBLE MOTEUR À
L'OUVERTURE : le volume sous le vrai qemu-x86_64 (le témoin 196 609 o au
fichier entier) — 0,03 s contre 20,0 s à l'échantillon Unicorn,
DIVERGENCE=0 ; le compteur par bloc au hook du harnais (l'écart nommé :
le qemu de Debian SANS CONFIG_PLUGIN). (c) LE RÉGIME ORACLE NATIF :
PRÉPARÉ (le runner, les scénarios, la signature, la confrontation
fail-closed) — son exécution au CI, jamais confondu avec le terrain.

**La mesure M4 (la liste fixe, n=5, l'horloge monotone).** AVANT 39,2 s
[39,2–39,7] · FROID 6,9 s · CHAUD 7,0 s (le run à 29,6 s : l'AUDIT 1/10
VÉCU) · le bras C 2,0 s — LE RATIO DE RÉGIME 3,5× (le seuil ×10 tenu).

**Le sort.** CONSACRÉ AU LABORATOIRE (le certificat et le double moteur) ;
le natif au geste du maître (l'armement du runner CI).

---

## OPT-07 — LES DEUX COULOIRS DE PERFORMANCE : LA PARITÉ SSE2 ET LES CHEMINS ISA (l'instruction 0205wxg5q, D226 — 20/11/2026)

**Le constat d'abord (R11).** Le gcc -O2 des blocs contrôlés n'emploie PAS
SSE2 (le décompte SIMD des .text : 0) — la parité se joue au GPR : loupe-13
le scellé 1,07× gcc-O2 (la bibliothèque tenue ÉGALE : les deux bras au
memcmp SCELLÉ, le call du bras C repointé).

**La variante SSE2 baseline (loupe-13-sse2 à la marge 0xCC00).** Le scan
16 octets à la fois (movdqu + pcmpeqb + pmovmskb — le baseline du x86-64,
AUCUNE extension au-delà, AUCUN dispatch : la garantie constructeur), le
premier octet diffusé sans pshufb (SSSE3 hors baseline), chaque candidat
confirmé au memcmp scellé : round-trip 100 %, zéro divergence aux 24
vecteurs, **3 928 instructions/op contre 115 292 gcc-O2 — le ratio 0,03×,
l'objectif « ≤ gcc-O2 » tenu avec 31,2× de marge**.

**Le couloir B.** AES-NI : LA DESCENTE EST DÉJÀ LE SCELLÉ (l'ère l'exige,
I3 de tls13-15 — 26 instructions/bloc) ; la variante à dispatch MESURÉE
PLUS LENTE (45 contre 26 : le prix du sondage par bloc — la leçon) ;
GHASH PCLMULQDQ : la frontière nommée I5, le chantier suivant ; x25519 :
la pertinence tranchée par la mesure (O(1)/session).

**Le sort.** La variante SSE2 CONSACRÉE AU LABORATOIRE (copie de
laboratoire à la marge — l'embarquement exigera la cérémonie d'ère).

---

## OPT-08 — LE COÛT EN TOKENS AU-DELÀ D'OPT-05 : LE COMPILATEUR D'ORACLE, LA BIBLIOTHÈQUE, LES RATIOS AU PLANCHER (l'instruction uagz3fby7, D227 — 20/11/2026)

**La campagne (quatre cellules n=18, la graine 20261117, le tokenizer
natif lu du champ usage).** éditer-H2 REPRODUIT (18/18, 2 452/40) ;
ajouter-H3 REFUSÉ POUR LA TROISIÈME FOIS (0/18 HORS-FORMAT — le format
d'ajout demeure la notation complète) ; composer-G (la cellule nouvelle :
l'index des scellés au prompt) : 3/18, 4 846 contre 5 079 — H4 FALSIFIÉE
(l'héritage déclaré n'achète pas la réponse : le domaine composait déjà
par appels) ; localiser-P REPRODUIT (18/18, 1 103/52 — le pointeur seul
tenu).

**Le compilateur d'oracle.** Le gabarit structuré des specs I → le code
généré PAR SCRIPT, zéro token LLM : **968 tokens supprimés aux 3 unités
(323/unité)** — la mesure : la longueur cl100k du code généré (ce que
l'agent n'émet plus).

**Les ratios au plancher (la méthode nommée).** éditer-H2 136,2× (le
matériau relu domine) ; localiser-P 38,0× ; ajouter-H3 4,1× ; composer-G
2,9× — la convention de périmètre : les trois champs consignés séparément.

**Le sort.** Le compilateur CONSACRÉ ; l'ajout par hunks REFUSÉ
DÉFINITIVEMENT en l'état (trois falsifications consignées).

---

## OPT-09 — LA VAGUE 9 EN UN LIGNE : LA SÉCURITÉ AU PLANCHER SANS CÉDER UN POINT (D224-D228 — 20/11/2026)

La fonction objectif lexicographique tenue : la SÉCURITÉ gagnée (2 006/2 098
déchargés, 811/817 ajusté, CF3 mécanisé 14/14, la non-interférence aux dix
familles, l'ancrage de transparence) SANS céder la performance (M4 3,5×
tenu), l'optimisation (OPT-06/07/08 consacrés) ni les tokens (le pointeur
seul reproduit 1 103/52) — le tableau de bord des quatre axes le porte.

## OPT-10 — La fenêtre de relecture de l'édition (mqf258e4l, la vague 10 ; le plan gelé sha256 7e7e5571… AVANT toute mesure)

**Le levier (le hot path mesuré)** : l'opération ÉDITER relit ~2 400 tokens de notation complète sur un total médian de 2 452 (le matériau domine, la réponse ne porte que 40 — le constat d'OPT-05).

**Le geste** : ne relire que la FENÊTRE du hunk (±12 lignes autour de la cible, verbatim — les ancres demeurent des lignes exactes), la consigne, et L'EMPREINTE sha256 de la notation complète (la garde : le client recoupe l'empreinte du cache avant l'application — CONTEXTE-DIVERGENT sinon) ; le reste en cache de session.

**La mesure (n=18, la graine 20261117, le tokenizer natif lu du champ usage, cl100k en parallèle, la re-tokenisation indépendante à ±1 — écart max 0)** : le total médian 2 452 → 1 146 (−53,3 %) ; le matériau relu 1 684 → 239 cl100k (×7,0) ; la réponse 40 inchangée ; le ratio au plancher (la paire de lignes du diff réel, 18 cl100k) : 136,2× → 63,6× natif ; la prose de prescription DOMINE désormais (866 > 239) : le prochain levier nommé — la grammaire du format, pas la notation.

**Les contrôles** : 18/18 verts au round-trip exact (garde+application+confrontation) ; le REFUS CONTEXTE-DIVERGENT vécu à la cellule AVANT (le modèle a varié, le client a refusé : fail-closed, jamais re-tirée) ; les QUATRE refus du pointeur re-roulés 5/5 VERT ; AUCUN scellé touché.

**Falsifiée** : H-F1 en son ordre de grandeur (le total ne descend pas d'un ordre de grandeur — la prose demeure) ; la mesure tranche, l'écart nommé.
