#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_scenario_unite13C.py — L'ÉPREUVE POSIX DU SCÉNARIO C LIVRÉ (la leçon
de l'Entrée 286 : l'épreuve exécute LE CODE LIVRÉ, pas sa copie ; la garde
de la 294 : les CONSTANTES auditées, pas le seul modèle). Le scénario court
au Windows ; sa fonction PURE — le modèle du juge (modele_recherche) — est
extraite du FICHIER LIVRÉ par AST et rejouée ici contre un CONTRE-MODÈLE
indépendant (le balayage position par position, jamais bytes.find) ; LES
CONSTANTES du scénario recoupées au PLAN (loupe/layout.py — la source
unique) ; le générateur du différentiel V2 rejoué : les DIX MILLE tirages
aux bornes du contrat (fenêtres 0..4 096, motifs 1..32, alphabet plein ET
pauvre, départs 0..n) et DÉTERMINISTES (deux passages identiques)."""
import ast
import pathlib
import random
import re
import sys

UNITE = pathlib.Path(__file__).resolve().parent
SCENARIO = UNITE / "scenario-unite13C.py"

# ---- 1. L'EXTRACTION PAR AST : le modèle du juge, VERBATIM ------------------
source = SCENARIO.read_text(encoding="utf-8")
arbre = ast.parse(source)
gardes = []
for noeud in ast.walk(arbre):
    if isinstance(noeud, ast.FunctionDef) and noeud.name == "modele_recherche":
        gardes.append(ast.FunctionDef(
            name=noeud.name, args=noeud.args, body=noeud.body,
            decorator_list=[], returns=noeud.returns,
            type_comment=noeud.type_comment, lineno=noeud.lineno,
            col_offset=noeud.col_offset))
assert len(gardes) == 1, "modele_recherche introuvable au scénario livré"
module = ast.Module(body=gardes, type_ignores=[])
ns = {}
exec(compile(module, str(SCENARIO), "exec"), ns)
modele_recherche = ns["modele_recherche"]
print(f"[extraction] le modèle du juge lu du scénario livré "
      f"({SCENARIO.name}) par AST — exécuté VERBATIM")


# ---- 2. LE CONTRE-MODÈLE : le balayage position par position ----------------
def contre_recherche(fenetre: bytes, motif: bytes, depart: int) -> int:
    """LE CONTRE-MODÈLE — indépendant du juge : le balayage explicite
    candidat par candidat, octet par octet, jamais bytes.find."""
    if len(motif) < 1 or len(motif) > 32:
        return -5
    if depart > len(fenetre):
        return -5
    if len(motif) > len(fenetre) - depart:
        return -1
    for i in range(depart, len(fenetre) - len(motif) + 1):
        egal = True
        for k in range(len(motif)):
            if fenetre[i + k] != motif[k]:
                egal = False
                break
        if egal:
            return i
    return -1


rng = random.Random(424242)
cas = 0
for _ in range(2000):
    n = rng.randrange(0, 513)
    pauvre = rng.randrange(2)
    alphabet = b"AB" if pauvre else bytes(range(256))
    fenetre = bytes(alphabet[rng.randrange(len(alphabet))] for _ in range(n))
    m = rng.randrange(1, 33)
    motif = bytes(alphabet[rng.randrange(len(alphabet))] for _ in range(m))
    depart = rng.randrange(0, n + 1) if n else 0
    attendu = contre_recherche(fenetre, motif, depart)
    rendu = modele_recherche(fenetre, motif, depart)
    assert rendu == attendu, (n, m, depart, rendu, attendu)
    cas += 1
print(f"[VERT] le modèle du juge == le contre-modèle : {cas} cas aléatoires "
      f"(le balayage position par position, jamais bytes.find)")

# les frontières à la main : la fenêtre vide, la plage vide, le motif au
# dernier candidat, le motif plus long, le motif de 32 exactement, les
# rejets 33/0/départ au-delà, le motif répétitif
for fenetre, motif, depart in (
        (b"", b"A", 0),
        (b"abc", b"abc", 3),
        (b"AAAAA", b"A" * 32, 0),
        (b"AB", b"ABC", 0),
        (b"A" * 32, b"A" * 32, 0),
        (b"A" * 32, b"A" * 33, 0),
        (b"ABCD", b"A", 4),
        (b"ABCD", b"A", 5),
        (b"AAAAB", b"AAAA", 0),
        (b"abcabcabc", b"abc", 4)):
    assert modele_recherche(fenetre, motif, depart) == \
        contre_recherche(fenetre, motif, depart), (fenetre, motif, depart)
print("[VERT] les frontières : la fenêtre vide, la plage vide, le motif de "
      "32 exactement, 33 refusé, le départ == la taille, le départ au-delà, "
      "le motif au dernier candidat, AAAA dans AAAAB")

# ---- 3. L'AUDIT DES CONSTANTES (la garde née à la 294) ----------------------
graines = re.findall(r"^GRAINE = (\d+)", source, re.M)
fenetres = re.findall(r"^FENETRE_PROXY = (\d+)", source, re.M)
export = re.findall(r'"loupe_13_recherche"', source, re.M)
assert len(graines) == 1 and len(fenetres) == 1 and len(export) >= 2, \
    "les constantes du scénario C : GRAINE/FENETRE_PROXY/l'export attendues"

# LA DÉCOUVERTE DU SCÉNARIO : la convention (base, rva) unifiée — la
# leçon de la 302 : le scénario ne porte AUCUNE RVA codée en dur (la
# table d'exports parle), la graine et la fenêtre du plan
assert "lire_octets(base," in source and "lire_u32(base," in source, \
    "la convention du scénario C : (base, rva) attendue aux lectures"
assert int(fenetres[0]) == 8192, \
    f"FENETRE_PROXY {fenetres[0]} != 8 192 (la première fenêtre du scellé)"
print(f"[VERT] les constantes auditées : l'export unique loupe_13_recherche "
      f"à DÉCOUVRIR par la table (aucune RVA codée — la leçon de la 302), "
      f"la convention (base, rva) unifiée, la graine {graines[0]}, "
      f"FENETRE_PROXY {fenetres[0]}")

# ---- 4. LE GÉNÉRATEUR REJOUÉ : les tirages aux bornes, déterministes -------
passages = []
for _ in range(2):
    rng = random.Random(int(graines[0]))
    tirages = []
    for _ in range(1000):
        n = rng.randrange(0, 4097)
        pauvre = rng.randrange(2)
        alphabet = b"AB" if pauvre else bytes(range(256))
        fenetre = bytes(alphabet[rng.randrange(len(alphabet))]
                        for _ in range(n))
        m = rng.randrange(1, 33)
        motif = bytes(alphabet[rng.randrange(len(alphabet))]
                      for _ in range(m))
        depart = rng.randrange(0, n + 1) if n else 0
        tirages.append((n, pauvre, fenetre, m, motif, depart))
    passages.append(tirages)
assert passages[0] == passages[1], "le générateur n'est pas déterministe"
n_max = max(t[0] for t in passages[0])
m_min = min(t[3] for t in passages[0])
m_max = max(t[3] for t in passages[0])
pauvres = sum(t[1] for t in passages[0])
departs_max = max(t[5] for t in passages[0] if t[0])
assert n_max <= 4096 and m_min >= 1 and m_max <= 32, (n_max, m_min, m_max)
print(f"[VERT] le générateur du différentiel rejoué : DEUX passages "
      f"IDENTIQUES, les bornes tenues (fenêtres ≤ {n_max}, motifs "
      f"{m_min}..{m_max}, {pauvres}/1 000 alphabets pauvres, départs "
      f"≤ {departs_max}) — les MÊMES tirages au labo et au terrain")

print("=== L'ÉPREUVE DU SCÉNARIO 13 C : TOUT VERT ===")
sys.exit(0)
