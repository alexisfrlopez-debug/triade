#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v210.py — LE PACK TRIADE_presentation_v0.21.0.zip (12
fichiers : les 5 documents PDF régénérés et cohérents, les descriptions,
le LISEZMOI, LE MANIFESTE DES EMPREINTES) + le manifeste séparé
empreintes_livrables_v0.21.0.txt. Le zip RELU pièce à pièce après
l'assemblage (chaque empreinte re-vérifiée au dézippage)."""
import hashlib
import pathlib
import shutil
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V10 = REPO / "scripts" / "vague10"
PACK = V10 / "pack-v210"
if PACK.exists():
    shutil.rmtree(PACK)
PACK.mkdir(parents=True)
ZIP = REPO / "TRIADE_presentation_v0.21.0.zip"

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.21.0.pdf",
     REPO / "edition-v0210" / "main.pdf",
     "Le manuscrit académique v0.21.0 — la vague 10 portée : la "
     "réconciliation de l'abstract au corps (811/817 = 99,3 %), le ratio "
     "M4 recalculé des médianes non arrondies, l'axe ajouter au coût "
     "opérationnel, la fenêtre de relecture (OPT-10 : 1 146, −53,3 %), le "
     "troisième bras C+G (l'effet notation isolé 18,1×), la faute SSE2 "
     "nommée et la re-mesure sur matériel aux baselines équitables, les "
     "gardes à 100 % déchargé-ou-gardé, la non-interférence étendue sous "
     "l'hypothèse de soundness du lifter, le registre neutre."),
    ("2-specification", "Protocole_TRIADE_v0.15.6_Specification.pdf",
     REPO / "scripts" / "spec_v156" / "main.pdf",
     "La spécification v0.15.6 — INCHANGÉE à la vague 10 (aucune règle "
     "R1-R11 modifiée, aucune cérémonie touchée : les changements de la "
     "vague 10 sont des preuves et des mesures, portées au manuscrit et "
     "aux preuves ; la table des preuves et l'annexe B à leur état v0.15.6)."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.5.pdf",
     REPO / "scripts" / "livre_v15" / "final.pdf",
     "Le Livre du Coffre v1.5 — INCHANGÉ à la vague 10 (la pièce "
     "opérationnelle française garde son style ; les références à la spec "
     "v0.15.6 et au dépôt public demeurent à l'état vécu)."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.21.0.pdf",
     V10 / "TRIADE_preuves_et_calculs_v0.21.0.pdf",
     "Les preuves et calculs v0.21.0 — les huit pièces verbatim de la "
     "vague 10 : la faute SSE2 et la re-mesure aux instructions, le temps "
     "réel sur matériel, la fenêtre de relecture, les gardes, la "
     "non-interférence étendue et le round-trip du lifter, le bras C+G "
     "(la construction, la mesure M4, la réconciliation avec le contrôle "
     "négatif) + LA TABLE DES EMPREINTES des pièces de contenu."),
    ("5-presentation", "TRIADE_presentation_20261120_v210.pdf",
     V10 / "TRIADE_presentation_20261120_v210.pdf",
     "La présentation v210 — les cinq points de la vague 10 (la faute "
     "nommée et corrigée, la fenêtre, les gardes, l'effet notation isolé, "
     "la réconciliation et le registre neutre), la table des statuts "
     "avant/après, LES EMPREINTES SHA-256 DES QUATRE AUTRES PIÈCES GRAVÉES "
     "(la convention : aucun document ne porte son propre sha-256, le "
     "manifeste du pack porte les cinq)."),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


manifest = ["LE MANIFESTE DES EMPREINTES — le pack TRIADE v0.21.0 (la vague 10)",
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

EMP = V10 / "empreintes_livrables_v0.21.0.txt"
EMP.write_text("\n".join(manifest) + "\n", encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.21.0.txt")

(PACK / "LISEZMOI.txt").write_text(
    "LE PACK DE PRÉSENTATION TRIADE v0.21.0 — la vague 10\n"
    "====================================================\n\n"
    "LES CINQ DOCUMENTS : le manuscrit académique v0.21.0 (la "
    "réconciliation, le registre neutre, les résultats de la vague 10), "
    "la spécification v0.15.6 (inchangée), le Livre du Coffre v1.5 "
    "(inchangé), les preuves et calculs v0.21.0 (les pièces verbatim des "
    "ateliers + la table des empreintes), la présentation v210 (les cinq "
    "points, la table des statuts, les empreintes gravées).\n\n"
    "LA CONVENTION DES EMPREINTES : aucun document ne porte son propre "
    "sha-256 ; la présentation grave les quatre autres ; le document de "
    "preuves grave les trois pièces de contenu ; CE manifeste porte les "
    "cinq.\n\n"
    "LES SIX INSTRUCTIONS DE LA VAGUE 10 exécutées aux plans gelés avant "
    "toute mesure (le commit 951e79b, EMPREINTES-PLANS-VAGUE10.txt) : "
    "1e2vq7rtw (la réconciliation + le linter interne), 3a91o5whb (le bras "
    "C+G), 8z4hj76w4 (la faute SSE2 et la re-mesure équitable), "
    "ifqm1d1i4 (les gardes + la non-interférence étendue), mqf258e4l (la "
    "fenêtre de relecture), rgttyp8bj (le registre neutre).\n\n"
    "LES GAPS NOMMÉS (jamais simulés) : M3 le temps humain au geste du "
    "terrain ; la seconde machine ; les témoins signés.\n",
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
        attendu = sha(PACK / info.filename)
        if hashlib.sha256(data).hexdigest() == attendu:
            ok += 1
        else:
            print(f"!! DIVERGENCE au dézippage : {info.filename}")
print(f"[pack] {ZIP} ({ZIP.stat().st_size} octets, "
      f"{len(list(PACK.rglob('*'))) - 5} entrées) — {ok} pièces relues "
      f"et recoupées")
