#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0232.py — LES DEUX ARCHIVES DE DÉPÔT de l'édition
v0.23.2 : LA SOUMISSION (README, le manuscrit, le manifeste des
empreintes, le rapport de vérification, la note des tables générées) et
LE COMPLET (les sources des cinq pièces, les ateliers des vagues 12-14,
les chaînes de génération et LES DEUX LINTERS v230/v232, le pack des
cinq documents). Le linter v232 EXIGÉ vert avant l'assemblage (le refus
ferme) ; chaque archive testée au dézippage."""
import hashlib
import pathlib
import subprocess
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V14 = REPO / "scripts" / "vague14"
OUT = REPO / "depot-zenodo-v0232"
OUT.mkdir(exist_ok=True)


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# (0) LE LINTER EXIGÉ VERT AVANT L'ASSEMBLAGE (le refus ferme)
print("[0] le linter v232 exigé vert avant l'assemblage…")
r = subprocess.run([sys.executable, str(V14 / "linter_v232.py")],
                   capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout[-2000:])
    raise SystemExit("LE LINTER v232 ROUGE — les archives REFUSÉES")
print("    le linter : VERT")

# ---- LA SOUMISSION -------------------------------------------------------
SUB = OUT / "TRIADE_soumission_v0.23.2.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.23.2 (la vague 14, "
               "la GÉNÉRATION CORRECTIVE — la session promise à l'Entrée "
               "384 : les CINQ pièces régénérées aux sources corrigées, "
               "le linter inter-pièces étendu aux quatre règles "
               "nouvelles, les trois packs assemblés à la version "
               "courante ; les corrections (a)-(j) portées : le canon "
               "GHASH unique sur la variété adoptée (schoolbook 63,39 "
               "[IQR 30] = 12,7×), les opérandes non arrondis du "
               "plancher M4 (6.912/2.056), la fermeture de la ventilation "
               "(20.715+16.497+0.213 = 37.425), la grille F/L (D203), la "
               "famille « the field beyond the pattern » portée à "
               "l'abstract, le bandeau du Livre v1.7 ; les résultats de "
               "la vague 14 portés au corps : le GHASH agrégé à 19,66 "
               "c/mult — 41,0× sur le scellé, H-CGP4 la mémoïsation "
               "content-addressed à −89,4 % sans aucun contrôle retiré, "
               "TPL-ADD-v4 à 7/18 avec la première conversion d'un refus "
               "honnête, H7 tirée et signée, le premier run Tamarin vécu "
               "— le lemme d'implication falsifié par un défaut de "
               "modélisation nommé, aucun verdict fabriqué). La v0.23.1 "
               "avait porté ces contenus au seul pack complet — la "
               "commande du maître (« je n'ai pas la version "
               "presentation et soumission du pack dans zenodo ») est "
               "honorée : la soumission et la présentation à la version "
               "courante. Le concept DOI 10.5281/zenodo.24367343 résout "
               "sur la version courante.\n")
    ajouter(z, REPO / "edition-v0230" / "main.pdf",
            "TRIADE_manuscrit_v0.23.2.pdf")
    ajouter(z, V14 / "empreintes_livrables_v0.23.2.txt")
    ajouter(z, REPO / "rapport_verification_v0.23.2.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS des registres bruts "
               "(edition-v0230/donnees/ — les macros régénérées des "
               "journaux vivants et des JSON bruts) ; le linter v232 "
               "(ÉTENDU : les quatre règles nouvelles — les chaînes de "
               "version, les décompositions recomposées par code depuis "
               "les CSV, tout ratio publié portant ses opérandes non "
               "arrondis, la détection T/X hors marqueur d'époque daté) "
               "extrait TOUT token numérique de la prose des cinq "
               "pièces, le recalcule des CSV/JSONL bruts et refuse toute "
               "divergence (153 VERT 0 ROUGE, le contrôle négatif vécu : "
               "cinq divergences injectées REFUSÉES au premier nom, la "
               "règle (C) refusant la fermeture privée de ses opérandes "
               "à ses deux étages).\n")

# ---- LE COMPLET ----------------------------------------------------------
CMP = OUT / "TRIADE_complet_v0.23.2.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.23.2 (la vague "
               "14, la génération corrective) : les sources des cinq "
               "documents (le manuscrit, la spécification v0.15.8, le "
               "Livre v1.7, les preuves, la présentation), les ateliers "
               "des vagues 12-13-14 (la vague 12 : la recomposabilité, "
               "la purge sémantique, la machinery générative, le double "
               "moteur, TPL-ADD-v2, la marge vierge ; la vague 13 : le "
               "GHASH PCLMULQDQ, la requalification, la ventilation "
               "quatre bras, TPL-ADD-v3, la purge v13, la génération "
               "v0.23.0 ; la vague 14 : la fermeture sécurité, le GHASH "
               "agrégé, H-CGP4, TPL-ADD-v4, la validité externe H7, les "
               "dix corrections), les chaînes de génération (vague13 + "
               "vague14) et LES DEUX LINTERS (le v230 : 71 VERT — le "
               "socle de tout token numérique ; le v232 ÉTENDU : 153 "
               "VERT — les QUATRE RÈGLES NOUVELLES : les chaînes de "
               "version, les décompositions recomposées par code depuis "
               "les CSV, tout ratio publié portant ses opérandes non "
               "arrondis, la détection T/X hors marqueur d'époque daté "
               "— le contrôle négatif vécu) et LE PACK des cinq "
               "documents.\n")
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
    for src in sorted((REPO / "scripts" / "vague13").glob("*.py")):
        ajouter(z, src, f"scripts/vague13/{src.name}")
    for src in sorted(V14.glob("*.py")):
        ajouter(z, src, f"scripts/vague14/{src.name}")
    ajouter(z, REPO / "rapport_verification_v0.23.2.txt",
            "rapport_verification_v0.23.2.txt")
    ajouter(z, V14 / "empreintes_livrables_v0.23.2.txt",
            "scripts/vague14/empreintes_livrables_v0.23.2.txt")
    # — LES ATELIERS DES VAGUES 12-13 (le périmètre de la v0.23.0) —
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
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    # — LES ATELIERS DE LA VAGUE 14 (la structure v0.23.1 reconduite) —
    for d in ("atelier-fermeture-f3uznui3l",
              "atelier-ghash-agrege-h1mz2sr8s",
              "atelier-hcgp4-s2p9bm3zd",
              "atelier-ajouter-v4-842vqyy1k",
              "atelier-validite-tcb7tpf9q"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "rig_garde" not in str(src):
                ajouter(z, src,
                        f"ateliers-vague14/{d}/{src.relative_to(racine)}")
    # — les plans gelés + le journal de la vague 14 (la structure v0.23.1) —
    for src in sorted(REPO.glob("PLAN-*.md")):
        ajouter(z, src, f"vague14/{src.name}")
    ajouter(z, REPO / "EMPREINTES-PLANS-VAGUE14.txt",
            "vague14/EMPREINTES-PLANS-VAGUE14.txt")
    ajouter(z, REPO / "REPRISE_PROJET.md", "vague14/REPRISE_PROJET.md")
    ajouter(z, REPO / "worklog.md", "vague14/worklog.md")
    # — LE PACK des cinq documents —
    for src in sorted((V14 / "pack-v232").rglob("*")):
        if src.is_file():
            ajouter(z, src,
                    f"pack-v232/{src.relative_to(V14 / 'pack-v232')}")

for f in (SUB, CMP):
    with zipfile.ZipFile(f) as z:
        mauvais = z.testzip()
        if mauvais is not None:
            raise SystemExit(f"ZIP CORROMPU : {mauvais} ({f.name})")
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    print(f"[archive] {f.name} : {f.stat().st_size} o, "
          f"{len(zipfile.ZipFile(f).namelist())} entrées, sha256 {h}")
