#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corriger_kit_m9f_e10.py — LE KIT TERRAIN M9-(f) RÉPARÉ au coffre
/test : LA RÉVISION 3 (l'erratum n° 10 — le contrat d'appel).

Les cinquième et sixième runs (le 07/11) ont EMIS le ClientHello SUR
LE RÉSEAU RÉEL (l'émission VERT ×2, la première émission réelle du
projet — l'erratum n° 9 validé sur le vrai noyau) puis sont morts À
LA PREMIÈRE LECTURE (-7 NOMMÉ, déterministe, le jumeau : le passager
éliminé sur pièces) ; LA SONDE SYS-06 a LU LE CODE EXACT de cette
première lecture réelle PAR LE TRAMPOLINE DE CAPTURE : -6,
0xC000000D STATUS_INVALID_PARAMETER, DÉTERMINISTE ×3 (le compas
étalonné avant la mesure, l'offre sys-05 VERT au même geste). LA
TABLE DE LA PASSATION 108 TRANCHE : INVALID_PARAMETER NOMME LE
CONTRAT D'APPEL ; l'A/B des notations nomme LE CHAMP : sys-05
(AfdFlags = 0) PASSE, sys-06 (AfdFlags = 0x20) REFUSÉ — LE VRAI
afd.sys REFUSE le bit 0x20 dans AfdFlags. L'erratum de lecture de
la révision 2 EST RÉFUTÉ PAR LE TERRAIN : TDI_RECEIVE_NORMAL (0x20)
RETOURNE au champ TdiFlags.

LA RÉPARATION SELON LA CHARTE (jamais une dérive silencieuse) : LA
RÉVISION 3 DE LA SPEC SYS-06 (AfdFlags = 0, TdiFlags =
TDI_RECEIVE_NORMAL 0x20 — la structure totale 40 o inchangée), la
notation corrigée (le QUATRIÈME champ porte le 0x20, le TROISIÈME
porte 0 — le même encode, le slot intact), le harnais suivi (le
noyau simulé AFD STRICT REFUSE désormais ce que le VRAI refuse —
131 contrôles · 131 VERTS × 3 graines) ; PUIS LA CÉRÉMONIE : LA
TROISIÈME SIGNATURE du développeur (la remise m8 e36141f7…
re-signée hors-ligne, l'ancre des ères 173fae9c… tenue, les DOUZE
arbres inchangés byte-identiques — Ed25519 déterministe, le recoup
D163 rejoint une CINQUIÈME fois), la garde 13/13 VERTS ; LE REBUILD
1.0.0-dev.4 (sha256 446279f3…) : le diff contrôlé — TROIS octets
sur 65 024 (la version R10 + LES DEUX IMMÉDIATES du contrat d'appel
dans sys-06), l'héritage 0.9.0 recomposé octet par octet (R7), la
carte génération 12, le verrou croisé 86/86.

Le geste au coffre /test (modèle corriger_kit_m9f_e9.py, D143 :
jamais un jet — les mises à jour EN PLACE, l'ancien contenu vit
dans l'histoire git) :
  1. le zip local RÉPARÉ vérifié (empreintes attendues ci-dessous) ;
  2. kit-m9f.zip du coffre MIS À JOUR EN PLACE (upload_update : le
     contenu remplacé, le fichier même conservé) ;
  3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE (l'erratum n° 10 + la
     révision 3 consignés au document du kit) ;
  4. preuves-m9f/LISEZMOI-preuves.txt MIS À JOUR (l'artefact dev.4,
     la carte génération 12, LE SEPTIÈME RUN attendu) — le
     réceptacle RÉ-ARMÉ ;
  5. l'index des livraisons mis à jour (la note de la révision 3) ;
  6. la vérification finale (la racine en ordre, les empreintes
     recoupées, les PIÈCES DE CÉRÉMONIE demeurées — la TROISIÈME
     remise 0978c117… + la clé ancre 188a7d42…).

Usage : python3 scripts/corriger_kit_m9f_e10.py
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

# le kit RÉPARÉ (assembler_kit_m9f.py rejoué le 07/11 après le rebuild
# dev.4 — le contrôle PERMANENT erratum n° 10 passé : le contrat
# d'appel relu dans l'image au bloc sys-06)
KIT_SHA = ("c0883c876f89faabb5d987c63dfebf1e2c3e99332339263739fbe88b"
           "982c4e46")
KIT_MD5 = "9209868796330fab0ea3f01b4879eb80"

# le kit de la révision 2 étendue (celui des runs 5-6 et de la sonde
# sys-06, le témoin de ce qu'on remplace) et son LISEZMOI + le
# LISEZMOI du réceptacle (l'ère dev.3, génération 11)
ANCIEN_MD5 = "79d44284c70261375a2b055070fda223"
ANCIEN_LIS_MD5 = "25f3d64e9e14c2a9798f7b3aeecfb66f"
ANCIEN_LIS_PREUVES_MD5 = "8a8a753c0d69b2e9b27f2f389cd4462e"

# les PIÈCES DE CÉRÉMONIE demeurées à la racine (le dossier du geste
# reçu : la TROISIÈME remise — la révision 3 — déposée par le
# développeur le 07/11, recoupée 13/13 et installée)
SIG_MD5 = "0978c117af62730508d60211f869bdf6"
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"

LISEZMOI_PREUVES = """TRIADE — preuves-m9f : LE RÉCEPTACLE DU RUN TERRAIN M9-(f)
========================================================================
(LA SESSION RÉELLE — LA GRANDE ŒUVRE : la finale 1.0.0 attend le vert
de CE run ; l'artefact 1.0.0-dev.4 — LE REBUILD DE LA RÉVISION 3 : le
contrat d'appel réparé SUR LE TERRAIN dans sys-06 [AfdFlags = 0,
TdiFlags = TDI_RECEIVE_NORMAL 0x20 — le VRAI afd.sys REFUSE le bit
0x20 dans AfdFlags, la mesure de la sonde], la carte génération 12)

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
--- note du 07/11/2026, seconde réparation (le kit m9f RÉPARÉ ENCORE
    — la révision 3, l'erratum n° 10 : le contrat d'appel) : les runs
    5-6 (le 07/11) ont EMIS le CH SUR LE RÉSEAU RÉEL (l'erratum n° 9
    validé sur le vrai noyau) puis sont morts À LA PREMIÈRE LECTURE
    (-7 déterministe, le jumeau) ; LA SONDE SYS-06 a LU LE CODE EXACT
    par le trampoline de capture : -6, STATUS_INVALID_PARAMETER ×3,
    DÉTERMINISTE — l'A/B des notations NOMME LE CHAMP : le VRAI
    afd.sys REFUSE le bit 0x20 dans AfdFlags (sys-05 AfdFlags=0 PASSE,
    sys-06 AfdFlags=0x20 REFUSÉ) ; l'erratum de lecture de la rév. 2
    RÉFUTÉ PAR LE TERRAIN : TDI_RECEIVE_NORMAL RETOURNE au champ
    TdiFlags. RÉPARATION SELON LA CHARTE : la révision 3 de la spec
    sys-06 (AfdFlags = 0, TdiFlags = 0x20) + la notation corrigée (le
    QUATRIÈME champ porte le 0x20 — le même encode, le slot intact) +
    le harnais suivi (le noyau simulé AFD STRICT — 131 · 131 VERTS ×
    3 graines) ; LA CÉRÉMONIE : la TROISIÈME signature du développeur
    (la remise m8 e36141f7… re-signée, l'ancre 173fae9c… tenue, les
    DOUZE arbres inchangés — Ed25519 déterministe, D163 rejoint une
    CINQUIÈME fois), la garde 13/13 VERTS ; LE REBUILD 1.0.0-dev.4
    (446279f3…) : le diff contrôlé TROIS octets sur 65 024 (la
    version R10 + LES DEUX IMMÉDIATES du contrat d'appel dans sys-06),
    la carte génération 12. kit-m9f.zip MIS À JOUR EN PLACE (md5
    92098687…), le LISEZMOI porte l'erratum, le réceptacle ré-armé ;
    la finale 1.0.0 attend LE SEPTIÈME run vert sur pièces.
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
    print("=== M9-(f) : LE KIT RÉPARÉ au coffre /test (la révision 3 — "
          "l'erratum n° 10, le contrat d'appel) ===")
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
              f"{KIT_MD5[:8]}…, sha256 {KIT_SHA[:16]}… (32 constantes PAR "
              f"AST + LE CONTRÔLE PERMANENT erratum n° 10 + extraction "
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
                            f"({md5_distant[:8]}…) — ni la révision 2 "
                            f"étendue ({ANCIEN_MD5[:8]}…) ni le réparé "
                            f"({KIT_MD5[:8]}…) : constater avant geste")
            maj_en_place(piece["id"], KIT_ZIP, KIT_MD5, "kit-m9f.zip")
            print("[2] kit-m9f.zip MIS À JOUR au coffre (le contenu "
                  "remplacé, le fichier même conservé, l'ancien kit vit "
                  "dans l'histoire git — les runs 5-6 et la sonde sys-06 "
                  "l'ont exécuté, il demeure la pièce de leurs archives)")

        # -- 3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE ---------------------------
        lis = racine.get("LISEZMOI-m9f.txt")
        if not lis:
            raise Refus("LISEZMOI-m9f.txt introuvable à la racine du /test")
        md5_lis_local = md5f(LISEZMOI_KIT)
        if lis.get("md5Checksum") == md5_lis_local:
            print("[3] LISEZMOI-m9f.txt porte déjà l'erratum n° 10 — "
                  "idempotent")
        else:
            if lis.get("md5Checksum") != ANCIEN_LIS_MD5:
                raise Refus(f"LISEZMOI-m9f.txt distant d'un md5 INATTENDU "
                            f"({(lis.get('md5Checksum') or 'ABSENT')[:8]}…)"
                            " — ni la révision 2 étendue ni le réparé : "
                            "constater avant geste")
            maj_en_place(lis["id"], LISEZMOI_KIT, md5_lis_local,
                         "LISEZMOI-m9f.txt")
            print("[3] LISEZMOI-m9f.txt MIS À JOUR (l'erratum n° 10 + la "
                  "révision 3 consignés au document du kit)")

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
                      "dev.4, la carte génération 12, LE SEPTIÈME RUN "
                      "attendu)")
        finally:
            os.unlink(chemin_preuves)
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"({sorted(restants)}) — le réceptacle doit être "
                        f"vierge pour le run")
        print("    preuves-m9f/ ré-armé : le réceptacle du SEPTIÈME run "
              "(le premier du contrat réparé)")

        # -- 5. l'index des livraisons mis à jour -------------------------------
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "le kit m9f RÉPARÉ ENCORE",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note de la "
                        "révision 3)")

        # -- 6. la vérification finale ------------------------------------------
        final = ds.list_folder(TEST_ID)
        attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                    "archives-livraisons", "archives-preuves",
                    "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                    "preuves-sonde-sys05", "preuves-sonde-sys06",
                    "corriger-wsb.bat", "corriger-wsb.ps1",
                    "signatures-I.txt", "cle-publique-I.txt",
                    "kit-sonde-sys05.zip", "LISEZMOI-sonde-sys05.txt",
                    "kit-sonde-sys06.zip", "LISEZMOI-sonde-sys06.txt"}
        manquants = attendus - set(final)
        if manquants:
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("le kit de la racine a divergé — refus")
        # les PIÈCES DE CÉRÉMONIE demeurées : la TROISIÈME remise (la
        # révision 3, recoupée 13/13 et installée) + la clé ancre
        if final["signatures-I.txt"].get("md5Checksum") != SIG_MD5:
            raise Refus(f"signatures-I.txt porte un md5 inattendu "
                        f"({(final['signatures-I.txt'].get('md5Checksum') or '-')[:8]}…"
                        f") — la troisième remise {SIG_MD5[:8]}… attendue")
        if final["cle-publique-I.txt"].get("md5Checksum") != CLE_MD5:
            raise Refus("cle-publique-I.txt != l'ancre des ères — la "
                        "continuité serait rompue")
        print(f"[6] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit réparé md5 {KIT_MD5[:8]}… recoupé) ; les PIÈCES DE "
              f"CÉRÉMONIE demeurées : la TROISIÈME remise {SIG_MD5[:8]}… "
              f"(la révision 3, installée) + la clé ancre "
              f"{CLE_MD5[:8]}…")
    except (Refus, ds.SyncError) as exc:
        print(f"[réparation] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE COFFRE /test PORTE LE KIT RÉPARÉ (le build 1.0.0-dev.4 — "
          "le contrat d'appel réparé, la révision 3 signée) : LE "
          "SEPTIÈME GESTE du développeur est attendu — dézipper "
          "kit-m9f.zip dans un dossier NEUF (D99), python scenario-m9f.py "
          "(~10 s, réseau vivant), renvoyer preuves-m9f/ ENTIER au coffre "
          "— la finale 1.0.0 attend le vert ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
