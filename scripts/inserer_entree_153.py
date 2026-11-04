#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_153.py — JOURNAL_TRAVAIL.md : insère l'Entrée 153 PAR
SCRIPT (ordre 152<153<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 153 — LE CHANTIER M7-(c) ACCOMPLI (« synchro git et drive puis continue » — la synchro vérifiée SUR PIÈCES : git propre pointe 6d1b8dd == ls-remote ; Drive série versionnée [070-09ddd06] le courant, 17 archives, /test vague m6d courante, zéro copie de bundle) : LE PATCH S scratch+fence.i DÉMONTRÉ EN EXÉCUTION sous qemu — LE DÉMONSTRATEUR INVITÉ `riscv/demo` (f72001 demo-patch, 191 instructions, 764 o, à 0x2000 dans la réserve RX — l'image porte LES MÊMES blocs du corpus + le démonstrateur ; le modèle unix/demo_patch.py PORTÉ EN INVITÉ : sous qemu le scénario vit DANS l'invité) : LA BASCULE PENDANT LE TRAFIC — 1 200 usages de l'ENTRÉE du journal (0x1840, la CIBLE du patch), l'apply ENTRE les usages 399 et 400, le rollback entre 799 et 800, chaque verdict contrôlé SUR PLACE, la transcription OCTET POUR OCTET (15 425 o == 15 425 attendus) — 800 lignes v1 + 400 lignes v2 (marque « j2: »), aucune déchirée, aucune perdue, aucun mélange ; L'EFFET AU GESTE MÊME (« j2: verdict » 12 o sous v2 — LE PATCH EST EFFECTIF ; « verdict » 8 o au retour) ; LE RETOUR À L'ÉTAT IMAGE (l'entrée revenue à l'octet près == ENTREE_SAUVEE, le remplaçant DORMANT, le verrou rendu) ; LES REFUS NOMMÉS 1/2/3/4 (l'absent et la somme par mutation IN-GUEST de la table R10 — mprotect par le démonstrateur, restaurée après) ; LE DEP FALSIFIÉ (0x7→0x3 : le mutard meurt au premier apply, la transcription s'arrête aux 400 lignes v1 EXACTEMENT — 4 290 o == 4 290, SIGSEGV ACCERR) ; LA FALSIFICATION DU DÉMONSTRATEUR (rompu au premier essai — non-vacuité) ; LES BASES FORCÉES du CHARGEUR (transcription identique) ; ZÉRO RÉGRESSION (le corpus sha relu + son rituel rejoué) ; LA CORRECTION tcp-07 (D157) : le PORT avait OUBLIÉ le marshalling du prot (`.protger` ne passait jamais a2 — mprotect recevait 0xB de débris, la page perdait son bit X, ACCERR) — nommé au premier apply par la démonstration, la pièce donnée par QEMU_STRACE (PROT_SEM), UNE ligne corrigée (`mv a2, t2`), le corpus REBUILDÉ sha256 ec343b4e… (l'ancien b34a7147… demeure le record de son époque) ; QUATRE leçons du geste (D157 : le port n'est conforme que CHEMIN RÉEL exécuté ; le journal de l'exécuteur est une pièce ; le sous-programme qui appelle sauve ra — .dire ; D150 réapprise — s10/t0) ; LE VERROU CROISÉ MULTI-PROFILS VIVANT (26 empreintes des DEUX ISA re-vérifiées AVANT l'édition, la géométrie miroir, la couche I partagée) ; LE CONTRÔLE D146 ADAPTÉ VERT (base réelle CONSTATÉE PAR TRACE — in_asm, le premier bloc - e_entry : 0x555555556000 ×6, D155 confirmé ; 3 bases forcées distinctes) ; LA CONFORMITÉ § 8.2 VERTE 7/7 (29 contrôles PASS, les éléments constatés depuis l'artefact) ; LA CRISTALLISATION 10/10 ; SCELLAGE 0.8.0-rc.1 (l'artefact INTACT — le scellage est un fait de carte) ; LES TROIS GARDES VIVANTES (re-scellage REFUSÉ, reconstruction REFUSÉE, la re-vérification PRÉSERVE la balise) (05/11)

**Détail.** La séquence du profil (fiche § 5) démontrée aux octets ET en
exécution : mprotect RW (bit X RETENU — D39) → la copie staging→croissance
→ fence rw,rw → LA BASCULE UN mot aligné (jal construit en registres) →
fence.i → mprotect RX ; le verrou tournant amoswap.d (mono-fil — fiche § 5,
la concurrence HORS périmètre nommée) ; FRONTIÈRES : code 5 STRUCTUREL sous
qemu (l'hôte accorde RWX sur mapping privé — la branche fail-closed vit dans
le bloc, la démonstration terrain en jugera si l'exécuteur refuse) ; le demo
n'est PAS un artefact de la lignée (pas de carte — l'instrument du chantier,
le modèle demo_patch.py) ; livrables : riscv/demo (sha e57fc74b…),
riscv/demo_patch.py (le scénario host-side : la transcription attendue
construite depuis le plan, byte-exact), riscv/verrou_multi_profils.py,
riscv/controle_base_reelle.py, riscv/conformite_profil.py (+ conformite.txt),
riscv/build_corpus.py (--sceller-rc), le corpus REBUILDÉ (sha ec343b4e…) ;
consignations : Entrée 153 PAR SCRIPT (la présente), D157 PAR SCRIPT (à la
suite de D156), fiche riscv64 (§ 8 la balise scellée + § 9 l'élément 5 +
§ 10), PLAN § État (M7-(c) RÉALISÉ) + la ligne M7 du tableau, worklog
+Task ID 71 ; la correction tcp-07 : le sha ancien b34a7147… reste le record
de l'Entrée 152/Task 70 (append-only — le record de ce qui fut) ; la carte
du corpus vit SOUS 0.8.0-rc.1 (le scellage est un fait de carte, l'artefact
INTACT) ; scripts suivis : riscv/demo_patch.py, verrou_multi_profils.py,
controle_base_reelle.py, conformite_profil.py, inserer_entree_153.py,
inserer_d157.py.

- SUITE : LE CHANTIER M7-(d) — l'export multi-profils + le terrain (le kit
  qemu-riscv64 au coffre /test, la réserve instrumentale D149 nommée dans
  chaque verdict ; le run terrain jugé POST-MORTEM ET SUR PIÈCES —
  D138/D145/D148) → la finale 0.8.0, LE JALON M7 FRANCHI — l'universalité
  DÉMONTRÉE.

"""

with open(chemin := CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 153" in texte:
    sys.exit("ECHEC : l'Entrée 153 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i152 = texte.find("## Entrée 152")
if i152 < 0:
    sys.exit("ECHEC : l'Entrée 152 introuvable (l'ordre 152<153)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j152 = nouveau.find("## Entrée 152")
j153 = nouveau.find("## Entrée 153")
jm = nouveau.find(MARQUEUR)
if not (0 <= j152 < j153 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(chemin, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 153 insérée ({len(ENTREE)} caractères) — "
      f"ordre 152<153<marqueur recoupé")
