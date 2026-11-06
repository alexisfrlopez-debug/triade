#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_sondesys05.py — LE KIT SONDE SYS-05 (m9-(g)) DÉPOSÉ au coffre
/test (le chantier promis par le recoup du quatrième run : lire LE NTSTATUS
BRUT de l'émission — la limite NOMMÉE de l'instrument, par un trampoline de
capture ; l'artefact INTACT, JAMAIS reconstruit).

LA VAGUE M9F DEMEURE (le kit-m9f.zip ACQUITTÉ 90a1d022… reste à la racine :
la sonde est UNE LIVRAISON ADDITIONNELLE au diagnostic, PAS un remplacement
— la finale 1.0.0 attend toujours le run m9f) :

  1. kit-sonde-sys05.zip déposé à la racine (le kit éprouvé au labo —
     assembler_kit_sondesys05.py : recoup AST 29 constantes == l'artefact/
     le plan, LES PORTES passées [erratum n° 7 hérité + S1 le squelette du
     trampoline EXACT + S2 la table NTSTATUS canonique + S3 le compas
     avant la mesure + S4 le témoin vivant], extraction vierge VERT) ;
  2. LISEZMOI-sonde-sys05.txt déposé à la racine (le document du kit,
     lisible AU coffre sans extraire) ;
  3. preuves-sonde-sys05/ NÉ au coffre (le réceptacle des pièces de la
     sonde) avec son LISEZMOI-preuves.txt ;
  4. L'INDEX MIS À JOUR (LISEZMOI-archives-livraisons.txt : la note de la
     livraison de la sonde) ;
  5. VÉRIFICATION : la racine porte la vague m9f INTACTE + la sonde + les
     résidents + les réceptacles ; les empreintes recoupées.

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_sondesys05.py
Code de sortie : 0 = sonde livrée au coffre ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-sonde-sys05.zip"
LISEZMOI_KIT = os.path.join(REPO, "tls13", "terrain",
                            "LISEZMOI-KIT-SONDE-SYS05.md")

KIT_SHA = "cc917600015641c65833e3ee0ed55895465fa56fbe7fad5bb4df132171e67b31"
KIT_MD5 = "215c2caa54332ce91b03fd55c335513b"

KIT_M9F_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"   # la vague m9f INTACTE

LISEZMOI_PREUVES = """TRIADE — preuves-sonde-sys05 : LE RÉCEPTACLE DE LA
SONDE SYS-05 (m9-(g))
========================================================================
(la mission : LIRE LE NTSTATUS BRUT de l'émission — la limite NOMMÉE de
l'instrument des quatre runs m9f, franchie par un trampoline de capture ;
l'artefact INTACT, JAMAIS reconstruit)

LES PIÈCES ATTENDUES (nées dans ./preuves-sonde-sys05/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-sonde-sys05.txt    le témoin — l'environnement, les T0, LES
                            OCTETS DU TRAMPOLINE consignés (la preuve
                            lisible de ce qui est exécuté), et CHAQUE
                            lecture : code + NTSTATUS NOMMÉ + classe de
                            sévérité (le compas, la mesure, les
                            variations) ;
  sonde-sys05-journal.log   le journal horodaté de la sonde ;
  VERDICT-sonde-sys05.txt   le verdict (VERT-MESURE, PERCÉE, ou ROUGE
                            nommé) ;
  ligne-recue.txt           (SI la contre-épreuve S4 a tenu — la percée)
                            la ligne applicative DÉCHIFFRÉE PAR LA
                            MACHINE ;
  journal-emissions.txt     (idem) tout ce que la machine a émis.

LE GESTE : dézipper kit-sonde-sys05.zip dans un dossier NEUF, python
scenario-sonde-sys05.py (Python 64 bits, réseau vivant — la cible
www.cloudflare.com:443 ; Windows 11 OU Windows 10, le refus constaté est
inter-générations). La sonde mesure, nomme, et si le refus disparaît :
LA POIGNÉE SUIT DANS LE MÊME RUN.

Quel que soit le verdict : renvoyer preuves-sonde-sys05/ TEL QUEL ICI —
le labo recoupe sur pièces (D138/D145/D148), NOMME le coupable (le
contrat du bloc sys-05, l'état de l'endpoint, ou le réseau) et répare
selon la charte : l'erratum de la notation + la révision 2 de la spec
sys-05 le cas échéant — jamais une dérive silencieuse.
"""

NOTE_INDEX = """
--- la livraison additionnelle (racine de /test) : la SONDE SYS-05
    (m9-(g)), le chantier promis par le recoup du quatrième run —
    déposée le 07/11/2026 (kit-sonde-sys05.zip + LISEZMOI-sonde-sys05.txt ;
    preuves-sonde-sys05/ reçoit les pièces de la sonde). LA VAGUE M9F
    DEMEURE : kit-m9f.zip (90a1d022…) reste à la racine — la finale 1.0.0
    attend toujours LE RUN m9f ; la sonde est l'INSTRUMENT DU DIAGNOSTIC :
    lire LE NTSTATUS BRUT que sys-05 consigne dans rdx (la limite NOMMÉE
    de l'instrument, sys-05 Q5) par UN TRAMPOLINE DE CAPTURE de 33 o posé
    au run (l'artefact 1.0.0-dev.2 INTACT — d8928934…, relu au T0 ;
    JAMAIS reconstruit), le compas étalonné AVANT la mesure (un handle
    invalide → -6 + STATUS_INVALID_HANDLE), la table NTSTATUS recoupée
    aux sources canoniques ntstatus.h (Wine ET ReactOS), les variations
    (taille, délai) et la contre-épreuve S4 (la poignée par LE RAPPEL
    STANDARD, sur une session NEUVE — si le refus disparaît : LA PERCÉE,
    le jalon en vue). Après le geste du développeur : le labo recoupe,
    nomme le coupable et répare selon la charte.
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
    print("=== LA SONDE SYS-05 (m9-(g)) LIVRÉE au coffre /test (la vague "
          "m9f demeure — la sonde est l'instrument du diagnostic) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_sondesys05.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-sonde-sys05.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-sonde-sys05.zip md5 divergent — réassembler")
    print(f"[0] le kit sonde : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (LES PORTES passées, l'extraction "
          f"vierge VERTE)")

    # -- 1. la vague m9f INTACTE, constatée AVANT le geste -----------------------
    racine = ds.list_folder(TEST_ID)
    kit_m9f = racine.get("kit-m9f.zip") or {}
    if kit_m9f.get("md5Checksum") != KIT_M9F_MD5:
        refus("ÉTAT", f"kit-m9f.zip au /test ne porte pas le md5 ACQUITTÉ "
                      f"({kit_m9f.get('md5Checksum', 'ABSENT')[:8]}… != "
                      f"{KIT_M9F_MD5[:8]}…) — la vague m9f doit demeurer "
                      "INTACTE")
    print(f"[1] la vague m9f demeure : kit-m9f.zip == le kit ACQUITTÉ "
          f"md5 {KIT_M9F_MD5[:8]}… (recoupé AVANT le geste)")

    # -- 2. kit-sonde-sys05.zip déposé à la racine ---------------------------------
    if "kit-sonde-sys05.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-sonde-sys05.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-sonde-sys05.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-sonde-sys05.zip md5 divergent après "
                           "téléversement")
        print(f"[2] déposé : kit-sonde-sys05.zip (md5 {KIT_MD5[:8]}… MATCH "
              f"par relecture)")
    else:
        present = ds.list_folder(TEST_ID)["kit-sonde-sys05.zip"]
        if present.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-sonde-sys05.zip déjà présent avec un AUTRE "
                           "md5")
        print("[2] kit-sonde-sys05.zip déjà déposé — idempotent")

    # -- 3. LISEZMOI-sonde-sys05.txt déposé à la racine ----------------------------
    if "LISEZMOI-sonde-sys05.txt" not in ds.list_folder(TEST_ID):
        ds.upload_create(TEST_ID, "LISEZMOI-sonde-sys05.txt",
                         pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-sonde-sys05.txt")
        if not apres:
            refus("DÉPÔT", "LISEZMOI-sonde-sys05.txt absent après "
                           "téléversement")
        local = md5_bytes(open(LISEZMOI_KIT, "rb").read())
        if apres.get("md5Checksum") != local:
            refus("DÉPÔT", "LISEZMOI-sonde-sys05.txt md5 divergent après "
                           "téléversement")
        print(f"[3] déposé : LISEZMOI-sonde-sys05.txt (md5 {local[:8]}… "
              f"MATCH)")
    else:
        print("[3] LISEZMOI-sonde-sys05.txt déjà déposé — idempotent")

    # -- 4. preuves-sonde-sys05/ né avec son LISEZMOI -------------------------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-sonde-sys05")
    if not receptacle:
        rid = ds.create_folder(TEST_ID, "preuves-sonde-sys05")
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[4] preuves-sonde-sys05/ NÉ avec son LISEZMOI-preuves.txt "
              "(les pièces attendues)")
    else:
        rid = receptacle["id"]
        if "LISEZMOI-preuves.txt" not in ds.list_folder(rid):
            televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[4] preuves-sonde-sys05/ déjà présent — idempotent")

    # -- 5. l'index mis à jour -------------------------------------------------------
    arch_l = ds.list_folder(TEST_ID).get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")
    index = ds.list_folder(arch_l["id"]).get(
        "LISEZMOI-archives-livraisons.txt")
    if index:
        _, corps, _ = ds.api("GET", ds.API + "/files/" + index["id"]
                             + "?alt=media")
        ancien = corps.decode("utf-8")
        if "la livraison additionnelle (racine de /test) : la SONDE SYS-05" \
                not in ancien:
            nouveau = ancien.rstrip("\n") + "\n" + NOTE_INDEX
            import tempfile
            with tempfile.NamedTemporaryFile("w", suffix=".txt",
                                             delete=False,
                                             encoding="utf-8",
                                             newline="\r\n") as f:
                f.write(nouveau)
                chemin = f.name
            try:
                ds.upload_update(index["id"], pathlib.Path(chemin))
            finally:
                os.unlink(chemin)
            print("[5] LISEZMOI-archives-livraisons.txt mis à jour (la "
                  "note de la livraison de la sonde)")
        else:
            print("[5] l'index porte déjà la sonde — idempotent")

    # -- 6. la vérification finale -----------------------------------------------------
    final = ds.list_folder(TEST_ID)
    attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                "kit-sonde-sys05.zip", "LISEZMOI-sonde-sys05.txt",
                "preuves-sonde-sys05",
                "archives-livraisons", "archives-preuves",
                "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                "corriger-wsb.bat", "corriger-wsb.ps1",
                "signatures-I.txt", "cle-publique-I.txt"}
    manquants = attendus - set(final)
    if manquants:
        refus("VÉRIFICATION", f"entrées attendues absentes de la racine : "
                              f"{sorted(manquants)}")
    if final["kit-m9f.zip"].get("md5Checksum") != KIT_M9F_MD5:
        refus("VÉRIFICATION", "kit-m9f.zip a divergé pendant le geste")
    print(f"[6] la racine porte la vague m9f INTACTE + LA SONDE + les "
          f"résidents + les réceptacles ({len(final)} entrées)")
    print("\n=== LA SONDE SYS-05 EST LIVRÉE : le geste du développeur — "
          "python scenario-sonde-sys05.py (machine Windows 11 OU 10, "
          "réseau vivant), puis preuves-sonde-sys05/ ENTIER au coffre ; le "
          "labo recoupe, NOMME le coupable (le contrat du bloc, l'état de "
          "l'endpoint, ou le réseau) et répare selon la charte ===")


if __name__ == "__main__":
    main()
