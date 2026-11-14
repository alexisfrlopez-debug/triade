#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 291 + Task 198 : LE GUIDE DE LA
LIGNE C DE L'ATELIER (la question du développeur : « je ne sais pas où
trouver la ligne C de l'atelier ») — la réponse sur pièces : la ligne
C-loupe-01-it1 n'existe pas encore, elle est à ÉCRIRE à la main du
développeur (l'onglet 5 · LIVRAISON du GUI) ; le livre qui compte est
l'atelier 013520 (UNE ligne : la T) ; LE PIÈGE NOMMÉ : l'état du GUI
vise encore l'atelier 012347, la copie imbriquée VIDE — le bon livre se
choisit au bouton « CHOISIR L'ATELIER EXISTANT… » de l'étape 2."""
import pathlib

REPO = pathlib.Path("/home/z/my-project/work/triade")

WORKLOG = """

Task ID: 198
Agent: Z.ai (agent principal — la session du guide : où vit la ligne C de l'atelier)
Task: LA QUESTION DU DÉVELOPPEUR (« je ne sais pas où trouver la ligne C de l'atelier ») : LA RÉPONSE SUR PIÈCES — la ligne C (C-loupe-01-it1) N'EXISTE PAS ENCORE, elle est À ÉCRIRE à la main du développeur (l'onglet 5 · LIVRAISON du GUI — le labo ne fabrique JAMAIS une ligne de mesure) ; le livre qui compte est l'atelier 013520 (quatre pièces, UNE ligne : la T) ; LE PIÈGE NOMMÉ : l'état du GUI vise encore l'atelier 012347, la copie imbriquée VIDE — le bon livre se choisit au bouton « CHOISIR L'ATELIER EXISTANT… » de l'étape 2.

Work Log:
- LA SONDE DES MIROIRS (89, avant toute réponse) : GitHub main @ 60d285e4 == le local (le push de la 290 A VÉCU) ; triade-history.bundle == l'état 290 local (77 422 062 o, a4c7a885…) ; D141 tenu (triade-history-288-ad9d2f5.bundle aux archives-bundles/, 95 bundles archivés) ; les TROIS textes du miroir (worklog, JOURNAL, la carte) identiques octet pour octet — LA PASSATION 290 EST COMPLÈTE, aucune dette derrière la session.
- LA SONDE DE L'ATELIER (90, au coffre) : /test/Nouveau run/test/TRIADE_gui_tous_runs_v1/atelier-campagne-d204-20261114-013520/ — QUATRE pièces (livraisons.csv, carnet_temps_humain.csv, defauts.csv, journal-ouverture.txt) ; livraisons.csv porte UNE ligne : T-loupe-01-it1,T,loupe-01,1,2026-11-14,2026-11-14,VERT,en attente — LA LIGNE C DEMEURE ABSENTE : la question du développeur était fondée, le livre attend son geste.
- LE GUIDE DONNÉ (toute en gestes du GUI tous-runs, consigné au chat) : ① LANCER-GUI-TOUS-RUNS.bat ; ② ÉTAPE 2 — LE PIÈGE : l'état vise l'atelier 012347 (la copie vide, 0 livraison) — « CHOISIR L'ATELIER EXISTANT… » et désigner le livre 013520 (sur la machine : à côté du kit couru — D:\\Downloads\\Runs Triade\\test\\TRIADE_gui_tous_runs_v1\\atelier-campagne-d204-20261114-013520 ; la marque du bon livre : sa livraisons.csv porte la ligne T) ; ③ ÉTAPE 4 · LES QUATORZE UNITÉS : la ligne C-loupe-01 → « OUVRIR L'UNITÉ CHOISIE → » ; ④ l'onglet « 5 · LIVRAISON » : LA DATE DU KIT 2026-11-14, LA DATE DU RUN 2026-11-14, LE VERDICT VERT (le run 15 VERT 0 ROUGE recoupé à la 287), LE RECOUP « en attente » (le recoup appartient au labo après le dépôt) ; ⑤ « CONSIGNER LA LIVRAISON » — la ligne naîtra C-loupe-01-it1,C,loupe-01,1,2026-11-14,2026-11-14,VERT,en attente, l'unité CLOSE au premier vert (§ 7, 1/3) ; ⑥ l'atelier ENTIER renvoyé au coffre /test — LES ONGLETS COMPAGNONS (attendus depuis la 287) : 4 · CARNET (le temps humain de la session C), 6 · DÉFAUTS (si un défaut se nomme), 7 · CHRONO (la mesure M4).
- LA CONSIGNATION : la présente Entrée 291 + Task 198 ; la carte OU-TROUVER portée à 291 ; l'atelier guide-ligne-C-291/ au dépôt (les sondes 89 et 90).
- SUITE : au développeur — LE GESTE ONGLET 5 (la ligne C au livre 013520), PUIS le run de l'unité 2 aux deux bras (les DEUX kits sont au /test) ; ENSUITE loupe-05 sha256, aux deux bras — le labo construit à la commande.
"""

JOURNAL = """

## Entrée 291 — LE GUIDE DE LA LIGNE C : où vit la ligne, comment elle naît (la question du développeur : « je ne sais pas où trouver la ligne C de l'atelier »)

- LA RÉPONSE COURTE : la ligne C ne se TROUVE nulle part — elle S'ÉCRIT. C-loupe-01-it1 est la ligne de livraison du run vert du bras C (recoupé à l'Entrée 287 : 15 VERT 0 ROUGE, la pièce 85b34ed4… == la gravure) ; elle vit dans livraisons.csv de L'ATELIER, et l'atelier qui compte est atelier-campagne-d204-20261114-013520 — au coffre : /test/Nouveau run/test/TRIADE_gui_tous_runs_v1/atelier-campagne-d204-20261114-013520/ (quatre pièces, UNE ligne : la T) ; elle naît de la MAIN du développeur à l'onglet 5 · LIVRAISON du GUI — le labo ne fabrique jamais une ligne de mesure.

- LE PIÈGE NOMMÉ (pourquoi la ligne est introuvable) : l'état du GUI (etat-tous-runs.json) vise ENCORE l'atelier 012347 — la copie imbriquée VIDE (0 livraison, née 01:23:47) — et NON le livre 013520. La session ouverte sur le mauvais livre ne montre aucune ligne : à l'étape 2, « CHOISIR L'ATELIER EXISTANT… » désigne le 013520 (sur la machine : à côté du kit couru — D:\\Downloads\\Runs Triade\\test\\TRIADE_gui_tous_runs_v1\\atelier-campagne-d204-20261114-013520). La marque du bon livre : sa livraisons.csv porte la ligne T-loupe-01-it1.

- LE GESTE ENTIER (le GUI tous-runs) : étape 4 → la ligne C-loupe-01 → « OUVRIR L'UNITÉ CHOISIE → » → l'onglet « 5 · LIVRAISON » → LA DATE DU KIT 2026-11-14, LA DATE DU RUN 2026-11-14, LE VERDICT VERT, LE RECOUP « en attente » → « CONSIGNER LA LIVRAISON ». La ligne naîtra : C-loupe-01-it1,C,loupe-01,1,2026-11-14,2026-11-14,VERT,en attente — l'unité CLOSE au premier vert (§ 7). Puis l'atelier ENTIER renvoyé au coffre /test.

- LES ONGLETS COMPAGNONS (attendus depuis la 287) : 4 · CARNET (le temps humain de la session C), 6 · DÉFAUTS (si un défaut se nomme), 7 · CHRONO (la mesure M4).

- LES MIROIRS À L'OUVERTURE (la sonde 89, VERT partout) : GitHub main @ 60d285e4 == le local ; le bundle == l'état 290 ; D141 tenu (95 bundles aux archives) ; les trois textes identiques — la passation 290 est complète, aucune dette. (14/11, la session du guide)
"""

ITEM_18 = """
18. **LE GUIDE DE LA LIGNE C DE L'ATELIER — OÙ ELLE VIT, COMMENT ELLE NAÎT (Entrée 291)** : la question du développeur (« je ne sais pas où trouver la ligne C ») — la ligne C-loupe-01-it1 N'EXISTE PAS ENCORE, elle est à écrire à la main (l'onglet 5 · LIVRAISON, jamais le labo) ; le livre qui compte : atelier-campagne-d204-20261114-013520 (au coffre sous /test/Nouveau run/test/TRIADE_gui_tous_runs_v1/, UNE ligne : la T) ; LE PIÈGE NOMMÉ : l'état du GUI vise l'atelier 012347, la copie vide — le bon livre se choisit à « CHOISIR L'ATELIER EXISTANT… » (étape 2) ; le geste : étape 4 → C-loupe-01 → onglet 5 (kit 2026-11-14, run 2026-11-14, VERT, recoup « en attente ») → CONSIGNER ; les miroirs VERT à l'ouverture (la passation 290 tenue : GitHub @ 60d285e, le bundle, D141, les trois textes) ; LA SUITE : le geste, puis le run de l'unité 2 aux deux bras.
"""

with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(JOURNAL)

carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
txt = carte.read_text(encoding="utf-8")
txt = txt.replace("Entrées 251-290", "Entrées 251-291")
txt = txt.replace("Tasks 158-197", "Tasks 158-198")
if not txt.endswith("\n"):
    txt += "\n"
txt += ITEM_18
carte.write_text(txt, encoding="utf-8", newline="\n")
print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md + la carte OU-TROUVER — "
      "l'Entrée 291 + Task 198")
