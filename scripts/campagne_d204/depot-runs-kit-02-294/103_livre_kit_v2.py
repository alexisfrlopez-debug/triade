#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""103_livre_kit_v2.py — LA LIVRAISON DU KIT v2 au coffre /test (le juge
corrigé, la pièce INTACTE) + LA CARTE DES KITS portée à l'unité 2 revenue.
Chaque pièce téléversée puis RECoupÉE PAR RE-TÉLÉCHARGEMENT byte-byte (la
règle du double téléchargement) ; la carte LISEZMOI-KITS-UNITES-D204.txt
mise à jour (la section 294) et re-téléchargée identique. Écritures par
LE RELAIS OAUTH (drive_sync)."""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

KIT2 = pathlib.Path("/home/z/my-project/work/triade/scripts/campagne_d204/"
                    "unite-02-T/kit-v2")
NOM_KIT = "kit-unite-loupe-02-T-20261114-v2"
CARTE_KITS = "LISEZMOI-KITS-UNITES-D204.txt"
BAC = pathlib.Path("/home/z/my-project/work/triade/scripts/campagne_d204/"
                   "depot-runs-kit-02-294")
CARTE_AVANT = BAC / "epreuves" / "carte-kits-290-telle-quelle.txt"


def sub(folder_id, name):
    for nom, it in ds.list_folder(folder_id).items():
        if nom == name and it["mimeType"] == ds.FOLDER_MIME:
            return it
    return None


def fiche(folder_id, name):
    """Un FICHIER nommé (la carte — pas un dossier)."""
    return ds.list_folder(folder_id).get(name)


def sha256_bytes(d):
    return hashlib.sha256(d).hexdigest()


def telecharge(file_id):
    st, body, _ = ds.api("GET", ds.API + f"/files/{file_id}?alt=media")
    assert st == 200, f"HTTP {st}"
    return body


coffre_test = sub(ds.DRIVE_ROOT_ID, "test")

# -- 1. le dossier du kit v2 ---------------------------------------------------
k2 = sub(coffre_test["id"], NOM_KIT)
if k2 is None:
    k2_id = ds.create_folder(coffre_test["id"], NOM_KIT)
    print(f"[créé] /test/{NOM_KIT} (id={k2_id[:12]}…)")
    k2 = {"id": k2_id}
else:
    print(f"[déjà] /test/{NOM_KIT} vit — idempotent (id={k2['id'][:12]}…)")

# -- 2. les DOUZE pièces, téléversées puis recoupées ----------------------------
PIECES = ["EMPREINTES-KIT-UNITE-02-T.txt", "LANCEUR-UNITE-02-T.bat",
          "LISEZMOI-KIT-UNITE-02-T.txt", "brouillon-loupe-02-lire.asm",
          "loupe.exe", "notation-loupe-02-lire.asm", "scenario-unite02.py",
          "temoin-1.bin", "temoin-384.bin", "temoin-3f.bin", "vide.bin",
          f"{NOM_KIT}.zip"]
presents = ds.list_folder(k2["id"])
verts, ecarts = 0, []
for nom in PIECES:
    local = (KIT2 / nom).read_bytes()
    h_local = sha256_bytes(local)
    distant = presents.get(nom)
    if distant is None:
        ds.upload_create(k2["id"], nom, KIT2 / nom)
        distant = ds.list_folder(k2["id"]).get(nom)
        print(f"    [téléversé] {nom}  {len(local)} o")
    # LE RECOUP : re-téléchargement byte-byte
    recu = telecharge(distant["id"])
    if recu == local and distant.get("md5Checksum") == hashlib.md5(local).hexdigest():
        verts += 1
        print(f"    [VERT] {nom}  sha256 {h_local[:16]}… "
              f"== re-téléchargé byte-byte")
    else:
        ecarts.append(nom)
        print(f"    [ÉCART] {nom} : le re-téléchargement diverge")
print(f"[kit v2] {verts}/{len(PIECES)} recoupés par re-téléchargement")
if ecarts:
    sys.exit(2)

# -- 3. LA CARTE DES KITS portée à l'unité 2 revenue ---------------------------
SECTION = """=== LES RUNS DE L'UNITÉ 2 REVENUS, LE JUGE v2 LIVRÉ — le 15/11/2026 (l'Entrée 294) ===
L'annonce « kit 02 C et T dans /test du drive » : les DEUX kits courus au terrain le 14/11 (16:46:34Z et 16:48:50Z, la machine PORTABLE · Windows 10 · Python 3.14.10 — la même que l'unité 1, CA2). Les dépôts : une copie datée au sein de chaque kit — la console du run, le témoin DATÉ et SIGNÉ de la main (Alexis Lopez, 14/11/2026 — D99), et les pièces du kit recoupées TROIS FOIS (la copie == le kit parent au coffre == le bac du labo : 22/22 VERT). RANGÉS à /archives-livraisons/unite-02-loupe-20261114/ (les noms conservés, md5 par md5 — D143 : déplacés, jamais jetés).
LE BRAS C : 20 VERT, 0 ROUGE — loupe-02-c.dll 925cd019… == la gravure ; SetFilePointerEx PRÉSENTE ; la première fenêtre lue INLINE au bloc session (l'écart nommé du bras C) ; LA PREMIÈRE LIVRAISON VERTE DE L'UNITÉ 2 — la ligne C-loupe-02-it1 attend sa consignation au livre (onglet 5 · LIVRAISON de l'atelier 013520 — il vit à /archives-livraisons/unite-01-loupe-20261114/atelier-campagne-d204-20261114-013520/, le choisir à « CHOISIR L'ATELIER EXISTANT… », étape 2).
LE BRAS T : 18 VERT, 2 ROUGE — L'ÉCART ÉTAIT AU JUGE, PAS À LA PIÈCE : le scénario v1 posait le journal d'édition à R_JOURNAL = 0xE4E0, 64 octets au-dessus de la vérité du layout (loupe/layout.py : 0xE4A0 — l'adresse même que le lea de la pièce vise, lue à l'octet près) ; la pièce lisait son compte à la BONNE adresse et tombait sur la zone zéroée du juge → compte 0 → AUCUN recouvrement → les DEUX vecteurs V2 ROUGE (les-bords-de-fenetre, cinq-entrees-dont-une-non-alignee) — rejoués octet par octet au labo ; l'AUDIT DES CONSTANTES (le scénario livré contre le layout — l'épreuve qui manquait) est désormais tenu au bac. Le témoin est signé ; le run NE CONSOMME PAS d'itération (le précédent 283/284 : la faute au labo ne consomme jamais).
LE KIT v2 : kit-unite-loupe-02-T-20261114-v2/ — LE SEUL CHANGEMENT : la constante du scénario remise à la vérité du layout (0xE4A0) ; loupe.exe 98354ff6… et les HUIT autres pièces INTACTES octet pour octet (comparez les EMPREINTES : une seule ligne bouge — scenario-unite02.py) ; le kit v1 demeure (D143). LA REPRISE : 1·KIT choisir le dossier v2 → 2·RUN lancer le LANCEUR → 3·TÉMOIN dater, signer de la main → preuves-unite02/ ENTIER au /test.
LE LIVRE : livraisons.csv porte encore les DEUX seules lignes de loupe-01 — l'unité 2 attend le geste de l'onglet 5 (C-loupe-02-it1 maintenant, T-loupe-02-it1 au retour du run v2). LA SUITE : loupe-05 sha256, aux deux bras.
"""

carte_avant = CARTE_AVANT.read_bytes()
carte = fiche(coffre_test["id"], CARTE_KITS)
assert carte is not None, "la carte des kits introuvable au /test"
# la section déjà posée ? (idempotence)
deja = telecharge(carte["id"])
if SECTION.encode("utf-8")[:80] in deja:
    print("[carte] la section 294 y vit déjà — idempotent")
else:
    assert deja == carte_avant, "la carte au coffre ≠ la carte rapatriée (écart)"
    nouvelle = deja + b"\n" + SECTION.encode("utf-8")
    provisoire = BAC / "epreuves" / "carte-kits-294.txt"
    provisoire.write_bytes(nouvelle)
    ds.upload_update(carte["id"], provisoire)
    print(f"[carte] mise à jour : {CARTE_KITS} "
          f"({len(nouvelle)} o, la section 294 ajoutée)")

# le RECOUP de la carte
recu = telecharge(carte["id"])
attendu = carte_avant + b"\n" + SECTION.encode("utf-8")
if recu == attendu:
    print(f"[carte] [VERT] re-téléchargée IDENTIQUE byte-byte "
          f"({len(recu)} o, sha256 {sha256_bytes(recu)[:16]}…)")
else:
    print("[carte] [ÉCART] la carte re-téléchargée diverge")
    sys.exit(2)

# -- 4. l'état final du /test --------------------------------------------------
racine = ds.list_folder(coffre_test["id"])
print(f"\n[/test] la racine porte {len(racine)} entrées ; "
      f"{NOM_KIT}/ : {len(ds.list_folder(k2['id']))} pièces")
print("[LIVRAISON] TOUT VERT — le kit v2 au coffre, la carte portée à 294")
