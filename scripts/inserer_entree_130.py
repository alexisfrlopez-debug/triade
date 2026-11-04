#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_130.py — JOURNAL_TRAVAIL.md : insère l'Entrée 130 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
129 < 130 < marqueur recoupé — le même contrat que les entrées 127-129)."""

import re
import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 130 — BUILD 0.6.0-dev.1 (03/11) : LE FLUX NAVIGATEUR EST EMBARQUÉ ET CÂBLÉ — les TROIS révisions R3 (http-08 cible à relever / http-10 routage Q2' + LIGNE DE FLUX / http-12 CLI --relever-https + PORTE M5) assemblées, harnaisées ET jugées ; proxy.exe 0.6.0-dev.1 construit (sha256 4b8f6af6…, entrée 0x8C80, SIX sections .text4, GetCommandLineW, version 0x00060000) ; l'oracle à scénarios ÉTENDU D136 écrit et VERT (365 cas) ; SIX écarts de câblage du builder nommés par l'oracle LUI-MÊME (fail-closed) et réparés ; cérémonie de signature en attente (D87)

**La reprise (le contexte était perdu, le dépôt a fait foi).** La session précédente s'était interrompue au milieu de l'implémentation D136 : les intentions (m5/I/README.md + les TROIS specs R3, écrites-avant-code), le plan (m5/layout.py), les notations finales (http-08:R3 377 o @0x8000, http-10:R3 2703 o @0x81C0 — 2e réarrêt D8, http-12:R3 779 o @0x8C80) et DEUX harnais (cible, session) étaient posés ; manquaient le TROISIÈME harnais (orchestrateur), l'ORACLE étendu et le passage du builder. Rien n'a été réécrit à l'aveugle : chaque pièce a été relue depuis le dépôt (spécifications, plan, notations, harnais M4, oracle M4) avant d'écrire la suite — l'héritage cites, jamais recopié (T5).

**Le harnais de l'orchestrateur (harnais_principal_r3.py — NOUVEAU, 800+ lignes).** V1 round-trip R3 + les DEUX ancêtres (R2 scellé 0.5.1 @0x7DC0, R1 scellé 0.4.0 @0x1800) ; V2 différentiel R2/R3 SANS argument : 14 scénarios, traces IDENTIQUES sauf LE CÂBLAGE (spawn 0x74C0 → 0x81C0) et l'appel GetCommandLineW (domaine nouveau, normalisé), divergence LÉGITIME nommée (.text4 corrompu : R2 nominal, R3 KO — miroir du domaine .text3 du harnais R2) ; V2bis LA CLI : 19 cas dirigés jugés par le modèle de PARSING écrit depuis la spécification (argument 0 sauté, comparaison byte-exact UTF-16 casse-sensible, séparateurs espace/tabulation, guillemets) — drapeau sain → politique armée + ligne « relever-https arme », TOUT autre argument → refus nommé ExitProcess 3 SANS initialisation, l'état .data compris (l'armement précède le refus) ; V3 fuzz des DEUX portes (400 mutations d'un point : champs héritage + porte M5 + octets gardés, ZÉRO passage silencieux) et de la CLI (300 lignes : quasi-drapeaux, drapeaux sains aux séparateurs et chemins variés, bruit) ; V4 falsification : ONZE mutations d'un point stables en taille TOUTES ATTRAPÉES (les deux contre-câblages 0x74C0/0x5580, la borne M5 ±0x10, le plancher abaissé, la ligne de politique amnésiée, la politique jamais armée, l'ordre d'initialisation, la politique armée SANS argument, l'argument inconnu accepté en silence, le code de sortie E4) + témoin vert. BILAN : 79 PASS, 0 ÉCHEC (graines 20261103 et 20261104).

**L'oracle à scénarios ÉTENDU (oracle_m5.py — NOUVEAU, le cœur D136).** executer(blobs, graine, volume) — le point d'entrée du builder. F1 RELEVÉE à volume (200 cas générés, politique armée) : le domaine http:// absolu (72 % routée — tunnel tls-08 par LE MÊME chemin Q2', port 443 FORCÉ E2, 28 % gardes et arrêts nommés — corps/TE → 501 et POST/PUT sans longueur → 411 LA LIGNE PORTE LE VERDICT NOMMÉ ; autorité vide → 400 et « HTTP:// » → 501 SANS ligne : le refus précède le routage), la ligne vérifiée OCTET PAR OCTET contre le MODÈLE DE COMPOSITION (ModeleRoutageR3 : la méthode PAR TABLE, l'hôte TRONQUÉ à 14, le port EFFECTIF, v = le verdict tls TRANSPORTÉ — la ligne nomme la cause, la réponse nomme l'effet —, e = accumulation + corps pompé, s = émissions .emettre, les relais délégués jamais comptés deux fois), la réponse exacte au client (page relayée, 502 ÉTIQUETÉE sur verdict 3), la compensation PAR COMPTAGE, le paquet P6/P7 au passage, ET la concordance avec la feuille (modele_cible, le 5e argument). F2 DOMAINES HÉRITÉS sous les DEUX politiques (150 cas) : Q7 à volume (politique 0 — l'ancêtre http-10:R2 scellé ÉMULÉ contre la révision, traces normalisées IDENTIQUES : R2 octet pour octet, aucune ligne) PUIS politique 1 (origine port 80, CONNECT le tunnel, https Q2' port explicite gagnant — les octets au client et la compensation sont ceux de l'ancêtre ÉMULÉ, la RÉFÉRENCE R7, le même arbitrage que l'oracle M3/M4 ; malformées et pair parti SANS ligne ; l'issue de la connexion amont est propriété du générateur, jamais dérivée des observations). F3 falsification : les TREIZE mutations du harnais ATTRAPÉES, le MODÈLE falsifié (ligne maquillée v=0 → v=1) NOMMÉ, témoin 14/14 vert. BILAN : 365 cas, 0 écart (graines 20261103 et 424242, empreintes distinctes).

**Le builder complété (build_m5.py) — SIX écarts de câblage nommés par l'oracle fail-closed, un par un, chacun réparé :** (1) les répertoires M4 absents du chemin d'import (carte_m4 introuvable) ; (2) la liste blanche RIP de http-10:R3 sans R_TAB_METHODES (I9 : la méthode PAR TABLE) ; (3) celle de http-12:R3 visant ENTREE_M5 au lieu de LA SESSION 0x81C0 (le contre-câblage serait indétectable) ; (4) la sentinelle -1 rendue 0xffffffffffffffff par capstone (les DEUX graphies admises) ; (5) les descripteurs d'imports hérités référencés au plan M4 au lieu du plan M3 qui les possède + l'en-tête PE (NumberOfSections 6, le SizeOfCode vestige du scellé restauré) ; (6) LA VERSION jamais écrite au-dessus de l'héritage (0x00060000) + la tranche .data absente du lecteur + la preuve R7 qui exclut désormais le delta version DOCUMENTÉ (le même arbitrage que la preuve M4 pour sa version). L'ordre d'import des oracles est consigné : build_m4 laisse sys.modules["layout"] = plan M4, les DEUX oracles et leurs harnais s'y lient AVANT que le plan M5 ne prenne le nom (liaison par objet module).

**Le build vert (chaîne complète re-vérifiée).** Sceau-I : 5 arbres d'intention conformes (m0-m4, clé réelle hors-ligne D87) ; héritage M3+M4 re-vérifié de bout en bout (524 + 492 verrous) ; l'image M4 composée == le scellé 0.5.1 OCTET POUR OCTET (sha256 fb41697d… — les runs v7/v8 PROUVENT ces octets) ; oracle structurel M5 : 312 verrous ; [PE] proxy.exe : 36 352 octets, 6 sections (.text4 0x8000-0x9FFF), kernel32 x10 + GetCommandLineW + ws2_32 x13 + secur32 x7, entrée 0x8C80 (http-12:R3), version 0x00060000, R_POLITIQUE à l'état image 0, la porte M5 (UNE entrée fail-closed, somme .text4 — la porte se garde elle-même) ET la porte R10 héritée (28 entrées) marchées ; [R7] 38 blocs octet-identiques au scellé 0.5.1, deltas .rdata/.text4/PE documentés ; oracle M4 (héritage rejoué) : 560 cas verts ; oracle M5 (D136) : 365 cas verts, falsification détectée ; --verifier re-validé. **proxy.exe 0.6.0-dev.1 : sha256 4b8f6af6caedb3e17811e6e25da1f1680068866bd1b417154fc54474170ec236.**

**La falsifiabilité constatée en passant (leçon D82 tenue).** Le harnais de session portait une arme creuse : la boucle Q7 de son V4 rejouait des scénarios ARMÉS à politique 0 (échec garanti par construction) — FILTRÉS (seuls les scénarios à politique 0 ont un attendu Q7 valide) ; le fuzz-CLI a produit UNE fois le drapeau EXACT comme « quasi-drapeau » (le retournement de casse tombé sur un trait d'union, qui n'a pas de casse — mutation sans effet) : l'assertion d'intention du harnais L'A ATTRAPÉE, le générateur ne vise plus que les LETTRES. Une suite qui ne peut pas échouer ne prouve rien : la sienne a échoué deux fois, pour de bonnes raisons.

**Frontières.** Arbres scellés intouchés ; 0.5.0 scellé D104 intact ; 0.5.1 fb41697d… REVÉRIFIÉ par la preuve R7 du build (l'image M4 composée == le scellé, octet pour octet) ; proxy.exe 0.6.0-dev.1 est un DEV (NON scellé — la carte génération 7 attend la cérémonie : « cérémonie requise, les secrets de la carte ne vivent pas au laboratoire », D87) ; aucune clé traversée ; aucun artefact scellé touché.

**Vérifiabilité.** `python3 m5/harnais_principal_r3.py` (79 PASS) ; `python3 m5/oracle_m5.py` (365 cas) ; `python3 m5/build_m5.py [--verifier] --graine 20261103` (chaîne verte, sha consigné) ; m5/proxy.exe (36 352 o).

**SUITE.** La cérémonie de signature par le développeur (D87 : clé hors-ligne, carte génération 7, conformité_profil à écrire), puis le kit VM ÉTAPE 2 (le navigateur du bac à sable, mandataire 127.0.0.1:25000, page http://autorite.test/ sous --relever-https) et le run M5-b étape 2 — le critère (b) de D136 : la page servie ET, sur la cible autonome, la 502 « Certificat rejete » reçue PAR LE NAVIGATEUR, la ligne de flux aux preuves. Le décor parefeu-muet v8 reste verrouillé. D139 demeure ouvert (T7 éventuel), non bloquant.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-129) ----------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 130" in texte:
    sys.exit("ECHEC : l'Entrée 130 existe déjà")
i129 = texte.find("## Entrée 129")
i130 = texte.find("## Entrée 130")
im = texte.find(MARQUEUR)
if not (0 <= i129 < im):
    sys.exit("ECHEC : ordre inattendu (129/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]
# ordre recoupé : 129 < 130 < marqueur
j129 = nouveau.find("## Entrée 129")
j130 = nouveau.find("## Entrée 130")
jm = nouveau.find(MARQUEUR)
if not (0 <= j129 < j130 < jm):
    sys.exit("ECHEC : ordre final non recoupé")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 130 insérée (ordre 129 < 130 < marqueur recoupé, "
      f"{len(ENTREE)} caractères)")
