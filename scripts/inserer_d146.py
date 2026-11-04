#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d146.py — DECISIONS.md : insère D146 PAR SCRIPT À LA SUITE de
D145 (insertion ASSERTÉE : D145 présente une fois, D146 absente, D146
ajoutée APRÈS D145 — fin du fichier)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D146 — AUCUN SCELLAGE rc/final SANS UN CONTRÔLE D'EXÉCUTION FULL-PE À LA BASE RÉELLE DE L'IMAGE : l'émulation à base 0 n'est pas un témoin de l'exécution réelle — un RVA nu y résout par accident ; le contrôle exécute une requête routée SERVIE (ou nomme le crash) avant que la carte ne se scelle

**Le constat qui fonde la décision (04/11, run e3, Entrée 141).** Le proxy scellé 0.6.0-rc.1 est MORT sur la première requête routée jamais reçue (la sonde d'armement du run e3) : la ligne de flux — code entièrement nouveau M5 — lit le couple (RVA, longueur) de la table des méthodes dans .rdata et passe le RVA NU comme pointeur à la copie ; sur Windows (image à 0x140000000) la lecture à 0x24A0 est une violation d'accès qui tue le processus. L'idiome hérité (http-02:R1 : « mov edx, dword [table] ; add rdx, r12 » avec r12 = base d'image) avait été PERDU dans la révision. OR tout le corpus avait jugé ce code VERT : l'oracle différentiel D136 (200 cas du domaine relevé, la ligne de flux octet par octet), les harnais de révision, la conformité § 8.2 — parce que TOUTE l'émulation M5 mappe l'image À BASE 0 (RVA = adresse) : le RVA nu y est une adresse mappée VALIDE, le défaut y est INVISIBLE PAR PRINCIPE. La conformité lit le PE sans l'exécuter ; les oracles exécutent les blocs à base 0. Aucun contrôle n'exécutait jamais l'image À SA BASE RÉELLE.

**La règle.** (1) Avant TOUT scellage rc ou final d'un artefact proxy, un CONTRÔLE D'EXÉCUTION À LA BASE RÉELLE doit être VERT : l'image PE entière est chargée à sa base préférée (0x140000000), l'IAT remplie par la marche des descripteurs, la ligne de commande réelle passée, et AU MOINS UNE REQUÊTE ROUTÉE EST SERVIE EN ÉMULATION (requête → réponse au client, ou refus nommé du contrat) — le crash, s'il existe, est NOMMÉ (adresse, instruction, bloc) AVANT la carte. (2) Le harnais de ce contrôle est un LIVRABLE DU JALON, rejouable par script, aux côtés des oracles — le défaut du rc.1 a été attrapé par le sien (scripts/reproduire_run_e3.py, modèle emulation_forensique D52h : base relogée, IAT marchée, fils coopératifs par CreateThread, sockets scriptées). (3) La preuve chirurgicale reste disponible à tout doute : le correctif SIMULÉ au crochet (jamais dans le binaire) qui fait renaître la chaîne isole la cause mieux qu'un diff.

**Frontières.** La règle s'applique aux GESTES DE SCELLAGE futurs (elle ne reconstruit rien a posteriori) ; elle ne remplace NI les oracles différentiels (la logique), NI la conformité § 8.2 (la structure) — elle couvre l'angle mort des deux : l'adressage RÉEL de l'image chargée ; elle n'exonère pas le run terrain (le critère (b) de D136 reste le juge du relèvement PAR LE NAVIGATEUR) ; l'émulation reste des API SHIMMÉES (winsock, secur32) — le contrôle constate l'adressage et le chemin de session, pas la vraie Schannel.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D146" in texte:
    sys.exit("ECHEC : D146 existe déjà")
if texte.count("## D145 —") != 1:
    sys.exit(f"ECHEC : D145 présente {texte.count('## D145 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D145 —") < nouveau.find("## D146")):
    sys.exit("ECHEC : ordre final inattendu (D146 avant D145)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D146 insérée à la suite de D145 — ordre recoupé")
