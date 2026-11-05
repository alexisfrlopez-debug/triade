#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cloturer_run_m7d.py — LA CLÔTURE D143 DU RUN M7-(d) : les pièces du run
déplacées de /test/preuves-m7/ vers /test/archives-preuves/preuves-run-m7d/
(règle D143 : archivage par DÉPLACEMENT, jamais un jet), le VERDICT-DU-RECOUP
laboratoire déposé AVEC elles (l'archive porte le jugement avec les pièces —
modèle m6d/Entrée 149), les DEUX index mis à jour, preuves-m7/ DEMEURE à la
racine avec son LISEZMOI (le réceptacle, prêt à un éventuel nouveau run).

La vague m7d (kit-m7d.zip + LISEZMOI-m7d.txt) DEMEURE la vague courante à la
racine de /test : le programme M6/M7 est accompli, aucun kit M8 n'est
annoncé — rien ne se jette (D143).

  1. les TROIS pièces du run → archives-preuves/preuves-run-m7d/
     (temoin-m7d.txt, scenario-m7d-journal.log, VERDICT-run-m7d.txt —
     déplacement, md5 constaté APRÈS le geste) ;
  2. VERDICT-recoup-labo-m7d.txt déposé (le jugement du labo — Entrée 155 :
     RECOUP VERT 29/29 sur pièces croisées, la finale 0.8.0 SCELLÉE, D159) ;
  3. LISEZMOI-archives-preuves.txt : la section preuves-run-m7d ;
  4. LISEZMOI-archives-livraisons.txt : la vague m7d DEMEURE courante
     (programme accompli, aucune vague suivante annoncée) ;
  5. préuves-m7/ ne porte plus que son LISEZMOI ; la racine inchangée par
     ailleurs ; les empreintes recoupées.

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/cloturer_run_m7d.py
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
    "/home/z/my-project/download/preuves-run-m7d/VERDICT-recoup-m7d.txt")

PIECES_RUN_M7D = ["temoin-m7d.txt", "scenario-m7d-journal.log",
                  "VERDICT-run-m7d.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m7d/ (clôturées le 05/11 au geste final — le run M7-(d) VERT sur
pièces, le recoup labo 29/29, la finale 0.8.0 scellée, le jalon M7 franchi) :
  - temoin-m7d.txt, scenario-m7d-journal.log, VERDICT-run-m7d.txt — les
    pièces DU RUN (la machine du développeur, WSL2 — un autre noyau que
    celui du laboratoire, l'instrument EMBARQUÉ du kit qemu-riscv64 statique
    md5 bae5a36f…, la réserve instrumentale D149 nommée) ;
  - VERDICT-recoup-labo-m7d.txt — le verdict du RECOUP laboratoire (Entrée
    155 : RECOUP VERT 29/29 sur pièces croisées — le juge est le code,
    l'attendu re-généré au geste même ; LA FINALE 0.8.0 SCELLÉE, l'artefact
    intact sha ec343b4e…, le jalon M7 franchi, D159) — l'archive porte le
    jugement AVEC les pièces.
  preuves-m7/ demeure à la racine avec son LISEZMOI (le réceptacle, prêt à
    un éventuel nouveau run).
"""

INDEX_LIVRAISONS_ADDENDUM = """

--- note du 05/11/2026 (le geste final M7-(d)) : la vague m7d DEMEURE la
    vague courante — le run terrain est VENU (16/16 PASS, le recoup labo
    29/29 sur pièces croisées, la finale 0.8.0 SCELLÉE — le jalon M7
    franchi, le programme M6/M7 accompli) ; aucun kit M8 n'est annoncé,
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
    print(f"[clôture] {nom} -> preuves-run-m7d/ (md5 {md5_attendu[:8]}… constaté "
          f"après le geste — D143 : un déplacement, jamais un jet)")


def maj_index_texte(file_id, marqueur, section, nom_log):
    _, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    texte = body.decode("utf-8")
    if marqueur in texte:
        print(f"[index] {nom_log} déjà à jour — constaté")
        return
    if marqueur == "preuves-run-m7d":
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
    print("=== M7-(d) : LA CLÔTURE D143 DU RUN m7d — les pièces à l'archive "
          "AVEC le verdict du recoup ===")

    if not VERDICT_RECOUP_LOCAL.exists():
        raise Refus("VERDICT-recoup-m7d.txt local introuvable — le recoup "
                    "d'abord (scripts/recouper_run_m7d.py)")

    racine = ds.list_folder(TEST_ID)
    arch_p = racine.get("archives-preuves")
    arch_l = racine.get("archives-livraisons")
    if not (arch_p or {}).get("id") or not (arch_l or {}).get("id"):
        raise Refus("les salles d'archive sont introuvables au coffre /test")

    # (1) les TROIS pièces du run -> preuves-run-m7d/ -------------------------
    pm7 = racine.get("preuves-m7") or {}
    if not pm7.get("id"):
        raise Refus("preuves-m7/ introuvable au coffre — la clôture refuse")
    run_m7d = ds.list_folder(arch_p["id"]).get("preuves-run-m7d")
    if not run_m7d:
        run_id = ds.create_folder(arch_p["id"], "preuves-run-m7d")
        print(f"[clôture] preuves-run-m7d/ créé dans archives-preuves/ ({run_id})")
    else:
        run_id = run_m7d["id"]
        print("[clôture] preuves-run-m7d/ déjà présent — constaté")
    for nom in PIECES_RUN_M7D:
        entree = ds.list_folder(pm7["id"]).get(nom)
        if not entree:
            deja = ds.list_folder(run_id).get(nom)
            if deja:
                print(f"[clôture] {nom} déjà archivé "
                      f"(md5 {deja.get('md5Checksum', '-')[:8]}…) — constaté")
                continue
            raise Refus(f"'{nom}' ni dans preuves-m7/ ni dans l'archive — "
                        "introuvable")
        deplacer_vers(entree["id"], nom, pm7["id"], run_id,
                      entree.get("md5Checksum"))

    # (2) le VERDICT-DU-RECOUP du labo déposé AVEC les pièces ----------------
    if "VERDICT-recoup-labo-m7d.txt" not in ds.list_folder(run_id):
        ds.upload_create(run_id, "VERDICT-recoup-labo-m7d.txt",
                         VERDICT_RECOUP_LOCAL)
        print("[clôture] VERDICT-recoup-labo-m7d.txt déposé (le jugement AVEC "
              "les pièces — Entrée 155 : RECOUP VERT 29/29, la finale 0.8.0 "
              "scellée)")
    else:
        print("[clôture] VERDICT-recoup-labo-m7d.txt déjà là — constaté")

    # (3) preuves-m7/ ne porte plus que son LISEZMOI ---------------------------
    restants = ds.list_folder(pm7["id"])
    if set(restants) != {"LISEZMOI-preuves.txt"}:
        raise Refus(f"preuves-m7/ ne porte pas seulement son LISEZMOI après "
                    f"la clôture : {sorted(restants)}")

    # (4) LES DEUX INDEX mis à jour --------------------------------------------
    idxp = ds.list_folder(arch_p["id"]).get("LISEZMOI-archives-preuves.txt")
    if not idxp:
        raise Refus("LISEZMOI-archives-preuves.txt introuvable")
    maj_index_texte(idxp["id"], "preuves-run-m7d", INDEX_PREUVES_SECTION,
                    "LISEZMOI-archives-preuves.txt (la section preuves-run-m7d)")

    idxl = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if not idxl:
        raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
    maj_index_texte(idxl["id"], "la vague m7d DEMEURE la vague courante",
                    INDEX_LIVRAISONS_ADDENDUM,
                    "LISEZMOI-archives-livraisons.txt (la vague m7d demeure)")

    # (5) LA VÉRIFICATION FINALE -------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    attendus = {"kit-m7d.zip", "LISEZMOI-m7d.txt", "corriger-wsb.bat",
                "corriger-wsb.ps1", "preuves-m5b", "preuves-m6", "preuves-m7",
                "archives-livraisons", "archives-preuves"}
    manquants = attendus - set(racine)
    if manquants:
        raise Refus(f"la racine de /test ne porte pas {sorted(manquants)}")
    if racine["kit-m7d.zip"].get("md5Checksum") != "4d17f3fada9b54ccb21e232e0a0a1ca5":
        raise Refus("le kit de la racine a divergé — refus")
    dans_run = ds.list_folder(run_id)
    attendues_run = set(PIECES_RUN_M7D) | {"VERDICT-recoup-labo-m7d.txt"}
    if attendues_run - set(dans_run):
        raise Refus(f"preuves-run-m7d/ incomplet : "
                    f"{sorted(attendues_run - set(dans_run))}")
    print(f"[vérif] la clôture D143 du run m7d CONSTATÉE dans "
          f"preuves-run-m7d/ ({len(attendues_run)} pièces : le run + le "
          f"verdict du recoup — l'archive porte le jugement avec les pièces)")
    print(f"[vérif] preuves-m7/ ne porte plus que son LISEZMOI "
          f"(le réceptacle demeure)")
    print("[vérif] la vague m7d DEMEURE la vague courante à la racine "
          "(kit-m7d.zip md5 4d17f3fa… recoupé — aucun kit M8 annoncé, rien "
          "ne se jette)")
    print("=== la clôture D143 du run m7d est FAITE — le jalon M7 franchi, "
          "l'archive porte le jugement avec les pièces ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Refus, ds.SyncError) as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(2)
