#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0210.py — LES DEUX ARCHIVES DE DÉPÔT de l'édition
v0.21.0 : LA SOUMISSION (README, le manuscrit, les empreintes, le
rapport de vérification, la note des tables générées) et LE COMPLET (les
sources des cinq pièces, les ateliers de la vague 10, les scripts, le
pack des cinq documents)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V10 = REPO / "scripts" / "vague10"
OUT = REPO / "depot-zenodo-v0210"
OUT.mkdir(exist_ok=True)


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# ---- LA SOUMISSION -------------------------------------------------------
SUB = OUT / "TRIADE_soumission_v0.21.0.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.21.0 (la vague 10 : "
               "la faute SSE2 nommée et la re-mesure aux baselines "
               "équitables, la fenêtre de relecture de l'édition, les "
               "gardes runtime et la non-interférence étendue, le bras "
               "C+G isolant l'effet notation, la réconciliation "
               "abstract/corps/tableaux et le registre neutre). Le "
               "concept DOI 10.5281/zenodo.24367343 résout sur la version "
               "courante.\n")
    ajouter(z, REPO / "edition-v0210" / "main.pdf",
            "TRIADE_manuscrit_v0.21.0.pdf")
    ajouter(z, V10 / "empreintes_livrables_v0.21.0.txt")
    ajouter(z, V10 / "rapport_verification_v0.21.0.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS des registres bruts "
               "(edition-v0210/donnees/ — les macros régénérées des "
               "journaux vivants et des JSON bruts) ; le linter v210 "
               "recalcule les médianes et les ratios au build et refuse "
               "toute divergence (65 VERT 0 ROUGE, le contrôle négatif "
               "vécu : la valeur mutée REFUSÉE au premier nom).\n")

# ---- LE COMPLET ----------------------------------------------------------
CMP = OUT / "TRIADE_complet_v0.21.0.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.21.0 : les "
               "sources des cinq documents, les ateliers de la vague 10 "
               "(la re-mesure SSE2, la fenêtre, les gardes et la "
               "non-interférence, le bras C+G), les scripts de génération "
               "et le linter inter-pièces + interne v210 (65 VERT 0 "
               "ROUGE — les médianes et ratios RECALCULÉS des pièces "
               "brutes, les empreintes re-vérifiées, le contrôle négatif "
               "vécu).\n")
    for src in sorted((REPO / "edition-v0210").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0210/{src.relative_to(REPO / 'edition-v0210')}")
    for d in ("spec_v156", "livre_v15"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html",
                                                ".png"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    for src in sorted(V10.glob("*.py")):
        ajouter(z, src, f"scripts/vague10/{src.name}")
    ajouter(z, V10 / "rapport_verification_v0.21.0.txt",
            "scripts/vague10/rapport_verification_v0.21.0.txt")
    ajouter(z, V10 / "empreintes_livrables_v0.21.0.txt",
            "scripts/vague10/empreintes_livrables_v0.21.0.txt")
    for d in ("atelier-remesure-sse2-8z4hj76w4",
              "atelier-fenetre-mqf258e4l",
              "atelier-gardes-ifqm1d1i4",
              "atelier-cg-3a91o5whb"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "gardes_smt" not in str(src):
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    for src in sorted((V10 / "pack-v210").rglob("*")):
        if src.is_file():
            ajouter(z, src,
                    f"pack-v210/{src.relative_to(V10 / 'pack-v210')}")

for f in (SUB, CMP):
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    print(f"[archive] {f.name} : {f.stat().st_size} o, sha256 {h[:16]}…")
