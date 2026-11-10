#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""porte_ere_011.py — LE PORT DE L'ÈRE 0.1.1 (D178/D179) sur carte_m10.py :
la génération 17, les versions 0.1.1-dev.1 / 0.1.1, le docstring de l'ère
nouvelle — LA VERSION COMMANDÉE PAR LE DÉVELOPPEUR, la dette [R10-PÉRIMÉE]
soldée à la naissance. Chaque remplacement ASSERTÉ (l'ancre doit vivre une
fois exactement)."""

CHEMIN = "/home/z/my-project/triade/loupe/carte_m10.py"

texte = open(CHEMIN, encoding="utf-8").read()
n_avant = texte.count("0.1.0-dev.8")


def remplace(ancien, nouveau, combien=1):
    global texte
    n = texte.count(ancien)
    assert n == combien, f"ancre {n}x (attendu {combien}) : {ancien[:80]!r}"
    texte = texte.replace(ancien, nouveau)


# 1. les constantes de version (les docstrings et GENERATION déjà portés par
#    le geste précédent — la table rafraîchie, la génération 17 en place)
remplace(
    'VERSION_DEV = "0.1.0-dev.8"     # la pièce vécue aux 10e/11e runs (l\'Entrée\n'
    "                                 # 217 : LE VERT TIENT ENTIER — la triple\n"
    "                                 # retouche des Entrées 209/210/214 portée\n"
    "                                 # au plan, la dette de l'Entrée 211 soldée)\n"
    'VERSION_FINALE = "0.1.0"        # la finale (le miroir layout.VERSION_FINALE\n'
    "                                # 0x00010000 — le scellage est un fait de\n"
    "                                # carte : la 0.1.0 attend le run terrain vert\n"
    "                                # recoupé M10-(e), jamais un build ici)",
    'VERSION_DEV = "0.1.1-dev.1"     # la version commandée par le développeur\n'
    "                                 # (D178/D179 — l'anti-rollback R6 s'ouvre à\n"
    "                                 # la monotonie R10 : 0.1.1-dev.1 > 0.1.0\n"
    "                                 # scellée) : la dette [R10-PÉRIMÉE] soldée\n"
    "                                 # à la naissance — la porte R10 de la pièce\n"
    "                                 # rafraîchie à la vérité des blocs, le code\n"
    "                                 # byte-identique au vécu des onze runs (R4)\n"
    'VERSION_FINALE = "0.1.1"        # la finale (le miroir layout.VERSION_FINALE\n'
    "                                # 0x00010100 — le scellage est un fait de\n"
    "                                # carte : la 0.1.1 attend le run terrain vert\n"
    "                                # recoupé DU DOUZIÈME RUN, jamais un build ici)")

open(CHEMIN, "w", encoding="utf-8").write(texte)
print(f"[carte_m10] l'ère 0.1.1 portée — {n_avant} littéraux « 0.1.0-dev.8 » "
      f"remplacés là où l'ère se déclare ; vérification :")
import subprocess
r = subprocess.run(["python3", "-c",
                    "import sys; sys.path.insert(0, '/home/z/my-project/triade/loupe'); "
                    "import carte_m10 as c; "
                    "assert c.GENERATION == 17 and c.VERSION_DEV == '0.1.1-dev.1' "
                    "and c.VERSION_FINALE == '0.1.1'; print('   GENERATION', "
                    "c.GENERATION, '| VERSION_DEV', c.VERSION_DEV, "
                    "| VERSION_FINALE', c.VERSION_FINALE)"],
                   capture_output=True, text=True)
print(r.stdout.strip() or r.stderr.strip())
assert r.returncode == 0, "la vérification d'import a échoué"
