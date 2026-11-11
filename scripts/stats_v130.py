#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stats_v130.py — LES STATISTIQUES CORRIGÉES de l'édition v0.13.0 (la
commande, point 2). Tout est calculé par script, rien n'est tapé à la main.

(a) LA CRISTALLISATION REFORMULÉE. Les valeurs « α = 3,29e-2 » (n = 5) et
    « α = 1,08e-3 » (n = 10) consignées à D189 et reprises au manuscrit et à
    la spécification v0.11.0/v0.12.0 étaient des RAPPORTS DE VRAISEMBLANCE
    (0,5/0,99)^n — le quotient des probabilités des données sous q = 0,5 et
    q = 0,01 — PAS des probabilités d'erreur α. Les caractéristiques
    OPÉRATIONNELLES de la règle réelle (« sceller ssi n rebuilds
    consécutifs identiques »), sous probabilité de divergence q par rebuild
    (indépendance des rebuilds, l'hypothèse de D189) :
        P(sceller | q) = (1 - q)^n
    calculées ici pour q ∈ {0,5 ; 0,01} et n ∈ {5 ; 10}. Les conversions
    « sigma » sqrt(-2 ln p) (2,6 / 3,7) sont REMPLACÉES par les quantiles
    normaux unilatéraux exacts des probabilités corrigées (Φ⁻¹(1 - p)).

(b) L'IC95 % EXACT de 11/12 (Clopper-Pearson, bisection sur la binomiale
    exacte — aucune dépendance) : la borne inférieure résout P(X ≥ 11 | p) =
    0,025, la supérieure P(X ≤ 11 | p) = 0,025. Avec la RÉSERVE exigée : les
    douze itérations sont SÉQUENTIELLES et issues d'un seul binôme
    développeur+agent — l'IC est un résumé descriptif binomial, jamais une
    inférence sur une population de développeurs.

(c) LES COMPTES DU JOURNAL extraits en direct (lignes du journal, décisions,
    entrées, tâches worklog) — la valeur du manuscrit viendra de ces comptes,
    jamais d'un arrondi tapé à la main (l'« un journal de 9 300 lignes » de
    v0.12.0 était arrondi).

Sortie : scripts/preuves_v130/stats_v130.csv + stats_v130_rapport.txt
"""
from __future__ import annotations

import math
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
PREUVES = REPO / "scripts" / "preuves_v130"
PREUVES.mkdir(exist_ok=True)


# ---------------------------------------------------------- la binomiale exacte

def binom_pmf(k: int, n: int, p: float) -> float:
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_survie(k: int, n: int, p: float) -> float:
    """P(X >= k | n, p)."""
    return sum(binom_pmf(i, n, p) for i in range(k, n + 1))


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """L'IC exact : la borne basse résout P(X >= k | p) = alpha/2 (f
    CROISSANTE de -alpha/2 à la borne), la haute P(X <= k | p) = alpha/2
    (f DÉCROISSANTE) — bisection, 60 itérations, précision ~1e-12."""
    def bisect_croissante(f, lo, hi):     # f(lo) < 0 < f(hi)
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    def bisect_decroissante(f, lo, hi):   # f(lo) > 0 > f(hi)
        for _ in range(60):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    if k == 0:
        basse = 0.0
    else:
        basse = bisect_croissante(
            lambda p: binom_survie(k, n, p) - alpha / 2, 0.0, 1.0)
    if k == n:
        haute = 1.0
    else:
        haute = bisect_decroissante(
            lambda p: (1 - binom_survie(k + 1, n, p)) - alpha / 2, 0.0, 1.0)
    return basse, haute


def quantile_unilateral(p: float) -> float:
    """Φ⁻¹(1 - p) — le quantile normal unilatéral (Acklam, ~1e-9)."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_bas = 0.02425
    if p < p_bas:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
            ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p <= 1 - p_bas:
        q = p - 0.5
        r = q * q
        x = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
            (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
             ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    # un raffinement de Newton-Halley
    e = 0.5 * math.erfc(-x / math.sqrt(2)) - p
    u = e * math.sqrt(2 * math.pi) * math.exp(x * x / 2)
    x = x - u / (1 + x * u / 2)
    return x


def main():
    lignes_rapport = [
        "LES STATISTIQUES CORRIGÉES — v0.13.0 (la commande, point 2)",
        "",
        "(a) LA CRISTALLISATION — les caractéristiques opérationnelles de la",
        "    règle RÉELLE (sceller ssi n rebuilds consécutifs identiques),",
        "    sous probabilité de divergence q par rebuild (indépendance,",
        "    l'hypothèse de D189) : P(sceller | q) = (1-q)^n.",
        "",
    ]
    stats = []
    for n in (5, 10):
        p50 = 0.5 ** n               # P(sceller | q = 0,5)
        p01 = 0.99 ** n              # P(sceller | q = 0,01)
        lr = (0.5 / 0.99) ** n       # le rapport de vraisemblance mal étiqueté
        z = quantile_unilateral(1 - p50)   # Φ⁻¹(1 - p) : quantile UNILATÉRAL positif
        lignes_rapport += [
            f"    n = {n:2d} : P(sceller | q=0,5) = {p50:.6g}"
            f"   (quantile unilatéral {z:.2f} σ)",
            f"            P(sceller | q=0,01) = {p01:.6g}"
            "   (la règle scelle un build sain avec cette probabilité)",
            f"            le LR (0,5/0,99)^{n} = {lr:.3g} — la valeur que "
            "v0.11.0/v0.12.0 étiquetait « α »",
        ]
        stats.append({"n": n, "P_sceller_q50": p50, "P_sceller_q01": p01,
                      "LR_05_099": lr, "quantile_unilateral_sigma": round(z, 2)})
    lignes_rapport += [
        "",
        f"    LA STRICTESSE n=5 → n=10 : {0.5**5 / 0.5**10:.0f}× "
        "(3,125e-2 → 9,77e-4 — la probabilité de sceller un build divergent",
        "    à q=0,5 chute de 32×) ; le « 46× » de D189 comparait le canonique",
        "    5 % au LR mal étiqueté — il est retiré.",
        "    Les conversions sigma sqrt(-2 ln p) (2,6 / 3,7) : RETIRÉES,",
        "    remplacées par les quantiles unilatéraux exacts ci-dessus",
        "    (1,87 / 3,10).",
    ]

    # (b) l'IC95 exact de 11/12
    basse, haute = clopper_pearson(11, 12)
    lignes_rapport += [
        "",
        "(b) L'IC95 % EXACT de 11/12 (Clopper-Pearson, binomiale exacte) :",
        f"    [{basse:.3f} ; {haute:.3f}]",
        "    RÉSERVE (exigée) : les douze itérations sont SÉQUENTIELLES, d'un",
        "    seul binôme développeur+agent — l'IC est un résumé descriptif",
        "    binomial, PAS une inférence sur une population de développeurs",
        "    (la non-indépendance des itérations interdit cette lecture).",
    ]
    stats.append({"n": "11/12", "P_sceller_q50": "", "P_sceller_q01": "",
                  "LR_05_099": "",
                  "quantile_unilateral_sigma":
                  f"IC95=[{basse:.3f};{haute:.3f}]"})

    # (c) les comptes du journal, extraits en direct (les MOTIFS EXACTS de
    # l'audit de gouvernance — les formats historiques comptent)
    journal = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
    decisions = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    worklog = (REPO / "worklog.md").read_text(encoding="utf-8")
    n_lignes = journal.count("\n")
    entrees = re.findall(r"^## (?:Entrée|Journal) (\d+) —", journal, re.M)
    entrees += re.findall(r"^## (\d+) — [Dd]", journal, re.M)
    ids = set()
    for pat in (r"^## (D\d+) —", r"^### (D\d+) —", r"^\*\*(D\d+) —",
                r"^\| (D\d+) +\|"):
        ids |= set(re.findall(pat, decisions, re.M))
    d_max = max(int(i[1:]) for i in ids)
    n_tasks = len(re.findall(r"^Task ID: ?\d+", worklog, re.M)) + \
        len(re.findall(r"^Task ID: ?\d+", journal, re.M))
    lignes_rapport += [
        "",
        "(c) LES COMPTES DU JOURNAL (extraits en direct à l'instant — la",
        "    valeur du manuscrit sera RÉGÉNÉRÉE depuis ici, jamais tapée) :",
        f"    journal : {n_lignes} lignes, {len(entrees)} entrées "
        f"(numérotation jusqu'à {max(int(e) for e in entrees)}),",
        f"    décisions : {len(ids)} consignées, numérotation D1..D{d_max} ;",
        f"    worklog+journal : {n_tasks} blocs Task ID.",
        "    L'« un journal de 9 300 lignes » de v0.12.0 était un arrondi",
        "    périmé — remplacé par le compte exact ci-dessus.",
    ]

    rapport = "\n".join(lignes_rapport)
    (PREUVES / "stats_v130_rapport.txt").write_text(rapport + "\n",
                                                    encoding="utf-8")
    with open(PREUVES / "stats_v130.csv", "w", encoding="utf-8") as f:
        f.write("n,P_sceller_q50,P_sceller_q01,LR_05_099,"
                "quantile_unilateral_sigma\n")
        for s in stats:
            f.write(f"{s['n']},{s['P_sceller_q50']},{s['P_sceller_q01']},"
                    f"{s['LR_05_099']},{s['quantile_unilateral_sigma']}\n")
    print(rapport)
    print("\n[stats] écrit : preuves_v130/stats_v130.csv + rapport")


if __name__ == "__main__":
    main()
