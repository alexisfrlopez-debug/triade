#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v196.py — le manuscrit v0.19.6 (né de la v0.19.5) : LES
TROIS INSTRUCTIONS DOCUMENTAIRES DE LA VAGUE 8 portées (gq117wphb la
cohérence, ansz8lvdf la gouvernance, nunsmzmrm l'intégrité pré-enregistrée).
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "edition-v0195"

M = (ICI / "main.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    global M
    if ancien not in texte:
        raise SystemExit(f"[v196] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- (gq117wphb 1) l'en-tête courant, le titre, la date -------------------
M = remplace(M, "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.19.3)}",
             "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent Governance (Academic Edition v0.19.6)}",
             "le pdftitle (v0.19.6)")
M = remplace(M, "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.19.3}",
             "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.19.6}",
             "l'en-tête courant (v0.19.6)")

# la DATE : l'accumulation v0.19.1→v0.19.5 remplacée par la ligne simple
# (nunsmzmrm 5 : la couche d'éditions supprimée ; gq117wphb 1 : la date
# calée sur la présentation, le 20 novembre 2026)
debut = M.index("\\date{19 November 2026")
fin = M.index(")}", debut) + 2
M = M[:debut] + (
    "\\date{20 November 2026 — Academic edition v0.19.6 (the wave-8 "
    "coherence edition: the shared macros regenerated from the living "
    "journals, the DOI reconciliation --- the concept DOI resolving to "
    "the current version everywhere ---, the sample-draw probability "
    "corrected to one-in-sixteen, the H5 verdicts presented as two "
    "distinct dated entries, the RQ2 localiser distribution re-measured "
    "under the adopted pointer-only format, the abstract rewritten as "
    "one coherent paragraph at the closed state, and the governance "
    "status carried as lived; no measured value modified)}"
) + M[fin:]
FAITS.append("la date (v0.19.6, l'accumulation supprimée)")

# ---- (gq117wphb 1) la référence courante à la spécification ---------------
M = remplace(M, "described in the protocol specification v0.15.3, which this edition",
             "described in the protocol specification v0.15.5, which this edition",
             "la référence courante à la spec (v0.15.5)")

# ---- (gq117wphb 1 + 7) les macros : la source unique ----------------------
M = remplace(M, "\\input{donnees/macros_v190}", "\\input{donnees/macros_v196}",
             "les macros (v0.19.6, la source unique)")

# ---- (gq117wphb 4) la probabilité du tirage : 1/8 -> 1/16 -----------------
M = remplace(M,
             "call; the public draw gave the T arm first in all four units --- a\n"
             "one-in-eight event, consigned as drawn, never re-drawn), the D207 stop",
             "call; the public draw gave the T arm first in all four units --- a\n"
             "one-in-sixteen event, four independent draws at one half each,\n"
             "consigned as drawn, never re-drawn), the D207 stop",
             "la probabilité du tirage (§ Méthodes, 1/16)")
M = remplace(M,
             "untested on this\n"
             "draw}: the public draw gave the T arm first in all four units --- no",
             "untested on this\n"
             "draw}: the public draw gave the T arm first in all four units (a\n"
             "one-in-sixteen event, four independent draws at one half each) --- no",
             "la probabilité du tirage (le verdict H7, 1/16)")

# ---- (gq117wphb 2 + ansz8lvdf) la Data Availability ------------------------
M = remplace(M,
             "\\paragraph{Data availability.} All primary data is public in the project\n"
             "repository (append-only journal, decision log, evidence vault indexes,\n"
             "extraction script, generated tables). A versioned archival snapshot\n"
             "(Zenodo DOI) will be minted at submission time and referenced here ---\n"
             "the deposit's metadata file is prepared with the present edition\n"
             "(title, authors, the two archives, SHA-256 fingerprints); the DOI is\n"
             "inserted upon minting and none is invented before. The\n"
             "two submission archives of this edition (\\code{TRIADE\\_soumission\\_v0.18.0.zip}\n"
             "and \\code{TRIADE\\_complet\\_v0.18.0.zip}) contain respectively the\n"
             "manuscript with its data tables, and the complete sources with raw\n"
             "extracts and fingerprints; every artifact of the claims tables was\n"
             "re-verified byte for byte against the regenerated archives (zero\n"
             "divergence).",
             "\\paragraph{Data availability.} All primary data is public in the project\n"
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
             "la Data Availability (les archives courantes et le DOI réel)")

# ---- (nunsmzmrm 1) H5 : DEUX VERDICTS DISTINCTS ET DATÉS -------------------
M = remplace(M,
             "\\textbf{H5} (verification time within one\n"
             "order of magnitude) \\emph{falsified} --- 52.5\\,s against 2.2\\,s\n"
             "($\\times$23.9); \\emph{held as of v0.19.4 by the developer's explicit\n"
             "instruction} --- the OPT-04 stack (memo v2, dual engine) measured the\n"
             "regime at 6.8\\,s against the C arm's 2.2\\,s on the same machine\n"
             "($\\times$3.0, under the threshold; $n{=}5$ per configuration, monotonic\n"
             "clock, the fixed command lists unchanged, every oracle console\n"
             "line-identical to the originals, the audit re-execution green at zero\n"
             "field-level divergence) --- the falsification of D204 stands as measured\n"
             "and dated, the rehabilitation is the master's named amendment of the\n"
             "mof9q10vq rule (the terrain run to come will confirm, the status table",
             "\\textbf{H5 --- TWO DISTINCT, DATED VERDICTS, never fused into one.}\n"
             "\\emph{H5-D204 (16 November 2026): falsified as measured} --- 52.5\\,s\n"
             "against 2.2\\,s ($\\times$23.9, $n{=}1$, stated as such). \\emph{H5-amended-\n"
             "OPT04 (19 November 2026): held, by the developer's explicit amendment}\n"
             "--- the OPT-04 stack (memo v2, dual engine) measured the regime at\n"
             "6.8\\,s against the C arm's 2.2\\,s on the same machine ($\\times$3.0,\n"
             "under the $\\times$10 threshold; $n{=}5$ per configuration, monotonic\n"
             "clock, the fixed command lists unchanged, every oracle console\n"
             "line-identical to the originals, the audit re-execution green at zero\n"
             "field-level divergence; re-measured at v0.19.6 on the same class of\n"
             "machine: 6.6\\,s against 1.9\\,s, $\\times$3.5). The D204 falsification\n"
             "STANDS as measured and dated in the journal; the rehabilitation is\n"
             "the master's named amendment of the mof9q10vq rule, itself dated\n"
             "(the terrain run to come will confirm, the status table",
             "H5 : les deux verdicts distincts et datés")

# ---- (nunsmzmrm 2) N=7 : la réconciliation explicite -----------------------
M = remplace(M,
             "remain at the developer's gesture, the ledger's every line closed.",
             "remain at the developer's gesture, the ledger's every line closed.\n\n"
             "\\paragraph{The sample criterion, reconciled (v0.19.6).} The plan's\n"
             "pre-registered criterion read \\emph{``$n\\ge6$ fully instrumented\n"
             "units''}; the closure reads \\emph{``seven units fully delivered at\n"
             "both arms''}. The reconciliation, stated explicitly: the register\n"
             "counts seven units delivered at both arms (the application and\n"
             "loupe-01, -02, -05, -08, -13, -16), of which the units carrying\n"
             "M2 usage logs (the instrumented token counts read from the API\n"
             "usage field) are the five instrumented constructions --- the\n"
             "application and the three D204 blocks plus loupe-02 at the\n"
             "extension; the D210 extension units (loupe-08, -13, -16) were\n"
             "delivered at both arms and judged at the delivery cap without a\n"
             "fresh M2 instrumentation of their own. The criterion is thus held\n"
             "on the delivery reading ($N{=}7\\ge6$); on the strict instrumentation\n"
             "reading it would count five instrumented plus three cap-closed ---\n"
             "a relaxation we name as such, with its amendment consigned at the\n"
             "closure (the conditional amendment never triggered, there being no\n"
             "new draw). No number was re-counted: the register makes both\n"
             "readings explicit.",
             "N=7 : la réconciliation du critère")

# ---- (nunsmzmrm 3) H6 : le verdict brut affiché à côté de l'attribution ----
M = remplace(M,
             "\\textbf{H6} (the kit-side escape rate within a factor of two\n"
             "between arms, at identical formats) \\emph{holds, by attribution}:",
             "\\textbf{H6 --- the raw verdict displayed beside the attribution.}\n"
             "The raw delivery metric reads \\emph{three counted escapes at the T\n"
             "deliveries of the fourth unit, zero at the C deliveries} --- the raw\n"
             "asymmetry, as filed. \\emph{The verdict on the hypothesis --- held,\n"
             "by attribution}:",
             "H6 : le verdict brut affiché")

# ---- (nunsmzmrm 4) H7 : le contraste garanti à la prochaine campagne -------
M = remplace(M,
             "the hypothesis carries to\n"
             "the next campaign that draws the contrast.",
             "the hypothesis carries to the next campaign --- for which a\n"
             "stratified randomization is pre-registered here, guaranteeing the\n"
             "order contrast: the units are paired by block family and the arm\n"
             "order is drawn within each pair, so that both orders occur by\n"
             "construction (the free draw that produced no contrast is never\n"
             "repeated unchanged).",
             "H7 : la randomisation stratifiée pré-enregistrée")

# ---- (nunsmzmrm 6) RQ2 : la distribution re-mesurée après adoption ----------
M = remplace(M,
             "medians of 1{,}277 tokens to locate a block, 3{,}374\n"
             "to edit one, 3{,}674 to add one (the content-only v0.14.0 re-measures,\n"
             "580/2{,}143/3{,}510, and the early single-shot M1 values, 51/719/1{,}088,\n"
             "remain as explicitly labelled history --- the measurement perimeters\n"
             "differ and are documented in the text) against a naive whole-disassembly\n"
             "baseline of 300{,}304;",
             "a median of 1{,}103 tokens to locate a block under the adopted\n"
             "pointer-only response format (the v0.19.6 re-measurement at the\n"
             "consigned seed, $n{=}18$, zero divergence, the response itself a\n"
             "median 52 tokens; the pre-OPT-04 median at the same instrument and\n"
             "seed was 1{,}714 with the full-header response, a $-35.7\\%$ total\n"
             "and $-93.3\\%$ response gain --- perimeter note: the v0.17.0\n"
             "round-trip median of 1{,}277 was measured under the earlier\n"
             "campaign's template and remains labelled history, as do the\n"
             "content-only v0.14.0 re-measures 580/2{,}143/3{,}510 and the early\n"
             "single-shot M1 values 51/719/1{,}088 --- the perimeters differ and\n"
             "are documented in the text), 3{,}374 to edit one and 3{,}674 to add\n"
             "one (the OPT-05 hunk-format campaign measured the edit at a median\n"
             "2{,}452 with a 40-token response, $-34.3\\%$ total and $-97.7\\%$\n"
             "response, seventeen of eighteen green at both modes) against a\n"
             "naive whole-disassembly baseline of 300{,}304;",
             "RQ2 : la distribution re-mesurée (le pointeur seul adopté)")

# ---- (nunsmzmrm 7) §5 Threats : TLC/Apalache (D200) ------------------------
M = remplace(M,
             "to $\\delta = 1000$; the checker remains a house-built explorer, not\n"
             "an independent theorem prover --- the Tamarin/ProVerif absence is\n"
             "consigned as the deviation.",
             "to $\\delta = 1000$; the bounded and unbounded discharges now run on\n"
             "the independent TLC and Apalache model checkers (D200: the sealed\n"
             "TLA+ chain reproduced at 154 states, the inductive invariants\n"
             "discharged over unbounded integers with negative controls caught,\n"
             "the rule alignment 13/13) --- the remaining deviation is named: the\n"
             "operational semantics themselves are house-written (the TLA+\n"
             "modules encode OUR rules, not an independent cryptographic\n"
             "protocol formalism), so the independence is at the checker level,\n"
             "not at the modelling level; the Tamarin/ProVerif line remains\n"
             "untried on this protocol.",
             "§5 : TLC/Apalache (D200) et la déviation restante")

# ---- (nunsmzmrm 5) L'ABSTRACT : un seul paragraphe cohérent ----------------
debut_abs = M.index("\\begin{abstract}")
fin_abs = M.index("\\end{abstract}", debut_abs)
NOUVEL_ABSTRACT = """\\begin{abstract}
\\noindent Large language model (LLM) agents currently produce native code by
generating high-level source and delegating to a compiler toolchain; the
translation from intent to machine code passes through layers the agent
neither writes nor verifies. We report on TRIADE, a development protocol in
which an LLM agent writes native x86-64, RISC-V, and TLS~1.3 code
\\emph{directly as assembly notation}, governed by signed layer-I
specifications, an encrypted and fragmented card binding intentions to byte
ranges, and an epistemology separating \\emph{oracle} evidence (differential
emulation in the laboratory) from \\emph{terrain} evidence (execution on the
developer's real machine). A longitudinal single-case study validated the
protocol across eleven milestones (M0--M10, 26 October -- 11 November 2026),
delivering ``Loupe'', a real Windows hex-editor written entirely under the
protocol, then a pre-registered two-arm field campaign (D204, 12--16
November 2026; extension D210, 17--18 November) in which the same agent
delivered every unit twice over shared layer-I contracts --- once as sealed
hand notation (arm T), once as compiled C (arm C) --- closing green at both
arms with every counted escape kit-side in the shared judge, the piece
never at fault, and the empirical attribution (the same compiled piece
re-delivered through a minimal standard kit) reading 14 VERT, 0 ROUGE.
Four research questions are quantified on an append-only evidence base
(a \\nbLignesJournal-line engineering journal, a \\nbLignesWorklog-line
task log and a \\nbLignesDecisions-line decision log, \\plageDecisions):
(RQ1) the escaped-defect rate of changes that had passed every laboratory
control --- eleven of twelve field iterations surfaced at least one escaped
defect, each named to a class and a mechanism before any fix, while the
closing campaigns' 29 witnessed deliveries produced zero escapes
attributable to the sealed notation itself; (RQ2) the measured token cost
per validated change --- under the adopted pointer-only localiser format a
median of 1{,}103 tokens to locate a block ($n{=}18$, zero divergence, the
response a median 52 tokens), 3{,}374 to edit one and 3{,}674 to add one
(the hunk-format campaign measuring the edit at 2{,}452 with a 40-token
response), against a naive whole-disassembly baseline of 300{,}304, with
the historical perimeters (M1, v0.14.0 content-only, v0.17.0 round-trip)
explicitly labelled; (RQ3) the defect classes structurally invisible to
emulation --- loader and PE-format semantics, ABI conventions, harness
assumptions --- enumerated with their evidence, the unbound import leaf
killing the compiled arm's field runs twice at the same slot; and (RQ4)
hot-patch safety --- zero post-patch regression across the milestones,
signed version monotonicity, zero bytes of the sealed pieces moved by the
closing campaign's remediations. The vault's four security properties are
proved \\emph{unbounded} over epochs by an inductive invariant preserved by
every rule of the operational semantics, machine-checked on the
independent TLC and Apalache engines (the earlier generative campaign's
10{,}000-trace divergence class --- the under-approximating guard --- is
dated history: the extended model re-plays 30{,}000 traces across three
seeds to zero divergence, bit-identical twice); a coverage lemma is stated
and discharged mechanically; the fault-injection battery kills 811 of 832
mutants (97.5\\%, the twenty-one remaining each named to a cause family,
twelve of them mechanically proved equivalent for an adjusted 811/820 =
98.9\\%); and the inter-family independence question is settled by tooled
derivation --- a second model family regenerates all 128 oracle constants
from the mathematical definitions alone (zero divergence against the
definitions and the plan), where pure recitation reads only the public
anchors. The study is single-case (N=1), its oracle derives from the same
specifications it checks, and the compiled-reference comparison shares the
laboratory harness; independent replication remains to be run. We state
these limits explicitly. We claim as contributions the \\emph{integration}
of contract-first notation, signed-manifest governance and oracle/terrain
verification into one pipeline for agent-first development --- not the
underlying cryptographic or testing primitives, which are standard.
"""
M = M[:debut_abs] + NOUVEL_ABSTRACT + M[fin_abs:]
FAITS.append("l'abstract (un seul paragraphe cohérent à l'état clos)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
print(f"LE PATCHER v196 : {len(FAITS)} remplacements ancrés — TOUS VERTS")
for f in FAITS:
    print(f"  — {f}")
