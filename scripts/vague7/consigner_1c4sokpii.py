#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_1c4sokpii.py — LA CONSIGNATION de l'instruction 1c4sokpii
(append-only partout) : l'Entrée 373 au worklog, la carte OU-TROUVER portée."""
import pathlib
import re

REPO = pathlib.Path("/home/z/my-project/depot")

wl = REPO / "worklog.md"
wl.write_text(wl.read_text(encoding="utf-8") + """
---
Task ID: 234
Agent: Z.ai (agent principal — la session 1c4sokpii : le plan D210 à son terme, l'indépendance inter-familles — la vague 7 close)
Task: L'INSTRUCTION 1c4sokpii EXÉCUTÉE (la cinquième et dernière de la vague 7, à la suite de la synchronisation des trois bords) : (1) n≥6 TENU SANS nouveau tirage (N = 7 unités aux deux bras lues du registre), (2) l'indépendance inter-familles LE GAP NOMMÉ (le local open-weights Qwen2.5-Coder-1.5B vécu — les tables non régénérées 0/64 à la récitation pure, le bras C 1984/2011), (3) LE TRI DES 56 SURVIVANTS + LES SHIMS D'INJECTION + LE NOUVEAU TAUX 811/832 (97,5 %) + LE RESTE DE 21 NOMMÉ, (4) le paquet d'évaluation (la reproduction EN UNE COMMANDE, la grille codée, le second annotateur à recruter, κ autotesté) — l'étape de vérification VERTE.

Work Log:
- (1) LE PLAN À SON TERME : le comptage LU DU REGISTRE (29 livraisons) — SEPT unités aux deux bras (app, loupe-01/02/05/08/13/16), N = 7 ≥ 6 TENU ; la séquence QUATRE unités épuisée à la cap (l'Entrée 358), AUCUN nouveau tirage — l'amendement conditionnel JAMAIS DÉCLENCHE ; les runs terrain clos au geste du développeur.
- (2) L'INDÉPENDANCE INTER-FAMILLES : l'API du bac n'expose QU'UNE famille (le CLI z-ai sans option modèle) — LA VOIE PRESCRITE VÉCUE : Qwen2.5-Coder-1.5B-Instruct OPEN-WEIGHTS LOCAL (1,54 G paramètres, CPU, torch 2.15 — le plafond 3 Go de RAM barre le 7B) ; LA CONFRONTATION PRÉALABLE tenue (les définitions math T/K == le plan du harnais, la dérivée exacte aux décimales) ; R1 LA RÉCITATION PURE : T 0/64, K 0/64 — le modèle répète les ancres puis dérive ; les corrections copient (64/64 — JAMAIS l'indépendance) ; LE GAP NOMMÉ : la capacité du local disponible ; LE BRAS C : le contrat loupe-13 mot pour mot au prompt → gcc -O2 → l'épreuve POSIX (l'école, les rejets, la différentielle 2 000 cas graine 20261115) 1984/2011 — le bord Q2 (-5 au lieu de -1) LE SECOND GAP NOMMÉ ; jamais simulé.
- (3) LE TRI ET L'INJECTION : le rejeu reproduit la console v0.14.0 À L'IDENTIQUE (776/832, la graine 20261111) ; les 56 triés AU NIVEAU INSTRUCTION (46 immédiats, 8 registres, 2 opérandes) ; LA BATTERIE K4 DE SEIZE SCÉNARIOS (l'ouverture manquée/verrouillée/refusée, ALLER vide/bornes/hexa/SUPPR/ÉCHAP, CHERCHER jusqu'à la FIN -1 [le compte d'occurrences LU DU FICHIER], le journal PLEIN des 256 DISTINCTS + le non-hexa, la ligne INCOMPLÈTE au fond, les touches aux bornes, la poignée AU MOT DE POIDS FORT, LES FAUTES PAR BLOC aux conventions des épreuves [sans session -4, hors fichier -3, sortie nulle -5, LE SHIM ReadFile EN ÉCHEC -6, la chaîne CHERCHER à poser_saisie, L'ÉTAT PROPRE à chaque appel — les verdicts eax au bloc, la barre portant le nom jamais le nombre]) ; LE NOUVEAU TAUX : 811/832 (97,5 %) — 35 tués PAR L'INJECTION (83,4 % → 93,3 % → 97,5 %) ; LE RESTE NOMMÉ : 21 survivants à TREIZE familles de causes (6 l'état mourant, 3 le shim aveugle, 2 le suivi de vue, et le code 3 jamais servi, RBP volatil, le sentinel adjacent, le site hors table, la poignée jamais servie, le champ au-delà du motif, la voie de l'échec jamais servie, la convergence des gardes, le chemin du recadrage, la cible détournée retombe) — AUCUN tueur affaibli.
- (4) LE PAQUET D'ÉVALUATION : les métadonnées Zenodo v0.19.4 PUBLIÉES (la Task 232) ; LA REPRODUCTION EN UNE COMMANDE (reproduire_1c4sokpii.sh — sept étapes aux graines consignées : la réconciliation, le linter v194 16/16, le triage, la batterie 811/832, le κ 3/3, l'épreuve POSIX 1984/2011, les empreintes 5/5 — VERT DE BOUT EN BOUT) ; LA GRILLE CODÉE (les 11 défauts du registre en F1×1/F2×1/F3×3/F5×3/L3×3, chaque classe du mécanisme consigné — l'annotateur 1 sur pièces) ; LE SECOND ANNOTATEUR À RECRUTER (le protocole écrit, l'acceptation κ ≥ 0,61 pré-enregistrée, AUCUNE annotation inventée) ; le calculateur κ autotesté 3/3.
- L'ÉTAPE DE VÉRIFICATION (la lettre de l'instruction) : la réconciliation re-jouée zéro divergence ; le linter re-roulé 16/16 ; le rejeu aux MÊMES graines (jamais un tirage nouveau) ; le κ aux cas synthétiques calculables à la main ; l'indépendance LE GAP NOMMÉ (jamais simulé) ; le plan pré-enregistré JAMAIS re-tiré ; les artefacts scellés INTACTS (la batterie écrit aux émulations, les pièces loupe.exe/proxy.exe jamais touchées) ; le présent diff consigné append-only.
- LA LIVRAISON : l'atelier atelier-plan-final-1c4sokpii/ au dépôt (les scripts, les CSV, les rapports, le source C de la seconde famille, les états bruts) ; le RAPPORT-1C4SOKPII.txt ; l'instruction archivée après exécution à /ARCHIVE/instructions_20261119/ (la règle du développeur) ; LA VAGUE 7 CLOSE (les cinq instructions exécutées).
  (20/11/2026, la session 1c4sokpii — le plan tenu sans un tirage, l'indépendance nommée sur pièces, l'injection tuant 35 survivants, le reste de 21 à sa cause : la vague 7 close, aucun contrôle retiré)
""", encoding="utf-8")
print("[Entrée 373] le worklog porté")

carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
t = carte.read_text(encoding="utf-8")
t = re.sub(r"\*Mise à jour : [^*]+\*", "*Mise à jour : 20/11/2026 (Entrée 373 — L'INSTRUCTION "
           "1c4sokpii EXÉCUTÉE, LA VAGUE 7 CLOSE : [1] n≥6 TENU SANS nouveau tirage "
           "[N = 7 unités aux deux bras lues du registre : app, loupe-01/02/05/08/13/16 ; "
           "la séquence épuisée à la cap, l'Entrée 358, l'amendement conditionnel jamais "
           "déclenché] ; [2] L'INDÉPENDANCE INTER-FAMILLES LE GAP NOMMÉ [le local "
           "open-weights Qwen2.5-Coder-1.5B vécu — l'API n'expose qu'une famille ; la "
           "confrontation math↔plan tenue ; la récitation pure 0/64+0/64 — la capacité du "
           "local, jamais simulé ; le bras C 1984/2011, le bord Q2 nommé] ; [3] LE TRI "
           "DES 56 + LES SHIMS D'INJECTION + LE NOUVEAU TAUX 811/832 [97,5 % — 35 tués "
           "par la batterie de fautes : l'ouverture manquée/verrouillée/refusée, ALLER "
           "vide/bornes/hexa, CHERCHER à la FIN, le journal plein, la ligne incomplète, "
           "les fautes par bloc au shim ReadFile en échec, l'état propre à chaque appel ; "
           "LE RESTE DE 21 NOMMÉ à treize familles de causes] ; [4] LE PAQUET "
           "D'ÉVALUATION [la reproduction EN UNE COMMANDE verte de bout en bout, la "
           "grille codée F1/F2/F3/F5/L3 des 11 défauts, le second annotateur à recruter "
           "— le protocole écrit, κ autotesté 3/3, les métadonnées Zenodo v0.19.4 "
           "vivantes] ; l'atelier au dépôt, l'instruction archivée ; la vague 7 CLOSE)*",
           t, count=1)
carte.write_text(t, encoding="utf-8")
print("[carte] l'en-tête porté à l'Entrée 373")
