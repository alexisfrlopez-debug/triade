#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_plan_m8c.py — PLAN_MILESTONES.md : le chantier M8-(c) RÉALISÉ
(la cérémonie de l'ère passée, le build exécuté — Entrée 160, D163).
Deux éditions append-aware : la ligne M8 du tableau des jalons (la fin
de ligne) et la cellule de statut du chantier (c) dans la table M8."""

import sys

CHEMIN = "docs/PLAN_MILESTONES.md"

ANCRE1 = "les chantiers (c-exécution)/(d) attendent** |"
NOUVELLE1 = ("LE CHANTIER (c) RÉALISÉ le 05/11 (Entrée 160, D163) — LA CÉRÉMONIE "
             "DE L'ÈRE PASSÉE SUR PIÈCES (signatures-I.txt déposé au coffre /test "
             "par le développeur, rapatrié md5 contrôlé, LE RECOUP DE L'ÈRE VERT "
             "12/12 : les DIX signatures des arbres inchangés == celles du 04/11 — "
             "la clé réutilisée PROUVÉE par le déterminisme Ed25519 ; m0 re-signé "
             "[le registre étendu], m8 l'arbre neuf signé ; LE GARDE VERT 12/12 : "
             "la dette D162 soldée) ET LE BUILD EXÉCUTÉ (construire : l'héritage "
             "re-vérifié M4 560 + M5 365 cas verts + structurels 524/492/312 "
             "verrous, la preuve R7 44 blocs octet-identiques au scellé 0.6.0, le "
             "harnais 61/61, l'ARTEFACT 0.9.0-dev.1 NÉ 44 544 o sha256 1492b0bc… "
             "IDENTIQUE à la pièce de vérification Task 76 — le déterminisme d'un "
             "poste à l'autre, la carte génération 8 vivante [le témoin "
             "e9cd8c549485… ne bouge pas], le verrou croisé 55 empreintes — GESTE "
             "DE BUILD, jamais scellage) ; LE CHANTIER (d) ATTEND (le kit terrain "
             "au coffre /test, le VRAI ntdll lu sur la machine du développeur — "
             "la finale 0.9.0 attend le run terrain vert)** |")

ANCRE2 = "— la main du développeur est SERVIE |"
NOUVELLE2 = ("— la main du développeur est SERVIE ; **RÉALISÉ le 05/11 (Entrée "
             "160, D163) : LA CÉRÉMONIE PASSÉE SUR PIÈCES + LE BUILD EXÉCUTÉ** "
             "(signatures-I.txt rapatrié du coffre /test md5 contrôlé ; le recoup "
             "de l'ère 12/12 VERT — les DIX signatures inchangées == les déposées "
             "du 04/11, la clé du 04/11 réutilisée PROUVÉE par le déterminisme "
             "Ed25519 ; sceau_I.py deposer : 12 signatures installées, l'atomicité "
             "vérifiée AVANT écriture ; le garde REPASSÉ VERT 12/12 — la dette "
             "D162 soldée ; construire() : le garde en tête PASSE, l'héritage "
             "re-vérifié, l'ARTEFACT m8/proxy.exe 0.9.0-dev.1 NÉ 44 544 o sha256 "
             "1492b0bc… == la pièce de vérification, la carte génération 8 vivante, "
             "le verrou croisé 55 empreintes, le tableau de bord 0 défaut) — le "
             "chantier (d) attend |")

with open(CHEMIN, encoding="utf-8") as f:
    texte = f.read()

for ancre, nouvelle, nom in ((ANCRE1, NOUVELLE1, "ligne M8 (jalons)"),
                             (ANCRE2, NOUVELLE2, "table des chantiers M8 (c)")):
    if ancre not in texte:
        sys.exit(f"ECHEC : ancre introuvable pour {nom} : {ancre[:60]!r}")
    if texte.count(ancre) != 1:
        sys.exit(f"ECHEC : ancre non unique pour {nom} ({texte.count(ancre)} occurrences)")
    texte = texte.replace(ancre, nouvelle, 1)

with open(CHEMIN, "w", encoding="utf-8") as f:
    f.write(texte)
print("PLAN mis à jour : le chantier M8-(c) RÉALISÉ (cérémonie passée + build exécuté)")
