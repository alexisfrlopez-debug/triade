#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v220.py — L'ÉDITION v0.22.0 DU MANUSCRIT née de la v0.21.0
par REMPLACEMENTS ANCRÉS (REFUS si une ancre manque — la méthode
établie). QUATRE FAMILLES :
  (A) LES CORRECTIONS SUR PIÈCES (zho5vilpy) : les ratios prose §7
      recalculés à une décimale (1,5× / 19,3× — la correction (b)), le
      ratio au plancher éditer AU MÊME TOKENIZER natif (la correction
      (c)), les headers/versions périmés (v0.22.0, la spec v0.15.7,
      l'état Data availability — la correction (d)), la conclusion RQ2
      alignée sur les formats adoptés (la correction (e));
  (B) LES RÉSULTATS DE LA VAGUE 11 portés : les couloirs SIMD, la
      boucle porteuse restructurée, le quatrième bras C+G+ (H-CGP2), la
      soundness du lifter au domaine (16 blocs), les gabarits
      versionnés, le coffre durci, les kits pré-enregistrés, la purge
      D81 ;
  (C) L'HISTORIQUE D'ÉDITION : la onzième vague a sa section (la date
      d'édition, l'abstract, la conclusion) ;
  (D) LE REGISTRE : le doublon typographique « and the / the » corrigé
      au passage (nommé)."""
from __future__ import annotations

import pathlib
import sys

SRC = pathlib.Path("/home/z/my-project/depot/edition-v0210/main.tex")
DST = pathlib.Path("/home/z/my-project/depot/edition-v0220/main.tex")
DST.parent.mkdir(parents=True, exist_ok=True)

R = []          # (ancienne, nouvelle, nom)


def remplace(ancienne: str, nouvelle: str, nom: str):
    R.append((ancienne, nouvelle, nom))


# ============ (A) LES CORRECTIONS SUR PIÈCES (zho5vilpy) ==================
remplace(
    "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand "
    "Under Signed-Intent Governance (Academic Edition v0.20.0)},",
    "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand "
    "Under Signed-Intent Governance (Academic Edition v0.22.0)},",
    "le pdftitle v0.22.0 (la correction (d))")

remplace(
    "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.20.0}",
    "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.22.0}",
    "le running header v0.22.0 (la correction (d))")

remplace(
    "described in the protocol specification v0.15.6, which this edition\n"
    "accompanies; we summarise only what the evaluation needs.",
    "described in the protocol specification v0.15.7 (the D81 purge "
    "edition: the five-thirds escrow is the active guard, the delivery "
    "instructions retired from the operational text), which this edition\n"
    "accompanies; we summarise only what the evaluation needs.",
    "la spécification courante v0.15.7 (la correction (d))")

remplace(
    "hand-written SSE2 notation sits \\emph{inside the class of the library's\n"
    "SIMD primitives} (1.6$\\times$ above the memchr idiom, 1.1$\\times$\n"
    "below \\code{memmem}), two orders below the compiled scalar path. The",
    "hand-written SSE2 notation sits \\emph{inside the class of the library's\n"
    "SIMD primitives} (1.5$\\times$ above the memchr idiom, 1.1$\\times$\n"
    "below \\code{memmem}), 19.3$\\times$ below the compiled scalar path\n"
    "--- both ratios restated at one decimal from the unrounded cycle\n"
    "counts (833/561 and 16{,}040/833; the prior edition's ``1.6$\\times$''\n"
    "and ``two orders'' were coarser roundings of the same measurements,\n"
    "corrected by the numeric linter of the present edition). The",
    "les ratios §7 à une décimale : 1,5× et 19,3× (la correction (b))")

remplace(
    "\\paragraph{Token cost.} The pointer-only localiser stands at a median\n"
    "of 1{,}103 tokens (response 52); the window editor at 1{,}146\n"
    "(response 40, a 53.3\\,\\% reduction of the edit total with the reread\n"
    "material down from 1{,}684 to 239 cl100k tokens --- the prescription\n"
    "prose now dominates, the next measured lever); the add operation's\n"
    "operational cost is the whole-notation path at 3{,}674 (the\n"
    "add-by-hunks format is refused for the third time, 0/18 --- reported\n"
    "as a refused format, never as the operation's cost); the floor\n"
    "ratios are 63.6$\\times$ (edit, window mode), 38.0$\\times$ (locate) and\n"
    "2.2$\\times$ (add, whole notation against the block-body floor) against\n"
    "the named floors (the real diff pair, the literal pointer, the block\n"
    "body).",
    "\\paragraph{Token cost.} The pointer-only localiser stands at a median\n"
    "of 1{,}053 native request tokens (the v0.21.0 \\mbox{total-perimeter} record\n"
    "of 1{,}103 dated alongside; $n{=}18$ at each wave); the hierarchical\n"
    "locator at 627 ($-40.5\\,\\%$: the coarse index of identifiers and\n"
    "short fingerprints first, then the fine pointer --- the expansion\n"
    "re-checked client-side); the templated editor at 674 ($-39.1\\,\\%$\n"
    "against the window re-measure at 1{,}106: the versioned template\n"
    "TPL-EDIT-v1 carries the format grammar once, its sha-256 engraved at\n"
    "the prompt, the prescription prose down 57\\,\\% --- 866 to 372 cl100k\n"
    "tokens, the lever the tenth wave had named); the add-by-skeleton at\n"
    "2{,}200 ($-28.5\\,\\%$ against the whole-notation 3{,}074 at the same\n"
    "perimeter, its feasibility 0 to 3 greens --- the fifteen honest\n"
    "out-of-format refusals remain, the gap named: the model must still\n"
    "learn the label and constant domain); the edit floor ratio is\n"
    "24.5$\\times$ at the \\emph{same} tokenizer --- the real diff pair\n"
    "re-tokenised through the campaign's own usage field (median 27.5\n"
    "native tokens over the eighteen tasks; the cl100k floor line --- 18\n"
    "tokens, the mixed ratio 63.6$\\times$ of the v0.21.0 edition ---\n"
    "remains dated history), the locate and add floors named as ever\n"
    "(the literal pointer, the block body).",
    "le paragraphe Token cost : les gabarits + le plancher natif/natif "
    "(les corrections (c) et les gabarits de la vague 11)")

remplace(
    "repository (append-only journal, decision log, evidence vault indexes,\n"
    "extraction script, generated tables) and in the versioned archival\n"
    "snapshots at the concept DOI \\doiConcept{} --- resolving to the latest\n"
    "archived version (v0.19.5 at this writing, version DOI\n"
    "\\doiVersionCourante{}; the earlier deposits 10.5281/zenodo.24367344\n"
    "and 10.5281/zenodo.24379173 are the dated v0.19.0 and v0.19.4\n"
    "archives; the distinction is consigned: the concept DOI is the\n"
    "citable reference, the version DOIs the dated records). This\n"
    "edition's own snapshot follows the developer's deposit gesture ---\n"
    "never minted without an explicit command. The two submission\n"
    "archives of the current deposit (\\code{TRIADE\\_soumission\\_v0.19.5.zip}\n"
    "and \\code{TRIADE\\_complet\\_v0.19.5.zip}) contain respectively the\n"
    "manuscript with its data tables, and the complete sources with raw\n"
    "extracts and fingerprints; every artifact of the claims tables was\n"
    "re-verified byte for byte against the regenerated archives (zero\n"
    "divergence).",
    "repository (append-only journal, decision log, evidence vault indexes,\n"
    "extraction script, generated tables) and in the versioned archival\n"
    "snapshots at the concept DOI \\doiConcept{} --- resolving to the latest\n"
    "archived version (v0.21.0 at this writing, version DOI\n"
    "\\doiVersionCourante{}; the earlier deposits 10.5281/zenodo.24367344,\n"
    "10.5281/zenodo.24379173 and 10.5281/zenodo.24382460 are the dated\n"
    "v0.19.0, v0.19.4 and v0.19.5 archives; the distinction is consigned:\n"
    "the concept DOI is the citable reference, the version DOIs the dated\n"
    "records). This edition's own snapshot follows the developer's deposit\n"
    "gesture --- never minted without an explicit command. The two\n"
    "submission archives of the current deposit\n"
    "(\\code{TRIADE\\_soumission\\_v0.22.0.zip} and\n"
    "\\code{TRIADE\\_complet\\_v0.22.0.zip}) contain respectively the\n"
    "manuscript with its data tables, and the complete sources with raw\n"
    "extracts and fingerprints; every artifact of the claims tables was\n"
    "re-verified byte for byte against the regenerated archives (zero\n"
    "divergence).",
    "l'état Data availability courant (la correction (d))")

# ============ (B)+(C) LA DATE D'ÉDITION : LA VAGUE ONZE ===================
remplace(
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
    "\\date{21 November 2026 — Academic edition v0.22.0 (the eleventh "
    "instruction batch: the cross-piece numeric linter extended to every "
    "numeral of the prose with the measured ratios restated at one "
    "decimal; the SIMD corridors measured on hardware --- the hybrid "
    "byte-search at 704 cycles inside the library's SIMD class, the "
    "SHA-NI body at 128.5 cycles per block; the AES-NI carrier loop "
    "restructured under its twelve-cycle target at 7.09 cycles per "
    "block; the fourth campaign arm separating the notation effect "
    "proper (55.7\\,\\%) from the verification regime (44.3\\,\\%); the "
    "lifter soundness established on its validated domain --- 942 "
    "encodings at zero divergence, the out-of-vocabulary guard "
    "fail-closed, sixteen blocks proven across seven families; the "
    "versioned templates cutting locate/edit/add again; the vault "
    "hardening proved on laboratory copies and the D81 delivery "
    "instructions purged from the operational documents)}",
    "la date d'édition v0.22.0 (la onzième vague a sa section)")

# ============ (A2) L'ABSTRACT RQ2 (la correction (e)) =====================
remplace(
    "(RQ2) the measured token cost\n"
    "per validated change --- under the adopted pointer-only localiser "
    "format a\n"
    "median of 1{,}103 tokens to locate a block ($n{=}18$, zero divergence, "
    "the\n"
    "response a median 52 tokens), 3{,}374 to edit one and 3{,}674 to add "
    "one\n"
    "(the hunk-format campaign measuring the edit at 2{,}452 with a "
    "40-token\n"
    "response), against a naive whole-disassembly baseline of 300{,}304, "
    "with\n"
    "the historical perimeters (M1, v0.14.0 content-only, v0.17.0 "
    "round-trip)\n"
    "explicitly labelled; (RQ3)",
    "(RQ2) the measured token cost\n"
    "per validated change --- under the adopted formats a median of "
    "1{,}053\n"
    "native request tokens to locate a block ($n{=}18$; the hierarchical\n"
    "locator at 627), 674 to edit one (the versioned template carrying "
    "the\n"
    "format grammar once, the prescription prose down 57\\,\\%) and "
    "2{,}200\n"
    "to add one (the skeleton format, its feasibility 0 to 3 greens --- "
    "the\n"
    "gap named), against a naive whole-disassembly baseline of "
    "300{,}304,\n"
    "with the historical perimeters (M1, v0.14.0 content-only, v0.17.0\n"
    "round-trip, the v0.21.0 window perimeter) explicitly labelled; (RQ3)",
    "l'abstract RQ2 aligné aux formats adoptés (la correction (e))")

remplace(
    "naïve de 300~304 ;",
    "naïve de 300~304 ; le onzième lot affine les trois formats — le "
    "localisateur hiérarchique à 627 natifs (−40,5 %), le gabarit "
    "versionné à 674 (−39,1 %, la prose de prescription −57 %), l'ajout "
    "par squelette à 2~200 (−28,5 %, la faisabilité 0→3 verts — l'écart "
    "nommé), chaque périmètre étiqueté ;",
    "l'abstract français RQ2 : les gabarits de la vague 11 (la correction "
    "(e))")

# ============ (C) L'HISTORIQUE D'ÉDITION À L'ABSTRACT =====================
remplace(
    "performance lanes. The present edition (v0.21.0) reconciles the\n"
    "abstract with the body, corrects and re-measures the SSE2 variant on\n"
    "hardware against fair library baselines, closes the memory-safety\n"
    "classification at 100\\,\\% discharged-or-guarded, extends the\n"
    "non-interference proof to x25519 and MD5 under the stated\n"
    "lifter-soundness hypothesis, adds the edit-window and third-arm\n"
    "measurements, and neutralises the register of the academic text.",
    "performance lanes. The v0.21.0 edition reconciled the abstract with\n"
    "the body, corrected and re-measured the SSE2 variant on hardware\n"
    "against fair library baselines, closed the memory-safety\n"
    "classification at 100\\,\\% discharged-or-guarded, extended the\n"
    "non-interference proof to x25519 and MD5 under the stated\n"
    "lifter-soundness hypothesis, added the edit-window and third-arm\n"
    "measurements, and neutralised the register of the academic text. The\n"
    "present edition (v0.22.0) carries the eleventh instruction wave: the\n"
    "SIMD corridors measured on hardware, the AES-NI carrier loop\n"
    "restructured under its twelve-cycle target, the fourth campaign arm\n"
    "separating the notation effect proper from the verification regime,\n"
    "the lifter soundness established on its validated domain, the\n"
    "versioned templates cutting the token budgets again, the vault\n"
    "hardening proved on laboratory copies with the D81 delivery\n"
    "instructions purged from the operational documents, and the "
    "cross-piece\n"
    "numeric linter extended to every numeral of the prose.",
    "l'historique d'édition : la onzième vague à l'abstract")

# ============ (B) LES RÉSULTATS DE LA VAGUE 11 ============================

# ---- la non-interférence : 16 blocs + la soundness du lifter au domaine --
remplace(
    "(\\cfTroisObligations{} obligations, certificates archived), and the\n"
    "the static non-interference proof covers 13 blocks across seven\n"
    "crypto families, restated as proven under the explicit lifter-\n"
    "soundness hypothesis (the IR-to-notation round-trip verifies the\n"
    "hypothesis on every covered block), with the negative control\n"
    "caught.",
    "(\\cfTroisObligations{} obligations, certificates archived), and the\n"
    "static non-interference proof covers 16 blocks across seven crypto\n"
    "families (the eleventh wave adds tls13-04 at the refined model ---\n"
    "the state secret, the total length a named public metadata --- and\n"
    "tls13-08), proven under the lifter-soundness hypothesis --- which "
    "the\n"
    "eleventh wave establishes \\emph{on its validated domain}: 942 "
    "distinct\n"
    "encodings confronted at zero divergence by the exact method (the\n"
    "writes observed at the diff and the write hooks, the reads by the\n"
    "differential sentinel), and a 7{,}769-mutant corpus whose 155\n"
    "divergences are \\emph{all} out-of-vocabulary --- the guard that\n"
    "follows: the lifter declares its soundness over the modelled classes\n"
    "and refuses any unmodelled class at load time (fail-closed, the\n"
    "refusal named). The GHASH key~H is covered as a secret (tls13-17 at\n"
    "the third argument: neither branch nor address tainted); the\n"
    "negative control caught in both directions.",
    "la non-interférence : 16 blocs + la soundness du lifter au domaine "
    "(le doublon « and the / the » corrigé au passage — nommé)")

# ---- l'Optimisation : le cache de round-trip + la cristallisation --------
remplace(
    "tenth batch adds the edit window (OPT-10: the reread material down\n"
    "7.0$\\times$, the total median 2{,}452 to 1{,}146 at $n{=}18$ with the\n"
    "independent re-tokenisation at zero drift and the pointer's four\n"
    "named refusals re-verified fail-closed).",
    "tenth batch adds the edit window (OPT-10: the reread material down\n"
    "7.0$\\times$, the total median 2{,}452 to 1{,}146 at $n{=}18$ with the\n"
    "independent re-tokenisation at zero drift and the pointer's four\n"
    "named refusals re-verified fail-closed); the eleventh batch adds "
    "the\n"
    "round-trip verdict cache (the key bound to the notation, the engine\n"
    "and the profile --- a hit returns the verdict without re-execution,\n"
    "the session-opening re-verification 283.7 to 0.4\\,ms, a 680.6$\\times$\n"
    "gain, every key divergence forcing the complete re-verification\n"
    "back) and the incremental crystallisation (the transitive closure "
    "of\n"
    "the real diff alone re-verified: 13 of 28 blocks, $-54\\,\\%$ of the\n"
    "verification post --- the 1-in-10 audit named a probabilistic net,\n"
    "never a proof; the capture demonstrated at the sought seed).",
    "l'Optimisation : le cache de round-trip 680,6× + la cristallisation "
    "incrémentale −54 %")

# ---- la lecture lexicographique : la onzième vague -----------------------
remplace(
    "\\paragraph{Lexicographic reading.} No compensation between ranks: "
    "each\n"
    "axis is reported for itself, and the tenth instruction batch "
    "improved\n"
    "the security rank without conceding performance, verification\n"
    "strength or token cost.",
    "\\paragraph{Lexicographic reading.} No compensation between ranks: "
    "each\n"
    "axis is reported for itself, and the eleventh instruction batch\n"
    "improved the security rank (the D81 purge, the vault hardening, the\n"
    "lifter guard) without conceding performance (the corridors and the\n"
    "carrier loop), verification strength (the four arms reconciled at\n"
    "zero drift) or token cost (the templates).",
    "la lecture lexicographique : la onzième vague")

# ---- LE QUATRIÈME BRAS (le paragraphe nouveau) ---------------------------
remplace(
    "campaign's own precedent for a unit closed at the cap, reported as\n"
    "such. The human-time metric is not measurable in the laboratory and\n"
    "awaits the developer's field run; no value is fabricated.\n",
    "campaign's own precedent for a unit closed at the cap, reported as\n"
    "such. The human-time metric is not measurable in the laboratory and\n"
    "awaits the developer's field run; no value is fabricated.\n"
    "\n"
    "\\paragraph{The fourth arm: the notation effect proper.} The fourth\n"
    "campaign arm (C+G+: the compiled C receiving the governance stack\n"
    "\\emph{and} the complete verification regime of the notation arm ---\n"
    "ten rebuilds per unit confronted at the byte, equal oracle volumes,\n"
    "the plan recomposition at every delivery) settles the "
    "requalification\n"
    "question the third arm left open. Measured on the same machine at\n"
    "$n{=}5$ per arm, order alternated against thermal drift: T\n"
    "\\quatreBrasT{}\\,s, C+G+ \\quatreBrasCGP{}\\,s, C+G \\quatreBrasCG{}\\,s, "
    "C\n"
    "\\quatreBrasC{}\\,s --- the notation effect \\emph{proper} "
    "(T$-$C+G+) is\n"
    "\\effetNotationPropre{}\\,s (\\partNotationPropre\\,\\% of T$-$C+G), the\n"
    "verification regime (C+G+$-$C+G) \\effetRegime{}\\,s "
    "(\\partRegime\\,\\%),\n"
    "the governance gestures \\effetGouvernanceOnze{}\\,s: the "
    "pre-registered\n"
    "H-CGP2 is confirmed --- the requalification rejected at both windows\n"
    "(the paired session and the wave-10 reference) --- and the\n"
    "three-effect ventilation closes exactly (\\effetNotationPropre{} $+$\n"
    "\\effetRegime{} $+$ \\effetGouvernanceOnze{} $=$ T$-$C at the "
    "millisecond).\n"
    "At equal oracle volumes the notation arm's living oracles cost "
    "33.48\\,s\n"
    "against 0.51\\,s compiled (the re-execution of the assembled "
    "notation\n"
    "under emulation against the compiled piece's native run, 66$\\times$);\n"
    "the notation session decomposed post by post attributes "
    "\\oraclesPart\\,\\%\n"
    "of its 43.7\\,s to the oracles --- the regime's cost is dominated "
    "by\n"
    "the verification volumes, not the writing.\n",
    "le quatrième bras C+G+ : la ventilation trois-effets (H-CGP2 "
    "confirmée)")

# ---- LES COULOIRS SIMD + LA BOUCLE PORTEUSE (les paragraphes nouveaux) ---
remplace(
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
    "(statically sound / bounded / guarded); zero out-of-frame accesses.\n"
    "\n"
    "\\paragraph{The SIMD corridors.} The three corridors are measured "
    "on\n"
    "hardware (RDTSC, pinned core, the sealed margins intact, the "
    "battery\n"
    "of \\batterieVecteurs{} vectors per search corridor --- buffer tails "
    "at\n"
    "every alignment, overlapping patterns, lengths 1--33, page\n"
    "boundaries, multiple occurrences, 512 property-based at the "
    "consigned\n"
    "seed --- at zero divergence): the hybrid memchr+memcmp byte-search "
    "at\n"
    "\\hybrideCycles{} cycles [IQR \\hybrideIqr{}] per absent "
    "4{,}096-byte\n"
    "search, \\hybrideGain{} below the sealed GPR notation "
    "(\\scelleGprCycles{})\n"
    "--- inside the class of the library's SIMD primitives; the SHA-NI\n"
    "compression body at \\shaniCorpsCbloc{} cycles per block "
    "(\\shaniGain{}\n"
    "below the sealed SHA-256 at equal work, the dispatch hoisted out "
    "of\n"
    "the loop, 202 cycles named); the AVX2 corridor dominated by its\n"
    "CPUID polling at the virtualised laboratory (the probe costs\n"
    "$\\approx$\\cpuidSondage{} cycles per call --- the hoisting to one "
    "probe\n"
    "per session is the named condition of its use; 5{,}846 cycles "
    "measured\n"
    "as sealed, the gap named).\n"
    "\n"
    "\\paragraph{The carrier loop restructured.} The AES-NI carrier "
    "loop\n"
    "of the GCM seal reaches \\porteuseVquatreInline{} cycles per block "
    "[IQR\n"
    "\\porteuseVquatreIqr{}] in its inline form (the key schedule "
    "exposed\n"
    "at independent addresses, the block body in the loop, no call): "
    "the\n"
    "pre-registered target of $\\le$\\porteuseCible{} cycles per block\n"
    "envelope included is \\emph{met}, a \\porteuseGain{} gain over the "
    "v2\n"
    "flow at \\porteuseVdeuxFlux{} --- joining the class of the "
    "compiler-called sealed block (7.62); the variants that did not "
    "break\n"
    "the dependency chain are named (the address table 53.11, the "
    "unrolling alone 53.17 --- the independent addressing mode is the\n"
    "lever, not the precomputation). The FIPS~197 key-schedule parity\n"
    "holds byte for byte at 256/256, the mutated-unrolling negative\n"
    "control caught at the first vector, the out-of-bound count "
    "refused\n"
    "fail-closed (nothing encrypted past the bound).\n"
    "\n"
    "\\paragraph{The vault hardened on laboratory copies.} The seven\n"
    "hardening gestures (a)--(g) are proved on laboratory copies at the\n"
    "public control passphrase (no real vault, no real phrase --- the\n"
    "absolute rule): the ciphertext fingerprint bound to the key and\n"
    "verified \\emph{before} the AEAD (corruption refused without\n"
    "destruction, falsification under a valid naive fingerprint "
    "destroyed\n"
    "with a formal report), the trap derivation epoch-bound (the\n"
    "anti-rollback extended to the trap), the Argon2 re-parametering\n"
    "ceremony versioned (the entropy floor verified: the strong "
    "passphrase\n"
    "admitted at 184 bits against the 60-bit gate, three weak ones\n"
    "refused), the phrase change under three-part escrow (the old "
    "phrase\n"
    "inoperant), the RAM guard specified and demonstrated (mlock,\n"
    "explicit zeroing verified byte for byte, the dumpable flag "
    "cleared),\n"
    "the epoch-witness anchoring and the FIDO2 prototype specified --- "
    "the\n"
    "network gesture and the physical token awaiting the developer's\n"
    "command, the gaps named. A z3 state machine proves the four\n"
    "invariants of the sentinel (the control names the unguarded "
    "machine\n"
    "where corruption destroys). The D81 delivery instructions are\n"
    "purged from the operational documents (the Book of the Vault v1.6\n"
    "and the specification v0.15.7: the five-thirds escrow is the "
    "active\n"
    "guard, the repository public --- the runbook simulation refused "
    "the\n"
    "trap gesture at the first named step, the \\purgeCommitsScannes{}-"
    "commit\n"
    "history scan found zero leak).\n"
    "\n"
    "\\paragraph{The pre-registered kits.} Six kits close the "
    "``awaiting''\n"
    "lines of the evidence tables \\emph{without producing a result} "
    "(the\n"
    "rule): the RISC-V \\code{fence.i} silicon probe, the "
    "third-machine\n"
    "Loupe run, the dudect replications at three sample sizes, the\n"
    "stratified H7 hypothesis, the second annotator at the pre-registered\n"
    "$\\kappa$, and the CF3 Tamarin model --- thirty fingerprints "
    "consigned\n"
    "before delivery, the 57 autotest checks green, no measurement "
    "taken\n"
    "(the developer's gesture remains the only source of terrain "
    "evidence).\n",
    "les paragraphes nouveaux : les couloirs SIMD, la boucle porteuse, "
    "le coffre durci, les kits pré-enregistrés")

# ============ (A3) LA CONCLUSION RQ2 (la correction (e)) ==================
remplace(
    "append-only records, quantifies the cost (medians of 1{,}277/3{,}374/\n"
    "3{,}674 tokens per locate/edit/add at the instrumented-round-trip\n"
    "perimeter; the content-only and M1 values remain labelled history), "
    "the",
    "append-only records, quantifies the cost (the adopted formats at "
    "the\n"
    "eleventh wave: the pointer-only localiser of D222 at 1{,}053 native\n"
    "request tokens, refined to the hierarchical locator at 627; the "
    "edit\n"
    "window of OPT-10 --- the decision taken, the format adopted ---\n"
    "refined to the versioned template at 674; the add skeleton at\n"
    "2{,}200 with its feasibility gap named; the earlier perimeters --- "
    "M1,\n"
    "content-only, full round-trip, whole-notation --- remain labelled\n"
    "history), the",
    "la conclusion RQ2 alignée (la correction (e))")

# ============ (C) LA CONCLUSION : LA ONZIÈME VAGUE ========================
remplace(
    "full-history secrets scan re-tried (ten findings triaged, no real\n"
    "token ever committed), the repository made public at decision D220 "
    "and\n"
    "joined by the Zenodo version DOI.",
    "full-history secrets scan re-tried (ten findings triaged, no real\n"
    "token ever committed), the repository made public at decision D220 "
    "and\n"
    "joined by the Zenodo version DOI. The eleventh wave closes the "
    "debts\n"
    "the tenth opened: the requalification rejected at the fourth arm "
    "(the\n"
    "notation effect proper \\partNotationPropre\\,\\% of the residual, "
    "the\n"
    "verification regime \\partRegime\\,\\%, the governance "
    "\\effetGouvernanceOnze\\,s),\n"
    "the carrier loop under its target, the corridors measured, the "
    "lifter\n"
    "sound on its domain, the templates cutting the budgets again --- "
    "and\n"
    "the operational documents purged of the delivery instructions the\n"
    "public repository can no longer carry.",
    "la conclusion : la onzième vague")

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
    # les macros v220 au lieu des v210
    texte = texte.replace("\\input{donnees/macros_v210}", "\\input{donnees/macros_v220}")
    DST.write_text(texte, encoding="utf-8")
    print(f"L'ÉDITION v0.22.0 : {len(R)} remplacements ancrés appliqués — "
          f"{DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
