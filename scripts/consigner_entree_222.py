#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE CONSIGNATION DE LA SESSION 222 — le douzième run recoupé, la balise
`loupe 0.1.1` SCELLÉE. Quatre gestes, chacun asserté :
  1. JOURNAL_TRAVAIL.md — l'Entrée 222 insérée AVANT le premier marqueur
     m5a:journal-des-builds (la règle du marqueur) ;
  2. DECISIONS.md — D181 appendée (l'ordre séquentiel des D) ;
  3. worklog.md — Task ID 129 appendé ;
  4. PLAN_MILESTONES.md — l'État du programme + la rangée (e) étendue.
"""

import pathlib

REPO = pathlib.Path("/home/z/my-project/triade")

ENTREE_222 = """## Entrée 222 — LE DOUZIÈME RUN RECOUPÉ 39/39 ET LA BALISE `loupe 0.1.1` SCELLÉE : LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE (11/11)

**Le fait (le geste du développeur).** Le message « dossier /kit-loupe avec les preuves déposé dans le dossier /test du drive » annonce LE DOUZIÈME RUN vécu : le kit 0.1.1-dev.1 (loupe-kit-13, LA VERSION COMMANDÉE D179) couru chez l'utilisateur, la vitrine vue par son témoin, les preuves au coffre. La suite annoncée de l'Entrée 221 s'accomplit : le labo rapatrie, recoupe, cristallise, scelle.

**LE RAPATRIEMENT (rapatrier_run_011_dev1.py).** LES SEPT PIÈCES du dossier du run kit-loupe/ rapatriées par ID vers upload/run-011-dev1/ (zone d'entrée terrain, jamais commitée), md5 recoupés à l'arrivée : les QUATRE pièces du kit == l'Entrée 221 (loupe.exe md5 5fc07b78… / sha256 c111510535767a40…, scenario 77872b71…, bat 2a3f22f4…, LISEZMOI 70340163…), temoin-fichier.bin == loupe.exe (LA SAUVEGARDE A EU LIEU — la copie que la seconde fenêtre ouvrit), ET LES DEUX TÉMOINS nés du run (temoin-loupe.txt 46db2210…, temoin-vitrine.txt d83ae8cb…).

**LE RECOUP (recouper_run12_011.py — le juge est le code, D138/D145/D148).** TRENTE-NEUF TRANCHES SUR PIÈCES CROISÉES, **39/39 VERT** : [A] les sept pièces contre le dépôt et le coffre (le kit loupe-kit-13/ INTACT, kit-loupe.zip == la vague dadfb48c…) ; [B] le témoin relu — **T0→T7 TOUT VERT POUR LA CINQUIÈME FOIS** (l'empreinte ASSERTÉE c1115105…, LE QWORD VERSION 0x00010101 LU SUR LA PIÈCE — l'ère 0.1.1 vécue au terrain, l'IAT 37 feuilles, la session sur l'ombre, LE PANNEAU, les lignes, la recherche == bytes.find, la boucle d'édition, les quatre rejets, la clôture INCHANGÉE), **S0 LA CASCADE 205 VÉCUE ENTIÈRE POUR LA DEUXIÈME FOIS** (P0 VERTE · P1 REFUSÉ 193/0xc000007b · P2 VERTE · P3 VERTE · P4 REFUSÉ — les axes nommés) ; [C] le témoin vitrine — **LA VITRINE VIVANTE LA TROISIÈME FOIS** ([1/4] 0 · [2/4] 0 · [3/4] aucun WER · [4/4] les trois vieux watchdog 1001, aucun neuf) — LA PREMIÈRE DE LA PIÈCE 0.1.1 ; [D] le labo parle — **LA DOCTRINE [SONDE-EXE] TENUE** (D178 : la ligne sonde-214 renvoyée telle quelle, le COFF relu Characteristics 0x0002 le bit DLL ABSENT, la doc LoadLibraryExA citée, la liaison PROUVÉE PAR LE VIVANT trois runs) ET **LE RÉSIDU DU PORT NOMMÉ [T0-PÉRIMÉ]** : le bandeau « la carte, génération 16, à régénérer au labo » du témoin est LE TEXTE DE L'ÈRE dev.12 (la dette était réelle alors, l'Entrée 211), périmé deux fois à l'ère 0.1.1 (soldée à l'Entrée 218, la carte génération 17 écrite à la naissance — D179) ; le bandeau version « 0.1.0-dev.257 » est le RENDU DYNAMIQUE du qword (VERSION_TXT = 0x00010101 & 0xFFFF = 257 — l'Entrée 213) — AUCUNE PORTE TOUCHÉE (les gates EMPREINTE-DIVERGENTE et PORTE-R10 exactes : l'asserté c1115105…, le qword 0x00010101), le résidu COSMÉTIQUE consigné, jamais un refus (les pièces du run immuables, D154) ; [E] LE VERDICT : **LE VERT TIENT ENTIER — LA BALISE `loupe 0.1.1` DÉBLOQUÉE SUR LE DOUZIÈME RUN RECOUPÉ**, la condition de l'Entrée 221 satisfaite — VERDICT-run-loupe-011-dev1.txt (md5 e553ac8c…) + les DEUX témoins → download/preuves-run-loupe-011-dev1/ (le modèle M9 : la pièce est du dépôt).

**LA CRISTALLISATION (D178 règle 2 : les passes se jouent au scellage).** Les compteurs partis à 2/10 (l'Entrée 221) — LES HUIT PASSES : chaque passe re-vérifie la recomposition == la pièce déployée (PLUS AUCUN écart — la dette [R10-PÉRIMÉE] n'existe pas à cette ère : « porte-r10=véridique » au journal de la carte), rejoue LES TROIS HARNAIS (61/61 · 53/53 · 45/45), incrémente les compteurs, re-signe la carte (la graine durable D144) : **26 BLOCS À 10/10, 0 incomplet** — la 10/10 exigée à la porte.

**LE SCELLAGE (build_loupe.py --sceller-final — LE MIROIR D165/D170, les portes adaptées au verdict du douzième run).** LES PORTES TRANCHÉES AVANT L'ÉCRITURE : le garde sceau I 14/14 ; LE VERDICT EXIGÉ COMME PIÈCE (VERDICT_RECOUP_011 → download/preuves-run-loupe-011-dev1/ : les CINQ PORTES assertées — le vert, le recoup 39/39, la condition, l'empreinte c1115105…, la vitrine LA TROISIÈME FOIS) ; la cristallisation 26 × 10/10 ; le verrou croisé 26 empreintes, l'artefact 0.1.1-dev.1 INTACT == LA PIÈCE DU DOUZIÈME RUN ; LA BASCULE version=0.1.1-dev.1 → 0.1.1 dans frag-bld (occurrence unique, vérifiée EN MÉMOIRE), les fragments re-chiffrés, L'ENTÊTE BALISE (version=0.1.1, génération 17, la racine re-dérivée 1f25afae…), la signature Ed25519 re-signée (la graine durable D144 : LE TÉMOIN NE BOUGE PAS), le tableau de bord « loupe 0.1.1 SCELLÉE sur le douzième run vert recoupé », le verrou croisé post-scellage 26 ; **L'ANTI-ROLLBACK ARMÉ — CONSTATÉ AU GESTE MÊME** (la reconstruction REFUSÉE) ; loupe.exe INTACT (c111510535767a40…, 127 488 o — le scellage est un fait de carte) : **LA BALISE `loupe 0.1.1` SCELLÉE — LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE** (D181).

**LE COFFRE (depot_entree_222.py).** LE RUN 12 ARCHIVÉ → archives-preuves/preuves-run-loupe-011-dev1/ [VERDICT e553ac8c… + temoin-loupe.txt 46db2210… + temoin-vitrine.txt d83ae8cb… — recoupés après dépôt, sans doublon] ; LE DOSSIER DU RUN kit-loupe/ recoupé pièce à pièce (les QUATRE == loupe-kit-13/, temoin-fichier.bin == loupe.exe) puis CORBEILLÉ (D99) ; LA RACINE DEMEURE À LA VAGUE DU SCELLEMENT [kit-loupe.zip dadfb48c… + LISEZMOI-loupe.txt 70340163… + loupe-kit-13/ — recoupés ; vagues-m10/ COMPLÈTE dev.1 → dev.12 + 0.1.1-dev.1] ; LE RÉCEPTACLE preuves-loupe/ RÉ-ARMÉ À L'ÈRE SCELLÉE [LISEZMOI-preuves.txt fd6deab4… — plus aucune pièce attendue, les captures bienvenues, un défaut éventuel → la 0.1.2+ commandée, jamais un hot-fix] ; LES DEUX INDEX reversés (livraisons + preuves) ; la racine 27 entrées, AUCUN doublon.

**Détail.** FRONTIÈRES : la balise `loupe 0.1.0` SCELLÉE DEMEURE (054de960… — l'anti-rollback vivant, la monotonie R10 n'ouvre jamais l'ancienne) ; les balises sœurs INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0) ; les notations D172-D175 INTACTES (R2 — la table R10 est un geste de BUILD) ; les secrets au seul .keys/ (D12) ; la clé privée jamais traversée (D87). L'ère 0.1.1 ouverte et refermée le même jour (11/11) : la version de maintenance à contrat stable (R4/R10) — DOUZE RUNS TERRAIN au total, l'application née de TRIADE vivante chez son utilisateur. Consignations : D181 PAR SCRIPT, la présente Entrée, le PLAN (l'État + la rangée (e)), worklog +Task ID 129. SUITE : au développeur — l'ère 0.1.1 scellée, M10 demeure franchi depuis la 0.1.0 ; les options du programme d'après M10 demeurent (le projet fils COFFRE-FORT dégélé D171, les chantiers nommés au § 1.10 de la v0.9.0).


"""

D181 = """
## D181 — LA BALISE `loupe 0.1.1` SCELLÉE SUR LE DOUZIÈME RUN VERT RECOUPÉ : LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE (le miroir D165/D170/D178 porté à l'ère 0.1.1 : le scellage REFUSE en l'absence du verdict du recoup vert — la porte est de PROCESSUS, jamais de console ; LA PIÈCE VIT AU DÉPÔT — le verdict du douzième run à download/preuves-run-loupe-011-dev1/, recoupé par md5 : la cérémonie est re-expérimentable d'un clone frais) ; LE RUN DU SCELLEMENT DE LA DETTE (T0→T7 TOUT VERT POUR LA CINQUIÈME FOIS, LA CASCADE 205 VÉCUE ENTIÈRE POUR LA DEUXIÈME, LA VITRINE VIVANTE LA TROISIÈME FOIS [0 ET 0 — LA PREMIÈRE DE LA PIÈCE 0.1.1, aucun WER], le recoup 39/39 — LE VERT TIENT ENTIER) ; LA DOCTRINE [SONDE-EXE] TENUE ET LE RÉSIDU DU PORT NOMMÉ [T0-PÉRIMÉ] (le bandeau « génération 16, à régénérer au labo » du scénario porté — texte d'ère dev.12, AUCUNE porte touchée : les gates exactes, les pièces du run immuables D154) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la cristallisation 26 × 10/10 exigée au geste — les huit passes depuis les compteurs 2/10 de D179, la recomposition == la pièce à chaque passe : PLUS AUCUN écart ; la bascule version=0.1.1-dev.1 → 0.1.1 dans frag-bld, occurrence unique vérifiée en mémoire ; l'entête balise version=0.1.1 génération 17 ; la re-signature à la graine durable D144 : LE TÉMOIN NE BOUGE PAS ; loupe.exe INTACT c1115105… — LE MÊME binaire que LE DOUZIÈME RUN a couru) ; L'ANTI-ROLLBACK ARMÉ (la reconstruction REFUSÉE, constaté au geste même ; la 0.1.0 scellée DEMEURE — la monotonie R10 ouvre l'ère suivante, jamais elle ne referme l'ancienne : (0,1,1,−1,1) < (0,1,1,0,0) refuse toute pré-version de la 0.1.1)

**Le contexte qui fonde la décision (11/11).** La version 0.1.1 fut commandée le 11/11 (D179 : la dette [R10-PÉRIMÉE] soldée à la naissance), le douzième run couru sur le champ, les preuves déposées au coffre — la boucle COMMANDÉ → NÉE → VÉCUE → RECOUPÉE → SCELLÉE bouclée en un jour : la version de maintenance à contrat stable (R4/R10), l'ère ouverte et refermée le même jour.

**Les règles.** (1) **La finale se scelle sur pièces, jamais sur console** : le --sceller-final EXIGE le verdict du recoup terrain VERT (39/39 + les cinq portes assertées : le vert, le recoup, la condition, l'empreinte, la vitrine) — D138/D145/D148/D154 étendues au geste final, le miroir de D165/D170/D178 à l'ère 0.1.1. (2) **Le scellage est un fait de carte** : la balise 0.1.1 vit dans frag-bld (occurrence unique, bascule vérifiée en mémoire), l'entête la porte, loupe.exe INTACT — le binaire que le terrain a couru EST le binaire final. (3) **L'anti-rollback arme l'ère refermée** : la carte scellée (0.1.1) interdit la reconstruction (R6) — constaté au geste même ; la re-vérification sous la balise scellée demeure licite (R5/R7). (4) **La clôture accompagne le scellage** : le run archivé AVEC son jugement (preuves-run-loupe-011-dev1/ au coffre ET au dépôt), le dossier du run corbeillé après recoup pièce à pièce (D99), le réceptacle ré-armé à l'ère scellée, le kit du scellement demeuré au coffre (loupe-kit-13). (5) **Aucune règle du cœur n'est modifiée** — la décision constate un scellage, elle ne légifère pas.

**Frontières.** La balise `loupe 0.1.0` SCELLÉE DEMEURE (054de960…) ; les balises sœurs INTACTES ; les notations D172–D175 INTACTES (R2) ; les secrets au seul .keys/ (D12) ; la clé privée jamais traversée (D87). Les pièces : loupe/ (l'ère 0.1.1 scellée, la carte génération 17 — l'entête version=0.1.1), le kit 0.1.1-dev.1 au coffre /test (loupe-kit-13, la vague du scellement), download/preuves-run-loupe-011-dev1/ (VERDICT e553ac8c… + les deux témoins), scripts/rapatrier_run_011_dev1.py, scripts/recouper_run12_011.py, scripts/depot_entree_222.py.
"""

WORKLOG_129 = """
Task ID: 129
Agent: Z.ai (agent principal)
Task: LE DOUZIÈME RUN RECOUPÉ 39/39 ET LA BALISE `loupe 0.1.1` SCELLÉE —
LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE (D181).

Work Log:
- LE RAPATRIEMENT (rapatrier_run_011_dev1.py) : les SEPT pièces de
  /test/kit-loupe/ (les QUATRE du kit == l'Entrée 221 : loupe.exe
  c1115105… / md5 5fc07b78…, scenario 77872b71…, bat 2a3f22f4…,
  LISEZMOI 70340163… ; temoin-fichier.bin == loupe.exe ; les DEUX
  témoins nés du run 46db2210… / d83ae8cb…) — md5 recoupés à
  l'arrivée.
- LE RECOUP (recouper_run12_011.py) 39/39 VERT : T0→T7 TOUT VERT POUR
  LA CINQUIÈME FOIS (le qword 0x00010101 lu sur la pièce — l'ère
  0.1.1), la cascade 205 POUR LA DEUXIÈME FOIS, LA VITRINE VIVANTE LA
  TROISIÈME FOIS (0 et 0 — la première de la pièce 0.1.1) ; la
  doctrine [SONDE-EXE] tenue (D178), le résidu [T0-PÉRIMÉ] nommé (le
  bandeau dev.12 du scénario porté, AUCUNE porte touchée) — LE VERT
  TIENT ENTIER ; VERDICT e553ac8c… + les DEUX témoins →
  download/preuves-run-loupe-011-dev1/.
- LA CRISTALLISATION : les HUIT passes (les compteurs 2/10 → 26 blocs
  à 10/10), la recomposition == la pièce à chaque passe (PLUS AUCUN
  écart — la dette n'existe pas à cette ère), les harnais 61/61 ·
  53/53 · 45/45 rejoués à chaque passe, la carte re-signée (D144).
- LE SCELLAGE (--sceller-final, le miroir D165/D170, les portes
  adaptées au verdict du douzième run) : le garde 14/14, LE VERDICT
  EXIGÉ COMME PIÈCE (les cinq portes assertées), la cristallisation
  10/10, le verrou croisé 26, la bascule 0.1.1-dev.1 → 0.1.1 dans
  frag-bld, l'entête version=0.1.1 génération 17 (racine 1f25afae…),
  la re-signature D144, l'anti-rollback ARMÉ constaté au geste même —
  **LA BALISE `loupe 0.1.1` SCELLÉE, loupe.exe INTACT (c1115105…,
  127 488 o)**.
- LE COFFRE (depot_entree_222.py) : le run 12 archivé
  (preuves-run-loupe-011-dev1/ au /test), kit-loupe/ recoupé puis
  corbeillé, la racine à la vague du scellement (27 entrées, AUCUN
  doublon), le réceptacle ré-armé à l'ère scellée (fd6deab4…), les
  DEUX index reversés.
- CONSIGNATIONS : D181, l'Entrée 222, le PLAN (l'État + la rangée
  (e)), le présent worklog.
- SUITE : au développeur — l'ère 0.1.1 scellée (M10 franchi depuis la
  0.1.0, douze runs au total) ; les options du programme d'après M10
  (§ 1.10 de la v0.9.0).
"""

ETAT_AJOUT = ("**LA BALISE `loupe 0.1.1` SCELLÉE le 11/11/2026 (Entrée 222, "
              "D181) : LA VERSION DE LA DETTE [R10-PÉRIMÉE] SOLDÉE — le "
              "douzième run recoupé 39/39 (T0→T7 TOUT VERT POUR LA CINQUIÈME "
              "FOIS, la cascade 205 pour la deuxième, LA VITRINE VIVANTE LA "
              "TROISIÈME FOIS [0 et 0 — la première de la pièce 0.1.1]), la "
              "cristallisation 26 blocs à 10/10, les portes du scellage "
              "adaptées au verdict (le miroir D165/D170), la bascule dans "
              "frag-bld, l'anti-rollback ARMÉ — loupe.exe INTACT "
              "(c1115105…, 127 488 o), la carte génération 17, la pièce du "
              "recoup au dépôt ; l'ère 0.1.1 ouverte et refermée le même "
              "jour : la version de maintenance à contrat stable (R4/R10).** ")

RANGEE_E_ANCIEN = ("**LA SUITE (D179, l'ère 0.1.1) : LA VERSION COMMANDÉE AU TERRAIN — le kit loupe-kit-13/ (la pièce 0.1.1-dev.1 c1115105…, la dette [R10-PÉRIMÉE] soldée à la naissance, 0 octet de code changé), LE DOUZIÈME RUN attendu (le même critère : le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine vivante) ; le labo recoupe, complète la cristallisation 10/10, ADAPTE les portes du scellage au verdict du run — si le vert tient : LA BALISE `loupe 0.1.1` SCELLÉE (la version de la dette soldée)** |")

RANGEE_E_NOUVEAU = ("**LA SUITE (D179, l'ère 0.1.1) : LA VERSION COMMANDÉE AU TERRAIN — le kit loupe-kit-13/ (la pièce 0.1.1-dev.1 c1115105…, la dette [R10-PÉRIMÉE] soldée à la naissance, 0 octet de code changé), LE DOUZIÈME RUN attendu (le même critère : le scénario ENTIER T0 → S0 → LA LIAISON ET la vitrine vivante) ; le labo recoupe, complète la cristallisation 10/10, ADAPTE les portes du scellage au verdict du run — si le vert tient : LA BALISE `loupe 0.1.1` SCELLÉE (la version de la dette soldée)** ; **LE DOUZIÈME RUN RECOUPÉ ET LA 0.1.1 SCELLÉE (Entrée 222, D181 — LE RUN DU SCELLEMENT DE LA DETTE) : T0→T7 TOUT VERT POUR LA CINQUIÈME FOIS, LA CASCADE 205 POUR LA DEUXIÈME, LA VITRINE VIVANTE LA TROISIÈME FOIS [0 et 0 — la première de la pièce 0.1.1, aucun WER], le recoup 39/39 — LE VERT TIENT ENTIER ; la doctrine [SONDE-EXE] tenue, le résidu [T0-PÉRIMÉ] nommé ; la cristallisation 26 × 10/10 [les huit passes], les portes adaptées au verdict, la bascule version=0.1.1 dans frag-bld, l'anti-rollback ARMÉ : LA BALISE `loupe 0.1.1` SCELLÉE — LA VERSION DE LA DETTE SOLDÉE, loupe.exe INTACT c1115105… (la carte génération 17, la pièce du recoup au dépôt) ; l'ère 0.1.1 ouverte et refermée le même jour — la version de maintenance à contrat stable (R4/R10)** |")


def main():
    # 1. JOURNAL — l'Entrée 222 avant le PREMIER marqueur
    chemin = REPO / "docs" / "JOURNAL_TRAVAIL.md"
    texte = chemin.read_text(encoding="utf-8")
    marqueur = "<!-- m5a:journal-des-builds v1"
    idx = texte.find(marqueur)
    assert idx > 0, "le marqueur du journal est introuvable"
    assert "## Entrée 222 —" not in texte, "l'Entrée 222 existe déjà"
    texte = texte[:idx] + ENTREE_222 + texte[idx:]
    chemin.write_text(texte, encoding="utf-8", newline="\n")
    print("[1/4] journal : l'Entrée 222 insérée avant le premier marqueur")

    # 2. DECISIONS — D181 appendée
    chemin = REPO / "docs" / "DECISIONS.md"
    texte = chemin.read_text(encoding="utf-8")
    assert "## D181 —" not in texte, "D181 existe déjà"
    assert texte.rstrip().endswith("D133, l'overflow p.32 le faux positif des filets du tableau des jalons)."), \
        "la fin de DECISIONS.md n'est pas celle attendue (D180)"
    chemin.write_text(texte.rstrip("\n") + "\n" + D181.lstrip("\n"),
                      encoding="utf-8", newline="\n")
    print("[2/4] décisions : D181 appendée après D180")

    # 3. WORKLOG — Task 129 appendée
    chemin = REPO / "worklog.md"
    texte = chemin.read_text(encoding="utf-8")
    assert "Task ID: 129" not in texte, "Task 129 existe déjà"
    chemin.write_text(texte.rstrip("\n") + "\n" + WORKLOG_129,
                      encoding="utf-8", newline="\n")
    print("[3/4] worklog : Task ID 129 appendée")

    # 4. PLAN — l'État + la rangée (e)
    chemin = REPO / "docs" / "PLAN_MILESTONES.md"
    texte = chemin.read_text(encoding="utf-8")
    ancre = "**État du programme.** **LA VERSION 0.1.1-dev.1 COMMANDÉE"
    assert texte.count(ancre) == 1, "l'ancre de l'État du programme est ambiguë"
    texte = texte.replace(
        ancre, "**État du programme.** " + ETAT_AJOUT
        + "**LA VERSION 0.1.1-dev.1 COMMANDÉE", 1)
    assert texte.count(RANGEE_E_ANCIEN) == 1, "la rangée (e) est introuvable"
    texte = texte.replace(RANGEE_E_ANCIEN, RANGEE_E_NOUVEAU, 1)
    chemin.write_text(texte, encoding="utf-8", newline="\n")
    print("[4/4] plan : l'État du programme + la rangée (e) étendue")

    print("LA CONSIGNATION EST COMPLÈTE — l'Entrée 222, D181, Task 129, le plan.")


if __name__ == "__main__":
    main()
