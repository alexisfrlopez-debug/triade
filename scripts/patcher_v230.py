#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_v230.py — LA GÉNÉRATION v0.23.0 (ylrzmlbn8, la vague 13) : les
écarts (a)-(f) du pack v0.22.0 portés aux pièces, les abstracts EN/FR
depuis les MÊMES canons, la voix « présent édition » unique, le changelog
gelé des vagues.

LA MÉTHODE : remplacements ancrés — REFUS si une ancre manque ; JAMAIS un
chiffre retapé à la main (la macro sourcée ou rien — les valeurs
canoniques aux macros_v230.tex) ; le verbatim historique demeure octet
pour octet (l'erratum vit au texte des preuves, à côté)."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
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

    # (c) LE −28,5 % corrigé PARTOUT (le canon : 1 − 2 199,5/3 073,5 =
    #     28,43 % — les opérandes non arrondis publiés)
    t = remplace(
        t,
        "2{,}200 ($-28.5\\,\\%$ against the whole-notation 3{,}074 at the same",
        "2{,}200 ($-28.4\\,\\%$ against the whole-notation 3{,}073.5 at the "
        "same",
        "(c) le ratio ajouter : −28,4 % aux opérandes non arrondis (EN)")
    t = remplace(
        t,
        "l'ajout par squelette à 2~200 (−28,5 %, la faisabilité 0→3 verts — l'écart nommé)",
        "l'ajout par squelette à 2~200 (−28,4 \\gabaritAjouterOp{}, la "
        "faisabilité 3/18 aux vagues 11-12 puis 6/18 à la treizième — "
        "l'écart nommé par classe de refus)",
        "(c) le ratio ajouter : −28,4 % (FR)")

    # (d) LE RÉSUMÉ FR ALIGNÉ : les MÊMES canons que l'EN (le résumé
    #     titrait les valeurs v0.17/v0.19.6 : 1 103/1 277/3 374/3 674)
    t = remplace(
        t,
        "1~103 tokens pour localiser (la re-mesure v0.19.6 reproduite à l'identique par le neuvième lot d'instructions,\n"
        "n=18, zéro divergence, la réponse elle-même une médiane de 52 tokens ;\n"
        "la médiane pré-OPT-04 au même instrument était de 1~714, un gain de\n"
        "−35,7 % au total et −93,3 % à la réponse ; note de périmètre : le\n"
        "round-trip v0.17.0 de 1~277 demeure historique étiqueté), 3~374 pour\n"
        "éditer (la campagne des hunks mesurant l'édition à 2~452, réponse 40\n"
        "tokens), 3~674 pour ajouter (les re-mesures v0.14.0 au contenu seul,\n"
        "580/2~143/3~510, et les valeurs M1 51/719/1~088 demeurent historiques et\n"
        "étiquetées telles — les\n"
        "périmètres de mesure diffèrent et sont documentés) contre une baseline\n"
        "naïve de 300~304 ; le onzième lot affine les trois formats — le localisateur hiérarchique à 627 natifs (−40,5 %), le gabarit versionné à 674 (−39,1 %, la prose de prescription −57 %), ",
        "\\gabaritLocaliserApres{} natifs pour localiser (le localisateur "
        "hiérarchique adopté, −40,5 \\gabaritLocaliserOp{} ; les mesures "
        "d'époque 1~714 puis 1~103 au pointeur seul demeurent historiques "
        "étiquetées), \\gabaritEditerApres{} pour éditer (le gabarit "
        "versionné TPL-EDIT-v1 adopté, −39,1 \\gabaritEditerOp{}, la prose "
        "de prescription −57 \\%), \\gabaritAjouterApres{} pour ajouter (le "
        "squelette, −28,4 \\gabaritAjouterOp{}, la faisabilité 3/18 aux "
        "vagues 11-12 puis 6/18 à la treizième — l'écart nommé) — CHAQUE "
        "valeur portant ID de décision, périmètre et statut à la TABLE "
        "CANONIQUE des budgets adoptés ; ",
        "(d) le résumé FR : les MÊMES canons que l'EN")

    # (d-bis) LA CAMPAGNE GÉNÉRATIVE ALIGNÉE (le FR disait 10 000/une
    #         classe d'écart : le modèle étendu re-playe 30 000 traces à
    #         zéro divergence)
    t = remplace(
        t,
        "et l'implémentation est testée contre le modèle par une campagne générative de conformité de 10~000 traces (graine consignée, tout chemin d'échec couvert, une classe d'écart unique trouvée, réduite et analysée ; zéro écart ailleurs — test de conformité model-based, renommé en la présente édition)",
        "et l'implémentation est testée contre le modèle par une campagne "
        "générative de conformité de 30~000 traces aux trois graines (tout "
        "chemin d'échec couvert, ZÉRO divergence, le rejeu bit-identique "
        "deux fois — la classe d'écart unique de la campagne d'origine, "
        "trouvée, réduite et analysée à l'époque, demeure l'histoire "
        "datée du modèle d'avant extension)",
        "(d-bis) la campagne générative : 30 000 traces à zéro divergence (FR)")

    # (f) « SETTLED » SCOPÉ : la formulation exacte (la dérivation outillée
    #     zéro divergence ; la récitation pure 0/64 le gap nommé)
    t = remplace(
        t,
        "and the inter-family independence question is settled by tooled",
        "and the inter-family independence question is answered in its "
        "tooled scope by",
        "(f) « settled » scopé (le début)")
    t = remplace(
        t,
        "where pure recitation reads only the public\n"
        "anchors.",
        "where pure recitation by the second, local model family reads "
        "only the public anchors --- and fails at 0/64, a named capacity "
        "gap, not a settled question.",
        "(f) « settled » scopé (le gap nommé)")

    # (a) LA PARTITION EXACTE DE LA BATTERIE 559 : les comptes nommés aux
    #     CINQ étiquettes (16 queue-16 + 3 queue-fin + 4 chevauchants +
    #     13 longueurs + 3 pages + 8 multi + 512 property-based = 559)
    t = remplace(
        t,
        "of \\batterieVecteurs{} vectors per search corridor --- buffer tails at\n"
        "every alignment, overlapping patterns, lengths 1--33, page\n"
        "boundaries, multiple occurrences, 512 property-based at the consigned\n"
        "seed --- at zero divergence)",
        "of \\batterieVecteurs{} vectors per search corridor --- the exact "
        "partition \\batteriePartition{} (sixteen buffer-tail vectors at "
        "every alignment of the last 16-byte block plus three at the "
        "buffer end, four overlapping patterns at periods one to four, "
        "thirteen lengths covering 1--33 --- the nominal list "
        "1, 2, 3, 4, 15, 16, 17, 18, 19, 20, 31, 32, 33 ---, three page "
        "crossings, eight multi-occurrence cases, 512 property-based at "
        "the consigned seed --- summing to \\batterieVecteurs{} exactly) "
        "at zero divergence)",
        "(a) la partition 559 exacte (le manuscrit)")

    # (b) LES LONGUEURS : les DEUX exacts ENSEMBLE (13 longueurs COUVRENT
    #     1-33 — la liste nominale publiée) — porté par la partition (a)

    # (e) LA TABLE CANONIQUE DES BUDGETS ADOPTÉS (une seule table, chaque
    #     valeur : ID de décision, périmètre, statut — les résultats de la
    #     vague 13 au même rang)
    t = remplace(
        t,
        "\\paragraph{The pre-registered kits.}",
        "\\paragraph{The canonical adopted-budgets table.} One table, "
        "every value carrying its decision ID, scope and status: locate "
        "1{,}053 $\\to$ \\gabaritLocaliserApres{} native (hierarchical, "
        "adopted D222/OPT-14) · edit 1{,}106 $\\to$ \\gabaritEditerApres{} "
        "(TPL-EDIT-v1, adopted OPT-14; the thirteenth wave's repair loop "
        "measures 712 per validated change at 18/18) · add 3{,}073.5 "
        "$\\to$ \\gabaritAjouterApres{} skeleton (measured OPT-14; "
        "feasibility 3/18, then 5/18 at the twelfth wave, then 6/18 at "
        "the thirteenth --- the repair loop converts none, the gap named "
        "by refusal class; the thirteenth wave measures 3{,}844 per "
        "validated change) --- the earlier perimeters (M1 51/719/1{,}088, "
        "content-only 580/2{,}143/3{,}510, whole-notation 3{,}374) remain "
        "dated history, labelled as such; the specification's dashboard "
        "(Table 19) is aligned on this table, its M1 budgets becoming "
        "dated history.\n\n"
        "\\paragraph{The pre-registered kits.}",
        "(e) la table canonique des budgets (le manuscrit)")

    # L'EN-TÊTE v0.23.0 (la date et la voix « présent édition »)
    t = remplace(
        t,
        "\\date{21 November 2026 — Academic edition v0.22.0 (the eleventh instruction batch: the cross-piece numeric linter extended to every numeral of the prose with the measured ratios restated at one decimal; the SIMD corridors measured on hardware --- the hybrid byte-search at 704 cycles inside the library's SIMD class, the SHA-NI body at 128.5 cycles per block; the AES-NI carrier loop restructured under its twelve-cycle target at 7.09 cycles per block; the fourth campaign arm separating the notation effect proper (55.7\\,\\%) from the verification regime (44.3\\,\\%); the lifter soundness established on its validated domain --- 942 encodings at zero divergence, the out-of-vocabulary guard fail-closed, sixteen blocks proven across seven families; the versioned templates cutting locate/edit/add again; the vault hardening proved on laboratory copies and the D81 delivery instructions purged from the operational documents)}",
        "\\date{22 November 2026 — Academic edition v0.23.0 (the present "
        "edition states the current state of the programme in one voice; "
        "the wave-by-wave changes live in the frozen edition changelog "
        "below; the thirteenth instruction batch: the GHASH corridor at "
        "63--64 cycles against the sealed 806 --- a 12.6$\\times$ gain, "
        "the full AES-GCM composition measured against OpenSSL EVP; the "
        "four-arm ventilation at equalised volumes settling the "
        "intrinsic-notation share at 5.5\\,\\% --- H-CGP3 held, the "
        "wave-eleven ``notation effect'' was the verification "
        "implementation; the TPL-ADD-v3 grammar and repair loop --- "
        "feasibility 6/18, the residual gap named by refusal class; the "
        "three requalifications --- the 58 memory-safety guards "
        "conditional (assumption-discharged) on the sealed artifact, the "
        "fifteen mutant exclusions proved-argued-bounded, the CF3 "
        "Tamarin model v2 with the adversary-at-threshold restriction "
        "removed; the Book of the Vault v1.7 and the specification "
        "v0.15.8 with the D81 delivery instructions purged at the "
        "semantic perimeter and the broken paragraphs rewritten; the "
        "599-vector battery partition published exactly; the EN/FR "
        "abstracts generated from the same canonical values)}",
        "l'en-tête v0.23.0 (la voix présent édition)")

    # LE CHANGELOG GELÉ (une section « Edition changelog » : chaque vague
    # UNE ligne datée)
    t = remplace(
        t,
        "\\section{Conclusion}\\label{sec:conclusion}",
        "\\section*{Edition changelog (frozen)}\\label{sec:changelog}\n"
        "\\noindent The body above states the current state in one "
        "voice; the waves are frozen history, one line each, the detail "
        "in the wave reports:\n"
        "\\begin{itemize}\\itemsep2pt\n"
        "\\item v0.14.0 (17 Nov 2026) --- the mutation battery re-run "
        "with composition killers; the compiler-reference comparison.\n"
        "\\item v0.15.x (17--18 Nov 2026) --- the proof-status table "
        "born; the explorer reproduced.\n"
        "\\item v0.18.x (18 Nov 2026) --- the two-arm campaign D204.\n"
        "\\item v0.19.0--v0.19.6 (19--20 Nov 2026) --- the OPT-04 "
        "pointer; the fault-injection battery; the kit v1.0.0.\n"
        "\\item v0.20.0 (20 Nov 2026) --- the floor edition: the "
        "four-axis dashboard, the memory-safety discharge, CF3 "
        "mechanised.\n"
        "\\item v0.21.0 (20 Nov 2026) --- the SSE2 re-measure; the "
        "edit-window; the third arm.\n"
        "\\item v0.22.0 (21 Nov 2026) --- the eleventh wave: the SIMD "
        "corridors, the carrier loop, the fourth arm, the lifter, the "
        "templates.\n"
        "\\item v0.22.1 (21 Nov 2026) --- the corrective release: the "
        "purged chains, the regenerated vault of ateliers.\n"
        "\\item v0.23.0 (22 Nov 2026) --- the present edition: the "
        "thirteenth wave carried, the requalifications, the equalised "
        "ventilation, the exact partition, the aligned abstracts.\n"
        "\\end{itemize}\n\n"
        "\\section{Conclusion}\\label{sec:conclusion}",
        "le changelog gelé des vagues")

    MAIN.write_text(t, encoding="utf-8")
    print("[v230] les corrections (a)-(f) portées au manuscrit v0.23.0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
