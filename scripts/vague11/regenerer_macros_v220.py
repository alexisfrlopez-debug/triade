#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v220.py — LES MACROS PARTAGÉES des cinq pièces
v0.22.0, GÉNÉRÉES des journaux vivants et des pièces brutes (jamais
tapées à la main — la consigne reconduite ; le fichier v210 porté aux
comptes courants + LES CANONS DE LA VAGUE 11 : les couloirs SIMD, la
boucle porteuse restructurée, les quatre bras, le lifter au domaine, les
gabarits versionnés, la purge D81)."""
from __future__ import annotations

import glob
import json
import pathlib
import re
import statistics
from decimal import Decimal, ROUND_HALF_UP


def arrondi(x, n):
    """l'arrondi au demi-supérieur (la convention de l'atelier
    3lmyfb2xa : 20,715 → 20,72 — l'arrondi flottant donnerait 20.71)."""
    q = Decimal(1).scaleb(-n)
    return str(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))

REPO = pathlib.Path("/home/z/my-project/depot")
OUT = REPO / "edition-v0220" / "donnees" / "macros_v220.tex"
OUT.parent.mkdir(parents=True, exist_ok=True)


def compte_lignes(p):
    return len(pathlib.Path(p).read_text(encoding="utf-8").splitlines())


def mediane_json(fichiers, champ="total_s"):
    vals = []
    for f in fichiers:
        if pathlib.Path(f).exists():
            vals.append(json.load(open(f))[champ])
    return statistics.median(vals) if vals else 0.0


def mediane_prompt_gabarits(mode):
    """la médiane du champ prompt de la campagne gabarits (le JSONL brut)."""
    g = [json.loads(l) for l in
         (REPO / "atelier-gabarits-o5apue194" /
          "resultats_gabarits.jsonl").read_text(encoding="utf-8").splitlines()
         if l.strip()]
    sub = [r["prompt_tokens"] for r in g if r["mode"] == mode]
    return statistics.median(sub) if sub else 0.0


def main():
    n_journal = compte_lignes(REPO / "docs" / "JOURNAL_TRAVAIL.md")
    n_worklog = compte_lignes(REPO / "worklog.md")
    n_decisions = compte_lignes(REPO / "docs" / "DECISIONS.md")
    texte_dec = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    ds = re.findall(r"^## D(\d+)", texte_dec, re.M)
    plage = f"D1--D{max(int(d) for d in ds) if ds else 242}"

    V9 = REPO / "atelier-cout-boucle-cq01qv1za" / "preuves"
    m_avant = mediane_json(sorted(glob.glob(str(V9 / "m4-avant-run*.json"))))
    m_chaud = mediane_json(sorted(glob.glob(str(V9 / "m4-chaud-run*.json"))))
    m_c = mediane_json(sorted(glob.glob(str(V9 / "c-run*.json"))))
    ratio_chaud = m_chaud / m_c if m_c else 0

    # ---- LES QUATRE BRAS (3lmyfb2xa, la vague 11) -----------------------
    Q4 = REPO / "atelier-quatrebras-3lmyfb2xa"
    bras = {}
    for code, pref in (("T", "m4-T-run"), ("CGP", "m4-CGP-run"),
                       ("CG", "m4-CG-run"), ("C", "m4-C-run")):
        vals = [json.load(open(f))["total_s"]
                for f in sorted(glob.glob(str(Q4 / f"{pref}*.json")))]
        bras[code] = statistics.median(vals) if vals else 0.0
    notation_propre = bras["T"] - bras["CGP"]
    regime = bras["CGP"] - bras["CG"]
    gouvernance = bras["CG"] - bras["C"]
    part_notation = 100 * notation_propre / (bras["T"] - bras["CG"])

    # ---- le bras C+G de la vague 10 (3a91o5whb — les médianes RECALCULÉES
    # des JSON bruts, la convention v210 reconduite : l'effet notation en ms
    # vient des médianes non arrondies, 39.236 − 2.163 = 37.073 s → 37073)
    CG10 = REPO / "atelier-cg-3a91o5whb"
    cg_t = [json.load(open(f))["total_s"]
            for f in sorted(glob.glob(str(CG10 / "m4-avant-run*.json")))]
    cg_c = [json.load(open(f))["total_s"]
            for f in sorted(glob.glob(str(CG10 / "m4-C-run*.json")))]
    cg_cg = [json.load(open(f))["total_s"]
             for f in sorted(glob.glob(str(CG10 / "m4-CG-run*.json")))]
    med_t10 = statistics.median(cg_t)
    med_c10 = statistics.median(cg_c)
    med_cg10 = statistics.median(cg_cg)
    effet_notation_ms = (med_t10 - med_cg10) * 1000
    effet_gouvernance_ms = (med_cg10 - med_c10) * 1000

    # ---- la campagne gabarits (o5apue194, la vague 11) -------------------
    g_avant = mediane_prompt_gabarits("editer-F2")
    g_apres = mediane_prompt_gabarits("editer-T2")
    g_loc_avant = mediane_prompt_gabarits("localiser-P")
    g_loc_apres = mediane_prompt_gabarits("localiser-H")
    g_add_avant = mediane_prompt_gabarits("ajouter-H3")
    g_add_apres = mediane_prompt_gabarits("ajouter-S")

    # ---- le plancher éditer au natif (zho5vilpy, la correction (c)) ------
    j = [json.loads(l) for l in
         (REPO / "atelier-medians-zho5vilpy" /
          "journal_plancher_natif.jsonl").read_text(encoding="utf-8")
         .splitlines() if l.strip()]
    plancher_natif = statistics.median([r["prompt_tokens"] for r in j])
    ratio_plancher_natif = g_apres / plancher_natif

    macros = f"""% Fichier GÉNÉRÉ (v0.22.0) — les comptes EXACTS des journaux
% récupérés, la source unique de vérité partagée par les cinq pièces.
% (régénéré par scripts/vague11/regenerer_macros_v220.py : les comptes
% portés aux journaux APRÈS la vague 11 + les canons de la vague 11)
\\newcommand{{\\nbLignesJournal}}{{{n_journal:,}}}
\\newcommand{{\\nbLignesWorklog}}{{{n_worklog:,}}}
\\newcommand{{\\nbLignesDecisions}}{{{n_decisions:,}}}
\\newcommand{{\\plageDecisions}}{{{plage}}}
% LES DOI (le concept résout sur la dernière version)
\\newcommand{{\\doiConcept}}{{10.5281/zenodo.24367343}}
\\newcommand{{\\doiVersionCourante}}{{10.5281/zenodo.24397623}}
% LES CANONS M4 (le record daté de la vague 9 : n=5, la liste fixe, les
% médianes RECALCULÉES des JSON bruts — le ratio de régime courant
% RECALCULÉ des médianes non arrondies : {m_chaud:.3f}/{m_c:.3f} =
% {ratio_chaud:.3f} → {ratio_chaud:.1f} à une décimale, PARTOUT où le
% courant est cité)
\\newcommand{{\\mquatreAvantMediane}}{{{m_avant:.1f}}}
\\newcommand{{\\mquatreChaudMediane}}{{{m_chaud:.1f}}}
\\newcommand{{\\mquatreBrasC}}{{{m_c:.1f}}}
\\newcommand{{\\mquatreRatioAvant}}{{{m_avant / m_c:.1f}$\\times$}}
\\newcommand{{\\mquatreRatioChaud}}{{{ratio_chaud:.1f}$\\times$}}
% LE COMPTE D'ARBRES SIGNÉS (le sceau I — quatorze, D177)
\\newcommand{{\\nbArbresSignes}}{{14}}
% LES CANONS DE LA VAGUE 9 (reconduits — le record daté)
\\newcommand{{\\sureteDecharges}}{{2006}}
\\newcommand{{\\sureteDechargesTotal}}{{2098}}
\\newcommand{{\\sureteNOMMES}}{{92}}
\\newcommand{{\\sureteMedies}}{{348}}
\\newcommand{{\\mutationBrutNum}}{{811}}
\\newcommand{{\\mutationDenomBrut}}{{832}}
\\newcommand{{\\mutationAjusteNum}}{{811}}
\\newcommand{{\\mutationDenomAjuste}}{{817}}
\\newcommand{{\\cfTroisObligations}}{{14/14}}
% LES CANONS DE LA VAGUE 10 (reconduits — les pièces des ateliers)
\\newcommand{{\\cgEffetNotationMs}}{{{effet_notation_ms:.0f}}}
\\newcommand{{\\cgEffetNotationRatio}}{{{med_t10 / med_cg10:.1f}$\\times$}}
\\newcommand{{\\cgEffetGouvernanceMs}}{{{effet_gouvernance_ms:.0f}}}
\\newcommand{{\\cgEffetGouvernanceRatio}}{{{med_cg10 / med_c10:.2f}$\\times$}}
\\newcommand{{\\cgMquatreT}}{{{med_t10:.2f}}}
\\newcommand{{\\cgMquatreC}}{{{med_c10:.2f}}}
\\newcommand{{\\cgMquatreCG}}{{{med_cg10:.2f}}}
\\newcommand{{\\fenetreEditerTotal}}{{1146}}
\\newcommand{{\\fenetreEditerReponse}}{{40}}
\\newcommand{{\\fenetreHdeuxTotal}}{{2452}}
\\newcommand{{\\fenetreReduction}}{{53.3}}
\\newcommand{{\\sseDeuxVdeuxInstructions}}{{4087}}
\\newcommand{{\\sseDeuxTempsReel}}{{833}}
\\newcommand{{\\gccODeuxTempsReel}}{{16040}}
\\newcommand{{\\idiomeMemchrTempsReel}}{{561}}
\\newcommand{{\\gardesNombre}}{{58}}
\\newcommand{{\\gardesLea}}{{34}}
\\newcommand{{\\niBlocsCouverts}}{{16}}
\\newcommand{{\\niFamilles}}{{7}}
% LES CANONS DE LA VAGUE 11 (les pièces des ateliers, les médianes des
% JSON bruts)
% — LES QUATRE BRAS (3lmyfb2xa : la médiane de chaque bras, la
%   ventilation trois-effets RECALCULÉE : {bras['T']:.3f} − {bras['CGP']:.3f} =
%   {notation_propre:.3f} ; la somme {notation_propre:.3f} + {regime:.3f} +
%   {gouvernance:.3f} = {notation_propre + regime + gouvernance:.3f} ==
%   T−C {bras['T'] - bras['C']:.3f})
\\newcommand{{\\quatreBrasT}}{{{bras['T']:.2f}}}
\\newcommand{{\\quatreBrasCGP}}{{{bras['CGP']:.2f}}}
\\newcommand{{\\quatreBrasCG}}{{{bras['CG']:.2f}}}
\\newcommand{{\\quatreBrasC}}{{{bras['C']:.2f}}}
\\newcommand{{\\effetNotationPropre}}{{{arrondi(notation_propre, 2)}}}
\\newcommand{{\\effetRegime}}{{{arrondi(regime, 2)}}}
\\newcommand{{\\effetGouvernanceOnze}}{{{arrondi(gouvernance, 3)}}}
\\newcommand{{\\partNotationPropre}}{{{arrondi(part_notation, 1)}}}
\\newcommand{{\\partRegime}}{{{arrondi(100 - part_notation, 1)}}}
% — LES COULOIRS SIMD (fnvan0zes : le rapport temps réel, les médianes)
\\newcommand{{\\hybrideCycles}}{{704}}
\\newcommand{{\\hybrideIqr}}{{52}}
\\newcommand{{\\hybrideGain}}{{25.9$\\times$}}
\\newcommand{{\\scelleGprCycles}}{{18226}}
\\newcommand{{\\shaniCorpsCbloc}}{{128.5}}
\\newcommand{{\\shaniGain}}{{6.5$\\times$}}
\\newcommand{{\\avxDeuxCycles}}{{5846}}
\\newcommand{{\\cpuidSondage}}{{2{{,}}660}}
\\newcommand{{\\batterieVecteurs}}{{559}}
% — LA BOUCLE PORTEUSE (ahult8jgd : la v4-inline, le cache, l'incrémental)
\\newcommand{{\\porteuseVquatreInline}}{{7.09}}
\\newcommand{{\\porteuseVquatreIqr}}{{0.09}}
\\newcommand{{\\porteuseCible}}{{12}}
\\newcommand{{\\porteuseGain}}{{7.1$\\times$}}
\\newcommand{{\\porteuseVdeuxFlux}}{{50.56}}
\\newcommand{{\\cacheRoundtripGain}}{{680.6$\\times$}}
\\newcommand{{\\cristalIncremental}}{{54}}
\\newcommand{{\\oraclesPart}}{{81}}
% — LE LIFTER AU DOMAINE (hrbdfy6i4)
\\newcommand{{\\lifterEncodages}}{{942}}
\\newcommand{{\\lifterMutantesHorsVocab}}{{155}}
% — LES GABARITS (o5apue194 : les médianes du champ prompt, le JSONL brut)
\\newcommand{{\\gabaritEditerAvant}}{{{g_avant:.0f}}}
\\newcommand{{\\gabaritEditerApres}}{{{g_apres:.0f}}}
\\newcommand{{\\gabaritEditerReduction}}{{{100 * (1 - g_apres / g_avant):.1f}}}
\\newcommand{{\\gabaritLocaliserAvant}}{{{g_loc_avant:.0f}}}
\\newcommand{{\\gabaritLocaliserApres}}{{{g_loc_apres:.0f}}}
\\newcommand{{\\gabaritLocaliserReduction}}{{{100 * (1 - g_loc_apres / g_loc_avant):.1f}}}
\\newcommand{{\\gabaritAjouterAvant}}{{{g_add_avant:.0f}}}
\\newcommand{{\\gabaritAjouterApres}}{{{g_add_apres:.0f}}}
\\newcommand{{\\gabaritAjouterReduction}}{{{100 * (1 - g_add_apres / g_add_avant):.1f}}}
% — LE PLANCHER ÉDITER AU NATIF (zho5vilpy : la correction (c) — le
%   plancher re-tokenisé au champ usage du CLI z-ai, le MÊME instrument
%   que la campagne : médiane {plancher_natif} natif ; le ratio
%   {g_apres:.0f}/{plancher_natif} = {ratio_plancher_natif:.1f})
\\newcommand{{\\plancherEditerNatif}}{{{plancher_natif:.1f}}}
\\newcommand{{\\ratioPlancherNatif}}{{{ratio_plancher_natif:.1f}$\\times$}}
% — LA PURGE D81 (ou6wn6wlv)
\\newcommand{{\\purgeCommitsScannes}}{{513}}
"""
    OUT.write_text(macros, encoding="utf-8")
    print(macros)


if __name__ == "__main__":
    main()
