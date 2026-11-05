#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m8d.py — LA PASSATION D141 DU BUNDLE au geste
« le chantier M8-(d) : le kit terrain déposé au coffre /test » (le geste 1e3aaf6 + sa consignation b5d5018) :
  1. triade-history-080-1e3aaf6.bundle (git bundle --all, pointe = LE commit
     du geste : le scénario du VRAI ntdll en quatre temps + l'épreuve de
     labo [recoup AST] + le dépôt au coffre [la vague m8d] + Entrée 162 +
     worklog Task 80) déposé au MIROIR (TRIADE-sauvegarde-git/ — D141) ;
  2. l'ancien courant triade-history-080-9193019.bundle (la cérémonie de
     l'ère installée + le build 0.9.0-dev.1 né) ARCHIVÉ VERSIONNÉ dans
     archives-bundles/ (jamais supprimé — D141) ;
  3. /test recoupé SANS copie de bundle.
La série 080 continue (la série 090 naîtra à la finale 0.9.0).
Chaque geste ASSERTÉ ; md5 recoupés AVANT tout déplacement ; idempotent.
Usage : python3 scripts/passe_bundle_m8d.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import pathlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-080-b5d5018.bundle"
ANCIEN = "triade-history-080-9193019.bundle"
TIP_ATTENDU = "b5d5018a9b96d17619e8a8396234aff5a735e1ca"
CHEMIN_LOCAL = REPO + "/bundles-080/" + BUNDLE


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def main():
    subprocess.run(["mkdir", "-p", REPO + "/bundles-080"], check=True)
    out = subprocess.run(["git", "bundle", "create", CHEMIN_LOCAL, "--all"],
                         cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        refus("BUNDLE-CREATE", out.stderr[:200])
    tetes = subprocess.run(["git", "bundle", "list-heads", CHEMIN_LOCAL],
                           cwd=REPO, capture_output=True, text=True).stdout
    ligne = next((l for l in tetes.splitlines()
                  if l.endswith("refs/heads/bundle051/v0.5.1-jalon-v7")), "")
    if not ligne.startswith(TIP_ATTENDU):
        refus("BUNDLE-TETES", f"la branche jalon != le geste : {ligne[:80]!r}")
    md5_local = ds.md5_of(pathlib.Path(CHEMIN_LOCAL))
    print(f"[0] bundle construit : {BUNDLE} "
          f"({pathlib.Path(CHEMIN_LOCAL).stat().st_size} o, "
          f"md5 {md5_local[:8]}…) — branche jalon == {TIP_ATTENDU[:8]}")

    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ancien = racine_m.get(ANCIEN) or refus("ETAT", f"{ANCIEN} introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives introuvables")

    if racine_m.get(BUNDLE):
        if racine_m[BUNDLE].get("md5Checksum") != md5_local:
            refus("DEPOT", f"{BUNDLE} déjà présent avec un md5 divergent")
        print(f"[2] {BUNDLE} déjà présent (md5 MATCH) — idempotent")
    else:
        ds.upload_create(miroir["id"], BUNDLE, pathlib.Path(CHEMIN_LOCAL))
        apres = lister(miroir["id"]).get(BUNDLE) or refus("DEPOT", "absent après dépôt")
        if apres.get("md5Checksum") != md5_local:
            refus("DEPOT", "md5 distant ≠ local après dépôt")
        print(f"[2] déposé au miroir : {BUNDLE} (md5 {md5_local[:8]}… MATCH)")

    if lister(archives["id"]).get(ANCIEN):
        print(f"[3] {ANCIEN} déjà archivé — idempotent")
    else:
        url = (ds.API + f"/files/{ancien['id']}"
               f"?addParents={archives['id']}&removeParents={miroir['id']}")
        st, rep, _ = ds.api("PATCH", url, body={})
        if st not in (200, 201):
            refus("ARCHIVAGE", f"HTTP {st} : {rep[:150]!r}")
        if ANCIEN in lister(miroir["id"]):
            refus("ARCHIVAGE", f"{ANCIEN} demeure au miroir")
        cible = lister(archives["id"]).get(ANCIEN) or refus("ARCHIVAGE", "absent des archives")
        if cible.get("md5Checksum") != ancien.get("md5Checksum"):
            refus("ARCHIVAGE", "md5 divergent après déplacement")
        print(f"[3] archivé versionné : {ANCIEN} → archives-bundles/ "
              f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé)")

    test = coffre.get("test")
    if test:
        copies = [n for n in lister(test["id"]) if n.endswith(".bundle")]
        if copies:
            refus("TEST", f"copies de bundle au /test : {copies}")
        print("[4] /test ne porte AUCUNE copie de bundle (recoupé)")

    final = lister(miroir["id"])
    courants = [n for n in final if n.startswith("triade-history-0") and n.endswith(".bundle")]
    if BUNDLE not in courants:
        refus("ETAT-FINAL", f"le courant absent : {courants}")
    print(f"[état] courants versionnés au miroir : {sorted(courants)} ; "
          f"archives ({len(lister(archives['id']))})")
    print("=== PASSATION TERMINÉE : le bundle courant porte LE KIT TERRAIN "
          "M8-(d) (le scénario du VRAI ntdll + l'épreuve AST + le dépôt au "
          "coffre + Entrée 162 + Task 80) — l'ancien (la cérémonie + le "
          "build 0.9.0-dev.1) vit aux archives ===")


if __name__ == "__main__":
    main()
