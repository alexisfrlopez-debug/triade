#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v195.py — le pack de présentation v0.19.5 (la clôture de
la vague 7, l'instruction 1c4sokpii). Le linter inter-pièces v195 doit
être VERT avant l'assemblage — le script le vérifie lui-même (échec
fermé). Le montage de la v0.19.4 reconduit."""
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V7 = REPO / "scripts" / "vague7"
PACK = V7 / "pack-v195"
ZIP = V7 / "TRIADE_presentation_v0.19.5_20261120.zip"

# ---- 0. le linter DOIT être vert (le zip est refusé sinon) ----
print("== le linter inter-pièces v195 — le zip est refusé si un contrôle "
      "est rouge")
r = subprocess.run([sys.executable, str(V7 / "linter_v195.py")],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
if r.returncode != 0:
    sys.exit("LE LINTER EST ROUGE — le pack est REFUSÉ.")

# ---- 1. les pièces ----
PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.19.5.pdf",
     REPO / "edition-v0195" / "main.pdf",
     "Le manuscrit scientifique (édition académique, en anglais). La "
     "v0.19.5 est L'ÉDITION DE LA CLÔTURE DE LA VAGUE 7 — née de la "
     "v0.19.4 (le coût de la boucle) : le critère d'échantillon du plan "
     "D210 tenu à N = 7 SANS NOUVEAU TIRAGE (sept unités aux deux bras "
     "lues du registre, l'amendement conditionnel jamais déclenché), la "
     "batterie d'injection de fautes (811/832 tués, 97,5 % — 83,4 % → "
     "93,3 % → 97,5 %, le reste de 21 nommé à treize familles de "
     "causes, AUCUN tueur affaibli), l'indépendance inter-familles au "
     "GAP NOMMÉ (jamais simulé : le local 1,5B récite 0/64 et copie à "
     "la correction ; le bras C généré passe l'épreuve POSIX à "
     "1984/2011), le paquet d'évaluation (la reproduction en une "
     "commande, la grille codée, le protocole du second annotateur "
     "pré-enregistré κ ≥ 0,61, le calculateur autotesté 3/3) — ET LE "
     "STATUT DE GOUVERNANCE PORTÉ À L'ÉTAT VÉCU : la cérémonie D183 "
     "vécue le 19/11, la phrase commise tournée et l'ancienne refusée, "
     "le re-scan trié, le dépôt public D220. AUCUNE valeur mesurée "
     "modifiée."),
    ("2-specification", "Protocole_TRIADE_v0.15.4_Specification.pdf",
     REPO / "scripts" / "spec_v154" / "main.pdf",
     "La spécification technique (Tectonic propre). La v0.15.4 est LE "
     "POINTEUR SEUL : une règle ADDITIVE à l'opération localiser "
     "(l'identifiant d'entrée + l'empreinte sha256 de la notation — deux "
     "champs littéraux ; le client expande, quatre refus nommés "
     "fail-closed), AUCUNE règle existante modifiée (D222 consigne "
     "l'adoption). INCHANGÉE par la v0.19.5 : l'instruction 1c4sokpii "
     "ne touche AUCUNE règle (mesure, évaluation et gouvernance "
     "seulement) — la pièce demeure à son scellé v0.15.4."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf",
     REPO / "scripts" / "livre_v13" / "final.pdf",
     "Le Livre du Coffre v1.3 (28 pages) — INCHANGÉ par la présente "
     "édition : aucun geste de cérémonie ne bouge (le runbook est "
     "scellé aux éditions courantes D180 ; l'entrée du scan périodique "
     "que D220 consigne attend l'édition documentée commandée du "
     "maître — jamais un ajout silencieux)."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.19.5.pdf",
     V7 / "TRIADE_preuves_et_calculs_v0.19.5.pdf",
     "Les preuves et calculs v0.19.5 : les pièces 1c4sokpii verbatim — "
     "le rapport d'instruction (le plan D210 à son terme, le tri des 56 "
     "survivants, la batterie K4 aux seize scénarios, le paquet "
     "d'évaluation), le rapport d'indépendance inter-familles (la "
     "confrontation math↔plan tenue, la récitation pure 0/64 + 0/64, "
     "les rondes de correction copiant, le gap nommé, le bras C à "
     "1984/2011), et le rapport du rejeu des fautes (la console v0.14.0 "
     "reproduite à l'identique, les 35 tués par l'injection, le reste "
     "de 21 nommé)."),
    ("5-presentation", "TRIADE_presentation_20261120_v195.pdf",
     V7 / "TRIADE_presentation_20261120_v195.pdf",
     "La présentation du 20/11 (édition v0.19.5) : la clôture de la "
     "vague 7 — les quatre points de la session, les canons reconduits "
     "(le pointeur seul, le ratio 3,0× — H5 tenue), la table des "
     "statuts, l'état des éditions, la gouvernance vécue (D183), le "
     "dépôt PUBLIC (D220) et le DOI Zenodo vivant."),
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
    "TRIADE — le pack de présentation v0.19.5 (la clôture de la vague "
    "7)\n"
    "==================================================================\n\n"
    "Les cinq documents régénérés de l'édition v0.19.5 — l'instruction\n"
    "1c4sokpii (la vague du 19/11, la cinquième et dernière) : LE PLAN\n"
    "D210 À SON TERME (le critère d'échantillon tenu à N = 7 SANS\n"
    "nouveau tirage — sept unités aux deux bras lues du registre), LA\n"
    "BATTERIE D'INJECTION DE FAUTES (811/832 tués, 97,5 % — 35 tués par\n"
    "l'injection, le reste de 21 NOMMÉ à treize familles de causes,\n"
    "aucun tueur affaibli, la console v0.14.0 reproduite d'abord),\n"
    "L'INDÉPENDANCE INTER-FAMILLES AU GAP NOMMÉ (jamais simulée — la\n"
    "confrontation math↔plan tenue, le local 1,5B récite 0/64 et copie\n"
    "à la correction, le bras C généré à 1984/2011), LE PAQUET\n"
    "D'ÉVALUATION (la reproduction en une commande, la grille codée,\n"
    "le protocole du second annotateur pré-enregistré κ ≥ 0,61, le\n"
    "calculateur autotesté 3/3) — ET LE STATUT DE GOUVERNANCE PORTÉ À\n"
    "L'ÉTAT VÉCU (la cérémonie D183 vécue le 19/11, la phrase tournée\n"
    "et l'ancienne refusée, le re-scan trié, le dépôt public D220). La\n"
    "spécification v0.15.4 et le Livre du Coffre v1.3 demeurent à leur\n"
    "scellé (aucune règle ne bouge, aucun geste de cérémonie ne\n"
    "bouge). AUCUNE valeur mesurée modifiée.\n\n"
    "Le dépôt est PUBLIC (D220) ; le DOI Zenodo vivant :\n"
    "10.5281/zenodo.24367344 — github.com/alexisfrlopez-debug/triade\n",
    encoding="utf-8")

# les empreintes
lignes_emp = ["TRIADE — empreintes du pack v0.19.5 (SHA-256)", "",
              f"{'pièce':52}{'octets':>10}  sha256", "-" * 100]
for nom, taille, h in empreintes:
    lignes_emp.append(f"{nom:52}{taille:>10,}  {h}")
(PACK / "empreintes_livrables_v0.19.5.txt").write_text(
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
    assert len(noms) >= 12, "le zip relu ne porte pas ses pièces"
    for nom, taille, h in empreintes:
        interne = next(n for n in noms if n.endswith(nom))
        donnees = z.read(interne)
        assert hashlib.sha256(donnees).hexdigest() == h, \
            f"la pièce relue diverge : {nom}"
print(f"\n[VERT] le zip relu pièce à pièce : {ZIP} "
      f"[{ZIP.stat().st_size:,} o, {len(noms)} fichiers]")
print("LE PACK v0.19.5 ASSEMBLÉ — le linter vert, les empreintes gravées, "
      "le zip relu : AUCUN contrôle rouge.")
