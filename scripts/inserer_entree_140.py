#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_140.py — JOURNAL_TRAVAIL.md : insère l'Entrée 140 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
139 < 140 < marqueur recoupé — le même contrat que les entrées 127-139)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 140 — LA PASSATION D141 REJOUÉE à la livraison e3 : le bundle courant triade-history-060-193b8d4 (la pointe de la vague e3) déposé au miroir, l'ancien 060-07d392e ARCHIVÉ VERSIONNÉ — la dette des six commits sans passation NOMMÉE et fermée ; GitHub porté à 193b8d4 (recoupé ls-remote)

**Le geste et la dette.** La vague e3 livrée (Entrée 139, commit 193b8d4), la passation D141 du bundle versionné est REJOUÉE : elle n'avait plus été exécutée depuis 07d392e — SIX commits de jalon (cérémonie 0.6.0 prête puis consommée, réparation 0.5.1, scellage carte génération 7, kit e2, verdict run e2) vivaient sans bundle versionné courant, à travers DEUX recyclages de labo ; l'ère 051 tenait la cadence d'une passation par livraison de jalon — elle est reprise. LA DETTE EST NOMMÉE, pas dissimulée : le miroir portait le courant 060-07d392e pendant que le hook post-commit maintenait seulement l'historique triade-history.bundle (sans nom versionné — D141 : « le numéro de version AU NOM du bundle »).

**L'exécution (scripts/passe_bundle_e3.py, modèle passe_bundle_060.py — chaque mutation RECOUPÉE PAR RELECTURE, idempotent par saut d'already-fait).** (0) le bundle construit localement (git bundle create --all, 15 128 008 o, md5 0eef6b2b…) et ASSERTÉ AVANT dépôt : la branche jalon du bundle pointe sur 193b8d4 (git bundle list-heads) — le bundle porte LA livraison e3 AVEC sa consignation ; (1) dépôt au miroir TRIADE-sauvegarde-git/ : md5 distant == local par relecture ; (2) l'ancien courant triade-history-060-07d392e.bundle (md5 2bb725ef… recoupé AVANT) ARCHIVÉ VERSIONNÉ dans archives-bundles/ par addParents/removeParents EN PARAMÈTRES DE REQUÊTE (leçon v7/Entrée 131) — JAMAIS supprimé ni écrasé ; (3) /test ne porte AUCUNE copie de bundle (recoupé, rien à retirer) ; (4) l'état final recoupé : la racine du miroir porte LE courant UNIQUE triade-history-060-193b8d4.bundle, archives-bundles/ en porte SIX (050-f62711b, 051-b210da4/200686e4/721ace3/3375e9b, 060-07d392e). Le canal GitHub porté à 193b8d4 dans le même geste (git push origin HEAD, recoupé par ls-remote — les trois canaux durables alignés : miroir de fichiers, bundle versionné, GitHub).

**Frontières.** Aucune suppression (l'archivage est un DÉPLACEMENT, la corbeille n'est pas touchée) ; le bundle --all embarque l'histoire complète (aucune clé — .keys/ est gitignoré et absent du dépôt) ; /test INTACT (8 entrées D143, la vague e3 courante) ; le hook post-commit n'est pas modifié (drive_sync + maj_kit rc=0 sur 193b8d4, .gdrive/last_sync.log) ; aucun artefact scellé touché ; le scellé 0.6.0-rc.1 (4b8f6af6…) et la carte génération 7 INTACTS.

**Vérifiabilité.** python3 scripts/passe_bundle_e3.py (rejeu = « déjà présent (md5 MATCH) — idempotent ») ; le listing API du miroir (courant unique + 6 archives) ; .gdrive/last_sync.log (miroir rc=0, kit rc=0, commit 193b8d4) ; git ls-remote origin (193b8d4).

**SUITE.** Inchangée — LE GESTE TERRAIN : m5b-kit-e3.zip depuis /test, dossier NEUF, corriger-wsb.bat, double-clic scenario-m5b.wsb, renvoyer TOUT preuves-m5b ; le critère (b) de D136 PAR LE NAVIGATEUR ; si vert : python3 m5/build_m5.py --sceller-final pose la finale 0.6.0. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-139) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 140" in texte:
    sys.exit("ECHEC : l'Entrée 140 existe déjà")
i139 = texte.find("## Entrée 139")
im = texte.find(MARQUEUR)
if not (0 <= i139 < im):
    sys.exit("ECHEC : ordre inattendu (139/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 139 < 140 < marqueur
j139 = nouveau.find("## Entrée 139")
j140 = nouveau.find("## Entrée 140")
jm = nouveau.find(MARQUEUR)
if not (0 <= j139 < j140 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 140 insérée ({len(ENTREE)} caractères) — ordre 139<140<marqueur recoupé")
