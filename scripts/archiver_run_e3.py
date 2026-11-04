#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_e3.py — LA CLÔTURE D143 DU RUN e3 : les 7 pièces du coffre
preuves-m5b sont DÉPLACÉES dans /test/archives-preuves/preuves-run-e3/,
rejointes par VERDICT-run-e3-rva-nu.txt ; un preuves-m5b VIERGE
(LISEZMOI-preuves.txt seul, liste e3 inchangée — les pièces attendues de
e4 sont les mêmes : le scénario e3 est repris tel quel par le kit e4) est
recréé ; l'index LISEZMOI-archives-preuves.txt est mis à jour EN PLACE.

Chaque geste ASSERTÉ ; chaque mutation RECOUPÉE PAR RELECTURE (D12
étendu — un 200 Drive ne prouve rien). Déplacements par
addParents/removeParents EN REQUÊTE (leçon v7/D143). Aucune suppression,
corbeille jamais vidée. REPRISE-CAPABLE : chaque étape saute ce qui est
déjà fait (recoupé par relecture). Modèle : archiver_run_e2.py.

Usage : python3 scripts/archiver_run_e3.py
Code de sortie : 0 = clôture faite et recoupée ; 2 = refus nommé.
"""

import hashlib
import json
import pathlib
import sys

REPO = "/home/z/my-project/triade-repo"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"     # dossier « test »
PREUVES_LOCAL = pathlib.Path(REPO + "/upload/preuves-e3")
VERDICT_LOCAL = PREUVES_LOCAL / "VERDICT-run-e3-rva-nu.txt"
LISEZMOI_PREUVES_LOCAL = PREUVES_LOCAL / "LISEZMOI-preuves.txt"
INDEX_LOCAL = pathlib.Path(REPO + "/upload/LISEZMOI-archives-preuves.txt")
INDEX_NOUVEAU = pathlib.Path(
    REPO + "/upload/LISEZMOI-archives-preuves-nouveau.txt")

RACINE_ATTENDUE = {
    "LISEZMOI-m5b-e3.txt", "m5b-kit-e3.zip", "scenario-m5b-e3.ps1",
    "corriger-wsb.bat", "corriger-wsb.ps1",
    "preuves-m5b", "archives-livraisons", "archives-preuves",
}
PIECES = [  # (nom, description pour le log)
    ("scenario-m5b-journal.log", "journal du scénario (3 277 o, 21 lignes)"),
    ("autorite-a-console.log", "console de l'autorité A (361 o)"),
    ("autorite-a-err.log", "erreurs de l'autorité A (0 o)"),
    ("edge-version.txt", "version du navigateur par VersionInfo (176 o)"),
    ("page-sonde-armement.txt", "réponse de la sonde d'armement (0 o)"),
    ("parefeu-vm.txt", "état parefeu section 0bis (828 o)"),
    ("proxy-journal.log", "journal du proxy — 134 o, LES 6 LIGNES"),
]
NOM_VERDICT = "VERDICT-run-e3-rva-nu.txt"

SECTION_INDEX = """preuves-run-e3/         Run du 04/11/2026 09:30–09:33Z (kit e3,
                        proxy 0.6.0-rc.1 SCELLÉ 4b8f6af6… — la garde
                        d'armement FONCTIONNELLE, D145) : 7 pièces +
                        VERDICT-run-e3-rva-nu.txt. ÉCHEC NOMMÉ CRASH DU
                        PROXY : la première requête routée jamais envoyée
                        au binaire (la sonde forme-absolue « GET
                        http://127.0.0.1/ ») tue le processus — la ligne
                        de flux (code NOUVEAU 0.6.0) lit l'entrée
                        (RVA, longueur) de la table des méthodes et passe
                        le RVA NU comme pointeur (l'idiome hérité
                        http-02 ajoute la base d'image : il a été perdu) ;
                        lecture à 0x24A0 hors image → violation d'accès.
                        REPRODUIT AU LABO (harnais full-PE unicorn à la
                        base réelle 0x140000000, journal identique ligne
                        à ligne, crash à http-10:R3+0xA46) et PROUVÉ
                        CHIRURGICALEMENT (le correctif simulé fait
                        renaître la ligne de flux et toute la chaîne
                        jusqu'à connect 443). Le proxy ÉTAIT armé
                        (« relever-https arme » au journal) : l'étiquette
                        REFUS PROXY-PAS-ARME est inexacte, la cause est
                        la MORT du processus. Les oracles étaient verts
                        parce que TOUTE l'émulation M5 vit à base 0 (le
                        RVA nu y résout par accident) — règle proposée
                        D146 : contrôle d'exécution À LA BASE RÉELLE
                        avant tout scellage. Le navigateur n'a jamais
                        joué, le critère (b) de D136 n'est PAS tranché ;
                        chemin proposé : notation corrigée + rc.2 (le
                        sceau-I m5 reste valide — l'arbre d'intention ne
                        change pas) + kit e4.
"""


def refus(nom, detail):
    print(f"[cloture-e3] REFUS {nom} : {detail}")
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
    if "preuves-run-e3" in arch:
        dest_id = arch["preuves-run-e3"]["id"]
        print(f"[cloture-e3] reprise : preuves-run-e3 existe (id "
              f"{dest_id[:12]}…)")
    else:
        attendu_initial = noms_pieces | {"LISEZMOI-preuves.txt"}
        if set(preuves) != attendu_initial:
            refus("preuves-m5b", f"contenu inattendu : {sorted(preuves)}")
        for nom, _ in PIECES:
            if preuves[nom].get("md5Checksum") != md5_locaux[nom]:
                refus("md5", f"{nom} distant != local")
        if (preuves["LISEZMOI-preuves.txt"].get("md5Checksum")
                != md5f(LISEZMOI_PREUVES_LOCAL)):
            refus("md5", "LISEZMOI-preuves.txt distant != local")
        print("[cloture-e3] état initial conforme : 8 entrées (7 pièces + "
              "LISEZMOI), md5 recoupés")
        st, rep, _ = ds.api("POST", ds.API + "/files", body={
            "name": "preuves-run-e3", "mimeType": ds.FOLDER_MIME,
            "parents": [arch_id]})
        if st != 200:
            refus("creation-dossier", f"HTTP {st} : {rep[:120]!r}")
        dest_id = json.loads(rep)["id"]
        print(f"[cloture-e3] dossier preuves-run-e3 créé (id {dest_id[:12]}…)")
        for nom, _ in PIECES:
            deplacer(preuves[nom]["id"], preuves_id, dest_id)
        preuves = ds.list_folder(preuves_id)

    # ---- 2. les pièces : toutes dans preuves-run-e3, md5 recoupés ---------
    run_e3 = ds.list_folder(dest_id)
    manquantes = noms_pieces - set(run_e3)
    if manquantes:
        # pièces restées dans preuves-m5b (reprise d'un état intermédiaire)
        for nom in sorted(manquantes):
            if nom not in preuves:
                refus("piece-perdue", f"{nom} ni dans preuves-m5b ni dans "
                                      f"preuves-run-e3")
            deplacer(preuves[nom]["id"], preuves_id, dest_id)
        run_e3 = ds.list_folder(dest_id)
        preuves = ds.list_folder(preuves_id)
    if not noms_pieces <= set(run_e3):
        refus("relecture-run-e3", f"il manque : {sorted(noms_pieces - set(run_e3))}")
    for nom, _ in PIECES:
        if run_e3[nom].get("md5Checksum") != md5_locaux[nom]:
            refus("relecture-md5", nom)
    print("[cloture-e3] les 7 pièces sont dans preuves-run-e3, md5 recoupés "
          "par relecture")

    # ---- 3. le verdict les rejoint ------------------------------------------
    if NOM_VERDICT not in run_e3:
        ds.upload_create(dest_id, NOM_VERDICT, VERDICT_LOCAL)
        run_e3 = ds.list_folder(dest_id)
    if run_e3.get(NOM_VERDICT, {}).get("md5Checksum") != md5_verdict:
        refus("verdict-md5", "VERDICT-run-e3-rva-nu.txt distant != local")
    print("[cloture-e3] VERDICT-run-e3-rva-nu.txt déposé, md5 recoupé")

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
    print("[cloture-e3] preuves-m5b recréé VIERGE (LISEZMOI-preuves.txt e3, "
          "md5 recoupé — la liste vaut pour e4 : le scénario est repris)")

    # ---- 5. l'index mis à jour EN PLACE --------------------------------------
    st, corps, _ = ds.api("GET", ds.API + "/files/"
                          + arch["LISEZMOI-archives-preuves.txt"]["id"]
                          + "?alt=media")
    texte = corps.decode("utf-8")
    if "preuves-run-e3/" in texte:
        print("[cloture-e3] index déjà à jour (reprise)")
    else:
        ancre = "RÈGLE D143 (03/11)"
        if texte.count(ancre) != 1:
            refus("index", f"ancre présente {texte.count(ancre)} fois")
        nouveau = texte.replace(ancre, SECTION_INDEX + "\n" + ancre)
        INDEX_NOUVEAU.write_text(nouveau, encoding="utf-8", newline="")
        ds.upload_update(arch["LISEZMOI-archives-preuves.txt"]["id"],
                         INDEX_NOUVEAU)
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + arch["LISEZMOI-archives-preuves.txt"]["id"]
                              + "?alt=media")
        if hashlib.md5(corps).hexdigest() != md5f(INDEX_NOUVEAU):
            refus("index-relecture", "md5 distant != md5 local")
        if "preuves-run-e3/" not in corps.decode("utf-8"):
            refus("index-relecture", "section e3 absente du distant")
        print("[cloture-e3] index LISEZMOI-archives-preuves.txt mis à jour "
              "EN PLACE, recoupé par relecture")

    # ---- 6. état final recoupé ----------------------------------------------
    test_final = ds.list_folder(TEST_ID)
    if set(test_final) != RACINE_ATTENDUE:
        refus("racine-finale", f"{sorted(set(test_final) ^ RACINE_ATTENDUE)}")
    arch_final = ds.list_folder(arch_id)
    attendues = set(arch) | {"preuves-run-e3"}
    if set(arch_final) != attendues:
        refus("archives-finale", f"{sorted(set(arch_final) ^ attendues)}")
    print(f"[cloture-e3] CLÔTURE D143 DU RUN e3 FAITE : archives-preuves = "
          f"{len(arch_final)} entrées ; preuves-m5b vierge ; racine /test "
          f"inchangée (8 entrées, la vague e3 ATTEND le kit e4) ; AUCUNE "
          f"suppression — la corbeille n'est pas vidée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
