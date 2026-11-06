#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9q.py — LA PASSATION du bundle au geste « LE QUATRIÈME RUN
TERRAIN (f) REÇU ET RECROPÉ : LE GESTE (ii) ACCOMPLI (Windows 11 build
26300) ET LE -6 SE RÉPÈTE À L'IDENTIQUE — LE SUSPECT (a) (la divergence
afd.sys Win10 ↔ Win11) ÉLIMINÉ SUR PIÈCES (le refus INTER-GÉNÉRATIONS) ;
le recoup 30/26→30/30, le run archivé ; ET LA SONDE SYS-05 (m9-(g)) — LE
CHANTIER PROMIS — OUVERTE ET LIVRÉE AU COFFRE (le trampoline de capture,
l'artefact INTACT ; la vague m9f DEMEURE) » : LA SÉRIE 090 POURSUIT À LA
POINTE COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : LE QUATRIÈME RUN RECROPÉ [Entrée 184 —
     la répétition à l'identique constatée PAR CODE (le journal du run 4
     == celui du run 3, ligne à ligne) ; le suspect (a) ÉLIMINÉ ; le
     recoup 30/30 ; le run archivé ; LA SONDE SYS-05 livrée : le kit
     215c2caa… au /test, la vague m9f INTACTE] + le worklog Task 102)
     est déposé au MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là,
     D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ; le
     kit m9f du /test porte le md5 ACQUITTÉ 90a1d022… INCHANGÉ ET le kit
     sonde le md5 215c2caa… (recoupés — l'état que le bundle porte) ;
  4. le push GitHub porte la pointe (D164 : la reprise confronte les
     trois miroirs — GitHub D'ABORD).

Usage : python3 scripts/passe_bundle_m9q.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import ast
import hashlib
import pathlib
import subprocess
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402
import assembler_kit_m9f as asm   # noqa: E402 — les TROIS PORTES, le juge

BUNDLE = None
ANCIEN = None
TIP_ATTENDU = None
CHEMIN_LOCAL = None

KIT_M9F_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"     # kit-m9f.zip au /test
KIT_SONDE_MD5 = "215c2caa54332ce91b03fd55c335513b"   # kit-sonde-sys05.zip


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


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
        refus("BUNDLE-TETES", f"la branche jalon du bundle ne pointe pas sur la "
                              f"pointe courante : {ligne_jalon[:80]!r}")
    octets = open(CHEMIN_LOCAL, "rb").read()
    md5_local = hashlib.md5(octets).hexdigest()
    print(f"[0] bundle construit : {BUNDLE} ({len(octets)} o, md5 "
          f"{md5_local[:8]}… — branche jalon == {TIP_ATTENDU[:7]} "
          f"(LE QUATRIÈME RUN RECROPÉ + LA SONDE SYS-05 LIVRÉE + sa "
          f"consignation)")
    # le bundle porte LE GESTE : les consignations relues dans l'arbre
    journal = subprocess.run(["git", "show", f"{TIP_ATTENDU}:docs/JOURNAL_TRAVAIL.md"],
                             cwd=REPO, capture_output=True, text=True).stdout
    if "## Entrée 184" not in journal \
            or "build 26300" not in journal:
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas l'Entrée "
                                "184 (le quatrième run recoupé — la machine "
                                "Windows 11, la répétition à l'identique)")
    worklog = subprocess.run(["git", "show", f"{TIP_ATTENDU}:worklog.md"],
                             cwd=REPO, capture_output=True, text=True).stdout
    if "## Task ID 102" not in worklog or "SONDE SYS-05" not in worklog:
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 102 (la sonde sys-05 livrée)")
    scenario = subprocess.run(
        ["git", "show", f"{TIP_ATTENDU}:tls13/terrain/scenario-m9f.py"],
        cwd=REPO, capture_output=True, text=True).stdout
    # LES TROIS PORTES DE L'ERRATUM n° 7 sur le scénario m9f INCHANGÉ
    # (le kit ACQUITTÉ ne doit pas avoir bougé : la sonde est ADDITIONNELLE)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as f:
        f.write(scenario)
        chemin_scenario_tip = pathlib.Path(f.name)
    try:
        verdict = asm._porte_e7_1_raw(ast.parse(scenario)) \
            or asm._porte_e7_2_ouvrir(ast.parse(scenario)) \
            or asm._porte_e7_3_echelle(chemin_scenario_tip)
        if verdict:
            refus("BUNDLE-CONTENU", "le scénario m9f du kit à la pointe ne "
                                  f"porte pas la réparation de l'erratum n° 7 "
                                  f"({verdict[0]})")
        if "ctypes.addressof(kit96)" not in scenario \
                or "ctypes.addressof(kit96_2)" not in scenario:
            refus("BUNDLE-CONTENU", "le scénario m9f du kit à la pointe ne "
                                    "porte pas LE POINTEUR aux DEUX sites "
                                    "OUVRIR")
    finally:
        chemin_scenario_tip.unlink(missing_ok=True)
    # LA SONDE vit à la pointe (le chantier livré)
    sonde = subprocess.run(
        ["git", "show", f"{TIP_ATTENDU}:tls13/terrain/scenario-sonde-sys05.py"],
        cwd=REPO, capture_output=True, text=True)
    if sonde.returncode != 0 or "SQUELETTE_TRAMPO" not in sonde.stdout \
            or "HANDLE_INVALIDE" not in sonde.stdout:
        refus("BUNDLE-CONTENU", "la sonde sys-05 est absente de la pointe "
                                "(le chantier promis : le trampoline de "
                                "capture)")
    plan = subprocess.run(
        ["git", "show", f"{TIP_ATTENDU}:docs/PLAN_MILESTONES.md"],
        cwd=REPO, capture_output=True, text=True).stdout
    if "LE QUATRIÈME RUN REÇU le 07/11/2026 (Entrée 184" not in plan:
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(f) du quatrième run")
    print("[0] le bundle porte LE GESTE : Entrée 184 (la répétition à "
          "l'identique, le suspect (a) éliminé, la machine Windows 11) + "
          "worklog Task 102 (la sonde livrée) + le scénario m9f INCHANGÉ "
          "(le kit ACQUITTÉ : les TROIS portes passées à la pointe) + LA "
          "SONDE (le trampoline de capture) + le plan (rangée (f) du "
          "quatrième run)")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    # L'ANCIEN découvert : le bundle 090-* courant de la racine, s'il n'est
    # pas le neuf (idempotence : absent si déjà re-passé)
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
                  f"ne porte que le courant ; le geste précédent demeure "
                  f"dans l'histoire)")

    # -- 4. /test : aucune copie de bundle + les DEUX kits (recoupés) ---------------
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
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; kit-m9f.zip == "
              f"le kit ACQUITTÉ md5 {KIT_M9F_MD5[:8]}… ET kit-sonde-sys05.zip =="
              f" le kit livré md5 {KIT_SONDE_MD5[:8]}… (recoupés — l'état que "
              "le bundle porte)")

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
        refus("PUSH", (push.stderr or push.stdout)[:200])
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe)")

    print("=== PASSATION FAITE : le bundle courant porte LE QUATRIÈME RUN "
          f"RECROPÉ + LA SONDE SYS-05 LIVRÉE ({TIP_ATTENDU[:7]}) — la série "
          "090 poursuit à la pointe ; l'ancien courant demeure dans "
          "l'histoire ; LE GESTE DU DÉVELOPPEUR SUR LA SONDE EST ATTENDU — "
          "puis le recoup, le coupable NOMMÉ, la réparation selon la charte "
          "— et si la percée tient : le run m9f réparé, LA FINALE 1.0.0 — "
          "LA GRANDE ŒUVRE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
