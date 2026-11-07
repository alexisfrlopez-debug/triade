#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9t.py — LA PASSATION du bundle au geste « LA PREMIÈRE
SIGNATURE DE LA RÉVISION 2 REÇUE, RECROPÉE 13/13 ET INSTALLÉE (LE GARDE
13/13 VERTS) ; PUIS L'ERRATUM n° 9 NOMMÉ AVANT LE KIT : SYS-06 LE MÊME
WSABUF « PACKÉ » — LA RÉVISION 2 ÉTENDUE (SPEC R2 + NOTATION + HARNAIS
RÉVISÉ, 131 · 131 VERTS × 3 graines), LA REMISE RÉGÉNÉRÉE (m8
c444d730…) » : LA SÉRIE 090 POURSUIT À LA POINTE COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : LA SIGNATURE REÇUE ET INSTALLÉE +
     L'ERRATUM n° 9 [Entrée 187 — la remise recoupée 13/13, la preuve
     D163 rejointe une troisième fois, le garde 13/13 verts ; sys-06 le
     même WSABUF, la réparation selon la charte, le harnais révisé] + le
     worklog Task 105) est déposé au MIROIR (TRIADE-sauvegarde-git/ —
     l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ; les
     DEUX kits du /test portent les md5 ACQUITTÉS (90a1d022… +
     215c2caa… — recoupés) ; les pièces de cérémonie demeurent
     (signatures-I.txt + cle-publique-I.txt : le dossier du geste reçu) ;
  4. le push GitHub porte la pointe (D164 : la reprise confronte les
     trois miroirs — GitHub D'ABORD ; le commit EMBARQUE le commit de
     passation 9854526 du geste précédent, le flux établi) ; si le refus
     de sortie REVENAIT : le refus est NOMMÉ, le miroir Drive porte
     TOUT (D141), la passation rend 2 SANS rien défaire.

Usage : python3 scripts/passe_bundle_m9t.py
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

KIT_M9F_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"     # kit-m9f.zip au /test
KIT_SONDE_MD5 = "215c2caa54332ce91b03fd55c335513b"   # kit-sonde-sys05.zip
SIGNATURES_MD5 = "af382476b050533b5be73c3ac0b49e9c"  # la remise reçue au /test
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"         # la clé publique du kit

LIGNE_M8 = ("m8 sys.1 "
            "c444d73059af33ce0d61bf48ce8ac976d1e86a566574dcb4ef63a771f7b1875a")


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def montrer(chemin_git):
    return subprocess.run(["git", "show", f"{TIP_ATTENDU}:{chemin_git}"],
                          cwd=REPO, capture_output=True, text=True).stdout


def main():
    global BUNDLE, TIP_ATTENDU, CHEMIN_LOCAL, ANCIEN
    # -- 0. la pointe courante : le geste + ses consignations -------------------
    TIP_ATTENDU = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                                 capture_output=True, text=True).stdout.strip()
    BUNDLE = f"triade-history-090-{TIP_ATTENDU[:7]}.bundle"
    CHEMIN_LOCAL = REPO + "/bundles-090/" + BUNDLE
    # le bundle local, construit et vérifié --------------------------------
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
          "SIGNATURE REÇUE ET INSTALLÉE + L'ERRATUM n° 9)")

    # le bundle porte LE GESTE : les consignations relues dans l'arbre -----
    journal = montrer("docs/JOURNAL_TRAVAIL.md")
    if "## Entrée 187" not in journal or "L'ERRATUM n° 9" not in journal:
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas "
                                "l'Entrée 187 (la signature reçue + l'erratum)")
    worklog = montrer("worklog.md")
    if "## Task ID 105" not in worklog or "c444d730" not in worklog:
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 105 (la remise régénérée m8 "
                                "c444d730…)")
    remise = montrer("v06/sceau-I/a-signer.txt")
    if LIGNE_M8 not in remise:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne porte pas la "
                                "ligne m8 c444d730… (la révision 2 étendue)")
    if remise.count(" 3e778fa0") != 0:
        refus("BUNDLE-CONTENU", "la remise à la pointe porte encore "
                                "l'empreinte périmée 3e778fa0… (erratum n° 9)")
    if len([l for l in remise.splitlines() if l.strip()]) != 13:
        refus("BUNDLE-CONTENU", f"la remise à la pointe ne compte pas 13 "
                                "lignes (rotation complète attendue)")
    spec06 = montrer("m8/I/sys-06-reception.md")
    if "révision 2" not in spec06 or "16 o + 24 o" not in spec06:
        refus("BUNDLE-CONTENU", "la spec sys-06 à la pointe n'est pas en "
                                "révision 2 (le WSABUF canonique)")
    harnais = montrer("m8/harnais_sys.py")
    if "wsabuf, 8)" not in harnais:
        refus("BUNDLE-CONTENU", "le harnais à la pointe ne lit pas buf à +8 "
                                "(l'instrument révisé)")
    if "rsp + 0x68], rdi" not in harnais:
        refus("BUNDLE-CONTENU", "les attendus V1 à la pointe ne portent pas "
                                "la pose canonique 0x68")
    maj = montrer("scripts/maj_kit.py")
    if "c444d730" not in maj:
        refus("BUNDLE-CONTENU", "maj_kit.py à la pointe ne porte pas la "
                                "re-cérémonie étendue (le NOTE_D130)")
    plan = montrer("docs/PLAN_MILESTONES.md")
    if ("LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE ET INSTALLÉE le 07/11"
            not in plan):
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(f) du geste")
    print("[0] le bundle porte LE GESTE : Entrée 187 (la signature reçue, "
          "recoupée 13/13, installée — le garde 13/13 verts ; l'erratum "
          "n° 9 nommé avant le kit) + worklog Task 105 + LA REMISE "
          "régénérée (m8 c444d730…, 13 lignes, la périmée 3e778fa0… "
          "absente) + la spec sys-06 R2 + le harnais révisé (buf à +8) + "
          "maj_kit.py (le NOTE_D130 étendu) + le plan (rangée (f) + État)")

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
                  f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — la racine "
                  f"ne porte que le courant)")

    # -- 4. /test : aucune copie de bundle + les DEUX kits + les pièces ------------
    test = coffre.get("test")
    if test:
        racine_t = lister(test["id"])
        copies = [n for n in racine_t if n.endswith(".bundle")]
        if copies:
            refus("TEST", f"copie(s) de bundle au /test (à traiter avant "
                          f"clôture) : {copies}")
        kit = racine_t.get("kit-m9f.zip") or {}
        if kit.get("md5Checksum") != KIT_M9F_MD5:
            refus("TEST", f"kit-m9f.zip au /test ne porte pas le md5 ACQUITTÉ "
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
                          f"remise reçue ({sig.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {SIGNATURES_MD5[:8]}… — le dossier du geste reçu)")
        cle = racine_t.get("cle-publique-I.txt") or {}
        if cle.get("md5Checksum") != CLE_MD5:
            refus("TEST", "cle-publique-I.txt au /test diverge de LA clé du kit "
                          f"({cle.get('md5Checksum', 'ABSENT')[:8]}… != "
                          f"{CLE_MD5[:8]}…)")
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; les DEUX kits == "
              f"les ACQUITTÉS md5 {KIT_M9F_MD5[:8]}… + {KIT_SONDE_MD5[:8]}… "
              f"(recoupés) ; les PIÈCES DE CÉRÉMONIE demeurent "
              f"(signatures-I.txt {SIGNATURES_MD5[:8]}… + cle-publique-I.txt "
              f"{CLE_MD5[:8]}… — le dossier du geste reçu)")

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
              f"SIGNATURE REÇUE ET INSTALLÉE + L'ERRATUM n° 9 ({TIP_ATTENDU[:7]}) "
              "— la série 090 poursuit ; GitHub en retard NOMMÉ, LA SECONDE "
              "SIGNATURE DU DÉVELOPPEUR (la remise étendue) EST ATTENDUE ===")
        return 2
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe ; "
          "le commit de passation 9854526 du geste précédent EMBARQUÉ, le "
          "flux tenu)")

    print("=== PASSATION FAITE : le bundle courant porte LA PREMIÈRE "
          "SIGNATURE DE LA RÉVISION 2 REÇUE ET INSTALLÉE (le garde 13/13 "
          "verts) + L'ERRATUM n° 9 — LA RÉVISION 2 ÉTENDUE (m8 "
          f"c444d730…, le harnais révisé, 131 · 131 VERTS × 3 graines) "
          f"({TIP_ATTENDU[:7]}) — la série 090 poursuit à la pointe ; "
          "l'ancien courant demeure dans l'histoire ; LA SECONDE SIGNATURE "
          "DU DÉVELOPPEUR EST ATTENDUE : la remise étendue → "
          "signatures-I.txt + cle-publique-I.txt au /test — puis deposer, "
          "le garde 13/13, LE REBUILD 1.0.0-dev.3 [sys-05 ET sys-06 "
          "réparés], LE KIT M9F RÉPARÉ, le run — ET SI LE VERT TIENT : LA "
          "FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
