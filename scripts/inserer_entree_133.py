#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_133.py — JOURNAL_TRAVAIL.md : insère l'Entrée 133 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
132 < 133 < marqueur recoupé — le même contrat que les entrées 127-132)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 133 — LE PAQUET DE CÉRÉMONIE 0.6.0 LIVRÉ + LE CANAL GITHUB RECONFIGURÉ (04/11) : « continue le paquet de cérémonie 0.6.0 et reconfigure origin pour le git push en echec » — l'arbre m5 ENTRE au sceau (11e arbre, balise 0.6.0, empreinte 1869422e…) et l'arbre v06 est re-signé pour le NOMMER (a8166442…, modèle D126) ; le paquet bout-en-bout prouvé (11/11 avec clé jetable) déposé dans /test avec LISEZMOI ; origin rebranché sur GitHub (jeton du dossier Tokens, JAMAIS affiché), les 11 commits jamais poussés du jalon enfin au miroir

**La demande (consignée fidèlement) et le précédent v7 relu.** « tu peux pas me faire comme pour la cérémonie v7 ? tu m'avais fait un zip avec le script de cérémonie en python, un document à signer, je mettais mon fichier de clé privée et ça produisais un document signé que je te donnais après » puis « continue le paquet de cérémonie 0.6.0 et reconfigure origin pour le git push en echec ». Le paquet v7 (download/paquet-ceremonie-v7.zip, relu pièce à pièce) : a-signer.txt (10 lignes « arbre balise empreinte », 1 ligne neuve m4/0.5.1) + ceremonie_hors_ligne.py (autonome, stdlib seule, autotest RFC 8032, chaque signature auto-vérifiée avant écriture) + LISEZMOI (le geste : signer hors ligne, rendre signatures-I.txt dans /test du Drive). L'état du sceau AVANT le geste : DIX arbres verts (m0-m4, m6, m7, demo, terrain, v06), l'arbre m5 HORS du sceau — et build_m5.py le nommait lui-même : « l'arbre m5 porte les révisions R3 écrites-avant-code (D136) — sa signature appartient à la cérémonie 0.6.0 ».

**Le périmètre ne grandit que signé (le modèle D126 appliqué à m5).** Deux éditions solidaires : (1) v06/sceau_I.py — la table ARBRES gagne « m5 : proxy.exe (relevement https), 0.6.0 » entre m4 et m6 (l'ordre canonique des codes de sortie conservé) ; (2) v06/I/README.md § 1 — « Dix arbres » devient « Onze arbres », la table porte la ligne m5 et une phrase nomme l'entrée (« même modèle que l'entrée de CF3 à la re-cérémonie D126 »). La re-signature de v06 n'est pas un effet de bord : c'est la CONTREBANDE ÉVITÉE — un code qui signerait onze arbres tandis que la spécification scellée en nomme dix serait exactement le mécanisme qui s'exempte de lui-même (§ 1, défaut X2). preparer : la remise passe à 11 lignes ; l'état pré-cérémonie est EXACT : 9 arbres verts à l'identique (mêmes empreintes que la cérémonie précédente — la re-signature des 9 lignes inchangées est déterministe, Ed25519, mêmes octets), m5 CODE 12 (manifeste déposé absent), v06 CODE 10 (README.md modifié). GEL consigné : m5/I/ et v06/I/ ne doivent plus bouger jusqu'au retour de la remise — les signatures couvrent les empreintes COURANTES (m5 1869422eca104a6ad84b45dcc0649132cb9230bb6b001ad1cefb32acf35f1c6e ; v06 a8166442abe2d98f2c01a04a08def03bc832829d54c56d07a75d1a92168a9e9f).

**La chaîne prouvée DEUX FOIS avant la livraison.** (1) Copie minimale du dépôt (/tmp/test-sceau : les 11 arbres I/ + sceau-I/ + sceau_I.py) : signer-test (clé de TEST du lab, spec § 8 — JAMAIS sur le dépôt réel) → deposer → verifier : 11 arbres VERTS code 0, empreintes m5 et v06 conformes — la table nouvelle est cohérente de bout en bout. (2) Le paquet lui-même (scripts/assembler_paquet_ceremonie_060.py) : autotest RFC 8032 VERT + clé JETABLE générée + signer (11 signatures auto-vérifiées) + verifier : TOUT VERT 11/11 — puis les artefacts de test DÉTRUITS (la clé privée jetable comprise) et le zip vérifié : 3 entrées, AUCUNE clé, intégrité OK (9 232 o). Le paquet : download/paquet-ceremonie-0.6.0.zip = a-signer.txt (11 lignes) + ceremonie_hors_ligne.py (inchangé, agnostique du compte d'arbres) + LISEZMOI-ceremonie-0.6.0.txt (le geste v7 à l'identique : python3 ceremonie_hors_ligne.py signer a-signer.txt cle-I-privee.txt → signatures-I.txt → /test ; contrôles sans la clé : ONZE lignes, ligne m5 balise 0.6.0, ligne v06 à l'empreinte a8166442… — « si vous lisez 3910e9bd… : ancien paquet, ne signez pas »).

**La livraison et le dossier /test.** paquet-ceremonie-0.6.0.zip + LISEZMOI-ceremonie-0.6.0.txt déposés dans /test (le point de reprise HISTORIQUE des paquets de cérémonie — le LISEZMOI v7 disait « là où vous avez pris ce paquet »), md5 recoupés par RELECTURE (2/2) ; /test porte 10 entrées (les 8 de la vague v8 D143 + les 2 nouvelles — la file de livraison vit sa vie, aucune suppression). Canal : scripts/livrer_paquet_ceremonie_060.py sur drive_sync (jetons .gdrive/).

**Le canal GitHub reconfiguré (la seconde demande).** Cause racine de l'échec « non bloquant » (Task 50) : dans le labo restauré, origin pointait vers le BUNDLE LOCAL upload/triade-history.bundle (lecture seule — un bundle ne reçoit pas de push). La mécanique authentique retrouvée dans le dépôt : check_auth.py (le jeton vit dans .gdrive/token_git.txt, masqué à l'écran) et l'Entrée 0 du journal (« configuré le credential helper vers .gdrive/git-credentials (600) »). Réparation : token_git.txt rapatrié du dossier Drive « Tokens » (93 o, md5 ca8c146b…, JAMAIS affiché), API /user 200 (compte alexisfrlopez-debug), .gdrive/git-credentials écrit (600), credential helper store, origin → https://github.com/alexisfrlopez-debug/triade.git. CONSTAT d'ampleur : GitHub ne portait que main (f62711b, D137) — les ONZE commits du jalon (07d392e…cd85d8a, la chirurgie 0.5.1 jusqu'au POST-SCRIPTUM Task 50) n'avaient JAMAIS été poussés, l'origin en bundle les faisait échouer en silence à chaque sync_backup. Poussée : bundle051/v0.5.1-jalon-v7 créée sur GitHub à cd85d8a (== HEAD local, recoupé par ls-remote) ; main INTACT à f62711b — fusionner le jalon dans main est une décision de clôture qui appartient au développeur, pas au labo. scripts/reconfigurer_origin_github.py persiste la mécanique (jeton masqué partout).

**Frontières.** La clé réelle du développeur jamais traversée, jamais affichée (le paquet ne contient AUCUNE clé ; la clé de test n'a vécu que dans /tmp, détruite) ; les 9 arbres signés INCHANGÉS (mêmes empreintes) ; aucun artefact scellé touché (proxy 0.6.0-dev.1 4b8f6af6… et scellé 0.5.1 fb41697d… intacts) ; le dépôt réel reste en état pré-cérémonie (clé DÉPOSÉE RÉELLE intacte, signatures des 10 arbres en place) ; .keys/ reste absent du labo (le scellage carte génération 7 exigera un geste dédié, proposé après la remise).

**Vérifiabilité.** python3 v06/sceau_I.py preparer / verifier (l'état nommé : 9 verts + m5 CODE 12 + v06 CODE 10) ; /tmp/test-sceau rejouable (signer-test → 11 verts) ; download/paquet-ceremonie-0.6.0.zip (3 entrées) ; listing de /test (10 entrées, md5 recoupés) ; git ls-remote origin (branche cd85d8a == HEAD) ; .gdrive/last_sync.log.

**SUITE.** Le retour attendu : signatures-I.txt dans /test → sceau deposer → verifier (ONZE arbres verts) → ARBRES_GARDE_M5 étendue de m5 (build_m5.py — geste post-cérémonie, la garde passera verte d'un coup) → scellage carte génération 7 (.keys absent du labo : le geste dédié sera proposé) → kit VM ÉTAPE 2 (le navigateur du bac à sable, mandataire 127.0.0.1:25000, page http://autorite.test/ sous --relever-https) → run M5-b étape 2 — le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, la ligne de flux aux preuves. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-132) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 133" in texte:
    sys.exit("ECHEC : l'Entrée 133 existe déjà")
i132 = texte.find("## Entrée 132")
im = texte.find(MARQUEUR)
if not (0 <= i132 < im):
    sys.exit("ECHEC : ordre inattendu (132/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 132 < 133 < marqueur
j132 = nouveau.find("## Entrée 132")
j133 = nouveau.find("## Entrée 133")
jm = nouveau.find(MARQUEUR)
if not (0 <= j132 < j133 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 133 insérée ({len(ENTREE)} caractères) — ordre 132<133<marqueur recoupé")
