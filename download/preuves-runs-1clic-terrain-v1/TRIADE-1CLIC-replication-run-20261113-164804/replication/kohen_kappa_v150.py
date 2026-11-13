#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kohen_kappa_v150.py — LE CALCULATEUR DU κ DE COHEN (v0.15.0, point 3).

La commande : « κ de Cohen calculé dès les annotations disponibles ».
Le calculateur est PRÊT et AUTOTESTÉ sur des annotations SYNTHÉTIQUES
(clairement étiquetées — jamais présentées comme des annotations
réelles) ; le κ RÉEL sera calculé le jour où les DEUX jeux
d'annotations existeront (le second annotateur est À RECRUTER — le
statut est consigné).

LA GRILLE (D189 ; étiquettes RENOMMÉES par D203 — l'ancienne
T1-T5/X1-X3 devient F1-F5/L1-L3 pour lever la collision avec les
taxonomies de défauts T1-T6/X1-X8 de la spécification ; la
correspondance est un-pour-un, T→F et X→L) : les
défauts sont codés dans les CINQ
classes terrain F1-F5 et les TROIS classes laboratoire L1-L3 :
  F1 chargeur/image      (le format, l'en-tête, la table des imports…)
  F2 ABI/matériel        (la convention d'appel, les registres, la pile)
  F3 sémantique du chargeur (ce que le VRAI chargeur fait que le
                          scénario ne faisait pas)
  F4 conventions système (les API, leurs codes, leurs retours)
  F5 environnement       (les locales, le build Windows, le poste)
  L1 logique             (une faute de la notation elle-même)
  L2 structure           (l'orchestration, l'agencement des blocs)
  L3 harnais             (l'instrument de mesure, pas la pièce)

LE κ DE COHEN (l'accord inter-annotateurs au-delà du hasard) :
  κ = (po − pe) / (1 − pe)
  po = l'accord observé (les désaccords comptés) ; pe = l'accord
  attendu sous indépendance (les marges). L'acceptation pré-enregistrée
  D189 : κ ≥ 0,61 (substantiel, Landis & Koch 1977).

Usage :  python3 kohen_kappa_v150.py                    (l'autotest)
        python3 kohen_kappa_v150.py ann1.csv ann2.csv   (le vrai κ,
        dès les deux jeux disponibles — CSV : une ligne par défaut,
        « id,classe » — les id communs requis)
"""
from __future__ import annotations

import csv
import pathlib
import sys

CLASSES = ["F1", "F2", "F3", "F4", "F5", "L1", "L2", "L3"]
# la table de correspondance D203 (l'ancienne grille T/X de D189)
CORRESPONDANCE = {"T1": "F1", "T2": "F2", "T3": "F3", "T4": "F4",
                  "T5": "F5", "X1": "L1", "X2": "L2", "X3": "L3"}
SEUIL = 0.61


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


def autotest():
    """L'AUTOTEST sur annotations SYNTHÉTIQUES (étiquetées comme telles —
    jamais des annotations réelles) : trois cas au κ calculable à la
    main."""
    print("=== L'AUTOTEST DU CALCULATEUR κ (annotations SYNTHÉTIQUES) ===")
    ok = True
    # cas 1 : l'accord parfait -> k = 1
    a1 = {f"d{i}": c for i, c in enumerate(
        ["F1", "F1", "F2", "F3", "F5", "L1", "L2", "F4"])}
    k, po, pe, n = kohen_kappa(a1, dict(a1))
    attendu = 1.0
    bon = abs(k - attendu) < 1e-12 and po == 1.0
    print(f"  accord parfait      : k = {k:+.4f} (attendu {attendu}) "
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
    # cas 3 : un accord partiel calculable a la main
    #   10 items : 7 accords (5*F1, 2*F2), 3 desaccords (F1 vs F2)
    a3 = {"a": "F1", "b": "F1", "c": "F1", "d": "F1", "e": "F1",
          "f": "F2", "g": "F2", "h": "F1", "i": "F1", "j": "F1"}
    b3 = {"a": "F1", "b": "F1", "c": "F1", "d": "F1", "e": "F1",
          "f": "F2", "g": "F2", "h": "F2", "i": "F2", "j": "F2"}
    # po = 7/10 ; marges a3 : 8 F1, 2 F2 ; b3 : 5 F1, 5 F2
    # pe = (8/10)*(5/10) + (2/10)*(5/10) = 0,40 + 0,10 = 0,50
    # k = (0,7 - 0,5)/(1 - 0,5) = 0,4
    k, po, pe, n = kohen_kappa(a3, b3)
    bon = (abs(po - 0.7) < 1e-12 and abs(pe - 0.5) < 1e-12
           and abs(k - 0.4) < 1e-12)
    print(f"  accord partiel      : k = {k:+.4f} (attendu +0,4000) "
          f"po={po:.3f} pe={pe:.3f} n={n} -> {'OK' if bon else 'ÉCART'}")
    ok &= bon
    print(f"[autotest] {'VERT' if ok else 'ROUGE'} — le calculateur est "
          f"PRET ; le seuil d'acceptation pre-enregistre demeure "
          f"κ ≥ {SEUIL} (D189)")
    return ok


def main():
    if len(sys.argv) == 3:
        f1, f2 = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
        ann1, ann2 = lire_annotations(f1), lire_annotations(f2)
        k, po, pe, n = kohen_kappa(ann1, ann2)
        verdict = ("SUBSTANTIEL (κ ≥ 0,61 — l'acceptation D189)"
                   if k >= SEUIL else
                   f"SOUS LE SEUIL 0,61 — le desaccord se CONSIGNE, "
                   f"les items en litige se NOMMENT")
        print(f"[κ de Cohen] k = {k:+.4f}  (po = {po:.3f}, pe = {pe:.3f}, "
              f"n = {n}) -> {verdict}")
        desaccords = [i for i in sorted(set(ann1) & set(ann2))
                      if ann1[i] != ann2[i]]
        if desaccords:
            print(f"[litiges] {len(desaccords)} item(s) :")
            for i in desaccords:
                print(f"  {i} : {ann1[i]} vs {ann2[i]}")
        return 0 if k >= SEUIL else 1
    return 0 if autotest() else 2


if __name__ == "__main__":
    sys.exit(main())
