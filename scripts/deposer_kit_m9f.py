#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_m9f.py — LE COFFRE /test PASSÉ À LA VAGUE M9-(f) (règle D143 :
archivage par DÉPLACEMENT, jamais un jet).

La vague m8d est CONSOMMÉE (le run m8d a rendu son verdict : VERT sur
pièces — la finale 0.9.0 SCELLÉE, le jalon M8 franchi, Entrée 164) ; le
kit M9-(f) est ANNONCÉ (LE DERNIER CHANTIER DU JALON : la session
RÉELLE, LA GRANDE ŒUVRE — la finale 1.0.0 attend le vert) :

  1. ARCHIVAGE DE LA VAGUE m8d → /test/archives-livraisons/vagues-m8/ :
     kit-m8d.zip, LISEZMOI-m8d.txt (déplacement PATCH, md5 constaté
     après) ;
  2. preuves-m9f/ NÉ au coffre (le réceptacle des preuves du run
     M9-(f)) avec son LISEZMOI-preuves.txt (les pièces attendues) ;
  3. LA VAGUE DÉPOSÉE à la racine de /test : kit-m9f.zip (le kit éprouvé
     au labo — assembler_kit_m9f.py : recoup AST 26 constantes ==
     l'artefact/le plan/la sonde — dont L'OCTET 0x72 DE L'ERRATUM n° 5
     relu dans l'image —, extraction vierge VERT) + LISEZMOI-m9f.txt
     (le document du kit, lisible AU coffre sans extraire) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la section
     m8d archivée + la vague courante m9f) ;
  5. VÉRIFICATION : la racine porte la vague courante + les résidents
     + les réceptacles + les salles d'archive ; les empreintes recoupées.

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_m9f.py
Code de sortie : 0 = coffre passé à la vague m9f ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-m9f.zip"
LISEZMOI_KIT = os.path.join(REPO, "tls13", "terrain", "LISEZMOI-KIT-M9F.md")

KIT_SHA = "5f30b34e480d0cc727737e893d57295205127168cefc1c9904826072d719fc99"
KIT_MD5 = "a73fb526222fae848aed877b5433deef"

VAGUE_M8D = ["kit-m8d.zip", "LISEZMOI-m8d.txt"]

LISEZMOI_PREUVES = """TRIADE — preuves-m9f : LE RÉCEPTACLE DU RUN TERRAIN M9-(f)
========================================================================
(LA SESSION RÉELLE — LA GRANDE ŒUVRE : la finale 1.0.0 attend le vert
de CE run ; l'artefact 1.0.0-dev.2, la carte génération 10)

LES PIÈCES ATTENDUES (nées dans ./preuves-m9f/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-m9f.txt            le témoin complet — l'environnement (la
                            version Windows, le Python), le ntdll (base,
                            sha256 du fichier), les SSN des TROIS noms du
                            transport lus par les DEUX lecteurs (Python +
                            le bloc sys-02), l'empreinte ÉPINGLÉE, la
                            cible résolue, chaque contrôle tranché ;
  scenario-m9f-journal.log  le journal horodaté du scénario ;
  VERDICT-run-m9f.txt       le verdict (VERT ou ROUGE nommé) ;
  ligne-recue.txt           LA LIGNE APPLICATIVE DÉCHIFFRÉE PAR LA
                            MACHINE (la réponse HTTP reçue chiffrée,
                            restituée en clair par le client TLS 1.3 de
                            l'artefact) ;
  journal-emissions.txt    TOUT ce que la machine a émis (le CH recoupé
                            octet par octet, le Finished client, la ligne
                            scellée, le close_notify).

LE CRITÈRE (le plan M9, ligne (f)) : la session TLS 1.3 RÉELLE avec un
serveur réel — la suite arrêtée proposée, le VRAI ntdll lu par sys-02,
les sockets par SYSCALLS, l'épinglage de l'empreinte attendue, la
ligne applicative chiffrée échangée — run terrain VERT sur pièces →
la balise finale 1.0.0 (fait de carte, D104) : le jalon M9 franchi.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (p. ex. « -6 l'épinglage divergent » : le certificat de la
cible a été renouvelé depuis le gel du 06/11 — c'est la NATURE de
l'épinglage, pas une panne du kit). Le labo recoupe sur pièces
(D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague m8d archivée (le run m8d a rendu son verdict : VERT sur
    pièces — la finale 0.9.0 SCELLÉE, le jalon M8 franchi ; archivée le
    06/11 au passage à la vague m9f)

--- la vague courante (racine de /test) : m9f — LE KIT TERRAIN M9-(f),
    LA GRANDE ŒUVRE (kit-m9f.zip + LISEZMOI-m9f.txt ; preuves-m9f/
    reçoit les preuves du run ; signatures-I.txt demeure la remise
    CONSOMMÉE de la cérémonie du build 1.0.0 — la copie de référence
    vit au dépôt v06/sceau-I/) — mis à jour le 06/11/2026 : LE DERNIER
    CHANTIER DU JALON — la session RÉELLE (le VRAI ntdll, les sockets
    par les VRAIS syscalls AFD, l'épinglage, la ligne chiffrée), la
    finale 1.0.0 attend le vert. L'ARTEFACT EST LE BUILD 1.0.0-dev.2
    (l'erratum n° 5 : la sonde du labo a nommé l'octet de longueur du
    record CH et le CCS hérité AVANT le terrain — la spécification
    scellée disait juste, la notation a été réparée à la source).
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


def main():
    print("=== M9-(f) : le coffre /test passe à la vague m9f "
          "(LA GRANDE ŒUVRE) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_m9f.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-m9f.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-m9f.zip md5 divergent — réassembler")
    print(f"[0] le kit : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague m8d ---------------------------------------------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m8")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m8")
        print("[1] vagues-m8/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    for nom in VAGUE_M8D:
        piece = ds.list_folder(TEST_ID).get(nom)
        if piece is None:
            deja = ds.list_folder(vagues_id).get(nom)
            if deja:
                print(f"[1] {nom} déjà archivé (md5 "
                      f"{deja.get('md5Checksum', '')[:8]}…) — idempotent")
                continue
            refus("ARCHIVAGE", f"{nom} introuvable ni à la racine ni aux "
                               f"archives")
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
        print(f"[1] archivé : {nom} → vagues-m8/ "
              f"(md5 {piece.get('md5Checksum', '')[:8]}… recoupé après)")

    # -- 2. preuves-m9f/ né avec son LISEZMOI ---------------------------------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-m9f")
    if not receptacle:
        rid = ds.create_folder(TEST_ID, "preuves-m9f")
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[2] preuves-m9f/ NÉ avec son LISEZMOI-preuves.txt "
              "(les pièces attendues)")
    else:
        rid = receptacle["id"]
        if "LISEZMOI-preuves.txt" not in ds.list_folder(rid):
            televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[2] preuves-m9f/ déjà présent — idempotent")

    # -- 3. la vague m9f déposée à la racine ----------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-m9f.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-m9f.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-m9f.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-m9f.zip md5 divergent après téléversement")
        print(f"[3] déposé : kit-m9f.zip (md5 {KIT_MD5[:8]}… MATCH par "
              f"relecture)")
    else:
        if racine["kit-m9f.zip"].get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-m9f.zip déjà présent avec un AUTRE md5")
        print("[3] kit-m9f.zip déjà déposé — idempotent")

    if "LISEZMOI-m9f.txt" not in ds.list_folder(TEST_ID):
        ds.upload_create(TEST_ID, "LISEZMOI-m9f.txt",
                         pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-m9f.txt")
        if not apres:
            refus("DÉPÔT", "LISEZMOI-m9f.txt absent après téléversement")
        local = md5_bytes(open(LISEZMOI_KIT, "rb").read())
        if apres.get("md5Checksum") != local:
            refus("DÉPÔT", "LISEZMOI-m9f.txt md5 divergent après "
                           "téléversement")
        print(f"[3] déposé : LISEZMOI-m9f.txt (md5 {local[:8]}… MATCH)")
    else:
        print("[3] LISEZMOI-m9f.txt déjà déposé — idempotent")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : m9f" not in ancien:
            nouveau = ancien.rstrip("\n") + "\n" + NOTE_INDEX
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                             encoding="utf-8",
                                             newline="\r\n") as f:
                f.write(nouveau)
                chemin = f.name
            try:
                ds.upload_update(index["id"], pathlib.Path(chemin))
            finally:
                os.unlink(chemin)
            print("[4] LISEZMOI-archives-livraisons.txt mis à jour "
                  "(la section m8d archivée + la vague courante m9f)")
        else:
            print("[4] l'index porte déjà la vague m9f — idempotent")

    # -- 5. la vérification finale -----------------------------------------------------
    final = ds.list_folder(TEST_ID)
    attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                "archives-livraisons", "archives-preuves",
                "preuves-m8d", "corriger-wsb.bat", "corriger-wsb.ps1",
                "signatures-I.txt"}
    manquants = attendus - set(final)
    if manquants:
        refus("VÉRIFICATION", f"entrées attendues absentes de la racine : "
                              f"{sorted(manquants)}")
    for nom in VAGUE_M8D:
        if nom in final:
            refus("VÉRIFICATION", f"{nom} demeure à la racine (archivage "
                                  f"inopérant)")
    print(f"[5] la racine porte la vague courante m9f + les résidents + "
          f"les réceptacles + les salles d'archive ({len(final)} entrées)")
    print("\n=== LE COFFRE /test EST À LA VAGUE m9f : le kit terrain M9-(f) "
          "attend le geste du développeur (python scenario-m9f.py sur la "
          "machine Windows, réseau vivant) — LA GRANDE ŒUVRE : la finale "
          "1.0.0 attend le vert ===")


if __name__ == "__main__":
    main()
