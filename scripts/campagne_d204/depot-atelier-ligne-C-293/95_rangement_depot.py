#!/usr/bin/env python3
"""95_rangement_depot.py — LE RANGEMENT du dépôt de l'atelier (la 293) :
le dossier atelier-campagne-d204-20261114-013520 déposé à la RACINE du
/test (15:54:52Z) est DÉPLACÉ — jamais jeté — à
/test/archives-livraisons/unite-01-loupe-20261114/ (le geste de la 289 :
les dépôts recoupés vont à l'archive de l'unité), SON NOM CONSERVÉ
(l'identité canonique du livre, la même qu'à la machine du développeur)."""
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

NOM_ATELIER = "atelier-campagne-d204-20261114-013520"


def refus(nom, detail):
    print(f"[rangement] REFUS {nom} : {detail}")
    sys.exit(2)


# -- 0. les dossiers -------------------------------------------------------
coffre_test = ds.list_folder(ds.DRIVE_ROOT_ID).get("test") or refus(
    "ETAT", "/test introuvable")
racine = ds.list_folder(coffre_test["id"])
atelier = racine.get(NOM_ATELIER) or refus(
    "ETAT", f"{NOM_ATELIER} n'est plus à la racine du /test")
if atelier["mimeType"] != ds.FOLDER_MIME:
    refus("ETAT", f"{NOM_ATELIER} n'est pas un dossier")
archives = racine.get("archives-livraisons") or refus(
    "ETAT", "archives-livraisons/ introuvable")
unite01 = ds.list_folder(archives["id"]).get("unite-01-loupe-20261114") or refus(
    "ETAT", "unite-01-loupe-20261114/ introuvable")
print(f"[0] l'atelier à la racine : {NOM_ATELIER} (id={atelier['id'][:12]}…) ; "
      f"l'archive cible : unite-01-loupe-20261114/ (id={unite01['id'][:12]}…)")

# -- l'idempotence : déjà rangé ? -------------------------------------------
deja = ds.list_folder(unite01["id"]).get(NOM_ATELIER)
if deja:
    print(f"[idempotent] {NOM_ATELIER} vit déjà à l'archive "
          f"(id={deja['id'][:12]}…) — vérification de la racine :")
    racine2 = ds.list_folder(coffre_test["id"]).get(NOM_ATELIER)
    print(f"    la racine {'ne porte PLUS le dossier' if racine2 is None else 'porte ENCORE le dossier — ÉCART'}")
    sys.exit(0)

# -- 1. le déplacement (addParents/removeParents, JAMAIS une suppression) ---
st, body, _ = ds.api(
    "PATCH",
    ds.API + f"/files/{atelier['id']}?removeParents={coffre_test['id']}"
             f"&addParents={unite01['id']}",
    body={})
if st not in (200, 201):
    refus("DEPLACEMENT", f"HTTP {st} : {body[:200]!r}")
print(f"[1] DÉPLACÉ : {NOM_ATELIER} → archives-livraisons/unite-01-loupe-20261114/")

# -- 2. le recoup PAR RE-LECTURE --------------------------------------------
racine2 = ds.list_folder(coffre_test["id"])
if NOM_ATELIER in racine2:
    refus("RECOUP", "le dossier demeure à la racine du /test")
archive_lst = ds.list_folder(unite01["id"])
if NOM_ATELIER not in archive_lst:
    refus("RECOUP", "le dossier n'apparaît pas à l'archive")
n_avant = len([n for n in racine if True])
n_apres = len(racine2)
print(f"[2] RECOUP : la racine porte {n_avant} → {n_apres} entrées ; "
      f"l'archive porte {len(archive_lst)} entrées — dont {NOM_ATELIER}")

# -- 3. les QUATRE pièces du bac == le dépôt recoupé (le déplacement ne
# touche JAMAIS le contenu ; les sha256 ci-dessous sont ceux du dépôt
# téléchargé AVANT le rangement — le recoup de la 293) ---------------------
import hashlib  # noqa: E402
for nom, attendu in [
    ("livraisons.csv", "f0afea11515d1f0b"),
    ("carnet_temps_humain.csv", "01de5e13cc2c6de5"),
    ("defauts.csv", "e2756e76a84ac9c5"),
    ("journal-ouverture.txt", "4c036f089e3fbb96"),
]:
    chemin = ("/home/z/my-project/work/triade/scripts/campagne_d204/"
              f"depot-atelier-ligne-C-293/epreuves/depot-racine/{nom}")
    sha = hashlib.sha256(open(chemin, "rb").read()).hexdigest()
    print(f"    (bac) {nom}  sha256 {sha[:16]}…  == le dépôt recoupé "
          f"{'OUI' if sha.startswith(attendu) else 'NON — ÉCART'}")

print("[3] le rangement tenu : déplacé, jamais jeté (D143) ; "
      "la racine du /test retrouve ses entrées attendues.")
