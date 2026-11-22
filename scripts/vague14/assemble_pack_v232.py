#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v232.py — LE PACK TRIADE_presentation_v0.23.2.zip (12
fichiers : les 5 documents PDF régénérés et cohérents, les descriptions,
le LISEZMOI, LE MANIFESTE DES EMPREINTES). Le zip REFUSÉ si un contrôle
est rouge — le linter v232 EXIGÉ vert avant l'assemblage (échec fermé).
Le zip RELU pièce à pièce après l'assemblage (chaque empreinte
re-vérifiée au dézippage)."""
import hashlib
import pathlib
import shutil
import subprocess
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V14 = REPO / "scripts" / "vague14"
PACK = V14 / "pack-v232"
if PACK.exists():
    shutil.rmtree(PACK)
PACK.mkdir(parents=True)
ZIP = REPO / "TRIADE_presentation_v0.23.2.zip"

# (0) LE LINTER EXIGÉ VERT AVANT L'ASSEMBLAGE (le refus ferme)
print("[0] le linter v232 exigé vert avant l'assemblage…")
r = subprocess.run([sys.executable, str(V14 / "linter_v232.py")],
                   capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout[-2000:])
    raise SystemExit("LE LINTER v232 ROUGE — le pack REFUSÉ")
print("    le linter : VERT")

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.23.2.pdf",
     REPO / "edition-v0230" / "main.pdf",
     "Le manuscrit académique v0.23.2 — la génération corrective de la "
     "vague 14 : les dix corrections sourcées (a)-(j) portées aux pièces "
     "(le canon GHASH unique sur la variante adoptée 63.39 [IQR 30] = "
     "12.7x, les opérandes non arrondis du plancher M4 6.912/2.056 = "
     "3.362, la fermeture de la ventilation 20.715+16.497+0.213 = 37.425, "
     "la grille F/L D203, la famille « the field beyond the pattern » "
     "portée à l'abstract EN), la vague 14 portée (le GHASH agrégé "
     "19.66 c/mult [IQR 19] — 41.0x sur le scellé 806.35 ; H-CGP4 la "
     "mémoïsation content-addressed a -89.4 % sans aucun contrôle "
     "retiré ; TPL-ADD-v4 7/18 — la première conversion d'un refus "
     "honnête ; H7 tirée et signée ; le premier run Tamarin vécu — le "
     "lemme d'implication falsifié par un défaut de modélisation nommé, "
     "aucun verdict fabriqué), le changelog gelé aux lignes v0.23.1 et "
     "v0.23.2, la disponibilité des données au DOI 24442241."),
    ("2-specification", "Protocole_TRIADE_v0.15.8_Specification.pdf",
     REPO / "scripts" / "spec_v158" / "main.pdf",
     "La spécification v0.15.8 — reconstruite aux sources corrigées de "
     "la génération v0.23.2 : « quatorze arbres VERTS » à la Table 15 "
     "(la correction (g)), la grille de replication F/L (renommée de "
     "T/X par D203 — les mentions d'époque datées), l'annexe B "
     "réalignée sur le journal des décisions (D75-D251)."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.7.pdf",
     REPO / "scripts" / "livre_v17" / "final.pdf",
     "Le Livre du Coffre v1.7 — reconstruit aux sources corrigées : le "
     "bandeau de couverture « Version 1.7 » PORTÉ (la correction (d), "
     "inachevée à la v0.23.1 — le PDF livré portait le bandeau 1.6), la "
     "date de couverture alignée sur la régénération, §10.1 v0.15.8, le "
     "chapitre 11 D75-D250."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.23.2.pdf",
     V14 / "TRIADE_preuves_et_calculs_v0.23.2.pdf",
     "Les preuves et calculs v0.23.2 — les pièces des CINQ ateliers de "
     "la quatorzième vague lues VERBATIM de leurs rapports (la fermeture "
     "sécurité et le premier run Tamarin, le GHASH agrégé, H-CGP4, "
     "TPL-ADD-v4, la validité externe H7) + LA CONSIGNATION DES DIX "
     "CORRECTIONS (a)-(j) avec la décomposition recomposée par code du "
     "census CSV (12 = 5+2+1+1+1+1+1) + l'héritage mesuré des vagues "
     "11-13 + la table des empreintes des cinq pièces."),
    ("5-presentation", "TRIADE_presentation_v232.pdf",
     V14 / "TRIADE_presentation_v232.pdf",
     "La présentation v232 — les six points de la vague 14 (la fermeture "
     "sécurité, le GHASH agrégé, H-CGP4, TPL-ADD-v4, la validité externe "
     "H7, la génération corrective elle-même), l'état des éditions (la "
     "v0.23.1 corrective close par la présente), l'héritage mesuré, les "
     "gaps nommés, LES EMPREINTES SHA-256 DES QUATRE AUTRES PIÈCES "
     "GRAVÉES (la convention : aucun document ne porte son propre "
     "sha-256, le manifeste du pack porte les cinq)."),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


manifest = ["LE MANIFESTE DES EMPREINTES — le pack TRIADE v0.23.2 (la "
            "vague 14, la génération corrective)",
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

EMP = V14 / "empreintes_livrables_v0.23.2.txt"
EMP.write_text("\n".join(manifest) + "\n", encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.23.2.txt")

(PACK / "LISEZMOI.txt").write_text(
    "LE PACK DE PRÉSENTATION TRIADE v0.23.2 — la vague 14, la génération "
    "corrective\n"
    "===========================================================\n\n"
    "LES CINQ DOCUMENTS : le manuscrit académique v0.23.2 (les dix "
    "corrections sourcées portées, la vague 14 portée au corps), la "
    "spécification v0.15.8 (reconstruite — « quatorze arbres »), le "
    "Livre du Coffre v1.7 (le bandeau de couverture porté à 1.7), les "
    "preuves et calculs v0.23.2 (les cinq rapports d'atelier verbatim + "
    "la consignation des corrections + la table des empreintes), la "
    "présentation v232 (les points de la vague, l'état des éditions, les "
    "empreintes gravées).\n\n"
    "LA GÉNÉRATION CORRECTIVE : la v0.23.1 (la release de la vague 14) "
    "avait porté les sources corrigées au seul pack COMPLET — la "
    "soumission et la présentation demeurées byte-byte à leur état "
    "v0.23.0, l'écart nommé au worklog. La commande du maître (« je "
    "n'ai pas la version presentation et soumission du pack dans "
    "zenodo ») commande la présente : les cinq pièces régénérées, le "
    "linter étendu aux quatre règles nouvelles, les trois packs "
    "assemblés à la version courante, la version publiée au concept "
    "Zenodo avec la soumission et la présentation à la version "
    "courante.\n\n"
    "LA CONVENTION DES EMPREINTES : aucun document ne porte son propre "
    "sha-256 ; la présentation grave les quatre autres ; le document de "
    "preuves grave les trois pièces de contenu ; CE manifeste porte les "
    "cinq.\n\n"
    "LES SIX INSTRUCTIONS DE LA VAGUE 14 exécutées aux plans gelés avant "
    "toute mesure (EMPREINTES-PLANS-VAGUE14.txt) : f3uznui3l (la fermeture "
    "sécurité : les 58 certificats re-vérifiés, la composition des gardes "
    "de frontière, Tamarin installé et le premier run vécu — le lemme "
    "d'implication falsifié, un défaut de modélisation nommé), "
    "h1mz2sr8s (le GHASH agrégé quatre blocs à réduction différée : "
    "19,66 c/mult, 41,0× sur le scellé), s2p9bm3zd (H-CGP4 la "
    "mémoïsation content-addressed : −89,4 % sans aucun contrôle "
    "retiré), 842vqyy1k (TPL-ADD-v4 les quatre leviers : 7/18, la "
    "première conversion d'un refus honnête), tcb7tpf9q (la validité "
    "externe : H7 tirée et signée, la campagne ouverte aux 28 unités), "
    "io13olvxz (les dix corrections sourcées — la présente génération).\n\n"
    "LES GAPS NOMMÉS (jamais simulés) : la cible TPL-ADD-v4 (≥ 15/18) "
    "manquée à 7/18 — le gap par classe de refus ; la cible ≤ 1 % du "
    "coût des gardes non tranchée au bac émulé ; la mesure "
    "d'entrelacement GHASH suivante ; le re-run Tamarin de "
    "l'amendement ; les 28 livraisons H7 au geste du maître ; la "
    "seconde machine (une seule au bac).\n",
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
