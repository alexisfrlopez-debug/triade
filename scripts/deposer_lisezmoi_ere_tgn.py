#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_lisezmoi_ere_tgn.py — LE DÉPÔT ET LE RECOUP DU KIT DE LA CÉRÉMONIE
D'ÈRE DU TGN au dossier /Cérémonie du Drive (modèle Entrées 159/167 —
deposer_lisezmoi_ere_m9.py) :
  1. LISEZMOI-ceremonie-ere-TGN.txt (la re-signature m0 + loupe pas à pas,
     la règle d'or « JAMAIS generer ») téléversé à la racine du /Cérémonie
     (ou déjà déposé par le hook D130 — idempotent), md5 CONTRÔLÉ PAR
     RELECTURE (aller-retour) ;
  2. la remise v06/sceau-I/a-signer.txt du kit recoupée == celle du dépôt
     (la charge RÉGÉNÉRÉE sur l'arbre complet — syncée par le geste du
     commit, D130) : QUATORZE arbres, m0 667fb5ae… (le registre étendu) et
     loupe 59e4871a… (l'arbre neuf) lus noir sur blanc ;
  3. l'état final listé (la main du développeur est SERVIE).

Usage : python3 scripts/deposer_lisezmoi_ere_tgn.py
Code de sortie : 0 = kit déposé et recoupé ; 2 = refus nommé."""

import hashlib
import pathlib
import sys

REPO = "/home/z/my-project/triade"
sys.path.insert(0, REPO + "/scripts")
import drive_sync as ds  # noqa: E402

LISEZMOI_LOCAL = pathlib.Path(
    "/home/z/my-project/download/LISEZMOI-ceremonie-ere-TGN.txt")
LISEZMOI_NOM = "LISEZMOI-ceremonie-ere-TGN.txt"
ASIGNER_LOCAL = pathlib.Path(REPO + "/v06/sceau-I/a-signer.txt")

EMP_M0 = "667fb5ae36e4ab3c"
EMP_LOUPE = "59e4871ab5b47623"


def refus(nom, detail):
    print(f"[kit-tgn] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_fichier(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def main():
    if not LISEZMOI_LOCAL.exists():
        refus("LOCAL", f"{LISEZMOI_LOCAL} introuvable")
    md5_local = md5_fichier(LISEZMOI_LOCAL)
    print(f"[0] le LISEZMOI local : {LISEZMOI_NOM} "
          f"({LISEZMOI_LOCAL.stat().st_size} o, md5 {md5_local[:8]}…)")

    coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
    cmt = coffre.get("Cérémonie") or refus("DOSSIER", "/Cérémonie introuvable")
    racine = ds.list_folder(cmt["id"])

    # -- 1. le LISEZMOI téléversé (ou déjà présent), md5 par relecture -------------
    deja = racine.get(LISEZMOI_NOM)
    if deja:
        if deja.get("md5Checksum") != md5_local:
            ds.upload_update(deja["id"], LISEZMOI_LOCAL)
        else:
            print(f"[1] {LISEZMOI_NOM} déjà présent (md5 MATCH) — idempotent")
    else:
        ds.upload_create(cmt["id"], LISEZMOI_NOM, LISEZMOI_LOCAL)
    apres = ds.list_folder(cmt["id"]).get(LISEZMOI_NOM) \
        or refus("DEPOT", f"{LISEZMOI_NOM} absent après dépôt")
    if apres.get("md5Checksum") != md5_local:
        refus("DEPOT", f"{LISEZMOI_NOM} : md5 distant ≠ local après dépôt")
    print(f"[1] déposé au /Cérémonie : {LISEZMOI_NOM} "
          f"(md5 {md5_local[:8]}… MATCH par relecture)")

    # -- 2. la remise du kit recoupée == celle du dépôt -----------------------------
    v06 = racine.get("v06") or refus("KIT", "v06/ introuvable au /Cérémonie")
    sceau = ds.list_folder(v06["id"]).get("sceau-I") \
        or refus("KIT", "v06/sceau-I/ introuvable")
    asigner_distant = ds.list_folder(sceau["id"]).get("a-signer.txt") \
        or refus("KIT", "v06/sceau-I/a-signer.txt introuvable au /Cérémonie")
    md5_local_asigner = md5_fichier(ASIGNER_LOCAL)
    if asigner_distant.get("md5Checksum") != md5_local_asigner:
        refus("REMISE", "a-signer.txt du kit ≠ celui du dépôt — la synchro "
                        "D130 n'a pas porté la charge régénérée (le commit "
                        "précède le dépôt)")
    lignes = ASIGNER_LOCAL.read_text(encoding="utf-8").splitlines()
    if len(lignes) != 14:
        refus("REMISE", f"{len(lignes)} lignes à la remise (attendu : 14 arbres)")
    m0 = next((l for l in lignes if l.startswith("m0 ")), "")
    loupe = next((l for l in lignes if l.startswith("loupe ")), "")
    if EMP_M0 not in m0:
        refus("REMISE", f"l'empreinte m0 n'est pas {EMP_M0}… — la charge du geste "
                        "n'est pas celle servie")
    if EMP_LOUPE not in loupe:
        refus("REMISE", f"l'empreinte loupe n'est pas {EMP_LOUPE}… — l'arbre neuf "
                        "absent de la remise")
    print(f"[2] la remise du kit == celle du dépôt (md5 "
          f"{md5_local_asigner[:8]}… MATCH — QUATORZE arbres ; "
          f"m0 {m0.split()[-1][:8]}… = LE REGISTRE ÉTENDU ; "
          f"loupe {loupe.split()[-1][:8]}… = L'ARBRE NEUF des 19 fichiers)")

    # -- 3. l'état final -------------------------------------------------------------
    final = sorted(ds.list_folder(cmt["id"]))
    print(f"[3] la racine du /Cérémonie ({len(final)} entrées) : "
          f"{', '.join(final[:16])}{'…' if len(final) > 16 else ''}")
    print("=== LE KIT DE LA CÉRÉMONIE D'ÈRE DU TGN EST DÉPOSÉ — la main du "
          "développeur est SERVIE (le LISEZMOI pas à pas + la remise FRAÎCHE "
          "des QUATORZE arbres + les outils) ===")
    return 0


if __name__ == "__main__":
    main()
