#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_loupe_r4.py — LE COFFRE /test PASSÉ À LA VAGUE LOUPE dev.4
(LA RETOUCHE DE L'ENTRÉE 206 — règle D143 : archivage par DÉPLACEMENT,
jamais un jet ; les vagues refusées aux pièces VERSIONNÉES).

LE TROISIÈME REFUS TERRAIN (l'Entrée 206) : LE VRAI CHARGEUR A
CARTOGRAPHIÉ dev.3 — LA PREMIÈRE FOIS AU TERRAIN (l'enveloppe de
l'Entrée 205 PROUVÉE : plus de refus 0xc000007b, les adresses scellées
CONSTATÉES au témoin) — puis LE TÉMOIN A NOMMÉ AU T0 : ÉCHEC NOMMÉ
[CADRE-NÉ], « le CADRE .data n'est pas né poignée INVALIDE
(l'initialiseur du build) ». L'AUTOPSIE SUR PIÈCES : le sentinel
INVALIDE à +8 (UNE TAILLE CADRE_POIGNEE prise pour un offset) et ZÉRO à
+528 (la chaîne des tailles du plan : chemin 520 + taille_f 8 — le
harnais CADRE_VIERGE, le scénario et l'assembleur disaient TOUS +528).
LA RETOUCHE dev.4 : l'initialiseur .data devient LE MIROIR EXACT du
CADRE_VIERGE du harnais (l'offset CALCULÉ, jamais gravé de tête) ET le
validateur du build relit LE MÊME miroir (dev.3 validait à +8 : un
garde blessé par le défaut qu'il croyait garder ne garde rien) ; le
scénario relit désormais LE .data ENTIER contre le miroir — la porte
demeure pour toujours.

  1. ARCHIVAGE DE LA VAGUE dev.3 → /test/archives-livraisons/
     vagues-m10/ EN PIÈCES VERSIONNÉES : kit-loupe.zip → kit-loupe-
     dev.3.zip (md5 13dbe746…) + LISEZMOI-loupe.txt → LISEZMOI-loupe-
     dev.3.txt (déplacement PATCH, md5 constaté après — le troisième
     refus du terrain est un FAIT, la pièce demeure) ;
  2. LA VAGUE dev.4 DÉPOSÉE à la racine de /test : kit-loupe.zip
     (md5 7175e90a… MATCH par relecture) + LISEZMOI-loupe.txt (le
     document du kit dev.4 — loupe.exe 0.1.0-dev.4, sha256
     1f2da283…) ;
  3. preuves-loupe/LISEZMOI-preuves.txt MIS À JOUR (l'artefact attendu
     0.1.0-dev.4, sha256 1f2da283… — la leçon de l'Entrée 206 nommée
     au réceptacle) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la vague
     dev.3 archivée après le troisième refus terrain + la vague
     courante dev.4) ;
  5. VÉRIFICATION : la racine porte la vague courante dev.4 + LES
     PIÈCES DE L'ÈRE DU TGN DEMEURÉES (signatures-I.txt f33c803a… +
     cle-publique-I.txt 188a7d42… — la vague ne les touche JAMAIS).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_loupe_r4.py
Code de sortie : 0 = coffre passé à la vague dev.4 ; 2 = refus nommé."""

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

# la vague dev.4 (la retouche de l'Entrée 206)
KIT_SHA = "2fc805e235891b75ef27905d80e3aeefbe1d9fcd25545fd8e015178d500f7385"
KIT_MD5 = "7175e90a5f092fe1252e1f6c7f0c0925"

# la vague dev.3 (REFUSÉE par le terrain — le témoin a nommé [CADRE-NÉ]
# au T0, l'image cartographiée par le VRAI chargeur pour la première fois)
ANCIEN_KIT_MD5 = "13dbe746ae5bfb67957c8e6b22846329"
ANCIEN_LISEZMOI_MD5 = "98085071ec7bc874a7cdfdd984fba9b4"

# les pièces de cérémonie qui DEMEURENT à la racine (l'ère du TGN —
# la vague ne les touche JAMAIS : signatures-I.txt est la remise
# INSTALLÉE f33c803a…, cle-publique-I.txt l'ancre des ères 188a7d42…)
PIECES_ERE = {"signatures-I.txt": "f33c803aad80711995c6ea61ce30aa7b",
              "cle-publique-I.txt": "188a7d42df2d03f68bfb50fada3a84a1"}

LISEZMOI_PREUVES_R4 = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU RUN TERRAIN M10-(e)
========================================================================
(LE RUN DE LOUPE, LE GRANDEUR NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact 0.1.0-dev.4, sha256
1f2da2833b47265e… — LA RETOUCHE DE L'ENTRÉE 206 : LE VRAI CHARGEUR A
CARTOGRAPHIÉ dev.3 [la première fois au terrain — l'enveloppe
PROUVÉE, plus de refus 0xc000007b], puis LE TÉMOIN A NOMMÉ
[CADRE-NÉ] : le CADRE .data n'était pas né poignée INVALIDE,
l'initialiseur du build avait posé le sentinel à +8 au lieu de +528
[la chaîne des tailles du plan] ; dev.4 fait de l'initialiseur .data
LE MIROIR EXACT du CADRE_VIERGE du harnais — zéros partout SAUF la
poignée INVALIDE à +528 — ET le scénario relit désormais LE .data
ENTIER contre le miroir ; la cascade diagnostic de l'Entrée 205
demeure : le VRAI chargeur nomme l'axe au témoin ; la carte
génération 13 — la balise `loupe 0.1.0` se scellera sur le vert
recoupé)

LES PIÈCES ATTENDUES (nées dans ./preuves-loupe/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-loupe.txt   le témoin complet — l'environnement (Windows,
                     Python 64 bits), l'empreinte ASSERTÉE de
                     l'artefact, LE .data ENTIER relu contre LE
                     MIROIR du CADRE_VIERGE (la leçon de l'Entrée
                     206), les adresses scellées CONSTATÉES (la
                     minilibc M1, la boucle démo, la famille sha M9,
                     la table K FIPS, le qword version R10, LE
                     BASERELOC minimal déclaré dirs[5]), l'IAT
                     résolue par le scénario-chargeur, chaque contrôle
                     tranché (la session, la double lecture, les
                     lignes, la recherche, l'édition à l'octet, les
                     rejets nommés, la clôture) ET LA SONDE DE
                     L'ENTRÉE 205 (P0..P4 : chaque axe reconstitué
                     VERTE/REFUS + GetLastError + NTSTATUS — la leçon
                     consignée) ;
  capture-*.png      LES CAPTURES DE LA VITRINE (optionnelles mais
                     bienvenues) : la fenêtre réelle après ouverture
                     d'un fichier de votre choix — l'entête, la grille
                     hexa, le miroir ASCII, LE PANNEAU D'EMPREINTES
                     (md5 + sha256) — la vie de l'application chez
                     vous, le cœur du grandeur nature.

LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1, dev.2 ou dev.3 existe encore, NE LE
RÉUTILISEZ PAS (un dossier neuf par run, l'artefact refusé ne se
réutilise jamais).

LE CRITÈRE (le plan M10, rangée (e)) : le développeur court LOUPE sur
SA machine — le VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine
— le run VERT sur pièces + le recoup labo N/N sur pièces croisées →
la balise `loupe 0.1.0` SCELLÉE (fait de carte, D104) : LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (les refus de dev.1 et dev.2 étaient des refus du chargeur —
0xc000007b ; le refus de dev.3 était un échec nommé AU TÉMOIN :
[CADRE-NÉ], l'image cartographiée, le défaut dans la pièce — les
défauts ont été nommés, la retouche est née ; ET LE SCÉNARIO RELIT LE
.data ENTIER CONTRE LE MIROIR : un écart d'un octet serait nommé).
Le labo recoupe sur pièces (D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague loupe dev.3 archivée après LE TROISIÈME REFUS TERRAIN
    (le run du 09/11 : LE VRAI CHARGEUR A CARTOGRAPHIÉ L'IMAGE — la
    première fois au terrain, l'enveloppe de l'Entrée 205 PROUVÉE —
    puis LE TÉMOIN A NOMMÉ AU T0 : ÉCHEC NOMMÉ [CADRE-NÉ], le CADRE
    .data pas né poignée INVALIDE, l'initialiseur du build — le
    sentinel était à +8, une TAILLE prise pour un offset, au lieu de
    +528 la chaîne des tailles du plan ; kit-loupe.zip md5 13dbe746…
    + LISEZMOI-loupe.txt → vagues-m10/ EN PIÈCES VERSIONNÉES
    [kit-loupe-dev.3.zip + LISEZMOI-loupe-dev.3.txt] — le refus est
    un FAIT, la pièce demeure, D143 ; le témoin du refus :
    temoin-loupe.txt 522 o archivé à archives-preuves/preuves-run-
    loupe-dev3/ AVEC le verdict ROUGE — l'échec nommé])

--- la vague courante (racine de /test) : loupe dev.4 — LA RETOUCHE
    DE L'ENTRÉE 206 (kit-loupe.zip md5 7175e90a… + LISEZMOI-
    loupe.txt ; loupe.exe 0.1.0-dev.4, 127 488 o, sha256 1f2da283… —
    l'initialiseur .data devient LE MIROIR EXACT du CADRE_VIERGE du
    harnais : zéros partout SAUF la poignée INVALIDE à +528, l'offset
    CALCULÉ par la chaîne des tailles, jamais gravé de tête ; ET le
    validateur du build relit LE MÊME miroir — un garde blessé par le
    défaut qu'il croyait garder ne garde rien ; ET le scénario relit
    LE .data ENTIER contre le miroir) — livrée le 09/11/2026 : la
    première application née de TRIADE repart chez son utilisateur —
    l'enveloppe PROUVÉE par le run dev.3, l'initialiseur GUERI ; la
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
    print("=== M10-(e) r4 : le coffre /test passe à LA VAGUE LOUPE dev.4 "
          "(la retouche de l'Entrée 206) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_loupe.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-loupe.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-loupe.zip md5 divergent — réassembler")
    print(f"[0] le kit dev.4 : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (l'épreuve d'extraction est VERTE)")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague dev.3 (le troisième refus est un FAIT) ------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m10")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m10")
        print("[1] vagues-m10/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    racine = ds.list_folder(TEST_ID)
    for nom, nouveau_nom, ancien_md5 in (
            ("kit-loupe.zip", "kit-loupe-dev.3.zip", ANCIEN_KIT_MD5),
            ("LISEZMOI-loupe.txt", "LISEZMOI-loupe-dev.3.txt",
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
                # la racine porte DÉJÀ la vague dev.4 — rien à archiver
                print("[1] kit-loupe.zip à la racine est déjà la vague "
                      "dev.4 — rien à archiver")
                continue
            if md5_avant != ancien_md5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.3 ni dev.4, refus")
        else:                                   # LISEZMOI-loupe.txt
            local_nouveau = md5_bytes(open(LISEZMOI_KIT, "rb").read())
            if md5_avant == local_nouveau:
                print("[1] LISEZMOI-loupe.txt à la racine est déjà la vague "
                      "dev.4 — rien à archiver")
                continue
            if md5_avant != ancien_md5:
                refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                                   f"({md5_avant}) — ni dev.3 ni dev.4, refus")
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

    # -- 2. la vague dev.4 déposée à la racine -------------------------------------
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

    # -- 3. le réceptacle : LISEZMOI-preuves.txt à l'artefact dev.4 ---------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        refus("RÉCEPTACLE", "preuves-loupe/ introuvable au /test")
    rid = receptacle["id"]
    # le témoin : le texte tel que téléversé (les fins de ligne \r\n du
    # fichier Drive — jamais la chaîne brute du script)
    attendu = md5_bytes(LISEZMOI_PREUVES_R4.replace("\n", "\r\n")
                        .encode("utf-8"))
    deja = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
    if deja and deja.get("md5Checksum") != attendu:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(LISEZMOI_PREUVES_R4)
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
              "(l'artefact attendu : 0.1.0-dev.4, 1f2da283…)")
    elif deja:
        print("[3] LISEZMOI-preuves.txt déjà à jour — idempotent")
    else:
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES_R4)
        print("[3] LISEZMOI-preuves.txt né (l'artefact attendu : "
              "0.1.0-dev.4, 1f2da283…)")

    # -- 4. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : loupe dev.4" not in ancien:
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
                  "(la vague dev.3 archivée après le troisième refus + la "
                  "vague courante dev.4)")
        else:
            print("[4] l'index porte déjà la vague dev.4 — idempotent")
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
        refus("ÉTAT-FINAL", "kit-loupe.zip dev.4 absent de la racine")
    print(f"[5] LES PIÈCES DE L'ÈRE DEMEURENT : signatures-I.txt "
          f"(f33c803a… la remise INSTALLÉE) + cle-publique-I.txt "
          f"(188a7d42… l'ancre) — la vague ne les a pas touchées")
    print("=== LE COFFRE /test PASSE À LA VAGUE dev.4 — la retouche de "
          "l'Entrée 206 déposée : le run rejoué attend le développeur ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
