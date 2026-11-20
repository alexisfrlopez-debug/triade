#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_pack_v220.py — LE PACK TRIADE_presentation_v0.22.0.zip (12
fichiers : les 5 documents PDF régénérés et cohérents, les descriptions,
le LISEZMOI, LE MANIFESTE DES EMPREINTES) + le manifeste séparé
empreintes_livrables_v0.22.0.txt. Le zip RELU pièce à pièce après
l'assemblage (chaque empreinte re-vérifiée au dézippage)."""
import hashlib
import pathlib
import shutil
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V11 = REPO / "scripts" / "vague11"
PACK = V11 / "pack-v220"
if PACK.exists():
    shutil.rmtree(PACK)
PACK.mkdir(parents=True)
ZIP = REPO / "TRIADE_presentation_v0.22.0.zip"

PIECES = [
    ("1-manuscrit", "TRIADE_manuscrit_v0.22.0.pdf",
     REPO / "edition-v0220" / "main.pdf",
     "Le manuscrit académique v0.22.0 — la vague 11 portée : les errata "
     "de la v0.21.0 nommés et corrigés (la décomposition mémoire — "
     "médiés 348, la somme 2098 exacte ; les ratios §7 à une décimale "
     "1,5×/19,3× ; le plancher éditer au tokenizer natif — 27,5, le "
     "ratio 24,5×, la ligne cl100k historique datée ; la conclusion RQ2 "
     "aux formats adoptés), les couloirs SIMD mesurés sur matériel "
     "(l'hybride 704 cycles dans la classe des primitives SIMD libc, le "
     "SHA-NI 128,5 c/bloc), la boucle porteuse AES-NI restructurée sous "
     "sa cible (7,09 c/bloc), le quatrième bras C+G+ et la ventilation "
     "trois-effets (notation propre 55,7 %, régime 44,3 %, gouvernance "
     "0,213 s), la soundness du lifter au domaine validé (942 encodages, "
     "la garde hors-vocabulaire fail-closed), les gabarits versionnés, "
     "le coffre durci sur copies de laboratoire, les kits "
     "pré-enregistrés, la purge D81."),
    ("2-specification", "Protocole_TRIADE_v0.15.7_Specification.pdf",
     REPO / "scripts" / "spec_v157" / "main.pdf",
     "La spécification v0.15.7 — la purge D81 portée à la vague 11 "
     "(l'instruction ou6wn6wlv : le séquestre 5/3 la garde active, le "
     "dépôt public D220 ; l'évolution de discipline amendée D223, la "
     "restauration post-panne, la correspondance v0.15.7 — onze "
     "remplacements ancrés, AUCUNE règle R1-R11 modifiée)."),
    ("3-coffre-fort", "Livre_du_Coffre_TRIADE_CF1-CF3_v1.6.pdf",
     REPO / "scripts" / "livre_v16" / "final.pdf",
     "Le Livre du Coffre v1.6 — la purge D81 portée à la vague 11 "
     "(l'instruction ou6wn6wlv : la règle 2 au séquestre 5/3 + "
     "reconstitution à froid + refus nommé, le récit D81 borné au 19 "
     "novembre 2026, la cérémonie D183, la check-list §8.3, le remède "
     "§9.2 — quinze remplacements ancrés)."),
    ("4-preuves-calculs", "TRIADE_preuves_et_calculs_v0.22.0.pdf",
     V11 / "TRIADE_preuves_et_calculs_v0.22.0.pdf",
     "Les preuves et calculs v0.22.0 — les NEUF pièces verbatim "
     "INTÉGRALES de la vague 11 (la purge D81, les couloirs SIMD, la "
     "boucle porteuse, les gabarits, le coffre durci, le quatrième bras, "
     "les kits pré-enregistrés, la soundness du lifter, le plancher "
     "natif et le recompte) + LA DÉCOMPOSITION MÉMOIRE CORRIGÉE avec "
     "l'erratum nommé (le compte « médiés 0 » publié à la v0.21.0 "
     "sommait à 1750, pas 2098 — le recompte du CSV brut porte 348, la "
     "somme exacte) + LA CAUSE du « couloir B : code 1 » + la table des "
     "empreintes."),
    ("5-presentation", "TRIADE_presentation_20261121_v220.pdf",
     V11 / "TRIADE_presentation_20261121_v220.pdf",
     "La présentation v220 — les neuf points de la vague 11 (la purge, "
     "les couloirs, la boucle porteuse, les gabarits, le coffre, le "
     "quatrième bras, les kits, le lifter, LES ERRATA + LE LINTER v220), "
     "la table des statuts, LES EMPREINTES SHA-256 DES QUATRE AUTRES "
     "PIÈCES GRAVÉES (la convention : aucun document ne porte son "
     "propre sha-256, le manifeste du pack porte les cinq)."),
]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


manifest = ["LE MANIFESTE DES EMPREINTES — le pack TRIADE v0.22.0 (la vague 11)",
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

EMP = V11 / "empreintes_livrables_v0.22.0.txt"
EMP.write_text("\n".join(manifest) + "\n", encoding="utf-8")
shutil.copy2(EMP, PACK / "empreintes_livrables_v0.22.0.txt")

(PACK / "LISEZMOI.txt").write_text(
    "LE PACK DE PRÉSENTATION TRIADE v0.22.0 — la vague 11\n"
    "====================================================\n\n"
    "LES CINQ DOCUMENTS : le manuscrit académique v0.22.0 (les errata "
    "nommés et corrigés, les résultats de la vague 11), la spécification "
    "v0.15.7 (la purge D81), le Livre du Coffre v1.6 (la purge D81), les "
    "preuves et calculs v0.22.0 (les neuf pièces verbatim intégrales + "
    "l'erratum de la décomposition mémoire + la table des empreintes), "
    "la présentation v220 (les neuf points, la table des statuts, les "
    "empreintes gravées).\n\n"
    "LA CONVENTION DES EMPREINTES : aucun document ne porte son propre "
    "sha-256 ; la présentation grave les quatre autres ; le document de "
    "preuves grave les trois pièces de contenu ; CE manifeste porte les "
    "cinq.\n\n"
    "LES NEUF INSTRUCTIONS DE LA VAGUE 11 exécutées aux plans gelés "
    "avant toute mesure (le commit 3962b26, EMPREINTES-PLANS-VAGUE11."
    "txt) : zho5vilpy (le linter étendu à tout token numérique + les "
    "corrections sur pièces), ou6wn6wlv (la purge D81), fnvan0zes (les "
    "couloirs SIMD), ahult8jgd (la boucle porteuse AES-NI), o5apue194 "
    "(les gabarits versionnés), vr9n3s3l7 (le durcissement du coffre), "
    "3lmyfb2xa (le quatrième bras C+G+), l4nnwqlld (les kits "
    "pré-enregistrés), hrbdfy6i4 (la soundness du lifter au domaine).\n\n"
    "LES GAPS NOMMÉS (jamais simulés) : l'ajouter-S à 3/18 (quinze "
    "refus honnêtes) ; la seconde machine ; Tamarin non installé au "
    "bac ; le FIDO2 physique au geste du maître ; la TSA et l'ancrage "
    "réseau au geste ; M3 le temps humain au terrain.\n",
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
