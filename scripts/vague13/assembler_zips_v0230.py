#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0230.py — LES DEUX ARCHIVES DE DÉPÔT de l'édition
v0.23.0 : LA SOUMISSION (README, le manuscrit, le manifeste des
empreintes, le rapport de vérification, la note des tables générées) et
LE COMPLET (les sources des cinq pièces, les ateliers des vagues 12-13,
les scripts de génération et LE LINTER v230, le pack des cinq
documents)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V13 = REPO / "scripts" / "vague13"
OUT = REPO / "depot-zenodo-v0230"
OUT.mkdir(exist_ok=True)


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# ---- LA SOUMISSION -------------------------------------------------------
SUB = OUT / "TRIADE_soumission_v0.23.0.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.23.0 (la vague 13 : "
               "la génération aux six écarts corrigés — la partition "
               "exacte de la batterie 559, les opérandes non arrondis de "
               "chaque ratio, les abstracts EN/FR depuis les mêmes "
               "macros, la table canonique des budgets adoptés, le "
               "dashboard de la spécification aligné, la voix « présent "
               "édition » unique et le changelog gelé des vagues ; les "
               "résultats : le couloir GHASH PCLMULQDQ à 63-64 cycles "
               "contre le scellé 806, l'AES-GCM complet mesuré face à "
               "OpenSSL EVP, la ventilation quatre bras aux volumes "
               "égalisés — la part notation intrinsèque 5,5 % —, la "
               "requalification des 58 gardes et des 15 exclusions, le "
               "Tamarin v2 sans restriction, TPL-ADD-v3 et sa boucle de "
               "réparation, le Livre v1.7 et la spécification v0.15.8). "
               "Le concept DOI 10.5281/zenodo.24367343 résout sur la "
               "version courante.\n")
    ajouter(z, REPO / "edition-v0230" / "main.pdf",
            "TRIADE_manuscrit_v0.23.0.pdf")
    ajouter(z, V13 / "empreintes_livrables_v0.23.0.txt")
    ajouter(z, REPO / "rapport_verification_v0.23.0.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS des registres bruts "
               "(edition-v0230/donnees/ — les macros régénérées des "
               "journaux vivants et des JSON bruts) ; le linter v230 "
               "extrait TOUT token numérique de la prose des cinq pièces, "
               "le recalcule des CSV/JSONL bruts et refuse toute "
               "divergence (71 VERT 0 ROUGE, le contrôle négatif vécu : "
               "les valeurs mutées REFUSÉES au premier nom).\n")

# ---- LE COMPLET ----------------------------------------------------------
CMP = OUT / "TRIADE_complet_v0.23.0.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.23.0 : les "
               "sources des cinq documents (le manuscrit, la "
               "spécification v0.15.8, le Livre v1.7, les preuves, la "
               "présentation), les ateliers des vagues 12-13 (la vague "
               "12 : la recomposabilité, la purge sémantique, la "
               "machinery générative, le double moteur, TPL-ADD-v2, la "
               "marge vierge ; la vague 13 : le GHASH PCLMULQDQ, la "
               "requalification, la ventilation quatre bras, TPL-ADD-v3, "
               "la purge v13, la génération v0.23.0), les scripts de "
               "génération et LE LINTER v230 (71 VERT 0 ROUGE — les "
               "canons bruts relus, les arithmétiques recalculées par "
               "code, les historiques datés, la classe structurelle ; "
               "l'ambiguïté FR/EN tranchée par la langue de la pièce ; "
               "le correctif d'alignement des contextes ; le contrôle "
               "négatif vécu) et LE PACK des cinq documents.\n")
    for src in sorted((REPO / "edition-v0230").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0230/{src.relative_to(REPO / 'edition-v0230')}")
    for d in ("spec_v158", "livre_v17"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html",
                                                ".png"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    ajouter(z, REPO / "scripts" / "vague12" / "linter_v230.py",
            "scripts/vague12/linter_v230.py")
    for src in sorted(V13.glob("*.py")):
        ajouter(z, src, f"scripts/vague13/{src.name}")
    ajouter(z, REPO / "rapport_verification_v0.23.0.txt",
            "rapport_verification_v0.23.0.txt")
    ajouter(z, V13 / "empreintes_livrables_v0.23.0.txt",
            "scripts/vague13/empreintes_livrables_v0.23.0.txt")
    for d in ("atelier-recomposabilite-6kbfrpn7k",
              "atelier-purge-0uug27teo",
              "atelier-double-moteur-14n3k8gd7",
              "atelier-conformite-alhmpl35u",
              "atelier-ajouter-v2-pgodgk35l",
              "atelier-marge-vierge-x705m50vl",
              "atelier-ghash-0g3400vql",
              "atelier-requalification-q8kugkpdu",
              "atelier-hcgp3-ay6zuzm8o",
              "atelier-ajouter-v3-5nwnwoceo",
              "atelier-purge-v13-h66o54pjd",
              "atelier-generation-v0230-ylrzmlbn8"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "gardes_smt" not in str(src) \
                    and "clone-test/" not in str(src):
                # native/ : les rig régénérables par les scripts committés
                # (l'exclusion nommée de la v0.22.1 reconduite)
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    for src in sorted((V13 / "pack-v230").rglob("*")):
        if src.is_file():
            ajouter(z, src,
                    f"pack-v230/{src.relative_to(V13 / 'pack-v230')}")

for f in (SUB, CMP):
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    print(f"[archive] {f.name} : {f.stat().st_size} o, sha256 {h}")
