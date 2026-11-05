#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d163.py — DECISIONS.md : insère la décision D163 PAR SCRIPT
(append-only à la suite de D162, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D163 = """
## D163 — LA CONTINUITÉ DE CLÉ D'UNE RE-CÉRÉMONIE SE PROUVE PAR LE DÉTERMINISME Ed25519 (re-signer un arbre inchangé avec la même clé redonne EXACTEMENT la signature déposée : la comparaison bit à bit des signatures des arbres inchangés EST la preuve de la réutilisation de la clé, sans jamais accéder à la clé privée — une divergence nomme une clé neuve : l'ARRÊT) ; LA CÉRÉMONIE DE L'ÈRE M8 PASSÉE, LA DETTE D162 SOLDÉE, LE GARDE VERT 12/12, L'ARTEFACT 0.9.0-dev.1 NÉ DU BUILD IDENTIQUE À SA PIÈCE DE VÉRIFICATION (le déterminisme d'un poste à l'autre : 1492b0bc… == 1492b0bc…) ; L'ACCÈS AU COFFRE NE DÉPEND JAMAIS D'UN JETON UNIQUE MORTEL (le relais compte de service, consigné le 29/10, porte les gestes de lecture — le jeton OAuth du relais est mort DEUX fois : 29/10, 05/11)

**Le contexte qui fonde la décision (05/11, la cérémonie de l'ère reçue).** Le développeur a exécuté la cérémonie hors-ligne (LISEZMOI-ceremonie-ere-M8.txt : la re-signature des 12 arbres, la règle d'or « JAMAIS generer ») et déposé signatures-I.txt dans le coffre /test. Le labo a recueilli la remise sur pièces : rapatriement md5 contrôlé, ancre de clé tenue (173fae9c…), puis LE RECOUP PROPRE À L'ÈRE : les DIX arbres inchangés portent les MÊMES signatures que celles déposées à la cérémonie 0.6.0 du 04/11 — la preuve que la clé du 04/11 a été réutilisée est NÉE DE LA COMPARAISON, pas d'une déclaration. Le dépôt canonique a suivi (l'atomicité : tout vérifié avant écriture), le garde est passé au vert 12/12 (m0 re-signé pour le registre étendu, m8 l'arbre neuf), et le build exécuté a donné l'artefact 0.9.0-dev.1 IDENTIQUE à la pièce de vérification du Task 76 — le même sha 1492b0bc… sur un AUTRE poste, après un AUTRE recyclage du disque : le déterminisme n'est pas une espérance, il est constaté.

**Les règles.** (1) **La preuve de continuité d'une clé de cérémonie est le déterminisme Ed25519** : la signature d'un message fixe par une clé fixe est reproductible bit à bit (RFC 8032) ; une remise de re-cérémonie qui re-signerait les arbres inchangés avec LA MÊME clé rend les MÊMES signatures — le recoup les compare aux déposées : IDENTIQUES = la clé est la même (prouvé), DIVERGENTES = une clé neuve a signé (l'ARRÊT : la continuité de l'état « réelle » serait rompue, la remise est refusée). Le labo fait cette preuve SANS jamais voir la clé privée : la moitié publique déposée + le déterminisme suffisent. (2) **La remise d'une re-cérémonie couvre TOUS les arbres** (spec § 5 : une rotation couvre tout) mais SEULS les arbres mutés/nouveaux changent de signature — les empreintes des autres ne bougent pas, et leurs signatures re-déposées sont les anciennes : c'est le VECTEUR de la preuve (1). (3) **L'artefact d'un build est prouvé AVANT de naître quand le build est déterministe** : la pièce de vérification par pièces détachées (Task 76) avait annoncé 1492b0bc… AVANT la cérémonie ; le build d'après-cérémonie sur un autre poste a donné le même sha — l'égalité constatée est la preuve que NI le garde ni la cérémonie ni le poste n'influencent les octets. (4) **L'accès au coffre Drive ne dépend jamais d'un jeton unique mortel** : le jeton OAuth du relais (refresh token d'une application en mode test) est mort DEUX fois (29/10, 05/11) — chaque ré-émission sur un poste révoque la précédente ; le RELAIS COMPTE DE SERVICE (clé posée à .gdrive/, JWT RS256, mécanisme relais_service_account.py) est la voie de reprise CONSIGNÉE, étendue au sondage LECTURE SEULE du coffre entier (scripts/sonder_coffre_sa.py : racine, /Cérémonie, miroir, /test) et au rapatriement des pièces (scripts/rapatrier_ceremonie_m8.py) ; le jeton OAuth peut être re-lancé par le développeur quand il le veut — les gestes ne l'attendent plus.

**Alternatives rejetées.** Faire confiance à la remise sans le recoup de l'ère (rejeté : « sur pièces, jamais sur mémoire » — la règle d'or du LISEZMOI dit « JAMAIS generer », la preuve que le développeur l'a suivie est la comparaison, pas la confiance) ; déposer la remise sans le recoup préalable (rejeté : le dépôt vérifie cryptographiquement, mais le recoup NOMME l'écart d'ère AVANT toute écriture — un dépôt refusé par sceau_I.py n'aurait pas dit SI la clé était la bonne) ; attendre le retour du jeton OAuth pour rapatrier (rejeté : le relais compte de service existe PRÉCISÉMENT pour ça, constaté le 29/10 — le geste ne se bloque pas sur un jeton mortel) ; re-signer au labo pour « débloquer » le build (rejeté : D87/D162 — le labo ne signe jamais, la clé de test déclasserait l'état « réelle »).

**Frontières.** La présente décision est la clôture de la dette D162 : la cérémonie de l'ère est PASSÉE (12/12 verts, état « reelle » intact), l'artefact 0.9.0-dev.1 est NÉ (44 544 o, sha256 1492b0bc0792e1ab…, la carte génération 8 vivante, le témoin e9cd8c549485… ne bouge pas) — c'est un GESTE DE BUILD, JAMAIS un scellage : la finale 0.9.0 attend le run terrain vert du chantier (d), aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; le scellé 0.6.0 INTACT (l'ancre R7 : 44 blocs octet-identiques au nouveau-né) ; le SSN du terrain demeure INCONNU du labo. Les pièces de l'arrêt : download/ceremonie-ere-m8/signatures-I.txt (la remise rapatriée, md5 ab22512a6864…), v06/sceau-I/signatures/ (12/12, m0 re-signé + m8 neuf), v06/sceau-I/cle-publique-I.txt (173fae9c… l'ancre tenue), m8/proxy.exe (1492b0bc…), m8/carte/ (la génération 8), scripts/sonder_coffre_sa.py, scripts/rapatrier_ceremonie_m8.py (le recoup de l'ère).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## D163" in texte:
    sys.exit("ECHEC : la décision D163 existe déjà")
i162 = texte.find("## D162")
if i162 < 0:
    sys.exit("ECHEC : D162 introuvable")

# D162 est la dernière décision : l'insert se fait à la suite (fin de fichier)
nouveau = texte.rstrip("\n") + "\n" + D163.rstrip("\n") + "\n"

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D163 insérée à la suite de D162 (append-only constaté)")
