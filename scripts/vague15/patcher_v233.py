#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_v233.py — LA GÉNÉRATION v0.23.3 (la release de la vague 15 — la
commande du maître « ok pour la suite (release de la vague etc…) » : LES
CINQ PIÈCES RÉGÉNÉRÉES au linter v2, l'atelier vxf37231r). LES GESTES :
(1) LE LINTER v2 PORTÉ AUX SOURCES — (A) la phrase sémantique « le
compilateur disparaît » RETIRÉE de la spec §1 (la formulation exacte
D182 : le compilateur N'EST JAMAIS LIVRÉ, la notation scellée l'est) et
les DEUX mentions citées reformulées sans la forme littérale ; (C) les
séquences de faisabilité n/18 DATÉES partout (le marqueur 2026 avant
chaque valeur, la campagne v5 nommée à part) ; (D) le claim de version
post-dépôt porté à la v0.23.2 courante ; (E) les gallicismes EN («
tranchée » → « settled », « five-thirds escrow » → la formulation
anglaise exigée). (2) L'ÉTAT PORTÉ À v0.23.3 (les en-têtes, la bannière,
les abstracts EN/FR, le changelog, la disponibilité des données au DOI
v0.23.2, la plage d'Entrées 305–387, le Livre v1.7 daté). (3) LA VAGUE
15 AU CORPS (la composition 0,7271 c/octet@4096, le TCB 58→34→11 et le
corridor des onze, le moteur d'oracles natif 5189×, TPL-ADD-v5 5/18 LA
CIBLE MANQUÉE, H7 servie + le second annotateur + le confound, CF3-v3
au verdict machine, l'écosystème d'adoption : le corpus 109, le gym,
la ladder, le guide, la doc EN, le kit 156 pièces). CHAQUE
remplacement ANCRÉ — REFUS si une ancre manque ou est ambiguë."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/depot")

PATCHES: list[tuple[str, str, str, str]] = []


def p(fichier, ancien, nouveau, nom):
    PATCHES.append((fichier, ancien, nouveau, nom))


M = "edition-v0230/main.tex"
S = "edition-v0230/donnees/statuts_v230.tex"

# ===========================================================================
# (1) LE MANUSCRIT — les en-têtes à v0.23.3
# ===========================================================================
p(M,
  "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under "
  "Signed-Intent Governance (Academic Edition v0.23.2)},",
  "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under "
  "Signed-Intent Governance (Academic Edition v0.23.3)},",
  "le pdftitle à v0.23.3")

p(M,
  "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.23.2}",
  "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.23.3}",
  "le running header à v0.23.3")

p(M,
  "\\date{22 November 2026 — Academic edition v0.23.2 (the present edition ",
  "\\date{23 November 2026 — Academic edition v0.23.3 (the present edition ",
  "la date de bannière au 23 novembre 2026")

# la bannière de date : la génération v0.23.3 (la vague 15 au résumé)
p(M,
  "the corrective generation of the fourteenth wave: the ten sourced "
  "corrections (a)--(j) carried to the five documents --- the wave-13 "
  "GHASH corridor restated at its adopted schoolbook canon 63.39 cycles "
  "[IQR 30] against the sealed 806.35, a $12.7\\times$ gain --- and every "
  "published ratio now carrying its unrounded operands; the fourteenth "
  "instruction batch carried: the GHASH aggregation at four blocks with "
  "deferred reduction at 19.66 cycles per multiplication [IQR 19] --- a "
  "$41.0\\times$ gain on the sealed 806.35 and $3.23\\times$ on the "
  "wave-13 corridor ($63.39/19.66$); the content-addressed memoisation of "
  "the regime at $-89.4$ per cent (the unrounded medians 24.163 $\\to$ "
  "2.555~s, no control removed --- H-CGP4 held); the TPL-ADD-v4 "
  "counter-example repair converting its first honest refusal at 7/18 "
  "greens for a median 3,990 tokens; the H7 replication order drawn and "
  "signed --- the campaign open to the 28 units; the CF3 Tamarin model v2 "
  "run at the first effective proof --- the implication lemma falsified "
  "by a named modelling defect (the shares as public variables), the "
  "amendment written and re-hashed, no verdict fabricated; the "
  "cross-piece numeric linter extended to the version strings, the "
  "recomposed decompositions, the ratio operands and the dated T/X "
  "labels)}",
  "the release of\n"
  "the fifteenth wave: the interleaved CTR$\\times$GHASH composition\n"
  "measured at 0.7271 cycles per byte at 4\\,KiB (the median 2{,}978.2\n"
  "cycles per 4{,}096-byte call; the pre-registered target of 2.0 held\n"
  "at 36 per cent; OpenSSL EVP at 0.5757 --- 2{,}357.9 cycles --- on the\n"
  "same silicon, the corridor within $1.26\\times$ of the tuned library;\n"
  "the sealed per-block chain $68.7\\times$ behind --- 204{,}544.5\n"
  "against 2{,}978.2 cycles --- no control removed); the\n"
  "guard TCB reduced $58\\to34\\to11$ (the eleven OS assumptions named,\n"
  "the eleven-guard corridor emitted at the virgin margin 0xFC00 --- 424\n"
  "bytes, the falsified guard refused at both boundaries and on the index\n"
  "face, the harness 36/36; the rejeu of the 116 certificates consigned at\n"
  "its corrected invocation, the first-pass invocation bug named in an\n"
  "append-only erratum); the native oracle engine line-identical to the\n"
  "Unicorn twin on both sealed crypto bodies (the content-addressed memo,\n"
  "the gate, the chained 1-in-10 audit; the medians 0.960\\,ms $\\to$\n"
  "0.000185\\,ms at the hit, a $5189\\times$ gain at the unrounded\n"
  "operands, the mechanisms orthogonal to the regime memoisation); the\n"
  "Nov 2026 TPL-ADD-v5 campaign (the structured expansion diff) at\n"
  "5/18 greens --- the Nov 2026 pre-registered target of\n"
  "$\\ge$15/18 missed, the unfavourable reading\n"
  "consigned (the subject's CLI variance named, the judges intact); the\n"
  "adoption-side ecosystem assembled by construction (the training corpus\n"
  "of 109 triples with sealed splits, the typed-reward training\n"
  "environment, the re-playable capability ladder, the model-independent\n"
  "agent guide, the canonical-English documentation core, the 156-piece\n"
  "developer kit with no trust anchor shipped); and the cross-piece\n"
  "linter extended to the five new classes (the semantic phrases, the\n"
  "decision ranges, the dated feasibility sequences, the post-deposit\n"
  "version claims, the English gallicisms) --- the five documents\n"
  "regenerated under it)}",
  "la bannière de date : la génération v0.23.3 (la vague 15)")

# ===========================================================================
# (2) LE MANUSCRIT — les abstracts EN/FR (l'état courant en une voix)
# ===========================================================================
p(M,
  "edition (v0.23.2) restates the programme in one voice and carries\n"
  "the twelfth to fourteenth waves: the GHASH corridor in PCLMULQDQ\n",
  "edition (v0.23.3) restates the programme in one voice and carries\n"
  "the twelfth to fifteenth waves: the GHASH corridor in PCLMULQDQ\n",
  "l'abstract EN : l'édition v0.23.3, les vagues 12-15")

# (C) les séquences de faisabilité DATÉES + la campagne v5 nommée à part
p(M,
  "feasibility 3/18 at waves 11-12, 6/18 at the thirteenth, then 7/18 at\n"
  "the fourteenth --- the counter-example repair converting its first\n"
  "honest refusal; the gap named by refusal class)",
  "the 2026 feasibility record: 3/18 at waves 11-12, 6/18 at the\n"
  "thirteenth (2026), then 7/18 at the fourteenth --- the counter-example\n"
  "repair converting its first honest refusal; the fifth version's\n"
  "campaign (Nov 2026) at 5/18, its pre-registered target missed and the\n"
  "unfavourable reading consigned; the gap named by refusal class)",
  "l'abstract EN : la faisabilité datée + la v5 (la cible manquée)")

p(M,
  "grammar with its repair loop (feasibility 3/18, then 5/18, then\n"
  "6/18, then 7/18 at the fourth version --- the counter-example repair\n"
  "converting its first honest refusal), the three requalifications (the\n"
  "58 memory-safety guards conditional assumption-discharged, the fifteen\n"
  "mutant exclusions proved-argued-bounded, the CF3 Tamarin model v2\n"
  "without the adversary restriction)",
  "grammar with its repair loop (the 2026 record: 3/18, then 5/18, then\n"
  "6/18, then 7/18 at the fourth version --- the counter-example repair\n"
  "converting its first honest refusal; the fifth campaign (Nov 2026) at\n"
  "5/18, the target missed, the reading consigned), the three\n"
  "requalifications (the 58 memory-safety guards conditional\n"
  "assumption-discharged, the fifteen mutant exclusions\n"
  "proved-argued-bounded, the CF3 Tamarin model v2 without the adversary\n"
  "restriction)",
  "l'abstract EN : la séquence de faisabilité datée + la v5")

# l'abstract EN : la vague 15 portée (la phrase ajoutée après la 14)
p(M,
  "drawn and signed H7 replication order (the campaign open to the 28\n"
  "units), the first effective Tamarin run (the implication lemma\n"
  "falsified by a named modelling defect, the amendment written, no\n"
  "verdict fabricated), and this corrective generation itself --- the ten\n"
  "sourced corrections (a)--(j) carried to the five documents, every\n"
  "published ratio at its unrounded operands.",
  "drawn and signed H7 replication order (the campaign open to the 28\n"
  "units), the first effective Tamarin run (the implication lemma\n"
  "falsified by a named modelling defect, the amendment written, no\n"
  "verdict fabricated), and this corrective generation itself --- the ten\n"
  "sourced corrections (a)--(j) carried to the five documents, every\n"
  "published ratio at its unrounded operands. The fifteenth wave adds:\n"
  "the interleaved CTR$\\times$GHASH composition measured at 0.7271\n"
  "cycles per byte at 4\\,KiB (the median 2{,}978.2 cycles per 4{,}096-\n"
  "byte call; the pre-registered target of 2.0 held at 36 per cent;\n"
  "OpenSSL EVP at 0.5757 --- 2{,}357.9 cycles --- on the same silicon,\n"
  "the corridor within $1.26\\times$ of the tuned library; the sealed\n"
  "per-block chain $68.7\\times$ behind --- 204{,}544.5 against\n"
  "2{,}978.2 cycles --- no control removed); the guard TCB reduced $58\\to34\\to11$ with the eleven OS guards emitted as a\n"
  "real corridor at the virgin margin 0xFC00 (the falsified guard refused\n"
  "at both boundaries and on the index face, the harness 36/36); the\n"
  "native oracle engine line-identical to the Unicorn twin on both sealed\n"
  "crypto bodies (the medians 0.960\\,ms $\\to$ 0.000185\\,ms at the hit,\n"
  "a $5189\\times$ gain at the unrounded operands); the TPL-ADD-v5\n"
  "structured expansion diff (Nov 2026) at 5/18 greens (the pre-registered\n"
  "target missed, the unfavourable reading consigned --- the subject's CLI\n"
  "variance named, the judges intact); and the adoption-side ecosystem\n"
  "assembled by construction (the 109-triple corpus, the typed-reward\n"
  "gym, the capability ladder, the agent guide, the English doc core,\n"
  "the 156-piece kit --- no trust anchor shipped).",
  "l'abstract EN : la vague 15 portée")

# (C) le résumé FR : la faisabilité datée + la v5
p(M,
  "la faisabilité 3/18 aux vagues 11-12, 6/18 à la treizième puis 7/18 à la "
  "quatorzième (la boucle de contre-exemple convertit son premier refus "
  "honnête) — l'écart nommé par classe de refus)",
  "la faisabilité 2026 : 3/18 aux vagues 11-12, 6/18 à la treizième "
  "(2026), puis 7/18 à la quatorzième (la boucle de contre-exemple "
  "convertit son premier refus honnête) ; la campagne v5 (nov. 2026) à "
  "5/18 — la cible manquée, la lecture défavorable consignée — l'écart "
  "nommé par classe de refus)",
  "le résumé FR : la faisabilité datée + la v5 (la cible manquée)")

# ===========================================================================
# (3) LE MANUSCRIT — le corps : la vague 15 portée
# ===========================================================================
# (C) le compte d'échantillons M4 daté (le marqueur avant le n/18)
p(M,
  "as complete instrumented round-trips with the model's native tokenizer\n"
  "(the usage log of every call, the $\\times$1.08 estimation abandoned),\n"
  "$n{=}18/18/15$ real samples (the card's own blocks and contracts, seed\n"
  "consigned in the pre-registered plan \\code{ede70035\\ldots}),",
  "as complete instrumented round-trips with the model's native tokenizer\n"
  "(the usage log of every call, the $\\times$1.08 estimation abandoned),\n"
  "the 2026 measurement at $n{=}18/18/15$ real samples (the card's own\n"
  "blocks and contracts, seed consigned in the pre-registered plan\n"
  "\\code{ede70035\\ldots}),",
  "(C) le compte M4 n=18/18/15 daté")

# RQ2 : la cinquième passe (5/18, 4 604, la cible manquée, la variance)
p(M,
  "repair converts its first (loupe-11) at 7/18 for a median 3{,}990\n"
  "tokens; the third pass measures 3{,}844 tokens per validated change at\n"
  "6/18, 18/18 for the edit operation at 712), the residual gap named by\n"
  "refusal class at the third pass (nine expansion-divergent, two\n"
  "out-of-format, one unknown-id): the gap has moved from domain",
  "repair converts its first (loupe-11) at 7/18 for a median 3{,}990\n"
  "tokens; the third pass measures 3{,}844 tokens per validated change at\n"
  "(2026) 6/18, (2026) 18/18 for the edit operation at 712), the fifth\n"
  "campaign (the structured expansion diff at\n"
  "opcode/operand/offset --- the line as written, its expansion at the\n"
  "exact point it breaks, the canonical pattern admitted; Nov 2026) at\n"
  "5/18 for a median\n"
  "4{,}604 tokens: the\n"
  "Nov 2026 pre-registered target of $\\ge$15/18\n"
  "missed, the cost target of $\\le$4{,}500 missed by 104 --- the\n"
  "unfavourable reading consigned, never a number adjusted, never a\n"
  "target re-drawn; the named cause is the subject's CLI variance (the\n"
  "three wave-14 greens lost at identical prompts, the judges intact, the\n"
  "chronic refusals unconverted --- the free-text HORS-FORMAT class\n"
  "remains), the residual gap named by\n"
  "refusal class at the third pass (nine expansion-divergent, two\n"
  "out-of-format, one unknown-id): the gap has moved from domain",
  "le corps RQ2 : la cinquième passe (5/18, 4 604, la cible manquée)")

# la table canonique : la cinquième passe + les canons de vérification v15
p(M,
  "skeleton (measured OPT-14; feasibility 3/18, then 5/18 at the twelfth "
  "wave, then 6/18 at the thirteenth, then 7/18 at the fourteenth --- the "
  "wave-13 repair loop converts none, the wave-14 counter-example repair "
  "converts its first (loupe-11); the gap named by refusal class; the "
  "thirteenth wave measures 3{,}844 per validated change, the fourteenth "
  "3{,}990)",
  "skeleton (measured OPT-14; the 2026 record: 3/18, then 5/18 at the "
  "twelfth wave, then 6/18 at the thirteenth (2026), then 7/18 at the "
  "fourteenth --- the wave-13 repair loop converts none, the wave-14 "
  "counter-example repair converts its first (loupe-11); the fifth "
  "campaign (Nov 2026) at 5/18, its target missed and the reading "
  "consigned; the gap named by refusal class; the thirteenth wave "
  "measures 3{,}844 per validated change, the fourteenth 3{,}990, the "
  "fifth 4{,}604)",
  "la table canonique : la cinquième passe (5/18, 4 604)")

p(M,
  "edit 1{,}106 $\\to$ \\gabaritEditerApres{} (TPL-EDIT-v1, adopted "
  "OPT-14; the thirteenth wave's repair loop measures 712 per validated "
  "change at 18/18)",
  "edit 1{,}106 $\\to$ \\gabaritEditerApres{} (TPL-EDIT-v1, adopted "
  "OPT-14; the thirteenth wave's repair loop measures 712 per validated "
  "change at (2026) 18/18)",
  "la table canonique : le 18/18 d'éditer daté")

p(M,
  "The verification-side canons at unrounded operands: the round-trip "
  "cache 285.725 ms $\\to$ 0.418 ms at the oracle opening (a "
  "683.6$\\times$ gain, the key bound to the notation, the engine and "
  "the profile); the wave-eleven regime ratio 39.24/2.163 $=$ "
  "18.1$\\times$.",
  "The verification-side canons at unrounded operands: the round-trip "
  "cache 285.725 ms $\\to$ 0.418 ms at the oracle opening (a "
  "683.6$\\times$ gain, the key bound to the notation, the engine and "
  "the profile); the wave-eleven regime ratio 39.24/2.163 $=$ "
  "18.1$\\times$; the fifteenth wave's native oracle engine at 0.960 ms "
  "$\\to$ 0.000185 ms on the memo hit (a $5189\\times$ gain recomputed "
  "at the unrounded medians, the engine line-identical to the Unicorn "
  "twin on both sealed crypto bodies, the mechanisms orthogonal to the "
  "regime memoisation and the incremental crystallisation); the "
  "interleaved CTR$\\times$GHASH composition at 0.7271 cycles per byte "
  "at 4\\,KiB (2{,}978.2 cycles [IQR 5.6] per 4{,}096-byte call, $n{=}20$ "
  "on the pinned core; the pre-registered target of 2.0 held at 36 per "
  "cent; OpenSSL EVP at 0.5757 (2{,}357.9 cycles [IQR 19.3]) --- the "
  "corridor within $1.26\\times$ of the tuned library; the sealed "
  "per-block chain at 49.9376 (204{,}544.5 cycles) --- "
  "$68.7\\times$ behind, no control removed; the parity at the rig "
  "itself: the corridor and the fallback produce the same 4{,}112 bytes "
  "on the rig's input, the guard green before the measurement).",
  "la table canonique : les canons de vérification de la vague 15")

# le TCB : le registre par étages + le corridor des onze + l'erratum
p(M,
  "(the OPT-01 margin-$0\\times$10000 model, never in the sealed\n"
  "binary): a two-sided check proven by an UNSAT certificate per guard\n"
  "(58/58 re-verified), falsified per guard in the laboratory variant\n"
  "(the violated invariant is refused at both zone boundaries and on\n"
  "the index face, the honest address admitted). Every access carries\n"
  "its proof-strength label (statically sound / bounded /\n"
  "conditional-assumption-discharged); zero out-of-frame accesses.",
  "(the OPT-01 margin-$0\\times$10000 model, never in the sealed\n"
  "binary): a two-sided check proven by an UNSAT certificate per guard\n"
  "(58/58 re-verified), falsified per guard in the laboratory variant\n"
  "(the violated invariant is refused at both zone boundaries and on\n"
  "the index face, the honest address admitted). Every access carries\n"
  "its proof-strength label (statically sound / bounded /\n"
  "conditional-assumption-discharged); zero out-of-frame accesses. The\n"
  "fifteenth wave re-drew the register by stages --- the 24 plan-field\n"
  "guards discharged by the layout proof, the 23 caller-contract guards\n"
  "discharged at composition by the caller's own certificate, the 11 OS\n"
  "accesses the named residual assumptions (the TCB $58\\to34\\to11$)\n"
  "--- and emitted the eleven OS guards as a real corridor at the\n"
  "virgin margin 0xFC00 (424 bytes, 116 instructions, the round-trip\n"
  "green, R4/R7 preserved --- no sealed address moves; the falsified\n"
  "guard refused at both boundaries and on the index face, the harness\n"
  "36/36; the dispatch cost named --- a median 22 instructions per call\n"
  "against the 7 of the inlined guard, the price of the single-field\n"
  "eleven-window emission); the rejeu of the 116 certificates is\n"
  "consigned at its corrected invocation (58 UNSAT $+$ 58 SAT, the\n"
  "first-pass invocation bug --- an option meant for stdin --- named in\n"
  "an append-only erratum beside the untouched report).",
  "le TCB : le registre par étages + le corridor des onze + l'erratum")

# le modèle formel : CF3-v3 au verdict machine + le port ProVerif
p(M,
  "and the first effective run \\emph{falsifies} the implication lemma on\n"
  "the delivered model: a two-step trace, the shares as public variables\n"
  "making the attacker's knowledge trivially satisfiable --- a modelling\n"
  "defect named, never an attack; the model amended by writing and\n"
  "re-hashed, the five other lemmata incomplete at budget --- no verdict\n"
  "fabricated); ProVerif remains untried.",
  "and the first effective run \\emph{falsifies} the implication lemma on\n"
  "the delivered model: a two-step trace, the shares as public variables\n"
  "making the attacker's knowledge trivially satisfiable --- a modelling\n"
  "defect named, never an attack; the model amended by writing and\n"
  "re-hashed, the five other lemmata incomplete at budget --- no verdict\n"
  "fabricated). The fifteenth wave carried the amended CF3-v3 to the\n"
  "verdict machine: L3 verified at 1{,}122 steps; L1, L2 and the three\n"
  "witnesses incomplete at the 4\\,GiB memory wall of the assembly\n"
  "sandbox --- the cause named (the decomposition of the attacker's\n"
  "knowledge goal, not the proof depth; partial evaluation bounds the\n"
  "memory but converges beyond the session budget --- the way for the\n"
  "real machine), the negative run prepared in both forms, no verdict\n"
  "fabricated; the ProVerif port delivered (the six active queries, the\n"
  "mirror events, the threshold oracle, the six semantic gaps named\n"
  "beside it) --- the run at the real machine, the models hashed and\n"
  "consigned.",
  "le modèle formel : CF3-v3 au verdict machine + le port ProVerif")

# H7 : la campagne servie + le second annotateur + le confound
p(M,
  "H7 carried to the next campaign, which drew it: the official table of\n"
  "the fourteenth wave drawn and signed, the campaign open to the 28\n"
  "units) and the second machine (the replication remains awaiting).",
  "H7 carried to the next campaign, which drew it: the official table of\n"
  "the fourteenth wave drawn and signed, the campaign open to the 28\n"
  "units --- the fifteenth wave served it: the generator re-executed\n"
  "bit-identically at the canonical sha 2de7d488, the fail-closed\n"
  "aggregator delivered with the D207 stop rules lived at the refusal,\n"
  "the second annotator's kit re-autotested at its four fixtures\n"
  "($\\kappa$ at the pre-registered rule), and the independence\n"
  "confound named --- the local second family sits below the capability\n"
  "frontier at 0/64, the discharge awaits a capable second family, no\n"
  "figure fabricated) and the second machine (the replication remains\n"
  "awaiting).",
  "H7 : la campagne servie, le second annotateur, le confound nommé")

# les kits : l'écosystème d'adoption de la vague 15
p(M,
  "the five other lemmata incomplete at budget; no verdict fabricated).",
  "the five other lemmata incomplete at budget; no verdict fabricated).\n"
  "\\paragraph{The adoption-side ecosystem (fifteenth wave).} Assembled\n"
  "by construction from the repository (\\code{git ls-files}, never a\n"
  "manually maintained list): the training corpus of 109 triples\n"
  "extracted mechanically from the append-only campaign journals (57 at\n"
  "the third, 52 at the fourth version; the splits sealed at the\n"
  "consigned seed --- 28/4/4 tasks, 77/16/16 triples, the held-out\n"
  "carrying the validators alone, no golden notation; the contamination\n"
  "canary unique; ten bit-identical rebuilds); the training environment\n"
  "with the typed multi-level reward (syntax, expansion, round-trip,\n"
  "oracle, mutation --- cumulative and strict; the reward is the judge's\n"
  "own verdict at every level, never a similarity; the anti-hacking\n"
  "check at the reward); the re-playable capability ladder (the rungs\n"
  "name the frontier, never an average; the checkpoint-kit-judges matrix\n"
  "fail-closed; the procedural generator resists contamination); the\n"
  "model-independent agent guide (the eleven rules, the graceful\n"
  "degradation named --- never a weakened judge --- and the pre-registered\n"
  "bench embedded); the canonical-English documentation core at the\n"
  "measured budgets (216 and 167 tokens against the 1{,}500 and 800\n"
  "ceilings); the 156-piece developer kit (the version-compatibility\n"
  "gate fail-closed, no trust anchor shipped, the genesis ceremony\n"
  "air-gapped by construction); the feedback, triage and reporting tools\n"
  "(the schema frozen by fingerprint before any report, the secrets\n"
  "gates lived at the refusal, the decision proposals addressed to the\n"
  "developer --- never applied); and the pre-registered hardware\n"
  "protocols with their fail-closed aggregator (a missing run refuses,\n"
  "never a partial verdict; the machine runs remain the developer's\n"
  "gesture).",
  "les kits : l'écosystème d'adoption de la vague 15")

# ===========================================================================
# (4) LE MANUSCRIT — le changelog, la disponibilité, la plage d'Entrées
# ===========================================================================
p(M,
  "\\item v0.23.2 (22 Nov 2026) --- the present edition, the corrective "
  "generation: the ten sourced corrections (a)--(j) carried to the five "
  "documents, every published ratio at its unrounded operands, the F/L "
  "replication grid, the extended cross-piece linter; the fourteenth wave "
  "carried (the GHASH aggregation, the regime memoisation, TPL-ADD-v4, "
  "the H7 draw, the first effective Tamarin run).",
  "\\item v0.23.2 (22 Nov 2026) --- the corrective generation: the ten "
  "sourced corrections (a)--(j) carried to the five documents, every "
  "published ratio at its unrounded operands, the F/L replication grid, "
  "the extended cross-piece linter; the fourteenth wave carried (the "
  "GHASH aggregation, the regime memoisation, TPL-ADD-v4, the H7 draw, "
  "the first effective Tamarin run).\n"
  "\\item v0.23.3 (23 Nov 2026) --- the present edition, the fifteenth "
  "wave released: the five documents regenerated under the five-class "
  "linter (the semantic phrases, the decision ranges, the dated "
  "feasibility sequences, the post-deposit version claims, the English "
  "gallicisms); the wave carried (the composition measurement, the TCB "
  "reduction, the native oracle engine, TPL-ADD-v5 with its target "
  "missed, the H7 campaign served, CF3-v3 at the verdict machine, the "
  "adoption-side ecosystem).",
  "le changelog gelé : la ligne v0.23.3 posée")

# (D) le claim de version + les dépôts datés
p(M,
  "(v0.23.1 at this writing, version DOI\n"
  "\\doiVersionCourante{}; the earlier deposits 10.5281/zenodo.24367344,\n"
  "10.5281/zenodo.24379173, 10.5281/zenodo.24382460, 10.5281/zenodo.24397623,\n"
  "10.5281/zenodo.24407701, 10.5281/zenodo.24420007 and\n"
  "10.5281/zenodo.24438614 are the dated v0.19.0, v0.19.4, v0.19.5,\n"
  "v0.21.0, v0.22.0, v0.22.1 and v0.23.0 archives; the distinction is\n"
  "consigned:",
  "(v0.23.2 at this writing, version DOI\n"
  "\\doiVersionCourante{}; the earlier deposits 10.5281/zenodo.24367344,\n"
  "10.5281/zenodo.24379173, 10.5281/zenodo.24382460, 10.5281/zenodo.24397623,\n"
  "10.5281/zenodo.24407701, 10.5281/zenodo.24420007, 10.5281/zenodo.24438614,\n"
  "10.5281/zenodo.24442241 and 10.5281/zenodo.24442951 are the dated\n"
  "v0.19.0, v0.19.4, v0.19.5, v0.21.0, v0.22.0, v0.22.1, v0.23.0, v0.23.1\n"
  "and v0.23.2 archives; the distinction is consigned:",
  "(D) le claim de version à la v0.23.2 courante + les dépôts datés")

p(M,
  "(\\code{TRIADE\\_soumission\\_v0.23.2.zip} and\n"
  "\\code{TRIADE\\_complet\\_v0.23.2.zip}) contain respectively the",
  "(\\code{TRIADE\\_soumission\\_v0.23.3.zip} and\n"
  "\\code{TRIADE\\_complet\\_v0.23.3.zip}) contain respectively the",
  "les archives de dépôt aux noms v0.23.3")

p(M,
  "de campagne, l'extension et les vagues d'instructions, Entrées "
  "305--385, portées par le journal de tâches",
  "de campagne, l'extension et les vagues d'instructions, Entrées "
  "305--387, portées par le journal de tâches",
  "la plage d'Entrées FR à 305–387")

p(M,
  "instruction waves, Entr\\'ees 305--385,",
  "instruction waves, Entr\\'ees 305--387,",
  "la plage d'Entrées EN à 305–387")

# ===========================================================================
# (5) LE MANUSCRIT — les gallicismes EN (la règle (E) du linter v2)
# ===========================================================================
p(M,
  "question ``would the pure compiled flow have produced the escapes?''\n"
  "tranch\\'ee on pieces. Three directional hypotheses were registered",
  "question ``would the pure compiled flow have produced the escapes?''\n"
  "settled on pieces. Three directional hypotheses were registered",
  "(E) « tranchée » → « settled on pieces » (le test d'attribution)")

p(M,
  "arm's native code, and the attribution tranch\\'ee on pieces that the\n"
  "compiled pure flow would not have produced them --- the",
  "arm's native code, and the attribution settled on pieces: the\n"
  "compiled pure flow would not have produced them --- the",
  "(E) « tranchée » → « settled on pieces » (le verdict d'attribution)")

p(M,
  "minimal standard kit, 14 VERT 0 ROUGE) tranch\\'ee on pieces that the\n"
  "compiled pure flow would not have",
  "minimal standard kit, 14 VERT 0 ROUGE) settled on pieces: the\n"
  "compiled pure flow would not have",
  "(E) « tranchée » → « settled on pieces » (l'extension)")

# (C) la table générée : la collision typographique n=18/18/15 (des tailles
#     d'échantillon, JAMAIS des comptes de faisabilité) résolue à la forme
#     liste — le marqueur du linter vise les séquences de faisabilité k/18
T = "edition-v0230/donnees/tables_generees_v180.tex"
p(T,
  "medians 1\\,277 [846--1\\,568] / 3\\,374 [2\\,337--5\\,444] / 3\\,674 [3\\,428--4\\,258], $n{=}18/18/15$; the perimeter decomposition",
  "medians 1\\,277 [846--1\\,568] / 3\\,374 [2\\,337--5\\,444] / 3\\,674 [3\\,428--4\\,258], $n{=}18{,}\\,18{,}\\,15$; the perimeter decomposition",
  "(C) la table générée : la collision typographique n=18/18/15 résolue "
  "(des tailles d'échantillon, pas des faisabilités)")

p(M,
  "described in the protocol specification v0.15.8 (the D81 purge "
  "edition: the five-thirds escrow is the active guard, the delivery "
  "instructions retired from the operational text), which this edition",
  "described in the protocol specification v0.15.8 (the D81 purge "
  "edition: the five-share threshold-three Shamir escrow is the active "
  "guard, the delivery instructions retired from the operational text), "
  "which this edition",
  "(E) « five-thirds escrow » → la formulation anglaise (les cinq parts "
  "à seuil trois)")

p(M,
  "purged from the operational documents (the Book of the Vault v1.6\n"
  "and the specification v0.15.8: the five-thirds escrow is the active\n"
  "guard, the repository public --- the runbook simulation refused the",
  "purged from the operational documents (the Book of the Vault v1.7\n"
  "and the specification v0.15.8: the five-share threshold-three Shamir\n"
  "escrow is the active guard, the repository public --- the runbook\n"
  "simulation refused the",
  "(E) « five-thirds escrow » → la formulation anglaise + le Livre v1.7 "
  "au D81")

# ===========================================================================
# (6) LA SPEC — la règle (A) : la formulation exacte D182 + les citations
# ===========================================================================
A = "scripts/spec_v158/sec-a.tex"
D = "scripts/spec_v158/sec-d.tex"

p(A,
  "pur. Le compilateur disparaît du pipeline de livraison : ce que l’agent "
  "écrit est ce qui\n"
  "s’exécute — et rien d’autre.",
  "pur. Le compilateur n’est jamais livré : la notation scellée, elle, "
  "l’est — ce que\n"
  "l’agent écrit est ce qui s’exécute, et rien d’autre.",
  "(A) la spec §1 : le compilateur N'EST JAMAIS LIVRÉ (la formulation "
  "exacte, D182 au protocole)")

p(A,
  "\\textbf{LA FORMULATION CORRIGÉE} (le manuscrit et, par lui, le protocole) :\n"
  "« le compilateur disparaît » devient « AUCUNE chaîne de traduction\n"
  "optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ;",
  "\\textbf{LA FORMULATION CORRIGÉE} (le manuscrit et, par lui, le protocole) :\n"
  "l’ancienne formule sémantique (le compilateur réputé retranché du\n"
  "pipeline) devient « AUCUNE chaîne de traduction\n"
  "optimisante ni opaque ; assemblage WYSIWYG vérifié par round-trip » ;",
  "(A) la spec : la citation reformulée sans la forme littérale (§ le "
  "manuscrit v0.10.0)")

p(D,
  "LA FORMULATION CORRIGÉE & « aucune chaîne de traduction optimisante ni\n"
  "opaque ; assemblage WYSIWYG vérifié par round-trip » (plus jamais « le\n"
  "compilateur disparaît ») ; « l'évolution du code volé est bloquée, son",
  "LA FORMULATION CORRIGÉE & « aucune chaîne de traduction optimisante ni\n"
  "opaque ; assemblage WYSIWYG vérifié par round-trip » (plus jamais\n"
  "l'ancienne formule sémantique du compilateur, retirée par D182) ; «\n"
  "l'évolution du code volé est bloquée, son",
  "(A) la spec annexe B : la rangée D182 reformulée sans la forme "
  "littérale")

# ===========================================================================
# (7) LA SPEC — la règle (C) : les séquences n/18 datées + la v5 à part
# ===========================================================================
p(D,
  "instrumentation — adoptés : 627 (hiérarchique, D222) / 674\n"
  "(TPL-EDIT-v1, OPT-14) / 2~200 (squelette, OPT-14), la faisabilité\n"
  "3/18 puis 5/18 puis 6/18 ; les M1 51 / 719 / 1 088 (D31) historiques\n"
  "datés \\\\",
  "instrumentation — adoptés : 627 (hiérarchique, D222) / 674\n"
  "(TPL-EDIT-v1, OPT-14) / 2~200 (squelette, OPT-14), la faisabilité\n"
  "2026 : 3/18 puis 5/18 puis 6/18 puis 7/18 à la vague 14 ; la campagne\n"
  "v5 (nov. 2026) à 5/18 — la cible manquée consignée, la variance du\n"
  "sujet nommée, les juges intacts ; les M1 51 / 719 / 1 088 (D31)\n"
  "historiques datés \\\\",
  "(C) la spec Tableau 19 : la faisabilité datée jusqu'à la v4 + la v5 "
  "nommée à part")

p(A,
  "D178 : la dette de la carte soldée par la RÉGÉNÉRATION DES\n"
  "NOTATIONS — 18/18 notations == la pièce OCTET POUR OCTET, l'écart de l'audit",
  "D178 : la dette de la carte soldée par la RÉGÉNÉRATION DES\n"
  "NOTATIONS (nov. 2026) — 18/18 notations == la pièce OCTET POUR\n"
  "OCTET, l'écart de l'audit",
  "(C) la spec : le 18/18 des notations daté (le onzième run)")

p(A,
  "le\n"
  "total 1~714 → 1~103 natifs (−35,7~\\%), la réponse 770 → 52\n"
  "(−93,3~\\%), zéro divergence 18/18, l'expansion client verte 18/18. Le",
  "le\n"
  "total 1~714 → 1~103 natifs (−35,7~\\%), la réponse 770 → 52\n"
  "(−93,3~\\%), (nov. 2026) zéro divergence 18/18, l'expansion client\n"
  "verte 18/18. Le",
  "(C) la spec : les 18/18 du pointeur seul datés")

p(D,
  "LA BALISE \\code{loupe 0.1.0} SCELLÉE & PAR FAIT DE CARTE (D178) : la dette de la\n"
  "carte soldée par la RÉGÉNÉRATION DES NOTATIONS (18/18 == la pièce OCTET POUR\n"
  "OCTET, l'écart de l'audit $587 \\to 0$), la cristallisation $26 \\times 10/10$, la",
  "LA BALISE \\code{loupe 0.1.0} SCELLÉE & PAR FAIT DE CARTE (D178) : la dette de la\n"
  "carte soldée par la RÉGÉNÉRATION DES NOTATIONS (nov. 2026 : 18/18 ==\n"
  "la pièce OCTET POUR\n"
  "OCTET, l'écart de l'audit $587 \\to 0$), la cristallisation $26 \\times 10/10$, la",
  "(C) la spec annexe B : le 18/18 de la balise daté")

p(D,
  "M9 franchi (finale \\code{1.0.0}), le TGN ouvert (« Loupe », la notation 18/18),",
  "M9 franchi (finale \\code{1.0.0}), le TGN ouvert (« Loupe » 2026, la\n"
  "notation 18/18),",
  "(C) la spec annexe B : le 18/18 du TGN daté (la rangée D176)")

# ===========================================================================
# (8) LE LIVRE — la date de couverture alignée sur la régénération
# ===========================================================================
L = "scripts/livre_v17/cover.html"
p(L,
  "<span>22 novembre 2026</span>",
  "<span>23 novembre 2026</span>",
  "la date de couverture du Livre alignée sur la génération v0.23.3")


# ===========================================================================
# L'APPLICATION — chaque ancre vérifiée UNIQUE, REFUS sinon
# ===========================================================================
def main() -> int:
    par_fichier: dict[str, list] = {}
    for fichier, ancien, nouveau, nom in PATCHES:
        par_fichier.setdefault(fichier, []).append((ancien, nouveau, nom))
    for fichier, patchs in par_fichier.items():
        chemin = REPO / fichier
        t = chemin.read_text(encoding="utf-8")
        for ancien, nouveau, nom in patchs:
            if ancien not in t:
                print(f"ANCRE MANQUANTE : {nom} ({fichier})")
                return 2
            if t.count(ancien) != 1:
                print(f"ANCRE AMBIGUE {t.count(ancien)}x : {nom} ({fichier})")
                return 2
            t = t.replace(ancien, nouveau)
            print(f"  — {nom}")
        chemin.write_text(t, encoding="utf-8")
    print(f"[v233] {len(PATCHES)} gestes ancrés portés aux "
          f"{len(par_fichier)} fichiers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
