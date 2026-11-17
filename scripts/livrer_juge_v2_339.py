#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_juge_v2_339.py — LA LIVRAISON DE LA CORRECTION AU COFFRE /test
(l'Entrée 339 — la correction commandée après la 338) : le kit GUI 1-clic
v2 (LE JUGE RÉPARÉ) et ses TROIS livres, le geste établi de la 331/337 :
upload + recoup md5 par re-téléchargement, échec fermé. Les QUATRE noms
sont NEUFS (le kit v1 et ses livres demeurent au coffre, INTACTS — D143 :
jamais recouverts) :

  kit-gui-1clic-unite02-d210-juge-v2-20261118.zip   LE KIT v2 (23 pièces)
  CORRECTIF-JUGE-V2-UNITE02-D210-20261118.txt       le défaut nommé, la
                                                    réparation livrée
  LISEZMOI-RUN-UNITE02-D210-1CLIC-V2-JUGE-REPARE.txt le livre v2 (copie
    racine du LISEZMOI du kit)
  EMPREINTES-GUI-UNITE02-D210-1CLIC-V2-JUGE-REPARE.txt les empreintes v2
    (copie racine de l'EMPREINTES-GUI du kit)
"""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER = pathlib.Path("/home/z/my-project/download")
V2 = DOSSIER / "TRIADE_gui_unite02_d210_v2"

LIVRAISON = [
    ("kit-gui-1clic-unite02-d210-juge-v2-20261118.zip",
     DOSSIER / "kit-gui-1clic-unite02-d210-juge-v2-20261118.zip"),
    ("CORRECTIF-JUGE-V2-UNITE02-D210-20261118.txt",
     V2 / "CORRECTIF-JUGE-V2-UNITE02-D210-20261118.txt"),
    ("LISEZMOI-RUN-UNITE02-D210-1CLIC-V2-JUGE-REPARE.txt",
     V2 / "LISEZMOI-RUN-UNITE02-D210-1CLIC.txt"),
    ("EMPREINTES-GUI-UNITE02-D210-1CLIC-V2-JUGE-REPARE.txt",
     V2 / "EMPREINTES-GUI-UNITE02-D210-1CLIC.txt"),
]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def main():
    print("=== LA LIVRAISON DE LA CORRECTION AU COFFRE /test "
          "(recoup md5, échec fermé) ===")
    ent = ds.list_folder(TEST_ID)
    for nom, chemin in LIVRAISON:
        md5_local = md5(chemin)
        if nom in ent:
            if ent[nom].get("md5Checksum") == md5_local:
                print(f"[livraison] {nom} : DÉJÀ LIVRÉ byte-byte (md5 "
                      f"{md5_local[:8]}…)")
                continue
            ds.upload_update(ent[nom]["id"], chemin)
            action = "mis à jour"
        else:
            ds.upload_create(TEST_ID, nom, chemin)
            action = "téléversé"
        # LE RECOUP : la fiche relue doit porter le md5 local
        ent2 = ds.list_folder(TEST_ID)
        md5_distant = ent2.get(nom, {}).get("md5Checksum")
        ok = md5_distant == md5_local
        print(f"[livraison] {nom} : {action} "
              f"({chemin.stat().st_size} o), md5 local "
              f"{md5_local[:8]}… / distant {str(md5_distant)[:8]}… "
              f"{'MATCH' if ok else 'ÉCART'}")
        if not ok:
            raise SystemExit(f"[livraison] ÉCART md5 pour {nom}")

    # le kit v1 DEMEURE (D143) : la preuve à la livraison même
    ent3 = ds.list_folder(TEST_ID)
    v1 = ent3.get("kit-gui-1clic-unite02-d210-20261118.zip")
    print("[D143] le kit v1 demeure au /test :", v1 is not None,
          (f"(md5 {str(v1.get('md5Checksum'))[:8]}…, "
           f"{v1.get('size')} o)") if v1 else "(ABSENT — NOMMER L'ÉCART)")

    print("[état] la racine du /test (les entrées de la livraison) :")
    for nom in sorted(ent3):
        if "juge-v2" in nom or "JUGE-REPARE" in nom:
            print("  -", nom, f"({ent3[nom].get('size')} o)")


if __name__ == "__main__":
    main()
