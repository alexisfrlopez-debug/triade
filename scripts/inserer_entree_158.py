#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_158.py — JOURNAL_TRAVAIL.md : insère l'Entrée 158 PAR
SCRIPT (ordre 157<158<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 158 — LE CHANTIER M8-(c) OUVERT SUR UNE DÉCOUVERTE : LE GARDE-SCEAU NOMME LA DETTE DE CÉRÉMONIE DE L'ÈRE (le registre figé m0 étendu au M8-(a) SANS re-signature — un diff d'intention non signé, D87) ; LA CÉRÉMONIE DU SCEAU I DE L'ÈRE M8 EST EXIGÉE AVANT TOUT BUILD (la remise du développeur, sa clé hors-ligne) ; LE BUILD 0.9.0-dev.1 ÉCRIT ET SES COMPOSANTS VÉRIFIÉS SUR PIÈCES DÉTACHÉES (l'exe composé 44 544 o, sha256 1492b0bc…, DÉTERMINISTE — AUCUN artefact écrit : le garde est armé, fail-closed)

LA DÉCOUVERTE (le premier geste du build — sur pièces, jamais sur mémoire) : le garde-sceau de l'Intention (D87, v06/sceau_I.py — « les chaînes de build appellent garde() et refusent un arbre divergé ») REFUSE au premier appel du chantier (c) : **l'arbre m0 a divergé — fichier modifié : README.md** (code 10 : « diff d'intention non signé : la clé hors-ligne du développeur est requise »). La mesure sur pièces : le M8-(a) (ab41def, D160 règle 6) a étendu le REGISTRE FIGÉ m0/I/README.md (le domaine `sys` créé, réservé M8 — « un identifiant n'est jamais réutilisé ») SANS cérémonie de re-signature ; les TROIS spécifications hello-01/02/03 sont INTACTES (seul le registre diverge — les sha comparés au manifeste signé de la cérémonie 0.6.0 du 04/11) ; l'arbre m8 est ABSENT de la table du sceau (la couche I du domaine, avec ses errata D161, n'a jamais été signée — l'arbre m5 lui-même ne fut signé qu'à la cérémonie 0.6.0). LE SCEAU FAIT SON TRAVAIL : le refus est la preuve vivante que le registre a mué sous signature — c'est exactement ce que D87 a bâti. La dette est contractée au M8-(a), elle est ÉCHUE au premier build.

LA CÉRÉMONIE DE L'ÈRE M8 (le geste EXIGÉ — il appartient au développeur) : la table du sceau ÉTENDUE au nouvel arbre (v06/sceau_I.py : `m8 : proxy.exe (domaine sys, syscalls directs), sys.1` — sceau_I.py n'est PAS couvert par l'arbre v06 [CF2/CF3/README seulement] : aucune cascade de signature) ; `sceau_I.py preparer` joué AU geste : **a-signer.txt écrit (12 arbres, les empreintes vivantes)** — la remise minimale du développeur : **m0** (le registre étendu) et **m8** (le domaine sys) signés hors-ligne avec SA clé Ed25519, puis `sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt` (l'atomicité de cérémonie : clé, signatures et manifestes basculent ENSEMBLE ou pas du tout — la remise du 04/11 fut de 11 lignes, celle-ci en demande 2). Le labo NE SIGNERA JAMAIS à sa place : la clé de TEST (lab, D105) DÉCLASSERAIT l'état « réelle » du dépôt — une régression de preuve, refusée sans décision nommée du développeur.

LE BUILD ÉCRIT (m8/build_m8.py — le modèle build_m5, la chaîne complète) : LE GARDE ARMÉ EN TÊTE (ARBRES_GARDE_M8 = m0-m5 + m8 — le refus CONSTATÉ au geste : le build s'arrête avant TOUT octet avec la notice de cérémonie) ; L'HÉRITAGE RE-VÉRIFIÉ DE BOUT EN BOUT (B4.assembler_tout_m4 + B3 + B5.assembler_tout_m5 — round-trip 100 % par bloc, les oracles structurels M3 524 + M4 492 + M5 312 verrous — et L'IMAGE M5 COMPOSÉE confrontée OCTET PAR OCTET au scellé 0.6.0 : sha c1e46fb0… MATCH — la carte génération 7 scellée version=0.6.0 prouve CES octets, le fait de carte D104) ; L'ORACLE STRUCTUREL M8 (54 verrous — LA RÈGLE DU DOMAINE : **AUCUN IAT PAR BLOC sys** [charte § 3, la preuve structurelle] ; le site syscall UNIQUE dans sys-01 [Q1], les SIX octets du trombone exacts, rax JAMAIS écrit avant le site [I2], AUCUN prologue [I3], le ret immédiat [I6] ; AUCUN syscall dans sys-02/sys-03 [I4 — lire n'est pas émettre] ; le MOTIF_STUB AVANT l'imm32 [I3 de sys-02, l'ordre des instructions constaté], memcmp libc-02 @0x1180 le SEUL appel [I2], la borne NumberOfNames lue UNE fois [I1] ; l'ordre résoudre-puis-émettre dans sys-03 [I3], l'échec court-circuité par js [I5], les fixtures CITÉES par déplacement [I4]) ; LA COMPOSITION (m8/composer_image_m8 : .text5 NOUVELLE — la réserve int3 0xA240+, les TROIS slots D161 [code + padding NOP] ; .rdata : l'héritage M5 octet pour octet + les fixtures du domaine dans la zone VIERGE vérifiée [le span-nom « NtWriteFile » 11 o @0x2EC0 SANS NUL — P1 est un SPAN ; la LIGNE de hello-02 byte-exact le fixture M0 @0x2ED0] + LA VERSION 0x00090001 @0x2820 [LE delta R10 documenté : geste de BUILD, JAMAIS un scellage — la 0.9.0 finale attend le terrain vert du chantier (d)]) ; L'ÉDITEUR PE32+ À SEPT SECTIONS (NumberOfSections 7, .text5 RX @0xA000 raw 0x8E00, SizeOfImage 0xC000, taille 0xAE00, l'entrée PE 0x8C80 INCHANGÉE [le principal n'est PAS recâblé, R7 — le domaine est la pièce rapportée], les 7 en-têtes [608 o] TIENNENT dans la marge 0x400 : LE DÉCALAGE DE PACKAGING D94 N'EST PAS REJOUÉ, les six premières sections raw inchangées) ; LA VALIDATION PE (les imports INCHANGÉS — kernel32 x2 descripteurs + ws2_32 + secur32 : le domaine ne déclare RIEN, la preuve structurelle ; les portes R10 28 entrées + M5 auto-consistantes ; la réserve .rdata 0x2F00+ VIERGE ; R_POLITIQUE 0) ; LA PREUVE R7 (les sections .text/.text2/.data/.text3/.text4 OCTET POUR OCTET == scellé ; .rdata identique SAUF la version et les fixtures ; les trouées du domaine exigées VIERGES DES DEUX CÔTÉS — 41 blocs hérités octet-identiques).

LES COMPOSANTS VÉRIFIÉS SUR PIÈCES DÉTACHÉES (le garde n'est PAS appelé — ce n'est pas construire(), c'est le test du code ; AUCUN artefact écrit, AUCUNE carte déposée) : l'héritage complet VERT de bout en bout ; l'oracle structurel M8 54 verrous ; la composition + le PE validé ; la preuve R7 ; **l'exe composé : 44 544 o (0xAE00), sha256 1492b0bc0792e1ab…, RE-CONSTATÉ IDENTIQUE au second passage (le déterminisme — le futur artefact)** ; les TROIS oracles appelés depuis le build sur les blobs (l'oracle M4 héritage 30 cas + l'oracle M5 héritage 29 cas + LE HARNAIS M8 le domaine 61 cas — volume réduit, le code d'appel validé). LA CARTE GÉNÉRATION 8 (m8/carte_m8.py — le modèle carte_m5 : le sel Argon2id propre à la génération, le sel HKDF M8, CARTE_DIR m8/carte/) : les primitives testées À BLANC dans un répertoire temporaire (JAMAIS dans m8/carte/ — aucune carte ne préexiste à son build) : charger_secrets (lignée D80 + graine durable D144), Argon2id + HKDF, XChaCha20-Poly1305, signature Ed25519, round-trip complet, listes blanches D15 — **la clé publique e9cd8c549485… : LE TÉMOIN NE BOUGE PAS** (la même graine qui signe les cartes depuis la re-scellée 0.5.1). LE HARNAIS ÉTENDU (m8/harnais_sys.py : la fonction executer(blobs, graine, volume) — le point d'entrée du build, modèle oracle_m5 ; l'Emulateur re-constate byte-égal les octets du build avec l'assemblage des notations : JAMAIS deux sources de vérité ; les modules déjà chargés RÉUTILISÉS — une seule instance du builder, la leçon D158 appliquée au mode build ; le re-jeu : 61/61 en mode autonome ET en mode blobs). L'ARRÊT D162 DES OFFSETS FICHIER (m8/layout.py, la source unique) : .text5 raw **0x8E00** (après .text4, les six premières raw inchangées), taille de fichier **0xAE00** — la 7e en-tête vit dans la marge des en-têtes, aucun décalage.

**Détail.** FRONTIÈRES : AUCUN artefact écrit (m8/proxy.exe N'EXISTE PAS — il naîtra de construire() après la cérémonie, le garde armé) ; AUCUNE carte déposée ; AUCUNE balise posée (la 0.9.0-dev.1 viendra du build — geste de BUILD jamais scellage ; la 0.9.0 attend le terrain vert du chantier (d)) ; le scellé 0.6.0 (m5/proxy.exe, c1e46fb0…) INTACT — l'ancre R7 de l'ère ; l'état de clé du sceau « réelle » INTACT (le labo ne signe rien : ni la clé de test [déclassement], ni une clé inventée) ; le labo ne connaît toujours pas le SSN du terrain (le chantier (d) lira le VRAI ntdll). Livrables : m8/build_m8.py (construire + verifier), m8/carte_m8.py (génération 8), m8/harnais_sys.py étendu (executer), m8/layout.py ARRÊTÉ (D162 : TEXT5_FILE 0x8E00, TAILLE_FICHIER 0xAE00), v06/sceau_I.py (la table étendue : m8 sys.1), v06/sceau-I/a-signer.txt (LA CHARGE DU DÉVELOPPEUR) ; consignations : la présente Entrée PAR SCRIPT, D162 PAR SCRIPT (à la suite de D161), PLAN (le chantier (c) OUVERT — la cérémonie attend), worklog +Task ID 76 ; scripts suivis : inserer_entree_158.py, inserer_d162.py.

- SUITE : LA CÉRÉMONIE DE L'ÈRE M8 (la remise du développeur : m0 + m8 signés hors-ligne, a-signer.txt) → LE DÉPÔT (sceau_I.py deposer) → LE GARDE REPASSÉ → LE BUILD EXÉCUTÉ (construire : l'artefact m8/proxy.exe 0.9.0-dev.1 + la carte génération 8 + le verrou croisé, la cristallisation au fil des vérifications) ; puis le chantier (d) — le kit terrain au coffre /test, le VRAI ntdll lu sur la machine du développeur.

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 158" in texte:
    sys.exit("ECHEC : l'Entrée 158 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i157 = texte.find("## Entrée 157")
if i157 < 0:
    sys.exit("ECHEC : l'Entrée 157 introuvable (l'ordre 157<158)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j157 = nouveau.find("## Entrée 157")
j158 = nouveau.find("## Entrée 158")
jm = nouveau.find(MARQUEUR)
if not (0 <= j157 < j158 < jm):
    sys.exit("ECHEC : l'ordre 157<158<marqueur n'est pas tenu "
             f"({j157}, {j158}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 158 insérée (l'ordre 157<158<marqueur constaté)")
