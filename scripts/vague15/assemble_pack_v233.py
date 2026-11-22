#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v233.py — LE PACK TRIADE_presentation_v0.23.3.zip (12
fichiers : les 5 documents PDF régénérés et cohérents, les descriptions,
le LISEZMOI, LE MANIFESTE DES EMPREINTES). Le zip REFUSÉ si un contrôle
est rouge — le linter v233 (LES CINQ CLASSES v2 INTÉGRÉES) EXIGÉ vert
avant l'assemblage (échec fermé). Le zip RELU pièce à pièce après
l'assemblage (chaque empreinte re-vérifiée au dézippage)."""
import hashlib
import pathlib
import shutil
import subprocess
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V15 = REPO / "scripts" / "vague15"
PACK = V15 / "pack-v233"
if PACK.exists():
    shutil.rmtree(PACK)
PACK.mkdir(parents=True)
ZIP = REPO / "TRIADE_presentation_v0.23.3.zip"

# (0) LE LINTER EXIGÉ VERT AVANT L'ASSEMBLAGE (le refus ferme)
print("[0] le linter v233 exigé vert avant l'assemblage…")
r = subprocess.run([sys.executable, str(V15 / "linter_v233.py")],
                   capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout[-2000:])
    raise SystemExit("LE LINTER v233 ROUGE — le pack REFUSÉ")
print("    le linter : VERT")

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.23.3.pdf",
     REPO / "edition-v0230" / "main.pdf",
     "Le manuscrit académique v0.23.3 — la release de la vague 15 : les "
     "cinq pièces régénérées sous le linter v2 à cinq classes (les "
     "phrases sémantiques retirées de la spec §1 — le compilateur N'EST "
     "JAMAIS LIVRÉ, la notation scellée l'est —, les plages "
     "décisionnelles, les faisabilités n/18 datées partout avec la "
     "campagne v5 (nov. 2026) nommée à part à 5/18 LA CIBLE MANQUÉE, le "
     "claim de version à la v0.23.2 courante, les gallicismes EN guéris), "
     "la vague 15 portée au corps (la composition 0.7271 c/octet@4096 "
     "aux opérandes en ligne — la cible ≤2.0 tenue au 36 %, OpenSSL EVP "
     "0.5757 à 1.26×, la chaîne scellée 68.7× derrière —, le TCB "
     "58→34→11 et le corridor des onze, le moteur d'oracles natif à "
     "5189×, TPL-ADD-v5 à 5/18 avec la lecture défavorable consignée, H7 "
     "servie, CF3-v3 au verdict machine, l'écosystème d'adoption), le "
     "changelog gelé aux lignes v0.23.2 et v0.23.3, la disponibilité des "
     "données au DOI 24442951."),
    ("2-specification", "Protocole_TRIADE_v0.15.8_Specification.pdf",
     REPO / "scripts" / "spec_v158" / "main.pdf",
     "La spécification v0.15.8 — reconstruite aux sources de la release "
     "v0.23.3 : la phrase sémantique retirée du §1 (la formulation "
     "exacte : le compilateur n'est jamais livré, la notation scellée "
     "l'est), les DEUX citations historiques reformulées sans la forme "
     "littérale, les séquences de faisabilité datées au Tableau 19 "
     "(jusqu'à 7/18 à la vague 14, la campagne v5 nommée à part à 5/18 "
     "la cible manquée consignée), les 18/18 datés aux annexe B et "
     "corps."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf",
     REPO / "scripts" / "livre_v17" / "final.pdf",
     "Le Livre du Coffre v1.7 — reconstruit : la date de couverture "
     "alignée sur la génération v0.23.3 (23 novembre 2026), le bandeau "
     "« Version 1.7 », §10.1 v0.15.8, le chapitre 11 D75–D250."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.23.3.pdf",
     V15 / "TRIADE_preuves_et_calculs_v0.23.3.pdf",
     "Les preuves et calculs v0.23.3 — les pièces des DIX-SEPT ateliers "
     "de la quinzième vague lues VERBATIM de leurs rapports (les quatre "
     "de l'Entrée 386 : CF3-vers-le-verdict, la mesure de composition, "
     "l'outil feedback, le triage ; les treize de l'Entrée 387 : le TCB "
     "58→34→11, le moteur d'oracles, TPL-ADD-v5, la validité externe, le "
     "trio D122, le corpus, le gym, l'eval, le guide, la doc EN, le kit, "
     "les protocoles matériels, le linter v2) + LA CONSIGNATION DE LA "
     "GÉNÉRATION + LES DEUX ERRATA DE PASSE NOMMÉS (le rejeu TCB à "
     "l'invocation corrigée — l'erratum append-only porté verbatim —, "
     "les splits du corpus recomptés des fichiers livrés 28/4/4 · "
     "77/16/16 contre les comptes de première passe au rapport) + la "
     "table des empreintes des cinq pièces."),
    ("5-presentation", "TRIADE_presentation_v233.pdf",
     V15 / "TRIADE_presentation_v233.pdf",
     "La présentation v233 — les sept points de la vague 15 (la "
     "composition 0,7271, le TCB 58→34→11 et le corridor des onze, le "
     "moteur d'oracles natif 5189×, TPL-ADD-v5 à sa cible manquée "
     "consignée, la validité externe servie, CF3-v3 au verdict machine, "
     "l'écosystème d'adoption et la génération), l'état des éditions, "
     "les gaps nommés, LES EMPREINTES SHA-256 DES QUATRE AUTRES PIÈCES "
     "GRAVÉES (la convention : aucun document ne porte son propre "
     "sha-256, le manifeste du pack porte les cinq)."),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


manifest = ["LE MANIFESTE DES EMPREINTES — le pack TRIADE v0.23.3 (la "
            "vague 15, la release)",
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

EMP = V15 / "empreintes_livrables_v0.23.3.txt"
EMP.write_text("\n".join(manifest) + "\n", encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.23.3.txt")

(PACK / "LISEZMOI.txt").write_text(
    "LE PACK DE PRÉSENTATION TRIADE v0.23.3 — la vague 15, la release\n"
    "===========================================================\n\n"
    "LES CINQ DOCUMENTS : le manuscrit académique v0.23.3 (les cinq "
    "classes du linter v2 portées aux sources, la vague 15 au corps), la "
    "spécification v0.15.8 (la phrase sémantique retirée, les "
    "faisabilités datées), le Livre du Coffre v1.7 (la date alignée), "
    "les preuves et calculs v0.23.3 (les dix-sept rapports verbatim + "
    "les deux errata de passe nommés + la table des empreintes), la "
    "présentation v233 (les sept points, l'état des éditions, les "
    "empreintes gravées).\n\n"
    "LA RELEASE DE LA VAGUE 15 : la vague close à l'Entrée 387 (les "
    "dix-sept instructions exécutées en deux sessions, les instructions "
    "archivées au coffre, le /instructions laissé vide), la commande du "
    "maître (« ok pour la suite (release de la vague etc…) ») commande "
    "la présente : les CINQ PIÈCES RÉGÉNÉRÉES sous le linter v2 de "
    "vxf37231r (les cinq classes : les phrases sémantiques, les plages "
    "décisionnelles, les faisabilités datées, les claims de version "
    "post-dépôt, les gallicismes EN — le contrôle négatif 5/5 vécu à "
    "l'atelier, les onze refus vécus à la chaîne intégrée), les TROIS "
    "PACKS assemblés à la version courante, la version publiée au "
    "concept Zenodo.\n\n"
    "LA CONVENTION DES EMPREINTES : aucun document ne porte son propre "
    "sha-256 ; la présentation grave les quatre autres ; le document de "
    "preuves grave les trois pièces de contenu ; CE manifeste porte les "
    "cinq.\n\n"
    "LES GAPS NOMMÉS (jamais simulés) : la cible TPL-ADD-v5 (≥ 15/18) "
    "manquée à 5/18 (la variance du sujet au CLI nommée, les juges "
    "intacts) ; les cinq lemmas au mur de mémoire 4 Go du bac (L3 "
    "vérifié, la voie du poste réel nommée) ; la cible ≤ 1 % du coût "
    "des gardes au kit terrain ; les 28 livraisons H7, l'annotateur, "
    "l'endpoint de la seconde famille, les machines du dudect, la carte "
    "RV64 — au geste du maître ; les sept fragments EN restants et le "
    "miroir FR de la doc ; les dépôts Zenodo du kit et du corpus.\n",
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
