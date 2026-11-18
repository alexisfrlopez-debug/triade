#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v191.py — le pack de présentation v0.19.1 (l'instruction 376f15f18 :
« un pack zip de présentation de 5 documents régénérés [...] avec le fichier
empreintes SHA-256 recalculées et le rapport de vérification. Le zip est refusé
si un seul contrôle est rouge. »). Le linter inter-pièces doit être VERT avant
l'assemblage — le script le vérifie lui-même (échec fermé)."""
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/work/repo-probe/triade")
V7 = REPO / "scripts" / "vague7"
PACK = V7 / "pack-v191"
ZIP = V7 / "TRIADE_presentation_v0.19.1_20261120.zip"

# ---- 0. le linter inter-pièces DOIT être vert (le zip est refusé sinon) ----
print("== le linter inter-pièces (le zip est refusé si un contrôle est rouge)")
r = subprocess.run([sys.executable, str(V7 / "linter_interpieces.py")],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
if r.returncode != 0:
    sys.exit("LE LINTER EST ROUGE — le pack est REFUSÉ.")

# ---- 1. les pièces à leurs noms de livraison ----
PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.19.1.pdf",
     REPO / "edition-v0191" / "main.pdf",
     "Le manuscrit scientifique (édition académique, 30 pages, en anglais) : le protocole, "
     "les campagnes D204/D210 closes, les résultats. La v0.19.1 est L'ÉDITION COURANTE — "
     "née de la v0.19.0 (l'Entrée 358 : la clôture D210, la lecture de l'attribution, les "
     "lignes M3), c'est l'ÉDITION DE COHÉRENCE INTER-PIÈCES (D218) : la référence à la "
     "spécification courante v0.15.1, les tailles des artefacts scellés passeur re-hachées "
     "aux octets livrés (61 952 / 102 390 o — les tailles v1 défaillantes étaient appariées "
     "aux hash v2+), les énoncés de timing matériel alignés sur les runs dudect SIGNÉS du "
     "13/11. AUCUNE valeur mesurée modifiée."),
    ("2-specification", "Protocole_TRIADE_v0.15.1_Specification.pdf",
     REPO / "scripts" / "spec_v151" / "final.pdf",
     "La spécification technique COMPLÈTE du protocole (66 pages) : les trois couches, les "
     "onze règles, les profils, le coffre-fort CF1-CF3, la gouvernance et le journal des "
     "décisions. La v0.15.1 est L'ÉDITION DE COHÉRENCE (D218) : AUCUNE règle modifiée — le "
     "douzième run VÉCU ET SCELLÉ porté au §16 (D181, l'Entrée 222), D19 requalifiée "
     "POLITIQUE DE PROJET (D182), les QUATORZE arbres signés au §12.4 (D177), le titre réel "
     "de l'annexe décisionnelle D75-D198, les budgets §4 annotés HISTORIQUES contre les "
     "mesures v0.17-v0.18 (D195)."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.2.pdf",
     REPO / "scripts" / "livre_v12" / "final.pdf",
     "Le livre opératoire du coffre-fort (27 pages) : les cérémonies, le runbook de "
     "migration CF1 vers CF3, le mode dégradé, les obligations par niveau. La v1.2 est "
     "L'ÉDITION DE COHÉRENCE (D218) : l'en-tête courant réparé (la scorie v1.0), le sommaire "
     "des décisions D75-D137, les QUATORZE arbres signés au ch. 4 (D177), la table "
     "d'empreintes portée à sha-256 (D184/D187, alignée sur l'annexe A de la spécification), "
     "la référence à la spécification courante v0.15.1. AUCUN geste de cérémonie changé."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.19.1.pdf",
     V7 / "TRIADE_preuves_et_calculs_v0.19.1.pdf",
     "Le dossier d'évidence (18 pages) : la chaîne d'épreuve, le rapport de vérification "
     "V1-V10 de l'édition, la campagne D204 réconciliée et la clôture D210, l'alignement du "
     "modèle formel (treize règles, la couverture aux 288 formes), les mesures (la plage RQ2 "
     "2,98-11,37× ATTRIBUÉE À L'ÈRE LOUPE CONTRE M1 — la correction 4 ; le canon M4 "
     "23,1×-17,9× avec l'écart d'arrondi 17,8× nommé à côté de la pièce R11 verbatim — la "
     "correction 7 ; la table tokens restructurée : l'itération corrective est L'APPEL "
     "ENTIER, prompts et complétions — la correction 8), l'égalité exacte des traces, la "
     "table des empreintes et le diff annoté des onze corrections."),
    ("5-presentation", "TRIADE_presentation_20261120.pdf",
     V7 / "TRIADE_presentation_20261120.pdf",
     "Le document choisi du laboratoire (5 pages) : le protocole en bref (la formulation "
     "D182/D190 — la correction 6), le coffre-fort aux définitions de la spécification "
     "§12/Table 11 et du Livre ch. 3-4 (CF2 la clé répartie Shamir 5/3 + la porte D120 ; "
     "CF3 la serrure piégée, le piège hors machine ; le coffre des phrases maîtresses "
     "DISTINGUÉ de l'export de continuité D16 — la correction 5), la validation empirique "
     "close, l'état des éditions au 20/11 avec la visibilité du dépôt « GitHub privé — à "
     "trancher avant soumission (D81) » (la correction 11), le contenu du pack et la suite."),
]

if PACK.exists():
    shutil.rmtree(PACK)
for sous_dossier, nom, source, _ in PIECES:
    d = PACK / sous_dossier
    d.mkdir(parents=True)
    shutil.copy2(source, d / nom)
    print(f"posé : {sous_dossier}/{nom} ({os.path.getsize(d / nom)} o)")

# ---- 2. la LICENSE ----
shutil.copy2(REPO / "LICENSE", PACK / "LICENSE")

# ---- 3. le LISEZMOI ----
lisezmoi = f"""LE LISEZMOI DU PACK DE PRÉSENTATION — TRIADE v0.19.1
(assemblé le 20/11/2026 par le laboratoire, à l'Entrée 359 — l'édition de
cohérence inter-pièces née de l'instruction 376f15f18, la vague 7 ; le linter
inter-pièces vert sur les cinq pièces, la falsification prouvée)

LA COMMANDE : l'audit inter-pièces du pack (l'instruction 376f15f18) — « un
linter INTER-PIÈCES qui refuse le build sur toute divergence d'une valeur
partagée (tailles d'artefacts, ratios, versions, nombre d'arbres signés,
statut des outils formels, visibilité du dépôt). Corrige aux sources, sans
changer aucune valeur mesurée sauf réconciliation sur pièces » — puis « un
pack zip de présentation de 5 documents régénérés [...] à leurs nouvelles
versions, avec le fichier empreintes SHA-256 recalculées et le rapport de
vérification ».

LE PACK — CINQ PIÈCES, CHACUNE L'ÉDITION COURANTE VÉRIFIÉE :

""" + "\n\n".join(f"  {i+1}-{sd}/{nom}\n      {desc}" for i, (sd, nom, _, desc) in enumerate(PIECES)) + """

LES ONZE CORRECTIONS (chacune sourcée au diff annoté — la pièce 4, section 7) :
  (1) la référence courante à la spécification (v0.13.0 → v0.15.1) ;
  (2) les énoncés de timing matériel alignés sur les runs dudect SIGNÉS du 13/11 ;
  (3) les tailles passeur re-hachées aux artefacts réels des archives
      (61 952 / 102 390 o — les tailles v1 défaillantes étaient appariées aux
      hash v2+) ;
  (4) la plage RQ2 2,98-11,37× ré-attribuée à l'ère Loupe contre M1 (aux
      preuves §5 et à la présentation §3 — le manuscrit disait juste) ;
  (5) les définitions CF2/CF3 de la présentation remises à la spec §12 Table 11
      et au Livre ch. 3-4 ; le coffre-fort (les phrases maîtresses) distingué
      de l'export de continuité D16 ;
  (6) « sans compilateur ni langage de programmation » remplacé par la
      formulation D182/D190 (aucune chaîne de traduction optimisante ni
      opaque ; WYSIWYG vérifié par round-trip) ;
  (7) la base d'arrondi M4 canonisée : 23,1× → 17,9× (39,3/2,2, la première
      exécution) — l'écart 17,8× (39,2/2,2, la seconde) nommé à côté, la pièce
      R11 demeurant verbatim ;
  (8) la table tokens restructurée : les itérations correctives = prompts +
      complétions (l'appel correctif entier), jamais un sous-ensemble de la
      seule écriture ;
  (9) la spécification : cinq réconciliations, AUCUNE règle modifiée (v0.15.1) ;
  (10) le Livre : cinq réconciliations documentaires (v1.2) ;
  (11) la présentation : la table de l'état des éditions et la visibilité du
      dépôt « GitHub privé — à trancher avant soumission (D81) ».

LA DISCIPLINE TENUE : AUCUNE valeur mesurée modifiée (la réconciliation des
tailles passeur est une mesure re-faite sur les octets réels, l'unique
changement chiffré, sourcé aux archives) ; AUCUNE règle de la spécification
modifiée ; les artefacts scellés et les arbres signés OCTET-IDENTIQUES
avant/après (passeur-c.dll re-haché au geste : fe4ddfc9842fb29b… ; la garde
du sceau de l'Intention : 14 arbres VERTS) ; les éditions scellées v0.19.0 /
v0.15.0 / v1.1 INTACTES et faisant foi.

LES EMPREINTES — empreintes_livrables_v0.19.1.txt porte chaque fichier du
pack à son sha256 et son md5, recalculés à l'assemblage. L'empreinte du zip
lui-même vit à la consignation (l'Entrée 359 du worklog) — un zip ne peut
pas porter son propre condensé.

LE RAPPORT DE VÉRIFICATION — rapport_verification_v0.19.1.txt (livré à la
racine du coffre avec le pack) : les dix points V1-V10, chacun VERT sur
pièces, dont le linter inter-pièces 71/71 et les contrôles négatifs 8/8.

LA VÉRIFICATION À LA RÉCEPTION :
  Windows :  certutil -hashfile <fichier> SHA256
  Linux :    sha256sum <fichier>
Comparer à empreintes_livrables_v0.19.1.txt — échec fermé.

LA LICENCE — LICENSE (le dépôt du projet fait foi).

LA FRONTIÈRE — ce pack PRÉSENTE le protocole : il ne remplace ni le dépôt
git (la source de vérité), ni les registres bruts de la campagne, ni le
coffre /test (l'atelier vivant). Le laboratoire ne touche à aucun jeton ; la
consignation et le push vivent au worklog du dépôt. Les quatre autres
instructions de la vague 7 demeurent au /instructions, séquencées.
"""
(PACK / "LISEZMOI.txt").write_text(lisezmoi, encoding="utf-8", newline="\n")

# ---- 4. les empreintes (recalculées au geste) ----
lignes = ["EMPREINTES DES LIVRABLES — PACK DE PRÉSENTATION TRIADE v0.19.1",
          "(assemblé le 20/11/2026 ; chaque valeur recalculée au geste — échec fermé)",
          ""]


def empreintes(chemin):
    data = chemin.read_bytes()
    return (len(data),
            hashlib.sha256(data).hexdigest(),
            hashlib.md5(data).hexdigest())


for sous_dossier, nom, _, _ in PIECES:
    taille, sha, md5 = empreintes(PACK / sous_dossier / nom)
    lignes.append(f"{sous_dossier}/{nom}")
    lignes.append(f"    {taille} octets  sha256 {sha}  md5 {md5}")
for extra in ("LICENSE", "LISEZMOI.txt"):
    taille, sha, md5 = empreintes(PACK / extra)
    lignes.append(extra)
    lignes.append(f"    {taille} octets  sha256 {sha}  md5 {md5}")
lignes += ["",
           "Le zip TRIADE_presentation_v0.19.1_20261120.zip ne peut pas porter son",
           "propre condensé — son sha256 est consigné à l'Entrée 359 du worklog",
           "et à la carte OU-TROUVER-LES-LIVRABLES du coffre.",
           "Le rapport de vérification (rapport_verification_v0.19.1.txt) est livré",
           "à la racine du coffre à côté du pack."]
(PACK / "empreintes_livrables_v0.19.1.txt").write_text("\n".join(lignes) + "\n",
                                                       encoding="utf-8", newline="\n")
print("empreintes gravées")

# ---- 5. le zip ----
if ZIP.exists():
    ZIP.unlink()
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for racine, _, fichiers in os.walk(PACK):
        for f in sorted(fichiers):
            p = Path(racine) / f
            z.write(p, p.relative_to(PACK))
taille, sha, md5 = empreintes(ZIP)
print(f"LE ZIP : {ZIP.name} — {taille} octets")
print(f"  sha256 {sha}")
print(f"  md5    {md5}")

# ---- 6. le test du zip (chaque pièce relue, empreintes re-vérifiées) ----
with zipfile.ZipFile(ZIP) as z:
    noms = z.namelist()
    assert len(noms) == 8, f"le zip doit porter 8 entrées, il en porte {len(noms)}"
    for sous_dossier, nom, _, _ in PIECES:
        data = z.read(f"{sous_dossier}/{nom}")
        assert hashlib.sha256(data).hexdigest() == empreintes(PACK / sous_dossier / nom)[1], nom
print("LE ZIP TESTÉ : 8 entrées, chaque pièce relue, les empreintes re-vérifiées — OK")
