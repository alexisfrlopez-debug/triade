#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d147.py — DECISIONS.md : insère D147 PAR SCRIPT À LA SUITE de
D146 (insertion ASSERTÉE : D146 présente une fois, D147 absente, D147
ajoutée APRÈS D146 — fin du fichier)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D147 — LA LICENCE DE RECONSTRUCTION D'UN SCELLÉ FAUTIF EST EXACTEMENT LE SAUT DE PRÉ-VERSION MINIMAL (rc.1 → dev.2 → rc.2, modèle D35) ET LE CONTRÔLE D146 DEVIENT EXIGENCE MÉCANIQUE DU GESTE DE SCELLAGE : la règle vit au code du build, pas au souvenir de l'agent

**Le constat qui fonde la décision (04/11, Entrée 142 — le chemin rc.2 accompli).** Le scellé 0.6.0-rc.1 était fautif (le crash du run e3, D146) : le corriger exigeait de reconstruire l'artefact, or l'anti-rollback (R6) interdit toute reconstruction sous balise scellée — le verrou fait bien son travail, mais la règle de gestion du correctif devait être ÉCRITE avant que le cas ne se représente, pas improvisée. Le précédent existait : D35 (M3, le rc.1 de la 0.3.0 fautif IAT) avait déjà tranché le modèle — correctif à contrat stable (R4), la lignée avance d'exactement un saut de pré-version, la cristallisation repart à zéro, le scellé fautif vit à l'historique JAMAIS reconstruit.

**La règle.** (1) LICENCE EXCLUSIVE : l'amendement de l'anti-rollback autorise UNE reconstruction précise, nommée en clair au code (build_m5._anti_rollback, dict LICENSE à une entrée : {« 0.6.0-rc.1 »: « 0.6.0-dev.2 »}) — motif constaté (l'Entrée qui nomme le défaut), version cible supérieure STRICTEMENT (R10 : 0x00060001 > 0x00060000), toute autre reconstruction sous balise scellée restant REFUSÉE fail-closed. (2) LA CRISTALLISATION DU CORRECTIF REPART À ZÉRO : dix passages exigés avant le scellage du rc corrigé (R6 — un correctif n'hérite pas des preuves du code fautif). (3) LE CONTRÔLE D146 EST EXÉCUTÉ PAR LE SCELLAGE MÊME : _sceller appelle le contrôle base réelle AVANT la bascule de balise et REFUSE tout scellage non vert — la règle D146 cesse d'être une consigne de conduite, elle devient une garde du build (fail-closed : l'agent ne peut pas l'oublier). (4) Le sha du scellé fautif reste consigné au code (SHA_PROXY_060_RC1) en mémoire du refus — il n'est JAMAIS reconstruit, l'historique git le porte.

**Alternatives rejetées.** Réécrire le scellé rc.1 en place (rejeté : une balise scellée est immuable § 9 — le verrou anti-rollback est la garantie d'existence de la lignée, le réécrire c'est le détruire) ; sauter directement à rc.2 sans dev.2 (rejeté : la reconstruction produit une pré-version DEV qui doit vivre ses preuves — oracles, cristallisation — AVANT d'être candidate ; le modèle D104/D35 sépare la construction de la candidature) ; laisser le contrôle D146 au bon vouloir de l'agent (rejeté : la leçon du rc.1 est précisément qu'un contrôle absent du geste est un contrôle qui n'existe pas — D145 avait fait ce chemin pour les gardes de scénario, D146 le fait pour le scellage).

**Frontières.** La licence couvre le SAUT MINIMAL, pas une permission générale : reconstruire encore sous rc.2 exigera une NOUVELLE décision nommée (la garde l'exprime : « procedure lourde R6 ou nouvelle version X.Y.Z+1 requise ») ; elle ne touche NI les cartes des jalons clos (m0-m4 : leurs verrous restent absolus), NI l'arbre d'intention (le correctif rc.2 s'est fait À CONTRAT STABLE — m5/I inchangé, le sceau-I reste valide) ; le kit terrain suit la vague (D143) : la vague consommée est archivée, jamais jetée ; le run terrain reste le juge du critère (b) de D136 — la licence répare le binaire, elle ne valide rien.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D147" in texte:
    sys.exit("ECHEC : D147 existe déjà")
if texte.count("## D146 —") != 1:
    sys.exit(f"ECHEC : D146 présente {texte.count('## D146 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D146 —") < nouveau.find("## D147")):
    sys.exit("ECHEC : ordre final inattendu (D147 avant D146)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D147 insérée à la suite de D146 — ordre recoupé")
