#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d148.py — DECISIONS.md : insère D148 PAR SCRIPT À LA SUITE de
D147 (insertion ASSERTÉE : D147 présente une fois, D148 absente, D148
ajoutée APRÈS D147 — fin du fichier)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D148 — LES VERDICTS DE SCÉNARIO SE RENDENT POST-MORTEM ET SUR PIÈCES : le rc « producteur » d'un verdict ne doit JAMAIS être le rc d'un processus à capture aveugle, et la preuve navigateur d'une page d'erreur vit À LA RÉCEPTION (jamais au DOM headless d'une 502 nue) — D138/D145 portées aux verdicts par le run e4 ; la matrice curl S3 est l'état stationnaire de la VM (jamais une régression du proxy)

**Le constat qui fonde la décision (04/11, run e4, Entrée 143).** Le scénario e3-==-e4 a rendu « ÉCHEC NOMMÉ (5) » alors que les pièces établissent le critère (b) de D136 PRÉSENT : les CINQ refus sont des artefacts d'instrument, dont QUATRE procèdent d'une SEULE cécité — le rc d'Edge capturé VIDE (la capture ExitCode est aveugle dans cette famille de VM, constat v6/complément d'arrêt D138). Le mécanisme : le helper Verdict-Vue prévoyait une branche RÉSERVE pour les « vues vides » — « producteur rc=0 — pièce à confirmer au labo » — mais son témoin de producteur était le rc d'EDGE, vide : la réserve devint ÉCHEC (AUTORITE-A-SERVIE, POIGNEE-B-REFUSEE), le rc vide fit échouer NAVIGATEUR-A/B, et le DOM vide du run B (Edge headless n'émet NI DOM NI CAPTURE pour une navigation échouée) fit nommer DOM-B-INVALIDE. Deux des ÉCHEC étaient des RÉSERVES prévues, transformées par un témoin aveugle.

**La règle.** (1) AUCUN verdict de scénario ne se rend sur une lecture EN LIVE d'un journal dont le producteur VIT (D145 étendue des gardes AUX VERDICTS) : les journaux se jugent POST-MORTEM (après la mort du producteur — le modèle v8 des verdicts proxy, après le quit) ou AU LABO sur pièces (D138). (2) LE TÉMOIN DE PRODUCTEUR d'un verdict (le rc qui distingue RÉSERVE d'ÉCHEC) doit être le rc d'un processus à capture FIABLE dans la VM — JAMAIS un rc connu aveugle (Edge, les autorités dans cette famille : le rc du PROXY par console capture, lui, est fiable) ; à défaut de rc fiable, la branche est la RÉSERVE (la pièce tranche au labo), jamais l'ÉCHEC. (3) LA PREUVE NAVIGATEUR D'UNE PAGE D'ERREUR vit À LA RÉCEPTION : une 502 NUE (ligne de statut sans corps — TXT_502_CERT 34 o, design M5 depuis 0.5.1/D140) échoue le chargement Chromium avec ERR_HTTP_RESPONSE_CODE_FAILURE et le headless n'émet alors ni DOM ni capture — le DOM-B-502 (grep « 502 » au DOM) est STRUCTURELLEMENT INSATISFIABLE sur ce build pour notre 502 ; la réception se prouve par le RECROISEMENT de producteurs indépendants : la ligne de flux servie (s=34) + l'événement nommé au journal proxy (« certificat rejete ») + la poignée refusée au journal autorité + l'erreur réseau du navigateur lui-même (ERR_HTTP_RESPONSE_CODE_FAILURE : elle n'existe QUE si le code d'erreur HTTP fut reçu). (4) LA MATRICE CURL : la branche S3 (révocation hors ligne de CURL, CERT_TRUST_REVOCATION_STATUS_UNKNOWN strict vs --ssl-no-revoke) est L'ÉTAT STATIONNAIRE de la VM (v6, v8, e4 : pièces identiques octet pour octet) — D140 concernait les credentials DU PROXY (preuve : le tunnel du run A s'établit hors ligne), jamais curl ; le libellé « RÉGRESSION à nommer » des scénarios e2-e4 (écrit en attendant S4) est une expectation périmée, à corriger à la prochaine vague de scénario.

**Alternatives rejetées.** Faire du verdict du scénario une autorité sur le run (rejeté : c'est le renversement exact de D138 — la vue in-VM est un diagnostic, JAMAIS un verdict ; l'instrument ne peut pas se juger lui-même) ; donner un corps à la 502 pour la rendre visible au DOM (rejeté : TXT_502_CERT est un fait SCELLÉ de la lignée 0.5.1→0.6.0, 34 octets exacts — modifier une réponse du scellé pour un caprice d'instrumentation serait la pire des inversions) ; capturer le rc d'Edge par un mécanisme contourné (rejeté au labo : SANS Windows sous la main, un contournement non testé serait une foi nouvelle dans un instrument non prouvé — la règle (2) rend le problème MOOT : on ne câble plus un témoin aveugle).

**Frontières.** La règle régit les SCÉNARIOS DE RUN futurs (livrables du labo, jamais un scellé) ; elle ne rétro-écrit PAS le scénario e3-==-e4 (la vague e4 est archivée avec ses libellés — le présent verdict juge sur pièces, c'est le modèle) ; le critère (b) de D136 reste ce qu'il est (la page servie ET la 502 reçues PAR LE NAVIGATEUR — la réception triplement recoupée fait foi, le rendu de la page d'erreur reste une réserve INSTRUMENTALE nommée, démontrable seulement par un navigateur fenêtré) ; la finale 0.6.0 est posée sur la validation consignée (Entrée 143) — la règle ne la remet pas en cause, elle en documente le chemin de preuve.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D148" in texte:
    sys.exit("ECHEC : D148 existe déjà")
if texte.count("## D147 —") != 1:
    sys.exit(f"ECHEC : D147 présente {texte.count('## D147 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D147 —") < nouveau.find("## D148")):
    sys.exit("ECHEC : ordre final inattendu (D148 avant D147)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D148 insérée à la suite de D147 — ordre recoupé")
