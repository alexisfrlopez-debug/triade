#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_152.py — JOURNAL_TRAVAIL.md : insère l'Entrée 152 PAR
SCRIPT (ordre 151<152<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 152 — LE CORPUS PARITAIRE RV64 ACCOMPLI (« lance le » — le chantier M7-(b) annoncé au Task 69) : LA TROISIÈME INSTANCIATION DE LA MÊME COUCHE I — les DOUZE blocs du patrimoine (hello-02/03, libc-01..08, tcp-07/11) + corpus-13, la notation RV64 native de 523 instructions (round-trip 100 %, capstone juge unique, graphie canonique du juge), l'instance charge LES MÊMES FICHIERS CANONIQUES de unix/I/ (13 specs, empreintes mesurées, aucune copie — le diff nul VERT en 4 recoupements : canoniques, observables R1↔R+1 par la chaîne M6 rejouée, 7 scellés octet-identiques à l'état zéro, parité § 8.3) ; L'ORACLE QEMU VERT SUR PIÈCES (réserve instrumentale D149 — TCG, noyau et syscalls réels) : le rituel de parité 6/6 — les DEUX lignes octet pour octet (« TRIADE M1 : minilibc 21/21 OK\\n » puis « corpus : autotest 21 vecteurs\\n ») code 0 — LA PARITÉ § 8.3 PAR EXÉCUTION sur les TROIS profils ; les bases forcées du CHARGEUR (-R 1G / -R 4G / -B+-R 2G) VERTES (indifférence à la base) ; la falsification 13 mutations 12/12 blocs rompus (zéro silence ; tcp-07 hors-chemin du rituel, son scénario est le chantier (c)) ; 1535 verrous structurels (appels/syscalls/données déclarés PAR BLOC, la GARDE ANTI-TABLE-X86 vivante — write 64, mprotect 226, exit_group 94 asm-generic, les numéros 1/10/231 REFUSÉS nommément) ; QUATRE LEÇONS DU GESTE, toutes attrapées par les gardes au premier passage (D156 : LA LEÇON imm12 — le verrou 0x3800 vu de la base .bss 0x3000 vit à +0x800 hors plage DE UN, la fenêtre s'est posée AU CENTRE 0x3400 ; le PIÈGE AMO — l'ISA AMO adresse [rs1] SANS déplacement, le premier jet encodait silencieusement la demande, refus nommé, le déplacement vit dans la formation déclarée ; le RECYCLAGE s3 — fenêtre de tcp-07 ET ardoise de tcp-11, dédié par rôle ; LA PORTE A GRANDI — l'extension A amoswap entre à la porte 791+1045) ; la sonde d122bc68, le corpus unix dd14195c, les cinq scellés Windows INTACTS (05/11)

**Détail.** La GÉOMÉTRIE MIROIR du plan unix (D8) : les MÊMES RVA (blocs 0x1000-0x1D80, croissance 0x1D80 en réserve ebreak), les MÊMES fixtures au même plan, les MÊMES séries (f70xxxx à la sonde, f71xxxx au corpus, f6xxxx demeure au jalon unix) ; les segments R 0x1000 (fixtures + staging + table R10) / RX 0x2000 (13 blocs + croissance) / RW 0x3000 (.bss pur filesz 0), ET_DYN/PIE e_machine 0xF3 e_flags 0, PT_GNU_STACK RW sans X, W^X constaté depuis les phdr ; l'artefact `riscv/corpus` 12 288 o sha256 b34a7147…, DÉTERMINISME constaté au rebuild ; le staging (journal v2 « j2: », 248 o qword-paddé ebreak) assemblé POUR la croissance 0x1D80, la table d'intégrité R10 le porte en première entrée (somme 0x27ddc53f… — la porte AVANT tout effet) ; le verrou tournant amoswap.d (l'extension A du profil — le portage du lock xchg), la restitution sd simple (mono-fil, fiche § 5) ; tcp-07 instancié avec LA SÉQUENCE du profil (fiche § 5 : mprotect RW → copie → fence rw,rw → LA BASCULE un mot jal construite en registres → fence.i → RX, .protger local) — le scénario complet est le chantier (c) ; consignations : Entrée 152 PAR SCRIPT (la présente), D156 PAR SCRIPT (à la suite de D155), fiche riscv64 (statut + § 6 la porte étendue + § 8 la balise + § 10 l'oracle corpus), PLAN § État (M7-(b) RÉALISÉ), riscv/I/README (la section corpus) ; la re-vérification complète rejouée (R5/R8 verts, cristallisation 2/10 par bloc) ; la carte génération 1 au SIXIÈME sel (m2, hachoir D34, sonde unix, corpus unix, sonde riscv, corpus riscv — clés projet partagées D27), frag-con TROIS PROFILS par bloc (§ 8.3-4 — la TROISIÈME colonne psABI est née), verrou croisé 13/13 ; la balise 0.8.0-dev.2 POSÉE par le build du corpus (geste de BUILD, jamais de scellage — le scellage 0.8.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté à l'exécuteur du jalon) ; scripts suivis : riscv/build_corpus.py, riscv/diff_nul_corpus.py, riscv/carte_corpus.py, outils/auteur.py (--corpus), notation/porte_roundtrip.py (AMO), inserer_entree_152.py, inserer_d156.py ; livrables : riscv/corpus, riscv/carte-corpus/, riscv/notation/ (13 + staging), la porte étendue.

- SUITE : LE CHANTIER M7-(c) — le patch scratch+fence.i EN DÉMONSTRATION (apply/effet/rollback, intégrité R10, refus nommés 1-5, le DEP falsifié) + le verrou multi-profils ; puis (d) l'export multi-profils + le terrain → la finale 0.8.0 (le terrain sera jugé POST-MORTEM ET SUR PIÈCES — D138/D145/D148, ré-établis sur originaux par la recoupure du Task 69).

"""

with open(chemin := CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 152" in texte:
    sys.exit("ECHEC : l'Entrée 152 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i151 = texte.find("## Entrée 151")
if i151 < 0:
    sys.exit("ECHEC : l'Entrée 151 introuvable (l'ordre 151<152)")

nouveau = texte.replace(
    MARQUEUR, ENTREE + MARQUEUR, 1)

# ordre recoupé : 151 < 152 < marqueur
j151 = nouveau.find("## Entrée 151")
j152 = nouveau.find("## Entrée 152")
jm = nouveau.find(MARQUEUR)
if not (0 <= j151 < j152 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(chemin, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 152 insérée ({len(ENTREE)} caractères) — "
      f"ordre 151<152<marqueur recoupé")
