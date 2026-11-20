#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v200.py — le manuscrit v0.20.0 (né de la v0.19.6) : LA
VAGUE 9 portée (h0mq0s2m6 le tableau de bord et la distance au
plancher, uagz3fby7 les tokens, bkobf06nu la boucle de vérification,
0205wxg5q les deux couloirs, bk79jvzbm la sécurité au plancher).
Chaque remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
M = (ICI / "main.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[v200] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- l'en-tête, le titre, la date ----------------------------------------
M = remplace(M, "Academic Edition v0.19.6)}",
             "Academic Edition v0.20.0)}", "le pdftitle (v0.20.0)")
M = remplace(M, "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.19.6}",
             "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.20.0}",
             "l'en-tête courant (v0.20.0)")
debut = M.index("\\date{20 November 2026")
fin = M.index(")}", debut) + 2
M = M[:debut] + (
    "\\date{20 November 2026 — Academic edition v0.20.0 (the wave-9 "
    "floor edition: the four-axis dashboard generated from the raw "
    "artifacts with named floors and overhead ratios, the memory-safety "
    "analysis extended to 2{,}006 of 2{,}098 accesses discharged by loop "
    "invariants, interval and alias analysis and bounded model checking, "
    "the three remaining ``killable'' mutants re-classified as "
    "sweep-proven equivalents, the CF3 inductive invariant mechanised in "
    "an independent proof assistant (14/14 obligations), the static "
    "non-interference proof carried on the ten crypto families, the "
    "crystallisation certificate and the double engine at session "
    "opening, the two performance lanes with the SSE2 baseline variant "
    "at 0.03$\\times$ the gcc-O2 cost, and the token campaign with the "
    "deterministic oracle compiler; no measured value modified)}"
) + M[fin:]
FAITS.append("la date (v0.20.0)")

# ---- la spec courante ------------------------------------------------------
M = remplace(M, "protocol specification v0.15.5, which this edition",
             "protocol specification v0.15.6, which this edition",
             "la référence courante à la spec (v0.15.6)")

# ---- les macros -------------------------------------------------------------
M = remplace(M, "\\input{donnees/macros_v196}",
             "\\input{donnees/macros_v200}", "les macros (v0.20.0)")

# ---- la partie française : la référence à la re-mesure ----------------------
M = remplace(M, "1~103 tokens pour localiser (la re-mesure v0.19.6 à la graine consignée,",
             "1~103 tokens pour localiser (la re-mesure v0.19.6 tenue à l'identique par la vague 9,", 
             "la re-mesure localiser tenue (v0.20.0)")

# ---- LA NOUVELLE SECTION : distance au plancher (h0mq0s2m6 point 2) ---------
# insérée avant la conclusion — les ratios par axe, la convention de
# périmètre OBLIGATOIRE avant toute comparaison
ancre_conclusion = "\\section{Conclusion}\\label{sec:conclusion}"
section_plancher = r"""\section{Distance to the floor}\label{sec:floor}
\paragraph{Scope convention (mandatory before any comparison).}
Each ratio below is measured over the \emph{total} operation cost
(material read, prescription prose, emitted response), with each field
also reported separately in the campaign artifacts; the floors are
named with their computation method, and no ratio is ever compared
across different scopes.

\paragraph{Security.} Of the 2{,}098 memory accesses classified by the
bounded analysis, \sureteDecharges{} are discharged by proof (95.6\,\%)
--- loop-invariant inference, interval and alias analysis, and bounded
model checking over the lifted notation --- and \sureteNOMMES{} carry
named causes together with a satisfiability certificate proving that no
static bound exists without the external invariant (OS contract, caller
structure, layout runtime field); zero out-of-frame accesses. The
mutation battery stands at \mutationBrutNum/\mutationDenomBrut{} raw
(97.5\,\%) and \mutationAjusteNum/\mutationDenomAjuste{} adjusted
(99.3\,\%, the 15 proven equivalents excluded from the denominator),
the two scores always presented side by side. The CF3 inductive
invariant is mechanised in an independent proof assistant
(\cfTroisObligations{} obligations, certificates archived), and the
static non-interference proof covers the ten crypto families with the
negative control caught.

\paragraph{Performance.} The M4 session runs at a median of
\mquatreAvantMediane{}\,s unoptimised, \mquatreChaudMediane{}\,s warm
with the memo stack (the 29.6\,s run is the lived 1-in-10 audit), and
\mquatreBrasC{}\,s at the compiled reference arm: a floor-ratio of
\mquatreRatioChaud{} against the C arm at equal work. The SSE2 baseline
variant of the byte-search block reaches \ssewRatio{} the gcc-O2 cost
at equal vectors (\ssewGainGPR{} over the sealed GPR notation), and the
AES-NI descent is already the sealed domain (the era profile requires
it).

\paragraph{Optimisation.} Every lever in the OPT journal is founded on
a measured hot path (R11); the wave adds the crystallisation certificate
(a one-block diff re-verifies 3 of 18 blocks), the double engine at
session opening (divergence zero at volume), and the deterministic
oracle compiler (968 oracle tokens removed over three units).

\paragraph{Token cost.} The pointer-only localiser stands at a median
of 1{,}103 tokens (response 52); the hunk editor at 2{,}452 (response
40, $-34.3\,\%$ / $-97.7\,\%$); the add-by-hunks format is refused for
the third time (0/18 --- the whole-notation path remains); the floor
ratios are 136.2$\times$ (edit: the reread material dominates), 38.0
$\times$ (locate), 4.1$\times$ (add) and 2.9$\times$ (compose) against
the named floors (the real diff pair, the literal pointer, the block
body).

\paragraph{Lexicographic reading.} No compensation between ranks: each
axis is reported for itself, and the wave improved the security rank
without conceding performance, verification strength or token cost.

"""
M = remplace(M, ancre_conclusion, section_plancher + ancre_conclusion,
             "la section distance-au-plancher (la vague 9)")

# ---- l'abstract anglais : la vague 9 portée (la phrase de clôture) ---------
M = remplace(M,
             "underlying cryptographic or testing primitives, which are standard.",
             "underlying cryptographic or testing primitives, which are "
             "standard. The floor edition (v0.20.0) adds the four-axis "
             "dashboard generated from the raw artifacts, the "
             "distance-to-the-floor section, the memory-safety discharge "
             "of 95.6\\,\\% of the 2{,}098 accesses by bounded model "
             "checking over the lifted notation, the CF3 inductive "
             "invariant mechanised in an independent proof assistant, "
             "the static non-interference proof on the ten crypto "
             "families, and the two performance lanes with the SSE2 "
             "baseline variant measured at 0.03$\\times$ the gcc-O2 "
             "cost at equal vectors.",
             "l'abstract anglais (la vague 9 portée)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
print(f"[v200] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print("  -", f)
