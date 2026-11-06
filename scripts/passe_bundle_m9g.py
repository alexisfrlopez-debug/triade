#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9g.py — LA PASSATION du bundle au geste « LE CHANTIER
M9-(d) : LE SOCLE SOCKET sys-04..06 NOTÉS-MESURÉS-PROUVÉS » :
LA SÉRIE 090 POURSUIT À LA POINTE 686b33e.
  1. le bundle triade-history-090-686b33e.bundle (git bundle --all, pointe =
     LE commit du geste : LE SOCLE SOCKET noté-mesuré-prouvé [sys-04..06,
     Entrée 176 : la notation 676/289/287 o ARRÊTÉE D161-rejoué, le noyau
     AFD STRICT du harnais — 131 contrôles · 131 VERTS × 3 graines, 19
     mutantes trahies, l'erratum de notation n° 3 (le DesiredAccess
     ZÉRO-étendu, attrapé par le round-trip AVANT le noyau) consigné sur
     pièces, l'instrument verifier_specs_m9d.py révisé phases 1+2 :
     116 VERTS] + le worklog Task 94) est déposé au MIROIR
     (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-514f42b.bundle (LA FAMILLE
     poignée + LE PRINCIPAL, Entrée 175, Task 93) est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ;
  4. le push GitHub porte la pointe (D164 : la reprise confronte les trois
     miroirs — GitHub D'ABORD).

Usage : python3 scripts/passe_bundle_m9g.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-090-686b33e.bundle"      # le courant NOUVEAU (le socle socket)
ANCIEN = "triade-history-090-514f42b.bundle"      # le courant actuel au miroir (la poignée + le principal)
TIP_ATTENDU = "686b33e4e5512e0ad80fe5eefdbd34509b96f698"
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
    print(f"[0] bundle construit : {BUNDLE} ({len(octets)} o, md5 {md5_local[:8]}… — "
          f"branche jalon == {TIP_ATTENDU[:7]} (LE SOCLE SOCKET "
          "sys-04..06 NOTÉ-MESURÉ-PROUVÉ + sa consignation)")
    temoin = open(REPO + "/m8/notation/sys-04-transport.asm", "rb").read()
    if not temoin:
        refus("BUNDLE-CONTENU", "m8/notation/sys-04-transport.asm vide — "
              "le bundle ne porterait pas le geste")

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
              f"que le courant ; LA FAMILLE poignée + LE PRINCIPAL demeure dans l'histoire)")

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
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives après la passation")

    # -- 6. le push GitHub à la pointe (D164 : GitHub D'ABORD) ----------------------
    push = subprocess.run(["git", "push", "origin", "bundle051/v0.5.1-jalon-v7"],
                          cwd=REPO, capture_output=True, text=True)
    if push.returncode != 0:
        refus("PUSH", (push.stderr or push.stdout)[:200])
    apres = subprocess.run(["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
                           cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == {TIP_ATTENDU[:7]} "
          f"(relu MATCH — les trois miroirs à la pointe)")

    print("=== PASSATION FAITE : le bundle courant porte LE SOCLE SOCKET "
          "sys-04..06 NOTÉ-MESURÉ-PROUVÉ (686b33e) — la série 090 poursuit "
          "à la pointe ; l'ancien 514f42b (LA FAMILLE poignée + LE PRINCIPAL) "
          "ARCHIVÉ VERSIONNÉ ; GitHub à la pointe ; le geste est PASSÉ ===")
    return 0


if __name__ == "__main__":
    main()
