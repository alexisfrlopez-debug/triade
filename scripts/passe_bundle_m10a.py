#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m10a.py — LA PASSATION du bundle au geste « M10-(a) RÉALISÉ :
LES DIX-HUIT SPÉCIFICATIONS POSÉES (la couche I complète du TGN, R2 tenue) ;
LE PLAN D'ADRESSAGE ARRÊTÉ AVANT LA NOTATION ; L'HÉRITAGE DÉCLARÉ PAR LA
CARTE (libc-03 RETIRÉ) ; LA TABLE i11xxxx ; L'INSTRUMENT 150 CONTRÔLES
VERTS » : LA SÉRIE 090 POURSUIT À LA POINTE COURANTE.
  1. le bundle triade-history-090-<pointe>.bundle (git bundle --all,
     pointe = LE commit du geste : les 18 spécifications loupe-01..18 +
     loupe/layout.py + le README étendu [la table i11] + l'Entrée 195 +
     la D172 + le PLAN [la rangée (a) RÉALISÉE] + le worklog Task 113 +
     les DEUX instruments du geste) est déposé au MIROIR
     (TRIADE-sauvegarde-git/ — l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-090-*.bundle est ARCHIVÉ VERSIONNÉ
     dans archives-bundles/ (JAMAIS supprimé ni écrasé) ;
  3. /test : AUCUNE copie de bundle n'y vit (recoupé) ; les pièces de
     l'ère close DEMEURENT (le kit-m9f RÉPARÉ 92098687…, les DEUX
     sondes, LA TROISIÈME remise 0978c117… + l'ancre 188a7d42…, les
     réceptacles ré-armés, l'archive du run 7 avec ses SIX pièces et
     LE VERDICT 34/34) — le geste M10-(a) ne livre AUCUN kit (la
     couche I seule vit : le kit terrain viendra à M10-(d)) ;
  4. le push GitHub porte la pointe (D164 : GitHub D'ABORD) ; si le
     refus de sortie REVENAIT : le refus est NOMMÉ, le miroir Drive
     porte TOUT (D141), la passation rend 2 SANS rien défaire.

Usage : python3 scripts/passe_bundle_m10a.py
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

# Les pièces de l'ère close qui demeurent au /test (le geste M10-(a) n'y
# touche PAS : la couche I seule vit, le kit terrain viendra à M10-(d))
KIT_M9F_MD5 = "9209868796330fab0ea3f01b4879eb80"     # le kit RÉPARÉ (dev.4)
KIT_SONDE05_MD5 = "215c2caa54332ce91b03fd55c335513b"  # kit-sonde-sys05.zip
KIT_SONDE06_MD5 = "67e2014d5a5725d19bcabce548d2475e"  # kit-sonde-sys06.zip
SIGNATURES_MD5 = "0978c117af62730508d60211f869bdf6"  # la TROISIÈME remise
CLE_MD5 = "188a7d42df2d03f68bfb50fada3a84a1"         # la clé ancre des ères

SIX_RUN7 = ["temoin-m9f.txt",
            "scenario-m9f-journal.log",
            "ligne-recue.txt",
            "journal-emissions.txt",
            "VERDICT-run-m9f.txt",
            "VERDICT-recoup-labo-m9f-7.txt"]

LES_18 = [f"loupe/I/loupe-{n:02d}-{nom}.md" for n, nom in [
    (1, "ouvrir"), (2, "lire"), (3, "fermer"), (4, "cadre"),
    (5, "sha256"), (6, "md5"), (7, "cumul"), (8, "ligne"),
    (9, "ecran"), (10, "peinture"), (11, "defilement"), (12, "aller"),
    (13, "recherche"), (14, "suivant"), (15, "curseur"), (16, "saisie"),
    (17, "sauver"), (18, "quitter")]]


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
          f"{md5_local[:8]}… — branche jalon == {TIP_ATTENDU[:7]} [M10-(a) "
          "LES DIX-HUIT SPÉCIFICATIONS POSÉES])")

    # le bundle porte LE GESTE : les consignations relues dans l'arbre -----
    journal = montrer("docs/JOURNAL_TRAVAIL.md")
    if ("## Entrée 195" not in journal
            or "LE CHANTIER M10-(a) RÉALISÉ — LES DIX-HUIT SPÉCIFICATIONS "
            "POSÉES" not in journal):
        refus("BUNDLE-CONTENU", "le journal à la pointe ne porte pas "
                                "l'Entrée 195 (les 18 spécifications posées)")
    worklog = montrer("worklog.md")
    if ("## Task ID 113" not in worklog
            or "LES DIX-HUIT SPÉCIFICATIONS LOUPE-01..18 POSÉES" not in worklog):
        refus("BUNDLE-CONTENU", "le worklog à la pointe ne porte pas la "
                                "Task ID 113 (le geste M10-(a))")
    for chemin in LES_18:
        if not montrer(chemin):
            refus("BUNDLE-CONTENU", f"{chemin} absent de l'arbre à la pointe")
    for chemin in ("loupe/layout.py", "loupe/I/README.md",
                   "scripts/verifier_specs_m10a.py",
                   "scripts/consigner_m10a.py"):
        if not montrer(chemin):
            refus("BUNDLE-CONTENU", f"{chemin} absent de l'arbre à la pointe")
    layout = montrer("loupe/layout.py")
    if ("VERSION_DEV = 0x00010001" not in layout
            or "-1: \"FIN (la fin nommée" not in layout):
        refus("BUNDLE-CONTENU", "loupe/layout.py à la pointe ne porte pas la "
                                "balise dev.1 ni la table des verdicts")
    readme = montrer("loupe/I/README.md")
    if ("| loupe-01 | i110001 |" not in readme
            or "Le chantier (a) est COMPLET : les 18" not in readme):
        refus("BUNDLE-CONTENU", "le README loupe à la pointe ne porte pas la "
                                "table i11xxxx ni le chantier (a) COMPLET")
    decisions = montrer("docs/DECISIONS.md")
    if "## D172 — LE CHANTIER M10-(a) RÉALISÉ" not in decisions:
        refus("BUNDLE-CONTENU", "DECISIONS à la pointe ne porte pas la D172")
    plan = montrer("docs/PLAN_MILESTONES.md")
    if "RÉALISÉ (Entrée 195, D172)" not in plan:
        refus("BUNDLE-CONTENU", "le plan à la pointe ne porte pas la rangée "
                                "(a) RÉALISÉE")
    print("[0] le bundle porte LE GESTE : les 18 spécifications + le plan "
          "d'adressage (la balise dev.1, la table des verdicts) + le README "
          "(la table i11, le chantier COMPLET) + l'Entrée 195 + la D172 + "
          "le PLAN (la rangée (a) RÉALISÉE) + la Task 113 + les DEUX "
          "instruments (verifier 150 contrôles, consigner)")

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

    # -- 4. /test : aucune copie de bundle + les pièces de l'ère close --------------
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
        pm9 = racine_t.get("preuves-m9f") or {}
        restants_m9f = sorted(lister(pm9["id"])) if pm9.get("id") else ["(ABSENT)"]
        if restants_m9f != ["LISEZMOI-preuves.txt"]:
            refus("TEST", f"preuves-m9f/ n'est pas RÉ-ARMÉ (son LISEZMOI seul "
                          f"attendu) : {restants_m9f}")
        arch_p = racine_t.get("archives-preuves") or {}
        run7 = lister(arch_p["id"]).get("preuves-run-m9f-7") if arch_p.get("id") else None
        if not run7:
            refus("TEST", "preuves-run-m9f-7/ absent de archives-preuves/ "
                          "(la clôture D143 du geste M9 n'est pas passée)")
        dans_run7 = sorted(lister(run7["id"]))
        if dans_run7 != sorted(SIX_RUN7):
            refus("TEST", f"preuves-run-m9f-7/ ne porte pas les SIX pièces "
                          f"attendues : {dans_run7}")
        print("[4] /test : AUCUNE copie de bundle (recoupé) ; les pièces de "
              "L'ÈRE CLOSE demeurent INTACTES (kit-m9f.zip == le RÉPARÉ "
              f"{KIT_M9F_MD5[:8]}… + les DEUX sondes + LA TROISIÈME remise "
              f"{SIGNATURES_MD5[:8]}… + l'ancre {CLE_MD5[:8]}… + les "
              "réceptacles RÉ-ARMÉS + l'archive du run 7 avec ses SIX "
              "pièces et LE VERDICT 34/34) — le geste M10-(a) ne livre "
              "AUCUN kit (la couche I seule vit : le kit terrain vivra à "
              "M10-(d), modèle m9f)")

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
              "le push sera re-tenté au geste suivant")
        print("=== PASSATION FAITE AU MIROIR : le bundle courant porte "
              f"M10-(a) RÉALISÉ ({TIP_ATTENDU[:7]}) — la série 090 "
              "poursuit ; GitHub en retard NOMMÉ ===")
        return 2
    apres = subprocess.run(
        ["git", "ls-remote", "origin", "refs/heads/bundle051/v0.5.1-jalon-v7"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    if not apres.startswith(TIP_ATTENDU):
        refus("PUSH", f"origin ne porte pas la pointe après push : {apres[:80]!r}")
    print(f"[6] push GitHub : origin/bundle051/v0.5.1-jalon-v7 == "
          f"{TIP_ATTENDU[:7]} (relu MATCH — les trois miroirs à la pointe ; "
          "le flux tenu)")

    print("=== PASSATION FAITE : le bundle courant porte M10-(a) RÉALISÉ — "
          "LES DIX-HUIT SPÉCIFICATIONS POSÉES (LA COUCHE I COMPLÈTE DU "
          "TGN, R2 TENUE : AUCUN OCTET DE NOTATION) + LE PLAN D'ADRESSAGE "
          "ARRÊTÉ AVANT LA NOTATION (LES 64 CONSTANTES MD5 DÉRIVÉES PAR "
          "ARITHMÉTIQUE, LA TABLE DES SEPT VERDICTS, LE CADRE, LES ZONES, "
          "L'IAT) + L'HÉRITAGE DÉCLARÉ PAR LA CARTE + LA TABLE i11xxxx + "
          "L'INSTRUMENT 150 CONTRÔLES VERTS — la série 090 poursuit à la "
          f"pointe ({TIP_ATTENDU[:7]}) ; l'ancien courant demeure dans "
          "l'histoire ; LES TROIS MIROIRS ALIGNÉS (local + Drive + "
          "GitHub) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
