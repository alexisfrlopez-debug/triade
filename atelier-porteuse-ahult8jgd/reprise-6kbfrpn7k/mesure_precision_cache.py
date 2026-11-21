#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mesure_precision_cache.py — LA REPRISE 6KBFRPN7K : le canon non arrondi du
cache de round-trip.

LA CAUSE (l'instruction 6kbfrpn7k, l'item 1) : le rapport v0.22.0 publie
« 283,7 ms → 0,4 ms » et « le gain 680,6× » — le lecteur recompose
283,7/0,4 = ×709,2 : LE RATIO NE SE RECOMPOSE PAS depuis les imprimés. Le
registre historique (registres/roundtrip-cache.json) porte apres_s arrondi à
la dixième de milliseconde (4 décimales de seconde) : le canon non arrondi
n'y vit pas.

LE GESTE : re-mesurer AU PROTOCOLE EXACT de roundtrip_cache.py (le même
échantillon tls13 des 28 notations, le même vérificateur R5, n=10 avant /
n=10 après, la même machine de bac) À LA PRÉCISION MICROSECONDE — la médiane
après publiée en ms à TROIS décimales, le gain RECALCULÉ des canons imprimés
lui-même. Le rapport historique DEMEURE octet pour octet ; la présente vit
au sous-dossier reprise-6kbfrpn7k/ et son canon est porté aux preuves v0.23.0
et au manuscrit.

Sortie : reprise-6kbfrpn7k/mesure-precision.json · rapport-mesure-precision.txt
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import statistics
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[2]
ICI = REPO / "atelier-porteuse-ahult8jgd"
ICI_CI = ICI / "reprise-6kbfrpn7k"

# ---- charger roundtrip_cache.py AVEC le REPO courant -----------------------
spec = importlib.util.spec_from_file_location("rc_reprise", ICI / "roundtrip_cache.py")
rc = importlib.util.module_from_spec(spec)
rc.REPO = REPO          # le chemin du dépôt patché AVANT l'exécution
spec.loader.exec_module(rc)
rc.REPO = REPO          # et re-patché après (l'exécution ne le réécrit pas)


def main() -> int:
    echant = rc.echantillon_tls13()
    memo = ICI_CI / "mesure-precision-memo.json"
    verif = rc.fabrique_verificateur_r5()

    # ---- la semence (le mémo posé une fois) --------------------------------
    if memo.exists():
        memo.unlink()
    cache = rc.CacheRoundTrip(memo, verif)
    t_semis, hits = rc.ouverture(cache, echant, actif=True)
    assert hits == 0 and len(cache._memo) == len(echant), "la semis"

    # ---- l'ouverture AVANT / APRÈS (n=10, la médiane, µs) ------------------
    avant = []
    for _ in range(10):
        cache.compteurs = {"hit": 0, "miss": 0, "refus": 0}
        dt, hits = rc.ouverture(cache, echant, actif=False)
        if dt < 0:
            print("ROUGE : l'ouverture sans cache a refusé")
            return 2
        avant.append(dt)
    apres = []
    for _ in range(10):
        cache.compteurs = {"hit": 0, "miss": 0, "refus": 0}
        dt, hits = rc.ouverture(cache, echant, actif=True)
        if dt < 0 or hits != len(echant):
            print(f"ROUGE : l'ouverture chaude hits={hits}/{len(echant)}")
            return 2
        apres.append(dt)

    med_avant = statistics.median(avant)
    med_apres = statistics.median(apres)
    gain_brut = med_avant / max(med_apres, 1e-9)
    # les canons IMPRIMÉS (trois décimales) — le ratio publié se recompose
    # DEPUIS LES IMPRIMÉS eux-mêmes (le lecteur retrouve exactement la valeur)
    canon_avant = round(med_avant * 1000, 3)
    canon_apres = round(med_apres * 1000, 3)
    gain_imprime = canon_avant / canon_apres

    rapport = [
        "LA REPRISE 6KBFRPN7K — LE CANON NON ARRONDI DU CACHE DE ROUND-TRIP",
        "(le protocole EXACT de roundtrip_cache.py re-exécuté à la précision",
        " microseconde ; le rapport historique demeure octet pour octet)",
        "",
        f"L'ÉCHANTILLON : {len(echant)} notations tls13 (le dépôt, les slots",
        " de layout.py), le contrat r5-v1, le moteur du jour",
        "",
        "LE TEMPS D'OUVERTURE (n=10, la médiane [min–max], cette machine) :",
        f"  AVANT (tout re-vérifié) : {canon_avant:.3f} ms",
        f"      [{min(avant)*1000:.3f}–{max(avant)*1000:.3f}]",
        f"  APRÈS (le mémo chaud, {len(echant)}/{len(echant)} hits) :",
        f"      {canon_apres:.3f} ms [{min(apres)*1000:.3f}–"
        f"{max(apres)*1000:.3f}]",
        f"  LE GAIN PUBLIÉ, RECOMPOSÉ DES CANONS IMPRIMÉS CI-DESSUS : "
        f"{gain_imprime:.1f}×",
        f"  (le brut non arrondi des médianes : {gain_brut:.1f}× — l'écart",
        " d'arrondi du canon à trois décimales, nommé ; tolérance du linter",
        " : 0,2 % relatif aux gains multiplicatifs)",
        "  (−{:.1f} %)".format((1 - med_apres / med_avant) * 100),
        "",
        "L'ERRATUM NOMMÉ (l'instruction 6kbfrpn7k) : la ligne v0.22.0",
        "« 283,7 ms → 0,4 ms, le gain 680,6× » ne se recomposait pas —",
        "le lecteur calculait 283,7/0,4 = ×709,2 ; la cause : la médiane",
        "après publiée à UNE décimale (0,4 ms) pour un ratio à trois",
        "chiffres significatifs ; le registre historique arrondi à la",
        "dixième de milliseconde. LE CANON À TROIS DÉCIMALES ci-dessus",
        "recompose le ratio publié à cette ligne.",
        "",
        "LES DIX VALEURS BRUTES (secondes, six décimales) :",
        "  avant : " + ", ".join(f"{x:.6f}" for x in avant),
        "  après : " + ", ".join(f"{x:.6f}" for x in apres),
        "",
        f"sha256 du mémo : {hashlib.sha256(memo.read_bytes()).hexdigest()[:16]}…",
        "LE VERDICT : " + ("VERT — le canon à trois décimales publié, le "
                            "gain recomposé" if med_apres > 0 else "ROUGE"),
    ]
    (ICI_CI / "rapport-mesure-precision.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    (ICI_CI / "mesure-precision.json").write_text(json.dumps({
        "n": 10,
        "avant_s": [round(x, 6) for x in avant],
        "apres_s": [round(x, 6) for x in apres],
        "medianes": {"avant_ms": round(med_avant * 1000, 3),
                     "apres_ms": round(med_apres * 1000, 3)},
        "gain_imprime_recompose": round(gain_imprime, 1),
        "gain_brut_non_arrondi": round(gain_brut, 1),
        "protocole": "roundtrip_cache.py re-exécuté, précision µs",
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(rapport))
    return 0


if __name__ == "__main__":
    sys.exit(main())
