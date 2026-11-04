#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d153.py — DECISIONS.md : insère D153 PAR SCRIPT À LA SUITE de
D152 (insertion ASSERTÉE : D152 présente une fois, D153 absente, D153
ajoutée APRÈS D152 — fin du fichier, modèle inserer_d152.py)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D153 — LE FLUX MESURÉ N'EST À PERSONNE (la narration de l'instrument ne vit JAMAIS sur le canal capturé — elle est différée à la sortie de la fenêtre) ; UN LIVRABLE TERRAIN NE SE DÉPOSE QUE S'IL EST VERT À L'EXTRACTION VIERGE (l'épreuve par extraction + run complet au labo, partie du montage — jamais une confiance en la construction) ; L'INSTRUMENT DU TERRAIN EST CELUI DU LABORATOIRE, RECOUPÉ OCTET POUR OCTET (le gabarit relocalisable à fixup unique, assemblé à adresse factice HAUTE)

**Le constat qui fonde la décision (05/11, chantier M6-(d), Entrée 148 — la démonstration M5-(c) + le kit terrain Linux).** Trois constats du geste fondent la règle : (1) LA PREMIÈRE ÉPREUVE DU KIT A ÉCHOUÉ NOMMÉ — le scénario terrain imprimait sa narration sur fd 1, le canal même que la capture détourne vers le tube : 102 octets de narration se sont retrouvés DANS le flux mesuré (T2a : « 14 992 o émis != 14 890 attendus »), et un fragment de narration littéral dans le trafic de l'ouvrier (T2b) ; le défaut était DANS L'INSTRUMENT (le scénario), pas dans l'artefact — et l'assertion octet-pour-octet l'a nommé au premier passage (un instrument tolérant l'aurait tu : le vert muet est l'espèce refusée). Le jumeau de laboratoire (demo_patch.py) était vert parce qu'il COLLECTIONNE ses constats et ne les imprime qu'à la fin — la différence entre les deux instruments ÉTAIT la leçon ; (2) C'EST L'ÉPREUVE PAR EXTRACTION VIERGE qui a attrapé le défaut — pas la construction, pas la compilation, pas l'inspection : le kit tel que le développeur l'exécuterait (dossier neuf, `python3 scenario-m6d.py`), rejoué au labo AVANT tout dépôt ; (3) LA CARTOUCHE EMBARQUÉE : le terrain n'assemble rien (aucune dépendance instrumentale au terrain — keystone/capstone restent au labo), mais un gabarit assemblé À BASE 0 aurait produit la forme imm32 TRONQUÉE du `mov r11, .retour` (inutilisable pour toute vraie adresse mmap) : le gabarit est assemblé à une ADRESSE FACTICE HAUTE (0x100000000000 — la forme imm64 est FORCÉE), recoupé contre l'instrument VIVANT de l'oracle octet pour octet, et relogé au terrain par UN fixup imm64 unique posé AVANT le mprotect RX.

**La règle.** (1) TOUT instrument qui mesure un flux par détournement de canal (capture fd 1, tube, socket) interdit à SA PROPRE narration de vivre sur le canal mesuré : la narration est différée à la sortie de la fenêtre de capture (ou vit sur un autre canal) — le flux capturé n'appartient qu'au producteur mesuré, et l'assertion octet-pour-octet demeure le juge (tout écart se nomme, jamais ne se tolère). (2) TOUT livrable terrain (kit, scénario, conteneur) n'est DÉPOSÉ au coffre que s'il est VERT À L'EXTRACTION VIERGE + RUN COMPLET au laboratoire — l'épreuve est une ÉTAPE DU MONTAGE (l'assembleur la conduit et refuse le dépôt sur échec), jamais une vérification optionnelle d'après-coup ; l'idempotence du montage garantit que le kit reconstruit est le kit éprouvé. (3) L'INSTRUMENT EMBARQUÉ au terrain est RECOUPÉ contre l'instrument du laboratoire OCTET POUR OCTET (la même source, assemblée au labo, vérifiée contre l'instrument en vie — puis relogée au terrain par le fixup minimal NOMMÉ) : le terrain exécute l'instrument du labo, jamais une réécriture ; le gabarit est assemblé à une adresse qui FORCE l'encodage complet (imm64), jamais à la base 0. (4) L'EMPREINTE du kit déposé est recoupée au coffre (md5 affiché par le passeur, vérifié avant le dépôt) — le kit au coffre EST le kit éprouvé, un écart est un refus.

**Alternatives rejetées.** Déposer le kit sur la confiance de la construction (rejeté : la première épreuve a échoué NOMMÉ — la preuve vivante que la construction ne suffit pas) ; tolérer les écarts mineurs du flux capturé (rejeté : « 102 octets de plus » est une narration dans le flux mesuré — l'instrument qui s'écoute n'entend plus le mesuré) ; embarquer keystone au terrain pour assembler la cartouche sur place (rejeté : le terrain n'installe RIEN — la cartouche pré-assemblée + fixup unique recoupée octet pour octet est le MÊME instrument sans dépendance) ; assembler le gabarit à base 0 (rejeté : keystone y émet la forme imm32 — tronquée pour toute vraie adresse mmap, le défaut serait latent jusqu'au crash du run développeur) ; faire vérifier l'épreuve par le développeur (rejeté : le terrain n'est jamais le premier témoin d'un livrable — le labo prouve, le terrain recoupe).

**Frontières.** La règle régit les instruments de mesure par capture de canal, le montage et le dépôt des livrables terrain ; elle ne touche NI l'artefact scellé (INTACT — sha dd14195c…, le patch est un fait de session), NI la suite de conformité (qui exécute la démonstration sur SON propre canal — la collecte différée y vit déjà), NI le déroulé du run développeur (le scénario déposé est le scénario éprouvé — le terrain recoupe, le labo a prouvé). Le kit m6d est DÉPOSÉ au coffre /test (md5 67b85983…) : la vague courante, le run VERT sur pièces posera la finale 0.7.0 (le jalon M6 franchi — l'exigence « validation terrain consignée » demeure, D149/D152 inchangées).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D153" in texte:
    sys.exit("ECHEC : D153 existe déjà")
if texte.count("## D152 —") != 1:
    sys.exit(f"ECHEC : D152 présente {texte.count('## D152 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D152 —") < nouveau.find("## D153")):
    sys.exit("ECHEC : ordre final inattendu (D152 < D153)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"D153 insérée ({len(DECISION)} caractères) — à la suite de D152, ordre recoupé")
