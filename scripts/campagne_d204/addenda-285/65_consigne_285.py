#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 285 + Task 192 (addenda) : le bac du
labo reconstitué après la remise à zéro du conteneur — l'état 284 re-recoupé
du coffre ; l'écart nommé du récit au chat ; la reprise du bras C donnée."""
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/work/triade")
SCRIPTS = pathlib.Path("/home/z/my-project/scripts")

WORKLOG = """

Task ID: 192
Agent: Z.ai (agent principal — la session de la reprise du bac et de la réponse au développeur)
Task: LA REMISE À ZÉRO DU CONTENEUR DU LABO VÉCUE ENTRE DEUX SESSIONS (le bac local revint vers l'état 276 — AUCUNE pièce permanente touchée : le coffre Drive, le miroir et GitHub demeurent la vérité) ; la question du développeur reçue : « je ne sais pas quoi faire pour continuer » — les DEUX « go » de la session précédente (la consignation 284, le kit loupe-01 × bras C) étaient DÉJÀ intégralement exécutés (b6b8469 poussé à 10:16:59Z, le kit au coffre 12/12) ; la réponse donnée : LA REPRISE DU BRAS C au GUI.

Work Log:
- LE RE-RECOUP DU COFFRE (tout revérifié, octet pour octet) : le /test sondé — RIEN de neuf depuis la dernière pièce du kit C (14/11 10:14:13Z) ; 139 pièces re-rapatriées (le « Nouveau run » entier, les TROIS kits loupe-01, les trois textes du miroir, la carte des kits, le MANIFESTE) ; le kit C re-recoupé 10/10 à sa gravure EMPREINTES (la DLL 85b34ed4…, le source 860ff1cf…, le scénario a21c5e19…, les QUATRE témoins octet pour octet ceux du kit T) ; T0 re-recoupé : loupe.exe 4d119b22… == le sha que porte le témoin signé, la v1 == la v2 ; le plan a78caf8c… VERROUILLÉ ; le livre re-lu : « T-loupe-01-it1,…,VERT » ; la carte OU-TROUVER à 284 (racine == miroir) ; le bundle courant : histoire complète, main @ 6a0d3de — GitHub interrogé À L'API : main @ 6a0d3de (LE PUSH DE LA 284 A VÉCU) ; le dépôt local resynchronisé au bundle.
- L'ÉCART NOMMÉ (D189) : le récit du GUI collé au chat porte DEUX chiffres qui ne sont pas ceux des pièces — « cristallisation, 6 minute(s) » (les pièces : 85 minutes) et « verdict ROUGE » (les pièces : « verdict VERT » au journal du GUI, « VERT » au livre) ; LE RÉCIT N'EST PAS LA PIÈCE ; l'atelier « 012347 — 0 livraison(s) » est la copie IMBRIQUÉE du GUI, vide — le livre qui compte est l'atelier 013520 rendu ENTIER au coffre ; si un nouveau run fut vécu dans cette copie, sa pièce n'est jamais jetée : renvoyé TEL QUEL, il sera recoupé.
- LA CONSIGNATION : la présente Entrée 285 + Task 192 ; la carte OU-TROUVER portée à 285 ; D141 tenu avant le commit (le courant 284-6a0d3de archivé versionné au miroir) ; le commit + le push GitHub au jeton ghp_ du /tokens ; le miroir Drive synchronisé, chaque geste recoupé par re-téléchargement.
- SUITE : au développeur — LA REPRISE DU BRAS C (télécharger kit-unite-loupe-01-C-20261114 du /test ; au GUI : 1·KIT choisir → 2·RUN lancer LANCEUR-UNITE-01-C.bat → 3·TÉMOIN dater, signer de la main → preuves-unite01C/ ENTIER au /test ; onglets 4-7) ; puis le labo recoupe et la campagne continue (loupe-02 × T ou l'appariement que le développeur arbitre) ; non bloquant : les deux jeux d'annotations pour la réplication, la commande réelle des unités 13-14.
"""

JOURNAL = """

## Entrée 285 — (addenda) LE BAC DU LABO RECONSTITUÉ APRÈS LA REMISE À ZÉRO DE SON CONTENEUR — L'ÉTAT 284 RE-RECOUPÉ DU COFFRE, RIEN N'A CHANGÉ : LE COFFRE EST LA VÉRITÉ (la question du développeur : « je ne sais pas quoi faire pour continuer »)

- L'ÉVÉNEMENT (l'infrastructure du labo, nommée telle quelle) : le conteneur du labo fut recyclé entre deux sessions — le bac local revint vers l'état 276 (les 59 pièces du « Nouveau run », les ateliers de construction du bras C, les scripts des Entrées 277-284 perdus du SEUL bac) ; AUCUNE pièce permanente ne fut touchée : le coffre Drive, le miroir TRIADE-sauvegarde-git et le dépôt GitHub demeurent LA vérité — la remise à zéro d'un bac ne muta RIEN de la chaîne, et la présente addenda le prouve par le re-recoup intégral.

- LE RE-RECOUP (tout revérifié du coffre, octet pour octet) : le /test sondé — RIEN de neuf depuis le kit du bras C (sa dernière pièce née le 14/11 10:14:13Z, rien à recevoir du développeur) ; 139 pièces re-rapatriées (le « Nouveau run » entier, les TROIS kits loupe-01, les trois textes du miroir, la carte des kits, le MANIFESTE de la Cérémonie — le manifeste du rapatriement vit au bac) ; LE KIT C re-recoupé : 10/10 pièces == la gravure EMPREINTES (la DLL 85b34ed4…, le source 860ff1cf…, le scénario a21c5e19…, les QUATRE témoins octet pour octet ceux du kit T, le zip cde28986… re-téléchargé intact) ; T0 re-recoupé : loupe.exe 4d119b22… == le sha que porte le témoin signé, la pièce du kit v1 == celle de la v2 (elle n'a jamais bougé) ; le plan a78caf8c… VERROUILLÉ ; le livre re-lu : livraisons.csv porte « T-loupe-01-it1, T, loupe-01, 1, 2026-11-14, 2026-11-14, VERT, en attente » et le journal du GUI « la livraison T-loupe-01-it1 est consignée (1/3, verdict VERT) », « cristallisation, 85 minute(s) » ; la carte OU-TROUVER à 284 (la racine == le miroir) ; le bundle courant : l'histoire complète, main @ 6a0d3de — ET GitHub interrogé à l'API : main @ 6a0d3de (« Entrée 284 + Task 191 » b6b8469 poussé à 10:16:59Z — LE PUSH A VÉCU) ; le dépôt local resynchronisé au bundle (l'état 284).

- L'ÉCART NOMMÉ (D189 — jamais maquillé) : le récit du GUI collé au chat par le développeur porte DEUX chiffres qui ne sont pas ceux des pièces — « cristallisation, 6 minute(s) » (les pièces : 85 minutes, M3) et « verdict ROUGE » (les pièces : « verdict VERT » au journal du GUI, « VERT » au livre de l'atelier) ; LE RÉCIT N'EST PAS LA PIÈCE — le dossier ENTIER revenu au coffre est la vérité, recoupé octet pour octet ; la ligne « L'ATELIER EXISTANT est repris … atelier-campagne-d204-20261114-012347 — 0 livraison(s) y vivent » : la copie IMBRIQUÉE du GUI, dont l'atelier né à 01:23:47 ne reçut JAMAIS la livraison du matin — le livre qui compte est l'atelier 013520, rendu ENTIER au coffre dans le « Nouveau run » ; si un NOUVEAU run fut vécu dans cette copie imbriquée, sa pièce n'est jamais jetée : qu'il soit renvoyé TEL QUEL, le labo le recoupera et l'écart sera nommé.

- LA RÉPONSE (la suite, tout au clic) : l'unité T-loupe-01 est CLOSE à it1 (§ 7 du plan — l'arrêt au premier vert recoupé : RIEN à refaire de ce bras) ; LA REPRISE EST LE BRAS C, le kit vit au coffre depuis 10:13:45Z : télécharger kit-unite-loupe-01-C-20261114 du /test → au GUI (LE MÊME dossier que le matin, celui dont l'atelier porte la ligne VERT), étape 4, unité loupe-01 × C : onglet 1·KIT CHOISIR le dossier (le GUI recoupe la gravure — une divergence, rien ne court) → onglet 2·RUN LANCER LANCEUR-UNITE-01-C.bat (sa console officielle : le scénario charge la DLL, découvre les exports par la table, juge par le modèle indépendant, écrit le témoin — preuves-unite01C/ naît) → onglet 3·TÉMOIN : DATER, SIGNER DE LA MAIN (D99), renvoyer preuves-unite01C/ ENTIER au /test → onglets 4-7 (le carnet au geste, la livraison M1 — la cap tenue par le GUI, les défauts nommés, le chrono M4) ; la DEUXIÈME livraison de la campagne — et la deuxième unité close des douze contrôlées — naîtra au geste.

- LA CONSIGNATION : la présente Entrée 285 + Task 192 ; la carte OU-TROUVER portée à 285 ; D141 tenu avant le commit (le courant 284-6a0d3de archivé versionné au miroir) ; le commit + le push GitHub au jeton ghp_ du /tokens ; le miroir Drive synchronisé (le bundle courant rafraîchi, les trois textes PATCHés en place, chaque geste recoupé par re-téléchargement). (14/11, la session de la reprise du bac — le coffre est la vérité)
"""

ITEM_12 = """
12. **LE BAC DU LABO RECONSTITUÉ — L'ÉTAT 284 RE-RECOUPÉ DU COFFRE (Entrée 285, addenda)** : le conteneur du labo recyclé entre deux sessions — le bac local revint vers 276, le coffre Drive, le miroir et GitHub demeurèrent LA vérité ; 139 pièces re-rapatriées, le kit C re-recoupé 10/10 à sa gravure, T0 re-recoupé (4d119b22… == le témoin), le plan VERROUILLÉ (a78caf8c…), GitHub vérifié à l'API (main @ 6a0d3de — le push de la 284 A VÉCU) ; L'ÉCART NOMMÉ : le récit du GUI collé au chat portait « 6 minutes » et « verdict ROUGE » — les pièces revenues disent 85 minutes et VERDICT VERT (le dossier ENTIER est la vérité, pas le récit) ; l'atelier 012347 (0 livraison) est la copie imbriquée VIDE — le livre qui compte est l'atelier 013520 rendu ENTIER au coffre ; LA SUITE au développeur : LE BRAS C au GUI (1·KIT choisir → 2·RUN lancer → 3·TÉMOIN signé de la main → preuves-unite01C/ ENTIER au /test).
"""

# ---- worklog + journal -------------------------------------------------------
with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(JOURNAL)

# ---- la carte OU-TROUVER : l'item 12 + les plages du pied --------------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
txt = carte.read_text(encoding="utf-8")
txt = txt.replace("Entrées 251-284", "Entrées 251-285")
txt = txt.replace("Tasks 158-191", "Tasks 158-192")
if not txt.endswith("\n"):
    txt += "\n"
txt += ITEM_12
carte.write_text(txt, encoding="utf-8", newline="\n")

# ---- l'atelier de la session : les scripts au dépôt -------------------------
dest = REPO / "scripts" / "campagne_d204" / "addenda-285"
dest.mkdir(parents=True, exist_ok=True)
for nom in ["60_sonde_test.py", "61_sonde_racine.py", "62_rapatrie_etat.py",
            "63_rerecoup.py", "64_verifie_push.py", "65_consigne_285.py",
            "66_sync_miroir_285.py"]:
    src = SCRIPTS / nom
    if src.exists():
        shutil.copy2(src, dest / nom)
        print(f"[atelier] {nom} versé au dépôt")

print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md + la carte OU-TROUVER — l'Entrée 285 + Task 192")
