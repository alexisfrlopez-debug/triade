#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m7c.py — LA PASSATION D141 DU BUNDLE au geste
« chantier M7-(c) accompli — le patch fence.i démontré en exécution + le
verrou multi-profils + le scellage 0.8.0-rc.1 » (D157) :
  1. le bundle triade-history-070-33cde07.bundle (git bundle --all, pointe =
     LE commit du geste : LE DÉMONSTRATEUR INVITÉ riscv/demo [f72001, 191
     instructions à 0x2000 dans la réserve RX, les MÊMES blocs du corpus —
     unix/demo_patch.py PORTÉ EN INVITÉ] : LA BASCULE PENDANT LE TRAFIC
     [1200 usages de l'ENTRÉE, apply ENTRE 399/400, rollback ENTRE 799/800,
     transcription byte-exact 15 425 o, 800 v1 + 400 v2, l'effet au geste
     même, le retour à l'état image, les refus 1-4 (IN-GUEST), le DEP
     SIGSEGV 4 290 o exacts, la falsification, les bases forcées, zéro
     régression] + LA CORRECTION tcp-07 [le PORT avait OUBLIÉ le
     marshalling du prot — mv a2, t2, la pièce par QEMU_STRACE ; le corpus
     REBUILDÉ sha ec343b4e…] + LE VERROU CROISÉ MULTI-PROFILS [26
     empreintes DEUX ISA avant l'édition] + LE CONTRÔLE D146 ADAPTÉ [base
     PAR TRACE 0x555555556000 ×6 + 3 forçages] + LA CONFORMITÉ 7/7 [29
     contrôles] + LA CRISTALLISATION 10/10 + LA BALISE 0.8.0-rc.1 SCELLÉE +
     les TROIS gardes vivantes + Entrée 153 + D157 + worklog Task 71) est
     déposé au MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-070-09ddd06.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé — D141) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé).

La cadence « une passation par geste de jalon » est tenue (leçon D141 :
aucune dette n'accumule) : le bundle courant porte désormais LE TROISIÈME
CHANTIER DU JALON M7 avec sa consignation. La série DEMEURE 070 (l'ère de
la balise 0.7.0 scellée) : la série 080 naîtra à la finale 0.8.0 du jalon.

Chaque geste ASSERTÉ ; md5 recoupés AVANT tout déplacement ; idempotent par
saut d'already-fait. Déplacement : addParents/removeParents EN PARAMÈTRES DE
REQUÊTE (leçon v7/D143).

Usage : python3 scripts/passe_bundle_m7c.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-070-33cde07.bundle"      # le courant NOUVEAU (chantier M7-(c), D157)
ANCIEN = "triade-history-070-09ddd06.bundle"      # le courant actuel au miroir (chantier M7-(b), D156)
TIP_ATTENDU = "33cde0778d3d50580bd409d31d5be66cc26fddf1"   # la pointe du geste (push recoupé)
CHEMIN_LOCAL = REPO + "/bundles-070/" + BUNDLE


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def main():
    # -- 0. le bundle local, construit et vérifié --------------------------------
    subprocess.run(["mkdir", "-p", REPO + "/bundles-070"], check=True)
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
          f"branche jalon == {TIP_ATTENDU[:7]} (le chantier M7-(c) accompli avec sa consignation)")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ancien = racine_m.get(ANCIEN) or refus("ETAT", f"l'ancien courant {ANCIEN} introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives-bundles/ introuvable")
    deja = racine_m.get(BUNDLE)
    deja_arch = lister(archives["id"]).get(BUNDLE)
    print(f"[état] ancien courant : {ANCIEN} (md5 {ancien.get('md5Checksum', '')[:8]}…)")

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
              f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — la racine ne porte que le courant)")

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
    print(f"[état] archives-bundles/ ({len(archives_finales)}) : {archives_finales}")
    if courants != [BUNDLE]:
        refus("ETAT-FINAL", f"la racine du miroir ne porte pas LE courant unique : {courants}")
    if ANCIEN not in archives_finales:
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives — D141 violée")
    print("[passation] D141 TERMINÉE — le bundle courant porte le CHANTIER M7-(c) "
          "ACCOMPLI (33cde07 : le patch fence.i démontré en exécution + le "
          "verrou multi-profils + la correction tcp-07 + la 0.8.0-rc.1 "
          "scellée + Entrée 153 + D157), l'ancien vit aux archives, rien "
          "n'a été supprimé")


if __name__ == "__main__":
    main()
