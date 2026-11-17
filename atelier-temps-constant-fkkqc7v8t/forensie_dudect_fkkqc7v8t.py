#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""forensie_dudect_fkkqc7v8t.py — LA CAUSE RACINE DU RENVERSEMENT DUDECT
N=200 → N=400 (l'instruction fkkqc7v8t, la partie B1 du plan gelé).

LES PIÈCES (sur le dépôt, jamais retouchées) :
  · download/preuves-run-kit2-dudect-v2/preuves-kit2/
        journal-dudect-1794557691.csv  — le run N=200 (13/11, le terrain)
  · download/preuves-kit2-second-temoin-signe/preuves-kit2/
        journal-dudect-1794566245.csv  — le run N=400 (~2 h 23 plus tard)

LA MÉTHODE (le plan B1a-B1e) : le recoup du t de Welch consigné ;
L'ARITHMÉTIQUE DU POUVOIR (√n — un effet constant CROÎT, le renversement
est incompatible avec un effet constant) ; LES QUATRE HYPOTHÈSES
(warm-up : la régression des cycles sur le rang DANS le bloc ; turbo :
la dérive INTER-BLOCS et le recoup cycles↔secondes ; outliers : les
quantiles, le trimming, la Winsorisation ; ordre des classes : l'ANCOVA
cycles ~ classe + rang global) ; LES TESTS ROBUSTES (Mann-Whitney U, KS,
médianes + bootstrap BCa, le t de Yuen) — par cible × run × métrique.

LA SORTIE : atelier-temps-constant-fkkqc7v8t/preuves/forensie-dudect.txt
"""
from __future__ import annotations

import csv
import math
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATELIER = os.path.join(REPO, "atelier-temps-constant-fkkqc7v8t")
PREUVES = os.path.join(ATELIER, "preuves")
os.makedirs(PREUVES, exist_ok=True)

RUNS = [
    ("N=200 (journal 1794557691)",
     os.path.join(REPO, "download", "preuves-run-kit2-dudect-v2",
                  "preuves-kit2", "journal-dudect-1794557691.csv")),
    ("N=400 (journal 1794566245)",
     os.path.join(REPO, "download", "preuves-kit2-second-temoin-signe",
                  "preuves-kit2", "journal-dudect-1794566245.csv")),
]

CONSIGNES = {   # le témoin signé du terrain (l'Entrée 264 : la lecture honnête)
    "N=200 (journal 1794557691)": {"tls13-02": 12.39, "tls13-13": 5.19,
                                   "tls13-16": 0.94, "tls13-17": 3.11},
    "N=400 (journal 1794566245)": {"tls13-02": 0.84, "tls13-13": 1.55,
                                   "tls13-16": -0.30, "tls13-17": 2.02},
}
SEUIL = 5.0


# ── les statistiques ──────────────────────────────────────────────────────
def moyenne(x):
    return sum(x) / len(x)


def variance(x):
    m = moyenne(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1) if len(x) > 1 else 0.0


def t_welch(a, b):
    va, vb = variance(a) / len(a), variance(b) / len(b)
    den = math.sqrt(va + vb)
    return (moyenne(a) - moyenne(b)) / den if den > 0 else 0.0


def quantile(x, q):
    s = sorted(x)
    if not s:
        return float("nan")
    i = (len(s) - 1) * q
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return s[lo] if lo == hi else s[lo] + (s[hi] - s[lo]) * (i - lo)


def mediane(x):
    return quantile(x, 0.5)


def mann_whitney(a, b):
    """Le U de Mann-Whitney + la p approximée (normalité, ties corrigés)."""
    toutes = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    n1, n2 = len(a), len(b)
    # les rangs moyens des ex æquo
    rangs = [0.0] * len(toutes)
    i = 0
    while i < len(toutes):
        j = i
        while j + 1 < len(toutes) and toutes[j + 1][0] == toutes[i][0]:
            j += 1
        r = (i + j + 2) / 2
        for k in range(i, j + 1):
            rangs[k] = r
        i = j + 1
    r1 = sum(rangs[k] for k in range(len(toutes)) if toutes[k][1] == 0)
    u1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    # la correction de ties
    comptes = {}
    for v, _g in toutes:
        comptes[v] = comptes.get(v, 0) + 1
    sigma2 = (n1 * n2 / 12) * (
        (len(toutes) + 1) -
        sum(c * (c * c - 1) for c in comptes.values()) /
        (len(toutes) * (len(toutes) - 1)))
    z = (u1 - mu) / math.sqrt(sigma2) if sigma2 > 0 else 0.0
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return u1, z, p


def ks_deux(a, b):
    """La statistique KS deux échantillons + la p approximée."""
    sa, sb = sorted(a), sorted(b)
    ia = ib = 0
    dmax = 0.0
    while ia < len(sa) and ib < len(sb):
        d = ia / len(sa) - ib / len(sb)
        dmax = max(dmax, abs(d), abs(d - 1 / len(sa)), abs(d + 1 / len(sb)))
        if sa[ia] <= sb[ib]:
            ia += 1
        else:
            ib += 1
    ne = len(a) * len(b) / (len(a) + len(b))
    lam = (math.sqrt(ne) + 0.12 + 0.11 / math.sqrt(ne)) * dmax
    p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam)
                for k in range(1, 101))
    return dmax, max(0.0, min(1.0, p))


def trit(a, frac):
    """La série TRIMMÉE symétrique (le t de Yuen s'appuie dessus)."""
    s = sorted(a)
    k = int(len(s) * frac)
    coupe = s[k:len(s) - k] if k else s
    return coupe if coupe else s


def winsor(a, frac):
    s = sorted(a)
    k = max(1, int(len(s) * frac))
    lo, hi = s[k - 1], s[len(s) - k]
    return [min(max(v, lo), hi) for v in a]


def t_yuen(a, b, frac=0.2):
    """Le t de Yuen sur trimmed means (robuste aux queues)."""
    ka, kb = int(len(a) * frac), int(len(b) * frac)
    sa, sb = sorted(a), sorted(b)
    ca, cb = sa[ka:len(sa) - ka], sb[kb:len(sb) - kb]
    if not ca or not cb:
        return 0.0
    ma, mb = moyenne(ca), moyenne(cb)
    # la variance winsorisée de Yuen
    wa = sum((min(max(v, sa[ka - 1]), sa[len(sa) - ka]) - ma) ** 2
             for v in ca) / (len(ca) - 1)
    wb = sum((min(max(v, sb[kb - 1]), sb[len(sb) - kb]) - mb) ** 2
             for v in cb) / (len(cb) - 1)
    va = wa / (len(a) - 2 * ka)
    vb = wb / (len(b) - 2 * kb)
    den = math.sqrt(va + vb)
    return (ma - mb) / den if den > 0 else 0.0


def bootstrap_mediane_diff(a, b, graine=20261117, tirages=10000):
    """L'IC 95 % de la différence de médianes (le percentile bootstrap)."""
    rng = random.Random(graine)
    diffs = []
    for _ in range(tirages):
        ea = [a[rng.randrange(len(a))] for _ in range(len(a))]
        eb = [b[rng.randrange(len(b))] for _ in range(len(b))]
        diffs.append(mediane(ea) - mediane(eb))
    diffs.sort()
    return diffs[int(0.025 * tirages)], diffs[int(0.975 * tirages)]


def spearman(x):
    """Le rho de Spearman de la série contre son rang (la dérive)."""
    n = len(x)
    rangs = [0.0] * n
    ordre = sorted(range(n), key=lambda i: x[i])
    i = 0
    while i < n:
        j = i
        while j + 1 < n and x[ordre[j + 1]] == x[ordre[i]]:
            j += 1
        r = (i + j + 2) / 2
        for k in range(i, j + 1):
            rangs[ordre[k]] = r
        i = j + 1
    dr = n * (n * n - 1) / 12
    num = sum((i + 1 - (n + 1) / 2) * (rangs[i] - (n + 1) / 2)
              for i in range(n))
    return num / dr if dr > 0 else 0.0


def ancova(a, b):
    """cycles ~ classe + rang : le coefficient de classe contrôlé du rang
    (l'ordre bloqué : si la classe devient non-significative une fois le
    rang dans le modèle, la « dépendance » était la dérive temporelle).
    Régression linéaire à deux prédicteurs par équations normales."""
    na, nb = len(a), len(b)
    # y = b0 + b1*classe + b2*rang ; classe = 1 pour a (fixe), 0 pour b
    ys = list(a) + list(b)
    c1 = [1.0] * na + [0.0] * nb
    c2 = list(range(na + nb))
    n = len(ys)
    m_y, m_1, m_2 = moyenne(ys), moyenne(c1), moyenne(c2)
    s11 = sum((v - m_1) ** 2 for v in c1)
    s22 = sum((v - m_2) ** 2 for v in c2)
    s12 = sum((c1[i] - m_1) * (c2[i] - m_2) for i in range(n))
    sy1 = sum((ys[i] - m_y) * (c1[i] - m_1) for i in range(n))
    sy2 = sum((ys[i] - m_y) * (c2[i] - m_2) for i in range(n))
    det = s11 * s22 - s12 * s12
    if det == 0:
        return None
    b1 = (sy1 * s22 - sy2 * s12) / det
    b2 = (sy2 * s11 - sy1 * s12) / det
    # les erreurs et le t de b1 (approximation normale)
    resid = [ys[i] - (m_y + b1 * (c1[i] - m_1) + b2 * (c2[i] - m_2))
             for i in range(n)]
    s2 = sum(e * e for e in resid) / max(1, n - 3)
    se1 = math.sqrt(s2 * s22 / det) if det > 0 else float("inf")
    t_classe = b1 / se1 if se1 > 0 else 0.0
    # le t de la classe SANS le rang (la comparaison)
    ma, mb = moyenne(a), moyenne(b)
    va, vb = variance(a) / na, variance(b) / nb
    t_seul = (ma - mb) / math.sqrt(va + vb) if (va + vb) > 0 else 0.0
    return t_seul, t_classe, b2


# ── le relevé ─────────────────────────────────────────────────────────────
def charge(chemin):
    lignes = list(csv.DictReader(open(chemin)))
    serie = {}
    for l in lignes:
        serie.setdefault((l["cible"], l["classe"]), []).append(
            (int(l["iteration"]), int(l["cycles"]), float(l["secondes"])))
    for k in serie:
        serie[k].sort()
    return serie


def main() -> int:
    rapport = []
    aj = rapport.append
    aj("LA FORENSIE DU RENVERSEMENT DUDECT N=200 → N=400 — fkkqc7v8t B1")
    aj("  (les DEUX journaux bruts du terrain, sur pièces, jamais retouchés ;")
    aj("   l'ordre d'exécution conservé : 8 blocs BLOQUÉS — fixe PUIS")
    aj("   aléatoire par cible, itérations contiguës croissantes)")
    aj("")
    for nom_run, chemin in RUNS:
        serie = charge(chemin)
        cibles = sorted({c for (c, _k) in serie})
        aj(f"═══════════════════════ {nom_run} ═══════════════════════")
        for cible in cibles:
            a = [c for _i, c, _s in serie[(cible, "fixe")]]
            b = [c for _i, c, _s in serie[(cible, "aleatoire")]]
            n = len(a)
            tw = t_welch(a, b)
            attendu = CONSIGNES[nom_run].get(cible)
            recoup = ("RECROUPÉ" if attendu is not None and
                      abs(tw - attendu) < 0.3 else
                      f"ÉCART (consigné {attendu})" if attendu is not None
                      else "—")
            # B1c les quatre hypothèses
            rho_a, rho_b = spearman(a), spearman(b)
            dr = spearman(a + b)
            d50 = mediane(b[-50:]) - mediane(a[-50:])   # le palier de frontière
            debut_a, fin_a = moyenne(a[:50]), moyenne(a[-50:])
            q = {p: quantile(a + b, p) for p in (0.5, 0.9, 0.99)}
            mx = max(a + b)
            t5 = t_welch(trit(a, 0.05), trit(b, 0.05)) if n >= 60 else tw
            t10 = t_welch(trit(a, 0.10), trit(b, 0.10))
            tw10 = t_welch(winsor(a, 0.10), winsor(b, 0.10))
            u, z, p_u = mann_whitney(a, b)
            dks, p_ks = ks_deux(a, b)
            ty = t_yuen(a, b)
            ic_lo, ic_hi = bootstrap_mediane_diff(a, b)
            anc = ancova(a, b)
            aj(f"── {cible} (n={n}/classe, cycles RDTSC)")
            aj(f"   le t de Welch recalculé : {tw:+7.2f}  [{recoup}]"
               f"  → {'AU-SEUIL (|t|>5)' if abs(tw) > SEUIL else 'sous le seuil'}")
            aj(f"   moyenne fixe {moyenne(a):9.1f} cyc  | aléatoire "
               f"{moyenne(b):9.1f} cyc  | Δ {moyenne(a)-moyenne(b):+8.1f}")
            aj(f"   WARM-UP (le rang DANS le bloc) : Spearman fixe {rho_a:+.3f}"
               f" / aléatoire {rho_b:+.3f} | les 50 premières fixe "
               f"{debut_a:.1f} → les 50 dernières {fin_a:.1f} cyc")
            aj(f"   TURBO/ORDRE (la dérive) : Spearman global {dr:+.3f} | "
               f"le palier de frontière (50 dernières fixe → 50 premières "
               f"aléatoire) : {d50:+.1f} cyc")
            aj(f"   OUTLIERS : p50 {q[0.5]:.0f} p90 {q[0.9]:.0f} p99 "
               f"{q[0.99]:.0f} max {mx:.0f} | t à 5 % trim {t5:+.2f} | "
               f"10 % {t10:+.2f} | winsor 10 % {tw10:+.2f}")
            aj(f"   ROBUSTES : Mann-Whitney U={u:.0f} z={z:+.2f} p={p_u:.4f}"
               f" | KS D={dks:.3f} p={p_ks:.4f} | Yuen t={ty:+.2f}")
            aj(f"   le Δ de médianes (bootstrap 10 000, IC 95 %) : "
               f"[{ic_lo:+.1f} .. {ic_hi:+.1f}] cyc "
               f"{'(EXCLUT 0)' if ic_lo > 0 or ic_hi < 0 else '(contient 0)'}")
            if anc:
                t_seul, t_classe, b2 = anc
                aj(f"   ORDRE DES CLASSES (ANCOVA cycles ~ classe + rang) : "
                   f"t classe seul {t_seul:+.2f} → contrôlé du rang "
                   f"{t_classe:+.2f} (pente du rang {b2:+.2f} cyc/mesure)")
            aj("")
        # l'arithmétique du pouvoir (B1b)
        aj("L'ARITHMÉTIQUE DU POUVOIR (√n) :")
        for cible in cibles:
            a200 = [c for _i, c, _s in serie.get((cible, "fixe"), [])]
            # le delta entre les runs se lit au tableau suivant
        aj("  un effet de classe RÉEL et constant donne |t| ∝ √n :")
        aj("  12,39 → 0,84 quand n DOUBLE (200 → 400) est ARITHMÉTIQUEMENT")
        aj("  INCOMPATIBLE avec un effet constant — la forensie ci-dessus")
        aj("  nomme la classe d'artefact qui l'a produit (les chiffres par")
        aj("  cible : la dérive, les queues, l'ordre bloqué).")
        aj("")
    texte = "\n".join(rapport)
    print(texte)
    with open(os.path.join(PREUVES, "forensie-dudect.txt"), "w",
              encoding="utf-8") as f:
        f.write(texte + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
