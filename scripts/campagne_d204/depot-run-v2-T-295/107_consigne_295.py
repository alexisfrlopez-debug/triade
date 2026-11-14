#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""107_consigne_295.py — LA CONSIGNATION de l'Entrée 295 + Task 202 : la
réception du run v2 du bras T (le dépôt preuves-unite02/, 20 VERT 0 ROUGE,
le témoin daté signé), l'unité 2 verte aux deux bras, les DEUX lignes au
livre attendues (la réponse à la question du développeur). Append au
worklog.md et au docs/JOURNAL_TRAVAIL.md ; la carte OU-TROUVER portée à
295 (l'entrée 21, l'en-tête, les renvois)."""
import pathlib

REPO = pathlib.Path("/home/z/my-project/work/triade")

WORKLOG = """

Task ID: 202
Agent: Z.ai (agent principal — la session du run v2 du bras T revenu vert signé)
Task: L'ANNONCE DU DÉVELOPPEUR (« preuves unite 02 dans /test du drive » + la question « je n'ai pas compris ce qu'il faut faire que je n'ai pas deja fait pour c loupe 02 ») : LE RUN v2 DU BRAS T REÇU ET RECOUPÉ — 20 VERT, 0 ROUGE, le témoin daté 14/11/2026 signé Alexis Lopez (D99) — L'UNITÉ 2 VERTE AUX DEUX BRAS ; le geste qui reste est LE MÊME aux deux bras et il n'était pas vécu au « C loupe 02 » non plus : LES DEUX LIGNES AU LIVRE.

Work Log:
- LA RESTAURATION DU BAC : le conteneur recyclé encore (la répétition des
  Entrées 285/293, nommée) — le bac local retombé à l'état 276 (les sessions
  277-294 vécurent en d'autres bacs, leurs consignations AU MIROIR) ; LA
  VÉRITÉ re-rapatriée du miroir Drive : le bundle courant 77 533 582 o
  (md5 1b39fb56…) == la pointe be7f948 (l'état 294 final), le dépôt local
  RESTAURÉ (fetch + reset --hard), l'Entrée 294 la dernière au journal —
  la chaîne sans trou.
- LE DÉPÔT (la sonde 104-S1) : preuves-unite02/ à la racine du /test (né au
  coffre 20:00:17Z le 14/11) — UNE pièce, temoin-unite02.txt 1 589 o
  (md5 02a5d7fc…, sha256 de170c5b…), re-téléchargée DEUX FOIS byte-byte
  IDENTIQUE ; LE DOSSIER ENTIER EST LÀ : le réceptacle ne porte QUE le
  témoin (le scénario n'écrit que lui — la ligne 454 ; la console vit au
  dossier du kit par le Tee-Object du LANCEUR).
- LE RECOUP (la sonde 104, 7/7 VERT) : loupe.exe 127 488 o sha256
  98354ff6… == la gravure du kit v2 == la pièce re-téléchargée re-hachée ==
  l'empreinte que porte le témoin (D143 : la pièce n'a jamais bougé) ; LES
  VINGT VECTEURS du v2 == LES VINGT du v1 (le témoin v1 aux archives en
  regard) — le diff v1→v2 recoupé au labo : la note de révision et la
  constante R_JOURNAL 0xE4E0→0xE4A0, RIEN d'autre ; les DEUX ROUGE du juge
  fautif v1 (V2:les-bords-de-fenetre, V2:cinq-entrees-dont-une-non-
  alignee) RETOURNÉS VERT au terrain — LA RÉPARATION VÉCUE ; la machine
  PORTABLE · Windows 10 · AMD64 · Python 3.14.10 (CA2 — la même que les
  SIX runs de la campagne) ; la chronologie tenue : run 19:53:02Z → la
  main 19:53:45Z → le coffre 20:00:17Z, jamais une date avant le run ;
  les DIX pièces du kit v2 au /test re-hachées 10/10 == la gravure.
- LA RÉPONSE À LA QUESTION : RIEN du run, RIEN du témoin ne manque — tout
  est vécu aux DEUX bras ; le geste qui manque est LA LIGNE AU LIVRE
  (l'onglet 5 · LIVRAISON de l'atelier 013520, choisi au TROISIÈME bouton
  « CHOISIR L'ATELIER EXISTANT… ») : livraisons.csv ne porte ENCORE que
  les DEUX lignes de loupe-01 (f0afea11…, inchangé depuis la 293) —
  C-loupe-02-it1 puis T-loupe-02-it1, la réponse portée à la carte du
  /test (la section 295).
- LE RANGEMENT (105) : preuves-unite02/ DÉPLACÉ — jamais jeté, D143 — à
  /test/archives-livraisons/unite-02-loupe-20261114/preuves-unite02/ (le
  nom conservé, md5 02a5d7fc… recoupé AVANT et APRÈS le geste, la racine
  du /test revenue à ses 14 entrées de la 294).
- LA CARTE DU /test (106) : LISEZMOI-KITS-UNITES-D204.txt PORTÉE À 295
  (12 646 → 15 448 o, sha256 c6f22126…) — la 294 INTACTE en tête, la
  section du run v2 revenu APPOSÉE en queue, re-téléchargée byte-byte
  identique.
- LA CONSIGNATION : la présente Task 202 + l'Entrée 295 ; la carte
  OU-TROUVER portée à 295 (l'entrée 21, l'en-tête de mise à jour, les
  renvois Entrées 251-295 / Tasks 158-202) ; le bac scripts/campagne_d204/
  depot-run-v2-T-295/ (les sondes, les epreuves/ : le témoin v2, le témoin
  v1 en regard, les scénarios v1/v2, le diff, la gravure, le RECOUP-104).
- SUITE : au développeur — LES DEUX LIGNES AU LIVRE (C-loupe-02-it1 et
  T-loupe-02-it1, l'onglet 5 de l'atelier 013520), puis l'atelier ENTIER
  au coffre /test ; ENSUITE loupe-05 sha256, aux deux bras — le labo
  construit à la commande.
"""

JOURNAL = """

## Entrée 295 — LE RUN v2 DU BRAS T REVENU : 20 VERT, 0 ROUGE, LE TÉMOIN DATÉ SIGNÉ — L'UNITÉ 2 VERTE AUX DEUX BRAS, LES DEUX LIGNES AU LIVRE ATTENDUES (l'annonce du développeur : « preuves unite 02 dans /test du drive » + la question : « je n'ai pas compris ce qu'il faut faire que je n'ai pas deja fait pour c loupe 02 »)

- LE DÉPÔT (la sonde 104-S1) : preuves-unite02/ à la racine du /test (né au coffre le 14/11 20:00:17Z) — UNE pièce, temoin-unite02.txt 1 589 o (md5 02a5d7fc…, sha256 de170c5b…), re-téléchargée DEUX FOIS byte-byte IDENTIQUE ; LE DOSSIER ENTIER EST LÀ : le réceptacle preuves-unite02/ ne porte QUE le témoin (le scénario n'écrit que lui — la console vit au dossier du kit par le Tee-Object du LANCEUR), la demande de la 294 satisfaite ENTIÈRE.

- LE RECOUP (la sonde 104, 7/7 VERT) : loupe.exe 127 488 o sha256 98354ff6… == la gravure du kit v2 == la pièce re-téléchargée et re-hachée == l'empreinte que porte le témoin — la pièce n'a jamais bougé (D143) ; LES VINGT VECTEURS du v2 == LES VINGT du v1 (le témoin v1 aux archives en regard) — le diff v1→v2 recoupé au labo : la note de révision et la constante R_JOURNAL 0xE4E0→0xE4A0, RIEN d'autre ; les DEUX ROUGE du juge fautif v1 (V2:les-bords-de-fenetre, V2:cinq-entrees-dont-une-non-alignee) RETOURNÉS VERT au terrain — LA RÉPARATION VÉCUE, le verdict 20 VERT, 0 ROUGE ; la main (D99) : daté le 14/11/2026, signé Alexis Lopez — LA MÊME MAIN que toute la campagne (Entrées 264/266/267/272/276/284/287/294) ; la machine : PORTABLE · Windows 10 · AMD64 · Python 3.14.10 (CA2 — la même que les SIX runs de la campagne) ; la chronologie tenue : le run 19:53:02Z → la main 19:53:45Z → le coffre 20:00:17Z, jamais une date avant le run ; les DIX pièces du kit v2 au /test re-hachées 10/10 == la gravure.

- CE QUE CELA FERME : LE BRAS T DE L'UNITÉ 2 EST VERT — L'UNITÉ 2 EST VERTE AUX DEUX BRAS (le bras C 20-0 à l'Entrée 294, le bras T 20-0 au présent run v2) ; le run T v1 18-2 NE CONSOMME PAS d'itération (la faute était au juge du labo, le précédent 283/284) — T-loupe-02-it1 consignera le run v2, la PREMIÈRE itération du bras T.

- LA RÉPONSE À LA QUESTION DU DÉVELOPPEUR (« je n'ai pas compris ce qu'il faut faire que je n'ai pas deja fait pour c loupe 02 ») : RIEN du run, RIEN du témoin — tout est vécu aux DEUX bras ; le geste qui manque est LE MÊME pour les deux, ET IL N'ÉTAIT PAS VÉCU AU « C loupe 02 » NON PLUS : LA LIGNE AU LIVRE. livraisons.csv de l'atelier 013520 (rangé à /test/archives-livraisons/unite-01-loupe-20261114/atelier-campagne-d204-20261114-013520/, sha256 f0afea11… inchangé depuis la 293) porte ENCORE les DEUX seules lignes de loupe-01 : l'unité 2 y attend C-loupe-02-it1 (kit 2026-11-14, run 2026-11-14, VERT, « en attente ») puis T-loupe-02-it1 (kit 2026-11-14, run 2026-11-14, VERT, « en attente ») — l'onglet 5 · LIVRAISON du GUI, l'atelier choisi au TROISIÈME bouton « CHOISIR L'ATELIER EXISTANT… » (jamais « CHOISIR LE DOSSIER… » qui veut campagne-d204, le refus nommé à la 292), puis l'atelier ENTIER renvoyé au coffre ; les onglets compagnons aux gestes vécus (4 · CARNET M3, 7 · CHRONO M4).

- LE RANGEMENT (105) : preuves-unite02/ DÉPLACÉ — jamais jeté, D143 — à /test/archives-livraisons/unite-02-loupe-20261114/preuves-unite02/ (le nom conservé, le md5 02a5d7fc… recoupé AVANT et APRÈS le geste, la racine du /test revenue à ses 14 entrées de la 294).

- LA CARTE DU /test (106) : LISEZMOI-KITS-UNITES-D204.txt PORTÉE À 295 (12 646 → 15 448 o, sha256 c6f22126…) — la 294 INTACTE en tête, la section du run v2 revenu APPOSÉE en queue (elle porte LA RÉPONSE à la question du développeur : les deux lignes, le chemin entier), re-téléchargée byte-byte identique.

- LA CONSIGNATION : la présente Entrée 295 + Task 202 ; la carte OU-TROUVER portée à 295 (l'entrée 21 au tableau de campagne, l'en-tête de mise à jour, les renvois Entrées 251-295 / Tasks 158-202) ; le bac scripts/campagne_d204/depot-run-v2-T-295/ (la sonde 104 et ses compléments, les epreuves/ : le témoin v2, le témoin v1 en regard, les scénarios v1/v2, le diff, la gravure, le RECOUP-104).

- SUITE : au développeur — LES DEUX LIGNES AU LIVRE (C-loupe-02-it1 et T-loupe-02-it1, l'onglet 5 · LIVRAISON de l'atelier 013520 choisi à « CHOISIR L'ATELIER EXISTANT… »), puis l'atelier ENTIER au coffre /test ; ENSUITE loupe-05 sha256, aux deux bras — le labo construit à la commande. (15/11, la session du run v2 revenu)
"""

ENTREE_21 = """
21. **LE RUN v2 DU BRAS T REVENU VERT SIGNÉ — L'UNITÉ 2 VERTE AUX DEUX BRAS, LES DEUX LIGNES AU LIVRE ATTENDUES (Entrée 295)** : l'annonce « preuves unite 02 dans /test du drive » — le dépôt preuves-unite02/ au /test (né 20:00:17Z le 14/11, UNE pièce : temoin-unite02.txt 1 589 o, md5 02a5d7fc…, re-téléchargé deux fois byte-byte) : LE DOSSIER ENTIER (le réceptacle ne porte QUE le témoin — le scénario n'écrit que lui, la console vit au dossier du kit) ; LE RECOUP 7/7 VERT (la sonde 104) : loupe.exe 98354ff6… == la gravure du kit v2 == l'empreinte portée au témoin ; les VINGT vecteurs du v2 == LES VINGT du v1 (le diff v1→v2 recoupé : la note de révision et la constante R_JOURNAL 0xE4E0→0xE4A0, RIEN d'autre), les DEUX ROUGE du juge fautif v1 (les-bords-de-fenetre, cinq-entrees-dont-une-non-alignee) RETOURNÉS VERT — LE VERDICT 20 VERT, 0 ROUGE ; la main (D99) : daté 14/11/2026, signé Alexis Lopez ; la machine PORTABLE · Windows 10 · Python 3.14.10 (CA2, la même que les SIX runs) ; la chronologie : run 19:53:02Z → main 19:53:45Z → coffre 20:00:17Z ; le kit v2 re-haché 10/10 == la gravure ; LE BRAS T VERT — L'UNITÉ 2 VERTE AUX DEUX BRAS (le C 20-0 à la 294), le run v1 18-2 ne consomme pas d'itération (283/284) ; LA RÉPONSE à « je n'ai pas compris ce qu'il faut faire que je n'ai pas deja fait pour c loupe 02 » : le geste qui manque est LE MÊME aux deux bras et il n'était pas vécu au C non plus — LES DEUX LIGNES AU LIVRE (onglet 5 · LIVRAISON, l'atelier 013520 choisi au TROISIÈME bouton « CHOISIR L'ATELIER EXISTANT… ») ; le dépôt RANGÉ à /test/archives-livraisons/unite-02-loupe-20261114/preuves-unite02/ (md5 recoupé avant/après, D143), la racine du /test revenue à 14 entrées ; LA CARTE LISEZMOI-KITS portée à 295 (15 448 o, c6f22126…) ; LA SUITE : les deux lignes au livre puis l'atelier entier au coffre, ensuite loupe-05 sha256, aux deux bras."""

# -- worklog + journal (append, UTF-8 LF, idempotent) ---------------------------
wl = (REPO / "worklog.md").read_text(encoding="utf-8")
if "Task ID: 202" in wl:
    print("[déjà] worklog.md porte Task 202 — pas de double append")
else:
    with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
        f.write(WORKLOG)
    print("[consigné] worklog.md (Task 202)")
jr = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
if "## Entrée 295" in jr:
    print("[déjà] docs/JOURNAL_TRAVAIL.md porte l'Entrée 295 — pas de double append")
else:
    with open(REPO / "docs" / "JOURNAL_TRAVAIL.md", "a", encoding="utf-8", newline="\n") as f:
        f.write(JOURNAL)
    print("[consigné] docs/JOURNAL_TRAVAIL.md (l'Entrée 295)")

# -- la carte OU-TROUVER (idempotent) ------------------------------------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
texte = carte.read_text(encoding="utf-8")
if "(Entrée 295)**" in texte:
    print("[déjà] la carte porte l'entrée 21 — pas de double apposition")
else:
    # 1. l'en-tête de mise à jour : l'Entrée 295 en tête de la chaîne
    nouvelle_entete = (
        "*Mise à jour : 15/11/2026 (Entrée 295 — LE RUN v2 DU BRAS T REVENU : "
        "20 VERT 0 ROUGE, le témoin daté 14/11/2026 signé Alexis Lopez (D99), "
        "loupe.exe 98354ff6… == la gravure == l'empreinte portée, les VINGT "
        "vecteurs == ceux du v1 — les DEUX ROUGE du juge fautif RETOURNÉS VERT, "
        "la réparation vécue au terrain ; la chronologie run 19:53:02Z → main "
        "19:53:45Z → coffre 20:00:17Z, la machine PORTABLE (CA2) ; LE DOSSIER "
        "ENTIER reçu (le réceptacle ne porte que le témoin), RANGÉ à /test/"
        "archives-livraisons/unite-02-loupe-20261114/preuves-unite02/ ; "
        "L'UNITÉ 2 VERTE AUX DEUX BRAS — le livre seul attend : LES DEUX LIGNES "
        "C-loupe-02-it1 et T-loupe-02-it1 à l'onglet 5 de l'atelier 013520 "
        "(livraisons.csv ne porte encore que les deux lignes de loupe-01), la "
        "carte LISEZMOI-KITS portée à 295 ; ")
    ancienne_entete = "*Mise à jour : 15/11/2026 (Entrée 294 —"
    assert ancienne_entete in texte, "l'en-tête 294 introuvable à la carte"
    texte = texte.replace(ancienne_entete, nouvelle_entete + "Entrée 294 —", 1)

    # 2. les renvois
    assert "Entrées 251-294) et au worklog (`worklog.md`, Tasks 158-201).*" in texte
    texte = texte.replace(
        "Entrées 251-294) et au worklog (`worklog.md`, Tasks 158-201).*",
        "Entrées 251-295) et au worklog (`worklog.md`, Tasks 158-202).*", 1)

    # 3. l'entrée 21 au tableau de campagne (en fin de fichier)
    assert texte.rstrip().endswith("loupe-05 sha256."), (
        "la carte ne finit pas à l'entrée 20 attendue")
    texte = texte.rstrip("\n") + "\n" + ENTREE_21 + "\n"

    carte.write_text(texte, encoding="utf-8", newline="\n")
    print("[portée] OU-TROUVER-LES-LIVRABLES.md : l'entrée 21, l'en-tête 295, "
          "les renvois 251-295 / 158-202")
