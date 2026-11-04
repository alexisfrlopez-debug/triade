#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d154.py — DECISIONS.md : insère D154 PAR SCRIPT À LA SUITE de
D153 (insertion ASSERTÉE : D153 présente une fois, D154 absente, D154
ajoutée APRÈS D153 — fin du fichier, modèle inserer_d153.py)."""

import sys

CHEMIN = "docs/DECISIONS.md"

DECISION = """

## D154 — LE TERRAIN D'UN KIT FAIT PARTIE DE SON CONTRAT (hors terrain : mort nommée AVANT tout geste — jamais un faux vert d'environnement, jamais une « portabilité » qui tuerait la preuve) ; LE VERDICT DU LABO SUR UN RUN TERRAIN SE REND SUR PIÈCES CROISÉES (témoin ↔ journal ↔ verdict recoupés ENTRE EUX, l'arithmétique RECOMPTÉE, les constats vérifiés CONTRE LA SOURCE, le noyau CONSTATÉ distinct, l'artefact RECALCULÉ au geste même) ; L'INSTRUMENT DE RECOUP EST LUI-MÊME SOUPÇONNABLE (un ÉCHEC NOMMÉ du recoup s'instruit comme défaut d'instrument AVANT d'être un défaut de pièces — corrigé sur pièces, rejoué, les pièces immuables)

**Le constat qui fonde la décision (05/11, run M6-(d) + scellage final 0.7.0, Entrée 149).** Quatre constats du geste fondent la règle : (1) LE PREMIER GESTE DU DÉVELOPPEUR A MORT NOMMÉE HORS TERRAIN — le kit lancé sous Windows natif (`c:\\m6-kit> python scenario-m6d.py`) est mort à l'ouverture de `libc.so.6`, AVANT T0, avant toute pièce, avant tout geste sur l'artefact : le fail-closed du kit tient MÊME HORS DE SON TERRAIN (un environnement faux ne produit ni faux vert ni preuves partielles), et la correction est LE TERRAIN NOMMÉ (WSL2, la recommandation D149 suivie), jamais une « portabilité » du scénario — sous Windows il n'y a ni ELF, ni mprotect, ni refus EACCES à constater : la preuve du (d) EST le noyau Linux qui parle ; (2) LE RUN VERT SUR UN NOYAU AUTRE — 6.18.54.1-microsoft-standard-WSL2 (la machine du développeur) contre 5.10.134… (le labo), l'ASLR complet constaté (randomize_va_space=2), le scellé relu dd14195c… avant tout geste : la vigilance D146 satisfaite PAR LE TÉMOIN, pas par la parole ; (3) LE RECOUP SUR PIÈCES CROISÉES — vingt-deux contrôles : les pièces recoupées entre elles (le témoin embarqué au journal == le fichier témoin ; les 16 constats du verdict == les 16 PASS du journal LIGNE POUR LIGNE ; la date du verdict == la date du témoin), l'arithmétique RECOMPTÉE (800 + 400 == 1 200 ; 778 + 560 == 1 338 ; indices 0..1337 exacts ; octets émis == attendus), les noms des constats vérifiés CONTRE LA SOURCE du scénario (le juge est le code), le sha du scellé RECALCULÉ au geste même depuis l'artefact du dépôt ; (4) LE PREMIER RECOUP A ÉCHOUÉ NOMMÉ — « C4 : divergence au rang 0 » : le défaut était DANS L'INSTRUMENT DU RECOUP (la comparaison des préfixes avait ses arguments inversés : l'attendu testé startswith du constat lu, au lieu du constat lu startswith de l'attendu) — la lignée D151/D152 (« l'instrument mentait, pas le code ») s'étend au RECOUP lui-même : l'instrument est corrigé sur pièces et REJOUÉ, les pièces n'ont pas bougé d'un octet ; le second passage : VERT 22/22.

**La règle.** (1) UN KIT TERRAIN DÉCLARE SON TERRAIN (le LISEZMOI le nomme, l'exigence fait partie du contrat du kit) : hors terrain, la mort est NOMMÉE avant tout geste — le kit ne se « porte » JAMAIS à un environnement qui ne porte pas sa preuve ; une demande de portage d'un kit hors de son terrain est une demande à instruire (un refus nommé, un kit sibling), jamais une correction du kit prouvé. (2) LE VERDICT DU LABO SUR UN RUN TERRAIN SE REND SUR PIÈCES CROISÉES, JAMAIS SUR CONSOLE : présence et md5 des pièces contre le coffre ; cohérence croisée témoin ↔ journal ↔ verdict ; RECOMPTE arithmétique de chaque compteur ; noms des constats contre la SOURCE du scénario ; noyau du témoin CONSTATÉ distinct de celui du labo ; empreinte de l'artefact RECALCULÉE au geste même. Le scellage final n'est exécuté qu'après ce recoup VERT : la porte est de PROCESSUS (le code exige déjà D146 + cristallisation + conformité — D147/D152 ; ce que seul le terrain produit, seul le recoup l'établit). (3) L'INSTRUMENT DE RECOUP EST LUI-MÊME FAILLIBLE ET DOIT L'AVOUER : un ÉCHEC NOMMÉ du recoup s'instruit comme défaut d'INSTRUMENT avant d'être un défaut de pièces (la correction se fait dans l'instrument, le rejeu le prouve, les pièces demeurent immuables — md5 contrôlés de part et d'autre) ; le recoup ÉCRIT son verdict à côté des pièces (VERDICT-recoup-*.txt — la pièce née du juge). (4) La balise finale est SCELLÉE sur le recoup vert, au terme de la MÊME chaîne que le rc — jamais sur la seule parole du run : le terrain juge, le labo recoupe, le code scelle.

**Alternatives rejetées.** Sceller sur le copier-coller console du développeur (rejeté : D145/D148 — le verdict est post-mortem SUR PIÈCES, la console n'est pas une pièce) ; rendre le scénario portable Windows (rejeté : le kit déclare son terrain — la preuve du (d) est le noyau Linux qui refuse EACCES, un shim la tuerait) ; exiger le même noyau que le labo (rejeté : l'exigence est l'AUTRE noyau — D146, la leçon du rc.1 : un vert sur le noyau du labo ne prouve pas le terrain) ; tolérer un écart de compte dans les pièces (rejeté : chaque compte se RECOMPTE — un vert approximatif est un faux vert) ; réécrire ou « nettoyer » les pièces pour les faire passer le recoup (rejeté : les pièces sont immuables, md5 contrôlés ; c'est l'instrument qui se corrige et se rejoue) ; instruire l'échec du recoup comme un échec du run sans rejeu (rejeté : l'instrument mentait, pas les pièces — le rejeu l'établit sur pièces).

**Frontières.** La règle régit les kits terrain (leur terrain déclaré), les runs développeur (leurs pièces) et le recoup labo (son instrument et son verdict) ; elle ne touche NI l'artefact scellé (INTACT — sha dd14195c…, le scellage est un fait de carte), NI le scénario déposé au coffre (le scénario éprouvé demeure, le terrain le rejoue tel quel), NI la chaîne de scellage (D147/D152 demeurent : le code exige D146 + cristallisation + conformité AVANT la bascule — la présente ajoute la porte de processus : le recoup vert PRÉCÈDE l'appel à --sceller-final), NI le PDF formel (byte-identique — l'état des jalons vit aux sources de travail, addendum Task 62). La finale 0.7.0 est SCELLÉE sur le run m6d recoupé VERT (Entrée 149) : LE JALON M6 FRANCHI, le jalon M7 ouvert (D149).
"""

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

if "\\n" in DECISION:
    sys.exit("ECHEC : séquence parasite backslash-n dans la décision")
if "## D154" in texte:
    sys.exit("ECHEC : D154 existe déjà")
if texte.count("## D153 —") != 1:
    sys.exit(f"ECHEC : D153 présente {texte.count('## D153 —')} fois (1 attendue)")

nouveau = texte.rstrip("\n") + "\n" + DECISION

if not (nouveau.find("## D153 —") < nouveau.find("## D154")):
    sys.exit("ECHEC : ordre final inattendu (D153 < D154)")

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(nouveau)
print(f"D154 insérée ({len(DECISION)} caractères) — à la suite de D153, ordre recoupé")
