#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_137.py — JOURNAL_TRAVAIL.md : insère l'Entrée 137 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
136 < 137 < marqueur recoupé — le même contrat que les entrées 127-136)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 137 — LE KIT VM ÉTAPE 2 LIVRÉ AU COFFRE : la vague e2 (le flux NAVIGATEUR, critère (b) de D136) — scénario Edge headless par le mandataire sur le proxy 0.6.0-rc.1 ARMÉ --relever-https, kit assemblé sur la base v8 (55 entrées, proxy + scénario remplacés, reprises assertées), livraison D143 complète (vague v8 + cérémonie 0.6.0 archivées, racine /test = vague courante seule) ; la finale 0.6.0 attend le run terrain

**La demande et la suite consignée.** « ok pour la suite » — la suite était écrite (Entrée 136, SUITE) : le kit VM ÉTAPE 2, puis le run M5-b étape 2 (critère (b) de D136), puis --sceller-final si vert. Le jalon M5 (b) avait l'étape 1 RENTRÉE (runs v7/v8, verdicts OK 0 réserve — par le CLIENT CLI forme-absolue) ; il manque le NAVIGATEUR : « un flux navigateur intercepté de bout en bout dans la VM ; échec propre sur certificat invalide constaté dans LE MÊME run ». Le proxy 0.6.0-rc.1 scellé (carte génération 7, 4b8f6af6…) porte exactement ce qu'il faut : le relèvement amont http→https sous politique armée (http-08:R3), la ligne de flux (http-10:R3), la CLI --relever-https (http-12:R3).

**Le scénario e2 (m5/vm/scenario-m5b-e2.ps1, BOM + CRLF, 805 lignes — la structure v8 reprise, les sections navigateur nouvelles).** (1) LE NAVIGATEUR DU BAC À SABLE : Edge localisé par sondes (Program Files (x86), Program Files, App Paths du registre, PATH) — REFUS NAVIGATEUR-ABSENT nommé (le critère (b) est un critère navigateur : sans navigateur, le run ne dit rien) ; version consignée au témoin (DIAG-EDGE-VERSION, pièce edge-version, diagnostique ADDITIF). (2) L'INVOCATION : headless, mandataire EXPLICITE 127.0.0.1:25000, page http://127.0.0.1/ (IP LITTÉRALE — D139 : hosts ignoré dans la VM, le décisif ne dépend d'AUCUNE résolution ; fixtures v5 à SAN IP inchangées) ; --proxy-bypass-list="<-loopback>" RETIRE la dérivation de boucle implicite de Chromium (sinon 127.0.0.1 contournerait le mandataire — l'échec serait nommé par les refus DOM/FLUX) ; --disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,HttpsFirstModeEnabled désactive la montée https du navigateur (un CONNECT serait REJETÉ par le protocole — D136 — et le repli http d'Edge aboutirait au même chemin relevé, trace au journal). (3) LA PREUVE NAVIGATEUR SUR LE DISQUE (D99/D138) : DEUX invocations par run (DOM par --dump-dom, capture par --screenshot, profils NEUFS à chaque fois) — le DOM est le DÉCISIF : DOM-A-MARQUEUR (la page de l'autorité REÇUE ET RENDUE par le navigateur — le marqueur TRIADE-M5B-PAGE-200 ne vit nulle part ailleurs), DOM-B-502 + DOM-B-SANS-PAGE (la page d'erreur « 502 » rendue par le navigateur ET le marqueur ABSENT — l'autorité autonome ne sert rien) ; la capture est ADDITIVE (DIAG-CAPTURE-A/B — l'œil juge, le verdict ne dépend pas d'elle). (4) L'ARMEMENT CONSTATÉ AVANT LE NAVIGATEUR : le proxy reçoit --relever-https par cmd /c (capture NATIVE de console, modèle v8) et la ligne « relever-https arme » est attendue sous 20 s APRÈS l'écoute — REFUS PROXY-SANS-ARMEMENT sinon (un proxy muet sur le relèvement ne prouverait rien, le run s'arrête AVANT de lancer le navigateur). (5) LES LIGNES DE FLUX aux verdicts : FLUX-A-V0 (« flux GET 127.0.0.1:443 v=0 e=NN s=NN ») et FLUX-B-V3 (v=3 = certificat rejete, TRANSPORTÉ tel quel de tls-08 — la ligne nomme la CAUSE, la 502 nomme l'effet), aiguilles écrites depuis le MODÈLE DE COMPOSITION du harnais (ligne_flux de harnais_session_r3.py — jamais devinées). (6) LES AUTORITÉS PAR DÉLAI (--arret-apres-secondes 150) : le navigateur fait un nombre de requetes INCONNU (page, favicon, capture) — jamais --arret-apres N (un compte trop bas couperait le run) ; l'attente de fin est bornée (restant + 20 s). (7) LE DÉCOR v8 REJOUÉ À L'IDENTIQUE : section 0bis parefeu muet (règles ALLOW TRIADE-M5B + inboundusernotification off, D142/D143), hosts + sonde D139, empreintes consignées (le témoin porte l'empreinte du binaire RÉELLEMENT exécuté — un écart sera nommé), matrice curl ADDITIVE (T2a/T2b/T3/T5 ports 4443/4444 + T6 Dnscache, branches S1-S4 recalibrées : S4 attendue depuis 0.5.1, S3 = RÉGRESSION à nommer), témoin D99 posé en dernier acte, échecs NOMMÉS (KIT-ABSENT | NAVIGATEUR-ABSENT | RACINE-NON-INSTALLEE | AUTORITE-MUETTE | PROXY-MUET | PROXY-SANS-ARMEMENT | NAVIGATEUR-A/B-ECHEC | DOM-A/B-INVALIDE | DOM-B-PAGE-SERVIE | FLUX-A/B-MANQUANT | AUTORITE/PROXY-SORTIE-ANORMALE).

**L'assemblage (scripts/assembler_kit_e2.py, modèle assembler_kit_v7 — Task 43).** Base = le kit v8 LIVRÉ (m5b-kit-v8.zip rapatrié du coffre PAR ID, md5 recoupé 3986421f… — le coffre fait foi) ; DEUX pièces remplacées (kit-m5b/proxy.exe : 0.5.1 fb41697d… → 0.6.0-rc.1 4b8f6af6… 36 352 o, asserté AVANT/APRÈS ; kit-m5b/scenario-m5b.ps1 : v8 → e2, BOM + CRLF assertés) + DEUX documents (LISEZMOI-KIT-M5B.md e2 ; preuves-m5b/LISEZMOI-preuves.txt e2) ; 51 reprises ASSERTÉES par md5 (fixtures v5 — racine 86525998… —, autorite_test.py, client-m5b.ps1 vestige de l'étape 1, scenario-m5b.wsb, python embarqué) ; le zip né porte m5b-kit/ à sa racine (structure v8 exacte, 55 entrées) et l'intégrité est RE-VÉRIFIÉE à la sortie (testzip, proxy relu == 4b8f6af6…, fixtures relues == v8) : **m5b-kit-e2.zip, 11 191 067 o, md5 76e7b02f8c922981dbdc64fb34c6f679**.

**La livraison D143 (scripts/livrer_vague_e2.py — chaque geste asserté, chaque mutation RECOUPÉE PAR RELECTURE, D12 étendu).** (1) La vague v8 CONSOMMÉE (run v8 OK 0 réserve — le décor est verrouillé) archivée dans archives-livraisons/vagues-m5b/ : LISEZMOI-m5b-v8.txt + scenario-m5b-v8.ps1 + m5b-kit-v8.zip (déplacements par addParents/removeParents EN REQUÊTE — la leçon du run v7). (2) Les pièces de cérémonie 0.6.0 CONSOMMÉES (onze arbres verts, 04/11) archivées au même endroit : paquet-ceremonie-0.6.0.zip + LISEZMOI-ceremonie-0.6.0.txt + signatures-I.txt RENOMMÉE signatures-I-0.6.0.txt à l'archive (deux remises du même nom y vivraient — la 0.5.1 y est déjà). (3) La vague e2 posée à la racine : m5b-kit-e2.zip + scenario-m5b-e2.ps1 (octet-identique au scénario du kit, l'identité racine/zip est la règle v8 — assertée) + LISEZMOI-m5b-e2.txt (le guide terrain : le geste, les résultats attendus, LES RISQUES CONSIGNÉS). (4) preuves-m5b/LISEZMOI-preuves.txt passé à la liste e2 (relu et recoupé) ; l'index LISEZMOI-archives-livraisons.txt mis à jour (section vagues-m5b + date, relu et recoupé). (5) ÉTAT FINAL recoupé : la racine /test porte EXACTEMENT {LISEZMOI-m5b-e2.txt, m5b-kit-e2.zip, scenario-m5b-e2.ps1, corriger-wsb.bat, corriger-wsb.ps1, preuves-m5b, archives-livraisons, archives-preuves} — la vague courante seule, la règle D143 tenue.

**Honnêteté des constats (le labo n'a NI Windows NI Edge NI PowerShell).** Le scénario e2 est RELU, pas exécuté : la lignée v2→v8 a prouvé que ce qui casse se nomme au premier lancement (PowerShell ou les refus du scénario) — les risques sont CONSIGNÉS au LISEZMOI terrain (faute PowerShell éventuelle ; Edge headless varie par build — la version est une pièce ; le DOM de la page d'erreur 502 attendu porteur du code, « 502 » aucun locale n'écrit le chiffre autrement ; la dérivation de boucle et la montée https couvertes par drapeaux). Le relèvement lui-même est prouvé au labo par l'oracle D136 (365 cas, ligne de flux octet par octet) — mais JAMAIS par un vrai navigateur : c'est précisément ce que le run décidera. La vue in-VM reste diagnostique (D138 : le rc du producteur fait foi, les pièces host jugées au labo — Verdict-Vue partout, RÉSERVE nommée sur vue vide + rc=0).

**Frontières.** L'artefact 0.6.0-rc.1 sha256 4b8f6af6… OCTET POUR OCTET inchangé (le kit EMBARQUE le binaire, il ne le touche pas — l'assertion d'assemblage le prouve) ; le sceau et les arbres d'intention INTACTS (onze verts constatés AVANT le geste — le scénario vit dans m5/vm/, HORS de l'arbre m5/I signé) ; les cartes m0/m3/m4 et la carte génération 7 INTACTES ; fixtures v5 INCHANGÉES (racine 86525998…) ; aucune clé réelle ne voyage (clés de test jetables) ; aucune suppression Drive (archivage, jamais de jet — la corbeille n'est pas un lieu d'archivage) ; le bruit de bits de mode préexistant n'est pas commis (phénomène connu et consigné) ; la finale 0.6.0 N'EST PAS posée (elle attend le verdict terrain — la carte ne ment pas).

**Vérifiabilité.** Le kit au coffre /test : m5b-kit-e2.zip md5 76e7b02f… (recoupé par relecture) ; le scénario relu du zip == m5/vm/scenario-m5b-e2.ps1 du dépôt ; `python3 scripts/assembler_kit_e2.py <kit-v8.zip> <sortie.zip>` rejoue l'assemblage (assertions fail-closed) ; `python3 v06/sceau_I.py verifier` : ONZE arbres VERTS (m5 = 1869422e…) ; la racine /test listée = 8 entrées D143 exactes ; LE TÉMOIN-M5B.TXT attendu du run e2 EST la preuve (modèle terrain.17 — les refus nommés désignent eux-mêmes le coupable).

**SUITE.** LE GESTE TERRAIN : télécharger m5b-kit-e2.zip depuis /test, extraire dans un dossier NEUF, corriger-wsb.bat, double-clic du scenario-m5b.wsb — cinq à huit minutes — puis renvoyer TOUT preuves-m5b (la liste vit au LISEZMOI-preuves et en dernière ligne du témoin). SI le verdict est OK (ou OK-sous-réserve levée sur pièces host) : `python3 m5/build_m5.py --sceller-final` pose la balise 0.6.0 avec la validation consignée (l'exigence est déjà écrite au code — le plan m5 : « la balise 0.6.0 est posée à la validation terrain »). D139 demeure ouvert (T7 éventuel), non bloquant ; le chantier (c) du M5 (patch à chaud du journal) n'est pas ouvert.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-136) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 137" in texte:
    sys.exit("ECHEC : l'Entrée 137 existe déjà")
i136 = texte.find("## Entrée 136")
im = texte.find(MARQUEUR)
if not (0 <= i136 < im):
    sys.exit("ECHEC : ordre inattendu (136/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 136 < 137 < marqueur
j136 = nouveau.find("## Entrée 136")
j137 = nouveau.find("## Entrée 137")
jm = nouveau.find(MARQUEUR)
if not (0 <= j136 < j137 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 137 insérée ({len(ENTREE)} caractères) — ordre 136<137<marqueur recoupé")
