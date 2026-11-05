#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_finale_090.py — LA PASSATION D141 DU BUNDLE au geste
« JALON M8 FRANCHI / RUN TERRAIN VERT SUR PIÈCES + RECOUP LABO 30/30 +
FINALE 0.9.0 SCELLÉE » : LA SÉRIE 090 NAÎT À LA FINALE 0.9.0.
  1. le bundle triade-history-090-4edf0c3.bundle (git bundle --all, pointe =
     LE commit du geste : LE RUN TERRAIN M8-(d) VERT SUR PIÈCES [35 verts /
     0 échecs sur la machine du développeur — Windows 10.0 build 26300, le
     VRAI ntdll lu par les DEUX lecteurs indépendants, LA TWIN 33 octets par
     l'IAT kernel32 == le syscall direct NtWriteFile, le refus nommé sur
     pièce VIDE] + LE RECOUP LABORATOIRE VERT 30/30 SUR PIÈCES CROISÉES [le
     juge est le code ; DEUX défauts d'instrument nommés par le fail-closed,
     corrigés et rejoués, les pièces immuables] + LA FINALE 0.9.0 SCELLÉE
     [--sceller-final né au geste, modèle D147/corpus : garde sceau I + le
     recoup terrain EXIGÉ COMME PIÈCE + cristallisation 55×10/10 + verrou
     croisé avant/après + bascule unique dev.1→0.9.0 dans frag-bld ;
     l'ARTEFACT INTACT 1492b0bc… — le fait de carte] + les consignations
     [Entrée 164, D165, PLAN jalon M8 FRANCHI, worklog Task ID 82]) est
     déposé au MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-080-b5d5018.bundle (le porteur de la
     vague m8d : le kit terrain + sa correction, Entrées 162-163/D158,
     Tasks 80-81) est ARCHIVÉ VERSIONNÉ dans archives-bundles/ (JAMAIS
     supprimé ni écrasé — D141) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé).

La cadence « une passation par geste de jalon » est tenue : le bundle
courant porte désormais LA FINALE DU JALON M8 avec sa consignation. LA
SÉRIE 090 NAÎT à la 0.9.0 — la série 080 s'achève avec lui aux archives.

Usage : python3 scripts/passe_bundle_finale_090.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-090-4edf0c3.bundle"      # le courant NOUVEAU (la finale 0.9.0)
ANCIEN = "triade-history-080-b5d5018.bundle"      # le courant actuel au miroir (la vague m8d corrigée)
TIP_ATTENDU = "4edf0c3bfa9504c84bca40e76f07bfca42318dc2"   # la pointe du geste (push recoupé)
CHEMIN_LOCAL = REPO + "/bundles-090/" + BUNDLE


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def main():
    # -- 0. le bundle local, construit et vérifié --------------------------------
    subprocess.run(["mkdir", "-p", REPO + "/bundles-090"], check=True)
    out = subprocess.run(["git", "bundle", "create", CHEMIN_LOCAL, "--all"],
                         cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        refus("BUNDLE-CREATE", out.stderr[:200])
    tetes = subprocess.run(["git", "bundle", "list-heads", CHEMIN_LOCAL],
                           cwd=REPO, capture_output=True, text=True).stdout
    ligne_jalon = next((l for l in tetes.splitlines()
                        if l.endswith("refs/heads/bundle051/v0.5.1-jalon-v7")), "")
    if not ligne_jalon.startswith(TIP_ATTENDU):
        refus("BUNDLE-TETES", f"la branche jalon du bundle ne pointe pas sur le "
                              f"geste : {ligne_jalon[:80]!r}")
    octets = open(CHEMIN_LOCAL, "rb").read()
    md5_local = hashlib.md5(octets).hexdigest()
    print(f"[0] bundle construit : {BUNDLE} ({len(octets)} o, md5 {md5_local[:8]}…) — "
          f"branche jalon == {TIP_ATTENDU[:7]} (LA FINALE 0.9.0 — le jalon M8 "
          f"franchi avec sa consignation)")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ancien = racine_m.get(ANCIEN) or refus("ETAT", f"l'ancien courant {ANCIEN} introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives-bundles/ introuvable")
    deja = racine_m.get(BUNDLE)
    deja_arch = lister(archives["id"]).get(BUNDLE)
    print(f"[état] ancien courant : {ANCIEN} (md5 {ancien.get('md5Checksum', '')[:8]}…)")
    print(f"[état] archives-bundles/ : {len(lister(archives['id']))} archives")

    # -- 2. dépôt du NOUVEAU courant au miroir --------------------------------------
    if deja or deja_arch:
        cible = deja or deja_arch
        if cible.get("md5Checksum") != md5_local:
            refus("DEPOT", f"{BUNDLE} existe déjà avec un md5 divergent — abandon")
        print(f"[2] {BUNDLE} déjà présent (md5 MATCH) — idempotent")
    else:
        ds.upload_create(miroir["id"], BUNDLE, ds.pathlib.Path(CHEMIN_LOCAL))
        apres = lister(miroir["id"])
        f = apres.get(BUNDLE) or refus("DEPOT", f"{BUNDLE} absent après dépôt")
        if f.get("md5Checksum") != md5_local:
            refus("DEPOT", f"{BUNDLE} : md5 distant ≠ local après dépôt")
        print(f"[2] déposé au miroir : {BUNDLE} (md5 {md5_local[:8]}… MATCH par relecture)")

    # -- 3. l'ancien ARCHIVÉ VERSIONNÉ (jamais supprimé, jamais écrasé) -------------
    deja_archives = lister(archives["id"]).get(ANCIEN)
    if deja_archives:
        if deja_archives.get("md5Checksum") != ancien.get("md5Checksum"):
            refus("ARCHIVAGE", f"{ANCIEN} : l'exemplaire archivé diverge de l'ancien courant")
        print(f"[3] {ANCIEN} déjà archivé — idempotent")
    else:
        url = (ds.API + f"/files/{ancien['id']}"
               f"?addParents={archives['id']}&removeParents={miroir['id']}")
        st, rep, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            refus("ARCHIVAGE", f"HTTP {st} : {rep[:150]!r}")
        apres_racine = lister(miroir["id"])
        apres_archives = lister(archives["id"])
        if ANCIEN in apres_racine:
            refus("ARCHIVAGE", f"{ANCIEN} RESTE à la racine du miroir — déplacement inopérant")
        cible = apres_archives.get(ANCIEN) or refus("ARCHIVAGE", f"{ANCIEN} absent de l'archive après déplacement")
        if cible.get("md5Checksum") != ancien.get("md5Checksum"):
            refus("ARCHIVAGE", f"{ANCIEN} : md5 diverge après déplacement")
        print(f"[3] archivé versionné : {ANCIEN} → archives-bundles/ "
              f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — la racine ne porte "
              f"que le courant ; la série 080 s'achève aux archives)")

    # -- 4. aucun bundle parasite au /test (recoupé, rien à retirer) ----------------
    test = coffre.get("test")
    if test:
        copies = [n for n in lister(test["id"]) if n.endswith(".bundle")]
        if copies:
            refus("TEST", f"copie(s) de bundle au /test (à traiter avant clôture) : {copies}")
        print("[4] /test ne porte AUCUNE copie de bundle — rien à retirer (recoupé)")

    # -- 5. l'état FINAL (recoupement) ----------------------------------------------
    final = lister(miroir["id"])
    courants = sorted(n for n in final if n.startswith("triade-history-0") and n.endswith(".bundle"))
    archives_finales = sorted(lister(archives["id"]))
    print(f"[état] courant au miroir : {courants}")
    print(f"[état] archives-bundles/ ({len(archives_finales)})")
    if courants != [BUNDLE]:
        refus("ETAT-FINAL", f"la racine du miroir ne porte pas LE courant unique : {courants}")
    if ANCIEN not in archives_finales:
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives — D141 violée")
    print("[passation] D141 TERMINÉE — le bundle courant porte LA FINALE 0.9.0 "
          "DU JALON M8 (4edf0c3 : le run terrain VERT sur pièces + le recoup "
          "labo 30/30 sur pièces croisées + la finale 0.9.0 scellée l'artefact "
          "intact + Entrée 164 + D165), l'ancien vit aux archives, LA SÉRIE "
          "090 EST NÉE, rien n'a été supprimé")


if __name__ == "__main__":
    main()
