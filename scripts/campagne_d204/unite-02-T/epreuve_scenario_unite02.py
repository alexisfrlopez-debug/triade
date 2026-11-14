#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_scenario_unite02.py — L'ÉPREUVE POSIX DU SCÉNARIO LIVRÉ (la leçon
de l'Entrée 286 : l'épreuve exécute LE CODE LIVRÉ, pas sa copie). Le
scénario court au Windows ; ses fonctions PURES — le modèle du juge
(modele_tampon) et les décalées du terrain (decales_terrain) — sont
extraites du FICHIER LIVRÉ par AST et rejouées ici contre un CONTRE-MODÈLE
indépendant (la sémantique du contrat réécrite) sur 2 000 cas aléatoires
et les frontières."""
import ast
import pathlib
import random
import sys

UNITE = pathlib.Path(__file__).resolve().parent
SCENARIO = UNITE / "scenario-unite02.py"

source = SCENARIO.read_text(encoding="utf-8")
arbre = ast.parse(source)
gardes = []
for noeud in ast.walk(arbre):
    if isinstance(noeud, ast.FunctionDef) and noeud.name in (
            "modele_tampon", "decales_terrain"):
        gardes.append(ast.FunctionDef(
            name=noeud.name, args=noeud.args, body=noeud.body,
            decorator_list=[], returns=noeud.returns,
            type_comment=noeud.type_comment, lineno=noeud.lineno,
            col_offset=noeud.col_offset))
assert len(gardes) == 2, "les DEUX fonctions pures introuvables au scénario"
module = ast.Module(body=gardes, type_ignores=[])
ns = {"min": min, "random": random, "GRAINE": 20261114}
exec(compile(module, str(SCENARIO), "exec"), ns)
modele_tampon = ns["modele_tampon"]
decales_terrain = ns["decales_terrain"]
print(f"[extraction] les DEUX fonctions pures lues du scénario livré "
      f"({SCENARIO.name}) par AST — exécutées VERBATIM")


def contre(donnees: bytes, dec: int, journal):
    """LE CONTRE-MODÈLE — la sémantique du contrat réécrite indépendamment."""
    if dec % 16 or dec >= len(donnees):
        raise ValueError("hors contrat")
    r = min(384, len(donnees) - dec)
    t = bytearray(donnees[dec:dec + r])
    for d, o in journal:
        if dec <= d < dec + r:
            t[d - dec] = o
    return r, bytes(t)


rng = random.Random(42)
cas = 0
for _ in range(2000):
    taille = rng.choice([1, 16, 384, 385, 196609,
                         rng.randrange(16, 5000)])
    donnees = rng.randbytes(taille)
    pool = list(range(0, (taille + 15) // 16 * 16, 16))
    dec = rng.choice(pool)
    if dec >= taille:
        continue
    journal = [(rng.randrange(0, taille + 800), rng.randrange(256))
               for _ in range(rng.randrange(6))]
    attendu = contre(donnees, dec, journal)
    rendu = modele_tampon(donnees, dec, journal)
    assert rendu == attendu, (dec, taille, journal, rendu, attendu)
    cas += 1
print(f"[VERT] le modèle du juge == le contre-modèle : {cas} cas aléatoires "
      f"(les tailles 1/16/384/385/196609/alea, les journaux 0-5 entrées)")

for t in (1, 16, 384, 385, 196609):
    ds = decales_terrain(t)
    assert all(d % 16 == 0 and d < t for d in ds), (t, ds)
    assert 0 in ds and (t - 1) // 16 * 16 in ds, (t, ds)
    assert len(ds) == len(set(ds)), (t, ds)
print("[VERT] les décalées du terrain : multiples de 16, < taille, "
      "UNIQUES, les frontières couvertes (0 et la dernière valide)")
print("L'ÉPREUVE POSIX DU SCÉNARIO EST VERTE — le juge livré dit la même "
      "chose que le contre-modèle indépendant")
