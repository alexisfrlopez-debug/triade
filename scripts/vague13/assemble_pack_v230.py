#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v230.py — LE PACK TRIADE_presentation_v0.23.0.zip (12
fichiers : les 5 documents PDF régénérés et cohérents, les descriptions,
le LISEZMOI, LE MANIFESTE DES EMPREINTES). Le zip RELU pièce à pièce
après l'assemblage (chaque empreinte re-vérifiée au dézippage)."""
import hashlib
import pathlib
import shutil
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V13 = REPO / "scripts" / "vague13"
PACK = V13 / "pack-v230"
if PACK.exists():
    shutil.rmtree(PACK)
PACK.mkdir(parents=True)
ZIP = REPO / "TRIADE_presentation_v0.23.0.zip"

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.23.0.pdf",
     REPO / "edition-v0230" / "main.pdf",
     "Le manuscrit académique v0.23.0 — la génération de la vague 13 : "
     "les six écarts du pack v0.22.0 portés aux pièces (la partition "
     "exacte de la batterie 559 — 16+3+4+13+3+8+512, la liste nominale "
     "des longueurs, les opérandes non arrondis de chaque ratio, le "
     "canon du cache recomposé 285.725 → 0.418 ms = ×683,6), les "
     "abstracts EN et FR générés des MÊMES macros, la table canonique "
     "des budgets adoptés, la voix « présent édition » unique et le "
     "changelog gelé des vagues v0.14.0 → v0.23.0, les résultats de la "
     "vague 13 (le couloir GHASH PCLMULQDQ à 63-64 cycles contre le "
     "scellé 806, l'AES-GCM complet face à OpenSSL EVP, la ventilation "
     "quatre bras aux volumes égalisés, la requalification des 58 "
     "gardes et des 15 exclusions, le Tamarin v2, TPL-ADD-v3)."),
    ("2-specification", "Protocole_TRIADE_v0.15.8_Specification.pdf",
     REPO / "scripts" / "spec_v158" / "main.pdf",
     "La spécification v0.15.8 — la purge sémantique D81 au vocabulaire "
     "élargi (h66o54pjd : le recensement exhaustif, les phrases cassées "
     "réécrites, les métadonnées v1.7/v0.15.8, D236 à l'annexe B ; la "
     "reprise : le Tableau 19 du dashboard aligné sur la table canonique "
     "des budgets adoptés, l'annexe B réalignée sur le journal des "
     "décisions, la rangée D251)."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf",
     REPO / "scripts" / "livre_v17" / "final.pdf",
     "Le Livre du Coffre v1.7 — la purge sémantique v13 (h66o54pjd : le "
     "recensement exhaustif au vocabulaire élargi, les résidus corrigés "
     "vers la garde active D223, les phrases cassées réécrites par "
     "réécriture complète, les métadonnées v1.7, la plage décisionnelle "
     "D75-D250 ; PDF reconstruit, 29 p.)."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.23.0.pdf",
     V13 / "TRIADE_preuves_et_calculs_v0.23.0.pdf",
     "Les preuves et calculs v0.23.0 — les pièces de la vague 13 lues "
     "VERBATIM de leurs rapports (le GHASH PCLMULQDQ, la requalification "
     "des gardes et des exclusions, la ventilation quatre bras, "
     "TPL-ADD-v3, la purge v13, le lifter, les médianes, les kits) + "
     "L'ERRATUM de la partition 559 (la coquille « 64+3 » qui sommait à "
     "607, la partition exacte publiée) + la table des empreintes des "
     "cinq pièces."),
    ("5-presentation", "TRIADE_presentation_v230.pdf",
     V13 / "TRIADE_presentation_v230.pdf",
     "La présentation v230 — les points de la vague 13 (le couloir "
     "GHASH, la requalification, la ventilation, TPL-ADD-v3, la purge "
     "v13, la génération v0.23.0), la table des statuts, LES EMPREINTES "
     "SHA-256 DES QUATRE AUTRES PIÈCES GRAVÉES (la convention : aucun "
     "document ne porte son propre sha-256, le manifeste du pack porte "
     "les cinq)."),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


manifest = ["LE MANIFESTE DES EMPREINTES — le pack TRIADE v0.23.0 (la vague 13)",
            "(chaque empreinte RECALCULÉE du fichier même — le linter "
            "re-vérifie)", ""]
for dossier, nom, source, description in PIECES:
    d = PACK / dossier
    d.mkdir()
    shutil.copy2(source, d / nom)
    (d / "description.txt").write_text(description + "\n",
                                       encoding="utf-8")
    manifest.append(f"{sha(d / nom)}  {nom}")
    print(f"[pièce] {nom} ({pathlib.Path(source).stat().st_size} o)")

EMP = V13 / "empreintes_livrables_v0.23.0.txt"
EMP.write_text("\n".join(manifest) + "\n", encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.23.0.txt")

(PACK / "LISEZMOI.txt").write_text(
    "LE PACK DE PRÉSENTATION TRIADE v0.23.0 — la vague 13\n"
    "====================================================\n\n"
    "LES CINQ DOCUMENTS : le manuscrit académique v0.23.0 (la génération "
    "aux six écarts corrigés, la voix « présent édition », le changelog "
    "gelé), la spécification v0.15.8 (la purge sémantique, le dashboard "
    "aligné), le Livre du Coffre v1.7 (la purge v13), les preuves et "
    "calculs v0.23.0 (les pièces verbatim + l'erratum de la partition "
    "559 + la table des empreintes), la présentation v230 (les points de "
    "la vague, la table des statuts, les empreintes gravées).\n\n"
    "LA CONVENTION DES EMPREINTES : aucun document ne porte son propre "
    "sha-256 ; la présentation grave les quatre autres ; le document de "
    "preuves grave les trois pièces de contenu ; CE manifeste porte les "
    "cinq.\n\n"
    "LES SIX INSTRUCTIONS DE LA VAGUE 13 exécutées aux plans gelés avant "
    "toute mesure (le commit b2fbcf8, EMPREINTES-PLANS-VAGUE13.txt) : "
    "0g3400vql (le couloir GHASH PCLMULQDQ et l'AES-GCM complet face à "
    "OpenSSL EVP), q8kugkpdu (les trois requalifications : les 58 "
    "gardes, les 15 exclusions, le Tamarin v2), 5nwnwoceo (TPL-ADD-v3 : "
    "la grammaire et la boucle de réparation), ay6zuzm8o (H-CGP3 : la "
    "ventilation quatre bras aux volumes égalisés), ylrzmlbn8 (la "
    "génération v0.23.0 : les écarts (a)-(f), les abstracts aux mêmes "
    "macros, le refactoring), h66o54pjd (la purge v13 : le Livre v1.7, "
    "la spec v0.15.8, la garde pre-commit/push).\n\n"
    "LA REPRISE : la session morte au recyclage du bac laissa la "
    "génération inachevée — la reprise porta les en-têtes périmés, la "
    "coquille « 599 », la clause dupliquée du résumé FR, la disponibilité "
    "des données, l'annexe B de la spec désalignée, l'abstract EN resté "
    "à l'état v0.22.0 — chaque constat nommé, chaque geste ancré.\n\n"
    "LES GAPS NOMMÉS (jamais simulés) : la cible TPL-ADD-v3 (≥ 17/18) "
    "manquée à 6/18 — le gap résiduel par classe de refus ; la seconde "
    "machine (une seule au bac) ; le plancher de débit mesuré sur la "
    "machine virtualisée ; tamarin-prover absent du bac (le modèle v2 "
    "hashé, aucun verdict fabriqué) ; la réplication indépendante à "
    "mener.\n",
    encoding="utf-8")

# ---- le zip + la RELECTURE pièce à pièce --------------------------------
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(PACK.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(PACK))
ok = 0
with zipfile.ZipFile(ZIP) as z:
    for info in z.infolist():
        data = z.read(info)
        chemin = PACK / info.filename
        if chemin.is_file() and hashlib.sha256(data).hexdigest() == \
                sha(chemin):
            ok += 1
        else:
            raise SystemExit(f"DIVERGENCE au dézippage : {info.filename}")
print(f"[pack] {ZIP.name} : {ZIP.stat().st_size} o, "
      f"{ok} fichiers re-vérifiés au dézippage")
h = hashlib.sha256(ZIP.read_bytes()).hexdigest()
print(f"[pack] sha256 {h}")
