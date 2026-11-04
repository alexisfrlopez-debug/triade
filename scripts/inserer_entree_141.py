#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_141.py — JOURNAL_TRAVAIL.md : insère l'Entrée 141 PAR
SCRIPT AVANT le marqueur m5a (insertion ASSERTÉE : marqueur unique, ordre
140 < 141 < marqueur recoupé — le même contrat que les entrées 127-140)."""

import sys

CHEMIN = "docs/JOURNAL_TRAVAIL.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 141 — RUN e3 ANALYSÉ SUR PIÈCES ET REPRODUIT AU LABO : ÉCHEC NOMMÉ CRASH DU PROXY 0.6.0-rc.1 — LE RVA NU DE LA LIGNE DE FLUX (http-10:R3, code NOUVEAU M5) ; l'étiquette REFUS PROXY-PAS-ARME est démentie par la pièce (« relever-https arme » y vit) ; les oracles étaient verts parce que TOUTE l'émulation vit à base 0 — règle D146 ; clôture D143 du run, chemin de réparation proposé (décision du développeur)

**Le constat sur pièces (7 pièces + LISEZMOI, 8/8 md5 conformes, run 09:30:55–09:33:29Z, VM 9687CE78).** Le scénario e3 s'arrête à la garde d'armement : la sonde forme-absolue « GET http://127.0.0.1/ HTTP/1.1 » reçoit RIEN (0 octet, MethodInvocationException LA MÊME SECONDE que sa connexion — pas un délai, une mort immédiate). L'étiquette du refus est FAUSSE cette fois : le journal proxy PORTE « relever-https arme » — LE PROXY ÉTAIT ARMÉ. La signature complète désigne la MORT DU PROCESSUS en traitant la requête : le journal s'arrête à la seconde « connexion entrante » (pas de « fin connexion », pas de ligne de flux, pas de « tunnel chiffre etabli »), le quit post-REFUS n'a pas opéré (pas d'« arret » — au run e2 le même quit avait opéré : le pipe était mort), l'autorité A n'a JAMAIS été contactée (0 requête servie, l'unique poignée refusée = la sonde TCP 443 du scénario, bénigne v7/v8), et Tuer n'a pas journalisé (le processus avait déjà rendu l'âme). C'était la PREMIÈRE requête routée jamais envoyée au binaire : e2 n'en avait envoyé aucune (sa garde lisait des fichiers), v8 tournait sur le 0.5.1. DIAG-EDGE-VERSION PASS (156.0.4314.58 par VersionInfo — la pièce edge-version.txt 176 o vit aux preuves, la pièce nouvelle e3 EST née) ; D139 inchangée (« Hôte inconnu », non bloquant, IP littérale).

**La reproduction au labo (scripts/reproduire_run_e3.py — harnais full-PE unicorn, modèle emulation_forensique D52h).** Le scellé 4b8f6af6… (LU, jamais écrit) émulé ENTIER : base préférée 0x140000000, IAT remplie par la marche des 4 descripteurs, ligne de commande réelle (cmd /c mange les redirections), fils coopératifs (console tcp-06 + sessions par accept), LA SÉQUENCE EXACTE du terrain (sonde TCP fermée, puis la sonde d'armement 51 o). RÉSULTAT : le journal capté reproduit le journal réel LIGNE POUR LIGNE jusqu'à la mort, puis FAUTE MÉMOIRE à http-10:R3 @0x81C0+0xA46 : « movzx eax, byte ptr [r12] » avec r12 = 0x24A0 — lecture HORS IMAGE (l'image vit à 0x140000000) : violation d'accès, le processus meurt, RST au client. IDENTIQUE AU TERRAIN.

**La cause racine.** La table des méthodes (R_TAB_METHODES @0x2410, héritage .rdata M4 ; chaînes à R_METHODES @0x24A0 « GET\\0HEAD\\0POST\\0… ») stocke des couples (RVA, longueur) — premier DWORD = RVA 32 BITS, contrat du lecteur hérité http-02:R1 @0x4D82-0x84 : « mov edx, dword [rax] ; add rdx, r12 » avec r12 = base d'image. La révision R3 de la session — LA LIGNE DE FLUX, code ENTIÈREMENT NOUVEAU 0.6.0 (le binaire 0.5.1 ne contient PAS la chaîne « flux », le run v8 n'en a jamais écrit) — lit l'entrée par « mov rdx, qword [r11] » (notation http-10-session-r3.asm lignes 186-194, désassemblage 0x84E8-0x850B) et passe le RVA NU comme pointeur source à .copier : L'AJOUT DE LA BASE A ÉTÉ PERDU. La ligne de flux est écrite pour TOUTE requête routée : TOUTE requête routée TUE le rc.1 — le navigateur du critère (b) ne serait jamais servi.

**Pourquoi les oracles étaient verts : la base d'émulation 0.** TOUT le corpus d'émulation M5 mappe l'image À BASE 0 (harnais session : ZONE_RDATA 0x2000, ZONE_TEXT4 0x8000 ; oracle F1 : les 200 cas du domaine relevé, la ligne jugée octet par octet ; harnais principal : image 0x1000-0xB000). À base 0 le RVA nu EST une adresse mappée : le code fautif y « fonctionne » PAR ACCIDENT. La base réelle n'a jamais été émulée ; la conformité § 8.2 lit le PE sans l'exécuter. Ce n'est pas une lacune des contrôles À LEUR MODÈLE : c'est un angle mort du modèle — règle D146.

**La preuve chirurgicale (le harnais, mode --corrige).** Le correctif simulé AU CROCHET de l'appel .copier (rdx = 0x140000000 + rdx, EXACTEMENT l'idiome hérité restauré — le reste est code réel du scellé) fait disparaître le crash et la chaîne REPART ENTIÈRE : la ligne de flux NAÎT (« flux GET 127.0.0.1:443 v=6 e=51 s=40 » — la méthode lue dans la table, le PORT 443 FORCÉ PAR LE RELÈVEMENT E2, e=51 = les octets de la requête ; v=6 = l'issue de secours du labo, sans vrai Schannel — l'issue terrain attendue est v=0 avec la page 200), puis getaddrinfo("127.0.0.1"), connect vers 443, et une réponse ENVOYÉE AU CLIENT (502 du stub au labo ; au terrain : la page 200 par le tunnel, chemin prouvé par l'oracle F1 et la pièce page-a.txt du v8). La pièce page-sonde-armement.txt aurait porté CES octets-là si le binaire n'était pas mort.

**La clôture D143 (scripts/archiver_run_e3.py, modèle archiver_run_e2.py, chaque mutation RECOUPÉE PAR RELECTURE).** Les 7 pièces DÉPLACÉES vers archives-preuves/preuves-run-e3/, rejointes par VERDICT-run-e3-rva-nu.txt (le diagnostic complet, miroir local upload/preuves-e3/) ; preuves-m5b recréé VIERGE (LISEZMOI-preuves.txt e3 — la liste vaut pour e4 : LE SCÉNARIO e3 EST REPRIS TEL QUEL, il est sain) ; index LISEZMOI-archives-preuves.txt mis à jour EN PLACE ; état final recoupé : archives-preuves = 11 entrées, racine /test inchangée (8 entrées, la vague e3 attend le kit e4), AUCUNE suppression, corbeille non vidée.

**Frontières.** Le scellé 0.6.0-rc.1 (4b8f6af6…) INTACT octet pour octet (lu en émulation, jamais écrit — le harnais n'écrit que sa propre mémoire) ; carte génération 7 et sceau ONZE arbres INTACTS ; le scellé 0.5.1 et les cartes m0-m4 INTACTS ; fixtures v5 inchangées (empreintes consignées par le run) ; m5/I INTACT (aucune intention ne bouge) ; le scénario e3 et le kit e3 au coffre INTACTS (la garde fail-closed D145 a fait SON travail : attraper AVANT le navigateur — seule l'ÉTIQUETTE du refus est inexacte) ; .keys/ absent ; aucune suppression Drive ; D139 ouverte non bloquante ; la finale 0.6.0 TOUJOURS NON POSÉE (elle attend un run VERT — la carte ne ment pas).

**Vérifiabilité.** python3 scripts/rapatrier_run_e3.py (8/8 md5) ; python3 scripts/reproduire_run_e3.py (le crash reproduit) puis --corrige (la chaîne renaît) ; python3 scripts/archiver_run_e3.py (rejeu = déjà fait, idempotent) ; archives-preuves/preuves-run-e3 (listing API) ; VERDICT-run-e3-rva-nu.txt (toute allégation y est citée sur pièce).

**SUITE (proposition — décision du développeur).** Le scellé ne se reconstruit pas (anti-rollback R6 : nouvelle version requise) : (1) corriger la notation http-10-session-r3 (restaurer l'idiome dword + base de http-02) — l'arbre d'INTENTION m5/I ne change pas, LE SCEAU-I m5 RESTE VALIDE, aucune nouvelle cérémonie ; (2) adjoindre au corpus le CONTRÔLE D'EXÉCUTION À LA BASE RÉELLE (règle D146 — le contrôle qui aurait attrapé le défaut avant scellage) ; (3) rebuild → oracles → conformité → 0.6.0-rc.2 → scellage rc (secrets au coffre, D144) ; (4) kit e4 (scénario e3 repris, étiquette de refus affinée) → GESTE TERRAIN → critère (b) de D136 ; si vert : --sceller-final pose la finale.
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

# -- assertions d'insertion (le contrat des entrées 127-140) ------------------
if texte.count(MARQUEUR) != 1:
    sys.exit(f"ECHEC : marqueur m5a présent {texte.count(MARQUEUR)} fois (1 attendu)")
if "## Entrée 141" in texte:
    sys.exit("ECHEC : l'Entrée 141 existe déjà")
i140 = texte.find("## Entrée 140")
im = texte.find(MARQUEUR)
if not (0 <= i140 < im):
    sys.exit("ECHEC : ordre inattendu (140/marqueur)")

nouveau = texte[:im] + ENTREE + "\n" + texte[im:]

# ordre recoupé : 140 < 141 < marqueur
j140 = nouveau.find("## Entrée 140")
j141 = nouveau.find("## Entrée 141")
jm = nouveau.find(MARQUEUR)
if not (0 <= j140 < j141 < jm):
    sys.exit("ECHEC : ordre final inattendu")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"Entrée 141 insérée ({len(ENTREE)} caractères) — ordre 140<141<marqueur recoupé")
