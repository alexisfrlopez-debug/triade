#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d152.py — DECISIONS.md : insère D152 PAR SCRIPT À LA SUITE de
D151 (insertion ASSERTÉE : D151 présente une fois, D152 absente, D152
ajoutée APRÈS D151 — fin du fichier, modèle inserer_d151.py)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D152 — LA BASE SE CONSTATE, ELLE NE SE DÉCRÈTE PAS (le témoin ptrace/maps à l'arrêt d'exec) ; UN TÉMOIN D'EXÉCUTION SE PROUVE FALSIFIABLE SUR LA CLASSE EXACTE DU DÉFAUT QU'IL GARDE (le mutant « RVA nu ») ; UN ALLOCATEUR PAR DÉCRÉMENT-RESTITUTION N'EST PAS UN ALLOCATEUR SOUS CONCURRENCE (le sommet est PAR FIL) ; UNE CHAÎNE DE RE-VÉRIFICATION PRÉSERVE LA BALISE SCELLÉE — le chantier M6-(c) : la conformité constatée, le D146 adapté exécuté au scellage même, les gardes vivantes

**Le constat qui fonde la décision (05/11, chantier M6-(c), Entrée 147 — la suite de conformité + le scellage 0.7.0-rc.1).** Quatre constats du geste fondent la règle :
(1) LA BASE SE CONSTATE : le contrôle D146 adapté (`unix/controle_base_reelle.py`) exécute l'image PIE par le NOYAU et lit la base de chargement dans /proc/<pid>/maps À L'ARRÊT D'EXEC garanti par PTRACE_TRACEME — 6 bases distinctes sur 6 exécutions, la MÊME base deux fois sous ADDR_NO_RANDOMIZE (personality, le mécanisme de setarch -R) : l'ASLR est un CONSTAT du noyau, jamais une croyance du contrôle (la sonde du chantier (a) émettait SA base ; le contrôle du jalon la LIT depuis le noyau — deux témoins indépendants de la même vérité) ;
(2) LA FALSIFIABILITÉ PORTE SUR LA CLASSE : le témoin d'exécution se prouve en tuant un mutant de LA CLASSE EXACTE du défaut qu'il garde — le « RVA nu » (le lea rip réécrit mov edi, <rva> : l'adresse sans la base, le geste de la ligne de flux qui tua le 0.6.0-rc.1 au run e3) meurt NOMMÉ (SIGSEGV à l'adresse nue, RIP rapporté au bloc du plan par la plage EXACTE de son slot) — en base aléatoire ET en base figée ; une mutation quelconque prouve la sensibilité, une mutation DE LA CLASSE prouve la GARDE ;
(3) L'ALLOCATEUR : à la cristallisation, refus intermittent (~1/11) « tcp-11 concurrence : verdicts divergents » — la chasse (240 essais instrumentés) a nommé la signature (rax = la longueur d'une AUTRE ligne) puis la cause : l'allocateur de sommets de la cartouche (décrément à l'entrée, restitution au retour) est un bump-LIFO que l'ordre de restitution INTERFOLÉ rompt — un fil libère, le plafond remonte sur le sommet d'un appel VIVANT, deux appels partagent la fenêtre et la pile ; D151 avait rendu la FENÊTRE par appel, le SOMMET restait à recouvrement — le sommet est désormais PAR FIL (attribué une fois, réutilisé en séquence dans son fil, JAMAIS restitué : la restitution interfolée était la faille) ; le bloc sous test était EXONÉRÉ : l'instrument mentait, pas le code ;
(4) LA BALISE : verifier() régénérait frag-bld avec la version EN DUR — après un scellage, toute re-vérification aurait REVERTI la balise scellée ; la re-vérification lit désormais la balise du manifeste et re-signe la carte SOUS elle (un scellé ne se revertit pas par la porte de la vérification).

**La règle.** (1) TOUT témoin d'exécution à la base réelle CONSTATE la base depuis le noyau (ptrace/maps à l'arrêt d'exec, ou l'émission par l'artefact lui-même) et recoupe le figeage (ADDR_NO_RANDOMIZE) — jamais une base décrétée, jamais une seule méthode. (2) TOUT témoin d'exécution chargé de garder une classe de défaut prouve sa falsifiabilité SUR CETTE CLASSE (le mutant de la classe, mort nommé) — la classe du défaut gardé est NOMMÉE au contrôle. (3) SOUS CONCURRENCE, aucune ressource n'est attribuée par décrément-restitution : l'attribution est PAR FIL (ou par pool de slots libres) — une LIFO à restitution interfolée est un recouvrement en attente ; l'instrument fautif n'invalide pas le code sous test (l'exonération se constate sur pièces), mais son refus fail-closed reste le seul mode (un faux vert de l'instrument est un faux vert du jalon). (4) UNE CHAÎNE DE RE-VÉRIFICATION ne déplace JAMAIS une balise : elle re-signe la carte sous la balise courante ; le registre des versions acceptées (plancher 0.7.0-dev.1) refuse toute balise hors lignée ; le scellage bascule la balise une fois, avec le contrôle D146 exécuté AU geste même (D146/D147 demeurent). (5) Le scellage rc/final vérifie l'artefact INTACT par sha constant — le scellage est un fait de carte, un écart d'artefact est un refus.

**Alternatives rejetées.** Décréter la base (rejeté : « 6 bases distinctes » sans témoin est une croyance — la sonde du (a) et le contrôle du (c) la constatent chacun à leur manière) ; prouver la falsifiabilité par une mutation quelconque (rejeté : la classe du défaut gardé est la seule preuve que la GARDE garde — un octet inversé prouve la sensibilité, pas la garde) ; garder l'allocateur par décrément en verrouillant toute la durée de l'appel (rejeté : tuer la concurrence réelle pour sauver l'instrument, c'est ne plus tester la concurrence — le sommet par fil préserve le VRAI parallélisme) ; blâmer le bloc journal sur le refus intermittent (rejeté : la signature l'exonérait — l'instrument se prouve fautif sur pièces AVANT que le code ne soit touché) ; permettre à la re-vérification de régénérer la balise dev (rejeté : la porte de la vérification deviendrait la porte de déscellement — silencieuse qui plus est).

**Frontières.** La règle régit les témoins d'exécution, les instruments concurrents et les chaînes de re-vérification des jalons ; elle ne touche NI les octets des scellés (l'artefact corpus est INTACT à travers le scellage — sha dd14195c…, un fait de carte), NI la porte R10 du corpus (la table d'intégrité et ses qwords de garde demeurent — D146/D147/D151 inchangées), NI le déroulé (d) (le --sceller-final attend le run terrain vert, l'exigence porte « validation terrain consignée »). Le scellé 0.7.0-rc.1 est POSÉ : immuable § 9, défaut → X.Y.Z+1 à contrat stable (R4), anti-rollback vivant (re-scellage et reconstruction refusés sur pièces).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D152" in texte:
    sys.exit("ECHEC : D152 existe déjà")
if texte.count("## D151 —") != 1:
    sys.exit(f"ECHEC : D151 présente {texte.count('## D151 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D151 —") < nouveau.find("## D152")):
    sys.exit("ECHEC : ordre final inattendu (D152 avant D151)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D152 insérée à la suite de D151 — ordre recoupé")
