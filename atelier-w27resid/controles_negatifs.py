#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les contrôles négatifs de W27RESID (C27/C28/C29) — sur COPIES, jamais sur
les pièces ni les sources réelles. Une mutation par classe, refusée nommément,
plus les inversions de sens."""
import importlib.util
import pathlib
import re
import sys

R = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("linter_v4", str(R / "scripts/vague20/linter_v4.py"))
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

# L'état corrigé : le manuscrit corrigé + la spec v0.15.17 + le Livre v1.16 + preuves/présentation v0.31.0
t = L.charge(R / "pack-v310")
t["manuscrit"] = L.texte(R / "edition-v0230/main.pdf")
t["specification"] = L.texte(R / "scripts/spec_v159/main.pdf")
t["livre"] = L.texte(R / "scripts/livre_v19/final.pdf")

base = L.controles_w27b(t, R)
print("socle (état corrigé) :", "VERT" if not base else f"ROUGE — {base}")
assert not base, "le socle doit être vert avant toute mutation"

essais = []


def essai(nom, classe, attendu_piece, mut=None, titres=None):
    tt = dict(t)
    if mut:
        for piece, (mot, remp) in mut.items():
            plat = re.sub(r"\s+", " ", L.normalise(tt[piece])).replace("\u2019", "'")
            assert mot in plat, f"ancre absente : {mot[:60]}"
            tt[piece] = plat.replace(mot, remp)
    r = L.controles_w27b(tt, R, titres_override=titres)
    refus = [x for x in r if x[0] == classe]
    ok = any(x[1] == attendu_piece for x in refus)
    essais.append((nom, ok, refus))


# --- C27 : le compte d'arbres muté dans une cellule d'état (Table 12 recréée) ---
essai("C27 — verifier 13 arbres ressuscité (Table 12, non daté)", "C27", "specification",
      mut={"specification": ("verifier 14 arbres VERTS", "verifier 13 arbres VERTS")})

# --- C27 : le compte de vecteurs muté ---
essai("C27 — compte de vecteurs muté (234 exécutables)", "C27", "presentation",
      mut={"presentation": ("235 exécutables", "234 exécutables")})

# --- C28 : le titre dupliqué (le défaut §1.23/§1.24 ressuscité) ---
titres_v158 = {}
spec158 = R / "scripts/spec_v158"
ts = []
for f in sorted(spec158.glob("*.tex")):
    ts += [x.strip() for x in re.findall(r"\\(?:sub)?section\*?\{([^}]+)\}", f.read_text(encoding="utf-8"))]
titres_v158["specification"] = ts
essai("C28 — le titre dupliqué de la v0.15.16 ressuscité", "C28", "specification",
      titres=titres_v158)

# --- C29 : le fragment français ressuscité dans le manuscrit anglais ---
essai("C29 — « installés à la vague 14 » ressuscité", "C29", "manuscrit",
      mut={"manuscrit": ("installed at wave 14", "installés à la vague 14")})

# --- C29 : le compte français « N pas » ressuscité ---
essai("C29 — « 1 122 pas » ressuscité", "C29", "manuscrit",
      mut={"manuscrit": ("1,122 steps, 29.4 s", "1 122 pas, 29,4 s")})

# --- C29 : une séquence anglaise dans une pièce française ---
essai("C29 — séquence anglaise dans la présentation", "C29", "presentation",
      mut={"presentation": ("les campagnes de la", "the campaigns of the and with the verdict that")})

verts = 0
print("=" * 78)
print("CONTRÔLES NÉGATIFS W27RESID — C27/C28/C29 (sur copies)")
print("=" * 78)
for nom, ok, refus in essais:
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    for c, p, m in refus[:2]:
        print(f"        → {c} {p} — {m[:110]}")
print(f"{verts}/{len(essais)}")
sys.exit(0 if verts == len(essais) else 3)
