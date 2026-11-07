#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9u.py — LA PASSATION du bundle au geste « LA SECONDE
SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE, RECROPÉE 13/13 ET INSTALLÉE
(LE GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.3 NÉ SUR L'INSTRUMENT
RÉVISÉ (LE DIFF CONTRÔLÉ : TROIS octets — la version R10 + LES DEUX
POSES DU WSABUF 0x64 → 0x68), LA CARTE GÉNÉRATION 11 ; LE KIT M9F
RÉPARÉ LIVRÉ AU COFFRE /test » : LA SÉRIE 090 POURSUIT À LA POINTE
COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : LA SECONDE SIGNATURE INSTALLÉE + LE
     REBUILD dev.3 + LE KIT RÉPARÉ [Entrée 188 — la remise recoupée
     13/13, la preuve D163 rejointe une quatrième fois, le garde 13/13
     verts ; les portes re-passées sys-05:R2 + sys-06:R2, l'artefact
     de23e577…, le diff contrôlé TROIS octets, la carte génération 11,
     le kit md5 79d44284… livré] + le worklog Task 106) est déposé au
     MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ;
     le kit-m9f.zip du /test porte le md5 RÉPARÉ (79d44284…) ; le kit
     sonde demeure l'ACQUITTÉ (215c2caa…) ; les pièces de cérémonie
     demeurent (signatures-I.txt 503f3822… la seconde remise + la clé
     ancre 188a7d42…) ;
  4. le push GitHub porte la pointe (D164 : GitHub D'ABORD ; le commit
     EMBARQUE le commit de passation 551eac9 du geste précédent, le
     flux établi) ; si le refus de sortie REVENAIT : le refus est
     NOMMÉ, le miroir Drive porte TOUT (D141), la passation rend 2
     SANS rien défaire.

Usage : python3 scripts/passe_bundle_m9u.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import pathlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = None
ANCIEN = None
TIP_ATTENDU = None
CHEMIN_LOCAL = None

KIT_M9F_MD5 = "79d44284c70261375a2b055070fda223"     # le kit RÉPARÉ au /test
KIT_SONDE_MD5 = "215c2caa54332ce91b03fd55c335513b"   # kit-sonde-sys05.zip
SIGNATURES_MD5 = "503f382229b4da0ddd43e833d31b2c2b"  # la SECONDE remise
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"         # la clé ancre des ères

LIGNE_M8 = ("m8 sys.1 "
            "c444d73059af33ce0d61bf48ce8ac976d1e86a566574dcb4ef63a771f7b1875a")
SHA_ARTEFACT = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
                "66b29226f")


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def montrer(chemin_git):
    return subprocess.run(["git", "show", f"{TIP_ATTENDU}:{chemin_git}"],
                          cwd=REPO, capture_output=True, text=True).stdout


def octets_de(chemin_git):
    return subprocess.run(["git", "show", f"{TIP_ATTENDU}:{chemin_git}"],
                          cwd=REPO, capture_output=True).stdout


def main():
    global BUNDLE, TIP_ATTENDU, CHEMIN_LOCAL, ANCIEN
    # -- 0. la pointe courante : le geste + ses consignations -------------------
    TIP_ATTENDU = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                                 capture_output=True, text=True).stdout.strip()
    BUNDLE = f"triade-history-090-{TIP_ATTENDU[:7]}.bundle"
    CHEMIN_LOCAL = REPO + "/bundles-090/" + BUNDLE
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
        refus("BUNDLE-TETES", "la branche jalon du bundle ne pointe pas sur "
                              f"la pointe courante : {ligne_jalon[:80]!r}")
    octets = open(CHEMIN_LOCAL, "rb").read()
    md5_local = hashlib.md5(octets).hexdigest()
    print(f"[0] bundle construit : {BUNDLE} ({len(octets)} o, md5 "
          f"{md5_local[:8]}… — branche jalon == {TIP_ATTENDU[:7]} (LA SECONDE "
          "SIGNATURE INSTALLÉE + LE REBUILD dev.3 + LE KIT RÉPARÉ)")

    # le bundle porte LE GESTE : les consignations relues dans l'arbre -----
    journal = montrer("docs/JOURNAL_TRAVAIL.md")
    if "## Entrée 188" not in journal or "LE REBUILD 1.0.0-dev.3 NÉ" not in journal:
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas "
                                "l'Entrée 188 (la seconde signature + le rebuild)")
    worklog = montrer("worklog.md")
    if "## Task ID 106" not in worklog or "de23e577" not in worklog:
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 106 (le rebuild de23e577…)")
    remise = montrer("v06/sceau-I/a-signer.txt")
    if LIGNE_M8 not in remise:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne porte pas la "
                                "ligne m8 c444d730… (la révision 2 étendue)")
    if len([l for l in remise.splitlines() if l.strip()]) != 13:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne compte pas 13 lignes")
    layout = montrer("tls13/layout.py")
    if "VERSION_DEV = 0x01000003" not in layout:
        refus("BUNDLE-CONTENU", "layout.py à la pointe ne porte pas la "
                                "version R10 0x01000003 (le dev.3)")
    build = montrer("tls13/build_m9.py")
    if 'sys-05:R2' not in build or 'sys-06:R2' not in build:
        refus("BUNDLE-CONTENU", "build_m9.py à la pointe ne porte pas les "
                                "contrats révisés sys-05:R2 + sys-06:R2 "
                                "(les portes de l'assemblage)")
    scenario = montrer("tls13/terrain/scenario-m9f.py")
    if SHA_ARTEFACT not in scenario:
        refus("BUNDLE-CONTENU", "le scénario à la pointe n'épingle pas "
                                "l'artefact de23e577… (le kit réparé)")
    if "T0.erratum-9" not in scenario or "OCTETS_POSE_WSABUF" not in scenario:
        refus("BUNDLE-CONTENU", "le scénario à la pointe ne porte pas le "
                                "contrôle T0.erratum-9 (la pose relue dans "
                                "l'image)")
    lis_kit = montrer("tls13/terrain/LISEZMOI-KIT-M9F.md")
    if "L'ERRATUM n° 9 + LA RÉVISION 2 ÉTENDUE" not in lis_kit:
        refus("BUNDLE-CONTENU", "le LISEZMOI du kit à la pointe ne porte pas "
                                "la section erratum n° 9 (la révision 2)")
    artefact = octets_de("tls13/proxy.exe")
    if hashlib.sha256(artefact).hexdigest() != SHA_ARTEFACT:
        refus("BUNDLE-CONTENU", "l'artefact à la pointe n'est pas le build "
                                "de23e577… (le rebuild dev.3)")
    plan = montrer("docs/PLAN_MILESTONES.md")
    if ("LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE"
            not in plan):
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(f) du geste")
    print("[0] le bundle porte LE GESTE : Entrée 188 (la seconde signature "
          "recoupée 13/13, installée — le garde 13/13 verts) + worklog Task "
          "106 + LA REMISE m8 c444d730… + la version R10 0x01000003 + les "
          "portes sys-05:R2/sys-06:R2 + le scénario épinglé de23e577… (le "
          "T0.erratum-9) + le LISEZMOI du kit + L'ARTEFACT de23e577… "
          "(l'empreinte constatée dans l'arbre) + le plan (rangée (f) + "
          "État)")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ANCIEN = next((n for n in sorted(racine_m)
                   if n.startswith("triade-history-090-")
                   and n.endswith(".bundle") and n != BUNDLE), None)
    if ANCIEN:
        ancien = racine_m.get(ANCIEN) or refus("ETAT", f"l'ancien courant {ANCIEN} "
                                                       "introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives-bundles/ "
                                                                 "introuvable")
    deja = racine_m.get(BUNDLE)
    deja_arch = lister(archives["id"]).get(BUNDLE)
    if ANCIEN:
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
    if not ANCIEN:
        print("[3] aucun ancien courant à archiver — idempotent")
    else:
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
                  f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — "
                  f"{len(apres_archives)} archives, rien supprimé)")

    # -- 4. /test : aucune copie de bundle + le kit réparé + les pièces -------------
    test = coffre.get("test")
    if test:
        racine_t = lister(test["id"])
        copies = [n for n in racine_t if n.endswith(".bundle")]
        if copies:
            refus("TEST", f"copie(s) de bundle au /test (à traiter avant "
                          f"clôture) : {copies}")
        kit = racine_t.get("kit-m9f.zip") or {}
        if kit.get("md5Checksum") != KIT_M9F_MD5:
            refus("TEST", f"kit-m9f.zip au /test ne porte pas le md5 RÉPARÉ "
                          f"({kit.get('md5Checksum', 'ABSENT')[:8]}… != "
                          f"{KIT_M9F_MD5[:8]}…)")
        kit_sonde = racine_t.get("kit-sonde-sys05.zip") or {}
        if kit_sonde.get("md5Checksum") != KIT_SONDE_MD5:
            refus("TEST", f"kit-sonde-sys05.zip au /test ne porte pas le md5 "
                          f"livré ({kit_sonde.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {KIT_SONDE_MD5[:8]}…)")
        sig = racine_t.get("signatures-I.txt") or {}
        if sig.get("md5Checksum") != SIGNATURES_MD5:
            refus("TEST", "signatures-I.txt au /test ne porte pas le md5 de la "
                          f"SECONDE remise ({sig.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {SIGNATURES_MD5[:8]}… — le dossier du geste reçu)")
        cle = racine_t.get("cle-publique-I.txt") or {}
        if cle.get("md5Checksum") != CLE_MD5:
            refus("TEST", "cle-publique-I.txt au /test diverge de LA clé ancre "
                          f"({cle.get('md5Checksum', 'ABSENT')[:8]}… != "
                          f"{CLE_MD5[:8]}…)")
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; kit-m9f.zip == "
              f"le RÉPARÉ md5 {KIT_M9F_MD5[:8]}… + kit-sonde-sys05.zip == le "
              f"livré {KIT_SONDE_MD5[:8]}… (recoupés) ; les PIÈCES DE "
              f"CÉRÉMONIE demeurent (signatures-I.txt {SIGNATURES_MD5[:8]}… la "
              f"seconde remise installée + cle-publique-I.txt {CLE_MD5[:8]}… "
              f"l'ancre)")

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
    if ANCIEN and ANCIEN not in archives_finales:
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives après la passation")

    # -- 6. le push GitHub à la pointe (D164 : GitHub D'ABORD) ----------------------
    push = subprocess.run(["git", "push", "origin", "bundle051/v0.5.1-jalon-v7"],
                          cwd=REPO, capture_output=True, text=True)
    if push.returncode != 0 and "up to date" not in (push.stderr or ""):
        print(f"[6] LE PUSH GITHUB EST REFUSÉ NOMMÉ : "
              f"{(push.stderr or push.stdout).strip()[:200]} — le labo NE "
              "CONTOURNE PAS le refus : le miroir Drive porte TOUT (D141), "
              "le push sera re-tenté au geste suivant — ou poussé par le "
              "développeur depuis sa machine (git push origin "
              "bundle051/v0.5.1-jalon-v7 : le dépôt local == le miroir == "
              "le bundle)")
        print("=== PASSATION FAITE AU MIROIR : le bundle courant porte LA "
              f"SECONDE SIGNATURE INSTALLÉE + LE REBUILD dev.3 + LE KIT "
              f"RÉPARÉ ({TIP_ATTENDU[:7]}) — la série 090 poursuit ; GitHub "
              "en retard NOMMÉ, LE CINQUIÈME RUN DU DÉVELOPPEUR (le premier "
              "du build réparé) EST ATTENDU ===")
        return 2
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe ; "
          "le commit de passation 551eac9 du geste précédent EMBARQUÉ, le "
          "flux tenu)")

    print("=== PASSATION FAITE : le bundle courant porte LA SECONDE "
          "SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE ET INSTALLÉE (le garde "
          "13/13 verts) + LE REBUILD 1.0.0-dev.3 (l'artefact de23e577…, le "
          f"diff contrôlé TROIS octets, la carte génération 11) + LE KIT "
          f"M9F RÉPARÉ livré au /test ({TIP_ATTENDU[:7]}) — la série 090 "
          "poursuit à la pointe ; l'ancien courant demeure dans l'histoire ; "
          "LE CINQUIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le premier du build "
          "réparé : dézipper kit-m9f.zip dans un dossier NEUF D99, python "
          "scenario-m9f.py, renvoyer preuves-m9f/ ENTIER au coffre) — ET SI "
          "LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE "
          "===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
