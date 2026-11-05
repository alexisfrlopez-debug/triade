#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d162.py — DECISIONS.md : insère la décision D162 PAR SCRIPT
(append-only à la suite de D161, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D162 = """
## D162 — LA CÉRÉMONIE DU SCEAU I DE L'ÈRE M8 EST EXIGÉE AVANT TOUT BUILD (le garde-sceau D87 NOMME la dette : le registre figé m0 fut étendu au M8-(a) SANS re-signature — un diff d'intention non signé ; la clé hors-ligne du développeur est requise, le labo ne signe JAMAIS à sa place) ; LA TABLE DU SCEAU ÉTENDUE À L'ARBRE m8 (le domaine sys — sceau_I.py n'est pas signé lui-même : aucune cascade) ; LES OFFSETS FICHIER DE L'ÈRE ARRÊTÉS (.text5 raw 0x8E00, taille 0xAE00 — les sept en-têtes tiennent dans la marge 0x400, le décalage de packaging D94 n'est pas rejoué) ; LE BUILD 0.9.0-dev.1 ÉCRIT, SES COMPOSANTS VÉRIFIÉS SUR PIÈCES DÉTACHÉES, AUCUN ARTEFACT AVANT LA CÉRÉMONIE

**Le contexte qui fonde la décision (05/11, chantier M8-(c)).** Le chantier (b) avait livré les trois notations prouvées (Entrée 157, D161). Le chantier (c) — le build — commence par LE GARDE (le modèle build_m5 : « les chaînes de build appellent garde() et refusent un arbre divergé », D87). Au premier appel, le garde REFUSE : l'arbre m0 a divergé (fichier modifié : README.md — code 10, « diff d'intention non signé »). La mesure sur pièces : le M8-(a) (D160 règle 6 : « le registre figé s'étend — le domaine sys est créé, réservé M8 ») a muté m0/I/README.md sans cérémonie de re-signature ; les spécifications hello-01/02/03 sont INTACTES (seul le registre diverge du manifeste signé à la cérémonie 0.6.0 du 04/11) ; l'arbre m8 — la couche I du domaine, avec ses errata D161 — n'a jamais été signé (l'arbre m5 lui-même ne le fut qu'à la cérémonie de SON scellage). La dette est née au M8-(a), elle est échue au premier geste du build : le sceau fait exactement son travail.

**La règle.** (1) **La cérémonie de l'ère M8 est le préalable de tout build** : la remise du développeur (SA clé Ed25519 hors-ligne, D87 — le même geste que la remise de 11 lignes du 04/11) porte AU MINIMUM **m0** (le registre figé étendu — les specs hello intactes, seul le README à re-signer) et **m8** (le domaine sys). La charge est PRÉPARÉE (`sceau_I.py preparer` → v06/sceau-I/a-signer.txt, 12 arbres, les empreintes vivantes) ; le dépôt suit la remise (`sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt` — l'atomicité de cérémonie : clé, signatures et manifestes basculent ensemble ou pas du tout). (2) **Le labo ne signe jamais à la place du développeur** : la clé de TEST (lab, D105) DÉCLASSERAIT l'état « réelle » du dépôt — une régression de preuve, refusée ; aucune clé inventée ; le refus nommé du garde est la seule réponse honnête tant que la remise n'est pas déposée. (3) **La table du sceau s'étend à l'arbre m8** (`m8 : proxy.exe (domaine sys, syscalls directs), sys.1`) : sceau_I.py n'est PAS couvert par l'arbre v06 (CF2/CF3/README seulement) — l'extension de la table ne diverge AUCUN arbre signé, aucune cascade. (4) **Les offsets fichier de l'ère sont arrêtés** (m8/layout.py, la source unique — modèle D94) : .text5 raw **0x8E00** (la 7e section vit après .text4, les SIX premières raw inchangées), taille de fichier **0xAE00** ; les SEPT en-têtes (608 o) TIENNENT dans la marge SizeOfHeaders 0x400 — le décalage de packaging D94 n'est PAS rejoué, aucun octet hérité ne bouge. (5) **Le build est écrit et vérifié par pièces détachées, aucun artefact avant la cérémonie** : le garde ARMÉ en tête de construire/verifier (le refus CONSTATÉ au geste, avec la notice de cérémonie) ; l'héritage re-vérifié de bout en bout (M3 524 + M4 492 + M5 312 verrous, l'image M5 composée == le scellé 0.6.0 OCTET PAR OCTET, sha c1e46fb0… — la carte génération 7 scellée prouve ces octets) ; l'oracle structurel M8 (54 verrous — LA RÈGLE AUCUN IAT PAR BLOC sys, le site syscall unique, le motif AVANT l'imm32, l'ordre résoudre-puis-émettre) ; la composition (.text5 + les fixtures dans la zone vierge + la version 0x00090001 : geste de BUILD jamais scellage) ; la validation PE (7 sections, imports inchangés, portes R10+M5) ; la preuve R7 (41 blocs hérités octet-identiques, les trouées du domaine vierges des deux côtés) ; **l'exe composé 44 544 o, sha256 1492b0bc0792e1ab…, re-constaté identique (le déterminisme)** ; les TROIS oracles appelés depuis le build (M4/M5 héritage + le harnais M8 : 61 contrôles sur les blobs du build) ; la carte génération 8 prête (m8/carte_m8.py — les primitives testées à blanc dans un répertoire temporaire : JAMAIS de carte avant son build ; la clé publique e9cd8c549485… : LE TÉMOIN NE BOUGE PAS, la graine durable D144). AUCUN fichier m8/proxy.exe, AUCUNE carte déposée : l'artefact naîtra de construire() quand le garde passera.

**Alternatives rejetées.** Contourner le garde (rejeté : le fail-closed est la doctrine — un garde contournable ne serait pas un garde ; le refus nommé EST le résultat du chantier) ; signer avec la clé de test du lab (rejeté : déclasser l'état « réelle » du dépôt serait une régression de preuve — la clé de test est « la preuve visible de l'état laboratoire », l'état PRÉSENT est réel depuis la cérémonie 0.6.0) ; retirer m0 de la liste gardée (rejeté : m0 EST l'héritage — hello-02 est dans le build ; sauter l'arbre fautif serait la contrebande exacte que D87 existe pour attraper) ; bâti l'artefact sans le garde « pour tester » (rejeté : un proxy.exe né hors garde serait un artefact illégitime ; les composants se testent par pièces détachées, l'assemblage complet attend la cérémonie) ; re-signer TOUT (rejeté : seuls les arbres mutés/nouveaux exigent la remise — m1-m7, demo, terrain, v06 sont intacts, leurs signatures en place restent valides ; la remise minimale est de 2 lignes).

**Frontières.** La présente décision N'EST NI un build NI un scellage : AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 — INTACTES ; la 0.9.0-dev.1 viendra du build après la cérémonie, geste de BUILD ; la 0.9.0 attend le terrain vert du chantier (d)) ; le scellé 0.6.0 (c1e46fb0…) est l'ANCRE R7 de l'ère — il ne bouge pas ; l'état de clé du sceau demeure « réelle » ; l'exe composé 1492b0bc… est une PIÈCE DE VÉRIFICATION (le déterminisme constaté), pas un artefact livré — l'artefact naîtra du build complet ; la carte génération 8 n'existe pas encore (ses primitives sont prêtes, le témoin ne bouge pas). Les pièces de l'arrêt : m8/build_m8.py, m8/carte_m8.py, m8/harnais_sys.py (executer), m8/layout.py (offsets arrêtés), v06/sceau_I.py (table étendue), v06/sceau-I/a-signer.txt (la charge du développeur), les empreintes constatées (héritage c1e46fb0…, composé 1492b0bc…, oracle M8 54 verrous, harnais 61/61).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## D162" in texte:
    sys.exit("ECHEC : la décision D162 existe déjà")
i161 = texte.find("## D161")
if i161 < 0:
    sys.exit("ECHEC : D161 introuvable")

# D161 est la dernière décision : l'insert se fait à la suite (fin de fichier)
nouveau = texte.rstrip("\n") + "\n" + D162.rstrip("\n") + "\n"

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D162 insérée à la suite de D161 (append-only)")
