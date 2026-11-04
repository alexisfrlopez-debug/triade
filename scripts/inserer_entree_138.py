#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_138.py — JOURNAL_TRAVAIL.md : insère l'Entrée 138 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
137 < 138 < marqueur recoupé — le même contrat que les entrées 127-137)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 138 — LE RUN e2 ANALYSÉ SUR PIÈCES : ÉCHEC NOMMÉ « REFUS PROXY-SANS-ARMEMENT » — le scellé 0.6.0-rc.1 est INNOCENT (l'armement A EU LIEU, la ligne vit à la pièce post-mortem) ; le coupable est LA GARDE EN LIVE du scénario e2, qui lit un journal encore ouvert (« vues vides », le symptôme des runs v7/v8 — D138) ; clôture D143 du run ; D145 : les gardes sont fonctionnelles ou post-mortem ; la correction e3 proposée

**La demande et le rapatriement.** « preuves déposées dans le drive /test, mais je pense que le run n'est pas tout vert » — 6 pièces rapatriées du coffre preuves-m5b (id 1QofaM11…, dépôt 04/11 00:25:36Z), 6/6 CONFORMES par md5 recoupé par relecture (scripts/rapatrier_preuves_e2.py, par id) ; le scénario exécuté == m5/vm/scenario-m5b-e2.ps1 du dépôt == la copie /test == le scénario du zip (md5 e06db6c0… recoupé aux TROIS exemplaires). Run daté 00:12:43–00:15:46Z, VM 9687CE78-D5CF-4 (la machine des runs v7/v8). Empreintes consignées PAR LE RUN : proxy.exe sha256 4b8f6af6… == LE 0.6.0-rc.1 SCELLÉ (carte génération 7), racine v5 86525998…, fixtures fe37071b…/08b8a6bf… intactes. Préalable au geste : le labo local était PÉRIMÉ à a5035e1 (recyclage survenu APRÈS la Task 55 — le dépôt avait vécu jusqu'à 9b3544d) : fast-forward origin recoupé par ls-remote, le bruit de bits de mode préexistant neutralisé par core.fileMode=false (rien commis), scripts d'exploration locaux non suivis (lister_drive.py, lister_preuves_e2.py, rapatrier_journal_v8.py, rapatrier_vagues_m5b.py — rapatrier_coffre_cf1.py local ancien mis à l'écart : la version du dépôt fait foi).

**Le verdict.** ÉCHEC NOMMÉ REFUS PROXY-SANS-ARMEMENT — la DERNIÈRE ligne du journal du scénario (00:13:37Z) : « aucune ligne « relever-https arme » au journal proxy en 20 s — journal : 0 o, debut : ». Le scénario fail-closed s'est arrêté LÀ (quit puis kill, exit 2) : le NAVIGATEUR N'A JAMAIS ÉTÉ LANCÉ, le run B jamais joué, le témoin jamais posé (il se pose en DERNIER acte — D99). LE CRITÈRE (b) DE D136 N'EST PAS TRANCHÉ : le run ne dit RIEN du navigateur — il dit un refus de décor. Les pièces absentes (temoin, dom-*, nav-*, curl-*, dnscache, ipconfig, hosts-lu, edge-version) sont CONFORMES à l'arrêt précoce ; l'opérateur a renvoyé le contenu de preuves-m5b TEL QUEL, comme le LISEZMOI l'exige.

**L'innocence du scellé (établie sur pièces).** La pièce proxy-journal.log (128 o) porte, DANS L'ORDRE DU CONTRAT http-12:R3 Q3 (bannière → armement → écoute) : « TRIADE M3 : proxy demarre (port 25000) », « relever-https arme », « commande inconnue » (voir ci-dessous), « connexion entrante »/« fin connexion » (la sonde TCP du scénario), « arret » ×2 (le quit post-REFUS a OPÉRÉ — thread console puis boucle d'acceptation, comportement identique au v8). Chronologie croisée : la sonde TCP réussit à 00:13:17 (« connect 127.0.0.1:25000 reussi ») donc l'ÉCOUTE était posée, donc — bannière et armement PRÉCÉDANT l'écoute (Q3) — les DEUX lignes étaient DÉJÀ ÉCRITES vingt secondes AVANT la lecture vide. L'autorité A : écoute 00:13:16, UNE poignée refusée SSLEOFError (= la sonde TCP 443 du scénario, connexion fermée avant poignée), 0 requête servie, « arret propre — motif=delai » à 00:15:46 (le délai 150 s, Entrée 137) — tout cohérent avec un run stoppé AVANT le navigateur. Décor v8 tenu (parefeu-vm.txt 828 o : trois profils ACTIFS, règles ALLOW TRIADE-M5B, notification d'écoute OFF — D142/D143). DIAG-EDGE-VERSION : ÉCHEC ADDITIF non bloquant (« le run continue ») — msedge.exe LOCALISÉ (Program Files (x86)) mais muet à --version en console ; à réparer en e3 par (Get-Item).VersionInfo.

**La cause racine (nommée) : la PREMIÈRE garde en live d'un fichier en cours d'écriture.** Faits : (a) tcp-11 écrit UNE WriteFile PAR LIGNE (contrat Q1 — aucun tampon applicatif), handle stdout posé par http-12:R3 avant la bannière ; (b) à 00:13:37 le fichier lu par le scénario fait 0 o ; (c) l'armement était écrit avant 00:13:17 (chronologie ci-dessus) ; (d) la pièce de 00:25:36 porte les 7 lignes COMPLÈTES, y compris les « arret » finaux — le contenu n'est apparu qu'APRÈS LA MORT du proxy. Conclusion : les lignes ÉTAIENT écrites, mais la LECTURE (PowerShell, dans la VM) d'un fichier du dossier C:\\preuves (mappé par le .wsb) dont le handle d'écriture est détenu par un processus VIVANT rend ZÉRO octet — le contenu ne devient lisible qu'à la fermeture du handle. C'est le MÊME SYMPTÔME que les « vues vides depuis la VM » consignées aux runs v7/v8 (réserves POIGNEE-B-REFUSEE : vues vides, producteur rc=0, pièces complètes jugées au labo post-mortem — D138). LA RÉGRESSION : le scénario v8 ne lisait le journal proxy qu'APRÈS le quit (verdicts post-mortem, 04:57:11 au v8) ; le scénario e2 a introduit la PREMIÈRE attente EN LIVE (« relever-https arme » sous 20 s, garde fail-closed précoce — Entrée 137, point 4) SANS la leçon D138. L'échec désigne le SCÉNARIO, pas le scellé. Le mécanisme intime (couche de redirection du dossier Sandbox ou autre) n'est pas tranché depuis le labo — le FAIT l'est, trois fois constaté (v7, v8, e2).

**« commande inconnue » : décor connu, pas un défaut du 0.6.0.** La ligne vit AUSSI au journal proxy du run v8 (VERDICT OK 0 réserve) à la MÊME place — 2e ligne après la bannière, avant la première connexion entrante : le phénomène accompagne le lancement cmd /c à stdin relayé depuis les runs de l'étape 1 ; il ne bloque rien (le quit opère après lui). Non élucidé depuis le labo ; consigné comme question ouverte additive (instrumenter le stdin au prochain run si le développeur le souhaite).

**La clôture D143 exécutée (scripts/archiver_run_e2.py, chaque mutation recoupée par relecture).** preuves-run-e2 (7 entrées : les 6 pièces + VERDICT-run-e2-vues-vides.txt, md5 recoupés) DANS archives-preuves ; preuves-m5b recréé VIERGE (LISEZMOI-preuves.txt e2 — la liste des pièces attendues e3 est la MÊME) ; l'index LISEZMOI-archives-preuves.txt mis à jour EN PLACE (section preuves-run-e2, date de tête 04/11) ; la racine /test INCHANGÉE (8 entrées D143) ; AUCUNE suppression, la corbeille n'est pas vidée. Honnêteté d'exécution : le premier passage du script s'est interrompu mi-chemin (upload_create exige un pathlib.Path — corrigé) ; le script est REPRISE-CAPABLE (chaque étape saute l'already-fait recoupé) et l'état final est recoupé par listing API.

**D145 (la règle nouvelle, insérée au DECISIONS.md dans le même geste).** AUCUNE garde de scénario ne dépend d'une lecture en live d'un fichier en cours d'écriture dans la VM : les gardes sont FONCTIONNELLES (port ouvert, réponse attendue) ou POST-MORTEM — D138 étendue aux gardes ; la preuve DECLARATIVE (une ligne de journal) ne GARDE rien, elle CONSTATE ; la preuve OPÉRATIVE (une réponse qui traverse la chaîne) GARDE.

**La correction proposée (vague e3 — le labo corrige sur pièces, modèle D104).** (1) LA GARDE D'ARMEMENT DEVIENT FONCTIONNELLE : le scénario envoie LUI-MÊME par TCP au mandataire la requête forme-absolue CLAIRE du navigateur (« GET http://127.0.0.1/ HTTP/1.1 » + Host: 127.0.0.1) et attend la page 200 de l'autorité A — relèvement http→https + tunnel + réponse = preuve OPÉRATIVE que le 0.6.0 est ARMÉ (un 0.5.1 — ou un rc.1 non armé — routerait vers l'origine port 80, muette : 502) ; REFUS PROXY-PAS-ARME nommé sinon ; la page reçue copiée en pièce page-sonde-armement.txt. (2) RELEVER-ARME DEVIENT UN VERDICT POST-MORTEM (la ligne au journal lu après le quit — modèle v8, plus AUCUNE lecture en live d'un fichier vivant). (3) DIAG-EDGE-VERSION réparé par (Get-Item msedge.exe).VersionInfo. (4) Le reste du décor e3 == e2 (drapeaux Edge, IP littérale D139, matrice curl, parefeu 0bis, témoin D99 en dernier acte). La construction et la livraison de la vague e3 attendent l'aval du développeur (c'est lui qui rejoue le run).

**Frontières.** Le scellé 0.6.0-rc.1 sha256 4b8f6af6… : AUCUN défaut constaté sur pièces (armé, écouté, arrêté proprement) ; l'artefact, la carte génération 7 et le sceau (onze arbres verts) INTACTS ; la finale 0.6.0 N'EST TOUJOURS PAS POSÉE (elle attend un run VERT — la carte ne ment pas) ; fixtures v5 inchangées ; aucune clé traversée ; aucune suppression Drive ; corbeille non vidée ; D139 demeure ouvert (T7 éventuel), non bloquant.

**Vérifiabilité.** archives-preuves/preuves-run-e2 (7 entrées, listing API recoupé) ; VERDICT-run-e2-vues-vides.txt (le diagnostic complet, miroir local upload/preuves-e2/) ; le journal proxy v8 (miroir local upload/preuves-run-v8/proxy-journal.log — la ligne « commande inconnue » au run VERT) ; scripts/rapatrier_preuves_e2.py + rapatrier_journal_v8.py + rapatrier_vagues_m5b.py (les pièces et la comparaison) ; scripts/archiver_run_e2.py (clôture rejouable, reprise-capable) ; ce commit (l'Entrée 138 + D145).

**SUITE.** Sur l'aval du développeur : construire et livrer la vague e3 (scénario à garde fonctionnelle + verdicts post-mortem, scripts/assembler_kit_e3.py et livrer_vague_e3.py sur les modèles e2) ; le run M5-b étape 2 REJOUÉ (le critère (b) de D136 : la page servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, la ligne de flux aux preuves) ; si vert : python3 m5/build_m5.py --sceller-final pose la finale 0.6.0 avec la validation consignée. D139 demeure ouvert, non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-137) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 138" in texte:
    sys.exit("ECHEC : l'Entrée 138 existe déjà")
i137 = texte.find("## Entrée 137")
im = texte.find(MARQUEUR)
if not (0 <= i137 < im):
    sys.exit("ECHEC : ordre inattendu (137/marqueur)")

# l'entrée ne doit contenir aucun marqueur de format parasite
if "\\n" in ENTREE:
    sys.exit("ECHEC : séquence parasite \\\\n dans l'entrée")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 137 < 138 < marqueur
j137 = nouveau.find("## Entrée 137")
j138 = nouveau.find("## Entrée 138")
jm = nouveau.find(MARQUEUR)
if not (0 <= j137 < j138 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 138 insérée ({len(ENTREE)} caractères) — ordre 137<138<marqueur recoupé")
