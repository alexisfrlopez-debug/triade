#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_complet_v0221.py — L'ARCHIVE COMPLÈTE v0.22.1 (la release
corrective de l'édition v0.22.0, la vague 12) : les sources de l'édition
DEMEURÉES (la balise v0.22.0 immuable — le manuscrit, les preuves, la
présentation inchangés), LES CHAÎNES CORRIGÉES (le Livre v1.6 et la spec
v0.15.7 reconstruits par la purge sémantique D81 — 0uug27teo), LES NEUF
ATELIERS de la vague 11 ET LES SIX de la vague 12 (la recomposabilité
6kbfrpn7k, la purge 0uug27teo, la machinery générative alhmpl35u, le
double moteur 14n3k8gd7, TPL-ADD-v2 pgodgk35l, les deux variantes à la
marge vierge x705m50vl), les scripts des deux vagues (le linter v230
compris) et LE PACK des cinq documents (inchangé, l'édition v0.22.0)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V11 = REPO / "scripts" / "vague11"
V12 = REPO / "scripts" / "vague12"
OUT = REPO / "depot-zenodo-v0221"
OUT.mkdir(exist_ok=True)


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


CMP = OUT / "TRIADE_complet_v0.22.1.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète v0.22.1, la RELEASE "
               "CORRECTIVE de l'édition v0.22.0 (la douzième vague "
               "d'instructions) : l'édition v0.22.0 DEMEURE (la balise "
               "immuable — le manuscrit, les preuves et la présentation "
               "inchangés, les errata consignés aux ateliers) ; LES "
               "CHAÎNES CORRIGÉES : le Livre du Coffre v1.6 et la "
               "spécification v0.15.7 purgés au périmètre sémantique de "
               "la garde D81 et RECONSTRUITS (les résidus prescriptifs "
               "remplacés par la garde active D223, les contextes "
               "historiques annotés) ; LES SIX ATELIERS de la vague 12 "
               "— la recomposabilité des ratios (les canons non arrondis "
               "re-mesurés et re-lus, le census 559 sommé par code, le "
               "linter v230 aux classes RATIOS et ÉTIQUETTES), la purge "
               "sémantique, la machinery de conformité générative (30 000 "
               "traces zéro divergence, le modèle z3 aux six invariants, "
               "la grille de réception fail-closed), le double moteur "
               "généralisé (divergence zéro, le gain 357x, le budget de "
               "risque pondéré, la menace du cache), TPL-ADD-v2 (le "
               "dictionnaire de domaine, la cible pré-enregistrée manquée "
               "et le gap nommé par classe) et les deux variantes à la "
               "marge vierge (le v5-entrelacé k∈{4,8} aux calendriers "
               "indépendants — la cible ≤3 c/bloc manquée au plancher "
               "MESURÉ de l'unité AES 0,459 c/aesenc, jamais un chiffre "
               "ajusté ; l'AVX2 après hissage au verdict sous R10 — le "
               "gain 12,4x du couloir de recherche, la batterie 559 "
               "re-roulée zéro divergence) — et LES NEUF de la vague 11 "
               "(la purge D81 au grep, les couloirs SIMD, la boucle "
               "porteuse, les gabarits, le coffre durci, le quatrième "
               "bras, les kits, le lifter, les errata) ; le linter v220 "
               "ET SON EXTENSION v230.\n")
    # (1) les sources de l'édition v0.22.0 (DEMEURÉES)
    for src in sorted((REPO / "edition-v0220").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0220/{src.relative_to(REPO / 'edition-v0220')}")
    # (2) LES CHAÎNES CORRIGÉES — les .tex/.py/.html ET LES PDF RECONSTRUITS
    for d in ("spec_v157", "livre_v16"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html",
                                                ".png", ".pdf"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    # (3) les scripts des deux vagues + les pièces de vérification
    for src in sorted(V11.glob("*.py")):
        ajouter(z, src, f"scripts/vague11/{src.name}")
    for src in sorted(V12.glob("*.py")):
        ajouter(z, src, f"scripts/vague12/{src.name}")
    ajouter(z, V11 / "rapport_verification_v0.22.0.txt",
            "scripts/vague11/rapport_verification_v0.22.0.txt")
    ajouter(z, V11 / "empreintes_livrables_v0.22.0.txt",
            "scripts/vague11/empreintes_livrables_v0.22.0.txt")
    ajouter(z, V12 / "rapport_verification_v0.22.1.txt",
            "scripts/vague12/rapport_verification_v0.22.1.txt")
    ajouter(z, V12 / "empreintes_livrables_v0.22.1.txt",
            "scripts/vague12/empreintes_livrables_v0.22.1.txt")
    # (4) LES NEUF ATELIERS de la vague 11
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
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    # (5) LES SIX ATELIERS de la vague 12
    for d in ("atelier-recomposabilite-6kbfrpn7k",
              "atelier-purge-0uug27teo",
              "atelier-conformite-alhmpl35u",
              "atelier-double-moteur-14n3k8gd7",
              "atelier-ajouter-v2-pgodgk35l",
              "atelier-marge-vierge-x705m50vl"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "states/" not in str(src) \
                    and "logs/" not in str(src):
                # native/ : les rig régénérables par le script committé
                # (la convention de la vague 11) ; states/ et logs/ : les
                # états TLA+ et les journaux volumineux des batteries —
                # les rapports et registres demeurent
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    # (6) LE PACK des cinq documents (l'édition v0.22.0 inchangée)
    for src in sorted((V11 / "pack-v220").rglob("*")):
        if src.is_file():
            ajouter(z, src,
                    f"pack-v220/{src.relative_to(V11 / 'pack-v220')}")

h = hashlib.sha256(CMP.read_bytes()).hexdigest()
n = len([i for i in zipfile.ZipFile(CMP).infolist()])
print(f"[archive] {CMP.name} : {CMP.stat().st_size} o, {n} entrées, "
      f"sha256 {h[:16]}…")
