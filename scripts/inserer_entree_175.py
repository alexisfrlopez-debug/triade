#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_175.py — LA CONSIGNATION DU GESTE « LE CHANTIER M9-(b)
CONTINUE : LA FAMILLE poignée + LE PRINCIPAL NOTÉS-MESURÉS-PROUVÉS » :
JOURNAL_TRAVAIL +Entrée 175 (ordre 174<175<marqueur, rejeu REFUSÉ), worklog
+Task ID 93. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 175 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE poignée + LE PRINCIPAL NOTÉS-MESURÉS-PROUVÉS — tls13-22..28 (le ClientHello composé, le ServerHello traité, le calendrier de clés à trois étages, le Finished calculé/vérifié, l'épinglage, LA MACHINE D'ÉTATS du client entier, le socle d'appel à rappels — RFC 8446 § 4/§ 7.1/§ 4.4.4 : le transcript source de vérité, la preuve de possession n'est jamais une parole) : la notation à la main (241/532/2130/239/285/2906/144 o, round-trip 100 %, les slots ARRÊTÉS 0x120/0x240/0x880/0x100/0x140/0xB80/0xB0 tassés depuis 0xED00 — la poignée finit 0xFB20 SOUS les fixtures x25519 immobiles, le principal 0xFF40..0x10B30 — la marge franchit 0xF000 comme le plan l'avait nommé, D161 rejoué), LE HARNAIS 52 contrôles · 52 VERTS × 3 graines (LE TRANSFERT RFC 8448 BLOC PAR BLOC sur les valeurs consignées, LA SESSION ENTIÈRE contre le simulateur, la falsification à chaque étage rend SON verdict nommé) ; DOUZE FAUTES nommées par le fail-closed, l'erratum n° 2 consigné sur pièces AVANT la notation (07/11)

**La reprise SUR LES TROIS MIROIRS (D164 rejouée — la demande du développeur : « on enchaine »).** La vérification LECTURE SEULE par script (scripts/verify_sync_m9f.py du labo, 16 VERTS — le dix-septième contrôle, l'arbre propre, ne voyait que l'empreinte du script éphémère lui-même : retiré avant la lecture, l'arbre est PROPRE) : HEAD == b59bf44 (la passation Task 92), le worklog porte la passation D141 consignée, le bundle courant triade-history-090-5487f7f.bundle UNIQUE au miroir (md5 f73af0a2… MATCH le consigné), archives-bundles/ : 36 archives (rien supprimé), /test sans copie, le kit Cérémonie/v06 déployé, GitHub == 5487f7f (LA POINTE du geste enregistrement — le commit de passation b59bf44 EMBARQUÉ), le jeton OAuth vivant, le hook a synchronisé la pointe (rc=0/rc=0). La réserve instrumentale D149 re-vérifiée AVANT usage : LE DISQUE LABO RECYCLÉ ENCORE (capstone/keystone/unicorn/pynacl/pefile emportés) — RÉINSTALLÉS PAR PROCÉDURE.

**LE LABO D'ABORD (scripts/derive_poignee.py — le juge est le code : le texte officiel RFC 8448 téléchargé de rfc-editor.org, § 3 parsé PAS À PAS, 41 contrôles VERTS).** Le couple x25519 et LE SECRET PARTAGÉ (8bd4054f…) recoupés par PyNaCl des DEUX côtés ; LE CALENDRIER étage par étage par la référence (early 33ad0a1c…, derived 6f2615a1…/43de77e0…, handshake 1dc826e9…, c_hs b3eddb12…, s_hs b67b7d69…, master 18df0684…, c_ap 9e40646c…, s_ap a11af9f0…) ; LES QUATRE CHAÎNES write/IV == TRANSFERT_8448 (le recoupement avec le geste enregistrement) ; LES TROIS HASH du transcript du RFC (CH..SH 860c06ed…, CH..CV edb7725f… RE-DÉRIVÉ — le RFC ne l'imprime pas, le code le dérive, CH..FinS 9608102a…) ; LES DEUX Finished (le serveur 9b9b141d… vérifié sur la coupe re-dérivée, le client a8ec436d…) ; LE VOL déverrouillé par la référence, le CERTIFICAT parsé (le DER 432 o de la PREMIÈRE entrée, l'empreinte recalculée), la marche du ServerHello pré-jouée (la construction re-jouée de verifier_specs_m9a).

**L'ERRATUM n° 2 (sur pièces, AVANT la notation — consigné dans tls13/I/README.md, le modèle M8-(b) libc-02 / av-10).** **(1)** le ClientHello du RFC 8448 § 3 compte **196 o** — l'offre RICHE d'un client généraliste (TROIS suites 1301/1303/1302, SNI « server », NEUF groupes, QUINZE sigalgs) : l'égalité octet pour octet promise par tls13-22 Q1 (« OCTET POUR OCTET la structure du premier message ») et tls13-27 Q3 (« les octets émis == les octets du RFC 8448 ») est IMPOSSIBLE PAR CONSTRUCTION contre l'offre MINIMALE scellée du jalon (114 o, charte § 1 : « le domaine ne propose JAMAIS ce qu'il ne prouve pas », I3 : SNI chantier futur nommé) — LA LECTURE CORRIGÉE : la construction re-jouée du plan (le fixture aléa @ +6, clé @ +82), les égalités qui TIENNENT (le SH traité VERBATIM 95 o, le secret partagé, LES SECRETS CONSIGNÉS du calendrier sur les hash du RFC en ARGUMENTS, les clés write/IV == LES QUATRE CHAÎNES, les DEUX Finished au niveau des BLOCS), la preuve de la machine = LA SESSION ENTIÈRE contre le SIMULATEUR. **(2)** le contexte de l'étiquette « derived » est le hash du TRANSCRIPT VIDE (Derive-Secret(., "derived", "") § 7.1 : Hash("") = e3b0c442…, 32 o — l'info imprimée par le RFC fait 49 o, JAMAIS un contexte de zéro octet) — la notation dérive le condensé du vide par tls13-01+04 AU GESTE MÊME. **(3)** la garde de tls13-23 P2 « ≥ 94 : 4 + 90 » compte l'en-tête DEUX FOIS : le ServerHello minimal = 90 o (4 + 86, la construction re-jouée) — la garde est rdx ≥ 90. Les écritures seules sont fautives, jamais la notation.

**La notation (les SEPT brouillons msx64 → les SEPT notations explicites WYSIWYG).** tls13-22 (h100022, 241 o · 47 instructions, slot 0x120) : LA COMPOSITION PAR OCTETS FIXES — chaque champ à son offset constant, les valeurs protocolaires du plan en IMMÉDIATS (T5), l'aléa copié @ +6, la clé publique @ +82, AUCUNE branche de données (charte § 1 : le message est FIXE). tls13-23 (h100023, 532 o · 129, slot 0x240) : LA MARCHE BORNÉE, chaque confrontation NOMMÉE dans l'ordre du corps (le type 2, la version 0x0303, l'aléa ≠ LA VALEUR MAGIQUE HRR au fixture R_HRR par OU cumulatif, l'écho session_id vide, LA SUITE 0x1301 lue GROS-BOUTISTE par xchg → -5 LA NÉGOCIATION REFUSÉE, la compression nulle, la région d'extensions qui DOIT épuiser le corps, supported_versions 0x0304 PRÉSENTE, key_share x25519 32 o PRÉSENTE, les extensions inconnues IGNORÉES — la règle du protocole), l'épuisement exact, PUIS tls13-13 — la clé privée n'est JAMAIS touchée sur un message refusé. tls13-24 (h100024, 2130 o · 336, slot 0x880 — le plus grand bloc de calcul pur du domaine) : LA MACHINE À DÉRIVER à TROIS étages STRICTS (le dispatch EST l'étape, -3 sur tout saut, l'étape 4 n'existe pas : CLOS), SEIZE étiquettes HKDF (les libellés aux fixtures R_LIB_* du plan — données PUBLIQUES), TROIS extraits, QUATRE déploiements tls13-15, le condensé du vide dérivé par 01+04, les contextes sortis COMPLETS (rk 176 + IV 12 + réserve + séquence 0), le hash du transcript est un ARGUMENT (le calendrier ne hache RIEN). tls13-25 (h100025, 239 o · 62, slot 0x100) : DEUX modes NOMMÉS (0 calculer, 1 vérifier), le reçu CONFRONTÉ par OU cumulatif des 32 différences — LE test À LA FIN (la discipline du verdict AEAD), le reçu JAMAIS modifié. tls13-26 (h100026, 285 o · 58, slot 0x140) : le SHA-256 du DER sur un contexte de PILE, la comparaison TEMPS CONSTANT (l'empreinte est une donnée de CONFIANCE), -6 NOMMÉ. tls13-27 (h100027, 2906 o · 567, slot 0xB80 — LE PLUS GRAND bloc du domaine : LA MACHINE D'ÉTATS) : QUATRE événements NOMMÉS (OUVRIR/ÉMETTRE/RECEVOIR/FERMER) sur le contexte session 17 520 o à la disposition DÉCLARÉE, LA LISTE FERMÉE des compositions (31 sites d'appel directs + TLS28 ×10 pour TOUTE entrée/sortie), le transcript initialisé (tls13-01 — la session naît VIERGE) et chaque message complet ABSORBÉ AVANT traitement (charte § 4), les coupes du hash sur la COPIE (RFC 8446 § 7.1 : le hash COURANT), le réassemblage au tampon @ +1136 (la borne 2^14 NOMMÉE), le certificat : l'extraction de la PREMIÈRE entrée (le u24 lu — le DÉTROIT de tls13-26), le CertificateVerify ABSORBÉ sans vérification (le chantier futur nommé : la confiance a tranché à l'épinglage), LA DISCIPLINE D'ÉCHEC : tout verdict négatif PROPAGÉ NOMMÉ, l'état passe à 5 (MORT), AUCUN octet applicatif après, un échec n'ÉMET RIEN de plus que l'offre déjà partie. tls13-28 (h100028, 144 o · 48, slot 0xB0) : LA ROTULE — le seul point du domaine où le calcul touche le monde : UN contexte de DEUX rappels, L'APPEL INDIRECT DÉCLARÉ (call r10 ×2 — la cible est une DONNÉE du contexte : NI un import NI un syscall, l'oracle structurel le constate), le zéro de réception est le refus -7 du KIT, AUCUNE copie (l'adaptateur).

**L'ARRÊT des slots (D161 rejoué — la mesure auteur décide).** Le MINIMUM admissible par longueur (multiple de 64, padding ≥ 16) : 22 @0xED00 (0x120, 47) · 23 @0xEE20 (0x240, 44) · 24 @0xF060 (0x880, 46) · 25 @0xF8E0 (0x100, 17) · 26 @0xF9E0 (0x140, 35) — **fin de la famille poignée à 0xFB20, SOUS les fixtures x25519 (R_U9 0xFF00, R_EXP_INV 0xFF20 — leur ARRÊT consigné ne bouge pas, miroir R7)** ; le principal suit À 0xFF40 — LA MARGE A FRANCHI 0xF000 comme le plan l'avait nommé (« la mesure décidera, jamais la négociation ») : 27 @0xFF40 (0xB80, 38) · 28 @0x10AC0 (0xB0, 32) — fin du principal 0x10B30 ; les fixtures POIGNÉE (les HUIT libellés alignés 16, la valeur magique HRR 32 o) à leur ARRÊT 0x10B40..0x10BD0. Les re-arrêts en cours de geste : 23 (524 → 532 : la lecture GROS-BOUTISTE de la suite par xchg), 27 (2864 → 2882 : l'INIT du transcript nommé après la première mesure → 2906 : LE KIT SAUVÉ au cadre, r9 VOLATIL clobberé par l'appel d'étage).

**Le harnais (tls13/harnais_poignee.py — le modèle harnais_enregistrement : LA RÉFÉRENCE de la lignée importée [harnais_aead : la référence GCM + TRANSFERT_8448], l'émulation nue aux RVA du plan, les VINGT-HUIT blocs posés, LA ZONE MORTE PROFONDE à −0xE000 [sous le cadre 0x43C8 de la machine ET les cadres imbriqués 0x4078/0xE8], LE SIMULATEUR : DEUX RAPPELS de machine code [l'émettre qui journalise, le recevoir qui sert la cassette] — la réalisation LICITE du contexte socle, tls13-28 I3).** 52 contrôles · 52 VERTS × 3 graines (20261107, 41, 20261108) : V0 les pièces (le scellé relu, les VINGT-ET-UNE notations précédentes INTACTES, les fixtures posés — les HUIT libellés, HRR, U9, EXP_INV, K —, la session 17 520 o recomptée, l'arbre I relu VERT AVEC l'erratum, LES PIÈCES CONSIGNÉES recoupées au geste même) ; V1 le round-trip 100 % (241/532/2130/239/285/2906/144 o) + les concordances (les appels directs : 22 AUCUN, 23 TLS13, 24 TLS06 ×3 + TLS08 ×16 + TLS15 ×4 + 01 + 04, 25 TLS05, 26 01+03+04, 27 LA LISTE FERMÉE [31 sites], 28 AUCUN direct ; L'APPEL INDIRECT DÉCLARÉ de 28 ×2 ; AUCUN syscall ; les déplacements RIP aux fixtures du plan SEULEMENT ; le CH == la construction re-jouée ; le temps constant STRUCTUREL : les TROIS comparaisons par OU cumulatif) ; V2 **LE TRANSFERT RFC 8448 BLOC PAR BLOC** (le SH du RFC VERBATIM → LE SECRET PARTAGÉ 8bd4054f… octet pour octet ; le calendrier étage par étage sur les hash CONSIGNÉS → LES SECRETS consignés ET LES QUATRE CHAÎNES du TRANSFERT_8448 [les contextes 200 o OCTET POUR OCTET, rk 176 + IV 12 + réserve + séquence 0] ET les clés Finished consignées ; le Finished client CALCULÉ == a8ec436d…, celui du serveur VÉRIFIÉ == 9b9b141d…, UN octet muté → -4 ; l'épinglage du certificat du transcript — l'empreinte recalculée ; le socle : journalisé/servie/-7/-1) ; V3 les punitifs (les refus nommés de chaque bloc — la négociation -5, HRR -5, les étages stricts -3, les modes -1, l'épinglage -6, rdx < 90 → -2, l'épuisement -1, l'extension inconnue IGNORÉE avec le secret INTACT, l'oracle différentiel 30 ServerHello aléatoires == X25519 de PyNaCl ZÉRO écart, la table des événements de 27 : tout événement hors de sa ligne → -3, l'état passe à 5) ; V4 le contrat (les non-volatiles, la pile, la zone morte profonde, **l'alignement msx64 : 205 entrées à travers LA SESSION ENTIÈRE — l'imbrication COMPTÉE, les feuilles SHA au cœur de la composition AVEC le principal — rsp ≡ 8 (mod 16) à CHAQUE entrée, les comptes EXACTS**, le kit INTACT — la machine COPIE, elle ne touche jamais la source) ; V5 la falsification (la clé privée divergente → le secret diverge, le hash muté → les clés divergent, le verify_data 32/32 → -4, la clé Finished mutée → -4, l'épinglage muté dans les DEUX sens 9/9 → -6) ; V6 le temps constant MESURÉ (le verdict du Finished : trois divergents → 18 416 instructions LE MÊME COMPTE ; l'épinglage : 31 405 ; la comparaison HRR : 1 239 089 — la position de la divergence INVISIBLE dans le temps) ; V7 **LA MACHINE : LA SESSION ENTIÈRE CONTRE LE SIMULATEUR** (OUVRIR : le journal == NOTRE CH cadré + NOTRE Finished — le simulateur a servi le SH du RFC VERBATIM et le vol re-scellé sous NOS clés [EE/Cert/CV verbatim, le Finished serveur RECALCULÉ sur NOTRE coupe], l'état 3 ; la session recoupée champ par champ contre la référence [le calendrier master/étape 3, les QUATRE contextes aux séquences exactes, les clés Finished, l'empreinte, le couple] ; ÉMETTRE : la charge du § 3 scellée sous NOTRE chaîne == la référence octet pour octet ; RECEVOIR : la charge restituée == la charge du RFC, rax == la longueur ; la close_notify serveur → l'état 4, rax = 0 ; FERMER : le close_notify émis == la référence ; LA FALSIFICATION à chaque étage : le SH muté → -5, l'étiquette du vol mutée → -4, l'empreinte du kit mutée → -6, LA COUPURE DU SOCLE → -7, OUVRIR sur l'état 3 → -3, l'état 5 ne rend PLUS RIEN — chaque session morte n'a émis QUE son offre, un échec n'ÉMET RIEN de plus, charte § 5).

**LES FAUTES nommées par le fail-closed (la preuve a corrigé la notation ET l'instrument — DOUZE, la méthode a tenu : la dérivation d'abord, le juge est le code).** (1) **la suite en BOUTISME MACHINE** : `cmp word ptr [rcx + 39], 0x1301` ne voyait JAMAIS les octets 13 01 (LE image 0x0113) — tout ServerHello était refusé -5 : la lecture GROS-BOUTISTE par `movzx eax, word / xchg al, ah`, la constante du plan directement. (2) les registres HAUTE-OCTET (`xchg r10b, r10h` — inexistants pour r8-r15) : la forme eax/al/ah. (3) `cmp rdx, imm64` inassemblable : movabs (la convention capstone du geste aead). (4) LES STUBS clobbraient rdi/rsi — NON-VOLATILES en msx64 (contrairement à SysV) : push/pop autour du rep movsb. (5) le stub recevoir avançait LA CASE DE PILE (`add [rsp], rax` — la copie du pointeur) au lieu de la cellule pointée : le pointeur RECHARGÉ, l'écriture À TRAVERS. (6) LE POINTEUR KIT (r9) utilisé après l'appel d'étage 1 — r9 est VOLATIL, clobberé : sauvé au cadre [rsp+0x38], nommé par le crash (lecture non-mappée). (7) l'immédiat sigalgs du CH (l'ordre des octets : 0x04080400 — sur-corrigé une fois, le deuxième fail a nommé la permutation). (8) les QUATRE copies rep movsq rsi/rdi INVERSÉES (le contexte zéro écrasait la sortie d'étage au lieu d'être écrit). (9) **LA TRANSCRIPTION MANUELLE du secret partagé** : un octet mutilé à la main (« fdbacf9f » pour « fdfbacf9 ») — RE-POSÉ PAR DÉRIVATION (PyNaCl) : la leçon consignée — JAMAIS recopiée à la main, TOUJOURS dérivée par code (déjà la leçon des libellés du geste hkdf). (10) les longueurs de libellés : « c hs traffic » = 12 o, pas 13 (l'étiquette RFC 0x12 = 18 AVEC le préfixe). (11) L'INIT DU TRANSCRIPT manquait à OUVRIR (tls13-01 : la session naît VIERGE — le kit fournit le CSPRG, le couple et la confiance, JAMAIS le transcript). (12) l'auteur : l'appel indirect sur REGISTRE (call r10) n'est pas un symbole de bloc — DÉCLARÉ (tls13-28 I2) ; TLS06/08/14/15/20/21 manquaient aux SYMBOLES (jamais appelés par les notations précédentes).

**Détail.** FRONTIÈRES : aucune balise ne bouge, AUCUN build (le chantier (e) attend — le garde VERT, la dette de cérémonie demeure : m0 CODE 10, tls13 CODE 12 — la remise du développeur précède tout build), l'arbre scellé tls13/I INTACT (verifier_specs_m9a relu VERT au harnais V0.f APRÈS l'erratum n° 2 — R2 tenue, l'erratum est la preuve sur pièces, jamais une réécriture), m8/proxy.exe INTACT (relu en V0.a), les familles sha, hkdf, x25519, aead ET enregistrement intactes (relues aux longueurs arrêtées en V0.b), AUCUNE règle modifiée, la charte tenue de § 1 à § 8 (la suite constante, les vecteurs officiels AVANT usage, le temps constant NOMMÉ structurel ET mesuré, le transcript absorbé avant traitement, l'échec propre et nommé, le bloc ne détient rien, aucun import aucun syscall — l'appel indirect DÉCLARÉ de la rotule excepté, NOP 0x90). Livrables : tls13/layout.py (la famille poignée + le principal ARRÊTÉS, les fixtures libellés+HRR, les A_* nouveaux), tls13/outils/auteur.py (les 28 blocs, les SYMBOLES complets, l'appel indirect déclaré), tls13/notation/ (7 brouillons + 7 notations explicites), tls13/harnais_poignee.py (52 contrôles VERTS × 3 graines), tls13/I/README.md (l'erratum n° 2 sur pièces). Consignations : la présente Entrée PAR SCRIPT, PLAN (chantier (b) : la famille poignée + le principal + État du programme), worklog +Task ID 93. SUITE : (d) le socle socket sys-04+ (la fondation I/O nommée par M8), (e) LA CÉRÉMONIE DU SCEAU I de l'ère + le build 1.0.0-dev.1, (f) le terrain — LA GRANDE ŒUVRE.
"""

TASK = """## Task ID 93 — LE CHANTIER M9-(b) CONTINUE : LA FAMILLE poignée + LE PRINCIPAL NOTÉS-MESURÉS-PROUVÉS (07/11)

- LA SYNCHRO VÉRIFIÉE SUR LES TROIS MIROIRS (« on enchaine ») :
  verify_sync_m9f.py 16 VERTS (l'arbre propre : le contrôle ne voyait que
  l'empreinte du script éphémère lui-même, retiré avant la lecture) — HEAD
  b59bf44 (la passation Task 92), le bundle courant 090-5487f7f UNIQUE, md5
  f73af0a2… MATCH, 36 archives, /test sans copie, GitHub == 5487f7f, le
  jeton OAuth vivant ; la réserve instrumentale RÉINSTALLÉE (le disque labo
  recyclé ENCORE : capstone/keystone/unicorn/pynacl/pefile).
- LE GESTE : tls13-22..28 — le ClientHello COMPOSÉ (114 o FIXES, la
  composition par octets, les valeurs du plan en immédiats, l'aléa @ +6, la
  clé @ +82), le ServerHello TRAITÉ (la marche bornée, chaque confrontation
  NOMMÉE, HRR par OU cumulatif au fixture, LA SUITE lue GROS-BOUTISTE → -5
  la négociation refusée, les extensions inconnues ignorées, l'épuisement
  exact, tls13-13 APRÈS le dernier refus), le CALENDRIER à trois étages
  STRICTS (SEIZE étiquettes HKDF aux fixtures R_LIB_*, TROIS extraits,
  QUATRE déploiements, le condensé du vide par 01+04 — l'erratum n° 2 :
  le contexte de « derived » est Hash(vide) 32 o, JAMAIS zéro octet), le
  FINISHED calculé/vérifié (DEUX modes nommés, le OU cumulatif des 32
  différences, LE test à la fin, le reçu jamais modifié), L'ÉPINGLAGE (le
  SHA-256 du DER sur pile, la comparaison temps constant, -6 nommé), LA
  MACHINE D'ÉTATS (17 520 o à la disposition déclarée, QUATRE événements
  nommés, LA LISTE FERMÉE des compositions, le transcript initialisé puis
  chaque message complet ABSORBÉ AVANT traitement, les coupes du hash sur
  la COPIE, le réassemblage borné 2^14, le certificat extrait (le u24 lu,
  le DÉTROIT de tls13-26), le CertificateVerify absorbé sans vérification
  [le chantier futur nommé], LA DISCIPLINE D'ÉCHEC : tout verdict négatif
  propagé nommé, l'état 5 ne rend PLUS RIEN, un échec n'ÉMET rien) et LA
  ROTULE (le socle à DEUX rappels, L'APPEL INDIRECT DÉCLARÉ, le zéro de
  réception est le refus -7 du kit, aucune copie).
- L'ERRATUM n° 2 consigné sur pièces AVANT la notation (tls13/I/README.md,
  verifier_specs_m9a relu VERT) : (1) le CH du RFC 8448 § 3 compte 196 o
  (trois suites, SNI « server », neuf groupes, quinze sigalgs) — l'égalité
  octet pour octet promise par tls13-22 Q1 et tls13-27 Q3 est IMPOSSIBLE
  PAR CONSTRUCTION contre l'offre minimale scellée (114 o, charte § 1, I3) :
  la preuve est la construction re-jouée + LA SESSION ENTIÈRE contre le
  simulateur, les égalités qui TIENNENT (le SH verbatim, le secret partagé,
  les secrets consignés, les QUATRE chaînes, les DEUX Finished au niveau
  des blocs) ; (2) le contexte de « derived » = Hash(vide) 32 o ; (3) la
  garde de tls13-23 P2 « ≥ 94 » compte l'en-tête deux fois — le SH minimal
  = 90. Les écritures seules sont fautives, jamais la notation.
- LES PREUVES : LE TRANSFERT RFC 8448 BLOC PAR BLOC (le labo
  derive_poignee.py 41 VERTS : le texte officiel parsé, TOUT recoupé par
  code — le couple et le secret par PyNaCl, le calendrier étage par étage,
  les QUATRE chaînes == TRANSFERT_8448, les trois hash dont CH..CV
  RE-DÉRIVÉ, les deux Finished, le vol déverrouillé, le certificat parsé,
  la marche du SH pré-jouée) ; LE HARNAIS tls13/harnais_poignee.py : 52
  contrôles · 52 VERTS × 3 graines — V2 le transfert bloc par bloc (le SH
  verbatim → le secret partagé octet pour octet ; le calendrier sur les
  hash consignés → les secrets ET les QUATRE chaînes ET les clés Finished ;
  le Finished client calculé == a8ec436d…, le serveur vérifié ==
  9b9b141d… ; l'épinglage) ; V4 l'alignement 205 entrées à travers la
  session ENTIÈRE (l'imbrication comptée), le kit INTACT ; V6 le temps
  constant MESURÉ (le verdict du Finished 18 416, l'épinglage 31 405, la
  comparaison HRR 1 239 089 — LE MÊME compte) ; V7 LA SESSION ENTIÈRE
  contre LE SIMULATEUR (deux rappels de machine code : l'émettre qui
  journalise, le recevoir qui sert la cassette ; OUVRIR → l'état 3, le
  journal == NOTRE CH cadré + NOTRE Finished [le SH du RFC servi verbatim,
  le vol re-scellé sous nos clés, le Finished serveur recalculé sur NOTRE
  coupe] ; la session recoupée champ par champ ; ÉMETTRE/RECEVOIR les
  charges du § 3 sous NOS chaînes d'application == la référence ; la
  close_notify des deux côtés ; LA FALSIFICATION : le SH muté → -5,
  l'étiquette mutée → -4, l'empreinte mutée → -6, LA COUPURE DU SOCLE →
  -7, OUVRIR sur l'état 3 → -3, l'état 5 ne rend PLUS RIEN).
- LES FAUTES nommées par le fail-closed (DOUZE — la preuve a corrigé la
  notation ET l'instrument) : la suite en BOUTISME MACHINE (cmp word
  0x1301 ne voit jamais 13 01 — la lecture par xchg), les registres
  haute-octet (r10b/r10h inexistants), cmp imm64 → movabs, LES STUBS et
  rdi/rsi NON-VOLATILES msx64 (push/pop), le stub écrivant la CASE DE
  PILE au lieu de la cellule pointée (le pointeur rechargé, l'écriture À
  TRAVERS), LE KIT (r9 VOLATIL) clobberé par l'appel d'étage — sauvé au
  cadre, l'immédiat sigalgs (0x04080400), les QUATRE copies rep movsq
  rsi/rdi INVERSÉES, LA TRANSCRIPTION MANUELLE du secret partagé (un
  octet mutilé — re-posé PAR DÉRIVATION : jamais recopiée à la main),
  les longueurs de libellés (« c hs traffic » = 12 o), L'INIT du
  transcript manquait à OUVRIR (tls13-01, la session naît VIERGE),
  l'auteur (l'appel indirect sur registre DÉCLARÉ ; TLS06/08/14/15/20/21
  aux SYMBOLES).
- L'ARRÊT : 22 @0xED00 (0x120) · 23 @0xEE20 (0x240) · 24 @0xF060 (0x880) ·
  25 @0xF8E0 (0x100) · 26 @0xF9E0 (0x140) — la poignée finit 0xFB20 SOUS
  les fixtures x25519 immobiles ; 27 @0xFF40 (0xB80) · 28 @0x10AC0 (0xB0) —
  fin du principal 0x10B30, LA MARGE a franchi 0xF000 comme le plan
  l'avait nommé ; les fixtures libellés+HRR @0x10B40..0x10BD0.
- FRONTIÈRES : aucune balise, AUCUN build (le chantier (e) attend — le
  garde VERT, la dette de cérémonie demeure), l'arbre I scellé relu VERT
  AVEC l'erratum (R2 tenue), m8/proxy.exe INTACT, les cinq familles
  précédentes intactes (relues en V0.b), la charte tenue de § 1 à § 8 ;
  consignations : Entrée 175 PAR SCRIPT, PLAN (chantier (b) : la famille
  poignée + le principal + État du programme), worklog +Task ID 93.
- SUITE : (d) le socle socket sys-04+ (la fondation I/O), (e) LA CÉRÉMONIE
  DU SCEAU I de l'ère + le build 1.0.0-dev.1, (f) le terrain — LA GRANDE
  ŒUVRE.
- PASSATION (le même geste, Task ID 93) : le bundle courant
  triade-history-090-b59bf44.bundle DÉPOSÉ AU MIROIR ASSERTÉ, l'ancien
  090-5487f7f ARCHIVÉ VERSIONNÉ, /test sans copie, le push GitHub à la
  pointe — LA SÉRIE 090 POURSUIT — le geste est PASSÉ.

Stage Summary:
- LA SIXIÈME FAMILLE et la dernière de la couche de calcul : LA POIGNÉE
  et LE PRINCIPAL existent en octets — le ClientHello composé, le
  ServerHello jugé champ par champ, le calendrier dérivé étage par étage,
  le Finished prouvé, la confiance épinglée, LA MACHINE orchestre la
  session ENTIÈRE et la rotule la touche au monde — LE CLIENT TLS 1.3
  ENTIER du jalon, zéro délégation cryptographique.
- LA PREUVE A CORRIGÉ LA NOTATION ET L'INSTRUMENT, DOUZE FOIS : le
  boutisme machine, les registres haute-octet, les non-volatiles msx64
  des rappels, le pointeur rechargé, le kit sauvé, les copies remises
  dans le bon sens, le secret RE-DÉRIVÉ après la transcription mutilée —
  le juge est le code, la méthode est la même depuis le geste hkdf.
- LE DOMAINE tls13 EST COMPLET : LES 28 BLOCS notés-mesurés-prouvés, de
  SHA-256 à la machine d'états — reste la fondation socket, la cérémonie
  du sceau, le build, le terrain : LA GRANDE ŒUVRE.
"""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 175" in journal:
        sys.exit("ÉCHEC : Entrée 175 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 174" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 174 introuvable")
    i = journal.index("## Entrée 174")
    j = journal.index(MARQUEUR)
    if not (i < j):
        sys.exit("ÉCHEC : l'ordre 174<marqueur est rompu")
    journal = journal[:i] + ENTREE + "\n" + journal[i:]
    JOURNAL.write_text(journal, encoding="utf-8")
    print("[journal] +Entrée 175 (ordre 174<175<marqueur)")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    log = WORKLOG.read_text(encoding="utf-8")
    if "Task ID 93" in log:
        sys.exit("ÉCHEC : Task ID 93 déjà consignée (rejeu REFUSÉ)")
    if "Task ID 92" not in log:
        sys.exit("ÉCHEC : ancrage Task ID 92 introuvable")
    log = log.rstrip() + "\n\n" + TASK
    WORKLOG.write_text(log, encoding="utf-8")
    print("[worklog] +Task ID 93")
    return 0


if __name__ == "__main__":
    sys.exit(main())
