#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les contrôles négatifs de C26 STATUS-INTERPIECES (W27RECON) — sur COPIES,
jamais sur les pièces ni les registres réels.

Exigence du prompt : au moins deux contrôles négatifs —
  (i)  STATUT MUTÉ DANS UNE PIÈCE : le Livre v1.16 retrouve le texte fautif
       de la v1.15 (« le déploiement n'est pas fait ») → refus C26 nommé ;
  (ii) REGISTRE MUTÉ : le statut d'ancrage dérivé passe EN ATTENTE (le
       journal amputé de l'édition courante) → les pièces disant DÉPLOYÉ
       sont refusées nommément.
Plus deux contrôles complémentaires (NV, ProVerif) pour couvrir les cinq
familles du registre.
"""
import importlib.util
import pathlib
import sys

R = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("linter_v4", str(R / "scripts/vague20/linter_v4.py"))
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

import re

# Les cinq pièces à l'état v0.32.0 approximé : le pack v310 + le Livre v1.16
t = L.charge(R / "pack-v310")
t["livre"] = L.texte(R / "scripts/livre_v19/final.pdf")

# Le socle : zéro refus C26 sur l'état réel (statuts dérivés des registres réels)
base = L.controles_w27(t, R)
print("socle (état réel) :", "VERT — 0 refus C26" if not base else f"ROUGE — {base}")
assert not base, "le socle doit être vert avant toute mutation"

essais = []


def essai(nom, attendu, mutation_pieces=None, override=None):
    tt = dict(t)
    if mutation_pieces:
        for piece, (mot, remp) in mutation_pieces.items():
            plat = re.sub(r"\s+", " ", L.normalise(tt[piece]))
            assert mot in plat, f"ancre absente pour {nom} : {mot[:60]}"
            tt[piece] = plat.replace(mot, remp)
    r = L.controles_w27(tt, R, override=override)
    refus_c26 = [x for x in r if x[0] == "C26"]
    ok = any(x[1] == attendu for x in refus_c26)
    essais.append((nom, ok, refus_c26))


# (i) STATUT MUTÉ DANS UNE PIÈCE — le Livre retrouve le texte fautif de v1.15
essai("statut muté dans une pièce (Livre v1.15 ressuscité)", "livre",
      mutation_pieces={"livre": ("le déploiement est APPLIQUÉ", "le déploiement n'est pas fait")})

# (i-bis) même classe de mutation, une autre pièce (présentation)
essai("statut muté dans une pièce (présentation NON DÉPLOYÉ)", "presentation",
      mutation_pieces={"presentation": ("l'ancrage de transparence est DÉPLOYÉ",
                                         "l'ancrage de transparence est NON DÉPLOYÉ")})

# (ii) REGISTRE MUTÉ — le journal amputé : le statut dérivé passe EN ATTENTE
statuts_reels = L._statuts_partages(R)
mut = dict(statuts_reels)
mut["ancrage"] = "EN ATTENTE"
essai("registre muté (journal amputé → EN ATTENTE)", "presentation", override=mut)
ok_livre = any(x[1] == "livre" for x in essais[-1][2]) and any(x[1] == "preuves" for x in essais[-1][2])
essais.append(("registre muté → le Livre ET les preuves refusés pareil", ok_livre, essais[-1][2]))

# (iii) complément NV — le registre dit mesuré, les pièces disent EN ATTENTE
mut_nv = dict(statuts_reels)
mut_nv["nv"] = "run matériel VERT (mesuré au poste réel)"
essai("registre NV muté (mesuré) → pièces EN ATTENTE refusées", "livre", override=mut_nv)

# (iv) complément ProVerif — une pièce prétend le run exécuté
essai("statut ProVerif muté dans une pièce", "presentation",
      mutation_pieces={"presentation": ("ProVerif : port livré, run non exécuté",
                                         "ProVerif : port livré, run exécuté")})

verts = 0
print("=" * 78)
print("CONTRÔLES NÉGATIFS C26 — STATUS-INTERPIECES (sur copies)")
print("=" * 78)
for nom, ok, refus in essais:
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    for c, p, m in refus[:3]:
        print(f"        → {c} {p} — {m[:110]}")
print(f"{verts}/{len(essais)}")
sys.exit(0 if verts == len(essais) else 3)
