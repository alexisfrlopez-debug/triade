#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_loupe_dev8.py + deposer_kit_loupe_r9.py — LE HUITIÈME RUN
ARCHIVÉ, LA VAGUE dev.8 VERSIONNÉE, LA VAGUE dev.9 DÉPOSÉE (règle D143 :
archivage par DÉPLACEMENT, jamais un jet).

LE HUITIÈME RUN TERRAIN (l'Entrée 213) : « dossier loupe-kit-8 avec les
preuves déposé dans le dossier /test du drive » — LA PREMIÈRE VAGUE
DÉPOSÉE PAR LE LABO LUI-MÊME (l'Entrée 211), vécue par le terrain.

LE TÉMOIN : T0→T7 TOUT VERT — LA PREMIÈRE FOIS [le contrôle D54 VERT,
la boucle d'édition, LES QUATRE REJETS DU T6 : -2, -5, -3, -1 —
[EAX-SANS-SIGNE] ACQUITTÉ, la clôture T7] ; [S0] ÉCHEC NOMMÉ
[SONDE-PYTHON] : ctypes.SetLastError inexistant — la cascade jamais
jouée ; LA VITRINE : morte ×2 0xC0000005, aucun WER — LA CINQUIÈME.

LA RETOUCHE DE L'ENTRÉE 213 : LA PIÈCE DEMEURE dev.7 (ACQUITTÉE —
l'autopsie la plus complète + LE SIMULATEUR DE VITRINE né au labo :
les deux vitrines vécues vertes sous Unicorn) ET LE KIT dev.9 (la
sonde S0 réparée, VERSION_TXT dérivé, LE TÉMOIN VITRINE PORTANT [4/4]
— le journal d'événements nommera la sixième mort si elle vient).

Usage : python3 scripts/deposer_kit_dev9.py
Code de sortie : 0 = tout déposé ; 2 = refus nommé."""

import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
ARCHIVES_PREUVES_ID = "1TRZtOdvqfovvZt0jdFdpMysrpHNKOzFk"
ARCHIVES_LIVRAISONS_ID = "1meUs8boUlod9cYYA6wlGn3NUEu8QiE76"
VAGUES_M10_ID = "1fk4etZwRRPMQMKTRX85QPOm5F7Q7qVPW"
RECEPTACLE_ID = "1WGeSPOU-LOnLGSVsisjp1HZrE-j8-Khd"
INDEX_PREUVES_ID = "1WK5OOuMOFFoUj3PevftZo3pHIFKQx7zu"
INDEX_LIVRAISONS_ID = "1LW5UyFaSPDziI1gMVhn5WmnPVLt3fW9s"
RECEPTACLE_LISEZMOI_ID = "1Q28-cq5TVuaVNGMroT3EkuuN-DrCkF_A"

LABO = "/home/z/my-project"
VERDICT_CHEMIN = f"{LABO}/coffre/VERDICT-run-loupe-dev8.txt"
KIT_NEUF = f"{LABO}/build-dev9/kit-loupe.zip"
LISEZMOI_NEUF = f"{LABO}/triade/loupe/terrain/LISEZMOI-KIT-LOUPE.md"
RECEPTACLE_NEUF = f"{LABO}/coffre/LISEZMOI-preuves-NEUF.txt"
DOSSIER_KIT9 = f"{LABO}/build-dev9/loupe-kit-9"

DOSSIER_ARCHIVE = "preuves-run-loupe-dev8"
TEMOINS = {
    "temoin-loupe.txt": "c8a0de8cd2c748c2c852b9687834738e",    # 3 636 o
    "temoin-vitrine.txt": "d5a792f0c0471271c0b6b44b812daba3",  # 389 o
}
VAGUE_ANCIENNE = {"kit-loupe.zip": "33b7ff3e",          # md5 partiel
                  "LISEZMOI-loupe.txt": "40111d26"}

NOTE_INDEX_PREUVES = """
--- le run loupe dev.8 archivé (le huitième run, l'Entrée 213 — LA
    PREMIÈRE VAGUE DÉPOSÉE PAR LE LABO LUI-MÊME, l'Entrée 211) :
    T0→T7 TOUT VERT — LA PREMIÈRE FOIS, le contrat fonctionnel
    ENTIÈREMENT PROUVÉ [le contrôle D54 VERT, la boucle d'édition,
    LES QUATRE REJETS DU T6 vécus verts : -2, -5, -3, -1 —
    [EAX-SANS-SIGNE] ACQUITTÉ, la clôture T7 : l'artefact relu
    inchangé] ; [S0] ÉCHEC NOMMÉ [SONDE-PYTHON] :
    ctypes.SetLastError inexistant — la cascade de l'Entrée 205
    mourut sur place, jamais jouée ; ET la vitrine morte ×2
    0xC0000005 sans rapport WER — LA CINQUIÈME MORT, la pièce
    ACQUITTÉE par l'autopsie la plus complète [imports,
    instruction par instruction, ZÉRO SSE, ZÉRO pointeur absolu,
    les 63 sites recoupés] + LE SIMULATEUR DE VITRINE né au labo
    [les deux vitrines vécues vertes sous Unicorn — sortie propre
    ExitProcess(0)] ; témoins temoin-loupe.txt 3 636 o md5
    c8a0de8c… + temoin-vitrine.txt 389 o md5 d5a792f0… archivés
    à preuves-run-loupe-dev8/ AVEC le verdict [la retouche de
    l'Entrée 213 : la pièce demeure dev.7 l'acquittée + le kit
    dev.9 — la sonde S0 réparée, le témoin vitrine PORTANT {4/4}
    le journal d'événements])
"""

NOTE_INDEX_LIVRAISONS = """
--- la vague loupe dev.8 archivée (consommée par le huitième run,
    l'Entrée 213) : kit-loupe.zip md5 33b7ff3e… + LISEZMOI-loupe.txt
    md5 40111d26… → vagues-m10/ EN PIÈCES VERSIONNÉES
    [kit-loupe-dev.8.zip + LISEZMOI-loupe-dev.8.txt] — la première
    vague déposée AU COFFRE PAR LE LABO LUI-MÊME (l'Entrée 211) ;
    le terrain l'a vécue en loupe-kit-8/ : T0→T7 TOUT VERT LA
    PREMIÈRE FOIS, puis [SONDE-PYTHON] au S0 et la vitrine morte
    pour la cinquième fois — la pièce ACQUITTÉE, le témoin
    ré-armé PORTANT.

--- la vague courante (racine de /test) : loupe dev.9 — LA VAGUE DU
    TÉMOIN PORTANT (kit-loupe.zip md5 a7a6bb76… + LISEZMOI-loupe.txt
    md5 44a36c85… ; loupe.exe 0.1.0-dev.7 INCHANGÉE, 127 488 o,
    sha256 388d4680… — L'ACQUITTÉE, aucune retouche sans défaut
    nommé, la méthode ; ET LE SCÉNARIO dev.9 : LA SONDE S0 RÉPARÉE
    [k32.SetLastError + ctypes.get_last_error sur un WinDLL né
    use_last_error=True], VERSION_TXT DÉRIVÉ de VERSION_R10 [le
    littéral périmé chassé], le texte T0 nomme la carte à sa
    génération réelle [13] ; ET LE TÉMOIN VITRINE dev.9 PORTANT :
    [4/4] LE JOURNAL D'ÉVÉNEMENTS — wevtutil consigne l'Application
    Error 1000 : LE MODULE FAUTIF ET LE DÉCALAGE DE L'EXCEPTION
    NOMMÉS — la sixième mort, si elle vient, sera nommée) — livrée
    le 09/11/2026, déposée par le labo en la forme canonique
    kit-loupe.zip + LISEZMOI ET en la forme dossier loupe-kit-9/
    prête à courir ; la balise `loupe 0.1.0` attend le vert
    recoupé : LE JALON M10.
"""


def refus(nom, detail):
    print(f"[depot] REFUS {nom} : {detail}")
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


def deposer_texte(folder_id, nom, texte):
    """Dépose un fichier texte (CRLF), idempotent par contenu."""
    deja = ds.list_folder(folder_id).get(nom)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8", newline="\r\n") as f:
        f.write(texte)
        chemin = f.name
    try:
        if deja:
            ds.upload_update(deja["id"], pathlib.Path(chemin))
        else:
            ds.upload_create(folder_id, nom, pathlib.Path(chemin))
    finally:
        os.unlink(chemin)


def lire_index(file_id):
    import urllib.request
    req = urllib.request.Request(
        f"https://drive.google.com/uc?export=download&id={file_id}")
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8")


def maj_index(file_id, note, marqueur):
    ancien = lire_index(file_id)
    if marqueur in ancien:
        print(f"    l'index porte déjà « {marqueur} » — idempotent")
        return
    nouveau = ancien.rstrip("\n") + "\n" + note
    import tempfile
    import pathlib
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8", newline="\r\n") as f:
        f.write(nouveau)
        chemin = f.name
    try:
        ds.upload_update(file_id, pathlib.Path(chemin))
    finally:
        os.unlink(chemin)
    print(f"    l'index mis à jour (+{len(note)} caractères)")


def main():
    print("=== M10-(e) : LE RUN dev.8 ARCHIVÉ + LA VAGUE dev.9 DÉPOSÉE "
          "(l'Entrée 213) ===")

    # -- 0. l'état du coffre ------------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    kit8 = racine.get("loupe-kit-8")
    if not kit8:
        refus("ÉTAT", "loupe-kit-8/ introuvable au /test — le dossier du run 8")
    preuves_run = ds.list_folder(kit8["id"]).get("preuves-loupe")
    if not preuves_run:
        refus("ÉTAT", "loupe-kit-8/preuves-loupe/ introuvable")
    temoins = ds.list_folder(preuves_run["id"])
    print(f"[0] loupe-kit-8/ — preuves-loupe/ porte {len(temoins)} pièce(s)")

    # -- 1. le dossier d'archive du run né ----------------------------------------
    arch = ds.list_folder(ARCHIVES_PREUVES_ID)
    cible = arch.get(DOSSIER_ARCHIVE)
    if cible:
        print(f"[1] {DOSSIER_ARCHIVE}/ déjà né — idempotent")
        cible_id = cible["id"]
    else:
        cible_id = ds.create_folder(ARCHIVES_PREUVES_ID, DOSSIER_ARCHIVE)
        print(f"[1] {DOSSIER_ARCHIVE}/ né aux archives-preuves")

    # -- 2. les témoins déplacés, md5 recoupés APRÈS ------------------------------
    for nom, md5_attendu in TEMOINS.items():
        t = temoins.get(nom)
        if t is None:
            deja = ds.list_folder(cible_id).get(nom)
            if deja and deja.get("md5Checksum") == md5_attendu:
                print(f"[2] {nom} déjà archivé — idempotent")
                continue
            refus("TÉMOIN", f"{nom} absent du run ET de l'archive")
        if t.get("md5Checksum") != md5_attendu:
            refus("TÉMOIN", f"{nom} md5 divergent : {t.get('md5Checksum')} "
                  f"!= {md5_attendu}")
        deplacer({"id": t["id"], "nom": nom,
                  "parents_courants": preuves_run["id"]}, cible_id)
        apres = ds.list_folder(cible_id).get(nom)
        if not apres or apres.get("md5Checksum") != md5_attendu:
            refus("TÉMOIN", f"{nom} : md5 divergent APRÈS déplacement")
        print(f"[2] archivé : {nom} (md5 {md5_attendu[:8]}… recoupé après)")

    # -- 3. le verdict du run déposé ----------------------------------------------
    verdict = open(VERDICT_CHEMIN, encoding="utf-8").read()
    deposer_texte(cible_id, "VERDICT-run-loupe-dev8.txt", verdict)
    print("[3] VERDICT-run-loupe-dev8.txt déposé (T0→T7 TOUT VERT LA "
          "PREMIÈRE FOIS — puis [SONDE-PYTHON] et la vitrine ; la pièce "
          "ACQUITTÉE)")

    # -- 4. la vague dev.8 versionnée aux archives (DÉPLACEMENT) ------------------
    for nom, md5_partiel in VAGUE_ANCIENNE.items():
        f = racine.get(nom)
        if f is None:
            deja = ds.list_folder(VAGUES_M10_ID).get(
                nom.replace(".zip", "-dev.8.zip").replace(
                    "LISEZMOI-loupe.txt", "LISEZMOI-loupe-dev.8.txt"))
            if deja:
                print(f"[4] {nom} déjà versionné — idempotent")
                continue
            refus("VAGUE", f"{nom} introuvable à la racine du /test")
        if not f.get("md5Checksum", "").startswith(md5_partiel):
            refus("VAGUE", f"{nom} md5 divergent : {f.get('md5Checksum')} "
                  f"!= {md5_partiel}…")
        nouveau_nom = ("kit-loupe-dev.8.zip" if nom.endswith(".zip")
                       else "LISEZMOI-loupe-dev.8.txt")
        deplacer({"id": f["id"], "nom": nom,
                  "parents_courants": TEST_ID}, VAGUES_M10_ID, nouveau_nom)
        apres = ds.list_folder(VAGUES_M10_ID).get(nouveau_nom)
        if not apres or not apres.get("md5Checksum", "").startswith(md5_partiel):
            refus("VAGUE", f"{nom} : md5 divergent APRÈS déplacement")
        print(f"[4] versionné : {nom} → vagues-m10/{nouveau_nom} "
              f"(md5 {md5_partiel}… recoupé après)")

    # -- 5. la vague dev.9 déposée à la racine ------------------------------------
    import hashlib
    kit_md5 = hashlib.md5(open(KIT_NEUF, "rb").read()).hexdigest()
    li_md5 = hashlib.md5(open(LISEZMOI_NEUF, "rb").read()).hexdigest()
    assert kit_md5.startswith("a7a6bb76") and li_md5.startswith("44a36c85")
    if racine.get("kit-loupe.zip") is None:
        ds.upload_create(TEST_ID, "kit-loupe.zip", pathlib.Path(KIT_NEUF))
        print(f"[5] kit-loupe.zip DÉPOSÉ (md5 {kit_md5[:8]}…, 31 688 o — "
              f"la vague dev.9)")
    else:
        print("[5] kit-loupe.zip déjà présent — idempotent")
    if racine.get("LISEZMOI-loupe.txt") is None:
        ds.upload_create(TEST_ID, "LISEZMOI-loupe.txt",
                         pathlib.Path(LISEZMOI_NEUF))
        print(f"[5] LISEZMOI-loupe.txt DÉPOSÉ (md5 {li_md5[:8]}…)")
    else:
        print("[5] LISEZMOI-loupe.txt déjà présent — idempotent")

    # -- 6. le kit visible loupe-kit-9/ (les QUATRE pièces du contrat) ------------
    racine2 = ds.list_folder(TEST_ID)
    kit9 = racine2.get("loupe-kit-9")
    if kit9:
        print("[6] loupe-kit-9/ déjà né — idempotent")
        kit9_id = kit9["id"]
    else:
        kit9_id = ds.create_folder(TEST_ID, "loupe-kit-9")
        print("[6] loupe-kit-9/ né")
    for piece in ("loupe.exe", "scenario-loupe.py", "temoin-vitrine.bat",
                  "LISEZMOI-KIT-LOUPE.md"):
        deja = ds.list_folder(kit9_id).get(piece)
        if deja:
            print(f"[6]   {piece} déjà déposé — idempotent")
            continue
        ds.upload_create(kit9_id, piece,
                         pathlib.Path(f"{DOSSIER_KIT9}/{piece}"))
        c = open(f"{DOSSIER_KIT9}/{piece}", "rb").read()
        print(f"[6]   {piece} déposé ({len(c)} o, "
              f"md5 {hashlib.md5(c).hexdigest()[:8]}…)")

    # -- 7. le réceptacle ré-armé ---------------------------------------------------
    recep = open(RECEPTACLE_NEUF, encoding="utf-8").read()
    deposer_texte(RECEPTACLE_ID, "LISEZMOI-preuves.txt", recep)
    print("[7] le réceptacle preuves-loupe/ ré-armé (l'artefact attendu "
          "0.1.0-dev.7 L'ACQUITTÉE, LE TÉMOIN VITRINE PORTANT [4/4] REQUIS)")

    # -- 8. les index mis à jour ----------------------------------------------------
    print("[8] les index :")
    maj_index(INDEX_PREUVES_ID, NOTE_INDEX_PREUVES, "preuves-run-loupe-dev8")
    maj_index(INDEX_LIVRAISONS_ID, NOTE_INDEX_LIVRAISONS,
              "la vague loupe dev.8 archivée")

    print("\n=== TERMINÉ : le run 8 archivé, la vague dev.8 versionnée, "
          "LA VAGUE dev.9 AU COFFRE ===")
    print("SUITE : LE RUN DU KIT dev.9 — T0→S0 ENTIERS ET LA VITRINE "
          "VIVANTE ; SI LA MORT VIENT ENCORE : LE JOURNAL D'ÉVÉNEMENTS "
          "[4/4] LA NOMMERA.")


if __name__ == "__main__":
    main()
