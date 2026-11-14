#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""104_consigne_294.py — LA CONSIGNATION : Entrée 294 au JOURNAL_TRAVAIL,
Task 201 au worklog, la carte OU-TROUVER portée à 294 (l'entrée 20,
l'en-tête de mise à jour, les renvois Entrées 251-294 / Tasks 158-201)."""
import pathlib
import re

REPO = pathlib.Path("/home/z/my-project/work/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
CARTE = REPO / "OU-TROUVER-LES-LIVRABLES.md"

# ---------------------------------------------------------------------------
ENTREE = """
## Entrée 294 — LES RUNS DE L'UNITÉ 2 REVENUS : LE BRAS C VERT 20-0 SIGNÉ ; LE BRAS T 18 VERT 2 ROUGE — L'ÉCART ÉTAIT AU JUGE, LA PIÈCE DROITE, LE KIT v2 LIVRÉ (l'annonce du développeur : « kit 02 C et T dans /test du drive »)

- LES DÉPÔTS (la sonde 97) : les DEUX kits de l'unité 2 courus au terrain le 14/11 — une copie datée née AU SEIN de chaque kit au coffre (16:50:59Z la T, 16:51:19Z la C) : la console du run, le témoin signé et les pièces du kit mêmes ; la chronologie tenue : T 16:46:34Z (la console) → 16:47:16Z (le témoin touché par la main) → la copie déposée 16:50:59Z ; C 16:48:50Z → 16:49:38Z → 16:51:19Z ; la machine : PORTABLE · Windows 10 · AMD64 · Python 3.14.10 (CA2 : la même que les QUATRE runs de la campagne).

- LE RECOUP TROIS FOIS (98) : chaque pièce du kit de chaque copie == le kit parent AU COFFRE (re-téléchargé) == le bac local du labo (la vérité de la construction 290) : 11 + 11 VERT, 0 écart — loupe.exe 98354ff6… et loupe-02-c.dll 925cd019… == les gravures ; les consoles UTF-16 LE (le Tee-Object de PowerShell — les accents INTACTS, la discipline du tuyau tenue), les témoins UTF-8.

- LE BRAS C : 20 VERT, 0 ROUGE (run-console-unite02C.txt 7 730 o, 669222e9…) — T0 VERT (925cd019…), l'image @ 0x7ff9b17c0000, les SIX exports découverts (SetFilePointerEx PRÉSENTE : l'écart nommé du kit 01 n'existe plus), la première fenêtre lue INLINE au bloc session (l'écart nommé du bras C), V1×9 + V2×3 + V3×4 + V4×2 + V5×1 ; le témoin (temoin-unite02C.txt 1 594 o, 7a700b55…) : daté 14/11/2026, signé Alexis Lopez (D99), la pièce == la gravure — LA PREMIÈRE LIVRAISON VERTE DE L'UNITÉ 2.

- LE BRAS T : 18 VERT, 2 ROUGE (run-console-unite02.txt 6 940 o, 67a13226…) — T0 VERT (98354ff6…), l'image @ 0x7ff7d7b90000, les SIX feuilles résolues (SetFilePointerEx comprise) ; les DEUX ROUGE : V2:les-bords-de-fenetre et V2:cinq-entrees-dont-une-non-alignee ; le témoin (temoin-unite02.txt 1 600 o, 843e82eb…) : daté 14/11/2026, signé Alexis Lopez, le verdict consigné « 18 VERT, 2 ROUGE — ÉCART NOMMÉ » par le scénario même.

- L'ÉCART ÉTAIT AU JUGE, PAS À LA PIÈCE (la preuve 99) : le lea du journal au slot loupe-02 de l'EXE RÉEL — décodé à l'octet près (4c 8d 35 b5 a1 00 00) — vise 0xE4A0, LA VÉRITÉ DU LAYOUT (loupe/layout.py, D161 : R_JOURNAL = 0xE4A0) ; le scénario livré portait R_JOURNAL = 0xE4E0, SOIXANTE-QUATRE octets trop haut ; LA PLOMBERIE : poser_journal écrivait la zone à 0xE4E0 (le compte à 0xF4E0), la pièce lisait son compte à 0xF4A0 — l'entrée #156 de la zone zéroée → compte 0 → AUCUN recouvrement → le tampon == la lecture fraîche sans les éditions → les DEUX V2 divergent du modèle ; REJOUÉ OCTET PAR OCTET AU LABO (100) : à 0xE4E0 les DEUX ROUGE du terrain reproduits, à 0xE4A0 le recouvrement vit ; le juge du bras C ÉCHAPPE à la faute (il découvre l'adresse du journal PAR LES EXPORTS de la dll — jamais une constante copiée à la main).

- LA FAUTE NOMMÉE AU LABO, LE GARDE NÉ : l'épreuve de la 290 valida le MODÈLE du juge (l'extraction AST + le contre-modèle, 2 000 cas) mais pas ses CONSTANTES d'adresse — l'oracle utilisait L.R_JOURNAL (droit) et le proxy éprouvait la même assomption : la faute ne pouvait être prise qu'au terrain, ELLE Y FUT PRISE ; L'AUDIT DES CONSTANTES (le scénario LIVRÉ contre le layout, par AST) désormais tenu au bac (100) : le v1 PRIS (R_JOURNAL +0x40), les juges qui coururent (01-T v2, 01-C v2, 02-C) nets — 22 VERT, 1 ROUGE (la faute même).

- LE KIT v2 (101-103) : LE SEUL CHANGEMENT — la constante remise à la vérité du layout, la faute demeurant NOMMÉE au commentaire et à la note de révision du docstring ; loupe.exe et les HUIT autres pièces INTACTES octet pour octet ; la gravure regravée (une seule ligne bouge : scenario-unite02.py 302fa3a1…), le LISEZMOI porteur de l'écart et de la reprise (cd9c0d57…), le zip v2 (e423b711…) ; LES ÉPREUVES 8 VERT 0 ROUGE (py_compile, l'audit des constantes du v2, la faute rejouée au lea de la pièce, le modèle AST == contre-modèle 2 000 cas + les décalées, la gravure == les pièces, les HUIT pièces intactes, le zip miroir) ; LIVRÉ au /test/kit-unite-loupe-02-T-20261114-v2/ — 12/12 recoupés PAR RE-TÉLÉCHARGEMENT, le kit v1 DEMEURE (D143).

- LE RANGEMENT (102) : les DEUX dépôts DÉPLACÉS — jamais jetés, D143 — à /test/archives-livraisons/unite-02-loupe-20261114/ (le dossier créé, les noms conservés), 13 + 13 fichiers md5 INTACTS après le geste, les kits de la racine retrouvant leur état de livraison 290 (12 pièces libres chacun) ; la racine du /test : 14 entrées (13 + le kit v2) ; LA CARTE LISEZMOI-KITS-UNITES-D204.txt portée à 294 (la section des runs revenus, 12 646 o, 91de873b…, re-téléchargée identique byte-byte).

- LE LIVRE (98-D) : livraisons.csv du livre rangé (unite-01-loupe-20261114/atelier-campagne-d204-20261114-013520) porte ENCORE les DEUX seules lignes de loupe-01 (T + C, 15:53:17Z — inchangé depuis la 293, sha256 f0afea11… == le recoup 293) : L'UNITÉ 2 N'EST PAS ENCORE AU LIVRE — la ligne C-loupe-02-it1 (VERT, la première livraison verte de l'unité) attend le geste de l'onglet 5, la ligne T-loupe-02-it1 attendra le run v2 revenu ; le run T 18-2 NE CONSOMME PAS d'itération (le précédent 283/284 : la faute au labo ne consomme jamais) ; l'atelier se choisit à « CHOISIR L'ATELIER EXISTANT… » (il vit désormais à archives-livraisons/unite-01-loupe-20261114/atelier-campagne-d204-20261114-013520/).

- LES ÉCARTS NOMMÉS : M2 NOMMÉ MANQUANT pour la session (les appels sans journal d'usage — la faute de la 290 répétée) ; M4 non instrumentée (les épreuves courues sans le chronomètre) ; l'écriture au coffre par LE RELAIS OAUTH (le compte de service seul refusé 403 à l'écriture, nommé) ; les consoles UTF-16 LE (l'artefact du Tee-Object, écart cosmétique — les accents intacts, les verdicts ASCII intacts).

- LA CONSIGNATION : la présente Entrée 294 + Task 201 ; la carte OU-TROUVER portée à 294 (l'entrée 20, l'en-tête, les renvois Entrées 251-294 / Tasks 158-201) ; le bac scripts/campagne_d204/depot-runs-kit-02-294/ (les sondes 97-103, les epreuves/ : les dépôts T et C rapatriés, le livre, la carte 290 telle quelle, la carte 294).

- SUITE : au développeur — ① LA LIGNE C-loupe-02-it1 AU LIVRE (onglet 5 · LIVRAISON de l'atelier 013520, choisi à « CHOISIR L'ATELIER EXISTANT… » : kit 2026-11-14, run 2026-11-14, VERT, « en attente ») ; ② LE RUN v2 DU BRAS T (le kit v2 au /test : 1·KIT choisir kit-unite-loupe-02-T-20261114-v2 → 2·RUN lancer → 3·TÉMOIN dater, signer de la main → preuves-unite02/ ENTIER au /test), puis la ligne T-loupe-02-it1 au livre ; ENSUITE loupe-05 sha256, aux deux bras — le labo construit à la commande. (15/11, la session des runs revenus)
"""

TASK = """

Task ID: 201
Agent: Z.ai (agent principal — la session des runs de l'unité 2 revenus : le bras C vert signé, le juge du bras T corrigé)
Task: L'ANNONCE DU DÉVELOPPEUR (« kit 02 C et T dans /test du drive ») : LES DEUX RUNS DE L'UNITÉ 2 REÇUS ET RECOUPÉS — le bras C 20 VERT 0 ROUGE (le témoin daté 14/11/2026, signé Alexis Lopez — D99 ; loupe-02-c.dll 925cd019… == la gravure ; SetFilePointerEx présente ; LA PREMIÈRE LIVRAISON VERTE DE L'UNITÉ 2) ; le bras T 18 VERT 2 ROUGE — L'ÉCART ÉTAIT AU JUGE, PAS À LA PIÈCE : le scénario v1 posait le journal à R_JOURNAL = 0xE4E0 (+0x40 au-dessus du layout 0xE4A0 — l'adresse du lea de la pièce, lue à l'octet près) ; la pièce lisait son compte à la bonne adresse, tombait sur la zone zéroée → compte 0 → aucun recouvrement → les DEUX vecteurs V2 ROUGE, rejoués octet par octet au labo.

Work Log:
- LA SONDE 97 : les copies datées nées au sein des DEUX kits (16:50:59Z / 16:51:19Z), les pièces rapatriées au bac (98) — recoup TROIS FOIS : la copie == le kit parent au coffre == le bac local, 11 + 11 VERT 0 écart ; les témoins signés, la machine PORTABLE (CA2 — la même que les quatre runs).
- LA PREUVE 99 : le lea du journal décodé DEPUIS L'EXE RÉEL (4c 8d 35 b5 a1 00 00 → 0xE4A0 == le layout D161 ; le cadre 0xE000 ==, les TROIS appels IAT aux slots du plan) — la pièce DROITE, le juge fautif (+0x40).
- LES ÉPREUVES 100 : L'AUDIT DES CONSTANTES (le garde qui manquait à la 290) — le v1 PRIS (22 VERT 1 ROUGE sur les QUATRE juges audités : 01-T v2, 01-C v2, 02-T v1, 02-C) ; LA FAUTE REJOUÉE : à 0xE4E0 les DEUX ROUGE du terrain reproduits (le compte lu à 0xF4A0 = l'entrée #156 de la zone zéroée), à 0xE4A0 le recouvrement vit.
- LE KIT v2 (101) : la constante seule changée (la faute nommée au commentaire et à la note de révision), les HUIT autres pièces INTACTES byte-byte, la gravure regravée (scenario-unite02.py 302fa3a1…, LISEZMOI cd9c0d57…), le zip e423b711… ; 8 ÉPREUVES VERT 0 ROUGE.
- LA LIVRAISON (103) : kit-unite-loupe-02-T-20261114-v2/ au /test, 12/12 recoupés PAR RE-TÉLÉCHARGEMENT ; la carte LISEZMOI-KITS-UNITES-D204.txt portée à 294 (12 646 o, 91de873b…, re-téléchargée identique) ; le kit v1 demeure (D143).
- LE RANGEMENT (102) : les DEUX dépôts déplacés à /test/archives-livraisons/unite-02-loupe-20261114/ (les noms conservés, 13 + 13 fichiers md5 intacts après le geste — jamais jetés) ; les kits de la racine à l'état de livraison 290 ; la racine du /test à 14 entrées.
- LE LIVRE : livraisons.csv porte encore les DEUX lignes de loupe-01 (f0afea11… == la 293) — C-loupe-02-it1 (VERT) attend l'onglet 5 ; T-loupe-02-it1 attendra le run v2 ; le run T 18-2 ne consomme PAS d'itération (le précédent 283/284).
- LES ÉCARTS NOMMÉS : M2 manquant (les appels sans journal d'usage), M4 non instrumentée, l'écriture par le relais OAuth (le compte de service refusé 403 — nommé), les consoles UTF-16 LE (le Tee-Object, écart cosmétique).
- LA CONSIGNATION : Entrée 294 + la présente Task 201 ; la carte OU-TROUVER portée à 294 (l'entrée 20, l'en-tête, les renvois 251-294 / 158-201) ; le bac depot-runs-kit-02-294/ (97-103 + epreuves/).
- SUITE : au développeur — ① la ligne C-loupe-02-it1 au livre (onglet 5, l'atelier choisi à « CHOISIR L'ATELIER EXISTANT… ») ; ② le run v2 du bras T (1·KIT choisir le dossier v2 → 2·RUN → 3·TÉMOIN signer de la main → preuves-unite02/ ENTIER au /test), puis la ligne T-loupe-02-it1 ; ENSUITE loupe-05 sha256, aux deux bras — le labo construit à la commande.
"""

ENTREE20 = """

20. **LES RUNS DE L'UNITÉ 2 REVENUS — LE BRAS C VERT 20-0 SIGNÉ ; LE BRAS T 18-2 : L'ÉCART ÉTAIT AU JUGE, LE KIT v2 LIVRÉ (Entrée 294)** : l'annonce « kit 02 C et T dans /test du drive » — les DEUX kits courus au terrain le 14/11 (T 16:46:34Z, C 16:48:50Z, la machine PORTABLE — CA2), les dépôts : une copie datée au sein de chaque kit (la console + le témoin + les pièces), recoupés TROIS FOIS (la copie == le kit parent au coffre == le bac du labo : 22/22 VERT) ; LES TÉMOINS datés 14/11/2026 et signés Alexis Lopez (D99), les pièces == les gravures (loupe.exe 98354ff6… / loupe-02-c.dll 925cd019…), SetFilePointerEx PRÉSENTE aux DEUX bras ; LE BRAS C : 20 VERT 0 ROUGE — LA PREMIÈRE LIVRAISON VERTE DE L'UNITÉ 2 (la ligne C-loupe-02-it1 attend l'onglet 5) ; LE BRAS T : 18 VERT 2 ROUGE — L'ÉCART ÉTAIT AU JUGE, PAS À LA PIÈCE : le scénario v1 posait le journal à R_JOURNAL = 0xE4E0, 64 octets au-dessus du layout (0xE4A0 — l'adresse que le lea de la pièce vise, lue à l'octet près) ; la pièce lisait son compte à la BONNE adresse, tombait sur la zone zéroée → compte 0 → aucun recouvrement → les DEUX vecteurs V2 ROUGE, REJOUÉS octet par octet au labo ; l'AUDIT DES CONSTANTES (le scénario livré contre le layout — l'épreuve qui manquait à la 290) désormais tenu (le v1 PRIS par le garde, les juges 01-T/01-C/02-C nets) ; le run T ne consomme PAS d'itération (le précédent 283/284) ; LE KIT v2 au /test/kit-unite-loupe-02-T-20261114-v2/ (LE SEUL CHANGEMENT : la constante ; loupe.exe et les HUIT autres pièces INTACTES octet pour octet, la gravure regravée — une seule ligne bouge ; 12/12 recoupés par re-téléchargement, le v1 demeure D143) ; LES DÉPÔTS RANGÉS à /test/archives-livraisons/unite-02-loupe-20261114/ (les noms conservés, md5 par md5, jamais jetés), la racine du /test à 14 entrées ; LA CARTE LISEZMOI-KITS portée à 294 ; LE LIVRE : livraisons.csv porte encore les DEUX lignes de loupe-01 — C-loupe-02-it1 à consigner MAINTENANT (l'atelier 013520 vit à archives-livraisons/unite-01-loupe-20261114/, le choisir à « CHOISIR L'ATELIER EXISTANT… »), T-loupe-02-it1 au retour du run v2 ; LA SUITE : le run v2 du bras T, puis loupe-05 sha256.
"""

CLAUSE_ENTETE = ("Entrée 294 — LES RUNS DE L'UNITÉ 2 REVENUS : le bras C 20 VERT 0 ROUGE "
                 "(le témoin daté signé, la pièce == la gravure, SetFilePointerEx présente — "
                 "LA PREMIÈRE LIVRAISON VERTE DE L'UNITÉ 2, la ligne C-loupe-02-it1 attend "
                 "l'onglet 5) ; le bras T 18 VERT 2 ROUGE — L'ÉCART ÉTAIT AU JUGE, PAS À LA "
                 "PIÈCE : le scénario v1 posait le journal à R_JOURNAL = 0xE4E0, +0x40 "
                 "au-dessus du layout (0xE4A0, l'adresse du lea de la pièce lue à l'octet "
                 "près) — la pièce lisait son compte à la bonne adresse, tombait sur la zone "
                 "zéroée → compte 0 → aucun recouvrement → les DEUX vecteurs V2 ROUGE, "
                 "rejoués octet par octet au labo ; l'AUDIT DES CONSTANTES (l'épreuve qui "
                 "manquait) désormais tenu ; LE KIT v2 livré au /test (la constante seule "
                 "changée, loupe.exe et les HUIT autres pièces intactes octet pour octet, "
                 "12/12 recoupés, le v1 demeure) ; les dépôts RANGÉS à /test/archives-"
                 "livraisons/unite-02-loupe-20261114/ (jamais jetés), la carte LISEZMOI-KITS "
                 "portée à 294 ; ")

# -- 1. le journal ---------------------------------------------------------------
j = JOURNAL.read_text(encoding="utf-8")
assert "Entrée 294" not in j
JOURNAL.write_text(j.rstrip("\n") + "\n" + ENTREE, encoding="utf-8")
print(f"[journal] Entrée 294 consignée : {len(JOURNAL.read_text(encoding='utf-8').splitlines())} lignes")

# -- 2. le worklog ----------------------------------------------------------------
w = WORKLOG.read_text(encoding="utf-8")
assert "Task ID: 201" not in w
WORKLOG.write_text(w.rstrip("\n") + "\n" + TASK, encoding="utf-8")
print(f"[worklog] Task 201 consigné : {len(WORKLOG.read_text(encoding='utf-8').splitlines())} lignes")

# -- 3. la carte ------------------------------------------------------------------
c = CARTE.read_text(encoding="utf-8")
assert "Entrée 294" not in c
# l'en-tête : la date + la clause de la 294 en tête de parenthèse
c2 = c.replace("*Mise à jour : 14/11/2026 (Entrée 293 —",
               "*Mise à jour : 15/11/2026 (" + CLAUSE_ENTETE + "Entrée 293 —", 1)
assert c2 != c, "l'en-tête n'a pas bougé"
# les renvois
c2 = c2.replace("Entrées 251-293) et au worklog (`worklog.md`, Tasks 158-200).*",
                "Entrées 251-294) et au worklog (`worklog.md`, Tasks 158-201).*", 1)
assert "251-294" in c2 and "158-201" in c2, "les renvois n'ont pas bougé"
# l'entrée 20 à la suite de la 19
c2 = c2.rstrip("\n") + "\n" + ENTREE20
CARTE.write_text(c2, encoding="utf-8")
print(f"[carte] portée à 294 : {len(c2.splitlines())} lignes, "
      f"l'entrée 20, l'en-tête, les renvois 251-294 / 158-201")

# -- 4. la vérification -----------------------------------------------------------
v = CARTE.read_text(encoding="utf-8")
checks = [("l'entrée 20", "**LES RUNS DE L'UNITÉ 2 REVENUS" in v and "Entrée 294)**" in v),
          ("l'en-tête", "Mise à jour : 15/11/2026" in v),
          ("les renvois", "Entrées 251-294" in v and "Tasks 158-201" in v)]
jj = JOURNAL.read_text(encoding="utf-8")
checks.append(("l'Entrée 294 au journal", "## Entrée 294 — LES RUNS DE L'UNITÉ 2 REVENUS" in jj))
ww = WORKLOG.read_text(encoding="utf-8")
checks.append(("la Task 201 au worklog", "Task ID: 201" in ww))
for nom, ok in checks:
    print(f"    [{'VERT' if ok else 'ROUGE'}] {nom}")
assert all(ok for _, ok in checks)
print("[CONSIGNATION] TOUT VERT")
