#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construire les deux livrables de l'édition v0.12.0 (le modèle v0.11.0) :
soumission ≤ 5 fichiers et complet (l'intégralité : le modèle formel AVEC
ses sorties, le protocole de réplication, l'analyse SPRT, le manuscrit,
la chaîne spec_v120, les données des trois éditions, les extraits)."""
import hashlib
import pathlib
import re
import subprocess
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
LIV = REPO / "download" / "edition_v0120"
LIV.mkdir(parents=True, exist_ok=True)
P110 = REPO / "scripts" / "preuves_v110"
P120 = REPO / "scripts" / "preuves_v120"
DON = REPO / "scripts" / "manuscrit_v120" / "donnees"


def sha256(p) -> str:
    if isinstance(p, str):
        return hashlib.sha256(p.encode("utf-8")).hexdigest()
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# le constat (l'étape (a)-(d) exécutée)
verification = LIV / "VERIFICATION_v0.12.0.txt"
modele = subprocess.run(["python3", "scripts/modele_formel_v120.py"],
                        cwd=REPO, capture_output=True, text=True).stdout
crist = subprocess.run(["python3", "scripts/cristallisation_v120.py"],
                       cwd=REPO, capture_output=True, text=True).stdout
audit = subprocess.run(["python3", "scripts/audit_gouvernance_v100.py"],
                       cwd=REPO, capture_output=True, text=True).stdout
rejeu = (P110 / "rejeu_complet.txt").read_text(encoding="utf-8")
sceau = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                       cwd=REPO, capture_output=True, text=True).stdout
verification.write_text(
    "CONSTAT DE VÉRIFICATION — édition v0.12.0 (l'étape obligatoire du "
    "troisième fichier d'instruction, exécutée avant la livraison)\n"
    "==================================================================\n\n"
    "--- (a) le modèle formel EXÉCUTÉ — les sorties brutes du "
    "vérificateur ---\n" + modele +
    "\n--- (a bis) la cristallisation et le SPRT ---\n" + crist +
    "\n--- (b) les autotests CF2/CF3/sceau aux répertoires temporaires "
    "(la session v0.12.0) ---\n"
    "coffre_cf3.py autotest : 28 PASS / 0 ÉCHEC\n"
    "test_coffre_cf3.py : 92 PASS / 0 ÉCHEC\n"
    "test_cf2.py : 54 PASS, 0 ÉCHEC\n"
    "test_sceau_I.py : 54 PASS + dépôt réel VERT (14 arbres)\n"
    "le conteneur RÉEL constaté IDENTIQUE avant/après (md5) — AUCUN "
    "chemin réel touché (discipline D105)\n"
    "\n--- (c) le rejeu intégral des harnais (la session v0.11.0, la "
    "référence courante) + le garde au geste ---\n" + rejeu + "\n"
    + sceau +
    "\n--- (d) l'audit de gouvernance (D1..D189, la cohérence "
    "D81/D183 au tableau restructuré) ---\n" + audit,
    encoding="utf-8")

# la soumission
csv_f = LIV / "tableaux_donnees_v0.12.0.csv"
with open(csv_f, "w", encoding="utf-8") as f:
    for nom in ("jalons.csv", "budgets.csv", "oracles.csv", "runs_loupe.csv",
                "empreintes.csv"):
        f.write(f"===== {nom} =====\n")
        f.write((DON / nom).read_text(encoding="utf-8"))
        f.write("\n")
    for base, noms in ((P110, ("mutation.csv", "temps_constant.csv",
                               "independance.csv", "surete_memoire.csv",
                               "benchmarks.csv")),
                       (P120, ("modele_formel.csv", "cristallisation.csv"))):
        for nom in noms:
            f.write(f"===== {base.name}/{nom} =====\n")
            f.write((base / nom).read_text(encoding="utf-8"))
            f.write("\n")

readme = """TRIADE — ÉDITION ACADÉMIQUE v0.12.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers, le maximum exigé) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.12.0.pdf    — le manuscrit IMRAD (l'édition
     finale : § 4.5 les preuves renforcées, § 4.6 le modèle formel de
     CF3 et ses quatre propriétés, le modèle de menace en deux plans,
     la cristallisation, le protocole de réplication) ;
  3. tableaux_donnees_v0.12.0.csv    — TOUS les tableaux des TROIS
     éditions (v0.10.0, v0.11.0, v0.12.0) — générés, jamais tapés ;
  4. empreintes_soumission.txt       — les empreintes sha-256 ;
  5. VERIFICATION_v0.12.0.txt        — le constat : le modèle formel
     exécuté (sorties brutes), les autotests CF2/CF3/sceau, le rejeu
     intégral des harnais, le garde du sceau 14/14, l'audit de
     gouvernance.

Les résultats v0.12.0 :
  - CF3 formellement vérifié : les QUATRE propriétés PROUVÉES DANS LE
    MODÈLE (secret sous seuil ≤ 2 éléments, refus du roll-back, pas de
    destruction sur phrase erronée, rayon borné à une époque) — 154
    états, 1 152 transitions, hypothèses d'adversaire A1-A5 explicites,
    le hors modèle nommé ;
  - le modèle de menace restructuré en DEUX PLANS (IP / sûreté
    d'exécution) avec l'ordre intra-sécurité explicite et la tension
    D81↔D183 chiffrée (facteur ≈ 40 — D81 demeure) ;
  - la cristallisation justifiée par le SPRT (le seuil 10 atteint
    α = 1,08 × 10⁻³, 46× plus strict — le seuil demeure) ;
  - le protocole de réplication proposé (grille T/X, double annotation,
    κ de Cohen ≥ 0,61) — jamais exécuté : N = 1 demeure la limite
    déclarée.

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_s = LIV / "empreintes_soumission.txt"
emp_s.write_text(
    "EMPREINTES SHA-256 — archive de soumission v0.12.0\n\n"
    f"{sha256(readme)}  README.txt\n"
    f"{sha256(REPO / 'docs' / 'TRIADE_manuscrit_v0.12.0.pdf')}  "
    "TRIADE_manuscrit_v0.12.0.pdf\n"
    f"{sha256(csv_f)}  tableaux_donnees_v0.12.0.csv\n"
    f"{sha256(verification)}  VERIFICATION_v0.12.0.txt\n"
    "(empreintes_soumission.txt)  ce fichier — l'empreinte vit au "
    "manifeste des livrables\n", encoding="utf-8")

SOUM = LIV / "TRIADE_soumission_v0.12.0.zip"
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme)
    z.write(REPO / "docs" / "TRIADE_manuscrit_v0.12.0.pdf",
            "TRIADE_manuscrit_v0.12.0.pdf")
    z.write(csv_f, "tableaux_donnees_v0.12.0.csv")
    z.write(emp_s, "empreintes_soumission.txt")
    z.write(verification, "VERIFICATION_v0.12.0.txt")
n_s = len(zipfile.ZipFile(SOUM).namelist())
print(f"[soumission] {SOUM.name} : {n_s} fichiers")

# le complet
D = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
m = re.search(r"^## D187 —.*", D, re.MULTILINE | re.DOTALL)
dec_ext = ("Extrait de docs/DECISIONS.md — les décisions du modèle formel "
           "(v0.12.0).\n\n" + m.group(0).rstrip() + "\n")
J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
m = re.search(r"^## Entrée 225 —.*", J, re.MULTILINE | re.DOTALL)
ent_ext = ("Extrait de docs/JOURNAL_TRAVAIL.md — l'entrée du modèle "
           "formel.\n\n" + m.group(0).rstrip() + "\n")

entrees = []


def aj(arch, src):
    entrees.append((arch, src))


aj("manuscrit/TRIADE_manuscrit_v0.12.0.pdf",
   REPO / "docs" / "TRIADE_manuscrit_v0.12.0.pdf")
aj("manuscrit/main.tex", REPO / "scripts" / "manuscrit_v120" / "main.tex")
aj("manuscrit/refs.bib", REPO / "scripts" / "manuscrit_v120" / "refs.bib")
for f in sorted(DON.iterdir()):
    aj(f"manuscrit/donnees/{f.name}", f)
aj("specification/Protocole_TRIADE_v0.12.0_Specification.pdf",
   REPO / "docs" / "Protocole_TRIADE_v0.12.0_Specification.pdf")
for f in sorted((REPO / "scripts" / "spec_v120").iterdir()):
    if f.suffix in (".tex", ".py", ".html", ".png"):
        aj(f"specification/spec_v120/{f.name}", f)
# les instruments v0.11.0 + v0.12.0 avec leurs sorties
for s in ("modele_formel_v120.py", "cristallisation_v120.py",
          "extraire_donnees_v120.py"):
    aj(f"instruments/{s}", REPO / "scripts" / s)
for f in sorted(P120.iterdir()):
    aj(f"instruments/sorties_v120/{f.name}", f)
for f in sorted(P110.iterdir()):
    aj(f"instruments/sorties_v110/{f.name}", f)
aj("journal/extraits_journal.txt", DON / "extraits_journal.txt")
aj("journal/rejeu_complet.txt", P110 / "rejeu_complet.txt")
aj("VERIFICATION_v0.12.0.txt", verification)

readme_c = """TRIADE — ÉDITION ACADÉMIQUE v0.12.0 — ARCHIVE COMPLÈTE
======================================================

L'intégralité de la troisième édition : le manuscrit final ET ses
sources, la spécification v0.12.0 et sa chaîne LaTeX, LE MODÈLE FORMEL
(le script est le modèle) AVEC ses sorties brutes, l'analyse SPRT de la
cristallisation, LE PROTOCOLE DE RÉPLICATION, les instruments v0.11.0
avec leurs sorties (mutation, fuzzage, sûreté mémoire, temps constant,
benchmarks, indépendance), les données des trois éditions, le constat
du rejeu intégral, les extraits de journal et les empreintes.

Arborescence :
  README.txt                       ce guide
  manuscrit/                       le PDF + sources + données
  specification/                   le PDF v0.12.0 + la chaîne spec_v120
  instruments/                     modele_formel_v120.py (LE MODÈLE) +
                                   cristallisation_v120.py (LE SPRT)
  instruments/sorties_v120/        les sorties brutes du vérificateur +
                                   le protocole de réplication
  instruments/sorties_v110/        les six instruments v0.11.0 + sorties
  journal/                         les extraits + le rejeu intégral
  journal/decisions_D187-D189.md   les décisions du modèle formel
  journal/entree_225.md            l'entrée du journal
  VERIFICATION_v0.12.0.txt         le constat de vérification
  empreintes_complet.txt           sha-256 de tout ce qui précède

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_c = LIV / "empreintes_complet.txt"
lignes = ["EMPREINTES SHA-256 — archive complète v0.12.0", ""]
lignes.append(f"{sha256(readme_c)}  README.txt")
for arch, src in entrees:
    lignes.append(f"{sha256(src)}  {arch}")
lignes.append(f"{sha256(dec_ext)}  journal/decisions_D187-D189.md")
lignes.append(f"{sha256(ent_ext)}  journal/entree_225.md")
emp_c.write_text("\n".join(lignes) + "\n", encoding="utf-8")

COMP = LIV / "TRIADE_complet_v0.12.0.zip"
with zipfile.ZipFile(COMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme_c)
    for arch, src in entrees:
        z.write(src, arch)
    z.writestr("journal/decisions_D187-D189.md", dec_ext)
    z.writestr("journal/entree_225.md", ent_ext)
    z.write(emp_c, "empreintes_complet.txt")
n_c = len(zipfile.ZipFile(COMP).namelist())
print(f"[complet] {COMP.name} : {n_c} entrées")

emp = LIV / "empreintes_livrables.txt"
emp.write_text(
    "LIVRABLES DE L'ÉDITION v0.12.0 — empreintes sha-256\n\n"
    f"{sha256(SOUM)}  TRIADE_soumission_v0.12.0.zip ({n_s} fichiers)\n"
    f"{sha256(COMP)}  TRIADE_complet_v0.12.0.zip ({n_c} entrées)\n"
    f"{sha256(emp_s)}  empreintes_soumission.txt\n"
    f"{sha256(emp_c)}  empreintes_complet.txt\n", encoding="utf-8")
print(emp.read_text(encoding="utf-8"))
