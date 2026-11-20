#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v210.py — L'ÉDITION v0.21.0 DU MANUSCRIT née de la v0.20.0
par REMPLACEMENTS ANCRÉS (REFUS si une ancre manque — la méthode
établie). TROIS FAMILLES :
  (A) LA RÉCONCILIATION (1e2vq7rtw) : l'abstract aligné au corps (811/817
      = 99,3 %, les 15 équivalents, les 6 survivants non équivalents) ;
      le ratio M4 courant recalculé des médianes non arrondies ; l'axe
      token ajouter au COÛT OPÉRATIONNEL (le format refusé nommé au
      bord, jamais rapporté comme coût) ;
  (B) LES RÉSULTATS DE LA VAGUE 10 portés : la fenêtre d'édition
      (OPT-10), le bras C+G (l'effet notation isolé), la re-mesure SSE2
      (LA FAUTE NOMMÉE + le temps réel + les baselines équitables), les
      gardes (100 % déchargé-ou-gardé), la non-interférence étendue (la
      requalification sous l'hypothèse du lifter) ;
  (C) LE REGISTRE NEUTRE (rgttyp8bj) : le lexique ritualiste remplacé,
      les majuscules d'emphase retirées de la prose, les pièces verbatim
      demeurées octet pour octet, AUCUNE valeur numérique modifiée hors
      la réconciliation documentée, AUCUNE revendication renforcée."""
from __future__ import annotations

import pathlib
import sys

SRC = pathlib.Path("/home/z/my-project/depot/edition-v0200/main.tex")
DST = pathlib.Path("/home/z/my-project/depot/edition-v0210/main.tex")
DST.parent.mkdir(parents=True, exist_ok=True)

R = []          # (ancienne, nouvelle, nom)


def remplace(ancienne: str, nouvelle: str, nom: str):
    R.append((ancienne, nouvelle, nom))


# ============ (A) LA RÉCONCILIATION =====================================
remplace(
    "twelve of them mechanically proved equivalent for an adjusted 811/820 =\n"
    "98.9\\%); and the inter-family independence question is settled by tooled\n",
    "fifteen of them mechanically proved equivalent for an adjusted 811/817 =\n"
    "99.3\\%, six non-equivalent survivors remaining, each named to a harness\n"
    "limit); and the inter-family independence question is settled by tooled\n",
    "l'abstract aligné au corps (811/817 = 99,3 %)")

remplace(
    "\\date{20 November 2026 — Academic edition v0.20.0 (the wave-9 floor "
    "edition: the four-axis dashboard generated from the raw artifacts "
    "with named floors and overhead ratios, the memory-safety analysis "
    "extended to 2{,}006 of 2{,}098 accesses discharged by loop invariants, "
    "interval and alias analysis and bounded model checking, the three "
    "remaining ``killable'' mutants re-classified as sweep-proven "
    "equivalents, the CF3 inductive invariant mechanised in an independent "
    "proof assistant (14/14 obligations), the static non-interference "
    "proof carried on the ten crypto families, the crystallisation "
    "certificate and the double engine at session opening, the two "
    "performance lanes with the SSE2 baseline variant at "
    "0.03$\\times$ the gcc-O2 cost, and the token campaign with the "
    "deterministic oracle compiler; no measured value modified)}",
    "\\date{20 November 2026 — Academic edition v0.21.0 (the tenth "
    "instruction batch: the abstract reconciled with the body at the "
    "current mutation score; the edit window reducing the reread "
    "material by 7.0$\\times$ for a 53.3\\,\\% total reduction; the "
    "third campaign arm separating the notation effect from governance "
    "alone (18.1$\\times$ residual verification cost); the byte-search "
    "SSE2 variant corrected under a fault found by a planted-occurrence "
    "differential and re-measured on hardware against fair baselines; "
    "the 92 runtime-based accesses brought to 100\\,\\% "
    "discharged-or-guarded; the static non-interference proof extended "
    "to x25519 and MD5 and restated under an explicit lifter-soundness "
    "hypothesis; the register of the manuscript neutralised to standard "
    "scientific tone)}",
    "la date d'édition v0.21.0")

remplace(
    "static non-interference proof covers the ten crypto families with the\n"
    "negative control caught.\n",
    "the static non-interference proof covers 13 blocks across seven\n"
    "crypto families, restated as proven under the explicit lifter-\n"
    "soundness hypothesis (the IR-to-notation round-trip verifies the\n"
    "hypothesis on every covered block), with the negative control\n"
    "caught.\n",
    "la non-interférence étendue + la requalification (§Sécurité du plancher)")

remplace(
    "\\paragraph{Token cost.} The pointer-only localiser stands at a median\n"
    "of 1{,}103 tokens (response 52); the hunk editor at 2{,}452 (response\n"
    "40, $-34.3\\,\\%$ / $-97.7\\,\\%$); the add-by-hunks format is refused for\n"
    "the third time (0/18 --- the whole-notation path remains); the floor\n"
    "ratios are 136.2$\\times$ (edit: the reread material dominates), 38.0\n"
    "$\\times$ (locate), 4.1$\\times$ (add) and 2.9$\\times$ (compose) against\n"
    "the named floors (the real diff pair, the literal pointer, the block\n"
    "body).\n",
    "\\paragraph{Token cost.} The pointer-only localiser stands at a median\n"
    "of 1{,}103 tokens (response 52); the window editor at 1{,}146\n"
    "(response 40, a 53.3\\,\\% reduction of the edit total with the reread\n"
    "material down from 1{,}684 to 239 cl100k tokens --- the prescription\n"
    "prose now dominates, the next measured lever); the add operation's\n"
    "operational cost is the whole-notation path at 3{,}674 (the\n"
    "add-by-hunks format is refused for the third time, 0/18 --- reported\n"
    "as a refused format, never as the operation's cost); the floor\n"
    "ratios are 63.6$\\times$ (edit, window mode), 38.0$\\times$ (locate) and\n"
    "16.0$\\times$ (add, whole notation) against the named floors (the real\n"
    "diff pair, the literal pointer, the block body).\n",
    "l'axe token ajouter au coût opérationnel + la fenêtre portée (paragraphe Token cost)")

# ============ (B) LES RÉSULTATS DE LA VAGUE 10 ===========================
remplace(
    "\\paragraph{Performance.} The M4 session runs at a median of\n"
    "\\mquatreAvantMediane{}\\,s unoptimised, \\mquatreChaudMediane{}\\,s warm\n"
    "with the memo stack (the 29.7\\,s run is the lived 1-in-10 audit), and\n"
    "\\mquatreBrasC{}\\,s at the compiled reference arm: a floor-ratio of\n"
    "\\mquatreRatioChaud{} against the C arm at equal work. The SSE2 baseline\n"
    "variant of the byte-search block reaches \\ssewRatio{} the gcc-O2 cost\n"
    "at equal vectors (\\ssewGainGPR{} over the sealed GPR notation), and the\n"
    "AES-NI descent is already the sealed domain (the era profile requires\n"
    "it).\n",
    "\\paragraph{Performance.} The M4 session runs at a median of\n"
    "\\mquatreAvantMediane{}\\,s unoptimised, \\mquatreChaudMediane{}\\,s warm\n"
    "with the memo stack (the 29.7\\,s run is the observed 1-in-10 audit),\n"
    "and \\mquatreBrasC{}\\,s at the compiled reference arm: a floor-ratio\n"
    "of \\mquatreRatioChaud{} against the C arm at equal work, recalculated\n"
    "from the unrounded medians and cited at one decimal wherever the\n"
    "current measurement is meant. The byte-search SSE2 variant was\n"
    "corrected and re-measured: the prior variant broadcast a four-byte\n"
    "pattern instead of the first byte (a fault surfaced by a\n"
    "planted-occurrence differential the prior confrontation could not\n"
    "see, 406 of 564 planted occurrences missed); the corrected variant\n"
    "passes all 88 vectors at zero divergence and costs \\sseDeuxVdeuxInstructions{}\n"
    "instructions per operation --- 0.04$\\times$ the gcc-O2 instruction\n"
    "count --- while on hardware (RDTSC, pinned core, $n{=}20$) it runs\n"
    "\\sseDeuxTempsReel{} cycles per absent 4{,}096-byte search against\n"
    "\\gccODeuxTempsReel{} for gcc-O2, \\idiomeMemchrTempsReel{} for the\n"
    "memchr-and-memcmp idiom and 933 for libc \\code{memmem}: the\n"
    "hand-written SSE2 notation sits \\emph{inside the class of the library's\n"
    "SIMD primitives} (1.6$\\times$ above the memchr idiom, 1.1$\\times$\n"
    "below \\code{memmem}), two orders below the compiled scalar path. The\n"
    "AES-NI descent is already the sealed domain (the era profile requires\n"
    "it), and the CPUID dispatch is hoisted out of the per-block loop in\n"
    "the laboratory variant (45 to 34.4 instructions per block, at exact\n"
    "parity with the sealed block under the same carrier).\n",
    "la Performance re-mesurée (le temps réel + les baselines équitables)")

remplace(
    "\\paragraph{Lexicographic reading.} No compensation between ranks: each\n"
    "axis is reported for itself, and the wave improved the security rank\n"
    "without conceding performance, verification strength or token cost.\n",
    "\\paragraph{Lexicographic reading.} No compensation between ranks: each\n"
    "axis is reported for itself, and the tenth instruction batch improved\n"
    "the security rank without conceding performance, verification\n"
    "strength or token cost.\n"
    "\n"
    "\\paragraph{The isolated notation effect.} The third campaign arm\n"
    "(C+G: the gcc-O2-compiled C receiving the full governance stack ---\n"
    "signed intentions, a chained crystallisation certificate, the\n"
    "contract-derived oracle, the kit) separates what hand-written\n"
    "notation costs from what governance alone costs. Measured on the same\n"
    "machine at $n{=}5$ per arm: T \\cgMquatreT{}\\,s, C \\cgMquatreC{}\\,s,\n"
    "C+G \\cgMquatreCG{}\\,s --- the governance gestures add\n"
    "\\cgEffetGouvernanceMs{}\\,ms (\\cgEffetGouvernanceRatio{}), while the\n"
    "residual \\cgEffetNotationMs{}\\,ms per session\n"
    "(\\cgEffetNotationRatio{}) is the notation's own proof burden: the\n"
    "twelve concurrent crystallisation rebuilds, the byte-exact\n"
    "round-trips and the plan recomposition that the compiled arm never\n"
    "requires. The sixth unit closed on its red at the correction cap\n"
    "(three named escapes: an external-composition answer, a faulty\n"
    "SHA-256 constant table caught by the independent judge at 0/3\n"
    "reference vectors, a completion-truncated final pass) --- the\n"
    "campaign's own precedent for a unit closed at the cap, reported as\n"
    "such. The human-time metric is not measurable in the laboratory and\n"
    "awaits the developer's field run; no value is fabricated.\n"
    "\n"
    "\\paragraph{Memory safety at one hundred percent.} The 92\n"
    "runtime-based accesses of the prior edition now close the\n"
    "classification: 34 address computations (LEA) are discharged\n"
    "relationally (the computed value feeds already-classified use\n"
    "sites), and the 58 true dereferences each carry a runtime guard\n"
    "derived from the named external invariant (the plan field, the\n"
    "caller's contract, the OS), with a two-sided check proven by an\n"
    "UNSAT certificate and falsified per guard (the violated invariant is\n"
    "refused at both zone boundaries and on the index face, the honest\n"
    "address admitted). Every access carries its proof-strength label\n"
    "(statically sound / bounded / guarded); zero out-of-frame accesses.\n",
    "les résultats C+G + les gardes (nouveaux paragraphes)")

remplace(
    "oracle compiler (968 oracle tokens removed over three units).\n",
    "oracle compiler (968 oracle tokens removed over three units); the\n"
    "tenth batch adds the edit window (OPT-10: the reread material down\n"
    "7.0$\\times$, the total median 2{,}452 to 1{,}146 at $n{=}18$ with the\n"
    "independent re-tokenisation at zero drift and the pointer's four\n"
    "named refusals re-verified fail-closed).\n",
    "OPT-10 porté au paragraphe Optimisation")

remplace(
    "The floor edition (v0.20.0) adds the four-axis dashboard generated from "
    "the raw artifacts, the distance-to-the-floor section, the memory-safety "
    "discharge of 95.6\\,\\% of the 2{,}098 accesses by bounded model "
    "checking over the lifted notation, the CF3 inductive invariant "
    "mechanised in an independent proof assistant, the static "
    "non-interference proof on the ten crypto families, and the two "
    "performance lanes with the SSE2 baseline variant measured at "
    "0.03$\\times$ the gcc-O2 cost at equal vectors.",
    "The floor edition (v0.20.0) added the four-axis dashboard generated\n"
    "from the raw artifacts, the distance-to-the-floor section, the\n"
    "memory-safety discharge of 95.6\\,\\% of the 2{,}098 accesses by bounded\n"
    "model checking over the lifted notation, the CF3 inductive invariant\n"
    "mechanised in an independent proof assistant, the static\n"
    "non-interference proof on the covered crypto families, and the two\n"
    "performance lanes. The present edition (v0.21.0) reconciles the\n"
    "abstract with the body, corrects and re-measures the SSE2 variant on\n"
    "hardware against fair library baselines, closes the memory-safety\n"
    "classification at 100\\,\\% discharged-or-guarded, extends the\n"
    "non-interference proof to x25519 and MD5 under the stated\n"
    "lifter-soundness hypothesis, adds the edit-window and third-arm\n"
    "measurements, and neutralises the register of the academic text.\n",
    "le passage d'édition v0.21.0 (les deux phrases alignées)")

# ============ (C) LE REGISTRE NEUTRE =====================================
remplace("$N{=}7\\ge6$: \\emph{held}. The four-unit draw sequence was exhausted",
        "$N{=}7\\ge6$: \\emph{met}. The four-unit draw sequence was exhausted",
        "registre : held (critère d'échantillon)")
remplace("fresh M2 instrumentation of their own. The criterion is thus held",
        "fresh M2 instrumentation of their own. The criterion is thus met",
        "registre : held (le critère)")
remplace("OPT04 (19 November 2026): held, by the developer's explicit amendment}",
        "OPT04 (19 November 2026): met, by the developer's explicit amendment}",
        "registre : held (OPT04)")
remplace("asymmetry, as filed. \\emph{The verdict on the hypothesis --- held,",
        "asymmetry, as filed. \\emph{The verdict on the hypothesis --- met,",
        "registre : held (le verdict H5)")
remplace("the consigned per-unit figures read 51\\% (the second unit, held),",
        "the consigned per-unit figures read 51\\% (the second unit, met),",
        "registre : held (la seconde unité)")
remplace("locked and refused opens; the GO mode lived end-to-end (the empty",
        "locked and refused opens; the GO mode ran end-to-end (the empty",
        "registre : lived (le mode GO)")
remplace("by a test): the honest cycle across \\emph{five} lived epochs, fifteen",
        "by a test): the honest cycle across \\emph{five} successive epochs, fifteen",
        "registre : lived (les époques)")
remplace("\\code{fence.i} semantics on physical RISC-V silicon (the lived M7",
        "\\code{fence.i} semantics on physical RISC-V silicon (the executed M7",
        "registre : lived (le M7)")
remplace("it), and the D183 sequestration ceremony was then \\emph{lived",
        "it), and the D183 sequestration ceremony was then \\emph{carried out",
        "registre : lived (la cérémonie 1)")
remplace("threat model: the control passphrase lived in clear at the repository",
        "threat model: the control passphrase was stored in clear at the repository",
        "registre : lived (la phrase en clair)")
remplace("repository visibility matrix (private until the ceremony is lived and",
        "repository visibility matrix (private until the ceremony is carried out and",
        "registre : lived (la visibilité)")
remplace("and the developer then lived the third gesture: the D183 sequestration",
        "and the developer then carried out the third action: the D183 sequestration",
        "registre : lived (le troisième geste)")
remplace("faults lived in the shared judge, the piece never at fault at either",
        "faults resided in the shared judge, the piece never at fault at either",
        "registre : lived (les fautes du juge)")
remplace("waiting: the D183 escrow ceremony was lived end-to-end on 19 November",
        "waiting: the D183 escrow ceremony was carried out end-to-end on 19 November",
        "registre : lived (la cérémonie 2)")
remplace("the sample criterion held at $N{=}7$ without a new draw, the",
        "the sample criterion met at $N{=}7$ without a new draw, the",
        "registre : held (la conclusion 1)")
remplace("confrontation held at zero divergence; the local open-weights second",
        "confrontation met at zero divergence; the local open-weights second",
        "registre : held (la conclusion 2)")
remplace("the master's named amendment of the mof9q10vq rule, itself dated",
        "the developer's dated amendment of the mof9q10vq rule, itself dated",
        "registre : the master's (l'amendement)")
remplace("la re-mesure v0.19.6 tenue à l'identique par la vague 9,",
        "la re-mesure v0.19.6 reproduite à l'identique par le neuvième lot "
        "d'instructions,",
        "registre : le résumé français (tenue/vague)")

# ============ L'EXÉCUTION =================================================
def main() -> int:
    texte = SRC.read_text(encoding="utf-8")
    manquants = []
    for ancienne, nouvelle, nom in R:
        if ancienne not in texte:
            manquants.append(nom)
            continue
        if texte.count(ancienne) != 1:
            manquants.append(f"{nom} (ANCRE NON UNIQUE)")
            continue
        texte = texte.replace(ancienne, nouvelle)
    if manquants:
        print("REFUS — les ancres introuvables :")
        for m in manquants:
            print("  -", m)
        return 2
    # les macros v210 au lieu des v200
    texte = texte.replace("\\input{donnees/macros_v200}", "\\input{donnees/macros_v210}")
    DST.write_text(texte, encoding="utf-8")
    print(f"L'ÉDITION v0.21.0 : {len(R)} remplacements ancrés appliqués — "
          f"{DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
