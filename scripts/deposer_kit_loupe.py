#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_loupe.py — LE COFFRE /test PASSÉ À LA VAGUE LOUPE (règle D143 :
archivage par DÉPLACEMENT, jamais un jet).

La vague m9f est CONSOMMÉE (le septième run a rendu son verdict : VERT
sur pièces — la finale 1.0.0 SCELLÉE, le jalon M9 franchi, Entrée 193) ;
la vague LOUPE est livrée (M10-(e) : LE RUN DU GRANDEUR NATURE — la
première application née de TRIADE chez son utilisateur ; la balise
`loupe 0.1.0` attend le vert) :

  1. ARCHIVAGE DE LA VAGUE m9f → /test/archives-livraisons/vagues-m9/ :
     kit-m9f.zip, LISEZMOI-m9f.txt (déplacement PATCH, md5 constaté
     après) ;
  2. preuves-loupe/ NÉ au coffre (le réceptacle du run M10-(e)) avec
     son LISEZMOI-preuves.txt (les pièces attendues) ;
  3. LA VAGUE DÉPOSÉE à la racine de /test : kit-loupe.zip (le kit
     éprouvé au labo — assembler_kit_loupe.py : le recoup des
     constantes PAR AST == l'artefact/le plan/les scellés, extraction
     vierge VERT) + LISEZMOI-loupe.txt (le document du kit, lisible AU
     coffre sans extraire) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la section
     m9f archivée + la vague courante loupe) ;
  5. VÉRIFICATION : la racine porte la vague courante + les PIÈCES DE
     L'ÈRE DU TGN DEMEURÉES (signatures-I.txt la remise INSTALLÉE
     f33c803a… + cle-publique-I.txt l'ancre 188a7d42… — la vague ne
     touche JAMAIS aux pièces de cérémonie) + les réceptacles + les
     salles d'archive ; les empreintes recoupées.

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_loupe.py
Code de sortie : 0 = coffre passé à la vague loupe ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-loupe.zip"
LISEZMOI_KIT = os.path.join(REPO, "loupe", "terrain", "LISEZMOI-KIT-LOUPE.md")

KIT_SHA = "1689fc2022150fd8624a157522a258a6a20eeb6aa59b010ce470800f510f5586"
KIT_MD5 = "ee43c991455720fb162e3aedb43c3a6d"

VAGUE_M9F = ["kit-m9f.zip", "LISEZMOI-m9f.txt"]

# les pièces de cérémonie qui DEMEURENT à la racine (l'ère du TGN —
# la vague ne les touche JAMAIS : signatures-I.txt est la remise
# INSTALLÉE f33c803a…, cle-publique-I.txt l'ancre des ères 188a7d42…)
PIECES_ERE = {"signatures-I.txt": "f33c803aad80711995c6ea61ce30aa7b",
              "cle-publique-I.txt": "188a7d42df2d03f68bfb50fada3a84a1"}

LISEZMOI_PREUVES = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU RUN TERRAIN M10-(e)
========================================================================
(LE RUN DE LOUPE, LE GRANDEUR NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact 0.1.0-dev.1, la carte
génération 13 — la balise `loupe 0.1.0` se scellera sur le vert
recoupé)

LES PIÈCES ATTENDUES (nées dans ./preuves-loupe/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-loupe.txt   le témoin complet — l'environnement (Windows,
                     Python 64 bits), l'empreinte ASSERTÉE de
                     l'artefact, les adresses scellées CONSTATÉES (la
                     minilibc M1, la boucle démo, la famille sha M9,
                     la table K FIPS, le qword version R10), l'IAT
                     résolue par le scénario-chargeur, chaque contrôle
                     tranché (la session, la double lecture, les
                     lignes, la recherche, l'édition à l'octet, les
                     rejets nommés, la clôture) ;
  capture-*.png      LES CAPTURES DE LA VITRINE (optionnelles mais
                     bienvenues) : la fenêtre réelle après ouverture
                     d'un fichier de votre choix — l'entête, la grille
                     hexa, le miroir ASCII, LE PANNEAU D'EMPREINTES
                     (md5 + sha256) — la vie de l'application chez
                     vous, le cœur du grandeur nature.

LE CRITÈRE (le plan M10, rangée (e)) : le développeur court LOUPE sur
SA machine — le VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine
— le run VERT sur pièces + le recoup labo N/N sur pièces croisées →
la balise `loupe 0.1.0` SCELLÉE (fait de carte, D104) : LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut. Le labo recoupe sur pièces (D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague m9f archivée (le septième run a rendu son verdict : VERT
    sur pièces — la finale 1.0.0 SCELLÉE, le jalon M9 franchi ; archivée
    au passage à la vague loupe)

--- la vague courante (racine de /test) : loupe — LE KIT TERRAIN
    M10-(e), LE GRANDEUR NATURE (kit-loupe.zip + LISEZMOI-loupe.txt ;
    preuves-loupe/ reçoit le témoin et les captures de la vitrine ;
    signatures-I.txt + cle-publique-I.txt DEMEURENT : les pièces de
    l'ère du TGN, la remise INSTALLÉE de la cérémonie Passée sur
    pièces — la vague ne les touche jamais) — livrée le 09/11/2026 :
    la première application née de TRIADE (loupe.exe 0.1.0-dev.1,
    50 688 o, sha256 f07dd2cf…) part chez son utilisateur — la session,
    le panneau d'empreintes, les lignes, la recherche, l'édition à
    l'octet, la vitrine réelle ; la balise `loupe 0.1.0` attend le
    vert recoupé : LE JALON M10.
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
    print("=== M10-(e) : le coffre /test passe à LA VAGUE LOUPE "
          "(le grandeur nature) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_loupe.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-loupe.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-loupe.zip md5 divergent — réassembler")
    print(f"[0] le kit : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague m9f ---------------------------------------------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m9")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m9")
        print("[1] vagues-m9/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    for nom in VAGUE_M9F:
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
        print(f"[1] archivé : {nom} → vagues-m9/ "
              f"(md5 {piece.get('md5Checksum', '')[:8]}… recoupé après)")

    # -- 2. preuves-loupe/ né avec son LISEZMOI ------------------------------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        rid = ds.create_folder(TEST_ID, "preuves-loupe")
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[2] preuves-loupe/ NÉ avec son LISEZMOI-preuves.txt "
              "(les pièces attendues)")
    else:
        rid = receptacle["id"]
        if "LISEZMOI-preuves.txt" not in ds.list_folder(rid):
            televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[2] preuves-loupe/ déjà présent — idempotent")

    # -- 3. la vague loupe déposée à la racine -------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-loupe.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-loupe.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-loupe.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-loupe.zip md5 divergent après téléversement")
        print(f"[3] déposé : kit-loupe.zip (md5 {KIT_MD5[:8]}… MATCH par "
              f"relecture)")
    else:
        if racine["kit-loupe.zip"].get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-loupe.zip déjà présent avec un AUTRE md5")
        print("[3] kit-loupe.zip déjà déposé — idempotent")

    if "LISEZMOI-loupe.txt" not in ds.list_folder(TEST_ID):
        ds.upload_create(TEST_ID, "LISEZMOI-loupe.txt",
                         pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-loupe.txt")
        if not apres:
            refus("DÉPÔT", "LISEZMOI-loupe.txt absent après téléversement")
        local = md5_bytes(open(LISEZMOI_KIT, "rb").read())
        if apres.get("md5Checksum") != local:
            refus("DÉPÔT", "LISEZMOI-loupe.txt md5 divergent après "
                           "téléversement")
        print(f"[3] déposé : LISEZMOI-loupe.txt (md5 {local[:8]}… MATCH)")
    else:
        print("[3] LISEZMOI-loupe.txt déjà déposé — idempotent")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : loupe" not in ancien:
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
                  "(la section m9f archivée + la vague courante loupe)")
        else:
            print("[4] l'index porte déjà la vague loupe — idempotent")
    else:
        print("[4] LISEZMOI-archives-livraisons.txt introuvable — l'index "
              "n'est pas mis à jour (nommé, non fatal)")

    # -- 5. vérification finale ------------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    for piece, md5_attendu in PIECES_ERE.items():
        p = racine.get(piece)
        if not p or p.get("md5Checksum") != md5_attendu:
            refus("PIÈCES-DE-L'ÈRE", f"{piece} absent ou divergent au /test "
                  f"— les pièces de cérémonie DEMEURENT (md5 "
                  f"{md5_attendu[:8]}… attendu)")
    print(f"[5] LES PIÈCES DE L'ÈRE DEMEURENT : signatures-I.txt "
          f"(f33c803a… la remise INSTALLÉE) + cle-publique-I.txt "
          f"(188a7d42… l'ancre) — la vague ne les a pas touchées")
    print(f"[5] la racine : {len(racine)} entrées — la vague loupe "
          f"(kit-loupe.zip + LISEZMOI-loupe.txt) + les pièces de l'ère + "
          f"les réceptacles + les archives")
    print("=== LE COFFRE EST À LA VAGUE LOUPE : la première application née "
          "de TRIADE attend son utilisateur — LE GRANDEUR NATURE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
