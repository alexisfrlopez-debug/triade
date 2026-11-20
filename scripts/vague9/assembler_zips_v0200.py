#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0200.py — les DEUX zips de dépôt Zenodo v0.20.0 (la
future version du concept 10.5281/zenodo.24367343 — la publication AU
GESTE DU MAÎTRE) : la soumission (le manuscrit, les empreintes, le
rapport de vérification) et le complet (les sources de l'édition, les
ateliers de la vague 9, les scripts)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V9 = REPO / "scripts" / "vague9"
OUT = REPO / "depot-zenodo-v0200"
OUT.mkdir(exist_ok=True)


def sha256_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# ---- LA SOUMISSION (5 entrées, la structure reconduite) --------------------
SUB = OUT / "TRIADE_soumission_v0.20.0.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.20.0 (la vague 9 : "
               "la sécurité au plancher, la boucle de vérification, les "
               "deux couloirs de performance, le coût en tokens au-delà "
               "d'OPT-05, le tableau de bord des quatre axes). Le concept "
               "DOI 10.5281/zenodo.24367343 résout sur la version courante "
               "; la publication de la présente AU GESTE DU MAÎTRE.\n")
    ajouter(z, REPO / "edition-v0200" / "main.pdf",
            "TRIADE_manuscrit_v0.20.0.pdf")
    ajouter(z, V9 / "empreintes_livrables_v0.20.0.txt")
    ajouter(z, V9 / "rapport_verification_v0.20.0.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS par les scripts "
               "d'extraction des registres bruts (edition-v0200/donnees/) "
               "— aucun chiffre tapé à la main ; le tableau de bord des "
               "quatre axes est GÉNÉRÉ des pièces brutes par atelier-"
               "dashboard-h0mq0s2m6/tableau_bord_v200.py et les ratios "
               "RECALCULÉS par le linter v200 au build (le pack complet "
               "porte l'atelier).\n")

# ---- LE COMPLET (les sources de l'édition et les pièces de la vague) --------
CMP = OUT / "TRIADE_complet_v0.20.0.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.20.0 : les "
               "sources des cinq documents, les ateliers de la vague 9 "
               "(la sécurité au plancher, les deux couloirs, la boucle de "
               "vérification, les tokens, le tableau de bord), les "
               "scripts de génération et le linter inter-pièces v200 "
               "(74 VERT 0 ROUGE, les ratios RECALCULÉS des pièces "
               "brutes, les empreintes sha-256 re-vérifiées).\n")
    # les sources des cinq pièces
    for src in sorted((REPO / "edition-v0200").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0200/{src.relative_to(REPO / 'edition-v0200')}")
    for d in ("spec_v156", "livre_v15"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html", ".png"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    for src in sorted(V9.glob("*.py")):
        ajouter(z, src, f"scripts/vague9/{src.name}")
    ajouter(z, V9 / "rapport_verification_v0.20.0.txt",
            "scripts/vague9/rapport_verification_v0.20.0.txt")
    ajouter(z, V9 / "empreintes_livrables_v0.20.0.txt",
            "scripts/vague9/empreintes_livrables_v0.20.0.txt")
    # les ateliers de la vague (les pièces)
    for d in ("atelier-securite-bk79jvzbm", "atelier-perf-0205wxg5q",
              "atelier-boucle-bkobf06nu", "atelier-tokens-uagz3fby7",
              "atelier-dashboard-h0mq0s2m6"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "certificats_smt" not in str(src) \
                    and "cf3_smt_certificats" not in str(src) \
                    and "certificats/" not in str(src) \
                    and "oracle_natif" not in str(src):
                ajouter(z, src, f"{d}/{src.relative_to(racine)}")
    # le pack des cinq documents
    for src in sorted((V9 / "pack-v200").rglob("*")):
        if src.is_file():
            ajouter(z, src, f"pack-v200/{src.relative_to(V9 / 'pack-v200')}")

for f in (SUB, CMP):
    print(f"[VERT] {f.name} [{f.stat().st_size:,} octets, "
          f"{len(zipfile.ZipFile(f).namelist())} entrées] "
          f"sha256:{sha256_file(f)[:16]}…")
