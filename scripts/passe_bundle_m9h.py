#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9h.py — LA PASSATION du bundle au geste « LA REPRISE SUR LES
TROIS MIROIRS : LE CHANTIER M9-(e) OUVERT — LA CÉRÉMONIE DU BUILD 1.0.0
ARMÉE » :
LA SÉRIE 090 POURSUIT À LA POINTE ae47935.
  1. le bundle triade-history-090-ae47935.bundle (git bundle --all, pointe =
     LE commit du geste : LA CÉRÉMONIE ARMÉE [Entrées 176+177 — la dette de
     consignation des Tasks 93/94 soldée : l'ordre 174<175 du journal
     restauré, l'Entrée 176 déposée, l'État du programme + les rangées (d)/(e)
     du plan complétées ; la remise fraîche 13 arbres : m8 72aadd38… (la
     révision M9-(d)) + tls13 42559862… (l'erratum n° 2), les onze autres
     inchangées ; LISEZMOI-ceremonie-build-1.0.0.txt au kit ; maj_kit ÉTENDU
     (NOTE_D130 réorientée) et REJOUÉ : 59/59 ALLER-RETOUR md5 + le recoup
     indépendant] + le worklog Task 95) est déposé au MIROIR
     (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-686b33e.bundle (LE SOCLE SOCKET,
     Entrée 176, Task 94) est ARCHIVÉ VERSIONNÉ dans archives-bundles/
     (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ;
  4. le push GitHub porte la pointe (D164 : la reprise confronte les trois
     miroirs — GitHub D'ABORD).

Usage : python3 scripts/passe_bundle_m9h.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-090-ae47935.bundle"      # le courant NOUVEAU (la cérémonie armée)
ANCIEN = "triade-history-090-686b33e.bundle"      # le courant actuel au miroir (le socle socket)
TIP_ATTENDU = "ae47935a41ee42cb4633cbc333f3821bb21322ff"
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
          f"branche jalon == {TIP_ATTENDU[:7]} (LA CÉRÉMONIE ARMÉE "
          "+ sa consignation)")
    temoin = open("/home/z/my-project/download/LISEZMOI-ceremonie-build-1.0.0.txt",
                  "rb").read()
    if not temoin:
        refus("BUNDLE-CONTENU", "download/LISEZMOI-ceremonie-build-1.0.0.txt vide — "
              "le kit ne porterait pas le geste")
    remise = open(REPO + "/v06/sceau-I/a-signer.txt", "r", encoding="utf-8").read()
    if "72aadd38" not in remise or "42559862" not in remise or len(remise.splitlines()) != 13:
        refus("BUNDLE-CONTENU", "a-signer.txt ne porte pas la remise fraîche "
              "(13 arbres, m8 72aadd38… + tls13 42559862…)")

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
              f"que le courant ; LE SOCLE SOCKET demeure dans l'histoire)")

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

    print("=== PASSATION FAITE : le bundle courant porte LA CÉRÉMONIE DU BUILD "
          "1.0.0 ARMÉE (ae47935) — la série 090 poursuit à la pointe ; "
          "l'ancien 686b33e (LE SOCLE SOCKET) ARCHIVÉ VERSIONNÉ ; GitHub à la "
          "pointe ; le geste est PASSÉ ===")
    return 0


if __name__ == "__main__":
    main()
