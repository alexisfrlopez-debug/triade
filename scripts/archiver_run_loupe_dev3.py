#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_loupe_dev3.py — LE TÉMOIN ROUGE DU RUN dev.3 ARCHIVÉ SUR PIÈCES
(règle D143 : archivage par DÉPLACEMENT, jamais un jet).

LE TROISIÈME REFUS TERRAIN (l'Entrée 206) : « preuves-loupe déposées
dans le dossier /test du drive » — LE VRAI CHARGEUR A CARTOGRAPHIÉ
dev.3 (la PREMIÈRE fois au terrain : l'enveloppe de l'Entrée 205 est
PROUVÉE — l'image mappée @0x7ff740e20000, les adresses scellées, la
table K, la porte R10 relues VERTES au témoin), puis LE RUN S'EST
ARRÊTÉ AU T0 : ÉCHEC NOMMÉ [CADRE-NÉ] — « le CADRE .data n'est pas né
poignée INVALIDE (l'initialiseur du build) ». L'AUTOPSIE SUR PIÈCES :
le sentinel INVALIDE à +8 (une TAILLE prise pour un offset), ZÉRO à
+528 (la chaîne des tailles du plan). LE REFUS EST UN FAIT, LA PIÈCE
DEMEURE.

  1. LE TÉMOIN RAPATRIÉ ET RECOUPÉ (md5 72761cd6… — 522 o, la ligne
     d'échec nommée) ;
  2. LE DOSSIER D'ARCHIVE né aux archives-preuves :
     preuves-run-loupe-dev3/ ;
  3. LE TÉMOIN DÉPLACÉ (addParents/removeParents — DÉPLACEMENT,
     jamais une copie) + md5 recoupé APRÈS ;
  4. LE VERDICT DU RUN déposé dans l'archive (VERDICT-run-loupe-
     dev3.txt : ROUGE — l'échec nommé [CADRE-NÉ], l'autopsie, la
     retouche dev.4 née) ;
  5. L'INDEX MIS À JOUR : LISEZMOI-archives-preuves.txt (la ligne du
     run loupe dev.3) ;
  6. LE RÉCEPTACLE demeure avec son LISEZMOI (preuves-loupe/ —
     ré-armé par la vague dev.4).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/archiver_run_loupe_dev3.py
Code de sortie : 0 = témoin archivé ; 2 = refus nommé."""

import hashlib
import json
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # dossier « test »
ARCHIVES_PREUVES_ID = "1TRZtOdvqfovvZt0jdFdpMysrpHNKOzFk"  # archives-preuves
INDEX_ID = "1WK5OOuMOFFoUj3PevftZo3pHIFKQx7zu"          # LISEZMOI-archives-preuves

TEMOIN_MD5 = "72761cd684c573273e557cc8c7f8b284"   # le témoin dev.3 (522 o)
DOSSIER_ARCHIVE = "preuves-run-loupe-dev3"

VERDICT = """VERDICT DU RUN TERRAIN M10-(e) — LOUPE dev.3 : ROUGE (l'échec nommé)
========================================================================
Le run du 09/11/2026 (le kit dev.3, la seconde vague de l'Entrée 205) :

  - LE VRAI CHARGEUR A CARTOGRAPHIÉ L'IMAGE — LA PREMIÈRE FOIS AU
    TERRAIN : LoadLibraryEx DONT_RESOLVE @ 0x7ff740e20000, l'empreinte
    ASSERTÉE (loupe.exe 127 488 o, sha256 b494ff906bc60277…), les
    adresses scellées CONSTATÉES (la minilibc M1, la boucle démo, la
    famille sha M9, la table K FIPS, le qword version R10 0x00010003)
    — L'ENVELOPPE DE L'ENTRÉE 205 EST PROUVÉE AU TERRAIN : plus de
    refus 0xc000007b, la leçon des Entrées 204/205 DEMEURE.
  - PUIS LE TÉMOIN A NOMMÉ AU T0 : ÉCHEC NOMMÉ [CADRE-NÉ] — « le
    CADRE .data n'est pas né poignée INVALIDE (l'initialiseur du
    build) ».
  - L'AUTOPSIE DE LABO SUR PIÈCES (l'artefact relu champ à champ) :
    le sentinel INVALIDE posé à +8 (DANS le chemin UTF-16) et ZÉRO à
    +528 — l'initialiseur du build avait pris CADRE_POIGNEE (UNE
    TAILLE, 8) pour un OFFSET ; le plan, le harnais (CADRE_VIERGE),
    le scénario et l'assembleur disaient TOUS +528.
  - LE COÛT SI LE T0 N'AVAIT PAS NOMMÉ : le zéro à +528 serait UNE
    SESSION FANTÔME au premier ouvrir() (loupe-01 croirait une session
    vivante — l'application ne pourrait JAMAIS ouvrir un fichier).

LA RETOUCHE dev.4 EST NÉE (l'Entrée 206) : l'initialiseur .data
DEVIENT LE MIROIR EXACT du CADRE_VIERGE du harnais (l'offset CALCULÉ
par la chaîne des tailles : CADRE_CHEMIN 520 + CADRE_TAILLE_F 8 =
528, jamais gravé de tête) ET le validateur du build relit LE MÊME
miroir (dev.3 validait à +8 : un garde blessé par le défaut qu'il
croyait garder ne garde rien). Le scénario relit désormais LE .data
ENTIER contre le miroir — la porte demeure pour toujours.

Un échec nommé vaut plus qu'un vert muet (charte § 9). Le labo
recoupe sur pièces (D138/D145/D148) ; l'archivage est un DÉPLACEMENT
(D143) — le refus du terrain est un FAIT, la pièce demeure.
"""

NOTE_INDEX = """
preuves-run-loupe-dev3/  LE TROISIÈME REFUS TERRAIN M10-(e) — le run
                         loupe dev.3 du 09/11/2026 : LE VRAI
                         CHARGEUR A CARTOGRAPHIÉ L'IMAGE (la première
                         fois au terrain — l'enveloppe de l'Entrée 205
                         PROUVÉE, plus de refus 0xc000007b), puis LE
                         TÉMOIN A NOMMÉ AU T0 : ÉCHEC NOMMÉ [CADRE-NÉ]
                         — « le CADRE .data n'est pas né poignée
                         INVALIDE (l'initialiseur du build) ».
                         Pièces : temoin-loupe.txt (522 o, md5
                         72761cd6… — l'empreinte ASSERTÉE
                         b494ff90…, les [T0] constatés, la ligne
                         d'échec) + VERDICT-run-loupe-dev3.txt
                         (ROUGE — l'échec nommé ; l'autopsie : le
                         sentinel à +8 au lieu de +528, UNE TAILLE
                         prise pour un offset ; la retouche dev.4
                         née : l'initialiseur .data MIROIR EXACT du
                         CADRE_VIERGE du harnais). Dossier déplacé de
                         preuves-loupe/ par DÉPLACEMENT (D143) ;
                         preuves-loupe/ demeure LE réceptacle (ré-armé
                         par la vague dev.4).
"""


def refus(nom, detail):
    print(f"[archive] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def main():
    print("=== M10-(e) : LE TÉMOIN ROUGE DU RUN dev.3 ARCHIVÉ SUR PIÈCES "
          "(D143 — l'Entrée 206) ===")

    # -- 1. le témoin au réceptacle, recoupé ---------------------------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        refus("RÉCEPTACLE", "preuves-loupe/ introuvable au /test")
    pieces = ds.list_folder(receptacle["id"])
    temoin = pieces.get("temoin-loupe.txt")
    if temoin is None:
        deja = ds.list_folder(ARCHIVES_PREUVES_ID).get(DOSSIER_ARCHIVE)
        if deja:
            arch = ds.list_folder(deja["id"])
            if arch.get("temoin-loupe.txt", {}).get("md5Checksum") == TEMOIN_MD5:
                print("[1] le témoin déjà archivé — idempotent")
                return 0
        refus("TÉMOIN", "temoin-loupe.txt introuvable au réceptacle "
                        "preuves-loupe/ et à l'archive")
    md5_avant = temoin.get("md5Checksum")
    if md5_avant != TEMOIN_MD5:
        refus("TÉMOIN", f"md5 {md5_avant} != l'attendu {TEMOIN_MD5} — "
                        "ce n'est pas le témoin du run dev.3")
    url = (ds.API + f"/files/{temoin['id']}?alt=media")
    st, corps, _ = ds.api("GET", url)
    if st != 200 or md5_bytes(corps) != TEMOIN_MD5:
        refus("TÉMOIN", "le téléchargement ne recoupe pas le md5")
    print(f"[1] le témoin dev.3 recoupé : 522 o, md5 {md5_avant[:8]}… — "
          f"la ligne d'échec [CADRE-NÉ] DANS la pièce")

    # -- 2. le dossier d'archive né ------------------------------------------
    archives = ds.list_folder(ARCHIVES_PREUVES_ID)
    dossier = archives.get(DOSSIER_ARCHIVE)
    if dossier is None:
        dossier_id = ds.create_folder(ARCHIVES_PREUVES_ID, DOSSIER_ARCHIVE)
        print(f"[2] {DOSSIER_ARCHIVE}/ né aux archives-preuves")
    else:
        dossier_id = dossier["id"]
        print(f"[2] {DOSSIER_ARCHIVE}/ déjà présent — idempotent")

    # -- 3. le témoin DÉPLACÉ (addParents/removeParents) ---------------------
    if temoin is not None:
        url = (ds.API + f"/files/{temoin['id']}"
               f"?addParents={dossier_id}&removeParents={receptacle['id']}")
        st, rep, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            refus("DÉPLACEMENT", f"HTTP {st} : {rep[:150]!r}")
        apres = ds.list_folder(dossier_id).get("temoin-loupe.txt")
        if (not apres or apres.get("md5Checksum") != TEMOIN_MD5
                or "temoin-loupe.txt" in ds.list_folder(receptacle["id"])):
            refus("DÉPLACEMENT", "md5 divergent ou la pièce demeure au "
                                "réceptacle après le geste")
        print(f"[3] temoin-loupe.txt DÉPLACÉ → {DOSSIER_ARCHIVE}/ "
              f"(md5 {TEMOIN_MD5[:8]}… recoupé APRÈS — le refus est un "
              f"FAIT, la pièce demeure)")

    # -- 4. le verdict du run déposé dans l'archive ---------------------------
    verdict = ds.list_folder(dossier_id).get("VERDICT-run-loupe-dev3.txt")
    if verdict is None:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                          encoding="utf-8",
                                          newline="\r\n") as f:
            f.write(VERDICT)
            chemin = f.name
        try:
            ds.upload_create(dossier_id, "VERDICT-run-loupe-dev3.txt",
                             pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        apres = ds.list_folder(dossier_id).get("VERDICT-run-loupe-dev3.txt")
        if not apres:
            refus("VERDICT", "absent après le dépôt")
        print(f"[4] VERDICT-run-loupe-dev3.txt déposé ({apres.get('size', 0)} o "
              f"— le dossier porte le jugement AVEC les pièces)")
    else:
        print("[4] VERDICT-run-loupe-dev3.txt déjà déposé — idempotent")

    # -- 5. l'index mis à jour --------------------------------------------------
    st, corps, _ = ds.api("GET", ds.API + f"/files/{INDEX_ID}?alt=media")
    ancien = corps.decode("utf-8")
    if DOSSIER_ARCHIVE + "/" in ancien:
        print("[5] l'index porte déjà la ligne du run loupe dev.3 — idempotent")
    else:
        marque = "— Fin de l'index (aucune allégation sans pièce citée) —"
        if marque not in ancien:
            refus("INDEX", "la marque de fin introuvable — l'index a bougé ?")
        nouveau = ancien.replace(marque, NOTE_INDEX.rstrip("\n") + "\n\n" + marque)
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(nouveau)
            chemin = f.name
        try:
            ds.upload_update(INDEX_ID, pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        print("[5] LISEZMOI-archives-preuves.txt mis à jour (la ligne du "
              "TROISIÈME REFUS terrain — le pas décisif ET l'échec nommé)")

    # -- 6. vérification finale -------------------------------------------------
    apres = ds.list_folder(receptacle["id"])
    if "temoin-loupe.txt" in apres:
        refus("ÉTAT-FINAL", "le témoin demeure au réceptacle après le geste")
    if not apres.get("LISEZMOI-preuves.txt"):
        refus("ÉTAT-FINAL", "le LISEZMOI du réceptacle a disparu "
                            "(la vague dev.4 le ré-arme)")
    arch = ds.list_folder(dossier_id)
    for piece in ("temoin-loupe.txt", "VERDICT-run-loupe-dev3.txt"):
        if not arch.get(piece):
            refus("ÉTAT-FINAL", f"{piece} absent de l'archive")
    print("[6] LE RÉCEPTACLE DEMEURE (preuves-loupe/ et son LISEZMOI) ; "
          "l'archive porte le témoin + le verdict")
    print("=== LE TÉMOIN ROUGE dev.3 ARCHIVÉ — le refus est un FAIT, la pièce "
          "demeure ; la retouche dev.4 part au terrain ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
