#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9k.py — LA PASSATION du bundle au geste « L'ERRATUM n° 5
NOMMÉ AVANT LE KIT ET RÉPARÉ À LA SOURCE ; LE BUILD 1.0.0-dev.2 NÉ ; LE
KIT TERRAIN M9-(f) DÉPOSÉ AU COFFRE /test » : LA SÉRIE 090 POURSUIT À LA
POINTE b3fe063.
  1. le bundle triade-history-090-b3fe063.bundle (git bundle --all, pointe =
     LE commit du geste : LE KIT DÉPOSÉ [Entrée 179 — l'erratum n° 5 : la
     sonde terrain du labo a nommé l'octet de longueur du record CH
     0x76 → 0x72 (le vol de dev.1 recevait le SILENCE de google/github/
     cloudflare/debian TOUS, preuve sur pièces), LE CCS hérité (RFC 8446
     § 4.1.3 : ignoré, un faux CCS = le refus -2), les verdicts internes
     64 bits — réparés À LA SOURCE, les arbres I INTACTS hors sceau, le
     garde 13/13 re-passé ; le build 1.0.0-dev.2 NÉ : tls13/proxy.exe
     65 024 o, sha256 d8928934…, DÉTERMINISTE, la carte GÉNÉRATION 10, le
     verrou croisé 86/86, le harnais 54/54 × 3 graines ; le kit
     scenario-m9f.py + LISEZMOI-KIT-M9F.md, 26 constantes recoupées PAR
     AST, kit-m9f.zip DÉPOSÉ au coffre /test (md5 a73fb526… MATCH relu),
     preuves-m9f/ NÉ, la cible figée www.cloudflare.com + l'empreinte
     épinglée 045d0758…] + le worklog Task 97) est déposé au MIROIR
     (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-3fa7168.bundle (LE BUILD NÉ,
     Entrée 178, Task 96) est ARCHIVÉ VERSIONNÉ dans archives-bundles/
     (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ;
  4. le push GitHub porte la pointe (D164 : la reprise confronte les trois
     miroirs — GitHub D'ABORD).

Usage : python3 scripts/passe_bundle_m9k.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-090-b3fe063.bundle"      # le courant NOUVEAU (le kit déposé)
ANCIEN = "triade-history-090-3fa7168.bundle"      # le courant au miroir (le build né)
TIP_ATTENDU = "b3fe063fa943553656ad5426dcaaa21ebbcb228d"
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
          f"branche jalon == {TIP_ATTENDU[:7]} (LE KIT DÉPOSÉ + sa consignation)")
    # le bundle porte LE GESTE : les consignations relues dans l'arbre
    journal = subprocess.run(["git", "show", f"{TIP_ATTENDU}:docs/JOURNAL_TRAVAIL.md"],
                             cwd=REPO, capture_output=True, text=True).stdout
    if "## Entrée 179" not in journal or "d892893469608fd69e381b92" not in journal:
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas l'Entrée 179 "
                                "(le sha de l'artefact dev.2 d8928934…)")
    worklog = subprocess.run(["git", "show", f"{TIP_ATTENDU}:worklog.md"],
                             cwd=REPO, capture_output=True, text=True).stdout
    if "## Task ID 97" not in worklog or "045d0758" not in worklog:
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la Task ID 97 "
                                "(l'empreinte épinglée)")
    scenario = subprocess.run(
        ["git", "show", f"{TIP_ATTENDU}:tls13/terrain/scenario-m9f.py"],
        cwd=REPO, capture_output=True, text=True).stdout
    if "EMPREINTE_EPINGLEE" not in scenario \
            or "a73fb526" not in worklog and "a73fb526" not in journal:
        refus("BUNDLE-CONTENU", "le scénario du kit absent de la pointe")
    print("[0] le bundle porte LE GESTE : Entrée 179 (le sha d8928934…) + "
          "worklog Task 97 + le scénario m9f + l'empreinte 045d0758…")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ancien = racine_m.get(ANCIEN) or refus("ETAT", f"l'ancien courant {ANCIEN} "
                                                   "introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives-bundles/ "
                                                                 "introuvable")
    deja = racine_m.get(BUNDLE)
    deja_arch = lister(archives["id"]).get(BUNDLE)
    print(f"[état] ancien courant : {ANCIEN} "
          f"(md5 {ancien.get('md5Checksum', '')[:8]}…)")
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
        print(f"[2] déposé au miroir : {BUNDLE} "
              f"(md5 {md5_local[:8]}… MATCH par relecture)")

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
                               "déplacement inopérant")
        cible = apres_archives.get(ANCIEN) or \
            refus("ARCHIVAGE", f"{ANCIEN} absent de l'archive après déplacement")
        if cible.get("md5Checksum") != ancien.get("md5Checksum"):
            refus("ARCHIVAGE", f"{ANCIEN} : md5 diverge après déplacement")
        print(f"[3] archivé versionné : {ANCIEN} → archives-bundles/ "
              f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — la racine "
              f"ne porte que le courant ; LE BUILD NÉ demeure dans l'histoire)")

    # -- 4. aucun bundle parasite au /test (recoupé, rien à retirer) ----------------
    test = coffre.get("test")
    if test:
        copies = [n for n in lister(test["id"]) if n.endswith(".bundle")]
        if copies:
            refus("TEST", f"copie(s) de bundle au /test (à traiter avant "
                          f"clôture) : {copies}")
        print("[4] /test ne porte AUCUNE copie de bundle — rien à retirer "
              "(recoupé)")

    # -- 5. l'état FINAL (recoupement) ----------------------------------------------
    final = lister(miroir["id"])
    courants = sorted(n for n in final
                      if n.startswith("triade-history-0") and n.endswith(".bundle"))
    archives_finales = sorted(lister(archives["id"]))
    print(f"[état] courant au miroir : {courants}")
    print(f"[état] archives-bundles/ ({len(archives_finales)})")
    if courants != [BUNDLE]:
        refus("ETAT-FINAL", f"la racine du miroir ne porte pas LE courant "
                            f"unique : {courants}")
    if ANCIEN not in archives_finales:
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives après la passation")

    # -- 6. le push GitHub à la pointe (D164 : GitHub D'ABORD) ----------------------
    push = subprocess.run(["git", "push", "origin", "bundle051/v0.5.1-jalon-v7"],
                          cwd=REPO, capture_output=True, text=True)
    if push.returncode != 0 and "up to date" not in (push.stderr or ""):
        refus("PUSH", (push.stderr or push.stdout)[:200])
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe)")

    print("=== PASSATION FAITE : le bundle courant porte LE KIT TERRAIN M9-(f) "
          "DÉPOSÉ (b3fe063) — la série 090 poursuit à la pointe ; l'ancien "
          "3fa7168 (LE BUILD NÉ) demeure dans l'histoire ; LA GRANDE ŒUVRE "
          "ATTEND LE GESTE DU DÉVELOPPEUR ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
