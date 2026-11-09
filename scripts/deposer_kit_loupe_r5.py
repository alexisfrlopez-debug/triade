#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_loupe_r5.py — LE COFFRE /test PASSÉ À LA VAGUE LOUPE dev.5
(LA RETOUCHE DE L'ENTRÉE 207 — règle D143 : archivage par DÉPLACEMENT,
jamais un jet ; les vagues refusées aux pièces VERSIONNÉES).

LE QUATRIÈME RUN TERRAIN (l'Entrée 207) : LE TÉMOIN T1 A NOMMÉ [SESSION]
— « loupe-01 a rendu 0xfffffffa (-6 SYSTÈME), le fichier pourtant relu
à l'instant » — ET LA VITRINE A VÉCU SA PREMIÈRE FOIS (« la fenêtre
s'ouvre et se referme immédiatement » — LA MORT SANS TÉMOIN).
L'AUTOPSIE SUR LA PIÈCE A NOMMÉ LA CLASSE DES ARGUMENTS PILE : les
arguments 5+ de l'ABI msx64 vivaient AU HOME SPACE au lieu de
[rsp+0x20]+ (loupe-01 : la disposition lue à la pile non initialisée ;
loupe-05 : le contexte SHA SUR LE VRAI SLOT — le VRAI ReadFile lisait
H0[0] 0x6A09E667… COMME UN POINTEUR ; loupe-06 pareil) ET DEUX AXES
D'ALIGNEMENT NOMMÉS PAR L'AUDIT D'ABI DU BUILD (loupe-10 le
sous-programme .peindre appelait TextOutW pile ≡8 ; loupe-11 le cadre
0x38). LA RETOUCHE dev.5 : les TROIS notations à leurs vrais slots +
les DEUX réalignements + LE GARDE GUÉRI PAR LA CONVENTION (les shims
relisent LES MÊMES SLOTS QUE LE VRAI — V7 le prouve sur la
falsification demandée) + LE TÉMOIN VITRINE AU KIT (temoin-vitrine.bat
— la prochaine mort sera nommée).

  1. ARCHIVAGE DE LA VAGUE dev.4 → /test/archives-livraisons/
     vagues-m10/ EN PIÈCES VERSIONNÉES : kit-loupe.zip → kit-loupe-
     dev.4.zip (md5 7175e90a…) + LISEZMOI-loupe.txt → LISEZMOI-loupe-
     dev.4.txt (md5 8208c423… — déplacement PATCH, md5 constaté après
     — le quatrième refus du terrain est un FAIT, la pièce demeure) ;
  2. LA VAGUE dev.5 DÉPOSÉE à la racine de /test : kit-loupe.zip
     (md5 8e080e8c… MATCH par relecture) + LISEZMOI-loupe.txt (le
     document du kit dev.5 — loupe.exe 0.1.0-dev.5, sha256 6f830f9c…) ;
  3. preuves-loupe/LISEZMOI-preuves.txt MIS À JOUR (l'artefact attendu
     0.1.0-dev.5, sha256 6f830f9c… — la leçon de l'Entrée 207 nommée
     au réceptacle, LE TÉMOIN VITRINE attendu) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la vague
     dev.4 archivée après le quatrième refus terrain + la vague
     courante dev.5) ;
  5. VÉRIFICATION : la racine porte la vague courante dev.5 + LES
     PIÈCES DE L'ÈRE DU TGN DEMEURÉES (signatures-I.txt f33c803a… +
     cle-publique-I.txt 188a7d42… — la vague ne les touche JAMAIS).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_loupe_r5.py
Code de sortie : 0 = coffre passé à la vague dev.5 ; 2 = refus nommé."""

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

# la vague dev.5 (la retouche de l'Entrée 207)
KIT_SHA = "8484a137481c26f13d014efb1f73a86dd865a6814fdfea91ee512d19decb05c5"
KIT_MD5 = "8e080e8c43277701c05ce12631ba6565"

# la vague dev.4 (REFUSÉE par le terrain — le témoin a nommé [SESSION]
# au T1 : le run le plus loin jamais vécu, l'image cartographiée)
ANCIEN_KIT_MD5 = "7175e90a5f092fe1252e1f6c7f0c0925"
ANCIEN_LISEZMOI_MD5 = "8208c42372b83720cf04b2ac84ae9bbb"

# les pièces de cérémonie qui DEMEURENT à la racine (l'ère du TGN)
PIECES_ERE = {"signatures-I.txt": "f33c803aad80711995c6ea61ce30aa7b",
              "cle-publique-I.txt": "188a7d42df2d03f68bfb50fada3a84a1"}

LISEZMOI_PREUVES_R5 = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU RUN TERRAIN M10-(e)
========================================================================
(LE RUN DE LOUPE, LE GRANDEUR NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact 0.1.0-dev.5, sha256
6f830f9c738265df… — LA RETOUCHE DE L'ENTRÉE 207 : le témoin T1 a nommé
[SESSION] sur dev.4 [loupe-01 a rendu -6 SYSTÈME, le fichier pourtant
relu à l'instant] ET LA VITRINE A VÉCU SA PREMIÈRE FOIS [« la fenêtre
s'ouvre et se referme immédiatement » — la mort SANS témoin] ;
l'autopsie a nommé LA CLASSE DES ARGUMENTS PILE : les arguments 5+ de
l'ABI msx64 AU HOME SPACE au lieu de [rsp+0x20]+ — loupe-01 [la
disposition lue à la pile non initialisée], loupe-05 [le contexte SHA
sur le vrai slot : le VRAI ReadFile lisait H0[0] 0x6A09E667… COMME UN
POINTEUR], loupe-06 pareil — ET DEUX AXES D'ALIGNEMENT nommés par
L'AUDIT D'ABI DU BUILD [loupe-10 le sous-programme .peindre pile ≡8,
loupe-11 le cadre 0x38] ; dev.5 porte les TROIS notations à leurs
vrais slots + les DEUX réalignements + LE GARDE GUÉRI PAR LA
CONVENTION [les shims relisent LES MÊMES SLOTS QUE LE VRAI] + LE
TÉMOIN VITRINE AU KIT ; la cascade diagnostic de l'Entrée 205 demeure ;
la carte génération 13 — la balise `loupe 0.1.0` se scellera sur le
vert recoupé)

LES PIÈCES ATTENDUES (nées dans ./preuves-loupe/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-loupe.txt     le témoin complet — l'environnement (Windows,
                       Python 64 bits), l'empreinte ASSERTÉE de
                       l'artefact, LE .data ENTIER relu contre LE
                       MIROIR du CADRE_VIERGE, les adresses scellées
                       CONSTATÉES, l'IAT résolue par le
                       scénario-chargeur, chaque contrôle tranché (la
                       session, la double lecture, les lignes, la
                       recherche, l'édition à l'octet, les rejets
                       nommés, la clôture) ET LA SONDE DE L'ENTRÉE 205
                       (P0..P4) ;
  temoin-vitrine.txt   LE TÉMOIN VITRINE (NOUVEAU, l'Entrée 207 : la
                       vitrine a vécu sa première mort SANS témoin) —
                       né par temoin-vitrine.bat : LES DEUX codes de
                       sortie (sans fichier, puis avec la copie
                       temoin-fichier.bin : la session naît entière)
                       et le rapport WER s'il y eut crash — LA
                       PROCHAINE MORT DE LA VITRINE SERA NOMMÉE ;
  capture-*.png        LES CAPTURES DE LA VITRINE (optionnelles mais
                       bienvenues) : la fenêtre réelle après ouverture
                       d'un fichier de votre choix — l'entête, la
                       grille hexa, le miroir ASCII, LE PANNEAU
                       D'EMPREINTES (md5 + sha256) — la vie de
                       l'application chez vous, le cœur du grandeur
                       nature.

LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1 à dev.4 existe encore, NE LE RÉUTILISEZ PAS
(loupe-kit-5/ par exemple — un dossier neuf par run, l'artefact
refusé ne se réutilise jamais).

LE CRITÈRE (le plan M10, rangée (e)) : le développeur court LOUPE sur
SA machine — le VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine
— le run VERT sur pièces + le recoup labo N/N sur pièces croisées →
la balise `loupe 0.1.0` SCELLÉE (fait de carte, D104) : LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (dev.1/dev.2 : les refus du chargeur 0xc000007b ; dev.3 :
[CADRE-NÉ] au T0 ; dev.4 : [SESSION] -6 au T1, la classe des
arguments pile — chaque défaut a été nommé, chaque défaut a reçu sa
retouche). Le labo recoupe sur pièces (D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague loupe dev.4 archivée après LE QUATRIÈME REFUS TERRAIN
    (le run du 09/11 : LE PLUS LOIN JAMAIS VÊCU — [T0] l'image
    cartographiée, LE CADRE NÉ MIROIR [la retouche de l'Entrée 206
    TENUE au terrain], l'IAT 37 feuilles posées — PUIS [T1] ÉCHEC
    NOMMÉ [SESSION] : loupe-01 a rendu -6 SYSTÈME, le fichier
    pourtant relu à l'instant ; ET LA VITRINE A VÉCU SA PREMIÈRE
    FOIS : « la fenêtre s'ouvre et se referme immédiatement » — la
    mort SANS témoin ; kit-loupe.zip md5 7175e90a… +
    LISEZMOI-loupe.txt 8208c423… → vagues-m10/ EN PIÈCES VERSIONNÉES
    [kit-loupe-dev.4.zip + LISEZMOI-loupe-dev.4.txt] — le refus est
    un FAIT, la pièce demeure, D143 ; le témoin du refus :
    temoin-loupe.txt 1 209 o md5 7bb40bae… archivé à archives-preuves/
    preuves-run-loupe-dev4/ AVEC le verdict — l'échec nommé ET
    l'autopsie de la classe])

--- la vague courante (racine de /test) : loupe dev.5 — LA RETOUCHE
    DE L'ENTRÉE 207 (kit-loupe.zip md5 8e080e8c… + LISEZMOI-loupe.txt
    ; loupe.exe 0.1.0-dev.5, 127 488 o, sha256 6f830f9c… — LA CLASSE
    DES ARGUMENTS PILE guérie : loupe-01/05/06 aux vrais slots
    [rsp+0x20+], loupe-10/11 réalignés par L'AUDIT D'ABI DU BUILD ;
    LE GARDE GUÉRI PAR LA CONVENTION : les shims relisent LES MÊMES
    SLOTS QUE LE VRAI — le défaut de dev.4 ne passerait plus jamais
    le labo [V7 : la falsification demandée, attrapée] ; LE TÉMOIN
    VITRINE AU KIT : temoin-vitrine.bat — la prochaine mort de la
    vitrine sera NOMMÉE) — livrée le 09/11/2026 : la première
    application née de TRIADE repart chez son utilisateur ; la balise
    `loupe 0.1.0` attend le vert recoupé : LE JALON M10.
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
    print("=== M10-(e) r5 : le coffre /test passe à LA VAGUE LOUPE dev.5 "
          "(la retouche de l'Entrée 207) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_loupe.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-loupe.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-loupe.zip md5 divergent — réassembler")
    print(f"[0] le kit dev.5 : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague dev.4 (le quatrième refus est un FAIT) ------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m10")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m10")
        print("[1] vagues-m10/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    racine = ds.list_folder(TEST_ID)
    for nom, nouveau_nom, ancien_md5 in (
            ("kit-loupe.zip", "kit-loupe-dev.4.zip", ANCIEN_KIT_MD5),
            ("LISEZMOI-loupe.txt", "LISEZMOI-loupe-dev.4.txt",
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
                      "dev.5 — rien à archiver")
                continue
            if md5_avant != ancien_md5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.4 ni dev.5, refus")
        else:                                   # LISEZMOI-loupe.txt
            local_nouveau = md5_bytes(open(LISEZMOI_KIT, "rb").read())
            if md5_avant == local_nouveau:
                print("[1] LISEZMOI-loupe.txt à la racine est déjà la vague "
                      "dev.5 — rien à archiver")
                continue
            if md5_avant != ancien_md5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.4 ni dev.5, refus")
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

    # -- 2. la vague dev.5 déposée à la racine -------------------------------------
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

    # -- 3. le réceptacle : LISEZMOI-preuves.txt à l'artefact dev.5 ---------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        refus("RÉCEPTACLE", "preuves-loupe/ introuvable au /test")
    rid = receptacle["id"]
    attendu = md5_bytes(LISEZMOI_PREUVES_R5.replace("\n", "\r\n")
                        .encode("utf-8"))
    deja = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
    if deja and deja.get("md5Checksum") != attendu:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(LISEZMOI_PREUVES_R5)
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
              "(l'artefact attendu : 0.1.0-dev.5, 6f830f9c… + LE TÉMOIN "
              "VITRINE attendu)")
    elif deja:
        print("[3] LISEZMOI-preuves.txt déjà à jour — idempotent")
    else:
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES_R5)
        print("[3] LISEZMOI-preuves.txt né (l'artefact attendu : "
              "0.1.0-dev.5, 6f830f9c…)")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : loupe dev.5" not in ancien:
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
                  "(la vague dev.4 archivée après le quatrième refus + la "
                  "vague courante dev.5)")
        else:
            print("[4] l'index porte déjà la vague dev.5 — idempotent")
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
        refus("ÉTAT-FINAL", "kit-loupe.zip dev.5 absent de la racine")
    print(f"[5] LES PIÈCES DE L'ÈRE DEMEURENT : signatures-I.txt "
          f"(f33c803a… la remise INSTALLÉE) + cle-publique-I.txt "
          f"(188a7d42… l'ancre) — la vague ne les a pas touchées")
    print("=== LE COFFRE /test PASSE À LA VAGUE dev.5 — la retouche de "
          "l'Entrée 207 déposée : le run rejoué attend le développeur ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
