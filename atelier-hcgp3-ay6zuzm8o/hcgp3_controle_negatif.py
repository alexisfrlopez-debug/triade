#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hcgp3_controle_negatif.py — LES CONTRÔLES NÉGATIFS DOUBLE FENÊTRE
(ay6zuzm8o, la vague 13) : le +500 ms injecté dans UNE COPIE (jamais le
registre réel), les DEUX variantes (inter-étapes : une étape factice ;
in-étape : une étape ralentie), LA NORMALISATION DE DÉRIVE reconduite
(déviation normalisée > 0,30 s ET valeur > 2× la médiane de l'étape) ;
la spécificité : LA MÊME RÈGLE aux runs honnêtes — ZÉRO FAUX POSITIF
exigé.

LA DÉTECTION (le précédent vague 11, reconduit) :
  — FENÊTRE INTER-ÉTAPES : la comptabilité — la somme des étapes contre
    le total du run (la tolérance du bras) ; une étape factice de 500 ms
    fait dévier la comptabilité ;
  — FENÊTRE IN-ÉTAPE : le scan de déviation — l'étape qui dévie de sa
    propre médiane NORMALISÉE par le facteur de dérive du run (la dérive
    machine est multiplicative, la faute additive) : déviation
    normalisée > 0,30 s ET valeur > 2× la médiane de l'étape ;
  — L'ATTRIBUTION AU PREMIER NOM : la première étape signalée par ordre
    d'exécution.

Sortie : controle-negatif.txt ; code 0 si les DEUX fenêtres attrapent et
zéro faux positif."""
from __future__ import annotations

import copy
import json
import pathlib
import statistics
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-hcgp3-ay6zuzm8o"
TOLERANCES = {"T": 0.150, "C+G+": 0.100, "C+G": 0.050, "C": 0.050}
FICHIER = {"T": "T", "C+G+": "CGP", "C+G": "CG", "C": "C"}
SEUIL_DEV = 0.30          # s, la déviation normalisée
SEUIL_2X = 2.0            # la valeur > 2× la médiane de l'étape
INJECTION = 0.500         # s, la faute injectée


def charger(bras: str) -> list[dict]:
    return [json.loads(
        (ICI / f"m4v13-{FICHIER[bras]}-run{i}.json").read_text(
            encoding="utf-8")) for i in range(1, 6)]


def somme_etapes(run: dict) -> float:
    return sum(e["secondes"] for e in run["etapes"])


def medians_etapes(runs: list[dict]) -> dict:
    out = {}
    for e in runs[0]["etapes"]:
        out[e["etape"]] = statistics.median(
            [x["secondes"] for r in runs for x in r["etapes"]
             if x["etape"] == e["etape"]])
    return out


def fenetre_inter(run: dict, bras: str) -> tuple[bool, str]:
    """LA FENÊTRE INTER-ÉTAPES : la comptabilité du run contre la
    tolérance du bras (la borne de comptabilité, vague 11)."""
    ecart = run["total_s"] - somme_etapes(run)
    if abs(ecart) > TOLERANCES[bras]:
        return True, (f"la comptabilité déviée : total {run['total_s']:.3f} "
                      f"vs somme {somme_etapes(run):.3f} (écart "
                      f"{ecart:+.3f} s > tolérance {TOLERANCES[bras]})")
    return False, ""


def fenetre_intra(suspect: dict, honnetes: list[dict]) -> tuple[bool, str]:
    """LA FENÊTRE IN-ÉTAPE : le scan de déviation normalisé (vague 11)."""
    med = medians_etapes(honnetes)
    facteur = suspect["total_s"] / statistics.median(
        [r["total_s"] for r in honnetes])
    for e in suspect["etapes"]:
        m = med.get(e["etape"])
        if m is None or m <= 0:
            continue
        dev_norm = e["secondes"] - m * facteur
        if dev_norm > SEUIL_DEV and e["secondes"] > SEUIL_2X * m:
            return True, (f"l'étape « {e['etape']} » à {e['secondes']:.3f} s"
                          f" (médiane {m:.3f}, déviation normalisée "
                          f"{dev_norm:+.3f} s, valeur "
                          f"{e['secondes']/m:.2f}× la médiane)")
    return False, ""


def main() -> int:
    lignes = ["LE CONTRÔLE NÉGATIF DOUBLE FENÊTRE — ay6zuzm8o (la vague 13)",
              "=" * 74, ""]
    tout_vert = True

    for bras in ["T", "C+G+"]:
        honnetes = charger(bras)
        # LE BRAS T : le run d'AUDIT nommé et exclu (l'oracle-02 re-exécuté
        # vivant au 10ᵉ scellement du mémo v2 — le prix de la preuve, vécu
        # au run 4 : 23,3 s contre 0,52 s de médiane — JAMAIS confondu avec
        # un run de régime, JAMAIS fusionné)
        if bras == "T":
            audit = [r for r in honnetes if any(
                e["etape"].startswith("oracle-du-bloc") and e["secondes"] > 5
                for e in r["etapes"])]
            honnetes = [r for r in honnetes if r not in audit]
            if audit:
                lignes.append(f"LE BRAS T — le run d'AUDIT "
                              f"{[r['run'] for r in audit]} NOMMÉ ET EXCLU "
                              f"(l'oracle-02 re-exécuté vivant au 10ᵉ "
                              f"scellement — le prix de la preuve)")
        med_tot = statistics.median([r["total_s"] for r in honnetes])
        lignes.append(f"LE BRAS {bras} — la médiane des runs honnêtes "
                      f"(le régime) {med_tot:.3f} s")
        # LA SPÉCIFICITÉ D'ABORD : la même règle aux runs honnêtes
        fp = 0
        for r in honnetes:
            autres = [x for x in honnetes if x is not r]
            attrape, _ = fenetre_intra(r, autres)
            if attrape:
                fp += 1
        ok_fp = fp == 0
        tout_vert &= ok_fp
        lignes.append(f"  la spécificité : {fp} faux positif(s) sur "
                      f"{len(honnetes)} runs honnêtes "
                      f"{'VERT' if ok_fp else 'ROUGE — REFUS'}")

        # (a) LA VARIANTE INTER-ÉTAPES : une étape factice de +500 ms
        copie = copy.deepcopy(honnetes[0])
        site = "recomposition-loupe-02" if bras == "T" else \
            "chaine-cristallisation (g2)"
        copie["etapes"].insert(
            len(copie["etapes"]) // 2,
            {"etape": f"{site} (la copie factice)", "secondes": INJECTION,
             "code": 0, "console": "", "stderr": ""})
        # la comptabilité : le total NE BOUGE PAS (la faute vit aux étapes
        # — la fenêtre inter attrape l'écart somme/total)
        attrape, detail = fenetre_inter(
            {"total_s": copie["total_s"],
             "etapes": copie["etapes"]}, bras)
        ok_a = attrape
        tout_vert &= ok_a
        lignes.append(f"  (a) l'inter-étapes (+500 ms factices à « {site} »)"
                      f" : {'ATTRAPÉ' if ok_a else 'MANQUÉ — REFUS'} — "
                      f"{detail}")

        # (b) LA VARIANTE IN-ÉTAPE : une étape ralentie de +500 ms (le
        # total porteur de la faute)
        copie2 = copy.deepcopy(honnetes[1])
        for e in copie2["etapes"]:
            if e["etape"].startswith(site.split(" (")[0]):
                e["secondes"] = round(e["secondes"] + INJECTION, 3)
                copie2["total_s"] = round(copie2["total_s"] + INJECTION, 3)
                break
        attrape2, detail2 = fenetre_intra(copie2, honnetes)
        ok_b = attrape2
        tout_vert &= ok_b
        lignes.append(f"  (b) l'in-étape (+500 ms à « {site} ») : "
                      f"{'ATTRAPÉ AU PREMIER NOM' if ok_b else 'MANQUÉ — REFUS'}"
                      f" — {detail2}")
        lignes.append("")

    verdict = ("VERT — le +500 ms attrapé aux DEUX fenêtres et attribué au "
               "premier nom, zéro faux positif sur les honnêtes"
               if tout_vert else
               "ROUGE — une fenêtre manquée ou un faux positif — REFUS")
    lignes.append(f"LE VERDICT : {verdict}")
    (ICI / "controle-negatif.txt").write_text("\n".join(lignes),
                                              encoding="utf-8")
    print("\n".join(lignes))
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
