#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_paquet6_shani.py — LE PAQUET 6/6 DE LA VAGUE 3 CONSACRÉ (la
variante SHA-NI, l'instruction lfh49a1xf) : le journal d'optimisation NAÎT
(OPT-01 — la première entrée, la référence D-… « format OPT-NN, versionné
avec la couche I »), la décision D205, l'Entrée 240, le worklog Task 147.
Append-only : les fins VÉRIFIÉES avant écriture, les rejeus REFUSÉS."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")

# --- LES TEXTES -------------------------------------------------------------------

JOURNAL_OPT = """# JOURNAL D'OPTIMISATION — le format OPT-NN (R11)

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
"""

D205 = """
## D205 — LA VARIANTE SHA-NI DE LA COMPRESSION SHA-256 CONSACRÉE AU LABORATOIRE, JAMAIS SCELLÉE (le paquet 6/6 de la vague du 12/11, l'instruction lfh49a1xf) : LE HOT PATH MESURÉ AVANT TOUT (R11 à la lettre — le hachage de fichiers volumineux instrumenté DANS LE HARNAIS LOUPE : **tls13-02 = 98,11 % des instructions exécutées** [64 Kio : 4 489 500/4 575 760 ; 256 Kio : 17 944 860/18 289 327, le profil stable, chaque condensé vérifié à hashlib avant verdict], la mesure consignée à preuves_v150/hotpath_shani/ AVANT le premier octet de la variante — l'ordre constaté sur les heures des fichiers par le vérificateur V6.a) ; LES SÉMANTIQUES SHA-NI ÉPINGLÉES PAR LE CODE sur le CPU natif du labo (experience_semantique_shani.py : l'opérande implicite de sha256rnds2 vit dans XMM0[63:0] — les sommes W+K —, dst=(C,D,G,H) reçoit le nouvel (A,B,E,F), src demeure ; msg1 : dst += σ0([dst1,dst2,dst3,src0]) ; msg2 : dst += σ1 CHAÎNÉ [src2,src3,dst0',dst1']) PUIS LA STRUCTURE ENTIÈRE ÉPROUVÉE À LA MAIN (epreuve_compression_shani.py : 100/100 au juge Python, les QUATRE vecteurs FIPS verts, le corpus aux bords vert — AVANT la notation) ; LA FAMILLE shani NÉE ÉCRITE-AVANT-CODE (shani/I/ : la sonde shani-01 CPUID [feuille 7 EBX bit 29 SHA ∧ feuille 1 ECX bit 9 SSSE3, rbx sauvé], la compression shani-02 [LE contrat de tls13-02 à la lettre — R4 : le corps DÉROULÉ en 16 phases, ZÉRO saut, xmm6/7 non volatils sauvés sur la pile, la table K @0x2F00 DU SCELLÉ citée par RIP en seize groupes alignés, le masque BE @0x2800], l'absorbeur shani-03 [LE contrat de tls13-03 à la lettre, la sonde RAPPELÉE UNE FOIS PAR APPEL — le sondage par bloc interdit, DEUX sites d'appel DIRECTS et STATIQUES : la variante 0xD080, LE SCELLÉ 0xC080 — le repli, R7]) ; L'ARRÊT D161 des slots sur les longueurs réelles (0xD000/0x40 · 0xD080/0x380 · 0xD400/0xC0 — la marge .text2 INT3 VIERGE du scellé loupe.exe, AUCUN octet du scellé touché) ; LA MESURE AVANT/APRÈS au laboratoire (8 Mio de PRNG déterministe, la même entrée, le condensé vérifié avant ET pendant le comptage, les opérations COMPLÈTES init+absorb+final, 15 répétitions, les médianes RDTSC : **l'avant [la composition scellée] 115 858 402 cycles = 13,811 cycles/o ; l'après [la variante dispatchée] 19 848 520 = 2,366 cycles/o ; LE GAIN 5,84× ; la surcharge du dispatch ±1 % — sous le bruit de mesure** [deux courses : +0,15 % et −0,69 %] ; le dry-run du kit : 6,52× à charge différente — l'ordre de grandeur stable) ; LE VÉRIFICATEUR DIX-HUIT CONTRÔLES VERTS (verifier_shani_v150.py : le round-trip 100 % [345 instructions], le temps constant STRUCTUREL [shani-02 zéro saut, shani-03 les sauts sur registres publics uniquement], la concordance au plan [les 20 RIP == le masque et les 16 groupes K ; les TROIS appels == le plan], l'héritage byte-identique, la sonde NATURELLE rendant 0 sous qemu64 [le repli vécu], LE ROUTAGE NOMMÉ aux deux sens [le compteur prouve le scellé exécuté au verdict 0 ; le verdict 1 forcé meurt DANS LE SLOT de la variante], la sonde réelle recroisée à /proc/cpuinfo, les QUATRE vecteurs dorés aux TROIS compositions, l'égalité scalaire/SHA-NI sur 1 000 tampons aux bords 0..65 537, l'invariance de découpage, les scellés INTACTS, le garde 14/14, l'ORDRE de R11) ; LE KIT TERRAIN LIVRÉ (shani/terrain/ : l'image 48 Kio [la K du scellé, le masque, la famille sha SCELLÉE extraite de loupe.exe, la variante assemblée — sha256 df851b7c…], le scénario bifteau sans outil [msx64 direct sous Windows, trampoline pré-assemblé sous POSIX], le LISEZMOI, le manifeste — la mesure du développeur dans les conditions exactes de l'instruction : même machine, même entrée, condensé vérifié avant comptage, opérations complètes) ; ET LE JOURNAL D'OPTIMISATION QUI NAÎT (docs/JOURNAL_OPTIMISATION.md — OPT-01, la première entrée : le format OPT-NN exigé par la règle de R11, versionné avec la couche I)

**Le contexte.** L'instruction lfh49a1xf (la vague 3, six fichiers reçus le 11/11 19:14 UTC) : identifier le hot path PAR MESURE d'abord, consigner la mesure avant toute optimisation (R11), puis — si le hot path est confirmé — créer la variante SHA-NI à dispatch CPUID avec repli scalaire sur les blocs scellés, contrat inchangé, adresses intactes, round-trip vérifié ; le kit de mesure terrain avant/après dans des conditions identiques ; aucun scellement ; les vecteurs dorés verts sur les deux chemins (dispatch forcé dans les deux sens), l'égalité des condensés sur corpus aléatoire, le contrôle structurel temps-constant, l'entrée OPT-NN au journal d'optimisation avec mesures avant/après, et le refus si le hot path n'est pas mesuré. Le hot path FUT mesuré (98,11 %) : l'optimisation n'est pas refusée, elle est fondée.

**Frontières.** Aucun artefact scellé touché (loupe.exe c1115105…, proxy.exe 446279f3…, demo.exe df8f2e50…, selftest.exe 8038585b… — sha256 recoupés avant ET après, INTACTS) ; le garde sceau-I 14/14 VERT avant et après ; la variante vit en COPIES DE LABORATOIRE aux adresses du plan — AUCUNE carte, AUCUNE cérémonie, AUCUNE balise (l'embarquement exigera la cérémonie d'ère du développeur) ; le run terrain de la mesure appartient au développeur (le kit livré, le témoin attendu) ; aucun chiffre fabriqué — tout nombre est LU d'une pièce ou mesuré devant témoin ; les consignations antérieures non réécrites (append-only).
"""

ENTREE240 = """

## Entrée 240 — LE PAQUET 6 DE LA VAGUE 3 EXÉCUTÉ : LA VARIANTE SHA-NI DE LA COMPRESSION SHA-256 (l'instruction lfh49a1xf menée à terme) : le hot path MESURÉ AVANT TOUT (tls13-02 = 98,11 % des instructions du hachage d'un fichier volumineux dans le harnais loupe — la mesure consignée AVANT le premier octet de la variante), les sémantiques SHA-NI ÉPINGLÉES PAR LE CODE sur le CPU natif du laboratoire, la famille shani NÉE ÉCRITE-AVANT-CODE (la sonde, la compression, l'absorbeur à dispatch — les contrats du scellé à la lettre), LE GAIN MESURÉ 5,84× au laboratoire (13,811 → 2,366 cycles/o, la surcharge du dispatch sous le bruit), le vérificateur DIX-HUIT contrôles VERTS, le KIT TERRAIN livré (la mesure du développeur, mêmes conditions, témoin attendu) — JAMAIS SCELLÉE : la cérémonie et l'embarquement appartiennent au développeur ; le journal d'optimisation NAÎT avec OPT-01 (12/11, la session de la vague 3, paquet 6/6)

**La mesure avant tout (R11).** mesure_hotpath_shani.py instrumente le harnais du noyau loupe RÉUTILISÉ TEL QUEL (l'émulation aux RVA du plan, les héritages extraits des scellés, le mini-OS virtuel) : le hachage de fichiers volumineux (64 Kio puis 256 Kio, graine 20261112) compté instruction par instruction par un hook SÉPARÉ — **tls13-02 = 98,11 % des instructions** (4 489 500/4 575 760 puis 17 944 860/18 289 327 — le profil stable ; l'initialisation 12 instructions, la finalisation 144 : O(1) ; chaque condensé VÉRIFIÉ à hashlib avant le verdict — l'instrument se contrôle avant de juger). La pièce consignée : preuves_v150/hotpath_shani/mesure_hotpath.txt (sha256 3f8678b3cd86f34b…) + comptage_instructions.csv (eb3038c04972ece7…), AVANT l'écriture de la couche I shani — l'ordre constaté sur les heures des fichiers (V6.a du vérificateur).

**Les sémantiques épinglées.** experience_semantique_shani.py : les hypothèses d'opérandes tranchées par l'exécution sur le CPU SHA-NI natif contre la référence FIPS en Python pur — l'opérande implicite de sha256rnds2 vit dans XMM0[63:0] (les sommes W+K — EAX n'y est pour rien, l'épreuve le prouva en faisant VARIER EAX sans effet), dst=(C,D,G,H) reçoit le nouvel (A,B,E,F), src demeure ; sha256msg1 : dst += σ0([dst1,dst2,dst3,src0]) ; sha256msg2 : dst += σ1 CHAÎNÉ (les éléments 2-3 lisent les éléments 0-1 déjà calculés — la fenêtre n'est pas une permutation). La mise en page de travail (F,E,B,A)/(H,G,D,C) — les paires renversées — dérivée de l'oracle du compilateur (gcc -msha, la transcription lue, pas un octet copié) puis RE-DÉRIVÉE à la main dans l'épreuve. epreuve_compression_shani.py : MA PROPRE structure — 16 phases déroulées, le cur TOUJOURS en xmm0, les groupes JAMAIS additionnés de K, le grattoir xmm7, xmm6/7 sauvés (le budget des six volatils ne suffit pas : le septième et le huitième vivent LOUÉS sur la pile, le contrat msx64 honoré) — confrontée au juge : 100/100 blocs aléatoires, les QUATRE vecteurs FIPS 180-4 § 6.3.1, le corpus aux bords : TOUT VERT sur le chemin matériel AVANT la notation. DEUX DÉFAUTS D'INSTRUMENT attrapés par l'épreuve elle-même (la méthode à l'œuvre) : la référence Python portait un piège de précédence (^ sous + — le jury faux, la machine juste) et les « vecteurs 448/896 bits » étaient des données fautives (les VRAIS messages du standard portés) — la machine était droite, les JUGES étaient faux : corrigés devant témoin.

**La famille shani (écrite-avant-code, D205).** shani/I/ : la sonde shani-01 (CPUID feuille 7 EBX bit 29 SHA ∧ feuille 1 ECX bit 9 SSSE3 — la CONJONCTION : pshufb/palignr exigent SSSE3, un SHA sans SSSE3 n'aura PAS la variante ; rbx sauvé, AUCUN autre effet) ; la compression shani-02 (LE contrat de tls13-02 à la lettre — R4 : le corps DÉROULÉ, ZÉRO saut, ZÉRO opérande mémoire indexé — le temps constant PAR CONSTRUCTION, le contrôle structurel le constate ; la table K @0x2F00 CELLE DU SCELLÉ en seize groupes alignés, le masque BE @0x2800 [la marge .rdata vierge constatée : 16 octets nuls dans loupe.exe] — JAMAIS re-déclarée) ; l'absorbeur shani-03 (LE contrat de tls13-03, le chemin PLEIN sur l'ÉGALITÉ STRICTE — le miroir du scellé ; LA SEULE DIFFÉRENCE : la sonde RAPPELÉE UNE FOIS PAR APPEL, le verdict en r15 sauvé, DEUX sites d'appel DIRECTS et STATIQUES — la variante 0xD080, LE SCELLÉ 0xC080 à son adresse d'origine, R7). L'ARRÊT D161 : 42/856/159 o mesurés → les slots minimums 0x40/0x380/0xC0 tassés à la contiguïté (fin de zone 0xD4C0 — la marge .text2 jusqu'à 0xDFFF demeure vierge). AUCUN bloc dans la carte : les ids g210001..003 sont PRÉFIGURÉS, la cérémonie appartient au développeur (charte § 3 du domaine).

**La vérification (verifier_shani_v150.py — 18 contrôles VERTS, la pièce preuves_v150/shani/rapport_verification.txt sha256 eca6b3e9f049f123…).** V1 : le round-trip 100 % (345 instructions keystone→capstone→keystone octet-identiques), le temps constant structurel (shani-02 zéro saut et tout accès à déplacement fixe ; les TROIS sauts de shani-03 chacun précédé de son test sur registre PUBLIC : r13 la longueur, rbp le complément, r15 le verdict CPU), la concordance au plan (les 20 déplacements RIP == le masque et les 16 groupes K ; les trois appels == 0xd000/0xd080/0xc080), l'héritage byte-identique (les notations tls13-01..04 ré-assemblées == les octets extraits du scellé loupe.exe). V2 : la sonde NATURELLE rend 0 sous Unicorn (le modèle qemu64 sans SHA — le repli vécu SANS forçage), les vecteurs FIPS, le corpus (120 tampons aux bords) et l'invariance de découpage au chemin scalaire, ET LE ROUTAGE NOMMÉ aux deux sens (le compteur d'instructions prouve que le verdict 0 exécute LE SCELLÉ — 4 compressions à 0xC080, 0 à la variante, la sonde UNE fois ; le verdict 1 FORCÉ — la sonde neutralisée en copie de laboratoire, le cache de traduction PURGÉ, la leçon de l'Entrée 157 rejouée — ROUTE à la variante et meurt DANS LE SLOT de shani-02 sur sha256rnds2 invalide sous qemu64). V3 : la sonde réelle rax = 1 RECROISÉE aux drapeaux /proc/cpuinfo (sha_ni ∧ ssse3) ; les QUATRE vecteurs dorés aux TROIS compositions (scellée ; variante dispatch réel → SHA-NI ; variante dispatch FORCÉ scalaire — « dispatch forcé dans les deux sens », l'exigence de l'instruction TENUE) ; l'égalité scalaire/SHA-NI sur 1 000 tampons aux longueurs aux bords (0, 1, 55, 56, 63, 64, 65, …, 65 537) — les trois condensats == hashlib ; l'invariance de découpage (un appel == 100×3 == 63/64/65/63/45) au chemin SHA-NI. V4 : la mesure. V5 : les QUATRE scellés INTACTS (sha256 identiques avant/après), le garde sceau-I 14/14. V6 : l'ORDRE de R11 (la mesure consignée avant la première notation — les heures des fichiers confrontées). TROIS DÉFAUTS D'INSTRUMENT du vérificateur lui-même attrapés et corrigés en route (l'écriture décalée de la carte native — tout accès unifié à base_img+rva ; le trampoline hand-derivé « 4C 89 D0 » qui était mov rax,r10 — ASSEMBLÉ PAR KEYSTONE depuis, jamais un octet gravé de tête ; le pas de 16 pour des gabarits de 21 — la cache servait une cible corrompue).

**La mesure avant/après (OPT-01).** 8 Mio de PRNG déterministe (graine 20261112:mesure), la même entrée aux deux bras, la même machine (le CPU SHA-NI du labo), le condensé VÉRIFIÉ à hashlib AVANT comptage et à CHAQUE répétition, les opérations COMPLÈTES init+absorb+final, 15 répétitions par bras, les médianes RDTSC (lfence+rdtsc) : **l'avant [la composition scellée tls13-01/03/04 — les octets que les onze runs ont vécus] 115 858 402 cycles = 13,811 cycles/o ; l'après [la variante, dispatch réel] 19 848 520 = 2,366 cycles/o ; LE GAIN 5,84× ; la surcharge du dispatch ±1 %** (le repli forcé == la composition scellée au bruit près : +0,15 % et −0,69 % aux deux courses — le prix de la sonde et de la branche est SOUS le seuil de bruit). La pièce : mesures_avant_apres.csv (sha256 4ca633c417e67049…).

**Le kit terrain.** shani/terrain/ : l'image image-shani.bin (48 Kio, plage RVA 0x2000-0xE000 — la table K DU SCELLÉ, le masque, la famille sha SCELLÉE extraite de loupe.exe à ses RVA d'origine [LE REPLI, R7], la variante assemblée ; sha256 df851b7c0041d700…), le scénario scenario-shani.py (BIFTEAU : sous Windows ctypes EST msx64 — appel direct ; sous POSIX le trampoline PRÉ-ASSEMBLÉ par keystone au labo, AUCUN outil exigé du terrain ; l'empreinte de l'image recoupée avant toute exécution), le LISEZMOI-KIT-SHNI.md (le geste du développeur en cinq minutes, la discipline de la mesure à la lettre de l'instruction, la lecture honnête du témoin — un processeur sans SHA rendra rax=0 et le témoin le dira : embarquer n'en vaudra pas la peine, c'est une réponse, pas un échec), le manifeste. Le DRY-RUN du laboratoire (l'instrument prouvé, PAS la mesure terrain) : temoin_dryrun_kit.txt — les vecteurs verts aux deux bras, 6,52× à charge différente (l'ordre de grandeur stable).

**Frontières.** Aucun artefact scellé touché (loupe.exe c1115105…, proxy.exe 446279f3…, demo.exe df8f2e50…, selftest.exe 8038585b… — recoupés AVANT et APRÈS, INTACTS) ; le garde sceau-I 14/14 VERT avant et après ; AUCUN scellement (la variante vit en copies de laboratoire, aucun bloc dans la carte, aucune balise — l'embarquement exigera la cérémonie d'ère du développeur) ; le run terrain de la mesure appartient au développeur (le kit livré, temoin-shani.txt attendu) ; aucun chiffre fabriqué — tout nombre est LU d'une pièce ou mesuré devant témoin ; les consignations antérieures non réécrites (append-only).
"""

WORKLOG = """

Task ID: 147
Agent: Z.ai (agent principal)
Task: LE PAQUET 6/6 DE LA VAGUE 3 (l'instruction lfh49a1xf) — LA VARIANTE
SHA-NI : le hot path mesuré d'abord (98,11 % — la mesure consignée AVANT),
les sémantiques épinglées par le code, la famille shani née
écrite-avant-code, le gain mesuré 5,84× au laboratoire, le vérificateur 18
contrôles VERTS, le kit terrain livré — JAMAIS SCELLÉE (D205, Entrée 240,
OPT-01).

Work Log:
- LA MESURE AVANT TOUT (R11) : le hachage de fichiers volumineux
  instrumenté DANS LE HARNAIS LOUPE (mesure_hotpath_shani.py) — tls13-02 =
  98,11 % des instructions exécutées (64/256 Kio, le profil stable, chaque
  condensé vérifié à hashlib avant verdict) ; la pièce consignée AVANT le
  premier octet de la variante (preuves_v150/hotpath_shani/, l'ordre
  constaté sur les heures des fichiers).
- LES SÉMANTIQUES ÉPINGLÉES PAR LE CODE : experience_semantique_shani.py
  (rnds2 : l'implicite en XMM0[63:0] — les sommes W+K —, EAU n'y est pour
  rien ; msg1/msg2 : les fenêtres, msg2 CHAÎNÉ) ; epreuve_compression_shani
  (MA structure à la main : 100/100 au juge Python, les QUATRE FIPS verts,
  le corpus aux bords vert — deux défauts de JUGE attrapés par la machine
  droite : la précédence ^/+ du Python, les faux messages 448/896).
- LA FAMILLE shani ÉCRITE-AVANT-CODE : la sonde (CPUID SHA ∧ SSSE3), la
  compression (LE contrat de tls13-02 — 16 phases déroulées, ZÉRO saut, K
  du scellé en seize groupes RIP, le masque @0x2800), l'absorbeur (LE
  contrat de tls13-03 — la sonde UNE fois par appel, les DEUX appels
  directs : 0xD080 la variante, 0xC080 LE SCELLÉ R7) ; l'ARRÊT D161
  (42/856/159 o → 0x40/0x380/0xC0) ; AUCUN bloc dans la carte (les ids
  préfigurés g210001..003 — la cérémonie au développeur).
- LA VÉRIFICATION (verifier_shani_v150.py, 18 VERTS) : round-trip 100 %
  (345 instructions), temps constant STRUCTUREL, concordance au plan (les
  20 RIP, les 3 appels), héritage byte-identique ; l'émulation (la sonde
  NATURELLE 0 sous qemu64, le routage NOMMÉ aux deux sens — le compteur
  prouve le scellé au verdict 0, le verdict 1 forcé meurt DANS LE SLOT de
  la variante) ; le natif (la sonde 1 recroisée /proc/cpuinfo, les QUATRE
  FIPS aux TROIS compositions, l'égalité sur 1 000 tampons aux bords,
  l'invariance) ; trois défauts d'instrument du vérificateur corrigés en
  route (l'accès unifié base_img+rva, le trampoline ASSEMBLÉ PAR KEYSTONE —
  « 4C 89 D0 » hand-derivé était mov rax,r10 —, le pas 32 des gabarits 21).
- LA MESURE : 8 Mio, la même entrée, le condensé vérifié avant ET pendant
  le comptage, les opérations COMPLÈTES, 15 répétitions : l'avant 115 858
  402 cycles (13,811/o) · l'après 19 848 520 (2,366/o) · LE GAIN 5,84× ·
  la surcharge du dispatch sous le bruit (+0,15 %/−0,69 % aux deux
  courses) ; le dry-run du kit : 6,52× à charge différente.
- LE KIT TERRAIN : image-shani.bin (48 Kio, sha256 df851b7c… — la K du
  scellé, le masque, la famille sha SCELLÉE [R7], la variante), le
  scénario bifteau sans outil, le LISEZMOI, le manifeste ; la mesure du
  développeur dans les conditions exactes de l'instruction — le témoin
  temoin-shani.txt attendu.
- Frontières : les QUATRE pièces scellées INTACTES (recoupées avant/après),
  garde sceau-I 14/14, AUCUN scellement (copies de laboratoire, aucune
  carte, aucune balise), le run terrain au développeur, aucun chiffre
  fabriqué, append-only.
- SUITE : la vague 3 est EXÉCUTÉE en ses six paquets (235→240) — au
  développeur : le témoin du kit SHA-NI, la cérémonie d'ère si la variante
  s'embarque, et la campagne de comparaison des workflows (le paquet 5,
  les bras T/C, le plan verrouillé D204).
"""


# --- L'APPEND VÉRIFIÉ (la fin attendue de chaque pièce) ----------------------------

def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str, marqueur_doublon: str, nouveau=False) -> None:
    if nouveau:
        if chemin.exists():
            sys.exit(f"[consigner] {nom} : existe déjà — création refusée")
        chemin.write_text(bloc, encoding="utf-8")
        print(f"[consigner] {nom} : CRÉÉ ({len(bloc)} o)")
        return
    texte = chemin.read_text(encoding="utf-8")
    if marqueur_doublon in texte:
        sys.exit(f"[consigner] {nom} : {marqueur_doublon} déjà présent — "
                 "rejeu refusé (append-only)")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 "dernière section — append refusé")
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} o)")


def main() -> int:
    # 1. LE JOURNAL D'OPTIMISATION NAÎT (OPT-01)
    append_verifie(REPO / "docs" / "JOURNAL_OPTIMISATION.md", "", JOURNAL_OPT,
                   "JOURNAL_OPTIMISATION.md", "## OPT-01", nouveau=True)

    # 2. D205 aux DÉCISIONS (append-only)
    fin_decisions = ("les consignations antérieures non réécrites "
                     "(append-only).")
    append_verifie(REPO / "docs" / "DECISIONS.md", fin_decisions, D205,
                   "DECISIONS.md (+D205)", "## D205 — LA VARIANTE SHA-NI")

    # 3. L'Entrée 240 au JOURNAL DE TRAVAIL (append-only)
    fin_journal = ("les consignations antérieures non réécrites "
                   "(append-only).")
    append_verifie(REPO / "docs" / "JOURNAL_TRAVAIL.md", fin_journal,
                   ENTREE240, "JOURNAL_TRAVAIL.md (+Entrée 240)",
                   "## Entrée 240 — LE PAQUET 6 DE LA VAGUE 3")

    # 4. LE WORKLOG Task 147 (append-only)
    fin_worklog = ("d'abord, l'optimisation refusée sinon).")
    append_verifie(REPO / "worklog.md", fin_worklog, WORKLOG,
                   "worklog.md (+Task 147)", "Task ID: 147")
    print("[consigner] LES QUATRE CONSIGNATIONS TENUES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
