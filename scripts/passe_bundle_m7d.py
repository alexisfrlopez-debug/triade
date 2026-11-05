#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""passe_bundle_m7d.py — LA PASSATION D141 DU BUNDLE au geste
« chantier M7-(d), la part laboratoire accomplie — l'export de continuité
multi-profils + le kit terrain déposé + la clôture D143 du run m6d » (D158) :
  1. le bundle triade-history-070-816eee7.bundle (git bundle --all, pointe =
     LE commit du geste : L'EXPORT DE CONTINUITÉ MULTI-PROFILS [le conteneur
     TRIADE-EXP1 729 277 o chiffré + signé, 126 fichiers — 81 specs I, 5
     artefacts B, 5 cartes C ; l'import AUTO-PORTANT aux CINQ étapes § 8.2,
     la géométrie et les dérivations publiques AU MANIFESTE ; les rituels
     rejoués sur les octets TRANSPORTÉS — la parité § 8.3 des TROIS profils
     dans un seul conteneur] + LE KIT TERRAIN M7 DÉPOSÉ AU COFFRE /test [le
     scellé riscv/corpus 0.8.0-rc.1 + le démonstrateur riscv/demo +
     L'INSTRUMENT EMBARQUÉ qemu-riscv64 10.0.13 STATIQUE ; épreuvé VERT
     16 PASS / 0 ÉCHEC à l'extraction vierge — D153] + LA CLÔTURE D143 DU
     RUN m6d [la vague m6d archivée dans vagues-m6/ ; les pièces du run +
     le verdict du recoup labo à preuves-run-m6d/] + Entrée 154 + D158 +
     worklog Task 72) est déposé au MIROIR (TRIADE-sauvegarde-git/ —
     l'histoire vit là, D141) ;
  2. l'ancien courant triade-history-070-33cde07.bundle (le porteur du
     chantier M7-(c) : le patch fence.i démontré en exécution, le verrou
     multi-profils, la 0.8.0-rc.1 scellée, Entrée 153/D157) est ARCHIVÉ
     VERSIONNÉ dans archives-bundles/ (JAMAIS supprimé ni écrasé — D141) ;
  3. aucun retrait /test : aucune copie de bundle n'y vit (recoupé).

La cadence « une passation par geste de jalon » est tenue (leçon D141 :
aucune dette n'accumule) : le bundle courant porte désormais LE QUATRIÈME
CHANTIER DU JALON M7 (la part laboratoire) avec sa consignation. La série
DEMEURE 070 (l'ère de la balise 0.7.0 scellée) : la série 080 naîtra à la
finale 0.8.0 du jalon.

Chaque geste ASSERTÉ ; md5 recoupés AVANT tout déplacement ; idempotent par
saut d'already-fait. Déplacement : addParents/removeParents EN PARAMÈTRES DE
REQUÊTE (leçon v7/D143).

Usage : python3 scripts/passe_bundle_m7d.py
Code de sortie : 0 = passation terminée et recoupée ; 2 = refus nommé."""

import hashlib
import subprocess
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

BUNDLE = "triade-history-070-816eee7.bundle"      # le courant NOUVEAU (chantier M7-(d) labo, D158)
ANCIEN = "triade-history-070-33cde07.bundle"      # le courant actuel au miroir (chantier M7-(c), D157)
TIP_ATTENDU = "816eee74c642990bbe0b7fab6555035d5026079c"   # la pointe du geste (push recoupé)
CHEMIN_LOCAL = REPO + "/bundles-070/" + BUNDLE


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


def lister(pid):
    return ds.list_folder(pid)


def main():
    # -- 0. le bundle local, construit et vérifié --------------------------------
    subprocess.run(["mkdir", "-p", REPO + "/bundles-070"], check=True)
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
    print(f"[0] bundle construit : {BUNDLE} ({len(octets)} o, md5 {md5_local[:8]}…) — "
          f"branche jalon == {TIP_ATTENDU[:7]} (le chantier M7-(d) la part laboratoire accomplie avec sa consignation)")

    # -- 1. l'état AVANT (assertions) ---------------------------------------------
    coffre = lister(ds.DRIVE_ROOT_ID)
    miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
    racine_m = lister(miroir["id"])
    ancien = racine_m.get(ANCIEN) or refus("ETAT", f"l'ancien courant {ANCIEN} introuvable au miroir")
    archives = racine_m.get("archives-bundles") or refus("ETAT", "archives-bundles/ introuvable")
    deja = racine_m.get(BUNDLE)
    deja_arch = lister(archives["id"]).get(BUNDLE)
    print(f"[état] ancien courant : {ANCIEN} (md5 {ancien.get('md5Checksum', '')[:8]}…)")

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
              f"(md5 {ancien.get('md5Checksum', '')[:8]}… recoupé — la racine ne porte que le courant)")

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
    print(f"[état] archives-bundles/ ({len(archives_finales)}) : {archives_finales}")
    if courants != [BUNDLE]:
        refus("ETAT-FINAL", f"la racine du miroir ne porte pas LE courant unique : {courants}")
    if ANCIEN not in archives_finales:
        refus("ETAT-FINAL", f"{ANCIEN} absent des archives — D141 violée")
    print("[passation] D141 TERMINÉE — le bundle courant porte LE CHANTIER M7-(d) "
          "LA PART LABORATOIRE ACCOMPLIE (816eee7 : l'export de continuité "
          "multi-profils VERT de bout en bout + le kit terrain DÉPOSÉ au "
          "coffre /test avec l'instrument EMBARQUÉ + la clôture D143 du run "
          "m6d + Entrée 154 + D158), l'ancien vit aux archives, rien "
          "n'a été supprimé")


if __name__ == "__main__":
    main()
