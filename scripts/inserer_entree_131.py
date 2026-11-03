#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_131.py — JOURNAL_TRAVAIL.md : insère l'Entrée 131 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
130 < 131 < marqueur recoupé — le même contrat que les entrées 127-130)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 131 — SYNCHRO DRIVE+GIT DEMANDÉE PAR LE DÉVELOPPEUR (03/11) : tout était à jour SAUF le geste 3 de la passation D141 — la copie /test du bundle 060 n'avait JAMAIS été retirée (le PATCH « 200-sans-effet », 5e instance du piège) ; CAUSE RACINE TRANCHÉE PAR PREUVE API : l'en-tête Content-Type manquant (Drive IGNORE un corps non déclaré — la leçon du commit 4faaf10 était trop large) ; le retrait ENFIN EFFECTIF, /test conforme D143 (8 entrées)

**La demande (consignée fidèlement) et l'état constaté.** « fais moi une synchro drive et git, je ne sais pas s'ils sont à jour » — vérification PAR PIÈCE avant tout geste : git local propre (branche bundle051/v0.5.1-jalon-v7, HEAD 4faaf10, un seul non-suivi bundles-060/ — zone de travail locale, jamais committée) ; hook post-commit rc=0 sur les DEUX derniers commits (07d392e à 17:36:16Z, 4faaf10 à 17:41:37Z — .gdrive/last_sync.log) ; drive_sync.py REJOUÉ : 0 téléversé, 0 mis à jour, 815 inchangés, 0 erreur ; bundle complet régénéré au miroir ; kit Cérémonie (D130) OK, v06 18 entrées ; la canonique triade-history-060-07d392e.bundle au miroir md5 2bb725ef… == copie locale (recoupé) ; archives-bundles/ : 5 bundles (050-f62711b, 051-b210da4, 051-200686e4, 051-721ace3, 051-3375e9b) ; racine Drive : REPRISE_PROJET.md et PROTOCOLE_TRIADE_AGENT.md à jour. UN SEUL ÉCART : /test portait 9 entrées au lieu des 8 de D143 — la copie du bundle 060 y figurait encore.

**L'enquête (deux fichiers, une chronologie).** La copie /test (id 1beZpC6Iik9dX9-b_-ZgltKVv-wkAZYbL, créée 2026-11-03T17:38:08Z) et la canonique miroir (id 1SRM35nG5p0UJYUcP3EbCNjF10AcbQJpd, créée 17:40:19Z) sont DEUX fichiers Drive distincts, md5 identiques (2bb725ef…) : la copie /test est bien le dépôt erroné d'AVANT la passation (le flux : commit 07d392e 17:36 → dépôt /test 17:38 → dépôt miroir 17:40 → commit 4faaf10 17:41), pas un geste postérieur du développeur. Le rejeu de passe_bundle_060.py a REFUSÉ sur son assertion d'état 0 (« l'ancien courant triade-history-051-3375e9b.bundle introuvable au miroir ») — preuve que les gestes 1 (dépôt miroir) et 2 (archivage versionné) étaient EFFECTIFS et que seul le geste 3 manquait ; le script n'étant pas idempotent sur son état initial, un script dédié (scripts/retirer_bundle_test_060.py, geste 3 SEUL, protections identiques : md5 recoupé AVANT retrait, canonique vérifiée, corbeille et jamais suppression, état recoupé PAR L'API après) a été écrit pour le rejeu.

**La cause racine (5e instance du piège PATCH, tranchée par preuve API).** La fonction api() de passe_bundle_060.py n'envoie PAS l'en-tête Content-Type — Drive IGNORE le corps d'un PATCH non déclaré et répond 200 SANS effet. Chronologie des graphies : (1) corps {"trashed": true} sans Content-Type → 200, aucun effet (l'exécution d'origine du 03/11) ; (2) la leçon consignée au commit 4faaf10 (« trashed est un paramètre de REQUÊTE, jamais du corps ») → graphie ?trashed=true → 200, aucun effet (paramètre inconnu ignoré — le code « corrigé » du geste 3 ne pouvait pas marcher non plus, il n'a simplement jamais été re-vérifié après correction : la recette du geste 3 ne recoupait PAS l'état trashed après le PATCH) ; (3) diagnostic capabilities : canTrash=True sur les trois fichiers sondés (le droit n'a JAMAIS été en cause) ; (4) la graphie qui FONCTIONNE : PATCH corps {"trashed": true} AVEC Content-Type: application/json → trashed=True constaté par relecture API. RÈGLE CORRIGÉE : trashed = champ du CORPS DÉCLARÉ par Content-Type ; addParents/removeParents = paramètres de REQUÊTE (le geste 2 a toujours marché ainsi) ; jamais combinés (403 du run v7, entrée 128). La leçon du 4faaf10 était trop large : le corps n'est pas interdit, il doit être DÉCLARÉ. LEÇON GÉNÉRALE (D12 étendu) : un HTTP 200 de Drive ne prouve RIEN — toute mutation doit être recoupée par une RELECTURE de l'état visé dans le même geste.

**Le geste réparé et recoupé.** Copie /test 1beZpC6I… mise à la corbeille (trashed=true PAR L'API) ; /test recoupe EXACTEMENT les 8 entrées de D143 : LISEZMOI-m5b-v8.txt, m5b-kit-v8.zip, scenario-m5b-v8.ps1, corriger-wsb.bat/.ps1, preuves-m5b, archives-preuves, archives-livraisons ; la canonique miroir intacte (md5 2bb725ef…) ; la corbeille n'est pas vidée (geste du développeur). Re-vérification complète : 13/13 OK, 0 écart.

**Frontières.** Aucune suppression définitive (corbeille seulement) ; aucune pièce d'archive ni bundle touché (les 5 archives et la canonique intacts, md5 recoupés) ; arbres scellés intouchés ; aucun artefact touché ; aucune clé traversée ; le dépôt git ne reçoit que le script du geste et la présente consignation.

**Vérifiabilité.** `python3 scripts/retirer_bundle_test_060.py` (idempotent : rejeu = « geste DÉJÀ effectif, rien à faire ») ; `.gdrive/last_sync.log` (les deux rc=0 du 03/11) ; listing API de /test (8 entrées) ; capabilities des trois fichiers (canTrash=True) ; diagnostic des createdTime (17:38:08Z vs 17:40:19Z).

**SUITE.** Inchangée : la cérémonie de signature par le développeur (D87 : clé hors-ligne, carte génération 7, conformité_profil à écrire), puis le kit VM ÉTAPE 2 (le navigateur du bac à sable) et le run M5-b étape 2 — le critère (b) de D136. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-130) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 131" in texte:
    sys.exit("ECHEC : l'Entrée 131 existe déjà")
i130 = texte.find("## Entrée 130")
im = texte.find(MARQUEUR)
if not (0 <= i130 < im):
    sys.exit("ECHEC : ordre inattendu (130/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 130 < 131 < marqueur
j130 = nouveau.find("## Entrée 130")
j131 = nouveau.find("## Entrée 131")
jm = nouveau.find(MARQUEUR)
if not (0 <= j130 < j131 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 131 insérée ({len(ENTREE)} caractères) — ordre 130<131<marqueur recoupé")
