#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""105_rangement_preuves.py — LE RANGEMENT DU DÉPÔT preuves-unite02/ (le
précédent 293/294 : le dépôt recoupé est DÉPLACÉ, jamais jeté — D143).
Le dossier né au /test le 14/11 20:00:17Z (le run v2 du bras T, recoupé
7/7 VERT à la sonde 104) part à /test/archives-livraisons/unite-02-
loupe-20261114/preuves-unite02/ (le nom CONSERVÉ). Chaque fichier
md5-recoupé AVANT le geste, re-listé et re-recoupé APRÈS.

Écriture par LE RELAIS OAUTH du coffre (drive_sync — la voie des Entrées
288/293/294 ; le compte de service seul est refusé 403 à l'écriture,
nommé)."""
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402


def sub(folder_id, name):
    for nom, it in ds.list_folder(folder_id).items():
        if nom == name and it["mimeType"] == ds.FOLDER_MIME:
            return it
    return None


def inventaire(folder_id, prefix=""):
    inv = {}
    for nom, it in ds.list_folder(folder_id).items():
        chemin = f"{prefix}/{nom}"
        if it["mimeType"] == ds.FOLDER_MIME:
            inv.update(inventaire(it["id"], chemin))
        else:
            inv[chemin] = (it["id"], it.get("md5Checksum", ""))
    return inv


coffre_test = sub(ds.DRIVE_ROOT_ID, "test")
assert coffre_test, "le /test introuvable"

# -- l'état AVANT --------------------------------------------------------------
dep = sub(coffre_test["id"], "preuves-unite02")
assert dep, "preuves-unite02/ introuvable à la racine du /test"
avant = inventaire(dep["id"])
assert len(avant) == 1, f"le dépôt porte {len(avant)} fichiers (1 attendu)"
chemin, (fid, md5_avant) = next(iter(avant.items()))
print(f"[avant] preuves-unite02{chemin} : id={fid[:12]}…, md5 {md5_avant}")

archives = sub(coffre_test["id"], "archives-livraisons")
assert archives, "archives-livraisons/ introuvable"
u2 = sub(archives["id"], "unite-02-loupe-20261114")
assert u2, "unite-02-loupe-20261114/ introuvable (la 294 l'avait créé)"

# -- idempotence ----------------------------------------------------------------
deja = sub(u2["id"], "preuves-unite02")
if deja is not None:
    print(f"[idempotent] preuves-unite02/ vit déjà à l'archive — rien à faire")
    sys.exit(0)

# -- LE GESTE : déplacer, jamais jeter -----------------------------------------
st, body, _ = ds.api(
    "PATCH",
    ds.API + f"/files/{dep['id']}?removeParents={coffre_test['id']}"
             f"&addParents={u2['id']}",
    body={})
if st not in (200, 201):
    print(f"[REFUS] le déplacement : HTTP {st} : {body[:200]!r}")
    sys.exit(2)
print("[déplacé] preuves-unite02/ → archives-livraisons/unite-02-loupe-20261114/")

# -- la preuve APRÈS -----------------------------------------------------------
tout_vert = True
copie = sub(u2["id"], "preuves-unite02")
if copie is None:
    print("[ÉCART] preuves-unite02/ absent de l'archive après le geste")
    tout_vert = False
else:
    apres = inventaire(copie["id"])
    if set(apres) != set(avant):
        print(f"[ÉCART] l'inventaire diverge ({len(avant)} avant, {len(apres)} après)")
        tout_vert = False
    for chemin, (fid, md5) in avant.items():
        if apres.get(chemin, (None, None))[1] != md5:
            print(f"[ÉCART] preuves-unite02{chemin} : md5 muté au geste")
            tout_vert = False
    print(f"[après] l'archive porte preuves-unite02{chemin} : "
          f"md5 {apres[chemin][1]} {'== AVANT, INTACT' if apres[chemin][1] == md5_avant else 'MUTÉ'}")
reste = sub(coffre_test["id"], "preuves-unite02")
if reste is not None:
    print("[ÉCART] preuves-unite02/ demeure à la racine du /test")
    tout_vert = False
n_racine = len(ds.list_folder(coffre_test["id"]))
print(f"[après] la racine du /test : {n_racine} entrées (14 - le dépôt rangé)")
if tout_vert:
    print("[rangement] TOUT VERT — D143 tenu : déplacé, jamais jeté, md5 recoupé")
sys.exit(0 if tout_vert else 2)
