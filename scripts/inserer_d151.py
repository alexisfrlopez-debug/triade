#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d151.py — DECISIONS.md : insère D151 PAR SCRIPT À LA SUITE de
D150 (insertion ASSERTÉE : D150 présente une fois, D151 absente, D151
ajoutée APRÈS D150 — fin du fichier, modèle inserer_d150.py)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D151 — ABSENT ≠ ILLISIBLE (une carte présente et indéchiffrable est un REFUS, jamais une permission) ; L'INSTRUMENT DE MUTATION NOMME SON GESTE (jamais un poser nu) ; LA FALSIFICATION EST EXHAUSTIVE PAR INSTRUCTION (un résidu de registre ne guérit plus rien) ; UN BLOC HORS-CHEMIN est épuisé par SON scénario, ET L'ENTRANT CONCURRENT PORTE SES ENTRÉES LOCALES — chaque refus traversé au chantier fonde sa règle écrite au code du build

**Le constat qui fonde la décision (04/11, chantier M6-(b), Entrée 146 — le geste interrompu à 14:40, repris et conduit jusqu'au vert).** Le corpus paritaire a traversé SES REFUS un à un, chaque refus nommé (fail-closed, jamais un faux vert) fondant une correction puis la présente règle :
(1) l'incident de l'état zéro : `m1/build_m1.py` lancé SANS argument a tourné — la garde de l'ère m1 traite « carte illisible » comme « absente » (`except ErreurCarte: pass`) et échoue OUVERTE ; selftest.exe est resté OCTET-IDENTIQUE, la carte m1 régénérée a été RESTAURÉE octet-pour-octet depuis git — le constat structurel est né : TOUTES les gardes m1→m5 (l'ère D147 comprise) échouent ouvertes sur carte illisible ;
(2) le SEGFAULT MUET de l'autotest : `img.poser` écrivait une page R sans ouverture — l'oracle est mort en silence au lieu de refuser ;
(3) « libc-08 falsifié : N=19 » : la fixture SC sert les DEUX sens (v6 inférieur memcmp(SA,SC)<0, v7 supérieur memcmp(SC,SA)>0) — l'oracle croyait « +1 devient 0 », la notation constatait DEUX verdicts perdus : l'attendu est corrigé SUR PIÈCES ;
(4) le SEGFAULT DÉTERMINISTE du journal (tcp-11:R2) : `add r12, rax` placé APRÈS le `call @A_MEMCPY` — memcpy rend dst (UNE ADRESSE, Q2 de son contrat), jamais la longueur : le compteur de longueur recevait une adresse géante et le suffixe sortait du mapping ; ET le staging (journal v2) portait LE MÊME PIÈGE — le remplaçant est corrigé AVANT d'être embarqué (il aurait crashé au chantier (d) dès un appel réel avec champ) ;
(5) « tcp-11 concurrence : verdicts divergents » : la cartouche n'était pas ré-entrante — entrées, sorties, sauvegarde de pile et pages PARTAGÉES entre threads : deux appels simultanés s'écrasaient mutuellement ;
(6) « libc-06 PASSÉ SILENCIEUX » : la mutation de la première instruction était « guérie » par un RÉSIDU DE REGISTRE (lea r8 muté, le store [r8] tombait encore sur le curseur — r8 résiduel de l'appelant) ;
(7) « tcp-07 : 78 mutations TOUTES silencieuses » : tcp-07 est HORS-CHEMIN du principal (corpus-13 ne l'appelle pas — la démonstration du patch est le chantier (d)) : AUCUNE corruption d'un bloc non exécuté ne peut dévier l'artefact, c'est un FAIT DE PLAN.

**La règle.** (1) **ABSENT ≠ ILLISIBLE** : une carte (ou toute pièce d'état) PRÉSENTE et indéchiffrable est un REFUS, jamais une permission — `build_corpus.py` distingue les deux dès sa naissance ; le correctif des cinq chaînes historiques (m1→m5) est un geste SÉPARÉ nommé pour le développeur, aucune urgence (les cartes m1→m4 sont des scellés d'archives, seule m5 vit sous la phrase du jour). (2) **L'INSTRUMENT DE MUTATION NOMME SON GESTE** : ouvrir mprotect RW, écrire, RESTAURER la protection trouvée ; en mode partagé : refus nommé — jamais un poser nu (le segfault est un refus muet, la pire espèce). (3) **UNE ADRESSE RENDUE N'EST JAMAIS UNE LONGUEUR** : la longueur se capture AVANT l'appel qui détruit son support volatile (memcpy rend dst, Q2 — l'add déplacé AVANT le call) ; le staging remplaçant est vérifié par le MÊME oracle AVANT d'être embarqué. (4) **L'ENTRANT CONCURRENT PORTE SES ENTRÉES LOCALES** : entrées LOCALES à l'appel, sommet attribué PAR APPEL sous un verrou court (pas 0x800), fenêtre de sorties par appel [sommet-0x200, sommet-0x1B8] — sous la profondeur d'imbrication maximale (corpus-13 → autotest/journal → feuilles), les cadres imbriqués n'y touchent jamais. (5) **LA FALSIFICATION EST EXHAUSTIVE PAR INSTRUCTION** : un bloc est rompu dès qu'une mutation dévie — un résidu de registre ne guérit plus rien ; l'attendu d'une falsification se corrige SUR PIÈCES (le différentiel des DEUX sens de la fixture). (6) **UN BLOC HORS-CHEMIN est épuisé par SON scénario** (tcp-07 : apply/rollback/effet, intégrité staging code 3, refus code 5) et par le V7 DEP EN FILS (la constante RWX 0x7 mutée en 0x3 : la page du code devient R+W sans X, le RET du patch lui-même faute — SIGSEGV constaté en fils, le père observe, le fils meurt : le code défaillant ne tue jamais l'instrument) ; le travailleur d'un test TERMINE ses lignes (le journal émet ce qu'on lui donne — son contrat), la fenêtre de scan d'un immédiat couvre le slot entier (0x60 → 0x200 : l'immédiat vit à +0x6e).

**Alternatives rejetées.** Considérer l'illisible comme absent (rejeté : c'est exactement le trou par lequel la garde s'éteint — l'échec ouvert de l'ère m1 est le constat, la règle le ferme) ; muter l'image sans nommer le geste mprotect (rejeté : le poser nu est un segfault muet — un échec qui n'enseigne rien) ; guérir une falsification par un résidu de registre (rejeté : le silence d'une mutation est un faux vert — l'exhaustivité par instruction est la seule mesure) ; compter tcp-07 dans le chemin du corpus-13 (rejeté : la démonstration du patch est le chantier (d) ; un fait de plan se NOMME, jamais ne se force) ; la ré-entrance par pages partagées et sommet fixe (rejeté : deux appels simultanés s'écrasent mutuellement, les verdicts divergent — l'instrument ment) ; corriger le journal v2 au chantier (d) (rejeté : le remplaçant embarqué aurait crashé dès le premier appel réel avec champ — un staging se vérifie AVANT l'embarquement).

**Frontières.** La règle régit les instruments de test et les chaînes de build des jalons (garde d'état, mutation, falsification, concurrence) ; elle ne touche NI les octets des scellés Windows (invariance ASSERTÉE par D149, mesurée par `diff_nul.py` à chaque build), NI le hachoir m6/ (l'échelle D34 garde ses propres idiomes), NI la table ERRNOS (D150 demeure) ; le corpus est un DEV (balise 0.7.0-dev.2 POSÉE par geste de BUILD, jamais scellée — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le contrôle D146 adapté, la garde anti-rollback n'existe pas encore : un DEV vivant se reconstruit librement, le plancher demeure 0.7.0-dev.1).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D151" in texte:
    sys.exit("ECHEC : D151 existe déjà")
if texte.count("## D150 —") != 1:
    sys.exit(f"ECHEC : D150 présente {texte.count('## D150 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D150 —") < nouveau.find("## D151")):
    sys.exit("ECHEC : ordre final inattendu (D151 avant D150)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D151 insérée à la suite de D150 — ordre recoupé")
