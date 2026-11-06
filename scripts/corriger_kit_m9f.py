#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corriger_kit_m9f.py — LA CORRECTION DU KIT TERRAIN M9-(f) APRÈS LE PREMIER
RUN du développeur (le 06/11 16:17, Windows 10.0 build 19045, Python 3.14.6) :
verdict ROUGE honnête nommé « T1.la-résolution » — « le miroir Python refuse
“NtCreateFile” : répertoire export absent ». LA FAUTE ÉTAIT AU KIT (l'erratum
n° 6, nommé par le recoup labo 25/25 sur pièces croisées) : T1 passait la
base de L'ARTEFACT (`base` = proxy.exe, SANS répertoire export) aux lecteurs
de SSN, au lieu de la base du VRAI ntdll (`ntdll_base`) — le refus -3 était
INÉVITABLE sur toute machine. Le terrain est LAVÉ (le VRAI ntdll localisé et
haché, l'artefact relu INTACT, le scénario exécuté fidèlement).

La correction À LA SOURCE (tls13/terrain/scenario-m9f.py : les TROIS sites
de résolution reçoivent `ntdll_base`) + LE CONTRÔLE PERMANENT à l'assemblage
(assembler_kit_m9f.py [2b] : l'AST exige `ntdll_base` aux trois lecteurs —
contrôle négatif PROUVÉ sur la source pré-réparation : 3 sites, 0 à
ntll_base → REFUS) ; le kit CORRIGÉ réassemblé et rééprouvé (26 constantes
PAR AST == l'artefact/le plan/la sonde, py_compile, extraction vierge VERT).

Le geste au coffre /test (modèle corriger_kit_m8d.py + cloturer_run_m8d.py,
D143 : archivage par DÉPLACEMENT, jamais un jet) :
  1. le zip local CORRIGÉ vérifié (empreintes attendues ci-dessous) ;
  2. kit-m9f.zip du coffre MIS À JOUR EN PLACE (upload_update : le contenu
     remplacé, le fichier même conservé — aucune entrée nouvelle, rien
     jeté ; l'ancien scénario vit dans l'histoire git, à la pointe
     pré-réparation 20ab30f) ;
  3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE (l'erratum n° 6 consigné au
     document du kit — l'honnêteté du terrain) ;
  4. le PREMIER RUN archivé : les TROIS pièces (temoin, journal, verdict)
     DÉPLACÉES vers archives-preuves/preuves-run-m9f/ ; le
     VERDICT-recoup-labo-m9f.txt déposé AVEC elles (l'archive porte le
     jugement avec les pièces — modèle m8d/Entrée 155) ;
  5. preuves-m9f/ ré-armé : il ne porte plus que son LISEZMOI-preuves.txt
     (le réceptacle, prêt au SECOND geste du développeur) ;
  6. LES DEUX INDEX mis à jour (archives-preuves : la section
     preuves-run-m9f ; archives-livraisons : la note de correction) ;
  7. la vérification finale (la racine en ordre, les empreintes recoupées).

Usage : python3 scripts/corriger_kit_m9f.py
Code de sortie : 0 = coffre corrigé et recoupé ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-m9f.zip"
LISEZMOI_KIT = os.path.join(REPO, "tls13", "terrain", "LISEZMOI-KIT-M9F.md")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f/VERDICT-recoup-labo-m9f.txt")

# le kit CORRIGÉ (assembler_kit_m9f.py rejoué le 06/11 au soir après la
# réparation de l'erratum n° 6)
KIT_SHA = ("85c75fc11ef8f1c4ff6527fb1515410970321fc28c0ca6155d926f6b"
           "198a0c83")
KIT_MD5 = "7d5380ceb19420f62cd4481f14431284"

# le kit défectueux d'origine (a73fb526) — le témoin de ce qu'on remplace
ANCIEN_MD5 = "a73fb526222fae848aed877b5433deef"

PIECES_RUN = ["temoin-m9f.txt", "scenario-m9f-journal.log",
              "VERDICT-run-m9f.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f/ (archivées le 06/11 au soir — LE PREMIER run M9-(f), ROUGE
T1.la-résolution NOMMÉ : l'erratum n° 6 du kit [la base de l'ARTEFACT passée
aux lecteurs de SSN au lieu de la base ntdll — proxy.exe sans répertoire
export, le refus -3 « répertoire export absent » INÉVITABLE sur toute
machine], la faute AU LABO, jamais au terrain — le kit corrigé ré-déposé,
le second run attendu) :
  - temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt — les
    pièces DU RUN (Windows 10.0 build 19045, Python 3.14.6 AMD64 — le
    VRAI ntdll localisé et haché 36b1a62e…, l'artefact relu INTACT
    d8928934…, l'octet de l'erratum n° 5 relu dans l'image, les SEIZE
    T0 tranchés [ok], la mort à T1 : deux lignes de journal) ;
  - VERDICT-recoup-labo-m9f.txt — le verdict du RECOUP laboratoire (ROUGE
    CONSTATÉ COHÉRENT 25/25 sur pièces croisées, D138/D145/D148 : la cause
    nommée sur pièces [E2 : le répertoire export de proxy.exe recalculé
    nul AU geste même], la finale 1.0.0 REFUSÉE pour CE run, le kit réparé
    à la source + le contrôle PERMANENT à l'assemblage) — l'archive porte
    le jugement AVEC les pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle,
  ré-armé pour le second geste du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 06/11/2026 au soir (la correction du kit m9f, l'erratum n° 6) :
    le premier run a rendu ROUGE T1.la-résolution — LA FAUTE AU KIT (la
    base de l'artefact passée aux lecteurs de SSN au lieu de la base
    ntdll), nommée par le recoup labo 25/25 sur pièces croisées ;
    kit-m9f.zip MIS À JOUR EN PLACE (md5 7d5380ce… — le contenu remplacé,
    le fichier même conservé, l'ancien scénario vit dans l'histoire git à
    la pointe pré-réparation 20ab30f) ; le LISEZMOI porte l'erratum ; le
    contrôle PERMANENT vit à l'assemblage (l'AST exige ntdll_base aux
    trois lecteurs) ; la finale 1.0.0 attend le second run VERT sur
    pièces.
"""


class Refus(Exception):
    """Tout refus nommé du passeur (fail-closed)."""


def md5f(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


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
    print(f"[archivage] {nom} -> preuves-run-m9f/ (md5 "
          f"{md5_attendu[:8]}… constaté après — D143 : un déplacement, "
          f"jamais un jet)")


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
    print("=== M9-(f) : LA CORRECTION DU KIT au coffre /test (l'erratum "
          "n° 6 — T1 : ntdll_base aux lecteurs de SSN) ===")
    try:
        # -- 1. le zip local corrigé, vérifié ---------------------------------
        if not os.path.isfile(KIT_ZIP):
            raise Refus(f"KIT : {KIT_ZIP} absent — assembler_kit_m9f.py "
                        "d'abord")
        if sha256f(KIT_ZIP) != KIT_SHA:
            raise Refus(f"KIT : kit-m9f.zip sha256 divergent "
                        f"({sha256f(KIT_ZIP)[:16]}…) — réassembler le kit "
                        f"corrigé")
        if md5f(KIT_ZIP) != KIT_MD5:
            raise Refus("KIT : kit-m9f.zip md5 divergent — réassembler")
        print(f"[1] le kit corrigé : {os.path.getsize(KIT_ZIP)} o, md5 "
              f"{KIT_MD5[:8]}…, sha256 {KIT_SHA[:16]}… (26 constantes PAR "
              f"AST + LE CONTRÔLE PERMANENT erratum n° 6 + extraction "
              f"vierge — VERT)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        arch_l = racine.get("archives-livraisons")
        if not (arch_p or {}).get("id") or not (arch_l or {}).get("id"):
            raise Refus("les salles d'archive sont introuvables au coffre "
                        "/test")

        # -- 2. kit-m9f.zip MIS À JOUR EN PLACE --------------------------------
        piece = racine.get("kit-m9f.zip")
        if not piece:
            raise Refus("kit-m9f.zip introuvable à la racine du /test — "
                        "deposer_kit_m9f.py d'abord")
        md5_distant = piece.get("md5Checksum", "")
        if md5_distant == KIT_MD5:
            print("[2] kit-m9f.zip porte DÉJÀ le md5 corrigé — idempotent")
        else:
            if md5_distant != ANCIEN_MD5:
                raise Refus(f"kit-m9f.zip distant d'un md5 INATTENDU "
                            f"({md5_distant[:8]}…) — ni l'original "
                            f"{ANCIEN_MD5[:8]}… ni le corrigé "
                            f"{KIT_MD5[:8]}… : constater avant geste")
            ds.upload_update(piece["id"], pathlib.Path(KIT_ZIP))
            apres = ds.list_folder(TEST_ID).get("kit-m9f.zip")
            if not apres or apres.get("md5Checksum") != KIT_MD5:
                raise Refus("kit-m9f.zip md5 divergent après mise à jour "
                            f"({(apres or {}).get('md5Checksum', 'ABSENT')[:8]}…)")
            print(f"[2] kit-m9f.zip MIS À JOUR au coffre — md5 "
                  f"{KIT_MD5[:8]}… MATCH par relecture (le contenu "
                  f"remplacé, le fichier même conservé, rien jeté)")

        # -- 3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE ---------------------------
        lis = racine.get("LISEZMOI-m9f.txt")
        if not lis:
            raise Refus("LISEZMOI-m9f.txt introuvable à la racine du /test")
        md5_lis_local = md5f(LISEZMOI_KIT)
        if lis.get("md5Checksum") == md5_lis_local:
            print("[3] LISEZMOI-m9f.txt porte déjà l'erratum — idempotent")
        else:
            ds.upload_update(lis["id"], pathlib.Path(LISEZMOI_KIT))
            apres = ds.list_folder(TEST_ID).get("LISEZMOI-m9f.txt")
            if not apres or apres.get("md5Checksum") != md5_lis_local:
                raise Refus("LISEZMOI-m9f.txt md5 divergent après mise à "
                            "jour")
            print(f"[3] LISEZMOI-m9f.txt MIS À JOUR (md5 "
                  f"{md5_lis_local[:8]}… MATCH — l'erratum n° 6 consigné au "
                  f"document du kit)")

        # -- 4. le PREMIER RUN archivé (les pièces + le verdict du recoup) -----
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f.txt local introuvable — "
                        "le recoup d'abord "
                        "(scripts/recouper_preuves_m9f.py)")
        pm9 = racine.get("preuves-m9f") or {}
        if not pm9.get("id"):
            raise Refus("preuves-m9f/ introuvable au coffre")
        run_m9f = ds.list_folder(arch_p["id"]).get("preuves-run-m9f")
        if not run_m9f:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f")
            print("[4] preuves-run-m9f/ créé dans archives-preuves/")
        else:
            run_id = run_m9f["id"]
            print("[4] preuves-run-m9f/ déjà présent — constaté")
        for nom in PIECES_RUN:
            entree = ds.list_folder(pm9["id"]).get(nom)
            if not entree:
                deja = ds.list_folder(run_id).get(nom)
                if deja:
                    print(f"[4] {nom} déjà archivé (md5 "
                          f"{deja.get('md5Checksum', '-')[:8]}…) — constaté")
                    continue
                raise Refus(f"'{nom}' ni dans preuves-m9f/ ni dans "
                            "l'archive — introuvable")
            deplacer_vers(entree["id"], nom, pm9["id"], run_id,
                          entree.get("md5Checksum"))
        if "VERDICT-recoup-labo-m9f.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f.txt déposé (le jugement "
                  "AVEC les pièces — ROUGE CONSTATÉ COHÉRENT 25/25, la "
                  "cause AU LABO, le kit réparé)")
        else:
            print("[4] VERDICT-recoup-labo-m9f.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé ----------------------------------------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle du SECOND run)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f)", avant_fin=True)
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "la correction du kit m9f, l'erratum n° 6",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note de "
                        "correction)")

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
            raise Refus("le kit de la racine a divergé — refus")
        dans_run = ds.list_folder(run_id)
        attendues_run = set(PIECES_RUN) | {"VERDICT-recoup-labo-m9f.txt"}
        if attendues_run - set(dans_run):
            raise Refus(f"preuves-run-m9f/ incomplet : "
                        f"{sorted(attendues_run - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit corrigé md5 {KIT_MD5[:8]}… recoupé) ; "
              f"preuves-run-m9f/ porte les {len(attendues_run)} pièces "
              f"(le run + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[correction] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE COFFRE /test PORTE LE KIT CORRIGÉ (l'erratum n° 6 "
          "réparé à la source, le contrôle PERMANENT à l'assemblage) : "
          "le SECOND geste du développeur est attendu — dézipper "
          "kit-m9f.zip, python scenario-m9f.py (~10 s, réseau vivant), "
          "renvoyer preuves-m9f/ ENTIER au coffre — la finale 1.0.0 "
          "attend le vert ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
