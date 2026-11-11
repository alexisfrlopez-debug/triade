#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construire les deux livrables de l'édition v0.13.0 (le modèle v0.12.0) :
soumission ≤ 5 fichiers et complet (l'intégralité : les corrections AVEC
leurs preuves — l'audit du benchmark, les statistiques corrigées, le rapport
de conformité ligne par ligne, le kit D183 —, le manuscrit, la chaîne
spec_v130, les données des quatre éditions, les extraits)."""
import hashlib
import pathlib
import re
import subprocess
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
LIV = REPO / "download" / "edition_v0130"
LIV.mkdir(parents=True, exist_ok=True)
P110 = REPO / "scripts" / "preuves_v110"
P120 = REPO / "scripts" / "preuves_v120"
P130 = REPO / "scripts" / "preuves_v130"
DON = REPO / "scripts" / "manuscrit_v130" / "donnees"
KIT = REPO / "scripts" / "kit_ceremonie_d183"


def sha256(p) -> str:
    if isinstance(p, str):
        return hashlib.sha256(p.encode("utf-8")).hexdigest()
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# le constat : le rapport de conformité + les sorties brutes des corrections
conformite = (P130 / "rapport_conformite_v130.txt").read_text(encoding="utf-8")
audit = subprocess.run(["python3", "scripts/audit_benchmark_v130.py"],
                       cwd=REPO, capture_output=True, text=True).stdout
stats = subprocess.run(["python3", "scripts/stats_v130.py"],
                       cwd=REPO, capture_output=True, text=True).stdout
gouvernance = subprocess.run(["python3", "scripts/audit_gouvernance_v100.py"],
                             cwd=REPO, capture_output=True, text=True).stdout
sceau = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                       cwd=REPO, capture_output=True, text=True).stdout
verification = LIV / "VERIFICATION_v0.13.0.txt"
verification.write_text(
    "CONSTAT DE VÉRIFICATION — édition v0.13.0 (l'étape obligatoire du "
    "quatrième fichier d'instruction, exécutée avant la livraison)\n"
    "==================================================================\n\n"
    "--- (0) LE RAPPORT DE CONFORMITÉ — la liste du point 1 de la "
    "commande, ligne par ligne ---\n" + conformite +
    "\n--- (1) L'AUDIT DU BENCHMARK rejoué (sorties brutes) ---\n" + audit +
    "\n--- (2) LES STATISTIQUES recalculées par script ---\n" + stats +
    "\n--- (3) le garde du sceau (les arbres signés INTACTS) ---\n" + sceau +
    "\n--- (4) l'audit de gouvernance (D1..D192) ---\n" + gouvernance,
    encoding="utf-8")

# la soumission : les tableaux fusionnés des quatre éditions
csv_f = LIV / "tableaux_donnees_v0.13.0.csv"
with open(csv_f, "w", encoding="utf-8") as f:
    for nom in ("jalons.csv", "budgets.csv", "oracles.csv", "runs_loupe.csv",
                "empreintes.csv"):
        f.write(f"===== {nom} =====\n")
        f.write((DON / nom).read_text(encoding="utf-8"))
        f.write("\n")
    for base, noms in ((P110, ("mutation.csv", "temps_constant.csv",
                               "independance.csv", "surete_memoire.csv",
                               "benchmarks.csv")),
                       (P120, ("modele_formel.csv", "cristallisation.csv")),
                       (P130, ("audit_benchmark.csv", "stats_v130.csv"))):
        for nom in noms:
            f.write(f"===== {base.name}/{nom} =====\n")
            f.write((base / nom).read_text(encoding="utf-8"))
            f.write("\n")

readme = """TRIADE — ÉDITION ACADÉMIQUE v0.13.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers, le maximum exigé) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.13.0.pdf    — le manuscrit IMRAD corrigé (les
     statistiques reformulées : l'IC95 exact de 11/12 et les
     caractéristiques opérationnelles du scellement ; le benchmark AUDITÉ :
     le facteur 15,3 retiré, les chiffres corrigés 75 983 contre 69 132 /
     77 505 ; la règle de comptage opérationnelle ; la neutralité :
     l'anti-debug arbitré, le terrain M7 requalifié, la conséquence D81 au
     modèle de menace ; l'état de l'art étendu — CompCert, LLM Compiler,
     Kitsune/POLUS, SWE-agent, sim-to-real, hardware-in-the-loop) ;
  3. tableaux_donnees_v0.13.0.csv    — TOUS les tableaux des QUATRE
     éditions (v0.10.0 à v0.13.0) — générés, jamais tapés ;
  4. empreintes_soumission.txt       — les empreintes sha-256 ;
  5. VERIFICATION_v0.13.0.txt        — le constat : le rapport de
     conformité ligne par ligne (31 VERT / 0 ROUGE), l'audit du benchmark
     rejoué, les statistiques recalculées, le garde du sceau 14/14, l'audit
     de gouvernance.

Les résultats v0.13.0 (les corrections de l'édition) :
  - le facteur « 15,3× » de v0.11.0 RETIRÉ : un artefact de périmètre (le
    compteur de la finalisation seule, comparé à l'opération complète de
    la référence) — les chiffres corrigés : l'opération complète des
    blocs 75 983 instructions contre 69 132 (gcc -O2) et 77 505 (-Os) ;
    la notation WYSIWYG est COMPÉTITIVE (−9 %/+2 %), plus compacte que
    -O2, moins que -Os ;
  - la cristallisation reformulée : P(sceller|q) = (1-q)^n (3,1 %/0,098 %
    à q = 50 % — 32× plus strict ; 95,1 %/90,4 % à q = 1 %) ; les « α »
    de D189 étaient des rapports de vraisemblance mal étiquetés ;
  - l'IC95 % exact de 11/12 : [0,615 ; 0,998] (Clopper-Pearson, la
    réserve de non-indépendance des itérations séquentielles) ;
  - la neutralité : l'anti-debug léger documenté honnêtement dans les
    deux documents ; le terrain M7 requalifié (qemu TCG au noyau réel —
    fence.i non prouvé sur silicium) ; la conséquence D81 (deux éléments
    trivialement disponibles, le média piège seul rempart) ;
  - le kit de la cérémonie D183 préparé SANS l'appliquer (l'outil au
    partage CF2 D120, l'autotest VERT) — le geste au développeur.

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_s = LIV / "empreintes_soumission.txt"
emp_s.write_text(
    "EMPREINTES SHA-256 — archive de soumission v0.13.0\n\n"
    f"{sha256(readme)}  README.txt\n"
    f"{sha256(REPO / 'docs' / 'TRIADE_manuscrit_v0.13.0.pdf')}  "
    "TRIADE_manuscrit_v0.13.0.pdf\n"
    f"{sha256(csv_f)}  tableaux_donnees_v0.13.0.csv\n"
    f"{sha256(verification)}  VERIFICATION_v0.13.0.txt\n"
    "(empreintes_soumission.txt)  ce fichier — l'empreinte vit au "
    "manifeste des livrables\n", encoding="utf-8")

SOUM = LIV / "TRIADE_soumission_v0.13.0.zip"
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme)
    z.write(REPO / "docs" / "TRIADE_manuscrit_v0.13.0.pdf",
            "TRIADE_manuscrit_v0.13.0.pdf")
    z.write(csv_f, "tableaux_donnees_v0.13.0.csv")
    z.write(emp_s, "empreintes_soumission.txt")
    z.write(verification, "VERIFICATION_v0.13.0.txt")
n_s = len(zipfile.ZipFile(SOUM).namelist())
print(f"[soumission] {SOUM.name} : {n_s} fichiers")

# le complet
D = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
m = re.search(r"^## D190 —.*?(?=^## D191 —)", D, re.MULTILINE | re.DOTALL)
m2 = re.search(r"^## D191 —.*?(?=^## D192 —)", D, re.MULTILINE | re.DOTALL)
m3 = re.search(r"^## D192 —.*", D, re.MULTILINE | re.DOTALL)
dec_ext = ("Extraits de docs/DECISIONS.md — les décisions des corrections "
           "(v0.13.0).\n\n" + m.group(0).rstrip() + "\n\n"
           + m2.group(0).rstrip() + "\n\n" + m3.group(0).rstrip() + "\n")
J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
m = re.search(r"^## Entrée 226 —.*", J, re.MULTILINE | re.DOTALL)
ent_ext = ("Extrait de docs/JOURNAL_TRAVAIL.md — l'entrée des "
           "corrections.\n\n" + m.group(0).rstrip() + "\n")

entrees = []


def aj(arch, src):
    entrees.append((arch, src))


aj("manuscrit/TRIADE_manuscrit_v0.13.0.pdf",
   REPO / "docs" / "TRIADE_manuscrit_v0.13.0.pdf")
aj("manuscrit/main.tex", REPO / "scripts" / "manuscrit_v130" / "main.tex")
aj("manuscrit/refs.bib", REPO / "scripts" / "manuscrit_v130" / "refs.bib")
for f in sorted(DON.iterdir()):
    aj(f"manuscrit/donnees/{f.name}", f)
aj("specification/Protocole_TRIADE_v0.13.0_Specification.pdf",
   REPO / "docs" / "Protocole_TRIADE_v0.13.0_Specification.pdf")
for f in sorted((REPO / "scripts" / "spec_v130").iterdir()):
    if f.suffix in (".tex", ".py", ".html", ".png"):
        aj(f"specification/spec_v130/{f.name}", f)
# les instruments des corrections + les éditions précédentes avec sorties
for s in ("audit_benchmark_v130.py", "stats_v130.py",
          "extraire_donnees_v130.py", "verifier_edition_v130.py",
          "revision_v130_md.py"):
    aj(f"instruments/{s}", REPO / "scripts" / s)
aj("instruments/kit_ceremonie_d183/sequestre_d183.py", KIT / "sequestre_d183.py")
aj("instruments/kit_ceremonie_d183/LISEZMOI-ceremonie-D183.txt",
   KIT / "LISEZMOI-ceremonie-D183.txt")
aj("instruments/kit_ceremonie_d183/AUTOTEST.txt", KIT / "AUTOTEST.txt")
for f in sorted(P130.iterdir()):
    aj(f"instruments/sorties_v130/{f.name}", f)
for f in sorted(P120.iterdir()):
    aj(f"instruments/sorties_v120/{f.name}", f)
for f in sorted(P110.iterdir()):
    aj(f"instruments/sorties_v110/{f.name}", f)
aj("journal/extraits_journal.txt", DON / "extraits_journal.txt")
aj("journal/rejeu_complet.txt", P110 / "rejeu_complet.txt")
aj("VERIFICATION_v0.13.0.txt", verification)

readme_c = """TRIADE — ÉDITION ACADÉMIQUE v0.13.0 — ARCHIVE COMPLÈTE
======================================================

L'intégralité de la quatrième édition : le manuscrit corrigé ET ses
sources, la spécification v0.13.0 et sa chaîne LaTeX (l'en-tête VERSION
enfin porté v0.13.0), LES PREUVES DES CORRECTIONS (l'audit du benchmark
avec ses sorties brutes, les statistiques recalculées, le rapport de
conformité ligne par ligne), LE KIT DE LA CÉRÉMONIE D183 (l'outil au
partage CF2, l'autotest VERT, le LISEZMOI — préparé, jamais appliqué),
les instruments des éditions v0.11.0/v0.12.0 avec leurs sorties, les
données des quatre éditions, les extraits de journal et les empreintes.

Arborescence :
  README.txt                       ce guide
  manuscrit/                       le PDF + sources + données (macros exactes)
  specification/                   le PDF v0.13.0 + la chaîne spec_v130
  instruments/                     audit_benchmark_v130.py (L'AUDIT),
                                   stats_v130.py (LES STATISTIQUES),
                                   extraire_donnees_v130.py (LE GÉNÉRATEUR
                                   anti-troncature), verifier_edition_v130.py
  instruments/kit_ceremonie_d183/  LE KIT D183 (outil + LISEZMOI + autotest)
  instruments/sorties_v130/        l'audit, les stats, le rapport de conformité
  instruments/sorties_v120/        le modèle formel + le SPRT (v0.12.0)
  instruments/sorties_v110/        les six instruments v0.11.0 + sorties
  journal/                         les extraits + le rejeu intégral
  journal/decisions_D190-D192.md   les décisions des corrections
  journal/entree_226.md            l'entrée du journal
  VERIFICATION_v0.13.0.txt         le constat de vérification
  empreintes_complet.txt           sha-256 de tout ce qui précède

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_c = LIV / "empreintes_complet.txt"
lignes = ["EMPREINTES SHA-256 — archive complète v0.13.0", ""]
lignes.append(f"{sha256(readme_c)}  README.txt")
for arch, src in entrees:
    lignes.append(f"{sha256(src)}  {arch}")
lignes.append(f"{sha256(dec_ext)}  journal/decisions_D190-D192.md")
lignes.append(f"{sha256(ent_ext)}  journal/entree_226.md")
emp_c.write_text("\n".join(lignes) + "\n", encoding="utf-8")

COMP = LIV / "TRIADE_complet_v0.13.0.zip"
with zipfile.ZipFile(COMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme_c)
    for arch, src in entrees:
        z.write(src, arch)
    z.writestr("journal/decisions_D190-D192.md", dec_ext)
    z.writestr("journal/entree_226.md", ent_ext)
    z.write(emp_c, "empreintes_complet.txt")
n_c = len(zipfile.ZipFile(COMP).namelist())
print(f"[complet] {COMP.name} : {n_c} entrées")

emp = LIV / "empreintes_livrables.txt"
emp.write_text(
    "LIVRABLES DE L'ÉDITION v0.13.0 — empreintes sha-256\n\n"
    f"{sha256(SOUM)}  TRIADE_soumission_v0.13.0.zip ({n_s} fichiers)\n"
    f"{sha256(COMP)}  TRIADE_complet_v0.13.0.zip ({n_c} entrées)\n"
    f"{sha256(emp_s)}  empreintes_soumission.txt\n"
    f"{sha256(emp_c)}  empreintes_complet.txt\n", encoding="utf-8")
print(emp.read_text(encoding="utf-8"))
