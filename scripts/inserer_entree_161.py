#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_161.py — JOURNAL_TRAVAIL.md : insère l'Entrée 161 PAR
SCRIPT (ordre 160<161<marqueur, rejeu REFUSÉ fail-closed)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"

ENTREE = """## Entrée 161 — LA REPRISE SUR LES TROIS MIROIRS + LA PASSATION REJOUÉE : GitHub EN AVANCE DU BUNDLE D'UN GESTE (le Task 78 poussé, la passation jamais jouée), l'alignement à la pointe consignée 9193019, LE JETON RELAIS ROUVRE LE CANAL D'ÉCRITURE (miroir 0 erreur, kit 62/62 — le piège du manifeste amputé désamorcé par le rapatriement, bundle 080-9193019 déposé, l'ancien archivé versionné) (« on reprend ce projet : signatures déposées dans le drive /test, et j'ai mis à jour le jeton relais du drive /tokens » — la suite, côté infrastructure)

**La reprise et la découverte.** Le disque labo encore recyclé ; la méthode A rejouée depuis le bundle 080-b7b6e01 (la pointe de la passation Task 77) ; les jetons installés (le RELAIS MIS À JOUR au /Tokens par le développeur), check_auth.py VERT (Drive 200, GitHub 200 alexisfrlopez-debug). Le recoup GitHub AVANT de travailler nomme la divergence : **origin à 9193019, UN COMMIT EN AVANCE du bundle** — le Task 78 d'une session précédente (la cérémonie de l'ère M8 vérifiée-installée + le garde 12/12 + le build 0.9.0-dev.1 né + Entrée 160 + D163) avait été POUSSÉ mais la session était morte AVANT la passation : le bundle ne portait pas la pointe. Le labo avait refait le geste en parallèle (cérémonie vérifiée sur quatre contrôles, dépôt, garde, relève D144, build — l'artefact 1492b0bc… IDENTIQUE) : le doublon est constaté AVANT consignation (aucune entrée doublée), l'alignement se fait PAR RESET à la pointe consignée (D159 : ce qui est consigné revient — le parallèle n'apporte rien que le déterminisme n'ait déjà prouvé : l'artefact régénéré au geste == la pièce, les signatures du sceau == la remise). L'état vérifié après alignement : garde 12 arbres VERTS (état « reelle »), carte génération 8 vivante, artefact régénéré 44 544 o sha256 1492b0bc… (la preuve de déterminisme S'ACCUMULE : trois postes, le même sha).

**LA PASSATION REJOUÉE (le geste que la session morte devait au coffre).** (1) LE MIROIR par le relais rouvert : drive_sync.py rc=0 — 16 téléversés, 7 mis à jour, 1 122 inchangés, 0 erreur, triade-history.bundle à la pointe. (2) LE KIT D130 : le premier rejeu depuis le labo amputé a produit LE PIÈGE DOCUMENTÉ (Entrées 132/159) — un MANIFESTE de 56 entrées pour un kit réel de 62 (les 6 LISEZMOI ignorés : « absent localement — conservé tel quel côté Drive ») ; LE RAPATRIEMENT CANONIQUE d'abord (les 6 LISEZMOI téléchargés, md5 contrôlés CONTRE LES MÉTADONNÉES Drive après écriture : 6/6 MATCH), le rejeu ensuite : **62 entrées attendues, 62 présentes, 62/62 vérifiés aller-retour** — le manifeste couvre le kit réel. (3) LE BUNDLE VERSIONNÉ : triade-history-080-9193019.bundle construit (git bundle --all, branche jalon == 9193019, 16 565 966 o, md5 a8cd69f8…), déposé au miroir (relu MATCH), l'ancien 080-b7b6e01 ARCHIVÉ VERSIONNÉ dans archives-bundles/ (md5 39393eaa… recoupé avant le déplacement PATCH addParents/removeParents — 25 archives, rien supprimé), /test recoupé SANS copie de bundle. Script de dépôt : scripts/passe_bundle_m8c_execution.py (le modèle m8c, chaque geste asserté, idempotent).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), l'artefact 0.9.0-dev.1 INTACT (régénéré identique, non suivi au git — prouvé par sa carte, il sera committé à la finale comme m5), le garde VERT 12/12 (état « réelle »), le scellé 0.6.0 INTACT (l'ancre R7), AUCUN secret exposé (les .keys/ et .gdrive/ hors dépôt, le jeton jamais affiché). Livrables : le coffre à jour (miroir + kit + bundle à la pointe 9193019, GitHub == la pointe recoupé), la présente consignation ; consignations : la présente Entrée PAR SCRIPT, DECISIONS +D164 PAR SCRIPT (la reprise confronte les TROIS miroirs et s'aligne sur la pointe GitHub ; le rapatriement de download/ précède maj_kit.py — doctrine ; le jeton relais rouvert porte l'écriture, le compte de service demeure le repli), worklog +Task ID 79 ; scripts suivis : inserer_entree_161.py, inserer_d164.py, passe_bundle_m8c_execution.py (dépôt), rapatrier_lisezmoi_ceremonie.py (labo, hors dépôt).

- SUITE : LE CHANTIER M8-(d) — le kit terrain au coffre /test du Drive (l'artefact 0.9.0-dev.1 + le scénario : le run lit le VRAI ntdll de la machine du développeur, le motif confronté, la ligne comparée par les DEUX chemins [hello-02 par l'IAT vs sys-03 par NtWriteFile], la version Windows consignée au témoin) ; le run terrain VERT sur pièces pose la finale 0.9.0 ; la cristallisation R6 progresse par les passages --verifier (1/10 par bloc sys à présent).

"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "## Entrée 161" in texte:
    sys.exit("ECHEC : l'Entrée 161 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in texte:
    sys.exit("ECHEC : marqueur journal-des-builds introuvable")
i160 = texte.find("## Entrée 160")
if i160 < 0:
    sys.exit("ECHEC : l'Entrée 160 introuvable (l'ordre 160<161)")

nouveau = texte.replace(MARQUEUR, ENTREE + MARQUEUR, 1)

j160 = nouveau.find("## Entrée 160")
j161 = nouveau.find("## Entrée 161")
jm = nouveau.find(MARQUEUR)
if not (0 <= j160 < j161 < jm):
    sys.exit("ECHEC : l'ordre 160<161<marqueur n'est pas tenu "
             f"({j160}, {j161}, {jm})")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print("Entrée 161 insérée (l'ordre 160<161<marqueur constaté)")
