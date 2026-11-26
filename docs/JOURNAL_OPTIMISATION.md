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

## OPT-11 — LES COULOIRS SIMD : L'HYBRIDE MEMCHR+MEMCMP, L'AVX2 À DISPATCH, LE SHA-NI AU CORPS NATIF (fnvan0zes, la vague 11 ; le plan gelé sha256 ebbfce71865d2ae8… AVANT toute mesure)

**Le levier (les hot paths mesurés)** : la recherche d'octets scellée GPR loupe-13 — 18 226 cycles/op (4096/16 absents) ; la compression SHA-256 scellée GPR tls13-02 — 53 243 cycles aux 64 blocs (832 cycles/bloc).

**Le geste** : (1) L'HYBRIDE à l'idiome memchr — la boucle externe au mot SIMD (la dernière fenêtre de 16 non-alignée, les bits sous la position courante ÉTEINTS, bsf UNE fois), la confirmation par LE MEMCMP SCELLÉ (0x1180, la bibliothèque tenue égale) ; le tampon < 16 octets au chemin octet-par-octet (l'interdit de sûreté mémoire demeure) ; 314 o à la marge VIERGE 0xCD00. (2) LE COULOIR AVX2 — les registres ymm (vmovdqu + vpcmpeqb + vpmovmskb), LE DISPATCH RUNTIME au sondage complet (OSXSAVE → XGETBV ×CR0 → leaf 7) une fois par appel, LE REPLI BASELINE SSE2 intégré (jamais un chemin mort) ; 494 o à 0xD100. (3) LE COULOIR SHA-NI — sha256rnds2/sha256msg1/sha256msg2 aux octets explicites (keystone ne les assemble pas — l'encodage 0F 38 CB/CC/CD /r + LE REX vérifié par objdump ET le re-dérivage canonique), la référence C d'abord vérifiée 256/256 contre le juge Python AVANT la notation ; 896 o à 0xD300, le repli au scellé GPR.

**La mesure (RDTSCP, cœur 1 fixé, n=20, médiane + IQR, drapeaux CPU consignés avx2+sha_ni+aes)** : l'hybride 704 cycles [IQR 52] — LE GAIN 25,9× sur le scellé GPR, DANS LA CLASSE des primitives SIMD de la libc (l'idiome memchr 561, la vague 10), 1,25× au-dessus de l'idiome ; LE SHA-NI CORPS (le dispatch de 21 o patché en place puis RESTAURÉ, la technique de laboratoire) 8 227 [6] aux 64 blocs = 128,5 cycles/bloc — LE GAIN 6,5× sur le scellé GPR (832/bloc), la forme pleine 2 820/bloc DOMINÉE PAR LE SONDAGE ; LE COMPTE STATIQUE : le corps SHA-NI 181 instructions contre le scellé GPR 122 — 4,3× moins d'instructions aux rnds2/msg1/msg2 natifs.

**La leçon du hissage généralisée** : le sondage cpuid(7) ≈ 2 660 cycles AU BAC VIRTUALISÉ (la sortie d'hyperviseur, mesurée à part) — au matériel nu ≈ 100 cycles ; le dispatch par appel ne se justifie QUE si l'appelant ne peut pas hisser — le TLS comprime des FLOTS : le sondage hissé PAR SESSION (le modèle OPT-01, la cérémonie d'ère) ; l'embarquement exigera le sondage hissé, le couloir porte la note.

**Les contrôles** : LA BATTERIE ÉLARGIE 559 vecteurs (64+3 en queue de tampon — chaque alignement du dernier bloc de 16 ; 4 chevauchants — périodes 1 à 4 ; 13 longueurs de motif — 1 à 33 octets, les bornes du vecteur et du masque ; 3 franchissements de page ; 8 multi-occurrences ; 512 property-based à la graine 20261120) — L'HYBRIDE 559/559 ZÉRO DIVERGENCE (Unicorn et natif), LE REPLI SSE2 DE L'AVX2 559/559 (le dispatch patché de laboratoire — la machine sans AVX2 le vit), LE SHA-NI 256/256 contre le scellé GPR au rig natif (le vecteur lm=33 : le REFUS DE CONTRAT attendu -5, vécu, ADMIS au bord) ; LE CONTRÔLE NÉGATIF de la différentielle vécu (la mutation du premier octet du motif suivie au juge, la mutation de la notation divergente au premier vecteur) ; le round-trip 100 % aux trois notations ; LES SCELLÉS 14/14 avant et après (la marge vierge, la garde du sceau re-vérifiée) ; les cellules existantes re-mesurées NON RÉGRESSÉES (le scellé loupe-13 18 226 [4], le scellé tls13-02 53 243 [164] — la classe tenue).

**Les fautes nommées et corrigées** : le masque non-aligné (pshufb m128 EXIGE align 16 — la faute #GP, la directive posée) ; LE REX OMISSIF (xmm9 lu silencieusement xmm1 sans REX.R/B — le schedule faux SANS signal ; le stade-par-stade contre la référence la nomme) ; le palignr à la mauvaise fenêtre (S[k] au lieu de S[k+2] — le terme W[i-7] faux) ; la page de la table K (0x2F000 écrit pour 0x2F00) ; le clobber cpuid des porteurs (rbx/rcx/rdx/rax — r10/r11 préserverés, le départ relu de la pile, la liste de clobbers de l'appelant msx64 étendue rbx, cc) ; le codegen -O2 du harnais (la séquence pendait à -O2 — le harnais, PAS les notations ; le rig compilé -O1, l'écart consigné).

**Les limites nommées** : UNE SEULE MACHINE au bac (≥2 machines, témoins signés — attendent le geste du maître, jamais simulés) ; le bac virtualisé piège cpuid (la mesure au matériel nu attend le terrain) ; Unicorn sans AVX/SHA-NI (LA BORNE NOMMÉE : les comptes statiques exacts à la place — 146 instructions le chemin AVX2, 57 le repli SSE2 — jamais une cellule Unicorn simulée).

## OPT-12 — LA BOUCLE PORTEUSE AES-NI : LA CIBLE ≤12 CYCLES/BLOC ATTEINTE À 7,09, LE CACHE DE ROUND-TRIP 680×, L'INCRÉMENT −54 % (ahult8jgd, la vague 11 ; le plan gelé sha256 6d3e94b2692d79c7… AVANT toute mesure)

**Le levier (le hot path mesuré)** : la boucle porteuse du flux AES-NI v2 — 50,56 cycles/bloc enveloppe comprise (la référence publiée 54, la même machine) contre le corps NI net 4 et la calibration du stub 3,75 : LA CHAÎNE add→mov→call sérialisée par registres porteurs paie ~46 cycles/bloc de forme.

**Le geste** : (1) LES V3 — la table d'adresses précalculée (53,11 — ne brise PAS la dépendance, l'écart nommé : le levier est le mode d'adressage indépendant, pas la précalcule), le déroulage k=4 (53,17 — idem), l'inline (48,41) ; (2) LES V4 — la restructure au mode d'adressage [base + index*8] : L'APPEL 7,81, L'INLINE 7,09 c/bloc [IQR 0,09] aux 64 blocs (5,10 aux 256) — LA CIBLE ≤12 ATTEINTE, LE GAIN 7,1× sur le v2, la boucle porteuse rejoint LA CLASSE du scellé appelé par le compilateur (7,62) ; (3) LE CACHE DE ROUND-TRIP — la clé sha256(notation || moteur || profil), le hit sans ré-exécution : l'ouverture 283,7 ms → 0,4 ms (680,6×), le contrôle négatif double (l'octet muté : clé différente ; le compte muté : re-vérification COMPLÈTE qui attrape) ; (4) LA CRISTALLISATION INCRÉMENTALE — la fermeture transitive du diff seule re-vérifiée (le diff réel tls13-02 : 11 blocs sur 28, −54 %), l'audit 1/10 maintenu (LE CONTRÔLE NÉGATIF NOMMÉ : le cristal empoisonné épargne le muté hors fermeture — l'audit est un filet probabiliste à 9,5 % par tirage, JAMAIS une preuve ; la garantie demeure la semence full-card).

**La décomposition des 37 s** (le bras T, n=5, la table publiée) : LES ORACLES PORTENT 81 % (35,3 s — les re-exécutions vivantes), la cristallisation 4,5 s, les round-trips 0,61 s, la recomposition 0,49 s — la somme réconciliée à 7 ms près (l'inter-poste borné) ; le recoupement avec le bras C+G+ (oracles à volumes égaux : 0,51 s) tranche : le coût du régime de vérification EST le volume d'oracle, pas la notation des octets.

**Les contrôles** : la parité observable intégrale (le calendrier FIPS 197, le vecteur C.1, la différentielle 64/64 ET 256/256 octet pour octet aux neuf formes, les replis forcés) ; LE CONTRÔLE NÉGATIF ATTRAPÉ (l'octet du déroulé muté — divergence au premier vecteur) ; la borne N ≤ 256 fail-closed ; le round-trip 100 % aux dix notations ; LES SCELLÉS INTACTS avant et après chaque exécution.

**Les limites nommées** : UNE SEULE MACHINE au bac ; les consoles de la décomposition non ligne-identiques aux historiques (les horodatages — l'écart nommé).

## OPT-13 — LE QUATRIÈME BRAS C+G+ : L'EFFET NOTATION PROPRE CONFIRMÉ À 55,7 %, LA VENTILATION TROIS-EFFETS PUBLIÉE (3lmyfb2xa, la vague 11 ; le plan gelé sha256 c2a484e720ba44e8… AVANT toute mesure)

**La question (falsifiable, pré-enregistrée)** : l'écart T−C+G = 37,07 s (la vague 10) est-il l'effet NOTATION PROPRE ou l'effet du RÉGIME DE VÉRIFICATION ? — le bras C+G+ répond : le C gcc-O2 recevant la gouvernance ET le régime de vérification complet du bras T (les rebuilds ×10 avec confrontation d'octets — l'équivalent compilé du round-trip, documenté comme tel ; les volumes oracle ÉGAUX comptés par unité ; la recomposition du plan).

**La mesure (les QUATRE bras, la même machine, n=5, l'ordre ALTERNÉ T→C+G+→C+G→C par run — la rotation contre la dérive thermique, l'horloge monotone)** : T 39,39 s [39,31–39,48] · C+G+ 18,68 s [18,41–19,08] · C+G 2,18 s [2,14–2,24] · C 1,97 s [1,92–1,98]. **LE VERDICT** : (T−C+G+) = 20,72 s = 55,7 % de (T−C+G) = 37,21 s — **> 30 % : H-CGP2 CONFIRMÉE, la requalification H-CGP1 REJETÉE**. LA VENTILATION TROIS-EFFETS : notation propre 20,72 s (55,7 %) + régime de vérification 16,50 s (44,3 %) + gouvernance 0,213 s — somme 37,43 s == T−C exacte.

**La décomposition du bras C+G+ (Σ = 18,678 s = le total)** : REBUILDS 15,865 s (84,9 % — 6 unités × 10 confrontations d'octets) ; ORACLES 0,507 s (2,7 % — 12 épreuves/14 contrôles + 2032 décalages, les volumes égaux au bras T) ; RECOMPOSITION 0,032 s ; GARDES 0,153 s ; gouvernance g2-g4 0,151 s ; base C 1,948 s. **LE RECROISEMENT AVEC LE BRAS T** : les oracles du bras T portent 33,48 s (85 %) contre 0,51 s au C+G+ AUX MÊMES VOLUMES (66×) — la différence vit dans la NATURE des oracles (les re-exécutions vivantes sous Unicorn de la notation, jamais demandées au compilé).

**Les contrôles** : la réconciliation 20/20 runs dans les tolérances nommées (T +31…61 ms ≤ 150 ; CGP +15…17 ms ≤ 100 ; C/CG ±1 ms ≤ 50) ; LE CONTRÔLE NÉGATIF double (+500 ms injectés dans une COPIE : la variante inter-étapes attrapée par la borne de comptabilité +0,541 s ; la variante in-étape attrapée par le scan de déviation — « recomposition-du-plan » 0,534 s vs médiane 0,032 s, ATTRIBUÉE au site vrai ; spécificité 0 faux positif sur 5 runs honnêtes) ; LES SCELLÉS 14/14 avant et après (les 5 runs T consignent scelles_intacts=true).

**Les gaps nommés** : la première mesure coupée par le bac au run 3 — REFAITE ENTIÈRE (9 registres archivés à session-interrompue-1/, jamais fusionnés) ; la confrontation d'octets intra-lot (le -o absolu vague 10 non reproduisible sans toucher l'atelier interdit — liaison par les sources) ; l'asymétrie de volume rebuilds (T 12×u01 vs C+G+ 10×6) publiée.

## OPT-14 — LE GABARIT VERSIONNÉ, LE LOCALISER HIÉRARCHIQUE, L'AJOUT PAR SQUELETTE : LA PROSE SAISIE (o5apue194, la vague 11 ; le plan gelé sha256 ea388f511982a808… AVANT toute mesure)

**Le levier (le constat v0.21.0)** : la prose domine l'opération éditer (866 cl100k sur 1 146 — la consigne en langue naturelle) ; le matériau déjà réduit (239).

**Le geste** : (1) L'ÉDITER-T2 — la consigne remplacée par le gabarit versionné TPL-EDIT-v1 (le corps vit une fois, l'ID + l'empreinte + les paramètres littéraux par opération, l'expansion côté client fail-closed) : 1 106 → 674 natif (**−39,1 %**), LA PROSE 866 → 372 (−57 % — le levier saisi) ; (2) LE LOCALISER-H — l'index grossier (IDs + empreintes courtes) puis l'entrée fine : 1 053 → 627 (**−40,5 %**, le matériau 826 → 335) ; (3) L'AJOUTER-S — le squelette dérivé de la couche I (le cadre ABI, la signature), l'agent ne remplit que la logique : 3 074 → 2 200 (**−28,5 %**), la faisabilité 0 → 3 verts.

**La lecture honnête** : l'ajouter demeure dominé par les REFUS HORS-FORMAT nommés (15/18 — les étiquettes inconnues, les constantes du domaine) : le squelette fait la moitié du chemin, le gap nommé — le prochain levier est le gabarit DU DOMAINE (étiquettes + constantes) étendu au squelette. Le refus CONTEXTE-DIVERGENT de loupe-07-cumul aux DEUX phases éditer (la variation est au modèle, pas au gabarit — consignée, jamais re-tirée).

**Les contrôles** : n=18 par opération à la graine 20261117 reconduite (l'ordre jamais re-tiré) ; 108 appels journalisés au champ usage ; la re-tokenisation indépendante à écart max 0 (≤1) ; LE CLIENT 16 VERT (les refus nommés re-roulés aux trois modes — GABARIT-DIVERGENT, POINTEUR-INCONNU, EMPREINTE-DIVERGENTE, EXPANSION-DIVERGENTE, INDEX-DIVERGENT, HORS-FORMAT) ; la garde sha256 de la fenêtre conservée ; AUCUN contrôle retiré.

OPT-15 — TPL-ADD-v2 (pgodgk35l) : LE DICTIONNAIRE DE DOMAINE VERSIONNÉ — la faisabilité 3/18 → 5/18 verts (l'ajouter-S v1 de la vague 11 : 3/18 ; le v2 au dictionnaire LBL/CST + le squelette : 5/18 — loupe-03-fermer, loupe-18-quitter, loupe-05-sha256 CONVERTIS, loupe-02 et loupe-04 tenus, loupe-13 perdu aux erreurs d'assemblage du modèle) ; le coût natif médian 3 718 (la cible ≤ 1 500 manquée — le dictionnaire et le few-shot PAIENT au prompt : la médiane v1 était 2 199 ; le lexique admissible coûte) ; LES TROIS PASSES du client nommées (l'expansion LBL aux adresses fixes = vice de conception — les étiquettes internes dépendent de la disposition du corps réécrit, corrigé à l'expansion AU NOM CANONIQUE avec la résolution locale ; le few-shot contre les définitions LBL-xxx: ; l'extraction étendue des constantes sémantiques du corps) ; le gap résiduel par classe : 7 HORS-FORMAT (les formes invalides du modèle : cmp mémoire-à-mémoire, movzx r64/r64, xor dword/r64, les troncatures, les symboles en clair VK_LEFT) · 3 ID-INCONNU (les IDs hallucinés au-delà du dictionnaire du bloc) · 3 EXPANSION-DIVERGENTE (l'IAT en opérande, le call-à-étiquette) ; JAMAIS re-tiré (la cible pré-enregistrée falsifiable, l'issue consignée telle quelle).

## OPT-16 — LE V5-ENTRELACÉ AUX CALENDRIERS INDÉPENDANTS ET L'AVX2 APRÈS HISSAGE : LA CIBLE ≤ 3 c/bloc MANQUÉE AU PLANCHER DE L'UNITÉ (0,459 c/aesenc mesuré), LE COULOIR DE RECHERCHE 12,4× (x705m50vl, la vague 12 ; le plan gelé sha256 c24a729de4305df6… AVANT toute mesure)

**Le levier (les deux constats)** : (a) la boucle porteuse v4-inline publiée à 7,09 [0,09] c/bloc aux 64 blocs — le levier nommé de v4 : « l'indépendance d'adressage, pas la précalculée », étendu aux CALENDRIERS de clés : k ∈ {4, 8} schedules aux adresses INDÉPENDANTES, les corps aesenc des k blocs ENTRELACÉS par tour (la lecture rk du flot j précède immédiatement son aesenc, les k-1 autres paires exécutent pendant la latence) ; (b) le couloir de recherche AVX2 à 5 846 [138] cycles/op (4096/16 absents) DOMINÉ PAR LE SONDAGE cpuid par appel (≈ 2 660 cycles la sortie d'hyperviseur, fnvan0zes : « l'embarquement exigera le sondage hissé, le couloir porte la note »).

**Le geste** : (1) ENT4 804 o à la marge 0xE200 et ENT8 1 536 o à 0xE800 (l'écart au plan nommé : le corps k=8 ne tient pas la fenêtre 0x200, et ent4 lui-même déborde 0xE400) — un registre de base PAR flot (rbx · rdi · rsi · rbp · r12-r15), le mode [base + rax + déplacement] plié, aucun add, aucune table ; LE MUTANT (le disp32 0x90 → 0x91 de la lecture du flot 0) et LA SONDE PLANCHER-AESENC (66 o : huit chaînes indépendantes sur REGISTRES SEULS, aucune donnée — le débit nu de l'unité, la cause mesurable) ; (2) LE COULOIR HISSÉ 441 o à 0xE600 — le sondage cpuid HISSE UNE FOIS PAR SESSION à l'appelant, le verdict RÉSOLU AU CHARGEMENT PASSÉ SOUS R10 (r10 = 0 → AVX2, ≠ 0 → le repli SSE2 intégré, jamais un chemin mort), LE PORTEUR r11 de la fenêtre (la leçon des registres porteurs 8z4hj76w4 reconduite : le repli16 atteint depuis la file AVX2 où rcx est consommé — la faute du premier passage vécue au vecteur 57, nommée).

**La mesure (RDTSCP, cœur 1, n = 20, médiane non arrondie + IQR, les cycles bruts publiés)** : ent4@64 413 c = **6,453** [0,125] · ent4@256 1 360 = **5,313** [0,070] · ent8@64 381 = **5,953** [0,125] · ent8@256 1 240 = **4,844** [0,039] c/bloc ENVELOPPE COMPRISE — contre v4-inline AU RIG MÊME 5,719 [0,031] et 4,762 [0,008] (les publiées 7,09/5,10 DATÉES d'un autre jour). **LA CIBLE PRÉ-ENREGISTRÉE ≤ 3 c/bloc MANQUÉE aux deux tailles — LE GAP NOMMÉ PAR MESURE** : le plancher-aesenc rend 1 880 c [2] aux 4 096 aesenc = **0,459 c/aesenc — l'unité débite 2,18 aesenc/cycle, le plancher arithmétique d'un bloc AES-128 est 10 × 0,459 = 4,59 c/bloc enveloppe libre** : aucune organisation des lectures ne descend sous le débit de l'unité, la cible ≤ 3 exigeait ≥ 3,33 aesenc/cycle ; ent8@256 vit à **1,055× le plancher** (l'entrelacement k=8 SATURE l'unité, l'écart résiduel 0,25 c/bloc = la pression des lectures, le compte Unicorn nomme le +48 % d'instructions : 24,5-25,4/bloc contre 16,6-16,9 à v4i) ; LA LECTURE HONNÊTE : l'indépendance d'adressage étendue au calendrier N'EST PAS le goulot sur cette machine — v4i (les lectures rk partagées) demeure devant aux deux tailles : LE GAP A DÉPLACÉ de l'organisation des lectures au débit de l'unité de silicium, le plancher mesuré le nomme. **LE COULOIR DE RECHERCHE HISSÉ : 470 c [26] contre 5 840 [148] au dispatch par appel — LE GAIN 12,4×** (le sondage ne se paie plus par appel) ; le repli SSE2 forcé 1 540 [10] (3,3× le chemin AVX2, 11,8× devant le scellé GPR — la machine sans AVX2 vit un repli honnête) ; LES NON-RÉGRESSIONS tenues (le couloir à dispatch 5 840 [148] contre la publiée 5 846 [138], le scellé loupe-13 18 228 [18] contre 18 226 [4] — les écarts 6 et 2 cycles dans l'IQR).

**Les contrôles** : la parité TOUT VERT — le calendrier FIPS 197 §5.2 par le scellé tls13-15 (ET les huit clés du banc 8/8) ; le vecteur FIPS C.1 aux quatre corps ; la différentielle 64/64 ET 256/256 octet pour octet contre le scellé appelé par bloc (aux calendriers égaux) ET LE MAPPAGE AUX HUIT CLÉS DIFFÉRENTES (le bloc i au calendrier i mod k, le juge le scellé à la bonne clé par bloc — 64/64 et 256/256) ; LES QUEUES aux huit tailles (restes 1-3 et 1-7 vécus) ; LA BATTERIE 559 re-roulée : le chemin AVX2 réel ET le repli forcé ZÉRO DIVERGENCE au natif, le repli ZÉRO DIVERGENCE sous Unicorn (LA BORNE : Unicorn sans AVX, le chemin ymm jamais simulé) ; LA BORNE N ≤ 256 fail-closed (rax = -2, rien chiffré) ; LE CONTRÔLE NÉGATIF (l'octet muté du corps entrelacé) ATTRAPÉ AU PREMIER VECTEUR ; le round-trip 100 % aux neuf corps ; LES SCELLÉS 14/14 avant et après CHAQUE partie (la garde à quatre reprises, les quatre pièces aux ancres R7).

**Les limites nommées** : UNE SEULE MACHINE au bac, virtualisée — le plancher 0,459 c/aesenc est le débit de CETTE machine virtualisée (le matériel nu peut différer, la mesure au terrain) ; la cible pré-enregistrée manquée consignée TELLE QUELLE, jamais re-tirée ; la faute de la passe morte nommée (le corps ent8 déclaré aux huit bases chargeait tout de rbx — réécrit, le mappage aux clés différentes le juge).

## OPT-17 — LE COULOIR GHASH EN PCLMULQDQ : LA CIBLE ≤ 80 CYCLES ATTEINTE (64,04/63,39 c), LE GAIN 12,6× SUR LE SCELLÉ, L'AES-GCM COMPLET FACE À OPENSSL EVP (0g3400vql, la vague 13 ; le plan gelé sha256:caab6f481ab3799f… AVANT toute mesure)

**Le levier (les constats mesurés).** Le GHASH restait le hotspot GCM non descendu (I5 de la spec : le chantier futur NOMMÉ) : le scellé tls13-17 — la marche bit-à-bit de l'algorithme 1 SP 800-38D, 128 itérations — mesure **806,35 c [10398]** la multiplication au rig virtualisé (RDTSCP, cœur 1, n = 20). Les comparaisons d'époque portaient sur le scellé et la libc, jamais sur OpenSSL (le contexte de l'instruction).

**Le geste.** (1) Le couloir GHASH en PCLMULQDQ aux DEUX variantes — le produit **Karatsuba 3× pclmulqdq** (ghash-pclmulqdq-karatsuba.asm, 334 o à la marge 0xE800) et **schoolbook 4×** (ghash-pclmulqdq-schoolbook.asm, 326 o à 0xEA00) — le domaine DÉRIVÉ ET VÉRIFIÉ : Xi = N_X (pshufb inverse), Hkey = twist(N_Y) = N_Y·x mod P̃ (le twist SANS BRANCHE : psllq par qword + le carry inter-qword par psrlq63/pslldq8/por + la retenue du bit 127 par pcmpgtd/pand/pxor sur C = 0xC200000000000000‖1), le sel HK = qs(Hkey)⊕Hkey, la réduction PAR DÉCALAGES (alg9 : psllq 5/1/57 + pslldq/psrldq + psrlq 1/5/1 — AUCUN clmul en réduction) ; le contrat tls13-17:R1 TENU (rcx=Z, rdx=X, r8=Y, rax=0, X/Y intacts, commutatif, chevauchement permis). (2) La sonde de session (sonde-session.asm, 73 o à 0xE600) : le sondage cpuid UNE FOIS PAR SESSION POUR TOUS LES CORRIDORS (leaf 1 : PCLMUL bit 1, AES bit 25, OSXSAVE bit 27 ; leaf 7 : SHA-NI bit 29), le verdict en rax/r10 — les couloirs ne sondent PLUS par appel (le comptage cpuid/session == 1, exigé). (3) Le dispatch du couloir sous r10 (r10&1 → pclmulqdq, sinon jmp au scellé 0xDFC0 — JAMAIS un chemin mort, le repli 32/32).

**La mesure (RDTSCP, cœur 1, n = 20, médiane non arrondie + IQR, cycles bruts ; la machine Xeon 3200 MHz, drapeaux aes/avx2/pclmulqdq/sha_ni consignés au registre).** karatsuba **64,04 c [22]** · schoolbook **63,39 c [30]** — LA CIBLE PRÉ-ENREGISTRÉE ≤ 80 c ATTEINTE aux deux ; la mesure TRANCHE : schoolbook devant de 0,65 c (1,0 %, DANS l'IQR — l'écart nommé non significatif, les deux livrées) ; le scellé 806,35 c — **LE GAIN 12,6×**. L'AES-GCM COMPLET (la porteuse v4-inline + le GHASH par bloc + l'étiquette, le calendrier par le scellé tls13-15) : **7,556 c/octet** @4096 contre la composition scellée-17 58,80 (7,8×) et le scellé tls13-18 64,34 (8,5×) ; face à OpenSSL EVP : **aes-128-gcm 0,5823 · aes-256-gcm 0,6169 c/octet** — OpenSSL 13,0× devant à 4096 (le GHASH agrégé 4 blocs/appel d'OpenSSL, l'écart NOMMÉ) ; **@64 la composition couloir 19,47 c/octet DEVANT EVP 23,66 (1,2×)** — le coût par appel d'EVP payé au petit message. LE SHA-256 complet : le corridor SHA-NI reconduit 45,11 c/octet — DOMINÉ PAR LE CPUID PAR APPEL du design v11 (170 240 c = 92,1 % ; le corps nu ≈ 228 c/bloc = 3,56 c/octet, le gain 3,7× sur le scellé 13,10) ; EVP_sha256 2,036 c/octet (1,75× devant le corps nu, l'agrégation nommée).

**Les contrôles.** La parité TRIPLE 25/25 : rig-GCM(couloir) == rig-GCM(scellé 17) == LE SCELLÉ tls13-18 == OpenSSL EVP (ct et étiquette octet pour octet) ; SHA : couloir == scellé 02 == EVP. La différentielle 320/320 zéro divergence contre le scellé (les deux variantes), les cas punitifs 7/7, la commutativité et X/Y intacts 32/32, le repli 32/32, le mutant (l'imm8 du premier clmul muté) ATTRAPÉ au premier vecteur, le round-trip 9/9. Le temps-constant STRUCTUREL : UNE empreinte de trace par classe (60 mesures, adresses et tailles seules hachées), AUCUNE instruction à latence variable sur le chemin (div/idiv/cpuid/rdtsc absents du corridor — le sondage VIT à l'appelant, PUBLIC), le seul jcc sur r10 public. Les scellés 14/14 avant et après (la garde du sceau-I), les quatre pièces aux ancres R7 recoupées.

**Les limites nommées.** LE BAC VIRTUALISÉ — les cycles sont LES CYCLES DE CETTE MACHINE (le cpuid y coûte ~2 660 c ; le silicium nu au geste du développeur au terrain) ; UNE SEULE machine ; le corridor SHA-NI d'époque RECONDUIT avec son dispatch par appel (le coût mesuré 92,1 % du total — la renotation hissée nommée geste suivant) ; la composition par blocs contre l'agrégation d'OpenSSL (l'écart @4096 structurel, jamais maquillé).

## PROVENANCE DES TABLEAUX — LE REGISTRE DE LA VAGUE 17 (atelier W17R4PER, D255)

> Toute valeur citée dans les tableaux est désormais recomposée depuis une **source
> canonique committée** (JSONL/JSON), avec son empreinte. Le registre vit à
> `replication-v17/provenance-v17.json`, généré par `scripts/vague17/provenance_tableaux.py`
> et gardé par les trois classes de provenance du linter (`--provenance`).

### Les quatre grandeurs, jamais additionnées ni comparées

| Grandeur | Objet | Unité | Ce qu'elle n'est pas |
|---|---|---|---|
| (a) contrainte d'artefact natif | l'absence de compilateur | propriété booléenne par artefact | une mesure de vitesse |
| (b) performance d'exécution | latence, débit, mémoire, taille | cycles, c/octet, c/bloc | un coût d'édition |
| (c) coût d'édition et de validation | tokens, temps, calcul | tokens par changement validé | une performance d'exécution |
| (d) sûreté et couverture | mutants, corpus, preuves | comptes, pourcentages | une vitesse |

### Le registre (11 lignes, recomposées le 24/11/2026)

| Id | Grandeur | n | Valeur recomposée | Statut | Source |
|---|---|---|---|---|---|
| tpl_v2 | (c) TPL-ADD-v2 | 18 | 5 verts · médiane 3 718,5 sur les 18 tâches · 2 959 sur les vertes | mesuré (VM, glm-4-plus) | `atelier-ajouter-v2-pgodgk35l/resultats_v2.jsonl` |
| tpl_v3_ajouter | (c) TPL-ADD-v3, mode ajouter | 18 | 6 verts · médiane 5 545 sur 18 · 3 844 sur les vertes | mesuré (VM, glm-4-plus) | `atelier-ajouter-v3-5nwnwoceo/resultats_v3.jsonl` |
| tpl_v3_editer | (c) TPL-ADD-v3, mode éditer | 18 | 18 verts · médiane 712,5 | mesuré (VM, glm-4-plus) | même fichier, mode `editer-v3` |
| tpl_v4 | (c) TPL-ADD-v4 | 18 | 7 verts · médiane 5 601 sur 18 · 3 990 sur les vertes | mesuré (VM, glm-4-plus) | `atelier-ajouter-v4-842vqyy1k/resultats_v4.jsonl` |
| tpl_v5 | (c) TPL-ADD-v5 | 18 | 5 verts · médiane 6 462,5 sur 18 · 4 604 sur les vertes | mesuré (VM, glm-4-plus) | `atelier-ajouter-v5-yfkpml1j2/resultats_v5.jsonl` |
| gabarits | (c) gabarits versionnés | 108 | 73 verts | mesuré (VM) | `atelier-gabarits-o5apue194/resultats_gabarits.jsonl` |
| corpus_train | (d) corpus v2.1 | 127 | 127 triples | mesuré (fichier livré) | `depot-zenodo-corpus-v21/train.jsonl` |
| corpus_dev | (d) corpus v2.1 | 24 | 24 triples | mesuré (fichier livré) | `depot-zenodo-corpus-v21/dev.jsonl` |
| corpus_test | (d) corpus v2.1 | 19 | 19 triples | mesuré (fichier livré) | `depot-zenodo-corpus-v21/test.jsonl` |
| corpus_dpo | (d) corpus v2.1 | 48 | 48 paires | mesuré (fichier livré) | `depot-zenodo-corpus-v21/dpo-paires.jsonl` |
| ghash_ratio | (b) GHASH agrégé / scellé | — | 78 888 / 1 606 = **49,12×** | mesuré (émulation + natif, même machine) | `atelier-ghash-agrege-h1mz2sr8s/registres/ghash-agrege.json` |

**Les deux conventions de médiane sont nommées, jamais confondues** : celle des 18 tâches
(refus compris — c'est elle que le manuscrit publie : 3 718 pour v2, 4 604 pour v5) et
celle des seules tâches vertes. Le fichier v3 porte DEUX modes de 18 tâches chacun
(`ajouter-v3` 6/18, `editer-v3` 18/18 à 712,5 — le 712 publié est la troncature de 712,5,
la convention de publication d'une décimale) ; les confondre donnerait 24/36, un compte
sans signification. L'écart de 0,5 est un arrondi de publication, nommé.

**Les contrôles vécus** : `--verifier` → `CONFORME` (10/10) ; `--controle-negatif` →
4/4 (valeur, ratio, compte, statut), chacun refusé au premier nom. **Ce que le registre
ne prouve pas** : aucune mesure au métal nu (statut « mesuré » = VM ou émulation, jamais
silicium), et l'opt05 n'entre pas au registre faute de champ structuré — l'absence est
nommée.

## OPT-18 — LE COULOIR VAES/VPCLMULQDQ : LA CIBLE ≤ 1,05 × EVP MANQUÉE À 5,66 ×, LA PORTE VERTE D'ABORD, CINQ FAUTES DE PREMIÈRE PASSE NOMMÉES ; LA SESSION NATIVE DU MOTEUR D'ORACLE TENUE À 0,266 S (W27VAES, la vague 27 ; le plan gelé sha256 958215b0dbce5efa… AVANT toute mesure)

**Le levier (les constats mesurés).** Le couloir entrelacé AVX2/AES-NI de W20PERF mesurait 0,7271 c/B et 1,26 × EVP sans cible propre ; CIB-AES-105 pré-enregistrait (D273) la spécialisation VAES/VPCLMULQDQ à ≤ 1,05 × OpenSSL EVP au même volume — la cible relative, jamais re-tirée.

**Le geste.** (1) LA NOTATION D'ABORD (couloir-vaes.asm, sha256 7911d03f… consignée AVANT l'implémentation) : CPUID hissé hors boucle (refus nommé SILICIUM-ABSENT, aucun repli), CTR×VAES deux blocs par vAESENC aux clés broadcastées, GHASH à pli de HUIT blocs par Karatsuba sur VPCLMULQDQ (une seule réduction par pli), entrelacement CTR(g+1)×GHASH(g). (2) L'IMPLÉMENTATION EXÉCUTABLE (couloir_vaes.c) — la session précédente mourut sur sa première passe fautive ; la reprise la solda : CINQ FAUTES NOMMÉES AU SOURCE (rev128 : PSHUFB annulant les indices à bit 7 — les quartets masqués ; le saignement des décalages 16 bits — la composition re-masquée 0xF0 ; le bswap16 surajouté — la réduction d'Intel vit dans le monde bitrev8-ordre-préservé, recoupé contre la référence GCM indépendante [gfmul(bitrev8(X), bitrev8(Y)) == bitrev8(X•Y)] ; le pli : vb assemblé [h1|h0] — les produits croisés C_{2p+1}⊗H^{7-2p} ; a01/b01 par permute2x128⊕va — les voies échangées au lieu du (lo⊕hi) de Karatsuba, l'idiome juste unpacklo⊕unpackhi par voie, ET les moitiés du produit de la voie 1 aux tas croisés). (3) LA SESSION NATIVE DU MOTEUR (prompt 6, geste 3) : le refus mmap 0xC000 du bac d'alors re-prouvé (mmap_min_addr 4 096 — la cartographie passe), la porte du moteur re-vécue verte (jumeau ligne-identique aux deux corps, le shim muté attrapé au premier vecteur, la mémo MISS à l'octet muté, l'audit 1-sur-10 zéro écart), puis LA SESSION : les 50 blocs assemblés DEPUIS LEURS NOTATIONS (sha256 recoupés 50/50 au manifeste-52), 235 vecteurs exécutés nativement (chaque bloc en sous-processus — un SIGSEGV nomme le vecteur FAULT, jamais la session).

**La mesure (n=20, cœur épinglé 0, 4 Kio, OpenSSL EVP 3.5.7 au même volume, quatre passes : 5,6468/5,6637/5,6904/5,6709 — IQR ≤ 116 ns ; l'environnement consigné : VM Xeon @ 2 793 MHz, fréquence non goupillée, le caveat nommé).** Le couloir 4 463 ns médian contre EVP 787 ns — **RATIO 5,66 × : LA CIBLE ≤ 1,05 × MANQUÉE, consignée telle quelle**. La décomposition du coût (le gap nommé par classe, puits anti-code-mort) : l'init 296 ns (l'expansion scalaire + les puissances H — 38 % de la session EVP entière), le chiffre seul 1 679 ns (1,145 c/octet estimé), le combiné inliné avec puits 1 916 ns (2,44 × — manque encore : le verdict robuste à la lecture), la frontière d'appel hors ligne 2,3× (4 462 vs 1 916 ns). LES CAUSES NOMMÉES : l'expansion hors boucle non spécialisée, la conversion rev128 PAR BLOC côté GHASH, le calendrier d'entrelacement écrit en C (le compilateur ne préserve pas la co-scheduling VAES/VPCLMULQDQ qu'un scheduleur assembleur tient — OpenSSL mesure 0,54 c/B sur la même machine). **LA SESSION NATIVE : 0,246/0,246/0,266/0,269/0,274 s — MÉDIANE 0,266 s, LA CIBLE T < 10 S (CIB-ORACLE-T) TENUE à 26,6× sous la borne ; la classification 235/235 identique au jumeau (81 OK / 154 FAULT), le digeste 81/81 identique, 77/81 strictement ligne-identiques, les quatre écarts d'UNE classe nommée (b20006 ne définit pas rax — le jumeau initialise à zéro, le natif y laisse 0xC000 ; le digeste identique aux quatre).**

**Les contrôles.** LA PORTE AVANT TOUTE MESURE (registre-porte.txt, le rejeu bit-identique rejeu-porte.txt) : la parité 20/20 vecteurs NIST CAVP 14.0 couloir == EVP octet pour octet (4 Kio paddés, tags compris — le juge croisé EVP au point scellé, les tags E_K(J0) des vecteurs vides recoupés à part) ; LE NÉGATIF : la variante mutée (rk13 ⊕ 0x5a) refusée AU PREMIER VECTEUR, le refus nommé ; LE ROUND-TRIP inter-implémentations couloir→EVP VERT. Le diagnostic qui départagea les fautes : la référence GCM Python (polynôme direct, validée sur le vecteur CAVP 13 octets ET le tag EVP 4 Kio), la trace du compte pli par pli, le juge croisé. Les scellés 14/14 avant et après (le sceau-I) ; la notation gelée INTACTE (7911d03f… inchangée) ; aucun artefact scellé touché, le couloir est une pièce de laboratoire autonome. **Ce que la mesure ne prouve pas** : aucun chiffre au silicium goupillé (VM, fréquence non goupillée — le kit machine réelle livré : source + notation + porte + la commande) ; les ~12 000 cas par bloc critique du protocole complet ne sont pas au corpus (les 235 vecteurs de la vague 20 demeurent l'échelle, l'attente de la vague 19 pour les 50 blocs au-delà).

## OPT-19 — LE COULOIR VAES, SECONDE CAMPAGNE : LES QUATRE CAUSES ATTAQUÉES, L'ÉCART
NOTATION-VS-C PUBLIÉ AU PROFIT DU COMPILATEUR (W28VAES, la vague 28 ; le plan gelé
sha256 37a4707e… AVANT toute mesure, EMPREINTES-PLANS-VAGUE28.txt)

L'AVANT (OPT-18, la vague 27) : 4 463 ns, 5,66 × EVP par appel (787 ns) — la cible
≤ 1,05 × manquée, la décomposition nommée par classes. L'APRÈS (la même porte d'abord :
20/20 CAVP pour CHACUNE des deux pièces, le mutant refusé, le round-trip vert, le rejeu
bit-identique — la convention session recoupée octet pour octet) :
- le portage C restructuré (le contexte de session, la frontière rev256 au pli, les
  locals/restrict — la cause dominante de la v2 était le rechargement des clés sous
  pointeur aliasable, nommée au source) : **1 012 ns** = 1,31 × EVP par appel, 2,47 × à
  contexte posé ;
- le schedule de notation en ASSEMBLAGE (les chaînes pipelinées deux à deux, la
  réduction pure SIMD) : **1 082 ns** = 1,41 × par appel, 2,68 × à contexte posé ;
- **L'ÉCART NOTATION-VS-C : 1,07 × AU PROFIT DU C** — le résultat distinct pré-enregistré :
  l'érosion de schedule N'EST PAS CONDUITE sur ce hot path ; le compilateur tient le
  calendrier dès que le C est écrit en forme ILP-friendly ; l'assemblage paye ses gestes
  de robustesse (l'acc au cadre, la ligne sauvée) plus cher que le compilateur ne paie son
  allocation de registres ;
- LE RÉSIDU STRUCTUREL nommé : EVP emprunte le chemin VAES512 (zmm, quatre blocs par
  vAESENC — le plafond mesuré 409 ns ≈ 0,28 c/octet à contexte posé), la notation gelée
  est ymm (deux blocs par vAESENC) — le corridor porte deux fois plus d'instructions AES ;
  la cible ≤ 1,05 × contre le chemin zmm demande la voie 512-bit — la notation est gelée
  (7911d03f… INTACTE), l'écart est nommé.

R11 : la mesure avant l'optimisation reconduite (la porte verte d'abord, chaque pièce) ;
la cible pré-enregistrée D273 JAMAIS re-tirée ; le verdict MANQUÉE publié tel quel ;
aucun artefact scellé touché (le sceau-I 14/14 avant et après) ; l'environnement consigné
(VM, cœur épinglé, fréquence non goupillée — le caveat nommé ; le kit machine réelle :
source, notation, porte, commandes — au rapport de l'atelier).

## OPT-16 — ÉDITER PAR DIFF STRUCTURÉ AU PLANCHER TOKEN : LA CIBLE ≤ 150 TENUE À 79,5
(W28OPT16, la vague 28 ; le plan gelé sha256 7e18806a… AVANT toute mesure, EMPREINTES-
PLANS-VAGUE28.txt)

L'AVANT : l'opération éditer adoptée coûtait 674 tokens natifs médians (TPL-EDIT-v1,
OPT-14) ; le plancher du diff réel : 27,5 tokens — le ratio 24,5×. LE SCHÉMA FERMÉ D264
étendu à l'édition : {op: "substituer", dst, offset, src} — l'agent ne rend QUE le diff
structuré ; LE CLIENT expande (la substitution à l'offset), confronte (le diff exact : la
ligne unique révisée, AUCUNE autre changée), le round-trip (keystone→capstone→keystone),
et REFUSE nommément : POINTEUR-INCONNU, EMPREINTE-DIVERGENTE, SCHÉMA-VIOLÉ, HORS-FORMAT
— la boucle de réparation bornée à trois tours réinjectant le refus exact.

LA MESURE (n=18, la graine 20261117, l'ordre canonique jamais re-tiré, le budget usage
lu à chaque appel) : MÉDIANE 79,5 TOKENS NATIFS SUR 18 — **CIBLE ≤ 150 TENUE** ; la
médiane sur les vertes (9/18) : 79 ; le ratio plancher : 2,89× LE DIFF RÉEL (au lieu de
24,5×) ; les refus par classe : 7 SCHÉMA-VIOLÉ (les tours de réparation — l'offset erroné
de la première passe le plus fréquent, corrigé au tour 2) ; la re-tokenisation
indépendante : écart 0 (les trois tâches à un tour re-notées à l'identique — 38/38,
38/38, 39/39) ; le juge D264 recoupé INTACT (9fc325e2…, expandeur_add.py —
JUGE-MODIFIÉ serait le refus).

LA LECTURE HONNÊTE : le diff structuré saisi le plancher (2,89× — de 24,5×) SANS lever
la faisabilité au-delà des 9/18 verts (les 9 rouges échouèrent la ligne exacte en trois
tours — la variance d'écriture machine demeure, nommée ; le décodage contraint au bord
reste le levier fermé D264). Les 6 premières tâches furent mesurées en deux séances (le
bord 429 dose l'appel — la reprise par point de contrôle, AUCUN chiffre re-tiré) ; la
convention des médianes : SUR 18 ET SUR VERTES, les deux nommées.

## OPT-20 — LE BUDGET TOKEN PAR VAGUE : LA PRODUCTION DE LA VAGUE 28 MESURÉE À 19 269 TOKENS NATIFS
(W28IMRAD, la vague 28, prompt 7, geste 4 ; le plan gelé sha256 consigné à
EMPREINTES-PLANS-VAGUE28.txt — la cible pré-enregistrée AVANT la mesure : le
budget de la vague suivante ≤ le compte de la présente)

LA MÉTA-OPTIMISATION (le protocole s'optimise lui-même) : le coût token de
génération du pack par vague, mesuré et pré-enregistré comme budget. LA
CONVENTION (nommée, honnête) : la vague PRODUIT des artefacts — les sept plans
gelés, les six premiers rapports d'atelier (le rapport du présent atelier hors
compte, sa taille ~500 tokens, la convention nommée), la prose source ajoutée
au manuscrit (la restructuration IMRAD, les trois paragraphes de travaux
connexes vérifiés, la note de vague 28, la note post-édition v0.33.0). LE
COMPTE NATIF est lu du CHAMP USAGE du bord — le texte porté par l'appel, la
convention OPT-14/16 reconduite : le compte est le LOG, jamais une estimation ;
le CL100K compté en parallèle (le compte distinct, jamais le juge).

LA MESURE : 17 pièces, 58 543 caractères — **19 269 TOKENS NATIFS** (19 744
cl100k). LA CIBLE BUDGET PRÉ-ENREGISTRÉE pour la vague 29 : **≤ 19 269 tokens
natifs de production** (la production de la vague 28 est le plafond ; la
lecture honnête : le budget borne la PRODUCTION autoriée, pas l'exécution des
chaînes de génération — les scripts tournent sans agent, les PDF naissent des
registres).

La pièce : atelier-w28imrad/mesurer_opt20.py + opt20-resultat.json (la
convention, les comptes, la liste des pièces).
