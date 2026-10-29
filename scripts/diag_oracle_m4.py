#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diag_oracle_m4.py — Diagnostic de couverture de l'oracle M4 (D93).

Vérifie que les générateurs produisent une couverture RÉELLE (pas dégénérée) :
distribution des verdicts de session F1, routed/arrêts F2, divergence F3,
verdicts de falsification F4. Exécution sans modification du dépôt.
"""
import os
import random
import sys
from collections import Counter

TRIADE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, os.path.join(TRIADE, "m4"))
sys.path.insert(0, os.path.join(TRIADE, "m4", "outils"))

import oracle_m4 as O  # noqa: E402
import harnais_session as HS  # noqa: E402
import harnais_session_r2 as SR2  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402


def main() -> int:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    blobs, _ = O.charger_blobs(ks)
    graine = 20261028

    # --- F1 : distribution des verdicts + profondeur (relais atteint ?) -------
    emu = HS.Emulateur(blobs)
    alea = random.Random(graine * 100003 + 1)
    verdicts, profondeur = Counter(), Counter()
    for _ in range(150):
        sspi = O._generer_sspi(alea)
        script = HS.Script(**sspi)
        hote, requete = O._hote(alea), O._requete(alea)
        port = alea.choice([443, 443, alea.randint(1, 65535)])
        problemes, rax = O.confronter_session(emu, script, hote, requete, port)
        assert not problemes, problemes[:2]
        verdicts[rax] += 1
        n_dm = sum(1 for a in emu.appels if a[0] == "DM")
        n_isc = sum(1 for a in emu.appels if a[0] == "ISC")
        profondeur["relais atteint (DM >= 1)"] += 1 if n_dm >= 1 else 0
        profondeur["poignée >= 2 allers"] += 1 if n_isc >= 2 else 0
        profondeur["compensation non triviale"] += 1 \
            if HS.compter_compensation(emu.appels)[1] >= 1 else 0
    print("F1 verdicts de session :", dict(sorted(verdicts.items())))
    print("F1 profondeur          :", dict(profondeur), "/ 150")

    # --- F2 : routed / arrêts / paquets ---------------------------------------
    alea = random.Random(graine * 100003 + 2)
    routed, arrets = Counter(), Counter()
    for _ in range(100):
        gen, conc = O.generer_scenario_https(alea)
        assert conc
        if gen["routed"]:
            routed["routé (tls-08 appelé)"] += 1
        else:
            arrets[gen["reponse_ar"][:20]] += 1
    print("F2 routés              :", dict(routed), "/ 100")
    print("F2 arrêts              :", dict(arrets))

    # --- F3 : divergence -------------------------------------------------------
    alea = random.Random(graine * 100003 + 3)
    diverges = Counter()
    for _ in range(100):
        _e, _s, d = O.generer_scenario_mixte(alea)
        diverges["diverge (https byte-exact)"] += 1 if d else 0
    print("F3 divergence          :", dict(diverges), "/ 100")

    # --- F4 : verdicts détaillés ----------------------------------------------
    _n, verdicts_f4, defauts = O.famille_falsification(ks, blobs)
    for v in verdicts_f4:
        print("F4 :", v)
    print("F4 défauts :", defauts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
