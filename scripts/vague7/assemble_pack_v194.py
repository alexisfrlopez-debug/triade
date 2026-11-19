#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v194.py — le pack de présentation v0.19.4 (l'instruction
cq01qv1za : « Produis ensuite le pack zip de présentation de 5 documents
régénérés avec empreintes SHA-256 et rapport de vérification ; refuse le
zip si un contrôle est rouge. »). Le linter inter-pièces v194 doit être
VERT avant l'assemblage — le script le vérifie lui-même (échec fermé)."""
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V7 = REPO / "scripts" / "vague7"
PACK = V7 / "pack-v194"
ZIP = V7 / "TRIADE_presentation_v0.19.4_20261120.zip"

# ---- 0. le linter DOIT être vert (le zip est refusé sinon) ----
print("== le linter inter-pièces v194 — le zip est refusé si un contrôle "
      "est rouge")
r = subprocess.run([sys.executable, str(V7 / "linter_v194.py")],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
if r.returncode != 0:
    sys.exit("LE LINTER EST ROUGE — le pack est REFUSÉ.")

# ---- 1. les pièces ----
PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.19.4.pdf",
     REPO / "edition-v0194" / "main.pdf",
     "Le manuscrit scientifique (édition académique, en anglais). La "
     "v0.19.4 est L'ÉDITION DU COÛT DE LA BOUCLE — née de la v0.19.3 "
     "(l'écart fermé) : le pointeur seul adopté au format de réponse de "
     "localiser (OPT-04 : −35,7 % au total, −93,3 % à la réponse, zéro "
     "divergence 18/18, l'expansion côté client à quatre refus nommés), "
     "la pile mémo v2 + double moteur adoptée au chemin de vérification "
     "(la clé étendue fichier + config émulateur + graine, l'audit 1 run "
     "sur 10 à compteur chaîné, QEMU-user au volume et Unicorn à "
     "l'échantillon consigné, divergence 0 sur 2 041 opérations), H5 "
     "DEVENUE TENUE PAR L'INSTRUCTION DU MAÎTRE (le ratio de régime 3,0× "
     "sous le seuil ×10 — la falsification D204 demeure consignée comme "
     "mesurée et datée). AUCUNE valeur mesurée modifiée."),
    ("2-specification", "Protocole_TRIADE_v0.15.4_Specification.pdf",
     REPO / "scripts" / "spec_v154" / "main.pdf",
     "La spécification technique (Tectonic propre). La v0.15.4 est LE "
     "POINTEUR SEUL : une règle ADDITIVE à l'opération localiser "
     "(l'identifiant d'entrée + l'empreinte sha256 de la notation — deux "
     "champs littéraux ; le client expande, quatre refus nommés "
     "fail-closed), AUCUNE règle existante modifiée (D222 consigne "
     "l'adoption) ; la mesure OPT-04 portée à la section « Ce que change "
     "la v0.15.4 »."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf",
     REPO / "scripts" / "livre_v13" / "final.pdf",
     "Le Livre du Coffre v1.3 (28 pages) — INCHANGÉ par la présente "
     "édition : aucun geste de cérémonie ne bouge (le runbook est scellé "
     "aux éditions courantes D180 : l'entrée du scan périodique que D220 "
     "consigne attend l'édition documentée commandée du maître — jamais "
     "un ajout silencieux)."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.19.4.pdf",
     V7 / "TRIADE_preuves_et_calculs_v0.19.4.pdf",
     "Les preuves et calculs v0.19.4 : les pièces OPT-04 verbatim — le "
     "rapport de la campagne pointeur (36 appels réels, les "
     "distributions, la vérification zéro divergence, la re-tokenisation "
     "indépendante), le rapport M4 (les distributions, la réconciliation "
     "D214 sur pièces, le ratio 3,0× et l'énoncé H5, les preuves "
     "d'identité de l'audit), les cinq contrôles négatifs (l'entrée de "
     "cache mutée, le compteur muté, la racine mutée, la clé changée, le "
     "moteur divergent — tous attrapés)."),
    ("5-presentation", "TRIADE_presentation_20261120_v194.pdf",
     V7 / "TRIADE_presentation_20261120_v194.pdf",
     "La présentation du 20/11 (édition v0.19.4) : le coût de la boucle "
     "sous R11 — les trois leviers, la table des statuts (H5 TENUE "
     "depuis OPT-04), l'état des éditions, le dépôt PUBLIC (D220) et le "
     "DOI Zenodo vivant."),
]

if PACK.is_dir():
    shutil.rmtree(PACK)
PACK.mkdir()

empreintes = []
for dossier, nom_livraison, source, description in PIECES:
    if not source.is_file():
        sys.exit(f"[REFUS] la pièce manque : {source}")
    cible = PACK / dossier
    cible.mkdir()
    shutil.copy2(source, cible / nom_livraison)
    h = hashlib.sha256(source.read_bytes()).hexdigest()
    empreintes.append((nom_livraison, source.stat().st_size, h))
    print(f"[VERT] {nom_livraison} [{source.stat().st_size:,} o, "
          f"sha256 {h[:16]}…]")
    (cible / "description.txt").write_text(description + "\n",
                                           encoding="utf-8")

# le LISEZMOI
(PACK / "LISEZMOI.txt").write_text(
    "TRIADE — le pack de présentation v0.19.4 (l'édition du coût de la "
    "boucle)\n"
    "==================================================================\n\n"
    "Les cinq documents régénérés de l'édition v0.19.4 — l'instruction\n"
    "cq01qv1za (la vague du 18/11, la quatrième) : LE POINTEUR SEUL au\n"
    "format de réponse de localiser (l'agent rend l'identifiant et\n"
    "l'empreinte, le client expande — quatre refus nommés), LA PILE\n"
    "MÉMO V2 + DOUBLE MOTEUR au chemin de vérification (la clé étendue\n"
    "fichier + config émulateur + graine, l'audit 1 run sur 10 à\n"
    "compteur chaîné, QEMU-user au volume, Unicorn à l'échantillon\n"
    "consigné — divergence 0 sur 2 041 opérations), H5 DEVENUE TENUE\n"
    "PAR L'INSTRUCTION DU MAÎTRE (le ratio 3,0× sous ×10 ; la\n"
    "falsification D204 demeure consignée). AUCUNE valeur mesurée\n"
    "modifiée, aucune graine supprimée, aucun vecteur réduit, aucune\n"
    "vérification retirée — la preuve : les 24 consoles d'oracles\n"
    "capturées identiques ligne à ligne aux originales.\n\n"
    "Le dépôt est PUBLIC (D220) ; le DOI Zenodo vivant :\n"
    "10.5281/zenodo.24367344 — github.com/alexisfrlopez-debug/triade\n",
    encoding="utf-8")

# les empreintes
lignes_emp = ["TRIADE — empreintes du pack v0.19.4 (SHA-256)", "",
              f"{'pièce':52}{'octets':>10}  sha256", "-" * 100]
for nom, taille, h in empreintes:
    lignes_emp.append(f"{nom:52}{taille:>10,}  {h}")
(PACK / "empreintes_livrables_v0.19.4.txt").write_text(
    "\n".join(lignes_emp) + "\n", encoding="utf-8")
print("\n".join(lignes_emp))

# ---- la relecture du zip (chaque pièce relue, les empreintes re-vérifiées)
if ZIP.exists():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(PACK.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(PACK))
with zipfile.ZipFile(ZIP) as z:
    noms = z.namelist()
    assert len(noms) >= 12, "le zip relelu ne porte pas ses pièces"
    for nom, taille, h in empreintes:
        interne = next(n for n in noms if n.endswith(nom))
        donnees = z.read(interne)
        assert hashlib.sha256(donnees).hexdigest() == h, \
            f"la pièce relue diverge : {nom}"
print(f"\n[VERT] le zip relu pièce à pièce : {ZIP} "
      f"[{ZIP.stat().st_size:,} o, {len(noms)} fichiers]")
print("LE PACK v0.19.4 ASSEMBLÉ — le linter vert, les empreintes gravées, "
      "le zip relu : AUCUN contrôle rouge.")
