#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_gui_unite08_342.py — LA LIVRAISON AU COFFRE /test du GUI
1-CLIC DE L'UNITÉ 02 D210 (l'Entrée 342 — la suite ① annoncée à la 341,
le précédent de la 337) : le kit zip + ses DEUX livres, le geste établi
de la 331/337 : upload + recoup md5 par re-téléchargement, échec fermé.
Les TROIS noms sont NEUFS (les kits de l'unité 01 — le v1 ET le v2 au
juge réparé — demeurent au coffre, INTACTS — D143 : jamais recouverts) :

  kit-gui-1clic-unite08-d210-20261118.zip   LE KIT GUI (18 pièces, la
                                            racine kit-unite-02-d210-
                                            20261118/)
  LISEZMOI-RUN-UNITE08-D210-1CLIC.txt       le livre du kit (copie
                                            racine du LISEZMOI du kit)
  EMPREINTES-GUI-UNITE08-D210-1CLIC.txt     les empreintes (copie
                                            racine de l'EMPREINTES-GUI)

AUCUN CORRECTIF ne vit cette livraison : le juge du kit est D204
INCHANGÉ (44384f5d…, la version corrigée) et la gravure NÉE PARSÉE —
les deux défauts de l'unité 01 (le T0 de la 337, le juge de la 338)
ne se reproduisent pas, NOMMÉS au LISEZMOI PARCE QU'ILS NE SE
REPRODUISENT PAS (D202)."""
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER = pathlib.Path("/home/z/my-project/download")
KIT = DOSSIER / "TRIADE_gui_unite08_d210_v1"

LIVRAISON = [
    ("kit-gui-1clic-unite08-d210-20261118.zip",
     DOSSIER / "kit-gui-1clic-unite08-d210-20261118.zip"),
    ("LISEZMOI-RUN-UNITE08-D210-1CLIC.txt",
     KIT / "LISEZMOI-RUN-UNITE08-D210-1CLIC.txt"),
    ("EMPREINTES-GUI-UNITE08-D210-1CLIC.txt",
     KIT / "EMPREINTES-GUI-UNITE08-D210-1CLIC.txt"),
]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def main():
    print("=== LA LIVRAISON AU COFFRE /test du GUI 1-CLIC UNITE08 "
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

    # D143 — les kits de l'unité 01 DEMEURENT (la preuve à la livraison
    # même) : le v1 ET le v2 au juge réparé
    ent3 = ds.list_folder(TEST_ID)
    for ancien in ("kit-gui-1clic-unite02-d210-20261118.zip",
                   "kit-gui-1clic-unite02-d210-juge-v2-20261118.zip"):
        v = ent3.get(ancien)
        print(f"[D143] {ancien} demeure au /test : "
              f"{v is not None}"
              + (f" (md5 {str(v.get('md5Checksum'))[:8]}…, "
                 f"{v.get('size')} o)" if v else " (ABSENT — NOMMER "
                 "L'ÉCART)"))

    print("[état] la racine du /test (les entrées unite08) :")
    for nom in sorted(ent3):
        if "unite08" in nom:
            print("  -", nom, f"({ent3[nom].get('size')} o)")


if __name__ == "__main__":
    main()
