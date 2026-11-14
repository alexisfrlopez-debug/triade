#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""108_passe_bundle_295.py — D141, LA PASSATION DU BUNDLE pour l'Entrée 295 :
le courant triade-history.bundle du miroir (l'état 294 final, la pointe
be7f948) est ARCHIVÉ VERSIONNÉ à archives-bundles/triade-history-294-
be7f948.bundle (jamais supprimé ni écrasé), md5 recoupé PAR RE-LECTURE ;
le courant sera rafraîchi à l'état 295 par la synchro d'après-commit."""
import hashlib
import subprocess
import sys
import pathlib

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

NOM_ARCHIVE = "triade-history-294-be7f948.bundle"
POINTE_294 = "be7f948f8f9a3447f2baee07efe69780fc7bd52d"
LOCAL = pathlib.Path("/home/z/my-project/work/triade-history-294.bundle")


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


# -- 0. l'état AVANT ----------------------------------------------------------
miroir = ds.list_folder(ds.DRIVE_ROOT_ID).get("TRIADE-sauvegarde-git") \
    or refus("ETAT", "miroir introuvable")
racine_m = ds.list_folder(miroir["id"])
courant = racine_m.get("triade-history.bundle") \
    or refus("ETAT", "le courant triade-history.bundle introuvable")
archives = racine_m.get("archives-bundles") \
    or refus("ETAT", "archives-bundles/ introuvable")
print(f"[état] le courant : md5 {courant.get('md5Checksum', '')[:8]}… ; "
      f"archives : {len(ds.list_folder(archives['id']))} entrées")

deja = ds.list_folder(archives["id"]).get(NOM_ARCHIVE)
if deja:
    print(f"[idempotent] {NOM_ARCHIVE} vit déjà aux archives "
          f"(md5 {deja.get('md5Checksum', '')[:8]}…) — rien à faire")
    sys.exit(0)

# -- 1. le bundle local (téléchargé du miroir, vérifié) ------------------------
if not LOCAL.exists():
    refus("LOCAL", f"{LOCAL} absent — le télécharger d'abord")
octets = LOCAL.read_bytes()
md5_local = hashlib.md5(octets).hexdigest()
if md5_local != courant.get("md5Checksum"):
    refus("MD5", f"la copie locale diverge du courant : {md5_local[:8]}… ≠ "
                 f"{courant.get('md5Checksum', '')[:8]}…")
tetes = subprocess.run(["git", "bundle", "list-heads", str(LOCAL)],
                       capture_output=True, text=True).stdout
main = next((l.split()[0] for l in tetes.splitlines()
             if l.endswith("refs/heads/main")), "")
if not main.startswith(POINTE_294[:7]):
    refus("POINTES", f"le courant ne porte pas l'état 294 : main={main[:7]}")
print(f"[1] le courant vérifié : md5 {md5_local[:8]}… MATCH, "
      f"main={main[:7]} (l'état 294 final)")

# -- 2. l'ARCHIVAGE VERSIONNÉ --------------------------------------------------
ds.upload_create(archives["id"], NOM_ARCHIVE, LOCAL)

# -- 3. le recoup PAR RE-LECTURE -----------------------------------------------
apres = ds.list_folder(archives["id"]).get(NOM_ARCHIVE) or refus(
    "ARCHIVAGE", f"{NOM_ARCHIVE} absent des archives après dépôt")
if apres.get("md5Checksum") != md5_local:
    refus("ARCHIVAGE", "md5 distant ≠ local après dépôt")
print(f"[3] archivé versionné : {NOM_ARCHIVE} → archives-bundles/ "
      f"(md5 {md5_local[:8]}… MATCH par re-lecture, "
      f"{len(ds.list_folder(archives['id']))} entrées aux archives)")
