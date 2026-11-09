#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_loupe_dev6.py — LE TÉMOIN DU RUN dev.6 ARCHIVÉ SUR PIÈCES
(règle D143 : archivage par DÉPLACEMENT, jamais un jet).

LE SIXIÈME RUN TERRAIN (l'Entrée 209) : le développeur a déposé le
dossier loupe-kit/ au /test du Drive — le kit dev.6 COMPLET (l'artefact
dev.5, sha256 6f830f9c…, la vague de l'Entrée 208) ET ses preuves
(preuves-loupe/ DANS le dossier du kit — la première fois que le
terrain rend le kit et le témoin ENSEMBLE, un dossier par run, D99
respecté de fait).

LE TÉMOIN : [T0] TOUT VERT (l'empreinte dev.5 ASSERTÉE, l'image
cartographiée DONT_RESOLVE, LE CADRE NÉ MIROIR, les scellés constatés,
l'IAT 37 feuilles — l'affichage T0 de la version portait un LITTÉRAL
PÉRIMÉ « 0x00010004 » tandis que la vérification comparait bien
0x00010005 : la porte R10 ouverte, l'affichage en retard — nommé par
l'Entrée 210) ; [T1]→[T4] VERTS ; [T5] ÉCHEC NOMMÉ [SAUVEGARDE] :
« loupe-17 → OK (1 octet écrit attendu) » — ET LA PREUVE ÉTAIT DANS
LE FICHIER : temoin-edition.bin portait 0x4D à l'octet 0, la taille
CONSTANTE, le motif intact — LA SAUVEGARDE AVAIT EU LIEU, c'est
l'attente du scénario qui fautait (loupe-17 rend SON 0 = OK, le
compte des octets part à LA BARRE D'ÉTAT). LE TÉMOIN VITRINE : les
DEUX fenêtres mortes 0xC0000005, AUCUN rapport WER — l'autopsie de
l'Entrée 209 a nommé [HINSTANCE-PEB] : l'entrée du build prenait le
RCX BRUT du point d'entrée (le PEB) pour hInstance, le slot
GetModuleHandleW était importé mais JAMAIS CÂBLÉ.

  1. LE DOSSIER D'ARCHIVE né aux archives-preuves :
     preuves-run-loupe-dev6/ ;
  2. LES DEUX TÉMOINS DÉPLACÉS du dossier du run
     (loupe-kit/preuves-loupe/ → l'archive ; addParents/removeParents
     — DÉPLACEMENT, jamais une copie) + md5 recoupés APRÈS ;
  3. LE VERDICT DU RUN déposé dans l'archive (VERDICT-run-loupe-
     dev6.txt : ROUGE AU T5 SUR UNE FAUSSE ERREUR — la sauvegarde
     PROUVÉE PAR LE FICHIER — ET la vitrine morte nommée
     [HINSTANCE-PEB]) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-preuves.txt.

Le dossier du run loupe-kit/ DEMEURE au /test (le kit tel que vécu
par le terrain — ses fichiers nés au run restent avec lui ; seules
les PREUVES partent à l'archive, la règle D143 s'applique au témoin).
Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/archiver_run_loupe_dev6.py
Code de sortie : 0 = témoins archivés ; 2 = refus nommé."""

import os
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # dossier « test »
ARCHIVES_PREUVES_ID = "1TRZtOdvqfovvZt0jdFdpMysrpHNKOzFk"  # archives-preuves
INDEX_ID = "1WK5OOuMOFFoUj3PevftZo3pHIFKQx7zu"          # LISEZMOI-archives-preuves

DOSSIER_ARCHIVE = "preuves-run-loupe-dev6"

# les témoins du run dev.6 (le sixième run, l'Entrée 209 — déposés par
# le terrain DANS le dossier du kit, preuves-loupe/ de loupe-kit/)
TEMOINS = {
    "temoin-loupe.txt": "5cb3014f7e0e92967a6d2096fb1ce282",    # 2 335 o
    "temoin-vitrine.txt": "bebad29e1b970526d3f32bfcc90658be",  # 389 o
}

VERDICT = """VERDICT DU RUN TERRAIN M10-(e) — LOUPE dev.6 : ROUGE AU T5 SUR UNE FAUSSE ERREUR — LA SAUVEGARDE PROUVÉE PAR LE FICHIER — ET LA VITRINE MORTE NOMMÉE [HINSTANCE-PEB]
===================================================================================================================================================
Le run du 09/11/2026 (la vague dev.6 de l'Entrée 208 — l'artefact
dev.5 INCHANGÉ, sha256 6f830f9c… ; le témoin déposé par le
développeur DANS le dossier du kit, loupe-kit/preuves-loupe/ — la
première fois que le terrain rend kit et témoin ENSEMBLE) :

  - [T0] TOUT VERT : l'empreinte ASSERTÉE (loupe.exe 127 488 o,
    sha256 6f830f9c738265df… — l'artefact dev.5 AUTHENTIQUE,
    AUCUN octet bougé par la retouche 208), l'image cartographiée
    DONT_RESOLVE, LE CADRE NÉ LE MIROIR DU CADRE_VIERGE, les
    adresses scellées CONSTATÉES, l'IAT 37 feuilles posées — ET
    l'affichage de la version portait le LITTÉRAL PÉRIMÉ
    « 0x00010004 » (la vérification comparait bien 0x00010005 :
    l'affichage en retard sur la porte R10 — nommé par l'Entrée
    210, le kit dev.8 le rend DYNAMIQUE {VERSION_R10}) ;
  - [T1]→[T4] VERTS : la session sur L'OMBRE, la double lecture,
    LE PANNEAU (md5 + sha256 == hashlib — la pièce jugée par sa
    propre application), les lignes, la recherche ;
  - [T5] ÉCHEC NOMMÉ [SAUVEGARDE] : « loupe-17 → OK (1 octet
    écrit attendu) » — ET LA PREUVE ÉTAIT DANS LE FICHIER :
    temoin-edition.bin portait 0x4D à l'octet 0, la taille
    CONSTANTE, le motif intact — LA SAUVEGARDE AVAIT EU LIEU PAR
    LE VRAI WriteFile, c'est L'ATTENTE du scénario qui fautait :
    le contrat publié de loupe-17 rend 0 = OK, le compte des
    octets part au TEXTE de la barre d'état — l'Entrée 209 a
    rendu l'attente au contrat (kit dev.7 : r != 1 → r != 0) ;
  - LA VITRINE : les DEUX fenêtres mortes 0xC0000005
    (-1073741819), AUCUN rapport WER — l'autopsie de l'Entrée
    209 a nommé [HINSTANCE-PEB] : l'entrée du build prenait le
    RCX BRUT du point d'entrée (le PEB) pour hInstance et le
    donnait à RegisterClassExW ET CreateWindowExW, le slot
    GetModuleHandleW (0x2400) était IMPORTÉ mais JAMAIS CÂBLÉ —
    la lignée prouvée (demo.exe 0.3.0, le scellé M2 dont la
    fenêtre VÉCUT) appelle GetModuleHandleW(NULL).

LA DOUBLE RETOUCHE DE L'ENTRÉE 209 : le build dev.6 (l'entrée
réécrite EN PLACE : r12 = LE VRAI MODULE — R7 tenue, le WndProc
@0x5DCB INTACT, le qword version 0x00010006) ET le kit dev.7
(l'attente T5 rendue au contrat publié : 0 = OK).
"""

NOTE_INDEX = """
--- le run loupe dev.6 archivé (le sixième run, l'Entrée 209 — le
    témoin déposé par le terrain DANS le dossier du kit
    loupe-kit/preuves-loupe/, la première fois kit et preuves
    ENSEMBLE) : ROUGE AU T5 SUR UNE FAUSSE ERREUR — « loupe-17 → OK
    (1 octet écrit attendu) » — ET LA PREUVE ÉTAIT DANS LE FICHIER :
    temoin-edition.bin portait 0x4D à l'octet 0, la taille
    CONSTANTE — LA SAUVEGARDE AVAIT EU LIEU, c'est l'attente du
    scénario qui fautait [le contrat publié de loupe-17 : 0 = OK,
    le compte des octets part à la barre d'état] ; la vitrine morte
    ×2 0xC0000005 sans rapport WER — [HINSTANCE-PEB] nommé par
    l'autopsie : le RCX brut du point d'entrée pris pour hInstance,
    GetModuleHandleW importé mais JAMAIS câblé ; témoins
    temoin-loupe.txt 2 335 o md5 5cb3014f… + temoin-vitrine.txt
    389 o md5 bebad29e… archivés à preuves-run-loupe-dev6/ AVEC le
    verdict [la double retouche de l'Entrée 209 : build dev.6 +
    kit dev.7])
"""


def refus(nom, detail):
    print(f"[archive] REFUS {nom} : {detail}")
    sys.exit(2)


def deplacer(fichier, destination_id, nouveau_nom=None):
    url = (ds.API + f"/files/{fichier['id']}"
           f"?addParents={destination_id}&removeParents={fichier['parents_courants']}")
    corps = {"name": nouveau_nom} if nouveau_nom else {}
    try:
        st, rep, _ = ds.api("PATCH", url, body=corps)
    except ds.SyncError as e:
        refus("DÉPLACEMENT", f"{fichier['nom']} : {e}")
    if st not in (200, 201):
        refus("DÉPLACEMENT", f"{fichier['nom']} : HTTP {st} : {rep[:150]!r}")


def main():
    print("=== M10-(e) : LE TÉMOIN DU RUN dev.6 ARCHIVÉ (l'Entrée 209 — "
          "le dossier du run loupe-kit/ au /test) ===")

    # -- 0. le dossier du run et ses preuves ------------------------------------
    racine = ds.list_folder(TEST_ID)
    kit = racine.get("loupe-kit")
    if not kit:
        refus("ÉTAT", "loupe-kit/ introuvable au /test — le dossier du run 6")
    preuves_run = ds.list_folder(kit["id"]).get("preuves-loupe")
    if not preuves_run:
        refus("ÉTAT", "loupe-kit/preuves-loupe/ introuvable — le témoin du run 6")
    temoins = ds.list_folder(preuves_run["id"])
    print(f"[0] le dossier du run : loupe-kit/ — preuves-loupe/ porte "
          f"{len(temoins)} pièce(s)")

    # -- 1. le dossier d'archive né ---------------------------------------------
    arch = ds.list_folder(ARCHIVES_PREUVES_ID)
    cible = arch.get(DOSSIER_ARCHIVE)
    if cible:
        print(f"[1] {DOSSIER_ARCHIVE}/ déjà né — idempotent")
        cible_id = cible["id"]
    else:
        cible_id = ds.create_folder(ARCHIVES_PREUVES_ID, DOSSIER_ARCHIVE)
        print(f"[1] {DOSSIER_ARCHIVE}/ né aux archives-preuves")

    # -- 2. les témoins déplacés, md5 recoupés APRÈS ----------------------------
    for nom, md5_attendu in TEMOINS.items():
        t = temoins.get(nom)
        if t is None:
            deja = ds.list_folder(cible_id).get(nom)
            if deja and deja.get("md5Checksum") == md5_attendu:
                print(f"[2] {nom} déjà archivé (md5 {md5_attendu[:8]}…) — "
                      f"idempotent")
                continue
            refus("TÉMOIN", f"{nom} absent du run ET de l'archive")
        if t.get("md5Checksum") != md5_attendu:
            refus("TÉMOIN", f"{nom} md5 divergent : {t.get('md5Checksum')} "
                  f"!= {md5_attendu}")
        fichier = {"id": t["id"], "nom": nom, "parents_courants": preuves_run["id"]}
        deplacer(fichier, cible_id)
        apres = ds.list_folder(cible_id).get(nom)
        if not apres or apres.get("md5Checksum") != md5_attendu:
            refus("TÉMOIN", f"{nom} : md5 divergent APRÈS déplacement")
        if nom in ds.list_folder(preuves_run["id"]):
            refus("TÉMOIN", f"{nom} demeure au run après déplacement")
        print(f"[2] archivé : {nom} (md5 {md5_attendu[:8]}… recoupé après)")

    # -- 3. le verdict déposé ------------------------------------------------------
    deja = ds.list_folder(cible_id).get("VERDICT-run-loupe-dev6.txt")
    if deja:
        print("[3] VERDICT-run-loupe-dev6.txt déjà déposé — idempotent")
    else:
        import tempfile
        import pathlib
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8", newline="\r\n") as f:
            f.write(VERDICT)
            chemin = f.name
        try:
            ds.upload_create(cible_id, "VERDICT-run-loupe-dev6.txt",
                             pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        print("[3] VERDICT-run-loupe-dev6.txt déposé (ROUGE AU T5 SUR UNE "
              "FAUSSE ERREUR — la sauvegarde PROUVÉE PAR LE FICHIER)")

    # -- 4. l'index mis à jour ------------------------------------------------------
    import urllib.request
    import tempfile
    import pathlib
    req = urllib.request.Request(
        f"https://drive.google.com/uc?export=download&id={INDEX_ID}")
    ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    if "preuves-run-loupe-dev6" in ancien:
        print("[4] l'index porte déjà le run dev.6 — idempotent")
    else:
        nouveau = ancien.rstrip("\n") + "\n" + NOTE_INDEX
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8", newline="\r\n") as f:
            f.write(nouveau)
            chemin = f.name
        try:
            ds.upload_update(INDEX_ID, pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        print("[4] LISEZMOI-archives-preuves.txt mis à jour (le run dev.6 "
              "archivé)")

    print("=== LE TÉMOIN DU RUN dev.6 ARCHIVÉ — la règle D143 tenue : "
          "DÉPLACEMENT, jamais un jet ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
