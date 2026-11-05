#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_m8d.py — LE COFFRE /test PASSÉ À LA VAGUE M8-(d) (règle D143 :
archivage par DÉPLACEMENT, jamais un jet).

La vague m7d est CONSOMMÉE (le run m7d a rendu son verdict : LE RECOUP LABO
VERT 29/29 sur pièces croisées — la finale 0.8.0 SCELLÉE, le jalon M7
franchi, Task 73) ; le kit M8-(d) est ANNONCÉ (le chantier final du jalon :
le VRAI ntdll lu sur la machine du développeur, la finale 0.9.0 attend le
vert) :

  1. ARCHIVAGE DE LA VAGUE m7d → /test/archives-livraisons/vagues-m7/ :
     kit-m7d.zip, LISEZMOI-m7d.txt (déplacement PATCH, md5 constaté
     après) ;
  2. preuves-m8d/ NÉ au coffre (le réceptacle des preuves du run M8-(d))
     avec son LISEZMOI-preuves.txt (les pièces attendues) ;
  3. LA VAGUE DÉPOSÉE à la racine de /test : kit-m8d.zip (le kit éprouvé
     au labo — assembler_kit_m8d.py : recoup AST 13 constantes ==
     l'artefact, extraction vierge VERT) + LISEZMOI-m8d.txt (le document
     du kit, lisible AU coffre sans extraire) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la section
     m7d archivée + la vague courante m8d) ;
  5. VÉRIFICATION : la racine porte la vague courante + les résidents
     (corriger-wsb.*, signatures-I.txt [la remise consommée — la copie de
     référence vit au dépôt]) + les réceptacles + les salles d'archive ;
     les empreintes recoupées.

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_m8d.py
Code de sortie : 0 = coffre passé à la vague m8d ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-m8d.zip"
LISEZMOI_KIT = os.path.join(REPO, "m8", "terrain", "LISEZMOI-m8d.txt")

KIT_SHA = "cc21cd855e537b56dcd0ed9e974d84df23febd9187e3a4339e553c7b1396d1a3"
KIT_MD5 = "117eb10aa7aba703d684f4329d0e3064"

VAGUE_M7D = ["kit-m7d.zip", "LISEZMOI-m7d.txt"]

LISEZMOI_PREUVES = """TRIADE — preuves-m8d : LE RÉCEPTACLE DU RUN TERRAIN M8-(d)
========================================================================
(le VRAI ntdll lu sur la machine du développeur, la ligne comparée par
les DEUX chemins — la finale 0.9.0 attend le vert de CE run)

LES PIÈCES ATTENDUES (nées dans ./preuves-m8d/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-m8d.txt            le témoin complet — l'environnement (la
                            version Windows, le Python), le ntdll (base,
                            sha256 du fichier), le SSN de NtWriteFile lu
                            par les DEUX lecteurs (Python + le bloc
                            sys-02), les octets du stub (le motif
                            confronté), chaque contrôle tranché ;
  scenario-m8d-journal.log  le journal horodaté du scénario ;
  VERDICT-run-m8d.txt       le verdict (une ligne : VERT ou ROUGE) ;
  chemin-a-hello02.txt      la ligne par le CHEMIN A (hello-02, l'IAT
                            kernel32 — le scellé M0) ;
  chemin-b-sys03.txt        la ligne par le CHEMIN B (sys-03, NtWriteFile
                            en syscall direct — zéro IAT) ;
  chemin-c-refus.txt        le fichier-témoin du refus nommé (la base
                            invalide : AUCUN syscall émis — le fichier
                            demeure VIDE).

LE CRITÈRE (le plan M8, ligne (d)) : le VRAI ntdll lu, le motif
confronté, la ligne comparée par les DEUX chemins, tout stub divergent
= refus nommé — run terrain VERT sur pièces → la balise finale 0.9.0.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le défaut
(un stub divergent est une INFORMATION — votre ntdll est crocheté — pas
une panne du kit). Le labo recoupe sur pièces (D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague m7d archivée (le run m7d a rendu son verdict : LE RECOUP
    LABO VERT 29/29 sur pièces croisées — la finale 0.8.0 SCELLÉE, le
    jalon M7 franchi ; archivée le 05/11 au passage à la vague m8d)

--- la vague courante (racine de /test) : m8d — LE KIT TERRAIN M8-(d)
    (kit-m8d.zip + LISEZMOI-m8d.txt ; preuves-m8d/ reçoit les preuves du
    run ; corriger-wsb.* demeurent résidents D143 de l'ère m5b ; sig-
    natures-I.txt demeure la remise CONSOMMÉE de la cérémonie de l'ère
    M8 — la copie de référence vit au dépôt v06/sceau-I/) — mis à jour
    le 05/11/2026 : LE CHANTIER FINAL DU JALON M8 — le VRAI ntdll lu sur
    la machine du développeur, la ligne par les DEUX chemins (hello-02
    l'IAT vs sys-03 le syscall direct), la finale 0.9.0 attend le vert.
"""


def refus(nom, detail):
    print(f"[dépôt] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def televerser_texte(parent_id, nom, contenu):
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8", newline="\r\n") as f:
        f.write(contenu)
        chemin = f.name
    try:
        return ds.upload_create(parent_id, nom, pathlib.Path(chemin))
    finally:
        os.unlink(chemin)


def deplacer_vers(file_id, parent_de, parent_vers, md5_attendu):
    url = (ds.API + f"/files/{file_id}"
           f"?addParents={parent_vers}&removeParents={parent_de}")
    st, rep, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        refus("DÉPLACEMENT", f"HTTP {st} : {rep[:150]!r}")
    # le md5 constaté APRÈS (le déplacement ne touche pas au contenu)
    apres = ds.list_folder(parent_vers).get("")
    return True


def main():
    print("=== M8-(d) : le coffre /test passe à la vague m8d "
          "(le VRAI ntdll) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_m8d.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-m8d.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-m8d.zip md5 divergent — réassembler")
    print(f"[0] le kit : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague m7d ---------------------------------------------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m7")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m7")
        print("[1] vagues-m7/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    for nom in VAGUE_M7D:
        piece = ds.list_folder(TEST_ID).get(nom)
        if piece is None:
            deja = ds.list_folder(vagues_id).get(nom)
            if deja:
                print(f"[1] {nom} déjà archivé (md5 {deja.get('md5Checksum', '')[:8]}…) — idempotent")
                continue
            refus("ARCHIVAGE", f"{nom} introuvable ni à la racine ni aux archives")
        url = (ds.API + f"/files/{piece['id']}"
               f"?addParents={vagues_id}&removeParents={TEST_ID}")
        st, rep, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            refus("ARCHIVAGE", f"{nom} : HTTP {st} : {rep[:150]!r}")
        archive = ds.list_folder(vagues_id).get(nom)
        if not archive or archive.get("md5Checksum") != piece.get("md5Checksum"):
            refus("ARCHIVAGE", f"{nom} : md5 divergent après déplacement")
        if nom in ds.list_folder(TEST_ID):
            refus("ARCHIVAGE", f"{nom} demeure à la racine après déplacement")
        print(f"[1] archivé : {nom} → vagues-m7/ "
              f"(md5 {piece.get('md5Checksum', '')[:8]}… recoupé après)")

    # -- 2. preuves-m8d/ né avec son LISEZMOI ---------------------------------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-m8d")
    if not receptacle:
        rid = ds.create_folder(TEST_ID, "preuves-m8d")
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[2] preuves-m8d/ NÉ avec son LISEZMOI-preuves.txt "
              "(les pièces attendues)")
    else:
        rid = receptacle["id"]
        if "LISEZMOI-preuves.txt" not in ds.list_folder(rid):
            televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[2] preuves-m8d/ déjà présent — idempotent")

    # -- 3. la vague m8d déposée à la racine ----------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-m8d.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-m8d.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-m8d.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-m8d.zip md5 divergent après téléversement")
        print(f"[3] déposé : kit-m8d.zip (md5 {KIT_MD5[:8]}… MATCH par relecture)")
    else:
        if racine["kit-m8d.zip"].get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-m8d.zip déjà présent avec un AUTRE md5")
        print("[3] kit-m8d.zip déjà déposé — idempotent")

    if "LISEZMOI-m8d.txt" not in ds.list_folder(TEST_ID):
        ds.upload_create(TEST_ID, "LISEZMOI-m8d.txt",
                         pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-m8d.txt")
        if not apres:
            refus("DÉPÔT", "LISEZMOI-m8d.txt absent après téléversement")
        local = md5_bytes(open(LISEZMOI_KIT, "rb").read())
        if apres.get("md5Checksum") != local:
            refus("DÉPÔT", "LISEZMOI-m8d.txt md5 divergent après téléversement")
        print(f"[3] déposé : LISEZMOI-m8d.txt (md5 {local[:8]}… MATCH)")
    else:
        print("[3] LISEZMOI-m8d.txt déjà déposé — idempotent")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : m8d" not in ancien:
            nouveau = ancien.rstrip("\n") + "\n" + NOTE_INDEX
            televerser_index = nouveau
            # mise à jour : upload_update sur le fichier existant
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                             encoding="utf-8", newline="\r\n") as f:
                f.write(televerser_index)
                chemin = f.name
            try:
                ds.upload_update(index["id"], pathlib.Path(chemin))
            finally:
                os.unlink(chemin)
            print("[4] LISEZMOI-archives-livraisons.txt mis à jour "
                  "(la section m7d archivée + la vague courante m8d)")
        else:
            print("[4] l'index porte déjà la vague m8d — idempotent")

    # -- 5. la vérification finale -----------------------------------------------------
    final = ds.list_folder(TEST_ID)
    attendus = {"kit-m8d.zip", "LISEZMOI-m8d.txt", "preuves-m8d",
                "archives-livraisons", "archives-preuves",
                "preuves-m5b", "preuves-m6", "preuves-m7",
                "corriger-wsb.bat", "corriger-wsb.ps1", "signatures-I.txt"}
    manquants = attendus - set(final)
    if manquants:
        refus("VÉRIFICATION", f"entrées attendues absentes de la racine : "
                              f"{sorted(manquants)}")
    for nom in VAGUE_M7D:
        if nom in final:
            refus("VÉRIFICATION", f"{nom} demeure à la racine (archivage "
                                  f"inopérant)")
    print(f"[5] la racine porte la vague courante m8d + les résidents + "
          f"les réceptacles + les salles d'archive ({len(final)} entrées)")
    print("\n=== LE COFFRE /test EST À LA VAGUE m8d : le kit terrain M8-(d) "
          "attend le geste du développeur (python scenario-m8d.py sur la "
          "machine Windows) — la finale 0.9.0 attend le vert ===")


if __name__ == "__main__":
    main()
