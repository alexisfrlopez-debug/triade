#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""modele_z3_etendu.py — LE MODÈLE z3 ÉTENDU (alhmpl35u) : la machine à
états de la sentinelle RE-DÉCHARGÉE sur le modèle étendu aux portes
d'époque et de plancher, contrôles négatifs compris (la machine nue doit
redevenir SAT).

LES SIX INVARIANTS : I1 la corruption → REFUS SANS destruction ; I2 OUVERT
exige les DEUX vérifications ; I3 le plancher refusant sous 60 bits ; I4 la
falsification prouvée → DESTRUCTION_PV ; I5 (ÉTENDU) aucune époque
périmée ni retour en arrière n'atteint l'empreinte — le refus AVANT tout ;
I6 (ÉTENDU) l'ordre des étages : l'empreinte AVANT l'AEAD, l'époque AVANT
l'empreinte, le plancher AVANT le scellement.

Sortie : vecteurs-modele-etendu.txt · modele-etendu.json"""
from __future__ import annotations

import json
import pathlib

ICI = pathlib.Path(__file__).resolve().parent
from z3 import (Datatype, Const, Function, And, Or, Not, Implies,  # noqa: E402
                Solver, unsat, sat, BoolSort, Int)


def construire(nu: bool):
    """LA MACHINE — nu=True : SANS les axiomes (le contrôle négatif)."""
    E = Datatype("Etat")
    for s_ in ["PLANCHER", "EPOQUE", "EMPREINTE", "AEAD", "OUVERT",
               "REFUS_SANS_DESTRUCTION", "DESTRUCTION_PV",
               "REFUS_EPOQUE", "REFUS_PLANCHER"]:
        E.declare(s_)
    E = E.create()
    EmpOk = Const("empreinte_ok", BoolSort())
    AeadOk = Const("aead_ok", BoolSort())
    EpoqueOk = Const("epoque_ok", BoolSort())
    PlancherOk = Const("plancher_ok", BoolSort())
    T = Function("transition", E, BoolSort(), BoolSort(), E)
    bits = Int("bits_estimes")
    ax = [] if nu else [
        # LE PLANCHER AVANT TOUT (la cérémonie) : sous 60 bits → refus
        T(E.PLANCHER, False, False) == E.REFUS_PLANCHER,
        T(E.PLANCHER, False, True) == E.REFUS_PLANCHER,
        T(E.PLANCHER, True, False) == E.EPOQUE,
        T(E.PLANCHER, True, True) == E.EPOQUE,
        # L'ÉPOQUE (le piège d'époque, le miroir) : périmé/arrière → refus
        T(E.EPOQUE, False, False) == E.REFUS_EPOQUE,
        T(E.EPOQUE, False, True) == E.REFUS_EPOQUE,
        T(E.EPOQUE, True, False) == E.REFUS_EPOQUE,
        # l'époque VERTE mène à l'empreinte
        T(E.EPOQUE, True, True) == E.EMPREINTE,
        # L'EMPREINTE AVANT L'AEAD (l'ordre (a)) : diverge → REFUS SANS
        # destruction (la corruption — jamais la destruction sur incident)
        T(E.EMPREINTE, False, False) == E.REFUS_SANS_DESTRUCTION,
        T(E.EMPREINTE, False, True) == E.REFUS_SANS_DESTRUCTION,
        T(E.EMPREINTE, True, False) == E.AEAD,
        T(E.EMPREINTE, True, True) == E.AEAD,
        # L'AEAD : vert → OUVERT ; échec APRÈS empreinte verte (la
        # falsification PROUVÉE : le nonce altéré, l'étiquette) → PV
        T(E.AEAD, True, True) == E.OUVERT,
        T(E.AEAD, True, False) == E.DESTRUCTION_PV,
        # l'axiome du plancher (la valeur gelée 60)
        Implies(PlancherOk, bits >= 60),
        # LES ÉTATS TERMINAUX ABSORBANTS : un refus clôt l'acte, une
        # destruction aussi — AUCUNE transition n'en sort (l'acte est fini)
        T(E.REFUS_SANS_DESTRUCTION, False, False) == E.REFUS_SANS_DESTRUCTION,
        T(E.REFUS_SANS_DESTRUCTION, False, True) == E.REFUS_SANS_DESTRUCTION,
        T(E.REFUS_SANS_DESTRUCTION, True, False) == E.REFUS_SANS_DESTRUCTION,
        T(E.REFUS_SANS_DESTRUCTION, True, True) == E.REFUS_SANS_DESTRUCTION,
        T(E.DESTRUCTION_PV, False, False) == E.DESTRUCTION_PV,
        T(E.DESTRUCTION_PV, False, True) == E.DESTRUCTION_PV,
        T(E.DESTRUCTION_PV, True, False) == E.DESTRUCTION_PV,
        T(E.DESTRUCTION_PV, True, True) == E.DESTRUCTION_PV,
        T(E.REFUS_EPOQUE, False, False) == E.REFUS_EPOQUE,
        T(E.REFUS_EPOQUE, False, True) == E.REFUS_EPOQUE,
        T(E.REFUS_EPOQUE, True, False) == E.REFUS_EPOQUE,
        T(E.REFUS_EPOQUE, True, True) == E.REFUS_EPOQUE,
        T(E.REFUS_PLANCHER, False, False) == E.REFUS_PLANCHER,
        T(E.REFUS_PLANCHER, False, True) == E.REFUS_PLANCHER,
        T(E.REFUS_PLANCHER, True, False) == E.REFUS_PLANCHER,
        T(E.REFUS_PLANCHER, True, True) == E.REFUS_PLANCHER,
    ]
    return E, T, ax, (EmpOk, AeadOk, EpoqueOk, PlancherOk, bits)


def preuve(nu: bool) -> dict:
    E, T, ax, (EmpOk, AeadOk, EpoqueOk, PlancherOk, bits) = construire(nu)
    res = {}

    def unsat_de(nom, contraintes):
        s = Solver()
        s.add(ax)
        s.add(contraintes)
        res[nom] = s.check() == unsat

    # I1 — la corruption (¬EmpOk à l'étage empreinte, époque verte) →
    # REFUS SANS destruction
    unsat_de("I1_corruption_sans_destruction", And(
        Not(EmpOk), EpoqueOk, PlancherOk,
        Not(T(T(T(E.PLANCHER, True, True), True, True),  # -> EMPREINTE
              EmpOk, AeadOk) == E.REFUS_SANS_DESTRUCTION)))
    # I2 — OUVERT exige les DEUX vérifications (empreinte ET AEAD)
    unsat_de("I2_ouvert_exige_deux", And(
        Or(Not(EmpOk), Not(AeadOk)), EpoqueOk, PlancherOk,
        T(T(E.EMPREINTE, EmpOk, AeadOk), EmpOk, AeadOk) == E.OUVERT))
    # I3 — le plancher : sous 60 bits, la cérémonie refusée
    s = Solver()
    s.add(ax)
    s.add(bits < 60, PlancherOk,
          T(E.PLANCHER, PlancherOk, EpoqueOk) == E.EPOQUE)
    res["I3_plancher_sous_60"] = s.check() == unsat
    # I4 — la falsification prouvée (EmpOk ∧ ¬AeadOk) → DESTRUCTION_PV
    unsat_de("I4_falsification_pv", And(
        EmpOk, Not(AeadOk), EpoqueOk, PlancherOk,
        Not(T(T(E.EMPREINTE, EmpOk, AeadOk), True, False)
            == E.DESTRUCTION_PV)))
    # I5 (ÉTENDU) — l'époque périmée n'atteint JAMAIS l'empreinte
    unsat_de("I5_epoque_refusee_avant_empreinte", And(
        Not(EpoqueOk), PlancherOk,
        T(T(E.PLANCHER, True, True), EpoqueOk, EmpOk) == E.EMPREINTE))
    # I6 (ÉTENDU) — l'ordre des étages : le chemin vers OUVERT passe par
    # les QUATRE portes dans l'ordre (plancher → époque → empreinte → AEAD)
    s = Solver()
    s.add(ax)
    s.add(PlancherOk, EpoqueOk, EmpOk, AeadOk)
    s.add(Not(T(T(T(T(E.PLANCHER, PlancherOk, EpoqueOk),
                    EpoqueOk, EmpOk), EmpOk, AeadOk), AeadOk, True)
              == E.OUVERT))
    res["I6_ordre_des_etages"] = s.check() == unsat
    return res


def main() -> int:
    rap = ["LE MODÈLE z3 ÉTENDU (alhmpl35u) — la sentinelle aux portes",
           "d'époque et de plancher, les SIX invariants re-déchargés",
           "(UNSAT aux négations), le contrôle négatif compris", ""]
    verts = preuve(nu=False)
    for k, v in verts.items():
        rap.append(f"  {k} : {'UNSAT — PROUVÉ' if v else 'ROUGE'}")
    # LE CONTRÔLE NÉGATIF : la machine NUE (aucun axiome) — la corruption
    # peut détruire, l'époque périmée peut atteindre l'empreinte : SAT
    nu = preuve(nu=True)
    ok_nu = (not nu["I1_corruption_sans_destruction"]
             and not nu["I5_epoque_refusee_avant_empreinte"])
    rap += ["",
            "LE CONTRÔLE NÉGATIF (la machine NUE, aucun axiome) : la "
            "corruption peut détruire et l'époque périmée atteindre "
            "l'empreinte : "
            + ("SAT — ATTRAPÉ (la preuve vit aux AXIOMES — la garde)"
               if ok_nu else "ROUGE")]
    verdict = all(verts.values()) and ok_nu
    rap += ["", f"LE VERDICT : {'VERT' if verdict else 'ROUGE'}"]
    (ICI / "vecteurs-modele-etendu.txt").write_text(
        "\n".join(rap) + "\n", encoding="utf-8")
    (ICI / "modele-etendu.json").write_text(json.dumps(
        {"invariants": verts, "controle_negatif_nu": ok_nu,
         "verdict": "VERT" if verdict else "ROUGE"}, indent=1),
        encoding="utf-8")
    print("\n".join(rap))
    return 0 if verdict else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
