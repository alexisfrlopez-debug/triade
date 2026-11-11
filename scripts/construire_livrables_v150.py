#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_livrables_v150.py — les archives de l'édition v0.15.0 (nées
de construire_livrables_v140.py par le même modèle) : soumission ≤ 5
fichiers + complet (les preuves non bornées, le raffinement, les kits,
la réplication, le rapport de vérification)."""
import hashlib
import pathlib
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
LIV = REPO / "download" / "edition_v0150"
LIV.mkdir(parents=True, exist_ok=True)
DON = REPO / "scripts" / "manuscrit_v150" / "donnees"
P110 = REPO / "scripts" / "preuves_v110"
P130 = REPO / "scripts" / "preuves_v130"
P140 = REPO / "scripts" / "preuves_v140"
P150 = REPO / "scripts" / "preuves_v150"
SOUM = LIV / "TRIADE_soumission_v0.15.0.zip"
COMP = LIV / "TRIADE_complet_v0.15.0.zip"


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# la soumission : le manuscrit + les tableaux fusionnés + empreintes + le constat
csv_f = LIV / "tableaux_donnees_v0.15.0.csv"
with open(csv_f, "w", encoding="utf-8") as f:
    for nom in ("jalons.csv", "budgets.csv", "oracles.csv", "runs_loupe.csv",
                "empreintes.csv"):
        f.write(f"===== {nom} =====\n")
        f.write((DON / nom).read_text(encoding="utf-8"))
        f.write("\n")
    for base, noms in ((P110, ("mutation.csv", "benchmarks.csv")),
                       (P130, ("audit_benchmark.csv", "stats_v130.csv")),
                       (P140, ("bras_c.csv", "remesure_rq2.csv",
                               "independance_agent.csv",
                               "rejeu_survivants.csv")),
                       (P150, ("modele_invariant.csv", "raffinement.csv"))):
        for nom in noms:
            f.write(f"===== {base.name}/{nom} =====\n")
            f.write((base / nom).read_text(encoding="utf-8"))
            f.write("\n")

readme = """TRIADE — ÉDITION ACADÉMIQUE v0.15.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.15.0.pdf    — le manuscrit : les QUATRE
     propriétés du coffre PROUVÉES NON BORNÉES en époques par invariant
     inductif (le plafond retiré, la préservation par les 13 règles, la
     translation d'époque, la fidélité D187 reproduite exactement, les
     bornes étendues zéro hors invariant), le RAFFINEMENT
     modèle-implémentation (34 pas, zéro écart, les chemins d'échec
     inclus, cinq époques vécues aux deux niveaux), la table des preuves
     ENFIN RENDUE (la dette des deux éditions précédentes guérie :
     longtable, 34 lignes), la table des STATUTS SYSTÉMATIQUES (prouvé
     non borné / prouvé borné / en attente de run matériel) et les
     menaces actualisées (l'uniformité structurelle et témoignée, le
     vérificateur maison, les kits en attente) ;
  3. tableaux_donnees_v0.15.0.csv    — tous les tableaux de données du
     manuscrit, générés par script depuis les sorties brutes des
     instruments (aucune valeur tapée à la main) ;
  4. empreintes_livrables.txt        — les empreintes sha256 de l'archive
     de soumission et des pièces principales ;
  5. rapport_verification_v0.15.0.txt — l'étape de vérification : le
     garde des quatorze arbres signés, les pièces scellées intactes, le
     model-checking et le raffinement RE-EXÉCUTÉS depuis un clone frais,
     les comptes confrontés, les tableaux régénérés identiques, chaque
     statut relu de sa pièce — 18 vérificateurs VERTS.

LA LECTURE HONNÊTE : « prouvé non borné » vaut sous les hypothèses
A1-A4 du modèle symbolique (A5 — canaux auxiliaires, failles
d'implémentation, compromission des trois éléments, quantique — est
hors modèle et le dit) ; les trois kits de mesure matérielle sont
PRÉPARÉS ET EN ATTENTE du run du développeur : AUCUN chiffre matériel
n'existe dans cette édition, aucun n'est fabriqué.
"""
readme_f = LIV / "README.txt"
readme_f.write_text(readme, encoding="utf-8")

emp_f = LIV / "empreintes_livrables.txt"
emp_f.write_text("LIVRABLES v0.15.0 (empreintes posées à la phase finale)\n",
                 encoding="utf-8")
rapport = P150 / "rapport_verification_v150.txt"

n_s = 0
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(readme_f, "README.txt")
    z.write(REPO / "scripts/manuscrit_v150/main.pdf",
            "TRIADE_manuscrit_v0.15.0.pdf")
    z.write(csv_f, "tableaux_donnees_v0.15.0.csv")
    z.write(emp_f, "empreintes_livrables.txt")   # réécrit après (phase 2)
    z.write(rapport, "rapport_verification_v0.15.0.txt")
    n_s = 5

# phase 2 : les empreintes finales (la soumission est empreintée APRÈS
# construction ; le fichier d'empreintes re-liste les pièces du zip)
emp_f.write_text(
    "LIVRABLES v0.15.0\n\n"
    f"{sha256(SOUM)}  soumission ({n_s} fichiers)\n"
    f"{sha256(REPO / 'scripts/manuscrit_v150/main.pdf')}  "
    "manuscrit (21 pages, la table des preuves rendue)\n"
    f"{sha256(REPO / 'docs/Protocole_TRIADE_v0.15.0_Specification.pdf')}  "
    "specification (64 pages, consignee n°56)\n"
    f"{sha256(REPO / 'loupe/loupe.exe')}  loupe.exe 0.1.1 (la piece "
    "scellee, INTACTE)\n"
    f"{sha256(REPO / 'tls13/proxy.exe')}  proxy.exe 1.0.0 (la piece "
    "scellee, INTACTE)\n", encoding="utf-8")
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(readme_f, "README.txt")
    z.write(REPO / "scripts/manuscrit_v150/main.pdf",
            "TRIADE_manuscrit_v0.15.0.pdf")
    z.write(csv_f, "tableaux_donnees_v0.15.0.csv")
    z.write(emp_f, "empreintes_livrables.txt")
    z.write(rapport, "rapport_verification_v0.15.0.txt")

# le complet : l'intégralité
n_c = 0
with zipfile.ZipFile(COMP, "w", zipfile.ZIP_DEFLATED) as z:
    # les documents
    z.write(REPO / "scripts/manuscrit_v150/main.tex",
            "manuscrit/main.tex")
    z.write(REPO / "scripts/manuscrit_v150/main.pdf",
            "manuscrit/TRIADE_manuscrit_v0.15.0.pdf")
    z.write(REPO / "scripts/manuscrit_v150/refs.bib",
            "manuscrit/refs.bib")
    z.write(REPO / "docs/Protocole_TRIADE_v0.15.0_Specification.pdf",
            "spec/Protocole_TRIADE_v0.15.0_Specification.pdf")
    z.write(REPO / "docs/PROTOCOLE_TRIADE.md", "spec/PROTOCOLE_TRIADE.md")
    n_c += 5
    # les preuves v150 (le modèle, l'invariant, le raffinement)
    for f in P150.iterdir():
        if f.is_file():
            z.write(f, f"preuves_v150/{f.name}")
            n_c += 1
    # les sources des preuves + les chaînes
    for f in (REPO / "scripts").glob("*_v150.py"):
        z.write(f, f"scripts/{f.name}")
        n_c += 1
    # les kits
    for dossier in ("kit_dudect", "kit_fencei", "kit_terrain_tiers"):
        base = REPO / "scripts/kits_mesure_v150" / dossier
        for f in base.rglob("*"):
            if f.is_file():
                z.write(f, f"kits_mesure_v150/{dossier}/"
                        f"{f.relative_to(base)}")
                n_c += 1
    # la réplication
    for f in (REPO / "scripts/replication_v150").iterdir():
        if f.is_file():
            z.write(f, f"replication_v150/{f.name}")
            n_c += 1
    # les données du manuscrit
    for f in DON.iterdir():
        if f.is_file():
            z.write(f, f"donnees/{f.name}")
            n_c += 1
    # les preuves historiques citées
    for base, noms in ((P110, ("mutation.csv", "benchmarks.csv")),
                       (P130, ("audit_benchmark.csv", "stats_v130.csv")),
                       (P140, ("bras_c.csv", "remesure_rq2.csv",
                               "independance_agent.csv",
                               "rejeu_survivants.csv"))):
        for nom in noms:
            z.write(base / nom, f"preuves_historiques/{base.name}/{nom}")
            n_c += 1
    # le README du complet
    z.write(readme_f, "README.txt")

emp_f.write_text(
    "LIVRABLES v0.15.0\n\n"
    f"{sha256(SOUM)}  soumission ({n_s} fichiers)\n"
    f"{sha256(COMP)}  complet ({n_c} entrées)\n"
    f"{sha256(REPO / 'scripts/manuscrit_v150/main.pdf')}  "
    "manuscrit (21 pages, la table des preuves rendue)\n"
    f"{sha256(REPO / 'docs/Protocole_TRIADE_v0.15.0_Specification.pdf')}  "
    "specification (64 pages, consignee n°56)\n"
    f"{sha256(REPO / 'loupe/loupe.exe')}  loupe.exe 0.1.1 (la piece "
    "scellee, INTACTE)\n"
    f"{sha256(REPO / 'tls13/proxy.exe')}  proxy.exe 1.0.0 (la piece "
    "scellee, INTACTE)\n", encoding="utf-8")
# la soumission une dernière fois avec les empreintes à jour
with zipfile.ZipFile(SOUM, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(readme_f, "README.txt")
    z.write(REPO / "scripts/manuscrit_v150/main.pdf",
            "TRIADE_manuscrit_v0.15.0.pdf")
    z.write(csv_f, "tableaux_donnees_v0.15.0.csv")
    z.write(emp_f, "empreintes_livrables.txt")
    z.write(rapport, "rapport_verification_v0.15.0.txt")

print(f"[soumission] {n_s} fichiers · [complet] {n_c} entrées")
print(f"  {SOUM.name} : {SOUM.stat().st_size} o, sha256 {sha256(SOUM)[:16]}…")
print(f"  {COMP.name} : {COMP.stat().st_size} o, sha256 {sha256(COMP)[:16]}…")
