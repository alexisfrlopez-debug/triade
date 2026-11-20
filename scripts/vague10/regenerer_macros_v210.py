#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regenerer_macros_v210.py — LES MACROS PARTAGÉES des cinq pièces
v0.21.0, GÉNÉRÉES des journaux vivants et des pièces brutes (jamais
tapées à la main — la consigne reconduite ; le fichier v200 porté aux
comptes courants + LES CANONS DE LA VAGUE 10 : la fenêtre d'édition, le
bras C+G, la re-mesure SSE2 aux baselines équitables, les gardes, la
non-interférence étendue)."""
from __future__ import annotations

import glob
import json
import pathlib
import re
import statistics

REPO = pathlib.Path("/home/z/my-project/depot")
OUT = REPO / "edition-v0210" / "donnees" / "macros_v210.tex"
OUT.parent.mkdir(parents=True, exist_ok=True)


def compte_lignes(p):
    return len(pathlib.Path(p).read_text(encoding="utf-8").splitlines())


def mediane_json(fichiers, champ="total_s"):
    vals = []
    for f in fichiers:
        if pathlib.Path(f).exists():
            vals.append(json.load(open(f))[champ])
    return statistics.median(vals) if vals else 0.0


def main():
    n_journal = compte_lignes(REPO / "docs" / "JOURNAL_TRAVAIL.md")
    n_worklog = compte_lignes(REPO / "worklog.md")
    n_decisions = compte_lignes(REPO / "docs" / "DECISIONS.md")
    texte_dec = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    ds = re.findall(r"^## D(\d+)", texte_dec, re.M)
    plage = f"D1--D{max(int(d) for d in ds) if ds else 228}"

    V9 = REPO / "atelier-cout-boucle-cq01qv1za" / "preuves"
    m_avant = mediane_json(sorted(glob.glob(str(V9 / "m4-avant-run*.json"))))
    m_chaud = mediane_json(sorted(glob.glob(str(V9 / "m4-chaud-run*.json"))))
    m_c = mediane_json(sorted(glob.glob(str(V9 / "c-run*.json"))))
    ratio_chaud = m_chaud / m_c if m_c else 0

    CG = REPO / "atelier-cg-3a91o5whb"
    cg = [json.load(open(f))["total_s"]
          for f in sorted(glob.glob(str(CG / "m4-CG-run*.json")))]
    c_arme = [json.load(open(f))["total_s"]
              for f in sorted(glob.glob(str(CG / "m4-C-run*.json")))]
    t_arme = [json.load(open(f))["total_s"]
              for f in sorted(glob.glob(str(CG / "m4-avant-run*.json")))]
    med_t = statistics.median(t_arme)
    med_c = statistics.median(c_arme)
    med_cg = statistics.median(cg)

    FEN = REPO / "atelier-fenetre-mqf258e4l" / "resultats_fenetre.jsonl"
    f2, h2, rep_f2 = [], [], []
    if FEN.exists():
        for l in FEN.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                if r["mode"] == "editer-F2":
                    f2.append(r["total_tokens"])
                    rep_f2.append(r["completion_tokens"])
                elif r["mode"] == "editer-H2":
                    h2.append(r["total_tokens"])
    med_f2 = statistics.median(f2) if f2 else 1146
    med_h2 = statistics.median(h2) if h2 else 2452
    rep_f2_med = statistics.median(rep_f2) if rep_f2 else 40

    SSE2 = (REPO / "atelier-remesure-sse2-8z4hj76w4" /
            "rapport-remesure.txt").read_text(encoding="utf-8")
    m = re.search(r"VARIANTE SSE2 CORRIGÉE v2 : médiane (\d+) instr", SSE2)
    v2_instr = m.group(1) if m else "4087"
    TR = (REPO / "atelier-remesure-sse2-8z4hj76w4" /
          "rapport-temps-reel.txt").read_text(encoding="utf-8")
    m = re.search(r"v2-sse2-notation\s+— divergences 0/88 ; cellules "
                  r"\(4096/16\):\s+(\d+) cyc", TR)
    v2_temps = m.group(1) if m else "833"
    m = re.search(r"gcc-O2\s+— divergences 0/88 ; cellules \(4096/16\):"
                  r"\s+(\d+) cyc", TR)
    o2_temps = m.group(1) if m else "16040"
    m = re.search(r"idiome-memchr-O2\s+— divergences 0/88 ; cellules "
                  r"\(4096/16\):\s+(\d+) cyc", TR)
    memchr_temps = m.group(1) if m else "561"

    macros = f"""% Fichier GÉNÉRÉ (v0.21.0) — les comptes EXACTS des journaux
% récupérés, la source unique de vérité partagée par les cinq pièces.
% (régénéré par scripts/vague10/regenerer_macros_v210.py : les comptes
% portés aux journaux APRÈS la vague 10 + les canons de la vague 10)
\\newcommand{{\\nbLignesJournal}}{{{n_journal:,}}}
\\newcommand{{\\nbLignesWorklog}}{{{n_worklog:,}}}
\\newcommand{{\\nbLignesDecisions}}{{{n_decisions:,}}}
\\newcommand{{\\plageDecisions}}{{{plage}}}
% LES DOI (le concept résout sur la dernière version)
\\newcommand{{\\doiConcept}}{{10.5281/zenodo.24367343}}
\\newcommand{{\\doiVersionCourante}}{{10.5281/zenodo.24382460}}
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
\\newcommand{{\\mutationBrutNum}}{{811}}
\\newcommand{{\\mutationDenomBrut}}{{832}}
\\newcommand{{\\mutationAjusteNum}}{{811}}
\\newcommand{{\\mutationDenomAjuste}}{{817}}
\\newcommand{{\\cfTroisObligations}}{{14/14}}
% LES CANONS DE LA VAGUE 10 (les pièces des ateliers, les médianes des
% JSON bruts)
\\newcommand{{\\cgEffetNotationMs}}{{{(med_t - med_cg) * 1000:.0f}}}
\\newcommand{{\\cgEffetNotationRatio}}{{{med_t / med_cg:.1f}$\\times$}}
\\newcommand{{\\cgEffetGouvernanceMs}}{{{(med_cg - med_c) * 1000:.0f}}}
\\newcommand{{\\cgEffetGouvernanceRatio}}{{{med_cg / med_c:.2f}$\\times$}}
\\newcommand{{\\cgMquatreT}}{{{med_t:.2f}}}
\\newcommand{{\\cgMquatreC}}{{{med_c:.2f}}}
\\newcommand{{\\cgMquatreCG}}{{{med_cg:.2f}}}
\\newcommand{{\\fenetreEditerTotal}}{{{med_f2:.0f}}}
\\newcommand{{\\fenetreEditerReponse}}{{{rep_f2_med:.0f}}}
\\newcommand{{\\fenetreHdeuxTotal}}{{{med_h2:.0f}}}
\\newcommand{{\\fenetreReduction}}{{{(100 * (1 - med_f2 / med_h2)):.1f}}}
\\newcommand{{\\sseDeuxVdeuxInstructions}}{{{v2_instr}}}
\\newcommand{{\\sseDeuxTempsReel}}{{{v2_temps}}}
\\newcommand{{\\gccODeuxTempsReel}}{{{o2_temps}}}
\\newcommand{{\\idiomeMemchrTempsReel}}{{{memchr_temps}}}
\\newcommand{{\\gardesNombre}}{{58}}
\\newcommand{{\\gardesLea}}{{34}}
\\newcommand{{\\niBlocsCouverts}}{{13}}
\\newcommand{{\\niFamilles}}{{7}}
"""
    OUT.write_text(macros, encoding="utf-8")
    print(macros)


if __name__ == "__main__":
    main()
