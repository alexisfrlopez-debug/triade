#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_loupe_dev4.py — LE TÉMOIN DU RUN dev.4 ARCHIVÉ SUR PIÈCES
(règle D143 : archivage par DÉPLACEMENT, jamais un jet).

LE QUATRIÈME RUN TERRAIN (l'Entrée 207) : « preuves-loupe déposées dans
le dossier /test du drive. quand je lance l'exe, la fenêtre s'ouvre et
se referme immédiatement » — le développeur a déposé SON DOSSIER KIT
ENTIER au /test (loupe-kit/ avec l'artefact relu, le scénario, le
LISEZMOI ET preuves-loupe/temoin-loupe.txt 1 209 o) : LE RUN LE PLUS
LOIN JAMAIS VÊCU — [T0] l'image cartographiée DONT_RESOLVE
@ 0x7ff600600000 (l'enveloppe PROUVÉE, la carte 206 TENUE : le CADRE
né MIROIR), l'IAT 37 feuilles posées — puis [T1] ÉCHEC NOMMÉ
[SESSION] : loupe-01 a rendu 0xfffffffa (-6 SYSTÈME — le fichier
pourtant relu à l'instant). ET LA VITRINE A VÉCU SA PREMIÈRE FOIS :
« la fenêtre s'ouvre et se referme immédiatement » — LA MORT SANS
TÉMOIN : le kit dev.5 PORTE DÉSORMAIS SON TÉMOIN VITRINE.

L'autopsie de labo a nommé LA CLASSE : les arguments 5+ de l'ABI msx64
au HOME SPACE au lieu de [rsp+0x20]+ (loupe-01 : la disposition lue à
la pile non initialisée ; loupe-05 : le contexte SHA au vrai slot —
H0[0] 0x6A09E667… lu comme un POINTEUR ; loupe-06 pareil) + DEUX AXES
NOMMÉS PAR L'AUDIT D'ABI DU BUILD (loupe-10 le sous-programme .peindre
pile ≡8 ; loupe-11 le cadre 0x38) — la retouche dev.5 est NÉE.

  1. LE TÉMOIN RAPATRIÉ ET RECOUPÉ (md5 7bb40bae… — 1 209 o, la ligne
     d'échec [SESSION] DANS la pièce) ;
  2. LE DOSSIER D'ARCHIVE né aux archives-preuves :
     preuves-run-loupe-dev4/ ;
  3. LE TÉMOIN DÉPLACÉ (addParents/removeParents — DÉPLACEMENT,
     jamais une copie) + md5 recoupé APRÈS ;
  4. LE VERDICT DU RUN déposé dans l'archive (VERDICT-run-loupe-
     dev4.txt : ROUGE AU T1, LE PAS LE PLUS LOIN — et la vitrine sans
     témoin) ;
  5. L'INDEX MIS À JOUR : LISEZMOI-archives-preuves.txt ;
  6. LE RÉCEPTACLE demeure avec son LISEZMOI (preuves-loupe/ —
     ré-armé par la vague dev.5).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/archiver_run_loupe_dev4.py
Code de sortie : 0 = témoin archivé ; 2 = refus nommé."""

import hashlib
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

TEMOIN_MD5 = "7bb40bae40d88a9d8b884742a6f17db5"   # le témoin dev.4 (1 209 o)
DOSSIER_ARCHIVE = "preuves-run-loupe-dev4"

VERDICT = """VERDICT DU RUN TERRAIN M10-(e) — LOUPE dev.4 : ROUGE AU T1 (LE PAS LE PLUS LOIN) + LA VITRINE SANS TÉMOIN
================================================================================================================
Le run du 09/11/2026 (le kit dev.4, la vague de l'Entrée 206 — le
dossier kit entier déposé par le développeur au /test/loupe-kit/) :

  - [T0] LE RUN LE PLUS LOIN JAMAIS VÊCU : l'empreinte ASSERTÉE
    (loupe.exe 127 488 o, sha256 1f2da2833b47265e…), L'IMAGE
    CARTOGRAPHIÉE DONT_RESOLVE @ 0x7ff600600000, LE CADRE NÉ MIROIR DU
    CADRE_VIERGE (la poignée INVALIDE à +528 — LA RETOUCHE DE L'ENTÉE
    206 TIENT, PREUVE AU TERRAIN), les adresses scellées CONSTATÉES,
    l'IAT 37 feuilles posées — TOUT LE T0 VERT.
  - [T1] ÉCHEC NOMMÉ [SESSION] : « loupe-01 a rendu 0xfffffffa (-6
    SYSTÈME — le fichier pourtant relu à l'instant) ».
  - ET LA VITRINE A VÉCU SA PREMIÈRE FOIS AU TERRAIN : « quand je
    lance l'exe, la fenêtre s'ouvre et se referme immédiatement » —
    LA MORT SANS TÉMOIN.

L'AUTOPSIE DE LABO SUR LA PIÈCE (capstone, les notations, le harnais)
A NOMMÉ LA CLASSE DES ARGUMENTS PILE : les arguments 5+ de l'ABI msx64
vivaient AU HOME SPACE [rsp..0x18] au lieu de [rsp+0x20]+ —
  - loupe-01 : le VRAI CreateFileW lisait dwCreationDisposition À LA
    PILE NON INITIALISÉE → le refus OS → -6 (LA LIGNE DU TÉMOIN) ;
  - loupe-05 : le contexte SHA (112 o) VIVAIT SUR LE VRAI SLOT — le
    VRAI ReadFile lisait H0[0] 0x6A09E667… COMME UN POINTEUR — la
    vitrine avec fichier explique SA mort : l'access violation tue le
    processus (« s'ouvre et se referme immédiatement ») ;
  - loupe-06 : le contexte MD5 (88 o) pareil (A = 0x67452301…).
ET DEUX AXES NOMMÉS PAR L'AUDIT D'ABI DU BUILD (la pièce neuve du
dev.5) : loupe-10 le sous-programme .peindre appelait TextOutW pile
≡8 (le VRAI gdi32 SSE peut fautter là où l'émulation passe) ;
loupe-11 le cadre 0x38 laissait TOUS ses appels IAT pile ≡8.

LA RETOUCHE dev.5 EST NÉE (l'Entrée 207) : les TROIS notations à
leurs vrais slots + les DEUX réalignements + LE GARDE GUÉRI PAR LA
CONVENTION (les shims CreateFileW/ReadFile/WriteFile RELISENT LES
MÊMES SLOTS QUE LE VRAI — le défaut ne passerait plus jamais le
labo, V7 le prouve sur la falsification demandée) + LE TÉMOIN
VITRINE AU KIT (temoin-vitrine.bat — la prochaine mort sera nommée).

Un échec nommé vaut plus qu'un vert muet (charte § 9). Le labo
recoupe sur pièces (D138/D145/D148) ; l'archivage est un DÉPLACEMENT
(D143) — le refus du terrain est un FAIT, la pièce demeure.
"""

NOTE_INDEX = """
preuves-run-loupe-dev4/  LE QUATRIÈME RUN TERRAIN M10-(e) — le run
                         loupe dev.4 du 09/11/2026 : LE PLUS LOIN
                         JAMAIS VÊCU ([T0] l'image cartographiée, LE
                         CADRE NÉ MIROIR — la retouche de l'Entrée
                         206 TENUE au terrain, l'IAT 37 feuilles)
                         PUIS [T1] ÉCHEC NOMMÉ [SESSION] : loupe-01 a
                         rendu -6 SYSTÈME (le fichier pourtant relu à
                         l'instant) ; ET LA VITRINE A VÉCU SA PREMIÈRE
                         FOIS (« la fenêtre s'ouvre et se referme
                         immédiatement » — la mort SANS témoin).
                         Pièces : temoin-loupe.txt (1 209 o, md5
                         7bb40bae… — l'empreinte ASSERTÉE 1f2da283…,
                         les [T0] constatés, la ligne [SESSION]) +
                         VERDICT-run-loupe-dev4.txt (l'autopsie : LA
                         CLASSE DES ARGUMENTS PILE au home space —
                         loupe-01/05/06 — + les deux axes d'alignement
                         nommés par l'audit du build — loupe-10/11 ;
                         la retouche dev.5 née : les vrais slots, le
                         garde guéri par la convention, LE TÉMOIN
                         VITRINE au kit). Le témoin DÉPLACÉ du dossier
                         kit du développeur (/test/loupe-kit/) par
                         DÉPLACEMENT (D143) ; preuves-loupe/ demeure
                         LE réceptacle (ré-armé par la vague dev.5).
"""


def refus(nom, detail):
    print(f"[archive] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def main():
    print("=== M10-(e) : LE TÉMOIN DU RUN dev.4 ARCHIVÉ SUR PIÈCES "
          "(D143 — l'Entrée 207) ===")

    # -- 1. le témoin au dossier kit du développeur, recoupé ----------------
    test = ds.list_folder(TEST_ID)
    kit = test.get("loupe-kit")
    if not kit or kit.get("mimeType") != ds.FOLDER_MIME:
        refus("DOSSIER-KIT", "/test/loupe-kit/ introuvable au /test")
    pieces = ds.list_folder(kit["id"])
    receptacle_kit = pieces.get("preuves-loupe")
    if not receptacle_kit or receptacle_kit.get("mimeType") != ds.FOLDER_MIME:
        # le témoin peut avoir été déjà déplacé par un run antérieur du script
        receptacle_kit = None
    temoin = None
    if receptacle_kit:
        temoin = ds.list_folder(receptacle_kit["id"]).get("temoin-loupe.txt")
    if temoin is None:
        deja = ds.list_folder(ARCHIVES_PREUVES_ID).get(DOSSIER_ARCHIVE)
        if deja:
            arch = ds.list_folder(deja["id"])
            if arch.get("temoin-loupe.txt", {}).get("md5Checksum") == TEMOIN_MD5:
                print("[1] le témoin déjà archivé — idempotent")
                return 0
        refus("TÉMOIN", "temoin-loupe.txt introuvable au dossier kit du "
                        "développeur ET à l'archive")
    md5_avant = temoin.get("md5Checksum")
    if md5_avant != TEMOIN_MD5:
        refus("TÉMOIN", f"md5 {md5_avant} != l'attendu {TEMOIN_MD5} — "
                        "ce n'est pas le témoin du run dev.4")
    url = (ds.API + f"/files/{temoin['id']}?alt=media")
    st, corps, _ = ds.api("GET", url)
    if st != 200 or md5_bytes(corps) != TEMOIN_MD5:
        refus("TÉMOIN", "le téléchargement ne recoupe pas le md5")
    print(f"[1] le témoin dev.4 recoupé : 1 209 o, md5 {md5_avant[:8]}… — "
          f"la ligne [SESSION] DANS la pièce")

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
    url = (ds.API + f"/files/{temoin['id']}"
           f"?addParents={dossier_id}&removeParents={receptacle_kit['id']}")
    st, rep, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        refus("DÉPLACEMENT", f"HTTP {st} : {rep[:150]!r}")
    apres = ds.list_folder(dossier_id).get("temoin-loupe.txt")
    if (not apres or apres.get("md5Checksum") != TEMOIN_MD5
            or "temoin-loupe.txt" in ds.list_folder(receptacle_kit["id"])):
        refus("DÉPLACEMENT", "md5 divergent ou la pièce demeure au dossier "
                             "kit après le geste")
    print(f"[3] temoin-loupe.txt DÉPLACÉ → {DOSSIER_ARCHIVE}/ "
          f"(md5 {TEMOIN_MD5[:8]}… recoupé APRÈS — le refus est un FAIT, "
          f"la pièce demeure)")

    # -- 4. le verdict du run déposé dans l'archive ---------------------------
    verdict = ds.list_folder(dossier_id).get("VERDICT-run-loupe-dev4.txt")
    if verdict is None:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                          encoding="utf-8",
                                          newline="\r\n") as f:
            f.write(VERDICT)
            chemin = f.name
        try:
            ds.upload_create(dossier_id, "VERDICT-run-loupe-dev4.txt",
                             pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        apres = ds.list_folder(dossier_id).get("VERDICT-run-loupe-dev4.txt")
        if not apres:
            refus("VERDICT", "absent après le dépôt")
        print(f"[4] VERDICT-run-loupe-dev4.txt déposé ({apres.get('size', 0)} o "
              f"— le dossier porte le jugement AVEC les pièces)")
    else:
        print("[4] VERDICT-run-loupe-dev4.txt déjà déposé — idempotent")

    # -- 5. l'index mis à jour -------------------------------------------------
    st, corps, _ = ds.api("GET", ds.API + f"/files/{INDEX_ID}?alt=media")
    ancien = corps.decode("utf-8")
    if DOSSIER_ARCHIVE + "/" in ancien:
        print("[5] l'index porte déjà la ligne du run loupe dev.4 — idempotent")
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
              "QUATRIÈME run — le pas le plus loin ET la vitrine sans témoin)")

    # -- 6. vérification finale -------------------------------------------------
    apres_kit = ds.list_folder(receptacle_kit["id"])
    if "temoin-loupe.txt" in apres_kit:
        refus("ÉTAT-FINAL", "le témoin demeure au dossier kit après le geste")
    if not ds.list_folder(TEST_ID).get("preuves-loupe"):
        refus("ÉTAT-FINAL", "le réceptacle preuves-loupe/ a disparu du /test")
    arch = ds.list_folder(dossier_id)
    for piece in ("temoin-loupe.txt", "VERDICT-run-loupe-dev4.txt"):
        if not arch.get(piece):
            refus("ÉTAT-FINAL", f"{piece} absent de l'archive")
    print("[6] LE RÉCEPTACLE DEMEURE (preuves-loupe/ au /test) ; l'archive "
          "porte le témoin + le verdict")
    print("=== LE TÉMOIN dev.4 ARCHIVÉ — le refus est un FAIT, la pièce "
          "demeure ; la retouche dev.5 part au terrain ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
