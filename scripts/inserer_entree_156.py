#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_156.py — JOURNAL_TRAVAIL.md : insère l'Entrée 156 PAR
SCRIPT (ordre 155<156<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 156 — L'ÈRE M6/M7 REFERMÉE PROPRE + LE PROGRAMME D'APRÈS M7 OUVERT : L'EXPORT DE CONTINUITÉ 0.8.0 + LE JALON M8 ET SON DOMAINE `sys` OUVERTS PAR LA COUCHE I ÉCRITE-AVANT-CODE (« continue » — la suite annoncée au Task 73 : les chantiers d'après M7 attendaient la décision du développeur)

L'EXPORT DE CONTINUITÉ 0.8.0 (le geste dédié annoncé à l'Entrée 155, D160 règle 6) : le conteneur TRIADE-continuite-multiprofils-0.8.0-20261105T044932Z.bin (729 327 o chiffré XChaCha20-Poly1305 + signé Ed25519, 126 fichiers — 81 specs I, 5 artefacts B, 5 cartes C) régénéré AU geste même depuis l'état scellé — les versions lues des CARTES : {win `0.6.0` / linux `0.7.0` / riscv `0.8.0`} (la carte du jalon porte ENFIN la finale, la racine f785e7f2…) ; l'IMPORT À SEC aux CINQ étapes § 8.2 VERT (déchiffrement, signature du conteneur + des 5 cartes, le verrou croisé 34 empreintes + 5 artefacts ENTIERS recalculés aux offsets du manifeste et recoupés aux frag-bld, l'oracle régénéré depuis les 81 specs — jamais importé D1, la reprise cohérente) ; LA PREUVE D'EXÉCUTION sur les octets TRANSPORTÉS VERT au geste même (corpus unix NATIF et corpus riscv SOUS QEMU chacun les DEUX lignes au code 0 — la parité § 8.3 des TROIS profils dans un seul conteneur ; les sondes aux quatre lignes code 6 ; le scellé win : frontière nommée, son rituel vit au poste Windows du développeur — le verrou (3) porte ses octets) ; la copie POUSSÉE au coffre Drive racine « Triade » (3-2-1 : l'état protocole qui quitte le poste porte la carte 0.8.0).

LE PROGRAMME D'APRÈS M7 OUVERT (D160, le modèle D149) : la demande « continue » EST la décision du développeur ; l'ordre des familles est LA FONDATION D'ABORD — syscalls directs (le jalon M8) → TLS 1.3 pur → profils additionnels (chacune s'appuie sur les résultats MESURÉS de la précédente ; la clause spec « hors périmètre courant » est LEVÉE NOMMÉMENT pour la seule première famille, les deux autres attendent leur décision propre) ; LE JALON M8 NAÎT sur le profil win : la lignée m8/ (m0-m5 les jalons win, m6/m7 réservés à l'auto-hébergement — m8 libre), le domaine `sys` CRÉÉ au registre figé (m0/I/README.md — un identifiant n'est jamais réutilisé), la charte des syscalls directs à HUIT RÈGLES (m8/I/README.md : le SSN est une DONNÉE jamais un octet de code ; le motif du stub VÉRIFIÉ avant toute extraction — un stub divergent = refus nommé, la contre-mesure du hook est un chantier futur jamais une contrebande ; AUCUN IAT dans le domaine — ntdll est LUE jamais APPELÉE ; l'ABI traversante un seul remappage rcx→r10, le noyau lit [rsp+0x28] de l'APPELANT ; fail-closed à SEPT verdicts nommés ; zéro état détenu ; la réserve d'ère Win10/11 x64 ; la lecture d'EAT BORNÉE par NumberOfNames, la comparaison par libc-04 l'héritage scellé) ; LA COUCHE I ÉCRITE-AVANT-CODE (le contrat précède l'octet, R2/D77) : sys-01 l'émetteur (g90001 — le trombone ABI `mov r10, rcx ; syscall ; ret`, SIX octets, AUCUN prologue : I3 la pile de l'appelant EST la pile du syscall), sys-02 le résolveur (g90002 — l'EAT de ntdll lue directement : e_lfanew dans sa fenêtre lisible, le motif PE, le répertoire export, la marche BORNÉE des noms, l'ordinal, le stub confronté au MOTIF_STUB AVANT l'imm32 à +4 ; le bloc qui LIT n'ÉMET pas — I4 la séparation est la garde), sys-03 la twin de hello-02 par NtWriteFile (g90003 — NEUF arguments dont cinq sur la pile, l'IO_STATUS_BLOCK mort au retour, le fixture-ligne de hello-02 CITÉ jamais recopié, zéro IAT : la preuve STRUCTURELLE du domaine, l'échec de résolution = AUCUN syscall émis) ; LE PLAN D'ADRESSAGE NÉ (m8/layout.py, source unique : la section .text5 préfigurée 0xA000-0xBFFF — le corps scellé 0.6.0 ne bouge pas d'un octet R7 ; les slots préfigurés D8 sys-01 @0xA000 / sys-02 @0xA400 / sys-03 @0xB000, arrêt définitif au chantier (b) sur les longueurs réelles ; les constantes MOTIF_STUB 4C8BD1B8 + OFF_SSN 4, les décalages PE/EAT, la table des SEPT verdicts, les versions 0.9.0-dev.1/0.9.0 — geste de BUILD jamais scellage, plancher R10 0x00040000 hérité ; l'héritage m5 CHARGÉ PAR CHEMIN ABSOLU — la leçon D158 appliquée dès la naissance, le module vérifié chargeant 52 blocs hérités + 3).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES — la 0.9.0-dev.1 viendra du premier build M8 au chantier (c)) ; TLS 1.3 pur et les profils additionnels demeurent HORS PÉRIMÈTRE (une décision propre chacun) ; la PEB-walk (ntdll sans IAT) et la contre-mesure du hooking sont des CHANTIERS FUTURS NOMMÉS (en l'état : la base est fournie par l'appelant, le stub divergent est un refus) ; l'export 0.8.0 au coffre est celui de l'ère close (le prochain naîtra de l'ère 0.9.0). Les chantiers du jalon M8 : (a) la couche I — ACCOMPLIE (la présente) ; (b) les blocs notés-mesurés-prouvés au harnais (la notation à la main via auteur.py, le round-trip, le différentiel sur FIXTURES ntdll synthétiques, la falsification — le labo ne connaît pas le SSN du terrain et ne le devine jamais) ; (c) le build 0.9.0-dev.1 (la composition .text5 sur le corps 0.6.0 INTACT, la carte génération 8, l'oracle structurel — la règle AUCUN IAT PAR BLOC sys) ; (d) le terrain (le kit au coffre /test, le run du développeur sur SA machine — le VRAI ntdll lu, le motif confronté, la ligne comparée, le recoup sur pièces ; la finale 0.9.0 attend le vert). Livrables : m8/I/ (README + charte + trois spécifications), m8/layout.py, m0/I/README.md (registre étendu), riscv/export/TRIADE-continuite-multiprofils-0.8.0-20261105T044932Z.bin (+ la copie au coffre Drive racine) ; consignations : la présente Entrée PAR SCRIPT, D160 PAR SCRIPT (à la suite de D159), PLAN (la ligne M8 du tableau + la section « Programme d'après M7 »), worklog +Task ID 74 ; scripts suivis : inserer_entree_156.py, inserer_d160.py, passe_bundle_m8a.py.

- SUITE : LE CHANTIER M8-(b) — les blocs notés-mesurés-prouvés : sys-01 l'émetteur (six octets, l'oracle I3 : aucun prologue), sys-02 le résolveur (la marche EAT sur FIXTURES ntdll synthétiques), sys-03 la twin de hello-02 (le différentiel : la MÊME ligne par les DEUX chemins) ; puis (c) le build 0.9.0-dev.1 + la carte génération 8, (d) le kit terrain au coffre /test.

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 156" in texte:
    sys.exit("ECHEC : l'Entrée 156 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i155 = texte.find("## Entrée 155")
if i155 < 0:
    sys.exit("ECHEC : l'Entrée 155 introuvable (l'ordre 155<156)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j155 = nouveau.find("## Entrée 155")
j156 = nouveau.find("## Entrée 156")
jm = nouveau.find(MARQUEUR)
if not (0 <= j155 < j156 < jm):
    sys.exit("ECHEC : l'ordre 155<156<marqueur n'est pas tenu "
             f"({j155}, {j156}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 156 insérée (l'ordre 155<156<marqueur constaté)")
