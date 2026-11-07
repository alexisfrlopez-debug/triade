#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run5_m9f.py — LE CINQUIÈME RUN M9-(f) ARCHIVÉ au coffre /test
(le run du 2026-11-07 07:23:36, reçu et recoupé — ROUGE T3.ouvrir NOMMÉ :
rax -7, état 5, MAIS LA CHAÎNE A CHANGÉ : la ligne « le rappel émission :
sys-05 rend -6 » des runs 1/3/4 a DISPARU — LA PREMIÈRE ÉMISSION RÉELLE
DU PROJET, l'erratum n° 9 validé sur le vrai noyau ; la mort a reculé
d'UN CRAN, à LA PREMIÈRE LECTURE — le recoup 33/33).

Le kit est ACQUITTÉ (le MÊME binaire dev.3, le MÊME scénario — le kit du
/test demeure 79d44284…) : AUCUN dépôt de kit, AUCUN retrait — le geste
est L'ARCHIVAGE SEUL (modèle archiver_run4, D143 : par DÉPLACEMENT,
jamais un jet) :
  1. les pièces locales vérifiées (le trio md5-contrôlé par le recoup +
     le verdict du recoup 33/33) ;
  2. preuves-run-m9f-5/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. le trio DU RUN DÉPLACÉ du réceptacle vers l'archive ;
  4. le VERDICT-recoup-labo-m9f-5.txt déposé AVEC les pièces (l'archive
     porte le jugement) ;
  5. preuves-m9f/ ré-armé (son LISEZMOI seul — le réceptacle du
     SIXIÈME run) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, le kit INCHANGÉ, les
     empreintes recoupées).

Usage : python3 scripts/archiver_run5_m9f.py
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

TRIO_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-5")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-run-m9f-5/"
    "VERDICT-recoup-labo-m9f-5.txt")

TRIO = {"temoin-m9f.txt": "b080c083",
        "scenario-m9f-journal.log": "3fec82c8",
        "VERDICT-run-m9f.txt": "02b90aa4"}

KIT_MD5 = "79d44284c70261375a2b055070fda223"   # le kit RÉPARÉ, INCHANGÉ

PIECES_RUN5 = sorted(TRIO) + ["VERDICT-recoup-labo-m9f-5.txt"]

INDEX_PREUVES_SECTION = """
preuves-run-m9f-5/ (archivées le 07/11, geste du CINQUIÈME run M9-(f) —
LE PREMIER RUN DU BUILD RÉPARÉ 1.0.0-dev.3 [l'erratum n° 9 : le WSABUF
canonique, la révision 2 étendue signée et installée] ; le terrain TENU
[Windows 11 build 26300, ntdll b072efae… — LE MÊME que le run 4 ; Python
3.13.9 — l'interpréteur seul change, sans effet sur le natif], l'artefact
RÉPARÉ de23e577… [LA POSE canonique relue DANS L'IMAGE aux DEUX blocs —
les DEUX contrôles T0.erratum-9 [ok]], le kit ACQUITTÉ INCHANGÉ
[79d44284…] ; ROUGE T3.ouvrir NOMMÉ : rax -7, état 5 — MAIS LA CHAÎNE A
CHANGÉ : la ligne « le rappel émission : sys-05 rend -6 » des runs 1/3/4
a DISPARU [sys-05 rend 0 : LA PREMIÈRE ÉMISSION RÉELLE DU PROJET — le CH
119 o PARTI SUR LE RÉSEAU par le VRAI afd.sys, recoupé octet pour octet ;
L'ERRATUM n° 9 VALIDÉ SUR LE TERRAIN RÉEL — L'A/B CONCLUT : la réparation
est la cause de la guérison] ; la mort a reculé d'UN CRAN — LA PREMIÈRE
LECTURE [sys-06, le ServerHello attendu : JAMAIS JOURNALÉE par le
scénario] rend non-nul → la machine -7 [« la coupure du socle », tls13-27
Q3], l'état 5 — la frontière que l'Entrée 187 nommait d'avance ; LE TEMPS
ÉLIMINE LE SILENCE [le run entier dans SA seconde : le verdict de
réception fut SEC — un refus du noyau ou une fermeture vive du pair, pas
une attente muette] :
  - temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt — les
    pièces DU RUN (Windows 10.0 build 26300, Python 3.13.9 AMD64, le run
    entier dans SA seconde 07:23:36 : T0/T1/T2 VERT, T3 le CH ÉMIS et
    recoupé, la première lecture en échec -7, la mort nommée un cran
    plus loin) ;
  - VERDICT-recoup-labo-m9f-5.txt — le verdict du RECOUP laboratoire
    (ROUGE CONSTATÉ COHÉRENT 33/33 sur pièces croisées, D138/D145/D148 :
    l'échelle REJOUÉE sur la clé privée DU RUN rend la clé du témoin, la
    construction CH re-jouée [114 o, le vol 119 o], la chaîne reconstituée
    depuis les contrats, LA DIFFÉRENCE D'UNE LIGNE constatée par code
    [F1 : le journal du run 5 == le journal du run 4 MOINS la ligne «
    sys-05 rend -6 », les horodatements exceptés], L'A/B PROPRE [F3 : le
    même noyau, l'autre pose — la réparation est la cause de la
    guérison], LA PRÉDICTION DE L'ENTRÉE 187 TENUE [F4 : un cran plus
    loin], LE -7 A CHANGÉ DE CHAÎNE [F5], LE TEMPS ÉLIMINE LE SILENCE
    [F6] — les candidats : le passager réseau [AFFAIBLI par le temps,
    PAS ÉLIMINÉ], le contrat de réception sys-06 [la spec R2 le nomme
    elle-même : « La réception n'a JAMAIS couru sur le terrain réel » —
    réparée PAR SYMÉTRIE, jamais mesurée par sonde], LA DEMI-FIN [le pair
    a refermé proprement à l'offre sans SNI] — LE CODE EXACT vit dans
    rdx : UN SEUL MOT D'INFORMATION MANQUE, LA SONDE sys-06 LE LIRAIT si
    le -7 se reproduit identique) — l'archive porte le jugement AVEC les
    pièces.
  preuves-m9f/ demeure à la racine avec son LISEZMOI (le réceptacle,
  ré-armé pour LE SIXIÈME run du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11/2026 (le CINQUIÈME run M9-(f) reçu et recoupé — le
    premier run du build réparé 1.0.0-dev.3) : le MÊME kit 79d44284…
    exécuté sur Windows 11 build 26300 (le run : 2026-11-07 07:23:36,
    l'heure de la machine du développeur) ; T0/T1/T2 VERT (LES DIX-HUIT
    T0 — dont LES DEUX T0.erratum-9 : la pose du WSABUF canonique relue
    DANS L'IMAGE aux DEUX blocs —, SSN 85/7/15, handle 0x284), le recoup
    du jalon VERT (le CH == la construction re-jouée, 119 o), LA PREMIÈRE
    ÉMISSION RÉELLE DU PROJET (sys-05 rend 0 : la ligne « le rappel
    émission : sys-05 rend -6 » des runs 1/3/4 a DISPARU — L'ERRATUM
    n° 9 VALIDÉ SUR LE VRAI NOYAU : le refus -6 ACCESS_VIOLATION de la
    sonde Entrée 185 est mort) ; LA MORT A RECULÉ D'UN CRAN — à LA
    PREMIÈRE LECTURE (le ServerHello attendu) : la réception rend
    non-nul → la machine -7 (« la coupure du socle »), l'état 5 —
    exactement la frontière que l'Entrée 187 nommait d'avance ; LE TEMPS
    ÉLIMINE LE SILENCE : le run entier dans SA seconde — le verdict de
    réception fut SEC (un refus du noyau ou une fermeture vive du pair,
    pas une attente muette : la garde-chien tire à 300 s) ; le kit
    ACQUITTÉ INCHANGÉ (le MÊME binaire dev.3 de23e577…, le MÊME
    scénario) ; le run archivé → archives-preuves/preuves-run-m9f-5/
    AVEC le verdict du recoup (33/33) ; LE GESTE AU DÉVELOPPEUR : LE
    SIXIÈME RUN — le MÊME kit, un dossier NEUF D99, réseau vivant (UN
    AUTRE réseau si possible : le discriminant du passager), les pièces
    au coffre /test/preuves-m9f/ — SI LE VERT VIENT : LA FINALE 1.0.0,
    LE JALON M9 — LA GRANDE ŒUVRE ; SI LE -7 SE REPRODUIT IDENTIQUE :
    LA SONDE sys-06 s'ouvre (nommée d'avance — lire le NTSTATUS brut ou
    le zéro de la réception, le miroir de l'Entrée 185).
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
    print(f"[archivage] {nom} -> preuves-run-m9f-5/ (md5 "
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
    print("=== M9-(f) : LE CINQUIÈME RUN ARCHIVÉ au coffre /test (le kit "
          "ACQUITTÉ demeure — le geste est l'archive seule) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in TRIO.items():
            chemin = TRIO_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — "
                            "ramasse_run5_m9f.py d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-m9f-5.txt local introuvable — "
                        "le recoup d'abord (scripts/recouper_run5_m9f.py)")
        print(f"[1] les pièces locales vérifiées (le trio md5-contrôlé + "
              f"le verdict du recoup {md5f(VERDICT_RECOUP_LOCAL)[:8]}…, "
              "33/33)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-run-m9f-5/ créé ------------------------------------------
        run_m9f5 = ds.list_folder(arch_p["id"]).get("preuves-run-m9f-5")
        if not run_m9f5:
            run_id = ds.create_folder(arch_p["id"], "preuves-run-m9f-5")
            print("[2] preuves-run-m9f-5/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_m9f5["id"]
            print("[2] preuves-run-m9f-5/ déjà présent — constaté")

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
        if "VERDICT-recoup-labo-m9f-5.txt" not in ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-m9f-5.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-m9f-5.txt déposé (le jugement "
                  "AVEC les pièces — ROUGE CONSTATÉ COHÉRENT 33/33, "
                  "L'ÉMISSION RÉPARÉE, la mort un cran plus loin)")
        else:
            print("[4] VERDICT-recoup-labo-m9f-5.txt déjà là — constaté")

        # -- 5. preuves-m9f/ ré-armé ----------------------------------------------
        restants = ds.list_folder(pm9["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-m9f/ ne porte pas seulement son LISEZMOI "
                        f"après l'archivage : {sorted(restants)}")
        print("[5] preuves-m9f/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle du SIXIÈME run)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-run-m9f-5",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-run-m9f-5)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "le CINQUIÈME run M9-(f) reçu et recoupé",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du "
                        "cinquième run)")

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
        if set(PIECES_RUN5) - set(dans_run):
            raise Refus(f"preuves-run-m9f-5/ incomplet : "
                        f"{sorted(set(PIECES_RUN5) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, le "
              f"kit RÉPARÉ md5 {KIT_MD5[:8]}… INCHANGÉ — recoupé) ; "
              f"preuves-run-m9f-5/ porte les {len(PIECES_RUN5)} pièces "
              "(le trio DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE CINQUIÈME RUN EST ARCHIVÉ avec son jugement : LA PREMIÈRE "
          "ÉMISSION RÉELLE DU PROJET (l'erratum n° 9 validé sur le vrai "
          "noyau), LA MORT UN CRAN PLUS LOIN — à la première lecture ; LE "
          "SIXIÈME RUN EST LE GESTE AU DÉVELOPPEUR (réseau vivant — SI LE "
          "-7 SE REPRODUIT IDENTIQUE : LA SONDE sys-06, nommée d'avance) "
          "===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
