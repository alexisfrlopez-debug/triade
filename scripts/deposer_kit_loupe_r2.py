#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_loupe_r2.py — LE COFFRE /test PASSÉ À LA VAGUE LOUPE dev.2
(LA RETOUCHE BASERELOC de l'Entrée 204 — règle D143 : archivage par
DÉPLACEMENT, jamais un jet).

Le run terrain M10-(e) a REFUSÉ dev.1 sur la machine du développeur :
0xc000007b au geste de cartographie (LoadLibraryEx DONT_RESOLVE) —
l'image ASLR sans table de relocalisation, le VRAI chargeur Windows ne
peut pas la reloger (la base de prédilection 0x140000000 est occupée
par python.exe lui-même chez l'utilisateur). La retouche (loupe.exe
0.1.0-dev.2, sha256 a8a65ed4…) rend le BASERELOC minimal au plan — le
miroir M1..M9 (12 o, entrées ABSOLUTE).

  1. ARCHIVAGE DE LA VAGUE dev.1 → /test/archives-livraisons/vagues-m10/ :
     kit-loupe.zip (md5 ee43c991…) + LISEZMOI-loupe.txt (déplacement
     PATCH, md5 constaté après — le refus du terrain est un FAIT, la
     pièce demeure) ;
  2. LA VAGUE dev.2 DÉPOSÉE à la racine de /test : kit-loupe.zip (md5
     d50288d8… MATCH par relecture) + LISEZMOI-loupe.txt (le document
     du kit dev.2) ;
  3. preuves-loupe/LISEZMOI-preuves.txt MIS À JOUR (l'artefact attendu
     0.1.0-dev.2, sha256 a8a65ed4… — la leçon de l'Entrée 204 nommée) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la vague
     dev.1 archivée après refus terrain + la vague courante dev.2) ;
  5. VÉRIFICATION : la racine porte la vague courante dev.2 + LES PIÈCES
     DE L'ÈRE DU TGN DEMEURÉES (signatures-I.txt f33c803a… +
     cle-publique-I.txt 188a7d42… — la vague ne les touche JAMAIS).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_loupe_r2.py
Code de sortie : 0 = coffre passé à la vague dev.2 ; 2 = refus nommé."""

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

# la vague dev.2 (la retouche de l'Entrée 204)
KIT_SHA = "62b1a080faea8143d9382ca5bca740abe09b79a6a9b1ece7be55ecd6f449c7c1"
KIT_MD5 = "d50288d82147959cba679f9320810b61"

# la vague dev.1 (REFUSÉE par le terrain — 0xc000007b)
ANCIEN_KIT_MD5 = "ee43c991455720fb162e3aedb43c3a6d"

# les pièces de cérémonie qui DEMEURENT à la racine (l'ère du TGN —
# la vague ne les touche JAMAIS : signatures-I.txt est la remise
# INSTALLÉE f33c803a…, cle-publique-I.txt l'ancre des ères 188a7d42…)
PIECES_ERE = {"signatures-I.txt": "f33c803aad80711995c6ea61ce30aa7b",
              "cle-publique-I.txt": "188a7d42df2d03f68bfb50fada3a84a1"}

LISEZMOI_PREUVES_R2 = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU RUN TERRAIN M10-(e)
========================================================================
(LE RUN DE LOUPE, LE GRANDEUR NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact 0.1.0-dev.2, sha256
a8a65ed4cc3778c6… — LA RETOUCHE BASERELOC de l'Entrée 204 : le
terrain a REFUSÉ dev.1 [0xc000007b, l'image ASLR sans table de
relocalisation, le VRAI chargeur Windows ne peut pas la reloger] ;
la carte génération 13 — la balise `loupe 0.1.0` se scellera sur le
vert recoupé)

LES PIÈCES ATTENDUES (nées dans ./preuves-loupe/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-loupe.txt   le témoin complet — l'environnement (Windows,
                     Python 64 bits), l'empreinte ASSERTÉE de
                     l'artefact, les adresses scellées CONSTATÉES (la
                     minilibc M1, la boucle démo, la famille sha M9,
                     la table K FIPS, le qword version R10, LE
                     BASERELOC minimal déclaré dirs[5]), l'IAT résolue
                     par le scénario-chargeur, chaque contrôle tranché
                     (la session, la double lecture, les lignes, la
                     recherche, l'édition à l'octet, les rejets nommés,
                     la clôture) ;
  capture-*.png      LES CAPTURES DE LA VITRINE (optionnelles mais
                     bienvenues) : la fenêtre réelle après ouverture
                     d'un fichier de votre choix — l'entête, la grille
                     hexa, le miroir ASCII, LE PANNEAU D'EMPREINTES
                     (md5 + sha256) — la vie de l'application chez
                     vous, le cœur du grandeur nature.

LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1 existe encore, NE LE RÉUTILISEZ PAS (un dossier
neuf par run, l'artefact refusé ne se réutilise jamais).

LE CRITÈRE (le plan M10, rangée (e)) : le développeur court LOUPE sur
SA machine — le VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine
— le run VERT sur pièces + le recoup labo N/N sur pièces croisées →
la balise `loupe 0.1.0` SCELLÉE (fait de carte, D104) : LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (le refus de dev.1 était une ligne — le défaut a été nommé, la
retouche est née). Le labo recoupe sur pièces (D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague loupe dev.1 archivée après REFUS TERRAIN (le run M10-(e)
    du 09/11 : 0xc000007b au geste de cartographie — l'image ASLR sans
    table de relocalisation, l'oubli nommé du premier build, TOUS les
    artefacts M1..M9 portaient la table ; kit-loupe.zip md5 ee43c991…
    + LISEZMOI-loupe.txt → vagues-m10/ — le refus est un FAIT, la
    pièce demeure, D143 ; le témoin du refus : la capture du
    développeur [python.exe — Image incorrecte, état 0xc000007b])

--- la vague courante (racine de /test) : loupe dev.2 — LA RETOUCHE
    BASERELOC de l'Entrée 204 (kit-loupe.zip md5 d50288d8… + LISEZMOI-
    loupe.txt ; loupe.exe 0.1.0-dev.2, 50 688 o, sha256 a8a65ed4… —
    le BASERELOC minimal rendu au plan, 12 o d'entrées ABSOLUTE, le
    miroir M1..M9 : l'image PI que le chargeur PEUT reloger ;
    preuves-loupe/ reçoit le témoin et les captures ; signatures-I.txt
    + cle-publique-I.txt DEMEURENT : les pièces de l'ère du TGN) —
    livrée le 09/11/2026 : la première application née de TRIADE
    repart chez son utilisateur ; la balise `loupe 0.1.0` attend le
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
    print("=== M10-(e) r2 : le coffre /test passe à LA VAGUE LOUPE dev.2 "
          "(la retouche BASERELOC de l'Entrée 204) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_loupe.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-loupe.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-loupe.zip md5 divergent — réassembler")
    print(f"[0] le kit dev.2 : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague dev.1 (le refus du terrain est un FAIT) --------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m10")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m10")
        print("[1] vagues-m10/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    racine = ds.list_folder(TEST_ID)
    local_lisezmoi_md5 = md5_bytes(open(LISEZMOI_KIT, "rb").read())
    for nom in ("kit-loupe.zip", "LISEZMOI-loupe.txt"):
        piece = racine.get(nom)
        if piece is None:
            deja = ds.list_folder(vagues_id).get(nom)
            if deja:
                print(f"[1] {nom} déjà archivé (md5 "
                      f"{deja.get('md5Checksum', '')[:8]}…) — idempotent")
            else:
                print(f"[1] {nom} absent de la racine — l'étape 2 le déposera")
            continue
        md5_avant = piece.get("md5Checksum")
        if nom == "kit-loupe.zip":
            if md5_avant == KIT_MD5:
                # la racine porte DÉJÀ la vague dev.2 — rien à archiver
                print("[1] kit-loupe.zip à la racine est déjà la vague "
                      "dev.2 — rien à archiver")
                continue
            if md5_avant != ANCIEN_KIT_MD5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.1 ni dev.2, refus")
        else:                                   # LISEZMOI-loupe.txt
            if md5_avant == local_lisezmoi_md5:
                print("[1] LISEZMOI-loupe.txt à la racine est déjà la vague "
                      "dev.2 — rien à archiver")
                continue
        url = (ds.API + f"/files/{piece['id']}"
               f"?addParents={vagues_id}&removeParents={TEST_ID}")
        st, rep, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            refus("ARCHIVAGE", f"{nom} : HTTP {st} : {rep[:150]!r}")
        archive = ds.list_folder(vagues_id).get(nom)
        if not archive or archive.get("md5Checksum") != md5_avant:
            refus("ARCHIVAGE", f"{nom} : md5 divergent après déplacement")
        if nom in ds.list_folder(TEST_ID):
            refus("ARCHIVAGE", f"{nom} demeure à la racine après déplacement")
        print(f"[1] archivé : {nom} → vagues-m10/ "
              f"(md5 {md5_avant[:8]}… recoupé après)")

    # -- 2. la vague dev.2 déposée à la racine -------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-loupe.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-loupe.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-loupe.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-loupe.zip md5 divergent après téléversement")
        print(f"[2] déposé : kit-loupe.zip (md5 {KIT_MD5[:8]}… MATCH par "
              f"relecture)")
    else:
        if racine["kit-loupe.zip"].get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-loupe.zip déjà présent avec un AUTRE md5")
        print("[2] kit-loupe.zip déjà déposé — idempotent")

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
        print(f"[2] déposé : LISEZMOI-loupe.txt (md5 {local[:8]}… MATCH)")
    else:
        local = md5_bytes(open(LISEZMOI_KIT, "rb").read())
        actuel = ds.list_folder(TEST_ID)["LISEZMOI-loupe.txt"]
        if actuel.get("md5Checksum") != local:
            ds.upload_update(actuel["id"], pathlib.Path(LISEZMOI_KIT))
            apres = ds.list_folder(TEST_ID).get("LISEZMOI-loupe.txt")
            if apres.get("md5Checksum") != local:
                refus("DÉPÔT", "LISEZMOI-loupe.txt md5 divergent après mise "
                               "à jour")
            print(f"[2] mis à jour : LISEZMOI-loupe.txt (md5 {local[:8]}… "
                  f"MATCH)")
        else:
            print("[2] LISEZMOI-loupe.txt déjà à jour — idempotent")

    # -- 3. le réceptacle : LISEZMOI-preuves.txt à l'artefact dev.2 ---------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        refus("RÉCEPTACLE", "preuves-loupe/ introuvable au /test")
    rid = receptacle["id"]
    # le témoin : le texte tel que téléversé (les fins de ligne \r\n du
    # fichier Drive — jamais la chaîne brute du script)
    attendu = md5_bytes(LISEZMOI_PREUVES_R2.replace("\n", "\r\n")
                        .encode("utf-8"))
    deja = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
    if deja and deja.get("md5Checksum") != attendu:
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(LISEZMOI_PREUVES_R2)
            chemin = f.name
        try:
            ds.upload_update(deja["id"], pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        apres = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
        if apres.get("md5Checksum") != attendu:
            refus("RÉCEPTACLE", "LISEZMOI-preuves.txt md5 divergent après "
                                "mise à jour")
        print("[3] preuves-loupe/LISEZMOI-preuves.txt mis à jour "
              "(l'artefact attendu : 0.1.0-dev.2, a8a65ed4…)")
    elif deja:
        print("[3] LISEZMOI-preuves.txt déjà à jour — idempotent")
    else:
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES_R2)
        print("[3] LISEZMOI-preuves.txt né (l'artefact attendu : "
              "0.1.0-dev.2, a8a65ed4…)")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : loupe dev.2" not in ancien:
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
                  "(la vague dev.1 archivée après refus + la vague "
                  "courante dev.2)")
        else:
            print("[4] l'index porte déjà la vague dev.2 — idempotent")
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
    k = racine.get("kit-loupe.zip")
    if not k or k.get("md5Checksum") != KIT_MD5:
        refus("ÉTAT-FINAL", "kit-loupe.zip dev.2 absent de la racine")
    print(f"[5] LES PIÈCES DE L'ÈRE DEMEURENT : signatures-I.txt "
          f"(f33c803a… la remise INSTALLÉE) + cle-publique-I.txt "
          f"(188a7d42… l'ancre) — la vague ne les a pas touchées")
    print(f"[5] la racine : {len(racine)} entrées — la vague loupe dev.2 "
          f"(kit-loupe.zip + LISEZMOI-loupe.txt) + les pièces de l'ère + "
          f"les réceptacles + les archives")
    print("=== LE COFFRE EST À LA VAGUE LOUPE dev.2 : la retouche BASERELOC "
          "repart chez son utilisateur — LE GRANDEUR NATURE rejoué ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
