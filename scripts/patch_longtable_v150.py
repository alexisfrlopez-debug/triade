#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patch longtable : la table des preuves de extraire_donnees_v150.py
passe de float table (rejetée silencieusement : « Float too large »,
la dette v0.13.0/v0.14.0) à LONGTABLE (elle se coupe sur les pages)."""
import pathlib

p = pathlib.Path("/home/z/my-project/triade/scripts/extraire_donnees_v150.py")
s = p.read_text("utf-8")

# localisation robuste : la caption « Strengthened evidence » est unique
motif_caption = 'tex.append(r"\\caption{Strengthened evidence'
i_caption = s.index(motif_caption)
i_debut = s.rindex("tex.append(", 0, i_caption - 2)  # le append du begin
motif_fin = 'tex.append(r"\\end{tabularx}\\end{table}")'
i_fin = s.index(motif_fin, i_caption)
i_fin_fin = i_fin + len(motif_fin)

nouveau = (
    '# v0.15.0 : LA DETTE SCELLÉE GUÉRIE — le float de la table des\n'
    '    # preuves (29 lignes en v0.13.0/v0.14.0, 34 en v0.15.0) était '
    'TROP\n'
    '    # GRAND pour une page et LaTeX le rejetait SILENCIEUSEMENT '
    '(« Float\n'
    '    # too large », la table jamais rendue) : elle devient LONGTABLE '
    '—\n'
    '    # elle se COUPE sur les pages, toutes les lignes sont rendues.\n'
    '    tex.append(r"\\begingroup\\scriptsize")\n'
    '    tex.append(r"\\begin{longtable}{@{}p{2.4cm} p{2.7cm} p{5.4cm} "\n'
    '               r"p{3.6cm}@{}}")\n'
    '    tex.append(r"\\caption{Strengthened evidence across editions, '
    'every "\n'
    '               r"row generated from the raw instrument outputs '
    '(no value "\n'
    '               r"typed by hand): the six v0.11.0 instruments '
    '(D185, "\n'
    '               r"consigned seeds), the v0.12.0 formal model and '
    'seal "\n'
    '               r"analysis (D187, D189), the v0.13.0 corrections '
    '(the "\n'
    '               r"audited benchmark, the corrected seal statistics), '
    'the "\n'
    '               r"v0.14.0 empirical programme, and the v0.15.0 '
    'unbounded "\n'
    '               r"proofs and refinement.}\\\\")\n'
    '    tex.append(r"\\label{tab:preuves}\\\\")\n'
    '    tex.append(r"\\toprule")\n'
    '    tex.append(r"\\textbf{Instrument} & \\textbf{Target} & "\n'
    '               r"\\textbf{Measured} & \\textbf{Raw source} \\\\\\")\n'
    '    tex.append(r"\\midrule\\\\endhead")\n'
    '    tex.append(r"\\bottomrule\\\\endfoot")'
)
fin_bloc = 'tex.append(r"\\end{longtable}\\\\endgroup")'

s2 = s[:i_debut] + nouveau + "\n    " + fin_bloc + s[i_fin_fin:]
p.write_text(s2, "utf-8")
import ast
ast.parse(s2)
print("OK : tab:preuves -> longtable (syntaxe vérifiée)")
