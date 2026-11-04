#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d145.py — DECISIONS.md : insère D145 PAR SCRIPT À LA SUITE de
D144 (insertion ASSERTÉE : D144 présente une fois, D145 absente, D145
ajoutée APRÈS D144 — fin du fichier)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D145 — AUCUNE GARDE DE SCÉNARIO NE DÉPEND D'UNE LECTURE EN LIVE D'UN FICHIER EN COURS D'ÉCRITURE DANS LA VM : les gardes sont FONCTIONNELLES (port ouvert, réponse attendue) ou POST-MORTEM — D138 étendue aux gardes ; la preuve déclarative CONSTATE, la preuve opérative GARDE

**Le constat qui fonde la décision (04/11, run e2, Entrée 138).** Le scénario e2 a introduit la PREMIÈRE garde en live d'un fichier en cours d'écriture : attendre la ligne « relever-https arme » du journal proxy sous 20 s, AVANT le navigateur (REFUS PROXY-SANS-ARMEMENT sinon). Le run a été REFUSÉ sur cette garde — alors que les pièces établissent que l'armement AVAIT eu lieu : la sonde TCP réussit à 00:13:17 (l'écoute était posée, donc bannière et armement — qui la PRÉCÈDENT au contrat http-12:R3 Q3 — étaient déjà écrits, par UNE WriteFile PAR LIGNE, tcp-11 Q1, aucun tampon applicatif), et la pièce post-mortem (128 o) porte les 7 lignes complètes du run. La lecture (PowerShell, dans la VM) d'un fichier du dossier mappé C:\\preuves dont le handle d'écriture appartient à un processus VIVANT rend ZÉRO octet — le contenu n'apparaît qu'à la fermeture du handle. C'est le MÊME symptôme que les « vues vides depuis la VM » des runs v7/v8 (réserves POIGNEE-B-REFUSEE : vues vides, producteur rc=0, pièces complètes jugées au labo — D138), troisième constat : v7, v8, e2. Le scénario v8 ne lisait le journal proxy qu'APRÈS le quit (verdicts post-mortem) : la garde en live du e2 était une RÉGRESSION de conception — le fail-closed précoce a fait son travail (refuser plutôt que prouver en vain), mais sur un instrument qui ne peut pas répondre.

**La règle.** (1) Toute garde fail-closed d'un scénario de run se fonde sur un état OBSERVABLE PENDANT le run : un PORT ouvert (sonde TCP) ou une RÉPONSE reçue (test fonctionnel) — JAMAIS le contenu d'un fichier en cours d'écriture par un processus vivant, quel que soit le dossier (mappé ou local : un buffer applicatif produit le même symptôme, v7/v8). (2) Les fichiers journaux sont jugés POST-MORTEM (après la mort du producteur — modèle v8 : verdicts après le quit) ou AU LABO sur pièces (D138 : le rc du producteur fait foi, les pièces host sont jugées au laboratoire). (3) La preuve DECLARATIVE (une ligne de journal) ne GARDE rien — elle CONSTATE ; la preuve OPÉRATIVE (une réponse qui traverse la chaîne exigée) GARDE.

**L'application (la correction e3, proposée à l'Entrée 138).** La garde d'armement devient FONCTIONNELLE : le scénario envoie par TCP au mandataire la requête forme-absolue CLAIRE du navigateur (« GET http://127.0.0.1/ HTTP/1.1 » + Host) et attend la page 200 de l'autorité A — relèvement http→https + tunnel + réponse = preuve OPÉRATIVE que le proxy est ARMÉ (un binaire non armé routerait vers l'origine port 80, muette : 502) ; REFUS PROXY-PAS-ARME nommé sinon ; la page reçue copiée en pièce. La ligne « relever-https arme » devient un VERDICT post-mortem (après le quit — modèle v8).

**Frontières.** La règle ne touche AUCUN scellé (elle régit les scénarios de run, livrables du labo) ; le critère (b) de D136 reste ce qu'il est (la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR — la sonde fonctionnelle est une GARDE, jamais une preuve du critère navigateur) ; le phénomène intime de la vue vide (couche du dossier Sandbox ou buffer applicatif) n'est pas tranché — la règle s'applique aux DEUX mécanismes connus.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D145" in texte:
    sys.exit("ECHEC : D145 existe déjà")
if texte.count("## D144 —") != 1:
    sys.exit(f"ECHEC : D144 présente {texte.count('## D144 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D144 —") < nouveau.find("## D145")):
    sys.exit("ECHEC : ordre final inattendu (D145 avant D144)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"D145 insérée ({len(DECISION)} caractères) — après D144, ordre recoupé")
