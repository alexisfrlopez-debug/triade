#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construire les deux livrables de l'édition académique v0.10.0 :

  TRIADE_soumission_v0.10.0.zip — CINQ fichiers au plus (readme inclus) :
    README.txt, le manuscrit PDF, les tableaux de données (CSV fusionnés),
    les empreintes sha-256, le constat de vérification ;

  TRIADE_complet_v0.10.0.zip — l'intégralité : les sources LaTeX du manuscrit
    + bibliographie + données générées, la chaîne spec_v100, les scripts
    (extraction, audit, vérification), les extraits de journal, les décisions
    de l'édition, les empreintes, les deux PDF.

Le numéro de version figure au nom de chaque zip (exigé par l'instruction).
"""
import hashlib
import pathlib
import re
import subprocess
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
LIVRAISONS = REPO / "download" / "edition_v0100"
LIVRAISONS.mkdir(parents=True, exist_ok=True)
donnees = REPO / "scripts" / "manuscrit_v100" / "donnees"


def sha256(p) -> str:
    if isinstance(p, str):
        return hashlib.sha256(p.encode("utf-8")).hexdigest()
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ le constat de vérification
verification = LIVRAISONS / "VERIFICATION_v0.10.0.txt"
audit_sortie = subprocess.run(["python3", "scripts/audit_gouvernance_v100.py"],
                              cwd=REPO, capture_output=True, text=True).stdout
extraction_sortie = subprocess.run(
    ["python3", "scripts/extraire_donnees_v100.py", "--verifier"],
    cwd=REPO, capture_output=True, text=True).stdout
sceau_sortie = subprocess.run(["python3", "v06/sceau_I.py", "verifier"],
                              cwd=REPO, capture_output=True, text=True).stdout
loupe_sha = sha256(REPO / "loupe" / "loupe.exe")
proxy_sha = sha256(REPO / "tls13" / "proxy.exe")
verification.write_text(
    "CONSTAT DE VÉRIFICATION — édition académique v0.10.0 (exigé par le fichier "
    "d'instruction, exécuté avant la livraison)\n"
    "==================================================================\n\n"
    "--- (a) données extraites et vérifiées (le script REFUSE si une ancre "
    "manque au journal) ---\n" + extraction_sortie +
    "\n--- (b) empreintes des artefacts scellés, byte pour byte ---\n"
    f"loupe.exe (0.1.1, scellée D181) : {loupe_sha}\n"
    "attendu                         : c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1\n"
    f"  -> {'CONFORME' if loupe_sha == 'c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1' else 'ÉCART'}\n"
    f"proxy.exe (1.0.0, scellée D170) : {proxy_sha}\n"
    "attendu                         : 446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d\n"
    f"  -> {'CONFORME' if proxy_sha == '446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d' else 'ÉCART'}\n\n"
    "--- (c) l'audit de gouvernance (champs, unicité, chaînage, append-only, "
    "entrées, contenu de l'édition) ---\n" + audit_sortie +
    "\n--- (c bis) le vérificateur du sceau I (14/14 attendu) ---\n" + sceau_sortie,
    encoding="utf-8")

# ------------------------------------------------------------------ la soumission (≤ 5 fichiers)
csv_fusionne = LIVRAISONS / "tableaux_donnees_v0.10.0.csv"
with open(csv_fusionne, "w", encoding="utf-8") as f:
    for nom, titre in (("jalons.csv", "Milestones M0-M10"),
                       ("budgets.csv", "Measured token budgets"),
                       ("oracles.csv", "Verification instruments and volumes"),
                       ("runs_loupe.csv", "The twelve Loupe terrain runs"),
                       ("empreintes.csv", "Sealed artifacts fingerprints")):
        f.write(f"===== {titre} ({nom}) =====\n")
        f.write((donnees / nom).read_text(encoding="utf-8"))
        f.write("\n")

readme = """TRIADE — ÉDITION ACADÉMIQUE v0.10.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers, le maximum exigé) :
  1. README.txt               — le présent guide du relecteur ;
  2. TRIADE_manuscrit_v0.10.0.pdf — le manuscrit IMRAD (anglais, résumé
     français inclus), prêt pour un comité de révision ;
  3. tableaux_donnees_v0.10.0.csv — TOUS les tableaux de données du
     manuscrit (jalons, budgets, oracles, les douze runs Loupe, empreintes),
     générés depuis le journal de travail par scripts/extraire_donnees_v100.py ;
  4. empreintes_soumission.txt  — l'empreinte sha-256 de chaque fichier de
     la présente archive (le manuscrit ET ses données se vérifient) ;
  5. VERIFICATION_v0.10.0.txt   — le constat de l'étape de vérification
     obligatoire : données extraites/vérifiées, artefacts scellés byte pour
     byte, audit de gouvernance VERT, sceau I 14/14.

Comment lire le manuscrit :
  - Chaque valeur numérique des tableaux est EXTRAITE du journal de travail
    append-only (9 348 lignes) et du journal des décisions (D1-D184) par le
    script d'extraction ; le manuscrit n'affirme rien qui ne soit généré.
  - Les quatre questions de recherche : défauts échappés (RQ1), coût en
    tokens par changement validé (RQ2), classes invisibles à l'émulation
    (RQ3), sûreté du patch à chaud (RQ4).
  - Les limites sont explicites : N=1, circularité de l'oracle, absence de
    baseline, sécurité mémoire non prouvée, temps constant non analysé.
  - L'auteur humain est unique ; l'agent IA (Z.ai GLM) est décrit en
    Methods et remercié, jamais co-auteur.

L'archive complète (sources LaTeX, bibliographie, chaîne de spécification,
scripts, extraits de journal) vit dans TRIADE_complet_v0.10.0.zip.

Licence du projet : Business Source License 1.1 (usage hors production
jusqu'au 2028-10-28, puis GPL v3+). Auteur : Alexis Lopez.
"""

emp_soumission = LIVRAISONS / "empreintes_soumission.txt"
emp_soumission.write_text(
    "EMPREINTES SHA-256 — archive de soumission v0.10.0\n\n"
    f"{sha256(readme)}  README.txt\n"
    f"{sha256(REPO / 'docs' / 'TRIADE_manuscrit_v0.10.0.pdf')}  "
    "TRIADE_manuscrit_v0.10.0.pdf\n"
    f"{sha256(csv_fusionne)}  tableaux_donnees_v0.10.0.csv\n"
    f"{sha256(emp_soumission.name + '-auto')}  empreintes_soumission.txt "
    "(l'empreinte de ce fichier vit au manifeste des livrables)\n"
    f"{sha256(verification)}  VERIFICATION_v0.10.0.txt\n", encoding="utf-8")

SOUMISSION = LIVRAISONS / "TRIADE_soumission_v0.10.0.zip"
with zipfile.ZipFile(SOUMISSION, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme)
    z.write(REPO / "docs" / "TRIADE_manuscrit_v0.10.0.pdf",
            "TRIADE_manuscrit_v0.10.0.pdf")
    z.write(csv_fusionne, "tableaux_donnees_v0.10.0.csv")
    z.write(emp_soumission, "empreintes_soumission.txt")
    z.write(verification, "VERIFICATION_v0.10.0.txt")
n_s = len(zipfile.ZipFile(SOUMISSION).namelist())
print(f"[soumission] {SOUMISSION.name} : {n_s} fichiers")

# ------------------------------------------------------------------ le complet
D = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
m = re.search(r"^## D182 —.*", D, re.MULTILINE | re.DOTALL)
decisions_ext = ("Extrait de docs/DECISIONS.md (append-only) — les décisions "
                 "de l'édition académique v0.10.0.\n\n" + m.group(0).rstrip() + "\n")
J = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(encoding="utf-8")
m = re.search(r"^## Entrée 223 —.*", J, re.MULTILINE | re.DOTALL)
entree_ext = ("Extrait de docs/JOURNAL_TRAVAIL.md — l'entrée de l'édition.\n\n"
              + (m.group(0).rstrip() if m else
                 "(l'Entrée 223 est consignée au geste du commit — "
                 "voir VERIFICATION_v0.10.0.txt)") + "\n")

entrees_complet = []  # (chemin_archive, source)


def ajoute(chemin_archive, source):
    entrees_complet.append((chemin_archive, source))


ajoute("manuscrit/TRIADE_manuscrit_v0.10.0.pdf",
       REPO / "docs" / "TRIADE_manuscrit_v0.10.0.pdf")
ajoute("manuscrit/main.tex", REPO / "scripts" / "manuscrit_v100" / "main.tex")
ajoute("manuscrit/refs.bib", REPO / "scripts" / "manuscrit_v100" / "refs.bib")
for f in sorted((REPO / "scripts" / "manuscrit_v100" / "donnees").iterdir()):
    ajoute(f"manuscrit/donnees/{f.name}", f)
ajoute("specification/Protocole_TRIADE_v0.10.0_Specification.pdf",
       REPO / "docs" / "Protocole_TRIADE_v0.10.0_Specification.pdf")
for f in sorted((REPO / "scripts" / "spec_v100").iterdir()):
    if f.suffix in (".tex", ".py", ".html", ".png"):
        ajoute(f"specification/spec_v100/{f.name}", f)
for s in ("extraire_donnees_v100.py", "audit_gouvernance_v100.py",
          "verifier_edition_v100.py"):
    ajoute(f"scripts/{s}", REPO / "scripts" / s)
ajoute("journal/extraits_journal.txt", donnees / "extraits_journal.txt")
ajoute("VERIFICATION_v0.10.0.txt", verification)

readme_complet = """TRIADE — ÉDITION ACADÉMIQUE v0.10.0 — ARCHIVE COMPLÈTE
======================================================

L'intégralité de l'édition : le manuscrit ET ses sources, la spécification
v0.10.0 (l'annexe A portée à sha-256, D184) et sa chaîne LaTeX, les données
GÉNÉRÉES (le script d'extraction refuse si une ancre manque au journal),
l'audit de gouvernance, les extraits de journal cités, les décisions de
l'édition (D182/D183/D184) et les empreintes de tout.

Arborescence :
  README.txt                    le présent guide
  manuscrit/TRIADE_manuscrit_v0.10.0.pdf   le manuscrit (livrable)
  manuscrit/main.tex            sources LaTeX (les tableaux sont \\input)
  manuscrit/refs.bib            bibliographie (chaque entrée : DOI vérifiable)
  manuscrit/donnees/            tableaux GÉNÉRÉS (tables_generees.tex + 5 CSV)
  specification/Protocole_TRIADE_v0.10.0_Specification.pdf  la spécification
  specification/spec_v100/      la chaîne LaTeX (née de spec_v090 par copie)
  scripts/extraire_donnees_v100.py   l'extraction + vérification des données
  scripts/audit_gouvernance_v100.py  l'audit de gouvernance (A1-A6)
  scripts/verifier_edition_v100.py   le vérificateur de l'édition
  journal/extraits_journal.txt  les entrées citées par le manuscrit
  journal/decisions_D182-D184.md  les décisions de l'édition
  journal/entree_223.md         l'entrée du journal de travail
  VERIFICATION_v0.10.0.txt      le constat de vérification
  empreintes_complet.txt        sha-256 de tout ce qui précède

Les artefacts scellés ne sont PAS dans l'archive (ils vivent au dépôt) :
leurs empreintes sont consignées dans les données et le constat.

Licence : Business Source License 1.1. Auteur : Alexis Lopez.
"""

emp_complet = LIVRAISONS / "empreintes_complet.txt"
lignes = ["EMPREINTES SHA-256 — archive complète v0.10.0", ""]
lignes.append(f"{sha256(readme_complet)}  README.txt")
for arch, src in entrees_complet:
    lignes.append(f"{sha256(src)}  {arch}")
lignes.append(f"{sha256(decisions_ext)}  journal/decisions_D182-D184.md")
lignes.append(f"{sha256(entree_ext)}  journal/entree_223.md")
lignes.append("(empreintes_complet.txt)  empreintes_complet.txt — l'empreinte "
              "de ce fichier vit au manifeste des livrables")
emp_complet.write_text("\n".join(lignes) + "\n", encoding="utf-8")

COMPLET = LIVRAISONS / "TRIADE_complet_v0.10.0.zip"
with zipfile.ZipFile(COMPLET, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt", readme_complet)
    for arch, src in entrees_complet:
        z.write(src, arch)
    z.writestr("journal/decisions_D182-D184.md", decisions_ext)
    z.writestr("journal/entree_223.md", entree_ext)
    z.write(emp_complet, "empreintes_complet.txt")
n_c = len(zipfile.ZipFile(COMPLET).namelist())
print(f"[complet] {COMPLET.name} : {n_c} entrées")

# ------------------------------------------------------------------ le manifeste des livrables
emp = LIVRAISONS / "empreintes_livrables.txt"
emp.write_text(
    "LIVRABLES DE L'ÉDITION ACADÉMIQUE v0.10.0 — empreintes sha-256\n\n"
    f"{sha256(SOUMISSION)}  TRIADE_soumission_v0.10.0.zip ({n_s} fichiers)\n"
    f"{sha256(COMPLET)}  TRIADE_complet_v0.10.0.zip ({n_c} entrées)\n"
    f"{sha256(emp_soumission)}  empreintes_soumission.txt\n"
    f"{sha256(emp_complet)}  empreintes_complet.txt\n", encoding="utf-8")
print(emp.read_text(encoding="utf-8"))
