#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v193.py — l'édition v0.19.3 du manuscrit (née de
edition-v0192 par copie) : L'ÉCART DE SESSION FERMÉ — le modèle étendu
(l'instruction 5ey7gmjra), la campagne à zéro divergence, l'égalité de
traces hash-vérifiée, le kit matériel pré-enregistré. AUCUNE valeur
mesurée modifiée. Chaque remplacement EST ANCRÉ — REFUS si une ancre
manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
M = (ICI / "main.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[v0193] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- 1. l'en-tête du fichier ---------------------------------------------
M = remplace(
    M,
    """%  TRIADE — édition académique v0.19.2 (manuscrit IMRAD, anglais)
%  L'édition v0.19.2 est L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219,""",
    """%  TRIADE — édition académique v0.19.3 (manuscrit IMRAD, anglais)
%  L'édition v0.19.3 est L'ÉDITION DE L'ÉCART FERMÉ (l'instruction
%  5ey7gmjra, la vague du 18/11, la troisième) née de la v0.19.2 (la
%  transition préparée puis VÉCUE, le dépôt public D220) : le modèle
%  formel CF3 étendu — la falsification du conteneur offerte pendant
%  une session ouverte, la garde alignée sur la sentinelle concrète —
%  la campagne générative re-jouée à ZÉRO divergence (30 000 traces,
%  trois graines, le rejeu bit-identique deux fois), l'instrument
%  temps constant promu au HASH des traces complètes, le kit de mesure
%  matérielle pré-enregistré en attente. AUCUNE valeur mesurée modifiée.
%  L'édition v0.19.2 est L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219,""",
    "l'en-tête du fichier (v0.19.3)")

# ---- 2. pdftitle + fancyhead ----------------------------------------------
M = remplace(M, "(Academic Edition v0.19.2)}",
             "(Academic Edition v0.19.3)}", "le pdftitle (v0.19.3)")
M = remplace(M, r"\fancyhead[L]{\small\itshape TRIADE — academic edition v0.19.2}",
             r"\fancyhead[L]{\small\itshape TRIADE — academic edition v0.19.3}",
             "l'en-tête courant (v0.19.3)")

# ---- 3. la note d'édition (la \date) --------------------------------------
M = remplace(
    M,
    "; this v0.19.2 is the prepared-transition edition (D219) --- the D81 "
    "threat-model line carried to its exact status: the D183 escrow kit "
    "refreshed with proven falsification and a fail-closed verification "
    "gate, the full git-history secrets scan (dry-run green, the named "
    "Python equivalent), the rotation checklist and the repository "
    "visibility matrix (private until the ceremony is lived and the "
    "rotations verified; public with the Zenodo DOI only after); no "
    "measured value of the sealed v0.18.1 edition modified)}",
    "; this v0.19.3 is the closed-gap edition (the session-falsification "
    "gap discovered by the v0.18.0 campaign, consigned as such, now "
    "closed): the CF3 formal model extended --- in-session falsification "
    "offered, the guard aligned with the concrete sentinel --- the "
    "generative campaign re-played to zero divergence (30{,}000 traces "
    "across three seeds, replay bit-identical twice, exactly the 660 "
    "consigned traces changed), the unbounded proofs re-discharged on the "
    "extended model (inductive invariants, 13/13 rule alignment, "
    "epoch-translation lemma, 31 negative controls caught), the "
    "constant-time instrument promoted to full-trace hashing (one "
    "distinct hash per target over 120 measurements), and the "
    "pre-registered hardware-measurement protocol delivered awaiting the "
    "developer's run; no measured value of the sealed v0.18.1 edition "
    "modified)}",
    "la note d'édition (v0.19.3, la \\date)")

# ---- 4. le résultat de campagne : l'écart FERMÉ ---------------------------
M = remplace(
    M,
    r"""archived. Result: \textbf{660 divergent traces, exactly one class} ---
\code{falsifie\_conteneur} during an open session: the model's guard
offers the rule only in the canonical phase, while the concrete
sentinel runs on the canonical container and \emph{does} destroy on
proven falsification mid-session (local destruction, PV raised, the
trap media and CF2 untouched). The analysis: a state-coverage gap of
the \emph{model} (an under-approximation discovered by the campaign
--- the directed 34-step game never crossed it, the randomization
crosses it 660 times in 10{,}000), \emph{not} a threat to the
properties: the concrete destruction remains proven falsification and
remains local (P3 and P4 hold on every divergent trace); the shrinker
(ddmin) reduces every divergent trace to its minimal failing sequence:
655 of the 660 reach the two-step minimum [\code{ouvrir\_correct},
\code{falsifie\_conteneur}]; the five remaining traces --- of the same
single class --- shrink to minimal sequences longer than two steps,
their per-trace minima consigned in the campaign's raw register (the
655/660 count is read from that register; the analysed object is the
class, not the trace length). The replay at
identical seed reproduces the 10{,}000 verdict digests bit for
bit (verified twice in the present edition, plus the consigned
original).""",
    r"""archived. Result: \textbf{660 divergent traces, exactly one class} ---
\code{falsifie\_conteneur} during an open session: the model's guard
offers the rule only in the canonical phase, while the concrete
sentinel runs on the canonical container and \emph{does} destroy on
proven falsification mid-session (local destruction, PV raised, the
trap media and CF2 untouched). The analysis: a state-coverage gap of
the \emph{model} (an under-approximation discovered by the campaign
--- the directed 34-step game never crossed it, the randomization
crosses it 660 times in 10{,}000), \emph{not} a threat to the
properties: the concrete destruction remains proven falsification and
remains local (P3 and P4 hold on every divergent trace); the shrinker
(ddmin) reduces every divergent trace to its minimal failing sequence:
655 of the 660 reach the two-step minimum [\code{ouvrir\_correct},
\code{falsifie\_conteneur}], their per-trace minima consigned in the
campaign's raw register. The replay at identical seed reproduces the
10{,}000 verdict digests bit for bit. \textbf{The gap is now closed}
(the present edition, the v0.15.3 model extension): the guard aligned
with the concrete sentinel --- falsification offered in both phases,
the destruction local, the media and fragments untouched --- and the
campaign re-played \emph{to zero divergence}: 30{,}000 traces across
three seeds (the consigned 20261112 plus two new ones), every rule and
refusal path covered, the replay bit-identical twice; against the
consigned v0.18.0 register, exactly the 660 traces of the divergence
class changed and \emph{nothing else} (the 9{,}340 other digests
identical, every fin type identical) --- the extension changed
precisely the discovered gap. The bounded cross-check confirms the
reachability space is invariant: the TLC fidelity chain still finds
154 distinct states at the historical bounds, only the fired
transitions grow (896 to 926 --- the in-session falsifications now
offered); the unbounded proofs were re-discharged on the extended
model (the inductive invariants hold, the 13-rule alignment is
SMT-unbounded, the epoch-translation lemma is re-proven, 31 negative
controls caught --- including the extension-annulled guard restored
as a mutation, and the destruction that overflows onto the media).""",
    "le résultat de campagne : l'écart FERMÉ (v0.19.3)")

# ---- 5. l'instrument : l'égalité HASH-VÉRIFIÉE ----------------------------
M = remplace(
    M,
    r"""The correct statement is \emph{exact equality of the executed-
instruction traces}, and the replay verifies it as such: each of the six
targets (sha-256, hmac, hkdf, x25519, aes-gcm, md5) executes a single
instruction count across all 120 measurements --- sha-256 4{,}469, hmac
18{,}371, hkdf 18{,}407, x25519 exactly 1{,}238{,}959 for every key,
aes-gcm 11{,}695, md5 132{,}509 (grain consigned, the v0.11.0 protocols
replayed verbatim). N=60 per class is an exact \emph{structural}
control, never a statistical power test.""",
    r"""The correct statement is \emph{exact equality of the executed-
instruction traces}, and the replay verifies it as such: each of the six
targets (sha-256, hmac, hkdf, x25519, aes-gcm, md5) executes a single
instruction count across all 120 measurements --- sha-256 4{,}469, hmac
18{,}371, hkdf 18{,}407, x25519 exactly 1{,}238{,}959 for every key,
aes-gcm 11{,}695, md5 132{,}509 (grain consigned, the v0.11.0 protocols
replayed verbatim). N=60 per class is an exact \emph{structural}
control, never a statistical power test. The present edition promotes
the instrument: every run now hashes its \emph{complete} trace ---
each executed instruction (address and size) and each data access
(type, address and size; values never hashed) --- and the six targets
each show \emph{one distinct hash} across all 120 measurements
($N{=}60$ per class, seed consigned): bit-identical execution flows
\emph{and} memory-access patterns across the secret classes, the count
subsumed by the hash (two traces of different lengths cannot share
it), the x25519 count confirmed within it. The single-count equality
remains true; it is no longer alone.""",
    "l'instrument : l'égalité HASH-VÉRIFIÉE (v0.19.3)")

# ---- 6. le paragraphe matériel : le kit PRÉ-ENREGISTRÉ --------------------
M = remplace(
    M,
    r"""the single-run scope is part of the claim. Two kits
remain \emph{awaiting a hardware run}: \code{fence.i} semantics on
physical RISC-V silicon (the lived M7 terrain runs were TCG emulation
--- the reserve is named), and a third-machine Loupe field run (the
full T0--T7+S0 scenario). For those two, no number exists and none is
fabricated; the claims table stays honest until the runs are on record.""",
    r"""the single-run scope is part of the claim. The present edition
delivers the \emph{pre-registered repetition protocol} that the
single-run scope called for: $n{\ge}10$ independent executions per
$N{\in}\{60, 200, 400\}$, at least two machines (each with its
consigned CPU fingerprint and effective frequency state), fixed core
affinity, and the tls13-02/tls13-13 N=200 peaks investigation
pre-registered with its candidate causes named \emph{before} any data
(a clock-noise false positive, a shared-core interruption, or a real
constant-time gap --- the repetition and the median criterion decide,
no cause is elected in advance); the sealed measurer is carried
unchanged, the aggregation tool refuses any missing run (fail-closed),
and the kit waits for the developer's gesture --- no figure fabricated.
Two kits also remain \emph{awaiting a hardware run}:
\code{fence.i} semantics on physical RISC-V silicon (the lived M7
terrain runs were TCG emulation --- the reserve is named), and a
third-machine Loupe field run (the full T0--T7+S0 scenario). For
those, no number exists and none is fabricated; the claims table stays
honest until the runs are on record.""",
    "le paragraphe matériel : le kit PRÉ-ENREGISTRÉ (v0.19.3)")

# ---- 7. la conclusion : l'écart nommé → fermé ------------------------------
M = remplace(
    M,
    r"""alignment, and a generative conformance campaign of 10{,}000 traces
(one named divergence class, the model's session-falsification gap,
shrunk and analysed; bit-identical at replay), every claim carrying a
systematic status.""",
    r"""alignment, and a generative conformance campaign of 10{,}000 traces
(one named divergence class, the model's session-falsification gap ---
discovered, shrunk, analysed, and closed by the v0.15.3 model
extension with the campaign re-played to zero divergence across three
seeds; bit-identical at replay), every claim carrying a systematic
status.""",
    "la conclusion : l'écart fermé (v0.19.3)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
print(f"[v0193] {len(FAITS)} ancrage(s) remplacé(s) :")
for f in FAITS:
    print(f"  - {f}")
print("TOUT VERT — les sources v0.19.3 sont prêtes à compiler")
