#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m8c_execution.py — LA PASSATION D141 DU BUNDLE au geste
« le chantier M8-(c) EXÉCUTÉ : la cérémonie de l'ère M8 installée + le build
0.9.0-dev.1 né » (le commit 9193019, la suite annoncée au Task 78) :
  1. le bundle triade-history-080-9193019.bundle (git bundle --all, pointe =
     LE commit du geste : la cérémonie du développeur VÉRIFIÉE [12/12 Ed25519
     contre 173fae9c…, le déterminisme prouvant la clé du 04/11 réutilisée,
     les signatures nouvelles exactement {m0, m8}] + DÉPOSÉE [le garde 12
     arbres VERTS, la dette D162 soldée] + LE BUILD EXÉCUTÉ [l'artefact
     44 544 o sha256 1492b0bc… DÉTERMINISTE inter-postes, la carte génération
     8, le verrou croisé 55/55] + Entrée 160 + D163 + worklog Task 78) est
     déposé au MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-080-b7b6e01.bundle (le porteur du kit
     de cérémonie de l'ère : LISEZMOI-ceremonie-ere-M8 + la remise, Task 77)
     est ARCHIVÉ VERSIONNÉ dans archives-bundles/ (JAMAIS supprimé ni
     écrasé — D141) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé).

Le relais OAuth du développeur (MIS À JOUR au /Tokens — la cause de la
reprise) porte l'écriture : le miroir, le kit et le bundle dans le MÊME geste.

La cadence « une passation par geste de jalon » est tenue. La série 080
continue (la série 090 naîtra à la finale 0.9.0 du jalon M8).

Chaque geste ASSERTÉ ; md5 recoupés AVANT tout déplacement ; idempotent par
saut d'already-fait. Déplacement : addParents/removeParents EN PARAMÈTRE DE
REQUÊTE (leçon v7/D143).

Usage : python3 scripts/passe_bundle_m8c_execution.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import pathlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-080-9193019.bundle"      # le courant NOUVEAU (le chantier M8-(c) exécuté)
ANCIEN = "triade-history-080-b7b6e01.bundle"      # le courant actuel au miroir (le kit de cérémonie, Task 77)
TIP_ATTENDU = "91930198c01984e93f08acaf067537cb1d3d0154"   # la pointe du geste (push recoupé)
CHEMIN_LOCAL = REPO + "/bundles-080/" + BUNDLE


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def main():
    # -- 0. le bundle local, construit et vérifié --------------------------------
    subprocess.run(["mkdir", "-p", REPO + "/bundles-080"], check=True)
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
    md5_local = ds.md5_of(pathlib.Path(CHEMIN_LOCAL))
    taille = pathlib.Path(CHEMIN_LOCAL).stat().st_size
    print(f"[0] bundle construit : {BUNDLE} ({taille} o, md5 {md5_local[:8]}…) — "
          f"branche jalon == {TIP_ATTENDU[:8]} (le chantier M8-(c) EXÉCUTÉ "
          f"avec sa consignation)")

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
        ds.upload_create(miroir["id"], BUNDLE, pathlib.Path(CHEMIN_LOCAL))
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
              f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — la racine "
              f"ne porte que le courant)")

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
    print(f"[état] courants versionnés au miroir : {courants} (+ triade-history.bundle, le nom standard)")
    print(f"[état] archives-bundles/ ({len(archives_finales)})")
    if BUNDLE not in courants:
        refus("ETAT-FINAL", f"le courant {BUNDLE} absent du miroir : {courants}")
    if ANCIEN not in archives_finales:
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives — D141 violée")
    print("[passation] D141 TERMINÉE — le bundle courant porte LE GESTE "
          "(9193019 : la cérémonie de l'ère M8 VÉRIFIÉE-INSTALLÉE [le garde "
          "12 arbres VERTS, la dette D162 soldée] + LE BUILD 0.9.0-dev.1 "
          "EXÉCUTÉ [l'artefact 44 544 o sha256 1492b0bc… DÉTERMINISTE "
          "inter-postes, la carte génération 8, le verrou croisé 55/55] + "
          "Entrée 160 + D163 + worklog Task 78), l'ancien (le kit de "
          "cérémonie de l'ère, b7b6e01) vit aux archives, rien n'a été supprimé")


if __name__ == "__main__":
    main()
