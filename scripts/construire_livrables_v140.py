#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_livrables_v140.py — les deux livrables v0.14.0 (le modèle
v130) : soumission ≤ 5 fichiers + complet (les SIX preuves du programme
empirique AVEC leurs sorties brutes, le kit terrain, les cinq ères)."""
import hashlib, pathlib, re, zipfile
REPO = pathlib.Path("/home/z/my-project/triade")
LIV = REPO / "download" / "edition_v0140"; LIV.mkdir(parents=True, exist_ok=True)
P110 = REPO / "scripts" / "preuves_v110"; P130 = REPO / "scripts" / "preuves_v130"
P140 = REPO / "scripts" / "preuves_v140"
DON = REPO / "scripts" / "manuscrit_v140" / "donnees"

def sha256(p):
    if isinstance(p, str):
        return hashlib.sha256(p.encode()).hexdigest()
    return hashlib.sha256(p.read_bytes()).hexdigest()

# la soumission : le manuscrit + les tableaux fusionnés + empreintes + le constat
csv_f = LIV / "tableaux_donnees_v0.14.0.csv"
with open(csv_f, "w", encoding="utf-8") as f:
    for nom in ("jalons.csv", "budgets.csv", "oracles.csv", "runs_loupe.csv",
                "empreintes.csv"):
        f.write(f"===== {nom} =====\n"); f.write((DON / nom).read_text(encoding="utf-8")); f.write("\n")
    for base, noms in ((P110, ("mutation.csv", "benchmarks.csv")),
                       (P130, ("audit_benchmark.csv", "stats_v130.csv")),
                       (P140, ("bras_c.csv", "remesure_rq2.csv",
                               "independance_agent.csv", "rejeu_survivants.csv"))):
        for nom in noms:
            f.write(f"===== {base.name}/{nom} =====\n")
            f.write((base / nom).read_text(encoding="utf-8")); f.write("\n")
readme = """TRIADE — ÉDITION ACADÉMIQUE v0.14.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.14.0.pdf    — le manuscrit : la comparaison
     contrôlée au compilateur (pré-enregistrée : zéro divergence, sha-256
     paritaire à travail égal, la notation testable au même degré), RQ2
     re-mesurée en distributions (580/2 143/3 510 contre la baseline
     naive 300 304 — lecture défavorable consignée), l'indépendance par
     instance isolée (128 constantes, zéro divergence), le re-jeu des
     832 mutants aux composition-killers (93,3 %, tls13/sys à 100 %) ;
  3. tableaux_donnees_v0.14.0.csv    — les tableaux des CINQ ères ;
  4. empreintes_soumission.txt       — les empreintes sha-256 ;
  5. VERIFICATION_v0.14.0.txt        — le constat de vérification.

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""
constat = LIV / "VERIFICATION_v0.14.0.txt"
constat.write_text("CONSTAT DE VÉRIFICATION — v0.14.0\n"
                   "==================================\n\n"
                   "Le manuscrit : 17 pages, zéro placeholder, zéro\n"
                   "débordement de marge, l'exposant 10^6 confirmé rendu,\n"
                   "les 12 valeurs-clés présentes, les macros résolues.\n\n"
                   "--- le plan pré-enregistré (CA5, l'empreinte D193) ---\n"
                   + (P140 / "PLAN_PREENREGISTRE_v140.md").read_text(encoding="utf-8")
                   + "\n\n--- le re-jeu des 832 mutants ---\n"
                   + (P140 / "rejeu_survivants_rapport.txt").read_text(encoding="utf-8")
                   + "\n\n--- le bras de référence ---\n"
                   + (P140 / "bras_c_rapport.txt").read_text(encoding="utf-8")
                   + "\n\n--- la re-mesure RQ2 ---\n"
                   + (P140 / "remesure_rq2_rapport.txt").read_text(encoding="utf-8")
                   + "\n\n--- l'indépendance ---\n"
                   + (P140 / "independance_agent_rapport.txt").read_text(encoding="utf-8"),
                   encoding="utf-8")
emp_s = LIV / "empreintes_soumission.txt"
emp_s.write_text("EMPREINTES SHA-256 — soumission v0.14.0\n\n"
                 f"{sha256(readme)}  README.txt\n"
                 f"{sha256(REPO / 'docs' / 'TRIADE_manuscrit_v0.14.0.pdf')}  manuscrit\n"
                 f"{sha256(csv_f)}  tableaux\n"
                 f"{sha256(constat)}  VERIFICATION\n", encoding="utf-8")
SOUM = LIV / "TRIADE_soumission_v0.14.0.zip"
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme)
    z.write(REPO / "docs" / "TRIADE_manuscrit_v0.14.0.pdf",
            "TRIADE_manuscrit_v0.14.0.pdf")
    z.write(csv_f, "tableaux_donnees_v0.14.0.csv")
    z.write(emp_s, "empreintes_soumission.txt")
    z.write(constat, "VERIFICATION_v0.14.0.txt")
n_s = len(zipfile.ZipFile(SOUM).namelist())

# le complet
E = []
def aj(a, s): E.append((a, s))
aj("manuscrit/TRIADE_manuscrit_v0.14.0.pdf", REPO / "docs" / "TRIADE_manuscrit_v0.14.0.pdf")
aj("manuscrit/main.tex", REPO / "scripts" / "manuscrit_v140" / "main.tex")
aj("manuscrit/refs.bib", REPO / "scripts" / "manuscrit_v140" / "refs.bib")
for f in sorted(DON.iterdir()): aj(f"manuscrit/donnees/{f.name}", f)
aj("specification/Protocole_TRIADE_v0.14.0_Specification.pdf",
   REPO / "docs" / "Protocole_TRIADE_v0.14.0_Specification.pdf")
for f in sorted((REPO / "scripts" / "spec_v140").iterdir()):
    if f.suffix in (".tex", ".py", ".html", ".png"):
        aj(f"specification/spec_v140/{f.name}", f)
for s in ("comparer_v140.py", "remesure_rq2_v140.py", "independance_v140.py",
          "rejeu_survivants_v140.py", "extraire_donnees_v140.py",
          "consigner_d193_preregistre.py"):
    aj(f"instruments/{s}", REPO / "scripts" / "bras_c_v140" / s
       if "comparer" in s else REPO / "scripts" / s)
aj("instruments/bras_c.c", REPO / "scripts" / "bras_c_v140" / "bras_c.c")
for f in sorted(P140.iterdir()): aj(f"instruments/sorties_v140/{f.name}", f)
for f in sorted(P130.iterdir()): aj(f"instruments/sorties_v130/{f.name}", f)
for f in sorted(P110.iterdir()): aj(f"instruments/sorties_v110/{f.name}", f)
for f in sorted((REPO / "scripts" / "kit_terrain_bras_c").iterdir()):
    aj(f"kit_terrain/{f.name}", f)
aj("journal/extraits_journal.txt", DON / "extraits_journal.txt")
aj("journal/rejeu_complet.txt", P110 / "rejeu_complet.txt")
aj("VERIFICATION_v0.14.0.txt", constat)
J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
m = re.search(r"^## Entrée 228 —.*", J, re.M | re.S)
D = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
m2 = re.search(r"^## D195 —.*?(?=^## D19[0-9]{2}|\Z)", D, re.M | re.S)
readme_c = """TRIADE — ÉDITION ACADÉMIQUE v0.14.0 — ARCHIVE COMPLÈTE
======================================================

L'intégralité : le manuscrit ET ses sources, la spécification v0.14.0,
LES SIX PREUVES du programme empirique avec leurs sorties brutes (le
plan pré-enregistré, le bras de référence, la re-mesure RQ2,
l'indépendance, le re-jeu des 832), le kit terrain EN ATTENTE, les
données des cinq ères, les extraits, les empreintes.

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""
emp_c = LIV / "empreintes_complet.txt"
lignes = ["EMPREINTES SHA-256 — complet v0.14.0", "",
          f"{sha256(readme_c)}  README.txt"]
for a, src in E: lignes.append(f"{sha256(src)}  {a}")
lignes.append(f"{sha256(m.group(0))}  journal/entree_228.md")
lignes.append(f"{sha256(m2.group(0))}  journal/decision_D195.md")
emp_c.write_text("\n".join(lignes) + "\n", encoding="utf-8")
COMP = LIV / "TRIADE_complet_v0.14.0.zip"
with zipfile.ZipFile(COMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme_c)
    for a, src in E: z.write(src, a)
    z.writestr("journal/entree_228.md", m.group(0))
    z.writestr("journal/decision_D195.md", m2.group(0))
    z.write(emp_c, "empreintes_complet.txt")
n_c = len(zipfile.ZipFile(COMP).namelist())
emp = LIV / "empreintes_livrables.txt"
emp.write_text(f"LIVRABLES v0.14.0\n\n{sha256(SOUM)}  soumission ({n_s} fichiers)\n"
               f"{sha256(COMP)}  complet ({n_c} entrées)\n", encoding="utf-8")
print(f"[soumission] {n_s} fichiers · [complet] {n_c} entrées")
print(emp.read_text(encoding="utf-8"))
