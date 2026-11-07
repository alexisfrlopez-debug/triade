#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run7_m9f.py — LE SEPTIÈME RUN M9-(f) ARCHIVÉ au coffre /test
(LE RUN DE LA GRANDE ŒUVRE : le 2026-11-07 12:21:26, reçu et recoupé —
VERT 34/34 SUR PIÈCES CROISÉES : LA SESSION RÉELLE ÉTABLIE, LA FINALE
1.0.0 SCELLÉE, LE JALON M9 FRANCHI).

Le kit est ACQUITTÉ (le kit RÉPARÉ 92098687… — LE MÊME que le run a
couru) : AUCUN dépôt de kit, AUCUN retrait — le geste est L'ARCHIVAGE
SEUL (modèle archiver_run4, D143 : par DÉPLACEMENT, jamais un jet) :
  1. les pièces locales vérifiées (les CINQ pièces md5-contrôlées par
     le recoup + le verdict du recoup 34/34) ;
  2. preuves-run-m9f-7/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. les CINQ pièces DU RUN DÉPLACÉES du réceptacle vers l'archive ;
  4. le VERDICT-recoup-labo-m9f-7.txt déposé AVEC les pièces (l'archive
     porte le jugement) ;
  5. preuves-m9f/ ré-armé (son LISEZMOI seul — le réceptacle demeure) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, le kit INCHANGÉ, les
     empreintes recoupées).

Usage : python3 scripts/archiver_run7_m9f.py
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

PIECES_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-7")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-7/"
    "VERDICT-recoup-labo-m9f-7.txt")

PIECES = {"temoin-m9f.txt": "339a4335",
          "scenario-m9f-journal.log": "acbe41c6",
          "ligne-recue.txt": "c9f4fd72",
          "journal-emissions.txt": "b1970feb",
          "VERDICT-run-m9f.txt": "0684256d"}

KIT_MD5 = "9209868796330fab0ea3f01b4879eb80"     # le kit RÉPARÉ, INCHANGÉ

PIECES_RUN7 = sorted(PIECES) + ["VERDICT-recoup-labo-m9f-7.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f-7/ (archivées le 07/11, LE GESTE DE LA GRANDE ŒUVRE — LE
SEPTIÈME run M9-(f) : LE PREMIER DU CONTRAT RÉPARÉ [l'erratum n° 10 :
AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20 — le contrat d'appel
relu dans l'image aux DEUX sites], l'artefact REBUILD 1.0.0-dev.4
[446279f3…] INTACT, le kit RÉPARÉ 92098687… INCHANGÉ ; VERT — LA
SESSION RÉELLE ÉTABLIE :
  - temoin-m9f.txt — LES VINGT T0 tranchés [ok] (dont LES DEUX
    erratum-9 ET LES DEUX erratum-10), le VRAI ntdll lu (SSN 85/7/15),
    le socket par LE VRAI afd.sys (zéro ws2_32), LA POIGNÉE OUVERTE
    (T3.ouvrir rax 0 état 3 — la mort -7 des runs 5/6 franchie), LE
    RECOUP DU CH (119 o == la construction re-jouée), LA LIGNE
    APPLICATIVE ÉCHANGÉE (le témoin HTTP/1.1 200 OK DÉCHIFFRÉ PAR LA
    MACHINE — 1369 o), LA GARDE -6 NOMMÉE contre le vrai serveur, LA
    FERMETURE PROPRE (close_notify 24 o, NtClose ×2, l'artefact relu
    inchangé) ;
  - scenario-m9f-journal.log — le run, HUIT lignes TOUTES VERTES, le
    run entier dans SA seconde (12:21:26) ;
  - ligne-recue.txt — LA PREMIÈRE LIGNE APPLICATIVE EN CLAIR DU
    PROJET (1369 o déchiffrés par la machine — « HTTP/1.1 200 OK ») ;
  - journal-emissions.txt — LES CINQ ÉMISSIONS DU RUN (436 o recadrés
    en CINQ records TLS SANS RESTE : le CH 119, le Finished 58, la
    ligne scellée 116, l'offre mutée 119, le close_notify 24) ;
  - VERDICT-run-m9f.txt — le verdict DU RUN : VERT — LA SESSION RÉELLE
    ÉTABLIE ;
  - VERDICT-recoup-labo-m9f-7.txt — le verdict du RECOUP laboratoire
    (VERT 34/34 sur pièces croisées, D138/D145/D148 : l'échelle REJOUÉE
    sur la clé privée DU RUN rend la clé du témoin, la construction CH
    re-jouée, LA LIGNE REÇUE LUE EN CLAIR sur la pièce, les émissions
    RECADRÉES record par record — LE CRITÈRE TENU : LA FINALE 1.0.0
    SCELLÉE, LE JALON M9 FRANCHI) — l'archive porte le jugement AVEC
    les pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle,
  ré-armé).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11, LE GESTE DE LA GRANDE ŒUVRE (LE SEPTIÈME run M9-(f)
    reçu et recoupé — le premier du contrat réparé) : le kit RÉPARÉ
    92098687… exécuté sur la machine familiale (Windows 10.0 build
    26300, le run : 2026-11-07 12:21:26) ; LES VINGT T0 [ok] (les DEUX
    erratum-10 compris), LA POIGNÉE OUVERTE — la mort -7 des runs 5/6
    FRANCHIE (le contrat d'appel réparé A VÉCU), LA LIGNE APPLICATIVE
    CHIFFRÉE ÉCHANGÉE (le témoin HTTP/1.1 200 OK DÉCHIFFRÉ PAR LA
    MACHINE), LA GARDE -6 NOMMÉE contre le vrai serveur, LA FERMETURE
    PROPRE ; le recoup labo VERT 34/34 sur pièces croisées (la ligne
    reçue LUE EN CLAIR sur la pièce, les CINQ émissions recadrées SANS
    RESTE) ; LE CRITÈRE TENU → LA FINALE 1.0.0 SCELLÉE (fait de carte
    — l'artefact 446279f3… INTACT, la balise au miroir de l'ère M8
    Entrée 164), LE JALON M9 FRANCHI — LA GRANDE ŒUVRE ; le run
    archivé → archives-preuves/preuves-run-m9f-7/ AVEC le verdict du
    recoup (34/34) ; le kit RÉPARÉ demeure au /test (la pièce du
    jalon).
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
    print(f"[archivage] {nom} -> preuves-run-m9f-7/ (md5 "
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
    print("=== M9-(f) : LE SEPTIÈME RUN ARCHIVÉ au coffre /test (LE RUN DE "
          "LA GRANDE ŒUVRE — le kit RÉPARÉ demeure, le geste est "
          "l'archive seule) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in PIECES.items():
            chemin = PIECES_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — le "
                            "rapatriement du recoup d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f-7.txt local introuvable — "
                        "le recoup d'abord (scripts/recouper_run7_m9f.py)")
        print(f"[1] les pièces locales vérifiées (les CINQ pièces "
              f"md5-contrôlées + le verdict du recoup "
              f"{md5f(VERDICT_RECOUP_LOCAL)[:8]}…, 34/34)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-run-m9f-7/ créé ------------------------------------------
        run_m9f7 = ds.list_folder(arch_p["id"]).get("preuves-run-m9f-7")
        if not run_m9f7:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f-7")
            print("[2] preuves-run-m9f-7/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_m9f7["id"]
            print("[2] preuves-run-m9f-7/ déjà présent — constaté")

        # -- 3. les CINQ pièces DU RUN, DÉPLACÉES depuis le réceptacle ----------
        pm9 = racine.get("preuves-m9f") or {}
        if not pm9.get("id"):
            raise Refus("preuves-m9f/ introuvable au coffre")
        for nom, prefixe in PIECES.items():
            entree = ds.list_folder(pm9["id"]).get(nom)
            if entree:
                if not entree.get("md5Checksum", "").startswith(prefixe):
                    raise Refus(f"la pièce distante {nom} d'un md5 "
                                "inattendu — constater avant geste")
                deplacer_vers(entree["id"], nom, pm9["id"], run_id,
                              entree["md5Checksum"])
            elif nom not in ds.list_folder(run_id):
                raise Refus(f"'{nom}' ni dans preuves-m9f/ ni dans "
                            "l'archive — introuvable")
            else:
                print(f"[3] {nom} déjà archivé — constaté")

        # -- 4. le verdict du recoup, déposé AVEC les pièces ---------------------
        if "VERDICT-recoup-labo-m9f-7.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f-7.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f-7.txt déposé (le jugement "
                  "AVEC les pièces — VERT 34/34, LE CRITÈRE TENU)")
        else:
            print("[4] VERDICT-recoup-labo-m9f-7.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé ----------------------------------------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle demeure)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f-7",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f-7)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "LE GESTE DE LA GRANDE ŒUVRE",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du "
                        "septième run)")

        # -- 7. la vérification finale ----------------------------------------------
        final = ds.list_folder(TEST_ID)
        attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                    "archives-livraisons", "archives-preuves",
                    "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                    "corriger-wsb.bat", "corriger-wsb.ps1",
                    "signatures-I.txt", "cle-publique-I.txt",
                    "kit-sonde-sys05.zip", "kit-sonde-sys06.zip",
                    "LISEZMOI-sonde-sys05.txt", "LISEZMOI-sonde-sys06.txt",
                    "preuves-sonde-sys05", "preuves-sonde-sys06"}
        manquants = attendus - set(final)
        if manquants:
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("le kit de la racine a divergé — le kit RÉPARÉ "
                        "doit demeurer 92098687…")
        dans_run = ds.list_folder(run_id)
        if set(PIECES_RUN7) - set(dans_run):
            raise Refus(f"preuves-run-m9f-7/ incomplet : "
                        f"{sorted(set(PIECES_RUN7) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit RÉPARÉ md5 {KIT_MD5[:8]}… INCHANGÉ — recoupé) ; "
              f"preuves-run-m9f-7/ porte les {len(PIECES_RUN7)} pièces "
              "(les CINQ pièces DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE SEPTIÈME RUN EST ARCHIVÉ avec son jugement : LA SESSION "
          "RÉELLE ÉTABLIE, LA FINALE 1.0.0 SCELLÉE, LE JALON M9 FRANCHI — "
          "LA GRANDE ŒUVRE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
