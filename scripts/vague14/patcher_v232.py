#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_v232.py — LA GÉNÉRATION CORRECTIVE v0.23.2 (la session de
génération promise à l'Entrée 384 — la demande du maître : « je n'ai pas la
version presentation et soumission du pack dans zenodo »). LES CORRECTIONS
RESTANTES (a)-(j) de io13olvxz portées aux sources — (c) les opérandes non
arrondis du plancher M4, (e2) la grille T/X → F/L (D203) au §4.1 et à la
table des statuts, (h) la fermeture aux opérandes non arrondis, (j) le canon
unique GHASH sur la variante ADOPTÉE (schoolbook 63,39 → 12,7×), (d) le
bandeau du Livre « Version 1.6 » → v1.7 — PUIS l'état de l'édition porté à
v0.23.2 (les en-têtes, la bannière, les abstracts EN/FR, le changelog, la
disponibilité des données au DOI v0.23.1, la plage d'Entrées, la vague 14
portée : le GHASH agrégé, H-CGP4, TPL-ADD-v4, H7 tirée, le premier run
Tamarin vécu). CHAQUE remplacement ANCRÉ — REFUS si une ancre manque ou
est ambiguë (le modèle des patchers v230)."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/depot")

# (fichier, ancienne chaîne, nouvelle chaîne, nom du geste)
PATCHES: list[tuple[str, str, str, str]] = []


def p(fichier, ancien, nouveau, nom):
    PATCHES.append((fichier, ancien, nouveau, nom))


# ===========================================================================
# (1) LE MANUSCRIT — les corrections restantes io13olvxz
# ===========================================================================
M = "edition-v0230/main.tex"

# (c) LES OPÉRANDES NON ARRONDIS DU PLANCHER M4 — publiés au §7 (le ratio
#     3,4× n'est recomposable qu'aux médianes non arrondies 6.912/2.056 ;
#     le lecteur des seuls arrondis 6.9/2.1 restait à 3.29)
p(M,
  "The M4 session runs at a median of\n"
  "\\mquatreAvantMediane{}\\,s unoptimised, \\mquatreChaudMediane{}\\,s warm\n"
  "with the memo stack (the 29.7\\,s run is the observed 1-in-10 audit),\n"
  "and \\mquatreBrasC{}\\,s at the compiled reference arm: a floor-ratio\n"
  "of \\mquatreRatioChaud{} against the C arm at equal work, recalculated\n"
  "from the unrounded medians and cited at one decimal wherever the\n"
  "current measurement is meant.",
  "The M4 session runs at a median of\n"
  "\\mquatreAvantMediane{}\\,s unoptimised, \\mquatreChaudMediane{}\\,s warm\n"
  "with the memo stack (the unrounded medians 6.912\\,s and 2.056\\,s; the\n"
  "29.7\\,s run is the observed 1-in-10 audit), and \\mquatreBrasC{}\\,s at\n"
  "the compiled reference arm: a floor-ratio of \\mquatreRatioChaud{} against\n"
  "the C arm at equal work, recalculated from the unrounded medians\n"
  "($6.912/2.056 = 3.362$, cited at one decimal wherever the current\n"
  "measurement is meant).",
  "(c) les opérandes non arrondis du plancher M4 (6.912/2.056)")

# (h) LA FERMETURE DE LA VENTILATION AUX OPÉRANDES NON ARRONDIS — la somme
#     20.715 + 16.497 + 0.213 = 37.425 == T−C, jamais « au millisecond »
#     sans les opérandes
p(M,
  "three-effect ventilation closes exactly (\\effetNotationPropre{} $+$\n"
  "\\effetRegime{} $+$ \\effetGouvernanceOnze{} $=$ T$-$C at the millisecond).",
  "three-effect ventilation closes exactly at the unrounded medians\n"
  "($20.715 + 16.497 + 0.213 = 37.425$\\,s $=$ T$-$C; the rounded macros\n"
  "leave a 13\\,ms residual --- the closure is stated at its operands).",
  "(h) la fermeture aux opérandes non arrondis (37.425)")

# (e2) LA GRILLE T/X → F/L (D203) au §4.1 — la collision avec les taxonomies
#      T1–T6/X1–X8 levée, la correspondance un-pour-un vit au kit
p(M,
  "a T/X coding grid for every defect (five terrain classes T1--T5\n"
  "--- loader/image, hardware ABI, loader semantics, system conventions,\n"
  "environment --- against three laboratory classes X1--X3), double",
  "an F/L coding grid for every defect (five terrain classes F1--F5\n"
  "--- loader/image, hardware ABI, loader semantics, system conventions,\n"
  "environment --- against three laboratory classes L1--L3; renamed from\n"
  "the earlier T/X labels by D203, the one-for-one correspondence living\n"
  "at the kit), double",
  "(e2) la grille F/L au §4.1 (D203)")

# (j) LE CANON UNIQUE GHASH SUR LA VARIANTE ADOPTÉE — schoolbook 63,39 c
#     [IQR 30] contre le scellé 806,35 : 12,7× ; le karatsuba 64,04 la
#     variante livrée non adoptée, l'écart 0,65 c DANS l'IQR nommé
p(M,
  "the GHASH corridor in PCLMULQDQ\n"
  "at 63--64 cycles against the sealed 806 (a $12.6\\times$ gain) with\n"
  "the full AES-GCM composition measured against OpenSSL EVP, the",
  "the GHASH corridor in PCLMULQDQ\n"
  "(the adopted schoolbook at 63.39 cycles [IQR 30] against the sealed\n"
  "806.35, a $12.7\\times$ gain; the karatsuba variant delivered at 64.04\n"
  "cycles, the 0.65-cycle gap inside the IQR, both notations shipped) with\n"
  "the full AES-GCM composition measured against OpenSSL EVP, the",
  "(j) le canon GHASH unique sur la variante adoptée (63.39 = 12.7×)")

# ===========================================================================
# (2) LE MANUSCRIT — l'état porté à v0.23.2 (les en-têtes, la bannière)
# ===========================================================================
p(M,
  "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under "
  "Signed-Intent Governance (Academic Edition v0.23.0)},",
  "pdftitle={TRIADE: Enabling LLM Agents to Write Native Code by Hand Under "
  "Signed-Intent Governance (Academic Edition v0.23.2)},",
  "le pdftitle à v0.23.2")

p(M,
  "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.23.0}",
  "\\fancyhead[L]{\\small\\itshape TRIADE — academic edition v0.23.2}",
  "le running header à v0.23.2")

p(M,
  "\\date{22 November 2026 — Academic edition v0.23.0 (the present edition "
  "states the current state of the programme in one voice; the wave-by-wave "
  "changes live in the frozen edition changelog below; the thirteenth "
  "instruction batch: the GHASH corridor at 63--64 cycles against the "
  "sealed 806 --- a 12.6$\\times$ gain, the full AES-GCM composition "
  "measured against OpenSSL EVP; the four-arm ventilation at equalised "
  "volumes settling the intrinsic-notation share at 5.5\\,\\% --- H-CGP3 "
  "held, the wave-eleven ``notation effect'' was the verification "
  "implementation; the TPL-ADD-v3 grammar and repair loop --- feasibility "
  "6/18, the residual gap named by refusal class; the three "
  "requalifications --- the 58 memory-safety guards conditional "
  "(assumption-discharged) on the sealed artifact, the fifteen mutant "
  "exclusions proved-argued-bounded, the CF3 Tamarin model v2 with the "
  "adversary-at-threshold restriction removed; the Book of the Vault v1.7 "
  "and the specification v0.15.8 with the D81 delivery instructions purged "
  "at the semantic perimeter and the broken paragraphs rewritten; the "
  "559-vector battery partition published exactly; the EN/FR abstracts "
  "generated from the same canonical values)}",
  "\\date{22 November 2026 — Academic edition v0.23.2 (the present edition "
  "states the current state of the programme in one voice; the wave-by-wave "
  "changes live in the frozen edition changelog below; the corrective "
  "generation of the fourteenth wave: the ten sourced corrections (a)--(j) "
  "carried to the five documents --- the wave-13 GHASH corridor restated at "
  "its adopted schoolbook canon 63.39 cycles [IQR 30] against the sealed "
  "806.35, a $12.7\\times$ gain --- and every published ratio now carrying "
  "its unrounded operands; the fourteenth instruction batch carried: the "
  "GHASH aggregation at four blocks with deferred reduction at 19.66 "
  "cycles per multiplication [IQR 19] --- a $41.0\\times$ gain on the "
  "sealed 806.35 and $3.23\\times$ on the wave-13 corridor; the "
  "content-addressed memoisation of the regime at $-89.4$ per cent with no "
  "control removed (H-CGP4 held); the TPL-ADD-v4 counter-example repair "
  "converting its first honest refusal at 7/18 greens for a median 3,990 "
  "tokens; the H7 replication order drawn and signed --- the campaign open "
  "to the 28 units; the CF3 Tamarin model v2 run at the first effective "
  "proof --- the implication lemma falsified by a named modelling defect "
  "(the shares as public variables), the amendment written and re-hashed, "
  "no verdict fabricated; the cross-piece numeric linter extended to the "
  "version strings, the recomposed decompositions, the ratio operands and "
  "the dated T/X labels)}",
  "la bannière de date à v0.23.2 (la génération corrective + la vague 14)")

# ===========================================================================
# (3) LE MANUSCRIT — les abstracts EN/FR (l'état courant en une voix)
# ===========================================================================
p(M,
  "edition (v0.23.0) restates the programme in one voice and carries\n"
  "the twelfth and thirteenth waves: the GHASH corridor in PCLMULQDQ\n",
  "edition (v0.23.2) restates the programme in one voice and carries\n"
  "the twelfth to fourteenth waves: the GHASH corridor in PCLMULQDQ\n",
  "l'abstract EN : l'édition v0.23.2, les vagues 12-14")

p(M,
  "grammar with its repair loop, the three requalifications (the 58\n"
  "memory-safety guards conditional assumption-discharged, the fifteen\n"
  "mutant exclusions proved-argued-bounded, the CF3 Tamarin model v2\n"
  "without the adversary restriction)",
  "grammar with its repair loop (feasibility 3/18, then 5/18, then\n"
  "6/18, then 7/18 at the fourth version --- the counter-example repair\n"
  "converting its first honest refusal), the three requalifications (the\n"
  "58 memory-safety guards conditional assumption-discharged, the fifteen\n"
  "mutant exclusions proved-argued-bounded, the CF3 Tamarin model v2\n"
  "without the adversary restriction)",
  "l'abstract EN : les quatre passes de la faisabilité")

p(M,
  "v0.15.8, the exact partition of the 559-vector battery, and the\n"
  "EN/FR abstracts generated from the same canonical values.",
  "v0.15.8, the exact partition of the 559-vector battery, and the\n"
  "EN/FR abstracts generated from the same canonical values. The\n"
  "fourteenth wave adds: the GHASH aggregation at four blocks with\n"
  "deferred reduction (19.66 cycles per multiplication [IQR 19] against\n"
  "the sealed 806.35 --- a $41.0\\times$ gain on the seal, $3.23\\times$ on\n"
  "the wave-13 corridor), the content-addressed memoisation of the\n"
  "verification regime ($-89.4$ per cent with no control removed), the\n"
  "drawn and signed H7 replication order (the campaign open to the 28\n"
  "units), the first effective Tamarin run (the implication lemma\n"
  "falsified by a named modelling defect, the amendment written, no\n"
  "verdict fabricated), and this corrective generation itself --- the ten\n"
  "sourced corrections (a)--(j) carried to the five documents, every\n"
  "published ratio at its unrounded operands.",
  "l'abstract EN : la vague 14 portée (la génération corrective)")

p(M,
  "its\n"
  "feasibility 3/18 at waves 11-12 then 6/18 at the thirteenth --- the\n"
  "gap named by refusal class)",
  "its\n"
  "feasibility 3/18 at waves 11-12, 6/18 at the thirteenth, then 7/18 at\n"
  "the fourteenth --- the counter-example repair converting its first\n"
  "honest refusal; the gap named by refusal class)",
  "l'abstract EN : la faisabilité à la quatorzième (7/18)")

p(M,
  "la faisabilité 3/18 aux vagues 11-12 puis 6/18 à la treizième — l'écart "
  "nommé par classe de refus)",
  "la faisabilité 3/18 aux vagues 11-12, 6/18 à la treizième puis 7/18 à la "
  "quatorzième (la boucle de contre-exemple convertit son premier refus "
  "honnête) — l'écart nommé par classe de refus)",
  "l'abstract FR : la faisabilité à la quatorzième (7/18)")

# ===========================================================================
# (4) LE MANUSCRIT — le corps : la vague 14 portée (RQ2, H7, Tamarin)
# ===========================================================================
p(M,
  "perimeter, its feasibility 3 to 6 greens across the three passes\n"
  "(the skeleton, then the domain dictionary, then the grammar with its\n"
  "repair loop --- the loop converts none of the honest refusals; the\n"
  "third pass measures 3{,}844 tokens per validated change at 6/18,\n"
  "18/18 for the edit operation at 712)",
  "perimeter, its feasibility 3 to 7 greens across the four passes\n"
  "(the skeleton, then the domain dictionary, then the grammar with its\n"
  "repair loop, then the counter-example repair --- the wave-13 loop\n"
  "converts none of the honest refusals, the wave-14 counter-example\n"
  "repair converts its first (loupe-11) at 7/18 for a median 3{,}990\n"
  "tokens; the third pass measures 3{,}844 tokens per validated change at\n"
  "6/18, 18/18 for the edit operation at 712)",
  "le corps RQ2 : les quatre passes (la quatorzième 7/18, 3 990)")

p(M,
  "skeleton (measured OPT-14; feasibility 3/18, then 5/18 at the twelfth "
  "wave, then 6/18 at the thirteenth --- the repair loop converts none, "
  "the gap named by refusal class; the thirteenth wave measures "
  "3{,}844 per validated change)",
  "skeleton (measured OPT-14; feasibility 3/18, then 5/18 at the twelfth "
  "wave, then 6/18 at the thirteenth, then 7/18 at the fourteenth --- the "
  "wave-13 repair loop converts none, the wave-14 counter-example repair "
  "converts its first (loupe-11); the gap named by refusal class; the "
  "thirteenth wave measures 3{,}844 per validated change, the fourteenth "
  "3{,}990)",
  "la table canonique : la quatrième passe (7/18, 3 990)")

p(M,
  "What the extension could not\nclose: the order test (the draw gave no "
  "contrast --- H7 carries to\nthe next campaign) and the second machine "
  "(the replication remains\nawaiting).",
  "What the extension could not\nclose at its own draw: the order test (the "
  "draw gave no contrast ---\nH7 carried to the next campaign, which drew "
  "it: the official table of\nthe fourteenth wave drawn and signed, the "
  "campaign open to the 28\nunits) and the second machine (the "
  "replication remains awaiting).",
  "le corps H7 : le contraste tiré à la quatorzième")

p(M,
  "randomized draw gave the T arm first in all four units, so arm and\n"
  "order remain confounded (H7 carries to the next campaign that draws\n"
  "the contrast).",
  "randomized draw gave the T arm first in all four units, so arm and\n"
  "order remain confounded --- the contrast is now drawn at the "
  "fourteenth\nwave (the official H7 table drawn and signed, the "
  "replication campaign\nopen to the 28 units, the deliveries the "
  "developer's gesture).",
  "la conclusion RQ1 : le contraste H7 tiré")

p(M,
  "the Tamarin line is now \\emph{tried at\n"
  "the modelling level} (the CF3 v2 model delivered with its\n"
  "adversary-at-threshold restriction removed, the secrecy guarantee\n"
  "reformulated as the implication \\emph{secret learnt $\\Rightarrow$\n"
  "the adversary held $\\ge$3 shares}, the threshold-reachability\n"
  "witness added, the model hashed), while the prover execution\n"
  "remains the developer's gesture (the assembly sandbox carries no\n"
  "tamarin-prover --- the gap named, no verdict fabricated); ProVerif\n"
  "remains untried.",
  "the Tamarin line is now \\emph{tried at\n"
  "the modelling level and run once} (the CF3 v2 model delivered with its\n"
  "adversary-at-threshold restriction removed, the secrecy guarantee\n"
  "reformulated as the implication \\emph{secret learnt $\\Rightarrow$\n"
  "the adversary held $\\ge$3 shares}, the threshold-reachability\n"
  "witness added, the model hashed; the prover installed at the assembly\n"
  "sandbox by the fourteenth wave --- Tamarin 1.12.0 with Maude 3.4 ---\n"
  "and the first effective run \\emph{falsifies} the implication lemma on\n"
  "the delivered model: a two-step trace, the shares as public variables\n"
  "making the attacker's knowledge trivially satisfiable --- a modelling\n"
  "defect named, never an attack; the model amended by writing and\n"
  "re-hashed, the five other lemmata incomplete at budget --- no verdict\n"
  "fabricated); ProVerif remains untried.",
  "le modèle formel : le premier run Tamarin vécu (falsifié honnête)")

p(M,
  "consigned --- still unproven pending the developer's prover run).",
  "consigned --- the fourteenth wave ran it at the sandbox: the "
  "implication\nlemma falsified at the first effective run (a two-step "
  "trace, the shares\nas public variables making the knowledge "
  "trivially satisfiable --- a\nmodelling defect named, the model "
  "amended by writing and re-hashed),\nthe five other lemmata "
  "incomplete at budget; no verdict fabricated).",
  "les kits pré-enregistrés : le run Tamarin vécu")

# ===========================================================================
# (5) LE MANUSCRIT — le changelog gelé, la disponibilité des données,
#     la plage d'Entrées
# ===========================================================================
p(M,
  "\\item v0.23.0 (22 Nov 2026) --- the present edition: the thirteenth "
  "wave carried, the requalifications, the equalised ventilation, the "
  "exact partition, the aligned abstracts.",
  "\\item v0.23.0 (22 Nov 2026) --- the thirteenth wave carried, the "
  "requalifications, the equalised ventilation, the exact partition, the "
  "aligned abstracts.\n"
  "\\item v0.23.1 (22 Nov 2026) --- the corrective release: the corrected "
  "sources and the six ateliers of the fourteenth wave in the complete "
  "archive; the five documents unchanged (the soumission and presentation "
  "packs carried byte-byte).\n"
  "\\item v0.23.2 (22 Nov 2026) --- the present edition, the corrective "
  "generation: the ten sourced corrections (a)--(j) carried to the five "
  "documents, every published ratio at its unrounded operands, the F/L "
  "replication grid, the extended cross-piece linter; the fourteenth wave "
  "carried (the GHASH aggregation, the regime memoisation, TPL-ADD-v4, "
  "the H7 draw, the first effective Tamarin run).",
  "le changelog gelé : v0.23.0 daté, v0.23.1 et v0.23.2 posées")

p(M,
  "(v0.22.1 at this writing, version DOI\n"
  "\\doiVersionCourante{}; the earlier deposits 10.5281/zenodo.24367344,\n"
  "10.5281/zenodo.24379173, 10.5281/zenodo.24382460, 10.5281/zenodo.24397623\n"
  "and 10.5281/zenodo.24407701 are the dated v0.19.0, v0.19.4, v0.19.5,\n"
  "v0.21.0 and v0.22.0 archives; the distinction is consigned:",
  "(v0.23.1 at this writing, version DOI\n"
  "\\doiVersionCourante{}; the earlier deposits 10.5281/zenodo.24367344,\n"
  "10.5281/zenodo.24379173, 10.5281/zenodo.24382460, 10.5281/zenodo.24397623,\n"
  "10.5281/zenodo.24407701, 10.5281/zenodo.24420007 and\n"
  "10.5281/zenodo.24438614 are the dated v0.19.0, v0.19.4, v0.19.5,\n"
  "v0.21.0, v0.22.0, v0.22.1 and v0.23.0 archives; the distinction is\n"
  "consigned:",
  "la disponibilité des données au DOI v0.23.1 (les dépôts datés)")

p(M,
  "(\\code{TRIADE\\_soumission\\_v0.23.0.zip} and\n"
  "\\code{TRIADE\\_complet\\_v0.23.0.zip}) contain respectively the",
  "(\\code{TRIADE\\_soumission\\_v0.23.2.zip} and\n"
  "\\code{TRIADE\\_complet\\_v0.23.2.zip}) contain respectively the",
  "les archives de dépôt aux noms v0.23.2")

p(M,
  "de campagne, l'extension et les vagues d'instructions, Entrées "
  "305--383, portées par le journal de tâches",
  "de campagne, l'extension et les vagues d'instructions, Entrées "
  "305--385, portées par le journal de tâches",
  "la plage d'Entrées FR à 305–385")

p(M,
  "instruction waves, Entr\\'ees 305--383,",
  "instruction waves, Entr\\'ees 305--385,",
  "la plage d'Entrées EN à 305–385")

# ===========================================================================
# (6) LA TABLE DES STATUTS — la grille F/L (D203) et le statut H7 exact
# ===========================================================================
S = "edition-v0230/donnees/statuts_v230.tex"
p(S,
  "Independent replication & awaiting (recruitment / real command) & "
  "the T/X grid finalised, the $\\kappa$ calculator autotested (synthetic "
  "cases), criteria pre-registered unchanged; the D210 extension executed "
  "and closed --- the H7 order contrast still to be drawn by the next "
  "campaign; the second machine remains awaiting \\\\",
  "Independent replication & awaiting (recruitment / real command) & "
  "the F/L grid finalised (renamed from T/X by D203, the correspondence "
  "at the kit), the $\\kappa$ calculator autotested (synthetic cases), "
  "criteria pre-registered unchanged; the D210 extension executed and "
  "closed --- the H7 order contrast drawn and signed at the fourteenth "
  "wave (the official table consigned, the campaign open to the 28 "
  "units); the second machine remains awaiting \\\\",
  "la table des statuts : la grille F/L + le statut H7 exact")

# ===========================================================================
# (7) LE LIVRE — le bandeau de couverture « Version 1.6 » → v1.7
#     (la correction (d) INACHEVÉE à f9f4799 — le PDF livré portait 1.6)
# ===========================================================================
L = "scripts/livre_v17/cover.html"
p(L,
  '<div class="label">Document compl&eacute;mentaire &middot; Version 1.6'
  '</div>',
  '<div class="label">Document compl&eacute;mentaire &middot; Version 1.7'
  '</div>',
  "(d) le bandeau du Livre « Version 1.6 » → v1.7")


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
    print(f"[v232] {len(PATCHES)} gestes ancrés portés aux "
          f"{len(par_fichier)} fichiers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
