#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 290 + Task 197 : L'UNITÉ 2 LOUPE-02
LIRE CONSTRUITE AUX DEUX BRAS ET LIVRÉE AU /test (la suite commandée par le
développeur : « go pour la suite ») — le bras T (la notation de campagne au
slot i110002, la cristallisation, l'oracle 22 VERT), le bras C (le source
gcc -O2, le contrat rejoué 20 VERT, les contrôles binaires 18 VERT), les
DEUX kits gravés et livrés (24 pièces recoupées byte-byte), les écarts
nommés (les fautes en route, la remise à zéro du bac, les tokens manquants)."""
import pathlib

REPO = pathlib.Path("/home/z/my-project/work/triade")

WORKLOG = """

Task ID: 197
Agent: Z.ai (agent principal — la session de la construction et de la livraison de l'unité 2)
Task: LA SUITE COMMANDÉE (« vérifie les dépôts dans /test puis go pour la suite ») : LA DEUXIÈME TÂCHE CONTRÔLÉE du plan a78caf8c… — LOUPE-02 LIRE (la fenêtre d'octets au tampon de session, bornée par la taille réelle — la double borne — puis LE RECOUVREMENT du journal d'édition) — CONSTRUITE AUX DEUX BRAS, ÉPROUVÉE AU LABO ET LIVRÉE au /test (24 pièces recoupées byte-byte, les gravures 10/10 aux deux bras, la carte portée à jour).

Work Log:
- LE BAC RECONSTITUÉ (après la remise à zéro du conteneur, nommé) : keystone/capstone/pefile/unicorn/pynacl réinstallés ; le compilateur croisé gcc-mingw-w64 14.2 re-extrait des .deb SANS ROOT (travail/mingw-debs — les paquets du jour 14.2.0-19+27+b1 : l'original -19+27 a quitté le pool) ; LA VÉRIFICATION de l'outillage : la re-compilation du source du kit 01 rend 93 625 o à la gravure près (l'horodatage PE du lieur + la disposition des imports du binutils +b1 — NOMMÉ, la pièce 85b34ed4… demeure, D143) ; la NON-DÉTERMINABILITÉ du lieur nommée (deux builds ne sont jamais identiques — la cristallisation est la règle du bras T, pas du bras C).
- LE BRAS T — L'ORACLE ÉCRIT-AVANT-CODE (oracle-depuis-I.txt) : le modèle Python du contrat AVANT la notation (P1→P2→P3, la double borne, le recouvrement, les quatre verdicts, le fail-closed).
- LE BRAS T — LA NOTATION À LA MAIN (brouillons/loupe-02-lire.asm → notation/loupe-02-lire.asm, 292 o, 79 instructions, slot 0x4240/320) : TROIS FAUTES NOMMÉES EN ROUTE — ① l'adressage à deux bases (keystone refuse [r14 + rcx*16] : le pointeur qui marche), ② LE DÉBORDEMENT DU SLOT (325 o > 320 : compactée à 292 — le lu pré-contré car l'échec le lit après l'épreuve du retour, le min par cmovbe, la poignée tenue en r14, le zéro par registre, la chute par étiquette), ③ LA CHUTE DE BOUCLE (le recouvrement tombait dans l'échec système : le saut du succès rendu explicite).
- LE BRAS T — LE BUILD (build_unite02.py, le mécanisme de l'unité 1) : 18/18 notations round-trip R5, les 17 scellées aux mesures d'arrêt D161, 121 verrous (43 structurels + l'audit msx64 : 78 appels IAT), LE DIFFÉRENTIEL au scellé CONFINÉ au slot loupe-02 [0x3440, 0x3580) et à la porte R10 (11 plages, 284 o) ; LA CRISTALLISATION : DIX rebuilds consécutifs IDENTIQUES (sha256 98354ff6ac07cf29…) ; L'ORACLE DU BLOC : 22 VERT 0 ROUGE (le différentiel à 2 032 décalages sur les témoins + le proxy.exe scellé R7, le recouvrement aux bords et NON ALIGNÉ, le journal INTACT, les rejets au tampon empoisonné, l'échec ReadFile ARMÉ au Nième appel, la falsification détectable, l'intégration : loupe-01 scellé appelle la notation à chaque naissance).
- LE BRAS T — LE SCÉNARIO TERRAIN (scenario-unite02.py) + SON ÉPREUVE POSIX (epreuve_scenario_unite02.py : le juge extrait par AST, exécuté VERBATIM contre un contre-modèle indépendant — 2 000 cas VERT) : UNE FAUTE PRISE PAR L'ÉPREUVE AVANT LE RUN, nommée, corrigée (la frontière dupliquée à taille 16 : [0, 0] — la dernière valide sans garde d'unicité) ; le verrou de plage (LockFile d'un second détenteur) pour E4 au terrain, avec la sortie NOMMÉ ABSENT si le système de fichiers l'ignore.
- LE BRAS C — LE SOURCE (source/loupe-02-c.c) : loupe_02_lire NEUVE (le contrat en C : E1→E2→E3, la double borne, SetFilePointerEx FILE_BEGIN À CHAQUE lecture, ReadFile du remplissage exact, le lu RECOUPÉ au demandé — fail-closed, remplissage 0 à l'échec, le recouvrement borné à la fenêtre, la garde EDITS_MAX) + LE BLOC SESSION REPRIS TEL QUEL du kit 01 (l'écart nommé du bras C : la première fenêtre lue INLINE à l'ouverture, le loupe-01 du plan APPELLE loupe-02) + journal[4112] en DONNÉE exportée ; la compilation consignée : x86_64-w64-mingw32-gcc-posix -O2 -shared (95 413 o, 925cd019…).
- LE BRAS C — LES ÉPREUVES : LE CONTRAT ENTIER REJOUÉ AU POSIX 20 VERT 0 ROUGE (le harnais à shims du kit 01 avec DEUX écarts nommés : SetFilePointerEx déclarée À LA VALEUR — le vrai prototype, jamais éprouvée au kit 01 qui ne l'appelait pas ; le tiroir d'échec de ReadFile pour E4) — une faute du HARNAIS prise en route et nommée (l'ordre d'évaluation des arguments en C : le dump du vide lisait l'état d'avant — la capture AVANT le printf) ; LES CONTRÔLES BINAIRES 18 VERT 0 ROUGE (PE32+ DLL, les SIX exports — journal DONNÉE comprise —, les SIX feuilles kernel32 : SetFilePointerEx PRÉSENTE, l'écart nommé du kit 01 n'existe plus ; AUCUN appel CRT dans la clôture des trois fonctions ; les relocations) ; LE SCÉNARIO TERRAIN (scenario-unite02C.py, l'édition v2 du kit 01 : la découverte par exports, la traversée au CHAMP Name) ÉPROUVÉ CONTRE LA PIÈCE ELLE-MÊME (epreuve_parse_unite02C.py : l'image mappée par sections, les SIX exports et les SIX feuilles lus ; le juge par AST contre le contre-modèle, 2 000 cas VERT).
- M4 (journal_verifications.jsonl, 8 lignes versées) : build-recomposition 0,476 s ; oracle-du-bloc 33,856 s ; epreuve-scenario-posix 0,296 s ; build-gcc-O2 0,719 s ; epreuve-contrat-posix 0,228 s ; controles-binaires 0,041 s ; l'assemblage REFUSÉ une fois (code 2 — LA MESURE M4 elle-même avait recompilé la pièce, l'horodatage PE l'avait changée : la ligne DEMEURÉE, la dll canonique restaurée de la gravure, la reprise 0,252 s).
- M2 NOMMÉ MANQUANT : les appels de construction de cette session (spec/oracle/notation/correctifs/source-c/tests-c) ne sont passés par AUCUN journal d'usage API — les comptages de tokens de l'unité 2 sont MANQUANTS NOMMÉS (le plan § 4 : l'estimation ×1,08 ne s'applique qu'aux manques documentés — ils le sont ici ; le développeur peut les lire au tableau de bord de l'API).
- LA LIVRAISON (87) : les DEUX kits montés au /test — kit-unite-loupe-02-T-20261114/ (12 pièces : la pièce 98354ff6…, la notation, le brouillon, le scénario, le lanceur UTF-8, les QUATRE témoins == la gravure du kit 01 octet pour octet, la gravure, le LISEZMOI, le zip) et kit-unite-loupe-02-C-20261114/ (12 pièces : la pièce 925cd019…, le source et le .def, le scénario, le lanceur, les mêmes témoins, la gravure, le LISEZMOI, le zip) — 24 pièces recoupées par DOUBLE téléchargement byte-byte, les gravures relues du coffre 10/10 aux deux bras, la carte LISEZMOI-KITS-UNITES-D204.txt PORTÉE À JOUR (la ligne de l'unité 2) et re-téléchargée identique ; la racine porte 13 entrées.
- SUITE : au développeur — LE RUN DE L'UNITÉ 2 aux DEUX bras (le GUI : 1·KIT choisir kit-unite-loupe-02-T[-C]-20261114 → 2·RUN lancer → 3·TÉMOIN dater et signer de la main → renvoyer preuves-unite02[/C]/ ENTIER au /test ; onglets 4-7 : carnet, livraison, défauts, chrono) ; TOUJOURS ATTENDUE la ligne C de l'atelier (l'onglet 5, la 289) ; PUIS loupe-05 sha256, aux deux bras — le labo construit à la commande.
"""

JOURNAL = """

## Entrée 290 — L'UNITÉ 2 LOUPE-02 LIRE CONSTRUITE AUX DEUX BRAS, ÉPROUVÉE, LIVRÉE AU /test (la suite commandée : « go pour la suite »)

- LE BAC RECONSTITUÉ (la remise à zéro du conteneur, nommée) : les paquets réinstallés, le compilateur croisé re-extrait des .deb sans root (les 14.2.0-19+27+b1 du jour — l'original a quitté le pool) ; la vérification sur le source du kit 01 : 93 625 o à la gravure près (l'horodatage PE + la disposition des imports du binutils +b1 — NOMMÉ ; la pièce 85b34ed4… demeure, D143 ; la non-déterminabilité du lieur nommée — la cristallisation est la règle du bras T).

- LE BRAS T : l'oracle écrit-avant-code, puis LA NOTATION À LA MAIN — 292 o, 79 instructions au slot 0x4240/320 — avec TROIS fautes nommées en route (l'adressage à deux bases refusé par keystone ; LE DÉBORDEMENT DU SLOT 325 > 320, compactée par le cmovbe, le lu pré-contré, la poignée en registre, le zéro par registre ; LA CHUTE DE BOUCLE vers l'échec système) ; LE BUILD : 18/18 round-trip R5, 121 verrous, le différentiel au scellé CONFINÉ au slot loupe-02 et à la porte R10 ; LA CRISTALLISATION dix rebuilds identiques (98354ff6…) ; L'ORACLE DU BLOC 22 VERT 0 ROUGE — le différentiel à 2 032 décalages (les témoins + le proxy.exe scellé), le recouvrement aux bords et non aligné, le journal INTACT, les rejets au poison, l'échec ReadFile armé, la falsification détectable, ET L'INTÉGRATION : loupe-01 scellé appelle la notation à chaque naissance de session.

- LE SCÉNARIO T ET SON ÉPREUVE : le juge extrait par AST, exécuté VERBATIM contre un contre-modèle (2 000 cas VERT) — une frontière dupliquée prise AVANT le run, nommée, corrigée ; le vecteur E4 armé par un verrou de plage au terrain (la sortie NOMMÉ ABSENT si le système l'ignore).

- LE BRAS C : loupe_02_lire NEUVE (E1→E2→E3, la double borne, la position reposée à CHAQUE lecture, le lu recoupé au demandé — fail-closed, le recouvrement borné, la garde EDITS_MAX) + le bloc session REPRIS TEL QUEL du kit 01 (l'écart nommé : la première fenêtre INLINE) + journal en DONNÉE exportée ; la compilation consignée gcc -O2 croisée (95 413 o, 925cd019…) ; LE CONTRAT REJOUÉ AU POSIX 20 VERT 0 ROUGE (le harnais à shims — SetFilePointerEx déclarée À LA VALEUR : le vrai prototype, jamais éprouvée au kit 01 ; le tiroir d'échec ReadFile ; une faute d'ORDRE D'ÉVALUATION du harnais prise et nommée) ; LES CONTRÔLES BINAIRES 18 VERT 0 ROUGE (les SIX exports, SetFilePointerEx PRÉSENTE — l'écart nommé du kit 01 n'existe plus, AUCUN appel CRT dans la clôture) ; le scénario v2 ÉPROUVÉ CONTRE LA PIÈCE (l'image mappée par sections : les SIX exports et les SIX feuilles lus ; le juge par AST, 2 000 cas).

- M4 : 8 lignes au journal_verifications.jsonl (build 0,476 s ; oracle 33,856 s ; épreuves 0,296/0,228/0,041 s ; gcc 0,719 s ; l'assemblage refusé une fois — LA MESURE avait recompilé la pièce, l'horodatage PE l'avait changée, la ligne demeurée, la reprise 0,252 s). M2 NOMMÉ MANQUANT : les appels de construction de la session ne sont passés par aucun journal d'usage — les comptages de l'unité 2 sont des manques documentés (le développeur peut les lire au tableau de bord).

- LA LIVRAISON : les DEUX kits au /test — 24 pièces recoupées par double téléchargement byte-byte, les gravures 10/10 relues du coffre, la carte LISEZMOI-KITS-UNITES-D204.txt portée à jour et re-téléchargée identique ; la racine porte 13 entrées. (14/11, la session de la construction — l'unité 2 attend son run)

- SUITE : au développeur — LE RUN DE L'UNITÉ 2 aux deux bras (1·KIT → 2·RUN → 3·TÉMOIN signé de la main → preuves-unite02[/C]/ ENTIER au /test ; onglets 4-7) ; toujours attendue la ligne C de l'atelier (l'onglet 5) ; PUIS loupe-05 sha256.
"""

ITEM_17 = """
17. **L'UNITÉ 2 LOUPE-02 LIRE CONSTRUITE AUX DEUX BRAS ET LIVRÉE (Entrée 290)** : le bac reconstué après la remise à zéro (le compilateur croisé re-extrait, la vérification sur le source du kit 01 : la gravure près — l'horodatage PE nommé, la pièce 85b34ed4… demeure) ; LE BRAS T : l'oracle écrit-avant-code, la notation à la main 292 o (trois fautes nommées : l'adressage à deux bases, le débordement du slot 325 > 320, la chute de boucle), le build aux verrous 121 au différentiel confiné, la cristallisation dix rebuilds identiques (98354ff6…), l'oracle du bloc 22 VERT 0 ROUGE (2 032 décalages + le proxy.exe scellé, le recouvrement, les rejets au poison, l'échec armé, la falsification, l'intégration par loupe-01 scellé) ; LE BRAS C : loupe_02_lire neuve + le bloc session repris tel quel (l'écart nommé : la première fenêtre INLINE), gcc -O2 croisée (925cd019…), le contrat rejoué au POSIX 20 VERT 0 ROUGE, les contrôles binaires 18 VERT 0 ROUGE (SetFilePointerEx PRÉSENTE : l'écart du kit 01 n'existe plus), le scénario v2 éprouvé contre la pièce même ; M4 journalisée (8 lignes, l'assemblage refusé une fois par la mesure elle-même — nommé), M2 NommÉ MANQUANT (les appels de la session sans journal d'usage) ; LA LIVRAISON : les DEUX kits au /test, 24 pièces recoupées byte-byte, les gravures 10/10 ×2, la carte à jour ; LA SUITE : le run de l'unité 2 aux deux bras, la ligne C de l'atelier toujours attendue, puis loupe-05 sha256.
"""

with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(JOURNAL)

carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
txt = carte.read_text(encoding="utf-8")
txt = txt.replace("Entrées 251-289", "Entrées 251-290")
txt = txt.replace("Tasks 158-196", "Tasks 158-197")
if not txt.endswith("\n"):
    txt += "\n"
txt += ITEM_17
carte.write_text(txt, encoding="utf-8", newline="\n")
print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md + la carte OU-TROUVER — "
      "l'Entrée 290 + Task 197")
