#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9r.py — LA PASSATION du bundle au geste « LE RUN DE LA
SONDE SYS-05 (g) REÇU ET RECROPÉ : LA MESURE RENDUE (LE NTSTATUS BRUT DU
GESTE M9F = 0xC0000005, TROIS fois, DÉTERMINISTE), LE COUPABLE NOMMÉ À
L'INSTRUCTION PRÈS ((b) LE CONTRAT D'APPEL — LA POSE DU WSABUF, spec
R1-Q3 « 12 o »), LE VERDICT MANQUANT EXPLIQUÉ (L'ERRATUM n° 8 : LE JMP
REL32 DU TROMPHONE T6), LA RÉVISION 2 DE LA SPEC + LA RÉPARATION À LA
SOURCE » : LA SÉRIE 090 POURSUIT À LA POINTE COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : LE RUN DE LA SONDE RECROPÉ [Entrée
     185 — la mesure 0xC0000005, le coupable LU dans l'artefact scellé,
     le recoup 31/31, le run archivé, LA RÉVISION 2 + l'erratum n° 8
     réparés à la source] + le worklog Task 103) est déposé au MIROIR
     (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé) ; les
     DEUX kits du /test portent les md5 ACQUITTÉS (90a1d022… +
     215c2caa… — recoupés : l'état que le bundle porte) ;
  4. le push GitHub porte la pointe (D164 : la reprise confronte les
     trois miroirs — GitHub D'ABORD) ; si le refus de sortie PERSISTE
     (le 403 nommé au geste précédent) : le refus est NOMMÉ, le miroir
     Drive porte TOUT (D141), la passation rend 2 SANS rien défaire.

Usage : python3 scripts/passe_bundle_m9r.py
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
          f"{md5_local[:8]}… — branche jalon == {TIP_ATTENDU[:7]} (LE RUN "
          "DE LA SONDE RECROPÉ + LA RÉVISION 2 + l'erratum n° 8)")

    # le bundle porte LE GESTE : les consignations relues dans l'arbre -----
    journal = montrer("docs/JOURNAL_TRAVAIL.md")
    if "## Entrée 185" not in journal or "0xC0000005" not in journal:
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas "
                                "l'Entrée 185 (la mesure 0xC0000005)")
    worklog = montrer("worklog.md")
    if "## Task ID 103" not in worklog or "WSABUF" not in worklog:
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 103 (le coupable nommé : la pose "
                                "du WSABUF)")
    spec = montrer("m8/I/sys-05-emission.md")
    if "révision 2" not in spec or "SEIZE octets" not in spec \
            or "16 o + 24 o" not in spec:
        refus("BUNDLE-CONTENU", "la spec sys-05 à la pointe ne porte pas la "
                                "RÉVISION 2 (le WSABUF canonique 16 o)")
    notation = montrer("m8/notation/sys-05-emission.asm")
    if "mov qword ptr [rsp + 0x68], rdi" not in notation \
            or "[rsp + 0x64], rdi" in notation:
        refus("BUNDLE-CONTENU", "la notation à la pointe ne porte pas la pose "
                                "corrigée (buf à +8)")
    for scen in ("tls13/terrain/scenario-m9f.py",
                 "tls13/terrain/scenario-sonde-sys05.py"):
        src = montrer(scen)
        if 'b"\\xe9" + struct.pack("<i"' in src:
            refus("BUNDLE-CONTENU", f"{scen} porte encore un jmp rel32 "
                                    "(l'erratum n° 8 non réparé)")
        if 'b"\\x48\\xba" + struct.pack("<Q", base + R_SYS01)' not in src:
            refus("BUNDLE-CONTENU", f"{scen} ne porte pas l'adressage ABSOLU "
                                    "du tromphone (l'erratum n° 8)")
    plan = montrer("docs/PLAN_MILESTONES.md")
    if "LE RUN DE LA SONDE REÇU le 07/11 au soir (Entrée 185" not in plan:
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(f) du run de la sonde")
    print("[0] le bundle porte LE GESTE : Entrée 185 (la mesure 0xC0000005, "
          "le coupable nommé : LA POSE DU WSABUF) + worklog Task 103 + LA "
          "RÉVISION 2 de la spec + la notation corrigée + l'erratum n° 8 "
          "réparé dans les DEUX scénarios + le plan (rangée (f) + État)")

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
        preuves_sonde = racine_t.get("preuves-sonde-sys05") or {}
        arch_p = racine_t.get("archives-preuves") or {}
        if arch_p and "preuves-sonde-sys05-1" not in lister(arch_p["id"]):
            refus("TEST", "archives-preuves/ ne porte pas preuves-sonde-sys05-1/ "
                          "(l'archivage du run d'abord)")
        if preuves_sonde and set(lister(preuves_sonde["id"])) != \
                {"LISEZMOI-preuves.txt"}:
            refus("TEST", f"preuves-sonde-sys05/ mal ré-armé : "
                          f"{sorted(lister(preuves_sonde['id']))}")
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; les DEUX kits == "
              f"les ACQUITTÉS md5 {KIT_M9F_MD5[:8]}… + {KIT_SONDE_MD5[:8]}… "
              "(recoupés) ; le run de la sonde ARCHIVÉ (preuves-sonde-sys05-1/) "
              "et le réceptacle ré-armé (recoupés — l'état que le bundle porte)")

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
              "CONTOURNE PAS le refus (le 403 du geste précédent, nommé) : "
              "le miroir Drive porte TOUT (D141), le push sera re-tenté au "
              "geste suivant — ou poussé par le développeur depuis sa "
              "machine (git push origin bundle051/v0.5.1-jalon-v7 : le "
              "dépôt local == le miroir == le bundle)")
        print("=== PASSATION FAITE AU MIROIR : le bundle courant porte LE RUN "
              f"DE LA SONDE RECROPÉ ({TIP_ATTENDU[:7]}) — la série 090 "
              "poursuit ; GitHub en retard NOMMÉ, LE REBUILD 1.0.0-dev.3 "
              "EST LE GESTE SUIVANT ===")
        return 2
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe)")

    print("=== PASSATION FAITE : le bundle courant porte LE RUN DE LA SONDE "
          f"RECROPÉ — LA MESURE RENDUE, LE COUPABLE NOMMÉ, LA RÉVISION 2 + "
          f"L'ERRATUM n° 8 ({TIP_ATTENDU[:7]}) — la série 090 poursuit à la "
          "pointe ; l'ancien courant demeure dans l'histoire ; LE REBUILD "
          "1.0.0-dev.3 EST LE GESTE SUIVANT — puis le kit m9f réparé, le "
          "run, LA FINALE 1.0.0 : LE JALON M9 — LA GRANDE ŒUVRE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
