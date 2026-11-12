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
