#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RESTRUCTUREUR DU MANUSCRIT EN CŒUR IMRAD (W28IMRAD, prompt 7 de la vague 28).

Le manuscrit v0.32.0 fait 41 pages : la section 7 « Distance to the floor » est
un journal d'optimisation, les notes post-édition suivent la conclusion — un
relecteur IMRAD se noie. LA RESTRUCTURE : le cœur IMRAD (Introduction, Methods,
Results RQ1–RQ4 + la décomposition quatre bras + la table des statuts,
Discussion, Threats to validity, Related work, Conclusion, Declarations) ;
LE JOURNAL OPT (« Distance to the floor »), LES PROGRAMMES DE RÉSULTATS
ÉTENDUS (les v0.11.0/v0.14.0/v0.15.0), LES NOTES POST-ÉDITION et LE CHANGELOG
gelé RENVOYÉS EN ANNEXES ; la décomposition quatre bras HISSEE du journal OPT
au cœur des Résultats (le plan la porte au cœur : RQ1–RQ4 + décomposition +
table des statuts) ; les travaux connexes ENRICHIS (JSONSchemaBench, les
backends de décodage contraint, AutoVecCoder, LLM4Decompile/SLaDe — vérifiés,
différenciés) ; le changelog porte la vague 28 ; la note post-édition v0.33.0.

AUCUNE valeur mesurée n'est modifiée : les déplacements sont intégraux (aucun
paragraphe coupé), les ajouts sont de la prose de position et d'annexe
seulement. Chaque geste est ANCRÉ (l'ancienne chaîne doit exister exactement,
une fois).
"""
import pathlib

R = pathlib.Path(__file__).resolve().parents[1]
MAIN = R / "edition-v0230" / "main.tex"

s = MAIN.read_text(encoding="utf-8")
S0 = s
FAITS = []


def coupe(txt, debut, fin, nom):
    """coupe le bloc [debut, fin) — les ancres doivent être uniques."""
    assert txt.count(debut) == 1, f"ancre non unique : {nom}"
    i = txt.index(debut)
    j = txt.index(fin, i)
    return txt[:i], txt[i:j], txt[j:]


def remplace(txt, ancien, nouveau, nom):
    assert txt.count(ancien) == 1, f"ancre non unique : {nom}"
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---------------------------------------------------------------------------
# 1. L'EN-TÊTE d'édition (le commentaire source) — la vague 28 portée
# ---------------------------------------------------------------------------
entete = (
    "% =====================================================================\n"
    "%  TRIADE — édition académique v0.33.0 (manuscrit IMRAD, anglais)\n"
    "%  L'édition v0.33.0 est L'ÉDITION DU CŒUR IMRAD (la vague 28, l'instruction\n"
    "%  6w0b61juk — les objectifs poussés à leur maximum) : le cœur IMRAD de\n"
    "%  12–15 pages (Introduction, Méthodes, Résultats — RQ1–RQ4 + la\n"
    "%  décomposition quatre bras hissée du journal OPT + la table des statuts,\n"
    "%  Discussion, Menaces sur la validité, Travaux connexes, Conclusion), LE\n"
    "%  JOURNAL OPT (« Distance to the floor »), LES PROGRAMMES DE RÉSULTATS\n"
    "%  ÉTENDUS, LES NOTES POST-ÉDITION et LE CHANGELOG gelé RENVOYÉS EN ANNEXES,\n"
    "%  les travaux connexes enrichis (JSONSchemaBench, les backends de décodage\n"
    "%  contraint, AutoVecCoder, LLM4Decompile/SLaDe — références vérifiées,\n"
    "%  différenciées), DEUX classes de linter nouvelles (C30 N-VALUE,\n"
    "%  C31 CLAIM-SCOPE), le budget token par vague mesuré et pré-enregistré\n"
    "%  (OPT-20). AUCUNE valeur mesurée n'est modifiée.\n"
)
s = remplace(s, "% =====================================================================\n%  TRIADE — édition académique v0.19.5 (manuscrit IMRAD, anglais)",
             entete, "l'en-tête d'édition v0.33.0")

# ---------------------------------------------------------------------------
# 2. LA DÉCOMPOSITION QUATRE BRAS hissée du journal OPT au cœur des Résultats
# ---------------------------------------------------------------------------
avant, quatre_bras, apres = coupe(
    s,
    "\\paragraph{Lexicographic reading.}",
    "\\paragraph{Memory safety at one hundred percent.}",
    "les paragraphes de la décomposition quatre bras")
soussec_quatre = (
    "\\subsection{The four-arm decomposition and the pre-registered "
    "campaigns' summary}\\label{sec:quatrebras}\n"
    "The decomposition the plan assigns to the core: the lexicographic\n"
    "reading, the isolated notation effect and the fourth arm, moved\n"
    "unchanged from the optimisation journal (annex) where they previously\n"
    "lived, so that the core results answer RQ1--RQ4 \\emph{and} the causal\n"
    "decomposition of what notation, verification and governance each cost.\n\n"
    + quatre_bras.rstrip() + "\n\n"
)
s = avant + apres
s = remplace(s, "\\input{donnees/statuts_v230.tex}",
             soussec_quatre + "\\input{donnees/statuts_v230.tex}",
             "la décomposition quatre bras hissée au cœur des Résultats")

# ---------------------------------------------------------------------------
# 3. LES PROGRAMMES DE RÉSULTATS ÉTENDUS détachés du cœur (annexés)
# ---------------------------------------------------------------------------
avant, etendus, apres = coupe(
    s,
    "% ------------------------------------------------------------------\n"
    "\\subsection{Strengthened evidence (the v0.11.0 programme)}\\label{sec:renforce}",
    "\\subsection{The four-arm decomposition",
    "les programmes de résultats étendus (3.5–3.7)")
s = avant + apres
BLOC_ETENDUS = etendus.rstrip() + "\n"

# ---------------------------------------------------------------------------
# 4. LE JOURNAL OPT (Distance to the floor) — détaché pour l'annexe
# ---------------------------------------------------------------------------
avant, floor, apres = coupe(
    s,
    "% ------------------------------------------------------------------\n"
    "\\section{Distance to the floor}\\label{sec:floor}",
    "\\section*{Edition changelog (frozen)}\\label{sec:changelog}",
    "le journal OPT")
s = avant + apres
BLOC_FLOOR = floor.rstrip() + "\n"

# ---------------------------------------------------------------------------
# 5. LE CHANGELOG détaché (annexé)
# ---------------------------------------------------------------------------
avant, changelog, apres = coupe(
    s,
    "\\section*{Edition changelog (frozen)}\\label{sec:changelog}",
    "\\section{Conclusion}\\label{sec:conclusion}",
    "le changelog gelé")
s = avant + apres
BLOC_CHANGELOG = changelog.rstrip() + "\n"

# ---------------------------------------------------------------------------
# 6. LES NOTES POST-ÉDITION détachées (annexées)
# ---------------------------------------------------------------------------
avant, notes, apres = coupe(
    s,
    "\\subsection{Post-edition note (v0.25.0): bounded guarantees, atomicity, provenance}",
    "% ------------------------------------------------------------------\n"
    "\\bibliography{refs}",
    "les notes post-édition")
s = avant + apres
BLOC_NOTES = notes.rstrip() + "\n"

# ---------------------------------------------------------------------------
# 7. LA NOTE DE VAGUE au changelog — la vague 28 portée (la dernière ligne)
# ---------------------------------------------------------------------------
old_line = ("\\item v0.32.0 (26 Nov 2026) --- the present edition, the "
            "twenty-fifth wave: the pack's own review is answered at the "
            "source --- ")
new_line = ("\\item v0.32.0 (26 Nov 2026) --- the twenty-fifth wave: the pack's "
            "own review is answered at the source --- ")
BLOC_CHANGELOG = BLOC_CHANGELOG.replace(old_line, new_line)
vague28 = (
    "\\item v0.33.0 (26 Nov 2026) --- the present edition, the "
    "twenty-eighth wave: the manuscript is restructured into the IMRAD core "
    "the reviewer asked for --- the optimisation journal, the extended "
    "results programmes, the post-edition notes and the frozen changelog "
    "moved to annexes, the four-arm decomposition hoisted into the core "
    "results, the related-work section enriched with the verified "
    "structured-output benchmark and constrained-decoding backends, "
    "AutoVecCoder, LLM4Decompile and SLaDe; the wave's measured results are "
    "the derived-memory harness (the map derived mechanically from the card "
    "C: 229 of 235 vectors executable, the jumeau console line-identical "
    "81/81, six tls-06 vectors refused as DEPASSEMENT --- the timeout gate: "
    "an honest stop is not an OK), the generalised native engine at volumes "
    "(12,000 cases, the hot regime at 4.56x C against the bare-call pilot, "
    "the console deferred and line-identical, the audit one-in-ten at zero "
    "discrepancy), the structured edit at the token floor (OPT-16: the "
    "median at 79.5 native tokens against the 150 target, HELD), the "
    "symmetric replay of the T piece (five core-contract probes green) and "
    "the pre-registered terrain-wave plan; two linter classes (C30 N-VALUE, "
    "C31 CLAIM-SCOPE) and the per-wave token budget (OPT-20). No measured "
    "value changed and no target re-aimed.\\end{itemize}"
)
BLOC_CHANGELOG = BLOC_CHANGELOG.replace("\\end{itemize}", vague28)

# ---------------------------------------------------------------------------
# 8. L'ASSEMBLAGE DES ANNEXES après les Declarations
# ---------------------------------------------------------------------------
BLOC_FLOOR = BLOC_FLOOR.replace(
    "\\section{Distance to the floor}\\label{sec:floor}",
    "\\section{Distance to the floor (the optimisation journal)}\\label{sec:floor}")
annexes = (
    "\n% ===================================================================\n"
    "\\appendix\n"
    "% ===================================================================\n"
    "\\section{The extended results programmes}\\label{sec:renforce-annexe}\n"
    "The three programmes below were core results subsections until the\n"
    "present edition; they are moved verbatim to this annex by the IMRAD\n"
    "restructure, and every measured value they carry is unchanged.\n\n"
    + BLOC_ETENDUS +
    "\n% ------------------------------------------------------------------\n"
    + BLOC_FLOOR +
    "\n% ------------------------------------------------------------------\n"
    "\\section{Post-edition notes}\\label{sec:notes}\n"
    "The notes below were post-edition subsections (8.1--8.7) until the\n"
    "present edition; they are moved verbatim to this annex, each frozen at\n"
    "its wave, the detail living in the wave reports.\n\n"
    + BLOC_NOTES +
    "\n% ------------------------------------------------------------------\n"
    + BLOC_CHANGELOG +
    "\n% ------------------------------------------------------------------\n"
    "\\bibliography{refs}\n"
)
s = remplace(s, "% ------------------------------------------------------------------\n\\bibliography{refs}",
             annexes, "les annexes assemblées (programmes étendus, journal OPT, notes, changelog)")

# ---------------------------------------------------------------------------
# 9. LES TRAVAUX CONNEXES ENRICHIS (références vérifiées, différenciées)
# ---------------------------------------------------------------------------
apres_positioning = (
    "\\paragraph{Structured outputs and constrained decoding.}\n"
    "The constrained-generation side of the adoption problem is now\n"
    "benchmarked on real schemas: JSONSchemaBench~\\cite{jsonschemabench}\n"
    "measures constrained-decoding approaches across efficiency, coverage\n"
    "and output quality, and the serving engines expose grammar backends\n"
    "--- XGrammar~\\cite{xgrammar}, Outlines~\\cite{outlines} and the\n"
    "guidance stack~\\cite{guidance} --- that enforce a schema at decode\n"
    "time. The SERVING-ABSENT refusal of the present study (the border\n"
    "accepts the \\code{response\\_format} field and does not apply it to\n"
    "the decode) was probed on pieces at the twenty-seventh wave and\n"
    "re-probed as an endpoint-selection gate at the twenty-eighth: an\n"
    "endpoint that accepts a schema without applying it is refused by\n"
    "name, which is why the structured-diff campaign (D264/OPT-16) runs\n"
    "its bounded repair loop client-side --- the closed schema holding the\n"
    "edit diff at a 79.5-native-token median, the free-text writing\n"
    "variance remaining the named residual. The benchmark's lesson cuts\n"
    "both ways: constraint fidelity is a serving property to be measured,\n"
    "never assumed.\n\n"
    "\\paragraph{Learned vectorisation and decompilation.}\n"
    "Two adjacent lines sharpen the positioning. AutoVecCoder\n"
    "~\\cite{autoveccoder} teaches LLMs to emit \\emph{explicitly vectorised}\n"
    "source code (an automated vectorisation pipeline with a reinforcement\n"
    "stage) --- their vectorisation is a source-level transformation, while\n"
    "the SIMD corridors here are hand-written notation under seal, measured\n"
    "against the tuned library (the 0.7271 cycles-per-byte interleaved\n"
    "corridor) and scheduled against the compiler on the frozen VAES\n"
    "notation (the notation-versus-C schedule gap published as a distinct\n"
    "result at the twenty-eighth wave). On the decompilation side,\n"
    "LLM4Decompile~\\cite{llm4decompile} and SLaDe~\\cite{slade} erode the\n"
    "anti-reverse-engineering premium that the IP plan of the threat model\n"
    "leans on --- the pack assumes it: the sealed notation's value is\n"
    "governance and provenance, not secrecy, and the decompilation line is\n"
    "cited to keep that assumption honest.\n\n"
    "\\paragraph{RL for code, and what the reward measures.}\n"
    "SuperCoder~\\cite{supercoder} optimises \\emph{execution speed} by\n"
    "reinforcement on runtime rewards --- the strongest published RL result\n"
    "on assembly optimisation, and the natural contrast for the adoption\n"
    "corpus's training plan: the reward there is the conformity judge's own\n"
    "verdict (syntax, expansion, round-trip, oracle, mutation --- cumulative\n"
    "and strict, never a similarity, never a runtime), because the property\n"
    "being trained is the machine-writing stability that the free-text\n"
    "refusals (HORS-FORMAT) name, not the speed of the artifact.\n\n"
    "\\paragraph{Design by contract and specification-first development.}"
)
s = remplace(s, "\\paragraph{Design by contract and specification-first development.}",
             apres_positioning, "les travaux connexes enrichis (trois paragraphes)")

# ---------------------------------------------------------------------------
# 10. LA NOTE POST-ÉDITION v0.33.0 (la vague 28, append-only)
# ---------------------------------------------------------------------------
note_v330 = (
    "\\subsection{Post-edition note (v0.33.0): the IMRAD core, the derived\n"
    "harness, the generalised engine}\n"
    "The twenty-eighth wave restructures the manuscript into the core the\n"
    "review asked for: this edition's core is Introduction, Methods, Results\n"
    "(RQ1--RQ4, the four-arm decomposition hoisted from the journal, the\n"
    "status table), Discussion, Threats, Related Work and Conclusion; the\n"
    "optimisation journal, the extended-results programmes, the post-edition\n"
    "notes and the frozen changelog are annexes, every measured value\n"
    "unchanged. The wave's own measurements, all pre-registered: the\n"
    "derived-memory harness executes 229 of 235 oracle vectors with the map\n"
    "derived mechanically from the card C (the jumeau console line-identical\n"
    "81/81, six tls-06 vectors refused as DEPASSEMENT --- the timeout gate:\n"
    "an honest stop is not an OK); the generalised native engine runs the\n"
    "12,000-case volume at a 4.56x C hot regime against the bare-call pilot\n"
    "(the committed engine's 1056x C and the 77x C end-to-end convention\n"
    "published alongside); the structured edit holds its 150-token target at\n"
    "a 79.5 median. No measured value changed and no target re-aimed.\n\n"
)
s = remplace(s, "\\subsection{Post-edition note (v0.31.0): one registry for targets}",
             note_v330 + "\\subsection{Post-edition note (v0.31.0): one registry for targets}",
             "la note post-édition v0.33.0")

MAIN.write_text(s, encoding="utf-8")
print(f"[restructure] {len(FAITS)} gestes ancrés :")
for f in FAITS:
    print("  -", f)
print(f"[restructure] {S0.count(chr(10))} -> {s.count(chr(10))} lignes ; "
      f"{len(S0)} -> {len(s)} caractères")
