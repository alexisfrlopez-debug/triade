#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_m7d.py — LE COFFRE /test PASSÉ À LA VAGUE M7-(d) + LA CLÔTURE
D143 DU RUN m6d (règle D143 : archivage par DÉPLACEMENT, jamais un jet).

La vague m6d est CONSOMMÉE (le run m6d a rendu son verdict : LE RECOUP LABO
VERT 22/22 sur pièces croisées — Entrée 149, la finale 0.7.0 SCELLÉE) :
D143 l'archive. Le plan des jalons l'attendait : « la clôture D143 des
pièces du run attend le dépôt du kit M7 ».

  1. ARCHIVAGE DE LA VAGUE m6d → /test/archives-livraisons/vagues-m6/ :
     kit-m6d.zip, LISEZMOI-m6d.txt (déplacement, md5 constaté après) ;
  2. LA CLÔTURE D143 DES PIÈCES DU RUN m6d →
     /test/archives-preuves/preuves-run-m6d/ : temoin-m6d.txt,
     scenario-m6d-journal.log, VERDICT-run-m6d.txt (les pièces DU RUN) +
     VERDICT-recoup-labo-m6d.txt (le verdict du RECOUP laboratoire —
     Entrée 149, écrit par le présent geste : l'archive porte le jugement
     avec les pièces) ; preuves-m6/ DEMEURE à la racine avec son LISEZMOI
     (le réceptacle, modèle preuves-m5b) ;
  3. LES DEUX INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (la
     section m6d + la vague courante m7d), LISEZMOI-archives-preuves.txt
     (la section preuves-run-m6d) ;
  4. preuves-m7/ NÉ au coffre (le réceptacle des preuves du run M7-(d))
     avec son LISEZMOI-preuves.txt (les pièces attendues) ;
  5. LA VAGUE DÉPOSÉE à la racine de /test : kit-m7d.zip (le kit éprouvé
     au labo — extraction vierge + run VERT 16/16, assembler_kit_m7d.py)
     + LISEZMOI-m7d.txt (le document du kit, lisible AU coffre sans
     extraire) ;
  6. VÉRIFICATION : la racine porte la vague courante + les résidents
     D143 + les trois réceptacles + les deux salles d'archive ; les
     empreintes recoupées ; les pièces m6d CONSTATÉES dans leurs archives
     à l'identique (md5).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/deposer_kit_m7d.py
Code de sortie : 0 = coffre passé à la vague m7d ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_LOCAL = "/home/z/my-project/download/vague-m7d/kit-m7d.zip"
LISEZMOI_KIT = os.path.join(REPO, "riscv", "terrain", "LISEZMOI-KIT-M7D.md")

KIT_SHA = "85f7b4bfcd6828406bd0b8c0ebb6f4b1b1ba03c5def7346afa36c88019311490"
KIT_MD5 = "4d17f3fada9b54ccb21e232e0a0a1ca5"

# la vague m6d (la racine de /test) — archivée dans archives-livraisons/
VAGUE_M6D = ["kit-m6d.zip", "LISEZMOI-m6d.txt"]
# les pièces DU RUN m6d (dans preuves-m6/) — archivées dans archives-preuves/
PIECES_RUN_M6D = ["temoin-m6d.txt", "scenario-m6d-journal.log", "VERDICT-run-m6d.txt"]

VERDICT_RECOUP_M6D = """VERDICT DU RECOUP LABORATOIRE — RUN TERRAIN M6-(d) (D154 : sur pièces croisées, post-mortem)

LE RUN (la machine du développeur) : WSL2, noyau 6.18.54.1-microsoft-standard-WSL2 —
UN AUTRE noyau que celui du laboratoire, ASLR complet (randomize_va_space=2),
témoin daté du 04/11 21:16 +0100, le scellé relu AVANT tout geste
(sha256 dd14195c…).

LE RECOUP : VERT 22/22 SUR PIÈCES CROISÉES (scripts/recouper_run_m6d.py :
les trois pièces recoupées ENTRE ELLES — témoin ↔ journal ↔ verdict, —
l'arithmétique recomptée, les constats vérifiés contre la SOURCE du
scénario, le noyau constaté distinct, l'artefact recalculé au geste même ;
le premier passage a ÉCHOUÉ NOMMÉ : le défaut était dans L'INSTRUMENT du
recoup, corrigé et rejoué, les pièces immuables — D154).

LA CONSÉQUENCE : LA FINALE 0.7.0 SCELLÉE (--sceller-final : le contrôle D146
adapté vert + cristallisation 10/10 + conformité 7/7 AU GESTE MÊME — la
suite exécutant la démonstration M5-(c) ; la bascule rc.1→0.7.0 dans
frag-bld, occurrence unique assertée, verrou croisé 13/13, l'artefact
INTACT sha dd14195c… — le scellage est un fait de carte ; les gardes
vivantes : re-scellage REFUSÉ, reconstruction REFUSÉE, la balise 0.7.0
PRÉSERVÉE par la re-vérification).

Consignation : Entrée 149 du JOURNAL_TRAVAIL (le jalon M6 franchi — 05/11),
D154 née du geste. La présente pièce est déposée à la clôture D143 (le
05/11, au passage du coffre à la vague m7d) : l'archive porte le jugement
AVEC les pièces — la salle preuves-run-m6d/ est le dossier de fin de run.
"""

LISEZMOI_PREUVES_M7 = (
    "Ce dossier reçoit les preuves du run M7-(d) — l'universalité rejouée\n"
    "(terrain qemu-riscv64).\n"
    "Après le run, y déposer le dossier preuves-m7/ du kit EXTRAIT, ENTIER :\n"
    "  - temoin-m7d.txt            l'environnement de la machine (uname,\n"
    "                              python, le noyau hôte, la version ET le\n"
    "                              md5 de l'instrument qemu, les empreintes\n"
    "                              des artefacts relues AVANT le run)\n"
    "  - scenario-m7d-journal.log  le run entier, constat par constat\n"
    "  - VERDICT-run-m7d.txt       le verdict post-mortem (chaque constat,\n"
    "                              les frontières nommées, la réserve D149)\n"
    "Le kit vit à la racine de /test : kit-m7d.zip + LISEZMOI-m7d.txt.\n"
    "Le geste : extraire kit-m7d.zip dans un dossier NEUF, puis\n"
    "  python3 scenario-m7d.py\n"
    "(qemu-riscv64 est DANS le kit — binaire statique, aucun paquet, aucun\n"
    "réseau, aucun droit root ; la réserve instrumentale D149 est NOMMÉE\n"
    "dans chaque verdict : TCG, noyau et syscalls réels de l'hôte.)\n"
    "Un verdict ÉCHEC NOMMÉ se renvoie TEL QUEL : la ligne nomme le défaut,\n"
    "un échec honnête vaut plus qu'un vert muet.\n"
)

INDEX_LIVRAISONS_ADDENDUM = """
  kit-m6d.zip + LISEZMOI-m6d.txt
                                           vague m6d consommée (le run m6d a
                                           rendu son verdict : LE RECOUP LABO
                                           VERT 22/22 sur pièces croisées —
                                           Entrée 149/D154, la finale 0.7.0
                                           SCELLÉE, le jalon M6 franchi ;
                                           archivée le 05/11 au passage à la
                                           vague m7d)

--- la vague courante (racine de /test) : m7d — LE KIT TERRAIN M7-(d)
    (kit-m7d.zip + LISEZMOI-m7d.txt ; preuves-m7/ reçoit les preuves du run ;
    corriger-wsb.* demeurent résidents D143 de l'ère m5b, inutiles au run
    qemu mais jamais jetés) — mis à jour le 05/11/2026
"""

INDEX_PREUVES_SECTION = """
preuves-run-m6d/ (archivées le 05/11 au passage à la vague m7d — la clôture
D143 que le plan des jalons attendait au dépôt du kit M7) :
  - temoin-m6d.txt, scenario-m6d-journal.log, VERDICT-run-m6d.txt — les
    pièces DU RUN (la machine du développeur, WSL2 — un autre noyau que
    celui du laboratoire) ;
  - VERDICT-recoup-labo-m6d.txt — le verdict du RECOUP laboratoire
    (Entrée 149 : VERT 22/22 sur pièces croisées, la finale 0.7.0 scellée,
    D154) — l'archive porte le jugement AVEC les pièces.
  preuves-m6/ demeure à la racine avec son LISEZMOI (le réceptacle vide,
    modèle preuves-m5b).
"""


class Refus(Exception):
    """Tout refus nommé du passeur (fail-closed)."""


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
        raise Refus(f"'{nom}' demeure à son ancienne place après le déplacement")
    print(f"[archive] {nom} -> sa salle d'archive (md5 {md5_attendu[:8]}… constaté "
          f"après le geste — D143 : un déplacement, jamais un jet)")


def televerser_texte(parent_id, nom, contenu):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        f.write(contenu)
        chemin_tmp = pathlib.Path(f.name)
    try:
        ds.upload_create(parent_id, nom, chemin_tmp)
    finally:
        os.unlink(chemin_tmp)


def main() -> int:
    print("=== M7-(d) : le coffre /test passe à la vague m7d "
          "+ la clôture D143 du run m6d ===")

    # (0) le kit local doit être LE kit éprouvé ---------------------------------
    with open(KIT_LOCAL, "rb") as f:
        kit = f.read()
    if (hashlib.sha256(kit).hexdigest() != KIT_SHA
            or hashlib.md5(kit).hexdigest() != KIT_MD5):
        raise Refus("kit-m7d.zip local != le kit éprouvé (sha/md5) — "
                    "assembler_kit_m7d.py d'abord")

    racine = ds.list_folder(TEST_ID)
    arch_l = racine.get("archives-livraisons") or {}
    arch_p = racine.get("archives-preuves") or {}
    if not arch_l.get("id") or not arch_p.get("id"):
        raise Refus("les salles d'archive sont introuvables au coffre /test")

    # (1) ARCHIVAGE de la vague m6d -> vagues-m6/ --------------------------------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m6")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m6")
        print(f"[archive] vagues-m6/ créé dans archives-livraisons/ ({vagues_id})")
    else:
        vagues_id = vagues["id"]
        print(f"[archive] vagues-m6/ déjà présent — constaté")
    for nom in VAGUE_M6D:
        entree = racine.get(nom)
        if not entree:
            deja = ds.list_folder(vagues_id).get(nom)
            if deja:
                print(f"[archive] {nom} déjà archivé "
                      f"(md5 {deja.get('md5Checksum', '-')[:8]}…) — constaté")
                continue
            raise Refus(f"'{nom}' ni à la racine ni dans vagues-m6/ — introuvable")
        deplacer_vers(entree["id"], nom, TEST_ID, vagues_id,
                      entree.get("md5Checksum"))

    # (2) LA CLÔTURE D143 des pièces du run m6d -> preuves-run-m6d/ --------------
    pm6 = racine.get("preuves-m6") or {}
    if not pm6.get("id"):
        raise Refus("preuves-m6/ introuvable au coffre — la clôture D143 refuse")
    run_m6d = ds.list_folder(arch_p["id"]).get("preuves-run-m6d")
    if not run_m6d:
        run_id = ds.create_folder(arch_p["id"], "preuves-run-m6d")
        print(f"[clôture] preuves-run-m6d/ créé dans archives-preuves/ ({run_id})")
    else:
        run_id = run_m6d["id"]
        print(f"[clôture] preuves-run-m6d/ déjà présent — constaté")
    for nom in PIECES_RUN_M6D:
        entree = ds.list_folder(pm6["id"]).get(nom)
        if not entree:
            deja = ds.list_folder(run_id).get(nom)
            if deja:
                print(f"[clôture] {nom} déjà archivé "
                      f"(md5 {deja.get('md5Checksum', '-')[:8]}…) — constaté")
                continue
            raise Refus(f"'{nom}' ni dans preuves-m6/ ni dans l'archive — introuvable")
        deplacer_vers(entree["id"], nom, pm6["id"], run_id,
                      entree.get("md5Checksum"))
    if "VERDICT-recoup-labo-m6d.txt" not in ds.list_folder(run_id):
        televerser_texte(run_id, "VERDICT-recoup-labo-m6d.txt", VERDICT_RECOUP_M6D)
        print("[clôture] VERDICT-recoup-labo-m6d.txt déposé (le jugement AVEC "
              "les pièces — Entrée 149)")
    else:
        print("[clôture] VERDICT-recoup-labo-m6d.txt déjà là — constaté")
    restants = ds.list_folder(pm6["id"])
    if set(restants) != {"LISEZMOI-preuves.txt"}:
        raise Refus(f"preuves-m6/ ne porte pas seulement son LISEZMOI après la "
                    f"clôture : {sorted(restants)}")

    # (3) LES DEUX INDEX mis à jour ----------------------------------------------
    idx = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if not idx:
        raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
    _, body, _ = ds.api("GET", ds.API + "/files/" + idx["id"] + "?alt=media")
    texte = body.decode("utf-8")
    if "vague m7d" not in texte:
        texte = texte.rstrip("\n") + "\n" + INDEX_LIVRAISONS_ADDENDUM
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write(texte)
            chemin_tmp = pathlib.Path(f.name)
        try:
            ds.upload_update(idx["id"], chemin_tmp)
        finally:
            os.unlink(chemin_tmp)
        print("[index] LISEZMOI-archives-livraisons.txt mis à jour "
              "(la section m6d + la vague courante m7d)")
    else:
        print("[index] déjà à jour (la vague m7d y est nommée) — constaté")

    idxp = ds.list_folder(arch_p["id"]).get("LISEZMOI-archives-preuves.txt")
    if not idxp:
        raise Refus("LISEZMOI-archives-preuves.txt introuvable")
    _, bodyp, _ = ds.api("GET", ds.API + "/files/" + idxp["id"] + "?alt=media")
    textep = bodyp.decode("utf-8")
    if "preuves-run-m6d" not in textep:
        marqueur = "— Fin de l'index"
        if marqueur in textep:
            textep = textep.replace(marqueur,
                                    INDEX_PREUVES_SECTION.lstrip("\n") + "\n" + marqueur,
                                    1)
        else:
            textep = textep.rstrip("\n") + "\n" + INDEX_PREUVES_SECTION
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write(textep)
            chemin_tmp = pathlib.Path(f.name)
        try:
            ds.upload_update(idxp["id"], chemin_tmp)
        finally:
            os.unlink(chemin_tmp)
        print("[index] LISEZMOI-archives-preuves.txt mis à jour "
              "(la section preuves-run-m6d)")
    else:
        print("[index] déjà à jour (preuves-run-m6d y est nommée) — constaté")

    # (4) preuves-m7/ NÉ au coffre -------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    pm7 = racine.get("preuves-m7")
    if not pm7:
        pm7_id = ds.create_folder(TEST_ID, "preuves-m7")
        print(f"[preuves] preuves-m7/ créé au coffre ({pm7_id})")
    else:
        pm7_id = pm7["id"]
        print(f"[preuves] preuves-m7/ déjà présent ({pm7_id}) — constaté")
    if "LISEZMOI-preuves.txt" not in ds.list_folder(pm7_id):
        televerser_texte(pm7_id, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES_M7)
        print("[preuves] LISEZMOI-preuves.txt déposé (les pièces attendues)")
    else:
        print("[preuves] LISEZMOI-preuves.txt déjà là — constaté")

    # (5) LA VAGUE DÉPOSÉE à la racine ---------------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-m7d.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-m7d.zip", pathlib.Path(KIT_LOCAL))
        print(f"[vague] kit-m7d.zip déposé ({len(kit)} o, md5 {KIT_MD5[:8]}…)")
    else:
        if racine["kit-m7d.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("kit-m7d.zip présent au coffre mais md5 divergent — "
                        "refus de cohabiter deux kits")
        print("[vague] kit-m7d.zip déjà déposé à l'identique — constaté")
    racine = ds.list_folder(TEST_ID)
    if "LISEZMOI-m7d.txt" not in racine:
        ds.upload_create(TEST_ID, "LISEZMOI-m7d.txt", pathlib.Path(LISEZMOI_KIT))
        print("[vague] LISEZMOI-m7d.txt déposé (le document du kit, lisible "
              "au coffre sans extraire)")
    else:
        print("[vague] LISEZMOI-m7d.txt déjà là — constaté")

    # (6) LA VÉRIFICATION FINALE ----------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    attendus = {"kit-m7d.zip", "LISEZMOI-m7d.txt", "corriger-wsb.bat",
                "corriger-wsb.ps1", "preuves-m5b", "preuves-m6", "preuves-m7",
                "archives-livraisons", "archives-preuves"}
    manquants = attendus - set(racine)
    if manquants:
        raise Refus(f"la racine de /test ne porte pas {sorted(manquants)}")
    if racine["kit-m7d.zip"].get("md5Checksum") != KIT_MD5:
        raise Refus("le kit déposé au coffre != le kit éprouvé (md5)")
    print(f"[vérif] la racine de /test porte la vague m7d ({len(racine)} "
          f"entrées — les résidents D143 + les trois réceptacles + les deux "
          f"salles d'archive) :")
    for nom, meta in sorted(racine.items()):
        if meta.get("mimeType") == ds.FOLDER_MIME:
            print(f"[vérif]   [DIR ] {nom}")
        else:
            print(f"[vérif]   [{meta.get('size', '?'):>7} o] {nom}  "
                  f"md5={meta.get('md5Checksum', '-')[:8]}…")
    dans_vagues = ds.list_folder(ds.list_folder(arch_l["id"])["vagues-m6"]["id"])
    for nom in VAGUE_M6D:
        if nom not in dans_vagues:
            raise Refus(f"'{nom}' absent de vagues-m6/ après le geste")
    print(f"[vérif] la vague m6d CONSTATÉE dans vagues-m6/ "
          f"({len(VAGUE_M6D)} pièces, md5 intacts)")
    dans_run = ds.list_folder(ds.list_folder(arch_p["id"])["preuves-run-m6d"]["id"])
    attendues_run = set(PIECES_RUN_M6D) | {"VERDICT-recoup-labo-m6d.txt"}
    if attendues_run - set(dans_run):
        raise Refus(f"preuves-run-m6d/ incomplet : "
                    f"{sorted(attendues_run - set(dans_run))}")
    print(f"[vérif] la clôture D143 CONSTATÉE dans preuves-run-m6d/ "
          f"({len(attendues_run)} pièces : le run + le verdict du recoup)")
    print("=== le coffre /test vit à la vague m7d ; la clôture D143 du run m6d "
          "est FAITE — le run du développeur attend ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Refus, ds.SyncError) as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(2)
