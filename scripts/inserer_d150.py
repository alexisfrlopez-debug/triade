#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d150.py — DECISIONS.md : insère D150 PAR SCRIPT À LA SUITE de
D149 (insertion ASSERTÉE : D149 présente une fois, D150 absente, D150
ajoutée APRÈS D149 — fin du fichier, modèle inserer_d149.py)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D150 — LA TABLE ERRNOS EST MOTIVÉE PAR BLOC, ET L'ÉTAT QUI TRAVERSE DES APPELS VIT EN MÉMOIRE : le contrat d'erreurs du jalon suit la discipline I1 des numéros de syscall (une entrée = un bloc qui la déclare, la table grandit par révision) ; un état qui doit survivre à des appels vit en .bss ou en non-volatil sauvegardé — jamais en registre volatile (r8/r9 meurent dans les blocs de travail, r11 dans chaque syscall)

**Le constat qui fonde la décision (04/11, chantier M6-(a), Entrée 145).** Deux faits du build de la sonde, tous deux attrapés par les gardes AVANT tout vert :
(1) la leçon C1 a fonctionné EN DIRECT : le symbole @L_FATAL portait 36, le message réel en fait 37 (le saut de ligne final laissé hors du compte de l'auteur) — verifier_symboles a REFUSÉ le build : l'arithmétique de l'auteur est vérifiée par la machine, jamais crue ;
(2) le premier sous-programme .emit plaçait le préfixe (r8) et la longueur (r9) en registres volatils, puis appelait su-03 (le verdict) : su-02 et su-03 clobber r8/r9 comme registres de travail, et chaque syscall de su-01 détruit r11 — le préfixe et le verdict MOURAIENT au premier appel (l'exécution rendait deux lignes au lieu de quatre : la première émission du .emit écrivait à une adresse doublée, rendait EFAULT, et le flux tombait silencieusement dans l'arrêt fatal). L'oracle natif a REFUSÉ fail-closed — jamais un faux vert : c'est exactement le comportement que D146 exigeait du scellage, ici au niveau du build.

**La règle.** (1) **TOUTE entrée de la table ERRNOS (et de ses sœurs par profil) est MOTIVÉE PAR BLOC** : une entrée existe parce que le contrat d'un bloc la déclare (au M6-(a) : EBADF par su-04:E1, la sonde du descripteur) ; la table grandit par RÉVISION au chantier qui déclare de nouveaux errno attendus — jamais par caprice, jamais par avance : le miroir exact de la discipline I1 des numéros de syscall (tout numéro non motivé est un refus de build → toute entrée non motivée est un refus de build ; tout errno hors table est VERDICT_FATAL, arrêt propre nommé — le fail-closed n'est pas négociable). (2) **UN ÉTAT QUI DOIT TRAVERSER DES APPELS VIT EN MÉMOIRE (.bss) ou en non-volatil sauvegardé — JAMAIS en registre volatile** : r8/r9 (et leurs équivalents par ABI) sont les travailleurs d'UN appel, r11 (et ses équivalents) meurt dans CHAQUE syscall — la mémoire, elle, traverse tout ; le verdict de la sonde vit au tampon +32 (TAMPON_NUM), le brut traverse en r10 (registre de travail interne que ni su-01, ni su-02, ni su-03 ne touchent), les arguments du sous-programme (r8/r9) sont consommés AVANT le premier appel. (3) **La sortie d'un artefact de démonstration PORTE son verdict final en code de sortie** (la sonde : code 6 = VERDICT_FATAL constaté — la branche fatale est terminale PAR CONTRAT, la démonstration des deux branches est complète à la première exécution).

**Alternatives rejetées.** Pré-remplir la table d'errno plausibles (rejeté : une entrée non motivée est un mensonge en attente — le fail-closed exige que SEUL le déclaré soit nommé, tout le reste est fatal) ; sauvegarder l'état par push/pop de non-volatils dans le sous-programme (rejeté : plus lourd que le tampon .bss déjà exigé par le formatage hex, et la pile du _start n'a pas de cadre d'appelant — le réflexe resterait registre-centré, la règle veut le réflexe mémoire) ; compter sur l'ordre pratique des clobbers (« r8 survit à su-03 en l'occurrence ») (rejeté : la pratique d'un appel n'est pas un contrat — les specs déclarent les volatils détruits, le code y croit ; M7 en héritera, a0-a7 tous volatils en psABI LP64, AUCUNE zone rouge).

**Frontières.** La règle régit les tables de contrat d'erreurs et les plans de registres des blocs des jalons M6/M7 (héritage de méthode) ; elle ne touche NI la table HRESULTS du primaire (D79 — le profil Windows demeure), NI les octets des scellés Windows (invariance ASSERTÉE par D149), NI le hachoir m6/ (l'échelle D34 garde ses propres idiomes) ; la sonde est un DEV (balise 0.7.0-dev.1 POSÉE, jamais scellée — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté, la garde anti-rollback n'existe pas encore : un DEV vivant se reconstruit librement).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D150" in texte:
    sys.exit("ECHEC : D150 existe déjà")
if texte.count("## D149 —") != 1:
    sys.exit(f"ECHEC : D149 présente {texte.count('## D149 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D149 —") < nouveau.find("## D150")):
    sys.exit("ECHEC : ordre final inattendu (D150 avant D149)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D150 insérée à la suite de D149 — ordre recoupé")
