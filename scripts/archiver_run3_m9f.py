#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run3_m9f.py — LE TROISIÈME RUN M9-(f) ARCHIVÉ au coffre /test
(le run du 2026-11-06 18:49:34, reçu et recoupé — ROUGE T3.ouvrir NOMMÉ :
sys-05 rend -6 à son premier appel réel, MAIS le recoup du jalon VERT :
le ClientHello de LA MACHINE == la référence octet pour octet, 119 o).

Le kit est ACQUITTÉ (le scénario exécuté fidèlement — rien ne le condamne,
le kit du /test demeure 90a1d022…) : AUCUN dépôt de kit, AUCUN retrait —
le geste est L'ARCHIVAGE SEUL (modèle corriger_kit_m9f.py, D143 : par
DÉPLACEMENT, jamais un jet) :
  1. les pièces locales vérifiées (le trio md5-contrôlé par le recoup +
     le verdict du recoup 26/26) ;
  2. preuves-run-m9f-3/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. le trio DU RUN DÉPLACÉ du réceptacle vers l'archive ;
  4. le VERDICT-recoup-labo-m9f-3.txt déposé AVEC les pièces (l'archive
     porte le jugement) ;
  5. preuves-m9f/ ré-armé (son LISEZMOI seul — le réceptacle de la
     RELANCE) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, le kit INCHANGÉ, les
     empreintes recoupées).

Usage : python3 scripts/archiver_run3_m9f.py
Code de sortie : 0 = coffre archivé et recoupé ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

TRIO_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-run-m9f")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-3/"
    "VERDICT-recoup-labo-m9f-3.txt")

TRIO = {"temoin-m9f.txt": "f8491dc2",
        "scenario-m9f-journal.log": "03e555c8",
        "VERDICT-run-m9f.txt": "b9d79a0c"}

KIT_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"   # le kit ACQUITTÉ, INCHANGÉ

PIECES_RUN3 = sorted(TRIO) + ["VERDICT-recoup-labo-m9f-3.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f-3/ (archivées le 06/11 au soir — LE TROISIÈME run M9-(f),
ROUGE T3.ouvrir NOMMÉ : sys-05 rend -6 à SON PREMIER APPEL RÉEL —
l'émission du CH refusée par le transport [un NTSTATUS non nul,
l'information vit dans rdx : la limite NOMMÉE de l'instrument] → la
machine propage -7 LE TRANSPORT EN ÉCHEC, l'état 5 ; MAIS LE RECOUP DU
JALON EST VERT : le ClientHello COMPOSÉ PAR LA MACHINE == la construction
re-jouée OCTET POUR OCTET [119 o — la preuve cryptographique du jalon
sur la machine réelle, les DEUX lecteurs d'accord : tls13-14 ==
l'échelle Python] ET LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE SUR LA
MACHINE RÉELLE [la clé publique attendue NON-NULLE 89d50a86… — le run 2
imprimait 000…0] ; le kit ACQUITTÉ, la frontière nommée d'avance [le
socle socket court POUR LA PREMIÈRE FOIS sur le VRAI afd.sys — le
LISEZMOI au mot près]) :
  - temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt — les
    pièces DU RUN (Windows 10.0 build 19045, Python 3.14.6 AMD64, le run
    entier dans SA seconde 18:49:34 : T0/T1/T2 VERT, T3 l'offre composée
    PARFAITE, l'émission refusée, la mort nommée) ;
  - VERDICT-recoup-labo-m9f-3.txt — le verdict du RECOUP laboratoire
    (ROUGE CONSTATÉ COHÉRENT 26/26 sur pièces croisées, D138/D145/D148 :
    l'échelle REJOUÉE sur la clé privée DU RUN rend la clé du témoin, la
    construction CH re-jouée [114 o, le vol 119 o], la chaîne -6 → -7
    reconstituée depuis les contrats, LA PREUVE EN UNE LIGNE [UNE SEULE
    émission tentée : celle du CH — l'append du rappel précède l'envoi],
    la finale 1.0.0 REFUSÉE pour CE run, le kit ACQUITTÉ, les candidats
    nommés [la divergence afd.sys Win10 ↔ Win11 ; la connexion refermée
    côté serveur ; le passager réseau]) — l'archive porte le jugement
    AVEC les pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle,
  ré-armé pour la RELANCE du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 06/11/2026 au soir, deuxième geste (le TROISIÈME run M9-(f)
    reçu et recoupé — la suite immédiate de la correction de l'erratum
    n° 7) : le kit corrigé 90a1d022… exécuté SIX MINUTES après son dépôt
    (le run : 2026-11-06 18:49:34, l'heure de la machine du développeur) ;
    T0/T1/T2 VERT, LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE (la clé
    publique attendue NON-NULLE 89d50a86… — le run 2 imprimait 000…0),
    LE RECOUP DU JALON VERT (le ClientHello de LA MACHINE == la
    construction de référence, 119 o, octet pour octet — la preuve
    cryptographique du jalon sur la machine réelle : les blocs scellés
    composent une offre PARFAITE) ; la mort NOMMÉE : sys-05 (L'ÉMISSION)
    rend -6 à SON PREMIER APPEL RÉEL → la machine propage -7 LE
    TRANSPORT EN ÉCHEC, l'état 5 ; le NTSTATUS vit dans rdx (la limite
    nommée de l'instrument) ; le kit ACQUITTÉ (le scénario exécuté
    fidèlement — le kit du /test INCHANGÉ 90a1d022…), la frontière nommée
    d'avance (l'artefact contre le VRAI afd.sys, le LISEZMOI au mot
    près) ; le run archivé → archives-preuves/preuves-run-m9f-3/ AVEC le
    verdict du recoup (26/26) ; LA RELANCE du développeur est le geste
    suivant — un réseau vivant distingue le passager du structurel ; si
    le -6 se répète À L'IDENTIQUE à l'émission du CH : la divergence
    afd.sys Windows 10 ↔ Windows 11 devient le suspect principal (une
    machine Windows 11, ou la sonde sys-05 au labo).
"""


class Refus(Exception):
    """Tout refus nommé du passeur (fail-closed)."""


def md5f(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def deplacer_vers(file_id, nom, parent_de, parent_vers, md5_attendu):
    url = (f"{ds.API}/files/{file_id}?"
           + "addParents=" + parent_vers
           + "&removeParents=" + parent_de)
    st, body, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        raise Refus(f"déplacement de '{nom}' impossible (HTTP {st}) : "
                    f"{body[:200]!r}")
    apres = ds.list_folder(parent_vers).get(nom)
    if not apres:
        raise Refus(f"'{nom}' absent de la salle d'archive après le geste")
    if apres.get("md5Checksum") != md5_attendu:
        raise Refus(f"'{nom}' archivé : md5 divergent après le geste")
    if nom in ds.list_folder(parent_de):
        raise Refus(f"'{nom}' demeure à son ancienne place après le geste")
    print(f"[archivage] {nom} -> preuves-run-m9f-3/ (md5 "
          f"{md5_attendu[:8]}… constaté après — D143 : un déplacement, "
          "jamais un jet)")


def maj_index_texte(file_id, marqueur, section, nom_log, avant_fin=False):
    _, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    texte = body.decode("utf-8")
    if marqueur in texte:
        print(f"[index] {nom_log} déjà à jour — constaté")
        return
    if avant_fin:
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
    print("=== M9-(f) : LE TROISIÈME RUN ARCHIVÉ au coffre /test (le kit "
          "ACQUITTÉ demeure — le geste est l'archive seule) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in TRIO.items():
            chemin = TRIO_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — "
                            "rapatrier_preuves_m9f.py d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f-3.txt local introuvable — "
                        "le recoup d'abord (scripts/recouper_run3_m9f.py)")
        print(f"[1] les pièces locales vérifiées (le trio md5-contrôlé + "
              f"le verdict du recoup {md5f(VERDICT_RECOUP_LOCAL)[:8]}…, "
              "26/26)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-run-m9f-3/ créé ------------------------------------------
        run_m9f3 = ds.list_folder(arch_p["id"]).get("preuves-run-m9f-3")
        if not run_m9f3:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f-3")
            print("[2] preuves-run-m9f-3/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_m9f3["id"]
            print("[2] preuves-run-m9f-3/ déjà présent — constaté")

        # -- 3. le trio DU RUN, DÉPLACÉ depuis le réceptacle ---------------------
        pm9 = racine.get("preuves-m9f") or {}
        if not pm9.get("id"):
            raise Refus("preuves-m9f/ introuvable au coffre")
        for nom, prefixe in TRIO.items():
            entree = ds.list_folder(pm9["id"]).get(nom)
            if entree:
                if not entree.get("md5Checksum", "").startswith(prefixe):
                    raise Refus(f"la pièce distante {nom} d'un md5 "
                                "inattendu — constater avant geste")
                deplacer_vers(entree["id"], nom, pm9["id"], run_id,
                              entree["md5Checksum"])
            elif nom not in ds.list_folder(run_id):
                raise Refus(f"'{nom}' ni dans preuves-m9f/ ni dans "
                            "l'archive — introuvable")
            else:
                print(f"[3] {nom} déjà archivé — constaté")

        # -- 4. le verdict du recoup, déposé AVEC les pièces ---------------------
        if "VERDICT-recoup-labo-m9f-3.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f-3.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f-3.txt déposé (le jugement "
                  "AVEC les pièces — ROUGE CONSTATÉ COHÉRENT 26/26, le kit "
                  "ACQUITTÉ, les candidats nommés)")
        else:
            print("[4] VERDICT-recoup-labo-m9f-3.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé ----------------------------------------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle de la RELANCE)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f-3",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f-3)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "le TROISIÈME run M9-(f) reçu et recoupé",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du "
                        "troisième run)")

        # -- 7. la vérification finale ----------------------------------------------
        final = ds.list_folder(TEST_ID)
        attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                    "archives-livraisons", "archives-preuves",
                    "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                    "corriger-wsb.bat", "corriger-wsb.ps1",
                    "signatures-I.txt", "cle-publique-I.txt"}
        manquants = attendus - set(final)
        if manquants:
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("le kit de la racine a divergé — le kit ACQUITTÉ "
                        "doit demeurer 90a1d022…")
        dans_run = ds.list_folder(run_id)
        if set(PIECES_RUN3) - set(dans_run):
            raise Refus(f"preuves-run-m9f-3/ incomplet : "
                        f"{sorted(set(PIECES_RUN3) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit ACQUITTÉ md5 {KIT_MD5[:8]}… INCHANGÉ — recoupé) ; "
              f"preuves-run-m9f-3/ porte les {len(PIECES_RUN3)} pièces "
              "(le trio DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE TROISIÈME RUN EST ARCHIVÉ avec son jugement : LE PLUS "
          "LOIN DU PROGRAMME (l'offre de LA MACHINE PARFAITE sur pièces, "
          "l'émission refusée au premier appel réel de sys-05) — LA "
          "RELANC DU DÉVELOPPEUR EST LE GESTE SUIVANT : réseau vivant, "
          "python scenario-m9f.py, preuves-m9f/ ENTIER au coffre ; si le "
          "-6 se répète à l'identique : la divergence afd.sys Win10 ↔ "
          "Win11 devient le suspect principal ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
