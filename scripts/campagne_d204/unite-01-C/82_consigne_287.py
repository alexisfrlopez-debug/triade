#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 287 + Task 194 : LE RUN DE L'UNITÉ 1 ×
BRAS C REVENU VERT, RECOUPÉ — LA DEUXIÈME UNITÉ CLOSE À IT1 (§ 7) : LOUPE-01
EST MESURÉE AUX DEUX BRAS, LA PREMIÈRE PAIRE APPARIÉE EST NÉE."""
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/work/triade")
SCRIPTS = pathlib.Path("/home/z/my-project/scripts")

WORKLOG = """

Task ID: 194
Agent: Z.ai (agent principal — la session du run vert du bras C, le recoup et la clôture de l'unité)
Task: LE TÉMOIN DU BRAS C REÇU AU COFFRE (l'annonce du développeur : « preuves-unite01C\\ dans le drive /test » — preuves-unite01C/ né le 14/11 12:57:07Z, temoin-unite01C.txt 1 334 o) : LE RUN DE L'UNITÉ 1 × BRAS C REVENU VERT, RECOUPÉ — LA DEUXIÈME UNITÉ CLOSE À IT1.

Work Log:
- LE RECOUP (19 VERT 0 ROUGE, le rapport au bac download/preuves-unite01C/RECOUP-287.txt et à l'atelier) : le témoin RAPATRIÉ puis RE-TÉLÉCHARGÉ, IDENTIQUES byte-byte (sha256 4cc0ee2b…, md5 2e14e1ec… == le champ du coffre) ; la pièce loupe-01-c.dll 93 625 o sha256 85b34ed4… == LA GRAVURE DU KIT v2 re-téléchargée et re-hachée == la gravure v1 == l'empreinte que porte le témoin (la pièce n'a jamais bougé) ; le scénario réparé du kit v2 re-haché 6340cd3c…, la gravure même 250d6534… ; LE VERDICT : 15 VERT, 0 ROUGE (T0, V1×8, V2×3, V3×3) — les QUINZE noms de vecteurs OCTET POUR OCTET ceux du témoin T ET les appels du scénario v2 livré ; la machine : LA MÊME LIGNE EXACTE que le témoin T (PORTABLE · Windows 10 · AMD64 · Python 3.14.10 — la constante du terrain, CA2) ; D99 TENU : daté 14/11/2026 de la main, signé Alexis Lopez.
- LA CHAÎNE : la chronologie sans trou — le kit v2 né 12:43:48Z au coffre → le run 12:55:25Z → le témoin touché 12:56:09Z (la main qui date et signe) → déposé 12:57:07Z ; LE V1 NE PEUT PAS ÉCRIRE UN TÉMOIN (re-vérifié aux octets réels de la pièce : « 4d 5a 90 00 » — la chaîne à l'RVA 0 vit TROIS caractères avant le premier NUL, jamais vide ; l'autopsie 286 : 25 itérations de dérive jusqu'à 0x7ffa23900094) — le témoin ne peut naître que de la traverse réparée ; le témoin signé de la main demeure LA PIÈCE du verdict (le même appui que la fermeture T — sa console verte ne fut jamais une condition).
- LA CLÔTURE (§ 7) : la DEUXIÈME livraison de la campagne — C-loupe-01-it1, VERT, RECOUPÉ VERT PAR LE LABO (le refus v1 ne consomme PAS d'itération : la pièce ne fut jamais mesurée, la faute était au scénario du labo nommée à 286 — le précédent 283/284) ; l'arrêt au premier vert recoupé : L'UNITÉ LOUPE-01 × C FERMÉE À IT1, LA DEUXIÈME UNITÉ CLOSE de la partie contrôlée (deux sur douze) ; LOUPE-01 EST LA PREMIÈRE TÂCHE MESURÉE AUX DEUX BRAS — la première paire appariée de la comparaison des workflows EST NÉE ; l'analyse demeure INTERDITE en cours de route (CA7).
- LES PIÈCES ENCORE ATTENDUES (l'écart nommé) : run-console-unite01C.txt — la console du refus v1, demandée à 286, attend SON DÉPÔT au /test (le contenu vit déjà au bac download/preuves-refus-C-v1/) ; les onglets 4-7 du GUI de l'unité C (le carnet M3, la ligne livraisons.csv, les défauts, le chrono M4) — l'atelier au coffre ne porte encore que la ligne T, l'atelier de l'unité C attend son retour.
- SUITE : au développeur — LOUPE-01 EST FINIE aux deux bras, RIEN à refaire ; les deux dépôts qui restent à la main (la console du refus, l'atelier de l'unité C) ; la campagne continue À LA COMMANDE du développeur — la prochaine unité du plan : LOUPE-02 LIRE, aux deux bras.
"""

JOURNAL = """

## Entrée 287 — LE RUN DE L'UNITÉ 1 × BRAS C REVENU VERT, RECOUPÉ — LA DEUXIÈME UNITÉ CLOSE À IT1 (§ 7) : LOUPE-01 EST MESURÉE AUX DEUX BRAS, LA PREMIÈRE PAIRE APPARIÉE DE LA CAMPAGNE EST NÉE (l'annonce du développeur : « preuves-unite01C\\ dans le drive /test »)

- LE TÉMOIN REÇU ET RECOUPÉ (octet pour octet — 19 contrôles VERT 0 ROUGE, le rapport au bac download/preuves-unite01C/RECOUP-287.txt et à l'atelier du dépôt) : preuves-unite01C/ au coffre /test (né le 14/11 12:57:07Z) — temoin-unite01C.txt 1 334 o, RAPATRIÉ puis RE-TÉLÉCHARGÉ : IDENTIQUES byte-byte (md5 2e14e1ec… == le champ du coffre, sha256 4cc0ee2b…) ; le témoin porte : le run 2026-11-14T12:55:25Z, la machine PORTABLE · Windows 10 · AMD64 · Python 3.14.10 — LA MÊME LIGNE EXACTE que le témoin du bras T (la constante du terrain, CA2), la pièce loupe-01-c.dll 93 625 o sha256 85b34ed4… == LA GRAVURE DU KIT v2 (re-téléchargée et re-hachée par le labo) == la gravure v1 == l'empreinte que porte le témoin — la pièce n'a jamais bougé (D143) ; LE VERDICT : 15 VERT, 0 ROUGE — VERT (T0, V1×8, V2×3, V3×3), les QUINZE noms de vecteurs OCTET POUR OCTET ceux du témoin T ET la liste attendue dérivée du source du scénario v2 livré ; D99 TENU : daté 14/11/2026 de la main, signé Alexis Lopez.

- LA CHAÎNE RECOUPÉE (le kit v2, la seule traverse qui peut écrire un témoin) : le kit v2 au coffre né 12:43:48Z — DOUZE minutes avant le run ; ses pièces re-hachées : la DLL 85b34ed4…, le scénario RÉPARÉ 6340cd3c…, la gravure même 250d6534…, le bac du miroir identique ; LE SCÉNARIO v1 NE PEUT PAS ÉCRIRE UN TÉMOIN — re-vérifié ce jour aux octets réels de la pièce : « 4d 5a 90 00 », la chaîne à l'RVA 0 vit TROIS caractères avant le premier NUL, JAMAIS vide (l'autopsie 286 : la boucle dérivait 25 itérations jusqu'à l'access violation 0x7ffa23900094, reproduite au labo OCTET PAR OCTET) ; la chronologie entière, sans trou : le kit v2 livré 12:43:48 → le run 12:55:25 → le témoin touché 12:56:09 (la main qui date et signe) → déposé 12:57:07 ; le témoin signé de la main (D99) demeure LA PIÈCE du verdict — le même appui que la fermeture du bras T (sa console verte, elle non plus, ne fut jamais une condition).

- LA LIVRAISON ET L'ARRÊT (§ 7 du plan) : la DEUXIÈME livraison de la campagne — C-loupe-01-it1, VERT, RECOUPÉ VERT PAR LE LABO (le refus v1 ne consomme PAS d'itération : la pièce ne fut jamais mesurée — AUCUN vecteur, AUCUN témoin, la faute était au scénario du labo nommée à l'Entrée 286 ; le précédent 283/284 du bras T) ; l'arrêt au premier vert recoupé : L'UNITÉ LOUPE-01 × C FERMÉE À IT1 — LA DEUXIÈME UNITÉ CLOSE de la partie contrôlée (deux sur douze) ; LOUPE-01 EST LA PREMIÈRE TÂCHE MESURÉE AUX DEUX BRAS (T it1 VERT, run 14/11 08:56:40Z ; C it1 VERT, run 14/11 12:55:25Z) — LA PREMIÈRE PAIRE APPARIÉE DE LA COMPARAISON DES WORKFLOWS EST NÉE ; l'analyse demeure INTERDITE en cours de route (CA7 — les agrégats n'iront qu'aux deux bras complets de la partie contrôlée, le journal brut demeure la seule vue courante).

- LES PIÈCES ENCORE ATTENDUES (l'écart nommé, jamais maquillé) : run-console-unite01C.txt — LA CONSOLE DU REFUS v1, demandée à l'Entrée 286, attend SON DÉPÔT au /test par la main (son contenu est déjà consigné TEL QUEL au bac download/preuves-refus-C-v1/run-console-unite01C-recu-chat.txt — la pièce d'un refus n'est jamais jetée, le dépôt reste le geste) ; LES ONGLETS 4-7 DU GUI de l'unité C — le carnet M3 au geste, la ligne livraisons.csv « C-loupe-01-it1 », les défauts nommés, le chrono M4 : l'atelier au coffre ne porte encore QUE la ligne T (sa dernière synchro s'arrête au 14/11 09:04Z) — l'atelier de l'unité C attend son retour au coffre, la ligne C naîtra au geste du développeur.

- LA REPRISE (au développeur) : LOUPE-01 EST FINIE aux deux bras — RIEN à refaire ; les deux dépôts qui restent à la main : (1) run-console-unite01C.txt au /test (la console du refus v1), (2) l'atelier de l'unité C rendu au coffre (les onglets 4-7 : le carnet, la livraison, les défauts, le chrono) ; LA CAMPAGNE CONTINUE À LA COMMANDE du développeur — la prochaine unité contrôlée du plan (§ 3) : LOUPE-02 LIRE, le même mécanisme de kit aux deux bras, la même question — ce que coûte et ce que protège chaque workflow.

- LA CONSIGNATION : la présente Entrée 287 + Task 194 ; la carte OU-TROUVER portée à 287 ; D141 tenu avant le commit (le courant 286-db5b02f archivé versionné au miroir) ; le commit (l'atelier du recoup : scripts/campagne_d204/unite-01-C/ — les sondes 77-80, le recoup 81, la consigne, la synchronisation — et le rapport d'épreuves) ; le push GitHub au jeton ghp_ du /tokens ; le miroir Drive synchronisé, chaque geste recoupé par re-téléchargement. (14/11, la session du run vert du bras C — la première paire appariée est née)
"""

ITEM_14 = """
14. **LE RUN VERT DU BRAS C RECOUPÉ — LA DEUXIÈME UNITÉ CLOSE À IT1 : LOUPE-01 MESURÉE AUX DEUX BRAS, LA PREMIÈRE PAIRE APPARIÉE (Entrée 287)** : preuves-unite01C/ au /test (né 12:57:07Z) — temoin-unite01C.txt recoupé 19 VERT 0 ROUGE : le run 12:55:25Z, la MÊME machine que le bras T (CA2), la pièce 85b34ed4… == la gravure v2 == la gravure v1 == l'empreinte du témoin, 15 VERT 0 ROUGE (les QUINZE noms octet pour octet ceux du témoin T et du scénario v2), daté 14/11/2026 et signé Alexis Lopez (D99) ; la chaîne : le kit v2 né 12:43:48 → le run 12:55:25 → la main 12:56:09 → le dépôt 12:57:07, aucun trou ; le v1 NE PEUT PAS écrire un témoin (l'Entrée 286, re-vérifiée aux octets réels) ; C-loupe-01-it1 VERT RECOUPÉ — l'unité loupe-01 × C FERMÉE À IT1 (§ 7 : le premier vert recoupé), la DEUXIÈME des douze contrôlées ; LOUPE-01 : LA PREMIÈRE TÂCHE MESURÉE AUX DEUX BRAS — l'analyse interdite en cours de route (CA7) ; ENCORE ATTENDUS : run-console-unite01C.txt au /test (la console du refus v1) et l'atelier de l'unité C (onglets 4-7 : carnet, livraison, défauts, chrono) ; LA SUITE à la commande du développeur : LOUPE-02 LIRE, aux deux bras.
"""

# ---- worklog + journal --------------------------------------------------------
with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(JOURNAL)

# ---- la carte OU-TROUVER --------------------------------------------------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
txt = carte.read_text(encoding="utf-8")
txt = txt.replace("Entrées 251-286", "Entrées 251-287")
txt = txt.replace("Tasks 158-193", "Tasks 158-194")
if not txt.endswith("\n"):
    txt += "\n"
txt += ITEM_14
carte.write_text(txt, encoding="utf-8", newline="\n")

# ---- l'atelier du recoup au dépôt ------------------------------------------
dest = REPO / "scripts" / "campagne_d204" / "unite-01-C"
for nom in ["77_sonde_preuves_unite01C.py", "78_rapatrie_temoin_C.py",
            "79_sonde_racine_kit_v2.py", "80_sonde_nouveau_run.py",
            "81_recoup_temoin_C.py", "82_consigne_287.py",
            "83_sync_miroir_287.py"]:
    src = SCRIPTS / nom
    if src.exists():
        shutil.copy2(src, dest / nom)
        print(f"[atelier] {nom} versé au dépôt")
# les rapports de sondes
for extra, cible in [
        ("/home/z/my-project/scripts/70_arborescence_preuves_unite01C.txt",
         "epreuves/sondage-preuves-unite01C.txt"),
        ("/home/z/my-project/scripts/72_racine_test_et_kit_v2.txt",
         "epreuves/sondage-racine-test-kit-v2.txt"),
        ("/home/z/my-project/scripts/73_nouveau_run.txt",
         "epreuves/sondage-nouveau-run.txt")]:
    p = pathlib.Path(extra)
    if p.exists():
        shutil.copy2(p, dest / cible)
        print(f"[atelier] {cible} versé au dépôt")

print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md + la carte OU-TROUVER — l'Entrée 287 + Task 194")
