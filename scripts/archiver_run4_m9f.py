#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run4_m9f.py — LE QUATRIÈME RUN M9-(f) ARCHIVÉ au coffre /test
(le run du 2026-11-06 19:20:57, reçu et recoupé — ROUGE T3.ouvrir NOMMÉ :
sys-05 rend -6 à son premier appel réel SUR WINDOWS 11 AUSSI : LA
RÉPÉTITION À L'IDENTIQUE, le suspect (a) ÉLIMINÉ sur pièces — le recoup
30/30, la sonde sys-05 s'ouvre).

Le kit est ACQUITTÉ (le MÊME binaire, le MÊME scénario — seule la machine
a changé : le kit du /test demeure 90a1d022…) : AUCUN dépôt de kit,
AUCUN retrait — le geste est L'ARCHIVAGE SEUL (modèle archiver_run3,
D143 : par DÉPLACEMENT, jamais un jet) :
  1. les pièces locales vérifiées (le trio md5-contrôlé par le recoup +
     le verdict du recoup 30/30) ;
  2. preuves-run-m9f-4/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. le trio DU RUN DÉPLACÉ du réceptacle vers l'archive ;
  4. le VERDICT-recoup-labo-m9f-4.txt déposé AVEC les pièces (l'archive
     porte le jugement) ;
  5. preuves-m9f/ ré-armé (son LISEZMOI seul — le réceptacle du prochain
     run) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, le kit INCHANGÉ, les
     empreintes recoupées).

Usage : python3 scripts/archiver_run4_m9f.py
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

TRIO_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-4")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-4/"
    "VERDICT-recoup-labo-m9f-4.txt")

TRIO = {"temoin-m9f.txt": "79c83775",
        "scenario-m9f-journal.log": "2b819ae4",
        "VERDICT-run-m9f.txt": "c95fb66e"}

KIT_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"   # le kit ACQUITTÉ, INCHANGÉ

PIECES_RUN4 = sorted(TRIO) + ["VERDICT-recoup-labo-m9f-4.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f-4/ (archivées le 06/11 au soir, troisième geste — LE
QUATRIÈME run M9-(f) : LE GESTE (ii) DU RECOUP-3 ACCOMPLI, la machine
CHANGÉE pour Windows 11 build 26300 [Python 3.14.3, ntdll b072efae… —
le run 3 avait lieu sur Windows 10 build 19045], l'artefact INTACT
[d8928934… — LE MÊME], le kit ACQUITTÉ INCHANGÉ [90a1d022…] ; ROUGE
T3.ouvrir NOMMÉ À L'IDENTIQUE : sys-05 rend -6 à SON PREMIER APPEL RÉEL
sur Windows 11 AUSSI → LA RÉPÉTITION CONSTATÉE PAR CODE [le journal du
run 4 == le journal du run 3, LIGNE À LIGNE, horodatements exceptés] →
LE SUSPECT (a) [la divergence afd.sys Win10 ↔ Win11] ÉLIMINÉ sur
pièces : le refus est INTER-GÉNÉRATIONS, STRUCTUREL au contrat d'appel
de sys-05 ou à l'état de l'endpoint — la finale 1.0.0 REFUSÉEE pour CE
run, fail-closed] ; T0/T1/T2 VERT partout, le recoup du jalon VERT [le
CH == la construction re-jouée, 119 o] et l'erratum n° 7 réparé [la clé
f650affb… NON-NULLE] :
  - temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt — les
    pièces DU RUN (Windows 10.0 build 26300, Python 3.14.3 AMD64, le
    run entier dans SA seconde 19:20:57 : T0/T1/T2 VERT, T3 l'offre
    composée PARFAITE, l'émission refusée À L'IDENTIQUE, la mort nommée) ;
  - VERDICT-recoup-labo-m9f-4.txt — le verdict du RECOUP laboratoire
    (ROUGE CONSTATÉ COHÉRENT 30/30 sur pièces croisées, D138/D145/D148 :
    l'échelle REJOUÉE sur la clé privée DU RUN rend la clé du témoin, la
    construction CH re-jouée [114 o, le vol 119 o], la chaîne -6 → -7
    reconstituée depuis les contrats, LA RÉPÉTITION À L'IDENTIQUE PAR
    CODE [F1], LE SUSPECT (a) ÉLIMINÉ [F3], LA CONNEXION ÉTABLIE aux
    deux runs [F4 — seul le SEND est refusé partout], les candidats
    re-évalués [le contrat d'appel de sys-05 ; l'état de l'endpoint ;
    le passager réseau INVRAISEMBLABLE] — LE NTSTATUS BRUT qui vit dans
    rdx DÉPARTAGE : LA SONDE sys-05 S'OUVRE) — l'archive porte le
    jugement AVEC les pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle,
  ré-armé pour le prochain run du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 06/11/2026 au soir, troisième geste (le QUATRIÈME run M9-(f)
    reçu et recoupé — le geste (ii) du recoup-3 : la machine Windows 11
    ENFIN essayée) : le MÊME kit 90a1d022… exécuté sur Windows 11 build
    26300 (le run : 2026-11-06 19:20:57, l'heure de la machine du
    développeur) ; T0/T1/T2 VERT (les SEIZE T0, SSN 85/7/15, handle
    0x280 — le socle PASSE sur Win11 aussi), le recoup du jalon VERT
    (le CH == la construction re-jouée, 119 o), l'erratum n° 7 réparé
    (la clé f650affb… NON-NULLE) ; LA MORT NOMMÉE À L'IDENTIQUE : sys-05
    (L'ÉMISSION) rend -6 à SON PREMIER APPEL RÉEL sur Windows 11 AUSSI —
    LE JOURNAL DU RUN 4 EST IDENTIQUE À CELUI DU RUN 3, LIGNE À LIGNE,
    les horodatements exceptés (constaté par code sur les pièces
    croisées) → LE SUSPECT (a) [la divergence afd.sys Win10 ↔ Win11] EST
    ÉLIMINÉ : le refus est INTER-GÉNÉRATIONS — STRUCTUREL au contrat
    d'appel de sys-05 ou à l'état de l'endpoint ; le kit ACQUITTÉ
    INCHANGÉ (le MÊME binaire, le MÊME scénario, l'offre PARFAITE sur
    pièces, UNE SEULE émission tentée) ; le run archivé →
    archives-preuves/preuves-run-m9f-4/ AVEC le verdict du recoup
    (30/30) ; LA SONDE sys-05 EST LE GESTE SUIVANT (le chantier promis
    par le recoup-3 : lire le NTSTATUS brut qui vit dans rdx — la
    limite NOMMÉE de l'instrument, franchie par un trampoline de
    capture SANS reconstruire l'artefact) ; kit-sonde-sys05.zip livré à
    la racine du /test.
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
    print(f"[archivage] {nom} -> preuves-run-m9f-4/ (md5 "
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
    print("=== M9-(f) : LE QUATRIÈME RUN ARCHIVÉ au coffre /test (le kit "
          "ACQUITTÉ demeure — le geste est l'archive seule) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in TRIO.items():
            chemin = TRIO_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — "
                            "ramasse_run4_m9f.py d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f-4.txt local introuvable — "
                        "le recoup d'abord (scripts/recouper_run4_m9f.py)")
        print(f"[1] les pièces locales vérifiées (le trio md5-contrôlé + "
              f"le verdict du recoup {md5f(VERDICT_RECOUP_LOCAL)[:8]}…, "
              "30/30)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-run-m9f-4/ créé ------------------------------------------
        run_m9f4 = ds.list_folder(arch_p["id"]).get("preuves-run-m9f-4")
        if not run_m9f4:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f-4")
            print("[2] preuves-run-m9f-4/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_m9f4["id"]
            print("[2] preuves-run-m9f-4/ déjà présent — constaté")

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
        if "VERDICT-recoup-labo-m9f-4.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f-4.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f-4.txt déposé (le jugement "
                  "AVEC les pièces — ROUGE CONSTATÉ COHÉRENT 30/30, LE "
                  "SUSPECT (a) ÉLIMINÉ, la sonde s'ouvre)")
        else:
            print("[4] VERDICT-recoup-labo-m9f-4.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé ----------------------------------------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle du prochain run)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f-4",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f-4)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "le QUATRIÈME run M9-(f) reçu et recoupé",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du "
                        "quatrième run)")

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
        if set(PIECES_RUN4) - set(dans_run):
            raise Refus(f"preuves-run-m9f-4/ incomplet : "
                        f"{sorted(set(PIECES_RUN4) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit ACQUITTÉ md5 {KIT_MD5[:8]}… INCHANGÉ — recoupé) ; "
              f"preuves-run-m9f-4/ porte les {len(PIECES_RUN4)} pièces "
              "(le trio DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE QUATRIÈME RUN EST ARCHIVÉ avec son jugement : LA "
          "RÉPÉTITION À L'IDENTIQUE SUR WINDOWS 11 — LE SUSPECT (a) "
          "ÉLIMINÉ SUR PIÈCES ; LA SONDE sys-05 EST LE GESTE SUIVANT "
          "(le chantier promis : lire le NTSTATUS brut qui vit dans rdx) "
          "===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
