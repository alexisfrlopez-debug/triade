#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_172.py — LA CONSIGNATION DU GESTE « LE CHANTIER M9-(b)
CONTINUE : LA FAMILLE x25519 NOTÉE-MESURÉE-PROUVÉE » : JOURNAL_TRAVAIL +Entrée
172 (ordre 171<172<marqueur, rejeu REFUSÉ), worklog +Task ID 90. Tout ancrage
absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 172 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE x25519 NOTÉE-MESURÉE-PROUVÉE — tls13-09..14 (f25519 addition, soustraction au verrou fail-closed, multiplication école 5×5, propagation+gel SANS BRANCHE, X25519 échelle de Montgomery RFC 7748 § 5, X25519 clé publique § 6.1) : la notation à la main (54/252/1078/281/2887/23 o, round-trip 100 %, les slots ARRÊTÉS 0x80/0x140/0x480/0x140/0xB80/0x40 tassés depuis 0xC980 — D161 rejoué), LES FIXTURES .text6 ARRÊTÉS (U9 @0xFF00, EXP_INV @0xFF20 — l'ARRÊT D95, la réserve .rdata M8 épuisée par K[64]), LE HARNAIS 46 contrôles · 46 VERTS × 3 graines (RFC 7748 § 5.2 + § 6.1 + LE TEST ITÉRÉ 1/1000 + LE TRANSFERT RFC 8448, la falsification attrapée, le temps constant MESURÉ 1 238 953 instructions EXACTEMENT) ; DEUX DÉFAUTS DE NOTATION nommés par le fail-closed (l'école : mul détruit rax ; l'échelle : le geste x2' lisait A au lieu d'AA, le cswap écrasait le bit du drapeau) ; DEUX ERRATA d'arithmétique des specs consignés AVANT la notation (07/11)

**La reprise SUR LES TROIS MIROIRS (D164 rejouée — la demande du développeur : « on reprend ce projet… vérifie si la synchro entre le git et le drive est ok, puis on continue les derniers chantiers », puis « on enchaine »).** La vérification LECTURE SEULE par script (scripts/verify_sync_m9b2.py du labo, 10 VERTS / 0 ROUGES) : le bundle courant triade-history-090-544b51a.bundle AU MIROIR TRIADE-sauvegarde-git/ relu md5 22eb71d9… == le consigné du worklog Task 89 == le bundle local (17 256 962 o, l'unique courant), archives-bundles/ relues : 33 archives (l'ancien 090-c82fe7b md5 5ca58429… présent — rien supprimé), /test sans copie de bundle (recoupé), GitHub interrogé par ls-remote : bundle051/v0.5.1-jalon-v7 == 544b51a — LA POINTE DU GESTE hkdf consignée par la passation (le commit de passation de68778 du Task 89 EMBARQUÉ au présent geste, le flux établi), le jeton OAuth relais rafraîchi vivant. La réserve instrumentale D149 re-vérifiée AVANT usage : le disque labo recyclé avait emporté keystone/capstone/unicorn/pefile/pynacl — RÉINSTALLÉS PAR PROCÉDURE. Les « modifications » m8/ du git status : DES BITS DE PERMISSION SEULS (100644→100755, 241 fichiers, 0 insertion/0 suppression — l'artefact du bac à sable recyclé, core.fileMode false local, AUCUN contenu) ; proxy.exe relu sha256 1492b0bc…b0cd4 INTACT.

**L'arbre scellé INTACT (la frontière première du geste) et LES DEUX ERRATA d'arithmétique consignés AVANT la notation (le modèle M9 : tls13-08 au geste hkdf, la spec elle-même l'exigeait — « le miroir ne les COPIE PAS, il les re-dérive — le juge est le code »).** LA DÉRIVATION PAR CODE d'abord (scripts/derive_x25519.py — TOUT VERT, le juge est le code) : (1) ERRATUM tls13-10 I1 : « 2p = 2^256 − 38 en radix 2^51 : (2^51 − 38) puis (2^51 − 1)×4 » — les membres ÉCRITS composent 2^255 − 38 ≡ −19 (mod p) ≠ 2p : la VRAIE décomposition est (2^51 − 38), (2^51 − 1)×3, (2^52 − 1) [le membre 4 = 0xFFFFFFFFFFFFF — un membre de 52 bits, l'invariant le permet], Σ membres·2^51i == 2·p PROUVÉ PAR CODE, la preuve sans-emprunt a + 2p ≥ 2p > b SAUVEE (2p = 2^256−38 > 2^255 > b lâche) ; la notation re-dérive (F25519_P2_MEMBRES posé au plan d'adressage, la source unique — l'écriture seule est fautive, jamais le contrat). (2) ERRATUM tls13-13 I5 : « entre 4 et 6 opérations par itération d'échelle » — la recette RFC 7748 § 5 (I2, NORMATIVE) exige 4 add + 4 sub + 10 mul = 18 appels PAR ITÉRATION (A, B, AA, BB, E, C, D, DA, CB, x3'², (DA−CB)², z3' [×2], x2', AE, AA+AE, z2' — le compte par code) ; la seconde moitié de I5 est correcte (l'inversion « entre 255 et 510 » : 255 carrés + 253 multiplications = 508 — p−2 porte 253 uns). Le décodage 32 o → membres (les décalages 0/13/38/25/12, le miroir inversé d'av-05) et l'encodage (la mini-passe de retenues puis les QUATRE quads — le retour ×19 du membre 4 IMPOSSIBLE : la valeur < p, le théorème) prouvés sur 700 vecteurs par le même script.

**La notation (les six brouillons msx64 → les six notations explicites WYSIWYG).** tls13-09 (h100009, addition réduite) 54 o · 15 instructions — CINQ additions membres à membres IN PLACE (la sortie ÉCRASE a, miroir av-07 Q2), la somme < 2^53 ne déborde jamais l'u64 (la représentation exacte), UNE passe TLS12, 0 push + sub 0x28 (l'ombre + l'alignement). tls13-10 (h100010, soustraction réduite) 252 o · 54 instructions — les CINQ membres de 2p EN IMMÉDIATS re-dérivés du plan (movabs imm64 — la convention des aînés), DEUX passes : a + 2p vers le SCRATCH de pile (chaque somme < 2^53, AUCUNE retenue — l'ordre n'importe pas) puis la chaîne sub/sbb CONTRE b (l'emprunt voyage en CF, les mov intercalés sont muets), LE VERROU fail-closed : jc → rax = −1 NOMMÉ et la sortie a JAMAIS écrite (le scratch meurt) — l'échec E1 d'av-08 ÉLEVÉ en verdict de la table du domaine. tls13-11 (h100011, multiplication) 1078 o · 230 instructions — L'ÉCOLE 5×5 DÉROULÉE (25 produits), les DIX logements u128 sur la pile (sous-cadre 0xC0 = 160 o de logements + 32 o d'ombre — le DIXIÈME reste NUL, il porte le REPLI UNIFORME : C[4] = T[4] + 19·T[9] avec T[9] vide), l'emprunt sortant d'un logement IMPOSSIBLE (< 5·2^104 < 2^107, la marge 2^21), LE REPLI ×19 en DEUX morceaux (mul r8 le bas AVEC sa retenue, imul le haut — la marge < 2^48 ferme la question), l'extraction : le sommet c = C4 >> 51 (shrd, le u128) vers C0 ×19, la chaîne r0..r3 avec reports 51 bits, r4 = (C4&M51) + c3 masqué, LE RETOUR FINAL r0 += 19·(r4 >> 51) (r0 < 2^51 + 19·2^12 < 2^52, la borne d'entrée 2^57 de TLS12 respire), rbx retenu (le pointeur b survit aux mul qui détruisent rdx:rax). tls13-12 (h100012, propagation + gel) 281 o · 80 instructions — le bloc FEUILLE FUSIONNÉ (UNE frontière d'appel pour les DEUX miroirs M7 av-06 + av-10 — LA DIVERGENCE NOMMÉE de la découpe M9) : la passe SÉQUENTIELLE 0→4 (le membre i masqué AVANT que le i+1 ne reçoive sa retenue, le débordement du cinquième REVIENT au premier ×19) puis LE GEL SANS BRANCHE DE DONNÉES (L'AMÉLIORATION NOMMÉE : le M7 branchait jb/ja, le M9 SÉLECTIONNE) — les membres 1..4 post-passe sont ≤ 2^51−1 : la comparaison membre à membre du cinquième au premier REDUIT À L'ÉGALITÉ avec le membre de p (le dépassement strict y est IMPOSSIBLE, l'écriture de la spec le disait déjà), le drapeau « ≥ p » produit en registre SANS ÉCRIRE (le OU des XOR), le masque 0/−1 DIFFUSÉ PAR SAR, la soustraction conditionnelle PAR ET LOGIQUE — l'entrée OCTET-IDENTIQUE si < p, ZÉRO si elle valait exactement p. tls13-13 (h100013, X25519 l'échelle de Montgomery) 2887 o · 459 instructions — le sous-cadre RÉEL 0x210 (la spec écrit « ≈ 0x300 » : la mesure s'incline, la consignation porte le nombre ; x1/x2/z2/x3/z3/a24 @+0x20..0x10F, S1..S4 @+0x110..0x1AF, le scalaire clampé @+0x1B0, le point u masqué @+0x1D0, l'exposant @+0x1F0), le clamp RFC 7748 dans la COPIE LOCALE (octet 0 &= 248, octet 31 &= 127 |= 64 — une opération PUBLIQUE sur la clé, I1/P2), le bit 255 du point u MASQUÉ dans la copie (P3 — les valeurs non canoniques ≡ réduites par l'arithmétique lâche même), le décodage membres (le miroir win d'av-05), LE CSWAP XOR MASQUÉ membre à membre (dix membres, le masque 0/−1 diffusé du drapeau par sar — RFC 7748 § 5 EXIGE le temps constant), LA RECETTE § 5 À CHAQUE ITÉRATION (18 appels : 4 add + 4 sub + 10 mul — l'erratum I5 consigné, le compte par code), AA à TROIS consommateurs destructifs (x2' le produit, E la différence, AA+AE le sommet : l'original S3 pour E, la copie x2 pour le produit, la copie S4 pour le sommet), l'inversion z2^(p−2) par carré-et-multiplie GAUCHE→DROITE sur l'exposant FIXE copié du FIXTURE R_EXP_INV (255 itérations bornées, LA BRANCHE DU BIT porte sur l'EXPOSANT PUBLIC — jamais un secret), la mini-passe de retenues puis les QUATRE quads (les décalages 51/13/38-26/25-39/12 en miroir du décodage), les non-volatils rdi/rbx/rbp retenus par 3 pushes (≡ 0 mod 16 aux appels). tls13-14 (h100014, X25519 clé publique) 23 o · 6 instructions — LE PASSE-PLAT DU COUPLE : rcx et rdx traversent, r8 désigne le FIXTURE U9 (le point de base u = 9 : la DONNÉE PUBLIQUE du plan d'adressage, JAMAIS un octet de code — I1), UNE composition TLS13.

**L'ARRÊT des slots (D161 rejoué — la mesure auteur décide, la préfiguration s'incline DEUX FOIS).** Le MINIMUM admissible par longueur (multiple de 64, padding ≥ 16, tassés depuis la fin hkdf 0xC980) : tls13-09 @0xC980 (slot 0x80, padding 74) · tls13-10 @0xCA00 (0x140, 68) · tls13-11 @0xCB40 (0x480, 74) · tls13-12 @0xCFC0 (0x140, 39) · tls13-13 @0xD100 (0xB80, 57) · tls13-14 @0xDC80 (0x40, 41) — **fin de la famille x25519 à 0xDCC0**. Les ré-arrêts en cours de geste : tls13-11 préfiguré 0x400 mesuré 1078 o → 0x480 (la chaîne décalée), tls13-13 préfiguré 0xA00 mesuré 2815 puis 2855 puis 2880 puis 2887 o (les corrections du fail-closed) → 0xB80 — chaque fois le plan ré-arrêté SUR LA MESURE, la préfiguration s'incline. **LES FIXTURES .text6 (l'ARRÊT nommé, miroir D95)** : la réserve .rdata M8 (R_K 0x2F00, 256 o) est ÉPUISÉE par K[64] (le constat du geste sha : « le prochain fixture du domaine vivra en .text6 ») — les fixtures NOUVEAUX vivent en .text6 AU-DELÀ du plancher de croissance des familles (la marge : la famille finit à 0xDCC0, les quatre familles restantes tiennent sous 0xF000, la mesure décidera) : **R_U9 = 0xFF00** (le point de base u = 9 sérialisé LE, X25519_BASE du plan) et **R_EXP_INV = 0xFF20** (l'exposant p−2 sérialisé LE, X25519_EXP_INV — le miroir d'av-11 qui le tenait en .rodata), les CONTENUS re-dérivés par arithmétique (V0.c : (9).to_bytes LE et (p−2).to_bytes LE, JAMAIS une copie d'écriture), les symboles U9/EXP_INV posés à l'auteur (les SEULS déplacements RIP du domaine hors l'ancêtre K).

**Le harnais (tls13/harnais_x25519.py — le modèle harnais_hkdf : l'émulation nue à les RVA du plan, les QUATORZE blocs posés, l'appelant factice msx64 aux sentinelles et canaris, L'INSTRUMENT PERMANENT posé à la naissance — et le mode « nue » SANS hook pour les boucles de vecteurs longues : mille pas ne se comptent pas, ils se vérifient, V6 compte quatre).** 46 contrôles · 46 VERTS × 3 graines (20261107, 41, 20261108) : V0 les pièces (le scellé 0.9.0 relu 44 544 o sha256 1492b0bc…, les familles sha ET hkdf INTACTES re-round-tripées aux longueurs arrêtées 74/387/139/165 + 435/151/347/310, LES FIXTURES posés et re-dérivés, l'arbre I scellé relu VERT — verifier_specs_m9a rejoué) ; V1 le round-trip 100 % (keystone == capstone, 15/54/230/80/459/6 instructions, les tailles == l'ARRÊT 54/252/1078/281/2887/23) + les concordances au plan (les appels de 09/10/11 == TLS12 ; de 13 == TLS09×4 + TLS10×4 + TLS11×13 — LA RECETTE COMPTÉE PAR CODE : 4+4+10 par itération + 2 l'inversion + 1 le produit final, l'erratum I5 consigné dans le verdict même ; de 14 == TLS13 ; les membres de 2p de 10 == F25519_P2_MEMBRES ; M51/P0/19 de 12 ; a24 = 121665 = (486662−2)/4 et le clamp et les 255 bornées de 13) + la structure (AUCUN syscall, AUCUN appel indirect, les déplacements RIP UNIQUEMENT aux DEUX fixtures : 4 lectures d'EXP_INV par 13 + 1 lea de U9 par 14 — les cibles re-dérivées des désassemblages) + le temps constant STRUCTUREL (09/11/12 ZÉRO saut conditionnel — le flot arithmétique est SANS BRANCHE ; 10 exactement UN : le verrou d'emprunt fail-closed, le CONTRAT jamais un secret ; 13 exactement TROIS : les deux compteurs de boucle + le bit de l'EXPOSANT PUBLIC p−2, chacun sur drapeau de REGISTRE — le scalaire ne touche JAMAIS une branche) ; V2 les vecteurs officiels RFC 7748 : les DEUX paires du § 5.2 OCTET POUR OCTET (la référence Python croisée AVANT de juger — l'instrument se contrôle), la paire du § 6.1 (les clés publiques d'Alice ET de Bob rendues par LE COUPLE tls13-14 au point 9, LE SECRET PARTAGÉ calculé des DEUX côtés — Alice × publique de Bob == Bob × publique d'Alice == K : la commutativité prouvée sur pièces), **LE TEST ITÉRÉ** (l'entrée 9 itérée : après 1 pas 422c8e7a…, après 1000 pas 684cf59b… — la seconde espèce du § 5.2, mille pas vérifiés sur l'émulation nue) + l'oracle différentiel (60 échelles aléatoires — scalaire ET point aléatoires, le bit 255 et les non-canoniques exercés ; 1600 opérations de champ : 400 couronnes de add/sub/mul/gel contre Python) ; V3 les cas punitifs (le gel : p → 0 EXACT, p−1 OCTET-IDENTIQUE, la passe préserve la valeur sur 100 formes lâches post-producteur ; LES LÂCHES DE L'ÉCOLE : 0·x, 1·x, (p−1)², le carré, les membres saturés 2^52−1 partout, a lâche ≥ p, a = b = 2^255−1 ; la soustraction lâche : a ∈ {p+2026, p, 2^255−38, 2^255−1, 0} — les DEUX bornes de P1 démontrées ; le point u NON CANONIQUE : les valeurs [p, 2^255) traitées comme réduites, le bit 255 masqué AVANT le décodage ; les dégénérés : u ∈ {0, 1, 2, 3, 8} de petit ordre → la sortie nulle, l'inversion 0^(p−2) = 0 par la composition même) ; V4 le contrat (les 8 non-volatiles rendus, la pile équilibrée, l'ombre et les logements intacts, la zone profonde intacte — la chaîne 13 → 11 → 12 ≈ 0x2F0 sous l'entrée ; **L'ALIGNEMENT msx64 à 20 398 entrées de callee** (TLS09 ×2040, TLS10 ×2040, TLS11 ×6118, TLS12 ×10198, TLS13 ×2 — les comptes EXACTS de la recette sur deux compositions), rsp ≡ 8 mod 16 chacune ; les entrées INTACTES — le scalaire, le point u, la clé privée relus octet pour octet, le clamp et le masque vivent dans les copies locales ; la sortie JAMAIS dépassée — les canaris après les 32 o intacts ; **LE VERROU fail-closed de 10 EXERCÉ HORS CONTRAT** : b = 2p+1000 (a + 2p − b = −1000 < 0) → l'emprunt sort au cinquième membre, rax = −1 NOMMÉ, la sortie a INTACTE — le fail-closed se prononce, il ne se tait jamais) ; V5 la falsification, ZÉRO SILENCE (6/6 mutations du scalaire ET du point attrapées — NOTE DE DISCIPLINE consignée : les trois bits bas du scalaire sont CLAMPÉS par RFC 7748, la mutation du bit 0 est un no-op PAR DESIGN, la falsification vise le bit 3, le plus bas NON clampé ; 3/3 de la clé privée → la clé publique diverge ; la comparaison non muette 3/3 ; **LES FIXTURES CORROMPUS → divergence** : U9 muté @0xFF00 → le couple diverge, EXP_INV muté @0xFF20 → le partage diverge — les données du plan sont LUES à travers la composition) ; V6 le temps constant MESURÉ (le SCALAIRE : 4 couronnes aléatoires, **1 238 953 instructions EXACTEMENT** ; le POINT u : 2 points (9 et la publique de Bob), LE MÊME COMPTE — le cswap masqué ne compte pas les différences ; add 95, sub 131, mul 310 instructions EXACTEMENT — le contenu JAMAIS, la longueur seule).

**LES DEUX DÉFAUTS DE NOTATION nommés par le fail-closed (la preuve corrige la notation — ENCORE : le geste hkdf avait ouvert la voie, celui-ci la confirme en statue).** (1) **tls13-11 L'ÉCOLE : mul DÉTRUIT rax** (rdx:rax = rax·[rbx+8j] — le produit ÉCRASE l'opérande) : le second mul de chaque rangée multipliait le DEMI-PRODUIT du premier au lieu de a_i — la BISECTION l'a nommé sur pièces contrôlées (a0×b1 → 0 : tous les produits de j ≥ 1 morts ; les vecteurs à opérande b0 seul passaient à travers — le piège des tests qui ne regardent pas assez) : CORRIGÉ par le RECHARGEMENT de a_i AVANT CHAQUE mul (le brouillon le documente : « le rechargement est LE geste de l'école »), re-mesuré 1002 → 1078 o, le slot ré-arrêté 0x400 → 0x480, la chaîne décalée (12 → 0xCFC0, 13 → 0xD100, 14 → 0xDC80). (2) **tls13-13 L'ÉCHELLE, DEUX fautes nommées par LA TRACE ITÉRATIVE** (le hook au sommet de .boucle contre la référence Python : l'état (x2, z2, x3, z3) comparé à CHAQUE pas — la première faute sortait à t = 252, la branche x2/z2 SEULE fautive) : (a) le geste x2' = AA·BB lisait x2 (qui tient encore A, MORT depuis DA) au lieu de la COPIE d'AA, et le sommet AA+AE manquait son instance — AA a TROIS consommateurs destructifs (x2' le produit, E la différence, AA+AE le sommet) : l'original S3 sert E, la copie x2 sert le produit, la copie S4 sert le sommet ; (b) `mov ebp, eax` lisait le bit k_t APRÈS que le cswap n'ait écrasé rax (rax est le SCRATCH du cswap — le drapeau swap = k_t recevait le déchet du dernier XOR masqué, la itérations suivantes permutaient au HASARD DU DÉTRITUS) : le bit PRÉSERVÉ en r11d AVANT le cswap, relu après. Re-mesuré 2815 → 2855 → 2880 → 2887 o (les corrections), ré-arrêté 0xB40 → 0xB80, REJOUÉ : 46/46 VERTS. Les défauts d'INSTRUMENT du harnais nommés et corrigés au geste : la convention movabs (14 imm64 — la convention des aînés tls13-05/07), la longueur arrêtée périmée (2884 → 2887 : la mesure d'après movabs), la formule des comptes d'alignement (les DEUX compositions), le verrou V4.e d'abord testé à l'ÉGALITÉ b = 2p (la soustraction exacte est LÉGALE — aucun emprunt : b = 2p+1000 l'exerce VRAIMENT), les mutations V5 du bit 0 du scalaire (absorbées par le clamp PAR DESIGN — le bit 3 vise ce que le protocole UTILISE, la note de discipline consignée dans le harnais même), la corruption des fixtures sur la MÊME instance que l'exécution (les DEUX émulations ont des mémoires DISTINCTES par construction — la discipline le consigne).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN build (le chantier (e) attend son geste — le garde est VERT), l'arbre scellé tls13/I INTACT (le sceau relu VERT au harnais V0 APRÈS le geste — R2 tenue : les errata vivent au journal, jamais dans l'arbre), m8/proxy.exe INTACT (1492b0bc…, relu en V0.a), les familles sha et hkdf intactes (relues aux longueurs arrêtées en V0.b), AUCUNE règle modifiée, la charte § 2 tenue (les vecteurs officiels AVANT usage — la référence croisée, la falsification), la charte § 3 tenue (le temps constant NOMMÉ par bloc et MESURÉ). Livrables : tls13/layout.py (la famille x25519 ARRÊTÉE + F25519_P2_MEMBRES/F25519_P0 re-dérivés + LES FIXTURES R_U9/R_EXP_INV + les adresses A_ADD..A_CLE_PUBLIQUE), tls13/outils/auteur.py (les 14 blocs, les symboles U9/EXP_INV), tls13/notation/ (6 brouillons + 6 notations explicites), tls13/harnais_x25519.py (46 contrôles VERTS × 3 graines) ; consignations : la présente Entrée PAR SCRIPT, PLAN (chantier (b) : la famille x25519 + État du programme), worklog +Task ID 90.

- SUITE : LE CHANTIER M9-(b) CONTINUE — la famille aead (tls13-15..19 : SP 800-38A/38D, l'arrêt AES-NI, GHASH sans table par donnée, le tag VÉRIFIÉ avant restitution, AUCUNE brique d'inversion — le fixture GCM_R du plan), les slots à la suite de 0xDCC0 ; puis (c) l'enregistrement + la poignée au harnais RFC 8448, (d) le socle socket sys-04+, (e) LA CÉRÉMONIE DE L'ÈRE + le build 1.0.0-dev.1, (f) le terrain — LA GRANDE ŒUVRE.

"""

TASK = """

## Task ID 90 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE x25519 NOTÉE-MESURÉE-PROUVÉE (07/11)

- LA SYNCHRO VÉRIFIÉE SUR LES TROIS MIROIRS (la demande du développeur :
  « vérifie si la synchro… puis on continue ») : le bundle 090-544b51a au
  miroir md5 22eb71d9… == consigné == local, 33 archives (l'ancien
  090-c82fe7b présent), /test sans copie, GitHub == 544b51a (la pointe hkdf),
  le jeton OAuth vivant ; la réserve instrumentale réinstallée (keystone/
  capstone/unicorn/pefile/pynacl — le disque recyclé les avait emportés) ;
  les « modifications » m8/ : des bits de permission seuls (core.fileMode
  false, AUCUN contenu — proxy.exe relu INTACT 1492b0bc…).
- LE GESTE : tls13-09..14 — f25519 addition (cinq membres in place, UNE
  passe), soustraction (les membres de 2p RE-DÉRIVÉS par arithmétique, DEUX
  passes a+2p au scratch puis sub/sbb, LE VERROU fail-closed rax = −1 NOMMÉ,
  RIEN écrit), multiplication (l'école 5×5 déroulée aux DIX logements u128
  [le dixième NUL porte le repli uniforme], le repli ×19 en deux morceaux,
  la chaîne 51 bits et le retour final), LE GARDIEN FUSIONNÉ propagation+gel
  SANS BRANCHE (le drapeau « ≥ p » en registre sans écrire, le masque 0/−1
  par sar, la soustraction conditionnelle par ET logique — l'amélioration
  nommée sur av-10 : le M7 branchait, le M9 sélectionne), l'échelle de
  Montgomery RFC 7748 § 5 (le clamp dans la copie locale, le bit 255 masqué,
  le cswap XOR MASQUÉ, LA RECETTE 18 appels par itération [4 add + 4 sub +
  10 mul — l'erratum I5 consigné], l'inversion z2^(p−2) à l'exposant PUBLIC
  du FIXTURE, la sérialisation en miroir d'av-05) et le couple du
  ClientHello (le point 9 au FIXTURE U9 — jamais un octet de code) — notés
  (54/252/1078/281/2887/23 o, round-trip 100 %), mesurés (les slots ARRÊTÉS
  0x80/0x140/0x480/0x140/0xB80/0x40 tassés depuis 0xC980, fin 0xDCC0 — D161
  rejoué, la préfiguration inclinée DEUX FOIS), prouvés (LE HARNAIS 46
  contrôles · 46 VERTS × 3 graines).
- LES FIXTURES .text6 ARRÊTÉS (miroir D95) : la réserve .rdata M8 ÉPUISÉE
  par K[64] — R_U9 = 0xFF00 (le point 9 LE) et R_EXP_INV = 0xFF20 (p−2 LE),
  les contenus re-dérivés par arithmétique (V0.c), JAMAIS copiés.
- LES PREUVES : RFC 7748 § 5.2 (les DEUX paires octet pour octet, la
  référence croisée avant de juger) + § 6.1 (les clés publiques par le
  couple, LE SECRET PARTAGÉ des DEUX côtés — la commutativité) + LE TEST
  ITÉRÉ (1 pas : 422c8e7a…, 1000 pas : 684cf59b…) + LE TRANSFERT RFC 8448
  (le key_share du ClientHello 99381de5… et le shared 8bd4054f… du
  transcript, octet pour octet) ; l'oracle différentiel 60 échelles + 1600
  opérations de champ ; les punitifs (p → 0 EXACT, les lâches, les
  saturés, les non-canoniques, les dégénérés → 0) ; le contrat (20 398
  entrées de callee alignées ≡ 8 mod 16 — les comptes EXACTS de la
  recette ; le verrou −1 exercé hors contrat, la sortie INTACTE) ; la
  falsification (6/6 + 3/3, les fixtures corrompus → divergence : les
  données du plan sont LUES) ; le temps constant MESURÉ (1 238 953
  instructions EXACTEMENT — le scalaire et le point JAMAIS comptés).
- LES DEUX ERRATA consignés AVANT la notation (le juge est le code) :
  tls13-10 I1 (les membres de 2p : « (2^51−38) puis (2^51−1)×4 » compose
  2^255−38 ≡ −19 — le membre 4 est 2^52−1) ; tls13-13 I5 (« entre 4 et 6
  opérations » : la recette § 5 exige 4+4+10 = 18).
- LES DEUX DÉFAUTS DE NOTATION nommés par le fail-closed : l'école — mul
  DÉTRUIT rax, le second mul de chaque rangée multipliait le demi-produit
  (la bisection : a0×b1 → 0) : a_i RECHARGÉ avant CHAQUE mul, re-mesuré
  1002 → 1078, slot 0x400 → 0x480 ; l'échelle — x2' lisait A au lieu de la
  copie d'AA [trois consommateurs destructifs] et le cswap ÉCRASAIT le bit
  du drapeau (rax est le scratch : k_t préservé en r11d) — nommés par LA
  TRACE ITÉRATIVE (l'état comparé à chaque pas contre Python, la première
  faute à t = 252), re-mesuré 2887, slot 0xB80, REJOUÉ VERT.
- FRONTIÈRES : aucune balise, AUCUN build, l'arbre scellé tls13/I INTACT
  (verifier_specs_m9a relu VERT au harnais V0), m8/proxy.exe INTACT, les
  familles sha et hkdf intactes (relues en V0.b) ; consignations : Entrée
  172 PAR SCRIPT, PLAN (chantier (b) : la famille x25519 + État du
  programme), worklog +Task ID 90.
- SUITE : la famille aead (tls13-15..19 — les slots à la suite de 0xDCC0),
  puis (c) RFC 8448, (d) sys-04+, (e) LA CÉRÉMONIE + le build 1.0.0-dev.1,
  (f) le terrain.

Stage Summary:
- LA TROISIÈME FAMILLE de la grande œuvre est notée-mesurée-prouvée :
  l'arithmétique du corps F(2^255−19) et L'ÉCHANGE DE CLÉS X25519 existent
  en octets — le couple du ClientHello (la clé publique) et le secret
  partagé du transcript officiel RFC 8448 rendus octet pour octet, le
  temps constant MESURÉ à l'instruction près.
- LA PREUVE A CORRIGÉ LA NOTATION, ENCORE : les deux défauts (mul détruit
  rax ; le cswap écrasait le bit du drapeau) nommés par la bisection et la
  trace itérative, corrigés et rejoués verts — le fail-closed est la
  méthode, pas l'accident.
"""


def inserer():
    j = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 172 —" in j:
        print("[inserer-172] REJEU REFUSÉ : l'Entrée 172 existe déjà.")
        return 1
    n = j.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-172] ÉCHEC : marqueur {n} fois dans le journal.")
        return 1
    if "## Entrée 171 —" not in j:
        print("[inserer-172] ÉCHEC : l'Entrée 171 est absente (ordre 171<172).")
        return 1
    j = j.replace(MARQUEUR, ENTREE + MARQUEUR)
    JOURNAL.write_text(j, encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 90 —" in w:
        print("[inserer-172] REJEU REFUSÉ : le Task ID 90 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-172] PASSÉ : Entrée 172 insérée avant le marqueur ; worklog +Task ID 90.")
    return 0


if __name__ == "__main__":
    sys.exit(inserer())
