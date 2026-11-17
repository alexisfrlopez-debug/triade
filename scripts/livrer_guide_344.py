#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_guide_344.py — LA LIVRAISON DU GUIDE DE LA LIGNE DE CARNET au
coffre /test (l'Entrée 344, le geste établi des livrer_* : upload + recoup
md5 par re-téléchargement, échec fermé) : GUIDE-LIGNE-CARNET-ET-SUITE-
20261118.txt (le guide du geste des lignes au livre — les DEUX lignes D210
attendues par livraisons.csv et le carnet M3, puis la suite de la campagne)
à la RACINE du /test, aux côtés des guides précédents (GUIDE-GESTE-
TERRAIN-ET-SUITE, les GUIDE-CORRECTIONS-LIVRE). La copie de l'utilisateur
naît à download/ du bac principal."""
import hashlib
import pathlib
import shutil
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
BAC = REPO / "scripts" / "campagne_d204" / "guide-ligne-carnet-344"
GUIDE = BAC / "GUIDE-LIGNE-CARNET-ET-SUITE-20261118.txt"
NOM = GUIDE.name
DOWNLOAD = pathlib.Path("/home/z/my-project/download")


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
    if not GUIDE.is_file():
        print("[ÉCART] le guide absent du bac : " + str(GUIDE))
        return 1
    md5_local = md5f(GUIDE)
    print(f"[livraison] {NOM} ({GUIDE.stat().st_size} o, md5 "
          f"{md5_local[:12]}…) :")

    ent = ds.list_folder(TEST_ID)
    if NOM in ent:
        if ent[NOM].get("md5Checksum") == md5_local:
            print("[livraison] DÉJÀ LIVRÉ byte-byte — idempotent")
        else:
            ds.upload_update(ent[NOM]["id"], GUIDE)
            print("[livraison] mis à jour (remplacement en place, D143)")
    else:
        ds.upload_create(TEST_ID, NOM, GUIDE)
        print("[livraison] téléversé à la racine du /test")

    # LE RECOUP : la pièce relue (re-téléchargée) doit porter le md5 local
    ent2 = ds.list_folder(TEST_ID)
    it = ent2.get(NOM)
    if it is None:
        print("[ÉCART] le guide absent du /test après le geste")
        return 1
    md5_distant = it.get("md5Checksum", "")
    relue = telecharge(it["id"])
    ok = (md5_distant == md5_local) and (
        hashlib.md5(relue).hexdigest() == md5_local)
    print(f"[livraison] RECOUPE md5 {md5_local[:12]}… "
          f"{'MATCH (re-téléchargé byte-byte)' if ok else 'ÉCART'}")

    # LA COPIE DE L'UTILISATEUR au download/ du bac principal
    DOWNLOAD.mkdir(parents=True, exist_ok=True)
    shutil.copy2(GUIDE, DOWNLOAD / NOM)
    print(f"[copie] {NOM} → download/ ({(DOWNLOAD / NOM).stat().st_size} o)")

    # L'ÉTAT de la racine après le geste
    ent3 = ds.list_folder(TEST_ID)
    guides = sorted(n for n in ent3 if n.startswith("GUIDE"))
    print(f"[état] la racine du /test : {len(ent3)} entrées ; les guides :")
    for g in guides:
        print("  -", g)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
