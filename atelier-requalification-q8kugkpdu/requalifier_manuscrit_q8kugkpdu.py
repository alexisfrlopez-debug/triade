#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""requalifier_manuscrit_q8kugkpdu.py — LES REQUALIFICATIONS DU MANUSCRIT
v0.23.0 (q8kugkpdu, la vague 13) : les QUATRE passages et la table des
statuts, au PATCHER ANCRÉ (REFUS si une ancre manque — la leçon des
vagues 8-12, jamais un remplacement sournois).

LES CIBLES (les lignes nommées du plan gelé, portées à edition-v0230) :
  (1) l'abstract EN (v0220 l.194-197) : « mechanically proved
      equivalent » → le statut exact (12 arguments sémantiques nommés +
      3 sweeps bornés, « proved-argued-bounded ») ;
  (2) le §floor « Memory safety at one hundred percent » (l.2034-2044) :
      « each carry a runtime guard » → le statut exact : sur l'artefact
      scellé les 58 sont « conditional (assumption-discharged) », les
      gardes ÉMISES en copies de laboratoire à la marge 0x10000 (OPT-01)
      et non au binaire scellé ; le TCB en liste exhaustive (24 · 23 · 11) ;
  (3) le §floor des scores mutation (l.1894-1898) : « the 15 proven
      equivalents » → le statut des 15 ;
  (4) le §limits (l.1752) : « the Tamarin/ProVerif line remains untried
      on this protocol » → le Tamarin ESSAYÉ au niveau du modèle (v2
      livré, restriction retirée, implication énoncée), l'exécution du
      prover au geste du maître (le gap nommé) ;
  (5) le §kits (l.2100-2107) : le kit Tamarin CF3 porte la v2
      reformulée ;
  (6) LA TABLE DES STATUTS : les TROIS lignes étendues (gardes,
      exclusions, Tamarin) — statuts_v230.tex (le geste de ylrzmlbn8
      porte le fichier, la présente écrit les lignes).

Le verbatim historique (les dossiers edition-v01xx/v0220) DEMEURE octet
pour octet — la présente ne touche QUE edition-v0230/."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
MAIN = REPO / "edition-v0230" / "main.tex"


def remplacer(texte: str, ancienne: str, nouvelle: str, nom: str) -> str:
    """Le remplacement ancré : REFUS si l'ancre manque ou n'est pas
    unique (jamais un remplacement sournois)."""
    n = texte.count(ancienne)
    if n != 1:
        sys.exit(f"[REFUS] l'ancre {nom} absente ou non unique ({n} fois)")
    return texte.replace(ancienne, nouvelle)


def main() -> int:
    t = MAIN.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # (1) L'ABSTRACT EN — le statut exact des 15 (l.194-197 de v0220)
    # ------------------------------------------------------------------
    t = remplacer(
        t,
        "and discharged mechanically; the fault-injection battery kills 811 of 832\n"
        "mutants (97.5\\%, the twenty-one remaining each named to a cause family,\n"
        "fifteen of them mechanically proved equivalent for an adjusted 811/817 =\n"
        "99.3\\%, six non-equivalent survivors remaining, each named to a harness\n"
        "limit);",
        "and discharged mechanically; the fault-injection battery kills 811 of 832\n"
        "mutants (97.5\\%, the twenty-one remaining each named to a cause family;\n"
        "fifteen of them are excluded from the adjusted denominator as\n"
        "\\emph{proved-argued-bounded} equivalents --- twelve by a named semantic\n"
        "argument on the notation (the empty read-set of the dying field, the\n"
        "adjacent sentinel, the converging guards, the unreachable off-table\n"
        "transfer site, the never-re-read RBP, the diverted target falling back)\n"
        "and three by a bounded sweep of the named scenario class (three border\n"
        "cells $\\times$ ten scrolls, thirty scenarios at zero divergence on the\n"
        "complete observable) --- for an adjusted 811/817 = 99.3\\%, never a\n"
        "mechanical unbounded proof; six non-equivalent survivors remaining,\n"
        "each named to a harness limit (three the blind shim, two the\n"
        "never-served failure path, one the never-served error code);",
        "abstract-15")

    # ------------------------------------------------------------------
    # (2) LE §floor MÉMOIRE — le statut exact des 58 gardes
    # ------------------------------------------------------------------
    t = remplacer(
        t,
        "and the 58 true dereferences each carry a runtime guard\n"
        "derived from the named external invariant (the plan field, the\n"
        "caller's contract, the OS), with a two-sided check proven by an\n"
        "UNSAT certificate and falsified per guard (the violated invariant is\n"
        "refused at both zone boundaries and on the index face, the honest\n"
        "address admitted). Every access carries its proof-strength label\n"
        "(statically sound / bounded / guarded); zero out-of-frame accesses.",
        "and the 58 true dereferences are requalified\n"
        "\\emph{conditional (assumption-discharged)} on the sealed artifact:\n"
        "each is a proof obligation conditional on a named external invariant\n"
        "--- the exhaustive trusted-computing base reads 24 plan-field\n"
        "accesses (the 960-byte CADRE layout), 23 caller-contract accesses\n"
        "(the AEAD context) and 11 OS accesses (the system-call buffer). The\n"
        "runtime guards themselves are \\emph{emitted in laboratory copies\n"
        "only} (the OPT-01 margin-$0\\times$10000 model, never in the sealed\n"
        "binary): a two-sided check proven by an UNSAT certificate per guard\n"
        "(58/58 re-verified), falsified per guard in the laboratory variant\n"
        "(the violated invariant is refused at both zone boundaries and on\n"
        "the index face, the honest address admitted). Every access carries\n"
        "its proof-strength label (statically sound / bounded /\n"
        "conditional-assumption-discharged); zero out-of-frame accesses.",
        "floor-memoire-58")

    # ------------------------------------------------------------------
    # (3) LE §floor DES SCORES — le statut des 15
    # ------------------------------------------------------------------
    t = remplacer(
        t,
        "(99.3\\,\\%, the 15 proven equivalents excluded from the denominator),",
        "(99.3\\,\\%, the 15 excluded equivalents labelled\n"
        "proved-argued-bounded --- twelve semantic arguments, three bounded\n"
        "sweeps, never mechanical unbounded proofs),",
        "floor-scores-15")

    # ------------------------------------------------------------------
    # (4) LE §limits — la ligne Tamarin
    # ------------------------------------------------------------------
    t = remplacer(
        t,
        "not at the modelling level; the Tamarin/ProVerif line remains\n"
        "untried on this protocol.",
        "not at the modelling level; the Tamarin line is now \\emph{tried at\n"
        "the modelling level} (the CF3 v2 model delivered with its\n"
        "adversary-at-threshold restriction removed, the secrecy guarantee\n"
        "reformulated as the implication \\emph{secret learnt $\\Rightarrow$\n"
        "the adversary held $\\ge$3 shares}, the threshold-reachability\n"
        "witness added, the model hashed), while the prover execution\n"
        "remains the developer's gesture (the assembly sandbox carries no\n"
        "tamarin-prover --- the gap named, no verdict fabricated); ProVerif\n"
        "remains untried.",
        "limits-tamarin")

    # ------------------------------------------------------------------
    # (5) LE §kits — le kit Tamarin porte la v2
    # ------------------------------------------------------------------
    t = remplacer(
        t,
        "the CF3 Tamarin model --- thirty fingerprints consigned\n"
        "before delivery, the 57 autotest checks green, no measurement taken\n"
        "(the developer's gesture remains the only source of terrain evidence).",
        "the CF3 Tamarin model --- thirty fingerprints consigned\n"
        "before delivery, the 57 autotest checks green, no measurement taken\n"
        "(the developer's gesture remains the only source of terrain\n"
        "evidence); the Tamarin kit now carries the \\emph{v2 reformulation}\n"
        "(q8kugkpdu: the porting restriction removed, the implication lemma\n"
        "stated, the threshold witness added, the new model hashed and\n"
        "consigned --- still unproven pending the developer's prover run).",
        "kits-tamarin-v2")

    MAIN.write_text(t, encoding="utf-8")
    print("[q8kugkpdu] les CINQ requalifications du manuscrit v0.23.0 "
          "appliquées (patcher ancré, zéro REFUS)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
