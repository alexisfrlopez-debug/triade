#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_vague_e2.py — LA LIVRAISON DE LA VAGUE e2 AU COFFRE /test (D143) :

  A. la vague v8 CONSOMMÉE (run v8 OK 0 réserve — le décor est verrouillé)
     et les pièces de cérémonie 0.6.0 CONSOMMÉES (onze arbres verts, 04/11)
     sont ARCHIVÉES dans archives-livraisons/vagues-m5b/ (jamais jetées) ;
  B. la vague e2 COURANTE est posée à la racine de /test :
       m5b-kit-e2.zip + scenario-m5b-e2.ps1 + LISEZMOI-m5b-e2.txt ;
  C. preuves-m5b/LISEZMOI-preuves.txt passe à la liste des pièces e2 ;
  D. l'index LISEZMOI-archives-livraisons.txt est mis à jour.

Chaque geste ASSERTÉ ; chaque mutation RECOUPÉE PAR RELECTURE (D12 étendu —
un 200 Drive ne prouve rien). Les déplacements : addParents/removeParents en
PARAMÈTRES DE REQUÊTE (la leçon du run v7, D143) ; le renommage de la
signature consommée (signatures-I-0.6.0.txt) désambiguïse l'archive — deux
remises du même nom y vivraient sinon.

Usage : python3 scripts/livrer_vague_e2.py   (idempotent par REFUS : la
vague e2 déjà livrée fait échouer l'assertion d'état initial)
Code de sortie : 0 = vague livrée et recoupée ; 2 = refus nommé."""

import hashlib
import json
import sys
import urllib.parse

REPO = "/home/z/my-project/triade-repo"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_LOCAL = "/home/z/my-project/download/vague-v8/m5b-kit-e2.zip"
SCENARIO_LOCAL = REPO + "/m5/vm/scenario-m5b-e2.ps1"
LISEZMOI_LOCAL = REPO + "/m5/vm/LISEZMOI-terrain-m5b-e2.txt"

KIT_MD5 = "76e7b02f8c922981dbdc64fb34c6f679"     # consigné par l'assembleur

ARCHIVER = [   # (nom actuel à la racine /test, nom à l'archive)
    ("LISEZMOI-m5b-v8.txt", None),
    ("scenario-m5b-v8.ps1", None),
    ("m5b-kit-v8.zip", None),
    ("paquet-ceremonie-0.6.0.zip", None),
    ("LISEZMOI-ceremonie-0.6.0.txt", None),
    ("signatures-I.txt", "signatures-I-0.6.0.txt"),   # remise 0.6.0 consommée
]
LIVRER = [   # (chemin local, nom cible à la racine /test)
    (KIT_LOCAL, "m5b-kit-e2.zip"),
    (SCENARIO_LOCAL, "scenario-m5b-e2.ps1"),
    (LISEZMOI_LOCAL, "LISEZMOI-m5b-e2.txt"),
]
RACINE_ATTENDUE_APRES = {
    "LISEZMOI-m5b-e2.txt", "m5b-kit-e2.zip", "scenario-m5b-e2.ps1",
    "corriger-wsb.bat", "corriger-wsb.ps1",
    "preuves-m5b", "archives-livraisons", "archives-preuves",
}

LISEZMOI_PREUVES_E2 = (
    "Ce dossier recevra les preuves du run M5-b ETAPE 2 (le flux navigateur).\r\n"
    "Apres le run, y vivre : temoin-m5b.txt, scenario-m5b-journal.log,\r\n"
    "proxy-journal.log, dom-a.txt, dom-b.txt, nav-a.png, nav-b.png,\r\n"
    "nav-a-err.txt, nav-b-err.txt, nav-a-cap-err.txt, nav-b-cap-err.txt,\r\n"
    "autorite-a.log, autorite-b.log (+ les -console/-err de l'autorite),\r\n"
    "hosts-lu.txt, matrice curl (curl-*.txt, page-d*.txt, autorite-d/e*),\r\n"
    "dnscache.txt, ipconfig-vm.txt, parefeu-vm.txt.\r\n"
    "Le dossier DOIT exister avant le double-clic (mapping du .wsb).\r\n"
)

INDEX_AJOUT = """  LISEZMOI-m5b-v8.txt + scenario-m5b-v8.ps1 + m5b-kit-v8.zip
                                           vague v8 consommée (run v8 OK
                                           0 réserve — le décor parefeu-muet
                                           est verrouillé pour les vagues)
  paquet-ceremonie-0.6.0.zip + LISEZMOI-ceremonie-0.6.0.txt
                                           cérémonie 0.6.0 CONSOMMÉE (remise
                                           du développeur 04/11 — ONZE arbres
                                           verts, m5 = 1869422e…)
  signatures-I-0.6.0.txt                   signature opérateur CONSOMMÉE par
                                           la cérémonie 0.6.0 (1 564 o, 11
                                           lignes — renommée à l'archive pour
                                           ne pas confondre avec la remise
                                           0.5.1 archivée au même nom)
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
        refus("KIT-E2", f"md5 diverge ({md5f(KIT_LOCAL)} — attendu {KIT_MD5}) : "
                        "rejouez scripts/assembler_kit_e2.py")
    kit_scenario = open(SCENARIO_LOCAL, "rb").read()
    import zipfile
    avec = zipfile.ZipFile(KIT_LOCAL).read("m5b-kit/kit-m5b/scenario-m5b.ps1")
    if kit_scenario != avec:
        refus("SCENARIO", "le scénario à livrer diverge de celui du kit "
                          "(l'identité racine/zip est la règle v8)")
    lisezMoi = open(LISEZMOI_LOCAL, "rb").read()
    if b"VAGUE e2" not in lisezMoi:
        refus("LISEZMOI", "le LISEZMOI-terrain e2 ne porte pas sa marque")

    # -- 1. l'état AVANT (la vague v8 courante + cérémonie consommée) ------------
    racine = lister(TEST_ID)
    attendu_avant = {
        "LISEZMOI-ceremonie-0.6.0.txt", "LISEZMOI-m5b-v8.txt", "archives-livraisons",
        "archives-preuves", "corriger-wsb.bat", "corriger-wsb.ps1", "m5b-kit-v8.zip",
        "paquet-ceremonie-0.6.0.zip", "preuves-m5b", "scenario-m5b-v8.ps1",
        "signatures-I.txt",
    }
    if set(racine) != attendu_avant:
        if "m5b-kit-e2.zip" in racine:
            refus("ETAT", "la vague e2 est DÉJÀ livrée (m5b-kit-e2.zip présent) — rejeu refusé")
        refus("ETAT", f"la racine /test ne porte pas l'état attendu : {sorted(set(racine))}")

    vagues = racine["archives-livraisons"]
    al = lister(vagues["id"])
    vm = al.get("vagues-m5b") or refus("ETAT", "archives-livraisons/vagues-m5b introuvable")
    preuves = racine["preuves-m5b"]

    # -- 2. l'archivage D143 (vague v8 + cérémonie 0.6.0 consommées) -------------
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

    # -- 3. la vague e2 posée à la racine -----------------------------------------
    for chemin, nom in LIVRER:
        if nom in lister(TEST_ID):
            refus("LIVRAISON", f"{nom} déjà présent — rejeu refusé")
        televerser(TEST_ID, nom, chemin)
        apres = lister(TEST_ID)
        f = apres.get(nom) or refus("LIVRAISON", f"{nom} absent après dépôt")
        if f.get("md5Checksum") != md5f(chemin):
            refus("LIVRAISON", f"{nom} : md5 distant ≠ local après dépôt")
        print(f"[livré] {nom} — {f.get('md5Checksum', '')[:8]}… md5 recoupé par relecture")

    # -- 4. preuves-m5b/LISEZMOI-preuves.txt → liste e2 ----------------------------
    import tempfile, pathlib
    contenu_preuves = lister(preuves["id"])
    lp = contenu_preuves.get("LISEZMOI-preuves.txt") or \
        refus("PREUVES", "preuves-m5b/LISEZMOI-preuves.txt introuvable (dossier non vierge ?)")
    if len(contenu_preuves) != 1:
        print(f"[preuves] ATTENTION : preuves-m5b porte {len(contenu_preuves)} entrées "
              f"(vierge attendue) — la règle D143 exige un dossier vierge avant run")
    tmp = pathlib.Path(tempfile.mkdtemp()) / "LISEZMOI-preuves.txt"
    tmp.write_bytes(LISEZMOI_PREUVES_E2.encode("utf-8"))
    ds.upload_update(lp["id"], tmp)
    relu = lire_fichier(lp["id"])
    if relu != LISEZMOI_PREUVES_E2.encode("utf-8"):
        refus("PREUVES", "LISEZMOI-preuves.txt relu ≠ contenu e2 attendu")
    print("[preuves] LISEZMOI-preuves.txt passé à la liste e2 (relu et recoupé)")

    # -- 5. l'index des archives, mis à jour ---------------------------------------
    idx = al.get("LISEZMOI-archives-livraisons.txt") or \
        refus("INDEX", "LISEZMOI-archives-livraisons.txt introuvable")
    texte_idx = lire_fichier(idx["id"]).decode("utf-8")
    ancre = "  GUIDE-patch-0.5.1-jalon-v7.txt"
    if "vague v8 consommée" in texte_idx:
        print("[index] déjà à jour — idempotent")
    else:
        if ancre not in texte_idx:
            refus("INDEX", "ancre d'insertion introuvable (la section vagues-m5b a changé)")
        # insertion : après le bloc v7 (ligne signatures-I.txt de la 0.5.1)
        marqueur_051 = "  signatures-I.txt"
        pos = texte_idx.find(marqueur_051)
        fin_ligne = texte_idx.find("\n", pos)
        fin_bloc = texte_idx.find("\n\n", fin_ligne)
        nouveau = texte_idx[:fin_bloc + 1] + INDEX_AJOUT + texte_idx[fin_bloc + 1:]
        nouveau = nouveau.replace(
            "mis à jour le 03/11/2026", "mis à jour le 04/11/2026", 1)
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
    print(f"[final] racine /test : {len(final)} entrées — la vague COURANTE est e2, "
          f"le décor est propre (corriger-wsb + preuves-m5b + les deux archives)")
    print("[livraison] VAGUE e2 LIVRÉE AU COFFRE — tout recoupé par relecture")


if __name__ == "__main__":
    main()
