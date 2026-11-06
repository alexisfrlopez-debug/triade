#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ramasse_sonde1.py — télécharge TOUTES les pièces du run terrain de la
sonde sys-05 depuis /test/preuves-sonde-sys05/ vers
download/preuves-sonde-sys05-1/ (dossier NEUF), contrôle les md5
aller-retour, et recoupe les kits à la racine du /test (l'acquitté sonde
215c2caa… + l'acquitté m9f 90a1d022…)."""
import hashlib
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

DEST = pathlib.Path("/home/z/my-project/download/preuves-sonde-sys05-1")
DEST.mkdir(parents=True, exist_ok=True)

racine = ds.list_folder(ds.DRIVE_ROOT_ID)
test = racine["test"]

# --- 0. les kits à la racine : recoup des acquittés -------------------------
print("=== /test : recoup des DEUX kits (les acquittés) ===")
racine_test = ds.list_folder(test["id"])
attendus_kits = {
    "kit-sonde-sys05.zip": "215c2caa54332ce91b03fd55c335513b",
    "kit-m9f.zip": "90a1d0222b64b0b10f6b44d7e530ec5f",
}
for nom, md5_attendu in attendus_kits.items():
    f = racine_test.get(nom)
    if f is None:
        print(f"  ABSENT : {nom}")
        continue
    md5 = f.get("md5Checksum", "-")
    marque = "OK " if md5 == md5_attendu else "KO!"
    print(f"  [{marque}] {nom} : md5={md5} (attendu {md5_attendu})")

# --- 1. le dossier preuves-sonde-sys05/ ENTIER ------------------------------
preuves = ds.list_folder(test["id"]).get("preuves-sonde-sys05")
if not preuves:
    print("PAS DE preuves-sonde-sys05/ DANS /test")
    sys.exit(1)

distants = ds.list_folder(preuves["id"])
print(f"\n=== /test/preuves-sonde-sys05/ : {len(distants)} pièce(s) "
      f"— téléchargement + md5 aller-retour ===")
if not distants:
    print("  (le dossier est VIDE)")
    sys.exit(1)

for nom, f in sorted(distants.items()):
    st, data, _ = ds.api(
        "GET", ds.API + f"/files/{f['id']}?alt=media")
    if st != 200:
        print(f"  KO! {nom} : téléchargement HTTP {st}")
        continue
    md5_local = hashlib.md5(data).hexdigest()
    md5_drive = f.get("md5Checksum", "-")
    match = "OK " if md5_local == md5_drive else "KO!"
    (DEST / nom).write_bytes(data)
    print(f"  [{match}] {nom} : {len(data)} o, md5={md5_local}"
          f" (drive: {md5_drive})")

# --- 2. la loi de naissance des pièces (le LISEZMOI du kit) -----------------
print("\n=== loi de naissance (le LISEZMOI du kit, § 2) ===")
attendues = ["temoin-sonde-sys05.txt", "sonde-sys05-journal.log",
             "VERDICT-sonde-sys05.txt", "LISEZMOI-preuves.txt"]
for nom in attendues:
    etat = "PRÉSENT" if nom in distants else "ABSENT"
    print(f"  {etat} : {nom}")
for nom in ["ligne-recue.txt", "journal-emissions.txt"]:
    if nom in distants:
        print(f"  PRÉSENT : {nom}  <- né SEULEMENT si S4 a couru")
    else:
        print(f"  absent  : {nom}  (naît seulement à la percée/mesure)")
