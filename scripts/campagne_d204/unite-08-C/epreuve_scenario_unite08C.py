#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_scenario_unite08C.py — L'ÉPREUVE POSIX DU SCÉNARIO LIVRÉ, bras C
(la leçon de l'Entrée 286 : l'épreuve exécute LE CODE LIVRÉ, pas sa copie ;
la garde de la 294 : les CONSTANTES et LA DÉCOUVERTE contre la pièce même).
Le modèle du juge (modele_ligne) extrait du FICHIER LIVRÉ par AST, rejoué
contre un CONTRE-MODÈLE indépendant ; les constantes recoupées au juge T
(la même graine, les mêmes tirages) ; LA DÉCOUVERTE PAR LA TABLE D'EXPORTS
rejouée contre la dll réelle — l'export unique lu, les gardes fail-closed."""
import ast
import pathlib
import pefile
import random
import re
import sys

UNITE = pathlib.Path(__file__).resolve().parent
SCENARIO = UNITE / "scenario-unite08C.py"
PIECE = UNITE / "source" / "loupe-08-c.dll"

source = SCENARIO.read_text(encoding="utf-8")
arbre = ast.parse(source)
gardes = []
for noeud in ast.walk(arbre):
    if isinstance(noeud, ast.FunctionDef) and noeud.name == "modele_ligne":
        gardes.append(ast.FunctionDef(
            name=noeud.name, args=noeud.args, body=noeud.body,
            decorator_list=[], returns=noeud.returns,
            type_comment=noeud.type_comment, lineno=noeud.lineno,
            col_offset=noeud.col_offset))
assert len(gardes) == 1, "modele_ligne introuvable au scénario livré"
module = ast.Module(body=gardes, type_ignores=[])
ns = {}
exec(compile(module, str(SCENARIO), "exec"), ns)
modele_ligne = ns["modele_ligne"]
print(f"[extraction] le modèle du juge lu du scénario livré "
      f"({SCENARIO.name}) par AST — exécuté VERBATIM")


# ---- LE CONTRE-MODÈLE (indépendant : position par position) -----------------
def contre_ligne(decalage: int, octets: bytes) -> bytes:
    n = min(len(octets), 16)
    ligne = bytearray(77)
    for k in range(8):
        ligne[k] = ord("0123456789ABCDEF"[(decalage >> (28 - 4 * k)) & 0xF])
    for i in range(8, 76):
        ligne[i] = 0x20
    for i in range(16):
        pos = 10 + 3 * i + (1 if i >= 8 else 0)
        if i < n:
            ligne[pos] = ord(f"{octets[i] >> 4:X}")
            ligne[pos + 1] = ord(f"{octets[i] & 0xF:X}")
    for i in range(16):
        if i < n:
            c = octets[i]
            ligne[60 + i] = c if 0x20 <= c <= 0x7E else ord(".")
    ligne[76] = 0
    return bytes(ligne)


rng = random.Random(777)
cas = 0
for _ in range(2000):
    decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
    longueur = rng.randrange(1, 17)
    octets = rng.randbytes(16)
    assert modele_ligne(decalage, octets[:longueur]) \
        == contre_ligne(decalage, octets[:longueur]), (decalage, longueur)
    cas += 1
print(f"[VERT] le modèle du juge C == le contre-modèle : {cas} cas "
      f"aléatoires — la ligne fait TOUJOURS 77 o")

# ---- LES CONSTANTES : la même graine, la même ligne que le juge T -----------
scen_T = (UNITE.parents[0] / "unite-08-T" / "scenario-unite08.py") \
    .read_text(encoding="utf-8")
graines_C = re.findall(r"^GRAINE = (\d+)", source, re.M)
graines_T = re.findall(r"^GRAINE = (\d+)", scen_T, re.M)
lignes_C = re.findall(r"^LIGNE = (\d+)", source, re.M)
lignes_T = re.findall(r"^LIGNE = (\d+)", scen_T, re.M)
assert graines_C == graines_T == ["20261115"], \
    f"les graines divergent : C {graines_C} T {graines_T}"
assert lignes_C == lignes_T == ["77"], \
    f"les lignes divergent : C {lignes_C} T {lignes_T}"
print(f"[VERT] les constantes auditées : GRAINE {graines_C[0]} == la graine "
      f"du juge T (les MÊMES tirages aux deux bras), LIGNE "
      f"{lignes_C[0]} o — l'appariement du plan (CA2)")

# ---- LA DÉCOUVERTE CONTRE LA PIÈCE MÊME (la garde de la 294) ---------------
pe = pefile.PE(str(PIECE))
exports = {(e.name.decode(), e.address)
           for e in pe.DIRECTORY_ENTRY_EXPORT.symbols}
assert exports == {("loupe_08_ligne", 0x1380)}, \
    f"la découverte attend l'export unique, la pièce porte : {exports}"
# la relecture des gardes : le répertoire d'exports au PE32+ (+112)
assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].VirtualAddress != 0, \
    "le répertoire d'exports absent — la garde du scénario refuserait"
print(f"[VERT] la découverte rejouée contre la pièce : l'export UNIQUE "
      f"loupe_08_ligne @+{list(exports)[0][1]:#x}, le répertoire présent "
      f"— les gardes fail-closed trouveraient la pièce juste")

# ---- LE GÉNÉRATEUR : DÉTERMINISTE, aux bornes du contrat -------------------
def tirages(graine: int):
    r = random.Random(graine)
    out = []
    for _ in range(10_000):
        decalage = r.randrange(0, 0x8000_0000 // 16) * 16
        longueur = r.randrange(1, 17)
        source_ = r.randbytes(16)
        out.append((decalage, longueur, source_))
    return out


premier = tirages(int(graines_C[0]))
second = tirages(int(graines_C[0]))
assert premier == second, "le générateur n'est pas déterministe"
assert all(d % 16 == 0 and 0 <= d <= 0x7FFFFFF0 for d, _, _ in premier)
assert all(1 <= n <= 16 for _, n, _ in premier)
print("[VERT] le générateur du V2 : 10 000 tirages DÉTERMINISTES, aux "
      "bornes du contrat (multiples de 16 ≤ 0x7FFFFFF0, longueurs 1..16)")

print("L'ÉPREUVE POSIX DU SCÉNARIO C EST VERTE — le juge livré dit la même "
      "chose que le contre-modèle, contre la pièce même, aux constantes du "
      "juge T apparié")
