#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m9x.py — LA PASSATION du bundle au geste « LE RUN DE LA
SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES : LE MOT D'INFORMATION EST VENU
(le code exact de la première lecture réelle LU : -6,
STATUS_INVALID_PARAMETER — l'A/B des notations nomme LE CHAMP : AfdFlags
0x20 REFUSÉ PAR LE VRAI NOYAU) ; L'ERRATUM n° 10 + LA RÉVISION 3 + LA
REMISE RÉGÉNÉRÉE m8 e36141f7… — LA TROISIÈME SIGNATURE ATTENDUE ; LE RUN
ARCHIVÉ » : LA SÉRIE 090 POURSUIT À LA POINTE COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : LE RECOUP 17/17 [Entrée 191 — le mot
     d'information venu, le champ nommé, l'erratum n° 10 + la révision
     3 + la remise e36141f7…] + le worklog Task 109) est déposé au
     MIROIR (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. /test : AUCUNE copie de bundle n'y vit (recoupé) ; le kit-m9f.zip
     du /test porte le md5 RÉPARÉ INCHANGÉ (79d44284…) ; la sonde
     sys-05 demeure l'ACQUITTÉ (215c2caa…) ; LA SONDE SYS-06 DEMEURE
     (kit-sonde-sys06.zip md5 67e2014d… + LISEZMOI) avec le réceptacle
     preuves-sonde-sys06/ RÉ-ARMÉ (son LISEZMOI seul — le run archivé)
     et l'archive preuves-sonde-sys06-1/ porte le QUATUOR + le verdict
     du recoup 17/17 ; les pièces de cérémonie demeurent (la SECONDE
     remise installée — la TROISIÈME est attendue) ; le réceptacle
     preuves-m9f/ CLOS ;
  4. le push GitHub porte la pointe (D164 : GitHub D'ABORD ; le push
     RÉPARÉ du geste précédent est TENU : origin == 43f942d à
     l'ouverture) ; si le refus de sortie REVENAIT : le refus est
     NOMMÉ, le miroir Drive porte TOUT (D141), la passation rend 2
     SANS rien défaire.

Usage : python3 scripts/passe_bundle_m9x.py
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
KIT_SONDE05_MD5 = "215c2caa54332ce91b03fd55c335513b"  # kit-sonde-sys05.zip
KIT_SONDE06_MD5 = "67e2014d5a5725d19bcabce548d2475e"  # kit-sonde-sys06.zip
SIGNATURES_MD5 = "503f382229b4da0ddd43e833d31b2c2b"  # la SECONDE remise installée
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"         # la clé ancre des ères

LIGNE_M8 = ("m8 sys.1 "
            "e36141f75ebd8e615c53ff1bd59a4f4cee45b9397eefa66773ffbf54580b"
            "3536")
SHA_ARTEFACT = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
                "66b29226f")

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
          f"{md5_local[:8]}… — branche jalon == {TIP_ATTENDU[:7]} (LE RUN "
          "DE LA SONDE SYS-06 ANALYSÉ SUR PIÈCES : LE MOT D'INFORMATION "
          "VENU, LE CHAMP NOMMÉ, LA RÉVISION 3)")

    # le bundle porte LE GESTE : les consignations relues dans l'arbre -----
    journal = montrer("docs/JOURNAL_TRAVAIL.md")
    if ("## Entrée 191" not in journal
            or "LE MOT D'INFORMATION EST VENU" not in journal):
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas "
                                "l'Entrée 191 (le run de la sonde analysé)")
    worklog = montrer("worklog.md")
    if ("## Task ID 109" not in worklog
            or "LE RUN DE LA SONDE SYS-06 REÇU" not in worklog):
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 109 (le recoup de la sonde sys-06)")
    if "recouper_sondesys06.py" not in worklog:
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne nomme pas le "
                                "script de recoup de la sonde sys-06")
    remise = montrer("v06/sceau-I/a-signer.txt")
    if LIGNE_M8 not in remise:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne porte pas la "
                                "ligne m8 e36141f7… (la révision 3)")
    if len([l for l in remise.splitlines() if l.strip()]) != 13:
        refus("BUNDLE-CONTENU", "la remise à la pointe ne compte pas 13 lignes")
    spec06 = montrer("m8/I/sys-06-reception.md")
    if "révision 3" not in spec06 or "l'erratum n° 10" not in spec06:
        refus("BUNDLE-CONTENU", "la spec sys-06 à la pointe ne porte pas la "
                                "révision 3 (l'erratum n° 10 — LE TERRAIN A "
                                "JUGÉ LA MESURE)")
    notation06 = montrer("m8/notation/sys-06-reception.asm")
    if ("spec sys-06:R3" not in notation06
            or "mov dword ptr [rsp + 0x80], 0x20" not in notation06
            or "mov dword ptr [rsp + 0x7C], 0" not in notation06):
        refus("BUNDLE-CONTENU", "la notation sys-06 à la pointe ne porte pas "
                                "la révision 3 (AfdFlags 0, TdiFlags 0x20)")
    harnais = montrer("m8/harnais_sys.py")
    if "L'ERRATUM n° 10" not in harnais:
        refus("BUNDLE-CONTENU", "le harnais à la pointe ne porte pas "
                                "l'erratum n° 10 (le noyau strict suit LE "
                                "TERRAIN)")
    majkit = montrer("scripts/maj_kit.py")
    if "LISEZMOI-ceremonie-revision3-sys06.txt" not in majkit:
        refus("BUNDLE-CONTENU", "maj_kit.py à la pointe ne porte pas le "
                                "LISEZMOI de la révision 3 (la main du "
                                "développeur)")
    layout = montrer("tls13/layout.py")
    if "VERSION_DEV = 0x01000003" not in layout:
        refus("BUNDLE-CONTENU", "layout.py à la pointe ne porte pas la "
                                "version R10 0x01000003 (le dev.3 — le "
                                "dev.4 attend LA SIGNATURE)")
    build = montrer("tls13/build_m9.py")
    if 'sys-05:R2' not in build or 'sys-06:R2' not in build:
        refus("BUNDLE-CONTENU", "build_m9.py à la pointe ne porte pas les "
                                "contrats sys-05:R2 + sys-06:R2 (les portes "
                                "re-passées R3 appartiennent au geste du "
                                "rebuild dev.4)")
    scenario = montrer("tls13/terrain/scenario-m9f.py")
    if SHA_ARTEFACT not in scenario:
        refus("BUNDLE-CONTENU", "le scénario à la pointe n'épingle pas "
                                "l'artefact de23e577… (le kit réparé)")
    if "T0.erratum-9" not in scenario or "OCTETS_POSE_WSABUF" not in scenario:
        refus("BUNDLE-CONTENU", "le scénario à la pointe ne porte pas le "
                                "contrôle T0.erratum-9 (la pose relue dans "
                                "l'image)")
    artefact = octets_de("tls13/proxy.exe")
    if hashlib.sha256(artefact).hexdigest() != SHA_ARTEFACT:
        refus("BUNDLE-CONTENU", "l'artefact à la pointe n'est pas le build "
                                "de23e577… (le rebuild dev.3 — le dev.4 "
                                "attend LA SIGNATURE)")
    sonde = montrer("tls13/terrain/scenario-sonde-sys06.py")
    if "R_SYS06" not in sonde or "T0.erratum-9" not in sonde:
        refus("BUNDLE-CONTENU", "la sonde sys-06 absente ou non épinglée à "
                                "la pointe (le bloc sys-06, les contrôles "
                                "erratum-9)")
    if not ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
            in sonde and "66b29226f" in sonde):
        refus("BUNDLE-CONTENU", "la sonde à la pointe n'épingle pas "
                                "l'artefact de23e577… (les DEUX moitiés du "
                                "sha du rebuild dev.3)")
    for chemin in ("scripts/ramasse_sondesys06.py",
                   "scripts/recouper_sondesys06.py",
                   "scripts/verifier_coherence_git_drive.py",
                   "scripts/archiver_sondesys06.py",
                   "scripts/consigner_entree191.py"):
        if not montrer(chemin):
            refus("BUNDLE-CONTENU", f"{chemin} absent de l'arbre à la pointe")
    plan = montrer("docs/PLAN_MILESTONES.md")
    if "LE RUN DE LA SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES" not in plan:
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(f) du geste (la sonde sys-06 analysée)")
    print("[0] le bundle porte LE GESTE : Entrée 191 (le mot d'information "
          "venu — le code exact LU : -6 INVALID_PARAMETER, l'A/B nomme LE "
          "CHAMP : AfdFlags 0x20 refusé par le VRAI noyau) + worklog Task "
          "109 + LA RÉPARATION (la spec sys-06 RÉVISION 3 + la notation "
          "corrigée + le harnais suivi) + LA REMISE m8 e36141f7… + le "
          "LISEZMOI-ceremonie-revision3 (la main du développeur) + les "
          "scripts du geste (ramasse, recouper, le vérificateur de "
          "cohérence, archiver, consigner 191) + le plan (rangée (f) + "
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
                          f"SECONDE remise ({sig.get('md5Checksum', 'ABSENT')[:8]}… "
                          f"!= {SIGNATURES_MD5[:8]}… — la TROISIÈME est attendue)")
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
            refus("TEST", f"preuves-m9f/ n'est pas CLOS (son LISEZMOI seul "
                          f"attendu) : {restants_m9f}")
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; kit-m9f.zip == "
              f"le RÉPARÉ md5 {KIT_M9F_MD5[:8]}… (INCHANGÉ) + la sonde sys-05 "
              f"== l'acquis {KIT_SONDE05_MD5[:8]}… + LA SONDE SYS-06 == le "
              f"livré {KIT_SONDE06_MD5[:8]}… AVEC le réceptacle "
              "preuves-sonde-sys06/ RÉ-ARMÉ (son LISEZMOI seul — le run "
              "archivé) ; les PIÈCES DE CÉRÉMONIE demeurent (signatures-I.txt "
              f"{SIGNATURES_MD5[:8]}… la seconde remise INSTALLÉE + "
              f"cle-publique-I.txt {CLE_MD5[:8]}…) ; preuves-sonde-sys06-1/ "
              "porte le QUATUOR + LE VERDICT DU RECOUP (17/17) ; preuves-m9f/ "
              "CLOS")

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
        print("=== PASSATION FAITE AU MIROIR : le bundle courant porte LE RUN "
              f"DE LA SONDE SYS-06 ANALYSÉ SUR PIÈCES ({TIP_ATTENDU[:7]}) — "
              "la série 090 poursuit ; GitHub en retard NOMMÉ, LA TROISIÈME "
              "SIGNATURE EST ATTENDUE ===")
        return 2
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe ; "
          "LE PUSH RÉPARÉ du geste précédent TENU à l'ouverture : origin == "
          "43f942d, la passation 108 — le flux tenu)")

    print("=== PASSATION FAITE : le bundle courant porte LE RUN DE LA SONDE "
          "SYS-06 REÇU ET ANALYSÉ SUR PIÈCES (LE MOT D'INFORMATION EST VENU "
          "— le code exact LU : -6, STATUS_INVALID_PARAMETER ; l'A/B NOMME "
          "LE CHAMP : AfdFlags 0x20 REFUSÉ PAR LE VRAI NOYAU ; le run "
          "archivé AVEC son jugement 17/17 ; L'ERRATUM n° 10 + LA RÉVISION "
          "3 + LA REMISE RÉGÉNÉRÉE m8 e36141f7…) — la série 090 poursuit à "
          f"la pointe ({TIP_ATTENDU[:7]}) ; l'ancien courant demeure dans "
          "l'histoire ; LA TROISIÈME SIGNATURE DU DÉVELOPPEUR EST ATTENDUE "
          "(la remise e36141f7… — v06/sceau-I/a-signer.txt, TREIZE arbres — "
          "à signer HORS LIGNE avec la clé du 04/11, ramener signatures-I.txt "
          "+ cle-publique-I.txt au /test) — puis deposer, le garde 13/13, "
          "LE REBUILD 1.0.0-dev.4, LE KIT M9F RÉPARÉ, le run — ET SI LE "
          "VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
