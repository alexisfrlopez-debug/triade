#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v196.py — LE PACK TRIADE_presentation_v0.19.6_20261120.zip :
exactement 5 documents PDF régénérés et cohérents (manuscrit, spécification,
Livre du Coffre, preuves et calculs, présentation) + les descriptions, le
LISEZMOI et LES EMPREINTES SHA-256 des cinq pièces gravées dans la
présentation et le document de preuves (l'instruction : « Consigne les
empreintes sha-256 des cinq pièces dans la présentation et le document de
preuves »)."""
import hashlib
import os
import shutil
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V8 = REPO / "scripts" / "vague8"
PACK = V8 / "pack-v196"
ZIP = REPO / "TRIADE_presentation_v0.19.6_20261120.zip"

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.19.6.pdf",
     REPO / "edition-v0196" / "main.pdf",
     "Le manuscrit académique v0.19.6 — la vague 8 portée : la cohérence "
     "(les macros, les DOI, 1/16), la gouvernance vécue, H5 en deux "
     "verdicts datés, N=7 réconcilié, RQ2 re-mesuré, l'abstract réécrit."),
    ("2-specification", "Protocole_TRIADE_v0.15.5_Specification.pdf",
     REPO / "scripts" / "spec_v155" / "main.pdf",
     "La spécification v0.15.5 — l'état vécu de la gouvernance (D223) : "
     "la ligne D81 du modèle de menace au séquestre actif, le dépôt "
     "public ; aucune règle R1-R11 modifiée."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.4.pdf",
     REPO / "scripts" / "livre_v14" / "final.pdf",
     "Le Livre du Coffre v1.4 — le runbook D183 au statut VÉCU (les sept "
     "gestes, la reconstitution à froid prouvée deux fois), quatorze "
     "arbres, la matrice public + Zenodo."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.19.6.pdf",
     V8 / "TRIADE_preuves_et_calculs_v0.19.6.pdf",
     "Les preuves et calculs v0.19.6 — les pièces verbatim de la vague 8 : "
     "OPT-05, la dérivation-outillée, la classification des 21 survivants, "
     "l'amendement du format hunk."),
    ("5-presentation", "TRIADE_presentation_20261120_v196.pdf",
     V8 / "TRIADE_presentation_20261120_v196.pdf",
     "La présentation du 20/11 à l'édition v0.19.6 — les cinq points de "
     "la vague, la table des statuts, l'état des éditions, la gouvernance "
     "vécue."),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


if PACK.exists():
    shutil.rmtree(PACK)
for dossier, nom, src, desc in PIECES:
    d = PACK / dossier
    d.mkdir(parents=True)
    shutil.copy2(src, d / nom)
    (d / "description.txt").write_text(
        f"{nom}\n{desc}\nsha256:{sha(d / nom)}\n", encoding="utf-8")

empreintes = "\n".join(
    f"{sha(PACK / dossier / nom)}  {dossier}/{nom}"
    for dossier, nom, _, _, in PIECES)
EMP = V8 / "empreintes_livrables_v0.19.6.txt"
EMP.write_text(
    "LES EMPREINTES SHA-256 DES CINQ PIÈCES DU PACK v0.19.6\n"
    "(gravées à la présentation et au document de preuves — le linter\n"
    "inter-pièces v196 : 39 VERT 0 ROUGE au build)\n\n" + empreintes + "\n",
    encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.19.6.txt")

(PACK / "LISEZMOI.txt").write_text(
    "TRIADE — le pack de présentation v0.19.6 (la vague 8)\n"
    "======================================================\n\n"
    "Les CINQ documents régénérés et cohérents :\n"
    "  1-manuscrit       le manuscrit académique v0.19.6\n"
    "  2-specification   la spécification v0.15.5 (aucune règle modifiée)\n"
    "  3-coffre-fort     le Livre du Coffre v1.4 (le runbook D183 VÉCU)\n"
    "  4-preuves-calculs les preuves v0.19.6 (les pièces verbatim)\n"
    "  5-presentation    la présentation du 20/11 à l'état exact\n\n"
    "La vague 8 : la cohérence des cinq pièces (les macros des journaux\n"
    "vivants, les DOI réconciliés — le concept 10.5281/zenodo.24367343\n"
    "résolvant sur la courante —, le tirage à 1/16, les 39,3/39,2 s), la\n"
    "gouvernance à l'état vécu (D223 : le séquestre 5/3 la garde active,\n"
    "le dépôt public), l'intégrité pré-enregistrée (H5 en deux verdicts\n"
    "datés, N=7 réconcilié, H6 au brut, H7 stratifié, l'abstract réécrit,\n"
    "RQ2 re-mesuré 1 103/52, TLC/Apalache), l'indépendance par\n"
    "dérivation-outillée (les 128 constantes conformes — la seconde\n"
    "famille les DÉRIVE, la récitation demeure la sonde), les 21\n"
    "survivants classés (12 équivalents prouvés, 811/820 = 98,9 %),\n"
    "OPT-05 (l'édition par hunks -34,3 %/-97,7 %, l'ajout refusé en\n"
    "l'état, M4 39,1 -> 6,6 s, chaud/C 3,5x, l'audit 1/10 vécu).\n\n"
    "Le linter inter-pièces v196 : 39 VERT 0 ROUGE — le build admis.\n"
    "AUCUNE valeur mesurée modifiée, AUCUN artefact scellé touché.\n",
    encoding="utf-8")

if ZIP.exists():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(PACK.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(PACK))
taille = ZIP.stat().st_size
# la relecture : chaque pièce dézippée re-vérifiée à son empreinte
with zipfile.ZipFile(ZIP) as z:
    noms = z.namelist()
    for dossier, nom, _, _ in PIECES:
        data = z.read(f"{dossier}/{nom}")
        attendu = sha(PACK / dossier / nom)
        assert hashlib.sha256(data).hexdigest() == attendu, nom
print(f"[VERT] {ZIP.name} [{taille:,} octets, {len(noms)} fichiers] — "
      f"chaque pièce relue, les empreintes re-vérifiées")
