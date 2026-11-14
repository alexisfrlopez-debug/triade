#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LA CONSIGNATION de l'Entrée 286 + Task 193 : LE REFUS DU BRAS C
REÇU — LA FAUTE AU LABO NOMMÉE (le terminateur lu à la chaîne, l'adresse du
plantage reproduite OCTET PAR OCTET), LA RÉPARATION LIVRÉE (le kit v2)."""
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/work/triade")
SCRIPTS = pathlib.Path("/home/z/my-project/scripts")
BAC = pathlib.Path("/home/z/my-project/download/preuves-refus-C-v1")

WORKLOG = """

Task ID: 193
Agent: Z.ai (agent principal — la session du refus du bras C et de sa réparation)
Task: LE PREMIER RUN DE L'UNITÉ 1 × BRAS C REVENU REFUSÉ (l'annonce au chat : la console du run — T0 VERT (la pièce loupe-01-c.dll 85b34ed4… recoupée à la gravure), l'image cartographiée @ 0x7ff9b74d0000, les QUATRE exports découverts — puis « access violation reading 0x00007FFA23900094 » à la traversée de la table d'imports, code 1, AUCUN vecteur, AUCUN témoin) : LA FAUTE AU LABO, NOMMÉE — le terminateur testé à la CHAÎNE du nom au lieu du CHAMP ; la pièce est SAINE.

Work Log:
- L'AUTOPSIE OCTET PAR OCTET (D122, au POSIX — l'image de la pièce mappée par sections, la boucle du scénario REJOUÉE) : au descripteur NUL, le champ Name vaut l'RVA 0 et lire_chaine(base, 0) lit L'EN-TÊTE DOS « MZ\\x90 » — jamais vide, la boucle ne s'y arrêtait pas ; elle dérivait à travers la table hint/nom de la pièce (25 itérations : « MZ », « InitializeCriticalSection », « VirtualProtect », « _initterm », « free », « vfprintf », « EnterCriticalSection », « ReadFile », « _unlock », « realloc »…) jusqu'à dereférer l'RVA bogué 0x6c430094 hors image : base 0x7ff9b74d0000 + 0x6c430094 = 0x7ffa23900094 — L'ADRESSE EXACTE de la console du développeur, reproduite au labo.
- L'ÉPREUVE QUI MANQUA, NOMMÉE AUSSI : le test_decouverte.py de l'Entrée 284 éprouvait SA PROPRE copie de la traversée (juste, elle, testait le champ Name) — jamais la boucle du scénario livré ; la leçon consignée : l'épreuve doit exécuter LE CODE LIVRÉ, pas sa copie.
- LA RÉPARATION (minimale : 20 lignes ajoutées, 2 retirées ; la pièce, le source C, le lanceur et les QUATRE témoins INTACTS octet pour octet) : le terminateur se lit au CHAMP Name (l'RVA NUL, AVANT toute lecture de chaîne) ; gardes fail-closed : au plus 64 descripteurs, aucun Name hors image — REFUS NOMMÉ « la pièce a divergé, rien ne court », jamais un plantage.
- LES ÉPREUVES DE LA RÉPARATION : la faute rejouée (les 25 itérations, l'adresse exacte) ; LA TRAVERSÉE DU SCÉNARIO v2 EXÉCUTÉE cette fois (le texte même du kit — les quatre lecteurs + la boucle gardée, extraits VERBATIM du fichier livré — couru contre l'image mappée : arrêt AU descripteur NUL @+0xa028, les deux descripteurs réels traversés (KERNEL32.dll, msvcrt.dll), les CINQ feuilles résolues, aucune garde vécue, RIEN lu hors image) ; LE CONTRAT ENTIER REJOUÉ 17 VERT 0 ROUGE (le juge hashlib) ; py_compile + l'audit AST.
- LA LIVRAISON : /test/kit-unite-loupe-01-C-20261114-v2/ — 12/12 pièces recoupées par re-téléchargement ET 12/12 au bac du miroir download/kit_unite_loupe_01_C_v2/ (24/24 VERT) ; le scénario v2 6340cd3c…, le LISEZMOI de l'écart et de la reprise 1ce0cf38…, la gravure REGRAVÉE 250d6534…, le zip ef5e3be5… ; les HUIT pièces intactes == la gravure v1 (85b34ed4…, 860ff1cf…, c0c9b9f4…, 29bdae2f…, df7e70e5…, 3396717b…, c5fc1f28…, e3b0c442…) ; le kit v1 DEMEURE au coffre (D143).
- LA PIÈCE DU REFUS : la console collée au chat consignée TELLE QUELLE au bac (download/preuves-refus-C-v1/run-console-unite01C-recu-chat.txt) — le fichier même (run-console-unite01C.txt, né du Tee du lanceur) attend SON DÉPÔT au /test par la main : la pièce d'un refus n'est jamais jetée.
- SUITE : au développeur — LA REPRISE au kit v2 (télécharger kit-unite-loupe-01-C-20261114-v2 du /test ; le GUI onglet 1·KIT choisir le dossier v2 → 2·RUN lancer LANCEUR-UNITE-01-C.bat → 3·TÉMOIN dater, signer de la main, renvoyer preuves-unite01C/ ENTIER au /test ; DÉPOSER AUSSI run-console-unite01C.txt, la console du refus v1) ; puis le labo recoupe et l'unité close (la deuxième des douze contrôlées).
"""

JOURNAL = """

## Entrée 286 — LE PREMIER RUN DE L'UNITÉ 1 × BRAS C REVENU REFUSÉ — LA FAUTE AU LABO NOMMÉE, L'ADRESSE DU PLANTAGE REPRODUITE OCTET PAR OCTET — LE KIT v2 LIVRÉ (l'annonce du développeur : la console du run au chat — T0 VERT, puis « access violation reading 0x00007FFA23900094 », code 1, AUCUN vecteur, AUCUN témoin)

- LA CONSOLE REÇUE (le chat est le canal, D189 — la pièce consignée TELLE QUELLE au bac download/preuves-refus-C-v1/run-console-unite01C-recu-chat.txt ; le fichier même, run-console-unite01C.txt né du Tee du lanceur, attend son dépôt au /test par la main) : T0 VERT — la pièce loupe-01-c.dll sha256 85b34ed4… == la gravure du kit, l'image cartographiée DONT_RESOLVE @ 0x7ff9b74d0000, les QUATRE exports découverts (loupe_01_ouvrir @+0x1e60, loupe_03_fermer @+0x2360, cadre 960 o @+0x8060, panneau 48 o @+0x8020) — LA PIÈCE EST SAINE ; puis l'exception au scénario ligne 214 (lire_chaine ← lire_u32(base, desc + 12)) : access violation reading 0x00007FFA23900094, le lanceur rend code 1, l'écho de fin vit, AUCUN vecteur, AUCUN témoin (le réceptacle preuves-unite01C/ n'était pas né).

- LA FAUTE AU LABO, NOMMÉE (jamais maquillée) : la boucle de résolution de la table d'imports testait le TERMINATEUR À LA CHAÎNE du nom (« si le nom est vide, arrête ») — mais au descripteur NUL le champ Name vaut l'RVA 0, et lire_chaine(base, 0) lit L'EN-TÊTE DOS « MZ\\x90 » : jamais vide, la boucle ne s'y arrêtait JAMAIS ; elle dérivait à travers la table hint/nom de la pièce (les 25 itérations rejouées au labo : « MZ », « InitializeCriticalSection », « VirtualProtect », « _initterm », « free », « vfprintf », « EnterCriticalSection », « ReadFile », « _unlock », « realloc »…) jusqu'à dereférer l'RVA bogué 0x6c430094 hors image : base 0x7ff9b74d0000 + 0x6c430094 = 0x7ffa23900094 — L'ADRESSE EXACTE DE LA CONSOLE DU DÉVELOPPEUR, reproduite au labo OCTET PAR OCTET (l'image de la pièce mappée par sections, la boucle du scénario rejouée pas à pas) ; L'ÉPREUVE QUI MANQUA, nommée aussi : le test_decouverte.py de l'Entrée 284 éprouvait SA PROPRE copie de la traversée (juste, elle, testait le champ) — jamais la boucle du scénario livré ; la leçon consignée : L'ÉPREUVE DOIT EXÉCUTER LE CODE LIVRÉ, PAS SA COPIE.

- LA RÉPARATION (minimale — 20 lignes ajoutées, 2 retirées au scénario seul ; la pièce loupe-01-c.dll, le source loupe-01-c.c, le lanceur et les QUATRE témoins INTACTS octet pour octet) : le terminateur se lit au CHAMP Name (l'RVA NUL, AVANT toute lecture de chaîne) ; gardes fail-closed : au plus 64 descripteurs, aucun champ Name hors image — REFUS NOMMÉ « la pièce a divergé, rien ne court », jamais un plantage.

- LES ÉPREUVES DE LA RÉPARATION (D122 — le labo n'a aucun Windows, la logique rejouée au POSIX) : LA FAUTE REJOUÉE contre les octets réels de la pièce (les 25 itérations, l'adresse du plantage EXACTE) ; LA TRAVERSÉE DU SCÉNARIO v2 EXÉCUTÉE cette fois — le texte même du kit (les quatre lecteurs + la boucle gardée, extraits VERBATIM du fichier livré) couru contre l'image de la pièce mappée par sections : ARRÊT AU DESCRIPTEUR NUL @+0xa028 (les deux descripteurs réels traversés : KERNEL32.dll, msvcrt.dll — jamais au-delà), les CINQ feuilles kernel32 résolues aux slots réels (SetFilePointerEx : l'écart nommé du bras C demeure), aucune garde vécue, RIEN lu hors image ; LE CONTRAT ENTIER REJOUÉ : 17 VERT 0 ROUGE (les quatre témoins champ à champ contre l'oracle hashlib — le juge indépendant, les rejets d'OS, la borne 2 Gio épars, la session double, le chemin trop long) ; py_compile + l'audit AST (la boucle gardée, sa clause else, le champ avant la chaîne).

- LE KIT v2 LIVRÉ : /test/kit-unite-loupe-01-C-20261114-v2/ — 12/12 pièces recoupées par re-téléchargement ET 12/12 au bac du miroir download/kit_unite_loupe_01_C_v2/ (24/24 VERT) ; les pièces neuves : le scénario RÉPARÉ 6340cd3c…, le LISEZMOI de l'écart et de la reprise 1ce0cf38…, la gravure REGRAVÉE du montage même 250d6534…, le zip ef5e3be5… ; les HUIT autres INTACTES == la gravure v1 octet pour octet (85b34ed4…, 860ff1cf…, c0c9b9f4…, 29bdae2f…, df7e70e5…, 3396717b…, c5fc1f28…, e3b0c442…) ; le kit v1 DEMEURE au coffre (D143 — la pièce n'est jamais jetée) ; l'écho du lanceur rend « preuves-unite01C<TAB>emoin… » : le « \\t » du chemin rendu TAB par la console — COSMÉTIQUE, nommé, le témoin vit bien à preuves-unite01C\\temoin-unite01C.txt.

- LA REPRISE (au développeur, tout au clic) : télécharger kit-unite-loupe-01-C-20261114-v2 du coffre /test ; le GUI onglet 1·KIT de l'unité loupe-01 × C → CHOISIR LE DOSSIER v2 (le GUI recoupe la gravure) ; onglet 2·RUN → LANCER LANCEUR-UNITE-01-C.bat (sa console officielle) ; onglet 3·TÉMOIN → DATER, SIGNER DE VOTRE MAIN (D99), renvoyer preuves-unite01C/ ENTIER au /test — ET DÉPOSER AUSSI run-console-unite01C.txt, la console du refus v1 (la pièce d'un refus n'est jamais jetée) ; onglets 4-7 (le carnet au geste, la livraison M1, les défauts nommés, le chrono M4) — la DEUXIÈME livraison de la campagne naîtra au geste, et l'unité loupe-01 × C pourra close à it1 (§ 7).

- LA CONSIGNATION : la présente Entrée 286 + Task 193 ; la carte OU-TROUVER portée à 286 ; D141 tenu avant le commit (le courant 285-478716c archivé versionné au miroir) ; le commit (l'atelier de la réparation : scripts/campagne_d204/unite-01-C/ — l'autopsie, le patch, les épreuves, le montage, la livraison) ; le push GitHub au jeton ghp_ du /tokens ; le miroir Drive synchronisé, chaque geste recoupé par re-téléchargement. (14/11, la session du refus du bras C — la pièce demeurait saine, la faute était au scénario du labo)
"""

ITEM_13 = """
13. **LE REFUS DU BRAS C REÇU — LA FAUTE AU LABO NOMMÉE, LE KIT v2 LIVRÉ (Entrée 286)** : la console du run (le chat, T0 VERT — la pièce 85b34ed4… recoupée, les QUATRE exports découverts — puis « access violation reading 0x7FFA23900094 », code 1, AUCUN vecteur) : le terminateur de la table d'imports testé à la CHAÎNE au lieu du CHAMP — à l'RVA 0 vit l'en-tête DOS « MZ », la boucle dérivait 25 itérations à travers la table hint/nom jusqu'à l'adresse EXACTE du plantage, reproduite au labo OCTET PAR OCTET ; l'épreuve de la 284 manqua la boucle livrée (elle éprouvait sa propre copie — nommé) ; LA RÉPARATION : le champ Name AVANT la chaîne, les gardes fail-closed (64 descripteurs, aucun Name hors image — REFUS nommé, jamais un plantage) ; LES ÉPREUVES : la traversée du scénario v2 EXÉCUTÉE VERBATIM contre l'image mappée (arrêt AU terminateur, les CINQ feuilles), le contrat entier REJOUÉ 17 VERT 0 ROUGE ; LE KIT v2 au /test/kit-unite-loupe-01-C-20261114-v2/ (12/12 + le bac 12/12, 24/24 recoupés ; les HUIT pièces intactes == la gravure v1, le v1 demeure D143) ; LA REPRISE : le kit v2 au GUI (1·KIT choisir → 2·RUN lancer → 3·TÉMOIN signé de la main → preuves-unite01C/ ENTIER au /test + DÉPOSER la console du refus) — la pièce d'un refus n'est jamais jetée.
"""

# ---- worklog + journal --------------------------------------------------------
with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(WORKLOG)
with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(JOURNAL)

# ---- la carte OU-TROUVER --------------------------------------------------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
txt = carte.read_text(encoding="utf-8")
txt = txt.replace("Entrées 251-285", "Entrées 251-286")
txt = txt.replace("Tasks 158-192", "Tasks 158-193")
if not txt.endswith("\n"):
    txt += "\n"
txt += ITEM_13
carte.write_text(txt, encoding="utf-8", newline="\n")

# ---- l'atelier de la réparation au dépôt ------------------------------------------
dest = REPO / "scripts" / "campagne_d204" / "unite-01-C"
for nom in ["70_autopsie_refus_C.py", "71_repare_scenario_C.py",
            "72_epreuve_reparation.py", "73_monte_kit_v2.py",
            "74_livre_kit_v2.py", "75_consigne_286.py",
            "76_sync_miroir_286.py"]:
    src = SCRIPTS / nom
    if src.exists():
        shutil.copy2(src, dest / nom)
        print(f"[atelier] {nom} versé au dépôt")
for extra, cible in [
        ("/home/z/my-project/work/kit_v2/DIFF-scenario-v1-v2.txt",
         "DIFF-scenario-v1-v2.txt"),
        ("/home/z/my-project/work/kit_v2/scenario-unite01C.py",
         "scenario-unite01C-v2.py"),
        ("/home/z/my-project/work/epreuve-C-v2/observe.txt",
         "epreuves/observe-v2.txt")]:
    p = pathlib.Path(extra)
    if p.exists():
        shutil.copy2(p, dest / cible)
        print(f"[atelier] {cible} versé au dépôt")

print("[consigné] worklog.md + docs/JOURNAL_TRAVAIL.md + la carte OU-TROUVER — l'Entrée 286 + Task 193")
