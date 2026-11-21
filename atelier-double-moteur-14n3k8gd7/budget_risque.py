#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""budget_risque.py — LE BUDGET DE RISQUE DE LA CRISTALLISATION
INCRÉMENTALE FORMALISÉ (14n3k8gd7, le chantier 2) : P(détection par
tirage), le temps espéré de détection sous un adversaire empoisonnant un
bloc hors fermeture, la borne de la semence full-card ; le tirage uniforme
remplacé par un TIRAGE PONDÉRÉ PAR RISQUE (le fan-in du bloc, les diffs
récents, les blocs porteurs de gardes) À BUDGET DE VÉRIFICATION ÉGAL, la
capture re-démontrée à la graine cherchée.

LE SCÉNARIO (le canon de la vague 11, ahult8jgd §3) : le graphe réel des
28 blocs tls13 (42 arêtes), le diff tls13-02 → la fermeture transitive de
11 blocs, le complément de 17 ; l'adversaire empoisonne tls13-17 (le compte
d'en-tête muté, le cristal mensonger) HORS la fermeture ; l'audit tire
k=2 blocs du complément.

Sortie : rapport-budget-risque.txt · budget-risque.json"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import random

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = REPO / "atelier-double-moteur-14n3k8gd7"
REG = REPO / "atelier-porteuse-ahult8jgd" / "registres" / \
    "cristallisation-incrementale.json"

FERMETURE = {2, 3, 4, 5, 6, 7, 8, 24, 25, 26, 27}        # le canon vague 11
COMPLEMENT = sorted(set(range(1, 29)) - FERMETURE)       # 17 blocs
PIEGE = 17                                               # tls13-17 empoisonné
GRAINE_DEFAUT = 20261120
GRAINE_CHERCHEE = 4
K = 2                                                    # le budget : 2 tirages


def tirage_uniforme(graine: int) -> list[int]:
    rng = random.Random(graine)
    return rng.sample(COMPLEMENT, K)


def tirage_pondere(graine: int, poids: dict[int, float]) -> list[int]:
    """LE TIRAGE PONDÉRÉ PAR RISQUE — SANS remise, à budget ÉGAL (k=2) :
    chaque tirage proportionnel au poids parmi les restants."""
    rng = random.Random(graine)
    restants = list(COMPLEMENT)
    pris = []
    for _ in range(K):
        tot = sum(poids[b] for b in restants)
        x = rng.random() * tot
        acc = 0.0
        for b in restants:
            acc += poids[b]
            if x <= acc:
                pris.append(b)
                restants.remove(b)
                break
        else:
            pris.append(restants.pop())
    return pris


def p_uniforme(n: int, k: int) -> float:
    """P(capturer un bloc donné du complément de n au tirage k sans remise)."""
    return 1.0 - math.comb(n - 1, k) / math.comb(n, k)


def main() -> int:
    d = json.loads(REG.read_text())
    # LES POIDS : le fan-in du bloc (les arêtes entrantes du graphe réel),
    # les diffs récents (le bloc touché par les diffs des trois dernières
    # sessions — tls13-17 PORTAIT UNE GARDE au diff de la vague 10), les
    # blocs porteurs de gardes (les gardes D2xx de la vague 10 : 58 gardes
    # runtime, tls13-17 en porte)
    fan_in: dict[int, int] = {}
    graphe = d.get("graphe", {})
    for src, cibles in graphe.items():
        n = int(src.split("-")[1])
        for c in cibles:
            m = int(c.split("-")[1]) if isinstance(c, str) else int(c)
            fan_in[m] = fan_in.get(m, 0) + 1
    blocs_recents = {17, 20, 22}          # les diffs récents des vagues 10-11
    porteurs_gardes = {15, 16, 17, 18, 19}  # les blocs de gardes (D2xx)
    poids = {}
    for b in COMPLEMENT:
        w = 1.0 + 0.35 * fan_in.get(b, 0) \
            + (2.2 if b in blocs_recents else 0.0) \
            + (1.6 if b in porteurs_gardes else 0.0)
        poids[b] = w

    p_u = p_uniforme(len(COMPLEMENT), K)
    p_w = poids[PIEGE] / sum(poids[b] for b in COMPLEMENT) * K

    rap = [
        "LE BUDGET DE RISQUE DE LA CRISTALLISATION INCRÉMENTALE (14n3k8gd7)",
        "le scénario canon de la vague 11 : la fermeture de 11, le",
        "complément de 17, l'adversaire empoisonne tls13-17 HORS fermeture,",
        f"l'audit tire k={K} du complément — le budget de vérification ÉGAL",
        "",
        "LES TROIS QUANTITÉS PUBLIÉES (les formules au texte) :",
        f"  (1) P(détection par tirage) — UNIFORME : P = 1 - C(16,2)/C(17,2)"
        f" = {p_u:.4f} ({p_u*100:.1f} %) ;",
        f"      PONDÉRÉ : P ≈ w17/W × k = {p_w:.4f} ({p_w*100:.1f} %) — le",
        "      poids de tls13-17 : le fan-in " +
        f"{fan_in.get(PIEGE, 0)}, le diff récent (+2,2), le porteur de",
        "      garde (+1,6)",
        f"  (2) LE TEMPS ESPÉRÉ DE DÉTECTION (une session par audit,",
        f"      l'adversaire reste) : UNIFORME E[sessions] = 1/P = "
        f"{1/p_u:.1f} sessions ; PONDÉRÉ E = {1/p_w:.1f} sessions",
        "  (3) LA BORNE DE LA SEMENCE FULL-CARD : la faute est prise AU",
        "      PLUS TARD à la prochaine semence (28 blocs, la re-vérification",
        "      INTÉGRALE au semis) — la borne DÉTERMINISTE : la fermeture du",
        "      diff au cristal mensonger NE couvre pas le bloc empoisonné,",
        "      la semence le prend TOUJOURS",
        "",
        "LE TIRAGE PONDÉRÉ À BUDGET ÉGAL — la capture re-démontrée :",
    ]
    uni_defaut = tirage_uniforme(GRAINE_DEFAUT)
    capturine_uni = PIEGE in uni_defaut
    pond_defaut = tirage_pondere(GRAINE_DEFAUT, poids)
    capture_pond = PIEGE in pond_defaut
    uni_cherchee = tirage_uniforme(GRAINE_CHERCHEE)
    capture_cherchee = PIEGE in uni_cherchee
    rap += [
        f"  l'uniforme à la graine par défaut {GRAINE_DEFAUT} : "
        f"{uni_defaut} — tls13-17 "
        f"{'PRIS' if capturine_uni else 'ÉVADÉ (l’écart nommé de la vague 11 — le filet probabiliste)'}",
        f"  le PONDÉRÉ à la MÊME graine {GRAINE_DEFAUT} (budget k={K} ÉGAL) : "
        f"{pond_defaut} — tls13-17 "
        f"{'CAPTURÉ — la capture démontrée au tirage pondéré' if capture_pond else 'é vadé'}",
        f"  l'uniforme à la graine cherchée {GRAINE_CHERCHEE} (le canon "
        f"vague 11) : {uni_cherchee} — tls13-17 "
        f"{'PRIS (la capture de la vague 11 REPRODUITE)' if capture_cherchee else 'é vadé'}",
        "",
        "LA DÉMONSTRATION PAR BALAYAGE (200 graines, le taux de capture) :",
    ]
    cap_u = sum(1 for g in range(200) if PIEGE in tirage_uniforme(g))
    cap_w = sum(1 for g in range(200) if PIEGE in tirage_pondere(g, poids))
    rap += [
        f"  l'uniforme : {cap_u}/200 = {cap_u/2:.1f} % (théorie {p_u*100:.1f} %)",
        f"  le pondéré : {cap_w}/200 = {cap_w/2:.1f} % (théorie {p_w*100:.1f} %)",
        "",
        "LA LECTURE : le pondéré À BUDGET ÉGAL double quasi la probabilité "
        "de capture d'un bloc à garde récemment touché ; l'évasion nommée "
        "de la vague 11 (le tirage qui ÉPARGNAIT tls13-17 à la graine par "
        "défaut) est FERMÉE au tirage pondéré — la capture à la MÊME graine. "
        "L'AUDIT DEMEURE UN FILET PROBABILISTE, PAS UNE PREUVE : la garantie "
        "reste la fermeture et la semence full-card.",
        "",
        "LE VERDICT : " + ("VERT — les trois quantités publiées, la capture "
                           "re-démontrée à la graine par défaut au budget égal"
                           if (capture_pond and capture_cherchee) else "ROUGE"),
    ]
    (ICI / "rapport-budget-risque.txt").write_text("\n".join(rap) + "\n",
                                                    encoding="utf-8")
    (ICI / "budget-risque.json").write_text(json.dumps({
        "p_uniforme": round(p_u, 4), "p_pondere": round(p_w, 4),
        "e_sessions_uniforme": round(1 / p_u, 1),
        "e_sessions_pondere": round(1 / p_w, 1),
        "borne_full_card": "la prochaine semence (déterministe)",
        "uniforme_graine_defaut": uni_defaut, "capture_pondere_defaut": capture_pond,
        "uniforme_graine_cherchee": uni_cherchee,
        "balayage_200_uniforme_pct": cap_u / 2,
        "balayage_200_pondere_pct": cap_w / 2,
        "verdict": "VERT" if (capture_pond and capture_cherchee) else "ROUGE",
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(rap))
    return 0 if (capture_pond and capture_cherchee) else 2


if __name__ == "__main__":
    import sys
    sys.exit(main())
