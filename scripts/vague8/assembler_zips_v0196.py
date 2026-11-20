#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0196.py — les DEUX zips de dépôt Zenodo v0.19.6 (la
future version du concept 10.5281/zenodo.24367343 — la publication AU
GESTE DU MAÎTRE) : la soumission (le manuscrit, les empreintes, le
rapport de vérification) et le complet (les sources de l'édition, les
ateliers de la vague, les scripts)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V8 = REPO / "scripts" / "vague8"
OUT = REPO / "depot-zenodo-v0196"
OUT.mkdir(exist_ok=True)


def sha256_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# ---- LA SOUMISSION (5 entrées, la structure reconduite) --------------------
SUB = OUT / "TRIADE_soumission_v0.19.6.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.19.6 (la vague 8 : "
               "la cohérence, la gouvernance vécue, l'intégrité "
               "pré-enregistrée, l'indépendance par dérivation-outillée, "
               "OPT-05). Le concept DOI 10.5281/zenodo.24367343 résout sur "
               "la version courante ; la publication de la présente AU "
               "GESTE DU MAÎTRE.\n")
    ajouter(z, REPO / "edition-v0196" / "main.pdf",
            "TRIADE_manuscrit_v0.19.6.pdf")
    ajouter(z, V8 / "empreintes_livrables_v0.19.6.txt")
    ajouter(z, V8 / "rapport_verification_v0.19.6.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS par les scripts "
               "d'extraction des registres bruts (edition-v0196/donnees/) — "
               "aucun chiffre tapé à la main ; la macro plage D1-D223 et "
               "les comptes de lignes sont régénérés des journaux vivants "
               "par scripts/vague8/regenerer_macros_v196.py.\n")

# ---- LE COMPLET (les sources de l'édition et les pièces de la vague) --------
CMP = OUT / "TRIADE_complet_v0.19.6.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.19.6 : les "
               "sources des cinq documents, les ateliers de la vague 8 "
               "(OPT-05, l'indépendance, la re-mesure RQ2, la "
               "classification), les scripts de génération et le linter "
               "inter-pièces (39 VERT 0 ROUGE).\n")
    # les sources des cinq pièces
    for src in sorted((REPO / "edition-v0196").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0196/{src.relative_to(REPO / 'edition-v0196')}")
    for d in ("spec_v155", "livre_v14"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html", ".png"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    for src in sorted(V8.glob("*.py")):
        ajouter(z, src, f"scripts/vague8/{src.name}")
    # les ateliers de la vague (les pièces)
    for d in ("atelier-opt05-pe6iv71fj", "atelier-independance-peap6ws09",
              "atelier-egalite-gq117wphb"):
        for src in sorted((REPO / d).rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000:
                ajouter(z, src, f"{d}/{src.relative_to(REPO / d)}")
    # le pack des cinq documents
    for src in sorted((V8 / "pack-v196").rglob("*")):
        if src.is_file():
            ajouter(z, src, f"pack-v196/{src.relative_to(V8 / 'pack-v196')}")

for f in (SUB, CMP):
    print(f"[VERT] {f.name} [{f.stat().st_size:,} octets, "
          f"{len(zipfile.ZipFile(f).namelist())} entrées] "
          f"sha256:{sha256_file(f)[:16]}…")
