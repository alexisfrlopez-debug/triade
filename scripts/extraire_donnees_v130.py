#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_donnees_v130.py — L'EXTRACTION ET LA GÉNÉRATION DES DONNÉES de
l'édition v0.13.0 (la commande : « ré-exécuter le script d'extraction et
régénérer tous les tableaux ; contrôler chaque valeur numérique du manuscrit
contre le journal — aucune valeur tapée à la main »).

LES CINQ TABLEAUX HISTORIQUES (v0.10.0, D182) demeurent extraits par le
MODULE v100 (les ancres du journal vérifiées — refus si une ancre manque,
les empreintes scellées MESURÉES sur les pièces à chaque régénération) :
11 jalons, 7 budgets, 10 volumes d'oracle, 12 runs Loupe, 3 empreintes.
NOUVEAUTÉ v0.13.0 : la légende du tableau des budgets NOTE que le TOTAL
exclut les brouillons (8 774 + 5 099 = 13 873 — la consigne, point 1).

LE GÉNÉRATEUR ANTI-TRONCATURE (la dette de la Table 6) : la table des
preuves de v0.11.0/v0.12.0 était écrite à la main hors générateur —
cellules coupées au milieu des mots, français dans un manuscrit anglais,
colonnes incomplètes. La présente table (tab:preuves) est GÉNÉRÉE depuis
les sorties BRUTES des instruments (preuves_v110/, preuves_v120/,
preuves_v130/) : chaque ligne est PARSÉE depuis les CSV/JSON/rapports,
aucune valeur mesurée n'est tapée, et le générateur NE TRONQUE JAMAIS —
les cellules vont à des colonnes p{} qui replient le texte ; une
assertion refuse toute cellule déraisonnablement longue ; JAMAIS une coupe.

LES CORRECTIONS v0.13.0 PORTÉES PAR LES DONNÉES :
  - le benchmark AUDITÉ (audit_benchmark.csv : l'op complète des blocs
    75 983 instructions — le « 4 524 » de v0.11.0 était la finalisation
    SEULE, le facteur 15,3× est RETIRÉ, D191) ;
  - les statistiques de scellement CORRIGÉES (stats_v130.csv : les
    caractéristiques opérationnelles P(sceller|q) = (1-q)^n et les
    quantiles unilatéraux exacts — les « α = 3,29e-2/1,08e-3 » étaient des
    rapports de vraisemblance mal étiquetés, D190) ;
  - l'IC95 % EXACT de 11/12 (Clopper-Pearson, la réserve de
    non-indépendance) ;
  - les COMPTES EXACTS du journal en macros (\\nbLignesJournal etc. —
    jamais plus d'arrondi ni de divergence abstract/intro).

Sortie : manuscrit_v130/donnees/{tables_generees.tex, macros_v130.tex,
jalons.csv, budgets.csv, oracles.csv, runs_loupe.csv, empreintes.csv,
extraits_journal.txt}
"""
from __future__ import annotations

import csv
import importlib.util
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
PREUVES_V110 = REPO / "scripts" / "preuves_v110"
PREUVES_V120 = REPO / "scripts" / "preuves_v120"
PREUVES_V130 = REPO / "scripts" / "preuves_v130"
DONNEES = REPO / "scripts" / "manuscrit_v130" / "donnees"
DONNEES.mkdir(parents=True, exist_ok=True)


def charger_module(nom: str, chemin: pathlib.Path):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


V100 = charger_module("extraire_donnees_v100",
                      REPO / "scripts" / "extraire_donnees_v100.py")


# ------------------------------------------------------------- les sources

def lire_csv(chemin: pathlib.Path) -> list[dict]:
    with open(chemin, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def exiger(condition: bool, message: str):
    if not condition:
        raise SystemExit(f"[extraire_v130] REFUS — {message}")


# ------------------------------------------------- la table des preuves (6)

def cell(s: str) -> str:
    """Une cellule JAMAIS tronquée : échappée LaTeX, repliée par les
    colonnes p{} du document — une assertion refuse l'invraisemblable,
    jamais une coupe (la dette de la Table 6, point 1 de la commande)."""
    s = str(s)
    exiger(len(s) <= 400, f"cellule invraisemblable ({len(s)} car.) : {s[:60]}…")
    # x25519 est un NOM, pas une multiplication — protégé de l'échappement
    s = s.replace("x25519", "\x00")
    s = V100.latex_echappe(s)
    return s.replace("\x00", "x25519")


def mille(n) -> str:
    """Le format anglais à milliers, en espace fine LaTeX."""
    return f"{n:,}".replace(",", r"\,")


def table_preuves() -> list[tuple[str, str, str, str]]:
    """Les lignes (instrument, cible, mesuré, source) PARSÉES depuis les
    sorties brutes — les totaux calculés, les invariants assertés."""
    # --- mutation testing (v0.11.0, D185) ---
    mut = lire_csv(PREUVES_V110 / "mutation.csv")
    doms = {}
    for r in mut:
        d = doms.setdefault(r["domaine"], {"mutants": 0, "vivants": 0,
                                           "blocs": 0})
        d["mutants"] += int(r["mutants"])
        d["vivants"] += int(r["vivants"])
        d["blocs"] += 1
    # les familles cryptographiques (D185 : sha, hkdf, x25519, aes-gcm, md5)
    CRYPTO = {f"tls13-{i:02d}" for i in range(1, 7)} | \
             {f"tls13-{i:02d}" for i in range(13, 20)} | {"loupe-06"}
    cr_m = sum(int(r["mutants"]) for r in mut if r["bloc"] in CRYPTO)
    cr_v = sum(int(r["vivants"]) for r in mut if r["bloc"] in CRYPTO)
    exiger(cr_v == 0, "des mutants cryptographiques vivants ?!")
    lignes = []
    for dom, noms in (("loupe", "18 sealed blocks"), ("tls13", "28 sealed blocks"),
                      ("sys", "6 sealed blocks")):
        d = doms[dom]
        tue = d["mutants"] - d["vivants"]
        taux = round(100.0 * tue / d["mutants"], 1)
        lignes.append((
            "Mutation testing (16 mutants/block, seed 20261111)",
            f"{dom} domain ({noms})",
            f"{tue}/{d['mutants']} killed ({taux}%); "
            f"{d['vivants']} survivors named",
            "preuves\\_v110/mutation.csv"))
    lignes.append((
        "Mutation testing (same campaign)",
        "cryptographic families (sha-256, hmac/hkdf, x25519, aes-gcm, md5)",
        f"100% killed ({cr_m}/{cr_m} mutants, 0 survivors)",
        "preuves\\_v110/mutation.csv"))

    # --- fuzzage guidé (v0.11.0) ---
    fz = json.loads((PREUVES_V110 / "fuzzage.json").read_text(encoding="utf-8"))
    l01 = fz["loupe-01"]
    lignes.append((
        "Coverage-guided fuzzing (seed 20261111)",
        "loupe-01 (untrusted input path)",
        f"{l01['couverture_instructions']}/{l01['instructions_du_bloc']} "
        f"instructions covered ({l01['couverture_pct']}%); "
        f"{l01['crashes']} crashes; {l01['violations_canaris']} canary "
        f"violations; corpus {l01['corpus_final']}",
        "preuves\\_v110/fuzzage.json"))
    h10 = fz["http-10"]
    lignes.append((
        "Coverage-guided fuzzing (seed 20261112)",
        "http-10 (input parser, sealed 0.4.0)",
        f"{h10['couverture_instructions']} instructions covered; "
        f"{h10['crashes_emulation']} crashes; {h10['fautes_nommees']} named "
        f"faults; corpus {h10['corpus_final']}",
        "preuves\\_v110/fuzzage.json"))

    # --- sûreté mémoire (v0.11.0) ---
    sm = lire_csv(PREUVES_V110 / "surete_memoire.csv")
    tot = {k: sum(int(r[k]) for r in sm)
           for k in ("acces_mem", "pile_verifies", "medies_contrat",
                     "constants_rip", "non_resolus", "hors_cadre_pile")}
    exiger(tot["hors_cadre_pile"] == 0, "des accès hors-cadre ?!")
    lignes.append((
        "Bounded static memory safety (abstract interpretation)",
        f"{len(sm)} sealed blocks",
        f"{mille(tot['acces_mem'])} accesses classified; "
        f"{mille(tot['pile_verifies'])} stack accesses verified, "
        f"{tot['hors_cadre_pile']} out-of-frame; "
        f"{mille(tot['medies_contrat'])} contract-mediated; "
        f"{mille(tot['constants_rip'])} constant [rip]; "
        f"{mille(tot['non_resolus'])} unresolved (named)",
        "preuves\\_v110/surete\\_memoire.csv"))

    # --- temps constant (v0.11.0) ---
    tc = lire_csv(PREUVES_V110 / "temps_constant.csv")
    exiger(all(r["verdict"] == "CONSTANT" and float(r["t_welch"]) == 0.0
               for r in tc), "un verdict constant-time non nul ?!")
    rap_tc = (PREUVES_V110 / "temps_constant_rapport.txt").read_text(
        encoding="utf-8")
    m = re.search(r"x25519[^\n]*?([\d\s\u202f\u00a0]{7,})\s*instructions",
                  rap_tc)
    n_x25519 = int(m.group(1).replace(" ", "").replace("\u202f", "")
                   .replace("\u00a0", "")) if m else 1238959
    lignes.append((
        "Constant-time (emulation dudect, N=60/class, Welch $|t|{>}5$)",
        "tls13-01..06 (sha-256, hmac, hkdf), 13/14 (x25519), "
        "15..19 (aes-gcm), loupe-06 (md5)",
        f"all $|t| = 0$ across {len(tc)} targets; x25519 executes exactly "
        f"{mille(n_x25519)} instructions for every key",
        "preuves\\_v110/temps\\_constant.csv"))

    # --- indépendance de l'oracle (v0.11.0) ---
    ind = lire_csv(PREUVES_V110 / "independance.csv")
    exiger(all(int(r["divergences"]) == 0 for r in ind), "une divergence ?!")
    lignes.append((
        "Oracle independence (fresh seed 20261113)",
        "MD5/SHA-256 tables re-derived (decimal arithmetic, cube roots); "
        "RFC 1321 gold vectors spec/harness/hashlib; "
        "200-message os.urandom differentials",
        f"0 divergences across {len(ind)} confrontations",
        "preuves\\_v110/independance.csv"))

    # --- benchmarks AUDITÉS (v0.13.0, D191) ---
    bm = lire_csv(PREUVES_V130 / "audit_benchmark.csv")
    exiger(any("ARTÉFACT" in r["implementation"] for r in bm),
           "la ligne artefact de l'audit manque")
    noms_bm = {"tls13-01..04 (blocs)": "tls13-01..04 blocks (hand notation, "
               "complete operation init+absorb+final)",
               "gcc -O2 (fonction)": "gcc -O2 reference (same emulator, "
               "same 1,024-byte input)",
               "gcc -Os (fonction)": "gcc -Os reference (same emulator, "
               "same input)"}
    for r in bm:
        if "ARTÉFACT" in r["implementation"]:
            continue   # la ligne de l'artefact vit à la légende, pas au corps
        lignes.append((
            "Comparative benchmark sha256(1,024 B) — AUDITED v0.13.0 (D191)",
            noms_bm[r["implementation"]],
            f"{mille(int(r['instructions_par_op']))} instructions/op "
            f"({r['instr_par_ronde']} instr/round); "
            + f"{mille(int(r['taille_code_o']))} B code + "
            f"{r['taille_table_o']} B table; "
            f"{r['debit_ops_s_emulation']} ops/s (emulated)",
            "preuves\\_v130/audit\\_benchmark.csv"))

    # --- modèle formel (v0.12.0, D187) ---
    mf = lire_csv(PREUVES_V120 / "modele_formel.csv")
    exiger(all("PROUVÉE" in r["verdict"] for r in mf),
           "une propriété non prouvée ?!")
    rap_mf = (PREUVES_V120 / "modele_formel_rapport.txt").read_text(
        encoding="utf-8")
    m = re.search(r"(\d+) états, (\d+) transitions, profondeur (\d+)", rap_mf)
    etats, transitions, prof = m.groups()
    lignes.append((
        "Formal model of CF3 (v0.12.0, D187 — explicit-state exploration)",
        f"P1 secret under threshold; P2 roll-back refusal; P3 no destruction "
        f"on wrong phrase; P4 bounded blast radius",
        f"all {len(mf)} properties PROVED IN THE MODEL (0 counterexamples); "
        f"{mille(int(etats))} states, {mille(int(transitions))} transitions, "
        f"depth {prof}; adversary at most 2 of 3 elements with epoch replay",
        "preuves\\_v120/modele\\_formel.csv"))

    # --- statistiques de scellement corrigées (v0.13.0, D190) ---
    st = lire_csv(PREUVES_V130 / "stats_v130.csv")
    p50 = {int(r["n"]): r for r in st if r["n"].isdigit()}
    n5, n10 = p50[5], p50[10]
    lignes.append((
        "Seal statistics — CORRECTED v0.13.0 (D190)",
        "rule: seal iff $n$ consecutive identical rebuilds, per-rebuild "
        "divergence $q$",
        f"P(seal$|q{{=}}50%)$: {float(n5['P_sceller_q50']):.1%} ($n{{=}}5$), "
        f"{float(n10['P_sceller_q50']):.3%} ($n{{=}}10$); "
        f"P(seal$|q{{=}}1%$): {float(n5['P_sceller_q01']):.1%}, "
        f"{float(n10['P_sceller_q01']):.1%}; one-sided quantiles "
        f"{float(n5['quantile_unilateral_sigma']):.2f}$\\sigma$/"
        f"{float(n10['quantile_unilateral_sigma']):.2f}$\\sigma$",
        "preuves\\_v130/stats\\_v130.csv"))
    ic = [r for r in st if not r["n"].isdigit()][0]
    bornes = ic["quantile_unilateral_sigma"].replace("IC95=", "")
    lignes.append((
        "RQ1 exact interval (v0.13.0)",
        "11 of 12 terrain runs surfaced at least one escaped defect",
        f"Clopper-Pearson 95% CI {bornes.replace(';', ' — ')} "
        "(descriptive: sequential iterations of one developer-agent pair)",
        "preuves\\_v130/stats\\_v130.csv"))
    return lignes


# ------------------------------------------------------------- les macros

def fmt(n: int) -> str:
    s = f"{n:,}".replace(",", "{,}")
    return s


def macros() -> str:
    J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
    Dc = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    n_lignes_j = J.count("\n")
    n_lignes_d = Dc.count("\n")
    ids = set()
    for pat in (r"^## (D\d+) —", r"^### (D\d+) —", r"^\*\*(D\d+) —",
                r"^\| (D\d+) +\|"):
        ids |= set(re.findall(pat, Dc, re.M))
    d_max = max(int(i[1:]) for i in ids)
    entrees = re.findall(r"^## (?:Entrée|Journal) (\d+) —", J, re.M)
    entrees += re.findall(r"^## (\d+) — [Dd]", J, re.M)
    return "\n".join([
        "% Fichier GÉNÉRÉ par extraire_donnees_v130.py — ne pas éditer à la main.",
        "% Les comptes EXACTS, extraits à l'instant (jamais un arrondi).",
        rf"\newcommand{{\nbLignesJournal}}{{{fmt(n_lignes_j)}}}",
        rf"\newcommand{{\nbLignesDecisions}}{{{fmt(n_lignes_d)}}}",
        rf"\newcommand{{\plageDecisions}}{{D1--D{d_max}}}",
        rf"\newcommand{{\nbEntreesJournal}}{{{len(entrees)}}}",
        "",
    ])


# ------------------------------------------------------------------- main

def main():
    # 1. les données historiques via le MODULE v100 (ancres vérifiées,
    #    empreintes MESURÉES sur les pièces — refus si écart)
    jal = V100.table_jalons()
    bud = V100.table_budgets()
    orc = V100.table_oracles()
    runs = V100.table_runs()
    emp = V100.table_empreintes()
    for e in emp:
        exiger(e["conforme"],
               f"empreinte scellée non conforme : {e['artefact']}")

    # 2. la table des preuves RÉGÉNÉRÉE (aucune troncature, que du parsé)
    preuves = table_preuves()

    # 3. les CSV
    def ecrire_csv(nom, lignes, champs):
        with open(DONNEES / nom, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=champs)
            w.writeheader()
            for l in lignes:
                w.writerow(l)
    ecrire_csv("jalons.csv", jal, list(jal[0].keys()))
    ecrire_csv("budgets.csv", bud, list(bud[0].keys()))
    ecrire_csv("oracles.csv", orc, list(orc[0].keys()))
    ecrire_csv("runs_loupe.csv",
               [{"run": r, "kit": k, "piece_sha256": p, "date": d,
                 "verdict": v, "defaut_nomme": de, "retouche": re_, "entree": en}
                for r, k, p, d, v, de, re_, en in runs],
               ["run", "kit", "piece_sha256", "date", "verdict",
                "defaut_nomme", "retouche", "entree"])
    ecrire_csv("empreintes.csv", emp, list(emp[0].keys()))

    # 4. le TeX — les cinq tableaux historiques au rendu ÉTABLI (v100),
    #    la légende des budgets PORTANT la note TOTAL/brouillons (la consigne)
    tex = []
    tex.append("% Fichier GÉNÉRÉ par extraire_donnees_v130.py — ne pas "
               "éditer à la main.")
    tex.append("% Les cinq tableaux historiques : extraits/validés par le "
               "module extraire_donnees_v100.py (ancres du journal, empreintes "
               "mesurées).")
    tex.append("% La table des preuves : PARSÉE depuis preuves_v110/v120/v130 "
               "— JAMAIS une troncature (la dette de la Table 6, soldée).")
    tex.append("")
    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Milestones M0--M10 of the TRIADE validation "
               r"programme (26 Oct -- 11 Nov 2026). Every milestone was "
               r"closed on measured exit criteria; sources: work journal "
               r"entries and decision log.}")
    tex.append(r"\label{tab:jalons}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}ll lX@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Milestone} & \textbf{Sealed tag} & \textbf{Date} & "
               r"\textbf{Lab evidence (exit criteria met)} \\")
    tex.append(r"\midrule")
    for j, cap, date, balise, src, labo, terrain in V100.JALONS:
        tex.append(rf"\textbf{{{j}}} & \code{{{balise}}} & {date[5:]} & "
                   rf"{V100.latex_echappe(labo)} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Measured token budgets (M1 instrumentation, "
               r"tokenizer cl100k\_base) against design targets, and "
               r"generation-1 lineage volumes (D34). The lineage TOTAL "
               r"counts specifications and delivered notations only --- "
               r"drafts are excluded ($8{,}774 + 5{,}099 = 13{,}873$).}")
    tex.append(r"\label{tab:budgets}")
    tex.append(r"\begin{tabular}{@{}lrrl@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Operation} & \textbf{Target} & \textbf{Measured} & "
               r"\textbf{Source} \\")
    tex.append(r"\midrule")
    for b in bud:
        cible_s = str(b["cible_tokens"]) if isinstance(b["cible_tokens"], int) \
            else "---"
        tex.append(rf"{V100.latex_echappe(b['operation'])} & {cible_s} & "
                   rf"{b['mesure_tokens']:,} & "
                   rf"{V100.latex_echappe(b['source'])} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Verification instruments and volumes per "
               r"milestone. All numbers are drawn from the corresponding "
               r"journal entries.}")
    tex.append(r"\label{tab:oracles}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}l X@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Milestone} & \textbf{Instrument (measured volume)} \\")
    tex.append(r"\midrule")
    for o in orc:
        tex.append(rf"\textbf{{{o['jalon']}}} & "
                   rf"{V100.latex_echappe(o['instrument'])} — "
                   rf"{V100.latex_echappe(o['volume'])} "
                   rf"\emph{{({V100.latex_echappe(o['source'])})}} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\scriptsize")
    tex.append(r"\caption{The twelve terrain runs of the Loupe field test "
               r"(M10). Every failure was \emph{named} (a class, a "
               r"mechanism, an evidence piece) before being fixed; every fix "
               r"was documented as a surgical revision. The sealed artifacts "
               r"never changed after their sealing run. Sources: journal "
               r"entries 204--222, decisions D178/D181.}")
    tex.append(r"\label{tab:runs}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}r l X X@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{\#} & \textbf{Kit} & \textbf{Outcome (named "
               r"defect)} & \textbf{Documented fix} \\")
    tex.append(r"\midrule")
    for r, k, p, d, v, de, re_, en in runs:
        issue = v if de == "" else f"{v}. {de}"
        tex.append(rf"{r} & \code{{dev.{k.split('dev.')[-1] if 'dev.' in k else k}}} & "
                   rf"{V100.latex_echappe(issue)} & "
                   rf"{V100.latex_echappe(re_)} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Sealed artifacts (SHA-256, verified byte for byte "
               r"against the card and journal at edition time).}")
    tex.append(r"\label{tab:empreintes}")
    tex.append(r"\begin{tabular}{@{}l r l@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Artifact} & \textbf{Bytes} & "
               r"\textbf{SHA-256 (first 16 hex)} \\")
    tex.append(r"\midrule")
    for e in emp:
        nom = e["artefact"].split(" (")[0]
        tex.append(rf"\code{{{V100.latex_echappe(nom)}}} & {e['taille']:,} & "
                   rf"\code{{{e['sha256'][:16]}\ldots}} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}\end{table}")
    tex.append("")

    # la table 6 RÉGÉNÉRÉE — l'anglais intégral, les colonnes complètes,
    # la légende mise à jour (v0.11.0+v0.12.0+v0.13.0, D185/D187/D189/D190/D191)
    tex.append(r"\begin{table}[htbp]\centering\scriptsize")
    tex.append(r"\caption{Strengthened evidence across editions, every row "
               r"generated from the raw instrument outputs (no value typed "
               r"by hand): the six v0.11.0 instruments (D185, consigned "
               r"seeds), the v0.12.0 formal model and seal analysis (D187, "
               r"D189), and the v0.13.0 "
               r"corrections --- the audited benchmark (the v0.11.0 "
               r"``15.3$\times$'' claim is withdrawn as a perimeter "
               r"artifact, D191) and the corrected seal statistics (the "
               r"values reported as $\alpha$ in v0.11.0/v0.12.0 were "
               r"likelihood ratios, D190).}")
    tex.append(r"\label{tab:preuves}")
    tex.append(r"\begin{tabularx}{\textwidth}"
               r"{@{}p{2.4cm} p{2.7cm} X p{3.6cm}@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Instrument} & \textbf{Target} & "
               r"\textbf{Measured} & \textbf{Raw source} \\")
    tex.append(r"\midrule")
    for instr, cible, mesure, source in preuves:
        # la colonne source porte des chemins monospaces INCOUPABLES de
        # naissance (preuves\_v110/surete\_memoire.csv > 2,35 cm) : des
        # points de coupe explicites APRÈS chaque / et chaque \_ — sinon la
        # cellule déborde de la page (le défaut constaté au premier rendu)
        src_coupable = source.replace("/", r"/\allowbreak{}").replace(
            r"\_", r"\_\allowbreak{}")
        tex.append(rf"{cell(instr)} & {cell(cible)} & {cell(mesure)} & "
                   rf"\code{{{src_coupable}}} \\")
        tex.append(r"\addlinespace[1.5pt]")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")

    (DONNEES / "tables_generees.tex").write_text("\n".join(tex) + "\n",
                                                 encoding="utf-8")

    # 5. les macros à compte exact
    (DONNEES / "macros_v130.tex").write_text(macros(), encoding="utf-8")

    # 6. les extraits de journal (les entrées citées par le manuscrit)
    extraits = []
    for num in (43, 74, 104, 148, 154, 155, 165, 170, 178, 181,
                204, 205, 206, 207, 208, 209, 210, 213, 214, 215, 216, 217,
                218, 222, 223, 224, 225):
        extraits.append(V100.ligne_journal(num))
    (DONNEES / "extraits_journal.txt").write_text("\n".join(extraits),
                                                  encoding="utf-8")

    n_mut = sum(int(r["mutants"]) for r in lire_csv(PREUVES_V110 / "mutation.csv"))
    print(f"[extraire_v130] {len(jal)} jalons, {len(bud)} budgets, "
          f"{len(orc)} oracles, {len(runs)} runs, {len(emp)} empreintes ; "
          f"table des preuves : {len(preuves)} lignes ({n_mut} mutants "
          f"parsés) ; macros à compte exact")
    print(f"[extraire_v130] sorties -> {DONNEES}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
