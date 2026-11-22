#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_spec_v158_reprise.py — LA REPRISE de la spec v0.15.8 : (1) le
Tableau 19 (tableau de bord de conformité) ALIGNÉ sur la table canonique
des budgets adoptés (la tâche (e) de ylrzmlbn8 — les budgets M1
51/719/1 088 deviennent historiques datés, les adoptés 627/674/2 200 au
rang courant) ; (2) L'ANNEXE B RÉALIGNÉE sur le journal des décisions —
la passe morte (h66o54pjd) avait posé les 22 rangées D229–D250 avec des
contenus décalés (D229 portait le texte de D227, D230 celui de D233,
D232 celui de D235, D242 celui de D248… les dates D232-D235 au 21 nov.
au lieu du 20) — chaque rangée réécrite à SA décision du journal ;
(3) la rangée D251 (l'édition v0.23.0) et le titre de section porté à
D75--D251. Remplacements ancrés — REFUS si une ancre manque."""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SECD = REPO / "scripts" / "spec_v158" / "sec-d.tex"


def remplace(t: str, ancien: str, nouveau: str, nom: str) -> str:
    if ancien not in t:
        print(f"ANCRE MANQUANTE : {nom}")
        sys.exit(2)
    if t.count(ancien) != 1:
        print(f"ANCRE AMBIGUE {t.count(ancien)}x : {nom}")
        sys.exit(2)
    print(f"  — {nom}")
    return t.replace(ancien, nouveau)


ANCIENNES = """D229 & 20 nov. 2026 & La vague 9 en une ligne : la sécurité au plancher sans céder un point (OPT-09) \\\\
D230 & 20 nov. 2026 & La fenêtre de relecture de l'édition (OPT-10) \\\\
D231 & 20 nov. 2026 & La vague 10 exécutée : l'édition v0.21.0 née, la réhabilitation H5 portée \\\\
D232 & 21 nov. 2026 & Les couloirs SIMD mesurés sur matériel (OPT-11) \\\\
D233 & 21 nov. 2026 & La boucle porteuse AES-NI à la cible, le cache de round-trip, la cristallisation incrémentale (OPT-12) \\\\
D234 & 21 nov. 2026 & Le quatrième bras C+G+ : H-CGP2 confirmée, la ventilation trois-effets (OPT-13) \\\\
D235 & 21 nov. 2026 & Le gabarit versionné, le localiser hiérarchique, l'ajout par squelette (OPT-14) \\\\
D236 & 21 nov. 2026 & La purge des instructions de remise D81 (l'histoire datée du 4 au 19 novembre 2026) : le séquestre 5/3 est la garde active, le dépôt public \\\\
D237 & 21 nov. 2026 & La boucle porteuse AES-NI à 7,09 cycles/bloc, le cache de round-trip 680$\\times$, la cristallisation incrémentale au graphe réel (OPT-12 consigné) \\\\
D238 & 21 nov. 2026 & Les six kits pré-enregistrés sans résultat (la règle des kits) \\\\
D239 & 21 nov. 2026 & Le lifter au domaine validé : 942 encodages zéro divergence \\\\
D240 & 21 nov. 2026 & Les errata et le linter : le plancher natif 27,5, le ratio 24,5$\\times$ \\\\
D241 & 21 nov. 2026 & La clôture de la vague 11 : l'édition v0.22.0 née aux cinq documents \\\\
D242 & 21 nov. 2026 & Le TPL-ADD-v2 au dictionnaire de domaine versionné (OPT-15) \\\\
D243 & 21 nov. 2026 & L'édition v0.22.0 : les corrections (a)-(f) portées, le linter v220 à tout token numérique \\\\
D244 & 21 nov. 2026 & La recomposabilité des ratios publiés : les canons non arrondis exigés, le census 559 sommé par code \\\\
D245 & 21 nov. 2026 & L'erratum de la purge D81 nommé : la purge au périmètre sémantique exacte \\\\
D246 & 21 nov. 2026 & La machinery générative : 30\\,000 traces à zéro divergence, aucun résultat produit \\\\
D247 & 21 nov. 2026 & Le double moteur généralisé : la divergence zéro aux trois moteurs \\\\
D248 & 21 nov. 2026 & Le coffre durci : les sept gestes sur copies de laboratoire, le modèle z3 aux invariants \\\\
D249 & 21 nov. 2026 & La marge vierge consacrée : les variantes aux marges ne touchent jamais les scellés \\\\
D250 & 21 nov. 2026 & La release v0.22.1 : la corrective de l'édition v0.22.0, le concept Zenodo résolvant \\\\"""

NOUVELLES = """D229 & 20 nov. 2026 & La vague 10 exécutée : les six instructions à leurs pièces, l'édition v0.21.0 née \\\\
D230 & 20 nov. 2026 & La faute SSE2 nommée et la re-mesure aux baselines équitables \\\\
D231 & 20 nov. 2026 & Le troisième bras C+G : l'effet notation isolé de la gouvernance seule \\\\
D232 & 20 nov. 2026 & Les 92 accès à 100\\,\\% déchargé-ou-gardé, la non-interférence étendue, la soundness du lifter \\\\
D233 & 20 nov. 2026 & La fenêtre de relecture de l'opération éditer (OPT-10) \\\\
D234 & 20 nov. 2026 & La réconciliation du score, du ratio et de l'axe, le registre neutre : l'édition v0.21.0 close \\\\
D235 & 20 nov. 2026 & Les couloirs SIMD à la marge : l'hybride memchr+memcmp, l'AVX2 à dispatch et repli, le SHA-NI au corps \\\\
D236 & 21 nov. 2026 & La purge des instructions de remise D81 (l'histoire datée du 4 au 19 novembre 2026) : le séquestre 5/3 est la garde active, le dépôt public \\\\
D237 & 21 nov. 2026 & La boucle porteuse AES-NI à 7,09 cycles/bloc, le cache de round-trip 680$\\times$, la cristallisation incrémentale au graphe réel (OPT-12 consigné) \\\\
D238 & 21 nov. 2026 & Le quatrième bras C+G+ : l'effet notation propre confirmé, la ventilation trois-effets (OPT-13) \\\\
D239 & 21 nov. 2026 & Le lifter au domaine validé : 942 encodages zéro divergence \\\\
D240 & 21 nov. 2026 & Les six kits pré-enregistrés des lignes « awaiting » sans résultat (la règle des kits) \\\\
D241 & 21 nov. 2026 & La prose saisie aux trois opérations : le gabarit versionné, le localisateur hiérarchique, l'ajout par squelette (OPT-14) \\\\
D242 & 21 nov. 2026 & Le durcissement du coffre sur copies de laboratoire, le modèle z3 aux invariants \\\\
D243 & 21 nov. 2026 & L'édition v0.22.0 née : les corrections (a)-(f) portées, le linter v220 à tout token numérique \\\\
D244 & 21 nov. 2026 & La recomposabilité des ratios publiés : les canons non arrondis exigés, le census 559 sommé par code \\\\
D245 & 21 nov. 2026 & L'erratum de la purge D81 nommé : la purge au périmètre sémantique exacte \\\\
D246 & 21 nov. 2026 & La machinery générative : 30\\,000 traces à zéro divergence, aucun résultat produit \\\\
D247 & 21 nov. 2026 & Le double moteur généralisé : la divergence zéro aux trois moteurs \\\\
D248 & 21 nov. 2026 & Le TPL-ADD-v2 au dictionnaire de domaine versionné, la cible pré-enregistrée manquée nommée (OPT-15) \\\\
D249 & 21 nov. 2026 & La marge vierge consacrée : les variantes aux marges ne touchent jamais les scellés \\\\
D250 & 21 nov. 2026 & La release v0.22.1 : la corrective de l'édition v0.22.0, le concept Zenodo résolvant \\\\
D251 & 22 nov. 2026 & L'édition v0.23.0 née : les écarts (a)-(f) portés aux pièces, la voix « présent édition » unique, le changelog gelé, les abstracts alignés aux mêmes canons \\\\"""


def main() -> int:
    t = SECD.read_text(encoding="utf-8")

    # (1) LE TABLEAU DE BORD ALIGNÉ (la tâche (e)) — les adoptés au rang
    #     courant, les M1 historiques datés
    t = remplace(
        t,
        "Budgets tokens (localiser / éditer / ajouter) & $\\leq$ 64 / 3 000 / 6 000 &\n"
        "instrumentation — mesurés M1 : 51 / 719 / 1 088 (D31) \\\\",
        "Budgets tokens (localiser / éditer / ajouter) & $\\leq$ 64 / 3 000 / 6 000 &\n"
        "instrumentation — adoptés : 627 (hiérarchique, D222) / 674\n"
        "(TPL-EDIT-v1, OPT-14) / 2~200 (squelette, OPT-14), la faisabilité\n"
        "3/18 puis 5/18 puis 6/18 ; les M1 51 / 719 / 1 088 (D31) historiques\n"
        "datés \\\\",
        "le Tableau 19 aligné sur la table canonique des budgets adoptés")

    # (2) L'ANNEXE B RÉALIGNÉE + (3) LA RANGÉE D251
    t = remplace(t, ANCIENNES, NOUVELLES,
                 "l'annexe B réalignée sur le journal (D229-D251)")

    # (4) LE TITRE DE SECTION PORTÉ À D251
    t = remplace(
        t,
        "\\section{Tableau décisionnel du coffre-fort (D75--D250)}"
        "\\label{sec:annexedecisions}",
        "\\section{Tableau décisionnel du coffre-fort (D75--D251)}"
        "\\label{sec:annexedecisions}",
        "le titre de l'annexe B à D75--D251")

    SECD.write_text(t, encoding="utf-8")
    print("[reprise-spec] la spec v0.15.8 alignée (dashboard + annexe B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
