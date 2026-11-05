#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_173.py — LA CONSIGNATION DU GESTE « LE CHANTIER M9-(b)
CONTINUE : LA FAMILLE aead NOTÉE-MESURÉE-PROUVÉE » : JOURNAL_TRAVAIL +Entrée
173 (ordre 172<173<marqueur, rejeu REFUSÉ), worklog +Task ID 91. Tout ancrage
absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 173 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE aead NOTÉE-MESURÉE-PROUVÉE — tls13-15..19 (AES-128 le déploiement des clés de tour, AES-128 le chiffrement d'un bloc, GHASH la multiplication GF(2^128), GCM sceller, GCM ouvrir — FIPS 197, SP 800-38A F.1.1, SP 800-38D § 6.3/§ 7.1, RFC 8446 § 5.2/§ 5.3) : la notation à la main (520/129/162/1076/1163 o, round-trip 100 %, les slots ARRÊTÉS 0x240/0xC0/0xC0/0x480/0x4C0 tassés depuis 0xDCC0 — fin de famille 0xE9C0, D161 rejoué), LE HARNAIS 49 contrôles · 49 VERTS × 3 graines (FIPS 197 C.1 + SP 800-38A F.1.1 + McGrew–Viega TC1..TC4 + LE TRANSFERT RFC 8448 des SEPT enregistrements ouverts ET rescellés octet pour octet, la falsification octet par octet, le verdict TEMPS CONSTANT mesuré) ; DEUX DÉFAUTS DE NOTATION nommés par la sonde du geste (la représentation GHASH ; le J0 terminal boutiste) (07/11)

**La reprise SUR LES TROIS MIROIRS (D164 rejouée — la demande du développeur : « vérifie si la synchro entre le git et le drive est ok, puis on continue les derniers chantiers », puis « on enchaine », puis « continue »).** La vérification LECTURE SEULE par script (scripts/verify_sync_m9d.py du labo, 22 VERTS / 0 ROUGES) : HEAD == 8b7b8e9 (la passation Task 90), le worklog porte la passation D141 consignée, le miroir TRIADE-sauvegarde-git/ porte les FICHIERS de la passation md5 MATCH (worklog.md, scripts/passe_bundle_m9c.py, JOURNAL, les notations x25519-13/14, le harnais — le hook post-commit a fait son geste), le bundle courant triade-history-090-06c2f4d.bundle UNIQUE au miroir, archives-bundles/ relues : 34 archives (l'ancien 090-544b51a versionné — rien supprimé), /test sans copie de bundle (recoupé), GitHub interrogé par ls-remote : bundle051/v0.5.1-jalon-v7 == 06c2f4d — LA POINTE DU GESTE x25519 (le commit de passation 8b7b8e9 EMBARQUÉ au geste présent, le flux établi), le jeton OAuth relais rafraîchi vivant ; les CINQ notations aead NON committées correctement ABSENTES du miroir (le geste présent les porte). La réserve instrumentale D149 re-vérifiée AVANT usage : keystone 0.9.2/capstone/unicorn présents, pynacl+pefile déjà au venv (l'import est « nacl » — la faute d'instrument nommée et pardonnée). L'ÉTAT DU GESTE TROUVÉ EN COURS : les cinq brouillons ET les cinq notations explicites posés, layout.py (les slots arrêtés) et auteur.py (les descriptions) modifiés — la notation était FAITE, la PREUVE pas encore : le geste a continué de la sonde.

**LA DÉRIVATION PAR CODE rejouée d'abord (scripts/derive_aead.py du labo — TOUT VERT, le juge est le code).** La référence Python : AES-128 pur FIPS 197 (la S-box DÉRIVÉE de l'arithmétique GF(2^8) — l'inversion puis la transformation affine § 5.1.1, JAMAIS une table copiée ; les Rcon dérivés de x^i), GHASH SP 800-38D § 6.3 (la marche de l'algorithme 1 MOT POUR MOT), GCM § 7.1 (J0 à 96 bits, inc32, le bloc de longueurs). LES VECTEURS OFFICIELS : FIPS 197 C.1 (69c4e0d8…), SP 800-38A F.1.1 (les QUATRE blocs), McGrew–Viega TC1..TC6 (les Test Cases de la spec gcm — chiffré, étiquette ET ouverture), ET LE TRANSFERT RFC 8448 : le texte officiel PARSÉ (les paires payload/enregistrement du § 3, le saut de page du bloc de 679 o franchi jamais avalé), les SEPT enregistrements chiffrés reconstruits octet pour octet par la référence (le vol serveur 679 o, le Finished client 58 o, le NewSessionTicket 227 o, les applicatives 72 o ×2, les close_notify 24 o ×2). LA SONDE AES-NI : les sémantiques d'AESKEYGENASSIST/AESENC/AESENCLAST LUES sur l'émulation AVANT la notation (la disposition DÉRIVÉE DE L'OBSERVATION : le mot d'AES-128 = RotWord∘SubWord(w3) ⊕ Rcon au DWORD 3 → pshufd 0xFF — les candidats de mémoire étaient FAUX tous les deux, la disposition réelle sert AUSSI w1, le secours d'AES-192/256), LA COMPOSITION pxor + 9×AESENC + AESENCLAST == FIPS 197 C.1 sur l'émulateur, la séquence préfixe-XOR ⊕ t CONTRE-PROUVÉE sur C.1. Les contre-preuves d'arithmétique : P4 (N ≤ 2^14 → 1024 blocs → le compteur u32 loin du rendement), les longueurs en bits ≤ 2^17 < 2^64, R = 0xE1||0^120 ET sa lecture par voies, le GHASH (le premier bit de X = le MSB de l'octet 0, le sortant = le bit 0 de l'octet 15), J0 = nonce||00000001.

**La notation (les cinq brouillons msx64 → les cinq notations explicites WYSIWYG — trouvées posées au geste précédent, CORRIGÉES au présent par la sonde).** tls13-15 (h100015, le déploiement des clés de tour) 520 o · 114 instructions — L'ARRÊT AES-NI (I3 : la transcription par l'instruction MATÉRIELLE, aucune table logicielle indexée par la clé — la faille que la charte § 3 interdit), AESKEYGENASSIST le SubWord/RotWord matériel, pshufd 0xFF la diffusion du mot d'AES-128 (le dword 3), la recette préfixe-XOR ⊕ t (w[i−4] ⊕ w[i−3] ⊕ w[i−2] ⊕ (w[i−1] ⊕ t) — la composition des XOR, contre-prouvée sur C.1), les DIX Rcon en IMMÉDIATS (I1 : aucune donnée RIP), les dix tours DÉROULÉS — AUCUN saut, AUCUN déplacement RIP, le flot temps constant PAR CONSTRUCTION. tls13-16 (h100016, le chiffrement d'un bloc) 129 o · 26 instructions — pxor RK[0] + NEUF AESENC + AESENCLAST RK[10] (sans MixColumns au dernier tour — FIPS 197 § 5.1), les clés chargées par movdqu NON ALIGNÉES (aucune précondition cachée), LA BRIQUE D'INVERSION N'EXISTE PAS (l'ouverture re-chiffre les compteurs — SP 800-38D § 6 : AES en sens unique, la découpe le nomme). tls13-17 (h100017, GHASH la multiplication) 162 o · 40 instructions — la marche de l'algorithme 1 § 6.3 MOT POUR MOT SANS TABLE PAR DONNÉE (la table de Shoup est la faille classique — la marche est lente ET constante, le choix minimal auditable ; PCLMULQDQ un CHANTIER FUTUR nommé, I5), LE DOMAINE GROS-BOUTISTE PAR BSWAP (la correction du geste — voir ci-dessous) : B = (h << 64) | l, h = bswap des octets 0..7 (l'octet 0 AU SOMMET), l = bswap des octets 8..15 ; l'extraction shld h, l, 1 POSE CF au bit courant (l'ancien bit 63 de la voie haute = LE PREMIER BIT DE LA CHAÎNE), le sbb LE CAPTURE AVANT que le shl de la voie basse n'écrase le drapeau — l'ordre shld/sbb/shl est LE geste de l'extraction ; le décalage de V vers la fin = shrd l, h, 1 puis shr h, 1, le sortant = l'ancien bit 0 de la voie basse (le CF du shrd au second sbb) ; LE REPLI R = 0xE1||0^120 : l'octet 0 au SOMMET de la voie haute — movabs 0xE1 << 56 en IMMÉDIAT (I4 : le bloc autoporteur), le masque 0/−1 par sbb, le repli PAR ET LOGIQUE — SANS BRANCHE (I1/I2 : le SEUL saut est la boucle sur le COMPTEUR public). tls13-18 (h100018, GCM sceller) 1076 o · 189 instructions — le cadre 0xE8 (l'ombre + J0/CB/H/Y/X/ks + les pointeurs, I5 : tout sur la PILE), J0 = nonce||0^31||1 FIGÉ dans son logement (le bloc compteur CB en est une COPIE qui mute : inc32 le u32 GROS-BOUTISTE par bswap, I3 — le rendement 2^32 hors d'atteinte par P4), l'ORDRE DES OPÉRATIONS (I1) : H = E(K, 0) D'ABORD (tls13-16), le CTR (le chiffré EXISTE avant le GHASH qui le digère), l'étiquette E(K, J0) ⊕ GHASH ; le GHASH accumule par APPELS RÉPÉTÉS à tls13-17 (I2 : l'AAD bourré, le chiffré bourré, les DEUX longueurs en BITS u64 gros-boutistes), les refus −1/−2 NOMMÉS (Q3 : pointeurs nuls, N ou A > 2^14). tls13-19 (h100019, GCM ouvrir) 1163 o · 204 instructions — la même recette sur le chiffré REÇU, LA DISCIPLINE DU VERDICT (I1) : la confrontation TEMPS CONSTANT — le OU cumulatif des 16 différences en UN seul drapeau (r10, AUCUN court-circuit), le branch sur LE drapeau ; PUIS le CTR (I2) : LA RESTITUTION EST LA DERNIÈRE OPÉRATION — l'étiquette divergente → rax = −4 NOMMÉ et la sortie clair INTACTE (fail-closed, RFC 8446 § 5.2 : l'enregistrement entier authentifié avant de rendre un octet).

**L'ARRÊT des slots (D161 rejoué — la mesure auteur décide).** Le MINIMUM admissible par longueur (multiple de 64, padding ≥ 16, tassés depuis la fin x25519 0xDCC0) : tls13-15 @0xDCC0 (slot 0x240, padding 56) · tls13-16 @0xDF00 (0xC0, 63) · tls13-17 @0xDFC0 (0xC0, 30) · tls13-18 @0xE080 (0x480, 76) · tls13-19 @0xE500 (0x4C0, 53) — **fin de la famille aead à 0xE9C0** (la marge : les familles restantes sous 0xF000, TENUE). Le ré-arrêt en cours de geste : tls13-17 préfiguré 139 o mesuré **162 o** après la correction de représentation — le slot 0xC0 TIENT (padding 30 ≥ 16), la chaîne NE BOUGE PAS ; les tailles de 18/19 INCHANGÉES par la correction J0 (l'immédiat u32 reste u32 — 0x01000000 au lieu de 0x00000001, les octets 00 00 00 01).

**LA SONDE DU GESTE (scripts/sonde_aead.py — le fail-closed AVANT le harnais : les cinq notations sur l'émulation contre la référence, le labo rejoué sur pièces) : 12/12 VERTS APRÈS les corrections — et 7/12 AVANT : LA PREUVE A CORRIGÉ LA NOTATION, ENCORE ET ENCORE (le geste hkdf avait ouvert la voie, x25519 l'a confirmée, celui-ci la scelle : LA MÉTHODE EST LA MÊME, la sonde d'abord, le harnais ensuite).** (1) **tls13-17 LA REPRÉSENTATION : le domaine GROS-BOUTISTE PAR BSWAP** — la première écriture tenait la chaîne de 16 octets en DEUX u64 little-endian (rax = les octets 0..7, r9 = les 8..15) et l'algorithme croyait lire le PREMIER bit de la chaîne au bit 63 de la voie basse : la sonde a renversé la multiplication **30 fois sur 30** (et la commutativité elle-même : X•Y ≠ Y•X — la représentation n'était même pas symétrique) ; la contre-preuve du labo avait déjà nommé la première lecture du repli (0xE1<<56, la lecture gros-boutiste) mais la correction d'alors s'était ARRÊTÉE À L'IMMÉDIAT — la REPRÉSENTATION restait fausse : le candidat LE classique (les bits LSB d'abord) testé et REJETÉ par le code (1/43), le candidat X-MSB rejeté (1/43), **LE CANDIDAT BSWAP/BE 63/63** — les DEUX voies bswapées au domaine gros-boutiste, l'extraction shld/sbb/shl (le drapeau capturé AVANT l'écrasement), le repli 0xE1<<56 au SOMMET de la voie haute : re-mesuré 139 → 162 o, le slot TIENT, REJOUÉ VERT (30 paires + les dégénérés + la commutativité aux DEUX ordres). (2) **tls13-18/19 LE J0 TERMINAL : le u32 1 posé en boutisme MACHINE** — `mov dword ptr [rsp + 0x2c], 1` écrit 01 00 00 00 : J0 se terminait en 0x01000000-ème position, inc32 comptait 0x01000001, 0x01000002… — le PREMIER bloc de compteur sortait 01 00 00 01 au lieu de 00 00 00 02 : le CHIFFRÉ faux (la sonde : TC2 rendait 5960118a… au lieu de 0388dace…) ET l'étiquette fausse (E(K, J0) faux) ; l'immédiat CORRIGÉ en 0x01000000 (les octets 00 00 00 01, le u32 GROS-BOUTISTE de la norme — taille NEUTRE), REJOUÉ VERT (TC1..TC4 chiffrés et étiquettes octet pour octet). Les défauts d'INSTRUMENT nommés et corrigés au geste : l'échelle *1 (la notation écrivait [rsp + rcx*1 + 0x70], capstone ne l'imprime pas — le round-trip V1 la nomme, la notation WYSIWYG suit : l'échelle 1 est IMPLICITE, cinq occurrences normalisées, mêmes octets) ; le piège d'import du labo (derive_aead.py se termine par sys.exit(0) au niveau module — l'import tue l'appelant : capturé à exec_module, l'espace de noms déjà peuplé) ; RET_MAGIQUE DÉPLACÉ 0xDE00 → 0xEF00 (la marge .text6 « après 0xDCC0 » du harnais x25519 est devenue L'INTÉRIEUR du slot de tls13-15 — le harnais aead le pose APRÈS sa famille, 0xE9C0 < 0xEF00 < les fixtures 0xFF00).

**Le harnais (tls13/harnais_aead.py — le modèle harnais_x25519 : l'émulation nue à les RVA du plan, les DIX-NEUF blocs posés, l'appelant factice msx64 aux sentinelles et canaris, l'instrument permanent posé à la naissance, le mode « nue » pour les longues exécutions).** 49 contrôles · 49 VERTS × 3 graines (20261107, 41, 20261108) : V0 les pièces (le scellé 0.9.0 relu 44 544 o sha256 1492b0bc…, les familles sha ET hkdf ET x25519 INTACTES re-round-tripées aux longueurs arrêtées 74/387/139/165 + 435/151/347/310 + 54/252/1078/281/2887/23, les fixtures re-dérivés, **la famille aead N'AJOUTE AUCUN FIXTURE** — R = 0xE1||0^120 en IMMÉDIAT, l'ARRÊT AES-NI tient l'expansion matérielle —, l'arbre I scellé relu VERT) ; V1 le round-trip 100 % (keystone == capstone, 114/26/40/189/204 instructions, les tailles == l'ARRÊT 520/129/162/1076/1163) + les concordances au plan (les appels de 18 et 19 == TLS16 ×3 + TLS17 ×3 — les sites statiques H/CTR/J0 et AAD/chiffré/longueurs ; les DIX Rcon de 15 en immédiats + pshufd 0xff ×10 ; la composition de 16 : pxor + NEUF aesenc + aesenclast ; le movabs 0xE1<<56 de 17 ; le J0 0x01000000 de 18/19) + la structure (**AUCUN déplacement RIP dans la famille ENTIÈRE** — contrairement à x25519 et ses deux fixtures, l'aead ne lit rien hors de ses arguments et de sa pile : le bloc autoporteur ; aucun syscall, aucun appel indirect) + le temps constant STRUCTUREL (15/16 ZÉRO saut conditionnel — le flot AES-NI SANS BRANCHE PAR CONSTRUCTION ; 17 exactement UN : le compteur de boucle public, le bit de X devient MASQUE par sbb ; 18 exactement DIX-SEPT et 19 exactement DIX-NEUF, TOUS sur les données PUBLIQUES — les comptes EXACTS vérifiés source par source : pointeurs, longueurs N et A, compteurs de boucle, la taille de bloc 16, le compteur de copie — ; LE VERDICT de 19 : test r10, r10, LE drapeau CUMULÉ des 16 différences) ; V2 les vecteurs officiels (FIPS 197 C.1 : le déploiement 176 o == la référence PUIS le bloc 69c4e0d8… ; SP 800-38A F.1.1 : les QUATRE blocs PAR LA COMPOSITION 15+16 — un déploiement faux rend un chiffrement faux ; McGrew–Viega TC1..TC4 : chiffrés ET étiquettes octet pour octet puis ouverts — TC5/TC6 aux IV de 8 et 60 octets HORS CONTRAT de la brique, P2 le nonce de 12 o la borne du protocole, la référence du labo les couvre ; **LE TRANSFERT RFC 8448 : les SEPT enregistrements chiffrés du § 3 OUVERTS par tls13-19** — le nonce = IV ⊕ séquence (RFC 8446 § 5.3), la tête 0x17 en AAD, le clair interne payload || type rendu — **PUIS RESCELLÉS par tls13-18 == l'enregistrement OCTET POUR OCTET** ; l'oracle différentiel : 100 scellages + 100 ouvertures aléatoires, ZÉRO écart) ; V3 les cas punitifs (le GHASH : X = 0 → 0, Y = 0 → 0, l'identité réfléchie 0x80||0^120 : X·ID == X, X = Y = 1, X = Y = R, la commutativité aux DEUX ordres sur 50 paires ; le chevauchement : la sortie SUR l'entrée pour 16 ET 17 — le bloc charge AVANT d'écrire ; **la borne P4 : N = 16384 EXACT scellé puis ouvert octet pour octet** ; N = 16385 et A = 16385 → rax = −2 NOMMÉS ; les refus −1 : les DOUZE pointeurs nuls — six de 18, six de 19 ; L'INDIFFÉRENCE : A = 0 avec le pointeur AAD NUL n'est PAS un refus — le couple longueur/pointeur, jamais le pointeur seul) ; V4 le contrat (les 8 non-volatiles rendus, la pile équilibrée, l'ombre et les QUATRE logements d'arguments de pile intacts — le cadre 0xE8, la zone profonde intacte ; **l'alignement msx64 à 20 entrées de callee** (TLS16 ×10 == 2×[2 + ⌈37/16⌉ = 5], TLS17 ×10 == 2×[⌈13/16⌉ + ⌈37/16⌉ + 1 = 5] — les comptes EXACTS de la recette sur le scellement ET l'ouverture), rsp ≡ 8 mod 16 chacune ; les entrées INTACTES : le nonce, le clair, l'AAD, le chiffré reçu, l'étiquette reçue — J0 et CB vivent dans les copies locales ; les sorties JAMAIS dépassées ; **le refus SANS corruption** : N hors borne → −2 AVANT toute écriture, le chiffré et l'étiquette demeurent VIERGES) ; V5 la falsification, ZÉRO SILENCE (la clé mutée premier/milieu/dernier octet → le chiffré ou l'étiquette divergent 3/3 ; le nonce et le clair mutés 6/6 ; **LES 16 OCTETS DE L'ÉTIQUETTE mutés UN PAR UN → rax = −4 NOMMÉ et la sortie clair INTACTE 16/16 — fail-closed : AUCUN octet restitué ; LES 53 OCTETS DU CHIFFRÉ mutés UN PAR UN → −4 et la sortie INTACTE 53/53** — la garde constatée mutation par mutation, Q4 de tls13-19 ; l'AAD muté → −4 3/3 : les données associées sont couvertes ; la comparaison non muette) ; V6 le temps constant MESURÉ (le déploiement : 4 clés, **114 instructions EXACTEMENT** — AESKEYGENASSIST temps constant PAR CONSTRUCTION ; le bloc : 3 paires, **26 instructions** — les dix tours TOUJOURS ; le GHASH : 3 paires, **2 199 instructions** — le bit de X devient masque, les 128 itérations TOUJOURS ; le scellage : 2 clairs et clés différents de même longueur, **12 531 instructions** — la longueur est publique, le contenu JAMAIS ; **LE VERDICT DE L'OUVERTURE : trois étiquettes divergentes — octets 0, 8 et 15 mutés — 11 755 instructions EXACTEMENT LE MÊME COMPTE : les 16 différences TOUTES accumulées avant LA branche, la position de la première divergence est INVISIBLE dans le temps** — I1 de tls13-19, LA discipline du verdict, la charte § 3 sur pièces ; l'ouverture conforme : 12 678 instructions).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN build (le chantier (e) attend son geste — le garde est VERT), l'arbre scellé tls13/I INTACT (le sceau relu VERT au harnais V0 APRÈS le geste — R2 tenue), m8/proxy.exe INTACT (1492b0bc…, relu en V0.a), les familles sha, hkdf ET x25519 intactes (relues aux longueurs arrêtées en V0.b), AUCUNE règle modifiée, la charte § 2 tenue (les vecteurs officiels AVANT usage — la référence croisée AVANT de juger, la falsification), la charte § 3 tenue (le temps constant NOMMÉ par bloc, structurel ET mesuré — le verdict compris). Livrables : tls13/layout.py (la famille aead ARRÊTÉE + les adresses A_CLES_TOUR..A_OUVRIR), tls13/outils/auteur.py (les 19 blocs — la description de h100017 corrigée au domaine gros-boutiste), tls13/notation/ (5 brouillons + 5 notations explicites corrigés), tls13/harnais_aead.py (49 contrôles VERTS × 3 graines) ; le labo : scripts/sonde_aead.py (la sonde du geste), scripts/candidats_ghash.py (les candidats rejetés 1/43 — la preuve de la représentation), scripts/verify_sync_m9d.py (la reprise D164) ; consignations : la présente Entrée PAR SCRIPT, PLAN (chantier (b) : la famille aead + État du programme), worklog +Task ID 91.

- SUITE : LE CHANTIER M9-(b) CONTINUE — la famille enregistrement (tls13-20/21 : l'enregistrement protéger/déprotéger — le chevauchement des fragments, le numéro de séquence au nonce par IV ⊕ seq), puis la poignée (tls13-23..28 : ServerHello, le calendrier des clés, Finished, l'épinglage, la machine d'états — LE TRANSFERT RFC 8448 en bout en bout) ; puis (d) le socle socket sys-04+, (e) LA CÉRÉMONIE DE L'ÈRE + le build 1.0.0-dev.1, (f) le terrain — LA GRANDE ŒUVRE.

"""

TASK = """

## Task ID 91 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE aead NOTÉE-MESURÉE-PROUVÉE (07/11)

- LA SYNCHRO VÉRIFIÉE SUR LES TROIS MIROIRS (la demande du développeur :
  « vérifie si la synchro… puis on continue », puis « on enchaine », puis
  « continue ») : verify_sync_m9d.py 22 VERTS / 0 ROUGES — HEAD 8b7b8e9
  (la passation Task 90), le miroir porte les fichiers de la passation
  md5 MATCH, le bundle courant 090-06c2f4d UNIQUE, 34 archives (rien
  supprimé), /test sans copie, GitHub == 06c2f4d (la pointe x25519 — le
  commit de passation EMBARQUÉ au geste présent, le flux établi), le
  jeton OAuth vivant ; les cinq notations aead non committées
  correctement ABSENTES du miroir.
- LE GESTE : tls13-15..19 — le déploiement des clés de tour (L'ARRÊT
  AES-NI : AESKEYGENASSIST le SubWord/RotWord MATÉRIEL, pshufd 0xFF le
  mot au dword 3 [la sonde du labo], la recette préfixe-XOR ⊕ t, les dix
  Rcon en IMMÉDIATS, les dix tours DÉROULÉS), le chiffrement d'un bloc
  (pxor + NEUF AESENC + AESENCLAST, la BRIQUE D'INVERSION n'existe
  pas), GHASH (la marche de l'algorithme 1 § 6.3 MOT POUR MOT, sans
  table par donnée, SANS BRANCHE — le masque 0/−1 par sbb, le repli par
  ET logique), GCM sceller (H = E(K,0) d'abord, le CTR, le GHASH par
  appels répétés, les longueurs u64 gros-boutistes, E(K,J0) ⊕ GHASH,
  les refus −1/−2 NOMMÉS) et GCM ouvrir (LA DISCIPLINE DU VERDICT : le
  OU cumulatif des 16 différences en UN drapeau, AUCUN court-circuit,
  PUIS le CTR — la restitution DERNIÈRE, l'étiquette divergente → −4
  NOMMÉ, la sortie INTACTE) — notés (520/129/162/1076/1163 o,
  round-trip 100 %), mesurés (les slots ARRÊTÉS 0x240/0xC0/0xC0/0x480/
  0x4C0 tassés depuis 0xDCC0, fin 0xE9C0 — D161 rejoué), prouvés (LE
  HARNAIS 49 contrôles · 49 VERTS × 3 graines).
- LES PREUVES : FIPS 197 C.1 (le déploiement ET le bloc), SP 800-38A
  F.1.1 (les quatre blocs PAR LA COMPOSITION — un déploiement faux rend
  un chiffrement faux), McGrew–Viega TC1..TC4 (chiffrés + étiquettes
  octet pour octet, puis ouverts ; TC5/TC6 hors contrat — P2 le nonce
  de 12 o), **LE TRANSFERT RFC 8448 : les SEPT enregistrements chiffrés
  du § 3 OUVERTS puis RESCELLÉS == l'enregistrement OCTET POUR OCTET**
  (le vol serveur 679 o, le Finished 58 o, le NewSessionTicket 227 o,
  les applicatives 72 o ×2, les close_notify 24 o ×2 — le nonce =
  IV ⊕ séquence, la tête 0x17 en AAD) ; l'oracle 100 scellages + 100
  ouvertures ZÉRO écart ; la borne P4 (N = 16384 exact), les refus −1
  (DOUZE pointeurs) et −2, l'indifférence (A = 0 : le pointeur nul
  n'est pas un refus) ; le contrat (20 entrées de callee alignées aux
  comptes EXACTS, les entrées intactes, les sorties jamais dépassées,
  le refus SANS corruption) ; la falsification (la clé/le nonce/le
  clair 12/12 ; **LES 16 octets de l'étiquette ET LES 53 octets du
  chiffré mutés UN PAR UN → −4, la sortie INTACTE 69/69**) ; le temps
  constant MESURÉ (114/26/2199/12531 instructions ; **LE VERDICT :
  trois étiquettes divergentes → 11 755 instructions LE MÊME COMPTE —
  la position de la divergence INVISIBLE dans le temps**).
- LES DEUX DÉFAUTS DE NOTATION nommés par LA SONDE du geste (la preuve
  corrige la notation : 7/12 avant, 12/12 après) : (1) tls13-17 LA
  REPRÉSENTATION — la première écriture tenait la chaîne en DEUX u64
  little-endian : renversée 30/30, la commutativité elle-même fausse ;
  la correction du labo d'avant s'était arrêtée à l'IMMÉDIAT du repli,
  la REPRÉSENTATION restait fausse ; les candidats LE-classique et
  X-MSB rejetés par le code (1/43), LE CANDIDAT BSWAP/BE 63/63 — les
  DEUX voies bswapées, l'extraction shld/sbb/shl (le drapeau capturé
  AVANT l'écrasement), le repli 0xE1<<56 au sommet de la voie haute ;
  re-mesuré 139 → 162, le slot 0xC0 TIENT. (2) tls13-18/19 LE J0
  TERMINAL — le u32 1 posé en boutisme MACHINE (01 00 00 00) : le
  premier compteur sortait 01 00 00 01, le CHIFFRÉ et l'étiquette
  faux ; l'immédiat corrigé 0x01000000 (les octets 00 00 00 01),
  taille NEUTRE, REJOUÉ VERT.
- Les défauts d'instrument corrigés au geste : l'échelle *1 (capstone
  ne l'imprime pas — cinq occurrences normalisées, mêmes octets), le
  sys.exit(0) du labo à l'import (capturé à exec_module), RET_MAGIQUE
  déplacé 0xDE00 → 0xEF00 (la marge .text6 du harnais x25519 était
  devenue l'intérieur du slot de tls13-15).
- FRONTIÈRES : aucune balise, AUCUN build, l'arbre scellé tls13/I
  INTACT (verifier_specs_m9a relu VERT au harnais V0), m8/proxy.exe
  INTACT, les familles sha, hkdf ET x25519 intactes (relues en V0.b) ;
  consignations : Entrée 173 PAR SCRIPT, PLAN (chantier (b) : la
  famille aead + État du programme), worklog +Task ID 91.
- SUITE : la famille enregistrement (tls13-20/21 — le chevauchement
  des fragments, le numéro de séquence au nonce), puis la poignée
  (tls13-23..28 — LE TRANSFERT RFC 8448 en bout en bout), (d) sys-04+,
  (e) LA CÉRÉMONIE + le build 1.0.0-dev.1, (f) le terrain.

Stage Summary:
- LA QUATRIÈME FAMILLE de la grande œuvre est notée-mesurée-prouvée :
  LE CHIFFREMENT AUTHENTIFIÉ de TLS 1.3 existe en octets — les SEPT
  enregistrements du transcript officiel RFC 8448 ouverts ET rescellés
  octet pour octet par les briques mêmes, le verdict temps constant
  MESURÉ (la position d'une divergence INVISIBLE dans le temps).
- LA PREUVE A CORRIGÉ LA NOTATION, TROISIÈME GESTE DE SUITE : la
  représentation GHASH (le domaine gros-boutiste par bswap — le
  candidat des candidats rejeté 1/43 par le code) et le J0 terminal
  (l'immédiat gros-boutiste) nommés par la sonde AVANT le harnais,
  corrigés et rejoués verts — la sonde d'abord, le harnais ensuite :
  LA MÉTHODE EST LA MÊME depuis le geste hkdf.
"""

def inserer():
    j = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 173 —" in j:
        print("[inserer-173] REJEU REFUSÉ : l'Entrée 173 existe déjà.")
        return 1
    n = j.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-173] ÉCHEC : marqueur {n} fois dans le journal.")
        return 1
    if "## Entrée 172 —" not in j:
        print("[inserer-173] ÉCHEC : l'Entrée 172 est absente (ordre 172<173).")
        return 1
    j = j.replace(MARQUEUR, ENTREE + MARQUEUR)
    JOURNAL.write_text(j, encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 91 —" in w:
        print("[inserer-173] REJEU REFUSÉ : le Task ID 91 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-173] PASSÉ : Entrée 173 insérée avant le marqueur ; worklog +Task ID 91.")
    return 0


if __name__ == "__main__":
    sys.exit(inserer())
