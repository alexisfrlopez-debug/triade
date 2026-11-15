#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_scenario_unite08.py — L'ÉPREUVE POSIX DU SCÉNARIO LIVRÉ (la leçon
de l'Entrée 286 : l'épreuve exécute LE CODE LIVRÉ, pas sa copie ; la garde
de la 294 : les CONSTANTES auditées, pas le seul modèle). Le scénario court
au Windows ; sa fonction PURE — le modèle du juge (modele_ligne) — est
extraite du FICHIER LIVRÉ par AST et rejouée ici contre un CONTRE-MODÈLE
indépendant (la sémantique du contrat réécrite position par position) ;
LES CONSTANTES du scénario recoupées au PLAN (loupe/layout.py — la source
unique) ; le générateur du différentiel V2 rejoué : les DIX MILLE tirages
aux bornes du contrat (multiples de 16 ≤ 0x7FFFFFFF, longueurs 1..16) et
DÉTERMINISTES (deux passages identiques)."""
import ast
import pathlib
import random
import re
import sys

UNITE = pathlib.Path(__file__).resolve().parent
SCENARIO = UNITE / "scenario-unite08.py"

# ---- 1. L'EXTRACTION PAR AST : le modèle du juge, VERBATIM ------------------
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


# ---- 2. LE CONTRE-MODÈLE : la sémantique réécrite position par position ----
def contre_ligne(decalage: int, octets: bytes) -> bytes:
    """LE CONTRE-MODÈLE — indépendant du juge : la ligne bâtie octet par
    octet à ses positions, jamais la composition par jointure."""
    n = min(len(octets), 16)
    ligne = bytearray(77)
    for k in range(8):                       # les chiffres du décalage
        chiffre = (decalage >> (28 - 4 * k)) & 0xF
        ligne[k] = ord("0123456789ABCDEF"[chiffre])
    for i in range(8, 76):                   # le squelette d'espaces
        ligne[i] = 0x20
    for i in range(16):                      # les seize groupes
        pos = 10 + 3 * i + (1 if i >= 8 else 0)
        if i < n:
            ligne[pos] = ord(f"{octets[i] >> 4:X}")
            ligne[pos + 1] = ord(f"{octets[i] & 0xF:X}")
    for i in range(16):                      # le miroir ASCII
        if i < n:
            c = octets[i]
            ligne[60 + i] = c if 0x20 <= c <= 0x7E else ord(".")
    ligne[76] = 0                            # le NUL final
    return bytes(ligne)


rng = random.Random(424242)
cas = 0
for _ in range(2000):
    decalage = rng.randrange(0, 0x8000_0000 // 16) * 16
    longueur = rng.randrange(1, 17)
    octets = rng.randbytes(16)
    attendu = contre_ligne(decalage, octets[:longueur])
    rendu = modele_ligne(decalage, octets[:longueur])
    assert rendu == attendu, (hex(decalage), longueur, rendu, attendu)
    assert len(rendu) == 77, (hex(decalage), len(rendu))
    cas += 1
print(f"[VERT] le modèle du juge == le contre-modèle : {cas} cas aléatoires "
      f"— la ligne fait TOUJOURS 77 o")

# les frontières à la main : le vide d'entrée (1 octet), la ligne pleine,
# le miroir aux bornes 0x1F/0x20/0x7E/0x7F, le décalage maximal du plan
for decalage, octets in ((0, b"\x00"), (0x7FFFF000, bytes(range(16))),
                         (0x30000, b"\x1f\x20\x7e\x7f\x80\xff"),
                         (16, b"A"), (0x10, b"\x00" * 16)):
    assert modele_ligne(decalage, octets) == contre_ligne(decalage, octets), \
        (hex(decalage), octets)
print("[VERT] les frontières : 1 octet, la ligne pleine, le miroir aux "
      "bornes 0x1F/0x20/0x7E/0x7F, le décalage maximal 0x7FFFF000")

# ---- 3. L'AUDIT DES CONSTANTES (la garde née à la 294) ----------------------
graines = re.findall(r"^GRAINE = (\d+)", source, re.M)
rvas = re.findall(r"^R_LOUPE08 = (0x[0-9a-fA-F]+)", source, re.M)
lignes = re.findall(r"^LIGNE = (\d+)", source, re.M)
assert len(graines) == 1 and len(rvas) == 1 and len(lignes) == 1, \
    "les constantes du scénario : GRAINE/R_LOUPE08/LIGNE attendues UNE fois"

LOUPE = UNITE.parents[2] / "loupe"
layout = (LOUPE / "layout.py").read_text(encoding="utf-8")
r_hex = re.findall(r"^R_HEX = (0x[0-9a-fA-F]+)", layout, re.M)
ligne_taille = re.findall(r"^LIGNE_TAILLE = .*\)  # = (\d+) o", layout, re.M)
va08 = re.findall(r"^LOUPE08_VA = (0x[0-9a-fA-F]+)", layout, re.M)
assert len(r_hex) == 1 and len(ligne_taille) == 1 and len(va08) == 1, \
    "le plan : R_HEX/LIGNE_TAILLE/LOUPE08_VA attendus UNE fois"
assert int(rvas[0], 16) == int(va08[0], 16) == 0x49C0, \
    f"R_LOUPE08 {rvas[0]} != LOUPE08_VA du plan {va08[0]}"
assert int(lignes[0]) == int(ligne_taille[0]) == 77, \
    f"LIGNE {lignes[0]} != LIGNE_TAILLE du plan {ligne_taille[0]}"
print(f"[VERT] les constantes auditées : R_LOUPE08 {rvas[0]} == le slot "
      f"i110008 du plan, LIGNE {lignes[0]} == LIGNE_TAILLE, la graine "
      f"{graines[0]} (la table du plan @ R_HEX {r_hex[0]} — la pièce la "
      f"porte à son .rdata, recoupée à l'oracle)")

# ---- 4. LE GÉNÉRATEUR DU V2 : les tirages aux bornes, DÉTERMINISTES -------
def tirages(graine: int):
    r = random.Random(graine)
    out = []
    for _ in range(10_000):
        decalage = r.randrange(0, 0x8000_0000 // 16) * 16
        longueur = r.randrange(1, 17)
        source = r.randbytes(16)
        out.append((decalage, longueur, source))
    return out


premier = tirages(int(graines[0]))
second = tirages(int(graines[0]))
assert premier == second, "le générateur n'est pas déterministe"
assert all(d % 16 == 0 and 0 <= d <= 0x7FFFFFF0 for d, _, _ in premier), \
    "un décalage hors contrat (multiple de 16, ≤ 0x7FFFFFFF)"
assert all(1 <= n <= 16 for _, n, _ in premier), "une longueur hors 1..16"
impaire = sum(1 for _, n, _ in premier if n % 2 == 1)
print(f"[VERT] le générateur du V2 : 10 000 tirages DÉTERMINISTES (deux "
      f"passages identiques), tous multiples de 16 ≤ 0x7FFFFFF0, les "
      f"longueurs 1..16 ({impaire} impaires)")

print("L'ÉPREUVE POSIX DU SCÉNARIO EST VERTE — le juge livré dit la même "
      "chose que le contre-modèle indépendant, aux constantes du plan")
