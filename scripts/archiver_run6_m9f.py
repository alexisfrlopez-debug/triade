#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run6_m9f.py — LE SIXIÈME RUN M9-(f) ARCHIVÉ au coffre /test
(le run du 2026-11-07 08:31:42, reçu et recoupé 33/33 — LE JUMEAU DU RUN 5 :
le -7 REPRODUIT IDENTIQUE, l'émission VERT encore, le run entier dans SA
seconde — LA CONDITION NOMMÉE D'AVANCE EST REMPLIE : LE PASSAGER ÉLIMINÉ
SUR PIÈCES, LA SONDE sys-06 S'OUVRE).

Le kit est ACQUITTÉ (le MÊME binaire dev.3, le MÊME scénario — le kit du
/test demeure 79d44284…) : AUCUN dépôt de kit, AUCUN retrait — le geste
est L'ARCHIVAGE SEUL (modèle archiver_run5, D143 : par DÉPLACEMENT,
jamais un jet) :
  1. les pièces locales vérifiées (le trio md5-contrôlé par le recoup +
     le verdict du recoup 33/33) ;
  2. preuves-run-m9f-6/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. le trio DU RUN DÉPLACÉ du réceptacle vers l'archive ;
  4. le VERDICT-recoup-labo-m9f-6.txt déposé AVEC les pièces (l'archive
     porte le jugement) ;
  5. preuves-m9f/ ré-armé (son LISEZMOI seul — le réceptacle est clos :
     le geste au développeur EST LA SONDE SYS-06, livrée au /test par
     le même geste) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, le kit INCHANGÉ, les
     empreintes recoupées).

Usage : python3 scripts/archiver_run6_m9f.py
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

TRIO_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-6")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-6/"
    "VERDICT-recoup-labo-m9f-6.txt")

TRIO = {"temoin-m9f.txt": "9351b2bf",
        "scenario-m9f-journal.log": "acdc0fe8",
        "VERDICT-run-m9f.txt": "f432bc45"}

KIT_MD5 = "79d44284c70261375a2b055070fda223"   # le kit RÉPARÉ, INCHANGÉ

PIECES_RUN6 = sorted(TRIO) + ["VERDICT-recoup-labo-m9f-6.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f-6/ (archivées le 07/11, geste du SIXIÈME run M9-(f) — LE
JUMEAU DU RUN 5, reçu sur la demande du recoup-5 « réessayez réseau
vivant » ; le terrain TENU [Windows 11 build 26300, ntdll b072efae… —
LE MÊME que les runs 4/5 ; Python 3.14.3 — l'interpréteur seul change,
sans effet sur le natif], l'artefact RÉPARÉ de23e577… [LE MÊME rebuild
dev.3 que le run 5], le kit ACQUITTÉ INCHANGÉ [79d44284…]) ; LA SECONDE
ÉMISSION RÉELLE DU PROJET [sys-05 rend 0 ENCORE : le CH 119 o ÉMIS et
recoupé octet pour octet — l'émission réparée du run 5 N'ÉTAIT PAS UN
PASSAGER : elle TIENT] ; LE ROUGE AU MÊME GESTE [T3.ouvrir rax -7, état
5 — LA PREMIÈRE LECTURE, le run entier dans SA seconde 08:31:42] ; LE
JUMEAU CONSTATÉ PAR CODE [F1 : le journal du run 6 == le journal du run
5 LIGNE À LIGNE, les horodatements exceptés ; F2 : les témoins
divergent sur les invariants seuls — l'interpréteur, l'ASLR, le handle,
LE BORD DNS changé 104.16.124.96 → 104.16.123.96, l'aléa et les clés ;
le noyau et l'artefact TENUS] ; LE -7 REPRODUIT IDENTIQUE — LA CONDITION
NOMMÉE D'AVANCE PAR LE RECOUP-5 ET LA PASSATION 107 REMPLIE : LE
PASSAGER ÉLIMINÉ SUR PIÈCES ; restent DEUX candidats : le contrat de
réception sys-06 [réparé PAR SYMÉTRIE, jamais mesuré par sonde] et LA
DEMI-FIN [le pair a refermé proprement à l'offre sans SNI] :
  - temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt — les
    pièces DU RUN (Windows 10.0 build 26300, Python 3.14.3 AMD64, le run
    entier dans SA seconde 08:31:42 : T0/T1/T2 VERT, T3 le CH ÉMIS et
    recoupé ENCORE, la première lecture en échec -7 au même geste que le
    run 5) ;
  - VERDICT-recoup-labo-m9f-6.txt — le verdict du RECOUP laboratoire
    (ROUGE CONSTATÉ COHÉRENT 33/33 sur pièces croisées, D138/D145/D148 :
    l'échelle REJOUÉE sur la clé privée DU RUN rend la clé du témoin,
    la construction CH re-jouée [114 o, le vol 119 o], LE JUMEAU CONSTATÉ
    PAR CODE [F1 : les journaux identiques ligne à ligne], LE PASSAGER
    ÉLIMINÉ SUR PIÈCES [F3 : l'émission VERT ×2, la réception -7 ×2, le
    run en SA seconde ×2, le bord DNS changé], LE TEMPS ENCORE [F5], LA
    COHÉRENCE UNANIME [F6 : aucune pièce conditionnelle née aux DEUX
    runs] — le verdict NOMME le geste : LA SONDE SYS-06 S'OUVRE) —
    l'archive porte le jugement AVEC les pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle m9f
  est clos : le geste au développeur EST LA SONDE SYS-06 — livrée au
  /test par le même geste, le réceptacle preuves-sonde-sys06/ né).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11/2026 (le SIXIÈME run M9-(f) reçu et recoupé — LE
    JUMEAU DU RUN 5) : le MÊME kit 79d44284… exécuté sur Windows 11
    build 26300 (le run : 2026-11-07 08:31:42, l'heure de la machine du
    développeur) ; T0/T1/T2 VERT (LES DIX-HUIT T0 — dont LES DEUX
    T0.erratum-9 —, SSN 85/7/15, handle 0x338), LE CH 119 o ÉMIS ET
    RECOUPÉ ENCORE (sys-05 rend 0 : LA SECONDE ÉMISSION RÉELLE DU
    PROJET — l'émission réparée du run 5 N'ÉTAIT PAS UN PASSAGER : elle
    TIENT) ; le run entier dans SA seconde (08:31:42) ; T3.ouvrir rax
    -7, état 5 — LA PREMIÈRE LECTURE, LE MÊME GESTE QUE LE RUN 5 ; le
    recoup labo 33/33 : LE JUMEAU CONSTATÉ PAR CODE (le journal du run 6
    == le journal du run 5 LIGNE À LIGNE, les horodatements exceptés ;
    les témoins divergent sur les invariants seuls — dont LE BORD DNS
    changé 104.16.124.96 → 104.16.123.96 : une AUTRE arête Cloudflare a
    répondu, le même verdict est revenu) ; LE -7 REPRODUIT IDENTIQUE —
    LA CONDITION NOMMÉE D'AVANCE EST REMPLIE : LE PASSAGER ÉLIMINÉ SUR
    PIÈCES ; restent le contrat de réception sys-06 et LA DEMI-FIN ; le
    run archivé → archives-preuves/preuves-run-m9f-6/ AVEC le verdict du
    recoup (33/33) ; LE GESTE AU DÉVELOPPEUR : LA SONDE SYS-06 — le
    kit-sonde-sys06.zip LIVRÉ à la racine par LE MÊME GESTE (le miroir
    de l'Entrée 185 : lire LE NTSTATUS BRUT de la première lecture
    réelle — rdx, sys-06 Q5 — ou LE ZÉRO de la demi-fin — Q2 ; le
    compas étalonné avant la mesure, la contre-épreuve standard S4
    embarquée : si la lecture rend des octets, LA POIGNÉE SUIT DANS LE
    MÊME RUN — LA PERCÉE, la finale 1.0.0 en vue, LE JALON M9 — LA
    GRANDE ŒUVRE).
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
    print(f"[archivage] {nom} -> preuves-run-m9f-6/ (md5 "
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
    print("=== M9-(f) : LE SIXIÈME RUN ARCHIVÉ au coffre /test (le kit "
          "ACQUITTÉ demeure — le geste est l'archive seule ; la sonde "
          "sys-06 se livre APRES, au même geste) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in TRIO.items():
            chemin = TRIO_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — "
                            "ramasse_run6_m9f.py d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f-6.txt local introuvable — "
                        "le recoup d'abord (scripts/recouper_run6_m9f.py)")
        print(f"[1] les pièces locales vérifiées (le trio md5-contrôlé + "
              f"le verdict du recoup {md5f(VERDICT_RECOUP_LOCAL)[:8]}…, "
              "33/33)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-run-m9f-6/ créé ------------------------------------------
        run_m9f6 = ds.list_folder(arch_p["id"]).get("preuves-run-m9f-6")
        if not run_m9f6:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f-6")
            print("[2] preuves-run-m9f-6/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_m9f6["id"]
            print("[2] preuves-run-m9f-6/ déjà présent — constaté")

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
        if "VERDICT-recoup-labo-m9f-6.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f-6.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f-6.txt déposé (le jugement "
                  "AVEC les pièces — ROUGE CONSTATÉ COHÉRENT 33/33, LE "
                  "JUMEAU, LE PASSAGER ÉLIMINÉ, LA SONDE NOMMÉE)")
        else:
            print("[4] VERDICT-recoup-labo-m9f-6.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé (le réceptacle m9f est CLOS) -----------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle m9f est CLOS — le geste "
              "au développeur est LA SONDE SYS-06, livrée au /test par le "
              "même geste)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f-6",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f-6)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "le SIXIÈME run M9-(f) reçu et recoupé",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du "
                        "sixième run)")

        # -- 7. la vérification finale ----------------------------------------------
        final = ds.list_folder(TEST_ID)
        attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                    "archives-livraisons", "archives-preuves",
                    "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                    "preuves-sonde-sys05", "kit-sonde-sys05.zip",
                    "LISEZMOI-sonde-sys05.txt",
                    "corriger-wsb.bat", "corriger-wsb.ps1",
                    "signatures-I.txt", "cle-publique-I.txt"}
        manquants = attendus - set(final)
        if manquants:
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_MD5:
            raise Refus("le kit de la racine a divergé — le kit RÉPARÉ "
                        "doit demeurer 79d44284…")
        dans_run = ds.list_folder(run_id)
        if set(PIECES_RUN6) - set(dans_run):
            raise Refus(f"preuves-run-m9f-6/ incomplet : "
                        f"{sorted(set(PIECES_RUN6) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit RÉPARÉ md5 {KIT_MD5[:8]}… INCHANGÉ — recoupé) ; "
              f"preuves-run-m9f-6/ porte les {len(PIECES_RUN6)} pièces "
              "(le trio DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE SIXIÈME RUN EST ARCHIVÉ avec son jugement : LE JUMEAU "
          "CONSTATÉ PAR CODE, LE -7 REPRODUIT IDENTIQUE, LE PASSAGER "
          "ÉLIMINÉ SUR PIÈCES — LA SONDE SYS-06 SE LIVRE AU /test PAR LE "
          "MÊME GESTE (le miroir de l'Entrée 185 : le NTSTATUS brut ou LE "
          "ZÉRO de la première lecture réelle) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
