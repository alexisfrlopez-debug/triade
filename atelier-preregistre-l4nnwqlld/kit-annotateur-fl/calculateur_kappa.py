#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""calculateur_kappa.py — LE CALCULATEUR DU κ DE COHEN, AUTOTESTÉ SUR FIXTURES
SYNTHÉTIQUES (kit l4nnwqlld, pièce 5 — le recrutement du second annotateur).

La lignée : kohen_kappa_v150.py (la réplication 1c4sokpii, la pièce v0.15.0)
— le calculateur porté, les étiquettes D203 (F1-F5 / L1-L3), les MÊMES
mathématiques, et DES FIXTURES PLUS NOMBREUSES : l'accord attendu EXACT PAR
CONSTRUCTION sur QUATRE cas (dont un cas à n = 50, la taille exigée par la
règle d'acceptation, au κ exact 0,64 construit à la main).

LA GRILLE (D189, les étiquettes D203 — grille-fl.csv du kit) :
  F1 chargeur/image · F2 ABI/matériel · F3 sémantique du chargeur ·
  F4 conventions système · F5 environnement ·
  L1 logique · L2 structure · L3 harnais.

LE κ DE COHEN : κ = (po − pe)/(1 − pe) ; po = l'accord observé ; pe =
l'accord attendu sous indépendance (les marges). L'ACCEPTATION
PRÉ-ENREGISTRÉE (D189, portée) : κ ≥ 0,61 (substantiel, Landis & Koch
1977) SUR n ≥ 50 ITEMS DOUBLES — les DEUX conditions, JAMAIS l'une sans
l'autre (un κ à n = 10 ne tranche rien : le calculateur le REFUSE).

LA FRONTIÈRE : AUCUNE annotation n'est inventée ici ; les fixtures sont
SYNTHÉTIQUES (étiquetées comme telles, jamais présentées comme des
annotations réelles) ; le κ réel se calculera le jour où les DEUX jeux
existeront (le second annotateur est À RECRUTER — le statut consigné).

Usage :
  python3 calculateur_kappa.py                          (l'autotest)
  python3 calculateur_kappa.py ann1.csv ann2.csv        (le vrai κ, dès les
                                                        deux jeux — CSV :
                                                        « id,classe », une
                                                        ligne par défaut,
                                                        les id COMMUNS exigés)
"""

from __future__ import annotations

import csv
import pathlib
import sys

CLASSES = ["F1", "F2", "F3", "F4", "F5", "L1", "L2", "L3"]
CORRESPONDANCE = {"T1": "F1", "T2": "F2", "T3": "F3", "T4": "F4",
                  "T5": "F5", "X1": "L1", "X2": "L2", "X3": "L3"}
SEUIL = 0.61
N_MIN = 50


def kohen_kappa(ann1: dict, ann2: dict):
    """Le κ de Cohen sur les id COMMUNS. Retour (k, po, pe, n)."""
    communs = sorted(set(ann1) & set(ann2))
    if not communs:
        raise ValueError("aucun id commun — les annotations ne se "
                         "confrontent pas")
    n = len(communs)
    classes = sorted(set(list(ann1.values()) + list(ann2.values()))
                     & set(CLASSES))
    if not classes:
        raise ValueError("aucune classe de la grille dans les annotations")
    po = sum(1 for i in communs if ann1[i] == ann2[i]) / n
    pe = sum(
        (sum(1 for i in communs if ann1[i] == c) / n)
        * (sum(1 for i in communs if ann2[i] == c) / n)
        for c in classes)
    if pe >= 1.0:
        return 1.0, po, pe, n   # accord parfait sur une classe unique
    k = (po - pe) / (1 - pe)
    return k, po, pe, n


def lire_annotations(chemin: pathlib.Path) -> dict:
    ann = {}
    with open(chemin, encoding="utf-8") as f:
        for ligne in csv.DictReader(f):
            cle = ligne.get("id") or ligne.get("défaut") or ligne.get("defaut")
            classe = (ligne.get("classe") or "").strip()
            if cle and classe:
                if classe not in CLASSES:
                    ancienne = CORRESPONDANCE.get(classe)
                    if ancienne is None:
                        raise ValueError(f"classe {classe!r} hors grille "
                                         f"(F1-F5, L1-L3) — {chemin}")
                    classe = ancienne   # l'ancienne étiquette T/X admise
                ann[cle.strip()] = classe
    if not ann:
        raise ValueError(f"aucune annotation lue dans {chemin}")
    return ann


def verdict_acceptation(k, n):
    """LA RÈGLE (gelée) : κ ≥ 0,61 ET n ≥ 50 — les DEUX, sinon le verdict
    ne se rend PAS (fail-closed : un κ hors taille ne tranche rien)."""
    if n < N_MIN:
        return (f"n = {n} < {N_MIN} — LA RÈGLE D'ACCEPTATION NE SE REND PAS "
                f"(le κ est consigné, le verdict attend n ≥ {N_MIN} items "
                "doubles)")
    if k >= SEUIL:
        return (f"SUBSTANTIEL : κ = {k:+.4f} ≥ 0,61 sur n = {n} — "
                "l'acceptation D189 REMPLIE")
    return (f"SOUS LE SEUIL : κ = {k:+.4f} < 0,61 sur n = {n} — le "
            "désaccord se CONSIGNE, les items en litige se NOMMENT, "
            "l'arbitrage court (REGLE-ACCEPTATION.txt)")


def autotest():
    """L'AUTOTEST sur QUATRE fixtures SYNTHÉTIQUES — l'accord attendu EXACT
    PAR CONSTRUCTION (chaque cas se vérifie à la main : les marges et les
    accords sont posés, le κ s'en dérive arithmétiquement)."""
    print("=== L'AUTOTEST DU CALCULATEUR κ (fixtures SYNTHÉTIQUES — jamais "
          "des annotations réelles) ===")
    ok = True
    # cas 1 : l'accord parfait -> k = 1
    a1 = {f"d{i}": c for i, c in enumerate(
        ["F1", "F1", "F2", "F3", "F5", "L1", "L2", "F4"])}
    k, po, pe, n = kohen_kappa(a1, dict(a1))
    bon = abs(k - 1.0) < 1e-12 and po == 1.0
    print(f"  accord parfait      : k = {k:+.4f} (attendu +1,0000) "
          f"po={po:.3f} n={n} -> {'OK' if bon else 'ÉCART'}")
    ok &= bon
    # cas 2 : le désaccord TOTAL (deux classes équiréparties) -> k < 0
    a2 = {f"d{i}": ("F1" if i % 2 == 0 else "F2") for i in range(10)}
    b2 = {f"d{i}": ("F2" if i % 2 == 0 else "F1") for i in range(10)}
    k, po, pe, n = kohen_kappa(a2, b2)
    bon = k < 0 and po == 0.0
    print(f"  desaccord total     : k = {k:+.4f} (attendu < 0) "
          f"po={po:.3f} pe={pe:.3f} n={n} -> {'OK' if bon else 'ÉCART'}")
    ok &= bon
    # cas 3 : l'accord partiel calculable à la main
    #   10 items : 7 accords (5*F1, 2*F2), 3 désaccords (F1 vs F2)
    a3 = {"a": "F1", "b": "F1", "c": "F1", "d": "F1", "e": "F1",
          "f": "F2", "g": "F2", "h": "F1", "i": "F1", "j": "F1"}
    b3 = {"a": "F1", "b": "F1", "c": "F1", "d": "F1", "e": "F1",
          "f": "F2", "g": "F2", "h": "F2", "i": "F2", "j": "F2"}
    # po = 7/10 ; marges a3 : 8 F1, 2 F2 ; b3 : 5 F1, 5 F2
    # pe = (8/10)*(5/10) + (2/10)*(5/10) = 0,50 ; k = (0,7-0,5)/0,5 = 0,4
    k, po, pe, n = kohen_kappa(a3, b3)
    bon = (abs(po - 0.7) < 1e-12 and abs(pe - 0.5) < 1e-12
           and abs(k - 0.4) < 1e-12)
    print(f"  accord partiel      : k = {k:+.4f} (attendu +0,4000) "
          f"po={po:.3f} pe={pe:.3f} n={n} -> {'OK' if bon else 'ÉCART'}")
    ok &= bon
    # cas 4 : LE CAS n = 50 À LA MAIN — po = 41/50 = 0,82 ; marges
    #   ann1 : 30 F1 + 20 F2 ; ann2 : 25 F1 + 25 F2 ;
    #   matrice : 23 F1/F1, 7 F1/F2, 2 F2/F1, 18 F2/F2 (accords 23+18 = 41)
    #   pe = (30/50)(25/50) + (20/50)(25/50) = 0,30 + 0,20 = 0,50
    #   k = (0,82 - 0,50)/(1 - 0,50) = 0,64 EXACT PAR CONSTRUCTION — et la
    #   règle se rend : n = 50 ≥ 50, κ = 0,64 ≥ 0,61 -> SUBSTANTIEL
    a4, b4 = {}, {}
    for i in range(50):
        a4[f"item{i:02d}"] = "F1" if i < 30 else "F2"
    for i in range(50):                       # 23 F1/F1, 7 F1/F2,
        if i < 23:                            # 2 F2/F1, 18 F2/F2
            b4[f"item{i:02d}"] = "F1"
        elif i < 30:
            b4[f"item{i:02d}"] = "F2"
        elif i < 32:
            b4[f"item{i:02d}"] = "F1"
        else:
            b4[f"item{i:02d}"] = "F2"
    k, po, pe, n = kohen_kappa(a4, b4)
    bon = (n == 50 and abs(po - 0.82) < 1e-12 and abs(pe - 0.5) < 1e-12
           and abs(k - 0.64) < 1e-12)
    v = verdict_acceptation(k, n)
    print(f"  cas n=50 construit  : k = {k:+.4f} (attendu +0,6400) "
          f"po={po:.3f} pe={pe:.3f} n={n} -> {'OK' if bon else 'ÉCART'} ; "
          f"règle : {v}")
    ok &= bon
    # cas 5 : la garde de taille — n = 10 au κ parfait : la règle REFUSE
    v = verdict_acceptation(0.9, 10)
    bon = v.startswith("n = 10")
    print(f"  garde de taille     : κ=0,9 à n=10 -> {v[:52]}… -> "
          f"{'OK' if bon else 'ÉCART'}")
    ok &= bon
    print(f"[autotest] {'VERT' if ok else 'ROUGE'} — le calculateur est "
          f"PRÊT ; l'acceptation pré-enregistrée demeure κ ≥ {SEUIL} "
          f"(Landis-Koch modéré/substantiel) SUR n ≥ {N_MIN} items doubles")
    return ok


def main():
    if len(sys.argv) == 3:
        f1, f2 = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
        ann1, ann2 = lire_annotations(f1), lire_annotations(f2)
        k, po, pe, n = kohen_kappa(ann1, ann2)
        print(f"[κ de Cohen] k = {k:+.4f}  (po = {po:.3f}, pe = {pe:.3f}, "
              f"n = {n})")
        print(f"[règle] {verdict_acceptation(k, n)}")
        desaccords = [i for i in sorted(set(ann1) & set(ann2))
                      if ann1[i] != ann2[i]]
        if desaccords:
            print(f"[litiges] {len(desaccords)} item(s) :")
            for i in desaccords:
                print(f"  {i} : {ann1[i]} vs {ann2[i]}")
        return 0 if (k >= SEUIL and n >= N_MIN) else 1
    return 0 if autotest() else 2


if __name__ == "__main__":
    sys.exit(main())
