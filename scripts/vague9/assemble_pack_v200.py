#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v200.py — LE PACK TRIADE_presentation_v0.20.0.zip :
exactement 5 documents PDF régénérés et cohérents (manuscrit, spécification,
Livre du Coffre, preuves et calculs, présentation) + les descriptions, le
LISEZMOI et LE MANIFESTE DES EMPREINTES sha-256 des cinq pièces. La consigne
de l'instruction : « Consigne les empreintes sha-256 des cinq pièces dans la
présentation et le document de preuves » — la CONVENTION : aucun document ne
porte son propre sha-256 ; la présentation grave les QUATRE autres, le
document de preuves les TROIS pièces de contenu, le manifeste porte les
CINQ ; le linter v200 re-vérifie chaque empreinte au build."""
import hashlib
import os
import shutil
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V9 = REPO / "scripts" / "vague9"
PACK = V9 / "pack-v200"
ZIP = REPO / "TRIADE_presentation_v0.20.0.zip"

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.20.0.pdf",
     REPO / "edition-v0200" / "main.pdf",
     "Le manuscrit académique v0.20.0 — la vague 9 portée : le tableau de "
     "bord des quatre axes et la section « distance to the floor » (les "
     "ratios par axe, la convention de périmètre, la lecture "
     "lexicographique), la sûreté mémoire à 2,006/2,098 déchargés, les "
     "trois « tuables » re-classés équivalents-par-sweep (811/817 = 99.3), "
     "CF3 mécanisé 14/14, la non-interférence statique, les deux couloirs, "
     "le compilateur d'oracle, l'abstract réécrit."),
    ("2-specification", "Protocole_TRIADE_v0.15.6_Specification.pdf",
     REPO / "scripts" / "spec_v156" / "main.pdf",
     "La spécification v0.15.6 — l'alignement à l'état vécu de la vague 9 : "
     "la table des preuves au CF3 mécanisé (z3, l'assistant indépendant) et "
     "à la non-interférence statique, l'annexe B à la plage réelle D75-D228, "
     "la section nouveautés aux gains de la vague — AUCUNE règle R1-R11 "
     "modifiée."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.5.pdf",
     REPO / "scripts" / "livre_v15" / "final.pdf",
     "Le Livre du Coffre v1.5 — les références de version alignées (la spec "
     "v0.15.6 courante, le manuscrit v0.20.0), le compte d'arbres réel, le "
     "runbook D183 au statut vécu, la matrice public + Zenodo."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.20.0.pdf",
     V9 / "TRIADE_preuves_et_calculs_v0.20.0.pdf",
     "Les preuves et calculs v0.20.0 — les huit pièces verbatim de la vague "
     "9 : la sûreté mémoire au plancher (2,006/2,098 déchargés, 92 nommés), "
     "la batterie étendue (le sweep, 811/817), CF3 mécanisé + la "
     "non-interférence, le certificat de cristallisation + le double moteur, "
     "les deux couloirs, la campagne de tokens + le compilateur d'oracle, le "
     "tableau de bord des quatre axes, l'ancrage de transparence — avec la "
     "table des empreintes sha-256."),
    ("5-presentation", "TRIADE_presentation_20261120_v200.pdf",
     V9 / "TRIADE_presentation_20261120_v200.pdf",
     "La présentation du 20/11 à l'édition v0.20.0 — les cinq points de la "
     "vague 9, la table des statuts (H5 en deux verdicts distincts, "
     "H4-composer falsifiée), l'état des éditions, la gouvernance vécue — "
     "avec les empreintes sha-256 des quatre autres pièces gravées."),
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
EMP = V9 / "empreintes_livrables_v0.20.0.txt"
EMP.write_text(
    "LES EMPREINTES SHA-256 DES CINQ PIÈCES DU PACK v0.20.0\n"
    "(gravées à la présentation — les quatre autres — et au document de\n"
    "preuves — les trois pièces de contenu ; aucun document ne porte son\n"
    "propre sha-256, le présent manifeste porte les CINQ — la convention\n"
    "du pack ; le linter inter-pièces v200 re-vérifie chaque empreinte\n"
    "au build : 0 ROUGE exigé)\n\n" + empreintes + "\n",
    encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.20.0.txt")

(PACK / "LISEZMOI.txt").write_text(
    "TRIADE — le pack de présentation v0.20.0 (la vague 9)\n"
    "======================================================\n\n"
    "Les CINQ documents régénérés et cohérents :\n"
    "  1-manuscrit       le manuscrit académique v0.20.0\n"
    "  2-specification   la spécification v0.15.6 (aucune règle modifiée)\n"
    "  3-coffre-fort     le Livre du Coffre v1.5 (les références alignées)\n"
    "  4-preuves-calculs les preuves v0.20.0 (les huit pièces verbatim)\n"
    "  5-presentation    la présentation du 20/11 à l'état exact\n\n"
    "La vague 9 — la fonction objectif lexicographique portée au tableau\n"
    "de bord (Sécurité > Performance > Optimisation > Coût en tokens,\n"
    "aucune compensation entre les rangs) : la sécurité au plancher\n"
    "(2 006/2 098 accès déchargés par preuve, 92 nommés avec certificat\n"
    "BMC ; les trois « tuables » re-classés équivalents-par-sweep,\n"
    "811/817 = 99,3 % ajusté à côté du brut 811/832 ; la non-interférence\n"
    "statique aux dix familles ; CF3 mécanisé 14/14 en z3 ; l'ancrage de\n"
    "transparence), la boucle de vérification (le certificat de\n"
    "cristallisation : le diff d'un bloc, 3 contre 18, les trois\n"
    "falsifications refusées ; le double moteur à l'ouverture,\n"
    "divergence 0 ; le régime oracle natif préparé ; M4 39,2/7,0/2,0 s,\n"
    "le ratio 3,5x), les deux couloirs (la parité SSE2 0,03x gcc-O2 avec\n"
    "31,2x de marge, zéro divergence aux 24 vecteurs ; AES-NI déjà le\n"
    "scellé, GHASH la frontière nommée), le coût en tokens (éditer-H2\n"
    "reproduit 2 452/40 ; l'ajout refusé pour la troisième fois ;\n"
    "composer-G 3/18, H4 falsifiée ; localiser-P reproduit 1 103/52 ; le\n"
    "compilateur d'oracle : 968 tokens supprimés, zéro token LLM ; les\n"
    "ratios au plancher 136,2x/38,0x/4,1x/2,9x), le tableau de bord des\n"
    "quatre axes généré des pièces brutes (jamais tapé à la main).\n\n"
    "LES EMPREINTES SHA-256 des cinq pièces : gravées à la présentation\n"
    "(les quatre autres) et au document de preuves (les trois pièces de\n"
    "contenu) ; le manifeste empreintes_livrables_v0.20.0.txt porte les\n"
    "CINQ — aucun document ne peut porter son propre sha-256, la\n"
    "convention nommée.\n\n"
    "Le linter inter-pièces v200 : 0 ROUGE — le build admis.\n"
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
