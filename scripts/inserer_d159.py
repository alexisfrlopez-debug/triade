#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d159.py — DECISIONS.md : insère la décision D159 PAR SCRIPT à la
suite de D158 (append-only, pas de rétrodatage — le contrat D24)."""

import sys

CHEMIN = "docs/DECISIONS.md"

D159 = """
## D159 — LA REPRISE D'UN POSTE SE MÈNE AUX MIROIRS, JAMAIS À LA MÉMOIRE (quand le poste de laboratoire est restauré à un état antérieur — perte de l'arbre de travail non commité — l'état VRAI du projet vit dans les miroirs externes consignés : le dépôt GitHub porté à la pointe par la passation D141, le coffre Drive pour les kits et les pièces ; la reprise est un FETCH + un RESET à la POINTE CONSIGNÉE, jamais une reconstruction de mémoire ; les instruments gitignorés se réinstallent par leurs PROCÉDURES du dépôt, l'identité constatée par empreinte ; ce qui n'a jamais été consigné est perdu par principe)

**Le constat qui fonde la décision (05/11/2026, le geste final M7-(d), Entrée 155 — le run terrain recoupé, la finale 0.8.0 scellée).** En ouverture du geste (le message du développeur « les preuves sont dans le dossier drive /test »), le poste de laboratoire s'est révélé RESTAURÉ à un instantané antérieur : l'arbre local portait l'état M6-(c) (passation 402508f), le worklog s'arrêtait à la Task 65, le JOURNAL à l'Entrée 147, DECISIONS à D152 — TOUT le jalon M7 (quatre chantiers, Entrées 150-154, D155-D158, Tasks 68-72) était ABSENT du disque, et avec lui les scripts de sonde du run écrits après la dernière passation. La doctrine « sur pièces, jamais sur mémoire » appliquée AU POSTE LUI-MÊME : (1) l'état réel établi par `ls-remote` — GitHub pointait sur `cc56930`, EXACTEMENT la pointe consignée par la dernière passation D141 (le bundle déposé au miroir portait cette même pointe, ASSERTÉE avant dépôt) ; (2) l'arbre ré-établi par `fetch` + `reset --hard` à cette pointe — les seuls écarts locaux étaient des BITS DE MODE (644→755, artefacts de la restauration), zéro changement de contenu ; (3) l'instrument qemu-riscv64 réinstallé par SA PROCÉDURE du dépôt (`riscv/outils/installer_qemu.sh`, le paquet statique Debian 10.0.13) et recoupé par empreinte : md5 `bae5a36f…` IDENTIQUE à l'instrument EMBARQUÉ du kit — le même instrument au laboratoire et au terrain, la réserve D149 inchangée ; (4) les dépendances Python réinstallées (pynacl, keystone-engine, capstone — le bac livré nu) ; (5) les preuves du run lues AU COFFRE (le trio complet, md5 contrôlés par pièce AVANT toute interprétation) — le coffre est la source, jamais la copie locale. RIEN du jalon ne s'est perdu : la cadence « une passation par geste de jalon » (leçon D141 : aucune dette n'accumule) avait poussé chaque geste vers les miroirs AU FIL DU JALON — c'est précisément le pari de D141, tenu au moment où il fallait le tenir.

**La règle.** (1) TOUT écart entre l'état local et l'état attendu se tranche par les PIÈCES EXTERNES : `ls-remote` d'abord, le log local n'est JAMAIS une preuve d'état courant ; un instantané restauré se constate (worklog, JOURNAL, DECISIONS, `git log` recoupés ENTRE EUX) avant tout geste. (2) La reprise d'un poste restauré est un FETCH + un RESET à la POINTE CONSIGNÉE (la passation nomme la pointe du geste ; le bundle du miroir la porte ASSERTÉE) — une divergence entre la pointe consignée et la pointe distante se traite et se NOMME avant tout geste : un reset « au jugé » vers une pointe non consignée serait une rétro-écriture. (3) Les instruments gitignorés ont des PROCÉDURES dans le dépôt (l'installation est une pièce — le constat fiche § 10) : la réinstallation passe par elles et l'empreinte est CONSTATÉE après (un instrument divergent de son consigné est un refus nommé — la règle D158-(3) au labo même). (4) Ce qui n'a jamais été commité ni déposé est PERDU PAR PRINCIPE : le travail d'un geste en cours se consigne au fur et à mesure (triple consignation), jamais en fin de session seulement — les scripts de sonde du run sont morts avec l'instantané et ont été RE-ÉCRITS, aucune pièce ne dépendait d'eux.

**Alternatives rejetées.** Reconstruire le jalon de mémoire (rejeté : la mémoire n'est pas une pièce — l'exactitude mot pour mot des consignations et des empreintes ne se re-crée pas, elle se FETCH ; une reconstruction serait une rétro-écriture déguisée) ; compter sur le bac à sable comme stockage durable (rejeté : constaté au geste même — il se restaure à un instantané antérieur sans avertissement, seuls les MIROIRS consignés font foi) ; dupliquer les bundles dans /test pour « doubler » la sauvegarde (rejeté : le miroir dédié TRIADE-sauvegarde-git/ est la place des bundles, /test est le coffre des pièces — D143 ; la redondance utile est GitHub + miroir, déjà tenue) ; recopier les pièces du coffre vers le dépôt (rejeté : les pièces vivent au coffre et dans download/ non committé, md5 contrôlés à CHAQUE lecture — D99 : zéro mélange).

**Frontières.** La règle régit la REPRISE de poste et l'établissement de l'état avant un geste ; elle ne touche NI la passation D141 (la cadence demeure « une passation par geste de jalon » — la finale 0.8.0 scellée reçoit la sienne, série 080), NI les scellés (aucune carte ni artefact n'a bougé — le jalon entier a été re-constaté vert APRÈS reprise : le verrou multi-profils, le contrôle D146, la conformité 7/7 exécutés AU geste de scellage même), NI le coffre (lecture seule pour le recoup — la clôture D143 est un déplacement nommé, jamais un jet), NI la réserve instrumentale D149 (le réinstallé est l'IDENTIQUE par empreinte). L'événement est consigné à l'Entrée 155 avec ses pièces (ls-remote, le reset, les md5).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## D159" in texte:
    sys.exit("ECHEC : la décision D159 existe déjà")
i158 = texte.find("## D158")
if i158 < 0:
    sys.exit("ECHEC : D158 introuvable")

# D158 est la dernière décision : l'insert se fait à la suite (fin de fichier)
nouveau = texte.rstrip("\n") + "\n" + D159.rstrip("\n") + "\n"

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("D159 insérée à la suite de D158 (append-only)")
