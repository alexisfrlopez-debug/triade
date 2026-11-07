#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9y.py — LA PASSATION du bundle au geste « LA TROISIÈME
SIGNATURE DE LA RÉVISION 3 REÇUE, RECROPÉE 13/13 ET INSTALLÉE (LE
GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.4 NÉ (LE DIFF CONTRÔLÉ :
TROIS octets — la version R10 + LES DEUX IMMÉDIATES DU CONTRAT
D'APPEL dans sys-06), LA CARTE GÉNÉRATION 12 ; LE KIT M9F RÉPARÉ
LIVRÉ AU COFFRE — LE SEPTIÈME RUN ATTENDU » : LA SÉRIE 090 POURSUIT
À LA POINTE COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : LE RECOUP 13/13 [Entrée 192 — la
     troisième signature reçue, recoupée et installée, le garde
     13/13 VERTS] + LE REBUILD dev.4 [le diff contrôlé TROIS octets]
     + LE KIT M9F RÉPARÉ [md5 92098687…] + le worklog Task 110) est
     déposé au MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là,
     D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. /test : AUCUNE copie de bundle n'y vit (recoupé) ; le kit-m9f.zip
     du /test porte le md5 RÉPARÉ (92098687… — le build 1.0.0-dev.4,
     le contrat d'appel réparé) ; la sonde sys-05 demeure l'ACQUITTÉ
     (215c2caa…) ; la sonde sys-06 demeure (67e2014d…) avec le
     réceptacle preuves-sonde-sys06/ ré-armé et l'archive
     preuves-sonde-sys06-1/ (le QUATUOR + le verdict 17/17) ; le
     réceptacle preuves-m9f/ RÉ-ARMÉ (le SEPTIÈME run attendu — le
     premier du contrat réparé) ; les pièces de cérémonie demeurent
     (la TROISIÈME remise 0978c117… INSTALLÉE + l'ancre 188a7d42…) ;
  4. le push GitHub porte la pointe (D164 : GitHub D'ABORD) ; si le
     refus de sortie REVENAIT : le refus est NOMMÉ, le miroir Drive
     porte TOUT (D141), la passation rend 2 SANS rien défaire.

Usage : python3 scripts/passe_bundle_m9y.py
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

KIT_M9F_MD5 = "9209868796330fab0ea3f01b4879eb80"     # le kit RÉPARÉ (dev.4) au /test
KIT_SONDE05_MD5 = "215c2caa54332ce91b03fd55c335513b"  # kit-sonde-sys05.zip
KIT_SONDE06_MD5 = "67e2014d5a5725d19bcabce548d2475e"  # kit-sonde-sys06.zip
SIGNATURES_MD5 = "0978c117af62730508d60211f869bdf6"  # la TROISIÈME remise installée
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"         # la clé ancre des ères

LIGNE_M8 = ("m8 sys.1 "
            "e36141f75ebd8e615c53ff1bd59a4f4cee45b9397eefa66773ffbf54580b"
            "3536")
SHA_ARTEFACT = ("446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453d"
                "b3b00d93d")
SIG_M8_INSTALLEE = ("1a0cd42d6d303eec8ed7c61cd3705c83fc1d961011ac88f34b0d5"
                    "f4f120d875714e14afaaade87328c49b2d37492a7f52f8fb1075ce"
                    "84c2a4fad720462031704")

QUATUOR_RUN1 = ["journal-emissions.txt",
                "VERDICT-recoup-labo-sonde-sys06-1.txt",
                "VERDICT-sonde-sys06.txt",
                "sonde-sys06-journal.log",
                "temoin-sonde-sys06.txt"]


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
          f"{md5_local[:8]}… — branche jalon == {TIP_ATTENDU[:7]} (LA "
          "TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE ET INSTALLÉE, LE "
          "REBUILD dev.4, LE KIT M9F RÉPARÉ)")

    # le bundle porte LE GESTE : les consignations relues dans l'arbre -----
    journal = montrer("docs/JOURNAL_TRAVAIL.md")
    if ("## Entrée 192" not in journal
            or "LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" not in journal):
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas "
                                "l'Entrée 192 (la troisième signature "
                                "installée)")
    worklog = montrer("worklog.md")
    if ("## Task ID 110" not in worklog
            or "LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" not in worklog):
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 110 (la cérémonie de la révision 3)")
    for nom_script in ("rapatrier_ceremonie_revision3.py",
                       "diff_dev3_dev4.py",
                       "corriger_kit_m9f_e10.py"):
        if nom_script not in worklog:
            refus("BUNDLE-CONTENU", f"le worklog à la pointe ne nomme pas le "
                                    f"script {nom_script}")
    remise = montrer("v06/sceau-I/a-signer.txt")
    if LIGNE_M8 not in remise:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne porte pas la "
                                "ligne m8 e36141f7… (la révision 3)")
    if len([l for l in remise.splitlines() if l.strip()]) != 13:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne compte pas 13 lignes")
    sig_m8 = montrer("v06/sceau-I/signatures/m8.txt").strip()
    if sig_m8 != SIG_M8_INSTALLEE:
        refus("BUNDLE-CONTENU", "la signature m8 installée à la pointe n'est "
                                "pas celle de la TROISIÈME remise (1a0cd42d… "
                                "— la cérémonie de la révision 3)")
    etat = montrer("v06/sceau-I/etat-cle.txt").strip()
    if etat != "reelle (ceremonie hors-ligne, D87)":
        refus("BUNDLE-CONTENU", "l'état de clé à la pointe n'est pas "
                                "« reelle (ceremonie hors-ligne, D87) »")
    layout = montrer("tls13/layout.py")
    if "VERSION_DEV = 0x01000004" not in layout:
        refus("BUNDLE-CONTENU", "layout.py à la pointe ne porte pas la "
                                "version R10 0x01000004 (le dev.4 — le "
                                "rebuild de la révision 3)")
    build = montrer("tls13/build_m9.py")
    if 'sys-05:R2' not in build or 'sys-06:R3' not in build:
        refus("BUNDLE-CONTENU", "build_m9.py à la pointe ne porte pas les "
                                "contrats sys-05:R2 + sys-06:R3 (les portes "
                                "re-passées de la révision 3)")
    if "génération 12" not in build:
        refus("BUNDLE-CONTENU", "build_m9.py à la pointe ne porte pas la "
                                "génération 12 (la carte du dev.4)")
    carte = montrer("tls13/carte_m9.py")
    if 'VERSION_DEV1 = "1.0.0-dev.4"' not in carte or "GENERATION = 12" not in carte:
        refus("BUNDLE-CONTENU", "carte_m9.py à la pointe ne porte pas la "
                                "version 1.0.0-dev.4 / la génération 12")
    scenario = montrer("tls13/terrain/scenario-m9f.py")
    if SHA_ARTEFACT not in scenario:
        refus("BUNDLE-CONTENU", "le scénario à la pointe n'épingle pas "
                                "l'artefact 446279f3… (le kit réparé)")
    if "T0.erratum-10" not in scenario or "OCTETS_AFDFLAGS" not in scenario \
            or "OCTETS_TDIFLAGS" not in scenario:
        refus("BUNDLE-CONTENU", "le scénario à la pointe ne porte pas le "
                                "contrôle T0.erratum-10 (le contrat d'appel "
                                "relu dans l'image)")
    artefact = octets_de("tls13/proxy.exe")
    if hashlib.sha256(artefact).hexdigest() != SHA_ARTEFACT:
        refus("BUNDLE-CONTENU", "l'artefact à la pointe n'est pas le build "
                                "446279f3… (le rebuild dev.4)")
    for chemin in ("scripts/rapatrier_ceremonie_revision3.py",
                   "scripts/diff_dev3_dev4.py",
                   "scripts/corriger_kit_m9f_e10.py",
                   "scripts/consigner_entree192.py"):
        if not montrer(chemin):
            refus("BUNDLE-CONTENU", f"{chemin} absent de l'arbre à la pointe")
    plan = montrer("docs/PLAN_MILESTONES.md")
    if "LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" not in plan:
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(f) du geste (la troisième signature "
                                "installée)")
    print("[0] le bundle porte LE GESTE : Entrée 192 (la troisième signature "
          "recoupée 13/13 et installée — le garde 13/13 VERTS) + worklog "
          "Task 110 + LE REBUILD 1.0.0-dev.4 (BLOCS_SOCLE sys-06:R3, la "
          "version R10 0x01000004, GENERATION 12, l'artefact 446279f3…) + "
          "LE KIT M9F RÉPARÉ (le T0.erratum-10, l'assembleur 32 constantes) "
          "+ la signature m8 installée (1a0cd42d…, l'état de clé « reelle ») "
          "+ les scripts du geste (rapatrier, diff, livrer, consigner 192) + "
          "le plan (rangée (f) + État)")

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

    # -- 4. /test : aucune copie de bundle + les kits + les pièces + l'archive ------
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
        kit_s05 = racine_t.get("kit-sonde-sys05.zip") or {}
        if kit_s05.get("md5Checksum") != KIT_SONDE05_MD5:
            refus("TEST", f"kit-sonde-sys05.zip au /test ne porte pas le md5 "
                          f"livré ({kit_s05.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {KIT_SONDE05_MD5[:8]}…)")
        kit_s06 = racine_t.get("kit-sonde-sys06.zip") or {}
        if kit_s06.get("md5Checksum") != KIT_SONDE06_MD5:
            refus("TEST", f"kit-sonde-sys06.zip au /test ne porte pas le md5 "
                          f"livré ({kit_s06.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {KIT_SONDE06_MD5[:8]}…)")
        if "LISEZMOI-sonde-sys06.txt" not in racine_t \
                or "preuves-sonde-sys06" not in racine_t:
            refus("TEST", "LA SONDE SYS-06 est incomplète au /test (le "
                          "LISEZMOI ou le réceptacle preuves-sonde-sys06/ "
                          "absent)")
        sig = racine_t.get("signatures-I.txt") or {}
        if sig.get("md5Checksum") != SIGNATURES_MD5:
            refus("TEST", "signatures-I.txt au /test ne porte pas le md5 de la "
                          f"TROISIÈME remise ({sig.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {SIGNATURES_MD5[:8]}…)")
        cle = racine_t.get("cle-publique-I.txt") or {}
        if cle.get("md5Checksum") != CLE_MD5:
            refus("TEST", "cle-publique-I.txt au /test diverge de LA clé ancre "
                          f"({cle.get('md5Checksum', 'ABSENT')[:8]}… != "
                          f"{CLE_MD5[:8]}…)")
        psonde = racine_t.get("preuves-sonde-sys06") or {}
        restants = sorted(lister(psonde["id"])) if psonde.get("id") else ["(ABSENT)"]
        if restants != ["LISEZMOI-preuves.txt"]:
            refus("TEST", f"preuves-sonde-sys06/ n'est pas ré-armé (son "
                          f"LISEZMOI seul attendu) : {restants}")
        arch_p = racine_t.get("archives-preuves") or {}
        run_s1 = lister(arch_p["id"]).get("preuves-sonde-sys06-1") if arch_p.get("id") else None
        if not run_s1:
            refus("TEST", "preuves-sonde-sys06-1/ absent de archives-preuves/ "
                          "(l'archivage du geste n'est pas passé)")
        dans_run1 = sorted(lister(run_s1["id"]))
        if dans_run1 != sorted(QUATUOR_RUN1):
            refus("TEST", f"preuves-sonde-sys06-1/ ne porte pas les CINQ pièces "
                          f"attendues : {dans_run1}")
        pm9 = racine_t.get("preuves-m9f") or {}
        restants_m9f = sorted(lister(pm9["id"])) if pm9.get("id") else ["(ABSENT)"]
        if restants_m9f != ["LISEZMOI-preuves.txt"]:
            refus("TEST", f"preuves-m9f/ n'est pas RÉ-ARMÉ (son LISEZMOI seul "
                          f"attendu — le réceptacle du SEPTIÈME run) : "
                          f"{restants_m9f}")
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; kit-m9f.zip == "
              f"le RÉPARÉ md5 {KIT_M9F_MD5[:8]}… (le build 1.0.0-dev.4, le "
              "contrat d'appel réparé) + la sonde sys-05 == l'acquis "
              f"{KIT_SONDE05_MD5[:8]}… + la sonde sys-06 == le livré "
              f"{KIT_SONDE06_MD5[:8]}… AVEC le réceptacle "
              "preuves-sonde-sys06/ ré-armé et l'archive "
              "preuves-sonde-sys06-1/ (le QUATUOR + LE VERDICT 17/17) ; le "
              "réceptacle preuves-m9f/ RÉ-ARMÉ (le SEPTIÈME run — le premier "
              "du contrat réparé) ; les PIÈCES DE CÉRÉMONIE demeurent "
              f"(signatures-I.txt {SIGNATURES_MD5[:8]}… la TROISIÈME remise "
              f"INSTALLÉE + cle-publique-I.txt {CLE_MD5[:8]}… l'ancre des "
              "ères)")

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
              f"TROISIÈME SIGNATURE DE LA RÉVISION 3 INSTALLÉE ({TIP_ATTENDU[:7]}) — "
              "la série 090 poursuit ; GitHub en retard NOMMÉ, LE "
              "SEPTIÈME RUN EST ATTENDU ===")
        return 2
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe ; "
          "le flux tenu)")

    print("=== PASSATION FAITE : le bundle courant porte LA TROISIÈME "
          "SIGNATURE DE LA RÉVISION 3 REÇUE, RECROPÉE 13/13 ET INSTALLÉE "
          "(LE GARDE 13/13 VERTS — la dette de cérémonie de la révision 3 "
          "SOLDÉE) + LE REBUILD 1.0.0-dev.4 (LE DIFF CONTRÔLÉ : TROIS "
          "octets — la version R10 + LES DEUX IMMÉDIATES DU CONTRAT "
          "D'APPEL dans sys-06) + LA CARTE GÉNÉRATION 12 + LE KIT M9F "
          "RÉPARÉ LIVRÉ AU COFFRE (md5 92098687…) — la série 090 poursuit "
          f"à la pointe ({TIP_ATTENDU[:7]}) ; l'ancien courant demeure dans "
          "l'histoire ; LE SEPTIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le "
          "premier du contrat réparé : kit-m9f.zip au /test, un dossier "
          "NEUF D99, python scenario-m9f.py — réseau vivant — renvoyer "
          "preuves-m9f/ ENTIER au coffre /test) — ET SI LE VERT TIENT : "
          "LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
