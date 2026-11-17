#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ranger_livrer_343.py — LE RANGEMENT DU DÉPÔT + LA LIVRAISON DU RAPPORT
(l'Entrée 343). LE RANGEMENT (le précédent 293/294/295/304/340 : le dépôt
recoupé est DÉPLACÉ-RENOMMÉ, jamais jeté — D143) : le dossier kit-unite-02-
d210-20261118/ né au /test le 17/11 23:10:27Z (le run terrain de l'unité
02 D210 LOUPE-08 LIGNE × BRAS T au kit GUI 1-clic livré à la 342 — le kit
DÉZIPPÉ + les preuves nées du run, recoupé 10/10 VERT au RECOUP-343) part
à /test/archives-livraisons/unite-08-d210-20261118/kit-unite-02-d210-
20261118-RUN-V1-VERT-20261118/ (le nom de l'unité loupe-08 — comme
l'archive unite-02-d210-20261118/ porte le nom du run loupe-02 de la 338 ;
chaque fichier md5-recoupé AVANT le geste, re-listé et re-recoupé APRÈS).
LA LIVRAISON (le précédent 333/338/340 : le rapport de réception au
/test) : RAPPORT-RECEPTION-RUN-UNITE08-D210-TERRAIN-20261118.txt == le
RECOUP-343-preuves-unite08.txt du bac, téléversé puis RE-TÉLÉCHARGÉ et
md5-recoupé (échec fermé)."""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite08-d210-343"
RAPPORT = BAC / "RECOUP-343-preuves-unite08.txt"
NOM_RAPPORT = "RAPPORT-RECEPTION-RUN-UNITE08-D210-TERRAIN-20261118.txt"
NOM_ARCHIVE = "kit-unite-02-d210-20261118-RUN-V1-VERT-20261118"
DOSSIER_ID = "1oxnULtkeTicLvqBlDeVhB06_GCaTBKqH"  # kit-unite-02-d210-20261118/
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


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

    # -- l'état AVANT ----------------------------------------------------------
    dep = sub(TEST_ID, "kit-unite-02-d210-20261118")
    if dep is None:
        print("[idempotent] kit-unite-02-d210-20261118/ n'est plus à la "
              "racine — le rangement fut déjà vécu")
    elif dep["id"] != DOSSIER_ID:
        print(f"[ÉCART] kit-unite-02-d210-20261118/ à la racine porte "
              f"l'id {dep['id']} — ce n'est pas le dépôt attendu "
              f"({DOSSIER_ID}) : ARRÊT, rien n'est déplacé")
        tout_vert = False
    else:
        avant = inventaire(dep["id"])
        print(f"[avant] kit-unite-02-d210-20261118/ (le dépôt du run "
              f"unite08) : {len(avant)} fichier(s)")
        for chemin, (fid, md5_avant) in sorted(avant.items()):
            print(f"  {chemin} : md5 {md5_avant}")

        archives = sub(TEST_ID, "archives-livraisons")
        assert archives, "archives-livraisons/ introuvable"
        u8 = sub(archives["id"], "unite-08-d210-20261118")
        if u8 is None:
            u8_id = ds.create_folder(archives["id"], "unite-08-d210-20261118")
            print("[créé] archives-livraisons/unite-08-d210-20261118/ "
                  "(le nom de l'unité loupe-08 — le précédent "
                  "unite-02-d210-20261118/ porte le run loupe-02)")
        else:
            u8_id = u8["id"]
            print("[constat] l'archive unite-08-d210-20261118/ existe déjà")

        deja = sub(u8_id, NOM_ARCHIVE)
        if deja is not None:
            print(f"[idempotent] {NOM_ARCHIVE}/ vit déjà à l'archive — "
                  "rien à déplacer")
        else:
            # -- LE GESTE : déplacer-renommer, jamais jeter --------------------
            st, body, _ = ds.api(
                "PATCH",
                ds.API + (f"/files/{dep['id']}"
                          f"?removeParents={TEST_ID}"
                          f"&addParents={u8_id}"),
                body={"name": NOM_ARCHIVE})
            if st not in (200, 201):
                print(f"[REFUS] le déplacement-renommage : HTTP {st} : "
                      f"{body[:200]!r}")
                sys.exit(2)
            print(f"[déplacé-renommé] kit-unite-02-d210-20261118/ → "
                  f"archives-livraisons/unite-08-d210-20261118/"
                  f"{NOM_ARCHIVE}/")

        # -- la preuve APRÈS ----------------------------------------------------
        copie = sub(u8_id, NOM_ARCHIVE)
        if copie is None:
            print(f"[ÉCART] {NOM_ARCHIVE}/ absent de l'archive après le "
                  "geste")
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
                    print(f"[ÉCART] {NOM_ARCHIVE}{chemin} : md5 muté au "
                          "geste")
                    tout_vert = False
                else:
                    print(f"[après] {NOM_ARCHIVE}{chemin} : md5 "
                          f"{md5_apres} == AVANT, INTACT")
        if sub(TEST_ID, "kit-unite-02-d210-20261118") is not None:
            print("[ÉCART] kit-unite-02-d210-20261118/ demeure à la racine "
                  "du /test")
            tout_vert = False

    # -- LA LIVRAISON DU RAPPORT AU /test --------------------------------------
    print(f"[livraison] {NOM_RAPPORT} ({RAPPORT.stat().st_size} o) :")
    ent = ds.list_folder(TEST_ID)
    md5_local = md5f(RAPPORT)
    if NOM_RAPPORT in ent:
        if ent[NOM_RAPPORT].get("md5Checksum") == md5_local:
            print(f"[livraison] DÉJÀ LIVRÉ byte-byte (md5 {md5_local[:8]}…)")
        else:
            ds.upload_update(ent[NOM_RAPPORT]["id"], RAPPORT)
            print("[livraison] mis à jour")
    else:
        ds.upload_create(TEST_ID, NOM_RAPPORT, RAPPORT)
        print("[livraison] téléversé")
    ent2 = ds.list_folder(TEST_ID)
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
    ent3 = ds.list_folder(TEST_ID)
    print(f"[état] la racine du /test : {len(ent3)} entrées ; les "
          "récentes :")
    for nom in sorted(ent3):
        if "D210" in nom or "20261118" in nom:
            print("  -", nom)
    print("[rangement+livraison] TOUT VERT — D143 tenu : déplacé-renommé, "
          "jamais jeté, md5 recoupé avant/après ; le rapport livré et "
          "recoupé"
          if tout_vert else
          "[rangement+livraison] ÉCARTS NOMMÉS ci-dessus")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
