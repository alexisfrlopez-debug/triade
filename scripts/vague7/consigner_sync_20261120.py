#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_sync_20261120.py — LA CONSIGNATION de la session de synchronisation
(append-only partout) : l'Entrée 372 au worklog, la carte OU-TROUVER portée."""
import pathlib
import re

REPO = pathlib.Path("/home/z/my-project/depot")

# ---- 1. l'Entrée 372 au worklog (append) ------------------------------------
wl = REPO / "worklog.md"
wl.write_text(wl.read_text(encoding="utf-8") + """
---
Task ID: 232
Agent: Z.ai (agent principal — la session de synchronisation : les jetons renouvelés, git vérifié, le Zenodo v0.19.4 publié, la livraison Drive préparée)
Task: LA SYNCHRONISATION DES TROIS BORDS À LA COMMANDE DU MAÎTRE (« mets a jour git drive et zenodo puis go pour la suite ») : le git VÉRIFIÉ (rien à pousser — la tête distante == 5be0320), LE ZENODO PORTÉ À LA v0.19.4 (la nouvelle version publiée, recoupée aux trois bords byte-byte), la livraison Drive PRÉPARÉE et nommée BLOQUÉE (le relais OAuth mort le 19/11 20:04, le compte de service lecteur seul — le 403 des Entrées 274/294).

Work Log:
- L'AMORÇAGE : les CINQ jetons du dossier public /Tokens (le lien du maître — la solution au problème œuf-poule : le dossier HORS coffre, lisible sans justificatif — le dossier porte le nom « Tokens », le parent hors coffre) téléchargés au bac : le jeton git VALIDE (le dépôt lu : public, droits de pousse), le jeton Zenodo VALIDE (le dépôt listé), le compte de service LECTEUR SEUL, le relais OAuth MORT (invalid_grant — sauvegardé le 12/11 20:04, mort le 19/11 20:04 : les 7 jours du mode testing Google ; la session cq01qv1za s'était close à 20:01, TROIS MINUTES avant la mort du jeton).
- LE GIT VÉRIFIÉ : la tête distante == la tête locale 5be0320 (l'Entrée 371 — la session précédente avait poussé) : ls-remote anonyme main = 5be0320, RIEN À POUSSER ; les QUATRE fichiers binaires reconstruits non consignés (les DLL/kit de campagne — les commodités de session de vljfs6pcj/cq01qv1za) RESTAURÉS À LA TÊTE : l'arbre de travail == le commit consigné, le miroir ne portera QUE le consigné.
- LE ZENODO v0.19.4 PUBLIÉ (la matrice D220 ligne 4 poursuivie — public + Zenodo, la même porte, la commande explicite du maître) : la nouvelle version du record 24367344 — LE DOI DE VERSION 10.5281/zenodo.24379173 (minté au geste, jamais inventé), LE CONCEPT DOI 10.5281/zenodo.24367343 résolvant désormais sur v0.19.4, la page https://zenodo.org/record/24379173 anonyme 200 « Academic Edition v0.19.4 » ; LES TROIS FICHIERS : TRIADE_soumission_v0.19.4.zip [258 393 o, sha256 8a3bed7a69b47905…] — README + manuscrit v0.19.4 + empreintes (les scellés loupe.exe/proxy.exe portés) + LE RAPPORT DE VÉRIFICATION V1-V10 + LES TABLEAUX GÉNÉRÉS des registres bruts (LA CAMPAGNE OPT-04 lue du journal_tokens.jsonl : les 36 appels et les distributions natives ; LA PILE M4 des 17 preuves JSON : les runs et les distributions par configuration — CHAQUE valeur CONFRONTÉE aux consignés du RAPPORT-cq01qv1za : les médianes/quartiles/min/max EXACTS, la méthode d'affichage de l'instrument extraire_pointeur.py reprise TELLE QUELLE, un écart eût été un REFUS) ; TRIADE_complet_v0.19.4.zip [622 013 o, sha256 21fa40a2b6adf1e4…, 113 entrées] — les chaînes v180/v190 PORTÉES du zip v0.19.0 (les preuves scellées, les scripts, les TLA+) + le manuscrit v0.19.4 (PDF + tex + données) + LES PREUVES v193 NÉES (l'écart CF3 fermé : les quatre rapports 5ey7gmjra + le rapport de vérification v0.19.3 — jamais déposés avant) + LES PREUVES v194 NÉES (les DEUX RAPPORTs cq01qv1za, le contrôle négatif 5/5, le PLAN gelé sha256 cb5d1943…, le journal des tokens, le mémo des sessions, les 17 preuves JSON, les empreintes du pack) + LES SCRIPTS v194 (les instruments) + LES MODULES TLA+ ÉTENDUS ; TRIADE_presentation_v0.19.4_20261120.zip [2 161 824 o, sha256 7a333777db88b8bf…] le pack des cinq documents ; LES MÉTADONNÉES : le titre v0.19.4, le champ version posé « v0.19.4 », la description anglaise à jour (le pointeur seul, la pile, H5 tenue, l'extension CF3, la cérémonie D183 vécue, le dépôt public D220), la licence busl-1.1 inchangée (le grant académique D209) ; LE RECOUP : les trois fichiers RE-TÉLÉCHARGÉS du record publié — md5 == local == Zenodo, 3/3 VERT byte-byte ; le concept DOI résolu sur la v0.19.4 ; l'état « done ».
- LES VÉRIFICATIONS RE-JOUÉES à l'assemblage : LE LINTER v194 16/16 VERT (« le build est admis ») ; LES EMPREINTES du pack recoupées 5/5 (manuscrit 6e3cf13d…, spécification ec40d219…, Livre 6dadf72d…, preuves f59ba532…, présentation 221da9b7…) ; LE PLAN gelé recoupé sha256 cb5d194340af… ; LA RÉCONCILIATION D210 re-roulée VERT (aucun défaut pour l'attribution, le carnet 5 lignes run-terrain, chaque ROUGE porte son échappée) ; LES SCELLÉS des 17 preuves M4 relus INTACTS (le champ scelles_intacts à chaque run).
- L'ÉCART NOMMÉ (D189 — même défavorable) : LA LIVRAISON AU COFFRE DRIVE BLOQUÉE — le relais OAuth EXPIRÉ (invalid_grant, le fichier au /Tokens est la sauvegarde du 12/11 : le jeton mort), le compte de service LECTEUR SEUL (le PUT 403 « The user does not have sufficient permissions for this file », la création 403 « Insufficient permissions for the specified parent » — la répétition EXACTE du 403 nommé aux Entrées 274/294 : le relais OAuth est LA voie d'écriture, le compte de service la voie de lecture — et la leçon de la Task 202 : le 200 muet du SA n'est jamais une preuve) ; TOUT EST PRÉPARÉ : scripts/livrer_session_cq01qv1za.py — UNE commande (le miroir drive_sync.py + le kit maj_kit.py au commit 5be0320 + les CINQ pièces au /test [les DEUX RAPPORTs, le contrôle négatif, le rapport de vérification v0.19.4, le rapport Zenodo] + le pack v0.19.4 à la RACINE + l'instruction cq01qv1za archivée /instructions → /ARCHIVE/instructions_20261119/) ; L'OUVERTURE attend l'un des DEUX gestes du maître : la ré-autorisation interactive du relais OAuth (le refresh_token neuf déposé au /Tokens) OU le rôle « Éditeur » accordé au compte de service sur le dossier « Triade » du coffre.
- LA SUITE : l'instruction 1c4sokpii (la dernière de la vague 7 — le plan D210 au terme, l'indépendance inter-familles, le tri des 56 survivants de mutation, le paquet d'évaluation d'artefacts, les matériaux de réplication) DÉBUTÉE à la suite du présent geste.
  (20/11/2026, la session de synchronisation — les trois bords : le git déjà en place, le Zenodo porté et recoupé, le coffre nommé bloqué et préparé : l'écart consigné, jamais subi en silence)
""", encoding="utf-8")
print("[Entrée 372] le worklog porté")

# ---- 2. la carte OU-TROUVER (l'en-tête porté à l'Entrée 372) ----------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
t = carte.read_text(encoding="utf-8")
t = re.sub(r"\*Mise à jour : [^*]+\*", "*Mise à jour : 20/11/2026 (Entrée 372 — LA "
           "SYNCHRONISATION DES TROIS BORDS à la commande du maître « mets a jour "
           "git drive et zenodo puis go pour la suite » : LE GIT VÉRIFIÉ [rien à "
           "pousser — la tête distante == 5be0320, l'Entrée 371 poussée par la "
           "session précédente], LE ZENODO v0.19.4 PUBLIÉ [le DOI de version "
           "10.5281/zenodo.24379173 minté au geste, le concept DOI "
           "10.5281/zenodo.24367343 résolvant sur la v0.19.4 ; les TROIS fichiers "
           "— soumission/complet/pack — recoupés byte-byte 3/3, les tableaux "
           "GÉNÉRÉS des registres bruts et CONFRONTÉS aux consignés, les preuves "
           "v193/v194 nées au complet, le linter v194 re-roulé 16/16], LA "
           "LIVRAISON DRIVE PRÉPARÉE ET NOMMÉE BLOQUÉE [le relais OAuth mort le "
           "19/11 20:04 — invalid_grant, le fichier au /Tokens est la sauvegarde "
           "du 12/11 ; le compte de service lecteur seul, le 403 des Entrées "
           "274/294 ; UNE commande l'ouvre : scripts/livrer_session_cq01qv1za.py "
           "— l'ouverture attend la ré-autorisation du relais OU le rôle Éditeur "
           "au compte de service] ; l'instruction 1c4sokpii DÉBUTÉE)*", t, count=1)
carte.write_text(t, encoding="utf-8")
print("[carte] l'en-tête porté à l'Entrée 372")
