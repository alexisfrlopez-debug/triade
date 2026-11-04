#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_e4.py — LA CLÔTURE D143 DU RUN e4 : les 36 pièces du coffre
preuves-m5b sont DÉPLACÉES dans /test/archives-preuves/preuves-run-e4/,
rejointes par VERDICT-run-e4-critere-b.txt ; le LISEZMOI-preuves.txt (liste
e4) DEMEURE en place — un preuves-m5b VIERGE l'attend ; l'index
LISEZMOI-archives-preuves.txt est mis à jour EN PLACE.

Chaque geste ASSERTÉ ; chaque mutation RECOUPÉE PAR RELECTURE (D12
étendu — un 200 Drive ne prouve rien). Déplacements par
addParents/removeParents EN REQUÊTE (leçon v7/D143). Aucune suppression,
corbeille jamais vidée. REPRISE-CAPABLE : chaque étape saute ce qui est
déjà fait (recoupé par relecture). Modèle : archiver_run_e3.py.

Usage : python3 scripts/archiver_run_e4.py
Code de sortie : 0 = clôture faite et recoupée ; 2 = refus nommé.
"""

import hashlib
import json
import pathlib
import sys
import time

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"     # dossier « test »
PREUVES_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-run-e4")
VERDICT_LOCAL = PREUVES_LOCAL / "VERDICT-run-e4-critere-b.txt"
INDEX_NOUVEAU = pathlib.Path("/tmp/LISEZMOI-archives-preuves-nouveau.txt")

RACINE_ATTENDUE = {
    "LISEZMOI-m5b-e4.txt", "m5b-kit-e4.zip", "scenario-m5b-e4.ps1",
    "corriger-wsb.bat", "corriger-wsb.ps1",
    "preuves-m5b", "archives-livraisons", "archives-preuves",
}
PIECES = [  # les 36 pièces du run (le LISEZMOI-preuves.txt reste en place)
    "autorite-a-console.log", "autorite-a-err.log", "autorite-a.log",
    "autorite-b-console.log", "autorite-b-err.log", "autorite-b.log",
    "autorite-d-console.log", "autorite-d-err.log", "autorite-d.log",
    "autorite-e-console.log", "autorite-e-err.log", "autorite-e.log",
    "curl-d2a.txt", "curl-d2b.txt", "curl-d3.txt", "curl-d5.txt",
    "dnscache.txt", "dom-a.txt", "dom-b.txt", "edge-version.txt",
    "hosts-lu.txt", "ipconfig-vm.txt",
    "nav-a-cap-err.txt", "nav-a-err.txt", "nav-a.png",
    "nav-b-cap-err.txt", "nav-b-err.txt",
    "page-d2a.txt", "page-d2b.txt", "page-d3.txt", "page-d5.txt",
    "page-sonde-armement.txt", "parefeu-vm.txt",
    "proxy-journal.log", "scenario-m5b-journal.log", "temoin-m5b.txt",
]
NOM_VERDICT = "VERDICT-run-e4-critere-b.txt"

SECTION_INDEX = """preuves-run-e4/         Run du 04/11/2026 12:06–12:12Z (kit e4,
                        proxy 0.6.0-rc.2 SCELLÉ c1e46fb0… — le scénario
                        e3 repris TEL QUEL, proxy remplacé) : 36 pièces +
                        VERDICT-run-e4-critere-b.txt. LE CRITÈRE (b) DE
                        D136 PRÉSENT SUR PIÈCES : la page de l'autorité
                        REÇUE ET RENDUE PAR LE NAVIGATEUR (dom-a.txt au
                        marqueur TRIADE-M5B-PAGE-200, capture nav-a.png
                        13 081 o, autorité A 5 requêtes servies PAR LE
                        TUNNEL) ET la 502 « Certificat rejete » REÇUE PAR
                        LE NAVIGATEUR (certificat auto-signé examiné puis
                        rejeté : « certificat rejete » + flux v=3 e=736
                        s=34 ×2 au journal proxy, poignée refusée ×3 à
                        l'autorité B, ERR_HTTP_RESPONSE_CODE_FAILURE ×2
                        chez Edge — réception TRIPLEMENT recroisée) —
                        LES DEUX DANS LE MÊME RUN. LE CRASH e3 GUÉRI à la
                        base réelle : la première requête routée qui tua
                        le rc.1 (la sonde 51 o) est servie — « flux GET
                        127.0.0.1:443 v=0 e=51 », page-sonde-armement.txt
                        NÉE (452 o). Le verdict du scénario « ÉCHEC NOMMÉ
                        (5) » est un artefact d'instrument (D138) : rc
                        Edge capturé vide, vues vides des journaux
                        vivants (RÉSERVES prévues empoisonnées par le rc
                        vide), DOM d'erreur vide PAR CONSTRUCTION (502
                        nue 34 o sans corps — le headless n'émet ni DOM
                        ni capture pour une navigation échouée). Matrice
                        curl IDENTIQUE au run v8 octet pour octet (S3
                        stationnaire, aucune régression). CONSÉQUENCE :
                        LA FINALE 0.6.0 SCELLÉE au geste même (Entrée
                        143, D148) — le jalon M5 RENTRÉ.
"""


def refus(nom, detail):
    print(f"[cloture-e4] REFUS {nom} : {detail}")
    sys.exit(2)


def md5f(chemin):
    return hashlib.md5(pathlib.Path(chemin).read_bytes()).hexdigest()


def deplacer(fid, source, dest):
    url = (ds.API + f"/files/{fid}"
           f"?addParents={dest}&removeParents={source}")
    st, rep, _ = ds.api("PATCH", url, body=b"{}")
    if st not in (200, 204):
        refus("deplacement", f"HTTP {st} : {rep[:120]!r}")


def lister_avec_reprise(pid, essais=5):
    """Listage avec reprise (constat e4 : lecture Drive parfois incohérente
    une requête sur N — relecture jusqu'à cohérence, jamais d'écriture
    aveugle)."""
    precedent = None
    for i in range(essais):
        actuel = ds.list_folder(pid)
        if actuel == precedent:
            return actuel
        precedent = actuel
        time.sleep(2)
    return precedent


def main():
    test = lister_avec_reprise(TEST_ID)
    if set(test) != RACINE_ATTENDUE:
        refus("racine-/test", f"{sorted(set(test) ^ RACINE_ATTENDUE)}")
    preuves_id = test["preuves-m5b"]["id"]
    arch_id = test["archives-preuves"]["id"]
    preuves = lister_avec_reprise(preuves_id)
    arch = lister_avec_reprise(arch_id)
    noms_pieces = set(PIECES)

    # md5 locaux (les pièces rapatriées font foi)
    for n in PIECES + [NOM_VERDICT]:
        if not (PREUVES_LOCAL / n).exists():
            refus("local", f"pièce locale absente : {n}")
    md5_locaux = {n: md5f(PREUVES_LOCAL / n) for n in PIECES}
    md5_verdict = md5f(VERDICT_LOCAL)
    md5_lisezmoi = md5f(PREUVES_LOCAL / "LISEZMOI-preuves.txt")

    # ---- 1. le dossier d'archive (créé si absent, repris sinon) ------------
    if "preuves-run-e4" in arch:
        dest_id = arch["preuves-run-e4"]["id"]
        print(f"[cloture-e4] reprise : preuves-run-e4 existe (id "
              f"{dest_id[:12]}…)")
    else:
        attendu_initial = noms_pieces | {"LISEZMOI-preuves.txt"}
        if set(preuves) != attendu_initial:
            refus("preuves-m5b", f"contenu inattendu : {sorted(set(preuves) ^ attendu_initial)}")
        for nom in PIECES:
            if preuves[nom].get("md5Checksum") != md5_locaux[nom]:
                refus("md5", f"{nom} distant != local")
        if (preuves["LISEZMOI-preuves.txt"].get("md5Checksum")
                != md5_lisezmoi):
            refus("md5", "LISEZMOI-preuves.txt distant != local")
        print("[cloture-e4] état initial conforme : 37 entrées (36 pièces + "
              "LISEZMOI), md5 recoupés")
        st, rep, _ = ds.api("POST", ds.API + "/files", body={
            "name": "preuves-run-e4", "mimeType": ds.FOLDER_MIME,
            "parents": [arch_id]})
        if st != 200:
            refus("creation-dossier", f"HTTP {st} : {rep[:120]!r}")
        dest_id = json.loads(rep)["id"]
        print(f"[cloture-e4] dossier preuves-run-e4 créé (id {dest_id[:12]}…)")
        for nom in PIECES:
            deplacer(preuves[nom]["id"], preuves_id, dest_id)
        preuves = lister_avec_reprise(preuves_id)

    # ---- 2. les pièces : toutes dans preuves-run-e4, md5 recoupés ---------
    run_e4 = lister_avec_reprise(dest_id)
    manquantes = noms_pieces - set(run_e4)
    if manquantes:
        # pièces restées dans preuves-m5b (reprise d'un état intermédiaire)
        for nom in sorted(manquantes):
            if nom not in preuves:
                refus("piece-perdue", f"{nom} ni dans preuves-m5b ni dans "
                                      f"preuves-run-e4")
            deplacer(preuves[nom]["id"], preuves_id, dest_id)
        run_e4 = lister_avec_reprise(dest_id)
        preuves = lister_avec_reprise(preuves_id)
    if not noms_pieces <= set(run_e4):
        refus("relecture-run-e4", f"il manque : {sorted(noms_pieces - set(run_e4))}")
    for nom in PIECES:
        if run_e4[nom].get("md5Checksum") != md5_locaux[nom]:
            refus("relecture-md5", nom)
    print("[cloture-e4] les 36 pièces sont dans preuves-run-e4, md5 recoupés "
          "par relecture")

    # ---- 3. le verdict les rejoint ------------------------------------------
    if NOM_VERDICT not in run_e4:
        ds.upload_create(dest_id, NOM_VERDICT, VERDICT_LOCAL)
        run_e4 = lister_avec_reprise(dest_id)
    if run_e4.get(NOM_VERDICT, {}).get("md5Checksum") != md5_verdict:
        refus("verdict-md5", "VERDICT-run-e4-critere-b.txt distant != local")
    print("[cloture-e4] VERDICT-run-e4-critere-b.txt déposé, md5 recoupé")

    # ---- 4. preuves-m5b VIERGE (le LISEZMOI demeure) ------------------------
    if set(preuves) - {"LISEZMOI-preuves.txt"}:
        refus("preuves-m5b-non-vide", f"{sorted(preuves)}")
    if "LISEZMOI-preuves.txt" not in preuves:
        ds.upload_create(preuves_id, "LISEZMOI-preuves.txt",
                         PREUVES_LOCAL / "LISEZMOI-preuves.txt")
        preuves = lister_avec_reprise(preuves_id)
    if set(preuves) != {"LISEZMOI-preuves.txt"}:
        refus("vierge", f"{sorted(preuves)}")
    if (preuves["LISEZMOI-preuves.txt"].get("md5Checksum")
            != md5_lisezmoi):
        refus("vierge-md5", "LISEZMOI-preuves.txt")
    print("[cloture-e4] preuves-m5b VIERGE (LISEZMOI-preuves.txt e4 demeure, "
          "md5 recoupé — la liste vaut pour toute reprise du kit e4)")

    # ---- 5. l'index mis à jour EN PLACE --------------------------------------
    st, corps, _ = ds.api("GET", ds.API + "/files/"
                          + arch["LISEZMOI-archives-preuves.txt"]["id"]
                          + "?alt=media")
    texte = corps.decode("utf-8")
    if "preuves-run-e4/" in texte:
        print("[cloture-e4] index déjà à jour (reprise)")
    else:
        ancre = "RÈGLE D143 (03/11)"
        if texte.count(ancre) != 1:
            refus("index", f"ancre présente {texte.count(ancre)} fois")
        if texte.count("preuves-run-e3/") != 1:
            refus("index", "section e3 absente (ordre inattendu)")
        nouveau = texte.replace(ancre, SECTION_INDEX + "\n" + ancre)
        if not (nouveau.find("preuves-run-e3/") < nouveau.find("preuves-run-e4/")
                < nouveau.find(ancre)):
            refus("index", "ordre final inattendu (e3 < e4 < ancre)")
        INDEX_NOUVEAU.write_text(nouveau, encoding="utf-8", newline="")
        ds.upload_update(arch["LISEZMOI-archives-preuves.txt"]["id"],
                         INDEX_NOUVEAU)
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + arch["LISEZMOI-archives-preuves.txt"]["id"]
                              + "?alt=media")
        if hashlib.md5(corps).hexdigest() != md5f(INDEX_NOUVEAU):
            refus("index-relecture", "md5 distant != md5 local")
        if "preuves-run-e4/" not in corps.decode("utf-8"):
            refus("index-relecture", "section e4 absente du distant")
        print("[cloture-e4] index LISEZMOI-archives-preuves.txt mis à jour "
              "EN PLACE, recoupé par relecture")

    # ---- 6. état final recoupé ----------------------------------------------
    test_final = lister_avec_reprise(TEST_ID)
    if set(test_final) != RACINE_ATTENDUE:
        refus("racine-finale", f"{sorted(set(test_final) ^ RACINE_ATTENDUE)}")
    arch_final = lister_avec_reprise(arch_id)
    attendues = set(arch) | {"preuves-run-e4"}
    if set(arch_final) != attendues:
        refus("archives-finale", f"{sorted(set(arch_final) ^ attendues)}")
    print(f"[cloture-e4] CLÔTURE D143 DU RUN e4 FAITE : archives-preuves = "
          f"{len(arch_final)} entrées ; preuves-m5b vierge ; racine /test "
          f"inchangée (8 entrées, la vague e4 demeure COURANTE — le jalon "
          f"est rentré) ; AUCUNE suppression — la corbeille n'est pas vidée")
    return 0


if __name__ == "__main__":
    sys.exit(main())
