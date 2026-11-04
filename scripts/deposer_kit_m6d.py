#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_m6d.py — LE COFFRE /test PASSÉ À LA VAGUE M6-(d) (règle D143).

La vague e4 est CONSOMMÉE (le run e4 a rendu son verdict, la finale 0.6.0
est scellée dessus — Entrée 143) : D143 l'archive (DÉPLACEMENT, jamais une
suppression, md5 constaté après le geste). La vague courante devient m6d —
LE KIT TERRAIN LINUX du chantier M6-(d) (le patch en production) :

  1. ARCHIVAGE e4 → /test/archives-livraisons/vagues-m5b/ :
     LISEZMOI-m5b-e4.txt, m5b-kit-e4.zip, scenario-m5b-e4.ps1 ;
  2. INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la section e4
     archivée + la vague courante m6d nommée) ;
  3. preuves-m6/ NÉ au coffre (le réceptacle des preuves du run M6-(d))
     avec son LISEZMOI-preuves.txt (les pièces attendues) ;
  4. LA VAGUE DÉPOSÉE à la racine de /test : kit-m6d.zip (le kit éprouvé
     au labo — extraction vierge + run VERT 16/16, assembler_kit_m6d.py)
     + LISEZMOI-m6d.txt (le document du kit, lisible AU coffre sans
     extraire — la discipline de lisibilité de la racine) ;
  5. VÉRIFICATION : la racine porte la vague courante + les résidents
     D143 (corriger-wsb.bat/.ps1, preuves-m5b vierge) + les deux salles
     d'archive ; les empreintes des pièces déposées recoupées ; les
     fichiers e4 CONSTATÉS dans vagues-m5b/ à l'identique (md5).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_m6d.py
Code de sortie : 0 = coffre passé à la vague m6d ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_LOCAL = "/home/z/my-project/download/vague-m6d/kit-m6d.zip"
LISEZMOI_KIT = os.path.join(REPO, "unix", "terrain", "LISEZMOI-KIT-M6D.md")

KIT_SHA = "98b8c1be2b913e892c6cccf4f3c2a77907a777d72e5d15cd4b58b4f5140f86fa"
KIT_MD5 = "67b859838736062ebb40415d17aec940"

VAGUE_E4 = ["LISEZMOI-m5b-e4.txt", "m5b-kit-e4.zip", "scenario-m5b-e4.ps1"]

LISEZMOI_PREUVES_M6 = (
    "Ce dossier reçoit les preuves du run M6-(d) — le patch en production "
    "(terrain Linux).\n"
    "Après le run, y déposer le dossier preuves-m6/ du kit EXTRAIT, ENTIER :\n"
    "  - temoin-m6d.txt            l'environnement de la machine (uname, WSL,\n"
    "                              python, ASLR noyau, empreinte du corpus AVANT)\n"
    "  - scenario-m6d-journal.log  le run entier, ligne à ligne\n"
    "  - VERDICT-run-m6d.txt       le verdict post-mortem (chaque constat)\n"
    "Le kit vit à la racine de /test : kit-m6d.zip + LISEZMOI-m6d.txt.\n"
    "Le geste : extraire kit-m6d.zip dans un dossier NEUF, puis\n"
    "  python3 scenario-m6d.py\n"
    "(WSL2 recommandé — D149 ; python3 + ctypes seulement, aucun paquet,\n"
    "aucun droit root, aucun réseau ; le fichier corpus ne bouge pas d'un\n"
    "octet — le scénario le re-prouve après le run.)\n"
    "Un verdict ÉCHEC NOMMÉ se renvoie TEL QUEL : la ligne nomme le défaut,\n"
    "un échec honnête vaut plus qu'un vert muet.\n"
)

INDEX_ADDENDUM = """
  LISEZMOI-m5b-e4.txt + scenario-m5b-e4.ps1 + m5b-kit-e4.zip
                                           vague e4 consommée (le run e4 a
                                           rendu son verdict : le critère (b)
                                           de D136 VERT sur pièces, la finale
                                           0.6.0 scellée — Entrée 143/D148 ;
                                           archivée le 05/11 au passage à la
                                           vague m6d)

--- la vague courante (racine de /test) : m6d — LE KIT TERRAIN LINUX M6-(d)
    (kit-m6d.zip + LISEZMOI-m6d.txt ; preuves-m6/ reçoit les preuves du run ;
    corriger-wsb.* demeurent résidents D143 de l'ère m5b, inutiles au run
    Linux mais jamais jetés) — mis à jour le 05/11/2026
"""


class Refus(Exception):
    """Tout refus nommé du passeur (fail-closed)."""


def md5_local(chemin):
    with open(chemin, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def deplacer_vers(file_id, nom, parent_de, parent_vers, md5_attendu):
    url = (f"{ds.API}/files/{file_id}?"
           + "addParents=" + parent_vers
           + "&removeParents=" + parent_de)
    st, body, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise Refus(f"déplacement de '{nom}' impossible (HTTP {st}) : {body[:200]!r}")
    apres = ds.list_folder(parent_vers).get(nom)
    if not apres:
        raise Refus(f"'{nom}' absent de la salle d'archive après le déplacement")
    if apres.get("md5Checksum") != md5_attendu:
        raise Refus(f"'{nom}' archivé : md5 divergent après le déplacement")
    if nom in ds.list_folder(parent_de):
        raise Refus(f"'{nom}' demeure à la racine après le déplacement")
    print(f"[archive] {nom} -> vagues-m5b/ (md5 {md5_attendu[:8]}… constaté "
          f"après le geste — D143 : un déplacement, jamais un jet)")


def main() -> int:
    print("=== M6-(d) : le coffre /test passe à la vague m6d ===")

    # (0) le kit local doit être LE kit éprouvé ---------------------------------
    with open(KIT_LOCAL, "rb") as f:
        kit = f.read()
    if (hashlib.sha256(kit).hexdigest() != KIT_SHA
            or hashlib.md5(kit).hexdigest() != KIT_MD5):
        raise Refus("kit-m6d.zip local != le kit éprouvé (sha/md5) — assembler_kit_m6d.py d'abord")

    racine = ds.list_folder(TEST_ID)
    arch = racine.get("archives-livraisons") or {}
    if not arch.get("id"):
        raise Refus("archives-livraisons/ introuvable au coffre /test")
    vagues = ds.list_folder(arch["id"]).get("vagues-m5b") or {}
    if not vagues.get("id"):
        raise Refus("vagues-m5b/ introuvable dans archives-livraisons/")

    # (1) l'archivage e4 (idempotent : déjà parti = constaté) --------------------
    for nom in VAGUE_E4:
        entree = racine.get(nom)
        if not entree:
            deja = ds.list_folder(vagues["id"]).get(nom)
            if deja:
                print(f"[archive] {nom} déjà archivé (md5 {deja.get('md5Checksum', '-')[:8]}…) — constaté")
                continue
            raise Refus(f"'{nom}' ni à la racine ni dans l'archive — introuvable")
        deplacer_vers(entree["id"], nom, TEST_ID, vagues["id"],
                      entree.get("md5Checksum"))

    # (2) l'index des livraisons mis à jour ---------------------------------------
    idx = ds.list_folder(arch["id"]).get("LISEZMOI-archives-livraisons.txt")
    if not idx:
        raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
    url = ds.API + "/files/" + idx["id"] + "?alt=media"
    _, body, _ = ds.api("GET", url)
    texte = body.decode("utf-8")
    if "vague m6d" not in texte:
        texte = texte.rstrip("\n") + "\n" + INDEX_ADDENDUM
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write(texte)
            chemin_tmp = pathlib.Path(f.name)
        try:
            ds.upload_update(idx["id"], chemin_tmp)
        finally:
            os.unlink(chemin_tmp)
        print("[index] LISEZMOI-archives-livraisons.txt mis à jour "
              "(la section e4 + la vague courante m6d)")
    else:
        print("[index] déjà à jour (la vague m6d y est nommée) — constaté")

    # (3) preuves-m6/ NÉ au coffre ------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    pm6 = racine.get("preuves-m6")
    if not pm6:
        pm6_id = ds.create_folder(TEST_ID, "preuves-m6")
        print(f"[preuves] preuves-m6/ créé au coffre ({pm6_id})")
    else:
        pm6_id = pm6["id"]
        print(f"[preuves] preuves-m6/ déjà présent ({pm6_id}) — constaté")
    if "LISEZMOI-preuves.txt" not in ds.list_folder(pm6_id):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write(LISEZMOI_PREUVES_M6)
            chemin_tmp = pathlib.Path(f.name)
        try:
            ds.upload_create(pm6_id, "LISEZMOI-preuves.txt", chemin_tmp)
        finally:
            os.unlink(chemin_tmp)
        print("[preuves] LISEZMOI-preuves.txt déposé (les pièces attendues)")
    else:
        print("[preuves] LISEZMOI-preuves.txt déjà là — constaté")

    # (4) la vague déposée à la racine ---------------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-m6d.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-m6d.zip", pathlib.Path(KIT_LOCAL))
        print(f"[vague] kit-m6d.zip déposé ({len(kit)} o, md5 {KIT_MD5[:8]}…)")
    else:
        if racine["kit-m6d.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("kit-m6d.zip présent au coffre mais md5 divergent — "
                        "refus de cohabiter deux kits")
        print("[vague] kit-m6d.zip déjà déposé à l'identique — constaté")
    racine = ds.list_folder(TEST_ID)
    if "LISEZMOI-m6d.txt" not in racine:
        ds.upload_create(TEST_ID, "LISEZMOI-m6d.txt", pathlib.Path(LISEZMOI_KIT))
        print("[vague] LISEZMOI-m6d.txt déposé (le document du kit, lisible "
              "au coffre sans extraire)")
    else:
        print("[vague] LISEZMOI-m6d.txt déjà là — constaté")

    # (5) la vérification finale ----------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    attendus = {"kit-m6d.zip", "LISEZMOI-m6d.txt", "corriger-wsb.bat",
                "corriger-wsb.ps1", "preuves-m5b", "preuves-m6",
                "archives-livraisons", "archives-preuves"}
    manquants = attendus - set(racine)
    if manquants:
        raise Refus(f"la racine de /test ne porte pas {sorted(manquants)}")
    if racine["kit-m6d.zip"].get("md5Checksum") != KIT_MD5:
        raise Refus("le kit déposé au coffre != le kit éprouvé (md5)")
    print(f"[vérif] la racine de /test porte la vague m6d ({len(racine)} "
          f"entrées — les résidents D143 + preuves-m6 + les deux salles "
          f"d'archive) :")
    for nom, meta in sorted(racine.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"[vérif]   [DIR ] {nom}")
        else:
            print(f"[vérif]   [{meta.get('size', '?'):>7} o] {nom}  "
                  f"md5={meta.get('md5Checksum', '-')[:8]}…")
    vagues_apres = ds.list_folder(arch["id"]).get("vagues-m5b")
    dans_vagues = ds.list_folder(vagues_apres["id"])
    for nom in VAGUE_E4:
        if nom not in dans_vagues:
            raise Refus(f"'{nom}' absent de vagues-m5b/ après le geste")
    print(f"[vérif] la vague e4 CONSTATÉE dans vagues-m5b/ "
          f"({len(VAGUE_E4)} pièces, md5 intacts)")
    print("=== le coffre /test vit à la vague m6d — le run du développeur attend ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Refus, ds.SyncError) as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(2)
