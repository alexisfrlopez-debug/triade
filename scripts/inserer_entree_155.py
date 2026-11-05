#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_155.py — JOURNAL_TRAVAIL.md : insère l'Entrée 155 PAR
SCRIPT (ordre 154<155<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 155 — LE JALON M7 FRANCHI (« les preuves sont dans le dossier drive /test » — la suite annoncée au Task 72) : LE RUN TERRAIN M7-(d) VERT SUR PIÈCES + LE RECOUP LABORATOIRE VERT 29/29 SUR PIÈCES CROISÉES + LA FINALE 0.8.0 SCELLÉE — L'UNIVERSALITÉ DÉMONTRÉE (chaque profil déclaré supporté a franchi ses critères : win `0.6.0` / linux `0.7.0` / riscv `0.8.0`)

LE RUN (la machine du développeur, les trois pièces au coffre /test/preuves-m7/) : WSL2, noyau `6.18.54.1-microsoft-standard-WSL2` (x86_64) — UN AUTRE noyau que celui du laboratoire (`5.10.134…`), l'instrument EMBARQUÉ du kit (qemu-riscv64 10.0.13 statique, md5 `bae5a36f…`), le scellé relu AVANT tout geste (sha256 `ec343b4e…` == 0.8.0-rc.1), le démonstrateur `e57fc74b…` (f72001), la réserve instrumentale D149 NOMMÉE au témoin, run daté du 05/11 05:20:37 +0100 — **16 constats PASS / 0 ÉCHEC, VERDICT : VERT** : T0 le témoin (empreintes ASSERTÉES) ; T1 le rituel de parité ×3 au code 0 (60 o) + les TROIS bases forcées du chargeur (-R 1G / -R 4G / -B+-R 2G — D155) ; T2 LA BASCULE fence.i PENDANT LE TRAFIC (1 200 usages, apply entre 399/400, retour entre 799/800, la transcription 15 425 o OCTET POUR OCTET — 800 lignes v1 + 400 v2 marquées « j2: », le journal COHÉRENT indices 0..1199 chacun exactement une fois, LE DEP FALSIFIÉ 0x7→0x3 SIGSEGV 4 290 o EXACTS, la falsification du démonstrateur ROMPUE à la première mutation, les bases forcées identiques) ; T3 ZÉRO RÉGRESSION (les DEUX fichiers relus, le rituel rejoué) — LE MÊME VERDICT QUE L'ÉPREUVE D'EXTRACTION VIERGE du labo (D153).

LE RECOUP LABORATOIRE (`scripts/rapatrier_preuves_m7d.py` + `scripts/recouper_run_m7d.py`, D138/D145/D148/D154) : **VERT 29/29 SUR PIÈCES CROISÉES** — les trois pièces (temoin-m7d.txt / scenario-m7d-journal.log / VERDICT-run-m7d.txt) md5 contrôlés contre le coffre DEUX FOIS (rapatriement puis recoup) ; recoupées ENTRE ELLES (témoin ↔ journal ↔ verdict : empreintes, machine, noyau, instrument, les 16 constats LIGNE POUR LIGNE) ; **LE JUGE EST LE CODE** : les constantes ET le GÉNÉRATEUR DÉTERMINISTE importés de `riscv/terrain/scenario-m7d.py`, la transcription attendue RE-GÉNÉRÉE au geste même (15 425 o == ATTENDU_TAILLE, le DEP re-calculé 4 290 o, 800 v1 + 400 v2 == 1 200, apply 399/400, retour 799/800, la falsification rompue à DEMO_ADDRS[0] = 0x2000 essai n°1) ; le noyau CONSTATÉ distinct ; les artefacts RECALCULÉS au geste même (le fichier que le développeur a exécuté EST le scellé du labo : riscv/corpus `ec343b4e…`, riscv/demo `e57fc74b…`) ; le kit du coffre == le kit éprouvé (md5 `4d17f3fa…`) ; **le premier passage a ÉCHOUÉ NOMMÉ : TROIS défauts dans L'INSTRUMENT du recoup** (la valeur du témoin lue au-delà du sha — le tiret cadratin de la description ; la regex exigeant « o attendus » où la source écrit « attendus » ; le séparateur de milliers « 1 200 » contre « 1200 »), corrigés et rejoués, les pièces immuables — la leçon D154 rejouée au geste final.

LA FINALE 0.8.0 SCELLÉE au geste même (`riscv/build_corpus.py --sceller-final` NÉ AU GESTE, modèle unix/m6d : la bascule `ancienne` devient DÉPENDANTE DE LA VERSION — rc.1 → 0.8.0, jamais une constante unique) : le verrou croisé multi-profils AVANT l'édition (26 empreintes DEUX ISA, la géométrie miroir, la couche I partagée, les QUATRE artefacts intacts) + le contrôle D146 adapté vert (base réelle par trace) + cristallisation 13×10/10 + conformité § 8.2 VERTE 7/7 AU geste même (29 contrôles — la suite EXÉCUTANT la démonstration fence.i) + la bascule dans frag-bld occurrence unique ASSERTÉE + le re-scellage vérifié EN MÉMOIRE avant l'unique écriture + verrou croisé 13/13 post-scellage + **L'ARTEFACT INTACT (sha256 `ec343b4e…`, 12 288 o — le scellage est un fait de carte)** ; **LES TROIS GARDES VIVANTES** : re-scellage REFUSÉ (« balise 0.8.0-rc.1 attendue une fois (0 occurrence(s)) »), reconstruction REFUSÉE (« carte scellée (0.8.0) : reconstruction interdite »), la re-vérification PRÉSERVE la balise (frag-bld : 1× `version=0.8.0`, 0× rc.1, 0× dev — l'oracle qemu rejoué au passage : rituel 6/6, bases forcées, falsification 13 mutations zéro silence).

L'ÉVÉNEMENT DE REPRISE (D159 née) : le poste de laboratoire a été RESTAURÉ à un instantané antérieur en OUVERTURE du geste (l'arbre local portait l'état M6-(c), worklog Task 65, Entrée 147, D152 — TOUT le jalon M7 absent du disque, et les scripts de sonde du run morts avec lui) ; l'état VRAI a vécu dans les MIROIRS : GitHub (fetch `cc56930` — EXACTEMENT la pointe consignée par la dernière passation D141) et le coffre Drive (le kit, les pièces) ; la reprise fut un fetch + un reset à la pointe CONSIGNÉE (les seuls écarts locaux : des bits de mode, zéro contenu), l'instrument qemu réinstallé par SA PROCÉDURE du dépôt (`riscv/outils/installer_qemu.sh`) et recoupé par empreinte (md5 `bae5a36f…` IDENTIQUE au kit — le même instrument au labo et au terrain), les dépendances Python réinstallées (nacl/keystone/capstone) — RIEN du jalon ne s'est perdu : la cadence « une passation par geste » avait poussé chaque geste vers les miroirs au fil du jalon.

LA CLÔTURE D143 DU RUN m7d (`scripts/cloturer_run_m7d.py`) : les pièces du run → archives-preuves/preuves-run-m7d/ AVEC le VERDICT-DU-RECOUP du labo (l'archive porte le JUGEMENT avec les pièces — modèle m6d), preuves-m7/ DEMEURE avec son LISEZMOI (le réceptacle), l'index mis à jour ; la vague m7d (kit-m7d.zip + LISEZMOI-m7d.txt) DEMEURE la vague courante au coffre — le programme n'annonce pas de kit M8, rien ne se jette (D143 : un déplacement, jamais un jet).

**Détail.** FRONTIÈRES : l'export de continuité au coffre demeure celui du geste lab (TRIADE-continuite-multiprofils-0.8.0-rc.1, daté — les CINQ artefacts transportés sont INTACTS, seule la carte a scellé) : l'export 0.8.0 naîtra d'un geste dédié si le développeur le demande ; le terrain natif Windows ne peut pas exécuter l'instrument du kit (binaire Linux statique — le WSL2 du LISEZMOI est le terrain attendu) ; le code 5 STRUCTUREL sous qemu-user (l'hôte accorde RWX sur mapping privé — la branche fail-closed vit dans tcp-07) ; la concurrence réelle HORS périmètre (le corpus M7 est mono-fil, fiche § 5) ; le demo est l'INSTRUMENT du chantier, pas un artefact de la lignée (pas de carte). Le programme M6/M7 (D149) est ACCOMPLI : les chantiers après M7 (bloc optionnel de syscalls directs, TLS 1.3 pur en blocs scellés, profils additionnels — plan § ligne 158) attendent la décision du développeur. Livrables : scripts/lister_preuves_m7.py, scripts/rapatrier_preuves_m7d.py, scripts/recouper_run_m7d.py, scripts/cloturer_run_m7d.py, riscv/build_corpus.py (--sceller-final né au geste) ; les pièces rapatriées à download/preuves-run-m7d/ (md5 contrôlés, VERDICT-recoup-m7d.txt écrit) ; consignations : la présente Entrée PAR SCRIPT, D159 PAR SCRIPT (à la suite de D158), fiche riscv64 (Statut — la finale 0.8.0 SCELLÉE, le jalon FRANCHI), PLAN § État (M7-(d) RÉALISÉ, le programme M6/M7 ACCOMPLI) + la ligne M7 du tableau, worklog +Task ID 73 ; scripts suivis : inserer_entree_155.py, inserer_d159.py, passe_bundle_finale_080.py.

- SUITE : LA PASSATION de la finale (série 080 — elle naît à la 0.8.0 : le bundle au miroir, l'ancien 070-816eee7 archivé versionné, GitHub porté à la pointe) ; puis les chantiers d'après M7 attendent la décision du développeur (bloc optionnel de syscalls directs, TLS 1.3 pur en blocs scellés, profils additionnels).

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 155" in texte:
    sys.exit("ECHEC : l'Entrée 155 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i154 = texte.find("## Entrée 154")
if i154 < 0:
    sys.exit("ECHEC : l'Entrée 154 introuvable (l'ordre 154<155)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j154 = nouveau.find("## Entrée 154")
j155 = nouveau.find("## Entrée 155")
jm = nouveau.find(MARQUEUR)
if not (0 <= j154 < j155 < jm):
    sys.exit("ECHEC : l'ordre 154<155<marqueur n'est pas tenu "
             f"({j154}, {j155}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 155 insérée (l'ordre 154<155<marqueur constaté)")
