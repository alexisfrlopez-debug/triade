#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_sondesys06.py — LE KIT SONDE SYS-06 (m9-(g)) DÉPOSÉ au coffre
/test (la sonde NOMMÉE D'AVANCE par le recoup-5 et la passation 107, OUVERTE
par le recoup du sixième run : LE JUMEAU CONSTATÉ PAR CODE, le -7 reproduit
identique, LE PASSAGER ÉLIMINÉ SUR PIÈCES — lire LE CODE EXACT de la
première lecture réelle : n / -7 le zéro de la demi-fin / -6 + LE NTSTATUS
BRUT de rdx, sys-06 Q5 ; l'artefact INTACT, JAMAIS reconstruit).

LA VAGUE M9F DEMEURE (le kit-m9f.zip ACQUITTÉ RÉPARÉ 79d44284… reste à
la racine : la sonde est UNE LIVRAISON ADDITIONNELLE au diagnostic, PAS
un remplacement — la finale 1.0.0 attend toujours le run m9f) :

  1. kit-sonde-sys06.zip déposé à la racine (le kit éprouvé au labo —
     assembler_kit_sondesys06.py : recoup AST 31 constantes == l'artefact/
     le plan [dont LA POSE DU WSABUF relue DANS L'IMAGE aux DEUX blocs],
     LES PORTES passées [erratum n° 7 hérité + S1 le squelette du
     trampoline EXACT vers sys-06 + S2 la table NTSTATUS canonique + S3
     le compas avant la mesure + S4 le témoin vivant + S5 LE GESTE
     DÉCOMPOSÉ : l'offre sys-05 direct AVANT la lecture], extraction
     vierge VERT) ;
  2. LISEZMOI-sonde-sys06.txt déposé à la racine (le document du kit,
     lisible AU coffre sans extraire) ;
  3. preuves-sonde-sys06/ NÉ au coffre (le réceptacle des pièces de la
     sonde) avec son LISEZMOI-preuves.txt ;
  4. L'INDEX MIS À JOUR (LISEZMOI-archives-livraisons.txt : la note de la
     livraison de la sonde sys-06) ;
  5. VÉRIFICATION : la racine porte la vague m9f INTACTE + la sonde
     sys-05 + LA SONDE SYS-06 + les résidents + les réceptacles ; les
     empreintes recoupées.

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_sondesys06.py
Code de sortie : 0 = sonde livrée au coffre ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-sonde-sys06.zip"
LISEZMOI_KIT = os.path.join(REPO, "tls13", "terrain",
                            "LISEZMOI-KIT-SONDE-SYS06.md")

KIT_SHA = "bf67cb84baea6ee3cb070b10d3eb0b73229b01beaf65b00c191f84fa68b47b84"
KIT_MD5 = "67e2014d5a5725d19bcabce548d2475e"

KIT_M9F_MD5 = "79d44284c70261375a2b055070fda223"   # la vague m9f INTACTE (RÉPARÉ)
KIT_SONDE05_MD5 = "215c2caa54332ce91b03fd55c335513b"   # la sonde sys-05 demeurée

LISEZMOI_PREUVES = """TRIADE — preuves-sonde-sys06 : LE RÉCEPTACLE DE LA
SONDE SYS-06 (m9-(g))
========================================================================
(la mission : LIRE LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE — la
sonde NOMMÉE D'AVANCE par le recoup du cinquième run, OUVERTE par le
recoup du sixième : le -7 reproduit identique, le passager éliminé sur
pièces ; l'artefact INTACT, JAMAIS reconstruit)

LES PIÈCES ATTENDUES (nées dans ./preuves-sonde-sys06/ du kit dézippé, à
glisser ICI EN ENTIER après le run) :

  temoin-sonde-sys06.txt    le témoin — l'environnement, les T0 (dont
                            LES DEUX contrôles erratum-9 : la pose du
                            WSABUF canonique relue DANS L'IMAGE aux
                            DEUX blocs), LES OCTETS DU TRAMPOLINE
                            consignés (la preuve lisible de ce qui est
                            exécuté), l'offre (sys-05 direct) et CHAQUE
                            lecture : code + NTSTATUS NOMMÉ + classe de
                            sévérité (le compas, la mesure, les
                            variations) ;
  sonde-sys06-journal.log   le journal horodaté de la sonde ;
  VERDICT-sonde-sys06.txt   le verdict (VERT-MESURE, PERCÉE, ou ROUGE
                            nommé) ;
  ligne-recue.txt           (SI la contre-épreuve S4 a tenu — la percée)
                            la ligne applicative DÉCHIFFRÉE PAR LA
                            MACHINE ;
  journal-emissions.txt     (idem) tout ce que la machine a émis.

LE GESTE : dézipper kit-sonde-sys06.zip dans un dossier NEUF, python
scenario-sonde-sys06.py (Python 64 bits, réseau vivant — la cible
www.cloudflare.com:443 ; Windows 11 OU Windows 10). La sonde mesure,
nomme, et si la lecture rend des octets : LA POIGNÉE SUIT DANS LE MÊME
RUN.

Quel que soit le verdict : renvoyer preuves-sonde-sys06/ TEL QUEL ICI —
le labo recoupe sur pièces (D138/D145/D148), NOMME le coupable (le
contrat du bloc sys-06, ou la demi-fin du pair) et répare selon la
charte : l'erratum de la notation + la révision de la spec sys-06 le
cas échéant — jamais une dérive silencieuse.
"""

NOTE_INDEX = """
--- la livraison additionnelle (racine de /test) : LA SONDE SYS-06
    (m9-(g)), la sonde NOMMÉE D'AVANCE par le recoup du cinquième run
    et la passation 107 — déposée le 07/11/2026 au geste du SIXIÈME run
    reçu et recoupé (kit-sonde-sys06.zip + LISEZMOI-sonde-sys06.txt ;
    preuves-sonde-sys06/ reçoit les pièces de la sonde). LE PRÉTEXTE :
    LE JUMEAU CONSTATÉ PAR CODE — le journal du run 6 == le journal du
    run 5 LIGNE À LIGNE (horodatements exceptés), l'émission VERT deux
    fois, la réception immédiate -7 deux fois, le run en SA seconde deux
    fois, le bord DNS changé (104.16.124.96 → 104.16.123.96) : LE
    PASSAGER ÉLIMINÉ SUR PIÈCES ; restent le contrat de réception sys-06
    et LA DEMI-FIN. LA VAGUE M9F DEMEURE : kit-m9f.zip (79d44284… le
    RÉPARÉ) reste à la racine — la finale 1.0.0 attend toujours LE RUN
    m9f ; la sonde est l'INSTRUMENT DU DIAGNOSTIC : lire LE CODE EXACT
    de LA PREMIÈRE LECTURE RÉELLE (n ≥ 1 le ServerHello arrivé, -7 LE
    ZÉRO de la demi-fin — sys-06 Q2, ou -6 + LE NTSTATUS BRUT que sys-06
    consigne dans rdx — Q5, la limite NOMMÉE de l'instrument) PAR UN
    TRAMPOLINE DE CAPTURE de 33 o posé au run (l'artefact 1.0.0-dev.3
    RÉPARÉ INTACT — de23e577…, relu au T0 avec LES DEUX contrôles
    erratum-9 ; JAMAIS reconstruit), LE GESTE M9F DÉCOMPOSÉ (l'offre du
    CH de référence par sys-05 DIRECT — le chemin réparé vert aux runs
    5/6 — PUIS la première lecture par le trampoline), le compas
    étalonné AVANT la mesure (un handle invalide → -6 +
    STATUS_INVALID_HANDLE), la table NTSTATUS recoupée aux sources
    canoniques ntstatus.h (Wine ET ReactOS), les variations (taille,
    délai) et la contre-épreuve S4 (la poignée par LE RAPPEL STANDARD,
    sur une session NEUVE — si la lecture rend des octets : LA PERCÉE,
    la finale 1.0.0 en vue, LE JALON M9 — LA GRANDE ŒUVRE). Après le
    geste du développeur : le labo recoupe, nomme le coupable et
    répare selon la charte.
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
    print("=== LA SONDE SYS-06 (m9-(g)) LIVRÉE au coffre /test (la vague "
          "m9f demeure — la sonde est l'instrument du diagnostic, le "
          "miroir de l'Entrée 185) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler_kit_sondesys06.py d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-sonde-sys06.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-sonde-sys06.zip md5 divergent — réassembler")
    print(f"[0] le kit sonde : {len(octets)} o, md5 {KIT_MD5[:8]}…, "
          f"sha256 {KIT_SHA[:16]}… (LES PORTES passées — dont LA PORTE S5 : "
          f"le geste m9f décomposé, l'offre AVANT la lecture — "
          f"l'extraction vierge VERTE)")

    # -- 1. la vague m9f INTACTE, constatée AVANT le geste -----------------------
    racine = ds.list_folder(TEST_ID)
    kit_m9f = racine.get("kit-m9f.zip") or {}
    if kit_m9f.get("md5Checksum") != KIT_M9F_MD5:
        refus("ÉTAT", f"kit-m9f.zip au /test ne porte pas le md5 RÉPARÉ "
                      f"({kit_m9f.get('md5Checksum', 'ABSENT')[:8]}… != "
                      f"{KIT_M9F_MD5[:8]}…) — la vague m9f doit demeurer "
                      "INTACTE")
    kit_sonde05 = racine.get("kit-sonde-sys05.zip") or {}
    if kit_sonde05.get("md5Checksum") != KIT_SONDE05_MD5:
        refus("ÉTAT", "kit-sonde-sys05.zip au /test a divergé (l'acquis de "
                      f"l'Entrée 185 : {kit_sonde05.get('md5Checksum', 'ABSENT')[:8]}… "
                      f"!= {KIT_SONDE05_MD5[:8]}…)")
    print(f"[1] la vague m9f demeure : kit-m9f.zip == le kit RÉPARÉ md5 "
          f"{KIT_M9F_MD5[:8]}… + la sonde sys-05 == l'acquis "
          f"{KIT_SONDE05_MD5[:8]}… (recoupés AVANT le geste)")

    # -- 2. kit-sonde-sys06.zip déposé à la racine ---------------------------------
    if "kit-sonde-sys06.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-sonde-sys06.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-sonde-sys06.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-sonde-sys06.zip md5 divergent après "
                           "téléversement")
        print(f"[2] déposé : kit-sonde-sys06.zip (md5 {KIT_MD5[:8]}… MATCH "
              f"par relecture)")
    else:
        present = ds.list_folder(TEST_ID)["kit-sonde-sys06.zip"]
        if present.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-sonde-sys06.zip déjà présent avec un AUTRE "
                           "md5")
        print("[2] kit-sonde-sys06.zip déjà déposé — idempotent")

    # -- 3. LISEZMOI-sonde-sys06.txt déposé à la racine ----------------------------
    if "LISEZMOI-sonde-sys06.txt" not in ds.list_folder(TEST_ID):
        ds.upload_create(TEST_ID, "LISEZMOI-sonde-sys06.txt",
                         pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-sonde-sys06.txt")
        if not apres:
            refus("DÉPÔT", "LISEZMOI-sonde-sys06.txt absent après "
                           "téléversement")
        local = md5_bytes(open(LISEZMOI_KIT, "rb").read())
        if apres.get("md5Checksum") != local:
            refus("DÉPÔT", "LISEZMOI-sonde-sys06.txt md5 divergent après "
                           "téléversement")
        print(f"[3] déposé : LISEZMOI-sonde-sys06.txt (md5 {local[:8]}… "
              f"MATCH)")
    else:
        print("[3] LISEZMOI-sonde-sys06.txt déjà déposé — idempotent")

    # -- 4. preuves-sonde-sys06/ né avec son LISEZMOI -------------------------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-sonde-sys06")
    if not receptacle:
        rid = ds.create_folder(TEST_ID, "preuves-sonde-sys06")
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[4] preuves-sonde-sys06/ NÉ avec son LISEZMOI-preuves.txt "
              "(les pièces attendues)")
    else:
        rid = receptacle["id"]
        if "LISEZMOI-preuves.txt" not in ds.list_folder(rid):
            televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES)
        print("[4] preuves-sonde-sys06/ déjà présent — idempotent")

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
        if "la livraison additionnelle (racine de /test) : LA SONDE SYS-06" \
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
                  "note de la livraison de la sonde sys-06)")
        else:
            print("[5] l'index porte déjà la sonde sys-06 — idempotent")

    # -- 6. la vérification finale -----------------------------------------------------
    final = ds.list_folder(TEST_ID)
    attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                "kit-sonde-sys05.zip", "LISEZMOI-sonde-sys05.txt",
                "preuves-sonde-sys05",
                "kit-sonde-sys06.zip", "LISEZMOI-sonde-sys06.txt",
                "preuves-sonde-sys06",
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
    if final["kit-sonde-sys05.zip"].get("md5Checksum") != KIT_SONDE05_MD5:
        refus("VÉRIFICATION", "kit-sonde-sys05.zip a divergé pendant le geste")
    if final["kit-sonde-sys06.zip"].get("md5Checksum") != KIT_MD5:
        refus("VÉRIFICATION", "kit-sonde-sys06.zip a divergé pendant le geste")
    print(f"[6] la racine porte la vague m9f INTACTE + la sonde sys-05 + "
          f"LA SONDE SYS-06 + les résidents + les réceptacles "
          f"({len(final)} entrées)")
    print("\n=== LA SONDE SYS-06 EST LIVRÉE : le geste au développeur — "
          "python scenario-sonde-sys06.py (machine Windows 11 OU 10, "
          "réseau vivant), puis preuves-sonde-sys06/ ENTIER au coffre ; le "
          "labo recoupe, NOMME le coupable (le contrat du bloc sys-06, ou "
          "la demi-fin du pair) et répare selon la charte ; SI LA LECTURE "
          "REND DES OCTETS : LA PERCÉE — la finale 1.0.0 en vue, LE JALON "
          "M9 — LA GRANDE ŒUVRE ===")


if __name__ == "__main__":
    main()
