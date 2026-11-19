#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v193.py — le pack de présentation v0.19.3 (l'instruction
5ey7gmjra : « Produis ensuite le pack zip de présentation de 5 documents
régénérés avec empreintes SHA-256 et rapport de vérification ; refuse le
zip si un contrôle est rouge. »). Le linter inter-pièces v193 doit être
VERT avant l'assemblage — le script le vérifie lui-même (échec fermé)."""
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/depot")
V7 = REPO / "scripts" / "vague7"
PACK = V7 / "pack-v193"
ZIP = V7 / "TRIADE_presentation_v0.19.3_20261120.zip"

# ---- 0. le linter DOIT être vert (le zip est refusé sinon) ----
print("== le linter inter-pièces v193 — le zip est refusé si un contrôle "
      "est rouge")
r = subprocess.run([sys.executable, str(V7 / "linter_v193.py")],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
if r.returncode != 0:
    sys.exit("LE LINTER EST ROUGE — le pack est REFUSÉ.")

# ---- 1. les pièces ----
PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.19.3.pdf",
     REPO / "edition-v0193" / "main.pdf",
     "Le manuscrit scientifique (édition académique, 31 pages, en anglais). "
     "La v0.19.3 est L'ÉDITION DE L'ÉCART FERMÉ — née de la v0.19.2 (la "
     "transition préparée puis vécue, le dépôt public D220) : le modèle "
     "formel CF3 étendu (la falsification offerte en session ouverte, la "
     "garde alignée sur la sentinelle concrète), la campagne re-jouée à "
     "zéro divergence (30 000 traces, trois graines, le rejeu bit-identique "
     "deux fois, exactement les 660 traces de la classe consignée changées), "
     "l'instrument temps constant promu au hash des traces complètes, le kit "
     "de mesure matérielle pré-enregistré en attente — la table des statuts "
     "portée (écart fermé, preuves non bornées couvrant la falsification en "
     "session, égalité hash-vérifiée, le protocole matériel pré-enregistré). "
     "AUCUNE valeur mesurée modifiée."),
    ("2-specification", "Protocole_TRIADE_v0.15.3_Specification.pdf",
     REPO / "scripts" / "spec_v153" / "final.pdf",
     "La spécification technique (66 pages, Tectonic propre). La v0.15.3 "
     "est L'ALIGNEMENT DU MODÈLE SUR LA RÈGLE : AUCUNE règle modifiée — la "
     "règle disait « seule la falsification prouvée détruit » (destruction "
     "locale, jamais le média ni les fragments) ; le modèle v0.15.0 "
     "sous-approximait (la garde canonique-seule — l'écart des 660 traces), "
     "la v0.15.3 le porte à la lettre : la falsification offerte aux DEUX "
     "phases, la lettre de la sentinelle rendue explicite au § CF3, la "
     "section « Ce que change la v0.15.3 » (les preuves re-déchargées, la "
     "campagne à zéro, l'instrument hash-vérifié, le kit matériel)."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf",
     REPO / "scripts" / "livre_v13" / "final.pdf",
     "Le Livre du Coffre v1.3 (28 pages) — INCHANGÉ par la présente "
     "édition : aucun geste de cérémonie ne bouge (le runbook est scellé "
     "aux éditions courantes D180 : l'entrée du scan périodique que D220 "
     "consigne attend l'édition documentée commandée du maître — jamais "
     "un ajout silencieux)."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.19.3.pdf",
     V7 / "TRIADE_preuves_et_calculs_v0.19.3.pdf",
     "Les preuves et calculs v0.19.3 (9 pages) : les pièces de la session "
     "5ey7gmjra — le diff exact des modules étendus, la batterie 96/96 "
     "(TLC + Apalache, 31 contrôles négatifs attrapés), la campagne 30 000 "
     "traces à zéro divergence (le recoup à la généalogie : exactement les "
     "660 changées), l'égalité hash-vérifiée 6/6 cibles, le kit matériel "
     "pré-enregistré ; les pièces permanentes reconduites (les empreintes "
     "scellées, la plage RQ2, le canon M4, la falsification D219)."),
    ("5-presentation", "TRIADE_presentation_20261120_v193.pdf",
     V7 / "TRIADE_presentation_20261120_v193.pdf",
     "La présentation du 20/11 (édition v0.19.3, 7 pages) : l'écart fermé, "
     "la batterie 96/96, la campagne à zéro, l'égalité hash-vérifiée, le "
     "protocole matériel pré-enregistré — et la lignée des éditions (la "
     "transition D183 préparée D219 puis VÉCUE, le dépôt PUBLIC D220, la "
     "matrice de visibilité honorée jusqu'à sa dernière marche)."),
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

# le LISEZMOI
lisezmoi = PACK / "LISEZMOI.txt"
lisezmoi.write_text(
    "TRIADE — le pack de présentation v0.19.3 (l'édition de l'écart fermé)\n"
    "====================================================================\n"
    "\n"
    "Les cinq documents régénérés de l'édition v0.19.3 — l'instruction\n"
    "5ey7gmjra (la vague du 18/11, la troisième) : le modèle formel CF3\n"
    "étendu (la falsification du conteneur offerte pendant une session\n"
    "ouverte — la garde alignée sur la sentinelle concrète : destruction\n"
    "locale sur falsification prouvée, le média et les fragments\n"
    "intacts), la campagne générative re-jouée à ZÉRO divergence (30 000\n"
    "traces aux trois graines, le rejeu bit-identique deux fois — contre\n"
    "le registre v0.18.0 : exactement les 660 traces de la classe\n"
    "consignée changées, rien d'autre), les preuves non bornées\n"
    "re-déchargées sur le modèle étendu (96/96 vert, 31 contrôles\n"
    "négatifs attrapés), l'instrument temps constant promu au HASH des\n"
    "traces complètes (une seule empreinte par cible sur 120 mesures),\n"
    "et le kit de mesure matérielle pré-enregistré EN ATTENTE (n>=10\n"
    "runs par N, >=2 machines, aucun chiffre fabriqué).\n"
    "\n"
    "Le dépôt GitHub est PUBLIC (le passage vécu le 19/11/2026, D220, à\n"
    "la décision explicite du développeur) : github.com/alexisfrlopez-"
    "debug/triade — et le DOI Zenodo vit : 10.5281/zenodo.24367344.\n"
    "\n"
    "LES PIÈCES :\n", encoding="utf-8")
with open(lisezmoi, "a", encoding="utf-8") as f:
    for dossier, nom, source, desc in PIECES:
        f.write(f"\n--- {dossier}/{nom}\n{desc}\n")
f_emp = PACK / "empreintes_livrables_v0.19.3.txt"
with open(f_emp, "w", encoding="utf-8") as f:
    f.write("LES EMPREINTES SHA-256 DES LIVRABLES v0.19.3 "
            "(générées le 2026-11-19)\n")
    f.write("=" * 64 + "\n\n")
    for nom, taille, h in empreintes:
        f.write(f"{h}  {nom}  [{taille:,} octets]\n".replace(",", " "))

# le zip
if ZIP.is_file():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(REPO / "LICENSE", "LICENSE")
    for p_ in sorted(PACK.rglob("*")):
        if p_.is_file():
            z.write(p_, str(p_.relative_to(PACK)))

# la relecture du zip (chaque pièce relue, les empreintes re-vérifiées)
with zipfile.ZipFile(ZIP) as z:
    noms = z.namelist()
    for nom, taille, h in empreintes:
        donnees = z.read(next(n for n in noms if n.endswith(nom)))
        assert hashlib.sha256(donnees).hexdigest() == h, f"RELECTURE {nom}"
print(f"\n[VERT] le zip relu : {len(noms)} entrées, chaque empreinte "
      f"re-vérifiée")
print(f"[VERT] {ZIP} [{ZIP.stat().st_size:,} o, sha256 "
      f"{hashlib.sha256(ZIP.read_bytes()).hexdigest()}]".replace(",", " "))
