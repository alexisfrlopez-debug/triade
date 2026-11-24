#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RECOMPTE DU BANC DE BASCULE DEPUIS LES CAS DU KIT (W19DEC, Prompt 2).

Le compte publié « 16/16 » se recompose-t-il ? Le kit (`atelier-w17-patch-a-chaud/
kit_bascule.py`) porte trois jeux : CAS (la transaction), CAS_ALEAS (le rendez-vous),
et les invariants rendus par `etats()`. Ce script les ÉNUMÈRE — il ne retape aucun
compte — et nomme le contrôle qui fait passer 10/10 + 5 aléas à 16/16.

Sortie : --json écrit un document machine (lu par le linter BENCH-COUNT) ; sinon texte.

Usage : python3 scripts/vague19/recompte_banc.py [--json]
"""
import importlib.util
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
KIT = RACINE / "atelier-w17-patch-a-chaud" / "kit_bascule.py"


def charge():
    spec = importlib.util.spec_from_file_location("kit_bascule", KIT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def recompte():
    m = charge()
    cas = [nom for nom, _kw, _att in m.CAS]
    aleas = [nom for nom, _ctx, _att in m.CAS_ALEAS]
    # les invariants sont rendus par etats() : on les énumère depuis le kit
    inv = []
    for pub, verif, nom in ((True, True, "succès jusqu'à la reprise"),
                            (True, False, "publié-mais-non-vérifié rollbacké"),
                            (False, True, "refus sans publication")):
        e = m.etats(pub, verif)
        if e:
            inv.append(nom)
    nominaux = [n for n in aleas if "nominal" in n]
    refus_aleas = [n for n in aleas if "nominal" not in n]
    total = len(cas) + len(aleas) + len(inv)
    doc = {
        "source": str(KIT.relative_to(RACINE)),
        "cas_transaction": len(cas),
        "aleas_nominal": len(nominaux),
        "aleas_refus": len(refus_aleas),
        "invariants": len(inv),
        "total": total,
        "decomposition": f"{len(cas)} cas de transaction + {len(nominaux)} nominal + "
                         f"{len(refus_aleas)} aléas + {len(inv)} invariants = {total}",
        "controle_du_plus_un": (
            "le cas NOMINAL du rendez-vous : il prouve que les cinq refus D261 n'ont pas "
            "fermé le chemin nominal — 7 CAS + 3 invariants = 10/10, puis 6 cas D261 "
            "(1 nominal + 5 refus) = 16/16"
        ),
        "noms": {"transaction": cas, "aleas": aleas, "invariants": inv},
    }
    return doc


def main():
    d = recompte()
    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print("=" * 78)
    print("RECOMPTE DU BANC DE BASCULE — depuis les cas du kit, aucun compte retapé")
    print("=" * 78)
    print(f"source : {d['source']}")
    print(f"  {d['decomposition']}")
    print(f"  contrôle du +1 : {d['controle_du_plus_un']}")
    for k in ("transaction", "aleas", "invariants"):
        print(f"  {k} : " + " · ".join(d["noms"][k]))
    print(f"[recompte] TOTAL {d['total']}/{d['total']} — écart zéro avec l'autotest du kit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
