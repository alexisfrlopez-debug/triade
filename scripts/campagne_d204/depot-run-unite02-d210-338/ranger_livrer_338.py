#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ranger_livrer_338.py — LE RANGEMENT DU DÉPÔT + LA LIVRAISON DU RAPPORT
(l'Entrée 338). LE RANGEMENT (le précédent 293/294/295 : le dépôt recoupé
est DÉPLACÉ, jamais jeté — D143) : le dossier preuves-unite02/ né au /test
le 17/11 19:03:26Z (le run terrain de l'unité 02 D210 au kit GUI 1-clic,
recoupé 10/10 VERT au RECOUP-338) part à /test/archives-livraisons/
unite-02-d210-20261118/preuves-unite02/ (le nom CONSERVÉ, chaque fichier
md5-recoupé AVANT le geste, re-listé et re-recoupé APRÈS). LA LIVRAISON (le
précédent 333 : le rapport de réception au /test) :
RAPPORT-RECEPTION-RUN-UNITE02-D210-TERRAIN-20261118.txt == le
RECOUP-338-preuves-unite02.txt du bac, téléversé puis RE-TÉLÉCHARGÉ et
md5-recoupé (échec fermé)."""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite02-d210-338"
RAPPORT = BAC / "RECOUP-338-preuves-unite02.txt"
NOM_RAPPORT = "RAPPORT-RECEPTION-RUN-UNITE02-D210-TERRAIN-20261118.txt"


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


def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def telecharge(file_id):
    st, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    if st != 200:
        raise RuntimeError(f"téléchargement impossible ({st})")
    return body


def main():
    tout_vert = True
    coffre_test = sub(ds.DRIVE_ROOT_ID, "test")
    assert coffre_test, "le /test introuvable"

    # -- l'état AVANT ----------------------------------------------------------
    dep = sub(coffre_test["id"], "preuves-unite02")
    if dep is None:
        print("[idempotent] preuves-unite02/ n'est plus à la racine — "
              "le rangement fut déjà vécu")
    else:
        avant = inventaire(dep["id"])
        print(f"[avant] preuves-unite02/ : {len(avant)} fichier(s)")
        for chemin, (fid, md5_avant) in sorted(avant.items()):
            print(f"  {chemin} : md5 {md5_avant}")

        archives = sub(coffre_test["id"], "archives-livraisons")
        assert archives, "archives-livraisons/ introuvable"
        u2 = sub(archives["id"], "unite-02-d210-20261118")
        if u2 is None:
            u2_id = ds.create_folder(archives["id"], "unite-02-d210-20261118")
            print("[créé] archives-livraisons/unite-02-d210-20261118/")
        else:
            u2_id = u2["id"]

        deja = sub(u2_id, "preuves-unite02")
        if deja is not None:
            print("[idempotent] preuves-unite02/ vit déjà à l'archive — "
                  "rien à déplacer")
        else:
            # -- LE GESTE : déplacer, jamais jeter ---------------------------
            st, body, _ = ds.api(
                "PATCH",
                ds.API + f"/files/{dep['id']}?removeParents={coffre_test['id']}"
                         f"&addParents={u2_id}",
                body={})
            if st not in (200, 201):
                print(f"[REFUS] le déplacement : HTTP {st} : {body[:200]!r}")
                sys.exit(2)
            print("[déplacé] preuves-unite02/ → archives-livraisons/"
                  "unite-02-d210-20261118/")

        # -- la preuve APRÈS ----------------------------------------------------
        copie = sub(u2_id, "preuves-unite02")
        if copie is None:
            print("[ÉCART] preuves-unite02/ absent de l'archive après le geste")
            tout_vert = False
        else:
            apres = inventaire(copie["id"])
            if set(apres) != set(avant):
                print(f"[ÉCART] l'inventaire diverge ({len(avant)} avant, "
                      f"{len(apres)} après)")
                tout_vert = False
            for chemin, (fid, md5_avant) in sorted(avant.items()):
                md5_apres = apres.get(chemin, (None, None))[1]
                if md5_apres != md5_avant:
                    print(f"[ÉCART] preuves-unite02{chemin} : md5 muté au geste")
                    tout_vert = False
                else:
                    print(f"[après] preuves-unite02{chemin} : md5 "
                          f"{md5_apres} == AVANT, INTACT")
        if sub(coffre_test["id"], "preuves-unite02") is not None:
            print("[ÉCART] preuves-unite02/ demeure à la racine du /test")
            tout_vert = False

    # -- LA LIVRAISON DU RAPPORT AU /test --------------------------------------
    print(f"[livraison] {NOM_RAPPORT} ({RAPPORT.stat().st_size} o) :")
    ent = ds.list_folder(coffre_test["id"])
    md5_local = md5f(RAPPORT)
    if NOM_RAPPORT in ent:
        if ent[NOM_RAPPORT].get("md5Checksum") == md5_local:
            print(f"[livraison] DÉJÀ LIVRÉ byte-byte (md5 {md5_local[:8]}…)")
        else:
            ds.upload_update(ent[NOM_RAPPORT]["id"], RAPPORT)
            print(f"[livraison] mis à jour")
    else:
        ds.upload_create(coffre_test["id"], NOM_RAPPORT, RAPPORT)
        print("[livraison] téléversé")
    ent2 = ds.list_folder(coffre_test["id"])
    md5_distant = ent2.get(NOM_RAPPORT, {}).get("md5Checksum")
    # LE RECOUP : la pièce relue (re-téléchargée) doit porter le md5 local
    if md5_distant == md5_local:
        relue = telecharge(ent2[NOM_RAPPORT]["id"])
        ok = hashlib.md5(relue).hexdigest() == md5_local
        print(f"[livraison] RECOUPE md5 {md5_local[:8]}… "
              f"{'MATCH (re-téléchargé byte-byte)' if ok else 'ÉCART'}")
        tout_vert &= ok
    else:
        print(f"[livraison] ÉCART md5 : local {md5_local[:8]}… / distant "
              f"{str(md5_distant)[:8]}…")
        tout_vert = False

    # -- l'état final de la racine du /test -------------------------------------
    ent3 = ds.list_folder(coffre_test["id"])
    print(f"[état] la racine du /test : {len(ent3)} entrées ; les récentes :")
    for nom in sorted(ent3):
        if "D210" in nom or "20261118" in nom:
            print("  -", nom)
    print("[rangement+livraison] TOUT VERT — D143 tenu : déplacé, jamais "
          "jeté, md5 recoupé ; le rapport livré et recoupé"
          if tout_vert else "[rangement+livraison] ÉCARTS NOMMÉS ci-dessus")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
