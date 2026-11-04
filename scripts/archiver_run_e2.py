#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_e2.py — LA CLÔTURE D143 DU RUN e2 : les 6 pièces du coffre
preuves-m5b sont DÉPLACÉES dans /test/archives-preuves/preuves-run-e2/,
rejointes par VERDICT-run-e2-vues-vides.txt ; un preuves-m5b VIERGE
(LISEZMOI-preuves.txt seul, liste e2 inchangée — les pièces attendues de
e3 sont les mêmes) est recréé ; l'index LISEZMOI-archives-preuves.txt est
mis à jour EN PLACE.

Chaque geste ASSERTÉ ; chaque mutation RECOUPÉE PAR RELECTURE (D12
étendu — un 200 Drive ne prouve rien). Déplacements par
addParents/removeParents EN REQUÊTE (leçon v7/D143). Aucune suppression,
corbeille jamais vidée. REPRISE-CAPABLE : chaque étape saute ce qui est
déjà fait (recoupé par relecture) — le premier passage s'étant interrompu
mi-chemin (upload_create exige un Path), la reprise repart de l'état
constaté sur le Drive.

Usage : python3 scripts/archiver_run_e2.py
Code de sortie : 0 = clôture faite et recoupée ; 2 = refus nommé.
"""

import hashlib
import json
import pathlib
import sys
import urllib.parse

REPO = "/home/z/my-project/triade-repo"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"     # dossier « test »
PREUVES_LOCAL = pathlib.Path(REPO + "/upload/preuves-e2")
VERDICT_LOCAL = PREUVES_LOCAL / "VERDICT-run-e2-vues-vides.txt"
LISEZMOI_PREUVES_LOCAL = PREUVES_LOCAL / "LISEZMOI-preuves.txt"
INDEX_LOCAL = pathlib.Path(REPO + "/upload/LISEZMOI-archives-preuves.txt")
INDEX_NOUVEAU = pathlib.Path(
    REPO + "/upload/LISEZMOI-archives-preuves-nouveau.txt")

RACINE_ATTENDUE = {
    "LISEZMOI-m5b-e2.txt", "m5b-kit-e2.zip", "scenario-m5b-e2.ps1",
    "corriger-wsb.bat", "corriger-wsb.ps1",
    "preuves-m5b", "archives-livraisons", "archives-preuves",
}
PIECES = [  # (nom, description pour le log)
    ("scenario-m5b-journal.log", "journal du scénario (2 923 o, 19 lignes)"),
    ("LISEZMOI-preuves.txt", "liste des pièces attendues e2 (526 o)"),
    ("autorite-a-console.log", "console de l'autorité A (361 o)"),
    ("autorite-a-err.log", "erreurs de l'autorité A (0 o)"),
    ("proxy-journal.log", "journal du proxy — 128 o, LES 7 LIGNES"),
    ("parefeu-vm.txt", "état parefeu section 0bis (828 o)"),
]
NOM_VERDICT = "VERDICT-run-e2-vues-vides.txt"

SECTION_INDEX = """preuves-run-e2/         Run du 04/11/2026 00:12–00:15Z (kit e2,
                        proxy 0.6.0-rc.1 SCELLÉ 4b8f6af6… — carte
                        génération 7, PREMIER run du flux NAVIGATEUR) :
                        6 pièces + VERDICT-run-e2-vues-vides.txt.
                        ÉCHEC NOMMÉ REFUS PROXY-SANS-ARMEMENT : le
                        scénario a lu le journal proxy à 0 o (garde en
                        live introduite par e2) alors que la pièce
                        post-mortem porte « relever-https arme » —
                        l'ARMEMENT A EU LIEU, le scellé n'est pas en
                        cause ; le navigateur n'a jamais joué, le
                        critère (b) de D136 n'est PAS tranché. Phénomène
                        des « vues vides » (v7/v8, D138) — règle étendue
                        D145 : gardes fonctionnelles ou post-mortem.
"""


def refus(nom, detail):
    print(f"[cloture-e2] REFUS {nom} : {detail}")
    sys.exit(2)


def md5f(chemin):
    return hashlib.md5(pathlib.Path(chemin).read_bytes()).hexdigest()


def deplacer(fid, source, dest):
    url = (ds.API + f"/files/{fid}"
           f"?addParents={dest}&removeParents={source}")
    st, rep, _ = ds.api("PATCH", url, body=b"{}")
    if st not in (200, 204):
        refus("deplacement", f"HTTP {st} : {rep[:120]!r}")


def main():
    test = ds.list_folder(TEST_ID)
    if set(test) != RACINE_ATTENDUE:
        refus("racine-/test", f"{sorted(set(test) ^ RACINE_ATTENDUE)}")
    preuves_id = test["preuves-m5b"]["id"]
    arch_id = test["archives-preuves"]["id"]
    preuves = ds.list_folder(preuves_id)
    arch = ds.list_folder(arch_id)
    noms_pieces = {n for n, _ in PIECES}

    # md5 locaux (les pièces rapatriées font foi)
    md5_locaux = {n: md5f(PREUVES_LOCAL / n) for n, _ in PIECES}
    md5_verdict = md5f(VERDICT_LOCAL)

    # ---- 1. le dossier d'archive (créé si absent, repris sinon) ------------
    if "preuves-run-e2" in arch:
        dest_id = arch["preuves-run-e2"]["id"]
        print(f"[cloture-e2] reprise : preuves-run-e2 existe (id "
              f"{dest_id[:12]}…)")
    else:
        if set(preuves) != noms_pieces:
            refus("preuves-m5b", f"contenu inattendu : {sorted(preuves)}")
        for nom, _ in PIECES:
            if preuves[nom].get("md5Checksum") != md5_locaux[nom]:
                refus("md5", f"{nom} distant != local")
        print("[cloture-e2] état initial conforme : 6 pièces, md5 recoupés")
        st, rep, _ = ds.api("POST", ds.API + "/files", body={
            "name": "preuves-run-e2", "mimeType": ds.FOLDER_MIME,
            "parents": [arch_id]})
        if st != 200:
            refus("creation-dossier", f"HTTP {st} : {rep[:120]!r}")
        dest_id = json.loads(rep)["id"]
        print(f"[cloture-e2] dossier preuves-run-e2 créé (id {dest_id[:12]}…)")
        for nom, _ in PIECES:
            deplacer(preuves[nom]["id"], preuves_id, dest_id)
        preuves = ds.list_folder(preuves_id)

    # ---- 2. les pièces : toutes dans preuves-run-e2, md5 recoupés ---------
    run_e2 = ds.list_folder(dest_id)
    manquantes = noms_pieces - set(run_e2)
    if manquantes:
        # pièces restées dans preuves-m5b (reprise d'un état intermédiaire)
        for nom in sorted(manquantes):
            if nom not in preuves:
                refus("piece-perdue", f"{nom} ni dans preuves-m5b ni dans "
                                      f"preuves-run-e2")
            deplacer(preuves[nom]["id"], preuves_id, dest_id)
        run_e2 = ds.list_folder(dest_id)
        preuves = ds.list_folder(preuves_id)
    if not noms_pieces <= set(run_e2):
        refus("relecture-run-e2", f"il manque : {sorted(noms_pieces - set(run_e2))}")
    for nom, _ in PIECES:
        if run_e2[nom].get("md5Checksum") != md5_locaux[nom]:
            refus("relecture-md5", nom)
    print("[cloture-e2] les 6 pièces sont dans preuves-run-e2, md5 recoupés "
          "par relecture")

    # ---- 3. le verdict les rejoint ------------------------------------------
    if NOM_VERDICT not in run_e2:
        ds.upload_create(dest_id, NOM_VERDICT, VERDICT_LOCAL)
        run_e2 = ds.list_folder(dest_id)
    if run_e2.get(NOM_VERDICT, {}).get("md5Checksum") != md5_verdict:
        refus("verdict-md5", "VERDICT-run-e2-vues-vides.txt distant != local")
    print("[cloture-e2] VERDICT-run-e2-vues-vides.txt déposé, md5 recoupé")

    # ---- 4. preuves-m5b recréé VIERGE ---------------------------------------
    if set(preuves) - {"LISEZMOI-preuves.txt"}:
        refus("preuves-m5b-non-vide", f"{sorted(preuves)}")
    if "LISEZMOI-preuves.txt" not in preuves:
        ds.upload_create(preuves_id, "LISEZMOI-preuves.txt",
                         LISEZMOI_PREUVES_LOCAL)
        preuves = ds.list_folder(preuves_id)
    if set(preuves) != {"LISEZMOI-preuves.txt"}:
        refus("vierge", f"{sorted(preuves)}")
    if (preuves["LISEZMOI-preuves.txt"].get("md5Checksum")
            != md5f(LISEZMOI_PREUVES_LOCAL)):
        refus("vierge-md5", "LISEZMOI-preuves.txt")
    print("[cloture-e2] preuves-m5b recréé VIERGE (LISEZMOI-preuves.txt e2, "
          "md5 recoupé)")

    # ---- 5. l'index mis à jour EN PLACE --------------------------------------
    st, corps, _ = ds.api("GET", ds.API + "/files/"
                          + arch["LISEZMOI-archives-preuves.txt"]["id"]
                          + "?alt=media")
    texte = corps.decode("utf-8")
    if "preuves-run-e2/" in texte:
        print("[cloture-e2] index déjà à jour (reprise)")
    else:
        ancre = "RÈGLE D143 (03/11)"
        if texte.count(ancre) != 1:
            refus("index", f"ancre présente {texte.count(ancre)} fois")
        nouveau = texte.replace(
            "ARCHIVES-PREUVES — INDEX DES RUNS M5-b (règle D143, mis à jour "
            "le 03/11/2026)",
            "ARCHIVES-PREUVES — INDEX DES RUNS M5-b (règle D143, mis à jour "
            "le 04/11/2026)")
        nouveau = nouveau.replace(ancre, SECTION_INDEX + "\n" + ancre)
        INDEX_NOUVEAU.write_text(nouveau, encoding="utf-8", newline="")
        ds.upload_update(arch["LISEZMOI-archives-preuves.txt"]["id"],
                         INDEX_NOUVEAU)
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + arch["LISEZMOI-archives-preuves.txt"]["id"]
                              + "?alt=media")
        if hashlib.md5(corps).hexdigest() != md5f(INDEX_NOUVEAU):
            refus("index-relecture", "md5 distant != md5 local")
        if "preuves-run-e2/" not in corps.decode("utf-8"):
            refus("index-relecture", "section e2 absente du distant")
        print("[cloture-e2] index LISEZMOI-archives-preuves.txt mis à jour "
              "EN PLACE, recoupé par relecture")

    # ---- 6. état final recoupé ----------------------------------------------
    test_final = ds.list_folder(TEST_ID)
    if set(test_final) != RACINE_ATTENDUE:
        refus("racine-finale", f"{sorted(set(test_final) ^ RACINE_ATTENDUE)}")
    arch_final = ds.list_folder(arch_id)
    attendues = set(arch) | {"preuves-run-e2"}
    if set(arch_final) != attendues:
        refus("archives-finale", f"{sorted(set(arch_final) ^ attendues)}")
    print(f"[cloture-e2] CLÔTURE D143 DU RUN e2 FAITE : archives-preuves = "
          f"{len(arch_final)} entrées ; preuves-m5b vierge ; racine /test "
          f"inchangée (8 entrées) ; AUCUNE suppression — la corbeille n'est "
          f"pas vidée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
