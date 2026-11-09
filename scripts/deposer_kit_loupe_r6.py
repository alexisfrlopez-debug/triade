#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_loupe_r6.py — LE COFFRE /test PASSÉ À LA VAGUE LOUPE dev.6
(LA RETOUCHE DE L'ENTRÉE 208, AU KIT SEUL — règle D143 : archivage par
DÉPLACEMENT, jamais un jet ; les vagues refusées aux pièces VERSIONNÉES).

LE CINQUIÈME RUN TERRAIN (l'Entrée 208) : LE TÉMOIN T1 A NOMMÉ [SESSION]
— « loupe-01 a rendu 0xfffffff9 (-7 VERROUILLÉ), le fichier pourtant
relu à l'instant » — ET LA PIÈCE EST ACQUITTÉE : l'appel était NÉ
PARFAIT (la classe de l'Entrée 207 TENUE AU TERRAIN — LA PREUVE PAR LE
NOM CHANGÉ : -6 SYSTÈME [l'appel mal né] DEVINT -7 VERROUILLÉ [l'appel
né, refusé pour une RAISON RÉELLE]), c'est LE KIT QUI FAUTAIT : le
scénario EST LE CHARGEUR — LoadLibraryEx TIENT loupe.exe comme section
vivante sans partage d'écriture, et le VRAI Windows refuse gle 32
d'ouvrir à l'écriture le fichier d'une image mappée : T1 OFFRAIT LA
PIÈCE ELLE-MÊME à l'écriture, impossible PAR CONSTRUCTION. loupe-01 a
traduit le refus AU NOM PRÈS (I4/E2) — LA VOIE NOMMÉE A VÉCU SON
PREMIER TERRAIN. LA VITRINE : rapportée une TROISIÈME fois SANS témoin
(temoin-vitrine.txt ABSENT du dépôt).

LA RETOUCHE DE L'ENTRÉE 208 — AU KIT SEUL, LA PIÈCE INCHANGÉE
(loupe.exe 0.1.0-dev.5, sha256 6f830f9c…, AUCUN arbre signé touché) :
  - L'OMBRE : la session T1 naît sur temoin-session.bin, LA COPIE
    byte-à-byte de la pièce (empreinte ASSERTÉE après la copie), née
    et morte au run — même loi que la sonde 205 et le témoin vitrine ;
  - LE FRÈRE chassé : la session double de T6 offrait elle aussi la
    pièce sous le chargeur (premier appel non vérifié — eût rendu -7
    et faussé le -5 attendu) — l'offrande est L'OMBRE ;
  - LA VITRINE SE VIT PAR SON TÉMOIN : temoin-vitrine.bat ASCII
    rejoué, le LISEZMOI le dit noir sur blanc, temoin-vitrine.txt
    REQUIS au réceptacle.

  1. ARCHIVAGE DE LA VAGUE dev.5 → /test/archives-livraisons/
     vagues-m10/ EN PIÈCES VERSIONNÉES : kit-loupe.zip → kit-loupe-
     dev.5.zip (md5 8e080e8c…) + LISEZMOI-loupe.txt → LISEZMOI-loupe-
     dev.5.txt (md5 71b84a54… — déplacement PATCH, md5 constaté après
     — le cinquième refus du terrain est un FAIT, la pièce demeure
     ACQUITTÉE) ;
  2. LA VAGUE dev.6 DÉPOSÉE à la racine de /test : kit-loupe.zip
     (md5 0a50bd7a… MATCH par relecture) + LISEZMOI-loupe.txt (le
     document du kit dev.6 — loupe.exe 0.1.0-dev.5 INCHANGÉ,
     sha256 6f830f9c…) ;
  3. preuves-loupe/LISEZMOI-preuves.txt MIS À JOUR (l'artefact
     attendu : 0.1.0-dev.5 ACQUITTÉ, L'OMBRE nommée, LE TÉMOIN
     VITRINE REQUIS — un run sans témoin vitrine ne recoupe pas) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la vague
     dev.5 archivée après le cinquième refus terrain — LA PIÈCE
     ACQUITTÉE — + la vague courante dev.6) ;
  5. VÉRIFICATION : la racine porte la vague courante dev.6 + LES
     PIÈCES DE L'ÈRE DU TGN DEMEURÉES (signatures-I.txt f33c803a… +
     cle-publique-I.txt 188a7d42… — la vague ne les touche JAMAIS).

Usage : python3 scripts/deposer_kit_loupe_r6.py
Code de sortie : 0 = coffre passé à la vague dev.6 ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-loupe.zip"
LISEZMOI_KIT = os.path.join(REPO, "loupe", "terrain", "LISEZMOI-KIT-LOUPE.md")

# la vague dev.6 (la retouche de l'Entrée 208 — AU KIT SEUL)
KIT_SHA = ("3fa58e8b7e3a55cc50f1817fb9d8ac6b"
           "91d1ff30671e65dc57bce5404a097a78")
KIT_MD5 = "0a50bd7abc10ee5846aca0e4f4502ac0"

# la vague dev.5 (LE TÉMOIN A NOMMÉ [SESSION] -7 AU T1 — ET LA PIÈCE
# EST ACQUITTÉE : le kit fautait, la retouche vit au kit seul)
ANCIEN_KIT_MD5 = "8e080e8c43277701c05ce12631ba6565"
ANCIEN_LISEZMOI_MD5 = "71b84a54d1760f29d66177325e1013ee"

# les pièces de cérémonie qui DEMEURENT à la racine (l'ère du TGN)
PIECES_ERE = {"signatures-I.txt": "f33c803aad80711995c6ea61ce30aa7b",
              "cle-publique-I.txt": "188a7d42df2d03f68bfb50fada3a84a1"}

LISEZMOI_PREUVES_R6 = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU RUN TERRAIN M10-(e)
========================================================================
(LE RUN DE LOUPE, LE GRANDEUR NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact 0.1.0-dev.5, sha256
6f830f9c738265df… — LA PIÈCE ACQUITTÉE au cinquième run [l'Entrée
208 : l'appel CreateFileW de loupe-01 était NÉ PARFAIT — la classe
de l'Entrée 207 TENUE AU TERRAIN, LA PREUVE PAR LE NOM CHANGÉ : -6
SYSTÈME devint -7 VERROUILLÉ ; c'était LE KIT QUI FAUTAIT : le
scénario EST LE CHARGEUR, l'image TIENT loupe.exe, et le VRAI
Windows refuse gle 32 l'écriture sur une section vivante — T1
offrait la pièce à l'écriture, impossible PAR CONSTRUCTION ;
loupe-01 a traduit le refus AU NOM PRÈS — LA VOIE NOMMÉE DE L'ÈRE A
VÉCU SON PREMIER TERRAIN] ; LA RETOUCHE DE L'ENTRÉE 208 EST AU KIT
SEUL : L'OMBRE — la session naît sur temoin-session.bin, la copie
byte-à-byte de la pièce, née et morte au run ; le frère de T6
chassé — la session double offre l'ombre, jamais la pièce sous le
chargeur ; LA VITRINE SE VIT PAR SON TÉMOIN ; la cascade diagnostic
de l'Entrée 205 demeure ; la carte génération 13 — la balise `loupe
0.1.0` se scellera sur le vert recoupé)

LES PIÈCES ATTENDUES (nées dans ./preuves-loupe/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-vitrine.txt   LE TÉMOIN VITRINE — REQUIS (l'Entrée 208 : la
                       vitrine a vécu TROIS fois SANS témoin — une
                       mort sans témoin NE RECOUPE PAS) — né par
                       temoin-vitrine.bat : LES DEUX codes de sortie
                       (la fenêtre vide sans fichier, puis avec la
                       copie temoin-fichier.bin : la session naît
                       entière) et le rapport WER s'il y eut crash —
                       LA MORT ÉVENTUELLE SERA NOMMÉE ;
  temoin-loupe.txt     le témoin complet — l'environnement (Windows,
                       Python 64 bits), l'empreinte ASSERTÉE de
                       l'artefact, LE .data ENTIER relu contre LE
                       MIROIR du CADRE_VIERGE, les adresses scellées
                       CONSTATÉES, l'IAT résolue par le
                       scénario-chargeur, chaque contrôle tranché (la
                       session sur L'OMBRE byte-à-byte de la pièce,
                       la double lecture, les lignes, la recherche,
                       l'édition à l'octet, les rejets nommés, la
                       clôture) ET LA SONDE DE L'ENTRÉE 205 (P0..P4) ;
  capture-*.png        LES CAPTURES DE LA VITRINE (optionnelles mais
                       bienvenues) : la fenêtre réelle après ouverture
                       d'un fichier de votre choix — l'entête, la
                       grille hexa, le miroir ASCII, LE PANNEAU
                       D'EMPREINTES (md5 + sha256) — la vie de
                       l'application chez vous, le cœur du grandeur
                       nature.

LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1 à dev.5 existe encore, NE LE RÉUTILISEZ PAS
(loupe-kit-6/ par exemple — un dossier neuf par run).

LE CRITÈRE (le plan M10, rangée (e)) : le développeur court LOUPE sur
SA machine — le VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine
— le run VERT sur pièces + le recoup labo N/N sur pièces croisées →
la balise `loupe 0.1.0` SCELLÉE (fait de carte, D104) : LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (dev.1/dev.2 : les refus du chargeur 0xc000007b ; dev.3 :
[CADRE-NÉ] au T0 ; dev.4 : [SESSION] -6 au T1, la classe des
arguments pile ; dev.5 : [SESSION] -7 au T1 — LA PIÈCE ACQUITTÉE,
LE KIT FAUTIF, l'ombre née — chaque défaut a été nommé, chaque
défaut a reçu sa retouche). Le labo recoupe sur pièces
(D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague loupe dev.5 archivée après LE CINQUIÈME REFUS TERRAIN
    (le run du 09/11 : [T0] TOUT VERT — l'empreinte dev.5 ASSERTÉE,
    LE CADRE NÉ MIROIR tenu DEUXIÈME fois, l'IAT 37 feuilles — PUIS
    [T1] ÉCHEC NOMMÉ [SESSION] : loupe-01 a rendu -7 VERROUILLÉ, le
    fichier pourtant relu à l'instant — ET LA PIÈCE EST ACQUITTÉE :
    l'appel était NÉ PARFAIT [la classe de l'Entrée 207 TENUE, LA
    PREUVE PAR LE NOM CHANGÉ : -6 SYSTÈME devint -7 VERROUILLÉ],
    c'est LE KIT QUI FAUTAIT [le scénario EST LE CHARGEUR : l'image
    TIENT loupe.exe, le VRAI Windows refuse gle 32 l'écriture sur
    une section vivante — T1 offrait la pièce à l'écriture,
    impossible PAR CONSTRUCTION] ; loupe-01 a traduit le refus AU
    NOM PRÈS — LA VOIE NOMMÉE A VÉCU SON PREMIER TERRAIN ; la
    vitrine rapportée une TROISIÈME fois SANS témoin ; kit-loupe.zip
    md5 8e080e8c… + LISEZMOI-loupe.txt 71b84a54… → vagues-m10/ EN
    PIÈCES VERSIONNÉES [kit-loupe-dev.5.zip + LISEZMOI-loupe-dev.5.
    txt] — le refus est un FAIT, LA PIÈCE DEMEURE ACQUITTÉE, D143 ;
    le témoin du refus : temoin-loupe.txt 1 209 o md5 0825dace…
    archivé à archives-preuves/preuves-run-loupe-dev5/ AVEC le
    verdict [la pièce acquittée, le kit fautif, l'autopsie])

--- la vague courante (racine de /test) : loupe dev.6 — LA RETOUCHE
    DE L'ENTRÉE 208, AU KIT SEUL (kit-loupe.zip md5 0a50bd7a… +
    LISEZMOI-loupe.txt ; loupe.exe 0.1.0-dev.5 INCHANGÉ, 127 488 o,
    sha256 6f830f9c… — LA PIÈCE ACQUITTÉE, AUCUN arbre signé touché ;
    L'OMBRE : la session T1 naît sur temoin-session.bin, la copie
    byte-à-byte de la pièce née et morte au run — même loi que la
    sonde 205 et le témoin vitrine ; LE FRÈRE DU DÉFAUT chassé : la
    session double de T6 offre l'ombre, jamais la pièce sous le
    chargeur ; LA VITRINE SE VIT PAR SON TÉMOIN : temoin-vitrine.bat
    ASCII rejoué, temoin-vitrine.txt REQUIS au réceptacle — une mort
    sans témoin ne recoupe pas) — livrée le 09/11/2026 : la première
    application née de TRIADE repart chez son utilisateur ; la
    balise `loupe 0.1.0` attend le vert recoupé : LE JALON M10.
"""


def refus(nom, detail):
    print(f"[dépôt] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def televerser_texte(parent_id, nom, contenu):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8", newline="\r\n") as f:
        f.write(contenu)
        chemin = f.name
    try:
        return ds.upload_create(parent_id, nom, pathlib.Path(chemin))
    finally:
        os.unlink(chemin)


def main():
    print("=== M10-(e) r6 : le coffre /test passe à LA VAGUE LOUPE dev.6 "
          "(la retouche de l'Entrée 208 — AU KIT SEUL) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_loupe.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-loupe.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-loupe.zip md5 divergent — réassembler")
    print(f"[0] le kit dev.6 : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague dev.5 (le cinquième refus est un FAIT) ------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m10")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m10")
        print("[1] vagues-m10/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    racine = ds.list_folder(TEST_ID)
    for nom, nouveau_nom, ancien_md5 in (
            ("kit-loupe.zip", "kit-loupe-dev.5.zip", ANCIEN_KIT_MD5),
            ("LISEZMOI-loupe.txt", "LISEZMOI-loupe-dev.5.txt",
             ANCIEN_LISEZMOI_MD5)):
        piece = racine.get(nom)
        if piece is None:
            deja = ds.list_folder(vagues_id).get(nouveau_nom)
            if deja:
                print(f"[1] {nouveau_nom} déjà archivé (md5 "
                      f"{deja.get('md5Checksum', '')[:8]}…) — idempotent")
            else:
                print(f"[1] {nom} absent de la racine — l'étape 2 le déposera")
            continue
        md5_avant = piece.get("md5Checksum")
        if nom == "kit-loupe.zip":
            if md5_avant == KIT_MD5:
                print("[1] kit-loupe.zip à la racine est déjà la vague "
                      "dev.6 — rien à archiver")
                continue
            if md5_avant != ancien_md5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.5 ni dev.6, refus")
        else:                                   # LISEZMOI-loupe.txt
            local_nouveau = md5_bytes(open(LISEZMOI_KIT, "rb").read())
            if md5_avant == local_nouveau:
                print("[1] LISEZMOI-loupe.txt à la racine est déjà la vague "
                      "dev.6 — rien à archiver")
                continue
            if md5_avant != ancien_md5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.5 ni dev.6, refus")
        # LE DÉPLACEMENT VERSIONNÉ (D143 : jamais un jet, jamais un nom
        # partagé — l'ambiguïté des vagues refusées est levée)
        url = (ds.API + f"/files/{piece['id']}"
               f"?addParents={vagues_id}&removeParents={TEST_ID}")
        st, rep, _ = ds.api("PATCH", url, body={"name": nouveau_nom})
        if st not in (200, 201):
            refus("ARCHIVAGE", f"{nom} : HTTP {st} : {rep[:150]!r}")
        archive = ds.list_folder(vagues_id).get(nouveau_nom)
        if not archive or archive.get("md5Checksum") != md5_avant:
            refus("ARCHIVAGE", f"{nouveau_nom} : md5 divergent après "
                               "déplacement")
        if nom in ds.list_folder(TEST_ID):
            refus("ARCHIVAGE", f"{nom} demeure à la racine après déplacement")
        print(f"[1] archivé VERSIONNÉ : {nom} → {nouveau_nom} "
              f"(md5 {md5_avant[:8]}… recoupé après)")

    # -- 2. la vague dev.6 déposée à la racine -------------------------------------
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
                  "MATCH)")
        else:
            print("[2] LISEZMOI-loupe.txt déjà à jour — idempotent")

    # -- 3. le réceptacle : LISEZMOI-preuves.txt à la vague dev.6 ---------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        refus("RÉCEPTACLE", "preuves-loupe/ introuvable au /test")
    rid = receptacle["id"]
    attendu = md5_bytes(LISEZMOI_PREUVES_R6.replace("\n", "\r\n")
                        .encode("utf-8"))
    deja = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
    if deja and deja.get("md5Checksum") != attendu:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(LISEZMOI_PREUVES_R6)
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
              "(l'artefact attendu : 0.1.0-dev.5 ACQUITTÉ + L'OMBRE + LE "
              "TÉMOIN VITRINE REQUIS)")
    elif deja:
        print("[3] LISEZMOI-preuves.txt déjà à jour — idempotent")
    else:
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES_R6)
        print("[3] LISEZMOI-preuves.txt né (l'artefact attendu : "
              "0.1.0-dev.5 ACQUITTÉ)")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : loupe dev.6" not in ancien:
            nouveau = ancien.rstrip("\n") + "\n" + NOTE_INDEX
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
                  "(la vague dev.5 archivée après le cinquième refus — LA "
                  "PIÈCE ACQUITTÉE — + la vague courante dev.6)")
        else:
            print("[4] l'index porte déjà la vague dev.6 — idempotent")
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
        refus("ÉTAT-FINAL", "kit-loupe.zip dev.6 absent de la racine")
    print(f"[5] LES PIÈCES DE L'ÈRE DEMEURENT : signatures-I.txt "
          f"(f33c803a… la remise INSTALLÉE) + cle-publique-I.txt "
          f"(188a7d42… l'ancre) — la vague ne les a pas touchées")
    print("=== LE COFFRE /test PASSE À LA VAGUE dev.6 — la retouche de "
          "l'Entrée 208 (AU KIT SEUL) déposée : le run rejoué attend le "
          "développeur ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
