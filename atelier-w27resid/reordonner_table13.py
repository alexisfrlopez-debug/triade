#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reordonner_table13.py — W27RESID (d) : la chronologie du terrain du Livre
(table 13) RÉORDONNÉE aux dates imprimées. L'ordre actuel suit l'ordre de la
conversation ; l'ordre rétabli suit les dates : 30/10 soir (cérémonie CF1→CF2)
→ 20:03 → 20:37 → 20:40 (MIGRER, époque 1, checksum 0cc89a96) → 20:41
(VÉRIFIER VERT — le rapport de boîte noire v1.1 du 30/10 20:41 fait foi,
D133) → 31/10 18:10 → 18:18 → 31/10 soir → à suivre. Les dates imprimées
demeurent telles quelles ; seul l'ordre des rangées change."""
import pathlib
import re

P = pathlib.Path(__file__).resolve().parents[1] / "scripts/livre_v19/sec-5.tex"
src = P.read_text(encoding="utf-8")

# Les rangées de la table tab:chronoterrain, entre \midrule et \bottomrule
m = re.search(r"(\\begin\{tabularx\}\{\\textwidth\}\{@\{\}l Y@\{\}\}.*?\\toprule\n"
              r"\\textbf\{Quand\} & \\textbf\{Ce qui s'est passé\} \\\\\n\\midrule\n)"
              r"(.*?)\n\\bottomrule", src, re.S)
assert m, "la table chronoterrain est introuvable"
entete, corps = m.group(1), m.group(2)

# Découpe en rangées : chaque rangée commence par une étiquette « Quand »
rangées = re.split(r"\n(?=\d{2}/10 |à suivre)", corps)
rangées = [r for r in rangées if r.strip()]
avant = [r.strip() for r in rangées]
print("Ordre actuel :")
for r in avant:
    print("  -", r.split(" &")[0])


def cle(r):
    """La clé chronologique de la rangée, à ses dates imprimées."""
    if r.startswith("30/10 soir"):
        return (30, 0, 0)          # la cérémonie CF1→CF2 ouvre la soirée
    if r.startswith("31/10 soir"):
        return (31, 23, 59)
    if r.startswith("à suivre"):
        return (99, 0, 0)
    m2 = re.match(r"(\d{2})/10 (\d{2}):(\d{2})", r)
    return (int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))


apres = sorted(rangées, key=cle)
print("\nOrdre rétabli :")
for r in apres:
    print("  -", r.strip().split(" &")[0])

if [r.strip() for r in apres] == avant:
    raise SystemExit("la table était déjà en ordre — rien à faire (ANOMALIE : l'ordre attendu divergeait)")

nouveau = m.group(0).replace(corps, "\n".join(r.rstrip() for r in apres))
src = src.replace(m.group(0), nouveau)
P.write_text(src, encoding="utf-8")
print("\n[table 13] rangées réordonnées aux dates imprimées — le texte de chaque rangée est inchangé")
