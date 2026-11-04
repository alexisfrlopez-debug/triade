#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_144.py — JOURNAL_TRAVAIL.md : insère l'Entrée 144 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
143 < 144 < marqueur recoupé — le même contrat que les entrées 127-143)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 144 — LE PLAN DES JALONS M6/M7 ÉCRIT (« ok, on enchaine » après le jalon M5 rentré) : le programme M6/M7 OUVERT au plan (D149 — quatre chantiers M6, quatre chantiers M7, critères mesurables, frontières nommées, décisions développeur attendues) ; les FICHES DE PROFIL COMPLÈTES nées AVANT le premier octet (docs/PROFIL_x86-64-linux-elf64.md et docs/PROFIL_riscv64-linux-elf64.md — les 7+1 éléments chacune, constats labo DATÉS du 04/11 : keystone 0.9.2 SANS RISC-V, capstone 5.0.7 désassemble RV64, qemu-riscv64 absent du bac à sable) ; le statut M5 FRANCHI consigné au plan (préambule, vue d'ensemble, chantiers (a)/(b)/(c)) et à la spécification (§ 18 + préambule : M0–M5 franchis, M6/M7 ouverts) ; le chantier M5-(c) REPORTÉ au M6-(d) — EXPLICITE, jamais silencieux ; l'écart D81 du PHRASE-CONTROLE-COFFRE.txt racine Drive FERMÉ (59 o 3 lignes → 33 o phrase seule, ouverture du coffre VERT avant/après, coffre INTÈGRE)

**L'ouverture du programme (D149, modèle des programmes D133/D77).** Le jalon M5 rentré (balise 0.6.0, Entrée 143), la suite annoncée au worklog était « les jalons M6/M7 attendent leur plan » — le plan est écrit. Il part d'un FAIT : le profil `x86-64-linux-elf64` N'EST PAS une page blanche — l'échelle d'auto-hébergement D34 y vit (hachoir `m6/` échelon 1 : ELF64 écrit à la main, exécuté NATIVEMENT au labo, oracle différentiel FIPS 180-4 sur le terrain natif ; sceau `m7/` échelon 2 phase 1) — la chaîne notation → octets → ELF64 → exécution réelle est PROUVÉE. Le jalon M6 porte ce qui manque à l'universalité : la parité du patrimoine M0–M5 (diff nul sur I, même oracle vert sur les deux profils, parité § 8.3 par exécution) et le durcissement format de l'artefact du jalon (ET_DYN/PIE à base aléatoire, trois segments R/RX/RW, PT_GNU_STACK sans X — l'ELF minimal auto-hôte, constaté ET_EXEC à 2 phdr, demeure valide pour SA lignée, l'écart est nommé). Quatre chantiers M6 : (a) durcissement format + table ERRNOS ; (b) corpus paritaire — audit de couplage (contrats classés A/B/C), révision de granularité R+1 des contrats au niveau FORMEL (arguments nommés dans I, convention d'appel vers frag-con, § 8.3-4), invariance des octets Windows ASSERTÉE, diff nul MESURÉ PAR SCRIPT ; (c) suite de conformité § 8.2 (modèle m5) + scellage 0.7.0-rc.1 avec contrôle D146 adapté (exécution full-ELF à la base réelle — l'image PIE au noyau) ; (d) LE PATCH EN PRODUCTION — le chantier M5-(c) refermé : moteur tcp-07 instancié (mprotect) et EMBARQUÉ, bascule du journal PENDANT le trafic, rollback, zéro régression, kit terrain Linux au coffre /test, run WSL2/VM du développeur, verdict sur pièces (D138/D145/D148) → finale 0.7.0. Quatre chantiers M7 (différés derrière M6, l'ordre isole les variables — D14) : (a) moteur de notation RV64 (l'assembleur maison OU moteur tiers passé à la même porte, capstone JUGE UNIQUE du round-trip) + qemu-riscv64 ; (b) la TROISIÈME instanciation de la même couche I (garde anti-table-x86 : write=1 est un refus nommé — la parité est SÉMANTIQUE, jamais lexicale) ; (c) patch scratch + fence.i + verrou croisé multi-profils ; (d) export de continuité multi-profils de bout en bout (les CINQ étapes) → finale 0.8.0.

**Les fiches de profil (l'exigence du manuel § 2, honorée avant tout octet).** `docs/PROFIL_x86-64-linux-elf64.md` : les 7+1 éléments — SysV (RDI RSI RDX RCX R8 R9, la zone rouge 128 o LE PIÈGE INVERSE de msx64, XMM tous volatils), ELF64 durci (ET_DYN, PT_GNU_STACK 0x6474e551 sans X), syscalls directs (RAX=nr, RDI RSI RDX R10 R8 R9 — le 4e argument par R10, RCX détruit par l'instruction ; contrat d'erreurs −errno fail-closed, table ERRNOS miroir de la table HRESULTS), patch à chaud (trampoline identique x86-64 + mprotect ; AUCUNE barrière I-cache requise — cohérence matérielle, Intel SDM vol. 3 § 8.1.3), notation (LE MÊME keystone 0.9.2/capstone 5.0.7 que le primaire — la thèse même de M6 à ISA constante), granularité D8, porte R10 déclinée + contrôle D146 adapté. `docs/PROFIL_riscv64-linux-elf64.md` : RV64IMA + Zifencei SANS extension C (instructions 4 o UNIQUES — choix assumé : granularité et bascule uniformes, le psABI autorise un cœur RV64GC à exécuter du RV64IMA), psABI LP64 (a0-a7, AUCUNE zone rouge — le piège inverse de SysV x86-64), e_machine 0xF3/e_flags 0, table asm-generic (write=64, exit_group=94…), patch scratch + fence.i (séquence de référence en sept gestes, portée du fence.i = cœur courant, mono-fil au jalon — frontière nommée), l'ASSEMBLEUR MAISON recommandé (keystone 0.9.2 ne porte PAS le RISC-V — CONSTAT labo), NOP canonique 0x13 / garde ebreak 0x00100073, l'exécuteur qemu-riscv64 avec la RÉSERVE INSTRUMENTALE nommée (l'ISA est exécutée par l'émulateur de processus, le noyau et les syscalls sont réels — jamais déguisée en exécution native).

**Les consignations d'état.** PLAN_MILESTONES.md : préambule complété (chantier (b) RÉALISÉ le 04/11 — critère (b) de D136 VERT sur pièces au run e4, balise 0.6.0 scellée, JALON M5 FRANCHI ; chantier (c) REPORTÉ), vue d'ensemble (ligne M5 : franchi le 04/11/2026), tableau du programme M5 (chantiers (a)/(b)/(c) à jour), la section « Programme M6/M7 — Universalité (ouvert le 04/11/2026, D149) » insérée avec les DEUX tableaux de chantiers, les frontières nommées (corpus nominal restreint — le serveur écho complet de M2 est un chantier OUVERT, jamais une réduction silencieuse) et les TROIS décisions développeur attendues (terrain M6 WSL2 recommandé / VM ; terrain M7 qemu avec réserve ; aval du report M5-(c)). PROTOCOLE_TRIADE.md : préambule (M0–M5 franchis, M6/M7 ouverts) et § 18 (M5 franchi 04/11 — balise 0.6.0 ; M6/M7 ouverts, fiches référencées) — le PDF v0.6.1 se régénère par le mécanisme établi (D17/D134), empreinte consignée PAR LE BUILD au tableau de bord.

**L'écart D81 FERMÉ (le reste nommé au Task 60 : « à corriger à la prochaine synchro »).** scripts/corriger_phrase_racine.py, fail-closed intégral : le PHRASE-CONTROLE-COFFRE.txt de la racine du coffre Drive (« Triade ») portait 59 o / 3 lignes — la ligne 1 ÉTAIT la phrase courante (conforme au constat), l'ouverture par --phrase-fichier ÉCHOUAIT (« déchiffrement impossible »), la copie du DÉPÔT (33 o, phrase seule, norme D81) ouvrait le coffre (rc=0) — la mutation fut exécutée APRÈS ces preuves (upload_update du contenu du dépôt), puis re-téléchargement IDENTIQUE octet pour octet (33 o) et ouverture du coffre par le fichier RAPATRIÉ : VERT (rc=0). Coffre .keys/coffre_fort.bin INTÈGRE (md5 23a2987a… attesté D144, jamais muté — lecture seule par lister). Aucun secret affiché (empreintes et tailles seules).

**Frontières.** AUCUNE balise posée (la 0.7.0-dev.1 viendra du premier build M6 — la présente est un geste de PLAN, jamais de scellage) ; les scellés 0.6.0/0.5.1, les cartes m0-m5, le sceau ONZE arbres, les arbres I, les fixtures v5 : INTACTS ; aucune suppression Drive, corbeille non vidée ; .keys/ gitignoré ; D139 ouverte non bloquante ; scripts suivis : corriger_phrase_racine.py, inserer_d149.py, inserer_entree_144.py ; livrables du plan : docs/PROFIL_x86-64-linux-elf64.md, docs/PROFIL_riscv64-linux-elf64.md, la section programme M6/M7 de PLAN_MILESTONES.md.

**Vérifiabilité.** python3 scripts/corriger_phrase_racine.py (idempotent par ses assertions : l'écart fermé, il refuse de re-muter) ; les fiches au dépôt (constats labo reproduits : keystone/capstone par python3 -c import…) ; PLAN_MILESTONES.md § Programme M6/M7 ; DECISIONS.md D149 (à la suite de D148).

**SUITE.** Le chantier M6-(a) est prêt à s'exécuter : le durcissement format (writer ET_DYN/PIE + GNU_STACK, table ERRNOS, layout unix/) — aucune décision développeur ne le bloque ; les décisions attendues (terrain WSL2/VM, réserve qemu, aval du report M5-(c)) sont nommées au plan et peuvent tomber au fil de l'eau.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-143) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 144" in texte:
    sys.exit("ECHEC : l'Entrée 144 existe déjà")
i143 = texte.find("## Entrée 143")
im = texte.find(MARQUEUR)
if not (0 <= i143 < im):
    sys.exit("ECHEC : ordre inattendu (143/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 143 < 144 < marqueur
j143 = nouveau.find("## Entrée 143")
j144 = nouveau.find("## Entrée 144")
jm = nouveau.find(MARQUEUR)
if not (0 <= j143 < j144 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 144 insérée ({len(ENTREE)} caractères) — ordre 143<144<marqueur recoupé")
