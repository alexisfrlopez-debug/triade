#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_v230_reprise.py — LA REPRISE de la génération v0.23.0 (la
session morte laissa le manuscrit inachevé : les en-têtes périmés
v0.22.0, une clause dupliquée au résumé FR par recouvrement des
remplacements (c-FR)/(d), la coquille « 599 » à l'en-tête date, la
disponibilité des données à l'état v0.21.0). Remplacements ancrés —
REFUS si une ancre manque ; jamais un chiffre retapé (la macro sourcée
ou rien) ; le verbatim historique demeure octet pour octet."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
ED = REPO / "edition-v0230"
MAIN = ED / "main.tex"


def remplace(t: str, ancien: str, nouveau: str, nom: str) -> str:
    if ancien not in t:
        print(f"ANCRE MANQUANTE : {nom}")
        sys.exit(2)
    if t.count(ancien) != 1:
        print(f"ANCRE AMBIGUE {t.count(ancien)}x : {nom}")
        sys.exit(2)
    print(f"  — {nom}")
    return t.replace(ancien, nouveau)


def main() -> int:
    t = MAIN.read_text(encoding="utf-8")

    # (1) LE PDFTITLE ET LE RUNNING HEADER À v0.23.0
    t = remplace(
        t,
        "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by "
        "Hand Under Signed-Intent Governance (Academic Edition v0.22.0)},",
        "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by "
        "Hand Under Signed-Intent Governance (Academic Edition v0.23.0)},",
        "le pdftitle à v0.23.0")
    t = remplace(
        t,
        "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.22.0}",
        "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.23.0}",
        "le running header à v0.23.0")

    # (2) LA COQUILLE « 599 » À L'EN-TÊTE \date (la batterie est 559 —
    #     16+3+4+13+3+8+512 ; le « 599 » passait inaperçu au linter par
    #     couverture fortuite d'un canon brut)
    t = remplace(
        t,
        "the 599-vector battery partition published exactly",
        "the 559-vector battery partition published exactly",
        "la coquille 599 → 559 (la batterie)")

    # (3) LE PASSAGE « PRESENT EDITION » DE L'ABSTRACT EN — la voix
    #     courante : v0.22.0/v0.22.1 à l'histoire datée, la présente
    #     v0.23.0 porte les douzième et treizième vagues
    t = remplace(
        t,
        "The\n"
        "present edition (v0.22.0) carries the eleventh instruction wave: the\n"
        "SIMD corridors measured on hardware, the AES-NI carrier loop\n"
        "restructured under its twelve-cycle target, the fourth campaign arm\n"
        "separating the notation effect proper from the verification regime,\n"
        "the lifter soundness established on its validated domain, the\n"
        "versioned templates cutting the token budgets again, the vault\n"
        "hardening proved on laboratory copies with the D81 delivery\n"
        "instructions purged from the operational documents, and the cross-piece\n"
        "numeric linter extended to every numeral of the prose.",
        "The\n"
        "v0.22.0 edition carried the eleventh instruction wave (the SIMD\n"
        "corridors measured on hardware, the AES-NI carrier loop under its\n"
        "twelve-cycle target, the fourth campaign arm, the lifter soundness,\n"
        "the versioned templates, the vault hardening with the D81 delivery\n"
        "instructions purged, the cross-piece numeric linter extended to\n"
        "every numeral of the prose), and v0.22.1 was the corrective release\n"
        "(the purged chains, the regenerated vault of ateliers). The present\n"
        "edition (v0.23.0) restates the programme in one voice and carries\n"
        "the twelfth and thirteenth waves: the GHASH corridor in PCLMULQDQ\n"
        "at 63--64 cycles against the sealed 806 (a $12.6\\times$ gain) with\n"
        "the full AES-GCM composition measured against OpenSSL EVP, the\n"
        "four-arm ventilation at equalised volumes settling the\n"
        "intrinsic-notation share at 5.5\\,\\% (the wave-eleven ``notation\n"
        "effect'' was the verification implementation), the TPL-ADD-v3\n"
        "grammar with its repair loop, the three requalifications (the 58\n"
        "memory-safety guards conditional assumption-discharged, the fifteen\n"
        "mutant exclusions proved-argued-bounded, the CF3 Tamarin model v2\n"
        "without the adversary restriction), the semantic-perimeter purge\n"
        "carried to the Book of the Vault v1.7 and the specification\n"
        "v0.15.8, the exact partition of the 559-vector battery, and the\n"
        "EN/FR abstracts generated from the same canonical values.",
        "la voix « present edition » (v0.23.0, les deux vagues portées)")

    # (4) LA CLAUSE DUPLIQUÉE AU RÉSUMÉ FR — le remplacement (d) de la
    #     passe morte recouvrait la clause transformée par (c-FR) : la
    #     clause « l'ajout par squelette… » vit DEUX fois ; la fusion
    #     propre (une seule occurrence, les opérandes à la macro)
    t = remplace(
        t,
        "\\gabaritAjouterApres{} pour ajouter (le squelette, −28,4 "
        "\\gabaritAjouterOp{}, la faisabilité 3/18 aux vagues 11-12 puis "
        "6/18 à la treizième — l'écart nommé) — CHAQUE valeur portant ID "
        "de décision, périmètre et statut à la TABLE CANONIQUE des "
        "budgets adoptés ; l'ajout par squelette à 2~200 (−28,4 "
        "\\gabaritAjouterOp{}, la faisabilité 3/18 aux vagues 11-12 puis "
        "6/18 à la treizième — l'écart nommé par classe de refus), chaque "
        "périmètre étiqueté ; l'édition v0.19.4 adopte le POINTEUR SEUL au",
        "\\gabaritAjouterApres{} pour ajouter (le squelette, −28,4 "
        "\\gabaritAjouterOp{}, la faisabilité 3/18 aux vagues 11-12 puis "
        "6/18 à la treizième — l'écart nommé par classe de refus), chaque "
        "périmètre étiqueté — CHAQUE valeur portant ID de décision, "
        "périmètre et statut à la TABLE CANONIQUE des budgets adoptés ; "
        "l'édition v0.19.4 adopte le POINTEUR SEUL au",
        "la clause dupliquée du résumé FR fusionnée (une seule occurrence)")

    # (5) LES PLAGES D'ENTRÉES PORTÉES À 383 (le worklog porte l'Entrée
    #     383 — la clôture de la vague 13 ; les deux pièces : le résumé
    #     FR et l'introduction)
    t = remplace(
        t,
        "de \\nbLignesJournal{} lignes (Entrées consignées jusqu'à 304 ; les "
        "clôtures\nde campagne et l'extension, Entrées 305--357, portées par "
        "le journal de tâches",
        "de \\nbLignesJournal{} lignes (Entrées consignées jusqu'à 304 ; les "
        "clôtures\nde campagne, l'extension et les vagues d'instructions, "
        "Entrées 305--383, portées par le journal de tâches",
        "la plage des Entrées du résumé FR (305–383)")
    t = remplace(
        t,
        "consigned through 304; the campaign closures and the extension,\n"
        "Entr\\'ees 305--357,\n"
        "carried in its \\nbLignesWorklog-line companion task log and the "
        "campaign",
        "consigned through 304; the campaign closures, the extension and "
        "the\ninstruction waves, Entr\\'ees 305--383,\n"
        "carried in its \\nbLignesWorklog-line companion task log and the "
        "campaign",
        "la plage des Entrées de l'introduction (305–383)")

    # (6) LA DISPONIBILITÉ DES DONNÉES — l'état au jour de la rédaction :
    #     v0.22.1 la dernière archivée (DOI 24420007), les dépôts
    #     antérieurs datés (24397623 la v0.21.0, 24407701 la v0.22.0),
    #     les archives de la présente aux noms v0.23.0
    t = remplace(
        t,
        "snapshots at the concept DOI \\doiConcept{} --- resolving to the "
        "latest\n"
        "archived version (v0.21.0 at this writing, version DOI\n"
        "\\doiVersionCourante{}; the earlier deposits "
        "10.5281/zenodo.24367344,\n"
        "10.5281/zenodo.24379173 and 10.5281/zenodo.24382460 are the dated\n"
        "v0.19.0, v0.19.4 and v0.19.5 archives; the distinction is consigned:",
        "snapshots at the concept DOI \\doiConcept{} --- resolving to the "
        "latest\n"
        "archived version (v0.22.1 at this writing, version DOI\n"
        "\\doiVersionCourante{}; the earlier deposits "
        "10.5281/zenodo.24367344,\n"
        "10.5281/zenodo.24379173, 10.5281/zenodo.24382460, "
        "10.5281/zenodo.24397623\n"
        "and 10.5281/zenodo.24407701 are the dated v0.19.0, v0.19.4, "
        "v0.19.5,\n"
        "v0.21.0 and v0.22.0 archives; the distinction is consigned:",
        "la disponibilité : v0.22.1 au jour de la rédaction, les DOI datés")
    t = remplace(
        t,
        "(\\code{TRIADE\\_soumission\\_v0.22.0.zip} and\n"
        "\\code{TRIADE\\_complet\\_v0.22.0.zip}) contain respectively the",
        "(\\code{TRIADE\\_soumission\\_v0.23.0.zip} and\n"
        "\\code{TRIADE\\_complet\\_v0.23.0.zip}) contain respectively the",
        "les archives de dépôt aux noms v0.23.0")

    MAIN.write_text(t, encoding="utf-8")
    print("[reprise] le manuscrit v0.23.0 porté à l'état courant complet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
