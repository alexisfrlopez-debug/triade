#!/usr/bin/env python3
"""96_passe_bundle_293.py — D141 : le courant triade-history.bundle du
miroir (l'état 291-037034a, le guide de la ligne C) est ARCHIVÉ VERSIONNÉ
à archives-bundles/triade-history-291-037034a.bundle (jamais supprimé ni
écrasé), md5 recoupé PAR RE-LECTURE ; le courant sera rafraîchi à l'état
293 par la synchro d'après-commit."""
import hashlib
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

NOM_ARCHIVE = "triade-history-291-037034a.bundle"
TIP_ATTENDU = "037034a33a8b323db3cbbb0a9c4f524b56517c92"
BAC = "/home/z/my-project/work/triade-history.bundle"


def refus(nom, detail):
    print(f"[passation] REFUS {nom} : {detail}")
    sys.exit(2)


# -- 0. l'état AVANT -------------------------------------------------------
coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
miroir = coffre.get("TRIADE-sauvegarde-git") or refus("ETAT", "miroir introuvable")
racine_m = ds.list_folder(miroir["id"])
courant = racine_m.get("triade-history.bundle") or refus(
    "ETAT", "le courant triade-history.bundle introuvable")
archives = racine_m.get("archives-bundles") or refus(
    "ETAT", "archives-bundles/ introuvable")
print(f"[état] le courant au miroir : md5 {courant.get('md5Checksum', '')[:8]}… ; "
      f"archives : {len(ds.list_folder(archives['id']))} entrées")

deja = ds.list_folder(archives["id"]).get(NOM_ARCHIVE)
if deja:
    print(f"[idempotent] {NOM_ARCHIVE} vit déjà aux archives "
          f"(md5 {deja.get('md5Checksum', '')[:8]}…) — rien à faire")
    sys.exit(0)

# -- 1. le courant du miroir TÉLÉCHARGÉ et vérifié --------------------------
st, octets, _ = ds.api("GET", ds.API + f"/files/{courant['id']}?alt=media")
if st != 200:
    refus("TELECHARGEMENT", f"HTTP {st}")
md5_local = hashlib.md5(octets).hexdigest()
if md5_local != courant.get("md5Checksum"):
    refus("MD5", f"le téléchargement diverge : {md5_local[:8]}… ≠ "
                 f"{courant.get('md5Checksum', '')[:8]}…")
import subprocess, tempfile, pathlib  # noqa: E402
with tempfile.NamedTemporaryFile(suffix=".bundle", delete=False) as f:
    f.write(octets)
    chemin = pathlib.Path(f.name)
tetes = subprocess.run(["git", "bundle", "list-heads", str(chemin)],
                       capture_output=True, text=True).stdout
main = next((l.split()[0] for l in tetes.splitlines()
             if l.endswith("refs/heads/main")), "")
chemin.unlink()
if not main.startswith(TIP_ATTENDU):
    refus("POINTES", f"le courant ne porte pas l'état 291 : main={main[:7]}")
print(f"[1] le courant téléchargé : md5 {md5_local[:8]}… MATCH, "
      f"main={main[:7]} (l'état 291, le guide de la ligne C)")

# -- 2. l'ARCHIVAGE VERSIONNÉ ----------------------------------------------
with tempfile.NamedTemporaryFile(suffix=".bundle", delete=False) as f:
    f.write(octets)
    chemin = pathlib.Path(f.name)
ds.upload_create(archives["id"], NOM_ARCHIVE, chemin)
chemin.unlink()

# -- 3. le recoup PAR RE-LECTURE -------------------------------------------
apres = ds.list_folder(archives["id"]).get(NOM_ARCHIVE) or refus(
    "ARCHIVAGE", f"{NOM_ARCHIVE} absent des archives après dépôt")
if apres.get("md5Checksum") != md5_local:
    refus("ARCHIVAGE", "md5 distant ≠ local après dépôt")
print(f"[3] archivé versionné : {NOM_ARCHIVE} → archives-bundles/ "
      f"(md5 {md5_local[:8]}… MATCH par re-lecture)")

# -- 4. la copie de travail du bac mise à jour ------------------------------
import pathlib  # noqa: E402
pathlib.Path(BAC).write_bytes(octets)
print(f"[4] la copie de travail du bac : {BAC} ({len(octets)} o, md5 {md5_local[:8]}…)")
