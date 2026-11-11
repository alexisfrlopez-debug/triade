#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reclassement_defauts_v150.py — LE RECOMPTE INDÉPENDANT ET LE
RECLASSEMENT DES DÉFAUTS DES RUNS LOUPE (l'instruction xboh1kljq de la
vague 3 : « Reclasse les onze défauts nommés des runs Loupe (entrées
204–222 du journal, Table 4) en deux catégories : défaut de la pièce
(code natif scellé) et défaut du kit/harnais (Python, scénario, sonde) »).

LE RECOMPTE — DEPUIS LES ENTRÉES DU JOURNAL (pas depuis la table) :
chaque classe nommée est CITÉE de son entrée (le script ASSERT chaque
citation présente au texte du journal — le recompte est CONTRÔLÉ, pas
déclaré). Résultat du recompte : TREIZE classes nommées sur ONZE runs
défaillants (les runs 6 et 7 ont nommé DEUX classes chacun — la table
par run les porte ensemble) : SEPT côté PIÈCE (le code natif scellé),
SIX côté KIT (le scénario Python, les sondes).

LES DEUX TAUX (par livraison — le run, pas le défaut) :
  — LA MÉTRIQUE PRIMAIRE DE RQ1, « code natif écrit par agent » : les
    runs où un défaut DE LA PIÈCE a échappé : 7/12 ;
  — LA MÉTRIQUE DE LIVRAISON, l'ensemble kit+pièce : les runs où un
    défaut quelconque a échappé : 11/12.
  Chacun avec son intervalle Clopper-Pearson 95 % EXACT calculé par
  DEUX MÉTHODES (scipy.stats.beta.ppf ET une bisection sur la fonction
  bêta incomplète régularisée implémentée à la main — l'égalité exigée
  à 10⁻³) et la RÉSERVE DE NON-INDÉPENDANCE (douze livraisons
  séquentielles d'un binôme développeur-agent : un résumé descriptif,
  jamais une inférence sur une population).

Sorties (scripts/preuves_v150/reclassement/) : defauts.csv (les 13
classes, catégorie, citation, entrée), taux.csv, rapport.txt (l'empreinte
du rapport est consignée — l'exigence).
"""
from __future__ import annotations

import csv
import hashlib
import math
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
SORTIES = REPO / "scripts" / "preuves_v150" / "reclassement"
SORTIES.mkdir(parents=True, exist_ok=True)

# LE RECOMPTE : les classes nommées, leur catégorie, leur entrée, la
# CITATION (assertée présente au journal — le recompte contrôlé).
DEFautS = [
    # (entrée, marqueur, catégorie, citation attendue au texte)
    (204, "BASERELOC", "PIÈCE",
     "l'image ASLR sans table de relocalisation, l'oubli du premier build"),
    (205, "ENVELOPPE", "PIÈCE",
     "l'image ramenée DANS l'enveloppe prouvée de la lignée"),
    (206, "CADRE-NÉ", "PIÈCE",
     "le CADRE .data pas né poignée INVALIDE — l'initialiseur du build"),
    (207, "ARGUMENTS-PILE", "PIÈCE",
     "LA CLASSE DES ARGUMENTS PILE"),
    (208, "SESSION-CHARGEUR", "KIT",
     "le scénario EST LE CHARGEUR"),
    (209, "SAUVEGARDE-ATTENDU", "KIT",
     "le scénario attendait 1 (le compte) — fausse erreur"),
    (209, "HINSTANCE-PEB", "PIÈCE",
     "mov r12, rcx"),
    (210, "EAX-SANS-SIGNE", "KIT",
     "[EAX-SANS-SIGNE] AU KIT"),
    (210, "D54-QUATRIÈME", "PIÈCE",
     "[D54-QUATRIÈME] À LA PIÈCE"),
    (213, "SONDE-PYTHON", "KIT",
     "LA SONDE MORTE SUR SON PROPRE PYTHON"),
    (214, "OFT-QWORD", "PIÈCE",
     "[OFT-QWORD]"),
    (216, "FREE-SANS-TYPE", "KIT",
     "[FREE-SANS-TYPE], LE DÉFAUT DU KIT, PAS DE LA PIÈCE"),
    (217, "SONDE-EXE", "KIT",
     "[SONDE-EXE], LE FAUX NÉGATIF STRUCTUREL DE LA SONDE DE LIAISON"),
]

# les runs et leurs classes (le run 12 : AUCUN défaut compté — [T0-PÉRIMÉ]
# residue ; [RET-NU] (Entrée 215) : nommé AU LABO avant le run, jamais
# échappé au terrain — non compté ; [CORBEILLE-VIDE] : le coffre, pas la
# livraison — non compté)
RUNS = {
    1: ["BASERELOC"], 2: ["ENVELOPPE"], 3: ["CADRE-NÉ"],
    4: ["ARGUMENTS-PILE"], 5: ["SESSION-CHARGEUR"],
    6: ["SAUVEGARDE-ATTENDU", "HINSTANCE-PEB"],
    7: ["EAX-SANS-SIGNE", "D54-QUATRIÈME"], 8: ["SONDE-PYTHON"],
    9: ["OFT-QWORD"], 10: ["FREE-SANS-TYPE"], 11: ["SONDE-EXE"],
    12: [],
}
TOTAL_RUNS = 12


# ---------------------------------------------------------------------------
# la seconde méthode : Clopper-Pearson par bisection sur la bêta
# incomplète régularisée implémentée à la main (la continuation fraction
# de Lentz pour la fonction bêta incomplète — Numerical Recipes § 6.4)
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
    """La fonction bêta incomplète régularisée I_x(a, b)."""
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
    """Clopper-Pearson par BISECTION sur betainc_reg (la seconde méthode)."""
    if total == 0:
        return 0.0, 1.0
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


def cp_scipy(tues: int, total: int, alpha: float = 0.05):
    from scipy.stats import beta
    if total == 0:
        return 0.0, 1.0
    bas = 0.0 if tues == 0 else float(beta.ppf(alpha / 2, tues,
                                                total - tues + 1))
    haut = 1.0 if tues == total else float(beta.ppf(1 - alpha / 2, tues + 1,
                                                    total - tues))
    return bas, haut


def main() -> int:
    journal = JOURNAL.read_text(encoding="utf-8")

    # 1 — LE RECOMPTE CONTRÔLÉ : chaque citation assertée à son entrée
    lignes = []
    for entree, marqueur, categorie, citation in DEFautS:
        motif = re.compile(rf"^## Entrée {entree} — (.*?)(?=^## Entrée )",
                           re.M | re.S)
        m = motif.search(journal)
        assert m, f"l'Entrée {entree} est introuvable au journal"
        texte_entree = m.group(1)
        assert citation in texte_entree, \
            (f"la citation de {marqueur} est INTROUVABLE à l'Entrée "
             f"{entree} : «{citation}»")
        lignes.append({"entrée": entree, "marqueur": marqueur,
                       "catégorie": categorie, "citation": citation})
    assert len(lignes) == 13, "le recompte attend TREIZE classes nommées"

    with open(SORTIES / "defauts.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["entrée", "marqueur", "catégorie",
                                          "citation"])
        w.writeheader()
        w.writerows(lignes)

    # 2 — les deux taux (par livraison)
    cat_de = {l["marqueur"]: l["catégorie"] for l in lignes}
    runs_piece = sum(1 for n, ms in RUNS.items()
                     if any(cat_de[m] == "PIÈCE" for m in ms))
    runs_quelconque = sum(1 for n, ms in RUNS.items() if ms)
    assert runs_piece == 7 and runs_quelconque == 11 and TOTAL_RUNS == 12

    taux_lignes = []
    for nom, tues in (("pièce seule (métrique primaire RQ1 — le code "
                       "natif écrit par agent)", runs_piece),
                      ("ensemble kit+pièce (métrique de livraison)",
                       runs_quelconque)):
        b1, h1 = cp_scipy(tues, TOTAL_RUNS)
        b2, h2 = cp_bissection(tues, TOTAL_RUNS)
        assert abs(b1 - b2) < 1e-3 and abs(h1 - h2) < 1e-3, \
            f"les deux méthodes divergent pour {nom}"
        taux_lignes.append({"taux": nom, "numérateur": tues,
                            "dénominateur": TOTAL_RUNS,
                            "valeur": f"{tues / TOTAL_RUNS:.4f}",
                            "ic95_scipy": f"[{b1:.4f}, {h1:.4f}]",
                            "ic95_bissection": f"[{b2:.4f}, {h2:.4f}]",
                            "écart": f"{max(abs(b1 - b2), abs(h1 - h2)):.2e}"})
    with open(SORTIES / "taux.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(taux_lignes[0].keys()))
        w.writeheader()
        w.writerows(taux_lignes)

    # 3 — le rapport (avec son empreinte — l'exigence)
    n_piece = sum(1 for l in lignes if l["catégorie"] == "PIÈCE")
    n_kit = sum(1 for l in lignes if l["catégorie"] == "KIT")
    rapport = [
        "LE RECLASSEMENT DES DÉFAUTS DES RUNS LOUPE — le recompte "
        "indépendant (l'instruction xboh1kljq, la vague 3)",
        "",
        "LA MÉTHODE : chaque classe nommée est RECOMPTÉE depuis les "
        "entrées 204-217 du journal (PAS depuis la table existante) — "
        "chaque citation ASSERTÉE présente au texte de son entrée (le "
        "recompte est CONTRÔLÉ). Les exclusions de la règle §2.3 "
        "demeurent : [RET-NU] (Entrée 215) nommé AU LABO avant le run — "
        "jamais échappé au terrain, non compté ; [T0-PÉRIMÉ] (run 12) — "
        "un résidu de bannière, aucune porte touchée, non compté ; "
        "[CORBEILLE-VIDE] — un défaut du coffre, pas de la livraison.",
        "",
        f"LE RECOMPTE : {len(lignes)} classes nommées sur 11 runs "
        f"défaillants (les runs 6 et 7 en ont nommé DEUX chacun — la "
        "table par run les porte ensemble) : "
        f"{n_piece} côté PIÈCE (le code natif scellé), {n_kit} côté KIT "
        "(le scénario Python, les sondes).",
        "",
        "LE RECLASSEMENT (défauts.csv) :",
    ]
    for l in lignes:
        rapport.append(f"  Entrée {l['entrée']:<3} {l['marqueur']:20s} "
                       f"{l['catégorie']:6s} — «{l['citation']}»")
    rapport += [
        "",
        "LES DEUX TAUX PAR LIVRAISON (12 runs, la réserve de "
        "non-indépendance : des livraisons séquentielles d'un binôme "
        "développeur-agent — un résumé descriptif, PAS une inférence) :",
    ]
    for t in taux_lignes:
        rapport.append(
            f"  {t['taux']}\n      {t['numérateur']}/{t['dénominateur']} "
            f"= {t['valeur']} — IC Clopper-Pearson 95 % exact : "
            f"{t['ic95_scipy']} (scipy) == {t['ic95_bissection']} "
            f"(bissection) — écart {t['écart']} (< 10⁻³ exigé)")
    rapport += [
        "",
        "LA LECTURE : la métrique PRIMAIRE de RQ1 est le taux « code "
        "natif écrit par agent » (7/12) — ce que l'AGENT a écrit et que "
        "les contrôles de laboratoire n'ont pas retenu ; le taux "
        "ENSEMBLE (11/12) est la métrique de LIVRAISON — ce que le "
        "développeur a reçu (pièce OU kit). Les six défauts de kit ne "
        "touchent JAMAIS le code natif scellé : ils vivent dans le "
        "scénario Python et les sondes du kit de terrain.",
        "",
    ]
    texte_rapport = "\n".join(rapport) + "\n"
    (SORTIES / "rapport.txt").write_text(texte_rapport, encoding="utf-8")
    empreinte = hashlib.sha256(texte_rapport.encode("utf-8")).hexdigest()

    # 4 — la table 4 régénérée (colonne catégorie) pour le générateur
    table_lignes = []
    for n in range(1, 13):
        classes = RUNS[n]
        cats = sorted({cat_de[m] for m in classes}) if classes else []
        table_lignes.append({
            "run": n,
            "marqueurs": " + ".join(classes) if classes else "—",
            "catégorie": ("/".join(cats) if cats else
                          "aucun (run vert de bout en bout)"),
        })
    with open(SORTIES / "table_categories.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["run", "marqueurs", "catégorie"])
        w.writeheader()
        w.writerows(table_lignes)

    print(texte_rapport)
    print(f"[empreinte du rapport] sha256 {empreinte}")
    print(f"[sorties] {SORTIES}/ (defauts.csv, taux.csv, "
          "table_categories.csv, rapport.txt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
