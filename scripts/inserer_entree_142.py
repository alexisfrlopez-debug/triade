#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_142.py — JOURNAL_TRAVAIL.md : insère l'Entrée 142 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
141 < 142 < marqueur recoupé — le même contrat que les entrées 127-141)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 142 — LE CHEMIN rc.2 ACCOMPLI : l'idiome hérité http-02:R1 RESTAURÉ dans la ligne de flux (notation corrigée, +16 o, slot préservé), le CONTRÔLE D146 né en livrable du jalon (m5/controle_base_reelle.py — le rc.1 y crashe à l'identique, FALSIFIABILITÉ PROUVÉE ; le rc.2 y SERT la requête routée), cristallisation repartie à zéro 52/52 × 10/10, SCELLAGE 0.6.0-rc.2 (sha c1e46fb0…) AVEC le contrôle D146 EXÉCUTÉ AU SCELLAGE même ; kit e4 LIVRÉ (scénario e3 repris TEL QUEL, proxy remplacé) — la finale attend le geste terrain

**Le correctif de notation (la première pièce du chemin proposé à l'Entrée 141).** Le BROUILLON m5/notation/brouillons/http-10-session-r3.asm est la source (la chaîne de vérité D96 : brouillon → auteur → notation) : la zone fautive (Q6, préfixe de la ligne de flux, lignes ~237-246) portait « mov rdx, qword [r11] » passant le RVA nu à .copier. L'IDIOME HÉRITÉ http-02:R1 RESTAURÉ : la base d'image est dérivée de l'adresse complète de la table (lea r11, [rip + TAB_METHODES]) moins son RVA (sub rdx, 0x2410 — immédiat numérique, pratique http-02 « mov r12d, 0x2830 » ; sub 64 bits OBLIGATOIRE : la base réelle 0x140000000 tient sur 33 bits, sub edx la tronquerait), puis « mov rax, [r11] ; add rax, rdx » AJOUTE la base au RVA lu avant l'appel. CINQ instructions nouvelles (+16 o), registres morts seuls (rax/r10/r11/rcx/rdx/r8 — le commentaire d'arrêt du brouillon les nomme), .copier préservé (rbx/r12/r13 intouchés) ; l'arithmétique recoupée : 0x84f3 + 7 − 0x60ea = 0x2410. La notation RÉGÉNÉRÉE par outils/auteur.py : g80002 2719 o (2703+16), padding 49→33 o, LE SLOT 2752 o NE BOUGE PAS (aucune adresse de bloc ne bouge, .copier glisse 0x8bf3→0x8c03, recalculé) ; g80001/g80003 inchangés. L'ARBRE m5/I NE CHANGE PAS (la spec Q6 exige « méthode (texte R_TAB_METHODES) » — c'est l'implémentation qui était fautive, le contrat est respecté PAR le correctif) : LE SCEAU-I m5 RESTE VALIDE, aucune cérémonie. À BASE 0 le code corrigé reste vert (base 0 + RVA = adresse : le piège D146, mais l'oracle différentiel demeure juge de la logique).

**Le contrôle D146, LIVRABLE DU JALON (m5/controle_base_reelle.py — modèle scripts/reproduire_run_e3.py D52h, la règle devenue OUTIL).** Moteur : image PE ENTIÈRE chargée à la base préférée 0x140000000, IAT remplie par la MARCHE des descripteurs (motif D54), ligne de commande réelle (« …proxy.exe » --relever-https), fils coopératifs par CreateThread shimmé (console + sessions), sockets scriptées, séquence e3 EXACTE (sonde TCP morte puis sonde d'armement 51 o). VERDICT fail-closed en TROIS pièces : (a) AUCUNE faute mémoire — sinon NOMMÉE (adresse, instruction, bloc, anneau) ; (b) la ligne de flux ÉMISE avec la méthode EN TEXTE ; (c) le CLIENT SERVI (réponse ou refus nommé du contrat). FALSIFIABILITÉ PROUVÉE SUR LE SCELLÉ FAUTIF : le rc.1 y ÉCHOUE à l'identique du terrain (« FAUTE MÉMOIRE acces=19 adresse=0x24A0 ; RIP=0x140008C06 (http-10:R3 @0x81C0+0xA46) sur : movzx eax, byte ptr [r12] » — KO a/b/c, verdict KO) ; le dev.2 y est VERT : ligne de flux « flux GET 127.0.0.1:443 v=6 e=51 s=40 » ÉMISE (la méthode lue de R_TAB_METHODES À LA BASE RÉELLE — e=51 = les octets de la requête, v=6 = l'issue de secours du labo sans vraie Schannel, frontière D146 assumée), client servi (« HTTP/1.1 502 Passerelle inaccessible » 40 o — le refus nommé du contrat sur poignée shimmée défaillante SEC_E_NO_AUTHENTICATING_AUTHORITY), getaddrinfo + connect 443 (le relèvement opéré), ExitProcess propre.

**Les versions et la licence (l'amendement D147, modèle D35 — M3).** layout.py : VERSION_DEV1 → « 0.6.0-dev.2 », VERSION_U64_DEV1 → 0x00060001 (R10 : monotonie > 0x00060000 = rc.1), VERSION_RC1 → « 0.6.0-rc.2 ». L'anti-rollback de build_m5.py AMENDÉ : la reconstruction est autorisée EXACTEMENT pour 0.6.0-rc.1 → 0.6.0-dev.2 (LICENSE dict à UNE entrée, motif constaté : le crash du run e3, Entrée 141/D146 — R4 contrat stable) ; toute autre reconstruction sous balise scellée reste REFUSÉE. Le scellage gagne l'exigence D146 MÉCANIQUE : _sceller exécute le contrôle base réelle AVANT la bascule de balise et REFUSE s'il n'est pas vert (« AUCUN scellage rc/final dans cet état ») — la règle vit au code, pas au bon vouloir. SHA_PROXY_060_RC1 conservé en mémoire du scellé fautif (JAMAIS reconstruit) ; SHA_PROXY_060_DEV2 posé après constat.

**La chaîne rc.2.** BUILD dev.2 : R5 100 % (g80002 round-trip 541/541 — le bloc corrigé), oracle structurel 524+492+312 verrous, R7 L'IMAGE M4 == LE SCELLÉ 0.5.1 OCTET POUR OCTET (38 blocs réutilisés, deltas documentés), oracle M4 560 cas + M5 365 cas verts (falsification détectée), PE 36 352 o TAILLE INCHANGÉE, carte génération 7 (lignée D80, graine durable D144), sha c1e46fb0b857b6f33c67aa7f26a1db3064f2e3adbd528414116b497220b6a20c. CRISTALLISATION REPARTIE À ZÉRO (D35) : DIX passages (le build + --verifier graines 20261104→20261112, volume complet), 52/52 blocs × 10/10, sha STABLE à travers tous. SCELLAGE rc.2 : garde sceau-I (6 arbres verts, clé réelle), CONTRÔLE D146 VERT EXÉCUTÉ AU SCELLAGE (le verdict vit au journal du scellage), cristallisation 52/52 × 10/10 vérifiée, conformité § 8.2 VERTE (58 contrôles, les DEUX portes vivantes), bascule dev.2 → rc.2 dans frag-bld (occurrence unique assertée), re-scellage EN MÉMOIRE vérifié avant l'unique écriture, verrou croisé R8 52 empreintes, proxy.exe INTACT (le scellage est un fait de carte). GARDES CONSTATÉES APRÈS : re-scellage REFUSÉ (« balise 0.6.0-dev.2 attendue une fois : 0 occurrence »), reconstruction REFUSÉE (« carte scellée (0.6.0-rc.2) : reconstruction interdite ») — l'anti-rollback est VIVANT.

**Le kit e4 (assembler_kit_e4.py, modèle e3 ; la 4e pièce du chemin).** Base : le kit e3 LIVRÉ rapatrié du coffre (m5b-kit-e3.zip, md5 981b1a5b… RECOUPÉ — le coffre fait foi). TROIS pièces remplacées : (1) proxy.exe rc.1 FAUTIF → rc.2 (l'égalité de la base au scellé fautif ASSERTÉE 4b8f6af6…/72cf8fdd… : le remplacement est un FAIT nommé) ; (2) LISEZMOI-KIT e4 (le proxy documenté, le correctif expliqué, les contingences) ; (3) LISEZMOI-preuves e4 (les MÊMES pièces — le scénario est repris). LE SCÉNARIO EST CELUI DE LA VAGUE e3 REPRIS TEL QUEL (byte-identique, asserté des deux côtés : base == dépôt, e4 == copie) : la garde fonctionnelle D145 (la sonde forme-absolue + page 200), les verdicts post-mortem, Edge par VersionInfo, le décor v8 — le run e3 s'est arrêté au crash du proxy AVANT le navigateur, le scénario n'avait rien à se reprocher. 52 reprises assertées (fixtures v5, autorité, python, wsb réseau coupé). m5b-kit-e4.zip 11 193 488 o, md5 0922b281352c02b3ed25cf9a778ba664 ; intégrité re-vérifiée à la sortie PUIS VÉRIFICATION DISQUE INDÉPENDANTE (kit-e4-verif/, proxy relu == rc.2, scénario relu == e3, fixtures, wsb, BOM/CRLF, marqueurs).

**La livraison D143 (livrer_vague_e4.py, chaque mutation RECOUPÉE PAR RELECTURE).** Vague e3 CONSOMMÉE ARCHIVÉE (LISEZMOI-m5b-e3.txt + scenario-m5b-e3.ps1 + m5b-kit-e3.zip → archives-livraisons/vagues-m5b/, md5 recoupés avant/après) ; vague e4 POSÉE (m5b-kit-e4.zip + scenario-m5b-e4.ps1 + LISEZMOI-m5b-e4.txt, md5 distants == locaux) ; preuves-m5b/LISEZMOI-preuves.txt → liste e4 (relu) ; index des archives mis à jour (bloc « vague e3 consommée » après le bloc e2, relu == réécrit) ; racine /test = EXACTEMENT 8 entrées D143 (vague courante e4 + corriger-wsb + preuves-m5b vierge + les deux archives).

**Frontières.** Le scellé rc.1 FAUTIF vit à l'historique git (JAMAIS reconstruit, JAMAIS réécrit) ; le scellé 0.5.1, les cartes m0-m4, le sceau ONZE arbres, l'arbre m5/I, les fixtures v5, le scénario e3 : INTACTS ; m5/vm/ gagne scenario-m5b-e4.ps1 (copie) + LISEZMOI-terrain-m5b-e4.txt ; scripts suivis : rapatrier_kit_e3.py, assembler_kit_e4.py, livrer_vague_e4.py, inserer_entree_142.py, inserer_d147.py ; .keys/ gitignoré ; aucune suppression Drive, corbeille non vidée ; D139 ouverte non bloquante ; LA FINALE 0.6.0 TOUJOURS NON POSÉE (elle attend un run VERT — la carte ne ment pas).

**Vérifiabilité.** python3 m5/controle_base_reelle.py (VERT sur le rc.2 du dépôt) ; python3 m5/build_m5.py --verifier --graine N (R5/R8 verts, carte rc.2 lisible) ; python3 scripts/assembler_kit_e4.py (rejeu : base e3 archivée au coffre — le script refuse proprement) ; m5/carte/tableau-de-bord.txt (version=0.6.0-rc.2) ; le kit au coffre /test (md5 0922b281… recoupé à la livraison).

**SUITE — LE GESTE TERRAIN (le kit e4 attend son run).** m5b-kit-e4.zip depuis /test, dossier NEUF, corriger-wsb.bat, double-clic scenario-m5b.wsb (~5-8 min), renvoyer TOUT preuves-m5b (page-sonde-armement.txt et edge-version.txt comprises) — le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, les lignes de flux v=0/v=3 aux preuves. Si vert : python3 m5/build_m5.py --sceller-final pose la finale 0.6.0 avec la validation consignée.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-141) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 142" in texte:
    sys.exit("ECHEC : l'Entrée 142 existe déjà")
i141 = texte.find("## Entrée 141")
im = texte.find(MARQUEUR)
if not (0 <= i141 < im):
    sys.exit("ECHEC : ordre inattendu (141/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 141 < 142 < marqueur
j141 = nouveau.find("## Entrée 141")
j142 = nouveau.find("## Entrée 142")
jm = nouveau.find(MARQUEUR)
if not (0 <= j141 < j142 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 142 insérée ({len(ENTREE)} caractères) — ordre 141<142<marqueur recoupé")
