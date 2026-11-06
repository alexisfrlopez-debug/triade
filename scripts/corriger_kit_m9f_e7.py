#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corriger_kit_m9f_e7.py — LA CORRECTION DU KIT TERRAIN M9-(f) APRÈS LE
SECOND RUN du développeur (le 06/11 16:56, mort d'un crash PYTHON nommé
sur la console : TypeError ligne 593 `kit96.raw[:32] = alea`) :
L'ERRATUM n° 7, TROIS fautes au kit dans le segment Python pur (la pose
du kit par tranches sur `.raw` — le crash ; l'échelle du recoup rendant
la « clé attendue » NULLE — x_3 né à 0, a24 = (p+1)//4 ; la TAILLE au
lieu du POINTEUR aux DEUX sites OUVRIR). L'acquittement « par
élimination » de l'Entrée 181 est RENVERSÉ par la pièce console — la
faute AU LABO, jamais au terrain (T0/T1/T2 VERT sur la machine réelle,
l'artefact relu INTACT au T0 du run mort lui-même).

La réparation À LA SOURCE (tls13/terrain/scenario-m9f.py : l'échelle ==
le pseudocode officiel RFC 7748 § 5, les 96 o posés EN UN GESTE,
r9 = ctypes.addressof(kit…) aux DEUX sites) + LE CONTRÔLE PERMANENT à
l'assemblage (assembler_kit_m9f.py [2c] : TROIS portes, preuve négative
sur la pointe 35706ef — les TROIS refus nommés) ; le kit CORRIGÉ
réassemblé et rééprouvé (26 constantes PAR AST, py_compile, extraction
vierge VERT, les portes [2b]/[2c] passées).

Le geste au coffre /test (modèle corriger_kit_m9f.py, D143 : archivage
par DÉPLACEMENT, jamais un jet) :
  1. le zip local CORRIGÉ vérifié (empreintes attendues ci-dessous) ;
  2. kit-m9f.zip du coffre MIS À JOUR EN PLACE (upload_update : le
     contenu remplacé, le fichier même conservé — l'ancien scénario
     vit dans l'histoire git, à la pointe pré-réparation 35706ef) ;
  3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE (l'erratum n° 7 consigné au
     document du kit) ;
  4. le SECOND RUN archivé : le journal DU RUN (le dépôt du
     développeur, md5 24680ac9…) DÉPLACÉ vers archives-preuves/
     preuves-run-m9f-2/ ; LA PIÈCE CONSOLE (le paste du 07/11 — celle
     qui RENVERSE l'acquittement) et le VERDICT-recoup-labo-m9f-2.txt
     déposés AVEC lui (l'archive porte le jugement avec les pièces) ;
  5. preuves-m9f/ ré-armé : il ne porte plus que son
     LISEZMOI-preuves.txt (le réceptacle, prêt au TROISIÈME geste) ;
  6. LES DEUX INDEX mis à jour (archives-preuves : la section
     preuves-run-m9f-2 ; archives-livraisons : la note de correction) ;
  7. la vérification finale (la racine en ordre, les empreintes
     recoupées).

Usage : python3 scripts/corriger_kit_m9f_e7.py
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
PIECE_CONSOLE = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-2/console-run-m9f.txt")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-2/"
    "VERDICT-recoup-labo-m9f-2.txt")

# le kit CORRIGÉ (assembler_kit_m9f.py rejoué le 07/11 après la
# réparation de l'erratum n° 7 — les portes [2b]/[2c] passées)
KIT_SHA = ("3666b1d7de520ba7d8a2057389b7a31f55d988e14ad5c361dd26031f"
           "158cf5c1")
KIT_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"

# le kit de l'erratum n° 6 (celui que le développeur a exécuté — le
# témoin de ce qu'on remplace) et son LISEZMOI
ANCIEN_MD5 = "7d5380ceb19420f62cd4481f14431284"
ANCIEN_LIS_MD5 = "b1b91887ffd3518bc85c15bb980f68fc"

JOURNAL_RUN2 = "scenario-m9f-journal.log"
JOURNAL_RUN2_MD5 = "24680ac98ee73ce3ae2fb7f90ec31f57"   # la pièce du run 2

PIECES_RUN2 = [JOURNAL_RUN2, "console-run-m9f.txt",
               "VERDICT-recoup-labo-m9f-2.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f-2/ (archivées le 07/11 — LE SECOND run M9-(f), CRASH
PYTHON nommé : l'erratum n° 7 du kit [TROIS fautes dans le segment
Python pur — la pose du kit par tranches sur `.raw` (le TypeError
ligne 593, LE crash du run), l'échelle du recoup rendant la « clé
attendue » NULLE (x_3 né à 0, a24 = (p+1)//4 : la fausse courbe), la
TAILLE au lieu du POINTEUR aux DEUX sites OUVRIR], la faute AU LABO,
l'acquittement « par élimination » de l'analyse du journal seul
RENVERSÉ par la pièce console ; T0/T1/T2 VERT sur la machine réelle —
l'erratum n° 6 prouvé réparé, LE VRAI afd.sys franchi pour la
première fois, le plus loin du programme sur le terrain) :
  - scenario-m9f-journal.log — la pièce DU RUN (171 o, md5 24680ac9…,
    TROIS lignes 16:56:09 : T0 VERT, T1 VERT, T2 VERT — le journal ne
    porte que les lignes journalées, le reste vivait sur la console) ;
  - console-run-m9f.txt — LA CONSOLE DU DÉVELOPPEUR (le paste du 07/11,
    md5 d6d1e931…) : les SEIZE T0 [ok], T1 aux SSN 85/7/15, T2 rax 0
    handle 0x304, T3 imprimant l'aléa et la clé privée DU RUN puis la
    « clé publique attendue » 000…0 (LE SYMPTÔME de la seconde faute),
    le TypeError ligne 593 — LA PIÈCE QUI RENVERSE L'ACQUITTEMENT ;
  - VERDICT-recoup-labo-m9f-2.txt — le verdict du RECOUP laboratoire
    (CRASH NOMMÉ COHÉRENT 12/12 sur pièces croisées, D138/D145/D148 :
    le crash REJOUÉ au labo, le symptôme EXPLIQUÉ sur pièces [la clé
    privée du run par l'échelle pré-réparation rend 000…0 — la vraie
    clé attendue eût été 1227429d…], les lignes 832/593 == la pointe
    35706ef octet pour octet, la finale 1.0.0 REFUSÉE pour CE run, le
    kit réparé à la source + le contrôle PERMANENT aux TROIS portes)
    — l'archive porte le jugement AVEC les pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle,
  ré-armé pour le TROISIÈME geste du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11/2026 (la correction du kit m9f, l'erratum n° 7) :
    le second run (06/11 16:56) est MORT d'un crash PYTHON nommé sur
    la console du développeur (TypeError ligne 593 :
    kit96.raw[:32] = alea — `.raw` est une copie bytes immuable : le
    crash était DÉTERMINISTE sur toute machine, l'acquittement « par
    élimination » de la note du 06/11 au soir est RENVERSÉ par la
    pièce) ; TROIS fautes au kit dans le segment Python pur (la pose
    du kit par tranches sur `.raw`, l'échelle du recoup rendant la clé
    attendue NULLE, la TAILLE au lieu du POINTEUR aux sites OUVRIR),
    réparées À LA SOURCE + LE CONTRÔLE PERMANENT aux TROIS portes à
    l'assemblage (preuve négative sur la pointe 35706ef : les TROIS
    refus nommés) ; kit-m9f.zip MIS À JOUR EN PLACE (md5 90a1d022… —
    le contenu remplacé, le fichier même conservé, l'ancien scénario
    vit dans l'histoire git à la pointe 35706ef) ; le LISEZMOI porte
    l'erratum ; le run 2 archivé → archives-preuves/preuves-run-m9f-2/
    AVEC la pièce console et le verdict du recoup ; la finale 1.0.0
    attend le TROISIÈME run vert sur pièces.
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
    print(f"[archivage] {nom} -> preuves-run-m9f-2/ (md5 "
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
    print("=== M9-(f) : LA CORRECTION DU KIT au coffre /test (l'erratum "
          "n° 7 — le crash PYTHON du second run, nommé sur la console) ===")
    try:
        # -- 1. le zip local corrigé, vérifié ---------------------------------
        if not os.path.isfile(KIT_ZIP):
            raise Refus(f"KIT : {KIT_ZIP} absent — assembler_kit_m9f.py "
                        "d'abord")
        if sha256f(KIT_ZIP) != KIT_SHA:
            raise Refus(f"KIT : kit-m9f.zip sha256 divergent "
                        f"({sha256f(KIT_ZIP)[:16]}…) — réassembler le kit "
                        "corrigé")
        if md5f(KIT_ZIP) != KIT_MD5:
            raise Refus("KIT : kit-m9f.zip md5 divergent — réassembler")
        print(f"[1] le kit corrigé : {os.path.getsize(KIT_ZIP)} o, md5 "
              f"{KIT_MD5[:8]}…, sha256 {KIT_SHA[:16]}… (26 constantes PAR "
              f"AST + les PORTES [2b]/[2c] de l'erratum 6/7 + extraction "
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
                            f"({md5_distant[:8]}…) — ni l'erratum 6 "
                            f"({ANCIEN_MD5[:8]}…) ni le corrigé "
                            f"({KIT_MD5[:8]}…) : constater avant geste")
            ds.upload_update(piece["id"], pathlib.Path(KIT_ZIP))
            apres = ds.list_folder(TEST_ID).get("kit-m9f.zip")
            md5_apres = (apres or {}).get("md5Checksum", "ABSENT")
            if not apres or md5_apres != KIT_MD5:
                raise Refus("kit-m9f.zip md5 divergent après mise à jour "
                            f"({md5_apres[:8]}…)")
            print(f"[2] kit-m9f.zip MIS À JOUR au coffre — md5 "
                  f"{KIT_MD5[:8]}… MATCH par relecture (le contenu "
                  f"remplacé, le fichier même conservé, rien jeté)")

        # -- 3. LISEZMOI-m9f.txt MIS À JOUR EN PLACE ---------------------------
        lis = racine.get("LISEZMOI-m9f.txt")
        if not lis:
            raise Refus("LISEZMOI-m9f.txt introuvable à la racine du /test")
        md5_lis_local = md5f(LISEZMOI_KIT)
        if lis.get("md5Checksum") == md5_lis_local:
            print("[3] LISEZMOI-m9f.txt porte déjà l'erratum n° 7 — "
                  "idempotent")
        else:
            if lis.get("md5Checksum") != ANCIEN_LIS_MD5:
                raise Refus(f"LISEZMOI-m9f.txt distant d'un md5 INATTENDU "
                            f"({(lis.get('md5Checksum') or 'ABSENT')[:8]}…)"
                            " — ni l'erratum 6 ni le corrigé : constater "
                            "avant geste")
            ds.upload_update(lis["id"], pathlib.Path(LISEZMOI_KIT))
            apres = ds.list_folder(TEST_ID).get("LISEZMOI-m9f.txt")
            if not apres or apres.get("md5Checksum") != md5_lis_local:
                raise Refus("LISEZMOI-m9f.txt md5 divergent après mise à "
                            "jour")
            print(f"[3] LISEZMOI-m9f.txt MIS À JOUR (md5 "
                  f"{md5_lis_local[:8]}… MATCH — l'erratum n° 7 consigné "
                  "au document du kit)")

        # -- 4. le SECOND RUN archivé (le journal + la pièce console + le
        #       verdict du recoup) ----------------------------------------------
        if not PIECE_CONSOLE.exists():
            raise Refus("console-run-m9f.txt local introuvable — la pièce "
                        "qui renverse l'acquittement")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f-2.txt local introuvable — "
                        "le recoup d'abord (scripts/eprouver_fix_m9f.py)")
        pm9 = racine.get("preuves-m9f") or {}
        if not pm9.get("id"):
            raise Refus("preuves-m9f/ introuvable au coffre")
        run_m9f2 = ds.list_folder(arch_p["id"]).get("preuves-run-m9f-2")
        if not run_m9f2:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f-2")
            print("[4] preuves-run-m9f-2/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_m9f2["id"]
            print("[4] preuves-run-m9f-2/ déjà présent — constaté")
        # (a) le journal DU RUN, DÉPLACÉ depuis le réceptacle du développeur
        entree = ds.list_folder(pm9["id"]).get(JOURNAL_RUN2)
        if entree:
            if entree.get("md5Checksum") != JOURNAL_RUN2_MD5:
                raise Refus(f"le journal du réceptacle porte un md5 "
                            f"inattendu ({entree.get('md5Checksum', '-')}"
                            "[:8]}…) — la pièce du run 2 attendue est "
                            f"{JOURNAL_RUN2_MD5[:8]}…")
            deplacer_vers(entree["id"], JOURNAL_RUN2, pm9["id"], run_id,
                          JOURNAL_RUN2_MD5)
        elif JOURNAL_RUN2 not in ds.list_folder(run_id):
            raise Refus(f"'{JOURNAL_RUN2}' ni dans preuves-m9f/ ni dans "
                        "l'archive — introuvable")
        else:
            print(f"[4] {JOURNAL_RUN2} déjà archivé — constaté")
        # (b) LA PIÈCE CONSOLE déposée (celle qui renverse l'acquittement)
        if "console-run-m9f.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "console-run-m9f.txt", PIECE_CONSOLE)
            print("[4] console-run-m9f.txt déposée (LA PIÈCE QUI RENVERSE "
                  "L'ACQUITTEMENT — le TypeError nommé, la clé attendue "
                  "NULLE lisible, le prompt revenu)")
        else:
            print("[4] console-run-m9f.txt déjà là — constaté")
        # (c) le verdict du recoup déposé AVEC les pièces
        if "VERDICT-recoup-labo-m9f-2.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f-2.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f-2.txt déposé (le jugement "
                  "AVEC les pièces — CRASH NOMMÉ COHÉRENT 12/12, la cause "
                  "AU LABO, le kit réparé)")
        else:
            print("[4] VERDICT-recoup-labo-m9f-2.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé -------------------------------------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle du TROISIÈME geste)")

        # -- 6. les DEUX INDEX mis à jour --------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f-2",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f-2)", avant_fin=True)
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "la correction du kit m9f, l'erratum n° 7",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note de "
                        "correction)")

        # -- 7. la vérification finale ------------------------------------------
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
        if set(PIECES_RUN2) - set(dans_run):
            raise Refus(f"preuves-run-m9f-2/ incomplet : "
                        f"{sorted(set(PIECES_RUN2) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit corrigé md5 {KIT_MD5[:8]}… recoupé) ; "
              f"preuves-run-m9f-2/ porte les {len(PIECES_RUN2)} pièces "
              "(le journal DU RUN + la pièce console + le verdict du "
              "recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[correction] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE COFFRE /test PORTE LE KIT CORRIGÉ (l'erratum n° 7 "
          "réparé à la source, le contrôle PERMANENT aux TROIS portes) : "
          "LE TROISIÈME GESTE du développeur est attendu — dézipper "
          "kit-m9f.zip dans un dossier NEUF (D99), python "
          "scenario-m9f.py (~10 s, réseau vivant), renvoyer preuves-m9f/ "
          "ENTIER au coffre — la finale 1.0.0 attend le vert ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
