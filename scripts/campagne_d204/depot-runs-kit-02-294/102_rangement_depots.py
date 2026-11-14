#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""102_rangement_depots.py — LE RANGEMENT DES DEUX DÉPÔTS (le précédent 293 :
le dépôt recoupé est DÉPLACÉ, jamais jeté — D143). Les DEUX copies datées
nées au sein des kits (le run 1-clic du LANCEUR : la console + le témoin
signé + les pièces) partent à /test/archives-livraisons/unite-02-loupe-
20261114/ (le nom CONSERVÉ). Chaque fichier md5-recoupé AVANT le geste,
re-listé et re-recoupé APRÈS ; les kits de la racine retrouvent leur état
de livraison 290 (le zip et les pièces libres, rien de plus).

Écritures par LE RELAIS OAUTH du coffre (drive_sync — la voie des
Entrées 288/293 ; le compte de service seul est refusé 403 à l'écriture,
nommé)."""
import json
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

FOLDER_ID = ds.DRIVE_ROOT_ID


def sub(folder_id, name):
    for nom, it in ds.list_folder(folder_id).items():
        if nom == name and it["mimeType"] == ds.FOLDER_MIME:
            return it
    return None


def inventaire(folder_id, prefix=""):
    """{chemin: (id, md5)} de TOUT l'arbre (la preuve AVANT)."""
    inv = {}
    for nom, it in ds.list_folder(folder_id).items():
        chemin = f"{prefix}/{nom}"
        if it["mimeType"] == ds.FOLDER_MIME:
            inv.update(inventaire(it["id"], chemin))
        else:
            inv[chemin] = (it["id"], it.get("md5Checksum", ""))
    return inv


coffre_test = sub(FOLDER_ID, "test")
archives = sub(coffre_test["id"], "archives-livraisons")

# -- l'état AVANT --------------------------------------------------------------
cibles = []
for kit in ("kit-unite-loupe-02-T-20261114", "kit-unite-loupe-02-C-20261114"):
    k = sub(coffre_test["id"], kit)
    assert k, f"{kit} introuvable"
    dep = sub(k["id"], kit)
    assert dep, f"la copie datée de {kit} introuvable"
    avant = inventaire(dep["id"])
    cibles.append((kit, k, dep, avant))
    print(f"[avant] {kit}/{kit} : {len(avant)} fichiers, "
          f"{sum(1 for _, m in avant.values() if m)} md5 consignés")

# -- le dossier d'accueil ------------------------------------------------------
u2 = sub(archives["id"], "unite-02-loupe-20261114")
if u2 is None:
    u2_id = ds.create_folder(archives["id"], "unite-02-loupe-20261114")
    print(f"[créé] /test/archives-livraisons/unite-02-loupe-20261114 (id={u2_id[:12]}…)")
    u2 = {"id": u2_id}
else:
    print(f"[déjà] unite-02-loupe-20261114 vit (id={u2['id'][:12]}…) — idempotent")

# -- LE GESTE : déplacer, jamais jeter -----------------------------------------
for kit, k, dep, avant in cibles:
    deja = sub(u2["id"], kit)
    if deja is not None:
        print(f"[idempotent] {kit} vit déjà à l'archive — rien à faire")
        continue
    st, body, _ = ds.api(
        "PATCH",
        ds.API + f"/files/{dep['id']}?removeParents={k['id']}"
                 f"&addParents={u2['id']}",
        body={})
    if st not in (200, 201):
        print(f"[REFUS] le déplacement de {kit} : HTTP {st} : {body[:200]!r}")
        sys.exit(2)
    print(f"[déplacé] {kit}/{kit} → archives-livraisons/unite-02-loupe-20261114/")

# -- la preuve APRÈS -----------------------------------------------------------
tout_vert = True
for kit, k, dep, avant in cibles:
    k_apres = sub(coffre_test["id"], kit)
    reste = ds.list_folder(k_apres["id"])
    n_apres = len([1 for it in reste.values()
                   if it["mimeType"] != ds.FOLDER_MIME])
    copie = sub(u2["id"], kit)
    if copie is None:
        print(f"[ÉCART] {kit} absent de l'archive après le geste")
        tout_vert = False
        continue
    apres = inventaire(copie["id"])
    if set(apres) != set(avant):
        print(f"[ÉCART] {kit} : l'inventaire diverge "
              f"({len(avant)} avant, {len(apres)} après)")
        tout_vert = False
    for chemin, (fid, md5) in avant.items():
        if apres.get(chemin, (None, None))[1] != md5:
            print(f"[ÉCART] {kit}{chemin} : md5 muté au geste")
            tout_vert = False
    imbrique = sub(k_apres["id"], kit)
    if imbrique is not None:
        print(f"[ÉCART] la copie datée demeure au kit {kit}")
        tout_vert = False
    print(f"[après] {kit} : {n_apres} pièces libres à la racine du kit "
          f"(l'état de livraison 290), la copie datée à l'archive : "
          f"{len(apres)} fichiers md5 INTACTS")

racine_test = len(ds.list_folder(coffre_test["id"]))
print(f"\n[rangement] la racine du /test : {racine_test} entrées "
      f"(inchangée — les dépôts vivaient AU SEIN des kits)")
if tout_vert:
    print("[rangement] TOUT VERT — D143 tenu : déplacés, jamais jetés, "
          "md5 par md5")
else:
    print("[rangement] ÉCARTS NOMMÉS CI-DESSUS")
sys.exit(0 if tout_vert else 2)
