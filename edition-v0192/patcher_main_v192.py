#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_main_v192.py — l'édition v0.19.2 du manuscrit (née de
edition-v0191 par copie) : LA LIGNE D81 DU MODÈLE DE MENACE (§4.1) AU
STATUT EXACT — la transition D81 → séquestre D183 PRÉPARÉE (D219,
l'instruction jx4l5vy5c). AUCUNE valeur mesurée modifiée. Chaque
remplacement EST ANCRÉ — REFUS si une ancre manque."""
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
M = (ICI / "main.tex").read_text(encoding="utf-8")
FAITS = []


def remplace(texte, ancien, nouveau, nom):
    if ancien not in texte:
        raise SystemExit(f"[v0192] ANCRE INTROUVABLE — {nom}")
    FAITS.append(nom)
    return texte.replace(ancien, nouveau, 1)


# ---- 1. l'en-tête du fichier ---------------------------------------------
M = remplace(
    M,
    """%  TRIADE — édition académique v0.19.1 (manuscrit IMRAD, anglais)
%  L'édition v0.19.1 est une ÉDITION DE COHÉRENCE INTER-PIÈCES née de la
%  v0.19.0 (la clôture D210 portée inchangée) : la référence à la
%  spécification courante (v0.13.0 → v0.15.1), les tailles des artefacts""",
    """%  TRIADE — édition académique v0.19.2 (manuscrit IMRAD, anglais)
%  L'édition v0.19.2 est L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219,
%  l'instruction jx4l5vy5c — la vague du 18/11, la deuxième) née de la
%  v0.19.1 (la clôture D210 et la cohérence inter-pièces portées
%  inchangées) : la ligne D81 du modèle de menace (§4.1) au statut
%  exact — le kit de séquestre D183 rafraîchi (la falsification prouvée),
%  le scan de secrets au dry-run vert, la checklist de rotation, la
%  matrice de visibilité du dépôt, l'extension transparence publique
%  documentée non appliquée. AUCUNE valeur mesurée modifiée. Les tailles
%  des artefacts""",
    "l'en-tête du fichier (v0.19.2)")

# ---- 2. pdftitle + fancyhead ----------------------------------------------
M = remplace(M, "(Academic Edition v0.19.1)}",
             "(Academic Edition v0.19.2)}", "le pdftitle (v0.19.2)")
M = remplace(M, r"\fancyhead[L]{\small\itshape TRIADE — academic edition v0.19.1}",
             r"\fancyhead[L]{\small\itshape TRIADE — academic edition v0.19.2}",
             "l'en-tête courant (v0.19.2)")

# ---- 3. la note d'édition (la \date) --------------------------------------
M = remplace(
    M,
    "; this v0.19.1 is a cross-piece coherence pass --- the current "
    "specification reference, the re-hashed sealed-artifact sizes, the "
    "hardware-timing statements aligned with the signed 13 November "
    "runs; no measured value of the sealed v0.18.1 edition modified)}",
    "; this v0.19.2 is the prepared-transition edition (D219) --- the D81 "
    "threat-model line carried to its exact status: the D183 escrow kit "
    "refreshed with proven falsification and a fail-closed verification "
    "gate, the full git-history secrets scan (dry-run green, the named "
    "Python equivalent), the rotation checklist and the repository "
    "visibility matrix (private until the ceremony is lived and the "
    "rotations verified; public with the Zenodo DOI only after); no "
    "measured value of the sealed v0.18.1 edition modified)}",
    "la note d'édition (v0.19.2, la \\date)")

# ---- 4. §4.1 : la première phrase D81 -------------------------------------
M = remplace(
    M,
    r"""--- and D81 \emph{remains} the active decision (the ceremony belongs to
the developer).""",
    r"""--- and D81 \emph{remains} the active decision (the ceremony belongs to
the developer) --- \emph{now prepared} as decision D219: the escrow kit
refreshed (the autotest re-run with proven falsification), the
full-history secrets scan dry-run green, the rotation checklist and the
repository visibility matrix delivered, the transparency-log extension
documented without applying it.""",
    "§4.1 la première phrase D81 (la transition préparée D219)")

# ---- 5. §4.1 : le paragraphe « Two gestures » au statut exact -------------
M = remplace(
    M,
    r"""load. Two gestures answer this row: the v0.13.0 edition \emph{prepares}
the D183 encrypted-escrow ceremony kit (Shamir 5-of-3 split,
cold-reconstitution proof, media-separation plan, withdrawal checklist)
at the laboratory, \emph{without applying it} --- closing the passphrase
exposure belongs to the developer; and the laboratory's own tests run on
temporary clones with test phrases only (the D105 visible-test boundary:
the real container is never opened by laboratory tests, and test states
are visibly marked as such).""",
    r"""load. Two gestures answer this row: the v0.13.0 edition \emph{prepared}
the D183 encrypted-escrow ceremony kit, and the v0.19.2 edition
completes the preparation as decision D219 --- the kit refreshed (the
autotest re-run: ten-of-ten threshold combinations exact, ten-of-ten
sub-threshold pairs inert, a forged part \emph{refused} by the
control-fingerprint gate; a fail-closed \code{--verifier} mode), the
full git-history secrets scan (the named Python equivalent of gitleaks,
its dry-run on a planted test repository green --- six of six caught,
zero false negatives; the real repository triaged: the D81 passphrase
known, nine test fixtures named, no real credential beyond the assumed
arbitration), the rotation checklist for any exposed passphrase, the
repository visibility matrix (private until the ceremony is lived and
the rotations verified; public with the Zenodo DOI only after), and the
transparency-log extension documented \emph{without applying it} ---
closing the passphrase exposure belongs to the developer; and the
laboratory's own tests run on temporary clones with test phrases only
(the D105 visible-test boundary: the real container is never opened by
laboratory tests, and test states are visibly marked as such).""",
    "§4.1 le paragraphe « Two gestures » au statut exact (D219)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
print(f"[v0192] {len(FAITS)} ancrage(s) remplacé(s) :")
for f in FAITS:
    print(f"  - {f}")
print("TOUT VERT — les sources v0.19.2 sont prêtes à compiler")
