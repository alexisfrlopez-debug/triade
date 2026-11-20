#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0220.py — LES DEUX ARCHIVES DE DÉPÔT de l'édition
v0.22.0 : LA SOUMISSION (README, le manuscrit, les empreintes, le
rapport de vérification, la note des tables générées) et LE COMPLET (les
sources des cinq pièces, les ateliers de la vague 11, les scripts, le
pack des cinq documents)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V11 = REPO / "scripts" / "vague11"
OUT = REPO / "depot-zenodo-v0220"
OUT.mkdir(exist_ok=True)


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# ---- LA SOUMISSION -------------------------------------------------------
SUB = OUT / "TRIADE_soumission_v0.22.0.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.22.0 (la vague 11 : "
               "la purge des instructions de remise D81 des pièces "
               "opératoires, les couloirs SIMD mesurés sur matériel, la "
               "boucle porteuse AES-NI restructurée sous sa cible, les "
               "gabarits versionnés, le coffre durci sur copies de "
               "laboratoire, le quatrième bras C+G+ séparant l'effet "
               "notation propre du régime de vérification, les kits "
               "pré-enregistrés, la soundness du lifter au domaine — et "
               "les errata nommés de la v0.21.0 : la décomposition "
               "mémoire corrigée (médiés 348, la somme 2098 exacte), les "
               "ratios restatés à une décimale, le plancher éditer au "
               "tokenizer natif). Le concept DOI "
               "10.5281/zenodo.24367343 résout sur la version courante.\n")
    ajouter(z, REPO / "edition-v0220" / "main.pdf",
            "TRIADE_manuscrit_v0.22.0.pdf")
    ajouter(z, V11 / "empreintes_livrables_v0.22.0.txt")
    ajouter(z, V11 / "rapport_verification_v0.22.0.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS des registres bruts "
               "(edition-v0220/donnees/ — les macros régénérées des "
               "journaux vivants et des JSON bruts) ; le linter v220 "
               "extrait TOUT token numérique de la prose des cinq pièces, "
               "le recalcule des CSV/JSONL bruts et refuse toute "
               "divergence (53 VERT 0 ROUGE, le contrôle négatif double "
               "vécu : les valeurs mutées REFUSÉES au premier nom).\n")

# ---- LE COMPLET ----------------------------------------------------------
CMP = OUT / "TRIADE_complet_v0.22.0.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.22.0 : les "
               "sources des cinq documents, les ateliers de la vague 11 "
               "(la purge D81, les couloirs SIMD, la boucle porteuse, les "
               "gabarits, le coffre durci, le quatrième bras, les kits, "
               "le lifter, les errata), les scripts de génération et LE "
               "LINTER v220 ÉTENDU À TOUT TOKEN NUMÉRIQUE (53 VERT 0 "
               "ROUGE — les canons bruts relus, les arithmétiques "
               "recalculées par code, les historiques datés, la classe "
               "structurelle ; l'ambiguïté FR/EN tranchée par la langue "
               "de la pièce ; le contrôle négatif double vécu).\n")
    for src in sorted((REPO / "edition-v0220").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0220/{src.relative_to(REPO / 'edition-v0220')}")
    for d in ("spec_v157", "livre_v16"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html",
                                                ".png"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    for src in sorted(V11.glob("*.py")):
        ajouter(z, src, f"scripts/vague11/{src.name}")
    ajouter(z, V11 / "rapport_verification_v0.22.0.txt",
            "scripts/vague11/rapport_verification_v0.22.0.txt")
    ajouter(z, V11 / "empreintes_livrables_v0.22.0.txt",
            "scripts/vague11/empreintes_livrables_v0.22.0.txt")
    for d in ("atelier-medians-zho5vilpy",
              "atelier-sequestre-ou6wn6wlv",
              "atelier-corridors-fnvan0zes",
              "atelier-porteuse-ahult8jgd",
              "atelier-gabarits-o5apue194",
              "atelier-coffre-vr9n3s3l7",
              "atelier-quatrebras-3lmyfb2xa",
              "atelier-preregistre-l4nnwqlld",
              "atelier-lifter-hrbdfy6i4"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "gardes_smt" not in str(src) \
                    and "clone-test/" not in str(src):
                # clone-test/ : le clone intégral du dépôt (513 Mo) — la
                # pièce de banc de la simulation D81, RÉGÉNÉRABLE au geste
                # (git clone) et dupliquée au miroir GitHub : les quatre
                # pièces de l'atelier (le plan, le rapport, la simulation,
                # l'outil) demeurent, le clone exclu — nommé.
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    for src in sorted((V11 / "pack-v220").rglob("*")):
        if src.is_file():
            ajouter(z, src,
                    f"pack-v220/{src.relative_to(V11 / 'pack-v220')}")

for f in (SUB, CMP):
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    print(f"[archive] {f.name} : {f.stat().st_size} o, sha256 {h[:16]}…")
