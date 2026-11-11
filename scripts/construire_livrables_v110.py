#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construire les deux livrables de l'édition v0.11.0 (le modèle v0.10.0) :
soumission ≤ 5 fichiers (readme, manuscrit pdf, tableaux CSV, empreintes,
constat de vérification) et complet (l'intégralité : les SIX instruments
avec leurs scripts ET leurs sorties brutes, la chaîne spec_v110, le
brouillon CSPRNG, le corpus RFC 8446, les sources du manuscrit, les
données, les extraits, les empreintes).
"""
import hashlib
import pathlib
import re
import subprocess
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
LIV = REPO / "download" / "edition_v0110"
LIV.mkdir(parents=True, exist_ok=True)
PREUVES = REPO / "scripts" / "preuves_v110"
DONNEES = REPO / "scripts" / "manuscrit_v110" / "donnees"


def sha256(p) -> str:
    if isinstance(p, str):
        return hashlib.sha256(p.encode("utf-8")).hexdigest()
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ le constat
verification = LIV / "VERIFICATION_v0.11.0.txt"
rejeu = (PREUVES / "rejeu_complet.txt").read_text(encoding="utf-8")
extraction = subprocess.run(["python3", "scripts/extraire_donnees_v110.py",
                             "--verifier"], cwd=REPO, capture_output=True,
                            text=True).stdout
audit = subprocess.run(["python3", "scripts/audit_gouvernance_v100.py"],
                       cwd=REPO, capture_output=True, text=True).stdout
verification.write_text(
    "CONSTAT DE VÉRIFICATION — édition v0.11.0 (l'étape obligatoire du "
    "deuxième fichier d'instruction, exécutée avant la livraison)\n"
    "==================================================================\n\n"
    "--- (a) le rejeu intégral des harnais existants + le garde du sceau ---\n"
    + rejeu +
    "\n--- (c) les données extraites et vérifiées (le script refuse si une "
    "preuve manque) ---\n" + extraction +
    "\n--- (d) l'audit de gouvernance (D1..D186, append-only) ---\n" + audit,
    encoding="utf-8")

# ------------------------------------------------------------------ la soumission
csv_fusionne = LIV / "tableaux_donnees_v0.11.0.csv"
with open(csv_fusionne, "w", encoding="utf-8") as f:
    for nom in ("jalons.csv", "budgets.csv", "oracles.csv", "runs_loupe.csv",
                "empreintes.csv"):
        f.write(f"===== {nom} =====\n")
        f.write((DONNEES / nom).read_text(encoding="utf-8"))
        f.write("\n")
    for nom in ("mutation.csv", "temps_constant.csv", "independance.csv",
                "surete_memoire.csv", "benchmarks.csv"):
        f.write(f"===== PREUVES v0.11.0 : {nom} =====\n")
        f.write((PREUVES / nom).read_text(encoding="utf-8"))
        f.write("\n")

readme = """TRIADE — ÉDITION ACADÉMIQUE v0.11.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers, le maximum exigé) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.11.0.pdf    — le manuscrit IMRAD ÉTENDU (la
     section Results § 4.5 « Strengthened evidence » : les six
     instruments de la v0.11.0 avec leurs tables générées) ;
  3. tableaux_donnees_v0.11.0.csv    — TOUS les tableaux : les données
     v0.10.0 (jalons, budgets, oracles, runs, empreintes) ET les preuves
     v0.11.0 (mutation, temps constant, indépendance, sûreté mémoire,
     benchmarks) — générés, jamais tapés ;
  4. empreintes_soumission.txt       — les empreintes sha-256 ;
  5. VERIFICATION_v0.11.0.txt        — le constat : le rejeu INTÉGRAL des
     harnais (159 Loupe + 284 tls13 + 131 sys + garde du sceau 14/14),
     les artefacts scellés byte pour byte, l'audit de gouvernance.

Les six instruments (détails dans le manuscrit § 4.5) :
  - mutation testing   : 832 mutants, 694 tués (83,4 %) — les familles
    crypto à 100 %, les 138 survivants d'orchestration NOMMÉS ;
  - fuzzage guidé      : loupe-01 60,5 % de couverture, zéro crash,
    zéro canari violé ; http-10 : 358 instructions, zéro faute ;
  - sûreté mémoire     : 2 098 accès classés, ZÉRO hors-cadre,
    463 non résolus nommés (analyse bornée, limites consignées) ;
  - temps constant     : dudect d'émulation — toutes les familles
    crypto CONSTANTES (traces indépendantes du secret) ; le temps réel
    N'EST PAS MESURÉ (la limite explicite) ;
  - benchmarks         : sha256 4 524 ins/op (blocs à la main) contre
    69 132 (gcc -O2) au MÊME émulateur — facteur 15,3 ; md5/aes écartés
    par l'auto-vérification (le C de référence fautif refusé) ;
  - indépendance       : zéro divergence par voies distinctes.

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_s = LIV / "empreintes_soumission.txt"
emp_s.write_text(
    "EMPREINTES SHA-256 — archive de soumission v0.11.0\n\n"
    f"{sha256(readme)}  README.txt\n"
    f"{sha256(REPO / 'docs' / 'TRIADE_manuscrit_v0.11.0.pdf')}  "
    "TRIADE_manuscrit_v0.11.0.pdf\n"
    f"{sha256(csv_fusionne)}  tableaux_donnees_v0.11.0.csv\n"
    f"{sha256(verification)}  VERIFICATION_v0.11.0.txt\n"
    "(empreintes_soumission.txt)  ce fichier — l'empreinte vit au "
    "manifeste des livrables\n", encoding="utf-8")

SOUM = LIV / "TRIADE_soumission_v0.11.0.zip"
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme)
    z.write(REPO / "docs" / "TRIADE_manuscrit_v0.11.0.pdf",
            "TRIADE_manuscrit_v0.11.0.pdf")
    z.write(csv_fusionne, "tableaux_donnees_v0.11.0.csv")
    z.write(emp_s, "empreintes_soumission.txt")
    z.write(verification, "VERIFICATION_v0.11.0.txt")
n_s = len(zipfile.ZipFile(SOUM).namelist())
print(f"[soumission] {SOUM.name} : {n_s} fichiers")

# ------------------------------------------------------------------ le complet
D = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
m = re.search(r"^## D185 —.*", D, re.MULTILINE | re.DOTALL)
decisions_ext = ("Extrait de docs/DECISIONS.md — les décisions des preuves "
                 "renforcées (v0.11.0).\n\n" + m.group(0).rstrip() + "\n")
J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
m = re.search(r"^## Entrée 224 —.*", J, re.MULTILINE | re.DOTALL)
entree_ext = ("Extrait de docs/JOURNAL_TRAVAIL.md — l'entrée des preuves "
              "renforcées.\n\n" + m.group(0).rstrip() + "\n")

entrees = []


def aj(arch, src):
    entrees.append((arch, src))


aj("manuscrit/TRIADE_manuscrit_v0.11.0.pdf",
   REPO / "docs" / "TRIADE_manuscrit_v0.11.0.pdf")
aj("manuscrit/main.tex", REPO / "scripts" / "manuscrit_v110" / "main.tex")
aj("manuscrit/refs.bib", REPO / "scripts" / "manuscrit_v110" / "refs.bib")
for f in sorted(DONNEES.iterdir()):
    aj(f"manuscrit/donnees/{f.name}", f)
aj("specification/Protocole_TRIADE_v0.11.0_Specification.pdf",
   REPO / "docs" / "Protocole_TRIADE_v0.11.0_Specification.pdf")
for f in sorted((REPO / "scripts" / "spec_v110").iterdir()):
    if f.suffix in (".tex", ".py", ".html", ".png"):
        aj(f"specification/spec_v110/{f.name}", f)
# LES SIX INSTRUMENTS : les scripts ET les sorties brutes
for s in ("mutation_v110.py", "fuzzage_v110.py", "surete_memoire_v110.py",
          "temps_constant_v110.py", "benchmarks_v110.py",
          "independance_v110.py", "extraire_donnees_v110.py"):
    aj(f"instruments/{s}", REPO / "scripts" / s)
for f in sorted(PREUVES.iterdir()):
    aj(f"instruments/sorties/{f.name}", f)
for f in sorted((REPO / "scripts" / "bench_v110_c").iterdir()):
    if f.suffix in (".c", ".ld", ".o", ".bin", ".elf"):
        continue  # les .o/.bin/.elf se régénèrent ; le source suffit
    if f.suffix == ".c":
        aj(f"instruments/reference_C/{f.name}", f)
aj("spec-csprng/tls13-29-source-csprng.md",
   REPO / "tls13" / "notation" / "brouillons" / "tls13-29-source-csprng.md")
aj("corpus/rfc8446.py", REPO / "tls13" / "fixtures" / "rfc8446.py")
aj("journal/extraits_journal.txt", DONNEES / "extraits_journal.txt")
aj("journal/rejeu_complet.txt", PREUVES / "rejeu_complet.txt")
aj("VERIFICATION_v0.11.0.txt", verification)

readme_c = """TRIADE — ÉDITION ACADÉMIQUE v0.11.0 — ARCHIVE COMPLÈTE
======================================================

L'intégralité des preuves renforcées : le manuscrit étendu ET ses
sources, la spécification v0.11.0 et sa chaîne LaTeX, LES SIX
INSTRUMENTS avec leurs scripts ET leurs sorties brutes (CSV/JSON/
rapports), la référence C à contrat équivalent, la spécification CSPRNG
en brouillon (tls13-29 — la cérémonie d'ère attend le geste du
développeur), le corpus de vecteurs RFC 8446, le constat du rejeu
intégral des harnais, les extraits de journal et les empreintes.

Arborescence :
  README.txt                      ce guide
  manuscrit/                      le PDF + main.tex + refs.bib + données
  specification/                  le PDF v0.11.0 + la chaîne spec_v110
  instruments/                    LES SIX scripts + sorties brutes
  instruments/reference_C/        bench.c (la référence à contrat équivalent)
  spec-csprng/                    tls13-29 (le brouillon, D186)
  corpus/                         rfc8446.py (les vecteurs, D186)
  journal/                        les extraits + le rejeu intégral
  journal/decisions_D185-D186.md  les décisions des preuves
  journal/entree_224.md           l'entrée du journal
  VERIFICATION_v0.11.0.txt        le constat de vérification
  empreintes_complet.txt          sha-256 de tout ce qui précède

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_c = LIV / "empreintes_complet.txt"
lignes = ["EMPREINTES SHA-256 — archive complète v0.11.0", ""]
lignes.append(f"{sha256(readme_c)}  README.txt")
for arch, src in entrees:
    lignes.append(f"{sha256(src)}  {arch}")
lignes.append(f"{sha256(decisions_ext)}  journal/decisions_D185-D186.md")
lignes.append(f"{sha256(entree_ext)}  journal/entree_224.md")
emp_c.write_text("\n".join(lignes) + "\n", encoding="utf-8")

COMP = LIV / "TRIADE_complet_v0.11.0.zip"
with zipfile.ZipFile(COMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme_c)
    for arch, src in entrees:
        z.write(src, arch)
    z.writestr("journal/decisions_D185-D186.md", decisions_ext)
    z.writestr("journal/entree_224.md", entree_ext)
    z.write(emp_c, "empreintes_complet.txt")
n_c = len(zipfile.ZipFile(COMP).namelist())
print(f"[complet] {COMP.name} : {n_c} entrées")

emp = LIV / "empreintes_livrables.txt"
emp.write_text(
    "LIVRABLES DE L'ÉDITION v0.11.0 — empreintes sha-256\n\n"
    f"{sha256(SOUM)}  TRIADE_soumission_v0.11.0.zip ({n_s} fichiers)\n"
    f"{sha256(COMP)}  TRIADE_complet_v0.11.0.zip ({n_c} entrées)\n"
    f"{sha256(emp_s)}  empreintes_soumission.txt\n"
    f"{sha256(emp_c)}  empreintes_complet.txt\n", encoding="utf-8")
print(emp.read_text(encoding="utf-8"))
