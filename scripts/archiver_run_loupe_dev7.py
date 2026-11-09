#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_loupe_dev7.py — LE TÉMOIN DU RUN dev.7 ARCHIVÉ SUR PIÈCES
(règle D143 : archivage par DÉPLACEMENT, jamais un jet).

LE SEPTIÈME RUN TERRAIN (l'Entrée 210) : « dossier loupe-kit-7 déposé
dans le dossier /test du drive / le kit n'était pas dans le drive, il
faudrait que le prochain y soit » — le kit dev.7 (l'artefact dev.6,
sha256 13a869a3…, la retouche de l'Entrée 209) avait voyagé HORS
coffre (le zip par le canal du bac à sable — le labo n'avait pas le
droit d'écriture au /test) ; le terrain l'a vécu en loupe-kit-7/ ET
rendu avec ses preuves, D99 tenu.

LE TÉMOIN : [T0] TOUT VERT (l'empreinte dev.6 ASSERTÉE, la
cartographie, les scellés — l'affichage de la version portait le
LITTÉRAL PÉRIMÉ « 0x00010004 », la vérification comparait bien
0x00010006) ; [T1]→[T5] TOUT VERT — **LA BOUCLE D'ÉDITION ENTIÈRE
VÉCUE : l'octet 0 mûté 0x00→0x4D SEUL, la taille CONSTANTE, la marque
levée, la session close — le contrat publié de loupe-17 [0 = OK]
PROUVÉ AU TERRAIN, l'Entrée 209 ACQUITTÉE** ; [T6] ÉCHEC NOMMÉ
[REJET-ABSENT] : « le chemin qui ne désigne rien → 0xfffffffe != -2
ABSENT » — la pièce rendait SES codes d'échec par « mov eax, imm32 »
(EAX seul, les 32 bits hauts de RAX à zéro), le contrat c_int64 du
scénario lisait le qword ENTIER : la pièce disait -2, le kit entendait
4294967294 — [EAX-SANS-SIGNE] ; T7/S0 jamais atteints. LE TÉMOIN
VITRINE : les DEUX fenêtres mortes 0xC0000005, AUCUN rapport WER —
alors que l'Entrée 209 avait câblé le fil [r12 =
GetModuleHandleW(NULL), vérifié au désassemblage] : LE DIFFÉRENTIEL A
NOMMÉ [D54-QUATRIÈME] — la lignée prouvée termine CHAQUE plage
FirstThunk par un slot NULL, le build posait les QUATRE plages
CONTIGUËS : le chargeur du terrain (le CHEMIN FirstThunk, la leçon
D97) laissait la marche de kernel32 déborder chez les noms user32,
RegisterClassExW résout à NULL, et l'entrée APPELLE LE NUL —
QUATRIÈME manifestation de la dérive de dépôt [D54, D68, D98].

  1. LE DOSSIER D'ARCHIVE né aux archives-preuves :
     preuves-run-loupe-dev7/ ;
  2. LES DEUX TÉMOINS DÉPLACÉS du dossier du run
     (loupe-kit-7/preuves-loupe/ → l'archive) + md5 recoupés APRÈS ;
  3. LE VERDICT DU RUN déposé (VERDICT-run-loupe-dev7.txt : T0→T5
     TOUT VERT, la sauvegarde PROUVÉE — puis [EAX-SANS-SIGNE] au T6
     ET [D54-QUATRIÈME] à la vitrine) ;
  4. L'INDEX MIS À JOUR : LISEZMOI-archives-preuves.txt.

Le dossier du run loupe-kit-7/ DEMEURE au /test. Aucune suppression,
aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/archiver_run_loupe_dev7.py
Code de sortie : 0 = témoins archivés ; 2 = refus nommé."""

import os
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # dossier « test »
ARCHIVES_PREUVES_ID = "1TRZtOdvqfovvZt0jdFdpMysrpHNKOzFk"  # archives-preuves
INDEX_ID = "1WK5OOuMOFFoUj3PevftZo3pHIFKQx7zu"          # LISEZMOI-archives-preuves

DOSSIER_ARCHIVE = "preuves-run-loupe-dev7"

# les témoins du run dev.7 (le septième run, l'Entrée 210)
TEMOINS = {
    "temoin-loupe.txt": "c199de743e36781e1e73094ff0d1b235",    # 2 598 o
    "temoin-vitrine.txt": "4077286f732d0f8d71e58e6061e9be17",  # 389 o
}

VERDICT = """VERDICT DU RUN TERRAIN M10-(e) — LOUPE dev.7 : T0→T5 TOUT VERT, LA SAUVEGARDE PROUVÉE — PUIS DEUX DÉFAUTS NOMMÉS D'UN MÊME TÉMOIN ([EAX-SANS-SIGNE] AU KIT, [D54-QUATRIÈME] À LA PIÈCE)
==================================================================================================================================================================================
Le run du 09/11/2026 (la vague dev.7 de l'Entrée 209 — l'artefact
dev.6, sha256 13a869a3…, la carte génération 14 ; le kit voyagé
HORS coffre par le canal du bac à sable, le terrain l'a vécu en
loupe-kit-7/ ; le témoin déposé DANS le dossier du kit) :

  - [T0] TOUT VERT : l'empreinte ASSERTÉE (loupe.exe 127 488 o,
    sha256 13a869a3b31b41d6… — l'artefact dev.6 AUTHENTIQUE),
    l'image cartographiée DONT_RESOLVE, LE CADRE NÉ MIROIR, les
    scellés constatés, l'IAT 37 feuilles — l'affichage de la
    version portait le LITTÉRAL PÉRIMÉ « 0x00010004 » (la
    vérification comparait bien 0x00010006 — nommé, le kit dev.8
    le rend DYNAMIQUE {VERSION_R10}) ;
  - [T1]→[T5] TOUT VERT : la session sur L'OMBRE, la double
    lecture, LE PANNEAU, les lignes, la recherche — ET LA BOUCLE
    D'ÉDITION ENTIÈRE VÉCUE : l'octet 0 mûté 0x00→0x4D SEUL, la
    taille CONSTANTE, la marque levée, la session close — LE
    CONTRAT PUBLIÉ DE loupe-17 [0 = OK] PROUVÉ AU TERRAIN PAR LE
    VRAI WriteFile, L'ENTRÉE 209 ACQUITTÉE ;
  - [T6] ÉCHEC NOMMÉ [REJET-ABSENT] : « le chemin qui ne désigne
    rien → 0xfffffffe != -2 ABSENT » — [EAX-SANS-SIGNE] : la pièce
    rendait ses codes d'échec par « mov eax, imm32 » (EAX seul,
    les 32 bits hauts de RAX à zéro — mov sur registre 32 bits
    vide le haut), le contrat c_int64 du scénario lisait le qword
    ENTIER : la pièce disait -2, le kit entendait 4294967294 ;
    T7/S0 jamais atteints ;
  - LA VITRINE : les DEUX fenêtres mortes 0xC0000005
    (-1073741819), AUCUN rapport WER — alors que l'Entrée 209
    avait câblé le fil [r12 = GetModuleHandleW(NULL), vérifié au
    désassemblage] et que l'autopsie labo avait tout passé —
    [D54-QUATRIÈME] NOMMÉ PAR LE DIFFÉRENTIEL : la lignée prouvée
    (demo.exe 0.3.0, le scellé M2 dont la fenêtre VÉCUT au même
    terrain) termine CHAQUE plage FirstThunk par un slot NULL
    (5/5) ; le build posait les QUATRE plages CONTIGUËS
    [kernel32@0x2400 · user32@0x2450 · gdi32@0x24E0 ·
    double@0x2818 — 3/4 sans séparateur] : le chargeur du terrain
    (le CHEMIN FirstThunk, la leçon D97) marche chaque plage
    jusqu'au premier NULL — la marche de kernel32 déborde chez les
    noms user32, RegisterClassExW résout à NULL, ET L'ENTRÉE
    APPELLE LE NUL — QUATRIÈME manifestation de la dérive de
    dépôt [D54, D68, D98, et celle-ci].

LA DOUBLE RETOUCHE DE L'ENTRÉE 210 : la pièce dev.7 (l'IAT
ENTIÈRE relogée à 0x3100 — QUATRE plages SÉPARÉES PAR NULL,
préremplies des RVA de noms, dir[12] mis à jour, les 63 sites
repointés, les vieilles plages VIDÉES ; les 20 rendus négatifs
étendus au 64 bits par « push imm8 ; pop rax » ; sha256
388d4680…, TAILLE INCHANGÉE 127 488 o, R7 tenue, le qword
version 0x00010007) ET le kit dev.8 (LE CONTRÔLE D54 au T0 — le
scénario MARCHE lui-même les quatre plages au compte exact ;
l'affichage de la version DYNAMIQUE).
"""

NOTE_INDEX = """
--- le run loupe dev.7 archivé (le septième run, l'Entrée 210 — le
    kit dev.7 voyagé HORS coffre par le canal du bac à sable, le
    terrain l'a vécu en loupe-kit-7/) : T0→T5 TOUT VERT — LA
    SAUVEGARDE DE L'ENTRÉE 209 PROUVÉE AU TERRAIN, la boucle
    d'édition ENTIÈRE vivante [l'octet 0 mûté 0x00→0x4D SEUL, la
    taille constante, la marque levée] — PUIS [T6] ÉCHEC NOMMÉ
    [REJET-ABSENT] : « 0xfffffffe != -2 » — [EAX-SANS-SIGNE] : la
    pièce rendait « mov eax, imm32 », le contrat c_int64 lisait le
    qword entier ; ET la vitrine morte ×2 0xC0000005 sans rapport
    WER — [D54-QUATRIÈME] nommé par le différentiel : les QUATRE
    plages FirstThunk CONTIGUËS, le chargeur du terrain marche
    chaque plage jusqu'au NULL — la marche de kernel32 déborde
    chez user32, RegisterClassExW résout à NULL, l'entrée appelle
    le NUL ; témoins temoin-loupe.txt 2 598 o md5 c199de74… +
    temoin-vitrine.txt 389 o md5 4077286f… archivés à
    preuves-run-loupe-dev7/ AVEC le verdict [la double retouche de
    l'Entrée 210 : pièce dev.7 + kit dev.8])
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
    print("=== M10-(e) : LE TÉMOIN DU RUN dev.7 ARCHIVÉ (l'Entrée 210 — "
          "le dossier du run loupe-kit-7/ au /test) ===")

    # -- 0. le dossier du run et ses preuves ------------------------------------
    racine = ds.list_folder(TEST_ID)
    kit = racine.get("loupe-kit-7")
    if not kit:
        refus("ÉTAT", "loupe-kit-7/ introuvable au /test — le dossier du run 7")
    preuves_run = ds.list_folder(kit["id"]).get("preuves-loupe")
    if not preuves_run:
        refus("ÉTAT", "loupe-kit-7/preuves-loupe/ introuvable — le témoin du run 7")
    temoins = ds.list_folder(preuves_run["id"])
    print(f"[0] le dossier du run : loupe-kit-7/ — preuves-loupe/ porte "
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
    deja = ds.list_folder(cible_id).get("VERDICT-run-loupe-dev7.txt")
    if deja:
        print("[3] VERDICT-run-loupe-dev7.txt déjà déposé — idempotent")
    else:
        import tempfile
        import pathlib
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8", newline="\r\n") as f:
            f.write(VERDICT)
            chemin = f.name
        try:
            ds.upload_create(cible_id, "VERDICT-run-loupe-dev7.txt",
                             pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        print("[3] VERDICT-run-loupe-dev7.txt déposé (T0→T5 TOUT VERT, la "
              "sauvegarde PROUVÉE — puis [EAX-SANS-SIGNE] + [D54-QUATRIÈME])")

    # -- 4. l'index mis à jour ------------------------------------------------------
    import urllib.request
    import tempfile
    import pathlib
    req = urllib.request.Request(
        f"https://drive.google.com/uc?export=download&id={INDEX_ID}")
    ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    if "preuves-run-loupe-dev7" in ancien:
        print("[4] l'index porte déjà le run dev.7 — idempotent")
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
        print("[4] LISEZMOI-archives-preuves.txt mis à jour (le run dev.7 "
              "archivé)")

    print("=== LE TÉMOIN DU RUN dev.7 ARCHIVÉ — la règle D143 tenue : "
          "DÉPLACEMENT, jamais un jet ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
