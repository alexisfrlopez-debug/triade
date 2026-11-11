#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_ic_reclassement_v150.py — LA SECONDE MÉTHODE EN SCRIPT SÉPARÉ
(l'exigence de l'instruction xboh1kljq : « recalcule les deux IC avec une
seconde méthode (script séparé) et exige l'égalité à 10⁻³ »).

Le recompte (reclassement_defauts_v150.py) calcule les deux intervalles
Clopper-Pearson par scipy.stats.beta.ppf (première méthode) et consigne
les valeurs à preuves_v150/reclassement/taux.csv. LE PRÉSENT SCRIPT est
INDÉPENDANT : il ne fait AUCUN appel à scipy — il relit taux.csv,
RECALCULE chaque intervalle par la seconde méthode (une BISECTION sur la
fonction bêta incomplète régularisée implémentée à la main — la
continuation fraction de Lentz, Numerical Recipes § 6.4) et EXIGE
l'égalité des deux méthodes à 10⁻³ près, borne par borne, pour les DEUX
taux (pièce seule 7/12, ensemble kit+pièce 11/12).

Verdict : VERT si les quatre bornes concordent à 10⁻³ ; ÉCHEC sinon
(exception levée — aucun verdict fabriqué). Le verdict est consigné à
preuves_v150/reclassement/verification_ic.txt (pièce archivée).
"""
from __future__ import annotations

import csv
import math
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[1]
DOSSIER = REPO / "scripts" / "preuves_v150" / "reclassement"
TAUX_CSV = DOSSIER / "taux.csv"
VERDICT_TXT = DOSSIER / "verification_ic.txt"
TOLERANCE = 1e-3  # l'exigence : égalité à 10⁻³


# ---------------------------------------------------------------------------
# la seconde méthode, sans scipy : la fonction bêta incomplète régularisée
# I_x(a, b) par la continuation fraction de Lentz (NR § 6.4), puis la
# bisection sur la définition exacte de Clopper-Pearson
# ---------------------------------------------------------------------------

def _betacf(a: float, b: float, x: float) -> float:
    MAXIT, EPS, FPMIN = 200, 3e-15, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def betainc_reg(a: float, b: float, x: float) -> float:
    """La fonction bêta incomplète régularisée I_x(a, b) — sans scipy."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(lbeta) * _betacf(a, b, x) / a
    return 1.0 - math.exp(lbeta) * _betacf(b, a, 1.0 - x) / b


def cp_bissection(tues: int, total: int, alpha: float = 0.05):
    """Clopper-Pearson exact PAR BISECTION (la seconde méthode)."""
    if tues == 0:
        bas = 0.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if betainc_reg(tues, total - tues + 1, mid) < alpha / 2:
                lo = mid
            else:
                hi = mid
        bas = (lo + hi) / 2
    if tues == total:
        haut = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if betainc_reg(tues + 1, total - tues, mid) < 1 - alpha / 2:
                lo = mid
            else:
                hi = mid
        haut = (lo + hi) / 2
    return bas, haut


def main() -> int:
    lignes = list(csv.DictReader(open(TAUX_CSV, encoding="utf-8")))
    assert len(lignes) == 2, "taux.csv doit porter les DEUX taux"

    rapport = ["LA SECONDE MÉTHODE EN SCRIPT SÉPARÉ — le verdict "
               "(l'exigence xboh1kljq : égalité à 10⁻³)", ""]
    tout_vert = True
    for l in lignes:
        nom = l["taux"]
        tues, total = int(l["numérateur"]), int(l["dénominateur"])
        # les bornes CONSIGNÉES par la première méthode (scipy)
        ic_consigne = l["ic95_scipy"].strip("[]").split(",")
        b_cons, h_cons = float(ic_consigne[0]), float(ic_consigne[1])
        # le recalcul PAR LA SECONDE MÉTHODE (bisection, sans scipy)
        b_biss, h_biss = cp_bissection(tues, total)
        ecart_b, ecart_h = abs(b_cons - b_biss), abs(h_cons - h_biss)
        vert = ecart_b <= TOLERANCE and ecart_h <= TOLERANCE
        tout_vert = tout_vert and vert
        rapport.append(
            f"  {nom}\n"
            f"      consigné (scipy)      : [{b_cons:.4f}, {h_cons:.4f}]\n"
            f"      recalculé (bisection) : [{b_biss:.4f}, {h_biss:.4f}]\n"
            f"      écarts borne basse {ecart_b:.2e} / borne haute "
            f"{ecart_h:.2e} — {'VERT' if vert else 'ÉCHEC'} "
            f"(tolérance 10⁻³)")
        print(rapport[-1])
        assert vert, f"ÉCHEC : les deux méthodes divergent pour {nom}"

    rapport += ["", "VERDICT : VERT — les DEUX intervalles concordent à "
                "10⁻³ près par les deux méthodes indépendantes.", ""]
    VERDICT_TXT.write_text("\n".join(rapport), encoding="utf-8")
    print(f"\nVERDICT : {'VERT' if tout_vert else 'ÉCHEC'} — consigné à "
          f"{VERDICT_TXT.relative_to(REPO)}")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    raise SystemExit(main())
