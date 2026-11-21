#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""census_batterie.py — LE CENSUS EXACT DE LA BATTERIE 559 (6kbfrpn7k, l'item 3).

LA CAUSE : la ligne v0.22.0 « 64 + 3 queue · 4 chevauchants · 13 longueurs ·
3 pages · 8 multi · 512 property-based » ne se recompose PAS — la somme
64+3+4+13+3+8+512 = 607 ≠ 559. Le census exact vit dans le GÉNÉRATEUR
(atelier-corridors-fnvan0zes/mesurer_corridors.py, la section (1) de main) ;
la présente l'exécute PAR CODE et somme par catégorie : la preuve que le
compte imprimé 559 est le compte du générateur, catégorie par catégorie.

Sortie : census-batterie.json · rapport-census.txt"""
from __future__ import annotations

import json
import pathlib
import random

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent

# LA GÉNÉRATION — LA COPIE EXACTE de mesurer_corridors.py § (1), la même
# graine (20261120) — le compte par catégorie est INDEPENDANT du tirage
# (les bornes des boucles font le census), la graine ne sert qu'à reproduire
# les tampons.
rng = random.Random(20261120)
vecteurs: list[tuple] = []

# (a) occurrences plantées EN QUEUE — le dernier bloc de 16, chaque position
for p in range(16):
    f = bytearray(rng.randrange(256) for _ in range(4096))
    m = bytes(rng.randrange(256) for _ in range(16))
    pos = max(0, 4096 - 16 - (15 - p))
    f[pos:pos + 16] = m
    vecteurs.append(("queue-16", bytes(f), m, bytes(f).find(m)))
# (a2) la queue à la longueur du motif
for lm in (1, 4, 16):
    f = bytearray(rng.randrange(256) for _ in range(1000))
    m = bytes(rng.randrange(256) for _ in range(lm))
    pos = 1000 - lm
    f[pos:pos + lm] = m
    vecteurs.append(("queue-fin", bytes(f), m, bytes(f).find(m)))
# (b) occurrences CHEVAUCHANTES (périodes 1 à 4)
for periode in range(1, 5):
    f = bytearray(0x41 for _ in range(512))
    base = bytes(rng.randrange(256) for _ in range(periode))
    m = (base * (16 // periode + 1))[:16]
    pos = rng.randrange(64, 448)
    for i in range(16):
        f[pos + i] = m[i]
    vecteurs.append(("chevauchant-p%d" % periode, bytes(f), m, bytes(f).find(m)))
# (c) LONGUEURS DE MOTIF 1 à >16
for lm in (1, 2, 3, 4, 15, 16, 17, 18, 19, 20, 31, 32, 33):
    f = bytearray(rng.randrange(256) for _ in range(2048))
    m = bytes(rng.randrange(256) for _ in range(lm))
    pos = rng.randrange(0, 2048 - lm)
    f[pos:pos + lm] = m
    vecteurs.append(("longueur-%d" % lm, bytes(f), m, bytes(f).find(m)))
# (d) FRANCHISSEMENT DE PAGE
for bord in ("avant", "apres", "traverse"):
    f = bytearray(rng.randrange(256) for _ in range(512))
    m = bytes(rng.randrange(256) for _ in range(8))
    pos = {"avant": 505, "apres": 513, "traverse": 508}[bord]
    f[pos:pos + 8] = m
    vecteurs.append(("page-" + bord, bytes(f), m, bytes(f).find(m)))
# (e) MULTI-OCCURRENCES (1 à 8)
for nocc in range(1, 9):
    f = bytearray(rng.randrange(256) for _ in range(2048))
    m = bytes(rng.randrange(256) for _ in range(6))
    positions = sorted(rng.sample(range(0, 2048 - 6), nocc))
    for p in positions:
        f[p:p + 6] = m
    vecteurs.append(("multi-%d" % nocc, bytes(f), m, bytes(f).find(m)))
# (f) TIRAGES PROPERTY-BASED (la graine consignée)
for k in range(512):
    n = rng.choice([17, 63, 100, 256, 1000, 4096])
    lm = rng.choice([1, 2, 3, 5, 8, 16, 17, 24, 32])
    f = bytearray(rng.randrange(256) for _ in range(n))
    m = bytes(rng.randrange(256) for _ in range(lm))
    if rng.random() < 0.7 and n > lm:
        p = rng.randrange(0, n - lm + 1)
        f[p:p + lm] = m
    vecteurs.append(("pbt-%d" % k, bytes(f), m, bytes(f).find(m)))

# ---- LE CENSUS PAR CATÉGORIE ----------------------------------------------
census: dict[str, int] = {}
for classe, *_ in vecteurs:
    cle = classe.split("-")[0]
    census[cle] = census.get(cle, 0) + 1
# les catégories affinées (queue-16 / queue-fin séparées, chevauchants,
# longueurs, pages, multi, pbt)
census_fins = {
    "queue-16 (le dernier bloc de 16, chaque position)": sum(
        1 for v in vecteurs if v[0] == "queue-16"),
    "queue-fin (l'occurrence finissant au dernier octet)": sum(
        1 for v in vecteurs if v[0] == "queue-fin"),
    "chevauchants (périodes 1 à 4)": sum(
        1 for v in vecteurs if v[0].startswith("chevauchant")),
    "longueurs de motif (1 à 33, treize valeurs)": sum(
        1 for v in vecteurs if v[0].startswith("longueur")),
    "franchissement de page (avant/après/traverse)": sum(
        1 for v in vecteurs if v[0].startswith("page")),
    "multi-occurrences (1 à 8)": sum(
        1 for v in vecteurs if v[0].startswith("multi")),
    "property-based (graine 20261120)": sum(
        1 for v in vecteurs if v[0].startswith("pbt")),
}
total = sum(census_fins.values())

rapport = [
    "LE CENSUS EXACT DE LA BATTERIE 559 (6kbfrpn7k, l'item 3)",
    "le générateur re-exécuté par code — le compte par catégorie sommé",
    "",
    "LA LIGNE v0.22.0 EN CAUSE : « 64 + 3 queue · 4 chevauchants ·",
    "13 longueurs · 3 pages · 8 multi · 512 property-based » — la somme",
    "64+3+4+13+3+8+512 = 607 ≠ 559 : ELLE NE SE RECOMPOSE PAS (le « 64 »",
    "faux pour les 16 queue-16, l'auteur comptant sans doute les 16",
    "alignements de queue comme 64).",
    "",
    "LE CENSUS EXACT (les bornes des boucles du générateur, la preuve par",
    "exécution) :",
]
for k, v in census_fins.items():
    rapport.append(f"  {v:4d}  {k}")
rapport += [
    "  ----",
    f"  {total:4d}  LE TOTAL — {'== 559 EXACTEMENT' if total == 559 else '≠ 559 — ROUGE'}",
    "",
    "LA LIGNE DE PROSE QUI RECOMPOSE (portée au §7 du manuscrit et au",
    "rapport-corridors de la génération suivante) : « 16 queue-16 + 3",
    "queue-fin + 4 chevauchants + 13 longueurs + 3 pages + 8 multi +",
    "512 property-based = 559 ».",
    "",
    "LE VERDICT : " + ("VERT — le census sommé par code fait 559 exactement"
                        if total == 559 else "ROUGE"),
]

(ICI / "census-batterie.json").write_text(json.dumps({
    "census": census_fins, "total": total,
    "attendu": 559,
    "verdict": "VERT" if total == 559 else "ROUGE",
}, ensure_ascii=False, indent=1), encoding="utf-8")
(ICI / "rapport-census.txt").write_text("\n".join(rapport) + "\n",
                                          encoding="utf-8")
print("\n".join(rapport))
import sys
sys.exit(0 if total == 559 else 2)
