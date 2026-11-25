#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Recoup du run COLLAB (kit-C, protocole COLLAB-X86-1).

Recompute les t de Welch des TROIS runs (N=60/200/400) depuis les ticks
bruts des csv de preuves-collab/ (l'extraction verbatim du zip du coffre),
et les compare aux valeurs imprimées aux sorties de run. Aucun chiffre
repris sans son témoin (le geste de l'Entrée 416/424).

Usage : python3 recoup_run_collab.py
Code de sortie : 0 = tous les t recoupés, 1 = au moins un écart.
"""
import csv
import math
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
PREUVES = ICI / "preuves-collab"


def t_de_welch(a, b):
    """Le t de Welch sur deux échantillons de ticks (le même geste que le
    mesureur : différences de moyennes sur erreurs-types empiriques)."""
    n1, n2 = len(a), len(b)
    m1, m2 = sum(a) / n1, sum(b) / n2
    v1 = sum((x - m1) ** 2 for x in a) / (n1 - 1)
    v2 = sum((x - m2) ** 2 for x in b) / (n2 - 1)
    return (m1 - m2) / math.sqrt(v1 / n1 + v2 / n2)


def t_annonces(chemin_sortie):
    """Extrait les t imprimés par le mesureur pour chaque cible."""
    texte = chemin_sortie.read_text(encoding="utf-8", errors="replace")
    sortis = {}
    motif = re.compile(
        r"\[(eq-constant|eq-branchue|sha256-logiciel|sha256-x86-shani"
        r"|tls13-02|tls13-13|tls13-16|tls13-17)\]"
        r"[^\[]*?t de Welch = (-?[\d.]+)")
    for m in motif.finditer(texte):
        sortis[m.group(1)] = float(m.group(2))
    return sortis


CLASSES = {"eq-constant": ("egal", "divergent"),
           "eq-branchue": ("egal", "divergent")}


def classes_de(cible):
    return CLASSES.get(cible, ("fixe", "aleatoire"))


def main():
    verts, ecarts = 0, 0
    for n in (60, 200, 400):
        csv_path = PREUVES / f"journal-dudect-collab-N{n}.csv"
        annonces = t_annonces(PREUVES / f"sortie-run-N{n}.txt")
        donnees = {}
        with open(csv_path) as f:
            for ligne in csv.DictReader(f):
                cle = (ligne["cible"], ligne["classe"])
                donnees.setdefault(cle, []).append(int(ligne["ticks"]))
        total = sum(len(v) for v in donnees.values())
        print(f"=== N={n} ({total} échantillons) ===")
        for cible in sorted(set(k[0] for k in donnees)):
            ca, cb = classes_de(cible)
            a, b = donnees.get((cible, ca), []), donnees.get((cible, cb), [])
            if not a or not b:
                print(f"  {cible}: CLASSE MANQUANTE")
                continue
            t = t_de_welch(a, b)
            attendu = annonces.get(cible)
            if attendu is None:
                print(f"  {cible}: non imprimé — t={t:+.2f}")
                continue
            ecart = abs(t - attendu)
            ok = ecart < 0.005  # l'arrondi d'impression du mesureur
            verdict = "VERT" if ok else f"ECART {ecart:.3f}"
            diver = "  (DIVERGENTE |t|>5)" if abs(t) > 5 else ""
            print(f"  {cible}: t={t:+.2f} imprimé={attendu:+.2f} "
                  f"écart={ecart:.3f} {verdict}{diver}")
            verts += ok
            ecarts += (not ok)
    print(f"\nBILAN : {verts} t recoupés VERT, {ecarts} écart(s)")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
