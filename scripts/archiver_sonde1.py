#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_sonde1.py — LE PREMIER RUN DE LA SONDE SYS-05 (m9-(g)) ARCHIVÉ
au coffre /test (le run du 2026-11-06 20:34:30, reçu et recoupé — VERT-
MESURE : LA MESURE RENDUE, LE COUPABLE NOMMÉ à l'instruction près : la
pose du WSABUF, spec R1-Q3 « 12 o » ; le verdict manquant expliqué par
l'erratum n° 8 ; le recoup 31/31).

Les DEUX kits sont ACQUITTÉS (le même binaire, le même scénario — le kit
de la racine demeure 215c2caa… ET 90a1d022…) : AUCUN dépôt de kit,
AUCUN retrait — le geste est L'ARCHIVAGE SEUL (modèle archiver_run4,
D143 : par DÉPLACEMENT, jamais un jet) :
  1. les pièces locales vérifiées (le trio md5-contrôlé par le recoup +
     le verdict du recoup 31/31) ;
  2. preuves-sonde-sys05-1/ créé dans archives-preuves/ (D99 : jamais
     mélanger les runs) ;
  3. le trio DU RUN DÉPLACÉ du réceptacle vers l'archive ;
  4. le VERDICT-recoup-labo-sonde-sys05-1.txt déposé AVEC les pièces
     (l'archive porte le jugement) ;
  5. preuves-sonde-sys05/ ré-armé (son LISEZMOI seul — le réceptacle du
     prochain run) ;
  6. LES DEUX INDEX mis à jour ;
  7. la vérification finale (la racine en ordre, les DEUX kits
     INCHANGÉS, les empreintes recoupées).

Usage : python3 scripts/archiver_sonde1.py
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

TRIO_LOCAL = pathlib.Path("/home/z/my-project/download/preuves-sonde-sys05-1")
VERDICT_RECOUP_LOCAL = pathlib.Path(
    "/home/z/my-project/download/preuves-sonde-sys05-1/"
    "VERDICT-recoup-labo-sonde-sys05-1.txt")

TRIO = {"temoin-sonde-sys05.txt": "dbfce3f7",
        "sonde-sys05-journal.log": "a860c870",
        "journal-emissions.txt": "42b60aa7"}

KIT_SONDE_MD5 = "215c2caa54332ce91b03fd55c335513b"   # l'acquitté, INCHANGÉ
KIT_M9F_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"     # l'acquitté, INCHANGÉ

PIECES_RUN1 = sorted(TRIO) + ["VERDICT-recoup-labo-sonde-sys05-1.txt"]

INDEX_PREUVES_SECTION = """
preuves-sonde-sys05-1/ (archivées le 07/11 au soir — LE PREMIER RUN de la
SONDE SYS-05 (m9-(g), le chantier promis par le recoup du run 4) : LA
MESURE RENDUE, LE COUPABLE NOMMÉ à l'instruction près — le NTSTATUS BRUT
du geste m9f EST 0xC0000005 STATUS_ACCESS_VIOLATION, TROIS fois
[déterministe : ni taille, ni délai, ni session], le compas étalonné
[-6 + 0xC0000008 sur le handle invalide : la capture lit VRAIMENT rdx],
la contre-épreuve S4 : NON-RÉGRESSION [le chemin standard meurt pareil :
-7, état 5] ; LE COUPABLE : (b) LE CONTRAT D'APPEL — LA POSE DU WSABUF
[spec R1-Q3 « 12 o » : buf posé à +4, le noyau lit le canonique à +8 —
relu dans l'ARTEFACT SCELLÉ à sys-05+0x46] ; le -6 des CINQ runs
EXPLIQUÉ ; le verdict manquant EXPLIQUÉ [l'erratum n° 8 : le jmp rel32
du tromphone T6, ~126 Tio ≫ 2 Gio] ; la même machine que le run 4
[build 26300, Python 3.14.3, ntdll b072efae…], l'artefact INTACT
[d8928934…], les DEUX kits ACQUITTÉS INCHANGÉS [215c2caa… + 90a1d022…] :
  - temoin-sonde-sys05.txt, sonde-sys05-journal.log,
    journal-emissions.txt — les pièces DU RUN (le run entier dans SA
    seconde 20:34:30 : T0/T1/T2 VERT, le trampoline 33 o consigné, le
    compas, LA MESURE, les variations, S4 ; journal-emissions.txt : le
    CH refusé, 119 o, UN enregistrement) ;
  - VERDICT-recoup-labo-sonde-sys05-1.txt — le verdict du RECOUP
    laboratoire (VERT-MESURE 31/31 sur pièces croisées, D138/D145/D148 :
    le trampoline DÉCODÉ instruction par instruction == le squelette
    spécifié, l'échelle DE LA SOURCE re-jouée sur la clé privée DU RUN
    rend la clé du témoin, la chaîne -6 → -7 reconstituée, le coupable
    LU dans l'artefact scellé, la mort en T6 nommée) — l'archive porte
    le jugement AVEC les pièces.
  preuves-sonde-sys05/ demeure à la racine avec son LISEZMOI (le
  réceptacle, ré-armé pour le prochain run du développeur).
"""

INDEX_LIVRAISONS_ADDENDUM = """
--- note du 07/11/2026 au soir (LE PREMIER RUN DE LA SONDE SYS-05 reçu et
    recoupé — la mesure que les quatre runs m9f attendaient) : le MÊME kit
    215c2caa… exécuté sur la machine Windows 11 build 26300 (le run :
    2026-11-06 20:34:30, l'heure de la machine du développeur) ;
    T0/T1/T2 VERT, le trampoline de capture posé (33 o consignés), le
    compas étalonné (STATUS_INVALID_HANDLE : la capture lit VRAIMENT
    rdx) ; LA MESURE : LE NTSTATUS BRUT DU GESTE M9F = 0xC0000005
    (STATUS_ACCESS_VIOLATION), classe ERREUR, TROIS fois — la mesure, la
    variation taille, la variation délai : DÉTERMINISTE ; S4 : le chemin
    standard meurt AU MÊME GESTE (-7, état 5) — NON-RÉGRESSION : le
    refus est AU BLOC ; LE COUPABLE NOMMÉ À L'INSTRUCTION PRÈS : (b) LE
    CONTRAT D'APPEL — LA POSE DU WSABUF (spec sys-05:R1 Q3 « 12 o », le
    pointeur buf à +4 au lieu du canonique +8 : le noyau lit une adresse
    FOLLE et rend ACCESS_VIOLATION — relu dans l'artefact scellé) ; le
    verdict du run manquant EXPLIQUÉ : l'erratum n° 8 (le jmp rel32 du
    tromphone NtClose du T6 ne peut pas coder ~126 Tio : struct.error —
    le T6 n'avait JAMAIS couru sur le terrain) ; le recoup labo 31/31,
    le run archivé → archives-preuves/preuves-sonde-sys05-1/ AVEC le
    verdict ; LA RÉPARATION SELON LA CHARTE : LA RÉVISION 2 DE LA SPEC
    SYS-05 (le WSABUF canonique 16 o) + l'erratum n° 8 réparé à la
    source (l'adressage absolu) ; LE REBUILD 1.0.0-dev.3 EST LE GESTE
    SUIVANT — puis le kit m9f réparé, le run du développeur, ET SI LE
    VERT TIENT : LA FINALE 1.0.0, le jalon M9 — LA GRANDE ŒUVRE.
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
    print(f"[archivage] {nom} -> preuves-sonde-sys05-1/ (md5 "
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
    print("=== M9-(g) : LE PREMIER RUN DE LA SONDE ARCHIVÉ au coffre "
          "/test (les DEUX kits ACQUITTÉS demeurent — le geste est "
          "l'archive seule) ===")
    try:
        # -- 1. les pièces locales, vérifiées ------------------------------------
        for nom, prefixe in TRIO.items():
            chemin = TRIO_LOCAL / nom
            if not chemin.exists():
                raise Refus(f"la pièce locale {nom} est absente — "
                            "ramasse_sonde1.py d'abord")
            if not md5f(chemin).startswith(prefixe):
                raise Refus(f"la pièce locale {nom} d'un md5 inattendu "
                            f"({md5f(chemin)[:8]}…)")
        if not VERDICT_RECOUP_LOCAL.exists():
            raise Refus("VERDICT-recoup-labo-sonde-sys05-1.txt local "
                        "introuvable — le recoup d'abord "
                        "(scripts/recouper_sonde1.py)")
        print(f"[1] les pièces locales vérifiées (le trio md5-contrôlé + "
              f"le verdict du recoup {md5f(VERDICT_RECOUP_LOCAL)[:8]}…, "
              "31/31)")

        racine = ds.list_folder(TEST_ID)
        arch_p = racine.get("archives-preuves")
        if not (arch_p or {}).get("id"):
            raise Refus("archives-preuves/ introuvable au coffre /test")

        # -- 2. preuves-sonde-sys05-1/ créé ---------------------------------------
        run_s1 = ds.list_folder(arch_p["id"]).get("preuves-sonde-sys05-1")
        if not run_s1:
            run_id = ds.create_folder(arch_p["id"], "preuves-sonde-sys05-1")
            print("[2] preuves-sonde-sys05-1/ créé dans archives-preuves/ "
                  "(D99 : jamais mélanger les runs)")
        else:
            run_id = run_s1["id"]
            print("[2] preuves-sonde-sys05-1/ déjà présent — constaté")

        # -- 3. le trio DU RUN, DÉPLACÉ depuis le réceptacle ---------------------
        psonde = racine.get("preuves-sonde-sys05") or {}
        if not psonde.get("id"):
            raise Refus("preuves-sonde-sys05/ introuvable au coffre")
        for nom, prefixe in TRIO.items():
            entree = ds.list_folder(psonde["id"]).get(nom)
            if entree:
                if not entree.get("md5Checksum", "").startswith(prefixe):
                    raise Refus(f"la pièce distante {nom} d'un md5 "
                                "inattendu — constater avant geste")
                deplacer_vers(entree["id"], nom, psonde["id"], run_id,
                              entree["md5Checksum"])
            elif nom not in ds.list_folder(run_id):
                raise Refus(f"'{nom}' ni dans preuves-sonde-sys05/ ni dans "
                            "l'archive — introuvable")
            else:
                print(f"[3] {nom} déjà archivé — constaté")

        # -- 4. le verdict du recoup, déposé AVEC les pièces ---------------------
        if "VERDICT-recoup-labo-sonde-sys05-1.txt" not in \
                ds.list_folder(run_id):
            ds.upload_create(run_id, "VERDICT-recoup-labo-sonde-sys05-1.txt",
                             VERDICT_RECOUP_LOCAL)
            print("[4] VERDICT-recoup-labo-sonde-sys05-1.txt déposé (le "
                  "jugement AVEC les pièces — VERT-MESURE 31/31, LE "
                  "COUPABLE NOMMÉ : LA POSE DU WSABUF)")
        else:
            print("[4] VERDICT-recoup-labo-sonde-sys05-1.txt déjà là — "
                  "constaté")

        # -- 5. preuves-sonde-sys05/ ré-armé --------------------------------------
        restants = ds.list_folder(psonde["id"])
        if set(restants) != {"LISEZMOI-preuves.txt"}:
            raise Refus(f"preuves-sonde-sys05/ ne porte pas seulement son "
                        f"LISEZMOI après l'archivage : {sorted(restants)}")
        print("[5] preuves-sonde-sys05/ ré-armé : il ne porte que son "
              "LISEZMOI-preuves.txt (le réceptacle du prochain run)")

        # -- 6. les DEUX INDEX mis à jour -----------------------------------------
        idxp = ds.list_folder(arch_p["id"]).get(
            "LISEZMOI-archives-preuves.txt")
        if not idxp:
            raise Refus("LISEZMOI-archives-preuves.txt introuvable")
        maj_index_texte(idxp["id"], "preuves-sonde-sys05-1",
                        INDEX_PREUVES_SECTION,
                        "LISEZMOI-archives-preuves.txt (la section "
                        "preuves-sonde-sys05-1)", avant_fin=True)
        arch_l = racine.get("archives-livraisons")
        if not (arch_l or {}).get("id"):
            raise Refus("archives-livraisons/ introuvable au coffre /test")
        idxl = ds.list_folder(arch_l["id"]).get(
            "LISEZMOI-archives-livraisons.txt")
        if not idxl:
            raise Refus("LISEZMOI-archives-livraisons.txt introuvable")
        maj_index_texte(idxl["id"], "LE PREMIER RUN DE LA SONDE SYS-05",
                        INDEX_LIVRAISONS_ADDENDUM,
                        "LISEZMOI-archives-livraisons.txt (la note du run "
                        "de la sonde)")

        # -- 7. la vérification finale ----------------------------------------------
        final = ds.list_folder(TEST_ID)
        attendus = {"kit-m9f.zip", "LISEZMOI-m9f.txt", "preuves-m9f",
                    "kit-sonde-sys05.zip", "LISEZMOI-sonde-sys05.txt",
                    "preuves-sonde-sys05",
                    "archives-livraisons", "archives-preuves",
                    "preuves-m5b", "preuves-m6", "preuves-m7", "preuves-m8d",
                    "corriger-wsb.bat", "corriger-wsb.ps1",
                    "signatures-I.txt", "cle-publique-I.txt"}
        manquants = attendus - set(final)
        if manquants:
            raise Refus(f"la racine de /test ne porte pas "
                        f"{sorted(manquants)}")
        if final["kit-sonde-sys05.zip"].get("md5Checksum") != KIT_SONDE_MD5:
            raise Refus("le kit sonde de la racine a divergé — "
                        "l'ACQUITTÉ doit demeurer 215c2caa…")
        if final["kit-m9f.zip"].get("md5Checksum") != KIT_M9F_MD5:
            raise Refus("le kit m9f de la racine a divergé — "
                        "l'ACQUITTÉ doit demeurer 90a1d022…")
        dans_run = ds.list_folder(run_id)
        if set(PIECES_RUN1) - set(dans_run):
            raise Refus(f"preuves-sonde-sys05-1/ incomplet : "
                        f"{sorted(set(PIECES_RUN1) - set(dans_run))}")
        print(f"[7] la racine demeure en ordre ({len(final)} entrées, les "
              f"DEUX kits ACQUITTÉS md5 {KIT_SONDE_MD5[:8]}… + "
              f"{KIT_M9F_MD5[:8]}… INCHANGÉS — recoupés) ; "
              f"preuves-sonde-sys05-1/ porte les {len(PIECES_RUN1)} pièces "
              "(le trio DU RUN + le verdict du recoup)")
    except (Refus, ds.SyncError) as exc:
        print(f"[archivage] REFUS (fail-closed) : {exc}", file=sys.stderr)
        return 2

    print("\n=== LE PREMIER RUN DE LA SONDE EST ARCHIVÉ avec son jugement : "
          "LA MESURE RENDUE (0xC0000005), LE COUPABLE NOMMÉ (LA POSE DU "
          "WSABUF) — LE REBUILD 1.0.0-dev.3 EST LE GESTE SUIVANT, PUIS LE "
          "KIT M9F RÉPARÉ, LE RUN, LA FINALE 1.0.0 : LE JALON M9 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
