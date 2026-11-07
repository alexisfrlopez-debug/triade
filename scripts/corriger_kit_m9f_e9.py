#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corriger_kit_m9f_e9.py — LE KIT TERRAIN M9-(f) RÉPARÉ au coffre /test :
LA RÉVISION 2 ÉTENDUE (l'erratum n° 8/n° 9 — le WSABUF canonique).

Les troisième et quatrième runs (le 07/11) sont morts À L'ÉMISSION du
ClientHello (-6 NOMMÉ, chaîne -6 → -7, déterministe sur DEUX générations
de Windows) ; la SONDE SYS-05 a MESURÉ le NTSTATUS brut :
0xC0000005 STATUS_ACCESS_VIOLATION, trois fois — LE COUPABLE NOMMÉ À
L'INSTRUCTION PRÈS : LA POSE DU WSABUF « packé » (buf à +4 là où le
canonique x64 fait SEIZE octets, buf à +8 — le noyau lit l'adresse
folle). La réception sys-06 portait LE MÊME défaut (l'erratum n° 9, la
symétrie send/recv du C_ASSERT AFD).

LA RÉPARATION SELON LA CHARTE (jamais une dérive silencieuse) : la
RÉVISION 2 des DEUX specs (sys-05 + sys-06 — le WSABUF canonique 16 o
NOMMÉ, la structure totale 40 o), les DEUX notations corrigées (mov
qword ptr [rsp+0x68], rdi — le MÊME encode 5 o, le slot intact), le
harnais RÉVISÉ (131 contrôles · 131 VERTS × 3 graines), l'erratum n° 8
réparé à la source ; PUIS LA CÉRÉMONIE : l'arbre m8 évolué — le garde
REFUSAIT le build (LE SIGNAL) — la remise étendue (m8 sys.1
c444d730…) RE-SIGNÉE par la clé hors-ligne du développeur (l'ancre des
ères 173fae9c… tenue, les DOUZE arbres inchangés byte-identiques —
Ed25519 déterministe, le recoup D163 rejoint une QUATRIÈME fois), la
garde 13/13 VERTS ; LE REBUILD 1.0.0-dev.3 (sha256 de23e577…) : le
diff contrôlé — TROIS octets sur 65 024 (la version R10 + LA POSE DU
WSABUF dans sys-05 ET sys-06, 0x64 → 0x68), l'héritage 0.9.0 recomposé
octet par octet (R7), la carte génération 11, le verrou croisé 86/86.

Le geste au coffre /test (modèle corriger_kit_m9f_e7.py, D143 : jamais
un jet — les mises à jour EN PLACE, l'ancien contenu vit dans
l'histoire git) :
  1. le zip local RÉPARÉ vérifié (empreintes attendues ci-dessous) ;
  2. kit-m9f.zip du coffre MIS À JOUR EN PLACE (upload_update : le
     contenu remplacé, le fichier même conservé) ;
  3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE (l'erratum n° 9 + la
     révision 2 consignés au document du kit) ;
  4. preuves-m9f/LISEZMOI-preuves.txt MIS À JOUR (l'artefact dev.3,
     la carte génération 11, LE CINQUIÈME RUN attendu) ;
  5. l'index des livraisons mis à jour (la note de la révision 2) ;
  6. la vérification finale (la racine en ordre, les empreintes
     recoupées, les PIÈCES DE CÉRÉMONIE demeurées — la seconde remise
     503f3822… + la clé ancre 188a7d42…).

Usage : python3 scripts/corriger_kit_m9f_e9.py
Code de sortie : 0 = coffre réparé et recoupé ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-m9f.zip"
LISEZMOI_KIT = os.path.join(REPO, "tls13", "terrain", "LISEZMOI-KIT-M9F.md")

# le kit RÉPARÉ (assembler_kit_m9f.py rejoué le 07/11 au soir après le
# rebuild dev.3 — le contrôle PERMANENT erratum n° 9 passé : la pose du
# WSABUF canonique relue dans l'image aux DEUX blocs)
KIT_SHA = ("1ced6ca071d6aa55ee961c02fb5f79c7276d4b82e6df861a5997c68a"
           "315fb22f")
KIT_MD5 = "79d44284c70261375a2b055070fda223"

# le kit de l'erratum n° 7 (celui des runs 3-4, le témoin de ce qu'on
# remplace) et son LISEZMOI + le LISEZMOI du réceptacle
ANCIEN_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"
ANCIEN_LIS_MD5 = "d5e7a4f59cd208c8347f7ac6ed763fe6"
ANCIEN_LIS_PREUVES_MD5 = "0387616d230a860da474c92009569146"

# les PIÈCES DE CÉRÉMONIE demeurées à la racine (le dossier du geste
# reçu : la SECONDE remise — la révision 2 étendue — déposée par le
# développeur le 07/11 au soir, recoupée 13/13 et installée)
SIG_MD5 = "503f382229b4da0ddd43e833d31b2c2b"
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"

LISEZMOI_PREUVES = """TRIADE — preuves-m9f : LE RÉCEPTACLE DU RUN TERRAIN M9-(f)
========================================================================
(LA SESSION RÉELLE — LA GRANDE ŒUVRE : la finale 1.0.0 attend le vert
de CE run ; l'artefact 1.0.0-dev.3 — LE REBUILD DE LA RÉVISION 2
ÉTENDUE : le WSABUF canonique posé à 0x68 dans sys-05 ET sys-06, la
carte génération 11)

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

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11/2026 au soir (le kit m9f RÉPARÉ — la révision 2
    étendue, l'erratum n° 8/n° 9 : le WSABUF canonique) : les runs 3-4
    (le 07/11) morts À L'ÉMISSION du CH (-6 → -7, déterministe sur
    Win10 ET Win11) ; LA SONDE SYS-05 a mesuré le NTSTATUS brut :
    0xC0000005 STATUS_ACCESS_VIOLATION × 3 — LE COUPABLE NOMMÉ À
    L'INSTRUCTION : la pose du WSABUF « packé » (buf à +4, le canonique
    x64 fait SEIZE octets : len à +0, padding 4 o, buf à +8 — le noyau
    lit l'adresse folle) ; sys-06 portait LE MÊME défaut (la symétrie
    send/recv). RÉPARATION SELON LA CHARTE : la révision 2 des DEUX
    specs + les DEUX notations (mov [rsp+0x68], rdi — le MÊME encode,
    le slot intact) + le harnais révisé (131 · 131 VERTS × 3 graines) ;
    LA CÉRÉMONIE : la remise étendue m8 c444d730… re-signée par la clé
    du développeur (l'ancre 173fae9c… tenue, les DOUZE arbres
    inchangés — Ed25519 déterministe), la garde 13/13 VERTS ; LE
    REBUILD 1.0.0-dev.3 (de23e577…) : le diff contrôlé TROIS octets
    sur 65 024 (la version R10 + les DEUX poses 0x64 → 0x68), la carte
    génération 11. kit-m9f.zip MIS À JOUR EN PLACE (md5 79d44284…),
    le LISEZMOI porte l'erratum, le réceptacle re-armé ; la finale
    1.0.0 attend LE CINQUIÈME run vert sur pièces.
"""


class Refus(Exception):
    """Tout refus nommé du livreur (fail-closed)."""


def md5f(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def maj_en_place(file_id, chemin_local, md5_attendu, nom_log):
    ds.upload_update(file_id, pathlib.Path(chemin_local))
    apres = None
    for tentative in range(3):        # la relecture peut courir la propagation
        apres = _entree_racine(nom_log)
        if apres and apres.get("md5Checksum") == md5_attendu:
            break
        import time
        time.sleep(2)
    if not apres or apres.get("md5Checksum") != md5_attendu:
        raise Refus(f"{nom_log} md5 divergent après mise à jour "
                    f"({(apres or {}).get('md5Checksum', 'ABSENT')[:8]}…)")
    print(f"    {nom_log} MIS À JOUR — md5 {md5_attendu[:8]}… MATCH par "
          f"relecture")


def _entree_racine(nom):
    return ds.list_folder(TEST_ID).get(nom)


def maj_index_texte(file_id, marqueur, section, nom_log):
    _, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    texte = body.decode("utf-8")
    if marqueur in texte:
        print(f"[index] {nom_log} déjà à jour — constaté")
        return
    texte = texte.rstrip("\n") + "\n" + section
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        f.write(texte)
        chemin_tmp = pathlib.Path(f.name)
    try:
        ds.upload_update(file_id, chemin_tmp)
    finally:
        os.unlink(chemin_tmp)
    print(f"[index] {nom_log} mis à jour")


def main() -> int:
    print("=== M9-(f) : LE KIT RÉPARÉ au coffre /test (la révision 2 "
          "étendue — l'erratum n° 9, le WSABUF canonique) ===")
    try:
        # -- 1. le zip local réparé, vérifié ---------------------------------
        if not os.path.isfile(KIT_ZIP):
            raise Refus(f"KIT : {KIT_ZIP} absent — assembler_kit_m9f.py "
                        "d'abord")
        if sha256f(KIT_ZIP) != KIT_SHA:
            raise Refus(f"KIT : kit-m9f.zip sha256 divergent "
                        f"({sha256f(KIT_ZIP)[:16]}…) — réassembler le kit "
                        "réparé")
        if md5f(KIT_ZIP) != KIT_MD5:
            raise Refus("KIT : kit-m9f.zip md5 divergent — réassembler")
        print(f"[1] le kit réparé : {os.path.getsize(KIT_ZIP)} o, md5 "
              f"{KIT_MD5[:8]}…, sha256 {KIT_SHA[:16]}… (28 constantes PAR "
              f"AST + le CONTRÔLE PERMANENT erratum n° 9 + extraction "
              f"vierge — VERT)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        arch_l = racine.get("archives-livraisons")
        if not (arch_p or {}).get("id") or not (arch_l or {}).get("id"):
            raise Refus("les salles d'archive sont introuvables au coffre "
                        "/test")

        # -- 2. kit-m9f.zip MIS À JOUR EN PLACE --------------------------------
        piece = racine.get("kit-m9f.zip")
        if not piece:
            raise Refus("kit-m9f.zip introuvable à la racine du /test")
        md5_distant = piece.get("md5Checksum", "")
        if md5_distant == KIT_MD5:
            print("[2] kit-m9f.zip porte DÉJÀ le md5 réparé — idempotent")
        else:
            if md5_distant != ANCIEN_MD5:
                raise Refus(f"kit-m9f.zip distant d'un md5 INATTENDU "
                            f"({md5_distant[:8]}…) — ni l'erratum n° 7 "
                            f"({ANCIEN_MD5[:8]}…) ni le réparé "
                            f"({KIT_MD5[:8]}…) : constater avant geste")
            maj_en_place(piece["id"], KIT_ZIP, KIT_MD5, "kit-m9f.zip")
            print("[2] kit-m9f.zip MIS À JOUR au coffre (le contenu "
                  "remplacé, le fichier même conservé, l'ancien kit vit "
                  "dans l'histoire git — les runs 3-4 l'ont exécuté, il "
                  "demeure la pièce de leurs archives)")

        # -- 3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE ---------------------------
        lis = racine.get("LISEZMOI-m9f.txt")
        if not lis:
            raise Refus("LISEZMOI-m9f.txt introuvable à la racine du /test")
        md5_lis_local = md5f(LISEZMOI_KIT)
        if lis.get("md5Checksum") == md5_lis_local:
            print("[3] LISEZMOI-m9f.txt porte déjà l'erratum n° 9 — "
                  "idempotent")
        else:
            if lis.get("md5Checksum") != ANCIEN_LIS_MD5:
                raise Refus(f"LISEZMOI-m9f.txt distant d'un md5 INATTENDU "
                            f"({(lis.get('md5Checksum') or 'ABSENT')[:8]}…)"
                            " — ni l'erratum n° 7 ni le réparé : constater "
                            "avant geste")
            maj_en_place(lis["id"], LISEZMOI_KIT, md5_lis_local,
                         "LISEZMOI-m9f.txt")
            print("[3] LISEZMOI-m9f.txt MIS À JOUR (l'erratum n° 9 + la "
                  "révision 2 étendue consignés au document du kit)")

        # -- 4. preuves-m9f/LISEZMOI-preuves.txt MIS À JOUR ---------------------
        pm9 = racine.get("preuves-m9f") or {}
        if not pm9.get("id"):
            raise Refus("preuves-m9f/ introuvable au coffre")
        lis_p = ds.list_folder(pm9["id"]).get("LISEZMOI-preuves.txt")
        if not lis_p:
            raise Refus("LISEZMOI-preuves.txt introuvable au réceptacle")
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(LISEZMOI_PREUVES)
            chemin_preuves = pathlib.Path(f.name)
        try:
            md5_preuves_local = md5f(chemin_preuves)
            if lis_p.get("md5Checksum") == md5_preuves_local:
                print("[4] LISEZMOI-preuves.txt déjà à jour — idempotent")
            else:
                if lis_p.get("md5Checksum") != ANCIEN_LIS_PREUVES_MD5:
                    raise Refus(
                        f"LISEZMOI-preuves.txt distant d'un md5 INATTENDU "
                        f"({(lis_p.get('md5Checksum') or 'ABSENT')[:8]}…) — "
                        "constater avant geste")
                ds.upload_update(lis_p["id"], chemin_preuves)
                apres = ds.list_folder(pm9["id"]).get("LISEZMOI-preuves.txt")
                if not apres or apres.get("md5Checksum") != md5_preuves_local:
                    raise Refus("LISEZMOI-preuves.txt md5 divergent après "
                                "mise à jour")
                print("[4] LISEZMOI-preuves.txt MIS À JOUR (l'artefact "
                      "dev.3, la carte génération 11, LE CINQUIÈME RUN "
                      "attendu)")
        finally:
            os.unlink(chemin_preuves)
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"({sorted(restants)}) — le réceptacle doit être "
                        f"vierge pour le run")
        print("    preuves-m9f/ ré-armé : le réceptacle du CINQUIÈME run "
              "(le premier du build réparé)")

        # -- 5. l'index des livraisons mis à jour -------------------------------
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "le kit m9f RÉPARÉ",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note de la "
                        "révision 2)")

        # -- 6. la vérification finale ------------------------------------------
        final = ds.list_folder(TEST_ID)
        attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                    "archives-livraisons", "archives-preuves",
                    "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                    "preuves-sonde-sys05", "corriger-wsb.bat",
                    "corriger-wsb.ps1", "signatures-I.txt",
                    "cle-publique-I.txt", "kit-sonde-sys05.zip",
                    "LISEZMOI-sonde-sys05.txt"}
        manquants = attendus - set(final)
        if manquants:
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("le kit de la racine a divergé — refus")
        # les PIÈCES DE CÉRÉMONIE demeurées : la SECONDE remise (la
        # révision 2 étendue, recoupée 13/13 et installée) + la clé ancre
        if final["signatures-I.txt"].get("md5Checksum") != SIG_MD5:
            raise Refus(f"signatures-I.txt porte un md5 inattendu "
                        f"({(final['signatures-I.txt'].get('md5Checksum') or '-')[:8]}…"
                        f") — la seconde remise {SIG_MD5[:8]}… attendue")
        if final["cle-publique-I.txt"].get("md5Checksum") != CLE_MD5:
            raise Refus("cle-publique-I.txt != l'ancre des ères — la "
                        "continuité serait rompue")
        print(f"[6] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit réparé md5 {KIT_MD5[:8]}… recoupé) ; les PIÈCES DE "
              f"CÉRÉMONIE demeurées : la SECONDE remise {SIG_MD5[:8]}… "
              f"(la révision 2 étendue, installée) + la clé ancre "
              f"{CLE_MD5[:8]}…")
    except (Refus, ds.SyncError) as exc:
        print(f"[réparation] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE COFFRE /test PORTE LE KIT RÉPARÉ (le build 1.0.0-dev.3 — "
          "le WSABUF canonique, la révision 2 étendue signée) : LE "
          "CINQUIÈME GESTE du développeur est attendu — dézipper "
          "kit-m9f.zip dans un dossier NEUF (D99), python scenario-m9f.py "
          "(~10 s, réseau vivant), renvoyer preuves-m9f/ ENTIER au coffre "
          "— la finale 1.0.0 attend le vert ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
