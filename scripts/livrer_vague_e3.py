#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_vague_e3.py — LA LIVRAISON DE LA VAGUE e3 AU COFFRE /test (D143) :

  A. la vague e2 CONSOMMÉE (run e2 : ÉCHEC NOMMÉ REFUS PROXY-SANS-ARMEMENT —
     un refus de décor D145, le scellé 0.6.0-rc.1 INNOCENT ; ses pièces
     vivent déjà à archives-preuves/preuves-run-e2) est ARCHIVÉE dans
     archives-livraisons/vagues-m5b/ (jamais jetée) ;
  B. la vague e3 COURANTE est posée à la racine de /test :
       m5b-kit-e3.zip + scenario-m5b-e3.ps1 + LISEZMOI-m5b-e3.txt ;
  C. preuves-m5b/LISEZMOI-preuves.txt passe à la liste des pièces e3
     (+ page-sonde-armement.txt + edge-version.txt) ;
  D. l'index LISEZMOI-archives-livraisons.txt est mis à jour.

Chaque geste ASSERTÉ ; chaque mutation RECOUPÉE PAR RELECTURE (D12 étendu —
un 200 Drive ne prouve rien). Les déplacements : addParents/removeParents en
PARAMÈTRES DE REQUÊTE (la leçon du run v7, D143).

Usage : python3 scripts/livrer_vague_e3.py   (idempotent par REFUS : la
vague e3 déjà livrée fait échouer l'assertion d'état initial)
Code de sortie : 0 = vague livrée et recoupée ; 2 = refus nommé."""

import hashlib
import sys

REPO = "/home/z/my-project/triade-repo"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_LOCAL = "/home/z/my-project/download/vague-e3/m5b-kit-e3.zip"
SCENARIO_LOCAL = REPO + "/m5/vm/scenario-m5b-e3.ps1"
LISEZMOI_LOCAL = REPO + "/m5/vm/LISEZMOI-terrain-m5b-e3.txt"

KIT_MD5 = "981b1a5b14e75a77207df32ca7c8d4c9"     # consigné par l'assembleur e3

ARCHIVER = [   # (nom actuel à la racine /test, nom à l'archive)
    ("LISEZMOI-m5b-e2.txt", None),
    ("scenario-m5b-e2.ps1", None),
    ("m5b-kit-e2.zip", None),
]
LIVRER = [   # (chemin local, nom cible à la racine /test)
    (KIT_LOCAL, "m5b-kit-e3.zip"),
    (SCENARIO_LOCAL, "scenario-m5b-e3.ps1"),
    (LISEZMOI_LOCAL, "LISEZMOI-m5b-e3.txt"),
]
RACINE_ATTENDUE_APRES = {
    "LISEZMOI-m5b-e3.txt", "m5b-kit-e3.zip", "scenario-m5b-e3.ps1",
    "corriger-wsb.bat", "corriger-wsb.ps1",
    "preuves-m5b", "archives-livraisons", "archives-preuves",
}

LISEZMOI_PREUVES_E3 = (
    "Ce dossier recevra les preuves du run M5-b ETAPE 2 (le flux navigateur).\r\n"
    "Apres le run, y vivre : temoin-m5b.txt, scenario-m5b-journal.log,\r\n"
    "proxy-journal.log, page-sonde-armement.txt (e3 : la sonde d'armement),\r\n"
    "edge-version.txt (e3 : version du navigateur par VersionInfo),\r\n"
    "dom-a.txt, dom-b.txt, nav-a.png, nav-b.png,\r\n"
    "nav-a-err.txt, nav-b-err.txt, nav-a-cap-err.txt, nav-b-cap-err.txt,\r\n"
    "autorite-a.log, autorite-b.log (+ les -console/-err de l'autorite),\r\n"
    "hosts-lu.txt, matrice curl (curl-*.txt, page-d*.txt, autorite-d/e*),\r\n"
    "dnscache.txt, ipconfig-vm.txt, parefeu-vm.txt.\r\n"
    "Le dossier DOIT exister avant le double-clic (mapping du .wsb).\r\n"
)

INDEX_AJOUT = """  LISEZMOI-m5b-e2.txt + scenario-m5b-e2.ps1 + m5b-kit-e2.zip
                                           vague e2 consommée (run e2 :
                                           ÉCHEC NOMMÉ REFUS PROXY-SANS-
                                           ARMEMENT — un refus de DÉCOR,
                                           D145 : la garde lisait en live un
                                           journal vivant « vues vides » ;
                                           le scellé 0.6.0-rc.1 INNOCENT ;
                                           les pièces du run vivent à
                                           archives-preuves/preuves-run-e2)
"""


def refus(nom, detail):
    print(f"[livraison] REFUS {nom} : {detail}")
    sys.exit(2)


def md5f(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


def lister(pid):
    return ds.list_folder(pid)


def lire_fichier(fid):
    st, corps, _ = ds.api("GET", ds.API + f"/files/{fid}?alt=media")
    if st != 200:
        refus("LECTURE", f"impossible de lire {fid} ({st})")
    return corps


def deplacer(fid, source, dest, nouveau_nom=None):
    """Déplacement par addParents/removeParents EN REQUÊTE (leçon v7/D143) ;
    renommage éventuel AU CORPS déclaré (Content-Type posé par ds.api)."""
    url = (ds.API + f"/files/{fid}"
           f"?addParents={dest}&removeParents={source}")
    corps = {"name": nouveau_nom} if nouveau_nom else {}
    st, rep, _ = ds.api("PATCH", url, body=corps)
    if st not in (200, 201):
        refus("DEPLACEMENT", f"HTTP {st} : {rep[:150]!r}")


def televerser(parent, nom, chemin):
    """Dépôt (création) — recoupé par relecture md5 par l'appelant."""
    ds.upload_create(parent, nom, ds.pathlib.Path(chemin))


def main():
    # -- 0. les pièces locales, assertées ---------------------------------------
    if md5f(KIT_LOCAL) != KIT_MD5:
        refus("KIT-E3", f"md5 diverge ({md5f(KIT_LOCAL)} — attendu {KIT_MD5}) : "
                        "rejouez scripts/assembler_kit_e3.py")
    kit_scenario = open(SCENARIO_LOCAL, "rb").read()
    import zipfile
    avec = zipfile.ZipFile(KIT_LOCAL).read("m5b-kit/kit-m5b/scenario-m5b.ps1")
    if kit_scenario != avec:
        refus("SCENARIO", "le scénario à livrer diverge de celui du kit "
                          "(l'identité racine/zip est la règle v8)")
    lisezMoi = open(LISEZMOI_LOCAL, "rb").read()
    if b"VAGUE e3" not in lisezMoi:
        refus("LISEZMOI", "le LISEZMOI-terrain e3 ne porte pas sa marque")

    # -- 1. l'état AVANT (la vague e2 courante) ----------------------------------
    racine = lister(TEST_ID)
    attendu_avant = {
        "LISEZMOI-m5b-e2.txt", "m5b-kit-e2.zip", "scenario-m5b-e2.ps1",
        "corriger-wsb.bat", "corriger-wsb.ps1",
        "preuves-m5b", "archives-livraisons", "archives-preuves",
    }
    if set(racine) != attendu_avant:
        if "m5b-kit-e3.zip" in racine:
            refus("ETAT", "la vague e3 est DÉJÀ livrée (m5b-kit-e3.zip présent) — rejeu refusé")
        refus("ETAT", f"la racine /test ne porte pas l'état attendu : {sorted(set(racine))}")

    vagues = racine["archives-livraisons"]
    al = lister(vagues["id"])
    vm = al.get("vagues-m5b") or refus("ETAT", "archives-livraisons/vagues-m5b introuvable")
    preuves = racine["preuves-m5b"]

    # -- 2. l'archivage D143 (vague e2 consommée) --------------------------------
    for nom, nouveau_nom in ARCHIVER:
        f = racine.get(nom) or refus("ARCHIVAGE", f"{nom} introuvable à la racine /test")
        md5_avant = f.get("md5Checksum")
        deplacer(f["id"], TEST_ID, vm["id"], nouveau_nom)
        # recoupement par RELECTURE (D12 étendu)
        apres_racine = lister(TEST_ID)
        apres_vm = lister(vm["id"])
        nom_final = nouveau_nom or nom
        if nom in apres_racine:
            refus("ARCHIVAGE", f"{nom} RESTE à la racine — le déplacement n'a pas pris")
        cible = apres_vm.get(nom_final)
        if not cible:
            refus("ARCHIVAGE", f"{nom_final} absent de vagues-m5b après déplacement")
        if md5_avant and cible.get("md5Checksum") != md5_avant:
            refus("ARCHIVAGE", f"{nom_final} : md5 diverge après déplacement")
        print(f"[archivé] {nom} → vagues-m5b/{nom_final} (md5 recoupé)")
        racine = apres_racine

    # -- 3. la vague e3 posée à la racine -----------------------------------------
    for chemin, nom in LIVRER:
        if nom in lister(TEST_ID):
            refus("LIVRAISON", f"{nom} déjà présent — rejeu refusé")
        televerser(TEST_ID, nom, chemin)
        apres = lister(TEST_ID)
        f = apres.get(nom) or refus("LIVRAISON", f"{nom} absent après dépôt")
        if f.get("md5Checksum") != md5f(chemin):
            refus("LIVRAISON", f"{nom} : md5 distant ≠ local après dépôt")
        print(f"[livré] {nom} — {f.get('md5Checksum', '')[:8]}… md5 recoupé par relecture")

    # -- 4. preuves-m5b/LISEZMOI-preuves.txt → liste e3 ----------------------------
    import tempfile
    import pathlib
    contenu_preuves = lister(preuves["id"])
    lp = contenu_preuves.get("LISEZMOI-preuves.txt") or \
        refus("PREUVES", "preuves-m5b/LISEZMOI-preuves.txt introuvable (dossier non vierge ?)")
    if len(contenu_preuves) != 1:
        print(f"[preuves] ATTENTION : preuves-m5b porte {len(contenu_preuves)} entrées "
              f"(vierge attendue) — la règle D143 exige un dossier vierge avant run")
    tmp = pathlib.Path(tempfile.mkdtemp()) / "LISEZMOI-preuves.txt"
    tmp.write_bytes(LISEZMOI_PREUVES_E3.encode("utf-8"))
    ds.upload_update(lp["id"], tmp)
    relu = lire_fichier(lp["id"])
    if relu != LISEZMOI_PREUVES_E3.encode("utf-8"):
        refus("PREUVES", "LISEZMOI-preuves.txt relu ≠ contenu e3 attendu")
    print("[preuves] LISEZMOI-preuves.txt passé à la liste e3 (relu et recoupé)")

    # -- 5. l'index des archives, mis à jour ---------------------------------------
    idx = al.get("LISEZMOI-archives-livraisons.txt") or \
        refus("INDEX", "LISEZMOI-archives-livraisons.txt introuvable")
    texte_idx = lire_fichier(idx["id"]).decode("utf-8")
    if "vague e2 consommée" in texte_idx:
        print("[index] déjà à jour — idempotent")
    else:
        # insertion : après le bloc signatures-I-0.6.0.txt (la dernière entrée
        # posée par livrer_vague_e2.py), avant la salle terrain-17/
        marqueur = "  signatures-I-0.6.0.txt"
        pos = texte_idx.find(marqueur)
        if pos < 0:
            refus("INDEX", "ancre d'insertion introuvable (signatures-I-0.6.0.txt)")
        fin_ligne = texte_idx.find("\n", pos)
        fin_bloc = texte_idx.find("\n\n", fin_ligne)
        if fin_bloc < 0:
            refus("INDEX", "fin de bloc introuvable (la section vagues-m5b a changé)")
        nouveau = texte_idx[:fin_bloc + 1] + INDEX_AJOUT + texte_idx[fin_bloc + 1:]
        tmp_idx = pathlib.Path(tempfile.mkdtemp()) / "LISEZMOI-archives-livraisons.txt"
        tmp_idx.write_bytes(nouveau.encode("utf-8"))
        ds.upload_update(idx["id"], tmp_idx)
        relu_idx = lire_fichier(idx["id"]).decode("utf-8")
        if relu_idx != nouveau:
            refus("INDEX", "l'index relu ≠ l'index réécrit")
        print("[index] LISEZMOI-archives-livraisons.txt mis à jour (relu et recoupé)")

    # -- 6. l'état FINAL (la règle D143 : la racine ne porte que la vague courante)
    final = lister(TEST_ID)
    if set(final) != RACINE_ATTENDUE_APRES:
        refus("ETAT-FINAL", f"racine /test = {sorted(set(final))} — "
                            f"attendu {sorted(RACINE_ATTENDUE_APRES)}")
    print(f"[final] racine /test : {len(final)} entrées — la vague COURANTE est e3, "
          f"le décor est propre (corriger-wsb + preuves-m5b + les deux archives)")
    print("[livraison] VAGUE e3 LIVRÉE AU COFFRE — tout recoupé par relecture")


if __name__ == "__main__":
    main()
