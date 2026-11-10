#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_finale_loupe_010.py — LA PASSATION D141 DU BUNDLE au geste
« JALON M10 FRANCHI / LE ONZIÈME RUN VERT RECOUPÉ 39/39 + LA FINALE
`loupe 0.1.0` SCELLÉE » : LA SÉRIE 090 POURSUIT À LA FINALE DU TGN.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all, pointe =
     LE commit de la clôture : LE ONZIÈME RUN recoupé 39/39 [T0→T7 tout vert
     la quatrième fois, LA CASCADE 205 vécue entière la première fois, LA
     VITRINE VIVANTE la seconde fois — l'Entrée 217] + LA DETTE DE LA CARTE
     SOLDÉE par la régénération des notations [18/18 == la pièce octet pour
     octet, 587 → 0 — l'Entrée 218] + LA BALISE loupe 0.1.0 SCELLÉE [fait de
     carte, l'artefact 054de960… INTACT] + LA CLÔTURE COMPLÉMENTAIRE [les
     pièces du recoup au dépôt, la porte réparée, D178, le PLAN clos —
     l'Entrée 219]) est déposé au MIROIR (TRIADE-sauvegarde-git/ — l'histoire
     vit là, D141) ;
  2. l'ancien courant triade-history-090-a541f4b.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé — D141) ;
  3. l'orphelin du geste parallèle discardé (scripts/consigner_entree_218.py
     — le miroir ne supprime jamais, la clôture le retire : le miroir dit ce
     que le dépôt dit) ;
  4. aucun retrait /test : aucune copie de bundle n'y vit (recoupé).

Usage : python3 scripts/passe_bundle_finale_loupe_010.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

ANCIEN = "triade-history-090-a541f4b.bundle"      # le courant actuel au miroir


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def main():
    # -- 0. la pointe locale (le commit de la clôture, poussé et recoupé) ------
    tip = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                         capture_output=True, text=True).stdout.strip()
    tip_court = tip[:7]
    bundle = f"triade-history-090-{tip_court}.bundle"
    chemin_local = REPO + "/bundles-090/" + bundle
    print(f"[0] la pointe de la clôture : {tip_court} ({bundle})")

    subprocess.run(["mkdir", "-p", REPO + "/bundles-090"], check=True)
    out = subprocess.run(["git", "bundle", "create", chemin_local, "--all"],
                         cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        refus("BUNDLE-CREATE", out.stderr[:200])
    tetes = subprocess.run(["git", "bundle", "list-heads", chemin_local],
                           cwd=REPO, capture_output=True, text=True).stdout
    ligne_main = next((l for l in tetes.splitlines()
                       if l.endswith("refs/heads/main")), "")
    if not ligne_main.startswith(tip):
        refus("BUNDLE-TETES", f"main du bundle != la pointe : {ligne_main[:80]!r}")
    octets = open(chemin_local, "rb").read()
    md5_local = hashlib.md5(octets).hexdigest()
    print(f"[0] bundle construit : {bundle} ({len(octets)} o, md5 "
          f"{md5_local[:8]}…) — main == {tip_court} (LA FINALE loupe 0.1.0 "
          f"— le jalon M10 franchi avec sa clôture)")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ancien = racine_m.get(ANCIEN) or refus("ETAT", f"l'ancien courant {ANCIEN} "
                                                "introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives-bundles/ introuvable")
    print(f"[état] ancien courant : {ANCIEN} (md5 "
          f"{ancien.get('md5Checksum', '')[:8]}…)")
    print(f"[état] archives-bundles/ : {len(lister(archives['id']))} archives")

    # -- 2. dépôt du NOUVEAU courant au miroir --------------------------------------
    deja = racine_m.get(bundle)
    deja_arch = lister(archives["id"]).get(bundle)
    if deja or deja_arch:
        cible = deja or deja_arch
        if cible.get("md5Checksum") != md5_local:
            refus("DEPOT", f"{bundle} existe déjà avec un md5 divergent — abandon")
        print(f"[2] {bundle} déjà présent (md5 MATCH) — idempotent")
    else:
        ds.upload_create(miroir["id"], bundle, ds.pathlib.Path(chemin_local))
        apres = lister(miroir["id"])
        f = apres.get(bundle) or refus("DEPOT", f"{bundle} absent après dépôt")
        if f.get("md5Checksum") != md5_local:
            refus("DEPOT", f"{bundle} : md5 distant ≠ local après dépôt")
        print(f"[2] déposé au miroir : {bundle} (md5 {md5_local[:8]}… MATCH "
              f"par relecture)")

    # -- 3. l'ancien ARCHIVÉ VERSIONNÉ (jamais supprimé, jamais écrasé) -------------
    deja_archives = lister(archives["id"]).get(ANCIEN)
    if deja_archives:
        if deja_archives.get("md5Checksum") != ancien.get("md5Checksum"):
            refus("ARCHIVAGE", f"{ANCIEN} : l'exemplaire archivé diverge de "
                               f"l'ancien courant")
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
            refus("ARCHIVAGE", f"{ANCIEN} RESTE à la racine du miroir — "
                               f"déplacement inopérant")
        cible = apres_archives.get(ANCIEN) or refus(
            "ARCHIVAGE", f"{ANCIEN} absent de l'archive après déplacement")
        if cible.get("md5Checksum") != ancien.get("md5Checksum"):
            refus("ARCHIVAGE", f"{ANCIEN} : md5 diverge après déplacement")
        print(f"[3] archivé versionné : {ANCIEN} → archives-bundles/ (md5 "
              f"{ancien.get('md5Checksum', '')[:8]}… recoupé — la racine ne "
              f"porte que le courant)")

    # -- 4. l'orphelin du geste parallèle discardé (le miroir == le dépôt) --------
    scripts_m = racine_m.get("scripts") or refus("ETAT", "scripts/ introuvable "
                                                  "au miroir")
    s_m = lister(scripts_m["id"])
    orphelin = s_m.get("consigner_entree_218.py")
    if orphelin:
        url = ds.API + f"/files/{orphelin['id']}"
        st, rep, _ = ds.api("PATCH", url, body={"trashed": True})
        if st not in (200, 201):
            refus("ORPHELIN", f"HTTP {st} : {rep[:150]!r}")
        if "consigner_entree_218.py" in lister(scripts_m["id"]):
            refus("ORPHELIN", "le fichier reste visible après corbeille")
        print("[4] l'orphelin consigner_entree_218.py (le geste parallèle "
              "discardé) CORBEILLÉ au miroir — le miroir dit ce que le dépôt dit")
    else:
        print("[4] aucun orphelin au miroir — rien à retirer")

    # -- 5. aucun bundle parasite au /test (recoupé, rien à retirer) ----------------
    test = coffre.get("test")
    if test:
        copies = [n for n in lister(test["id"]) if n.endswith(".bundle")]
        if copies:
            refus("TEST", f"copie(s) de bundle au /test : {copies}")
        print("[5] /test ne porte AUCUNE copie de bundle — rien à retirer (recoupé)")

    # -- 6. l'état FINAL (recoupement) ----------------------------------------------
    final = lister(miroir["id"])
    courants = sorted(n for n in final
                      if n.startswith("triade-history-0") and n.endswith(".bundle"))
    print(f"[état] courant au miroir : {courants}")
    if courants != [bundle]:
        refus("ETAT-FINAL", f"la racine du miroir ne porte pas LE courant "
                            f"unique : {courants}")
    if ANCIEN not in lister(archives["id"]):
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives — D141 violée")
    print("[passation] D141 TERMINÉE — le bundle courant porte LA FINALE "
          f"`loupe 0.1.0` DU JALON M10 ({tip_court} : le onzième run recoupé "
          "39/39 + la dette soldée + la balise scellée l'artefact intact + "
          "la clôture complète), l'ancien vit aux archives, LA SÉRIE 090 "
          "POURSUIT, rien n'a été supprimé")


if __name__ == "__main__":
    main()
