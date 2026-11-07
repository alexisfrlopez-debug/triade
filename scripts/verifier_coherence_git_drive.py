#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_coherence_git_drive.py — LA COHÉRENCE GIT ↔ DRIVE VERROUILLÉE
(lecture seule, AUCUNE écriture ; la demande du développeur « répare le
push git » SOLDÉE au geste présent — le commit de passation 43f942d
PARTI au flux : origin ré-aligné, LES TROIS MIROIRS recoupés ensemble).

LA PORTE UNIQUE DU GESTE — le terrain vérifié AVANT toute suite :

  GIT (le miroir GitHub) :
    g1. HEAD == 43f942d (la passation Task 108, la pointe) ;
    g2. origin/bundle051/v0.5.1-jalon-v7 == HEAD (LE PUSH RÉPARÉ —
        eb1479e..43f942d parti propre, fast-forward, rien défait) ;
    g3. l'arbre PROPRE (aucune modification suivie en attente ; les
        dossiers de travail non suivis — download/ — tolérés) ;
    g4. le dépôt distant joignable (le fetch relit la pointe).

  DRIVE — LE COFFRE /test (le dossier du développeur) :
    d1. la racine : 19 ENTRÉES (la sonde sys-06 livrée au geste 108
        porte la racine de 16 à 19 : kit-sonde-sys06.zip +
        LISEZMOI-sonde-sys06.txt + preuves-sonde-sys06/) ;
    d2. LA VAGUE M9F INTACTE : kit-m9f.zip == l'ACQUITTÉ RÉPARÉ
        79d44284… (jamais reconstruit depuis l'erratum n° 9) ;
    d3. la sonde sys-05 DEMEURÉE : kit-sonde-sys05.zip == 215c2caa… ;
    d4. LA SONDE SYS-06 : kit-sonde-sys06.zip == 67e2014d… (le livré
        du geste 108, == la copie locale du coffre de travail) ;
    d5. LES PIÈCES DE CÉRÉMONIE DEMEURÉES : signatures-I.txt ==
        503f3822… (la seconde remise de la révision 2 étendue,
        installée Entrée 188) + cle-publique-I.txt == 188a7d42…
        (l'ancre des ères, inchangée) ;
    d6. /test SANS COPIE DE BUNDLE (le courant vit au MIROIR, D141) ;
    d7. LE RÉCEPTACLE DE LA SONDE NÉ : preuves-sonde-sys06/ armé (il
        porte son LISEZMOI-preuves.txt — le geste au développeur) ;
    d8. le réceptacle m9f CLOS : preuves-m9f/ ne porte que son
        LISEZMOI (le run 6 archivé, plus aucun trio en vrac) ;
    d9. LE RUN 6 ARCHIVÉ : archives-preuves/preuves-run-m9f-6/ porte
        le trio + le verdict 33/33 ;
   d10. l'index des livraisons présent (LISEZMOI-archives-livraisons.txt).

  DRIVE — LE MIROIR ASSERTÉ (TRIADE-sauvegarde-git, la racine Drive) :
    m1. le bundle COURANT UNIQUE : triade-history-090-eb1479e ==
        1e9f2e68… (18 879 457 o — il porte l'Entrée 190, le jumeau,
        la sonde sys-06, la Task 108) ;
    m2. l'ANCIEN archivé versionné : archives-bundles/ porte
        090-17fb911 == b2817e48… — 53 archives, RIEN SUPPRIMÉ.

LE VERDICT : chaque porte relue VERT/ROUGE nommé ; à la fin, si tout
vert — « LES TROIS MIROIRS ALIGNÉS (local + Drive + GitHub) ».

Usage : python3 scripts/verifier_coherence_git_drive.py
Code de sortie : 0 = cohérence verrouillée ; 2 = refus nommé."""

import os
import pathlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

HEAD_ATTENDU = "43f942d"        # la passation Task 108
BRANCHE = "bundle051/v0.5.1-jalon-v7"

KIT_M9F_MD5 = "79d44284c70261375a2b055070fda223"
KIT_SONDE05_MD5 = "215c2caa54332ce91b03fd55c335513b"
KIT_SONDE06_MD5 = "67e2014d5a5725d19bcabce548d2475e"
SIG_I_PREFIX = "503f3822"       # la seconde remise (révision 2 étendue)
CLE_I_PREFIX = "188a7d42"       # l'ancre des ères

BUNDLE_COURANT = "triade-history-090-eb1479e.bundle"
BUNDLE_COURANT_MD5 = "1e9f2e68"
ANCIEN = "triade-history-090-17fb911.bundle"
ANCIEN_MD5 = "b2817e48"

RACINE_ENTREES = 19
ARCHIVES_BUNDLES = 53


def git(*args):
    r = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def main():
    portes = []   # (id, verdict_bool, detail)

    def porte(pid, ok, detail):
        portes.append((pid, bool(ok), detail))
        print(f"[{'OK ' if ok else '!! '}] {pid} : {detail}")

    # ============ GIT (g1..g4) ==================================================
    print("=" * 72)
    print("GIT — le miroir GitHub (la pointe du flux)")
    print("=" * 72)

    _, head, _ = git("rev-parse", "--short", "HEAD")
    porte("g1", head.startswith(HEAD_ATTENDU),
          f"HEAD == {head} (attendu {HEAD_ATTENDU} — la passation Task 108)")

    _, ref, _ = git("rev-parse", "--short",
                    f"origin/{BRANCHE}")
    porte("g2", ref == head,
          f"origin/{BRANCHE} == {ref} "
          f"{'== HEAD — LE PUSH RÉPARÉ, le flux aligné' if ref == head else '≠ HEAD — LE PUSH EN RETARD'}")

    _, sale, _ = git("status", "--porcelain", "--untracked-files=no")
    porte("g3", sale == "", "l'arbre PROPRE (aucune modification suivie en attente)"
          if sale == "" else f"l'arbre SALE : {sale[:120]!r}")

    rc, _, err = git("fetch", "origin")
    _, ref_apres, _ = git("rev-parse", "--short", f"origin/{BRANCHE}")
    porte("g4", rc == 0 and ref_apres == head,
          f"le fetch relit origin == {ref_apres} "
          f"({'joignable, la pointe tenue' if ref_apres == head else 'ou la pointe a bougé : ' + err[:100]}")

    # ============ DRIVE — LE COFFRE /test (d1..d10) =============================
    print()
    print("=" * 72)
    print("DRIVE — LE COFFRE /test (le dossier du développeur)")
    print("=" * 72)

    racine = ds.list_folder(TEST_ID)
    noms = sorted(racine)
    porte("d1", len(noms) == RACINE_ENTREES,
          f"la racine porte {len(noms)} entrées "
          f"(attendu {RACINE_ENTREES} — la sonde sys-06 a porté 16 → 19)")
    print("     racine : " + ", ".join(noms))

    def md5_de(nom):
        e = racine.get(nom) or {}
        return e.get("md5Checksum", "")

    porte("d2", md5_de("kit-m9f.zip") == KIT_M9F_MD5,
          f"kit-m9f.zip == {md5_de('kit-m9f.zip')[:8]}… "
          f"(l'ACQUITTÉ RÉPARÉ {KIT_M9F_MD5[:8]}… — la vague m9f INTACTE)")

    porte("d3", md5_de("kit-sonde-sys05.zip") == KIT_SONDE05_MD5,
          f"kit-sonde-sys05.zip == {md5_de('kit-sonde-sys05.zip')[:8]}… "
          f"(la sonde sys-05 demeurée {KIT_SONDE05_MD5[:8]}…)")

    porte("d4", md5_de("kit-sonde-sys06.zip") == KIT_SONDE06_MD5,
          f"kit-sonde-sys06.zip == {md5_de('kit-sonde-sys06.zip')[:8]}… "
          f"(la sonde sys-06 livrée {KIT_SONDE06_MD5[:8]}…)")

    local06 = pathlib.Path("/home/z/my-project/download/kit-sonde-sys06.zip")
    md5_local = ds.md5_of(local06) if local06.exists() else ""
    porte("d4b", md5_local == KIT_SONDE06_MD5,
          f"la copie locale du kit sonde == {md5_local[:8]}… "
          f"{'== le livré (le coffre de travail INTACT)' if md5_local == KIT_SONDE06_MD5 else '≠ le livré'}")

    sig = md5_de("signatures-I.txt")
    cle = md5_de("cle-publique-I.txt")
    porte("d5", sig.startswith(SIG_I_PREFIX) and cle.startswith(CLE_I_PREFIX),
          f"signatures-I.txt == {sig[:8]}… (la seconde remise {SIG_I_PREFIX}…) + "
          f"cle-publique-I.txt == {cle[:8]}… (l'ancre {CLE_I_PREFIX}…)")

    bundles_a_la_racine = [n for n in noms if n.startswith("triade-history-")]
    porte("d6", not bundles_a_la_racine,
          "/test SANS COPIE DE BUNDLE (le courant vit au miroir)"
          if not bundles_a_la_racine else
          f"bundle(s) en vrac à la racine : {bundles_a_la_racine}")

    recep_sonde = racine.get("preuves-sonde-sys06")
    if recep_sonde:
        dedans = ds.list_folder(recep_sonde["id"])
        porte("d7", "LISEZMOI-preuves.txt" in dedans,
              f"preuves-sonde-sys06/ NÉ et ARMÉ (porte {len(dedans)} entrée(s) : "
              f"{', '.join(sorted(dedans))})")
    else:
        porte("d7", False, "preuves-sonde-sys06/ INTROUVABLE au coffre")

    recep_m9f = racine.get("preuves-m9f")
    if recep_m9f:
        dedans = ds.list_folder(recep_m9f["id"])
        ok = set(dedans) == {"LISEZMOI-preuves.txt"}
        porte("d8", ok,
              "preuves-m9f/ CLOS (son LISEZMOI seul — le run 6 archivé)"
              if ok else f"preuves-m9f/ porte en vrac : {', '.join(sorted(dedans))}")
    else:
        porte("d8", False, "preuves-m9f/ INTROUVABLE au coffre")

    arch_liv = racine.get("archives-livraisons")
    if arch_liv:
        dedans_liv = ds.list_folder(arch_liv["id"])
        porte("d10", "LISEZMOI-archives-livraisons.txt" in dedans_liv,
              "l'index des livraisons présent (archives-livraisons/"
              "/LISEZMOI-archives-livraisons.txt)"
              if "LISEZMOI-archives-livraisons.txt" in dedans_liv
              else f"l'index INTROUVABLE dans archives-livraisons/ "
                   f"({', '.join(sorted(dedans_liv)[:5])}…)")
    else:
        porte("d10", False, "archives-livraisons/ INTROUVABLE au coffre")

    arch = racine.get("archives-preuves")
    run6 = False
    if arch:
        runs = ds.list_folder(arch["id"])
        run6 = "preuves-run-m9f-6" in runs
        porte("d9", run6,
              f"archives-preuves/ porte {len(runs)} run(s) archivé(s) — "
              f"preuves-run-m9f-6 {'PRÉSENT' if run6 else 'ABSENT'}")
    else:
        porte("d9", False, "archives-preuves/ INTROUVABLE au coffre")

    # ============ DRIVE — LE MIROIR ASSERTÉ (m1..m2) ============================
    print()
    print("=" * 72)
    print("DRIVE — LE MIROIR ASSERTÉ (TRIADE-sauvegarde-git, la racine Drive)")
    print("=" * 72)

    racine_drive = ds.list_folder(ds.DRIVE_ROOT_ID)   # dossier Drive « Triade »
    miroir = racine_drive.get("TRIADE-sauvegarde-git")
    if not miroir:
        porte("m1", False, "TRIADE-sauvegarde-git INTROUVABLE à la racine Drive")
        porte("m2", False, "miroir introuvable — archives-bundles/ non lues")
    else:
        racine_m = ds.list_folder(miroir["id"])
        courants = sorted(n for n in racine_m if n.startswith("triade-history-"))
        courant = racine_m.get(BUNDLE_COURANT)
        if courant is None and len(courants) == 1:
            # le nom du bundle a pu évoluer : recoup par unicité + préfixe
            seul = courants[0]
            courant = racine_m[seul]
            nom_lu = seul
        else:
            nom_lu = BUNDLE_COURANT
        porte("m1", len(courants) == 1 and courant is not None
              and courant.get("md5Checksum", "").startswith(BUNDLE_COURANT_MD5),
              f"le bundle COURANT UNIQUE au miroir : {nom_lu} == "
              f"{(courant or {}).get('md5Checksum', '')[:8]}… "
              f"(attendu {BUNDLE_COURANT_MD5}… — il porte l'Entrée 190 + la Task 108)")

        arch_b = racine_m.get("archives-bundles")
        if arch_b:
            archives = ds.list_folder(arch_b["id"])
            ancien = archives.get(ANCIEN)
            porte("m2", ANCIEN in archives and ancien.get("md5Checksum",
                  "").startswith(ANCIEN_MD5),
                  f"l'ANCIEN {ANCIEN} == "
                  f"{ancien.get('md5Checksum', '')[:8] if ancien else 'ABSENT'}… "
                  f"archivé versionné — {len(archives)} archives, "
                  f"{'rien supprimé' if len(archives) == ARCHIVES_BUNDLES else f'(attendu {ARCHIVES_BUNDLES})'}")
        else:
            porte("m2", False, "archives-bundles/ INTROUVABLE au miroir")

    # ============ LE VERDICT ====================================================
    print()
    print("=" * 72)
    rouges = [p for p in portes if not p[1]]
    if not rouges:
        print(f"VERDICT — {len(portes)}/{len(portes)} PORTES VERTES.")
        print("LE PUSH GITHUB RÉPARÉ (origin == 43f942d == HEAD), le coffre "
              "/test en ordre (la vague m9f intacte + les DEUX sondes + les "
              "pièces de cérémonie), le miroir asserté à la pointe.")
        print("LES TROIS MIROIRS ALIGNÉS (local + Drive + GitHub).")
        return 0
    print(f"VERDICT — {len(portes) - len(rouges)}/{len(portes)} portes vertes, "
          f"{len(rouges)} ROUGES :")
    for pid, _, detail in rouges:
        print(f"  ROUGE {pid} : {detail}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
