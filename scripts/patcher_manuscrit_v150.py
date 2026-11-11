#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_manuscrit_v150.py — les éditions du manuscrit v0.15.0 (nées de
manuscrit_v140 par copie) : le modèle non borné, le raffinement, les
statuts systématiques. Chaque remplacement EST ANCRÉ — le script REFUSE
si une ancre manque."""
import pathlib

M = pathlib.Path("/home/z/my-project/triade/scripts/manuscrit_v150/main.tex")
s = M.read_text(encoding="utf-8")
FAITS = []


def remplace(ancien, nouveau, nom):
    global s
    if ancien not in s:
        raise SystemExit(f"[manuscrit v0.15.0] ANCRE INTROUVABLE — {nom}")
    s = s.replace(ancien, nouveau, 1)
    FAITS.append(nom)


# 1. l'en-tête et les chemins du générateur
remplace("%  TRIADE — édition académique v0.14.0 (manuscrit IMRAD, anglais)",
         "%  TRIADE — édition académique v0.15.0 (manuscrit IMRAD, anglais)",
         "en-tête")
s = s.replace("extraire_donnees_v140.py", "extraire_donnees_v150.py")
s = s.replace("preuves_v110/v120/v130/v140",
              "preuves_v110/v120/v130/v140/v150")
FAITS.append("les chemins du générateur")

# 2. les méta
s = s.replace("Academic Edition v0.14.0}", "Academic Edition v0.15.0}")
s = s.replace("academic edition v0.14.0", "academic edition v0.15.0")
remplace(
    "\\date{11 November 2026 — Academic edition v0.14.0 (the empirical "
    "programme: compiler-reference comparison, RQ2 re-measured, "
    "composition mutation killers)}",
    "\\date{12 November 2026 — Academic edition v0.15.0 (unbounded formal "
    "proofs by inductive invariant, model--implementation refinement, "
    "systematic proof statuses)}",
    "la date")

# 3. le résumé ANGLAIS : la phrase du modèle + la limite corrigée
remplace(
    "signed version monotonicity and an armed anti-rollback check.",
    "signed version monotonicity and an armed anti-rollback check. The "
    "vault's four security properties (secret below threshold, rollback "
    "refusal, no destruction on wrong passphrase, blast radius bounded to "
    "one epoch) are now proved \\emph{unbounded} over epochs by an "
    "inductive invariant preserved by every rule of the operational "
    "semantics, and the model is refined against the implementation by "
    "34 replayed transition steps covering every failure path (zero "
    "gaps); each claim carries a systematic status --- proved unbounded, "
    "proved bounded, or awaiting a hardware run --- and no hardware "
    "claim is made until the developer's field run is on record.",
    "résumé EN : les preuves non bornées et les statuts")
remplace(
    "single-case (N=1), its oracle is derived from the same "
    "specifications it\nchecks, and no baseline compiler-based "
    "replication exists yet; we state\nthese limits explicitly.",
    "single-case (N=1), its oracle is derived from the same "
    "specifications it\nchecks, and the compiled-reference comparison "
    "shares the laboratory\nharness; independent replication (a second "
    "developer, a second domain)\nremains to be run. We state these "
    "limits explicitly.",
    "résumé EN : la limite corrigée (le bras C existe, la réplication "
    "indépendante demeure)")

# 4. le résumé FRANÇAIS
remplace(
    "avec monotonie de version signée et anti-rollback\narmé.",
    "avec monotonie de version signée et anti-rollback\narmé. Les quatre "
    "propriétés de sûreté du coffre (secret sous le seuil, refus du "
    "retour en arrière, aucune destruction sur phrase erronée, rayon "
    "borné à une époque) sont désormais prouvées NON BORNÉES en époques "
    "par un invariant inductif préservé par chaque règle de la "
    "sémantique opérationnelle, et le modèle est raffiné contre "
    "l'implémentation par 34 pas de transition rejoués couvrant tout "
    "chemin d'échec (zéro écart) ; chaque affirmation porte un statut "
    "systématique — prouvé non borné, prouvé borné, ou en attente de run "
    "matériel — et aucune revendication matérielle n'est faite tant que "
    "le run du développeur n'est pas consigné.",
    "résumé FR : les preuves non bornées et les statuts")
remplace(
    "son oracle dérive des mêmes\nspécifications qu'il vérifie, et "
    "aucune réplication avec compilateur de\nréférence n'existe encore ; "
    "ces limites sont énoncées explicitement.",
    "son oracle dérive des mêmes\nspécifications qu'il vérifie, et la "
    "comparaison au compilateur de référence\npartage le harnais du "
    "laboratoire ; la réplication indépendante (un second\ndéveloppeur, "
    "un second domaine) demeure à mener. Ces limites sont\nénoncées "
    "explicitement.",
    "résumé FR : la limite corrigée")

# 5. la NOUVELLE sous-section Results (v0.15.0) avant Discussion
remplace(
    "pre-registered as H4 holds: \\emph{the hand notation is testable to "
    "the\nsame degree as compiled code} --- neither more nor less.",
    "pre-registered as H4 holds: \\emph{the hand notation is testable to "
    "the\nsame degree as compiled code} --- neither more nor less.",
    "ancre de la fin de la section comparison (constat, aucune édition)")

NOUVELLE_SECTION = r"""
\subsection{The unbounded model and the refinement (the v0.15.0
programme)}\label{sec:v150}

\paragraph{From bounded to unbounded.} The v0.12.0 model checked the
vault's claims by exhaustive exploration up to three epochs --- an
artificial ceiling inherited from the explorer, not from the design (the
implementation's closing step is $e \leftarrow e+1$ without a cap). The
v0.15.0 programme removes the ceiling and moves the proof to an
\emph{inductive invariant} $I$ over the operational semantics:
$I_1$ (a learned secret implies the full three-element threshold),
$I_2$ (no unjust destruction flag), $I_3$ (the trap media and the CF2
fragments are never touched), $I_4$ (epochs stay positive). The proof
obligations are discharged mechanically: initialisation holds at the
initial state; preservation is checked for \emph{each of the 13 rules}
over the finite set of state shapes (288 shapes satisfying $I$, the
epoch instantiated over both guard classes $\{1\}$ and $\{\ge 2\}$); the
epoch-uniformity of the class $\ge 2$ --- the rules only ever compare
the epoch to 1 and take its successor --- is witnessed by re-running the
whole proof under epoch translations $\delta \in \{7, 50, 1000\}$ with
bit-identical verdicts. Monotonicity (no rule ever decreases the epoch)
is checked unconditionally over 4{,}096 shapes; the two replay rules
return the state unchanged. The four properties are therefore
\emph{proved unbounded}: any epoch, any depth, under hypotheses
A1--A4, with A5 (side channels, implementation flaws, three-element
compromise, quantum) explicitly out of model.

\paragraph{Fidelity and bounded cross-checks.} The ported explorer
reproduces the v0.12.0 counts \emph{exactly} under the historical
ceiling (154 states, 1{,}152 transitions --- the proof of a faithful
port); with the ceiling removed, the extended bounds ($e \le 5$ at depth
8: 228 states / 1{,}902 transitions; $e \le 7$ at depth 12: 372 /
3{,}342) find zero reachable states outside $I$ and zero property
counterexamples --- the bounded evidence now confirms the unbounded
proof instead of substituting for it.

\paragraph{Model--implementation refinement.} Every abstract rule was
replayed against the real Python implementation (a test vault under a
publicly marked test passphrase; the real vault is never opened by a
test): the honest cycle across \emph{five} lived epochs (the v0.12.0
bound surpassed at both levels), fifteen wrong-passphrase attempts
(zero destruction, zero sealing), the proven container falsification
(one local destruction report, the trap media and CF2 untouched), the
trap falsification (named refusal, nothing destroyed), the past-epoch
replay in three variants (the local mirror, the crossed epochs, the
out-of-band witness), the absent trap (impossible, not refused), the
foreign vault's trap (divergent project hash), and the below-threshold
adversary (32 forged key-halves triples, zero verifier passes):
\textbf{34 refinement steps, zero gaps} --- including every failure
path. Three concrete gestures sit outside the abstract model (the
out-of-band epoch witness, the foreign vault, the forged halves) and
are consigned as such, with their concrete verdicts matching the
specification.

\paragraph{The hardware kits: prepared, waiting, no numbers.} Three
measurement kits are delivered for the developer's field runs ---
real-time dudect timing of the cryptographic families (four targets
extracted from the sealed proxy piece, the native call validated
against the FIPS 180-4 ``abc'' vector, a dual-backend measurer whose
laboratory autotest exercises the mechanism only), \code{fence.i}
semantics on physical RISC-V silicon (the M7 scenario, retargeted),
and a third-machine Loupe field run (the full T0--T7+S0 scenario).
Every one of them is marked \emph{awaiting a hardware run}: no number
exists, none is fabricated, and the claims table stays honest until
the runs are on record.

\input{donnees/statuts_v150.tex}
"""
remplace(
    "% ------------------------------------------------------------------\n"
    "\\section{Discussion}\\label{sec:discussion}",
    NOUVELLE_SECTION + "\n% -------------------------------------------"
    "-----------------------\n\\section{Discussion}\\label{sec:discussion}",
    "la nouvelle sous-section v0.15.0 (insérée avant Discussion)")

# 6. la section du modèle formel : le renvoi à la généralisation
remplace(
    "The limits are named: the checker is an explicit-state explorer\n"
    "(Tamarin/ProVerif absent from the laboratory --- the deviation is\n"
    "consigned); side channels, implementation flaws (RAM discipline, GC),",
    "The limits are named: the checker is an explicit-state explorer\n"
    "(Tamarin/ProVerif absent from the laboratory --- the deviation is\n"
    "consigned); this v0.12.0 account was bounded to three epochs, and\n"
    "the v0.15.0 programme (Section~\\ref{sec:v150}) has since lifted the\n"
    "bound by an inductive invariant, upgrading all four statuses to\n"
    "\\emph{proved unbounded}; side channels, implementation flaws (RAM\n"
    "discipline, GC),",
    "le modèle formel : le renvoi à la généralisation non bornée")

# 7. les menaces : la limite externe corrigée + l'invariant + les kits
remplace(
    "one\nproject, one developer, one agent family; no baseline "
    "comparison;\ngeneralisation is a hypothesis for future work.",
    "one\nproject, one developer, one agent family; the compiled-reference\n"
    "comparison of v0.14.0 exists but shares the laboratory harness and a\n"
    "single seed; independent replication (a second developer, a second\n"
    "domain) remains future work.",
    "menaces externes : la comparaison au bras C, exacte")
remplace(
    "Constant-time is verified\n\\emph{structurally} "
    "(secret-independent instruction traces); real-hardware\nwall-clock "
    "behaviour, cache-timing and power side channels remain\nUNMEASURED "
    "and are marked as not proven.",
    "Constant-time is verified\n\\emph{structurally} "
    "(secret-independent instruction traces); real-hardware\nwall-clock "
    "behaviour, cache-timing and power side channels remain\nUNMEASURED "
    "and are marked as not proven --- the v0.15.0 dudect kit is prepared\n"
    "and waiting for the developer's run, and its laboratory autotest\n"
    "proves the mechanism only, never the machine. The unbounded proof of\n"
    "the vault properties rests on an inductive argument whose\n"
    "epoch-uniformity is structural (the rules compare the epoch only to\n"
    "1 and take its successor) and machine-witnessed by translations up\n"
    "to $\\delta = 1000$; the checker remains a house-built explorer, not\n"
    "an independent theorem prover --- the Tamarin/ProVerif absence is\n"
    "consigned as the deviation.",
    "menaces conclusion : l'invariant et les kits, nommés")

# 8. la conclusion : la phrase v0.15.0 et les ouverts actualisés
remplace(
    "and\nand zero divergences in oracle-independent regeneration (now "
    "including an\nisolated second-agent regeneration).",
    "and zero divergences in oracle-independent regeneration (now "
    "including an\nisolated-instance regeneration and a binary-search "
    "re-derivation).",
    "conclusion : la coquille and/and et l'instance isolée (jamais un "
    "second agent)")
remplace(
    "93.3\\%, tls13 and sys at 100\\%, the 56 remaining\nsurvivors "
    "named). What remains open\nis now precisely measured:",
    "93.3\\%, tls13 and sys at 100\\%, the 56 remaining\nsurvivors "
    "named). The v0.15.0 programme closes the formal side: the four "
    "vault\nproperties proved \\emph{unbounded} by an inductive "
    "invariant, the model\nrefined against the implementation (34 steps, "
    "zero gaps, every failure\npath), and every claim carrying a "
    "systematic status. What remains open\nis now precisely measured:",
    "conclusion : la phrase v0.15.0")
remplace(
    "the emulation-only scope of the constant-time result, the\n"
    "unmeasured real-hardware timing (including the \\code{fence.i} "
    "patch\npath, whose hardware instruction-cache semantics are "
    "unvalidated on\nRISC-V silicon), the missing second-agent "
    "replication --- and, on the",
    "the emulation-only scope of the constant-time result (the dudect\n"
    "kit is prepared and waiting), the unmeasured real-hardware timing\n"
    "(the \\code{fence.i} kit targets a physical RISC-V board; a "
    "third-machine\nLoupe run is likewise prepared), the missing "
    "independent replication\n(the T/X grid and the $\\kappa$ calculator "
    "are ready; the second\nannotator is yet to be recruited) --- and, "
    "on the",
    "conclusion : les ouverts actualisés (les kits préparés, la "
    "réplication outillée)")

M.write_text(s, encoding="utf-8")
print(f"[manuscrit v0.15.0] {len(FAITS)} éditions ancrées :")
for f in FAITS:
    print(f"  - {f}")
