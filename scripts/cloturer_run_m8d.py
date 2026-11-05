#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cloturer_run_m8d.py — LA CLÔTURE D143 DU RUN M8-(d) : les pièces du run
déplacées de /test/preuves-m8d/ vers /test/archives-preuves/preuves-run-m8d/
(règle D143 : archivage par DÉPLACEMENT, jamais un jet), le VERDICT-DU-RECOUP
laboratoire déposé AVEC elles (l'archive porte le jugement avec les pièces —
modèle m7d/Entrée 155), les DEUX index mis à jour, preuves-m8d/ DEMEURE à la
racine avec son LISEZMOI (le réceptacle, prêt à un éventuel nouveau run).

La vague m8d (kit-m8d.zip + LISEZMOI-m8d.txt) DEMEURE la vague courante à la
racine de /test : le jalon M8 est FRANCHI (finale 0.9.0 scellée), aucun kit
suivant n'est annoncé — rien ne se jette (D143).

Usage : python3 scripts/cloturer_run_m8d.py
Code de sortie : 0 = clôture faite et recoupée ; 2 = refus nommé."""

import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m8d/VERDICT-recoup-m8d.txt")

PIECES_RUN_M8D = ["temoin-m8d.txt", "scenario-m8d-journal.log",
                  "VERDICT-run-m8d.txt", "chemin-a-hello02.txt",
                  "chemin-b-sys03.txt", "chemin-c-refus.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m8d/ (clôturées le 05/11 au geste final — le run M8-(d) VERT sur
pièces, le recoup labo 30/30, la finale 0.9.0 scellée, LE JALON M8 FRANCHI) :
  - temoin-m8d.txt, scenario-m8d-journal.log, VERDICT-run-m8d.txt,
    chemin-a-hello02.txt, chemin-b-sys03.txt, chemin-c-refus.txt — les pièces
    DU RUN (la machine du développeur, Windows 10.0 build 26300 natif — le
    VRAI ntdll lu par les DEUX lecteurs indépendants, le SSN RE-LU de
    l'imm32 du stub consigné, LA TWIN 33 octets par les DEUX chemins [l'IAT
    kernel32 et le syscall direct NtWriteFile], le refus nommé -1 sur pièce
    VIDE) ;
  - VERDICT-recoup-labo-m8d.txt — le verdict du RECOUP laboratoire (le juge
    est le code : les constantes importées de la source, le fixture et le
    sha RECALCULÉS au geste même ; RECOUP VERT 30/30 sur pièces croisées —
    deux défauts d'instrument nommés par le fail-closed, corrigés et
    rejoués, les pièces immuables ; LA FINALE 0.9.0 SCELLÉE — l'artefact
    intact 1492b0bc…, le jalon M8 franchi, D165) — l'archive porte le
    jugement AVEC les pièces.
  preuves-m8d/ demeure à la racine avec son LISEZMOI (le réceptacle, prêt à
  un éventuel nouveau run).
"""

INDEX_LIVRAISONS_ADDENDUM = """

--- note du 05/11/2026 (le geste final M8-(d)) : la vague m8d DEMEURE la
    vague courante — le run terrain est VENU (35 verts / 0 échecs, le recoup
    labo 30/30 sur pièces croisées, LA FINALE 0.9.0 SCELLÉE — LE JALON M8
    FRANCHI, le programme M8 accompli) ; aucun kit suivant n'est annoncé,
    la vague ne se consomme pas d'elle-même : rien ne se jette (D143).
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
    print(f"[clôture] {nom} -> preuves-run-m8d/ (md5 {md5_attendu[:8]}… constaté "
          f"après le geste — D143 : un déplacement, jamais un jet)")


def maj_index_texte(file_id, marqueur, section, nom_log):
    _, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    texte = body.decode("utf-8")
    if marqueur in texte:
        print(f"[index] {nom_log} déjà à jour — constaté")
        return
    if marqueur == "preuves-run-m8d":
        fin = "— Fin de l'index"
        if fin in texte:
            texte = texte.replace(fin, section.lstrip("\n") + "\n" + fin, 1)
        else:
            texte = texte.rstrip("\n") + "\n" + section
    else:
        texte = texte.rstrip("\n") + "\n" + section
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as f:
        f.write(texte)
        chemin_tmp = pathlib.Path(f.name)
    try:
        ds.upload_update(file_id, chemin_tmp)
    finally:
        os.unlink(chemin_tmp)
    print(f"[index] {nom_log} mis à jour")


def main() -> int:
    print("=== M8-(d) : LA CLÔTURE D143 DU RUN m8d — les pièces à l'archive "
          "AVEC le verdict du recoup ===")

    if not VERDICT_RECOUP_LOCAL.exists():
        raise Refus("VERDICT-recoup-m8d.txt local introuvable — le recoup "
                    "d'abord (scripts/recouper_run_m8d.py)")

    racine = ds.list_folder(TEST_ID)
    arch_p = racine.get("archives-preuves")
    arch_l = racine.get("archives-livraisons")
    if not (arch_p or {}).get("id") or not (arch_l or {}).get("id"):
        raise Refus("les salles d'archive sont introuvables au coffre /test")

    # (1) les SIX pièces du run -> preuves-run-m8d/ ------------------------------
    pm8 = racine.get("preuves-m8d") or {}
    if not pm8.get("id"):
        raise Refus("preuves-m8d/ introuvable au coffre — la clôture refuse")
    run_m8d = ds.list_folder(arch_p["id"]).get("preuves-run-m8d")
    if not run_m8d:
        run_id = ds.create_folder(arch_p["id"], "preuves-run-m8d")
        print(f"[clôture] preuves-run-m8d/ créé dans archives-preuves/ ({run_id})")
    else:
        run_id = run_m8d["id"]
        print("[clôture] preuves-run-m8d/ déjà présent — constaté")
    for nom in PIECES_RUN_M8D:
        entree = ds.list_folder(pm8["id"]).get(nom)
        if not entree:
            deja = ds.list_folder(run_id).get(nom)
            if deja:
                print(f"[clôture] {nom} déjà archivé "
                      f"(md5 {deja.get('md5Checksum', '-')[:8]}…) — constaté")
                continue
            raise Refus(f"'{nom}' ni dans preuves-m8d/ ni dans l'archive — "
                        "introuvable")
        deplacer_vers(entree["id"], nom, pm8["id"], run_id,
                      entree.get("md5Checksum"))

    # (2) le VERDICT-DU-RECOUP du labo déposé AVEC les pièces --------------------
    if "VERDICT-recoup-labo-m8d.txt" not in ds.list_folder(run_id):
        ds.upload_create(run_id, "VERDICT-recoup-labo-m8d.txt",
                         VERDICT_RECOUP_LOCAL)
        print("[clôture] VERDICT-recoup-labo-m8d.txt déposé (le jugement AVEC "
              "les pièces — RECOUP VERT 30/30, la finale 0.9.0 scellée)")
    else:
        print("[clôture] VERDICT-recoup-labo-m8d.txt déjà là — constaté")

    # (3) preuves-m8d/ ne porte plus que son LISEZMOI -----------------------------
    restants = ds.list_folder(pm8["id"])
    if set(restants) != {"LISEZMOI-preuves.txt"}:
        raise Refus(f"preuves-m8d/ ne porte pas seulement son LISEZMOI après "
                    f"la clôture : {sorted(restants)}")

    # (4) LES DEUX INDEX mis à jour ------------------------------------------------
    idxp = ds.list_folder(arch_p["id"]).get("LISEZMOI-archives-preuves.txt")
    if not idxp:
        raise Refus("LISEZMOI-archives-preuves.txt introuvable")
    maj_index_texte(idxp["id"], "preuves-run-m8d", INDEX_PREUVES_SECTION,
                    "LISEZMOI-archives-preuves.txt (la section preuves-run-m8d)")

    idxl = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if not idxl:
        raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
    maj_index_texte(idxl["id"], "la vague m8d DEMEURE la vague courante",
                    INDEX_LIVRAISONS_ADDENDUM,
                    "LISEZMOI-archives-livraisons.txt (la vague m8d demeure)")

    # (5) LA VÉRIFICATION FINALE -----------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    attendus = {"kit-m8d.zip", "LISEZMOI-m8d.txt", "corriger-wsb.bat",
                "corriger-wsb.ps1", "preuves-m5b", "preuves-m6", "preuves-m7",
                "preuves-m8d", "archives-livraisons", "archives-preuves"}
    manquants = attendus - set(racine)
    if manquants:
        raise Refus(f"la racine de /test ne porte pas {sorted(manquants)}")
    if racine["kit-m8d.zip"].get("md5Checksum") != "ad6cbffe70e48695495d1073e149e580":
        raise Refus("le kit de la racine a divergé — refus")
    dans_run = ds.list_folder(run_id)
    attendues_run = set(PIECES_RUN_M8D) | {"VERDICT-recoup-labo-m8d.txt"}
    if attendues_run - set(dans_run):
        raise Refus(f"preuves-run-m8d/ incomplet : "
                    f"{sorted(attendues_run - set(dans_run))}")
    print(f"[vérif] la clôture D143 du run m8d CONSTATÉE dans "
          f"preuves-run-m8d/ ({len(attendues_run)} pièces : le run + le "
          f"verdict du recoup — l'archive porte le jugement avec les pièces)")
    print(f"[vérif] preuves-m8d/ ne porte plus que son LISEZMOI "
          f"(le réceptacle demeure)")
    print("[vérif] la vague m8d DEMEURE la vague courante à la racine "
          "(kit-m8d.zip md5 ad6cbffe… recoupé — le jalon M8 franchi, aucun "
          "kit suivant annoncé, rien ne se jette)")
    print("=== la clôture D143 du run m8d est FAITE — LE JALON M8 FRANCHI, "
          "l'archive porte le jugement avec les pièces ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Refus, ds.SyncError) as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(2)
