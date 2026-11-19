#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v192.py — le pack de présentation v0.19.2 (l'instruction jx4l5vy5c :
« Produis ensuite le pack zip de présentation de 5 documents régénérés avec
empreintes SHA-256 et rapport de vérification ; refuse le zip si un contrôle
est rouge. »). Le linter inter-pièces ÉTENDU aux statuts D81/D183 doit être
VERT avant l'assemblage — le script le vérifie lui-même (échec fermé)."""
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/bac")
V7 = REPO / "scripts" / "vague7"
PACK = V7 / "pack-v192"
ZIP = V7 / "TRIADE_presentation_v0.19.2_20261120.zip"

# ---- 0. le linter inter-pièces DOIT être vert (le zip est refusé sinon) ----
print("== le linter inter-pièces ÉTENDU (D81/D183) — le zip est refusé si un contrôle est rouge")
r = subprocess.run([sys.executable, str(V7 / "linter_interpieces.py")],
                   capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr)
if r.returncode != 0:
    sys.exit("LE LINTER EST ROUGE — le pack est REFUSÉ.")

# ---- 1. les pièces à leurs noms de livraison ----
PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.19.2.pdf",
     REPO / "edition-v0192" / "main.pdf",
     "Le manuscrit scientifique (édition académique, 31 pages, en anglais) : le protocole, "
     "les campagnes D204/D210 closes, les résultats. La v0.19.2 est L'ÉDITION COURANTE — "
     "née de la v0.19.1 (la cohérence inter-pièces, D218), c'est L'ÉDITION DE LA TRANSITION "
     "PRÉPARÉE (D219, l'instruction jx4l5vy5c) : la ligne D81 du §4.1 à SON STATUT EXACT — "
     "the transition to the D183 encrypted escrow is now prepared as decision D219 (le kit "
     "rafraîchi avec la falsification prouvée et la porte fail-closed --verifier, le scan de "
     "secrets de l'historique git complet au dry-run vert — six of six planted secrets "
     "caught, zero false negatives — et son triage, la rotation checklist, la matrice de "
     "visibilité du dépôt, l'extension transparence documentée sans être appliquée), la "
     "note d'édition v0.19.2. AUCUNE valeur mesurée modifiée."),
    ("2-specification", "Protocole_TRIADE_v0.15.2_Specification.pdf",
     REPO / "scripts" / "spec_v152" / "final.pdf",
     "La spécification technique COMPLÈTE du protocole (66 pages) : les trois couches, les "
     "onze règles, les profils, le coffre-fort CF1-CF3, la gouvernance et le journal des "
     "décisions. La v0.15.2 est L'ÉDITION DE LA TRANSITION PRÉPARÉE (D219) : AUCUNE règle "
     "modifiée — la ligne D81 du modèle de menace (§15) au statut exact (la transition D183 "
     "PRÉPARÉE, le geste au développeur ; le dépôt PRIVÉ tant que la cérémonie n'est pas "
     "vécue et la rotation vérifiée — public + Zenodo seulement après), le § 1.18 « Ce que "
     "change la v0.15.2 », le journal des versions porté."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.3.pdf",
     REPO / "scripts" / "livre_v13" / "final.pdf",
     "Le livre opératoire du coffre-fort (28 pages) : les cérémonies, le runbook de "
     "migration CF1 vers CF3, le mode dégradé, les obligations par niveau. La v1.3 porte "
     "LA CÉRÉMONIE DE SÉQUESTRE D183 (§ 7.5 — préparée, le geste au maître) : l'analyse "
     "chiffrée au facteur ≈ 40, la preuve à froid de l'outil (la part forgée REFUSÉE), le "
     "pas à pas en sept gestes (cinq médias dont deux hors nuage — répétition — découpage — "
     "répartition — preuve à froide ×2 --verifier — retrait humain listé — entretien), les "
     "frontières et l'encadré « pourquoi le kit ne s'applique pas tout seul » ; le pointeur "
     "au runbook et à la garde de la phrase. AUCUN geste de cérémonie changé."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.19.2.pdf",
     V7 / "TRIADE_preuves_et_calculs_v0.19.2.pdf",
     "Le dossier d'évidence (21 pages) : la chaîne d'épreuve, LE RAPPORT DE VÉRIFICATION "
     "V1-V10 DE L'EXÉCUTION D219 (la première exigence tenue avant tout — les pièces "
     "scellées intactes, le sceau aux QUATORZE arbres ; le kit rafraîchi ; LA FALSIFICATION "
     "PROUVÉE — une part forgée REFUSÉE par la porte de l'empreinte de contrôle ; le dry-run "
     "du scan 6/6, zéro faux négatif ; le triage du vrai dépôt — la phrase D81 connue, neuf "
     "fixtures nommées, aucune fuite réelle), l'autotest et les consoles de l'épreuve, la "
     "campagne D204 réconciliée et la clôture D210, le modèle formel (288 formes), les "
     "mesures, l'égalité des traces, la table des empreintes et le diff annoté."),
    ("5-presentation", "TRIADE_presentation_20261120.pdf",
     V7 / "TRIADE_presentation_20261120.pdf",
     "Le document choisi du laboratoire (7 pages) : le protocole en bref, le coffre-fort, "
     "la validation empirique close, LA TRANSITION D81 → D183 PRÉPARÉE (D219 — le kit, la "
     "falsification, le scan, la matrice), l'état des éditions au 20/11 (v0.19.2 / v0.15.2 / "
     "v1.3) avec la visibilité du dépôt « GitHub PRIVÉ — public + Zenodo seulement après la "
     "cérémonie VÉCUE et les rotations vérifiées (la matrice de visibilité) », le contenu du "
     "pack et la suite (la cérémonie au maître, le DOI au jeton)."),
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
lisezmoi = f"""LE LISEZMOI DU PACK DE PRÉSENTATION — TRIADE v0.19.2
(assemblé le 19/11/2026 par le laboratoire, à l'Entrée 360 — l'exécution de
l'instruction jx4l5vy5c, la vague 7, la deuxième : la transition D81 → D183
PRÉPARÉE (D219) ; le linter inter-pièces étendu aux statuts D81/D183, vert
sur les cinq pièces, la falsification prouvée 11/11)

LA COMMANDE (l'instruction jx4l5vy5c) : « Prépare la bascule de garde durable
D81 vers le séquestre chiffré D183, SANS jamais toucher au coffre réel ni aux
phrases réelles (D105) » — le kit de cérémonie rafraîchi (l'autotest sur
phrase de test publique marquée, le LISEZMOI pas à pas, le manifeste sha256,
les listes de contrôle, le geste de retrait), la décision append-only de
transition avec l'analyse chiffrée perte/exposition (facteur ≈ 40) et le
statut « préparée, geste au développeur », la procédure de scan de secrets
sur l'historique git complet avec dry-run sur un dépôt de test à secrets
plantés, la checklist de rotation de toute phrase exposée, la matrice de
décision visibilité dépôt (privé tant que D183 n'est pas appliqué et les
rotations vérifiées ; public + Zenodo seulement après), l'extension
transparence publique documentée non appliquée, la ligne D81 du modèle de
menace au statut exact et le runbook du Livre (section cérémonie D183).

LE PACK — CINQ PIÈCES, CHACUNE L'ÉDITION COURANTE VÉRIFIÉE :

""" + "\n\n".join(f"  {i+1}-{sd}/{nom}\n      {desc}" for i, (sd, nom, _, desc) in enumerate(PIECES)) + """

CE QUE LA PRÉPARATION PORTE (la décision D219, append-only) :
  — LE KIT RAFRAÎCHI (scripts/kit_ceremonie_d183/) : l'outil sequestre_d183.py
    étendu du mode --verifier fail-closed (le sha256 du rendu confronté à
    l'empreinte de contrôle du manifeste — tout écart un REFUS nommé) et de la
    falsification à l'autotest (une part forgée REFUSÉE aux deux combinaisons
    éprouvées, l'honnête VERT par la même porte) ;
  — LE SCAN DE SECRETS DE L'HISTORIQUE GIT COMPLET : l'équivalent Python nommé
    de gitleaks/trufflehog (absents du bac — l'écart D207), le dry-run
    6/6 zéro faux négatif zéro faux positif, le triage du vrai dépôt (472
    commits, 5 847 blobs : la phrase D81 connue, neuf fixtures de test nommées,
    AUCUN identifiant réel au-delà de l'arbitrage assumé) ;
  — LA CHECKLIST DE ROTATION de toute phrase exposée ;
  — LA MATRICE DE VISIBILITÉ DU DÉPÔT (quatre états, l'ordre strict) ;
  — L'EXTENSION TRANSPARENCE PUBLIQUE documentée non appliquée (Rekor/Sigstore
    ou RFC 3161 — le format du témoin, la vérification machine, le delta au
    modèle de menace aux deux bords).

LA DISCIPLINE TENUE : le coffre réel et les phrases réelles JAMAIS approchés
(D105 — la preuve : passeur.exe/passeur-c.dll re-téléchargés intacts, les
scells locaux inchangés, le sceau aux QUATORZE arbres verts à l'ouverture et
à la clôture) ; AUCUNE valeur mesurée modifiée ; AUCUNE règle de la
spécification modifiée ; AUCUN geste de cérémonie du Livre changé ; les
éditions scellées v0.19.0/v0.19.1, v0.15.0/v0.15.1 et v1.1/v1.2 INTACTES et
faisant foi.

LES EMPREINTES — empreintes_livrables_v0.19.2.txt porte chaque fichier du
pack à son sha256 et son md5, recalculés à l'assemblage. L'empreinte du zip
lui-même vit à la consignation (l'Entrée 360 du worklog) — un zip ne peut
pas porter son propre condensé.

LE RAPPORT DE VÉRIFICATION — rapport_verification_v0.19.2.txt (livré à la
racine du coffre avec le pack) : les dix points V1-V10, chacun VERT sur
pièces, dont le linter inter-pièces étendu 87/87 et les contrôles négatifs
11/11 (le statut D183 muté « préparée → appliquée » ATTRAPÉ ; la visibilité
publique prématurée REFUSÉE).

LA VÉRIFICATION À LA RÉCEPTION :
  Windows :  certutil -hashfile <fichier> SHA256
  Linux :    sha256sum <fichier>
Comparer à empreintes_livrables_v0.19.2.txt — échec fermé.

LA LICENCE — LICENSE (le dépôt du projet fait foi).

LA FRONTIÈRE — ce pack PRÉSENTE le protocole : il ne remplace ni le dépôt
git (la source de vérité), ni les registres bruts de la campagne, ni le
coffre /test (l'atelier vivant). Le laboratoire ne touche à aucun jeton ; la
consignation et le push vivent au worklog du dépôt. Les trois instructions
restantes de la vague 7 (5ey7gmjra, cq01qv1za, 1c4sokpii) demeurent au
/instructions, séquencées ; l'instruction jx4l5vy5c est archivée après
exécution (la règle du développeur).
"""
(PACK / "LISEZMOI.txt").write_text(lisezmoi, encoding="utf-8", newline="\n")

# ---- 4. les empreintes (recalculées au geste) ----
lignes = ["EMPREINTES DES LIVRABLES — PACK DE PRÉSENTATION TRIADE v0.19.2",
          "(assemblé le 19/11/2026 ; chaque valeur recalculée au geste — échec fermé)",
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
           "Le zip TRIADE_presentation_v0.19.2_20261120.zip ne peut pas porter son",
           "propre condensé — son sha256 est consigné à l'Entrée 360 du worklog",
           "et à la carte OU-TROUVER-LES-LIVRABLES du coffre.",
           "Le rapport de vérification (rapport_verification_v0.19.2.txt) est livré",
           "à la racine du coffre à côté du pack."]
(PACK / "empreintes_livrables_v0.19.2.txt").write_text("\n".join(lignes) + "\n",
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
