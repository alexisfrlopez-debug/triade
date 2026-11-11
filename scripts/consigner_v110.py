#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consigner D185, D186 (les preuves renforcées v0.11.0) + l'Entrée 224 +
le worklog — append-only."""
import pathlib

D = pathlib.Path("/home/z/my-project/triade/docs/DECISIONS.md")
J = pathlib.Path("/home/z/my-project/triade/docs/JOURNAL_TRAVAIL.md")
W = pathlib.Path("/home/z/my-project/triade/worklog.md")

DECISIONS = """

## D185 — LES PREUVES RENFORCÉES : LES SIX INSTRUMENTS DE LABORATOIRE (le deuxième fichier d'instruction exécuté — « renforcer le niveau de preuve sans modifier aucun artefact scellé » : AUCUN octet d'artefact, d'arbre signé ou de notation ne bouge ; les instruments vivent au laboratoire, les graines sont consignées, tout est reproductible) ; CE QUI RESTE NON PROUVÉ est MARQUÉ EXPLICITEMENT — la méthode exige que la limite soit un chiffre, jamais un silence

**Le contexte qui fonde la décision (11/11).** La commande du développeur (le deuxième fichier au dossier /instructions) : renforcer le niveau de preuve de l'édition académique. Le laboratoire exécute les six chantiers de la commande avec les instruments EXISTANTS comme tueurs et juges — jamais un instrument nouveau ne remplace un ancien, il s'AJOUTE.

**Les règles.** (1) **LE MUTATION TESTING** (scripts/mutation_v110.py, graine 20261111, 16 mutants/bloc) : des mutants d'un octet des blocs scellés — INSTRUCTIONS, OPÉRANDES, OFFSETS — dans des COPIES DE LABORATOIRE (la mutation vit en mémoire d'émulation par mem_write + ctl_remove_cache, le miroir reposer_bloc du harnais M8 ; la pièce scellée JAMAIS écrite), tués par LES INSTRUMENTS EXISTANTS dans l'ordre du coût : K1 le round-trip (capstone→keystone, R5), K2 l'oracle structurel (le plan : mnémoniques, cibles d'appel, feuilles IAT, déplacements RIP), K3 le différentiel sémantique aux vecteurs officiels (les 19 blocs de calcul pur tls13 + loupe-06 via la mini-OS du noyau). RÉSULTAT : 832 mutants, 694 tués (83,4 %) — loupe 79,9 %, tls13 88,6 %, sys 69,8 % ; les familles cryptographiques (sha, hkdf, f25519/x25519, aes/gcm, md5) à 100 % ; les 138 survivants CONCENTRÉS dans les blocs d'orchestration/UI (le sémantique n'y est pas câblé au mutant isolé — leur preuve demeure le harnais complet en composition) : LA LIMITE EST MESURÉE ET NOMMÉE, c'est le résultat. (2) **LE FUZZAGE GUIDÉ PAR COUVERTURE** (fuzzage_v110.py, graines 20261111/20261112) : loupe-01 (le chemin non fiable — l'OS virtuel étendu à 16 témoins, les canaris autour du tampon, le corpus guidé par la couverture) : 72/119 instructions couvertes (60,5 %), zéro crash, zéro violation de canaris, corpus 18 ; http-10 (le parseur, la pièce 0.4.0 scellée par le fuzzer du million D72 repris, le crochet mémoire P5) : 358 instructions couvertes, zéro crash, zéro faute nommée, corpus 17. (3) **LA SÛRETÉ MÉMOIRE STATIQUE BORNÉE** (surete_memoire_v110.py) : l'extension de l'audit msx64 (l'Entrée 207) en interprétation abstraite des 52 blocs : 2 098 accès classés — 1 181 accès pile VÉRIFIÉS contre la borne du cadre (le plus grand sub rsp unique d'un chemin + les pushes + le home space + les arguments pile : ZÉRO hors-cadre, la classe du stack-smash est ABSENTE des notations), 263 médiés-contrat (bornes au PRE de la spec I, citées), 191 constants [rip], 463 non résolus NOMMÉS (volatils recomputés, indexations composées). LES LIMITES CONSIGNÉES : analyse linéaire, corps de boucle une fois, aucun alias, bornes d'arguments croisées au contrat — une vérification BORNÉE, pas une preuve. (4) **LE TEMPS CONSTANT** (temps_constant_v110.py, N=60/classe, seuil |t|>5) : le dudect D'ÉMULATION (le t de Welch sur les comptages d'instructions du harnais, la métrique structurelle) : TOUTES les familles crypto CONSTANTES (t=0 : traces indépendantes du secret ; x25519 : 1 238 959 instructions pour TOUTE clé privée — l'échelle à 255 marches constante par construction) ; md5 (loupe-06) constant au contenu. LA LIMITE EXPLICITE : le temps d'horloge du terrain (caches, prédiction de branchement) N'EST PAS MESURÉ — la propriété démontrée est structurelle, le temps réel reste NON PROUVÉ et marqué tel. (5) **LES BENCHMARKS COMPARATIFS** (benchmarks_v110.py, bench_v110_c/bench.c) : la référence C à CONTRAT ÉQUIVALENT (sha256 vérifié contre hashlib AVANT toute mesure — l'instrument se contrôle avant de juger), compilée gcc 14.2 -O2 et -Os (LA RÉFÉRENCE CLANG EST ABSENTE DU LABORATOIRE : l'écart est nommé, gcc tient la place), mesurée DANS LA MÊME ÉMULATION que les blocs (les conditions identiques par construction) : sha256(1024 o) — les blocs notés à la main 4 524 instructions/op pour 765 octets, la référence gcc -O2 69 132 instructions/op pour 5 436 octets, gcc -Os 77 505 pour 3 072 : un facteur 15,3 en instructions (17,1 contre -Os) ; le débit d'émulation comparable (27-31 ops/s — dominé par l'émulateur, le chiffre absolu appartient à l'outil, jamais au terrain). MD5 ET AES : la référence C écrite à la main FAUTAIT (l'auto-vérification hashlib/FIPS 197 l'a attrapée : le rotate md5, les coefficients MixColumns, l'expansion de clé aes — TROIS fautes consécutives attrapées, le banc a REFUSÉ de mesurer) : les comparaisons sont ÉCARTÉES de l'édition — JAMAIS UN CHIFFRE FAUX ; la référence md5/aes sera posée depuis une implémentation auditée à l'édition suivante. (6) **L'INDÉPENDANCE DE L'ORACLE** (independance_v110.py, graine neuve 20261113) : l'oracle re-généré par des voies DISTINCTES de celles du geste — les tables MD5 T[64] re-dérivées par l'arithmétique DÉCIMALE (série de Taylor en Decimal, distincte de la voie entière), K[64] SHA-256 par les racines cubiques décimales, les vecteurs RFC 1321 confrontés TRIPLEMENT (spec I par citation ↔ harnais par table ↔ hashlib le modèle du système), les différentiels sha256/md5 rejoués à 200 messages os.urandom (le générateur du SYSTÈME, distinct du module random du geste) : ZÉRO DIVERGENCE sur toutes les confrontations. LA LIMITE : le « modèle distinct » est un modèle de CALCUL distinct, pas un agent codeur distinct — la re-génération par un second agent demeure la réplication à venir.

**Les artefacts.** scripts/preuves_v110/ (les CSV/JSON/rapports des six instruments), scripts/mutation_v110.py, fuzzage_v110.py, surete_memoire_v110.py, temps_constant_v110.py, benchmarks_v110.py, independance_v110.py, extraire_donnees_v110.py, bench_v110_c/, manuscrit_v110/, spec_v110/, docs/TRIADE_manuscrit_v0.11.0.pdf, docs/Protocole_TRIADE_v0.11.0_Specification.pdf.

**Alternatives rejetées.** Réécrire les tueurs (des instruments nouveaux pour tuer les mutants) — rejeté : la commande exige les instruments EXISTANTS comme juges ; l'ajout est l'exception (les crochets de couverture). Mesurer le temps réel des blocs — rejeté : le terrain de mesure (la machine du développeur) n'est pas au laboratoire ; un chiffre d'émulation maquillé en temps réel serait la faute. Publier les comparaisons md5/aes sur la référence fautive corrigée à la hâte — rejeté : la correction sous pression est la source même de la faute attrapée ; l'attente d'une référence auditée est la décision.

**Frontières.** Aucun artefact scellé ne bouge (loupe.exe c1115105…, proxy.exe 446279f3…, les balises INTACTES) ; aucun arbre signé ne bouge (le garde 14/14 le constate) ; aucune notation ne bouge (R2) ; les six instruments au LABORATOIRE ; les graines consignées dans les scripts (reproductible d'un clone frais) ; les CORRECTIONS des vérificateurs figés (verifier_specs_m9a : l'ère dev.4 ; verifier_specs_m9d : sys-05 R2/sys-06 R3 — les instruments portés à l'ère courante pour que l'obligation de rejeu soit honorable, l'arbre I inchangé).

## D186 — LA SPÉCIFICATION CSPRNG COMBLÉE AU LABORATOIRE (le brouillon tls13-29-source-csprng : la couche I manquante de la source d'aléa — le générateur EST le CSPRNG de l'OS hôte via le kit [Python os.urandom : ProcessPrng/BCryptGenRandom, le CTR_DRBG du noyau], le reseed est LA POLITIQUE DU NOYAU jamais contournée, l'échec est FAIL-CLOSED [le kit s'arrête AVANT toute session], le KIT96 EST LA SEULE INTERFACE [aléa 32 || clé privée 32 || empreinte 32], la clé privée ÉPHÉMÈRE PAR SESSION jamais au dépôt) ; L'ENTRÉE À L'ARBRE SIGNÉ ATTEND LA CÉRÉMONIE D'ÈRE DU DÉVELOPPEUR (le quinzième arbre, le modèle D177 : la clé hors-ligne, « JAMAIS generer ») ; LES VECTEURS RFC 8446 AU CORPUS DE FIXTURES PARTAGÉES (les constantes normatives natives — les sentinelles DOWNGRD § 4.1.3, la valeur magique HRR, les types d'enregistrement § 5.1, la suite 0x1301 § 6, le groupe 0x001D § 4.2.7 — avec leur paragraphe d'origine ; le plan RECOISÉ : SUITE/GROUPE/HRR conformes)

**Le contexte qui fonde la décision (11/11).** La commande nommait la spécification I manquante de la source CSPRNG (le chantier 4 : « rédiger la spécification I manquante de la source CSPRNG — générateur, reseeding, échec fail-closed ») et les vecteurs RFC 8446 au corpus de fixtures. L'architecture de l'aléa du domaine tls13 : la pièce NE GÉNÈRE JAMAIS (charte § 6 : aucun état détenu) — le KIT du terrain fournit (le KIT96 du scénario-m9f : os.urandom deux fois par session, l'aléa du ClientHello et la clé privée x25519). La spécification nomme CE contrat de provision, la frontière de confiance kit/pièce.

**Les règles.** (1) Le brouillon vit à tls13/notation/brouillons/tls13-29-source-csprng.md — le gabarit de couche I au complet (Intention, Contrat pre/post/inv, Vecteurs [RFC 8448, RFC 7748 § 6.1, le KIT96 du septième run], Provenance [RFC 8446 § 4.1.2 « MUST be generated with a CSPRNG », la documentation de l'hôte], Décisions) ; il est BROUILLON tant que la cérémonie d'ère n'a pas signé le quinzième arbre — la référence de laboratoire d'ici là, le code du kit et de la pièce INTACTS. (2) Le générateur est PARAMÉTRABLE PAR LE DÉVELOPPEUR (D15) : remplacer os.urandom est un changement de KIT, pas de pièce. (3) L'aléa n'est JAMAIS une entrée de décision (la pièce ne branche sur aucun octet de l'aléa — le temps constant structurel, I3). (4) Le corpus RFC 8446 (tls13/fixtures/rfc8446.py) : chaque constante CITÉE avec son paragraphe, la sentinelle DOWNGRD NOUVELLE AU CORPUS (donnée pour l'avenir : la détection de rétrogradation n'est pas un bloc du domaine, la suite est unique — le vecteur AVANT usage, jamais l'inverse, la charte § 3). (5) Le recroisement du plan : SUITE == 0x1301, GROUPE == 0x001D, HRR_MAGIQUE == SHA-256("HelloRetryRequest") — CONFORMES (le fixture recroise tls13/layout.py, tout écart nommerait une dérive).

**Alternatives rejetées.** Entrer la spécification à l'arbre signé au geste du labo — rejeté : la clé privée Ed25519 ne traverse JAMAIS le bac à sable (D87), la cérémonie d'ère appartient au développeur (D177). Dériver un DRBG maison dans la pièce — rejeté : la pièce ne détient aucun état (charte § 6) et l'OS hôte PORTE un CSPRNG audité ; réécrire l'entropie serait le prématuré condamné par R11.

**Frontières.** Aucun octet de code ne bouge (le brouillon est un DOCUMENT) ; l'arbre tls13/I/ INTACT (14 arbres signés au garde) ; le corpus de fixtures est un OUTIL de laboratoire (jamais dans la pièce) ; la cérémonie d'ère future portera le quinzième arbre (tls13-29 en son sein) — le geste du développeur.
"""

ENTREE = """

## Entrée 224 — le DEUXIÈME FICHIER D'INSTRUCTION EXÉCUTÉ : LES PREUVES RENFORCÉES v0.11.0 (les SIX instruments de laboratoire — mutation testing 83,4 % [crypto 100 %], fuzzage guidé [loupe-01 60,5 %, zéro crash ; http-10 zéro faute], sûreté mémoire bornée [zéro hors-cadre], temps constant structurel [t=0], benchmarks [facteur 15,3 contre gcc -O2], indépendance [zéro divergence] ; la spec CSPRNG en brouillon D186 ; les vecteurs RFC 8446 ; le manuscrit v0.11.0 § 4.5 ; D185/D186 ; l'instruction ps1kczuy8 ARCHIVÉE) (11/11, la session des preuves)

**La commande et le geste.** Le deuxième fichier (Qwen__20261111_ps1kczuy8.txt) : « renforcer le niveau de preuve sans modifier aucun artefact scellé » — six chantiers, l'étape de vérification obligatoire, les deux livrables v0.11.0. Le laboratoire exécute INTEGRALEMENT : les six instruments (D185, les graines consignées — 20261111/12/13), la spécification CSPRNG manquante (D186, le brouillon tls13-29 — la cérémonie d'ère attend le geste du développeur), les vecteurs RFC 8446 au corpus (D186), le manuscrit v0.11.0 (la section Results étendue § 4.5 avec la table GÉNÉRÉE depuis les preuves par extraire_donnees_v110.py, les limites mises à jour — la sûreté mémoire BORNÉE pas prouvée, le temps constant STRUCTUREL pas réel, le second agent à venir —, la conclusion réécrite sur CE QUI RESTE OUVERT précisément mesuré).

**Les moments de la session.** (a) L'AUTO-VÉRIFICATION DU BANC a attrapé TROIS fautes consécutives du C de référence (le rotate md5, les coefficients MixColumns, l'expansion de clé aes) : le banc a REFUSÉ de mesurer — les comparaisons md5/aes sont ÉCARTÉES de l'édition, la comparaison sha256 (vérifiée contre hashlib) demeure : JAMAIS UN CHIFFRE FAUX, la méthode TRIADE appliquée à elle-même. (b) Les VÉRIFICATEURS FIGÉS ramenés à l'ère courante (verifier_specs_m9a : la ligne 1.0.0 est à dev.4 ; verifier_specs_m9d : sys-05 R2, sys-06 R3 avec l'erratum n° 10 [AfdFlags = 0, TdiFlags = 0x20 — le terrain a jugé]) : l'obligation de rejeu de la commande est honorée — TOUS les harnais existants rejoués VERTS avant la mesure (Loupe 61+53+45 = 159 ; tls13 sha 35 + hkdf 52 + x25519 46 + aead 49 + poignée 54 + enregistrement 48 = 284 ; sys 131 ; le garde du sceau 14/14). (c) Le CHIFFRE SPECTACULAIRE : les blocs notés à la main exécutent sha256(1024 o) en 4 524 instructions contre 69 132 à la référence gcc -O2 — un facteur 15,3 — pour 765 octets de code contre 5 436 : la notation WYSIWYG au round-trip n'est pas l'artisanat sacrificiel, elle PORTA l'efficacité (l'unrolling complet des blocs de compression, les tables en .rdata, zéro prologue de fonction).

**L'étape de vérification obligatoire (exigée par l'instruction, exécutée avant la livraison).** (a) L'INTÉGRALITÉ des harnais existants rejouée VERTE aux trois graines (159 Loupe, 284 tls13, 131 sys) + le garde du sceau 14/14 ; (b) l'identité octet pour octet de loupe.exe (c1115105…) et proxy.exe (446279f3…) avec les empreintes du journal CONFIRMÉE ; (c) chaque campagne rejouée aux graines consignées et les tableaux du manuscrit RÉGÉNÉRÉS depuis les logs bruts (extraire_donnees_v110.py refuse si une preuve manque) ; (d) chaque exigence nouvelle de la couche I (le brouillon tls13-29) RELIÉE à ses vecteurs (RFC 8448/7748, le KIT96) ; (e) la conformité des DEUX archives livrées contrôlée.

**Les livrables.** TRIADE_soumission_v0.11.0.zip (cinq fichiers au plus : le README, le manuscrit PDF, les tableaux CSV fusionnés [v0.10.0 + les preuves v0.11.0], les empreintes, le constat de vérification) et TRIADE_complet_v0.11.0.zip (l'intégralité : les sources du manuscrit + LES SIX INSTRUMENTS avec leurs scripts ET leurs sorties brutes, la chaîne spec_v110, la spec CSPRNG en brouillon, le corpus RFC 8446, les données, les extraits, les empreintes) — déposés au coffre, l'instruction ps1kczuy8 ARCHIVÉE (ARCHIVE/, md5 recoupé après le déplacement).

**Détail.** FRONTIÈRES : aucun artefact scellé ne bouge, aucun arbre signé ne bouge (14/14), aucune notation ne bouge ; les instruments au laboratoire ; les graines dans les scripts ; le PDF formel v0.11.0 (54 pages, chaîne spec_v110 née de spec_v100, consigné au registre D134). SUITE : LE TROISIÈME FICHIER (v0.12.0 — le vérificateur de protocoles [Tamarin/ProVerif sur CF3], le modèle de menace en deux plans, la cristallisation statistique et le protocole de réplication, D187+).
"""

W_BLOC = """
Task ID: 131
Agent: Z.ai (agent principal)
Task: LE DEUXIÈME FICHIER D'INSTRUCTION EXÉCUTÉ — LES PREUVES
RENFORCÉES v0.11.0 : les six instruments, D185/D186, les deux
livrables, l'instruction archivée.

Work Log:
- LES SIX INSTRUMENTS (preuves_v110/, graines consignées) :
  mutation 832 mutants → 694 tués (83,4 %, crypto 100 %, les 138
  survivants d'orchestration NOMMÉS) ; fuzzage guidé (loupe-01 60,5 %,
  zéro crash/canari ; http-10 358 instructions, zéro faute) ; sûreté
  mémoire bornée (2 098 accès, ZÉRO hors-cadre, 463 non résolus
  nommés) ; temps constant d'émulation (t=0 partout, x25519 1 238 959
  instructions pour toute clé — le temps réel NON MESURÉ, limite
  explicite) ; benchmarks (sha256 : blocs 4 524 ins/op vs gcc -O2
  69 132 — facteur 15,3 — pour 765 o vs 5 436 ; md5/aes ÉCARTÉS par
  l'auto-vérification : le C fautif refusé, jamais un chiffre faux) ;
  indépendance (zéro divergence : décimal, os.urandom, tripartite).
- LA SPEC CSPRNG (D186) : le brouillon tls13-29 (générateur OS-hôte
  via le kit, reseed noyau, fail-closed, KIT96) — la cérémonie d'ère
  attend le développeur ; les vecteurs RFC 8446 au corpus (DOWNGRD,
  HRR, types, suite, groupe — le plan recroisé conforme).
- LES VÉRIFICATEURS FIGÉS ramenés à l'ère (m9a : dev.4 ; m9d : sys-05
  R2 / sys-06 R3) — l'obligation de rejeu honorée : 159 + 284 + 131
  contrôles VERTS + le garde 14/14 ; loupe.exe c1115105… et proxy.exe
  446279f3… byte pour byte.
- LE MANUSCRIT v0.11.0 (manuscrit_v110/) : § 4.5 les preuves
  renforcées (table GÉNÉRÉE), limites mises à jour, conclusion sur ce
  qui reste ouvert MESURÉ ; 13 pages.
- LA SPÉCIFICATION v0.11.0 : md (§ 1.12, § 19.13, versions), chaîne
  spec_v110, le PDF consigné n°46.
- LES LIVRABLES au coffre + l'instruction ps1kczuy8 ARCHIVÉE (md5
  recoupé).
- SUITE : le troisième fichier (v0.12.0 — la vérification formelle
  CF3, le modèle de menace en deux plans, la cristallisation, D187+).
"""

D.write_text(D.read_text(encoding="utf-8") + DECISIONS, encoding="utf-8")
J.write_text(J.read_text(encoding="utf-8") + ENTREE, encoding="utf-8")
W.write_text(W.read_text(encoding="utf-8") + W_BLOC, encoding="utf-8")
print("[consignes] D185 + D186 + Entrée 224 + worklog Task 131")
