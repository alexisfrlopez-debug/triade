#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""répare la boucle du corps de tab:preuves (détruite par le patch
longtable : la boucle vivait entre le begin et le end remplacés)."""
import ast
import pathlib

p = pathlib.Path("/home/z/my-project/triade/scripts/extraire_donnees_v150.py")
s = p.read_text("utf-8")

BS = chr(92)
ancien = (
    '    tex.append(r"' + BS + 'bottomrule")\n'
    '    tex.append(r"' + BS + 'endfoot")\n'
    '    tex.append(r"' + BS + 'end{longtable}' + BS + 'endgroup")'
)
nouveau = (
    '    tex.append(r"' + BS + 'bottomrule")\n'
    '    tex.append(r"' + BS + 'endfoot")\n'
    '    for instr, cible, mesure, source in preuves:\n'
    '        # la colonne source porte des chemins monospaces INCOUPABLES\n'
    '        # de naissance : des points de coupe explicites APRÈS chaque /\n'
    '        # et chaque ' + BS + '_ (sinon la cellule déborde)\n'
    '        src_coupable = source.replace("/", r"/' + BS + 'allowbreak{}")'
    '.replace(\n'
    '            r"' + BS + '_", r"' + BS + '_ ' + BS + 'allowbreak{}")\n'
    '        tex.append(rf"{cell(instr)} & {cell(cible)} & {cell(mesure)}'
    ' & "\n'
    '                   rf"' + BS + 'code{{{src_coupable}}} ' + BS + BS + '")\n'
    '        tex.append(r"' + BS + 'addlinespace[1.5pt]")\n'
    '    tex.append(r"' + BS + 'bottomrule")\n'
    '    tex.append(r"' + BS + 'end{longtable}' + BS + 'endgroup")'
)
assert ancien in s, "ancre introuvable"
s = s.replace(ancien, nouveau, 1)
p.write_text(s, "utf-8")
ast.parse(s)
print("OK : la boucle du corps est réinsérée")
