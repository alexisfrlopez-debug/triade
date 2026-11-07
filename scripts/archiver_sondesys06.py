#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_sondesys06.py — LE RUN DE LA SONDE SYS-06 (m9-(g)) ARCHIVÉ
au coffre /test (le run du 2026-11-07 09:28:56, reçu et recoupé — VERT-
MESURE 17/17 : LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE LU ET NOMMÉ,
-6 + STATUS_INVALID_PARAMETER, DÉTERMINISTE ; L'A/B DES NOTATIONS
NOMME LE CHAMP : AfdFlags 0x20 REFUSÉ PAR LE VRAI NOYAU — l'erratum
n° 10, LE TERRAIN A JUGÉ LA MESURE).

Les kits sont ACQUITTÉS (kit-m9f.zip 79d44284… + kit-sonde-sys05.zip
215c2caa… + kit-sonde-sys06.zip 67e2014d… — le livré du geste 108) :
AUCUN dépôt de kit, AUCUN retrait — le geste est L'ARCHIVAGE SEUL
(modèle archiver_sonde1 / archiver_run4, D143 : par DÉPLACEMENT, jamais
un jet) :
  1. les pièces locales vérifiées (le QUATUOR md5-contrôlé par le
     recoup + le verdict du recoup 17/17) ;
  2. preuves-sonde-sys06-1/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. le QUATUOR DU RUN DÉPLACÉ du réceptacle vers l'archive (le témoin,
     le journal, LE VERDICT VERT-MESURE du kit, l'émission de S4) ;
  4. le VERDICT-recoup-labo-sonde-sys06-1.txt déposé AVEC les pièces
     (l'archive porte le jugement) ;
  5. preuves-sonde-sys06/ ré-armé (son LISEZMOI seul — le réceptacle du
     prochain run) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, les TROIS kits
     INCHANGÉS, les empreintes recoupées).

Usage : python3 scripts/archiver_sondesys06.py
Code de sortie : 0 = coffre archivé et recoupé ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

QUATUOR_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-sonde-sys06")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-sonde-sys06/"
    "VERDICT-recoup-labo-sonde-sys06.txt")

# le QUATUOR DU RUN : le témoin, le journal, LE VERDICT du kit (né cette
# fois — l'erratum n° 8 du T6 est réparé depuis), l'émission de la
# contre-épreuve S4
QUATUOR = {"temoin-sonde-sys06.txt": "69122e4d",
           "sonde-sys06-journal.log": "05b499b7",
           "VERDICT-sonde-sys06.txt": "a4f68279",
           "journal-emissions.txt": "1bd8f538"}

KIT_M9F_MD5 = "79d44284c70261375a2b055070fda223"     # l'ACQUITTÉ, INCHANGÉ
KIT_SONDE05_MD5 = "215c2caa54332ce91b03fd55c335513b"  # l'ACQUITTÉ, INCHANGÉ
KIT_SONDE06_MD5 = "67e2014d5a5725d19bcabce548d2475e"  # le livré 108, INCHANGÉ

PIECES_RUN1 = sorted(QUATUOR) + ["VERDICT-recoup-labo-sonde-sys06-1.txt"]

INDEX_PREUVES_SECTION = """
preuves-sonde-sys06-1/ (archivées le 07/11 — LE RUN DE LA SONDE SYS-06
(m9-(g), le miroir de l'Entrée 185 livré au geste 108) : LE MOT
D'INFORMATION EST VENU — LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE
LU ET NOMMÉ [la limite de l'instrument FRANCHIE par le trampoline de
capture, l'artefact INTACT] : code -6, NTSTATUS STATUS_INVALID_PARAMETER
(0xC000000D), CLASSE ERREUR — un vrai refus du noyau, DÉTERMINISTE
[la mesure + la variation taille capacité 1 + la variation délai 2 s,
les TROIS identiques ; le compas étalonné : STATUS_INVALID_HANDLE sur
le handle invalide — la capture lit VRAIMENT rdx ; l'offre sys-05
rax 0 AU MÊME GESTE : le handle et le chemin lavés ; S4 : le chemin
standard meurt AU MÊME GESTE, rax -7 état 5 — la coupure du socle, la
mesure du trampoline parle pour les DEUX] ; LA TABLE DE LA PASSATION
108 TRANCHE : ni la percée [n ≥ 1], ni la demi-fin [-7 / rdx 0], ni le
bug du bloc [PENDING], ni le pair [RESET/DISCONNECT] —
INVALID_PARAMETER NOMME LE CONTRAT D'APPEL ; L'A/B DES NOTATIONS LE
RESSERRE AU CHAMP : sys-05 [l'émission, AfdFlags 0] PASSE sur LE MÊME
montage, sys-06 [AfdFlags 0x20] est REFUSÉ — LE VRAI afd.sys [Win11
build 26300] REFUSE le bit 0x20 dans le champ AfdFlags ; l'erratum de
lecture de l'Entrée 187 [la mesure WinDbg citée : 0x20 en TROISIÈME
champ] EST RÉFUTÉ PAR LE TERRAIN : TDI_RECEIVE_NORMAL [0x20]
RETOURNE au champ TdiFlags, le placement de la littérature ; le -7 des
SIX runs m9f EST DÉSORMAIS LU : la machine -7/état 5 == sys-06 -6 ==
le noyau INVALID_PARAMETER — les SIX runs mouraient DU CONTRAT
D'APPEL ; le recoup labo 17/17 :
  - temoin-sonde-sys06.txt, sonde-sys06-journal.log,
    VERDICT-sonde-sys06.txt, journal-emissions.txt — les pièces DU RUN
    (le run entier : les T0 [les DEUX erratum-9 relus dans l'image],
    le trampoline 33 o, le compas étalonné AVANT la mesure, L'OFFRE
    sys-05 rax 0, LA MESURE -6 + 0xC000000D, les DEUX variations, S4
    [rax -7 état 5, l'émission 119 o == le CH de référence], T6
    PROPRE) ;
  - VERDICT-recoup-labo-sonde-sys06-1.txt — le verdict du RECOUP
    laboratoire (17/17 sur pièces croisées, D138/D145/D148 :
    l'artefact IDENTIQUE de23e577…, le VRAI ntdll b072efae… — le même
    noyau que les runs 5/6, le trampoline == le squelette de la
    source, la table NTSTATUS canonique, L'A/B DES NOTATIONS lue
    octet par octet) — l'archive porte le jugement AVEC les pièces.
  preuves-sonde-sys06/ demeure à la racine avec son LISEZMOI (le
  réceptacle, ré-armé pour le prochain run du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11 (LE RUN DE LA SONDE SYS-06 reçu et recoupé — LE MOT
    D'INFORMATION qui manquait à l'instrument) : le MÊME kit
    67e2014d… exécuté sur la machine Windows 11 build 26300 (le run :
    2026-11-07 09:28:56, l'heure de la machine du développeur) ; le
    compas étalonné (STATUS_INVALID_HANDLE : la capture lit VRAIMENT
    rdx) ; L'OFFRE sys-05 VERT (rax 0 — la reproduction des runs 5/6) ;
    LA MESURE : LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE = -6,
    NTSTATUS STATUS_INVALID_PARAMETER (0xC000000D), CLASSE ERREUR —
    TROIS fois [la mesure, la variation taille, la variation délai :
    DÉTERMINISTE] ; S4 : le chemin standard meurt AU MÊME GESTE (-7,
    état 5) — la mesure parle pour les DEUX ; LA TABLE DE LA PASSATION
    108 TRANCHE : INVALID_PARAMETER NOMME LE CONTRAT D'APPEL ; L'A/B
    DES NOTATIONS NOMME LE CHAMP : AfdFlags 0x20 EST LE PARAMÈTRE
    INVALIDE (sys-05 passe AfdFlags 0 sur LE MÊME montage) — LE VRAI
    noyau REFUSE le bit 0x20 dans AfdFlags, l'erratum de lecture de
    l'Entrée 187 EST RÉFUTÉ PAR LE TERRAIN : TDI_RECEIVE_NORMAL
    RETOURNE au champ TdiFlags ; le recoup labo 17/17, le run archivé
    → archives-preuves/preuves-sonde-sys06-1/ AVEC le verdict ; LA
    RÉPARATION SELON LA CHARTE : L'ERRATUM n° 10 + LA RÉVISION 3 DE LA
    SPEC SYS-06 [AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20] +
    la notation corrigée [le même encode 8 o, le slot intact] + le
    harnais suivi [131 contrôles · 131 VERTS × 3 graines] + la remise
    régénérée m8 e36141f7… ; LA TROISIÈME SIGNATURE DU DÉVELOPPEUR
    ATTENDUE — puis LE REBUILD 1.0.0-dev.4, LE KIT M9F RÉPARÉ, le
    run, ET SI LE VERT TIENT : LA FINALE 1.0.0, le jalon M9 — LA
    GRANDE ŒUVRE.
"""


class Refus(Exception):
    """Tout refus nommé du passeur (fail-closed)."""


def md5f(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def deplacer_vers(file_id, nom, parent_de, parent_vers, md5_attendu):
    url = (f"{ds.API}/files/{file_id}?"
           + "addParents=" + parent_vers
           + "&removeParents=" + parent_de)
    st, body, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise Refus(f"déplacement de '{nom}' impossible (HTTP {st}) : "
                    f"{body[:200]!r}")
    apres = ds.list_folder(parent_vers).get(nom)
    if not apres:
        raise Refus(f"'{nom}' absent de la salle d'archive après le geste")
    if apres.get("md5Checksum") != md5_attendu:
        raise Refus(f"'{nom}' archivé : md5 divergent après le geste")
    if nom in ds.list_folder(parent_de):
        raise Refus(f"'{nom}' demeure à son ancienne place après le geste")
    print(f"[archivage] {nom} -> preuves-sonde-sys06-1/ (md5 "
          f"{md5_attendu[:8]}… constaté après — D143 : un déplacement, "
          "jamais un jet)")


def maj_index_texte(file_id, marqueur, section, nom_log, avant_fin=False):
    _, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    texte = body.decode("utf-8")
    if marqueur in texte:
        print(f"[index] {nom_log} déjà à jour — constaté")
        return
    if avant_fin:
        fin = "— Fin de l'index"
        if fin in texte:
            texte = texte.replace(fin, section.lstrip("\n") + "\n" + fin, 1)
        else:
            texte = texte.rstrip("\n") + "\n" + section
    else:
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
    print("=== M9-(g) : LE RUN DE LA SONDE SYS-06 ARCHIVÉ au coffre "
          "/test (les TROIS kits ACQUITTÉS demeurent — le geste est "
          "l'archive seule) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in QUATUOR.items():
            chemin = QUATUOR_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — "
                            "ramasse_sondesys06.py d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-sonde-sys06.txt local "
                        "introuvable — le recoup d'abord "
                        "(scripts/recouper_sondesys06.py)")
        print(f"[1] les pièces locales vérifiées (le QUATUOR md5-contrôlé + "
              f"le verdict du recoup {md5f(VERDICT_RECOUP_LOCAL)[:8]}…, "
              "17/17)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-sonde-sys06-1/ créé ---------------------------------------
        run_s1 = ds.list_folder(arch_p["id"]).get("preuves-sonde-sys06-1")
        if not run_s1:
            run_id = ds.create_folder(arch_p["id"], "preuves-sonde-sys06-1")
            print("[2] preuves-sonde-sys06-1/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_s1["id"]
            print("[2] preuves-sonde-sys06-1/ déjà présent — constaté")

        # -- 3. le QUATUOR DU RUN, DÉPLACÉ depuis le réceptacle -------------------
        psonde = racine.get("preuves-sonde-sys06") or {}
        if not psonde.get("id"):
            raise Refus("preuves-sonde-sys06/ introuvable au coffre")
        for nom, prefixe in QUATUOR.items():
            entree = ds.list_folder(psonde["id"]).get(nom)
            if entree:
                if not entree.get("md5Checksum", "").startswith(prefixe):
                    raise Refus(f"la pièce distante {nom} d'un md5 "
                                "inattendu — constater avant geste")
                deplacer_vers(entree["id"], nom, psonde["id"], run_id,
                              entree["md5Checksum"])
            elif nom not in ds.list_folder(run_id):
                raise Refus(f"'{nom}' ni dans preuves-sonde-sys06/ ni dans "
                            "l'archive — introuvable")
            else:
                print(f"[3] {nom} déjà archivé — constaté")

        # -- 4. le verdict du recoup, déposé AVEC les pièces ---------------------
        if "VERDICT-recoup-labo-sonde-sys06-1.txt" not in \
                ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-sonde-sys06-1.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-sonde-sys06-1.txt déposé (le "
                  "jugement AVEC les pièces — VERT-MESURE 17/17, LE "
                  "COUPABLE NOMMÉ : LE CHAMP AfdFlags)")
        else:
            print("[4] VERDICT-recoup-labo-sonde-sys06-1.txt déjà là — "
                  "constaté")

        # -- 5. preuves-sonde-sys06/ ré-armé --------------------------------------
        restants = ds.list_folder(psonde["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-sonde-sys06/ ne porte pas seulement son "
                        f"LISEZMOI après l'archivage : {sorted(restants)}")
        print("[5] preuves-sonde-sys06/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle du prochain run)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-sonde-sys06-1",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-sonde-sys06-1)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "LE RUN DE LA SONDE SYS-06",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du run "
                        "de la sonde)")

        # -- 7. la vérification finale ----------------------------------------------
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
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_M9F_MD5:
            raise Refus("le kit m9f de la racine a divergé — "
                        "l'ACQUITTÉ doit demeurer 79d44284…")
        if final["kit-sonde-sys05.zip"].get("md5Checksum") != \
                KIT_SONDE05_MD5:
            raise Refus("le kit sonde sys-05 de la racine a divergé — "
                        "l'ACQUITTÉ doit demeurer 215c2caa…")
        if final["kit-sonde-sys06.zip"].get("md5Checksum") != \
                KIT_SONDE06_MD5:
            raise Refus("le kit sonde sys-06 de la racine a divergé — "
                        "le livré du geste 108 doit demeurer 67e2014d…")
        dans_run = ds.list_folder(run_id)
        if set(PIECES_RUN1) - set(dans_run):
            raise Refus(f"preuves-sonde-sys06-1/ incomplet : "
                        f"{sorted(set(PIECES_RUN1) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, les "
              f"TROIS kits md5 {KIT_M9F_MD5[:8]}… + {KIT_SONDE05_MD5[:8]}… "
              f"+ {KIT_SONDE06_MD5[:8]}… INCHANGÉS — recoupés) ; "
              f"preuves-sonde-sys06-1/ porte les {len(PIECES_RUN1)} pièces "
              "(le QUATUOR DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE RUN DE LA SONDE SYS-06 EST ARCHIVÉ avec son jugement : "
          "LE CODE EXACT LU (-6, INVALID_PARAMETER), LE CHAMP NOMMÉ "
          "(AfdFlags 0x20 REFUSÉ PAR LE VRAI NOYAU) — L'ERRATUM n° 10 ET "
          "LA RÉVISION 3 SONT LA RÉPARATION, LA TROISIÈME SIGNATURE EST "
          "ATTENDUE, PUIS LE REBUILD 1.0.0-dev.4, LE KIT RÉPARÉ, LE RUN : "
          "SI LE VERT TIENT, LA FINALE 1.0.0, LE JALON M9 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
