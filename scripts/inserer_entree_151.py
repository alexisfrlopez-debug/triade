#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_151.py — JOURNAL_TRAVAIL.md : insère l'Entrée 151 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
150 < 151 < marqueur recoupé — le même contrat que les entrées 127-150)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 151 — LA RECOUPURE POST-MORTEM DES DÉCISIONS D138/D145/D148 ACCOMPLIE (« continue » — la reprise de session M7) : les TROIS décisions FIDÈLES à leurs pièces originales — les pièces fondatrices RAPATRIÉES des archives du coffre (v6 : 28 ; e2 : 7 ; e4 : 37 re-contrôlées ; v8 : la matrice S3 ciblée), md5 contrôlés contre le coffre, LECTURE SEULE ; chaque fait fondateur cité par les décisions RETROUVÉ SUR PIÈCE, mot pour mot et octet pour octet ; UNE PRÉCISION NOMMÉE sur la formulation D148 (la pièce T2b porte la Date du run) ; l'instrument du recoup CORRIGÉ SUR PIÈCES après son ÉCHEC NOMMÉ (trois défauts d'instrument, les pièces immuables — D154 étendue au recoup de doctrine) (05/11)

**Le geste (la promesse de reprise : sans les trois décisions il n'y a pas de verdict de run — le terrain M7-(d) les appliquera ; or D154 dit que l'instrument est lui-même soupçonnable : les décisions SONT l'instrument, on les recoupe SUR PIÈCES).** La reprise a suivi l'ordre promis : (1) l'état du labo re-vérifié AU geste même sur les originaux (la porte round-trip 783 + 1037 VERT, le build rejoué sha d122bc68… CONSTANT, la sonde à l'oracle qemu 6/6 code 6, le corpus unix dd14195c… INTACT, le coffre /test recoupé — la vague m6d demeure courante) ; (2) les décisions D138-D155 relues depuis DECISIONS.md (sur pièces, jamais de mémoire) ; (3) la recoupure elle-même. **LE RAPATRIEMENT** (scripts/rapatrier_preuves_doctrine.py, lecture seule, aucune écriture au coffre) : preuves-run-v6 (28 pièces — D138), preuves-run-e2 (7 — D145), preuves-run-v8 EN FETCH CIBLÉ (la matrice S3 + hosts — la revendication D148 « v6, v8, e4 : pièces identiques octet pour octet »), preuves-run-e4 (37 — les copies Task 61 re-contrôlées md5 contre le coffre, le coffre fait foi ; l'unique extra local LISEZMOI-preuves.txt NOMMÉ — le readme du réceptacle, jamais une pièce) — TOUT CONFORME.

**D138 sur pièces v6 — LA LECTURE VIRTUALISÉE EST AVEUGLE, confirmée mot pour mot.** page-d2b.txt = 279 o EXACT, marqueur TEMOIN-PAGE : TRIADE-M5B-PAGE-200 complet, IDENTIQUE v6/e4 (la même page réelle, md5 d6f98eb29f…) ; l'étiquette auto-contradictoire SUR PIÈCE (« diagnostic ECHEC DIAG-CURL-IP-SANS-REVOCATION — … — rc=0 » : le T2b RÉUSSI étiqueté ÉCHEC) ; les lectures in-VM VUES VIDES («  » ×2 au journal) et la branche S2 nommée À TORT, renversée S3 par le labo sur pièces (le VERDICT v6 porte « BRANCHE S3 » et le renversement §3-4) ; AUTORITE-B « arret propre — 0 requete(s) servie(s), 2 poignee(s) refusee(s) — motif=delai » DANS SA PIÈCE tandis que le rc capturé reste vide (« recu ») ; AUTORITE-A jamais arrêtée — SA pièce sans « requete servie » NI « arret propre » (0 servie → --arret-apres 1 jamais atteint → Kill), rc capturé vide. NOTE B6 : les instances v2/v3 sont des consignations antérieures (leurs pièces vivent au coffre, preuves-run-v2-depot1/2/3) ; le décompte « quatrième instance » est PORTÉ PAR LA PIÈCE VERDICT v6 (§1 et §7).

**D145 sur pièces e2 — AUCUNE GARDE EN LIVE D'UN FICHIER VIVANT, confirmée mot pour mot.** Le REFUS PROXY-SANS-ARMEMENT SUR PIÈCE (la garde en live a lu « journal : 0 o » sous 20 s — le navigateur jamais lancé) ; la sonde TCP à 00:13:17 SUR PIÈCE (« proxy demarre — sonde : connect 127.0.0.1:25000 reussi », l'autorité A à 00:13:16 — l'écoute était posée, donc bannière et armement, qui la PRÉCÈDENT au contrat http-12:R3 Q3, étaient déjà écrites) ; **la pièce post-mortem = 128 o EXACT, 7 lignes EXACTES, ligne 2 « relever-https arme »** (l'armement que la garde cherchait, lisible seulement après la mort du producteur) ; le CONTRASTE 0 o vivant / 128 o post-mortem consigné mot pour mot par la pièce VERDICT e2 §4 (texte aplati : « ZÉRO octet », « 7 lignes COMPLÈTES », « UNE WriteFile PAR LIGNE ») ; l'application e4 SUR PIÈCE (la garde FONCTIONNELLE « armement PROUVE PAR OPERATION », le verdict « POST-MORTEM apres le quit, D145 : la ligne CONSTATE, c'est la SONDE d'armement qui a garde »).

**D148 sur pièces e4 — LES VERDICTS POST-MORTEM ET SUR PIÈCES, confirmée mot pour mot.** « VERDICT : M5-B ETAPE 2 — ECHEC NOMMÉ (5) » SUR PIÈCE ; les CINQ refus aux NOMS EXACTS (NAVIGATEUR-A ; AUTORITE-A-SERVIE ; NAVIGATEUR-B ; DOM-B-INVALIDE ; POIGNEE-B-REFUSEE) ; le rc d'Edge capturé VIDE (« code de sortie » ×2, « producteur rc= » ×2 — la réserve transformée en ÉCHEC par le témoin aveugle) ; dom-b.txt VIDE (0 o, md5 d41d8cd98f…) + « DOM B vu : 0 o » + « nav-b.png ABSENTE » ; la réception TRIPLEMENT recoupée (certificat rejete + la ligne de flux servie s=34 ; poignee de main refusee au journal autorité ; ERR_HTTP_RESPONSE_CODE_FAILURE au navigateur) ; la 502 NUE servie s=34 (TXT_502_CERT 34 o) ; le libellé périmé « REGRESSION a nommer » SUR PIÈCE et le tunnel du run A établi hors ligne (D140 concernait les credentials DU PROXY, jamais curl).

**LA PRÉCISION NOMMÉE (D148, matrice S3 — consignée append-only, la règle D148 elle-même CONFIRMÉE).** La formulation « pièces identiques octet pour octet » est EXACTE pour curl-d2a/d3/d5 + hosts-lu (md5 identiques v6/v8/e4) ; pour la pièce T2b (curl-d2b.txt) elle vaut SAUF LA LIGNE Date — la seule ligne qui varie entre v6/v8/e4 est la Date du run (pièce CRLF de longueur fixe : même taille 946 o, trois md5 distincts). LA STATIONNARITÉ S3 EST CONFIRMÉE EN SUBSTANCE ; la précision vit au présent VERDICT (download/recoup-post-mortem/VERDICT-recoup-doctrine.txt) et en la présente entrée — D148 n'est PAS rétro-écrite (append-only, la règle inchangée).

**L'instrument corrigé sur pièces (D154 — la lignée D151/D152/D154 étendue au recoup de doctrine lui-même).** Le premier passage a rendu ÉCHEC NOMMÉ (3) — TOUS défauts d'INSTRUMENT, les pièces immuables (md5 contrôlés aux DEUX passages) : (1) la vérification du jeu e4 exigeait l'égalité stricte alors que la copie Task 61 porte l'LIseMOI du réceptacle (l'extra est désormais NOMMÉ, jamais une pièce) ; (2) la C4 matchait « UNE WriteFile PAR LIGNE » contre le texte BRUT — la pièce VERDICT wrappe (« UNE WriteFile PAR\\nLIGNE »), la matching se fait désormais sur le texte APLATI ; (3) la D7 cherchait la ligne Date à l'index 17 — la pièce T2b est CRLF (38 lignes en splitlines, la Date à l'index 24), corrigé sur pièces. Le second passage : RECOUP VERT, le verdict écrit (VERDICT-recoup-doctrine.txt, la pièce née du juge).

**Frontières.** Le coffre /test INCHANGÉ (lecture seule, aucune écriture — la vague m6d demeure courante, la clôture D143 attend le dépôt du kit M7) ; AUCUNE pièce modifiée (md5 contrôlés avant et après, les pièces immuables) ; la finale 0.7.0, le scellé 0.8.0-dev.1, le corpus dd14195c… et la sonde d122bc68… INTACTS ; download/ HORS dépôt git (les pièces du labo, jamais committées — modèle preuves-run-m6d) ; .gdrive/ jamais lu ; aucune passation (le présent geste n'est pas un geste de jalon) ; scripts suivis : rapatrier_preuves_doctrine.py, recouper_doctrine_post_mortem.py, inserer_entree_151.py.

**Vérifiabilité.** python3 scripts/rapatrier_preuves_doctrine.py (le rapatriement re-joué — md5 == coffre) ; python3 scripts/recouper_doctrine_post_mortem.py (le recoup re-joué — RECOUP VERT, l'instrument corrigé prouvé par le rejeu) ; download/recoup-post-mortem/VERDICT-recoup-doctrine.txt (le verdict écrit) ; les pièces download/preuves-run-{v6,e2,v8,e4}/ ; DECISIONS.md D138/D145/D148 (les originaux des décisions).

**SUITE.** LE CHANTIER M7-(b) — la TROISIÈME instanciation de la même couche I : le corpus paritaire RISC-V (les MÊMES fichiers I que unix/ — le diff nul mesuré par script, l'oracle régénéré vert sur l'instance qemu, la parité § 8.3 sur les TROIS profils, la garde anti-table-x86 au corpus entier) ; le point d'attention NOMMÉ demeure : la portée imm12 des charges — les fenêtres par ANCES auipc+addi (le modèle des paires sr-04 généralisé, chaque fenêtre déclarée en I3) ; puis (c) le patch scratch+fence.i + le verrou multi-profils, (d) l'export multi-profils + le terrain → la finale 0.8.0 (le terrain sera jugé POST-MORTEM ET SUR PIÈCES — D138/D145/D148, la présente recoupure vient de le ré-établir sur originaux).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-150) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 151" in texte:
    sys.exit("ECHEC : l'Entrée 151 existe déjà")
i150 = texte.find("## Entrée 150")
im = texte.find(MARQUEUR)
if not (0 <= i150 < im):
    sys.exit("ECHEC : ordre inattendu (150/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 150 < 151 < marqueur
j150 = nouveau.find("## Entrée 150")
j151 = nouveau.find("## Entrée 151")
jm = nouveau.find(MARQUEUR)
if not (0 <= j150 < j151 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 151 insérée ({len(ENTREE)} caractères) — ordre 150<151<marqueur recoupé")
