#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_139.py — JOURNAL_TRAVAIL.md : insère l'Entrée 139 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
138 < 139 < marqueur recoupé — le même contrat que les entrées 127-138)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 139 — LA VAGUE e3 CONSTRUITE ET LIVRÉE (« go pour reconstruire le kit e3 ») : la correction D145 appliquée au scénario — la garde d'armement FONCTIONNELLE (la SONDE forme-absolue reçoit la page 200 de l'autorité), RELEVER-ARME en verdict POST-MORTEM, Edge par VersionInfo ; le scellé 0.6.0-rc.1 N'A PAS BOUGÉ D'UN OCTET (l'assembleur l'asserte) ; kit e3 au coffre /test, vague e2 archivée

**La demande et le préalable.** « go pour reconstruire le kit e3 » — l'aval nommé par l'Entrée 138. AVANT tout geste, l'état du labo : le dépôt local était PÉRIMÉ à a5035e1 (recyclage survenu APRÈS la Task 56 — les commits 4580164…142fc44 vivaient déjà chez origin) : fast-forward recoupé par ls-remote (142fc44, la pointe GitHub), le bruit de bits de mode neutralisé par reset --hard (précédent Task 39 — 0 insertion/0 suppression, rien à perdre), git propre ensuite. Les pièces du run e2 rapatriées À NEUF du coffre (scripts/rapatrier_preuves_e3.py — les 7 entrées de archives-preuves/preuves-run-e2, 7/7 CONFORMES par md5, miroir local download/preuves-run-e2/) : le verdict relu AVANT d'écrire la correction, la correction suit les pièces, pas la mémoire.

**Le scénario e3 (m5/vm/scenario-m5b-e3.ps1 — construire_scenario_e3.py, ONZE remplacements ancrés ASSERTÉS R1–R11, modèle construire_v8_scenario.py).** Tout ce qui n'est pas nommé est repris OCTET POUR OCTET de l'e2 (le décor e2/v8 est verrouillé par les runs) ; BOM+CRLF préservés (852 lignes, 49 669 o). LES TROIS CORRECTIONS de l'Entrée 138 : (1) LA GARDE D'ARMEMENT DEVIENT FONCTIONNELLE — la fonction Sonde-Armement remplace Attendre-Ligne (la coupable du run e2, supprimée) : le scénario se connecte au mandataire 127.0.0.1:25000, écrit la requête forme-absolue claire du navigateur (« GET http://127.0.0.1/ HTTP/1.1 » + Host), recopie la réponse en pièce page-sonde-armement.txt (posée dans TOUS les cas, octets partiels compris — ReceiveTimeout 25 s, la lecture ne juge que des octets reçus, jamais d'une vue de fichier) ; la garde exige LA PAGE 200 DE L'AUTORITÉ A (le statut « HTTP/1.1 200 » + le marqueur TRIADE-M5B-PAGE-200, relu) : relèvement http→https + tunnel + réponse = preuve OPÉRATIVE (un 0.5.1, ou un rc.1 non armé, routerait vers l'origine port 80, muette : 502) ; REFUS PROXY-PAS-ARME nommé sinon, l'extrait de réponse (borné à 160 caractères lisibles) distingue le 502 du silence ; (2) LA LIGNE « relever-https arme » DEVIENT UN VERDICT POST-MORTEM (Verdict-Vue APRÈS le quit — modèle v8, PLUS AUCUNE lecture en live d'un fichier vivant) ; (3) DIAG-EDGE-VERSION par (Get-Item msedge.exe).VersionInfo (le --version du run e2 était muet), la pièce edge-version.txt posée AUX PREUVES dans les deux cas. L'HONNÊTETÉ DES ÉTIQUETTES (leçon Entrée 134) : les détails des verdicts AUTORITE-A-SERVIE, TUNNEL-A et FLUX-A-V0 NOMMENT la sonde — elle est elle-même servie, elle établit aussi un tunnel et produit aussi une ligne v=0 ; le décisif navigateur reste le DOM (dom-a.txt), la sonde ne l'approche pas. La liste A ENVOYER du témoin gagne les deux pièces nouvelles.

**La réponse attendue de la sonde est PROUVÉE AVANT le run** : le chemin forme-absolue http:// sous politique armée est validé par l'oracle D136 F1 (200 cas, ligne de flux et octets au client vérifiés OCTET PAR OCTET contre le modèle) ; la réponse exacte « HTTP/1.1 200 OK » + page de l'autorité est la pièce page-a.txt du run v8 (le même tunnel, client CLI) ; le marqueur ne vit nulle part ailleurs que dans la page de l'autorité (autorite_test.py, MARQUEUR_PAGE). Le refus attendu d'un non-armé est prouvé par l'oracle F2 (politique 0 : l'origine port 80, muette, 502).

**L'assemblage (scripts/assembler_kit_e3.py, modèle assembler_kit_e2.py).** La base est le kit e2 LIVRÉ (download/vague-v8/m5b-kit-e2.zip, md5 76e7b02f… recoupé AVANT le geste — le coffre fait foi) : 55 entrées, LE PROXY N'EST PAS REMPLACÉ — l'égalité base == dépôt ASSERTÉE octet pour octet (4b8f6af6…, 36 352 o : la correction touche le scénario, JAMAIS le scellé) ; le scénario de la base asserté e2 (Attendre-Ligne + PROXY-SANS-ARMEMENT présents — le remplacement est un FAIT nommé, pas une hypothèse) ; TROIS pièces remplacées (scénario e3, LISEZMOI-KIT-M5B.md e3, LISEZMOI-preuves.txt e3) et 52 reprises assertées par empreinte (fixtures v5 racine 86525998…, autorite_test.py, wsb réseau coupé, python embarqué, client vestige). m5b-kit-e3.zip : 11 192 711 o, md5 981b1a5b14e75a77207df32ca7c8d4c9 — intégrité re-vérifiée à la sortie (lecture différée) PUIS vérification indépendante sur disque (extraction kit-e3-verif/, 16/16 : proxy, identité scénario racine/zip, les trois LISEZMOI, fixtures, wsb, 55 entrées).

**La livraison (scripts/livrer_vague_e3.py, modèle livrer_vague_e2.py — chaque mutation RECOUPÉE PAR RELECTURE, D12 étendu).** La vague e2 CONSOMMÉE archivée dans archives-livraisons/vagues-m5b/ (LISEZMOI-m5b-e2.txt + scenario-m5b-e2.ps1 + m5b-kit-e2.zip, md5 recoupés avant/après, aucune suppression) ; la vague e3 posée à la racine /test (m5b-kit-e3.zip 981b1a5b… + scenario-m5b-e3.ps1 6b347fa0… + LISEZMOI-m5b-e3.txt a554b9b3…, md5 distants == locaux par relecture) ; preuves-m5b/LISEZMOI-preuves.txt passé à la liste e3 (LES DEUX PIÈCES NOUVELLES y vivent — page-sonde-armement.txt + edge-version.txt : la liste « e3 == e2 » de l'Entrée 138 est ainsi CORRIGÉE de ce que la correction ajoute, l'opérateur sait quoi renvoyer) ; l'index LISEZMOI-archives-livraisons.txt mis à jour (le bloc « vague e2 consommée » après signatures-I-0.6.0.txt, relu == réécrit) ; la racine /test = EXACTEMENT 8 entrées D143 (vague courante e3 + corriger-wsb ×2 + preuves-m5b vierge + les deux archives).

**Frontières.** Le scellé 0.6.0-rc.1 sha256 4b8f6af6… : PAS UN OCTET BOUGÉ (l'assembleur l'asserte base == dépôt, le zip relu l'affirme, la carte génération 7 vit sous la lignée D80 du coffre) ; le sceau (onze arbres verts) et les arbres scellés INTACTS (le scénario vit dans m5/vm/, hors des arbres d'intention) ; fixtures v5 inchangées ; la finale 0.6.0 TOUJOURS NON POSÉE (elle attend un run VERT — la carte ne ment pas) ; aucune clé traversée (les clés du kit sont les clés de test jetables) ; aucune suppression Drive ; corbeille non vidée ; D139 demeure ouvert (T7 éventuel), non bloquant.

**Vérifiabilité.** python3 scripts/construire_scenario_e3.py (11 remplacements, rejeu = écriture identique) ; python3 scripts/assembler_kit_e3.py <kit-e2.zip> <sortie> ; python3 scripts/livrer_vague_e3.py (idempotent par REFUS) ; m5/vm/scenario-m5b-e3.ps1 (852 lignes, BOM+CRLF) ; download/vague-e3/ (kit + LISEZMOI-KIT + kit-e3-verif/) ; le listing API de /test (8 entrées, vague e3) ; m5/vm/LISEZMOI-terrain-m5b-e3.txt (livré en LISEZMOI-m5b-e3.txt).

**SUITE.** LE GESTE TERRAIN : m5b-kit-e3.zip depuis /test, dossier NEUF, corriger-wsb.bat, double-clic scenario-m5b.wsb (cinq à huit minutes), renvoyer TOUT preuves-m5b (la liste vit au témoin — les pièces nouvelles page-sonde-armement.txt et edge-version.txt comprises). Le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, la ligne de flux aux preuves. Si vert : python3 m5/build_m5.py --sceller-final pose la finale 0.6.0 avec la validation consignée. D139 demeure ouvert, non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-138) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 139" in texte:
    sys.exit("ECHEC : l'Entrée 139 existe déjà")
i138 = texte.find("## Entrée 138")
im = texte.find(MARQUEUR)
if not (0 <= i138 < im):
    sys.exit("ECHEC : ordre inattendu (138/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 138 < 139 < marqueur
j138 = nouveau.find("## Entrée 138")
j139 = nouveau.find("## Entrée 139")
jm = nouveau.find(MARQUEUR)
if not (0 <= j138 < j139 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 139 insérée ({len(ENTREE)} caractères) — ordre 138<139<marqueur recoupé")
